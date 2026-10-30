using System;
using System.IO;
using System.Linq;
using UnityEditor;
using UnityEditor.Build.Reporting;
using UnityEngine;
using UnityEngine.Rendering;

namespace Dispo.Editor.CI
{
    /// <summary>Batchmode entry points called by Tools/Studio/studio.ps1. Each exits with 0 on success.</summary>
    public static class StudioCI
    {
        public static void CompileCheck()
        {
            var problems = new System.Collections.Generic.List<string>();
            if (EditorUtility.scriptCompilationFailed) problems.Add("script compilation failed");
            var hdrp = ProjectSetup.VerifyRenderPipeline();
            if (hdrp != null) problems.Add(hdrp);

            Debug.Log($"[StudioCI] defaultRenderPipeline={GraphicsSettings.defaultRenderPipeline?.GetType().FullName} " +
                      $"globalSettings={GraphicsSettings.GetSettingsForRenderPipeline<UnityEngine.Rendering.HighDefinition.HDRenderPipeline>()?.name}");
            Finish("CompileCheck", problems.Count == 0 ? null : string.Join("; ", problems));
        }

        public static void BuildWindows64()
        {
            var path = Arg("-buildPath") ?? Path.GetFullPath("../Builds/Windows64-Dev/DispoGame.exe");
            var options = new BuildPlayerOptions
            {
                scenes = EditorBuildSettings.scenes.Where(s => s.enabled).Select(s => s.path).ToArray(),
                locationPathName = path,
                target = BuildTarget.StandaloneWindows64,
                options = BuildOptions.Development,
            };
            var report = BuildPipeline.BuildPlayer(options);
            var s = report.summary;
            Debug.Log($"[StudioCI] build result={s.result} errors={s.totalErrors} size={s.totalSize} time={s.totalTime} path={path}");
            Finish("BuildWindows64", s.result == BuildResult.Succeeded ? null : $"build {s.result}, {s.totalErrors} errors");
        }

        static string Arg(string name)
        {
            var args = Environment.GetCommandLineArgs();
            var i = Array.IndexOf(args, name);
            return i >= 0 && i + 1 < args.Length ? args[i + 1] : null;
        }

        static void Finish(string method, string error)
        {
            if (error == null) Debug.Log($"[StudioCI] {method} OK");
            else Debug.LogError($"[StudioCI] {method} FAILED: {error}");
            EditorApplication.Exit(error == null ? 0 : 1);
        }
    }
}
