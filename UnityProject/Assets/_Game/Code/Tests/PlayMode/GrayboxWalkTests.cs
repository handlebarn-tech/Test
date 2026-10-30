using System.Collections;
using Dispo.Presentation.Graybox;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;

namespace Dispo.PlayMode.Tests
{
    public sealed class GrayboxWalkTests
    {
        const float Ft = 0.3048f;

        [UnitySetUp]
        public IEnumerator LoadGraybox()
        {
            yield return SceneManager.LoadSceneAsync("Retail", LoadSceneMode.Single);
            yield return SceneManager.LoadSceneAsync("BackRooms", LoadSceneMode.Additive);
        }

        // Spawn in Retail -> east arch -> vestibule -> BOH door -> BOH aisle, steering with real collisions.
        static readonly Vector2[] RouteFt = { new Vector2(36.7f, 15.5f), new Vector2(36.7f, 30.6f), new Vector2(41.5f, 30.6f), new Vector2(41.5f, 38f) };

        [UnityTest]
        public IEnumerator Player_SpawnsInRetail_WalksToBoh_StaysOnFloor()
        {
            var player = Object.FindAnyObjectByType<GrayboxTestPlayer>();
            Assert.IsNotNull(player, "GrayboxTestPlayer missing; rebuild the graybox");
            Assert.IsTrue(Room("Retail").bounds.Contains(Probe(player)), "player does not spawn inside Room_Retail");

            var minY = float.MaxValue;
            foreach (var wp in RouteFt)
            {
                var target = new Vector3(wp.x * Ft, 0, -wp.y * Ft);
                var deadline = Time.time + 30f;
                while (Flat(player.transform.position - target).magnitude > 0.1f)
                {
                    if (Time.time > deadline) Assert.Fail($"stuck at {player.transform.position} on the way to {wp} ft; blocked by: {Blocker(player, target)}");
                    player.ScriptedWorldMove = Flat(target - player.transform.position).normalized;
                    minY = Mathf.Min(minY, player.transform.position.y);
                    yield return null;
                }
            }
            player.ScriptedWorldMove = Vector3.zero;
            yield return new WaitForSeconds(0.5f);

            Assert.IsTrue(Room("BOH").bounds.Contains(Probe(player)), $"player ended at {player.transform.position}, not in Room_BOH");
            Assert.Greater(Mathf.Min(minY, player.transform.position.y), -0.1f, "player fell through the floor");
        }

        static Collider Room(string id) => GameObject.Find($"Room_{id}")?.GetComponent<Collider>() ?? throw new AssertionException($"Room_{id} missing");
        static Vector3 Probe(GrayboxTestPlayer p) => p.transform.position + Vector3.up;
        static string Blocker(GrayboxTestPlayer p, Vector3 target)
        {
            var pos = p.transform.position;
            var hit = Physics.CapsuleCast(pos + Vector3.up * 0.3f, pos + Vector3.up * 1.5f, 0.24f, Flat(target - pos).normalized, out var h, 0.5f,
                ~0, QueryTriggerInteraction.Ignore);
            return hit ? h.collider.name : "nothing (too slow?)";
        }

        static Vector3 Flat(Vector3 v) => new Vector3(v.x, 0, v.z);
    }
}
