"""PreToolUse guard for the main checkout (DEC-045).

The Studio Hub works in the repo root; workcells that build or code run in
`.claude/worktrees/*`. In the main checkout this blocks execution work
(Unity, studio.ps1, Blender, builds) and edits to code/assets, so the Hub
cannot do worker tasks even by accident. Exit 2 = deny, stderr is shown to Claude.
Any other outcome (exit 0, a crash, python missing) lets the tool run: fail open.
Self-test: python -I Tools/Studio/hub_guard_test.py
"""
import json
import os
import re
import sys

# Real invocations only, not commands whose text merely names a tool (BUILD-004).
EXEC = re.compile(
    r"(-File\s+|&\s*|^|[;|&(]\s*)['\"]?[^\s'\";|&]*studio\.ps1\b"  # studio runner via -File, & or as a statement
    r"|unity\.exe['\"]?[ \t]+-\w"                                  # Unity editor exe with flags
    r"|(^|\s)-batchmode\b"
    r"|(blender\.exe['\"]?|(^|[;|&(]\s*)blender)[ \t][^\n;|&]*?-[bP]\b"  # Blender exe with -b / -P
    r"|\bdotnet\s+(build|test)\b",
    re.I | re.M,
)
# Text that is data, not commands: heredoc bodies, PowerShell here-strings, git commit messages.
DATA = [
    re.compile(r"<<-?\s*['\"]?(\w+)['\"]?[^\n]*\n.*?^\s*\1\s*$", re.S | re.M),
    re.compile(r"@(['\"])\r?\n.*?\r?\n\1@", re.S),
    re.compile(r"\s-m\s+(\"[^\"]*\"|'[^']*')"),
]
BLOCKED_DIRS = ("UnityProject", "Tools")


def in_worktree(path):
    return re.search(r"[\\/]\.claude[\\/]worktrees[\\/]", path or "") is not None


def is_exec(cmd):
    for pattern in DATA:
        cmd = pattern.sub(" ", cmd)
    return EXEC.search(cmd) is not None


def is_code_path(path, root):
    if not path or not root:
        return False
    full = os.path.normcase(os.path.abspath(os.path.join(root, path)))
    return any(full.startswith(os.path.normcase(os.path.join(os.path.abspath(root), d)) + os.sep) for d in BLOCKED_DIRS)


def check(data):
    cwd = data.get("cwd") or ""
    project = os.environ.get("CLAUDE_PROJECT_DIR") or ""
    if in_worktree(cwd) or in_worktree(project):  # a worker whose shell cwd left its worktree is still a worker (REVIEW-W4B)
        return None
    root = project or cwd
    tool = data.get("tool_name", "")
    inp = data.get("tool_input") or {}
    if tool in ("Bash", "PowerShell"):
        cmd = inp.get("command") or ""
        if not in_worktree(cmd) and is_exec(cmd):
            return "execution work (Unity/studio.ps1/Blender/builds) is not allowed in the main checkout. Start a workcell session for it."
    elif tool in ("Edit", "Write", "NotebookEdit"):
        fp = inp.get("file_path") or inp.get("notebook_path") or ""
        if not in_worktree(fp) and is_code_path(fp, root):
            return "code/asset edits under UnityProject/ or Tools/ are not allowed in the main checkout. Start a workcell session for it."
    return None


def main():
    try:
        data = json.load(sys.stdin)
        reason = check(data) if isinstance(data, dict) else None
    except Exception:
        return 0  # never break tools on a malformed payload
    if reason:
        sys.stderr.write("DEC-045 hub_guard: " + reason + "\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
