using System.Linq;
using NUnit.Framework;
using UnityEditor;
using UnityEngine;

namespace Dispo.ProcArt.Tests
{
    /// <summary>PROC-002: the Blender jar-fill FBX import as meters, +Y up, inside the deli-jar cavity, with a LODGroup.</summary>
    public class JarFillImportTests
    {
        const string Dir = "Assets/_Game/Art/Procedural/JarFill/";
        static readonly string[] Families = { "GreenDense", "GreenAiry", "PurpleHeavy", "OrangePistil", "Frosty", "DarkCompact" };
        static readonly int[] Steps = { 0, 10, 20, 40, 70, 100 };
        static readonly int[] StepTriBudget = { 5000, 1400, 40 }; // per LOD, Tools/Blender/params/jar_fill.json
        // Cavity of PROC_DeliJar (deli_jar.json, GAP-PROC-01, REF-007 estimate): 152.4 x 139.7 mm body - 4 mm walls,
        // 8 mm floor, 235 mm rim. Band 55 mm; DEC-046 wants every step above 0 g to show at least 12 mm above it.
        const float HalfX = 0.0722f, HalfZ = 0.06585f, Floor = 0.008f, Rim = 0.235f, Band = 0.055f, MinAboveBand = 0.012f, Eps = 1e-4f;

        [Test]
        public void EveryFamilyImportsWithStepsLodsAndFitsTheJar([ValueSource(nameof(Families))] string family)
        {
            var asset = AssetDatabase.LoadAssetAtPath<GameObject>($"{Dir}PROC_JarFill_{family}.fbx");
            Assert.IsNotNull(asset, "FBX missing");
            var go = Object.Instantiate(asset);
            try
            {
                var lods = go.GetComponent<LODGroup>();
                Assert.IsNotNull(lods, "no LODGroup (the _LOD<n> suffix auto-setup)");
                Assert.AreEqual(3, lods.lodCount);
                float prevTop = 0;
                foreach (int step in Steps)
                {
                    for (int lod = 0; lod < 3; lod++)
                    {
                        var t = go.transform.Find($"PROC_JarFill_{family}_F{step:000}_LOD{lod}");
                        if (step == 0 && lod > 0) { Assert.IsNull(t, "SOLD OUT has only LOD0 shake"); continue; }
                        Assert.IsNotNull(t, $"F{step:000}_LOD{lod} missing");
                        var mesh = t.GetComponent<MeshFilter>().sharedMesh;
                        // LOD2 block is body-only; the FBX drops its unused accent slot.
                        Assert.AreEqual(lod == 2 ? 1 : 2, t.GetComponent<MeshRenderer>().sharedMaterials.Length, $"F{step:000}_LOD{lod} materials");
                        Assert.LessOrEqual(mesh.triangles.Length / 3, StepTriBudget[lod], $"F{step:000}_LOD{lod} tris");
                        var m = go.transform.worldToLocalMatrix * t.localToWorldMatrix;
                        var vs = mesh.vertices.Select(v => m.MultiplyPoint3x4(v)).ToArray();
                        Assert.That(vs.All(v => Mathf.Abs(v.x) <= HalfX + Eps && Mathf.Abs(v.z) <= HalfZ + Eps
                                                && v.y >= Floor - Eps && v.y <= Rim + Eps),
                            $"F{step:000}_LOD{lod} leaves the jar cavity (scale/axis wrong?)");
                        if (step > 0)
                            Assert.GreaterOrEqual(vs.Max(v => v.y), Band + MinAboveBand - Eps, $"F{step:000}_LOD{lod} hidden by the base band (DEC-046)");
                        if (lod == 0)
                        {
                            float top = vs.Max(v => v.y);
                            Assert.GreaterOrEqual(top, prevTop, $"F{step:000} lower than the step below it");
                            prevTop = top;
                        }
                    }
                }
                Assert.Greater(prevTop, 0.2f, "full jar should reach near the rim");
            }
            finally { Object.DestroyImmediate(go); }
        }
    }
}
