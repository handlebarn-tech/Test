using System;
using System.Collections.Generic;
using System.Linq;

namespace Dispo.Simulation.Slice
{
    public enum CustomerState { NotArrived, Queued, Serving, Done }
    public enum CustomerOutcome { None, Bought, Walkout, NoSale }
    public enum PatienceState { Calm, Impatient, Leaving }

    public sealed class Customer
    {
        public int Index;                 // 1-based
        public double SpawnTime;
        public bool Rush;
        public ArchetypeDef Archetype;
        public IntentFamily TrueFamily;   // hidden from the player
        public double Grams;
        public double Budget;             // post-tax $, 0 = no budget
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
            double t = 0;
            for (int i = 1; i <= c.customersPerShift; i++)
            {
                bool rush = i >= c.rushFirstIndex && i <= c.rushLastIndex;
                if (i > 1) t += rush ? c.arrivalGapRushSec : c.arrivalGapNormalSec;
                var arch = Pick(rng, c.archetypes, a => a.weight);
                var fam = d.Intents.Get(Pick(rng, c.familyWeights, f => f.w).id);
                double grams = Pick(rng, c.weightOdds, w => w.w).g;
                double budget = arch.hasBudget ? Math.Floor(grams * c.budgetPerGram[rng.Next(c.budgetPerGram.Length)]) : 0;
                double patience = arch.patienceSec * (rush ? c.rushPatienceMult : 1);
                list.Add(new Customer
                {
                    Index = i, SpawnTime = t, Rush = rush, Archetype = arch, TrueFamily = fam, Grams = grams, Budget = budget,
                    Line = RenderLine(d.Lines, OneOf(rng, d.Lines.Openers(arch.id)), OneOf(rng, fam.cores), grams, budget),
                    PatienceMax = patience, Patience = patience,
                });
            }
            return list;
        }

        /// <summary>§2.6: opener + core + weight clause + optional budget clause.</summary>
        public static string RenderLine(SliceLines l, string opener, string core, double grams, double budget) =>
            $"{opener} {core}, {l.Weight(grams)}." + (budget > 0 ? string.Format(l.budgetClause, budget) : "");

        static T OneOf<T>(Random rng, IReadOnlyList<T> xs) => xs[rng.Next(xs.Count)];

        static T Pick<T>(Random rng, IReadOnlyList<T> xs, Func<T, double> weight)
        {
            double r = rng.NextDouble() * xs.Sum(weight);
            foreach (var x in xs) { r -= weight(x); if (r < 0) return x; }
            return xs[xs.Count - 1];
        }
    }
}
