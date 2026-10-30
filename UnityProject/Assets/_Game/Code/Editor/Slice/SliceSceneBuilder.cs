using System;
using System.IO;
using System.Linq;
using Dispo.Presentation.Slice;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.UIElements;

namespace Dispo.Editor.Slice
{
    /// <summary>
    /// Generates Gameplay_Slice.unity (GAME-002, DEC-029): one SliceGame object with its UIDocument and data refs.
    /// Everything else (jars, NPCs, TEMP anchors, UI) is built at runtime. Rerun after changing references:
    /// menu Dispo › Slice › Build Scene, or batchmode -executeMethod Dispo.Editor.Slice.SliceSceneBuilder.Build.
    /// </summary>
    public static class SliceSceneBuilder
    {
        public const string ScenePath = "Assets/_Game/Scenes/Gameplay_Slice.unity";
        const string Ui = "Assets/_Game/UI/Slice", Mats = "Assets/_Game/Prefabs/Slice/Materials", Data = "Assets/_Game/Data";

        [MenuItem("Dispo/Slice/Build Scene")]
        public static void BuildMenu() => Debug.Log(BuildScene());

        public static void Build()
        {
            try { Debug.Log("[Slice] Build OK " + BuildScene()); EditorApplication.Exit(0); }
            catch (Exception e) { Debug.LogError($"[Slice] Build FAILED: {e}"); EditorApplication.Exit(1); }
        }

        static string BuildScene()
        {
            var panel = AssetDatabase.LoadAssetAtPath<PanelSettings>($"{Ui}/SlicePanelSettings.asset");
            if (!panel)
            {
                panel = ScriptableObject.CreateInstance<PanelSettings>();
                AssetDatabase.CreateAsset(panel, $"{Ui}/SlicePanelSettings.asset");
            }
            panel.themeStyleSheet = Load<ThemeStyleSheet>($"{Ui}/SliceTheme.tss");
            panel.scaleMode = PanelScaleMode.ScaleWithScreenSize;
            panel.referenceResolution = new Vector2Int(1920, 1080);
            panel.screenMatchMode = PanelScreenMatchMode.MatchWidthOrHeight;
            panel.match = 0.5f;
            EditorUtility.SetDirty(panel);

            var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
            var go = new GameObject("SliceGame");
            var doc = go.AddComponent<UIDocument>();
            doc.panelSettings = panel;
            var g = go.AddComponent<SliceGame>();
            g.Document = doc;
            g.Style = Load<StyleSheet>($"{Ui}/Slice.uss");
            g.Batches = Load<TextAsset>($"{Data}/Catalog/batches.json");
            g.Terpenes = Load<TextAsset>($"{Data}/Catalog/terpenes.json");
            g.EngineTables = Load<TextAsset>($"{Data}/Catalog/engine_tables.json");
            g.PricingJson = Load<TextAsset>($"{Data}/Catalog/pricing.json");
            g.Manifest = Load<TextAsset>($"{Data}/Catalog/manifest.json");
            g.Config = Load<TextAsset>($"{Data}/Slice/SliceConfig.json");
            g.Intents = Load<TextAsset>($"{Data}/Slice/SliceIntents.json");
            g.Lines = Load<TextAsset>($"{Data}/Slice/SliceLines.json");
            g.JarShell = Mat("Slice_JarShell", new Color(0.12f, 0.12f, 0.13f));
            g.JarFill = Mat("Slice_JarFill", new Color(0.35f, 0.55f, 0.25f));
            g.Npc = Mat("Slice_Npc", new Color(0.55f, 0.6f, 0.7f));
            g.Bag = Mat("Slice_Bag", new Color(0.85f, 0.75f, 0.55f));
            EditorSceneManager.SaveScene(scene, ScenePath);

            var list = EditorBuildSettings.scenes.ToList();
            if (!list.Any(s => s.path == ScenePath))
            {
                list.Add(new EditorBuildSettingsScene(ScenePath, true));
                EditorBuildSettings.scenes = list.ToArray();
            }
            AssetDatabase.SaveAssets();
            return ScenePath;
        }

        static T Load<T>(string path) where T : UnityEngine.Object =>
            AssetDatabase.LoadAssetAtPath<T>(path) ?? throw new InvalidOperationException($"missing {typeof(T).Name} at {path}");

        static Material Mat(string name, Color color)
        {
            var path = $"{Mats}/{name}.mat";
            var mat = AssetDatabase.LoadAssetAtPath<Material>(path);
            if (mat) return mat;
            Directory.CreateDirectory(Mats);
            mat = new Material(Shader.Find("HDRP/Lit") ?? throw new InvalidOperationException("HDRP/Lit shader not found"));
            mat.SetColor("_BaseColor", color);
            AssetDatabase.CreateAsset(mat, path);
            return mat;
        }
    }
}
