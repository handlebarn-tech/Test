using System;
using System.Collections.Generic;
using System.Linq;

namespace Dispo.Simulation.Slice
{
    public enum CustomerState { NotArrived, Queued, Serving, Done }
    public enum CustomerOutcome { None, Bought, Walkout, NoSale }
    public enum PatienceState { Calm, Impatient, Leaving }

    /// <summary>One item the customer asks for (GAME-006): a family (hidden from the player) and a stated weight.</summary>
    public sealed class Ask
    {
        public IntentFamily Family;
        public double Grams;
        public string Clause;             // its words in the line ("something for sleep, a half"), for the request strip
        public string Chip;               // chip the player searched with for this item
    }

    public sealed class Customer
    {
        public int Index;                 // 1-based
        public double SpawnTime;
        public bool Rush;
        public ArchetypeDef Archetype;
        public List<Ask> Asks = new List<Ask>();   // 1-2 items (GAME-006); [0] is the slice's single ask
        public IntentFamily TrueFamily { get => Asks[0].Family; set => Asks[0].Family = value; }   // hidden from the player
        public double Grams { get => Asks[0].Grams; set => Asks[0].Grams = value; }
        public double Budget;             // post-tax $ for the whole cart, 0 = no budget
        public string Line;
        public double PatienceMax, Patience;

        public CustomerState State;
        public CustomerOutcome Outcome;
        public double ServiceStart = -1, EndTime = -1, QueueWait;
        public int Rejections;
        public string Chip;               // last chip the player searched with
        public bool AutoFilled;
        public double LastFit = -1, LastSatisfaction = -1;

        public bool HasBudget => Budget > 0;
        public PatienceState PatienceStateOf(double impatientFraction) =>
            Outcome == CustomerOutcome.Walkout ? PatienceState.Leaving
            : Patience / PatienceMax > impatientFraction ? PatienceState.Calm : PatienceState.Impatient;
    }

    /// <summary>Seeded customer generator (SLICE_DESIGN §1, §2). Same seed → same list.</summary>
    public static class CustomerGenerator
    {
        public static List<Customer> Generate(SliceData d, Random rng)
        {
            var c = d.Config;
            var list = new List<Customer>();
            // GAME-006 second items. Offset 4 [GDD]: seed 1 keeps its DEC-027 SOLD OUT (20 of offsets 1-30 do; GAME-010 retunes).
            var more = new Random(c.seed + 4);
            double t = 0;
            for (int i = 1; i <= c.customersPerShift; i++)
            {
                bool rush = i >= c.rushFirstIndex && i <= c.rushLastIndex;
                if (i > 1) t += rush ? c.arrivalGapRushSec : c.arrivalGapNormalSec;
                var arch = Pick(rng, c.archetypes, a => a.weight);
                var fam = d.Intents.Get(Pick(rng, c.familyWeights, f => f.w).id);
                double grams = Pick(rng, c.weightOdds, w => w.w).g;
                var asks = new List<Ask> { new Ask { Family = fam, Grams = grams } };
                // GAME-006 [GDD]: a second clause from the existing family cores, rolled on its own stream so the slice's draws
                // (and its seeded jar fills) stay as they were. Asks stay within the M1 cap; over-limit asks are GAME-007.
                var fits = c.weightOdds.Where(w => grams + w.g <= c.adultUseLimitGrams).ToList();
                if (more.NextDouble() < c.twoItemAskChance && fits.Count > 0)
                {
                    var fam2 = d.Intents.Get(Pick(more, c.familyWeights, f => f.w).id);
                    double g2 = Pick(more, fits, w => w.w).g;
                    var core2 = OneOf(more, fam2.cores.Where(x => !x.Contains('.')).ToList());   // "an eighth of something. I've got…" doesn't read
                    asks.Add(new Ask { Family = fam2, Grams = g2, Clause = SecondClause(d.Lines, core2, g2) });
                }
                double budget = arch.hasBudget ? Math.Floor(asks.Sum(a => a.Grams) * c.budgetPerGram[rng.Next(c.budgetPerGram.Length)]) : 0;
                string opener = OneOf(rng, d.Lines.Openers(arch.id)), core = OneOf(rng, fam.cores);
                asks[0].Clause = $"{core}, {d.Lines.Weight(grams)}";
                double patience = arch.patienceSec * (rush ? c.rushPatienceMult : 1);
                list.Add(new Customer
                {
                    Index = i, SpawnTime = t, Rush = rush, Archetype = arch, Asks = asks, Budget = budget,
                    Line = RenderLine(d.Lines, opener, core, grams, budget, asks.Count > 1 ? asks[1].Clause : null),
                    PatienceMax = patience, Patience = patience,
                });
            }
            return list;
        }

        /// <summary>§2.6: opener + core + weight clause + optional second item (GAME-006) + optional budget clause.</summary>
        public static string RenderLine(SliceLines l, string opener, string core, double grams, double budget, string second = null) =>
            $"{opener} {core}, {l.Weight(grams)}" + (second != null ? string.Format(l.andClause, second) : "") + "."
            + (budget > 0 ? string.Format(l.budgetClause, budget) : "");

        /// <summary>GAME-006: "an eighth of something for energy".</summary>
        public static string SecondClause(SliceLines l, string core, double grams) => string.Format(l.secondClause, l.Weight(grams), core);

        static T OneOf<T>(Random rng, IReadOnlyList<T> xs) => xs[rng.Next(xs.Count)];

        static T Pick<T>(Random rng, IReadOnlyList<T> xs, Func<T, double> weight)
        {
            double r = rng.NextDouble() * xs.Sum(weight);
            foreach (var x in xs) { r -= weight(x); if (r < 0) return x; }
            return xs[xs.Count - 1];
        }
    }
}
