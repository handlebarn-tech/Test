using System;
using System.Collections.Generic;
using System.Linq;
using Dispo.Domain.Engine;
using UnityEngine;

namespace Dispo.Simulation.Slice
{
    /// <summary>Data/Slice/SliceConfig.json: every slice constant (SLICE_DESIGN §8). No defaults here: the JSON is the source.</summary>
    [Serializable]
    public sealed class SliceConfig
    {
        public int customersPerShift;
        public double arrivalGapNormalSec, arrivalGapRushSec;
        public int rushFirstIndex, rushLastIndex, shiftDayOfWeek, seed;
        public ArchetypeDef[] archetypes;
        public double rushPatienceMult;
        public IdWeight[] familyWeights;
        public GramWeight[] weightOdds;
        public double[] budgetPerGram;
        public int resultCount;
        public double fitRelaxedFactor, fastSeconds, slowSeconds, waitGraceSeconds, waitPenaltyPerSec, waitPenaltyCap;
        public double wFit, wPrice, wSpeed;
        public double acceptThreshold;
        public int maxRejections;
        public double starCutoff3, starCutoff2;
        public int roughShiftThreshold, queueSlots;
        public double impatientFraction;
        public double startGramsPerBatch, startFillMin, startFillMax;
        public int jarMinVisibleStepPct;
        public int minLowStartJars;
        public double lowStockFraction;
        public int anxietyLowBelow, anxietyModerateBelow, moreOptionsN, moreOptionsStep;
        public double toastSeconds, holdConfirmSeconds, npcWalkSpeed;
        public double adultUseLimitGrams;
        public int storeOpenHour, storeCloseHour, shiftStartHour;

        public static SliceConfig FromJson(string json) => JsonUtility.FromJson<SliceConfig>(json);
    }

    [Serializable] public sealed class ArchetypeDef { public string id, label; public double weight, patienceSec; public bool hasBudget; }
    [Serializable] public sealed class IdWeight { public string id; public double w; }
    [Serializable] public sealed class GramWeight { public double g, w; }
    [Serializable] public sealed class DomainValue { public string d; public int v; }

    /// <summary>One row of Data/Slice/SliceIntents.json: a golden-checked parse (SLICE_DESIGN §2.2).</summary>
    [Serializable]
    public sealed class IntentFamily
    {
        public string id, rc, lbl, chip, keyword, primary;
        public DomainValue[] crit, neg;
        public string[] cores;

        public Dictionary<string, int> Crit => crit.ToDictionary(x => x.d, x => x.v);
        public Dictionary<string, int> Neg => neg.ToDictionary(x => x.d, x => x.v);
    }

    [Serializable]
    public sealed class SliceIntents
    {
        public IntentFamily[] families;
        public static SliceIntents FromJson(string json) => JsonUtility.FromJson<SliceIntents>(json);
        public IntentFamily Get(string id) => families.Single(f => f.id == id);
    }

    [Serializable] public sealed class OpenerSet { public string archetype; public string[] lines; }
    [Serializable] public sealed class WeightPhrase { public double g; public string phrase; }

    /// <summary>Data/Slice/SliceLines.json: line templates and fixed UI wording (SLICE_DESIGN §2.6, §3.5, §10).</summary>
    [Serializable]
    public sealed class SliceLines
    {
        public OpenerSet[] openers;
        public WeightPhrase[] weightPhrases;
        public string budgetClause, rejectPrice, rejectFit, rejectOther, notEnough, wrongWeight, overLimit, idVerified;
        public string fitOk, fitFallback, fallbackBanner, noneMatched;
        public string toastSale, toastSaleDetail, toastReject, toastLeave, toastWalkout;
        public string anxietyLow, anxietyModerate, anxietyHigh;
        public string[] patienceWords;

        public static SliceLines FromJson(string json) => JsonUtility.FromJson<SliceLines>(json);
        public string[] Openers(string archetype) => openers.Single(o => o.archetype == archetype).lines;
        public string Weight(double g) => weightPhrases.Single(w => w.g == g).phrase;
    }

    /// <summary>Everything a shift needs, loaded from JSON text (the caller does file IO, like Catalog.Load).</summary>
    public sealed class SliceData
    {
        public Catalog Catalog;
        public SliceConfig Config;
        public SliceIntents Intents;
        public SliceLines Lines;

        public static SliceData Load(string batches, string terpenes, string tables, string pricing, string config, string intents, string lines) =>
            new SliceData
            {
                Catalog = Catalog.Load(batches, terpenes, tables, pricing),
                Config = SliceConfig.FromJson(config),
                Intents = SliceIntents.FromJson(intents),
                Lines = SliceLines.FromJson(lines),
            };
    }
}
