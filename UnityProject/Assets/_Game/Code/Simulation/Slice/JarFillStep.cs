using System;
using System.Collections.Generic;
using System.Linq;

namespace Dispo.Simulation.Slice
{
    /// <summary>
    /// GAME-005: which stepped fill mesh (PROC-002 `_F&lt;pct&gt;_`) a jar shows for fill = grams / startGrams.
    /// 0 g → 0 (SOLD OUT); otherwise the nearest step at or above <paramref name="minVisiblePct"/>, ties go up (DEC-046).
    /// </summary>
    public static class JarFillStep
    {
        public static int For(double fill, IEnumerable<int> stepsPct, int minVisiblePct)
        {
            if (fill <= 0) return 0;
            return stepsPct.Where(s => s > 0 && s >= minVisiblePct)
                .OrderBy(s => Math.Round(Math.Abs(s - fill * 100), 6)).ThenByDescending(s => s)
                .First();
        }
    }
}
