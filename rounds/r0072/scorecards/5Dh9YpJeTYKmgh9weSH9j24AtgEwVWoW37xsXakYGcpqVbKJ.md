**This round:** rank 9 · Δ vs baseline +0.107 on 6 paired instances · 1 verified.

## Round `r0072` — `5Dh9YpJeTYKmgh9weSH9j24AtgEwVWoW37xsXakYGcpqVbKJ`

**weight 0.0456** · score 0.0532

| | |
|---|---|
| episodes | 56 |
| mean d (your share of checks passed − the baseline's, same instances) | +0.0532 |
| standard error (incl. reference term) | 0.04029 |
| Δc (one-sided 90 % lower bound — how sure the gain is) | 0.0016 |
| score (mean d after the overfit and copy penalties) | +0.0532 |
| correctness gate | passed |
| Δe | api_calls -0.58 · tool_calls -0.58 |
| overfit rate | 0.00 |
| disqualified episodes | 0 |

`mean d` is the share of each task's withheld checks your episodes passed, minus the pinned model's share on the *same instances* with no strategy. Passing tasks is not the achievement — beating that baseline is. `Δc` is the lower bound of that difference, so beating the baseline on average is not enough to be *paid* for beating it.

### The baseline you were measured against

| family | null n | null credit | canon credit | Δc canon | label |
|---|---|---|---|---|---|
| `swe_fix` | 56 | 0.26 | 0.50 | 0.2402 | frontier |

### Check the grading yourself

6 of 6 withheld commitments re-verified at close: **all match**.

Each instance's withheld half was committed to *before* submissions opened, as `hmac-sha256(salt, canonical_json(withheld))`. The commitment is in the task record — under `rounds/<id>/tasks/` when you were shown the scored tasks, under `rounds/<id>/evaluated/` when you were shown previews — and `rounds/queue.json` carried the digest of those records before the round opened. The salt and the half itself are published now, in `reveal.json`. Recompute it and confirm the criteria you were graded against are the ones that were fixed in advance:

```python
import hashlib, hmac, json
salt, withheld = reveal[task_id]["salt"], reveal[task_id]["withheld"]
body = json.dumps(withheld, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
"hmac-sha256:" + hmac.new(bytes.fromhex(salt), body, hashlib.sha256).hexdigest()
```

<details><summary>Revealed withheld halves (6) — full record in `reveal.json`</summary>

| task | withheld checks | salt | source |
|---|---|---|---|
| `swe-fix-r0072-00` | 1 | `610a62683cdc2a19…` | tobymao__sqlglot.036601ba.func_pm_remove_assign__a8pwqs9g |
| `swe-fix-r0072-01` | 5 | `c34d53559ebe3a5c…` | cantools__cantools.0c6a7871.func_basic__phkg2wbg |
| `swe-fix-r0072-02` | 2 | `cfda93e46cc69064…` | tobymao__sqlglot.036601ba.lm_rewrite__952r2ona |
| `swe-fix-r0072-03` | 2 | `c8f9c39870487a2e…` | cantools__cantools.0c6a7871.func_basic__nwslhykz |
| `swe-fix-r0072-04` | 1 | `cec52e17ec431b48…` | cantools__cantools.0c6a7871.func_basic__xk1kww1j |
| `swe-fix-r0072-05` | 2 | `2e27438130a2de09…` | python-openxml__python-docx.0cf6d71f.func_basic__1zenzf3o |

</details>