using System.Collections.Generic;
using System.IO;
using System.Linq;
using Dispo.Domain.Engine;
using Dispo.Presentation.Graybox;
using UnityEngine;

namespace Dispo.Presentation.Slice
{
    public enum DoorActor { Player, Customer, Staff }
    public enum DoorPhase { Closed, Opening, Open, Closing }

    /// <summary>One REF-012 DOORS.json row as Gameplay reads it (CONTROLS_FLOW_PS1 §7.1); missing fields take the CF§7.1 placeholders.</summary>
    public sealed class DoorRow
    {
        public sealed class Leaf { public string Object; public float? ClosedYaw; public float OpenAngle = 90; public float WidthFt = 3; }

        public string Id, Lock = "none", Hardware = "none";
        public int Leaves;             // 1 / 2 spawn; 0 (opening) and null (unknown, stored as 0) spawn nothing
        public bool Placed = true;     // false: no pos_ft (e.g. Grille_101B), skipped until its GAP closes
        public bool SelfClosing = true, ProppedOpen, Customers, Staff;
        public Vector3? AnchorA, AnchorB;   // DOORS.json anchor positions, used when the scene anchor is missing
        public readonly List<Leaf> LeafList = new List<Leaf>();

        public bool Spawns => Placed && (Leaves == 1 || Leaves == 2);

        const float Ft = 0.3048f;

        /// <summary>Parses DOORS.json; every placeholder used is added to <paramref name="placeholders"/> as "Id.field".</summary>
        public static List<DoorRow> Parse(string json, List<string> placeholders)
        {
            var rows = new List<DoorRow>();
            foreach (Dictionary<string, object> d in (List<object>)((Dictionary<string, object>)Json.Parse(json))["doors"])
            {
                object Get(string k) => d.TryGetValue(k, out var v) ? v : null;
                var r = new DoorRow { Id = (string)Get("id") };
                r.Leaves = Get("leaves") is double n ? (int)n : 0;
                r.Placed = Get("pos_ft") != null;
                rows.Add(r);
                if (!r.Spawns) continue;
                void Placeholder(string field) => placeholders?.Add($"{r.Id}.{field}");

                if (Get("lock") is string l) r.Lock = l; else Placeholder("lock");
                if (Get("hardware") is string h) r.Hardware = h; else Placeholder("hardware");
                if (Get("selfClosing") is bool sc) r.SelfClosing = sc; else Placeholder("selfClosing");   // unknown → true (GAP-CF-03)
                if (Get("defaultState") is string ds) r.ProppedOpen = ds == "proppedOpen"; else Placeholder("defaultState");
                if (Get("npcUse") is List<object> use) { r.Customers = use.Contains("customer"); r.Staff = use.Contains("staff"); }
                else Placeholder("npcUse");
                if (Get("anchors") is Dictionary<string, object> an)
                {
                    r.AnchorA = AnchorPos(an, "A");
                    r.AnchorB = AnchorPos(an, "B");
                }

                float rowWidth = Get("leafWidth_ft") is double w ? (float)w : 3f;
                var leafRows = r.Leaves == 2 && Get("leafObjects") is List<object> lo ? lo.Cast<Dictionary<string, object>>().ToList() : new List<Dictionary<string, object>> { d };
                if (r.Leaves == 2 && leafRows.Count != 2) { Placeholder("leafObjects"); leafRows = new List<Dictionary<string, object>> { d }; }
                foreach (var ld in leafRows)
                {
                    object L(string k) => ld.TryGetValue(k, out var v) ? v : null;
                    var leaf = new Leaf { Object = L("object") as string ?? $"Door_{r.Id}", WidthFt = L("leafWidth_ft") is double lw ? (float)lw : rowWidth };
                    if (L("closedRotation") is List<object> cr && cr.Count == 3) leaf.ClosedYaw = (float)(double)cr[1];   // else the hinge's scene yaw
                    if (L("openAngle") is double oa) leaf.OpenAngle = (float)oa; else Placeholder("openAngle");
                    r.LeafList.Add(leaf);
                }
            }
            return rows;
        }

        static Vector3? AnchorPos(Dictionary<string, object> anchors, string side)
            => anchors.TryGetValue(side, out var a) && a is Dictionary<string, object> ad && ad.TryGetValue("pos_ft", out var p) && p is List<object> xy
                ? new Vector3((float)(double)xy[0] * Ft, 0, -(float)(double)xy[1] * Ft) : (Vector3?)null;
    }

    /// <summary>CF§3.2 door state machine (pure, EditMode-tested): Closed → Opening → Open → Closing; locks and npcUse; propped open.</summary>
    public sealed class DoorState
    {
        public const float OpenSeconds = 0.45f;      // doorOpenSeconds [GDD]
        public const float AutoCloseDelay = 1.5f;    // doorAutoCloseDelay [GDD]

        public readonly DoorRow Row;
        public DoorPhase Phase { get; private set; }
        public float T { get; private set; }         // 0 closed .. 1 open
        public bool Propped { get; private set; }
        float _idle;

        public DoorState(DoorRow row)
        {
            Row = row;
            if (row.ProppedOpen) { Propped = true; Phase = DoorPhase.Open; T = 1; }   // DEC-103: loads open, no auto-close
        }

        /// <summary>Ease-out open fraction for the swing.</summary>
        public float Eased => 1 - (1 - T) * (1 - T);
        /// <summary>A closed leaf blocks; swinging and open leaves never do (CF§3.2 collision).</summary>
        public bool Blocks => Phase == DoorPhase.Closed;
        public bool IsOpenOrOpening => Phase == DoorPhase.Open || Phase == DoorPhase.Opening;

        /// <summary>
        /// May this actor open the door? <paramref name="entering"/> = coming from side B (outside, for the entry);
        /// <paramref name="entryLocked"/> = DEC-076 entry lock in force (never in the Quick shift). The player is staff.
        /// </summary>
        public bool Allows(DoorActor a, bool entering, bool entryLocked)
        {
            if (a == DoorActor.Customer && (!Row.Customers || Row.Lock == "staffOnly")) return false;
            if (a == DoorActor.Staff && !Row.Staff) return false;
            if (Row.Lock == "keyed") return false;   // [GDD] nobody in the slice holds a key
            if (Row.Lock == "entryTimeLock" && entryLocked && entering) return false;   // free egress: leaving always works
            return true;
        }

        public bool Open(DoorActor a, bool entering, bool entryLocked)
        {
            if (!Allows(a, entering, entryLocked)) return false;
            if (Phase == DoorPhase.Closed || Phase == DoorPhase.Closing) Phase = DoorPhase.Opening;
            _idle = 0;
            return true;
        }

        /// <summary>Close it; a propped door loses its prop, so its own selfClosing / lock apply from now on.</summary>
        public void Close()
        {
            Propped = false;
            if (IsOpenOrOpening) Phase = DoorPhase.Closing;
        }

        public bool Toggle(DoorActor a, bool entering, bool entryLocked)
        {
            if (IsOpenOrOpening) { Close(); return true; }
            return Open(a, entering, entryLocked);
        }

        /// <summary><paramref name="occupied"/>: someone is inside either trigger (holds a self-closing door open).</summary>
        public void Tick(float dt, bool occupied)
        {
            switch (Phase)
            {
                case DoorPhase.Opening:
                    T = Mathf.Min(1, T + dt / OpenSeconds);
                    if (T >= 1) { Phase = DoorPhase.Open; _idle = 0; }
                    break;
                case DoorPhase.Open:
                    if (Propped || !Row.SelfClosing) break;
                    _idle = occupied ? 0 : _idle + dt;
                    if (_idle >= AutoCloseDelay) Phase = DoorPhase.Closing;
                    break;
                case DoorPhase.Closing:
                    T = Mathf.Max(0, T - dt / OpenSeconds);
                    if (T <= 0) Phase = DoorPhase.Closed;
                    break;
            }
        }
    }

    /// <summary>
    /// GAME-025 door runtime (CF§3.2, §7.1): finds World's Door_&lt;Id&gt; leaves and their _Hinge pivots by name, builds a trigger box
    /// around each Anchor_Door_&lt;Id&gt;_A/_B, swings the leaves (kinematic) and toggles their colliders. No door geometry is made here.
    /// </summary>
    public sealed class SliceDoor : MonoBehaviour   // one per slice, runs every door (file name = class for Unity)
    {
        public const float TriggerDepth = 1.2f;       // [GDD] trigger volume ≈ 1.2 m × leaf width
        public const float PromptSeconds = 1.5f;      // [GDD] "Locked" / "Staff only" prompt time
        const float Ft = 0.3048f;

        public sealed class Door
        {
            public DoorState State;
            public Transform[] Hinges;
            public float[] ClosedYaw, OpenAngle;
            public Collider[] Colliders;
            public Vector3 A, B;
            public float HalfWidth;
            public Vector3 Normal => Flat(B - A).normalized;
            public Vector3 Mid => (A + B) / 2;
        }

        public GrayboxTestPlayer Player;
        public System.Func<bool> Paused = () => false;
        /// <summary>DEC-076 entry lock; the slice is a Quick shift, so it never locks (CF§3.2).</summary>
        public System.Func<bool> EntryLocked = () => false;
        public System.Func<IEnumerable<(Vector3 pos, DoorActor who)>> Npcs = () => Enumerable.Empty<(Vector3, DoorActor)>();
        public readonly List<Door> Doors = new List<Door>();

        string _prompt = "";
        float _promptUntil;
        public string Prompt => Time.unscaledTime < _promptUntil ? _prompt : "";

        /// <summary>DOORS.json: the assigned TextAsset, else the repo's Docs/Reference copy (Editor and dev machines).</summary>
        public static string LoadJson(TextAsset asset)
        {
            if (asset) return asset.text;
            var path = Path.GetFullPath(Path.Combine(Application.dataPath, "../../Docs/Reference/DOORS.json"));
            return File.Exists(path) ? File.ReadAllText(path) : null;
        }

        /// <summary>Wires every spawnable row whose leaves exist in the scene; logs one line for missing doors and placeholders.</summary>
        public int Build(IEnumerable<DoorRow> rows, ICollection<string> placeholders = null)
        {
            var fallbacks = new List<string>();
            foreach (var r in rows.Where(r => r.Spawns))
            {
                var leaves = r.LeafList.Select(l => GameObject.Find(l.Object)).ToArray();
                if (leaves.Any(l => !l)) continue;   // World has not placed this door yet
                var hinges = r.LeafList.Select((l, i) => GameObject.Find(l.Object + "_Hinge")?.transform ?? leaves[i].transform.parent).ToArray();
                if (hinges.Any(h => !h)) { Debug.LogWarning($"[Slice] door {r.Id}: no _Hinge pivot, skipped"); continue; }
                var d = new Door
                {
                    State = new DoorState(r),
                    Hinges = hinges,
                    ClosedYaw = r.LeafList.Select((l, i) => l.ClosedYaw ?? hinges[i].eulerAngles.y).ToArray(),
                    OpenAngle = r.LeafList.Select(l => l.OpenAngle).ToArray(),
                    Colliders = leaves.SelectMany(Colliders).ToArray(),
                    A = AnchorPos($"Anchor_Door_{r.Id}_A", r.AnchorA, hinges[0], -1, fallbacks),
                    B = AnchorPos($"Anchor_Door_{r.Id}_B", r.AnchorB, hinges[0], 1, fallbacks),
                    HalfWidth = r.LeafList.Sum(l => l.WidthFt) * Ft / 2,
                };
                Doors.Add(d);
                Pose(d);
            }
            if (Doors.Count == 0) Debug.Log("[Slice] doors: none found");
            else Debug.Log($"[Slice] doors: {Doors.Count} ({string.Join(", ", Doors.Select(x => x.State.Row.Id))})");
            if (fallbacks.Count > 0) Debug.LogWarning($"[Slice] door anchors from DOORS.json positions: {string.Join(", ", fallbacks)}");
            if (placeholders != null && placeholders.Count > 0) Debug.LogWarning($"[Slice] DOORS.json placeholders (CF§7.1): {string.Join(", ", placeholders)}");
            return Doors.Count;
        }

        static IEnumerable<Collider> Colliders(GameObject leaf)
        {
            var c = leaf.GetComponentsInChildren<Collider>();
            return c.Length > 0 ? c : new Collider[] { leaf.AddComponent<BoxCollider>() };   // a closed leaf blocks (CF§3.2)
        }

        static Vector3 AnchorPos(string name, Vector3? fromJson, Transform hinge, int side, List<string> fallbacks)
        {
            var go = GameObject.Find(name);
            if (go) return go.transform.position;
            fallbacks.Add(name);
            // shortcut: no anchor and no JSON position → 0.6 m either side of the hinge along its local Z; upgrade when World places anchors.
            return fromJson ?? hinge.position + hinge.forward * (0.6f * side);
        }

        void Update()
        {
            if (Paused()) return;   // pause freezes door animation (SPEC_SHIFT_DAY §7)
            bool locked = EntryLocked();
            Vector3 pp = Player ? Player.transform.position : default, pv = Player && Player.TryGetComponent<CharacterController>(out var cc) ? cc.velocity : default;
            var npcs = Npcs().ToList();
            foreach (var d in Doors)
            {
                bool occupied = false;
                if (Player)
                {
                    bool inA = InTrigger(d, d.A, pp), inB = InTrigger(d, d.B, pp);
                    occupied = inA || inB;
                    // Walk-through: in a trigger and moving toward the door (velocity · door direction > 0). No key press.
                    if (occupied && !d.State.IsOpenOrOpening && Vector3.Dot(Flat(pv), Flat(d.Mid - pp)) > 0.01f) TryOpen(d, DoorActor.Player, inB, locked);
                }
                foreach (var (pos, who) in npcs)
                {
                    bool inA = InTrigger(d, d.A, pos), inB = InTrigger(d, d.B, pos);
                    if (!inA && !inB) continue;
                    occupied = true;
                    if (!d.State.IsOpenOrOpening) d.State.Open(who, inB, locked);
                }
                d.State.Tick(Time.deltaTime, occupied);
                Pose(d);
            }
        }

        void TryOpen(Door d, DoorActor who, bool entering, bool locked)
        {
            bool ok = d.State.Open(who, entering, locked);
            if (!ok) Say("Locked");
            else if (d.State.Row.Lock == "staffOnly") Say("Staff only");
        }

        /// <summary>E: toggle the door whose trigger the player stands in (lowest E priority, CF§3.3). False when none is in reach.</summary>
        public bool ToggleInReach()
        {
            if (!Player) return false;
            var p = Player.transform.position;
            var d = Doors.Where(x => InTrigger(x, x.A, p) || InTrigger(x, x.B, p)).OrderBy(x => Flat(x.Mid - p).sqrMagnitude).FirstOrDefault();
            if (d == null) return false;
            if (d.State.IsOpenOrOpening) d.State.Close();
            else TryOpen(d, DoorActor.Player, InTrigger(d, d.B, p), EntryLocked());
            return true;
        }

        void Say(string text) { _prompt = text; _promptUntil = Time.unscaledTime + PromptSeconds; }

        /// <summary>Trigger box centred on an anchor: TriggerDepth along the door normal × the opening width along the wall.</summary>
        public static bool InTrigger(Door d, Vector3 anchor, Vector3 p)
        {
            var n = d.Normal;
            var off = Flat(p - anchor);
            return Mathf.Abs(Vector3.Dot(off, n)) <= TriggerDepth / 2 && Mathf.Abs(Vector3.Dot(off, Vector3.Cross(Vector3.up, n))) <= d.HalfWidth;
        }

        static void Pose(Door d)
        {
            for (int i = 0; i < d.Hinges.Length; i++)
                d.Hinges[i].rotation = Quaternion.Euler(0, d.ClosedYaw[i] + d.OpenAngle[i] * d.State.Eased, 0);
            foreach (var c in d.Colliders) c.enabled = d.State.Blocks;
        }

        static Vector3 Flat(Vector3 v) => new Vector3(v.x, 0, v.z);
    }
}
