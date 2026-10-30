using UnityEngine;
using UnityEngine.InputSystem;

namespace Dispo.Presentation.Graybox
{
    /// <summary>
    /// First-person capsule (WASD + mouse, Shift to run). GAME-025 / CONTROLS_FLOW_PS1 §1.2: mouse look is always on while the cursor is
    /// locked (no button hold), raw (no smoothing / acceleration / head-bob), pitch ±85°; a click re-locks a free cursor while walking.
    /// Sensitivity, invert Y and FOV are per-machine PlayerPrefs settings (never read by the sim).
    /// </summary>
    [RequireComponent(typeof(CharacterController))]
    public sealed class GrayboxTestPlayer : MonoBehaviour
    {
        public const string PrefSensitivity = "look.sensitivity", PrefInvertY = "look.invertY", PrefFov = "look.fovVertical";
        public const float DefaultSensitivity = 0.10f, MinSensitivity = 0.02f, MaxSensitivity = 0.40f;   // °/count [GDD]
        public const float DefaultFov = 70f, MinFov = 60f, MaxFov = 90f;                                  // vertical ° [GDD]

        public float WalkSpeed = 1.4f;
        public float RunSpeed = 3.0f;
        public float LookSensitivity = DefaultSensitivity;
        public bool InvertY;
        public float FovVertical = DefaultFov;
        public float PitchClamp = 85f;   // [GDD]
        public Transform Eye;

        /// <summary>When set, overrides keyboard input with a world-space direction (PlayMode tests) and freezes look (UI screens, pause).</summary>
        public Vector3? ScriptedWorldMove;

        CharacterController _controller;
        float _verticalSpeed, _pitch;

        void Awake()
        {
            _controller = GetComponent<CharacterController>();
            LoadSettings();
        }

        public void LoadSettings()
        {
            LookSensitivity = Mathf.Clamp(PlayerPrefs.GetFloat(PrefSensitivity, DefaultSensitivity), MinSensitivity, MaxSensitivity);
            InvertY = PlayerPrefs.GetInt(PrefInvertY, 0) == 1;
            FovVertical = Mathf.Clamp(PlayerPrefs.GetFloat(PrefFov, DefaultFov), MinFov, MaxFov);
            ApplyFov();
        }

        public void SaveSettings()
        {
            PlayerPrefs.SetFloat(PrefSensitivity, LookSensitivity);
            PlayerPrefs.SetInt(PrefInvertY, InvertY ? 1 : 0);
            PlayerPrefs.SetFloat(PrefFov, FovVertical);
            PlayerPrefs.Save();
            ApplyFov();
        }

        // CF§1.2: FOV is set at runtime on the player camera, not in the World-owned builder.
        void ApplyFov() { if (Eye && Eye.TryGetComponent<Camera>(out var cam)) cam.fieldOfView = FovVertical; }

        void Update()
        {
            var dt = Time.deltaTime;
            Vector3 move;
            if (ScriptedWorldMove.HasValue)
            {
                move = ScriptedWorldMove.Value * WalkSpeed;
            }
            else
            {
                var kb = Keyboard.current;
                var input = Vector2.zero;
                if (kb != null)
                {
                    if (kb.wKey.isPressed) input.y += 1;
                    if (kb.sKey.isPressed) input.y -= 1;
                    if (kb.dKey.isPressed) input.x += 1;
                    if (kb.aKey.isPressed) input.x -= 1;
                }
                var speed = kb != null && kb.leftShiftKey.isPressed ? RunSpeed : WalkSpeed;
                move = (transform.forward * input.y + transform.right * input.x).normalized * speed;

                var mouse = Mouse.current;
                if (mouse != null)
                {
                    if (Cursor.lockState == CursorLockMode.Locked) Look(mouse.delta.ReadValue());
                    else if (mouse.leftButton.wasPressedThisFrame) { Cursor.lockState = CursorLockMode.Locked; Cursor.visible = false; }
                }
            }

            _verticalSpeed = _controller.isGrounded ? -1f : _verticalSpeed + Physics.gravity.y * dt;
            _controller.Move((move + Vector3.up * _verticalSpeed) * dt);
        }

        /// <summary>Raw look: yaw on the body, clamped pitch on the eye.</summary>
        public void Look(Vector2 counts)
        {
            var d = counts * LookSensitivity;
            transform.Rotate(0, d.x, 0);
            _pitch = Mathf.Clamp(_pitch + (InvertY ? d.y : -d.y), -PitchClamp, PitchClamp);
            if (Eye) Eye.localEulerAngles = new Vector3(_pitch, 0, 0);
        }

        public float Pitch => _pitch;
    }
}
