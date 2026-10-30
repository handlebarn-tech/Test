using System;
using System.Collections.Generic;
using System.Linq;

namespace Dispo.Simulation.Slice
{
    public enum IdFormat { Horizontal, Vertical }
    public enum IdType { DriverLicense, IdCard, Passport, Military }

    /// <summary>SPEC_COMP002 §3 ID case table (validity from B1/B2 and store policy O3).</summary>
    public enum IdCase { AzLicense21, OutOfStateLicense21, PassportMilitary21, AzVerticalRecent, AzVerticalStale, OutOfStateVertical21, Expired, Under21 }

    /// <summary>One ID shown at the stand (GAME-008). Name is generated (no real people); State is "" for passport / military.</summary>
    public sealed class IdCard
    {
        public IdCase Case;
        public string Name, State;
        public IdType Type;
        public IdFormat Format;
        public DateTime Dob, Expires;
    }

    /// <summary>The law the player applies (B1, B2, O3). The generator builds each case to land on its side of these rules.</summary>
    public static class IdRules
    {
        public const string Arizona = "ARIZONA";

        /// <summary>
        /// Valid = unexpired on <paramref name="today"/> (expiry day itself counts, B2 "unexpired"), 21+ (B1), and an Arizona
        /// vertical ID within verticalGraceDays of the 21st birthday (B2, O3). Out-of-state vertical IDs at 21+ are valid (O3, GAP-COMP-03).
        /// </summary>
        public static bool IsValid(IdCard id, DateTime today, SliceConfig cfg)
        {
            if (id.Expires.Date < today.Date) return false;
            var turned = id.Dob.AddYears(cfg.minAgeYears);
            if (today.Date < turned.Date) return false;
            return !(id.Format == IdFormat.Vertical && id.State == Arizona && (today.Date - turned.Date).Days > cfg.verticalGraceDays);
        }

        /// <summary>Why an ID fails, as an index into SliceLines.idReasons (0 under 21, 1 expired, 2 vertical past grace), or -1 if valid.</summary>
        public static int Reason(IdCard id, DateTime today, SliceConfig cfg)
        {
            if (today.Date < id.Dob.AddYears(cfg.minAgeYears).Date) return 0;
            if (id.Expires.Date < today.Date) return 1;
            return IsValid(id, today, cfg) ? -1 : 2;
        }

        /// <summary>Whole years of age on <paramref name="today"/>.</summary>
        public static int Age(DateTime dob, DateTime today) => today.Year - dob.Year - (today.Date < dob.AddYears(today.Year - dob.Year).Date ? 1 : 0);
    }

    /// <summary>Seeded ID cases (SPEC_COMP002 §3) with dates computed against the in-game date [GDD].</summary>
    public static class IdCardGenerator
    {
        public static bool ExpectedValid(IdCase c) =>
            c != IdCase.AzVerticalStale && c != IdCase.Expired && c != IdCase.Under21;

        public static IdCase PickCase(SliceConfig cfg, Random rng)
        {
            var w = cfg.idCaseWeights;
            double r = rng.NextDouble() * w.Sum(x => x.w);
            foreach (var x in w) { r -= x.w; if (r < 0) return (IdCase)Enum.Parse(typeof(IdCase), x.id); }
            return (IdCase)Enum.Parse(typeof(IdCase), w[w.Length - 1].id);
        }

        public static IdCard Make(IdCase c, DateTime today, SliceConfig cfg, SliceLines l, Random rng)
        {
            today = today.Date;
            var id = new IdCard
            {
                Case = c, State = IdRules.Arizona, Type = rng.Next(2) == 0 ? IdType.DriverLicense : IdType.IdCard, Format = IdFormat.Horizontal,
                Name = $"{l.idFirstNames[rng.Next(l.idFirstNames.Length)]} {l.idLastNames[rng.Next(l.idLastNames.Length)]}",
                Expires = today.AddDays(rng.Next(1, 5 * 365)),
            };
            string OtherState() => l.idOtherStates[rng.Next(l.idOtherStates.Length)];
            // A DOB whose 21st birthday was exactly `days` ago (Feb 29 birthdays skipped so the day count is exact).
            DateTime TurnedAgo(int days)
            {
                for (int step = days < 0 ? -1 : 1; ; days += step)   // step away from the boundary, never across it
                {
                    var dob = today.AddDays(-days).AddYears(-cfg.minAgeYears);
                    if (dob.AddYears(cfg.minAgeYears) == today.AddDays(-days)) return dob;
                }
            }
            DateTime Adult() => TurnedAgo(cfg.verticalGraceDays + 1 + rng.Next(0, 45 * 365));
            switch (c)
            {
                case IdCase.AzLicense21: id.Dob = Adult(); break;
                case IdCase.OutOfStateLicense21: id.Dob = Adult(); id.State = OtherState(); break;
                case IdCase.PassportMilitary21: id.Dob = Adult(); id.State = ""; id.Type = rng.Next(2) == 0 ? IdType.Passport : IdType.Military; break;
                case IdCase.AzVerticalRecent: id.Dob = TurnedAgo(rng.Next(0, cfg.verticalGraceDays + 1)); id.Format = IdFormat.Vertical; break;
                case IdCase.AzVerticalStale: id.Dob = TurnedAgo(cfg.verticalGraceDays + 1 + rng.Next(0, 330)); id.Format = IdFormat.Vertical; break;
                case IdCase.OutOfStateVertical21: id.Dob = TurnedAgo(rng.Next(0, 330)); id.Format = IdFormat.Vertical; id.State = OtherState(); break;
                case IdCase.Expired:
                    id.Dob = Adult(); id.Expires = today.AddDays(-rng.Next(1, 2 * 365));
                    if (rng.Next(2) == 0) id.State = OtherState();
                    break;
                case IdCase.Under21:
                    id.Dob = TurnedAgo(-rng.Next(1, 3 * 365));   // 21st birthday 1 day to 3 years ahead
                    id.Format = rng.Next(2) == 0 ? IdFormat.Vertical : IdFormat.Horizontal;
                    if (rng.Next(3) == 0) id.State = OtherState();
                    break;
            }
            return id;
        }
    }
}
