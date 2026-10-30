using System;
using System.IO;
using UnityEditor;
using UnityEngine;
using UnityEngine.Rendering.HighDefinition;

namespace Dispo.Editor.Lookdev
{
    /// <summary>
    /// ART-006: HDRP Lit bud materials for every PROC_JarFill_&lt;Look&gt;.fbx. The FBX's own material colours are lost by
    /// Unity's import (GAME-005: all looks rendered white), so each look gets a body + accent material built from the
    /// same colours as the Blender generator (Tools/Blender/params/jar_fill.json families) and remapped on the importer.
    /// Runs with the graybox build (studio.ps1 unity-graybox); idempotent.
    /// </summary>
    public static class BudMaterials
    {
        const string ParamsPath = "../Tools/Blender/params/jar_fill.json"; // the editor's working dir is UnityProject/
        const string FillDir = "Assets/_Game/Art/Procedural/JarFill";
        const string MatDir = FillDir + "/Materials";

        [Serializable] sealed class Params { public Family[] families; }
        [Serializable] sealed class Family { public string id; public float[] body, accent; }

        [MenuItem("Dispo/Lookdev/Apply Bud Materials")]
        public static void ApplyMenu() => Debug.Log($"[Lookdev] {Apply()}");

        public static string Apply()
        {
            var p = JsonUtility.FromJson<Params>(File.ReadAllText(ParamsPath));
            if (p?.families == null || p.families.Length == 0) throw new InvalidDataException($"{ParamsPath}: no families");
            Directory.CreateDirectory(MatDir);
            int remapped = 0;
            foreach (var f in p.families)
            {
                var fbx = $"{FillDir}/PROC_JarFill_{f.id}.fbx";
                var importer = AssetImporter.GetAtPath(fbx) as ModelImporter ?? throw new FileNotFoundException($"{fbx} missing (run the PROC jar_fill generator)");
                // material names come from the Blender generator (jar_fill.py build(): M_Proc_Bud_<id>, M_Proc_BudAccent_<id>)
                var mats = new[]
                {
                    (src: $"M_Proc_Bud_{f.id}", mat: Mat($"M_Bud_{f.id}", f.body, 0.25f)),
                    (src: $"M_Proc_BudAccent_{f.id}", mat: Mat($"M_BudAccent_{f.id}", f.accent, 0.4f)),
                };
                var map = importer.GetExternalObjectMap();
                var changed = false;
                foreach (var (src, mat) in mats)
                {
                    var id = new AssetImporter.SourceAssetIdentifier(typeof(Material), src);
                    if (map.TryGetValue(id, out var cur) && cur == mat) continue;
                    importer.AddRemap(id, mat);
                    changed = true;
                }
                if (!changed) continue;
                importer.SaveAndReimport();
                remapped++;
            }
            AssetDatabase.SaveAssets();
            return $"bud materials: looks={p.families.Length} remapped={remapped}";
        }

        /// <summary>Blender colours are linear; Unity's SetColor takes sRGB in a linear project, hence .gamma.</summary>
        static Material Mat(string name, float[] rgb, float smooth)
        {
            var path = $"{MatDir}/{name}.mat";
            var mat = AssetDatabase.LoadAssetAtPath<Material>(path);
            if (!mat)
            {
                mat = new Material(Shader.Find("HDRP/Lit") ?? throw new InvalidOperationException("HDRP/Lit shader not found"));
                AssetDatabase.CreateAsset(mat, path);
            }
            mat.SetColor("_BaseColor", new Color(rgb[0], rgb[1], rgb[2]).gamma);
            mat.SetFloat("_Smoothness", smooth);
            mat.SetFloat("_Metallic", 0f);
            HDMaterial.ValidateMaterial(mat);
            EditorUtility.SetDirty(mat);
            return mat;
        }
    }
}
