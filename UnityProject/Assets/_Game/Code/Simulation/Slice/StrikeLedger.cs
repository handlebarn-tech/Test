using System;
using System.Collections.Generic;

namespace Dispo.Simulation.Slice
{
    /// <summary>One compliance strike (SPEC_COMP002 §7): why, whose sale, when (sim seconds).</summary>
    public sealed class Strike
    {
        public string Reason;
        public int CustomerIndex;
        public double Time;
    }

    /// <summary>
    /// The shift's strike ledger (GAME-007; GAME-008/009 add the sources). Strikes never end the shift (DEC-032);
    /// the report flags "Manager review" at strikeReviewThreshold.
    /// </summary>
    public sealed class StrikeLedger
    {
        readonly List<Strike> _strikes = new List<Strike>();
        public IReadOnlyList<Strike> Strikes => _strikes;
        public event Action<Strike> Added;

        public Strike Add(string reason, int customerIndex, double time)
        {
            var s = new Strike { Reason = reason, CustomerIndex = customerIndex, Time = time };
            _strikes.Add(s);
            Added?.Invoke(s);
            return s;
        }
    }
}
