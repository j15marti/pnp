# QUOTIENT-PIVOT-SWITCH71: exact five-role handoff

**Status:** PROVED/EXACT for the uniform source family and charged adaptive policy; COMPUTATIONAL for 4,534 checks with zero failures; **P versus NP remains OPEN**. No existing agent schedule or scientific routing changed.

## Roles 4 and 5: check the exact construction

For each q>=1, take two variable-disjoint copies F_(b0), F_(b1) of the prescribed 2-SAT orientation chain (each q+3 variables and q+4 binary clauses), plus a shared original switch x. For every source binary clause (l1 OR l2) in arm a∈{0,1}, add private c1,c2,p and two binary clauses each enforcing c1=var(l1), c2=var(l2), p=x XOR a. Add a proper ternary (p OR signed(c1) OR signed(c2)). All source signs remain source-readable.

Exact counts: n=8q+31, m2=12q+48, k=2q+8, M=14q+56. Original variables=2q+7, functional auxiliaries=6(q+4), new free auxiliaries=0. No initial unit clauses; the binary-only CNF is SAT and implies **no literal**. All k physical ternary supports are pairwise disjoint, hence h_raw=k. The full incidence graph is connected.

For fixed x=a, pivots of arm a equal zero and its source binary clauses become active; opposite pivots equal one and satisfy the inactive arm. Thus SAT iff b0!=1^q OR b1!=1^q; #SAT(target)=2^(q+3)(#SAT(F_b0)+#SAT(F_b1)). Each satisfying original-source assignment has exactly one auxiliary extension. On the all-one UNSAT pair, deleting **any one** ternary makes the target SAT.

**Crucial adaptive result:** paid SCC of the 2-CNF backbone equates pivots to x or not-x, and source copies to original variables. ZERO ternaries shrink. In the resulting representation, every genuine ternary contains x or not-x. Consequently h_quotient=1, k_quotient=k. Testing one first-clause candidate from at most three names identifies x in O(k), and branching x once yields k'=0 in *both* branches. Then solve SCC 2-SAT. The solver can use complete DPLL fallback on other inputs, with no answer label supplied in advance.

At the all-one pair, each of 2q independent orientation sign words can be individually flipped to produce SAT with no other field change. Every exact deterministic addressed-word decider must therefore read those 2q fields, an Omega(N/log N) input-acquisition bound, not a universal exponential bound.

Fixed-width grammar: w=ceil(log2(64(22q+88))) bits/word; N=(56q+226)w. Full source reads, 24(q+4) initial implication arcs, SCC, quotient, discovery, two conditional branches, source reconstruction, clause replay, failed tests, space and explicit output are charged. Work and peak live *logical* words are O(n+M).

## Roles 1-3: common hostile controls

The family has exactly three structural states:
- S0 raw k=h=2q+8, no binary-forced literals, initial unit propagation stalls.
- S1 SCC quotient k remains 2q+8 but h drops to 1; no ternary shortened, no SAT decision yet.
- S2 choose discovered x, restrict and propagate; k drops to zero in both branches, one or two SCC decisions, with failed first branch paid.

Use matched SAT b0=(0,1,...,1), b1=1^q and UNSAT b0=b1=1^q. Also use reverse SAT b0=1^q, b1=(0,1,...,1) to force the policy to pay for an unsuccessful first branch. Test any proposed lower-bound potential against h shrinking without k shrinking, source-aware direct scans, caching, signed renaming, alternative representations, and the exact adaptive portfolio. No SAT decider is required to materialize the quotient or enumerate backdoor assignments.

At q=8, the adaptive instrumented events were 3,666 SAT and 4,766 UNSAT, with 1/2 actual pivot branches. The deliberately complete-leaf fixed raw backdoor enumerator has exact theoretical 4,096 SAT and 16,777,216 UNSAT leaves. The large fixed-policy counts are **not actual solver runs** and are not all-decider bounds. At q=1024 n=8,223, M=14,392, N=1,208,970 bits; actual adaptive events 314,562 SAT, 409,134 UNSAT; no DPLL fallback on this family.

## Corpus and missing theorem

Unlike Role 2 QUIET-EQUIV67, SCC substitution here shortens no ternary. Unlike Role 4 SCC-AFFINE-LOCK70, no Gaussian rank processing is needed: SCC reveals a new *one-variable branching interface*. This is a new restricted hostile-control trajectory, not a novel SCC primitive, not a proof of P≠NP.

Role 5 checks the construction, labels, witness counts, all-ternary deletion criticality, no binary backbone forced literal, quotient h=1, 2q sign sensitivity, and resource charges. Independent peer consumption is not yet confirmed.

**First missing lemma:** prove a source-computable all-decider progress obstruction that remains after *any* polynomially acquired representation, variable split, direct decision, recomputation or switching, for a single fixed NP-complete language. All three obligations (measure, work inequality, coverage) are **OPEN**.

## Verified artifacts

- Main report: `research/agents/lspv-4/2026-10-24_0736_LSPV-4_QUOTIENT_PIVOT_SWITCH71.tex`
- Independent mini: `research/agents/lspv-4/2026-10-24_0736_QUOTIENT_PIVOT71_MINI.py`
- Raw summary: `research/agents/lspv-4/2026-10-24_0736_QUOTIENT_PIVOT71_RAW.json`
- Complete full auditor `dual_guard_split71.py` and three raw suite JSON files are included in the downloadable user package; local files are NOT assumed visible to other scheduled runtimes.

The existing five-task coordination remains unchanged.