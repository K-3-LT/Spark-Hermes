"""Round bests: for each of the round's bugs, the highest credit any miner's strategy has reached so far.

A log, not a score: refreshed while a round evaluates (`progress.best` in `docs/live/live.json`, from
`orchestrate._progress`), and the final ones kept at close (`~/.spark-hermes-state/rounds/<rid>/close/bests.json`).
They are computed from the current round's episodes only, so a new round starts with none.

An episode's credit is the share of the bug's hidden tests that pass (0 when disqualified or void, `grade.py`), so a
best is shown with the tests behind it: `fixed` of `tests` hidden tests. The baseline (`null`) and the reference
strategy (`canon`) are not miners and never hold a best; the baseline's own credit is kept beside it for comparison.
Every strategy that ties the best holds it.
"""

from __future__ import annotations

REFERENCE = frozenset({"null", "canon"})
_EPS = 1e-9


def tasks_view(episodes: list[dict], round_id: str) -> dict[str, dict]:
    """{surface: {"tasks": {task_id: {credit, void, dq, tests}}}} from graded episodes, the shape `_progress` reads
    off the worker, so the close and the live board compute bests the same way."""
    out: dict[str, dict] = {}
    for e in episodes:
        if e.get("round_id") != round_id or not e.get("surface") or not e.get("task_id"):
            continue
        broken = (e.get("detail") or {}).get("broken") or {}
        out.setdefault(e["surface"], {"tasks": {}})["tasks"][str(e["task_id"])] = {
            "credit": float(e.get("credit") or 0.0),
            "void": bool(e.get("void")),
            "dq": bool(e.get("disqualified")),
            "tests": len(broken) or None,
        }
    return out


def round_bests(by_surface: dict) -> dict[str, dict]:
    """{task_id: {credit, by, fixed, tests, baseline}} — per bug, the highest credit among the miners' finished,
    non-void episodes, every strategy that reached it, the hidden tests behind it, and the baseline's credit."""
    best: dict[str, dict] = {}
    for surface, row in by_surface.items():
        if surface in REFERENCE:
            continue
        for task, ep in ((row or {}).get("tasks") or {}).items():
            if ep.get("void"):
                continue
            c = 0.0 if ep.get("dq") else float(ep.get("credit") or 0.0)
            b = best.get(task)
            if b is None or c > b["credit"] + _EPS:
                best[task] = {"credit": c, "by": [surface], "tests": ep.get("tests")}
            elif abs(c - b["credit"]) <= _EPS:
                b["by"].append(surface)
                b["tests"] = b["tests"] or ep.get("tests")
    base = ((by_surface.get("null") or {}).get("tasks")) or {}
    out = {}
    for task in sorted(best):
        b = best[task]
        n = b["tests"]
        bt = base.get(task)
        out[task] = {
            "credit": round(b["credit"], 4),
            "by": sorted(b["by"]),
            "fixed": round(b["credit"] * n) if n else None,  # credit = fixed / tests (0 after any regression)
            "tests": n,
            "baseline": None if bt is None or bt.get("void") else round(float(bt.get("credit") or 0.0), 4),
        }
    return out
