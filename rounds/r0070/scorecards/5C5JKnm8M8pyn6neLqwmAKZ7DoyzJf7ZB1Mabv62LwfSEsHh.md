**This round:** rank 3 · Δ vs baseline +0.062 on 8 paired instances · 1 verified.

## Round `r0070` — `5C5JKnm8M8pyn6neLqwmAKZ7DoyzJf7ZB1Mabv62LwfSEsHh`

**weight 0.1525** · score 0.0834

| | |
|---|---|
| episodes | 56 |
| mean d (your share of checks passed − the baseline's, same instances) | +0.0834 |
| standard error (incl. reference term) | 0.049548 |
| Δc (one-sided 90 % lower bound — how sure the gain is) | 0.0200 |
| score (mean d after the overfit and copy penalties) | +0.0834 |
| correctness gate | passed |
| Δe | api_calls -0.72 · tool_calls -0.76 |
| overfit rate | 0.00 |
| disqualified episodes | 0 |

`mean d` is the share of each task's withheld checks your episodes passed, minus the pinned model's share on the *same instances* with no strategy. Passing tasks is not the achievement — beating that baseline is. `Δc` is the lower bound of that difference, so beating the baseline on average is not enough to be *paid* for beating it.

### The baseline you were measured against

| family | null n | null credit | canon credit | Δc canon | label |
|---|---|---|---|---|---|
| `swe_fix` | 56 | 0.32 | 0.29 | -0.0325 | frontier |

### Check the grading yourself

8 of 8 withheld commitments re-verified at close: **all match**.

Each instance's withheld half was committed to *before* submissions opened, as `hmac-sha256(salt, canonical_json(withheld))`. The commitment is in the task record — under `rounds/<id>/tasks/` when you were shown the scored tasks, under `rounds/<id>/evaluated/` when you were shown previews — and `rounds/queue.json` carried the digest of those records before the round opened. The salt and the half itself are published now, in `reveal.json`. Recompute it and confirm the criteria you were graded against are the ones that were fixed in advance:

```python
import hashlib, hmac, json
salt, withheld = reveal[task_id]["salt"], reveal[task_id]["withheld"]
body = json.dumps(withheld, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()
"hmac-sha256:" + hmac.new(bytes.fromhex(salt), body, hashlib.sha256).hexdigest()
```

<details><summary>Revealed withheld halves (8) — full record in `reveal.json`</summary>

| task | withheld checks | salt | source |
|---|---|---|---|
| `swe-fix-r0070-01` | 2 | `faabf873f868d1da…` | python-openxml__python-docx.0cf6d71f.lm_rewrite__63e87gh1 |
| `swe-fix-r0070-03` | 2 | `d998a9ffc336a122…` | tobymao__sqlglot.036601ba.combine_module__l83tbwp3 |
| `swe-fix-r0070-11` | 3 | `78c002897e25fe4d…` | andialbrecht__sqlparse.e57923b3.lm_rewrite__n19hsh7s |
| `swe-fix-r0070-12` | 1 | `858ff6f5e4b1317b…` | pylint-dev__astroid.b114f6b5.func_basic__dnxncskq |
| `swe-fix-r0070-14` | 1 | `6ff8a8317c71e0af…` | tobymao__sqlglot.036601ba.func_pm_remove_assign__bcn24cfm |
| `swe-fix-r0070-18` | 2 | `e0550460c34609ec…` | python-openxml__python-docx.0cf6d71f.func_basic__7wy8hhlh |
| `swe-fix-r0070-23` | 3 | `19fd0f96d34a7797…` | tobymao__sqlglot.036601ba.func_pm_remove_cond__uo6i6a3w |
| `swe-fix-r0070-26` | 2 | `879044c67782517b…` | tobymao__sqlglot.036601ba.combine_module__n402i04b |

</details>