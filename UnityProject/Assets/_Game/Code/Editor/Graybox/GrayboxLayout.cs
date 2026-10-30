using System;
using System.IO;
using System.Linq;
using UnityEngine;

namespace Dispo.Editor.Graybox
{
    /// <summary>JsonUtility mirror of Assets/_Game/Art/Graybox/graybox_layout.json (plan feet, +x east, +y south).</summary>
    [Serializable]
    public sealed class GrayboxLayout
    {
        public const string DataPath = "Assets/_Game/Art/Graybox/graybox_layout.json";
        public const float Ft = 0.3048f;

        public Height[] heights;
        public Spawn spawn;
        public Floor[] floors;
        public Room[] rooms;
        public Wall[] walls;
        public Fixture[] fixtures;
        public RefCam[] cameras;
        public Anchor[] anchors;
        public Stations stations;
        public JarSlots jarSlots;
        public Door[] doors;

        [Serializable] public sealed class Rect { public float x0, x1, y0, y1; }
        [Serializable] public sealed class Height { public string key; public float ft; public string gap; public string note; }
        [Serializable] public sealed class Spawn { public string zone; public float x, y, yaw; }
        [Serializable] public sealed class Floor { public string id, zone; public Rect r; }
        [Serializable] public sealed class Room { public string id, zone, conf; public Rect r; }
        [Serializable] public sealed class Opening { public string id, h, conf, note; public float from, to; }
        [Serializable] public sealed class Wall { public string id, zone, conf, gap; public float ax, ay, bx, by, t; public Opening[] openings; }
        /// <summary>h/@base name a height key; hFt/baseFt (ART-006, ROOM_FIXTURES rows) give feet directly when h is empty.
        /// ART-007: tag (contents / condition) is appended to the object name; yaw (deg) turns each box about its centre.</summary>
        [Serializable] public sealed class Fixture { public string id, zone, h, conf, shape, note, tag; public string @base; public float hFt, baseFt, yaw; public bool solid; public Rect[] rects; }
        [Serializable] public sealed class RefCam { public string tile, zone, room, h, conf, note; public float x, y, yaw, pitch, fov; public string Id => $"REF_{tile}_{room}"; }

        [Serializable] public sealed class Anchor { public string id, zone, conf, note; public float x, y, h, yaw; }
        /// <summary>DEC-039 numbered POS stations, each with a monitor and a DEC-021/026 scale stand. The slice station also gets the SLICE_DESIGN §7 anchors.</summary>
        [Serializable] public sealed class Stations
        {
            public string zone, conf, gap, note, slice;
            public float customerOff, playerOff, monitorW, monitorD, monitorH;
            public Stand stand;
            public Station[] list;
        }
        /// <summary>(x, y) = station centre on the counter's staff edge; staff = compass side (N/E/S/W) the budtender stands on.</summary>
        [Serializable] public sealed class Station { public string reg, staff; public float x, y; }
        [Serializable] public sealed class Stand
        {
            public string conf, gap, note;
            public float w, d, offsetT, topFt, post, board, scaleW, scaleD, scaleH, panelW, panelH, panelT;
            public float[] shelvesFt;
        }
        /// <summary>Jar slots on open shelves and deli back counters. ART-007: numbered by a seeded weighted draw (run.fill), so stocking slots 0..N-1 fills the walls unevenly (REFERENCES_INDEX 8.4).</summary>
        [Serializable] public sealed class JarSlots
        {
            public string zone, conf, gap, note;
            public int seed;
            public float pitch, shelfT;
            public float[] rowsFt;
            public JarRun[] runs;
        }
        /// <summary>rowsFt overrides JarSlots.rowsFt; counter = the run is a back counter (solid to its row height); fill = 0..1 share stocked first.</summary>
        [Serializable] public sealed class JarRun { public string id; public bool alongX, counter; public float yaw, fill; public float[] rowsFt; public Rect r; }
        /// <summary>DOORS.json leaf door (REF-012): each leaf hangs on a pivot at its hinge (x, y); closed pivot yaw = Unity yaw, open adds openAngle.</summary>
        [Serializable] public sealed class Door { public string id, zone, conf, gap, note; public bool pair, open; public float h, t; public Leaf[] leaves; }
        [Serializable] public sealed class Leaf { public string name, pivot; public float x, y, w, yaw, openAngle; }

        public static GrayboxLayout Load()
        {
            var layout = JsonUtility.FromJson<GrayboxLayout>(File.ReadAllText(DataPath));
            if (layout?.walls == null || layout.walls.Length == 0) throw new InvalidDataException($"{DataPath}: no walls parsed");
            return layout;
        }

        public Height H(string key) =>
            heights.FirstOrDefault(h => h.key == key) ?? throw new InvalidDataException($"{DataPath}: unknown height key '{key}'");

        /// <summary>Plan feet to Unity metres (REF-001 mapping X = x*0.3048, Z = -y*0.3048).</summary>
        public static Vector3 ToWorld(float x, float y, float heightFt = 0) => new Vector3(x * Ft, heightFt * Ft, -y * Ft);
    }
}
