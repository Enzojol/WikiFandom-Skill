# Evals

These evals measure whether the skill actually helps. Each wiki gets a YAML file of questions whose answers someone has checked on the wiki:

```yaml
wiki: battlenations
synced_at: 2026-11-23      # KB snapshot the answers were verified against
questions:
  - id: bn-001
    q: "Which building trains the Heavy Gunner?"
    answer: "..."           # verified on the wiki
    source: https://battlenations.fandom.com/wiki/...
    kind: lookup            # lookup | compare | aggregate | multi-hop
  - id: bn-002
    q: "Top 3 infantry units by HP at max rank?"
    answer: ["...", "...", "..."]
    kind: aggregate
```

Run each question twice, with the skill and without it, and report accuracy per `kind`. The `aggregate` and `compare` questions are where SQL over typed tables should make the biggest difference.

`battlenations.yaml` is a template: fill in the answers after a real `fetch`.
