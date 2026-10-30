using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.HighDefinition;
using L = Dispo.Editor.Graybox.GrayboxLayout;

namespace Dispo.Editor.Graybox
{
    /// <summary>
    /// CaptureReferenceViews (TOOLCHAIN 18): renders every REF_* camera plus a top-down orthographic plan view.
    /// Batchmode (needs a GPU, so no -nographics): -executeMethod Dispo.Editor.Graybox.GrayboxCapture.CaptureAll -outDir &lt;dir&gt; -commit &lt;sha&gt;
    /// </summary>
    public static class GrayboxCapture
    {
        public const int Width = 1920, Height = 1080;
        public const float TopDownPxPerFt = 20f, TopDownMarginFt = 2f;
        const float FixedEv = 13f;
        const string Lighting = "Lighting_Day scene + " + GrayboxBuilder.SunName + " 20000 lux, fixed exposure EV 13";

        [Serializable] sealed class Entry { public string cameraId, tile, room, scene, resolution, commit, timestamp, lighting, conf, note, file; }
        [Serializable] sealed class Manifest { public List<Entry> captures = new List<Entry>(); public string topDown; public float topDownPxPerFt, topDownMarginFt, buildingWidthFt, buildingDepthFt; }

        public static void CaptureAll()
        {
            try
            {
                var outDir = Arg("-outDir") ?? Path.GetFullPath("../Artifacts/Screenshots/manual");
                var n = CaptureTo(outDir, Arg("-commit") ?? "unknown");
                Debug.Log($"[Graybox] Capture OK count={n} dir={outDir}");
                EditorApplication.Exit(0);
            }
            catch (Exception e)
            {
                Debug.LogError($"[Graybox] Capture FAILED: {e}");
                EditorApplication.Exit(1);
            }
        }

        public static int CaptureTo(string outDir, string commit)
        {
            Directory.CreateDirectory(outDir);
            var layout = L.Load();
            EditorSceneManager.OpenScene($"{GrayboxBuilder.ScenesDir}/{GrayboxBuilder.Zones[0]}.unity", OpenSceneMode.Single);
            foreach (var s in GrayboxBuilder.Zones.Skip(1).Append("Lighting_Day"))
                EditorSceneManager.OpenScene($"{GrayboxBuilder.ScenesDir}/{s}.unity", OpenSceneMode.Additive);

            var volume = new GameObject("CaptureExposure").AddComponent<Volume>();
            volume.isGlobal = true;
            volume.priority = 1000;
            volume.sharedProfile = ScriptableObject.CreateInstance<VolumeProfile>();
            var exposure = volume.sharedProfile.Add<Exposure>(true);
            exposure.mode.Override(ExposureMode.Fixed);
            exposure.fixedExposure.Override(FixedEv);

            // The test player's camera would otherwise be part of the scene render list; keep it out.
            var player = GameObject.Find(GrayboxBuilder.PlayerName);
            if (player) player.SetActive(false);

            var manifest = new Manifest { topDownPxPerFt = TopDownPxPerFt, topDownMarginFt = TopDownMarginFt, buildingWidthFt = 47.19f, buildingDepthFt = 76.03f };
            var stamp = DateTime.UtcNow.ToString("o");
            try
            {
                foreach (var c in layout.cameras)
                {
                    var go = GameObject.Find(c.Id) ?? throw new InvalidOperationException($"camera {c.Id} not in scenes; rebuild the graybox");
                    var file = c.Id + ".png";
                    Render(go.GetComponent<Camera>(), Width, Height, Path.Combine(outDir, file));
                    manifest.captures.Add(new Entry
                    {
                        cameraId = c.Id, tile = c.tile, room = c.room, scene = go.scene.name, resolution = $"{Width}x{Height}",
                        commit = commit, timestamp = stamp, lighting = Lighting, conf = c.conf, note = c.note, file = file,
                    });
                }
                manifest.topDown = CaptureTopDown(outDir, manifest);
            }
            finally
            {
                if (player) player.SetActive(true);
                UnityEngine.Object.DestroyImmediate(volume.gameObject);
            }
            File.WriteAllText(Path.Combine(outDir, "captures.json"), JsonUtility.ToJson(manifest, true));
            return manifest.captures.Count + 1;
        }

        /// <summary>Orthographic, north-up, fixtures hidden: pixel (px, py) = plan ((px / ppf) - margin, (py / ppf) - margin) ft.</summary>
        static string CaptureTopDown(string outDir, Manifest m)
        {
            var hidden = UnityEngine.Object.FindObjectsByType<Transform>(FindObjectsInactive.Exclude)
                .Where(t => t.name == "Fixtures" && t.parent && t.parent.name.StartsWith("Graybox_")).Select(t => t.gameObject).ToList();
            hidden.ForEach(g => g.SetActive(false));
            var go = new GameObject("TOPDOWN_Plan");
            try
            {
                var w = Mathf.RoundToInt((m.buildingWidthFt + 2 * m.topDownMarginFt) * m.topDownPxPerFt);
                var h = Mathf.RoundToInt((m.buildingDepthFt + 2 * m.topDownMarginFt) * m.topDownPxPerFt);
                var cam = go.AddComponent<Camera>();
                cam.orthographic = true;
                cam.orthographicSize = h / m.topDownPxPerFt / 2 * L.Ft;
                cam.nearClipPlane = 0.1f;
                cam.farClipPlane = 50f;
                var centre = L.ToWorld(m.buildingWidthFt / 2, m.buildingDepthFt / 2);
                go.transform.SetPositionAndRotation(centre + Vector3.up * 20f, Quaternion.Euler(90, 0, 0));
                Render(cam, w, h, Path.Combine(outDir, "TOPDOWN_Plan.png"));
                return "TOPDOWN_Plan.png";
            }
            finally
            {
                UnityEngine.Object.DestroyImmediate(go);
                hidden.ForEach(g => g.SetActive(true));
            }
        }

        static void Render(Camera cam, int w, int h, string path)
        {
            var rt = new RenderTexture(w, h, 24, RenderTextureFormat.ARGB32, RenderTextureReadWrite.sRGB);
            var wasEnabled = cam.enabled;
            cam.enabled = true;
            try
            {
                var request = new RenderPipeline.StandardRequest { destination = rt };
                // A few frames so HDRP history buffers settle.
                for (var i = 0; i < 4; i++)
                {
                    if (RenderPipeline.SupportsRenderRequest(cam, request)) RenderPipeline.SubmitRenderRequest(cam, request);
                    else { cam.targetTexture = rt; cam.Render(); cam.targetTexture = null; }
                }
                var prev = RenderTexture.active;
                RenderTexture.active = rt;
                var tex = new Texture2D(w, h, TextureFormat.RGB24, false);
                tex.ReadPixels(new Rect(0, 0, w, h), 0, 0);
                tex.Apply();
                RenderTexture.active = prev;
                File.WriteAllBytes(path, tex.EncodeToPNG());
                UnityEngine.Object.DestroyImmediate(tex);
            }
            finally
            {
                cam.enabled = wasEnabled;
                rt.Release();
                UnityEngine.Object.DestroyImmediate(rt);
            }
        }

        static string Arg(string name)
        {
            var args = Environment.GetCommandLineArgs();
            var i = Array.IndexOf(args, name);
            return i >= 0 && i + 1 < args.Length ? args[i + 1] : null;
        }
    }
}
