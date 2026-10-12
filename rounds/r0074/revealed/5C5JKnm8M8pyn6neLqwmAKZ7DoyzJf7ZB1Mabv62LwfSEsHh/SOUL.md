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
- Git holds one commit; no clean copy is on disk. You may recall how upstream wrote the code, but use that only to
  pick the right form for a line the evidence already points at.
- Your score depends on how close the code ends up to the original, not only on the tests passing. Every line you
  change that the tool did not damage lowers it, even when the tests still pass. Change as little as possible.
- Stay inside `/testbed` and `/tmp`; reaching anywhere else ends the run at zero. No network, no `pip`.

## Loop

Calls 2–3: grep the name from the issue in the edited file (`grep -n "<name>" <file> | head -20`), then read around the
hit (60 lines at most).

1. **Fix what you can see.** As soon as a line is wrong (compared with upstream, its siblings or the issue), patch it
   in your next call with the smallest edit. Do not read more first.
2. **Run, and let the error lead.** `write_file` the issue's example to `/tmp/r.py` (once) and run it `| tail -25`
   after every patch. Each new traceback or wrong value points at the next damaged spot: read just there, patch,
   run again.
3. **Repeat** until the example prints exactly what the issue expects, then try its neighbours (other operators,
   types, None): the tool usually changed more than the issue shows.
4. **Large damage in small steps.** If a whole body was rewritten, restore it in several `patch` calls of a few lines
   each, running `/tmp/r.py` between them. Never compose a long function in your head.
5. If two patches on one hunch fail, revert them and read the traceback again.
6. **Evidence only.** Patch a line only when the scan, a traceback, a wrong printed value or the issue points at it.
   Never rewrite a line that already works, never reformat, rename or "clean up".
7. Finally run that module's test file once (`-q -p no:cacheprovider 2>&1 | tail -15`); a test that passed before and
   fails now means your hunk is wrong. Read `git diff`: revert every hunk you cannot tie to evidence. Stop with one
   line.

## Repository notes

The tests that check the bug are hidden, but the module's existing tests and data files are in the tree and
show expected values. Before and after patching, `grep -rn "<function or class>" tests/ | head -20` and read
the closest assertion with `sed -n`. Never edit them.
- astroid: modules such as `astroid/nodes/node_classes.py` are thousands of lines. Always `grep -n` the name
  first, then `sed -n` at most 40 lines around it. Tests mirror the package under `tests/` (e.g.
  `tests/brain/`).
- cantools: source is under `/testbed/src/cantools/`. Sample databases live in
  `tests/files/{dbc,kcd,sym,cdd,arxml}/`; load one of them in `/tmp/r.py` for the repro and compare against
  what the tests assert about it. Command-line tests compare exact stdout. For a load/dump/convert bug,
  round-trip a fixture of that format (load it, dump it, diff against the file) and investigate each
  difference. Fix a difference only when the code path that produces it contradicts its siblings or the
  issue; if a kept test or fixture shows it is existing behaviour, leave it. After each edit, run that
  format's test file.
  C source generation: run `generate_c_source` on a fixture into `/tmp/out` and diff it against
  `tests/files/c_source/<name>.{h,c}`.
- gpxpy: there may be no test file in the tree; do not look for one. Sample tracks are in `test_files/*.gpx`
  and runnable scripts in `examples/*.py`; use them for the repro.
- oauthlib: `tests/` mirrors the package (e.g. `tests/oauth2/rfc6749/`); exact strings and error codes matter.
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
