**This round:** not ranked · Δ vs baseline -0.162 on 6 paired instances · 4 verified.

## Round `r0076` — `5EwAJCVFUV1UwBqQpT7JqcEGSGBsM3gwxiJNehTeVKqKqkqc`

**weight 0.0062** · score 0.0042

| | |
|---|---|
| episodes | 38 |
| mean d (your share of checks passed − the baseline's, same instances) | +0.0042 |
| standard error (incl. reference term) | 0.069652 |
| Δc (one-sided 90 % lower bound — how sure the gain is) | 0.0000 |
| score (mean d after the overfit and copy penalties) | +0.0042 |
| correctness gate | passed |
| Δe | api_calls -0.29 · tool_calls -0.25 |
| overfit rate | 0.00 |
| disqualified episodes | 0 |

`mean d` is the share of each task's withheld checks your episodes passed, minus the pinned model's share on the *same instances* with no strategy. Passing tasks is not the achievement — beating that baseline is. `Δc` is the lower bound of that difference, so beating the baseline on average is not enough to be *paid* for beating it.

### The baseline you were measured against

| family | null n | null credit | canon credit | Δc canon | label |
|---|---|---|---|---|---|
| `swe_fix` | 52 | 0.39 | 0.50 | 0.1146 | frontier |

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
| `swe-fix-r0076-00` | 9 | `4fe191befcd85d9d…` | cantools__cantools.0c6a7871.func_pm_ctrl_shuffle__cd4jsy0h |
| `swe-fix-r0076-01` | 1 | `96fd73c6f9caa4bb…` | oauthlib__oauthlib.1fd52536.lm_rewrite__c0hjbwnd |
| `swe-fix-r0076-02` | 2 | `27916b680c2814d8…` | pylint-dev__astroid.b114f6b5.func_pm_ctrl_shuffle__6m3144vw |
| `swe-fix-r0076-03` | 3 | `3b9c02466495f2b7…` | python-openxml__python-docx.0cf6d71f.func_pm_ctrl_shuffle__bc8gr6mb |
| `swe-fix-r0076-04` | 1 | `795265c604622148…` | tobymao__sqlglot.036601ba.func_pm_remove_cond__m7o1jzpd |
| `swe-fix-r0076-05` | 8 | `1e1cbc52d4eaba4f…` | marshmallow-code__marshmallow.9716fc62.func_basic__9qtb0vsu |

</details>