# Evals

These evals measure whether the skill actually helps: the same questions are answered by Claude with and without it, and graded against answers checked on the live wiki.

## Question files

One YAML file per wiki:

```yaml
wiki: battlenations
synced_at: 2026-11-24      # KB snapshot the answers were verified against
questions:
  - id: bn-001
    kind: lookup            # lookup | compare | aggregate | multi-hop
    q: "In Battle Nations, what is the Riot Trooper's HP at each rank?"
    answer: "70, 85, 105, 120, 140, 155 (ranks 1 to 6)"
    notes: "optional grading notes (what counts as partial)"
    source: https://battlenations.fandom.com/wiki/Riot_Trooper
```

Answers are checked on the live wiki (rendered page or page source), not taken from the knowledge base alone.

## Running

```bash
kb fetch battlenations --yes        # build the KBs the skill arm will use (whole wiki)
uv run evals/run.py --kb-dir ~/.fandom-kb --model sonnet      # → evals/results/<date>/{web,skill}/*.json
uv run evals/grade.py evals/results/<date>                    # judge + evals/results/<date>/report.md
```

- `web` arm: `claude -p --restricted` with WebSearch and WebFetch only, which is what Claude has without the skill.
- `skill` arm: the same, plus this repo loaded with `--plugin-dir`, Bash limited to `uv run` / `python3`, and the pre-built KBs.
- `--restricted` keeps user settings, hooks and other plugins out of both arms. Each run starts in an empty working directory.
- The judge (`opus` by default, no tools) grades correct / partial / wrong and keeps a one-line reason for each verdict.
