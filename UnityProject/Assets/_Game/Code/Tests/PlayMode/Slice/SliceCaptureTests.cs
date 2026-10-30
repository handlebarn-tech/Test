using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Dispo.Presentation.Slice;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.HighDefinition;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;
using UnityEngine.UIElements;

namespace Dispo.Slice.PlayMode.Tests
{
    /// <summary>
    /// One screenshot per slice screen + the report (GAME-002 capture). Needs a GPU, so it skips under -nographics.
    /// Run: Unity -batchmode -runTests -testPlatform PlayMode -testCategory SliceCapture -sliceCaptureDir &lt;dir&gt; (no -nographics).
    /// </summary>
    public sealed class SliceCaptureTests
    {
        const int W = 1920, H = 1080;

        [UnityTest, Category("SliceCapture")]
        public IEnumerator Capture_EachScreen()
        {
            if (SystemInfo.graphicsDeviceType == GraphicsDeviceType.Null) Assert.Ignore("needs a GPU: run without -nographics");
            yield return SceneManager.LoadSceneAsync("Retail", LoadSceneMode.Single);
            foreach (var s in new[] { "Exterior", "Lighting_Day", "Gameplay_Slice" }) yield return SceneManager.LoadSceneAsync(s, LoadSceneMode.Additive);
            yield return null;

            // Same fixed exposure as GrayboxCapture (EV 13, temporary sun in Exterior).
            var volume = new GameObject("CaptureExposure").AddComponent<Volume>();
            volume.isGlobal = true; volume.priority = 100;
            volume.sharedProfile = ScriptableObject.CreateInstance<VolumeProfile>();
            var exposure = volume.sharedProfile.Add<Exposure>(true);
            exposure.mode.Override(ExposureMode.Fixed);
            exposure.fixedExposure.Override(13f);
            volume.sharedProfile.Add<MotionBlur>(true).intensity.Override(0f);  // the jar shot teleports the camera

            var g = UnityEngine.Object.FindAnyObjectByType<SliceGame>();
            var uiRt = new RenderTexture(W, H, 24, RenderTextureFormat.ARGB32, RenderTextureReadWrite.sRGB);
            var ps = UnityEngine.Object.Instantiate(g.Document.panelSettings);  // never touch the shared asset
            ps.targetTexture = uiRt; ps.clearColor = true; ps.colorClearValue = Color.clear;
            g.Document.panelSettings = ps;
            // The camera must have the panel's pixel size, or the projected jar labels land in the wrong place.
            var camRt = new RenderTexture(W, H, 24, RenderTextureFormat.ARGB32, RenderTextureReadWrite.sRGB);
            g.ViewCamera.targetTexture = camRt;
            var args = Environment.GetCommandLineArgs();
            int ai = Array.IndexOf(args, "-sliceCaptureDir");
            string dir = ai >= 0 ? args[ai + 1] : Path.GetFullPath(Path.Combine(Application.dataPath, "../../Artifacts/Screenshots/slice"));
            Directory.CreateDirectory(dir);

            var shots = new List<string>();
            int n = 0;
            IEnumerator Shot(string name)
            {
                yield return null; yield return null;
                var file = Path.Combine(dir, $"SLICE_{++n:00}_{name}.png");
                Composite(g.ViewCamera, uiRt, file);
                shots.Add(Path.GetFileName(file));
            }

            Time.timeScale = 10;
            var seen = new HashSet<SliceScreen>();
            bool saleShot = false, jarShot = false, debugShot = false;
            float deadline = Time.realtimeSinceStartup + 600;
            while (g.FinalReport == null && Time.realtimeSinceStartup < deadline)
            {
                if (g.Sim.Serving != null && (g.Screen != SliceScreen.World || g.CustomerAtCounter) && seen.Add(g.Screen))
                {
                    Time.timeScale = 0;
                    if (g.Screen == SliceScreen.World && !debugShot) { debugShot = true; yield return Shot("World_Hud"); }
                    else if (g.Screen != SliceScreen.World) yield return Shot(g.Screen.ToString());
                    if (g.Screen == SliceScreen.Results)
                    {
                        g.Inspect(g.Sim.Results.Cards[0]);
                        yield return Shot("Detail");
                        g.Back();
                    }
                    if (g.Screen == SliceScreen.Query)
                    {
                        g.View.DebugVisible = true;
                        yield return Shot("Query_DebugOverlay");
                        g.View.DebugVisible = false;
                    }
                    Time.timeScale = 10;
                }
                if (!saleShot && g.Sim.Sales.Count == 1 && g.Screen == SliceScreen.World)
                {
                    saleShot = true; Time.timeScale = 0;
                    yield return Shot("Sale_Toast");
                    Time.timeScale = 10;
                }
                if (!jarShot && g.Sim.Inventory.SoldOutIds.Count > 0 && g.Screen == SliceScreen.World)
                {
                    jarShot = true; Time.timeScale = 0;
                    var cam = g.ViewCamera.transform;
                    var keep = (cam.position, cam.rotation);
                    var jar = g.JarTops.First(kv => kv.Key == g.Sim.Inventory.SoldOutIds[0]).Value;
                    cam.position = jar + new Vector3(0, 0.25f, -1.6f);
                    cam.rotation = Quaternion.LookRotation(jar - cam.position);
                    yield return Shot("Jars_SoldOut_Low");
                    cam.SetPositionAndRotation(keep.position, keep.rotation);
                    Time.timeScale = 10;
                }
                SliceBotTests.Step(g);
                yield return null;
            }
            Time.timeScale = 1;
            Assert.IsNotNull(g.FinalReport, "shift did not end");
            yield return Shot("Report");
            Debug.Log($"[SliceCapture] OK {shots.Count} shots in {dir}: {string.Join(", ", shots)}");
            Assert.IsTrue(new[] { "Dialogue", "Query", "Results", "Detail", "Pos", "Report", "Sale_Toast", "Jars_SoldOut_Low" }
                .All(s => shots.Any(f => f.Contains(s))), string.Join(", ", shots));
        }

        /// <summary>World camera render with the UI panel texture alpha-blended on top.</summary>
        static void Composite(Camera cam, RenderTexture ui, string path)
        {
            var rt = new RenderTexture(W, H, 24, RenderTextureFormat.ARGB32, RenderTextureReadWrite.sRGB);
            var request = new RenderPipeline.StandardRequest { destination = rt };
            if (RenderPipeline.SupportsRenderRequest(cam, request)) RenderPipeline.SubmitRenderRequest(cam, request);
            else { cam.targetTexture = rt; cam.Render(); cam.targetTexture = null; }
            var world = Read(rt);
            var top = Read(ui);
            var a = world.GetPixels32();
            var b = top.GetPixels32();
            for (int i = 0; i < a.Length; i++) a[i] = Color32.Lerp(a[i], new Color32(b[i].r, b[i].g, b[i].b, 255), b[i].a / 255f);
            world.SetPixels32(a);
            File.WriteAllBytes(path, world.EncodeToPNG());
            rt.Release();
        }

        static Texture2D Read(RenderTexture rt)
        {
            var prev = RenderTexture.active;
            RenderTexture.active = rt;
            var tex = new Texture2D(rt.width, rt.height, TextureFormat.RGBA32, false);
            tex.ReadPixels(new Rect(0, 0, rt.width, rt.height), 0, 0);
            tex.Apply();
            RenderTexture.active = prev;
            return tex;
        }
    }
}
