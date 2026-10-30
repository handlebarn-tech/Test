using System;
using System.Collections.Generic;
using System.Linq;

namespace Dispo.Simulation.Slice
{
    public enum CustomerState { NotArrived, AtStand, Queued, Serving, Done }   // AtStand: waiting at the ID stand (GAME-008)
    public enum CustomerOutcome { None, Bought, Walkout, NoSale, Refused }      // Refused: a bad ID caught at the stand
    public enum PatienceState { Calm, Impatient, Leaving }

    /// <summary>One item the customer asks for (GAME-006): a family (hidden from the player) and a stated weight.</summary>
    public sealed class Ask
    {
        public IntentFamily Family;
        public double Grams;
        public string Clause;             // its words in the line ("something for sleep, a half"), for the request strip
        public string Chip;               // chip the player searched with for this item
        public double Fit = -1;           // fit when the customer accepted it (GAME-007 trim penalty), -1 = never accepted
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
        public bool OverLimit;            // GAME-007: asked for more than the 1 oz cap (SPEC_COMP002 §2 shape)
        public IdCard Id;                 // GAME-008: shown at the ID stand while the player covers it, else null
        public bool IdChecked, IdRefusedValid;
        public double CheckInDelay;       // GAME-008: extra wait (s) when the player declined to cover check-in [GDD]
        public bool Medical, OutOfStateCard;   // GAME-009: MED card verified at check-in; an out-of-state card must ring as adult-use
        public double History14d;         // GAME-009: medical grams bought in the last 14 days (seeded)
        public int OutOfStateMedAttempts; // tries to ring an out-of-state card as medical (1st blocked + hint, later + strike)

        /// <summary>Whether this customer may take a trimmed weight (SPEC_COMP002 §2 / §4): over-limit asks and medical allotments.</summary>
        public bool CanTrim => OverLimit || Medical;
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
            var over = new Random(c.seed + 7);   // GAME-007 over-limit asks, own stream for the same reason
            var med = new Random(c.seed + 13);   // GAME-009 medical customers, own stream for the same reason
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
                // GAME-007 [GDD]: SPEC_COMP002 §2 over-limit asks replace the ask list; the player trims at the register.
                int shape = -1;
                IntentFamily y = null, z = null;
                string coreY = null, coreZ = null;
                if (over.NextDouble() < c.overLimitAskChance)
                {
                    shape = over.Next(ShapeGrams.Length);
                    y = d.Intents.Get(Pick(over, c.familyWeights, f => f.w).id);
                    z = d.Intents.Get(Pick(over, c.familyWeights, f => f.w).id);
                    coreY = OneOf(over, y.cores.Where(x => !x.Contains('.')).ToList());
                    coreZ = OneOf(over, z.cores.Where(x => !x.Contains('.')).ToList());
                }
                double total = shape >= 0 ? ShapeGrams[shape] : asks.Sum(a => a.Grams);
                double budget = arch.hasBudget ? Math.Floor(total * c.budgetPerGram[rng.Next(c.budgetPerGram.Length)]) : 0;
                string opener = OneOf(rng, d.Lines.Openers(arch.id)), core = OneOf(rng, fam.cores);
                List<string> spoken;
                if (shape >= 0) asks = OverLimitAsks(d.Lines, shape, fam, core, y, coreY, z, coreZ, out spoken);
                else
                {
                    asks[0].Clause = $"{core}, {d.Lines.Weight(grams)}";
                    spoken = asks.Select(a => a.Clause).ToList();
                }
                double patience = arch.patienceSec * (rush ? c.rushPatienceMult : 1);
                list.Add(new Customer
                {
                    Index = i, SpawnTime = t, Rush = rush, Archetype = arch, Asks = asks, Budget = budget, OverLimit = shape >= 0,
                    Line = Say(d.Lines, opener, spoken, budget),
                    PatienceMax = patience, Patience = patience,
                });
                // GAME-009 [GDD] (SPEC_COMP002 §4): medicalCustomerShare are MED patients with 0-3 prior buys in the last 14 days.
                var cust = list[list.Count - 1];
                if (med.NextDouble() < c.medicalCustomerShare)
                {
                    cust.Medical = true;
                    cust.OutOfStateCard = med.NextDouble() < c.outOfStateMedChance;
                    int buys = med.Next(c.medicalHistoryMaxBuys + 1);
                    for (int b = 0; b < buys; b++) cust.History14d += c.weightOdds[med.Next(c.weightOdds.Length)].g;
                }
            }
            return list;
        }

        /// <summary>§2.6: opener + core + weight clause + optional second item (GAME-006) + optional budget clause.</summary>
        public static string RenderLine(SliceLines l, string opener, string core, double grams, double budget, string second = null) =>
            Say(l, opener, second != null ? new[] { $"{core}, {l.Weight(grams)}", second } : new[] { $"{core}, {l.Weight(grams)}" }, budget);

        /// <summary>opener + clauses joined with "and" + "." + optional budget clause.</summary>
        public static string Say(SliceLines l, string opener, IReadOnlyList<string> clauses, double budget) =>
            $"{opener} {clauses[0]}" + string.Concat(clauses.Skip(1).Select(x => string.Format(l.andClause, x))) + "."
            + (budget > 0 ? string.Format(l.budgetClause, budget) : "");

        /// <summary>Total grams of each SPEC_COMP002 §2 ask shape (all over the 28 g cap).</summary>
        public static readonly double[] ShapeGrams = { 31.5, 56, 35 };

        /// <summary>
        /// SPEC_COMP002 §2 ask shapes (weights from STD_WEIGHTS [SRC]): 0 "an ounce of X and an eighth of Y"; 1 "two ounces" of X
        /// (two 28 g asks, the second can only be dropped); 2 "a half of X and a half of Y and a quarter of Z".
        /// <paramref name="spoken"/> = the clauses as the customer says them.
        /// </summary>
        public static List<Ask> OverLimitAsks(SliceLines l, int shape, IntentFamily x, string coreX, IntentFamily y, string coreY,
            IntentFamily z, string coreZ, out List<string> spoken)
        {
            Ask A(IntentFamily f, double g, string clause) => new Ask { Family = f, Grams = g, Clause = clause };
            List<Ask> asks;
            switch (shape)
            {
                case 0: asks = new List<Ask> { A(x, 28, $"{coreX}, {l.Weight(28)}"), A(y, 3.5, SecondClause(l, coreY, 3.5)) }; break;
                case 1:
                    asks = new List<Ask> { A(x, 28, $"{coreX}, {l.Weight(28)}"), A(x, 28, l.anotherOunce) };
                    spoken = new List<string> { $"{coreX}, {l.twoOunces}" };
                    return asks;
                default: asks = new List<Ask> { A(x, 14, $"{coreX}, {l.Weight(14)}"), A(y, 14, SecondClause(l, coreY, 14)), A(z, 7, SecondClause(l, coreZ, 7)) }; break;
            }
            spoken = asks.Select(a => a.Clause).ToList();
            return asks;
        }

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
