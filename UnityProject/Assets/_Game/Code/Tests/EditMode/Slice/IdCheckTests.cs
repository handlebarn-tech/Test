using System;
using System.IO;
using System.Linq;
using Dispo.Simulation.Slice;
using NUnit.Framework;
using UnityEngine;

namespace Dispo.Slice.Tests
{
    /// <summary>GAME-008: ID rules at boundary dates, the case generator, cover / decline, admit / refuse outcomes.</summary>
    public class IdCheckTests
    {
        static string Read(string rel) => File.ReadAllText(Path.Combine(Application.dataPath, rel));
        static string Cat(string f) => Read("_Game/Data/Catalog/" + f);
        static SliceData Load() => SliceData.Load(Cat("batches.json"), Cat("terpenes.json"), Cat("engine_tables.json"), Cat("pricing.json"),
            Read("_Game/Data/Slice/SliceConfig.json"), Read("_Game/Data/Slice/SliceIntents.json"), Read("_Game/Data/Slice/SliceLines.json"));

        static readonly DateTime Today = new DateTime(2026, 10, 27);
        static IdCard Card(DateTime dob, DateTime exp, IdFormat f = IdFormat.Horizontal, string state = IdRules.Arizona) =>
            new IdCard { Dob = dob, Expires = exp, Format = f, State = state, Type = IdType.DriverLicense, Name = "Test Person" };

        [Test]
        public void Rules_BoundaryDates()
        {
            var cfg = Load().Config;
            var exp = Today.AddYears(2);
            bool V(IdCard c) => IdRules.IsValid(c, Today, cfg);
            Assert.IsTrue(V(Card(Today.AddYears(-21), exp)), "21st birthday today");
            Assert.IsFalse(V(Card(Today.AddYears(-21).AddDays(1), exp)), "21st birthday tomorrow");
            Assert.IsTrue(V(Card(Today.AddDays(-30).AddYears(-21), exp, IdFormat.Vertical)), "AZ vertical, day 30 after turning 21");
            Assert.IsFalse(V(Card(Today.AddDays(-31).AddYears(-21), exp, IdFormat.Vertical)), "AZ vertical, day 31");
            Assert.IsTrue(V(Card(Today.AddDays(-31).AddYears(-21), exp, IdFormat.Vertical, "NEVADA")), "out-of-state vertical at 21+ (O3)");
            Assert.IsFalse(V(Card(Today.AddYears(-21).AddDays(1), exp, IdFormat.Vertical, "NEVADA")), "out-of-state vertical under 21");
            Assert.IsTrue(V(Card(Today.AddYears(-30), Today)), "expires today = still unexpired");
            Assert.IsFalse(V(Card(Today.AddYears(-30), Today.AddDays(-1))), "expired yesterday");
            Assert.AreEqual(0, IdRules.Reason(Card(Today.AddYears(-20), exp), Today, cfg));
            Assert.AreEqual(1, IdRules.Reason(Card(Today.AddYears(-30), Today.AddDays(-1)), Today, cfg));
            Assert.AreEqual(2, IdRules.Reason(Card(Today.AddDays(-31).AddYears(-21), exp, IdFormat.Vertical), Today, cfg));
            Assert.AreEqual(-1, IdRules.Reason(Card(Today.AddYears(-30), exp), Today, cfg));
        }

        [Test]
        public void Generator_EachCase_LandsOnItsSide()
        {
            var d = Load();
            var rng = new System.Random(1);
            foreach (IdCase c in Enum.GetValues(typeof(IdCase)))
                for (int i = 0; i < 300; i++)
                {
                    var id = IdCardGenerator.Make(c, Today, d.Config, d.Lines, rng);
                    Assert.AreEqual(IdCardGenerator.ExpectedValid(c), IdRules.IsValid(id, Today, d.Config), $"{c} #{i}: dob {id.Dob:d} exp {id.Expires:d} {id.Format} {id.State}");
                    Assert.AreEqual(c, id.Case);
                }
            CollectionAssert.AreEquivalent(Enum.GetNames(typeof(IdCase)), d.Config.idCaseWeights.Select(w => w.id), "every case has a weight");
            Assert.AreEqual(100, d.Config.idCaseWeights.Sum(w => w.w), 1e-9, "SPEC §3 weights");
        }

        [Test]
        public void ShiftDate_IsTheShiftDayOfWeek()
        {
            var sim = new ShiftSim(Load());
            Assert.AreEqual(sim.Cfg.shiftDayOfWeek, (int)sim.Today.DayOfWeek);
        }

        /// <summary>A shift whose cover prompt fires (chance 1), ticked to the offer.</summary>
        static ShiftSim Offered(SliceData d = null)
        {
            d = d ?? Load();
            d.Config.coverCheckInChance = 1;
            var sim = new ShiftSim(d);
            int offers = 0;
            sim.CoverOffered += () => offers++;
            while (sim.Cover == CoverState.None) sim.Tick(1);
            Assert.AreEqual(1, offers);
            Assert.AreEqual(CoverState.Offered, sim.Cover);
            return sim;
        }

        /// <summary>Accept, then tick until the 3 covered arrivals are at the stand.</summary>
        static ShiftSim Covered()
        {
            var sim = Offered();
            sim.AcceptCover();
            Assert.AreEqual(sim.Cfg.coverCheckInCount, sim.StandTotal);
            while (sim.Stand.Count < sim.StandTotal) sim.Tick(1);
            return sim;
        }

        [Test]
        public void Cover_SameSeed_SameIds()
        {
            string Dump(ShiftSim s) => string.Join("\n", s.Customers.Where(c => c.Id != null).Select(c => $"{c.Index}|{c.Id.Case}|{c.Id.Name}|{c.Id.Dob:d}|{c.Id.Expires:d}|{c.Id.State}|{c.Id.Format}"));
            var a = Offered(); a.AcceptCover();
            var b = Offered(); b.AcceptCover();
            Assert.AreEqual(Dump(a), Dump(b));
            Assert.AreEqual(3, a.Customers.Count(c => c.Id != null));
            Assert.IsTrue(a.Customers.Where(c => c.Id != null).All(c => c.State == CustomerState.NotArrived), "the next arrivals, not ones already in line");
        }

        [Test]
        public void Prompt_OnlyAtRushStart_OncePerShift()
        {
            var sim = Offered();
            Assert.GreaterOrEqual(sim.Time, sim.Customers.Where(c => c.Rush).Min(c => c.SpawnTime));
            sim.DeclineCover();
            for (int i = 0; i < 2000; i++) sim.Tick(1);
            Assert.AreEqual(CoverState.Declined, sim.Cover);
            var d = Load(); d.Config.coverCheckInChance = 0;
            var none = new ShiftSim(d);
            for (int i = 0; i < 2000; i++) none.Tick(1);
            Assert.AreEqual(CoverState.None, none.Cover, "chance 0: never offered");
        }

        [Test]
        public void Decline_AddsCheckInWaitToTheNextArrivals()
        {
            var sim = Offered();
            sim.DeclineCover();
            var delayed = sim.Customers.Where(c => c.CheckInDelay > 0).ToList();
            Assert.AreEqual(sim.Cfg.coverCheckInCount, delayed.Count);
            Assert.IsTrue(delayed.All(c => c.CheckInDelay == sim.Cfg.declineCheckInDelaySec && c.State == CustomerState.NotArrived && c.Id == null));
        }

        static Customer AtStand(ShiftSim sim, bool valid)
        {
            var c = sim.Stand.First();
            var l = sim.Data.Lines;
            c.Id = IdCardGenerator.Make(valid ? IdCase.AzLicense21 : IdCase.Under21, sim.Today, sim.Cfg, l, new System.Random(3));
            return c;
        }

        [Test]
        public void RefusingAValidId_IsAWalkout()
        {
            var sim = Covered();
            var c = AtStand(sim, true);
            sim.Refuse(c);
            Assert.AreEqual(CustomerOutcome.Walkout, c.Outcome);
            Assert.IsTrue(c.IdRefusedValid);
            var r = sim.Report();
            Assert.AreEqual(1, r.ValidIdsRefused);
            Assert.AreEqual(1, r.IdsChecked);
            Assert.AreEqual(0, r.Strikes.Count);
            Assert.GreaterOrEqual(r.Walkouts, 1);
        }

        [Test]
        public void AdmittingAnInvalidId_AddsOneStrike_AndTheyQueue()
        {
            var sim = Covered();
            var c = AtStand(sim, false);
            sim.Admit(c);
            Assert.AreEqual(CustomerState.Queued, c.State);
            Assert.Contains(c, sim.Queue);
            var r = sim.Report();
            Assert.AreEqual(1, r.Strikes.Count);
            Assert.AreEqual(sim.Data.Lines.strikeBadId, r.Strikes[0].Reason);
            Assert.AreEqual(c.Index, r.Strikes[0].CustomerIndex);
            var v = AtStand(sim, true);
            sim.Admit(v);
            Assert.AreEqual(1, sim.Report().Strikes.Count, "a valid admit adds none");
        }

        [Test]
        public void RefusingABadId_IsCaught_NotAWalkout()
        {
            var sim = Covered();
            var c = AtStand(sim, false);
            int walkouts = sim.Report().Walkouts;
            sim.Refuse(c);
            Assert.AreEqual(CustomerOutcome.Refused, c.Outcome);
            var r = sim.Report();
            Assert.AreEqual(1, r.BadIdsCaught);
            Assert.AreEqual(walkouts, r.Walkouts);
            Assert.AreEqual(0, r.Strikes.Count);
        }

        [Test]
        public void AnIgnoredStand_DrainsPatience_ShiftStillEnds()
        {
            var d = Load();
            d.Config.coverCheckInChance = 1;
            var sim = SliceTests.RunBot(d, 0.5, acceptCover: true);   // accepts the cover, never works the stand
            var covered = sim.Customers.Where(c => c.Id != null).ToList();
            Assert.AreEqual(sim.Cfg.coverCheckInCount, covered.Count);
            Assert.IsTrue(covered.All(c => c.Outcome == CustomerOutcome.Walkout && !c.IdChecked), "nobody checked them: they walked out");
        }
    }
}
