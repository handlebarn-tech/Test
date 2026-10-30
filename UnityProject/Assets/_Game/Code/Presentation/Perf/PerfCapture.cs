using System;
using System.Collections.Generic;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Text;
using Dispo.Presentation.Slice;
using Unity.Profiling;
using UnityEngine;

namespace Dispo.Presentation.Perf
{
    /// <summary>PERF-001: with the player arg <c>-perf &lt;json&gt;</c>, a bot plays the seed-1 slice shift (same steps as
    /// SliceBotTests), samples frame time and render/memory counters every frame, writes JSON and quits.</summary>
    public sealed class PerfCapture : MonoBehaviour
    {
        public const float TimeScale = 20;      // as SliceBotTests: a full shift in a couple of real minutes
        const int WarmupFrames = 60;            // skip shader/PSO warm-up spikes right after load
        const float TimeoutSec = 600;

        static readonly string[] RenderCounters = { "Draw Calls Count", "Batches Count", "SetPass Calls Count", "Triangles Count", "Vertices Count" };
        static readonly string[] MemoryCounters = { "Total Used Memory", "Total Reserved Memory", "System Used Memory", "Gfx Used Memory" };

        string _out;
        float _loadSec, _start;
        readonly List<float> _ms = new List<float>(), _cpu = new List<float>(), _gpu = new List<float>();
        readonly List<(string name, ProfilerRecorder rec, List<long> vals)> _counters = new List<(string, ProfilerRecorder, List<long>)>();
        readonly FrameTiming[] _timing = new FrameTiming[1];
        SliceGame _game;
        int _frame;

        public static string Arg()
        {
            var args = Environment.GetCommandLineArgs();
            var i = Array.IndexOf(args, "-perf");
            return i >= 0 && i + 1 < args.Length ? args[i + 1] : null;
        }

        public void Begin(string outPath, float loadSec)
        {
            _out = outPath;
            _loadSec = loadSec;
            QualitySettings.vSyncCount = 0;
            Application.targetFrameRate = -1;
            Application.runInBackground = true;   // an unfocused window must not pause the run
            foreach (var n in RenderCounters) _counters.Add((n, ProfilerRecorder.StartNew(ProfilerCategory.Render, n), new List<long>()));
            foreach (var n in MemoryCounters) _counters.Add((n, ProfilerRecorder.StartNew(ProfilerCategory.Memory, n), new List<long>()));
            _game = FindAnyObjectByType<SliceGame>();
            _start = Time.realtimeSinceStartup;
            Time.timeScale = TimeScale;
        }

        void Update()
        {
            if (_out == null) return;
            float t = Time.realtimeSinceStartup - _start;
            if (_game == null || _game.Sim == null) { if (t > 10) Finish("SliceGame missing"); return; }
            if (_game.FinalReport != null) { Finish(null); return; }
            if (t > TimeoutSec) { Finish($"timeout at screen {_game.Screen}"); return; }
            Step(_game);

            if (++_frame <= WarmupFrames) return;
            _ms.Add(Time.unscaledDeltaTime * 1000f);
            FrameTimingManager.CaptureFrameTimings();
            if (FrameTimingManager.GetLatestTimings(1, _timing) == 1)
            {
                _cpu.Add((float)_timing[0].cpuFrameTime);
                _gpu.Add((float)_timing[0].gpuFrameTime);
            }
            foreach (var c in _counters) if (c.rec.Valid) c.vals.Add(c.rec.LastValue);
        }

        // Copy of SliceBotTests.Step without the asserts (Presentation can't reference the test assembly).
        static void Step(SliceGame g)
        {
            var c = g.Sim.Serving;
            if (c == null) return;
            switch (g.Screen)
            {
                case SliceScreen.World: if (g.CustomerAtCounter) g.Talk(); break;
                case SliceScreen.Dialogue: g.LookItUp(); break;
                case SliceScreen.Query: g.ChooseChip(g.Sim.CurrentAsk.Family); break;
                case SliceScreen.Results:
                    var card = g.Sim.Results.Cards.FirstOrDefault(k => g.Sim.Free(k.Rep.Id) >= g.Sim.CurrentAsk.Grams);
                    if (card != null) g.Choose(card);
                    break;
                case SliceScreen.Pos:   // GAME-006 cart; GAME-007: trim an over-limit cart, add only what fits
                    if (g.Sim.Meter == Dispo.Simulation.Slice.MeterState.Red)   // drop the last line; a lone medical line over the allotment rings adult-use
                    { if (g.Sim.Cart.Count > 1) g.PosRemove(g.Sim.Cart.Count - 1); else if (g.Sim.MedicalSale) g.ToggleSaleType(); else g.PosCancel(); }
                    else if (g.Sim.CanAddItem && g.Sim.CartGrams + g.Sim.CurrentAsk.Grams <= g.Sim.CartCap) g.AddItem();
                    else { if (g.Sim.MedicalSale && g.Sim.Serving.OutOfStateCard) g.ToggleSaleType(); g.PosConfirm(); }   // GAME-009
                    break;
            }
        }

        void Finish(string error)
        {
            Time.timeScale = 1;
            var r = _game ? _game.FinalReport : null;
            var ms = _ms.OrderBy(x => x).ToArray();
            var json = new StringBuilder("{\n");
            void Add(string k, object v) => json.Append($"  \"{k}\": {v},\n");
            string S(string s) => "\"" + (s ?? "").Replace("\\", "/").Replace("\"", "'") + "\"";
            string F(double d) => d.ToString("0.###", CultureInfo.InvariantCulture);
            double Avg(IReadOnlyCollection<float> v) => v.Count > 0 ? v.Average() : -1;

            Add("completed", error == null ? "true" : "false");
            Add("error", S(error));
            Add("unityVersion", S(Application.unityVersion));
            Add("gpu", S(SystemInfo.graphicsDeviceName));
            Add("graphicsApi", S(SystemInfo.graphicsDeviceType.ToString()));
            Add("vramTotalMB", SystemInfo.graphicsMemorySize);
            Add("cpu", S(SystemInfo.processorType));
            Add("ramTotalMB", SystemInfo.systemMemorySize);
            Add("resolution", S($"{Screen.width}x{Screen.height}"));
            Add("quality", S(QualitySettings.names[QualitySettings.GetQualityLevel()]));
            Add("timeScale", F(TimeScale));
            Add("loadSec", F(_loadSec));
            Add("shiftRealSec", F(Time.realtimeSinceStartup - _start));
            Add("frames", ms.Length);
            Add("frameMsAvg", F(Avg(ms)));
            Add("frameMsP50", F(Pct(ms, 0.50)));
            Add("frameMsP95", F(Pct(ms, 0.95)));
            Add("frameMsP99", F(Pct(ms, 0.99)));
            Add("frameMsMax", F(ms.Length > 0 ? ms[ms.Length - 1] : -1));
            Add("fpsAvg", F(ms.Length > 0 ? 1000.0 / ms.Average() : -1));
            var worst = ms.Skip((int)(ms.Length * 0.99)).ToArray();  // 1% low = average FPS of the slowest 1% of frames
            Add("fps1PctLow", F(worst.Length > 0 ? 1000.0 / worst.Average() : -1));
            Add("cpuFrameMsAvg", F(Avg(_cpu)));
            Add("cpuFrameMsP95", F(Pct(_cpu.OrderBy(x => x).ToArray(), 0.95)));
            Add("gpuFrameMsAvg", F(Avg(_gpu)));
            Add("gpuFrameMsP95", F(Pct(_gpu.OrderBy(x => x).ToArray(), 0.95)));
            foreach (var (name, rec, vals) in _counters)
            {
                var key = char.ToLowerInvariant(name[0]) + new string(name.Substring(1).Where(char.IsLetter).ToArray());
                bool mem = MemoryCounters.Contains(name);
                double div = mem ? 1024.0 * 1024.0 : 1;
                Add(key + (mem ? "MBAvg" : "Avg"), F(vals.Count > 0 ? vals.Average() / div : -1));
                Add(key + (mem ? "MBMax" : "Max"), F(vals.Count > 0 ? vals.Max() / div : -1));
                rec.Dispose();
            }
            if (r != null) Add("shift", S($"served={r.CustomersServed} walkouts={r.Walkouts} noSales={r.NoSales} revenue={F(r.RevenuePostTax)} stars={r.Stars}"));
            json.Append($"  \"seed\": {(_game && _game.Sim != null ? _game.Sim.Cfg.seed : -1)}\n}}\n");

            Directory.CreateDirectory(Path.GetDirectoryName(Path.GetFullPath(_out)));
            File.WriteAllText(_out, json.ToString());
            Debug.Log($"[Perf] wrote {_out} completed={error == null} {error}");
            _out = null;
            Application.Quit(error == null ? 0 : 1);
        }

        static double Pct(float[] sorted, double p) => sorted.Length == 0 ? -1 : sorted[Math.Max(0, Math.Min(sorted.Length - 1, (int)Math.Ceiling(p * sorted.Length) - 1))];
    }
}
