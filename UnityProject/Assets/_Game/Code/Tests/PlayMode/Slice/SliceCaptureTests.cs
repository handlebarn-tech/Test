using System;
using System.Collections;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using Dispo.Presentation.Slice;
using Dispo.Simulation.Slice;
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
            exposure.fixedExposure.Override(11f);   // 2 EV brighter than GrayboxCapture: the jar wall is unlit until ART-003 lighting
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

            // GAME-007: the last customer asks "a half of X and a half of Y and a quarter of Z" (35 g, SPEC_COMP002 §2 shape 2) so
            // the register shows a red, 3-line cart; it is shot at 100/125/150 % text, then the bot trims it. The last one, so the
            // earlier sale and SOLD OUT shots keep the seed-1 flow.
            var c1 = g.Sim.Customers[g.Sim.Customers.Count - 1];
            var lines = g.Sim.Data.Lines;
            c1.Asks = CustomerGenerator.OverLimitAsks(lines, 2, c1.TrueFamily, c1.TrueFamily.cores[0], c1.TrueFamily, c1.TrueFamily.cores[0],
                c1.TrueFamily, c1.TrueFamily.cores[0], out var spoken);
            c1.Line = CustomerGenerator.Say(lines, lines.Openers(c1.Archetype.id)[0], spoken, 0);
            c1.OverLimit = true; c1.Budget = 0;

            Time.timeScale = 10;
            var seen = new HashSet<SliceScreen>();
            bool saleShot = false, jarShot = false, debugShot = false, cartShot = false;
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
                    // Stand 1.8 m out from the jar toward the register, so it works for any jar-wall orientation.
                    var toward = Vector3.ProjectOnPlane(keep.position - jar, Vector3.up).normalized;
                    cam.position = jar + toward * 1.8f + Vector3.up * 0.3f;
                    cam.rotation = Quaternion.LookRotation(jar - cam.position);
                    yield return null; yield return null;
                    var label = g.View.JarLabel(g.Sim.Inventory.SoldOutIds[0]);
                    Assert.IsNotNull(label, "SOLD OUT label exists");
                    Assert.AreEqual("SOLD OUT", label.text);
                    Assert.AreEqual(DisplayStyle.Flex, label.resolvedStyle.display, "SOLD OUT label visible in the jar shot");
                    var vp = g.ViewCamera.WorldToViewportPoint(jar);
                    var want = new Vector2(vp.x * W, (1 - vp.y) * H);   // the camera RT and panel RT are both W×H
                    Assert.Less(Vector2.Distance(want, new Vector2(label.resolvedStyle.left + 30, label.resolvedStyle.top + 12)), 8f, "label sits over its jar (label is ~60 px wide)");
                    yield return Shot("Jars_SoldOut_Low");
                    // GAME-005: close-up of the canisters (band colour, label, fill step) around the sold-out jar.
                    var mid = jar - Vector3.up * 0.25f;
                    cam.position = mid + toward * 0.7f;
                    cam.rotation = Quaternion.LookRotation(mid - cam.position);
                    yield return Shot("Jars_Closeup");
                    cam.SetPositionAndRotation(keep.position, keep.rotation);
                    Time.timeScale = 10;
                }
                if (!cartShot && g.Screen == SliceScreen.Pos && g.Sim.Serving == c1)
                {
                    cartShot = true; Time.timeScale = 0;
                    while (g.Sim.CanAddItem)
                    {
                        g.AddItem();
                        var ask = g.Sim.CurrentAsk;
                        g.ChooseChip(ask.Family);
                        Assert.AreEqual(Response.Accept, g.Choose(g.Sim.Results.Cards.First(k => g.Sim.Free(k.Rep.Id) >= ask.Grams)).Response);
                    }
                    Assert.AreEqual(MeterState.Red, g.Sim.Meter, "35 g cart is red");
                    foreach (var pct in new[] { 100, 125, 150 })
                    {
                        g.SetTextScale(pct);
                        yield return Shot($"Pos_Cart_Red_{pct}");
                        CheckRegister(g.Document.rootVisualElement, pct);
                    }
                    g.SetTextScale(100);
                    Time.timeScale = 10;
                }
                SliceBotTests.Step(g);
                yield return null;
            }
            Time.timeScale = 1;
            Assert.IsNotNull(g.FinalReport, "shift did not end");
            yield return Shot("Report");
            Debug.Log($"[SliceCapture] OK {shots.Count} shots in {dir}: {string.Join(", ", shots)}");
            Assert.AreEqual(CustomerOutcome.Bought, c1.Outcome, "the bot trimmed the over-limit cart and sold it");
            Assert.AreEqual(1, g.FinalReport.OverLimitTrims);
            Assert.IsTrue(new[] { "Dialogue", "Query", "Results", "Detail", "Pos", "Report", "Sale_Toast", "Jars_SoldOut_Low", "Jars_Closeup",
                    "Pos_Cart_Red_100", "Pos_Cart_Red_125", "Pos_Cart_Red_150" }
                .All(s => shots.Any(f => f.Contains(s))), string.Join(", ", shots));
        }

        /// <summary>
        /// REVIEW-W4W m1/m4, UX_COUNTER_INTEL §10: cart-line stepper / grams / price / ✕ columns line up across rows; the register and
        /// its Confirm sit inside the 1728×972 title-safe area (never scroll); the meter value and state words stay readable.
        /// </summary>
        static void CheckRegister(VisualElement root, int pct)
        {
            var rows = root.Query(className: "cart-line").ToList();
            Assert.AreEqual(3, rows.Count, $"{pct} %: 3 cart lines");
            foreach (var cls in new[] { "cart-step", "cart-grams", "cart-price" })
            {
                var xs = rows.Select(r => r.Q(className: cls).worldBound.x).ToList();
                Assert.Less(xs.Max() - xs.Min(), 1f, $"{pct} %: {cls} column aligned ({string.Join(", ", xs)})");
            }
            foreach (var r in rows)
                Assert.LessOrEqual(r.Query(className: "cart-step").ToList().Last().worldBound.xMax, r.worldBound.xMax + 0.5f, $"{pct} %: ✕ inside its row");
            var safe = new Rect(96, 54, W - 192, H - 108);
            bool Inside(Rect b) => b.xMin >= safe.xMin - 0.5f && b.yMin >= safe.yMin - 0.5f && b.xMax <= safe.xMax + 0.5f && b.yMax <= safe.yMax + 0.5f;
            var pos = root.Q(className: "pos").worldBound;
            Assert.IsTrue(Inside(pos), $"{pct} %: register {pos} inside the safe area");
            var confirm = root.Query<Button>().ToList().Single(b => b.text == "Hold to confirm").worldBound;
            Assert.IsTrue(Inside(confirm) && pos.Contains(confirm.center), $"{pct} %: Confirm {confirm} on screen");
            foreach (var cls in new[] { "meter-value", "meter-label", "cart-name", "cart-grams", "cart-price" })
                foreach (var l in root.Query<Label>(className: cls).ToList())
                    Assert.Less(l.worldBound.height, 2 * l.resolvedStyle.fontSize, $"{pct} %: {cls} '{l.text}' stays one line");
            Assert.IsNotNull(root.Q<Label>(className: "meter-hint"), $"{pct} %: red trim hint shown");
            var title = root.Q(className: "pos").Q<Label>(className: "h1").worldBound;
            foreach (var t in root.Query(className: "toast").ToList())
                Assert.IsFalse(t.worldBound.Overlaps(title), $"{pct} %: toast {t.worldBound} covers the register title {title}");
            Debug.Log($"[SliceCapture] register {pct} %: panel {pos}, confirm {confirm}");
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
