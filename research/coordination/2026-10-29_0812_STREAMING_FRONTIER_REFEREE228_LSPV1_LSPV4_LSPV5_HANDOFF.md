# STREAMING-FRONTIER-REFEREE228, LSPV-2 to LSPV-1/3/4/5

29 October 2026, 08:12 PDT. **ADD ONLY**. All five existing roles, task identities, enabled states and staggered schedules are unchanged. Both hypothetical universes remain under investigation. Neither P=NP nor P!=NP is proved.

## One missing lemma and four falsifiable proposals

Missing: a uniform fully charged effective procedure that obtains a *repeatably closed*, physically smaller decision-equivalent child on **all** ordinary SAT inputs, or an independent all-program contradiction in one model's simultaneous time/space limits.

1. Native sequential tape: can the already-known four-live-name cyclic exact22 frontier be implemented with no hidden O(n) occurrence table? **YES, RESTRICTED PROVED** with paid source scans and O(log N) writable cells.
2. Can one fixed static b=q=O(log N) boundary/backdoor architecture cover unbounded connected exact22? **NO under the specific syntactic assumptions, PROVED prior and independently checked**.
3. Does unsigned connected incidence + every-variable exactly 2 positive and 2 negative occurrences determine SAT? **NO, FALSIFIED** by same-scope, same-quotas connected exact22 UNSAT W1 and SAT W1' obtained by two opposite flips of the x1 literal signs.
4. Can dynamic existential projection + shared circuits/BDDs/Tseitin provide a general single recursive SAT child of length N^lambda with same-class closure? **OPEN**; code cap and physical growth do not provide guarantee.

## Precise restricted theorem, model and numerical controls

For n divisible by three, take the n signed cyclic triples on indices (i,i+1,i+2) mod n together with n/3 disjoint block triples (3j,3j+1,3j+2), signed to ensure exactly two occurrences of each polarity per name. Parser validates a canonical encoded order, all signs/identifiers/separators, strictness, and every degree quota with *n paid rescans* of a read-only sequential input tape. Frontier DP retains the first two wrap-around variables plus the last two live variables; at most four live bits, 16 states, four just-closing clauses, 32 candidates/stage. On one read-only sequential input tape plus one writable tape:

`T2=O(n*N*polylog(N))`, `S2=O(log N)`, input head moves `O(n*N)`, input sweeps/rewinds O(n), one decision bit. The source has N=Theta(n log(n+2)) physically encoded bits; no assumption of constant-cost random jumps. These are mathematical *algorithm construction bounds* rather than Python heap measurements. One read/write tape simulator: conservatively `T1=O(n*N^2*polylog N)`, `P1=O(N)` including initial source. A fixed UTM receives a compiled finite program and must pay its own simulation overhead. No native indexed RAM time-space implication is asserted.

Reproducer reran byte-identically: 65 valid signed exact22 cycle sources n=3,6,9,12,15 all matched brute-force SAT, three malformed encodings rejected; exemplar `(n,bytes,input_head_moves,max_states)` (3,40,524,4), (6,78,1954,13), (9,116,4296,15), (12,167,8189,16), (15,217,13243,16). It also independently checked 32,768 assignments on W1 and W1' (same unsigned scopes, balanced signs and graph; opposite labels). Separate sign probe exhaustively covered all 6^3=216 and 6^6=46,656 balanced patterns and sampled 100,000 each at n=9,12, finding no UNSAT on that *special* cyclic grammar; all-label SAT for arbitrary exact22 is demonstrably false (W1). Finite findings are COMPUTATIONAL, not all-size theorems.

Independent archive replay: `python3 audit.py` produced byte-identical JSON to archived `results.json`, SHA256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca`; original totals 4,680 boundary subsets, 7,191 local discovery checks, 139 brute-force checks. Static bound, reread under exact grammar: k<=4b, n<=3b+12bq, b+q>=sqrt(n/3)-1/4 for b>0; b=0 forces q>=n/3. This is not a general time lower bound.

## Code and theorem searches (actual repository, file, blob)

- `arminbiere/cadical/src/elim.cpp` @ `c401152c7a733803d0b407d98e8a295ab44f7e99`: bounded elimination caps resolvents and stores extension clauses. https://github.com/arminbiere/cadical/blob/c60730422e758ef1cebe7aeddf2dda31c996bf04/src/elim.cpp
- `berkeley-abc/abc/src/bdd/cudd/cuddAndAbs.c` @ `a321afdc2eff29c1400a735004cf163d6e5ece3d`: `Cudd_bddAndAbstractLimit` returns NULL when node budget is exceeded. https://github.com/berkeley-abc/abc/blob/b6e16bddb089b3dd386c7c28a4ac26b410076b6f/src/bdd/cudd/cuddAndAbs.c
- `crillab/d4/core/Main.cc` @ `cc834c9d12dec5f8ba08024c29116a15a581ec54`: actual d-DNNF compilation and projected-variable flags, no worst-case polynomial compiled size. https://github.com/crillab/d4/blob/333370cc1e843dd0749c1efe88516e72b5239174/core/Main.cc
- `openai/math/preprints/Polynomial-Time-Unitary-Synthesis-from-a-Boolean-Oracle-October-5-2026/build/sections/01-introduction.tex` @ `5ad06c26238e2572e93f68b380f542b2ab1845fe`, `06-recursion.tex` @ `65bf0450f460311b13a11a136db6ada4520cb6f0`, `07-compilation.tex` @ `869be8c325d6d149bf8825c1191b33732d89c2d2`: uniform single-call quantum skeleton, *uncomputed target-dependent Boolean oracle tables*. Not a classical SAT solver or proof of polynomial construction of oracle.
- Existing project `j15marti/pnp/research/agents/lspv-5/2026-10-28_2048_W1-RING-TRANSFER-REFEREE188_repro.py` @ `f4a467c98ccfe0c3e17dee2913b4ed0e8b50a123`: borrowed W1 clause list; fixed-pair flip and brute force newly rerun, no claim prior literature's novelty. Project ARC207, ONE-SHOT-PARITY-PADDING226, RACE77, 227 two-universe analysis retained.
- Primary works checked/referenced in `.bib`: Nishimura-Ragde-Szeider SAT 2004 backdoors; Freuder AAAI 1990 bounded-width CSP; FLMV JACM 2005 SAT time/space; Williams Computational Complexity 2006.

## Exact status and handoffs

**PROVED/EXACT, RESTRICTED:** static-interface theorem (prior), native streaming frontier algorithm on authenticated special cyclic grammar. **FALSIFIED:** universal static log/log interface within that grammar, label from unsigned incidence/degree, any inference of all-SAT contraction from this easy class. **COMPUTATIONAL:** byte-identical source audit, 65 cycle comparisons, 3 malformed, 32,768 W1-pair assignment checks, balanced sign finite probes. **CONDITIONAL:** P=NP and P!=NP are individually compatible with all restricted findings. **OPEN:** universal moving/hierarchical authenticated summary, same-class power-shrinking one-child map, unrestricted all-decider native FLMV contradiction, P versus NP.

Next: LSPV-1 quantify any proposed all-SAT transformation's same-machine outputs; LSPV-2 select growing-cutwidth exact22 hard core and charge twice-applied re-entry from DNNF/BDD/Tseitin; LSPV-3 test sign-position queries and independent side costs; LSPV-4 reproduce symbolic one-/two-tape head movement and peak cells, compare only model-matched native published bounds; LSPV-5 referee the scope-pair labels and report markings. No task/schedule edits. The current Python is a symbol-head instrument, not a finite-state TM simulator or a kernel-verified proof.

## Files

`2026-10-29_0812_LSPV-2_STREAMING_FRONTIER_REFEREE228.tex`, `.pdf`, `.bib`, `_repro.py`, `_raw.json`, `_sign_probe.json`, supplemental `sign_variants_probe.py`, `matched_W1.py`, source archive `audit.py`, `results.json`, and this handoff. The original user Library zip is an independent input, not replaced.
