using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using Dispo.Domain.Engine;
using Dispo.Presentation.Graybox;
using Dispo.Simulation.Slice;
using UnityEngine;
using UnityEngine.InputSystem;
using UnityEngine.UIElements;

namespace Dispo.Presentation.Slice
{
    public enum SliceScreen { World, Dialogue, Query, Results, Detail, Pos, Report }

    /// <summary>
    /// Lives in Gameplay_Slice.unity (DEC-029). Runs one shift (SLICE_DESIGN): finds ART anchors by name (TEMP_ fallbacks when
    /// missing), spawns jars and NPC capsules, ticks the ShiftSim and drives the terminal/POS flow. The public flow methods are
    /// what the UI buttons call, and what the PlayMode bot calls.
    /// </summary>
    public sealed class SliceGame : MonoBehaviour
    {
        [Header("Data")]
        public TextAsset Batches, Terpenes, EngineTables, PricingJson, Manifest, Config, Intents, Lines;
        [Header("Presentation")]
        public UIDocument Document;
        public StyleSheet Style;
        public Material JarShell, Npc, Bag;
        [Header("Jars (GAME-005)")]
        public GameObject JarModel;          // PROC_DeliJar.fbx
        public GameObject[] FillModels;      // PROC_JarFill_<Look>.fbx, one per bud look
        public Material JarGlass, LabelText;

        public ShiftSim Sim { get; private set; }
        public SliceScreen Screen { get; private set; } = SliceScreen.World;
        public ShiftReport FinalReport { get; private set; }
        public readonly List<string> FallbackAnchors = new List<string>();
        public bool AutoFillIntent;        // UX assist, off by default (SLICE_DESIGN §10 #2)
        public float InteractReach = 3f;

        const float Ft = 0.3048f;
        SliceView _view;
        GrayboxTestPlayer _player;
        Transform _terminal, _spawn, _exit, _service, _servicePlayer;
        Transform[] _slots;
        readonly Dictionary<string, Renderer[]> _jarFill = new Dictionary<string, Renderer[]>();
        readonly Dictionary<string, Vector3> _jarTop = new Dictionary<string, Vector3>();
        readonly Dictionary<Customer, GameObject> _npcs = new Dictionary<Customer, GameObject>();
        MaterialPropertyBlock _mpb;  // Unity forbids creating it in a field initializer
        Material _label;
        static readonly Regex FillStepName = new Regex(@"_F(\d+)_");
        // [GDD] placeholder: each brand has its own band colour (DEC-043) but none are recorded, so brands hash into generic hues.
        static readonly Color[] BandPalette =
        {
            new Color(0.12f, 0.45f, 0.20f), new Color(0.15f, 0.30f, 0.65f), new Color(0.70f, 0.15f, 0.15f), new Color(0.85f, 0.55f, 0.10f),
            new Color(0.45f, 0.20f, 0.55f), new Color(0.10f, 0.55f, 0.55f), new Color(0.15f, 0.15f, 0.15f), new Color(0.80f, 0.35f, 0.55f),
        };
        Card _detail;
        double _posGrams;
        float _hold;
        bool _holding;
        string _lastReject;
        System.DateTime _snapshot;

        // ---------------- setup ----------------

        void Start()
        {
            _mpb = new MaterialPropertyBlock();
            var data = SliceData.Load(Batches.text, Terpenes.text, EngineTables.text, PricingJson.text, Config.text, Intents.text, Lines.text);
            Sim = new ShiftSim(data);
            Sim.Left += OnLeft;
            Sim.Inventory.Sold += OnSold;
            _snapshot = System.DateTime.Parse((string)((Dictionary<string, object>)((List<object>)((Dictionary<string, object>)Json.Parse(Manifest.text))["sources"])[1])["invExported"]).Date;

            FindAnchors();
            SpawnJars();
            _player = FindAnyObjectByType<GrayboxTestPlayer>();
            if (_player) PlacePlayer();

            _view = new SliceView(Document.rootVisualElement, Style, this);
            if (FallbackAnchors.Count > 0) Debug.LogWarning($"[Slice] TEMP fallback anchors (ART-002 pending): {string.Join(", ", FallbackAnchors)}");
            Debug.Log($"[Slice] shift ready: {Sim.Customers.Count} customers, {Sim.Inventory.JarBatchIds.Count} jars, seed {Sim.Cfg.seed}");
        }

        Transform Anchor(string name, float xFt, float yFt, float hFt)
        {
            var go = GameObject.Find(name);
            if (go) return go.transform;
            FallbackAnchors.Add(name);
            var t = new GameObject("TEMP_" + name).transform;
            t.SetParent(transform, false);
            t.position = new Vector3(xFt * Ft, hFt * Ft, -yFt * Ft);
            return t;
        }

        /// <summary>SLICE_DESIGN §7 names. Fallback spots: REF-001 plan feet (registers x 20-42 / y 7-9.2, lane x 6-9, entry x 0 / y 11-20).</summary>
        void FindAnchors()
        {
            _spawn = Anchor("Anchor_CustomerSpawn", 2.0f, 16.5f, 0);
            _exit = Anchor("Anchor_CustomerExit", 0.6f, 12.5f, 0);
            _slots = Enumerable.Range(0, Sim.Cfg.queueSlots).Select(i => Anchor($"Anchor_QueueSlot_{i}", 7.5f, 11.8f + 2f * i, 0)).ToArray();
            _service = Anchor("Anchor_ServiceCustomer", 30f, 10.4f, 0);
            _servicePlayer = Anchor("Anchor_ServicePlayer", 30f, 5.6f, 0);
            _terminal = Anchor("Interact_Terminal", 30f, 7.6f, 3.6f);
            Anchor("Interact_Scale", 32f, 6.2f, 3.6f);
            foreach (var n in new[] { "Interact_Terminal", "Interact_Scale" })
                if (FallbackAnchors.Contains(n)) Prop(transform.Find("TEMP_" + n), PrimitiveType.Cube, new Vector3(0.35f, 0.25f, 0.06f), JarShell);
        }

        static GameObject Prop(Transform parent, PrimitiveType type, Vector3 scale, Material m)
        {
            var go = GameObject.CreatePrimitive(type);
            Destroy(go.GetComponent<Collider>());
            go.transform.SetParent(parent, false);
            go.transform.localScale = scale;
            if (m) go.GetComponent<Renderer>().sharedMaterial = m;
            return go;
        }

        void SpawnJars()
        {
            var batches = Sim.Data.Catalog.Batches.ToDictionary(b => b.Id);
            var font = Resources.GetBuiltinResource<Font>("LegacyRuntime.ttf");
            _label = new Material(LabelText);
            var ids = Sim.Inventory.JarBatchIds;
            for (int i = 0; i < ids.Count; i++)
            {
                // Fallback layout: north jar wall front (x 19.5-44.5, 3 shelves), then the east wall (x 45.45, y 2-14).
                int row = i / 26, col = i % 26, e = i - 78;
                var slot = i < 78 ? Anchor($"Anchor_JarSlot_{i:000}", 19.5f + col, 1.6f, 3f + row)
                                  : Anchor($"Anchor_JarSlot_{i:000}", 45.4f, 2f + e % 13, 3f + e / 13);
                // The canister's label face is +Z; ART's slot anchors face into the room.
                var jar = Instantiate(JarModel, slot, false).transform;
                jar.name = $"Jar_{ids[i]}";
                var b = batches[ids[i]];
                _mpb.Clear();
                _mpb.SetColor("_BaseColor", BandPalette[Hash(b.Brand) % BandPalette.Length]);
                foreach (var r in jar.GetComponentsInChildren<Renderer>())
                {
                    if (r.name.Contains("_Glass_")) r.sharedMaterial = JarGlass;
                    if (r.name.Contains("_Band_")) r.SetPropertyBlock(_mpb);
                }
                float top = jar.GetComponentsInChildren<Renderer>().Max(r => r.bounds.max.y);
                // Look per batch: [GDD] placeholder until art data exists (PROC-002 handoff); no per-strain looks invented.
                _jarFill[ids[i]] = Instantiate(FillModels[Hash(ids[i]) % FillModels.Length], jar, false).GetComponentsInChildren<Renderer>();
                JarLabel(jar, $"{Wrap(b.StrainName, 14)}\n{b.Brand}", font);
                _jarTop[ids[i]] = new Vector3(jar.position.x, top + 0.05f, jar.position.z);
                SetFill(ids[i]);
            }
            _label.SetTexture("_UnlitColorMap", font.material.mainTexture);
            Font.textureRebuilt += OnFontRebuilt;
        }

        void OnFontRebuilt(Font f) { if (_label && f.material) _label.SetTexture("_UnlitColorMap", f.material.mainTexture); }
        void OnDestroy() => Font.textureRebuilt -= OnFontRebuilt;

        /// <summary>Generic text on the front label card (strain + brand from batches.json, no logos). The THC % tag stays blank: no THC data.</summary>
        void JarLabel(Transform jar, string text, Font font)
        {
            // Text box inside the PROC_DeliJar label card (deli_jar.json label: 0.10 x 0.08 m from 0.065 m), below the THC tag.
            const float faceZ = 0.0765f, centreY = 0.092f, maxW = 0.088f, maxH = 0.042f;
            var tm = new GameObject("Label_Text").AddComponent<TextMesh>();
            tm.transform.SetParent(jar, false);
            tm.transform.SetLocalPositionAndRotation(new Vector3(0, centreY, faceZ), Quaternion.Euler(0, 180, 0)); // TextMesh reads from -Z
            tm.font = font;
            tm.fontSize = 48;
            tm.anchor = TextAnchor.MiddleCenter;
            tm.alignment = TextAlignment.Center;
            tm.color = Color.black;
            tm.text = text;
            tm.GetComponent<MeshRenderer>().sharedMaterial = _label;
            var size = tm.GetComponent<MeshRenderer>().localBounds.size;
            tm.characterSize = size.x > 0 && size.y > 0 ? Mathf.Min(maxW / size.x, maxH / size.y) : 0.0015f;
        }

        static string Wrap(string s, int width)
        {
            var lines = new List<string> { "" };
            foreach (var w in s.Split(' '))
                if (lines[lines.Count - 1].Length == 0) lines[lines.Count - 1] = w;
                else if (lines[lines.Count - 1].Length + 1 + w.Length <= width) lines[lines.Count - 1] += " " + w;
                else lines.Add(w);
            return string.Join("\n", lines);
        }

        /// <summary>Stable FNV-1a (string.GetHashCode is salted per run).</summary>
        static int Hash(string s)
        {
            uint h = 2166136261;
            foreach (var c in s ?? "") h = (h ^ c) * 16777619;
            return (int)(h & 0x7fffffff);
        }

        /// <summary>GAME-005: show the one PROC-002 fill step for grams / startGrams (JarFillStep); the steps come from the mesh names.</summary>
        void SetFill(string id)
        {
            var rs = _jarFill[id];
            int step = JarFillStep.For(Sim.Inventory.Fill(id), rs.Select(StepOf).Distinct(), Sim.Cfg.jarMinVisibleStepPct);
            foreach (var r in rs) r.enabled = StepOf(r) == step;
        }

        static int StepOf(Renderer r) => int.Parse(FillStepName.Match(r.name).Groups[1].Value);

        /// <summary>The fill step the jar's enabled renderers show, as a fraction (0 = SOLD OUT crumbs). Throws if two steps are on.</summary>
        public float JarFillShown(string id) => _jarFill[id].Where(r => r.enabled).Select(StepOf).Distinct().DefaultIfEmpty(-1).Single() / 100f;
        public int[] JarFillSteps(string id) => _jarFill[id].Select(StepOf).Distinct().OrderBy(s => s).ToArray();
        public IEnumerable<KeyValuePair<string, Vector3>> JarTops => _jarTop;

        void PlacePlayer()
        {
            var cc = _player.GetComponent<CharacterController>();
            cc.enabled = false;
            _player.transform.SetPositionAndRotation(_servicePlayer.position, Quaternion.LookRotation(Vector3.ProjectOnPlane(_service.position - _servicePlayer.position, Vector3.up)));
            cc.enabled = true;
        }

        // ---------------- loop ----------------

        void Update()
        {
            if (Sim == null) return;
            if (!Sim.IsOver) Sim.Tick(Time.deltaTime);
            else if (FinalReport == null) { FinalReport = Sim.Report(); Show(SliceScreen.Report); }

            MoveNpcs();
            HandleInput();
            if (_holding)
            {
                _hold += Time.unscaledDeltaTime;
                if (_hold >= Sim.Cfg.holdConfirmSeconds) { _holding = false; _hold = 0; PosConfirm(); }
            }
            if (_player) _player.ScriptedWorldMove = Screen == SliceScreen.World ? (Vector3?)null : Vector3.zero;
            _view.Tick();
        }

        void HandleInput()
        {
            var kb = Keyboard.current;
            if (kb == null) return;
            if (kb.eKey.wasPressedThisFrame && Screen == SliceScreen.World && CanTalk) Talk();
            if (kb.escapeKey.wasPressedThisFrame) Back();
            if (kb.mKey.wasPressedThisFrame && Screen == SliceScreen.Results) More();
            if (kb.f3Key.wasPressedThisFrame) _view.ToggleDebug();
        }

        public SliceView View => _view;
        public Camera ViewCamera => _player && _player.Eye ? _player.Eye.GetComponent<Camera>() : Camera.main;
        public bool PlayerInReach => !_player || Vector3.Distance(_player.transform.position, _terminal.position) <= InteractReach;
        public bool CustomerAtCounter => Sim.Serving != null && _npcs.TryGetValue(Sim.Serving, out var go) && Flat(go.transform.position - _service.position) < 0.3f;
        public bool CanTalk => CustomerAtCounter && PlayerInReach;

        void MoveNpcs()
        {
            float step = (float)Sim.Cfg.npcWalkSpeed * Time.deltaTime;
            foreach (var c in Sim.Customers)
            {
                if (c.State == CustomerState.NotArrived) continue;
                if (!_npcs.TryGetValue(c, out var go))
                {
                    if (c.State == CustomerState.Done) continue;
                    go = _npcs[c] = SpawnNpc(c);
                }
                if (!go) continue;
                int qi = Sim.Queue.IndexOf(c);
                var target = c.State == CustomerState.Serving ? _service.position
                    : c.State == CustomerState.Done ? _exit.position
                    : qi >= 0 && qi < _slots.Length ? _slots[qi].position : _spawn.position;
                var p = go.transform.position;
                var flat = new Vector3(target.x, p.y, target.z);
                go.transform.position = Vector3.MoveTowards(p, flat, step);
                if (c.State == CustomerState.Done && Flat(go.transform.position - _exit.position) < 0.05f) { Destroy(go); _npcs[c] = null; continue; }

                // Patience is body language (UX §1.4): impatient customers turn orange.
                var tint = c.PatienceStateOf(Sim.Cfg.impatientFraction) == PatienceState.Calm ? new Color(0.55f, 0.6f, 0.7f) : new Color(0.9f, 0.55f, 0.2f);
                _mpb.SetColor("_BaseColor", tint);
                go.GetComponent<Renderer>().SetPropertyBlock(_mpb);
            }
        }

        GameObject SpawnNpc(Customer c)
        {
            var go = GameObject.CreatePrimitive(PrimitiveType.Capsule);
            Destroy(go.GetComponent<Collider>());
            go.name = $"NPC_Customer_{c.Index:00}";
            go.transform.SetParent(transform, false);
            go.transform.position = _spawn.position + Vector3.up;
            go.transform.localScale = new Vector3(0.5f, 0.85f, 0.5f);
            if (Npc) go.GetComponent<Renderer>().sharedMaterial = Npc;
            return go;
        }

        static float Flat(Vector3 v) => new Vector2(v.x, v.z).magnitude;

        // ---------------- flow (UI buttons and the PlayMode bot call these) ----------------

        public void Talk()
        {
            if (Sim.Serving == null) return;
            Show(SliceScreen.Dialogue);
        }

        /// <summary>Dialogue "Look it up": Results again with the same chip after a REJECT, else Query.</summary>
        public void LookItUp()
        {
            if (Sim.Serving == null) return;
            if (Sim.Results != null) Show(SliceScreen.Results);
            else if (AutoFillIntent) ChooseChip(Sim.Serving.TrueFamily, true);
            else Show(SliceScreen.Query);
        }

        public void EditSearch() => Show(SliceScreen.Query);

        public void ChooseChip(IntentFamily f, bool autoFilled = false)
        {
            Sim.Search(f, autoFilled);
            _view.Message = "";
            Show(SliceScreen.Results);
        }

        public void More() { if (Sim.Results != null && Sim.Results.MoreAvailable) { Sim.MoreOptions(); Show(SliceScreen.Results); } }

        public void Inspect(Card card) { _detail = card; Show(SliceScreen.Detail); }
        public Card DetailCard => _detail;

        /// <summary>Choose a card: present it to the customer (§3.1 steps 5-7).</summary>
        public PresentResult Choose(Card card)
        {
            var c = Sim.Serving;
            var r = Sim.Present(card);
            switch (r.Response)
            {
                case Response.Blocked: _view.Message = r.Line; Show(SliceScreen.Results); break;
                case Response.Accept: _posGrams = c.Grams; _view.Message = ""; Show(SliceScreen.Pos); break;
                case Response.Reject:
                    _lastReject = r.Line;
                    _view.Toast(Sim.Data.Lines.toastReject, r.Line, true);
                    Show(SliceScreen.Dialogue);
                    break;
                case Response.Leave: Show(SliceScreen.World); break; // OnLeft toasts
            }
            return r;
        }

        public string LastReject => _lastReject;
        public double PosGrams => _posGrams;

        public void PosSelectWeight(double g) { _posGrams = g; _view.Message = ""; Show(SliceScreen.Pos); }

        public void PosHold(bool down) { _holding = down && Screen == SliceScreen.Pos; if (!down) _hold = 0; }
        public float HoldProgress => _holding ? Mathf.Clamp01(_hold / (float)Sim.Cfg.holdConfirmSeconds) : 0;

        /// <summary>POS Confirm (after the hold). Blocked → message; sale → toast via OnSold.</summary>
        public string PosConfirm()
        {
            if (Screen != SliceScreen.Pos || Sim.Pending == null) return "no open sale";
            var blocked = Sim.Confirm(_posGrams);
            if (blocked == Sim.Data.Lines.overLimit) _view.Toast("⚠ " + blocked, "", true);
            if (blocked != null) { _view.Message = blocked; Show(SliceScreen.Pos); return blocked; }
            Show(SliceScreen.World);
            return null;
        }

        public void PosCancel() { Sim.Cancel(); _view.Message = ""; Show(SliceScreen.Results); }

        /// <summary>Esc / Back: one screen back.</summary>
        public void Back()
        {
            switch (Screen)
            {
                case SliceScreen.Dialogue: case SliceScreen.Query: case SliceScreen.Results: Show(SliceScreen.World); break;
                case SliceScreen.Detail: Show(SliceScreen.Results); break;
                case SliceScreen.Pos: PosCancel(); break;
            }
        }

        void Show(SliceScreen s)
        {
            if (s != SliceScreen.Report && Sim.Serving == null && s != SliceScreen.World) s = SliceScreen.World;
            if (FinalReport != null) s = SliceScreen.Report;
            Screen = s;
            _view?.Render();
            UnityEngine.Cursor.lockState = CursorLockMode.None;
            UnityEngine.Cursor.visible = true;
        }

        void OnSold(SaleEvent e)
        {
            var l = Sim.Data.Lines;
            _view.Toast(string.Format(l.toastSale, e.StrainName, l.Weight(e.Grams)),
                string.Format(l.toastSaleDetail, e.PricePostTax.ToString("0.00"), e.GramsBefore.ToString("0.#"), e.GramsAfter.ToString("0.#")), false);
            SetFill(e.BatchId);
            if (_npcs.TryGetValue(Sim.Customers[e.CustomerIndex - 1], out var npc) && npc)
                Prop(npc.transform, PrimitiveType.Cube, new Vector3(0.45f, 0.25f, 0.3f), Bag).transform.localPosition = new Vector3(0.6f, -0.2f, 0);
        }

        void OnLeft(Customer c)
        {
            var l = Sim.Data.Lines;
            if (c.Outcome == CustomerOutcome.Walkout) _view?.Toast(l.toastWalkout, "", true);
            if (c.Outcome == CustomerOutcome.NoSale) _view?.Toast(l.toastLeave, _lastReject ?? "", true);
            if (Screen != SliceScreen.World && Sim.Serving == null) Show(SliceScreen.World);
        }

        /// <summary>Batch age in whole weeks from the COA date to the catalog snapshot date (deterministic, §10).</summary>
        public int AgeWeeks(Batch b) => b.TestDate.HasValue ? (int)((_snapshot - b.TestDate.Value).TotalDays / 7) : -1;
    }
}
