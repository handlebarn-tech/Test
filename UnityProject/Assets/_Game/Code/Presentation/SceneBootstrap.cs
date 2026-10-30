using UnityEngine;
using UnityEngine.SceneManagement;

namespace Dispo.Presentation
{
    /// <summary>Lives in Bootstrap; loads the additive scene set at startup.</summary>
    public sealed class SceneBootstrap : MonoBehaviour
    {
        public const string BootstrapScene = "Bootstrap";
        public const string NightLightingScene = "Lighting_Night";

        // Lighting_Night is in the build but not loaded at boot; day/night swapping belongs to gameplay.
        public static readonly string[] AdditiveScenes =
        {
            "Retail", "BackRooms", "Hub", "Exterior", "GameplaySystems", "NPCs", "Audio", "Lighting_Day", "Gameplay_Slice",
        };

        // Marker the studio smoke launch waits for in Player.log.
        public const string ReadyMarker = "STUDIO_SMOKE_READY";

        private System.Collections.IEnumerator Start()
        {
            foreach (var scene in AdditiveScenes)
            {
                if (!SceneManager.GetSceneByName(scene).isLoaded)
                    yield return SceneManager.LoadSceneAsync(scene, LoadSceneMode.Additive);
            }
            Debug.Log($"{ReadyMarker} scenes={SceneManager.sceneCount}");

            var perfOut = Perf.PerfCapture.Arg();  // PERF-001: `-perf <json>` plays the bot shift, writes metrics, quits
            if (perfOut != null) gameObject.AddComponent<Perf.PerfCapture>().Begin(perfOut, Time.realtimeSinceStartup);
        }
    }
}
