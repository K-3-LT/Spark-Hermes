# Fix the injected bug in /testbed

A tool broke working code in the Python project at `/testbed`. Put it back. The tests that
exposed the bug were removed before your episode; the rest of the suite remains. Each broken
test you make pass earns its share of the credit; partial fixes earn real credit. Any
previously-passing test that now fails zeroes the task. Nobody answers questions.

## Rules of this episode

- Edit first: patch the source, then verify. About 25 tool calls before the budget ends. An
  untouched tree scores zero.
- Python and pytest: `/opt/miniconda3/envs/testbed/bin/python` - the `python` on PATH lacks the
  project. Write the full path every time.
- Work only inside `/testbed` (the fix) and `/tmp` (scratch). Nothing else, not even `ls`
  elsewhere: reaching outside ends the episode at zero.
- Put the repro in `/tmp/r.py` with `write_file` - never an `echo` heredoc. The issue's expected
  output is the spec: your repro must print it exactly; a clean exit proves nothing.
- One search per symbol: `grep -rn "<name>" /testbed --include=*.py | grep -v /tests/ |
  head -20`. Never a second search for the same symbol. Per file: two reads (`limit` 60), never
  more. No whole-suite runs - only the changed module's test file.
- If `patch` cannot write a `/testbed` file, once: `cp <file> /tmp/w.py && patch /tmp/w.py && cp
  /tmp/w.py <file>`. Never `sudo`, never `chmod`.
- No network, no pip, no test or config edits, no fixture or golden files, no flags that
  regenerate expected output. From the fix: no pytest/inspect/importlib/subprocess/exec/eval.
- sqlglot only: `/testbed/docs/sqlglot/` holds generated pages with the PRISTINE source - the
  bug did not alter them. After the repro, strip the one relevant page to text in `/tmp`, print
  the suspect function, and change exactly the differing lines. Adapt, never paste.
- A wrong value with no failing line: print the intermediate values along the data path; patch
  where the value first diverges. One value still wrong after a fix is a second altered site -
  find its producer and patch it.
- Tests failing after your edit: narrow or `git checkout -- <file>`. Before DONE: the repro must
  match the expected output line by line; green pytest alone proves nothing. `git diff` must
  contain only intended edits. A comment labeling a change (`# Changed`, `# Reversed`, `# Added`,
  `# Removed`) marks an injected line - fix every hit.

## The bug

Traceback: the last `/testbed` frame is the suspect. Wrong value, no crash: instrument the data
path - print intermediate values, find where the value diverges from what the issue implies, and
patch that statement. One value fixed, another still wrong: a second altered site - find its
producer (getter, helper, sibling) and patch it. Small function (40 lines or fewer) and still
failing: check every statement once. Several symptoms: several sites - same function, siblings,
package neighbors, in that order.

## Stop

Repro matches. Module tests pass. `git diff` shows only the fix. One-line reply, stop.

Revision v24.
