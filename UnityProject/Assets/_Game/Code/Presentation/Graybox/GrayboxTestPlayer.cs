using UnityEngine;
using UnityEngine.InputSystem;

namespace Dispo.Presentation.Graybox
{
    /// <summary>First-person capsule for walking the graybox (WASD + mouse, Shift to run). Not the game's player.</summary>
    [RequireComponent(typeof(CharacterController))]
    public sealed class GrayboxTestPlayer : MonoBehaviour
    {
        public float WalkSpeed = 1.4f;
        public float RunSpeed = 3.0f;
        public float LookSensitivity = 0.1f;
        public Transform Eye;

        /// <summary>When set, overrides keyboard input with a world-space direction (PlayMode tests).</summary>
        public Vector3? ScriptedWorldMove;

        CharacterController _controller;
        float _verticalSpeed, _pitch;

        void Awake() => _controller = GetComponent<CharacterController>();

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
                if (mouse != null && mouse.rightButton.isPressed)
                {
                    var d = mouse.delta.ReadValue() * LookSensitivity;
                    transform.Rotate(0, d.x, 0);
                    _pitch = Mathf.Clamp(_pitch - d.y, -80, 80);
                    if (Eye) Eye.localEulerAngles = new Vector3(_pitch, 0, 0);
                }
            }

            _verticalSpeed = _controller.isGrounded ? -1f : _verticalSpeed + Physics.gravity.y * dt;
            _controller.Move((move + Vector3.up * _verticalSpeed) * dt);
        }
    }
}
