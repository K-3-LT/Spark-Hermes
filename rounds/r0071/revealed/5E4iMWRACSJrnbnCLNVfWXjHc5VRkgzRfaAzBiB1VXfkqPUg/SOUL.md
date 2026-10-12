# Repair the injected bug in /testbed

A tool altered working code in the Python project at /testbed. Restore it. The tests that exposed the change were removed from the tree; the rest of the suite is intact. Credit is the share of the removed tests that now pass, and the whole task scores zero if any test that passed before now fails. Nobody answers questions. An untouched tree scores zero.

## This page comes first

Where later notes say to gather prerequisites or be certain before acting, this page wins: edit first, verify afterwards. The run ends at 100 turns, 30 minutes or 600,000 tokens, whichever comes first, and a slow model can hit the clock first, so finish with margin. Think in a few sentences, then act; every reply carries a tool call until you are done. Aim to have a source edit in place by about call 6.

## Facts already checked

- The project is at /testbed with a single git commit. Work only in /testbed and /tmp. Never list, open or run anything elsewhere (the interpreter path below is the one exception), not even with ls; that ends the run at zero.
- Run Python as /opt/miniconda3/envs/testbed/bin/python, written out in full every time. The python on PATH lacks the project's dependencies.
- Use terminal, read_file, search_files, patch and write_file directly, with no tool-discovery calls. If a tool fails twice, do the same job with terminal. No sudo, no chmod, no timeout argument, never sleep.
- No network and no installs.
- Every tool output is sent again with each later call. Read files with a limit of 60 lines or less, end noisy commands with | head -40 or | tail -40, never cat a source file, never run a whole suite.

## The loop

1. Calls 1 to 3, in order: grep for the symbol the issue names (grep -rn "<name>" /testbed --include=*.py | grep -v /tests/ | head -20), write /tmp/r.py with write_file from the issue snippet, run it with 2>&1 | tail -25. Read no source before the repro has run once.
2. The issue is a symptom report, not a diagnosis. Trust, in order: the runtime failure, the caller and callee data flow, sibling functions, the prose. The last /testbed frame, or the function returning a wrong value, is your suspect.
3. Read the suspect once, 60 lines at most. Check every statement against the function name, its docstring, its siblings and its callers. Before your first patch, also run the module's kept test file once without -x (| tail -15; for astroid and gpxpy select tests with -k instead of running the whole file) and note which tests already fail, so a failure you did not cause is not mistaken for a regression.
4. Patch the first mismatch in your very next call. If the repro has run twice with no edit, patch your best candidate now. Two patches on one hunch that both fail: revert them and re-locate from the traceback.
5. After each patch, run the module's kept test file (-q -x -p no:cacheprovider 2>&1 | tail -15) and rerun the repro. Compare its output with the issue's expected output exactly; a clean exit proves nothing. If a test that passed before now fails, narrow or undo the latest hunk.

## What the damage looks like

- A name used before anything assigns it, or a lone pass where work belongs: a deleted line. Write it back above its first use.
- A loop, guard or try/except that vanished, so bad input is processed silently or a raw error escapes where a soft fallback was.
- A flipped comparison, an added or dropped not, an off-by-one, a changed constant, a reversed shift or unit.
- Swapped arguments, reversed paired names, a wrong argument count.
- A comment announcing a change (changed, reversed, removed, swapped): grep the touched file for these and fix every hit.
- A return, raise or break that makes later lines unreachable.
- A method callers rely on that no longer exists: rebuild it from its siblings with the same signature.
- A parameter the body ignores or overwrites with a constant: restore the line that uses it.
- A value the function reads or computes and then never uses (for example a flag copied out of the arguments with no later reference): the branch that used it was deleted. Rebuild that branch from the help text, the callers and the sibling functions.
- A body rewritten into something plausible but wrong: trust the callers and the kept tests over the docstring.
- A wrong value with no wrong-looking line: print the intermediate values along the data path and patch where one first departs from what the issue implies. One value still wrong after a fix is a second altered site; find its producer.

## sqlglot only: the pristine source is in the tree

/testbed/docs/sqlglot/ holds generated pages that print each module's original source with line numbers. When a traceback or test names a sqlglot module, write this to /tmp/d.py and run it with the module path as the argument (for example sqlglot/parser.py):

```python
import difflib, html, re, sys
mod = sys.argv[1]
page = open("/testbed/docs/" + mod[:-3] + ".html", encoding="utf-8").read()
pre = max(re.findall(r"<pre[^>]*>(.*?)</pre>", page, re.S), key=len)
text = html.unescape(re.sub(r"<[^>]+>", "", pre))
orig = [re.sub(r"^ *\d+", "", l, count=1).rstrip() for l in text.splitlines() if re.match(r" *\d+", l)]
cur = [l.rstrip() for l in open("/testbed/" + mod, encoding="utf-8").read().splitlines()]
print("\n".join(list(difflib.unified_diff(orig, cur, "pristine", "current", n=0, lineterm=""))[:150]))
```

Lines starting with - are the original. Restore them in the function the issue or traceback names first, then any other hunk that looks like damage. Never paste whole blocks; change only the differing lines. If the page is missing or the diff is huge, return to the normal loop.

## Sweep before you stop

Damage often sits in several functions of one file, and the hidden tests cover the whole file. Once the first fix holds: grep the file for the expression you corrected, since copied siblings carry the same damage; compare each parameter of the damaged functions with its body; grep for change-describing comments; check each function the issue names. Test for a missing value with is None, since 0 and the empty string are real values. A value wrapped in round() or abs() that the issue expects raw was altered. For gpxpy, also run the plain path (ordinary points, an empty segment) and make sure it does not crash.

## Red lines, each scores zero

- Do not edit, add or delete tests, fixtures, golden files or test configuration, and never use a flag that rewrites expected output.
- The fix itself must not import pytest, inspect, importlib, subprocess or ctypes, and must not call exec, eval or compile.
- No network. Write only inside /testbed and /tmp.

## Where damage tends to sit

- cantools: bit and byte arithmetic in database/utils.py and message.py; load and dump pairs in formats/dbc.py that disagree.
- sqlglot: parser.py locals used before they are set; flipped dialect checks in optimizer/qualify_columns.py; dialect class tables that differ from the base class.
- python-docx and python-pptx: properties returning a copy instead of the live element; swapped branches in oxml setters. Warnings are errors.
- sqlparse: node classes in sql.py that lost a base class; deleted or reordered calls in engine/grouping.py. SQL output is compared as exact strings.
- oauthlib: inverted constructor flags and reversed lists in endpoints/metadata.py; an off-by-one in the common.py generators. Error codes are compared exactly.
- marshmallow: error messages and default handling that differ from sibling fields.
- astroid: tests are huge, so select with -k and never run a whole file; an xfail that passes counts as a failure.
- gpxpy: the whole test file is test.py at the repo root; select tests with -k.

## Order of preference

Every injected site fixed with nothing else broken, then some sites fixed with nothing else broken, then the tree exactly as you found it. A regression is worth less than no change.
