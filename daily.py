"""Entrypoint for the daily scheduled run.

Steps that are pure code (always safe to run):
  1. Fetch new videos and transcripts
  2. Rebuild the static site
  3. Commit and push if anything changed

The analysis + research step (turning new transcripts into SoftwareNews
records) is performed by the curating agent that invokes this script — see
AGENT.md for the runbook.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))


def sh(cmd: list[str], check: bool = True) -> int:
    print(f"\n$ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=str(ROOT), check=check).returncode


def main() -> None:
    sh([sys.executable, "pipeline/run_fetch.py"])
    sh([sys.executable, "docs/build.py"])

    # Commit + push if there are changes.
    rc = subprocess.run(["git", "diff", "--quiet"], cwd=str(ROOT)).returncode
    rc_staged = subprocess.run(["git", "diff", "--cached", "--quiet"], cwd=str(ROOT)).returncode
    if rc == 0 and rc_staged == 0:
        # Check for untracked
        out = subprocess.run(
            ["git", "ls-files", "--others", "--exclude-standard"],
            cwd=str(ROOT), capture_output=True, text=True,
        ).stdout.strip()
        if not out:
            print("[daily] no changes to commit")
            return

    sh(["git", "add", "-A"])
    sh(["git", "commit", "-m", "daily: refresh archive"], check=False)
    sh(["git", "push"], check=False)


if __name__ == "__main__":
    main()
