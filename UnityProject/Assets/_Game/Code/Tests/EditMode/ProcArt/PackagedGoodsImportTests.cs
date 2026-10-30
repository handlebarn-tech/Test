using System.Linq;
using NUnit.Framework;
using UnityEditor;
using UnityEngine;

namespace Dispo.ProcArt.Tests
{
    /// <summary>PROC-004: packaged-goods FBX import as meters, +Y up, with a 3-LOD LODGroup, budgets and the label slot.</summary>
    public class PackagedGoodsImportTests
    {
        const string Dir = "Assets/_Game/Art/Procedural/Packaged/";
        const float Eps = 1e-4f;

        // id, label slot on LOD0, LOD0/1/2 tri budget, Unity size x/y/z (m) — from Tools/Blender/params/packaged_goods.json.
        static readonly object[][] Items =
        {
            new object[] { "PrepackJar", true, new[] { 400, 200, 40 }, new Vector3(0.064f, 0.077f, 0.064f) },
            new object[] { "FlowerPouch", true, new[] { 400, 200, 40 }, new Vector3(0.10f, 0.13f, 0.035f) },
            new object[] { "PrerollTube", true, new[] { 400, 200, 40 }, new Vector3(0.024f, 0.12f, 0.024f) },
            new object[] { "PrerollMultipack", true, new[] { 120, 40, 20 }, new Vector3(0.075f, 0.115f, 0.026f) },
            new object[] { "VapeCartBox", true, new[] { 120, 40, 20 }, new Vector3(0.035f, 0.11f, 0.035f) },
            new object[] { "EdibleBox", true, new[] { 120, 40, 20 }, new Vector3(0.085f, 0.11f, 0.025f) },
            new object[] { "EdibleBag", true, new[] { 400, 200, 40 }, new Vector3(0.09f, 0.125f, 0.03f) },
            new object[] { "ExtractJar", true, new[] { 400, 200, 40 }, new Vector3(0.038f, 0.033f, 0.038f) },
            new object[] { "BevCan", true, new[] { 400, 200, 40 }, new Vector3(0.066f, 0.122f, 0.066f) },
            new object[] { "BevBottle", true, new[] { 600, 300, 40 }, new Vector3(0.06f, 0.20f, 0.06f) },
            new object[] { "TopicalTube", true, new[] { 600, 300, 40 }, new Vector3(0.045f, 0.155f, 0.034f) },
            new object[] { "MerchTee", false, new[] { 160, 60, 20 }, new Vector3(0.22f, 0.03f, 0.28f) },
            new object[] { "MerchLighter", true, new[] { 160, 60, 20 }, new Vector3(0.025f, 0.082f, 0.012f) },
            new object[] { "MerchGrinder", false, new[] { 400, 200, 40 }, new Vector3(0.055f, 0.045f, 0.055f) },
        };

        [TestCaseSource(nameof(Items))]
        public void ItemImportsWithLodsSizeBudgetsAndLabel(string id, bool label, int[] budget, Vector3 size)
        {
            var asset = AssetDatabase.LoadAssetAtPath<GameObject>($"{Dir}PROC_Pkg_{id}.fbx");
            Assert.IsNotNull(asset, "FBX missing");
            var go = Object.Instantiate(asset);
            try
            {
                var lods = go.GetComponent<LODGroup>();
                Assert.IsNotNull(lods, "no LODGroup (the _LOD<n> suffix auto-setup)");
                Assert.AreEqual(3, lods.lodCount);
                for (int lod = 0; lod < 3; lod++)
                {
                    var parts = go.GetComponentsInChildren<MeshFilter>().Where(f => f.name.EndsWith($"_LOD{lod}")).ToArray();
                    Assert.IsNotEmpty(parts, $"LOD{lod} missing");
                    Assert.LessOrEqual(parts.Sum(f => f.sharedMesh.triangles.Length / 3), budget[lod], $"LOD{lod} tris");
                    var vs = parts.SelectMany(f =>
                    {
                        var m = go.transform.worldToLocalMatrix * f.transform.localToWorldMatrix;
                        return f.sharedMesh.vertices.Select(v => m.MultiplyPoint3x4(v));
                    }).ToArray();
                    var min = new Vector3(vs.Min(v => v.x), vs.Min(v => v.y), vs.Min(v => v.z));
                    var max = new Vector3(vs.Max(v => v.x), vs.Max(v => v.y), vs.Max(v => v.z));
                    Assert.That(Mathf.Abs(min.y) < Eps, $"LOD{lod} origin not at the bottom (min y {min.y})");
                    Assert.That(Vector3.Distance(max - min, size) < 1e-3f, $"LOD{lod} size {max - min} != {size} (scale/axis wrong?)");
                }
                var body = go.transform.Find($"PROC_Pkg_{id}_Body_LOD0");
                Assert.IsNotNull(body, "Body_LOD0 missing");
                var mats = body.GetComponent<MeshRenderer>().sharedMaterials;
                Assert.AreEqual(label, mats.Any(m => m.name.Contains("PkgLabel")), "label slot");
                Assert.IsNotEmpty(body.GetComponent<MeshFilter>().sharedMesh.uv2, "UVMap_Label (uv2) missing");
            }
            finally { Object.DestroyImmediate(go); }
        }
    }
}
