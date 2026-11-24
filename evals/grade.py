#!/usr/bin/env python3
# /// script
# requires-python = ">=3.9"
# dependencies = ["pyyaml>=6.0"]
# ///
"""Grade eval answers against the verified answers, then write report.md.

    uv run evals/grade.py evals/results/2026-11-24

A judge model (no tools) compares each answer with the expected one and returns correct / partial / wrong.
Scores: correct = 1, partial = 0.5, wrong = 0. Every verdict keeps the judge's reason, so it can be audited.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
JUDGE = """You grade answers to questions about a wiki. Compare the CANDIDATE answer with the EXPECTED answer.

QUESTION: {q}
EXPECTED: {expected}
GRADING NOTES: {notes}
CANDIDATE: {answer}

Rules:
- "correct": every required fact in EXPECTED is present and right (numbers must match; order matters only if the
  question asks for a ranking). Extra correct detail is fine.
- "partial": some required facts right, some missing or wrong (e.g. 3 of 5 items of a list, right name wrong number).
- "wrong": the main fact is wrong or missing, the candidate refuses, or says it can't find the answer.
- Judge facts, not wording or format.

Reply with JSON only: {{"verdict": "correct" | "partial" | "wrong", "reason": "<one sentence>"}}"""
SCORE = {"correct": 1.0, "partial": 0.5, "wrong": 0.0}


def judge(rec: dict, spec: dict, model: str) -> dict:
    expected = spec["answer"] if isinstance(spec["answer"], str) else json.dumps(spec["answer"], ensure_ascii=False)
    if not rec.get("answer"):
        return {"verdict": "wrong", "reason": f"no answer ({rec.get('error')})"}
    prompt = JUDGE.format(q=spec["q"], expected=expected, notes=spec.get("notes", "none"), answer=rec["answer"])
    p = subprocess.run(["claude", "-p", prompt, "--restricted", "--strict-mcp-config", "--tools", "",
                        "--disable-slash-commands", "--model", model, "--no-session-persistence",
                        "--output-format", "json"], capture_output=True, text=True, timeout=300)
    text = json.loads(p.stdout).get("result", "") if p.stdout.strip().startswith("{") else ""
    try:
        return json.loads(text[text.index("{"): text.rindex("}") + 1])
    except ValueError:
        return {"verdict": "wrong", "reason": f"judge output unreadable: {text[:200]!r}"}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("results", type=Path)
    ap.add_argument("--model", default="opus", help="judge model")
    ap.add_argument("-j", type=int, default=6)
    ap.add_argument("--force", action="store_true", help="re-grade answers that already have a verdict")
    a = ap.parse_args(argv)
    specs = {}
    for f in (ROOT / "evals").glob("*.yaml"):
        s = yaml.safe_load(f.read_text())
        for q in s["questions"]:
            specs[q["id"]] = {**q, "wiki": s["wiki"]}
    recs = [json.loads(p.read_text()) for p in sorted(a.results.glob("*/*.json")) if p.parent.name != "workdir"]

    def grade(rec):
        if "verdict" not in rec or a.force:
            rec.update(judge(rec, specs[rec["id"]], a.model))
            (a.results / rec["arm"] / f"{rec['id']}.json").write_text(json.dumps(rec, ensure_ascii=False, indent=1))
            print(f"{rec['arm']:5} {rec['id']:8} {rec['verdict']:8} {rec.get('reason', '')[:90]}", flush=True)
        return rec

    with ThreadPoolExecutor(a.j) as ex:
        recs = list(ex.map(grade, recs))
    write_report(a.results, recs, specs)


def write_report(out: Path, recs: list, specs: dict):
    meta = json.loads((out / "meta.json").read_text()) if (out / "meta.json").exists() else {}
    arms = sorted({r["arm"] for r in recs}, key=lambda x: (x != "web", x))
    kinds = ["lookup", "compare", "aggregate", "multi-hop"]
    wikis = sorted({r["wiki"] for r in recs})

    def acc(rows):
        return f"{100 * sum(SCORE.get(r.get('verdict'), 0) for r in rows) / len(rows):.0f}%" if rows else "–"

    def col(rows, k):
        vals = [r.get(k) or 0 for r in rows]
        return sum(vals) / len(vals) if vals else 0

    L = [f"# Eval results ({out.name})", "",
         f"Answering model: `{meta.get('model', '?')}` through `claude -p --restricted`. "
         f"`web` = WebSearch + WebFetch only; `skill` = the same plus fandom-kb with pre-built KBs. "
         f"Score: correct 1, partial 0.5, wrong 0.", "",
         "| | " + " | ".join(arms) + " |", "|---|" + "---|" * len(arms),
         "| **overall** | " + " | ".join(acc([r for r in recs if r["arm"] == arm]) for arm in arms) + " |"]
    for k in kinds:
        L.append(f"| {k} | " + " | ".join(acc([r for r in recs if r["arm"] == arm and r["kind"] == k]) for arm in arms) + " |")
    for w in wikis:
        L.append(f"| {w} | " + " | ".join(acc([r for r in recs if r["arm"] == arm and r["wiki"] == w]) for arm in arms) + " |")
    L.append("| avg cost | " + " | ".join(f"${col([r for r in recs if r['arm'] == arm], 'cost_usd'):.3f}" for arm in arms) + " |")
    L.append("| avg time | " + " | ".join(f"{col([r for r in recs if r['arm'] == arm], 'seconds'):.0f}s" for arm in arms) + " |")
    L.append("| avg turns | " + " | ".join(f"{col([r for r in recs if r['arm'] == arm], 'turns'):.1f}" for arm in arms) + " |")
    sk = [r for r in recs if r["arm"] == "skill" and "used_kb" in r]
    if sk:
        used = [r for r in sk if r["used_kb"]]
        L += ["", f"Skill arm used the knowledge base on **{len(used)}/{len(sk)}** questions: "
              f"accuracy {acc(used)} when it did, {acc([r for r in sk if not r['used_kb']])} when it didn't."]
    L += ["", "## Per question", "", "| id | kind | question | " + " | ".join(arms) + " |", "|---|---|---|" + "---|" * len(arms)]
    by = {(r["id"], r["arm"]): r for r in recs}
    for qid in sorted({r["id"] for r in recs}):
        s = specs[qid]
        L.append(f"| {qid} | {s['kind']} | {s['q']} | " + " | ".join(by.get((qid, arm), {}).get("verdict", "–") for arm in arms) + " |")
    L += ["", "## Verdicts", ""]
    for qid in sorted({r["id"] for r in recs}):
        s = specs[qid]
        L += [f"### {qid}: {s['q']}", "", f"Expected: {s['answer'] if isinstance(s['answer'], str) else json.dumps(s['answer'], ensure_ascii=False)}", ""]
        for arm in arms:
            r = by.get((qid, arm))
            if r:
                ans = (r.get("answer") or r.get("error") or "").strip().replace("\n", " ")
                L.append(f"- **{arm}** ({r.get('verdict')}, {r.get('seconds')}s, ${r.get('cost_usd') or 0:.3f}): {ans[:400]}"
                         f"\n  - judge: {r.get('reason', '')}")
        L.append("")
    (out / "report.md").write_text("\n".join(L), encoding="utf-8")
    print(f"→ {out / 'report.md'}", file=sys.stderr)


if __name__ == "__main__":
    main()
