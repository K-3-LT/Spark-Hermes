# Restore the damaged code in /testbed

A tool edited working code in the Python project at `/testbed` so that it misbehaves; put it back. The tests that
exposed the damage were removed; the rest of the suite is still there. You earn the share of the removed tests that
pass after your edit, and score zero if any test that passed before now fails. Nobody will answer questions.

## Budget rules (they decide most runs)

- Every tool output is re-sent with every later call, and the run stops at a fixed token budget. Never read a whole
  file: `read_file` always with `offset` and `limit` (at most 60), or `sed -n 'A,Bp'`; `grep -n` first. End shell
  commands with `| head -40`. One whole-file read can end the run.
- Keep each thought to a few sentences, then call a tool. A reply that thinks at length without a tool call wastes
  the turn and can end the run.
- Call `terminal`, `read_file`, `search_files`, `patch`, `write_file` directly; never `tool_call` or `tool_search`.
  If a tool fails twice, do the job with `terminal`.

## Call 1: scan for damage

Your first tool call is this `terminal` command, copied exactly:

```
cd /testbed && B=/opt/miniconda3/envs/testbed/bin; { find . -name '*.py' -not -path './.git/*' -printf '%TY-%Tm-%Td %p\n' | grep -v -e /tests/ -e /test_ -e /docs/ | awk '{c[$1]++;d[NR]=$1;f[NR]=$2} END{for(k in c)if(c[k]>m){m=c[k];M=k} for(i=1;i<=NR;i++)if(d[i]!=M)print "edited after the rest of the tree:",f[i]}' | head -8; [ -x $B/ruff ] && $B/ruff check --no-cache --quiet --output-format concise --select F821,F841,F811,F823 --extend-exclude 'tests,test,test_*.py,docs,doc,examples,benchmarks,scripts,features' .; grep -rnE --include=*.py '[^[:space:]#].*#.*\b([Ss]wap|[Ii]ncorrect|[Bb]ug|[Cc]hanged?|[Ww]rong|[Ii]nvert|[Rr]evers|[Aa]lter|[Ss]ubtle|[Ii]nstead of|[Ss]witch|[Rr]emoved|[Mm]odified)' . | grep -v -e /tests/ -e /test_ -e /docs/ -e '://' -e '# wrong encoding'; [ -d docs/sqlglot ] && $B/python -c "import html,re,pathlib as P,difflib
for h in sorted(P.Path('docs/sqlglot').rglob('*.html')):
 c=P.Path('sqlglot',*h.relative_to('docs/sqlglot').with_suffix('.py').parts);t=h.read_text();k=t.find('id=\x22L-1\x22')
 if not c.exists() or k<0 or c.name=='_version.py':continue
 a=html.unescape(re.sub(r'<[^>]+>','',re.sub(r'<span class=.linenos.>.*?</span>','',t[t.rindex('<',0,k):t.index('</pre>',k)]))).splitlines()
 x=[l for l in difflib.unified_diff([y.rstrip() for y in a],[y.rstrip() for y in c.read_text().splitlines()],lineterm='',n=0) if l[:1] in '+-' and l[:3] not in ('---','+++') and l[1:].strip()]
 if 0<len(x)<=80:print('==',c,len(x),'lines differ from docs (- original, + current)');print(*x[:40],sep=chr(10))"; } 2>/dev/null | head -80
```

`edited after the rest of the tree` names the files the tool changed: the damage is in them, usually all of it, so
work there first. Other lines are leads: an undefined name or an unused variable means a nearby statement was deleted
or reordered; a comment describing a change marks an altered line; under `== sqlglot/<file>` the `-` lines are the
original code. A deleted statement goes back by insertion: keep every line around it.

## Facts

- Python with the project's dependencies: `/opt/miniconda3/envs/testbed/bin/python`, in full every time.
- Git holds one commit; no clean copy is on disk. But you know these open-source projects well: you can recall how
  upstream wrote the damaged code. Your score depends on how exactly the code ends up as upstream wrote it, not only
  on the tests passing. Undo the tool's changes, nothing more, in upstream's own form.
- Stay inside `/testbed` and `/tmp`; reaching anywhere else ends the run at zero. No network, no `pip`.

## Loop: recall, diff, restore

1. **Read** the code the issue is about in the edited file: `grep -n "def \|class " <file> | head -60`, then
   `sed -n 'A,Bp' <file>` for the suspect function and its neighbours (60 lines at most per call).
2. **Recall.** `write_file` `/tmp/orig.py` with that function as upstream wrote it, from memory: same names, order
   and form. For a long function write it in parts (`/tmp/orig1.py`, `/tmp/orig2.py`), never one long thought.
3. **Diff.** `sed -n 'A,Bp' <file> > /tmp/cur.py; diff /tmp/orig.py /tmp/cur.py | head -60`. Each difference is a
   candidate change the tool made.
4. **Restore** each difference that the issue, the function's siblings or the kept tests support, copying upstream's
   form with `patch`. Do not invent a different fix.
5. **Run.** `write_file` the issue's example to `/tmp/r.py` once and run it `| tail -25` after each round of patches.
   A new error or a wrong value points at the next damaged function: repeat 1–4 there. The tool often changed more
   than the issue shows; check every function in the edited files that the issue's path touches.
6. **Finish.** Run that module's test file once (`-q -p no:cacheprovider 2>&1 | tail -15`); a test that passed before
   and fails now means a hunk is wrong. `git diff` must contain only restorations. Stop with one line.

## Repository notes

The tests that check the bug are hidden, but the module's existing tests and data files are in the tree and
show expected values. Before and after patching, `grep -rn "<function or class>" tests/ | head -20` and read
the closest assertion with `sed -n`. Never edit them.
- astroid: modules such as `astroid/nodes/node_classes.py` are thousands of lines. Always `grep -n` the name
  first, then `sed -n` at most 40 lines around it. Tests mirror the package under `tests/` (e.g.
  `tests/brain/`).
- marshmallow: source is under `/testbed/src/marshmallow/`; tests are flat under `tests/` and compare error
  messages exactly.
- oauthlib: `tests/` mirrors the package (e.g. `tests/oauth2/rfc6749/`); exact strings and error codes matter.
- python-docx: source is under `/testbed/src/docx/`; `tests/` mirrors it (e.g. `tests/opc/`, `tests/styles/`,
  `tests/image/`), and sample files are in `tests/test_files/`. Acceptance steps in `features/steps/*.py` and
  `features/*.feature` state expected default values.
- sqlglot: `/testbed/docs/sqlglot/<module path>.html` embeds the original, unbroken source of each module.
  As soon as you know the suspect module (or the repro already prints the expected output), write it out
  and diff it in one call, with `M` set to the module path without `.py`:
  `M=sqlglot/optimizer/qualify_columns; cd /testbed && /opt/miniconda3/envs/testbed/bin/python -c "import re,html,sys;h=open('docs/'+sys.argv[1]+'.html').read();i=h.rindex('<',0,h.index('id=\x22L-1\x22'));p=h[i:h.index('</pre>',i)];p=re.sub(r'<span class=.linenos.>.*?</span>','',p);open('/tmp/orig.py','w').write(html.unescape(re.sub(r'<[^>]+>','',p)).lstrip())" $M && diff /tmp/orig.py $M.py | head -60`
  The docs may be a slightly different version: if the diff is long, read only the suspect function in
  both (`grep -n -A40 "def <name>" /tmp/orig.py`). Copy the original lines of the damaged part with
  `patch`; never write that part yourself. Then rerun `/tmp/r.py` and stop.
  Optimizer and dialect expectations live in `tests/fixtures/optimizer/*.sql` as input/expected pairs.

## Red lines (any one scores zero)

- Edit production source only: never tests, fixtures, golden files, test config or packaging.
- The fix must not use `pytest`, `inspect`, `importlib`, `subprocess`, `exec` or `eval`. No refactors or renames.
