"""Shared local paths and the pinned upstream release for the maintained branch."""
from pathlib import Path
import json, subprocess
UP = Path(__file__).resolve().parents[1]
ROOT = UP.parents[1]
CONFIG = json.loads((UP / "zh-upstream.json").read_text(encoding="utf-8"))
TAG = CONFIG["upstream_tag"]
VERSION = TAG.removeprefix("v").removesuffix("-base")
NAME = "Balatro3DS-" + VERSION + "-zh-fix" + str(CONFIG["local_revision"])
WORK = UP / "work"
RELEASE = WORK / "releases" / TAG
OUT = ROOT / "outputs" / ("v" + VERSION + "-zh-fixes")
TOOLS = ROOT / "work" / "cia-tools"

def run(exe, *args):
    p = subprocess.run([str(exe), *map(str, args)], cwd=UP, capture_output=True, text=True)
    if p.returncode:
        raise RuntimeError(p.stdout + p.stderr)
    return p.stdout + p.stderr
