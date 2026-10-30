using System;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.HighDefinition;
using G = Dispo.Editor.Graybox.GrayboxBuilder;
using L = Dispo.Editor.Graybox.GrayboxLayout;

namespace Dispo.Editor.Lookdev
{
    /// <summary>
    /// ART-003: builds the additive Retail_Lookdev scene (TI finishes, millwork, neon, lights) from retail_lookdev.json on top
    /// of the generated Retail graybox (DEC-029). Graybox fixtures are looked up by id in graybox_layout.json, never by fileID.
    /// Runs after the graybox in Dispo.Editor.Graybox.GrayboxBuilder.Build (studio.ps1 unity-graybox); same stamp/skip rule.
    /// </summary>
    public static class LookdevBuilder
    {
        public const string SceneName = "Retail_Lookdev";
        public const string RootName = "Lookdev_Retail";
        public const string DataPath = "Assets/_Game/Art/Lookdev/retail_lookdev.json";
        const string ScenePath = G.ScenesDir + "/" + SceneName + ".unity";
        const string LookdevDir = "Assets/_Game/Art/Lookdev";
        const string TexDir = LookdevDir + "/Textures";
        const string WalnutDir = "Assets/_Game/Art/ThirdParty/PolyHaven/oak_veneer_05";
        const string StampPrefix = "_BuildStamp ";
        static readonly string[] HashedSources = { DataPath, L.DataPath, "Assets/_Game/Code/Editor/Lookdev/LookdevBuilder.cs" };

        [Serializable] sealed class Data
        {
            public string room;
            public float interiorEv, skyAmbient;
            public Ceiling ceiling;
            public Soffit soffit;
            public Panels panels;
            public Floor[] floors;
            public Millwork millwork;
            public Neon neon;
            public Downlights downlights;
            public Pendants pendants;
        }
        [Serializable] sealed class Ceiling { public string key, conf; public float t; }
        [Serializable] sealed class Soffit { public string key, conf, gap; public float depth; public string[] walls; }
        [Serializable] sealed class Panels { public float w, d, t, bottomFt, cable, x0, y0, pitchX, pitchY; public int nx, ny; public string conf, gap; }
        [Serializable] sealed class Floor { public string id, mat, conf; public float t; public L.Rect rect; }
        [Serializable] sealed class Millwork { public string[] fixtures; public string key, conf; public float toe, top, overhang; }
        [Serializable] sealed class Neon { public string text, wall, conf, gap; public float faceX, y0, y1, bottomFt, heightFt, nits; }
        [Serializable] sealed class Downlights { public float x0, x1, y0, y1, pitch, lumens, angle, kelvin; public string conf, gap; }
        [Serializable] sealed class Pendants { public string[] fixtures; public float lumens, kelvin, range; public string conf; }

        [MenuItem("Dispo/Lookdev/Rebuild Retail Lookdev")]
        public static void BuildMenu() => Debug.Log($"[Lookdev] {BuildAll(force: true)}");

        public static string BuildAll(bool force = false)
        {
            var d = JsonUtility.FromJson<Data>(File.ReadAllText(DataPath)) ?? throw new InvalidDataException($"{DataPath}: empty");
            var layout = L.Load();
            var stamp = StampPrefix + Hash128.Compute(string.Concat(HashedSources.Select(p => File.ReadAllText(p).Replace("\r", "")))).ToString();
            EnsureInBuildSettings();

            var scene = File.Exists(ScenePath)
                ? EditorSceneManager.OpenScene(ScenePath, OpenSceneMode.Single)
                : EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            var olds = scene.GetRootGameObjects().Where(g => g.name == RootName).ToList();
            if (!force && olds.Count == 1 && olds[0].transform.Find(stamp)) return "lookdev unchanged";
            foreach (var old in olds) UnityEngine.Object.DestroyImmediate(old);

            var room = layout.rooms.First(r => r.id == d.room).r;
            var m = Materials(d);
            var root = new GameObject(RootName).transform;
            G.Child(root, stamp);

            // Ceiling and soffits
            var ceilFt = layout.H(d.ceiling.key).ft;
            var ceil = G.Child(root, "Ceiling");
            G.Box(ceil, $"CLG_Gypsum_PT1 [h={ceilFt}ft DEC-037] [conf {d.ceiling.conf}]", room, ceilFt, d.ceiling.t, m.pt1, false);
            var soffitFt = layout.H(d.soffit.key).ft;
            foreach (var w in d.soffit.walls)
                G.Box(ceil, $"Soffit_{w} [h={soffitFt}ft DEC-037] [extent {d.soffit.gap}, conf {d.soffit.conf}]", SoffitRect(room, w, d.soffit.depth), soffitFt, ceilFt - soffitFt, m.pt1, false);

            // CLG-1 walnut panels on stainless cables
            var p = d.panels;
            var panels = G.Child(root, "AccentPanels_CLG1");
            for (var j = 0; j < p.ny; j++)
                for (var i = 0; i < p.nx; i++)
                {
                    var r = new L.Rect { x0 = p.x0 + i * p.pitchX, y0 = p.y0 + j * p.pitchY };
                    r.x1 = r.x0 + p.w;
                    r.y1 = r.y0 + p.d;
                    var name = $"CLG1_Panel_{j}_{i} [4x8 walnut, drop+grid {p.gap}, conf {p.conf}]";
                    G.Box(panels, name, r, p.bottomFt, p.t, m.walnut, false);
                    foreach (var (cx, cy) in new[] { (r.x0 + 0.5f, r.y0 + 0.5f), (r.x1 - 0.5f, r.y0 + 0.5f), (r.x0 + 0.5f, r.y1 - 0.5f), (r.x1 - 0.5f, r.y1 - 0.5f) })
                        G.Box(panels, $"{name} cable", Square(cx, cy, p.cable), p.bottomFt + p.t, ceilFt - p.bottomFt - p.t, m.steel, false);
                }

            // Floor tile overlays (no colliders: the graybox floor carries them)
            var floors = G.Child(root, "Floor");
            foreach (var f in d.floors) G.Box(floors, $"{f.id} [conf {f.conf}]", f.rect, 0, f.t, f.mat == "tl2" ? m.tl2 : m.tl1, false);

            // Counter millwork over the graybox counters: black toe, walnut body, quartz top (34" AFF)
            var mw = d.millwork;
            var topFt = layout.H(mw.key).ft;
            var mill = G.Child(root, "Millwork");
            const float skin = 0.01f; // just outside the graybox counter box so the two never z-fight
            foreach (var id in mw.fixtures)
            {
                var fx = layout.fixtures.FirstOrDefault(f => f.id == id) ?? throw new InvalidDataException($"{DataPath}: graybox fixture {id} not found");
                for (var i = 0; i < fx.rects.Length; i++)
                {
                    var r = Grow(fx.rects[i], skin);
                    var name = $"MW_{id.Replace("FX_", "")}_part{i} [top {topFt}ft DEC-037] [conf {mw.conf}]";
                    G.Box(mill, $"{name} toe ML-1", r, 0, mw.toe, m.black, false);
                    G.Box(mill, $"{name} body WD-1", r, mw.toe, topFt - mw.top - mw.toe, m.walnut, false);
                    G.Box(mill, $"{name} top QZ-2", Grow(fx.rects[i], mw.overhang), topFt - mw.top + skin, mw.top, m.quartz, false);
                }
            }

            // Neon (W wall faces east)
            var n = d.neon;
            var neon = GameObject.CreatePrimitive(PrimitiveType.Quad);
            neon.name = $"Neon_{n.text.Replace(" ", "")} [bottom {n.bottomFt}ft TI A901] [wall+size {n.gap}, conf {n.conf}]";
            neon.transform.SetParent(root, false);
            UnityEngine.Object.DestroyImmediate(neon.GetComponent<MeshCollider>());
            neon.transform.position = L.ToWorld(n.faceX, (n.y0 + n.y1) / 2, n.bottomFt + n.heightFt / 2);
            neon.transform.rotation = Quaternion.Euler(0, -90, 0); // quad normal (-Z) -> +X, text reads left-to-right from inside the room
            neon.transform.localScale = new Vector3(n.y1 - n.y0, n.heightFt, 1) * L.Ft;
            neon.GetComponent<MeshRenderer>().sharedMaterial = m.neon;

            // Lights (3500 K, physical units, no shadows)
            var lights = G.Child(root, "Lights");
            var dl = d.downlights;
            int k = 0;
            for (var y = dl.y0; y <= dl.y1 + 0.001f; y += dl.pitch)
                for (var x = dl.x0; x <= dl.x1 + 0.001f; x += dl.pitch)
                {
                    if (UnderPanel(p, x, y)) continue;
                    var inSoffit = d.soffit.walls.Any(w => Inside(SoffitRect(room, w, d.soffit.depth), x, y));
                    var h = (inSoffit ? soffitFt : ceilFt) - 0.05f;
                    Lamp(lights, $"L4_Downlight_{k++:00} [type TI §6.7] [grid {dl.gap}, conf {dl.conf}]", LightType.Spot, L.ToWorld(x, y, h), dl.lumens, dl.kelvin, dl.angle, 0);
                }
            var pd = d.pendants;
            foreach (var id in pd.fixtures)
            {
                var fx = layout.fixtures.FirstOrDefault(f => f.id == id) ?? throw new InvalidDataException($"{DataPath}: graybox fixture {id} not found");
                var h = layout.H(fx.h).ft - (fx.rects[0].x1 - fx.rects[0].x0) / 2 - 0.05f; // just under the globe
                for (var i = 0; i < fx.rects.Length; i++)
                {
                    var r = fx.rects[i];
                    Lamp(lights, $"Pendant_{id.Replace("FX_Pendants_", "")}_{i} [conf {pd.conf}]", LightType.Point, L.ToWorld((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, h), pd.lumens, pd.kelvin, 0, pd.range);
                }
            }

            // Interior exposure inside the retail room only (the exterior keeps Lighting_Day's)
            var vol = new GameObject($"Volume_RetailInterior [fixed EV {d.interiorEv}]");
            vol.transform.SetParent(root, false);
            vol.transform.position = L.ToWorld((room.x0 + room.x1) / 2, (room.y0 + room.y1) / 2, ceilFt / 2);
            var box = vol.AddComponent<BoxCollider>();
            box.isTrigger = true;
            box.size = new Vector3(room.x1 - room.x0, ceilFt, room.y1 - room.y0) * L.Ft;
            var volume = vol.AddComponent<Volume>();
            volume.isGlobal = false;
            volume.priority = 10;
            volume.sharedProfile = Profile(d.interiorEv, d.skyAmbient);

            EditorSceneManager.MarkSceneDirty(scene);
            if (!EditorSceneManager.SaveScene(scene, ScenePath)) throw new IOException($"could not save {ScenePath}");
            return $"lookdev built: lights={lights.childCount} millwork={mill.childCount} panels={p.nx * p.ny}";
        }

        public static float InteriorEv => JsonUtility.FromJson<Data>(File.ReadAllText(DataPath)).interiorEv;

        static bool UnderPanel(Panels p, float x, float y)
        {
            for (var j = 0; j < p.ny; j++)
                for (var i = 0; i < p.nx; i++)
                    if (x >= p.x0 + i * p.pitchX && x <= p.x0 + i * p.pitchX + p.w && y >= p.y0 + j * p.pitchY && y <= p.y0 + j * p.pitchY + p.d) return true;
            return false;
        }

        static L.Rect SoffitRect(L.Rect room, string wall, float depth)
        {
            const float face = 0.2f; // inner face of the 0.2-ft exterior walls (graybox W_Ext_*)
            float x0 = room.x0 + face, x1 = room.x1 - face, y0 = room.y0 + face, y1 = room.y1;
            switch (wall)
            {
                case "N": return new L.Rect { x0 = x0, x1 = x1, y0 = y0, y1 = y0 + depth };
                case "E": return new L.Rect { x0 = x1 - depth, x1 = x1, y0 = y0, y1 = y1 };
                case "W": return new L.Rect { x0 = x0, x1 = x0 + depth, y0 = y0, y1 = y1 };
                default: throw new InvalidDataException($"{DataPath}: soffit wall '{wall}' not supported");
            }
        }

        static bool Inside(L.Rect r, float x, float y) => x >= r.x0 && x <= r.x1 && y >= r.y0 && y <= r.y1;
        static L.Rect Grow(L.Rect r, float e) => new L.Rect { x0 = r.x0 - e, x1 = r.x1 + e, y0 = r.y0 - e, y1 = r.y1 + e };
        static L.Rect Square(float cx, float cy, float s) => new L.Rect { x0 = cx - s / 2, x1 = cx + s / 2, y0 = cy - s / 2, y1 = cy + s / 2 };

        static void Lamp(Transform parent, string name, LightType type, Vector3 pos, float lumens, float kelvin, float angle, float rangeM)
        {
            var go = new GameObject(name);
            go.transform.SetParent(parent, false);
            go.transform.SetPositionAndRotation(pos, Quaternion.Euler(90, 0, 0));
            var light = go.AddComponent<Light>();
            go.AddComponent<HDAdditionalLightData>();
            light.type = type;
            light.lightUnit = LightUnit.Lumen;
            light.intensity = lumens;
            light.useColorTemperature = true;
            light.colorTemperature = kelvin;
            light.color = Color.white;
            light.shadows = LightShadows.None;
            if (type == LightType.Spot)
            {
                light.spotAngle = angle;
                light.innerSpotAngle = angle * 0.5f;
                light.range = 6f;
            }
            else light.range = rangeM;
        }

        sealed class Mats { public Material pt1, walnut, black, steel, quartz, tl1, tl2, neon; }

        static Mats Materials(Data d) => new Mats
        {
            pt1 = Mat("LD_PT1_Gypsum", new Color(0.86f, 0.86f, 0.84f), smooth: 0.15f), // SW7646 First Star read as a light warm grey
            walnut = Mat("LD_WD1_Walnut", new Color(0.42f, 0.27f, 0.18f), Tex($"{WalnutDir}/oak_veneer_05_diff_2k.jpg"), Tex($"{WalnutDir}/oak_veneer_05_nor_gl_2k.jpg", normal: true), 1f, 0.35f),
            black = Mat("LD_ML1_BlackPatina", new Color(0.04f, 0.04f, 0.04f), smooth: 0.35f, metal: 0.6f),
            steel = Mat("LD_StainlessCable", new Color(0.75f, 0.75f, 0.76f), smooth: 0.7f, metal: 1f),
            quartz = Mat("LD_QZ2_Quartz", Color.white, Tex($"{TexDir}/QZ2_quartz.png"), null, 1f / 1f, 0.75f),
            tl1 = Mat("LD_TL1_Marble12x24", Color.white, Tex($"{TexDir}/TL1_marble_12x24.png"), null, 1f / (2 * L.Ft), 0.7f), // texture = 24"x24"
            tl2 = Mat("LD_TL2_Pattern8x8", Color.white, Tex($"{TexDir}/TL2_pattern_8x8.png"), null, 1f / (16f / 12f * L.Ft), 0.3f), // texture = 16"x16"
            neon = NeonMat(d.neon.nits),
        };

        static Texture2D Tex(string path, bool normal = false)
        {
            if (normal && AssetImporter.GetAtPath(path) is TextureImporter ti && ti.textureType != TextureImporterType.NormalMap)
            {
                ti.textureType = TextureImporterType.NormalMap;
                ti.SaveAndReimport();
            }
            return AssetDatabase.LoadAssetAtPath<Texture2D>(path) ?? throw new FileNotFoundException($"{path} missing; run python Tools/Assets/lookdev_textures.py");
        }

        /// <summary>HDRP/Lit, created once and re-set on every build; textured materials use triplanar world mapping so tile size is real-world.</summary>
        static Material Mat(string name, Color color, Texture2D baseMap = null, Texture2D normalMap = null, float worldScale = 1f, float smooth = 0.5f, float metal = 0f)
        {
            var mat = LoadOrCreate(name, "HDRP/Lit");
            mat.SetColor("_BaseColor", color);
            mat.SetFloat("_Smoothness", smooth);
            mat.SetFloat("_Metallic", metal);
            mat.SetTexture("_BaseColorMap", baseMap);
            mat.SetTexture("_NormalMap", normalMap);
            mat.SetFloat("_UVBase", baseMap ? 5f : 0f); // 5 = triplanar
            mat.SetFloat("_TexWorldScale", worldScale);
            HDMaterial.ValidateMaterial(mat);
            EditorUtility.SetDirty(mat);
            return mat;
        }

        static Material NeonMat(float nits)
        {
            var mat = LoadOrCreate("LD_Neon_White", "HDRP/Lit");
            var tex = Tex($"{TexDir}/Neon_FineCannabis.png");
            HDMaterial.SetSurfaceType(mat, true);
            mat.SetColor("_BaseColor", new Color(0, 0, 0, 1));
            mat.SetTexture("_BaseColorMap", tex); // alpha cuts the quad to the lettering + glow
            mat.SetFloat("_UVBase", 0f);
            mat.SetTexture("_EmissiveColorMap", tex);
            mat.SetFloat("_UseEmissiveIntensity", 0f);
            mat.SetColor("_EmissiveColor", new Color(1f, 0.97f, 0.92f) * nits);
            HDMaterial.ValidateMaterial(mat);
            EditorUtility.SetDirty(mat);
            return mat;
        }

        static Material LoadOrCreate(string name, string shader)
        {
            var path = $"{LookdevDir}/Materials/{name}.mat";
            var mat = AssetDatabase.LoadAssetAtPath<Material>(path);
            if (mat) return mat;
            Directory.CreateDirectory($"{LookdevDir}/Materials");
            mat = new Material(Shader.Find(shader) ?? throw new InvalidOperationException($"{shader} shader not found"));
            AssetDatabase.CreateAsset(mat, path);
            return mat;
        }

        static VolumeProfile Profile(float ev, float skyAmbient)
        {
            var path = $"{LookdevDir}/Retail_Interior_Volume.asset";
            var profile = AssetDatabase.LoadAssetAtPath<VolumeProfile>(path);
            if (!profile)
            {
                profile = ScriptableObject.CreateInstance<VolumeProfile>();
                AssetDatabase.CreateAsset(profile, path);
            }
            if (!profile.TryGet<Exposure>(out var exposure))
            {
                exposure = profile.Add<Exposure>(true);
                exposure.name = nameof(Exposure);
                AssetDatabase.AddObjectToAsset(exposure, profile);
            }
            exposure.mode.Override(ExposureMode.Fixed);
            exposure.fixedExposure.Override(ev);
            // shortcut: no baked GI yet, so the sky's ambient probe floods the closed room; damp it here until PERF/lighting bakes APV
            if (!profile.TryGet<IndirectLightingController>(out var indirect))
            {
                indirect = profile.Add<IndirectLightingController>(true);
                indirect.name = nameof(IndirectLightingController);
                AssetDatabase.AddObjectToAsset(indirect, profile);
            }
            indirect.indirectDiffuseLightingMultiplier.Override(skyAmbient);
            indirect.reflectionLightingMultiplier.Override(skyAmbient);
            EditorUtility.SetDirty(profile);
            AssetDatabase.SaveAssets();
            return profile;
        }

        static void EnsureInBuildSettings()
        {
            if (EditorBuildSettings.scenes.Any(s => s.path == ScenePath)) return;
            // in the build so play-mode tests can load it; SceneBootstrap does not load it yet (GAME decides)
            EditorBuildSettings.scenes = EditorBuildSettings.scenes.Append(new EditorBuildSettingsScene(ScenePath, true)).ToArray();
        }
    }
}
