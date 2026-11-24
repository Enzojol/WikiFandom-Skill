#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Run the evals: every question twice, with and without the skill, through headless Claude Code.

    uv run evals/run.py --kb-dir ~/.fandom-kb             # all evals/*.yaml → evals/results/<date>/
    uv run evals/run.py battlenations --model sonnet -j 4

Arms (both `claude -p --restricted`, so user settings, hooks and other plugins stay out):
  web    WebSearch + WebFetch: what Claude has without the skill
  skill  the same + this repo loaded as a plugin, Bash limited to `uv run` / `python3`, KBs from --kb-dir

Then grade with `uv run evals/grade.py evals/results/<date>`.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
PROMPT = ("{q}\n\nAnswer the question as accurately as you can. Be concise: give the answer first, "
          "then one line on where it comes from.")

ARMS = {
    "web": ["--tools", "WebSearch,WebFetch", "--disable-slash-commands", "--allowedTools", "WebSearch", "WebFetch"],
    "skill": ["--tools", "Bash,Read,Glob,Grep,Skill,WebSearch,WebFetch", "--plugin-dir", str(ROOT),
              "--allowedTools", "Bash(uv run *)", "Bash(python3 *)", "Read", "Glob", "Grep", "Skill", "WebSearch", "WebFetch"],
}


def scrub(text, args):
    """Replace machine-specific paths with placeholders so results can be shared as is."""
    if not isinstance(text, str):
        return text
    home = str(Path.home())
    for path, label in ((str(args.kb_dir), "<kb-dir>"), (str(ROOT), "<repo>"), (home, "~")):
        text = text.replace(path, label).replace(path.replace("/", "-"), label)  # Claude Code encodes paths with "-"
    return text


def run_one(arm: str, wiki: str, q: dict, args, out_dir: Path) -> dict:
    out = out_dir / arm / f"{q['id']}.json"
    if out.exists() and not args.force:
        return json.loads(out.read_text())
    cmd = ["claude", "-p", PROMPT.format(q=q["q"]), "--restricted", "--strict-mcp-config", "--model", args.model,
           "--no-session-persistence", "--output-format", "stream-json", "--verbose", *ARMS[arm]]
    env = {**os.environ, "FANDOM_KB_DIR": str(args.kb_dir)}
    t = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=args.timeout, env=env, cwd=args.workdir)
        data, tools = {"result": None, "error": p.stderr[-2000:]}, []
        for line in p.stdout.splitlines():
            try:
                ev = json.loads(line)
            except ValueError:
                continue
            if ev.get("type") == "result":
                data = ev
            elif ev.get("type") == "assistant":
                for block in ev.get("message", {}).get("content", []) or []:
                    if block.get("type") == "tool_use":
                        inp = block.get("input") or {}
                        tools.append({"tool": block.get("name"),
                                      "input": scrub(inp.get("command") or inp.get("query") or inp.get("url")
                                                     or inp.get("skill") or "", args)})
    except subprocess.TimeoutExpired:
        data, tools = {"result": None, "error": f"timeout after {args.timeout}s"}, []
    rec = {"id": q["id"], "wiki": wiki, "kind": q["kind"], "arm": arm, "question": q["q"],
           "answer": scrub(data.get("result"), args),
           "error": scrub(data.get("error") or (data.get("subtype") if data.get("is_error") else None), args),
           "cost_usd": data.get("total_cost_usd"), "turns": data.get("num_turns"),
           "seconds": round(time.time() - t, 1), "denials": data.get("permission_denials"), "tools": tools,
           "used_kb": any("fandom_kb.py" in str(x["input"]) or x["tool"] == "Skill" for x in tools)}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(rec, ensure_ascii=False, indent=1))
    print(f"{arm:5} {q['id']:8} {rec['seconds']:6}s ${rec['cost_usd'] or 0:.3f}  {(rec['answer'] or rec['error'] or '')[:70]!r}",
          flush=True)
    return rec


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("wikis", nargs="*", help="eval files to run (default: every evals/*.yaml with answers)")
    ap.add_argument("--kb-dir", type=Path, default=Path.home() / ".fandom-kb", help="pre-built KBs for the skill arm")
    ap.add_argument("--model", default="sonnet")
    ap.add_argument("--arms", default="web,skill")
    ap.add_argument("-j", type=int, default=4, help="parallel runs")
    ap.add_argument("--timeout", type=int, default=600)
    ap.add_argument("--out", type=Path, default=ROOT / "evals" / "results" / date.today().isoformat())
    ap.add_argument("--force", action="store_true", help="re-run questions that already have a result")
    args = ap.parse_args(argv)
    args.kb_dir = args.kb_dir.expanduser().resolve()
    args.workdir = args.out / "workdir"  # empty working dir: nothing from the repo leaks into the answers
    args.workdir.mkdir(parents=True, exist_ok=True)
    files = [ROOT / "evals" / f"{w}.yaml" for w in args.wikis] or sorted((ROOT / "evals").glob("*.yaml"))
    jobs = []
    for f in files:
        spec = yaml.safe_load(f.read_text())
        for q in spec["questions"]:
            if q.get("answer") in (None, "TODO"):
                continue
            for arm in args.arms.split(","):
                jobs.append((arm, spec["wiki"], q))
    print(f"{len(jobs)} runs, model {args.model}, KBs in {args.kb_dir}", file=sys.stderr)
    with ThreadPoolExecutor(args.j) as ex:
        list(ex.map(lambda j: run_one(*j, args, args.out), jobs))
    (args.out / "meta.json").write_text(json.dumps({"model": args.model, "kb_dir": str(args.kb_dir).replace(str(Path.home()), "~"),
                                                    "files": [f.name for f in files]}, indent=1))


if __name__ == "__main__":
    main()
