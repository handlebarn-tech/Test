using System;
using System.Collections.Generic;
using System.Linq;
using Dispo.Domain.Engine;

namespace Dispo.Simulation.Slice
{
    /// <summary>Emitted once per confirmed sale (SLICE_DESIGN §4).</summary>
    public sealed class SaleEvent
    {
        public string BatchId, StrainName;
        public int CustomerIndex;
        public double Grams, PricePreTax, PricePostTax, GramsBefore, GramsAfter;
        public bool Medical;   // GAME-009: rung as a medical sale (medicalTaxRate)
    }

    /// <summary>Single stock authority (§4): grams per in-stock batch. Engine stock, POS, jars and the report read it.</summary>
    public sealed class InventoryService
    {
        readonly Catalog _cat;
        readonly SliceConfig _cfg;
        readonly Dictionary<string, double> _grams = new Dictionary<string, double>();

        /// <summary>Batch ids that started in stock, in catalog order (one jar each).</summary>
        public readonly List<string> JarBatchIds;
        public readonly Dictionary<string, double> StartGrams = new Dictionary<string, double>();
        public readonly List<string> SoldOutIds = new List<string>();
        public event Action<SaleEvent> Sold;

        /// <summary>
        /// DEC-027: each jar starts at a seeded fill in [startFillMin, startFillMax] × startGramsPerBatch, with at least
        /// minLowStartJars below lowStockFraction. Grams are floored to the smallest sale weight so sales can empty a jar exactly.
        /// [GDD] The forced-low jars are drawn first from <paramref name="bestsellers"/> (the families' rank-1 batches), so
        /// demand meets a low jar and SOLD OUT happens in a normal shift; random jars alone almost never sell out.
        /// </summary>
        public InventoryService(Catalog cat, SliceConfig cfg, Random rng, IEnumerable<string> bestsellers)
        {
            _cat = cat; _cfg = cfg;
            double unit = cat.Pricing.Weights.Min();
            double Draw(double lo, double hi) => Math.Floor((lo + rng.NextDouble() * (hi - lo)) * cfg.startGramsPerBatch / unit) * unit;
            JarBatchIds = cat.Batches.Where(b => b.InStock).Select(b => b.Id).ToList();
            foreach (var id in JarBatchIds) _grams[id] = Draw(cfg.startFillMin, cfg.startFillMax);
            var top = bestsellers.Distinct().Where(_grams.ContainsKey).ToList();
            var rest = JarBatchIds.Except(top).ToList();
            for (int lows = 0; lows < cfg.minLowStartJars && top.Count + rest.Count > 0; lows++)
            {
                var pool = top.Count > 0 ? top : rest;
                int i = rng.Next(pool.Count);
                _grams[pool[i]] = Draw(cfg.startFillMin, cfg.lowStockFraction);
                pool.RemoveAt(i);
            }
            foreach (var kv in _grams) StartGrams[kv.Key] = kv.Value;
        }

        public double Grams(string batchId) => _grams.TryGetValue(batchId, out var g) ? g : 0;
        /// <summary>Jar fill = grams / a full jar (§4, linear).</summary>
        public double Fill(string batchId) => Grams(batchId) / _cfg.startGramsPerBatch;
        public bool IsSoldOut(string batchId) => Grams(batchId) <= 0;
        public bool IsLow(string batchId) => !IsSoldOut(batchId) && Fill(batchId) < _cfg.lowStockFraction;

        /// <summary>Decrements grams once; at 0 g the batch goes OOS in the engine (batchInStock L15472).</summary>
        public void Sell(SaleEvent e)
        {
            double before = Grams(e.BatchId);
            if (e.Grams <= 0 || before < e.Grams) throw new InvalidOperationException($"cannot sell {e.Grams} g of {e.BatchId} ({before} g left)");
            e.GramsBefore = before;
            e.GramsAfter = _grams[e.BatchId] = before - e.Grams;
            if (e.GramsAfter <= 0)
            {
                _grams[e.BatchId] = e.GramsAfter = 0;
                _cat.SetInStock(e.BatchId, false);
                SoldOutIds.Add(e.BatchId);
            }
            Sold?.Invoke(e);
        }
    }
}
