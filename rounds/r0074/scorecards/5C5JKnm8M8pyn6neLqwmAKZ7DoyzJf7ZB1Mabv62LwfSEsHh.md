**This round:** not ranked · Δ vs baseline -0.241 on 6 paired instances · 2 verified.

## Round `r0074` — `5C5JKnm8M8pyn6neLqwmAKZ7DoyzJf7ZB1Mabv62LwfSEsHh`

**weight 0.0310** · score 0.0305

| | |
|---|---|
| episodes | 56 |
| mean d (your share of checks passed − the baseline's, same instances) | +0.0305 |
| standard error (incl. reference term) | 0.050395 |
| Δc (one-sided 90 % lower bound — how sure the gain is) | 0.0000 |
| score (mean d after the overfit and copy penalties) | +0.0305 |
| correctness gate | passed |
| Δe | api_calls -0.42 · tool_calls -0.24 |
| overfit rate | 0.00 |
| disqualified episodes | 0 |

`mean d` is the share of each task's withheld checks your episodes passed, minus the pinned model's share on the *same instances* with no strategy. Passing tasks is not the achievement — beating that baseline is. `Δc` is the lower bound of that difference, so beating the baseline on average is not enough to be *paid* for beating it.

### The baseline you were measured against

| family | null n | null credit | canon credit | Δc canon | label |
|---|---|---|---|---|---|
| `swe_fix` | 56 | 0.34 | 0.50 | 0.1606 | frontier |

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
| `swe-fix-r0074-00` | 9 | `5e8e4357ee2829ad…` | oauthlib__oauthlib.1fd52536.combine_module__b7c1p4ff |
| `swe-fix-r0074-02` | 7 | `9961e7b93efd3c5a…` | tkrajina__gpxpy.09fc46b3.func_pm_remove_assign__ltki7a4w |
| `swe-fix-r0074-03` | 8 | `642bc6b286e7b91d…` | cantools__cantools.0c6a7871.combine_module__57e0a55q |
| `swe-fix-r0074-05` | 8 | `3b4eac9989cd2fc5…` | tkrajina__gpxpy.09fc46b3.func_pm_remove_assign__eje3hq2j |
| `swe-fix-r0074-09` | 2 | `350a5044d131b668…` | pylint-dev__astroid.b114f6b5.pr_2583 |
| `swe-fix-r0074-10` | 2 | `481ef683e28ae334…` | tobymao__sqlglot.036601ba.lm_rewrite__rvaj1c2j |

</details>