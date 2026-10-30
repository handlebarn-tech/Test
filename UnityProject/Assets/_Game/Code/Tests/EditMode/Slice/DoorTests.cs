using System.Collections.Generic;
using System.IO;
using System.Linq;
using Dispo.Presentation.Graybox;
using Dispo.Presentation.Slice;
using NUnit.Framework;
using UnityEngine;

namespace Dispo.Slice.Tests
{
    /// <summary>GAME-025: CONTROLS_FLOW_PS1 §3.2 door state machine and REF-012 DOORS.json reading; §1.2 look clamp.</summary>
    public sealed class DoorTests
    {
        static List<string> _placeholders;
        static Dictionary<string, DoorRow> _rows;

        static Dictionary<string, DoorRow> Rows()
        {
            if (_rows != null) return _rows;
            var json = File.ReadAllText(Path.GetFullPath(Path.Combine(Application.dataPath, "../../Docs/Reference/DOORS.json")));
            _placeholders = new List<string>();
            return _rows = DoorRow.Parse(json, _placeholders).ToDictionary(r => r.Id);
        }

        static DoorRow Row(string lockKind = "none", bool selfClosing = true, bool customers = false, bool staff = true)
            => new DoorRow { Id = "T", Leaves = 1, Lock = lockKind, SelfClosing = selfClosing, Customers = customers, Staff = staff };

        [Test]
        public void StateMachine_ClosedOpeningOpenClosing()
        {
            var d = new DoorState(Row());
            Assert.AreEqual(DoorPhase.Closed, d.Phase);
            Assert.IsTrue(d.Blocks);
            Assert.IsTrue(d.Open(DoorActor.Player, false, false));
            Assert.AreEqual(DoorPhase.Opening, d.Phase);
            Assert.IsFalse(d.Blocks, "a swinging leaf never blocks");
            d.Tick(DoorState.OpenSeconds / 2, true);
            Assert.AreEqual(DoorPhase.Opening, d.Phase);
            d.Tick(DoorState.OpenSeconds, true);
            Assert.AreEqual(DoorPhase.Open, d.Phase);
            d.Tick(10, true);
            Assert.AreEqual(DoorPhase.Open, d.Phase, "an occupied trigger holds it open");
            d.Tick(DoorState.AutoCloseDelay * 0.9f, false);
            Assert.AreEqual(DoorPhase.Open, d.Phase);
            d.Tick(DoorState.AutoCloseDelay * 0.2f, false);
            Assert.AreEqual(DoorPhase.Closing, d.Phase, "auto-close after the delay");
            d.Tick(DoorState.OpenSeconds, false);
            Assert.AreEqual(DoorPhase.Closed, d.Phase);
            Assert.IsTrue(d.Blocks);
        }

        [Test]
        public void NotSelfClosing_StaysOpen_UntilToggled()
        {
            var d = new DoorState(Row(selfClosing: false));
            d.Open(DoorActor.Player, false, false);
            d.Tick(1, false); d.Tick(100, false);
            Assert.AreEqual(DoorPhase.Open, d.Phase);
            Assert.IsTrue(d.Toggle(DoorActor.Player, false, false));
            Assert.AreEqual(DoorPhase.Closing, d.Phase);
        }

        [Test]
        public void Locks_Refuse()
        {
            var keyed = new DoorState(Row("keyed"));
            Assert.IsFalse(keyed.Open(DoorActor.Player, false, false));
            Assert.AreEqual(DoorPhase.Closed, keyed.Phase, "a refused door does not open");
            var staffOnly = new DoorState(Row("staffOnly", customers: true));
            Assert.IsTrue(staffOnly.Allows(DoorActor.Player, true, false), "the player is staff");
            Assert.IsTrue(staffOnly.Allows(DoorActor.Staff, true, false));
            Assert.IsFalse(staffOnly.Allows(DoorActor.Customer, true, false));
        }

        [Test]
        public void NpcUse_FromDoorsJson()
        {
            var r = Rows();
            var restroom = new DoorState(r["Hall_Restroom"]);   // DEC-110 W7: staff only, customers never path through
            Assert.IsFalse(restroom.Allows(DoorActor.Customer, false, false));
            Assert.IsTrue(restroom.Allows(DoorActor.Staff, false, false));
            var entry = new DoorState(r["Entry"]);
            Assert.IsTrue(entry.Allows(DoorActor.Customer, true, false));
            var emergency = new DoorState(r["Emergency_RetailE"]);   // npcUse empty: nobody paths through, the player may open it
            Assert.IsFalse(emergency.Allows(DoorActor.Customer, false, false));
            Assert.IsFalse(emergency.Allows(DoorActor.Staff, false, false));
            Assert.IsTrue(emergency.Allows(DoorActor.Player, false, false));
        }

        [Test]
        public void EntryTimeLock_LetsLeaversOut_NobodyIn()
        {
            var entry = new DoorState(Rows()["Entry"]);
            Assert.AreEqual("entryTimeLock", entry.Row.Lock);
            Assert.IsTrue(entry.Allows(DoorActor.Customer, true, false), "before 22:00 (or Quick shift) customers come in");
            Assert.IsFalse(entry.Allows(DoorActor.Customer, true, true), "after 22:00 nobody new enters");
            Assert.IsFalse(entry.Allows(DoorActor.Player, true, true));
            Assert.IsTrue(entry.Allows(DoorActor.Customer, false, true), "an exiting customer still gets out");
        }

        [Test]
        public void Openings_SpawnNothing_PairsHaveTwoLeaves()
        {
            var r = Rows();
            foreach (var id in new[] { "Arch_W", "Arch_E", "Grille_101B" }) Assert.IsFalse(r[id].Spawns, id);
            var entry = r["Entry"];
            Assert.IsTrue(entry.Spawns);
            CollectionAssert.AreEqual(new[] { "Door_Entry_L", "Door_Entry_R" }, entry.LeafList.Select(l => l.Object));
            CollectionAssert.AreEqual(new float[] { -90, 90 }, entry.LeafList.Select(l => l.OpenAngle), "signed swing out (west), never flipped");
            Assert.AreEqual("Door_Hall_Restroom", r["Hall_Restroom"].LeafList.Single().Object);
            Assert.IsTrue(_placeholders.Contains("Entry.selfClosing"), "unknown selfClosing → placeholder true, listed");
            Assert.IsTrue(entry.SelfClosing);
        }

        [Test]
        public void ProppedOpen_StartsOpen_NeverAutoCloses_UntilClosed()
        {
            var r = Rows();
            CollectionAssert.AreEquivalent(new[] { "Vest_FOH", "Vest_BOH", "Hall_Office", "HUB2_HUB" }, r.Values.Where(x => x.Spawns && x.ProppedOpen).Select(x => x.Id));
            var d = new DoorState(r["Vest_FOH"]);
            Assert.AreEqual(DoorPhase.Open, d.Phase);
            Assert.IsFalse(d.Blocks, "collider off while propped");
            d.Tick(1000, false);
            Assert.AreEqual(DoorPhase.Open, d.Phase);
            d.Close();
            Assert.IsFalse(d.Propped);
            d.Tick(DoorState.OpenSeconds, false);
            Assert.AreEqual(DoorPhase.Closed, d.Phase);
            d.Open(DoorActor.Player, false, false);
            d.Tick(DoorState.OpenSeconds, false); d.Tick(DoorState.AutoCloseDelay + 0.01f, false);
            Assert.AreEqual(DoorPhase.Closing, d.Phase, "once unpropped its own selfClosing applies");
        }

        [Test]
        public void Look_PitchClampAndInvert()
        {
            var go = new GameObject("p", typeof(CharacterController));
            var eye = new GameObject("eye").transform;
            eye.SetParent(go.transform, false);
            var p = go.AddComponent<GrayboxTestPlayer>();
            p.Eye = eye;
            p.LookSensitivity = 0.1f;
            p.Look(new Vector2(0, -100000));
            Assert.AreEqual(85f, p.Pitch, 1e-4, "±85° clamp");
            p.Look(new Vector2(0, 100000));
            Assert.AreEqual(-85f, p.Pitch, 1e-4);
            p.InvertY = true;
            p.Look(new Vector2(0, 100));
            Assert.AreEqual(-75f, p.Pitch, 1e-3, "invert Y flips the vertical delta");
            p.Look(new Vector2(100, 0));
            Assert.AreEqual(10f, go.transform.eulerAngles.y, 1e-3, "raw yaw: 0.1 °/count, no acceleration");
            Object.DestroyImmediate(go);
        }
    }
}
