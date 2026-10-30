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

        [Serializable] public sealed class Rect { public float x0, x1, y0, y1; }
        [Serializable] public sealed class Height { public string key; public float ft; public string gap; public string note; }
        [Serializable] public sealed class Spawn { public string zone; public float x, y, yaw; }
        [Serializable] public sealed class Floor { public string id, zone; public Rect r; }
        [Serializable] public sealed class Room { public string id, zone, conf; public Rect r; }
        [Serializable] public sealed class Opening { public string id, h, conf, note; public float from, to; }
        [Serializable] public sealed class Wall { public string id, zone, conf, gap; public float ax, ay, bx, by, t; public Opening[] openings; }
        [Serializable] public sealed class Fixture { public string id, zone, h, conf, shape, note; public string @base; public bool solid; public Rect[] rects; }
        [Serializable] public sealed class RefCam { public string tile, zone, room, h, conf, note; public float x, y, yaw, pitch, fov; public string Id => $"REF_{tile}_{room}"; }

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
