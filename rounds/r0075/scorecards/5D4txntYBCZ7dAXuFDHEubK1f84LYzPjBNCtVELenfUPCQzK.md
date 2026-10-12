**This round:** not ranked · Δ vs baseline -0.039 on 6 paired instances · 3 verified.

## Round `r0075` — `5D4txntYBCZ7dAXuFDHEubK1f84LYzPjBNCtVELenfUPCQzK`

**weight 0.0456** · score 0.0423

| | |
|---|---|
| episodes | 54 |
| mean d (your share of checks passed − the baseline's, same instances) | +0.0423 |
| standard error (incl. reference term) | 0.057105 |
| Δc (one-sided 90 % lower bound — how sure the gain is) | 0.0000 |
| score (mean d after the overfit and copy penalties) | +0.0423 |
| correctness gate | passed |
| Δe | api_calls -0.38 · tool_calls -0.25 |
| overfit rate | 0.00 |
| disqualified episodes | 0 |

`mean d` is the share of each task's withheld checks your episodes passed, minus the pinned model's share on the *same instances* with no strategy. Passing tasks is not the achievement — beating that baseline is. `Δc` is the lower bound of that difference, so beating the baseline on average is not enough to be *paid* for beating it.

### The baseline you were measured against

| family | null n | null credit | canon credit | Δc canon | label |
|---|---|---|---|---|---|
| `swe_fix` | 54 | 0.34 | 0.50 | 0.1639 | frontier |

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
| `swe-fix-r0075-00` | 5 | `1ed8017af8c3e9b0…` | andialbrecht__sqlparse.e57923b3.func_pm_remove_cond__5xn3knbz |
| `swe-fix-r0075-01` | 6 | `8856b26597bb0552…` | python-openxml__python-docx.0cf6d71f.combine_file__uq3vw9qi |
| `swe-fix-r0075-02` | 1 | `32787587d24e16e8…` | tobymao__sqlglot.036601ba.func_pm_ctrl_invert_if__yusdgxrb |
| `swe-fix-r0075-03` | 2 | `97ca04dc75bd5924…` | tkrajina__gpxpy.09fc46b3.func_pm_ctrl_shuffle__ogjxh6o7 |
| `swe-fix-r0075-04` | 1 | `f1053521215585c0…` | tkrajina__gpxpy.09fc46b3.func_pm_ctrl_shuffle__qakwv18i |
| `swe-fix-r0075-05` | 3 | `4b62230236c68b5f…` | cantools__cantools.0c6a7871.combine_file__fn54v17l |

</details>