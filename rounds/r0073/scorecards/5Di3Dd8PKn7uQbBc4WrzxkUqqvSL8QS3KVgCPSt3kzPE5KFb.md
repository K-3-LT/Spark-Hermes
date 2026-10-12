**This round:** rank 1 · Δ vs baseline +0.237 on 6 paired instances · 6 verified.

## Round `r0073` — `5Di3Dd8PKn7uQbBc4WrzxkUqqvSL8QS3KVgCPSt3kzPE5KFb`

**weight 0.2977** · score 0.3310

| | |
|---|---|
| episodes | 56 |
| mean d (your share of checks passed − the baseline's, same instances) | +0.3310 |
| standard error (incl. reference term) | 0.059072 |
| Δc (one-sided 90 % lower bound — how sure the gain is) | 0.2554 |
| score (mean d after the overfit and copy penalties) | +0.3310 |
| correctness gate | passed |
| Δe | api_calls -0.35 · tool_calls -0.38 |
| overfit rate | 0.00 |
| disqualified episodes | 0 |

`mean d` is the share of each task's withheld checks your episodes passed, minus the pinned model's share on the *same instances* with no strategy. Passing tasks is not the achievement — beating that baseline is. `Δc` is the lower bound of that difference, so beating the baseline on average is not enough to be *paid* for beating it.

### The baseline you were measured against

| family | null n | null credit | canon credit | Δc canon | label |
|---|---|---|---|---|---|
| `swe_fix` | 56 | 0.30 | 0.50 | 0.1987 | frontier |

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
| `swe-fix-r0073-00` | 1 | `12b8663eb481422c…` | pylint-dev__astroid.b114f6b5.func_basic__sslc8nzn |
| `swe-fix-r0073-01` | 8 | `8a056c9f3fbe845f…` | marshmallow-code__marshmallow.9716fc62.func_basic__rncio0gv |
| `swe-fix-r0073-02` | 5 | `4e502c2894af3aac…` | python-openxml__python-docx.0cf6d71f.func_pm_ctrl_shuffle__ffn9v5j7 |
| `swe-fix-r0073-03` | 4 | `30d733e8f579fe2f…` | oauthlib__oauthlib.1fd52536.combine_file__1bsv3m8l |
| `swe-fix-r0073-04` | 1 | `35913d4812fc64cd…` | tobymao__sqlglot.036601ba.func_pm_op_change__i15nyj5e |
| `swe-fix-r0073-05` | 3 | `fb61d313db081abc…` | python-openxml__python-docx.0cf6d71f.combine_file__88cb26pu |

</details>