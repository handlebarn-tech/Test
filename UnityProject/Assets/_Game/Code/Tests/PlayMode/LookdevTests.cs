using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;

namespace Dispo.PlayMode.Tests
{
    /// <summary>ART-003: the Retail_Lookdev additive scene keeps the TI heights (DEC-037) and leaves the slice anchors intact.</summary>
    public sealed class LookdevTests
    {
        const float Ft = 0.3048f, Tol = 0.5f / 12f * Ft; // half an inch

        [UnitySetUp]
        public IEnumerator LoadRetailWithLookdev()
        {
            yield return SceneManager.LoadSceneAsync("Retail", LoadSceneMode.Single);
            yield return SceneManager.LoadSceneAsync("Retail_Lookdev", LoadSceneMode.Additive);
        }

        static Renderer[] Parts(string prefix) =>
            SceneManager.GetSceneByName("Retail_Lookdev").GetRootGameObjects().SelectMany(g => g.GetComponentsInChildren<Renderer>(true))
                .Where(r => r.name.StartsWith(prefix)).ToArray();

        static void AssertFt(float metres, float feet, string what) => Assert.AreEqual(feet * Ft, metres, Tol, $"{what}: {metres / Ft:0.###} ft, expected {feet} ft");

        [Test]
        public void TiHeights_CeilingSoffitCounterNeon()
        {
            AssertFt(Parts("CLG_Gypsum_PT1").Single().bounds.min.y, 9f, "gypsum ceiling");
            var soffits = Parts("Soffit_");
            Assert.IsNotEmpty(soffits, "no soffits");
            foreach (var s in soffits) AssertFt(s.bounds.min.y, 7.5f, s.name);
            var tops = Parts("MW_").Where(r => r.name.Contains("top QZ-2")).ToArray();
            Assert.IsNotEmpty(tops, "no counter tops");
            foreach (var t in tops) AssertFt(t.bounds.max.y, 34f / 12f, t.name);
            AssertFt(Parts("Neon_").Single().bounds.min.y, 6f, "neon bottom (72\" AFF)");
        }

        [Test]
        public void NoAccentPanel_CoversARetailCamera()
        {
            // REVIEW-W4F m2: a CLG-1 panel around a CCTV camera blinds its reference view
            var cams = SceneManager.GetSceneByName("Retail").GetRootGameObjects().SelectMany(g => g.GetComponentsInChildren<Camera>(true))
                .Where(c => c.name.StartsWith("REF_") && c.name.EndsWith("_Retail")).ToArray();
            Assert.IsNotEmpty(cams, "no Retail reference cameras");
            foreach (var panel in Parts("CLG1_Panel_").Where(r => !r.name.EndsWith("cable")))
                foreach (var cam in cams)
                {
                    var b = panel.bounds;
                    var p = cam.transform.position;
                    Assert.IsFalse(p.x >= b.min.x && p.x <= b.max.x && p.z >= b.min.z && p.z <= b.max.z, $"{panel.name} covers {cam.name}");
                }
        }

        [Test]
        public void Lights_Are3500K_AndSliceAnchorsStillAboveCounter()
        {
            var lights = SceneManager.GetSceneByName("Retail_Lookdev").GetRootGameObjects().SelectMany(g => g.GetComponentsInChildren<Light>(true)).ToArray();
            Assert.Greater(lights.Length, 10, "too few lookdev lights");
            Assert.IsTrue(lights.All(l => l.useColorTemperature && Mathf.Approximately(l.colorTemperature, 3500f)), "TI lighting is 3500 K");
            var terminal = GameObject.Find("Interact_Terminal");
            Assert.IsNotNull(terminal, "Interact_Terminal missing");
            Assert.Greater(terminal.transform.position.y, 34f / 12f * Ft, "POS terminal must sit on the 34\" counter");
        }
    }
}
