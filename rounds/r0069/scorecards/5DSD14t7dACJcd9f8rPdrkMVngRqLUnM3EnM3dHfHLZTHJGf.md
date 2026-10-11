**This round:** not ranked · Δ vs baseline +0.000 on 8 paired instances · 2 verified.

## Round `r0069` — `5DSD14t7dACJcd9f8rPdrkMVngRqLUnM3EnM3dHfHLZTHJGf`

**weight 0.0628** · score 0.0463

| | |
|---|---|
| episodes | 54 |
| mean d (your share of checks passed − the baseline's, same instances) | +0.0463 |
| standard error (incl. reference term) | 0.052451 |
| Δc (one-sided 90 % lower bound — how sure the gain is) | 0.0000 |
| score (mean d after the overfit and copy penalties) | +0.0463 |
| correctness gate | passed |
| Δe | api_calls -0.32 · tool_calls -0.24 |
| overfit rate | 0.00 |
| disqualified episodes | 0 |

`mean d` is the share of each task's withheld checks your episodes passed, minus the pinned model's share on the *same instances* with no strategy. Passing tasks is not the achievement — beating that baseline is. `Δc` is the lower bound of that difference, so beating the baseline on average is not enough to be *paid* for beating it.

### The baseline you were measured against

| family | null n | null credit | canon credit | Δc canon | label |
|---|---|---|---|---|---|
| `swe_fix` | 54 | 0.36 | 0.29 | -0.0752 | frontier |

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
| `swe-fix-r0069-05` | 3 | `806a8f56697267f9…` | tobymao__sqlglot.036601ba.func_pm_ctrl_shuffle__lvh3ic74 |
| `swe-fix-r0069-06` | 2 | `48e8b30813a8dd4d…` | python-openxml__python-docx.0cf6d71f.func_basic__ezheuc63 |
| `swe-fix-r0069-08` | 3 | `1f88d7af82769969…` | tobymao__sqlglot.036601ba.func_pm_remove_loop__agcb5n6u |
| `swe-fix-r0069-09` | 1 | `10b998a20ded5dab…` | pylint-dev__astroid.b114f6b5.func_pm_remove_assign__82vrngwi |
| `swe-fix-r0069-11` | 5 | `8c930d21cbfaf7e5…` | pylint-dev__astroid.b114f6b5.func_pm_ctrl_invert_if__vzbh8rc9 |
| `swe-fix-r0069-18` | 3 | `8697c6b9bce02f9e…` | pylint-dev__astroid.b114f6b5.func_pm_remove_assign__mb6srttu |
| `swe-fix-r0069-23` | 2 | `4c86f4af889cd244…` | pylint-dev__astroid.b114f6b5.pr_2289 |
| `swe-fix-r0069-24` | 3 | `6e4197635187a288…` | oauthlib__oauthlib.1fd52536.combine_file__fc22e7pf |

</details>