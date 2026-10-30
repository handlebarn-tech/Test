using System.IO;
using System.Linq;
using Dispo.Presentation;
using UnityEditor;
using UnityEditor.SceneManagement;
using UnityEngine;
using UnityEngine.Rendering;
using UnityEngine.Rendering.HighDefinition;

namespace Dispo.Editor
{
    /// <summary>
    /// Idempotent batchmode project setup (no GUI wizard):
    /// Unity.exe -batchmode -nographics -quit -projectPath UnityProject -executeMethod Dispo.Editor.ProjectSetup.Run
    /// </summary>
    public static class ProjectSetup
    {
        public const string HdrpAssetPath = "Assets/Settings/HDRP/HDRenderPipelineAsset.asset";
        public const string ScenesFolder = "Assets/_Game/Scenes";

        public static void Run()
        {
            PlayerSettings.colorSpace = ColorSpace.Linear;
            EditorSettings.serializationMode = SerializationMode.ForceText;
            VersionControlSettings.mode = "Visible Meta Files";
            SetActiveInputHandler(1); // 1 = Input System package only

            var hdrp = AssetDatabase.LoadAssetAtPath<HDRenderPipelineAsset>(HdrpAssetPath);
            if (hdrp == null)
            {
                Directory.CreateDirectory(Path.GetDirectoryName(HdrpAssetPath));
                hdrp = ScriptableObject.CreateInstance<HDRenderPipelineAsset>();
                AssetDatabase.CreateAsset(hdrp, HdrpAssetPath);
            }
            GraphicsSettings.defaultRenderPipeline = hdrp;
            var current = QualitySettings.GetQualityLevel();
            for (var i = 0; i < QualitySettings.names.Length; i++)
            {
                QualitySettings.SetQualityLevel(i, false);
                QualitySettings.renderPipeline = hdrp;
            }
            QualitySettings.SetQualityLevel(current, false);

            CreateScenes();
            AssetDatabase.SaveAssets();
            Debug.Log("[ProjectSetup] done");
        }

        static void SetActiveInputHandler(int value)
        {
            var playerSettings = Unsupported.GetSerializedAssetInterfaceSingleton("PlayerSettings");
            if (playerSettings == null) return;
            var so = new SerializedObject(playerSettings);
            var prop = so.FindProperty("activeInputHandler");
            if (prop == null) return;
            prop.intValue = value;
            so.ApplyModifiedPropertiesWithoutUndo();
        }

        static void CreateScenes()
        {
            var names = new[] { SceneBootstrap.BootstrapScene }
                .Concat(SceneBootstrap.AdditiveScenes)
                .Concat(new[] { SceneBootstrap.NightLightingScene })
                .ToArray();

            foreach (var name in names)
            {
                var path = $"{ScenesFolder}/{name}.unity";
                if (File.Exists(path)) continue;
                var scene = EditorSceneManager.NewScene(NewSceneSetup.EmptyScene, NewSceneMode.Single);
                if (name == SceneBootstrap.BootstrapScene)
                {
                    new GameObject("SceneBootstrap", typeof(SceneBootstrap));
                    var cam = new GameObject("Main Camera", typeof(Camera)) { tag = "MainCamera" };
                    cam.transform.position = new Vector3(0f, 1.6f, -5f);
                }
                EditorSceneManager.SaveScene(scene, path);
            }

            EditorBuildSettings.scenes = names
                .Select(n => new EditorBuildSettingsScene($"{ScenesFolder}/{n}.unity", true))
                .ToArray();
        }

        /// <summary>Returns null when HDRP is correctly assigned, otherwise the problem.</summary>
        public static string VerifyRenderPipeline()
        {
            if (!(GraphicsSettings.defaultRenderPipeline is HDRenderPipelineAsset))
                return $"GraphicsSettings.defaultRenderPipeline is not HDRP ({GraphicsSettings.defaultRenderPipeline})";
            for (var i = 0; i < QualitySettings.names.Length; i++)
            {
                var rp = QualitySettings.GetRenderPipelineAssetAt(i);
                if (rp != null && !(rp is HDRenderPipelineAsset))
                    return $"Quality level {QualitySettings.names[i]} uses non-HDRP asset {rp}";
            }
            if (GraphicsSettings.GetSettingsForRenderPipeline<HDRenderPipeline>() == null)
                return "HDRP global settings are not registered";
            if (PlayerSettings.colorSpace != ColorSpace.Linear)
                return "Color space is not Linear";
            return null;
        }
    }
}
