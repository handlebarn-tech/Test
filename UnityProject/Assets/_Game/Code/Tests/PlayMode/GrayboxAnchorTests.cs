using System.Collections;
using System.Linq;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;

namespace Dispo.PlayMode.Tests
{
    /// <summary>Every SLICE_DESIGN §7 anchor exists in the Retail scene with its exact name (GAME-002 finds them by name).</summary>
    public sealed class GrayboxAnchorTests
    {
        const int MinJarSlots = 77; // in-stock batch count in the current snapshot (SLICE_DESIGN §7)

        static readonly string[] Required =
        {
            "Anchor_CustomerSpawn", "Anchor_CustomerExit",
            "Anchor_QueueSlot_0", "Anchor_QueueSlot_1", "Anchor_QueueSlot_2", "Anchor_QueueSlot_3",
            "Anchor_ServiceCustomer", "Anchor_ServicePlayer", "Interact_Terminal", "Interact_Scale",
        };

        [UnitySetUp]
        public IEnumerator LoadRetail()
        {
            yield return SceneManager.LoadSceneAsync("Retail", LoadSceneMode.Single);
        }

        [Test]
        public void SliceAnchors_AllPresent_Unique_InRetail()
        {
            var names = SceneManager.GetSceneByName("Retail").GetRootGameObjects()
                .SelectMany(g => g.GetComponentsInChildren<Transform>(true)).Select(t => t.name).ToList();
            var expected = Required.Concat(Enumerable.Range(0, MinJarSlots).Select(i => $"Anchor_JarSlot_{i:000}"));
            var missing = expected.Where(n => !names.Contains(n)).ToList();
            Assert.IsEmpty(missing, $"missing anchors (rebuild the graybox): {string.Join(", ", missing)}");
            var dupes = names.Where(n => n.StartsWith("Anchor_") || n.StartsWith("Interact_")).GroupBy(n => n).Where(g => g.Count() > 1).Select(g => g.Key).ToList();
            Assert.IsEmpty(dupes, $"duplicate anchor names: {string.Join(", ", dupes)}");
        }

        [Test]
        public void Scale_IsOnItsStand_NextToTerminal()
        {
            var scale = GameObject.Find("Interact_Scale").transform.position;
            var terminal = GameObject.Find("Interact_Terminal").transform.position;
            var player = GameObject.Find("Anchor_ServicePlayer").transform.position;
            Assert.Less(Vector3.Distance(scale, terminal), 1.5f, "scale too far from the POS monitor");
            Assert.Less(Vector3.Distance(new Vector3(scale.x, 0, scale.z), player), 1.5f, "scale out of reach of the budtender anchor");
            Assert.IsTrue(Physics.Raycast(scale + Vector3.up * 0.01f, Vector3.down, out var hit, 1.5f) && hit.collider.name.StartsWith("FX_ScaleStand_"),
                "Interact_Scale does not sit above a scale stand");
        }
    }
}
