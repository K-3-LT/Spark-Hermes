# Restore the damaged code in /testbed

A tool edited working code in the Python project at `/testbed` so that it misbehaves; put it back. The tests that
exposed the damage were removed before your run and the rest of the suite is still there. You earn the share of the
removed tests that pass after your edit, and the whole task scores zero if any test that passed before now fails.
Nobody will answer questions.

## This page comes first

If other notes tell you to gather prerequisites or to be certain before acting, this page overrides them: act first,
verify after. You have about 25 tool calls and every tool output is sent again with each later call, so long outputs
end runs early. Have a source edit in place by about call 8. Think in a few sentences, then act; every reply carries
a tool call until you are done. An untouched tree scores zero.

## Call 1: scan for damage

Your first tool call is this `terminal` command, copied exactly:

```
cd /testbed && B=/opt/miniconda3/envs/testbed/bin; { find . -name '*.py' -not -path './.git/*' -printf '%TY-%Tm-%Td %p\n' | grep -v -e /tests/ -e /test_ -e /docs/ | awk '{c[$1]++;d[NR]=$1;f[NR]=$2} END{for(k in c)if(c[k]>m){m=c[k];M=k} for(i=1;i<=NR;i++)if(d[i]!=M)print "edited after the rest of the tree:",f[i]}' | head -8; [ -x $B/ruff ] && $B/ruff check --no-cache --quiet --output-format concise --select F821,F841,F811,F823 --extend-exclude 'tests,test,test_*.py,docs,doc,examples,benchmarks,scripts,features' . | tee /tmp/f8; grep -rnE --include=*.py '[^[:space:]#].*#.*\b([Ss]wap|[Ii]ncorrect|[Bb]ug|[Cc]hanged?|[Ww]rong|[Ii]nvert|[Rr]evers|[Aa]lter|[Ss]ubtle|[Ii]nstead of|[Ss]witch|[Rr]emoved|[Mm]odified)' . | grep -v -e /tests/ -e /test_ -e /docs/ -e '://' -e '# wrong encoding'; [ -d docs/sqlglot ] && $B/python -c "import html,re,pathlib as P,difflib
for h in sorted(P.Path('docs/sqlglot').rglob('*.html')):
 c=P.Path('sqlglot',*h.relative_to('docs/sqlglot').with_suffix('.py').parts);t=h.read_text();k=t.find('id=\x22L-1\x22')
 if not c.exists() or k<0 or c.name=='_version.py':continue
 a=html.unescape(re.sub(r'<[^>]+>','',re.sub(r'<span class=.linenos.>.*?</span>','',t[t.rindex('<',0,k):t.index('</pre>',k)]))).splitlines()
 x=[l for l in difflib.unified_diff([y.rstrip() for y in a],[y.rstrip() for y in c.read_text().splitlines()],lineterm='',n=0) if l[:1] in '+-' and l[:3] not in ('---','+++') and l[1:].strip()]
 if 0<len(x)<=80:print('==',c,len(x),'lines differ from docs (- original, + current)');print(*x[:40],sep=chr(10))"; [ -s /tmp/f8 ] && $B/python -c "import ast,difflib,re,sys
k=0
for l in open('/tmp/f8'):
 m=re.match(r'(.+?):(\d+):\d+: F8[24]1',l)
 if not m or k>1:continue
 n=int(m[2]);s=open(m[1]).read();L=s.splitlines();F=[f for f in ast.walk(ast.parse(s)) if isinstance(f,(ast.FunctionDef,ast.AsyncFunctionDef))]
 g=lambda f:[x.strip() for x in L[f.lineno-1:f.end_lineno] if x.strip()]
 t=min([f for f in F if f.lineno<=n<=f.end_lineno],key=lambda f:f.end_lineno-f.lineno,default=0)
 r,b=max([(difflib.SequenceMatcher(None,g(f),g(t)).ratio(),f) for f in F if t and f is not t],key=lambda x:x[0],default=(0,0))
 if r<.35:continue
 A=set(g(t));x=[y for y in g(b) if y not in A and re.match(r'[\w.\[\]]+ ?[-+*/|&]?= ',y)]
 if x:k+=1;print('==',t.name,'lacks these assignments of its sibling',b.name+':');print(*x[:8],sep=chr(10))"; } 2>/dev/null | head -80
```

Empty output means nothing was found: go on with the loop. Otherwise each line is a lead. `edited after the rest of
the tree` names the files the tool changed: the damage is in them, usually all of it, so read those first. An undefined name or a
variable assigned but never used means a nearby statement was deleted or reordered; under `== <function> lacks`
the listed lines of its sibling show what else may be missing there; a comment describing a change (`# Swapped ...`,
`# Changed ...`) marks an altered line; under `== sqlglot/<file>` the `-` lines are the original code. A deleted
statement goes back by insertion: keep every line around it.
Restore the leads that touch the code the issue is about; ignore the rest. Then, in the edited files, take each function
the issue's path goes through, write out how upstream implements it from memory, and compare line by line: each
difference is a candidate. When the issue's example passes, also try its neighbours (other operators, types,
arguments, empty and None inputs) before you stop: the tool rarely breaks only the case the issue shows.

## Facts (already checked)

- The project is at `/testbed`; some packages live under `/testbed/src/<pkg>/`. Git holds one commit and no clean
  copy exists on disk (`/opt/sh-pristine` and site-packages hold the same damaged code). Use git only for the final
  `git diff`.
- You know these open-source projects. For each suspect function, first recall how upstream implements it, then
  compare the current code with that line by line: every difference is a candidate edit. Prefer the upstream form
  where it agrees with the function's siblings, callers and kept tests.
- Python with the project's dependencies and pytest: `/opt/miniconda3/envs/testbed/bin/python`, written in full every
  time; the `python` on PATH lacks them.
- Call `terminal`, `read_file`, `search_files`, `patch`, `write_file` directly; never `tool_call` or `tool_search`.
  If a tool fails twice, do the same job with `terminal`. Omit the terminal `timeout` argument and never sleep.
- Keep outputs small: `grep -n` first, then read at most 60 lines (`read_file` with `offset`/`limit`, or `sed -n`);
  end commands with `| head -40` or `| tail -40`; never `cat` a source file or run the whole test suite.
- Stay inside `/testbed` and `/tmp`, and write only there. Do not list or open anything else, `/ep` and `/runner`
  included: reaching outside ends the run at zero.

## Loop

Call 1 is always the scan below. Calls 2–4 are always, in this order: the locate grep, `write_file` of `/tmp/r.py`,
and running it. Read no source and no tests before the repro has run once; its output decides what you read next.

1. **Locate.** `grep -rn "<name from the issue>" /testbed --include=*.py | grep -v /tests/ | head -20`.
2. **Reproduce.** `write_file` the issue's snippet to `/tmp/r.py` (fix the snippet, never the library, if the snippet
   itself is broken) and run it with the full python path `| tail -25`. The last `/testbed` frame, or the function
   that returns the wrong value, is the suspect. The issue's stated output is the target: match it exactly; a clean
   exit proves little.
3. **Baseline.** Before the first patch, run the test file that covers the suspect module once without `-x`
   (`-m pytest <file> -q -p no:cacheprovider 2>&1 | tail -15`) and note which tests already fail.
4. **Read the suspect once** (60 lines at most) and audit each statement against the function's name, docstring,
   siblings and callers. Typical damage:
   - a name used before anything assigns it, or a lone `pass` where work belongs: a deleted line;
   - a loop, guard, `raise` or `try/except` fallback that vanished;
   - an inverted condition, flipped operator, added or dropped `not`, off-by-one, or changed constant;
   - swapped arguments or paired names, or the wrong argument count;
   - an early `return`/`raise`/`break` that makes later lines unreachable;
   - a method callers rely on that no longer exists: rebuild it from its siblings, same signature;
   - a whole body rewritten into something plausible but wrong: trust callers and kept tests over the docstring.
   If no line looks wrong but a value is, print the intermediate values along the data path in `/tmp` and patch where
   the value first departs from what the issue implies. The audit ends in a patch.
5. **Patch** the first mismatch in your next call, with the smallest edit, then rerun `/tmp/r.py`. If the repro has
   run twice without an edit, patch your best candidate now. If two patches on one hunch both fail, revert them and
   locate again from the traceback.
6. **Check.** Rerun the baseline test file. A test that passed in the baseline and fails now means your latest hunk
   is wrong: narrow or revert that hunk. Then rerun `/tmp/r.py`.
7. **Sweep.** Damage often sits in more than one place: the same function, its siblings, other modules of the package.
   If the output still differs from the issue in one value, that value is another altered site, not original
   behaviour: find what produces it (getter, helper, sibling) in the same file first, then the package, and patch it.
   The issue's list of symptoms is the complete work list; patch only on concrete evidence.
8. **Finish.** Compare the repro's output with the issue's expected output line by line. Read `git diff`, undo anything
   unintended, remove debug prints, and stop with a one-line reply.

## Repository notes

The tests that check the bug are hidden, but the module's existing tests and data files are in the tree and
show expected values. Before and after patching, `grep -rn "<function or class>" tests/ | head -20` and read
the closest assertion with `sed -n`. Never edit them.
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

- Modify production source only: never tests, fixtures, golden files, test configuration or packaging, and never a
  flag that regenerates expected output.
- No network, no `pip`. The fix must not use `pytest`, `inspect`, `importlib`, `subprocess`, `exec` or `eval`.
- No refactors, renames or formatting changes. A regression is worse than an unchanged tree.

## Projects you will meet

| Project | Source | Tests | Watch out |
|---|---|---|---|
| astroid | `astroid/` | `tests/` flat, `tests/brain/` | an xfail test that now passes counts as a failure; warnings are errors |
| cantools | `src/cantools/` | `tests/`, samples in `tests/files/` | command-line tests compare exact stdout |
| python-docx | `src/docx/` | `tests/` mirror the source | warnings are errors |
| python-pptx | `src/pptx/` | `tests/` mirror the source | warnings are errors |
| sqlglot | `sqlglot/` | `tests/`, `tests/dialects/` | `tests/fixtures/` holds golden files |
| oauthlib | `oauthlib/` | `tests/` mirror the source | exact error messages and codes |
| marshmallow | `src/marshmallow/` | `tests/` flat | exact error messages |
| sqlparse | `sqlparse/` | `tests/` flat | exact formatted SQL |
| gpxpy | `gpxpy/` | `test.py` at the root | select tests with `-k` |
