using System.Collections;
using System.Collections.Generic;
using Dispo.Presentation.Graybox;
using Dispo.Presentation.Slice;
using NUnit.Framework;
using UnityEngine;
using UnityEngine.SceneManagement;
using UnityEngine.TestTools;

namespace Dispo.Slice.PlayMode.Tests
{
    /// <summary>GAME-025 (CONTROLS_FLOW_PS1 §2–§3): Esc pause from every screen, and a test-built door the scripted player walks through.</summary>
    public sealed class SliceControlsTests
    {
        [UnityTearDown]
        public IEnumerator Reset() { Time.timeScale = 1; yield return null; }

        /// <summary>
        /// Plays seed 1 with the bot; the first time each of World (customer at the counter), Query, Pos, IdCheck and Report is up,
        /// TogglePause (what Esc calls) shows the menu, Sim.Time holds for 2 s real time, and Resume returns to the same screen.
        /// </summary>
        [UnityTest, Timeout(600000)]
        public IEnumerator Esc_PausesEveryScreen_AndFreezesSim()
        {
            yield return SceneManager.LoadSceneAsync("Retail", LoadSceneMode.Single);
            yield return SceneManager.LoadSceneAsync("Gameplay_Slice", LoadSceneMode.Additive);
            yield return null;
            var g = Object.FindAnyObjectByType<SliceGame>();
            g.Sim.Cfg.coverCheckInChance = 1;   // reach the ID panel
            var want = new HashSet<SliceScreen> { SliceScreen.World, SliceScreen.Query, SliceScreen.Pos, SliceScreen.IdCheck, SliceScreen.Report };
            bool holdChecked = false;
            Time.timeScale = 20;
            float deadline = Time.realtimeSinceStartup + 400;
            while (want.Count > 0)
            {
                Assert.Less(Time.realtimeSinceStartup, deadline, $"not reached: {string.Join(", ", want)}");
                var s = g.Screen;
                bool ready = s != SliceScreen.World || g.CustomerAtCounter;
                if (want.Contains(s) && ready)
                {
                    want.Remove(s);
                    var cartBefore = g.Sim.Cart.Count;
                    if (s == SliceScreen.Pos && !holdChecked)
                    {
                        holdChecked = true;
                        g.PosHold(true);
                        yield return null;
                        Assert.Greater(g.HoldProgress, 0, "hold running");
                    }
                    Time.timeScale = 1;
                    g.TogglePause();
                    Assert.IsTrue(g.Paused);
                    Assert.IsTrue(g.View.PauseVisible, $"pause menu over {s}");
                    Assert.AreEqual(0, g.HoldProgress, "a POS hold is cancelled on pause");
                    Assert.IsFalse(g.WantsCursorLocked, "cursor free while paused");
                    double t = g.Sim.Time;
                    yield return new WaitForSecondsRealtime(2f);
                    Assert.AreEqual(t, g.Sim.Time, $"Sim.Time advanced while paused on {s}");
                    Assert.AreEqual(s, g.Screen, "the screen underneath stays");
                    g.TogglePause();
                    Assert.IsFalse(g.Paused);
                    Assert.IsFalse(g.View.PauseVisible);
                    Assert.AreEqual(s, g.Screen, "Resume returns to the same screen");
                    Assert.AreEqual(cartBefore, g.Sim.Cart.Count, "same cart");
                    Assert.AreEqual(s == SliceScreen.World, g.WantsCursorLocked, "cursor of the screen underneath (batchmode does not hold a real lock)");
                    Time.timeScale = 20;
                }
                if (g.FinalReport == null) SliceBotTests.Step(g);
                yield return null;
            }
            Assert.IsTrue(holdChecked);
        }

        /// <summary>CF§3.2: hinge + leaf + two anchors built here; the scripted player walks into trigger A, passes, and the door closes.</summary>
        [UnityTest]
        public IEnumerator Door_OpensForPlayer_LetsThrough_AutoCloses()
        {
            yield return SceneManager.LoadSceneAsync("Retail", LoadSceneMode.Single);   // a floor and lighting; no slice
            var origin = new Vector3(0, 100, 0);   // high above the store geometry
            var floor = GameObject.CreatePrimitive(PrimitiveType.Cube);
            floor.transform.position = origin + new Vector3(0, -0.5f, 0);
            floor.transform.localScale = new Vector3(10, 1, 10);

            var hinge = new GameObject("Door_Test_Hinge").transform;   // leaf extends along local +X; closed yaw 0
            hinge.position = origin;
            var leaf = GameObject.CreatePrimitive(PrimitiveType.Cube);
            leaf.name = "Door_Test";
            leaf.transform.SetParent(hinge, false);
            leaf.transform.localPosition = new Vector3(0.45f, 1.05f, 0);
            leaf.transform.localScale = new Vector3(0.9f, 2.1f, 0.05f);
            new GameObject("Anchor_Door_Test_A").transform.position = origin + new Vector3(0.45f, 0, -0.6f);
            new GameObject("Anchor_Door_Test_B").transform.position = origin + new Vector3(0.45f, 0, 1.0f);
            var row = new DoorRow { Id = "Test", Leaves = 1, Lock = "none", SelfClosing = true, Staff = true };
            row.LeafList.Add(new DoorRow.Leaf { Object = "Door_Test", ClosedYaw = 0, OpenAngle = -90, WidthFt = 0.9f / 0.3048f });

            // The graybox's own player (real CharacterController setup), moved onto the test floor.
            var player = Object.FindAnyObjectByType<GrayboxTestPlayer>();
            Assert.IsNotNull(player, "GrayboxTestPlayer missing from Retail");
            var body = player.gameObject;
            var cc = body.GetComponent<CharacterController>();
            cc.enabled = false;
            body.transform.SetPositionAndRotation(origin + new Vector3(0.45f, 0.1f, -2.5f), Quaternion.identity);
            cc.enabled = true;
            player.ScriptedWorldMove = Vector3.zero;

            var doors = new GameObject("Doors").AddComponent<SliceDoor>();
            doors.Player = player;
            Assert.AreEqual(1, doors.Build(new[] { row }));
            var d = doors.Doors[0];
            Assert.AreEqual(DoorPhase.Closed, d.State.Phase);
            Assert.IsTrue(leaf.GetComponent<Collider>().enabled, "a closed leaf blocks");
            yield return null;

            player.ScriptedWorldMove = Vector3.forward;
            bool sawOpen = false;
            float deadline = Time.time + 8;
            while (body.transform.position.z < origin.z + 2.2f)
            {
                if (Time.time > deadline)
                {
                    var pos = body.transform.position;
                    var hit = Physics.CapsuleCast(pos + Vector3.up * 0.3f, pos + Vector3.up * 1.5f, 0.24f, Vector3.forward, out var h, 0.5f, ~0, QueryTriggerInteraction.Ignore);
                    Assert.Fail($"player stuck at {pos}, door {d.State.Phase}, blocked by {(hit ? h.collider.name : "nothing")}");
                }
                sawOpen |= d.State.Phase == DoorPhase.Open;
                yield return null;
            }
            player.ScriptedWorldMove = Vector3.zero;
            Assert.IsTrue(sawOpen, "door opened on the walk-through");
            Assert.AreEqual(-90f, Mathf.DeltaAngle(0, hinge.eulerAngles.y), 1f, "open at the signed DOORS.json angle");

            deadline = Time.time + DoorState.AutoCloseDelay + DoorState.OpenSeconds + 2;
            while (d.State.Phase != DoorPhase.Closed)
            {
                Assert.Less(Time.time, deadline, $"door did not close ({d.State.Phase})");
                yield return null;
            }
            Assert.IsTrue(leaf.GetComponent<Collider>().enabled, "closed again → blocks");
            Assert.AreEqual(0f, Mathf.DeltaAngle(0, hinge.eulerAngles.y), 0.5f);
        }
    }
}
