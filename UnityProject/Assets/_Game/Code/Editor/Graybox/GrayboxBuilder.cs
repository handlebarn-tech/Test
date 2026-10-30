using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Dispo.Presentation.Graybox;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering.HighDefinition;
using L = Dispo.Editor.Graybox.GrayboxLayout;

namespace Dispo.Editor.Graybox
{
    /// <summary>
    /// Rebuilds the Retail / BackRooms / Hub / Exterior scene contents from graybox_layout.json.
    /// Batchmode: -executeMethod Dispo.Editor.Graybox.GrayboxBuilder.Build. Everything lives under one
    /// "Graybox_&lt;Zone&gt;" root per scene, which is deleted and regenerated on every run.
    /// </summary>
    public static class GrayboxBuilder
    {
        public static readonly string[] Zones = { "Retail", "BackRooms", "Hub", "Exterior" };
        public const string ScenesDir = "Assets/_Game/Scenes";
        const string MaterialsDir = "Assets/_Game/Art/Graybox/Materials";
        public const string PlayerName = "GrayboxTestPlayer";
        public const string SunName = "Graybox_TempSun (move to Lighting_Day)";

        [MenuItem("Dispo/Graybox/Rebuild From Layout")]
        public static void BuildMenu() => BuildAll();

        public static void Build()
        {
            try
            {
                var counts = BuildAll();
                Debug.Log($"[Graybox] Build OK {counts}");
                EditorApplication.Exit(0);
            }
            catch (Exception e)
            {
                Debug.LogError($"[Graybox] Build FAILED: {e}");
                EditorApplication.Exit(1);
            }
        }

        public static string BuildAll()
        {
            var layout = L.Load();
            var mats = new Dictionary<string, Material>
            {
                ["wall"] = Mat("GB_Wall", new Color(0.82f, 0.82f, 0.80f)),
                ["floor"] = Mat("GB_Floor", new Color(0.30f, 0.30f, 0.32f)),
                ["fixture"] = Mat("GB_Fixture", new Color(0.25f, 0.55f, 0.45f)),
                ["fixtureLow"] = Mat("GB_FixtureLowConf", new Color(0.75f, 0.45f, 0.20f)),
                ["ground"] = Mat("GB_Ground", new Color(0.18f, 0.20f, 0.18f)),
            };
            int walls = 0, fixtures = 0, cams = 0;

            foreach (var zone in Zones)
            {
                var scene = EditorSceneManager.OpenScene($"{ScenesDir}/{zone}.unity", OpenSceneMode.Single);
                foreach (var old in scene.GetRootGameObjects().Where(g => g.name == $"Graybox_{zone}")) UnityEngine.Object.DestroyImmediate(old);
                var root = new GameObject($"Graybox_{zone}").transform;

                var floorParent = Child(root, "Floor");
                foreach (var f in layout.floors.Where(f => f.zone == zone))
                    Box(floorParent, f.id, f.r, -0.5f, 0.5f, mats["floor"], true);

                var ceiling = layout.H("ceiling");
                var wallParent = Child(root, "Walls");
                foreach (var w in layout.walls.Where(w => w.zone == zone)) walls += BuildWall(layout, w, ceiling, wallParent, mats["wall"]);

                var fixParent = Child(root, "Fixtures");
                foreach (var f in layout.fixtures.Where(f => f.zone == zone))
                {
                    var h = layout.H(f.h);
                    var baseFt = string.IsNullOrEmpty(f.@base) ? 0 : layout.H(f.@base).ft;
                    var mat = f.conf == "Low" ? mats["fixtureLow"] : mats["fixture"];
                    var name = $"{f.id} [conf {f.conf}] [h={h.ft}ft {h.gap}]";
                    for (var i = 0; i < f.rects.Length; i++)
                    {
                        var partName = f.rects.Length == 1 ? name : $"{name} part{i}";
                        if (f.shape == "sphere") Sphere(fixParent, partName, f.rects[i], h.ft, mat);
                        else Box(fixParent, partName, f.rects[i], baseFt, h.ft, mat, f.solid);
                    }
                    fixtures++;
                }

                var roomParent = Child(root, "Rooms");
                foreach (var r in layout.rooms.Where(r => r.zone == zone))
                {
                    var go = Box(roomParent, $"Room_{r.id}", r.r, 0, ceiling.ft, null, true);
                    go.GetComponent<BoxCollider>().isTrigger = true;
                }

                var camParent = Child(root, "RefCameras");
                foreach (var c in layout.cameras.Where(c => c.zone == zone))
                {
                    var go = new GameObject(c.Id);
                    go.transform.SetParent(camParent, false);
                    go.transform.position = L.ToWorld(c.x, c.y, layout.H(c.h).ft);
                    go.transform.rotation = Quaternion.Euler(c.pitch, c.yaw, 0);
                    var cam = go.AddComponent<Camera>();
                    cam.fieldOfView = c.fov;
                    cam.nearClipPlane = 0.05f;
                    cam.enabled = false; // reference views only; GrayboxCapture renders them on demand
                    cams++;
                }

                if (zone == layout.spawn.zone) BuildPlayer(root, layout.spawn);
                if (zone == "Exterior") BuildExterior(root, mats["ground"]);

                EditorSceneManager.MarkSceneDirty(scene);
                if (!EditorSceneManager.SaveScene(scene)) throw new IOException($"could not save {scene.path}");
            }
            return $"walls={walls} fixtures={fixtures} cameras={cams}";
        }

        /// <summary>Axis-aligned wall split around its openings; each opening gets a header from its height to the ceiling.</summary>
        static int BuildWall(L layout, L.Wall w, L.Height ceiling, Transform parent, Material mat)
        {
            var alongX = Mathf.Approximately(w.ay, w.by);
            if (!alongX && !Mathf.Approximately(w.ax, w.bx)) throw new InvalidDataException($"{w.id}: walls must be axis-aligned");
            float s0 = alongX ? Mathf.Min(w.ax, w.bx) : Mathf.Min(w.ay, w.by);
            float s1 = alongX ? Mathf.Max(w.ax, w.bx) : Mathf.Max(w.ay, w.by);
            float c = alongX ? w.ay : w.ax, ht = w.t / 2;
            L.Rect Span(float a, float b) => alongX
                ? new L.Rect { x0 = a, x1 = b, y0 = c - ht, y1 = c + ht }
                : new L.Rect { x0 = c - ht, x1 = c + ht, y0 = a, y1 = b };

            var pieces = 0;
            var cursor = s0;
            foreach (var o in (w.openings ?? Array.Empty<L.Opening>()).OrderBy(o => o.from))
            {
                if (o.from < s0 - 0.01f || o.to > s1 + 0.01f || o.to <= o.from) throw new InvalidDataException($"{w.id}/{o.id}: opening outside wall");
                if (o.from > cursor) Box(parent, $"{w.id}_seg{pieces++} [h={ceiling.ft}ft {ceiling.gap}] [t {w.gap}]", Span(cursor, o.from), 0, ceiling.ft, mat, true);
                var oh = layout.H(o.h);
                Box(parent, $"{w.id}_{o.id}_header [opening {o.to - o.from:0.##}ft x {oh.ft}ft {oh.gap}] [conf {o.conf}]",
                    Span(o.from, o.to), oh.ft, ceiling.ft - oh.ft, mat, true);
                cursor = o.to;
            }
            if (s1 > cursor) Box(parent, $"{w.id}_seg{pieces++} [h={ceiling.ft}ft {ceiling.gap}] [t {w.gap}]", Span(cursor, s1), 0, ceiling.ft, mat, true);
            return 1;
        }

        static void BuildPlayer(Transform root, L.Spawn spawn)
        {
            var go = new GameObject(PlayerName);
            go.transform.SetParent(root, false);
            go.transform.position = L.ToWorld(spawn.x, spawn.y) + Vector3.up * 0.05f;
            go.transform.rotation = Quaternion.Euler(0, spawn.yaw, 0);
            var cc = go.AddComponent<CharacterController>();
            cc.height = 1.75f;
            cc.radius = 0.25f;
            cc.center = new Vector3(0, 0.875f, 0);
            cc.stepOffset = 0.3f;
            cc.minMoveDistance = 0; // default 1 mm drops every step at high frame rates
            var eye = new GameObject("Eye").transform;
            eye.SetParent(go.transform, false);
            eye.localPosition = new Vector3(0, 1.6f, 0);
            var cam = eye.gameObject.AddComponent<Camera>();
            cam.depth = 10; // draws over the Bootstrap camera
            cam.nearClipPlane = 0.05f;
            go.AddComponent<GrayboxTestPlayer>().Eye = eye;
        }

        static void BuildExterior(Transform root, Material ground)
        {
            Box(root, "Ground [no site plan; flat placeholder]", new L.Rect { x0 = -60, x1 = 110, y0 = -60, y1 = 140 }, -1.05f, 1f, ground, true);
            var sun = new GameObject(SunName);
            sun.transform.SetParent(root, false);
            sun.transform.rotation = Quaternion.Euler(55, 150, 0);
            var light = sun.AddComponent<Light>();
            light.type = LightType.Directional;
            if (!sun.GetComponent<HDAdditionalLightData>()) sun.AddComponent<HDAdditionalLightData>();
            light.intensity = 20000f; // lux; graybox only, real lighting belongs to Lighting_Day
        }

        static Transform Child(Transform parent, string name)
        {
            var t = new GameObject(name).transform;
            t.SetParent(parent, false);
            return t;
        }

        static GameObject Box(Transform parent, string name, L.Rect r, float bottomFt, float heightFt, Material mat, bool collider)
        {
            var go = GameObject.CreatePrimitive(PrimitiveType.Cube);
            go.name = name;
            go.transform.SetParent(parent, false);
            go.transform.position = L.ToWorld((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, bottomFt + heightFt / 2);
            go.transform.localScale = new Vector3(Mathf.Abs(r.x1 - r.x0), heightFt, Mathf.Abs(r.y1 - r.y0)) * L.Ft;
            if (mat) go.GetComponent<MeshRenderer>().sharedMaterial = mat;
            else UnityEngine.Object.DestroyImmediate(go.GetComponent<MeshRenderer>());
            if (!collider) UnityEngine.Object.DestroyImmediate(go.GetComponent<BoxCollider>());
            go.isStatic = true;
            return go;
        }

        static void Sphere(Transform parent, string name, L.Rect r, float centreFt, Material mat)
        {
            var go = GameObject.CreatePrimitive(PrimitiveType.Sphere);
            go.name = name;
            go.transform.SetParent(parent, false);
            go.transform.position = L.ToWorld((r.x0 + r.x1) / 2, (r.y0 + r.y1) / 2, centreFt);
            go.transform.localScale = Vector3.one * (r.x1 - r.x0) * L.Ft;
            go.GetComponent<MeshRenderer>().sharedMaterial = mat;
            UnityEngine.Object.DestroyImmediate(go.GetComponent<SphereCollider>());
            go.isStatic = true;
        }

        static Material Mat(string name, Color color)
        {
            var path = $"{MaterialsDir}/{name}.mat";
            var mat = AssetDatabase.LoadAssetAtPath<Material>(path);
            if (mat) return mat;
            Directory.CreateDirectory(MaterialsDir);
            mat = new Material(Shader.Find("HDRP/Lit") ?? throw new InvalidOperationException("HDRP/Lit shader not found"));
            mat.SetColor("_BaseColor", color);
            AssetDatabase.CreateAsset(mat, path);
            return mat;
        }
    }
}
