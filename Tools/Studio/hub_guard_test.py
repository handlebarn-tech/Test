"""Self-test for hub_guard.py (BUILD-004). Run: python -I Tools/Studio/hub_guard_test.py"""
import json
import os
import subprocess
import sys

GUARD = os.path.join(os.path.dirname(os.path.abspath(__file__)), "hub_guard.py")
HUB = r"C:\Repo"
WORKER = r"C:\Repo\.claude\worktrees\task-x"
HEREDOC = "cat > Docs/Handoffs/X.md <<'EOF'\nRun studio.ps1 unity-build, then Unity.exe -batchmode and blender -b -P gen.py\nEOF"
HERESTRING = "git commit -F - @'\nBUILD: studio.ps1 -File runs Unity.exe -batchmode\n'@"

CASES = [  # (name, payload or raw stdin, expected exit)
    ("hub build blocked", {"cwd": HUB, "tool_name": "PowerShell", "tool_input": {"command": "powershell -NoProfile -File Tools/Studio/studio.ps1 unity-build"}}, 2),
    ("hub & studio blocked", {"cwd": HUB, "tool_name": "PowerShell", "tool_input": {"command": "& .\\Tools\\Studio\\studio.ps1 doctor"}}, 2),
    ("hub unity exe blocked", {"cwd": HUB, "tool_name": "Bash", "tool_input": {"command": "\"C:/Unity/Editor/Unity.exe\" -projectPath UnityProject -quit"}}, 2),
    ("hub batchmode blocked", {"cwd": HUB, "tool_name": "Bash", "tool_input": {"command": "$UNITY -batchmode -quit"}}, 2),
    ("hub blender blocked", {"cwd": HUB, "tool_name": "Bash", "tool_input": {"command": "blender -b -P Tools/Blender/generate.py"}}, 2),
    ("hub dotnet blocked", {"cwd": HUB, "tool_name": "Bash", "tool_input": {"command": "dotnet test UnityProject/x.sln"}}, 2),
    ("worker build allowed", {"cwd": WORKER, "tool_name": "PowerShell", "tool_input": {"command": "powershell -File Tools/Studio/studio.ps1 unity-build"}}, 0),
    ("hub build in worktree path allowed", {"cwd": HUB, "tool_name": "Bash", "tool_input": {"command": f"powershell -File {WORKER}\\Tools\\Studio\\studio.ps1 status"}}, 0),
    ("hub git allowed", {"cwd": HUB, "tool_name": "Bash", "tool_input": {"command": "git merge --no-ff review/wave-3a -m \"Merge: studio.ps1 unity-build fixes, Unity.exe -batchmode\""}}, 0),
    ("hub doc heredoc allowed", {"cwd": HUB, "tool_name": "Bash", "tool_input": {"command": HEREDOC}}, 0),
    ("hub here-string allowed", {"cwd": HUB, "tool_name": "PowerShell", "tool_input": {"command": HERESTRING}}, 0),
    ("hub grep allowed", {"cwd": HUB, "tool_name": "Bash", "tool_input": {"command": "grep -n studio.ps1 Docs/*.md; rg -i unity -n Docs"}}, 0),
    ("hub code edit blocked", {"cwd": HUB, "tool_name": "Edit", "tool_input": {"file_path": HUB + r"\Tools\Studio\studio.ps1"}}, 2),
    ("hub unity edit blocked", {"cwd": HUB, "tool_name": "Write", "tool_input": {"file_path": "UnityProject/Assets/x.cs"}}, 2),
    ("hub notebook edit blocked", {"cwd": HUB, "tool_name": "NotebookEdit", "tool_input": {"notebook_path": HUB + r"\Tools\a.ipynb"}}, 2),
    ("hub doc edit allowed", {"cwd": HUB, "tool_name": "Write", "tool_input": {"file_path": HUB + r"\Docs\BACKLOG.md"}}, 0),
    ("worker code edit allowed", {"cwd": WORKER, "tool_name": "Edit", "tool_input": {"file_path": WORKER + r"\Tools\Studio\studio.ps1"}}, 0),
    ("worker cwd outside worktree allowed", {"cwd": r"C:\Temp", "tool_name": "Bash", "tool_input": {"command": "$UNITY -batchmode -quit"}, "_project": WORKER}, 0),
    ("bad payload allowed", "{not json", 0),
    ("non-object payload allowed", "[1, 2]", 0),
]


def run(stdin, project=HUB):
    env = dict(os.environ, CLAUDE_PROJECT_DIR=project)
    return subprocess.run([sys.executable, "-I", GUARD], input=stdin, capture_output=True, text=True, env=env).returncode


def main():
    failed = 0
    for name, payload, want in CASES:
        got = run(payload) if isinstance(payload, str) else run(json.dumps(payload), payload.pop("_project", HUB))
        ok = got == want
        failed += not ok
        print(f"{'PASS' if ok else 'FAIL'} {name}: exit {got} (want {want})")
    print(f"{len(CASES) - failed}/{len(CASES)} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
