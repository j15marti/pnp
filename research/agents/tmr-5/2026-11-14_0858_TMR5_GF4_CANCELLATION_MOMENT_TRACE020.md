# TMR-5/020: GF(4) semantic cancellation and a full-moment machine-trace firewall

**Date:** November 14, 2026, 08:58 PST, America/Los_Angeles. **Role:** TMR-5, new PNP Machine Bottleneck Redteam and synthesis agent. **Status:** peer TMR-3/023 GF4-OR23 and TMR-4/023 MC23 receive favorable *restricted mathematical* review below; the paired all-r counterexamples below are **CANDIDATE/RESTRICTED** pending independent TMR-1/TMR-2 review; experiments **COMPUTATIONAL**; **P versus NP OPEN**.

**Exact artifacts:** `experiments/tmr/tmr5_gf4_moment_firewall020.cjs` is the V8-executed standalone checker; `results/raw/tmr/2026-11-14_0852_TMR5_GF4_MOMENT_FIREWALL020_RAW.json` is the unchanged raw result. Independently authored native CPython control is local-only. No new schedule/task was made or modified.

## 1. The two independent peers and their scopes

**TMR-3/023, GF4-OR23:** Let `K=GF(4)=GF(2)[alpha]/(alpha^2+alpha+1)`, with `alpha != 0,1`. For a Boolean function `f:{0,1}^b -> {0,1}`, its canonical multilinear extension is

$$
\widetilde f(z)=\sum_{a\in\{0,1\}^b}f(a)\prod_{i:a_i=1}z_i\prod_{i:a_i=0}(1+z_i).
$$

The `2^b`-query lower bound holds **only when f is given as an opaque Boolean-value oracle**. Run any deterministic correct evaluator on the zero oracle. If it fails to query some `a^*`, the zero and the single-spike oracle at `a^*` are indistinguishable, yet their extension values differ by a product of nonzero factors `alpha` and `1+alpha`. Hence every coordinate must be queried even with unlimited workspace. This independently verifies the **restricted black-box** mathematical argument. A separately supplied white-box OR function factors and admits linear streaming evaluation; it does not have the oracle restriction. The published peer native code/raw were inspected, not rerun byte-for-byte in this run.

**TMR-4/023, MC23:** For a proper three-distinct-variable clause `C` and assignment `a`, with `x_v=(-1)^{a_v}` and `eta_C(v)=(-1)^{b_C(v)}` for its unique falsifying bit, the exact identity is

$$
8\mathbf 1[C(a)=0]=\prod_{v\in V(C)}(1+\eta_C(v)x_v).
$$

Thus the complete count `m` and all signed Walsh moments of degrees 1, 2 and 3 determine the **entire violated-clause function** of `F`, add under appended clauses, and preserve SAT/UNSAT labels after every identical clause suffix. This independently verifies MC23 **as a clause-stream continuation congruence**, not as an all-transition quotient of arbitrary machines. The eight-occurrence opposite-label degree-two collision is genuinely minimal for the fixed-three-variable proper clause language: any UNSAT member must contain all eight forbidden signatures. TMR-4's original report/source/raw were inspected; its V8 and native experiments were not rerun byte-for-byte here.

## 2. New exact infinite family: one GF(4) point has equal SAT and UNSAT values

For `r>=1`, in the fixed-ID proper E3 sign-stream language, define

$$
U_r=\bigwedge_{s\in\{0,1\}^3}\bigwedge_{j=1}^r C_s,
\qquad
S_r=\bigwedge_{j=1}^{8r}C_{000}.
$$

Each clause `C_s` excludes only assignment `s`; every encoded source is exactly `L=24r` sign bits in this restricted grammar, with identifiers implicit. `U_r` is UNSAT and `S_r` has exactly seven satisfying assignments. No statement is made that this is the full ordinary 3-CNF bit length; the ordinary explicit encoding additionally pays identifiers, records and headers, and the two formulae can still be encoded to equal length.

Set `alpha^2=alpha+1`, so `alpha^3=1` and `1+alpha=alpha^2`. For the three-variable Boolean OR function `f_{S_r}(a)=a_1 OR a_2 OR a_3`, its unique multilinear extension is

$$
\widetilde f_{S_r}(z)=1+\prod_{i=1}^3(1+z_i).
$$

Consequently,

$$
\boxed{
\widetilde f_{U_r}(\alpha,\alpha,\alpha)
=0
=\widetilde f_{S_r}(\alpha,\alpha,\alpha)
}
$$

despite their **opposite SAT labels and equal source lengths**. More generally, writing `|a|` for Hamming weight,

$$
\widetilde f(\alpha,\ldots,\alpha)
=\sum_{a:f(a)=1}\alpha^{2b-|a|},
$$

with addition in characteristic two. Hence this one-point summary depends only on three parity-of-counts classes `|a| mod 3`; satisfying witnesses may cancel. The smallest number of variables for *any nonzero Boolean function with zero such evaluation* is `b=2`, e.g. XOR of two variables; for **proper E3 CNF** the one-clause `(x_1 OR x_2 OR x_3)` already supplies a SAT example with zero evaluation. Eight clause occurrences are the smallest possible *equal-m* opposite-label pair when one E3 member is UNSAT.

**Status:** exact elementary field calculation, but independently reviewed project theorem status remains CANDIDATE/RESTRICTED. This falsifies any inference that a single non-Boolean GF(4) extension evaluation distinguishes SAT versus UNSAT, but does **not** contradict TMR-3's sound black-box claim or its proposed use of a richer collection of evaluations.

## 3. A second firewall: full semantic moments do not determine machine cost

For every `r>=1`, let `G_r` be the clause-order permutation of `U_r` obtained by exchanging its first occurrence of `C_{000}` with its first occurrence of `C_{001}`. All other occurrences remain fixed. Then

$$
H_3(G_r)=H_3(U_r),\qquad
\mathrm{SAT}(G_r)=\mathrm{SAT}(U_r)=0.
$$

Consider **one fixed finite-control one-head total decider B for the restricted E3 language**, serving all lengths. It reads every sign bit once from the left endmarker, builds an eight-bit signature mask in finite control, and outputs UNSAT exactly when every signature occurs. Before output, **only if the first completed clause signature equals `000`**, it makes one fully charged left-right traversal of the read-only input, with no other change. Malformed lengths are rejected as MALFORMED. Every input-head motion, output write and halt transition is charged, and only one output cell is visited. For source length `L=24r`:

$$
T_B(U_r)=3(L+1)+2,\qquad
T_B(G_r)=L+3,\qquad
S_B(U_r)=S_B(G_r)=1.
$$

The extra `2(L+1)` physical movements are genuine legal steps. Both labels remain correct for **all restricted E3 sources**, with one fixed finite program. A total correct general 3-SAT decider can implement the same fully charged E3 dispatch before falling back to a total correct exhaustive general solver. This safe dispatch does not yield a general polynomial SAT algorithm.

Therefore *full degree-three source semantic congruence is not a cost-exact, program-independent Turing-machine configuration quotient*. An abstract state that forgets the first clause signature while promising the **same exact trace/cost** for every representative is invalid for this B. A conservative MAY abstraction may retain both paths, but its shortest path can follow the genuinely cheap branch and need not give the delayed representative's time. A source-bound simulation may separately retain the first-signature flag or the exact source and real machine configuration; any consequent lower bound remains algorithm- and source-specific.

**This does not falsify TMR-4/023**, which explicitly disclaims the arbitrary-machine transfer. It provides a physically charged witness that its missing bridge cannot be silently supplied.

## 4. Executed falsification, controls and evidence limitations

**Published exact hosted-V8 function** checked 65,812 complete Boolean functions with `b=1..4`, all GF(4) target evaluations at `alpha^b`, with **0, 3, 63, 16,383 nonempty functions whose extension vanishes** for `b=1,2,3,4` respectively; 2,046 nonzero oracle Lagrange weights for `b<=10`; 128 equal-length opposite-label E3 pairs (`r=1..128`); and 128 full-H3-equal yet unequal charged-time source permutations. The four recorded paired physical traces are `r=1,2,16,128`: for `r=1`, `L=24`, runtimes 77 and 27, with one writable output cell each. Other controls: 589 E3 scanning and malformed cases, nine general CNF fixture families (Horn, Horn UNSAT, 2-SAT, XOR, independent products, auxiliaries, variable renaming, repeated clauses) over 160 Boolean assignments. **Zero assertion failures.** This executes a restricted physical head interpreter, not a generic TM compiler.

**Separately authored native CPython:** the exact source locally available at `/mnt/data/tmr5_audit/tmr5_semantic_bridge020.py` was directly executed on the same mathematical fixtures and independently returned the 65,812/2,046/128/128/589/160 totals with zero final assertion failures. It is local-only, not published in this repository. A preliminary native test made a false auxiliary-variable control prediction of six models for a two-clause lifting. The correct value is twelve because two unused variables remain freely assignable. The assertion failed, was corrected, and the repaired independent run passed. Neither erroneous value has been used to support the theorem. No full preflight script, actual native peer replay, root TeX compilation or unrestricted Turing-machine simulator was executed.

**Physical model note:** the E3 sign-stream has an implicit ordered three-variable universe and no variable-ID fields. The independent general CNF controls are separate truth-table checks. For ordinary explicit inputs a uniform total parser plus fallback must pay record checks, identifiers and all work; the present exact small constants are not asserted for that encoding.

## 5. Required proof chain and explicit next test

The shared separation objective still is

$$
\forall\text{ fixed correct total uniform }A\ 
\forall k\ge1\ \forall C>0\ \forall L_0\ 
\exists F\text{ valid}, |F|\ge L_0:
T_A(F)>C(|F|+1)^k.
$$

Neither the GF(4) oracle bound nor a compact polynomial-size Walsh summary forces any arbitrary decider to execute a prescribed extension-evaluation algorithm. A field evaluation may even lose the SAT bit. A full H3 moment summary preserves clause semantics but not every allowed machine transition. The Williams/Cook-Mertz arbitrary-multitape Tree Evaluation simulation supplies a valid **space upper bound**, not a general joint time/space lower bound. Explicit references: Williams STOC 2025 Theorem 1.1 and Remark 1.6 identify `TIME[t] subset SPACE[sqrt(t log t)]` for multitape TMs and a random-access model limit; the Cook-Mertz procedure is for Tree Evaluation, with costly time in the small-space regime. No universal polynomial SAT decision algorithm or lower-bound potential was produced.

**NEXT TMR-3/TMR-4/TMR-1 joint target:** extract an ACTUAL machine block node function `F_v` from the Williams block-respecting construction, not just a generic oracle. Exhibit one explicit source and machine where a proposed cheaper polynomial representation does or does not preserve **all interpolation identities needed by the actual algorithm**. Charge its bit-generation, physical input reads, dynamic dependencies, extension arithmetic, caching, recomputation and total peak space on the **same machine**. TMR-2 should review the cancellation families and TMR-5 should independently replay the exact physical node generator and source-bound abstraction before promoting any transfer. The computational difficulty of composition for all arbitrary machines remains OPEN.

**Corpus and preservation:** TMR directive SHA `47459817e66dccf1f3079e6c724c0fd2643e7bc4`, complete proof1 SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343` (28,714 chars), full authentic proof2 Git blob SHA `930c5eeddafce656717f28055a7a9a755f44737c` (1,051,196 chars), complete main.tex SHA `5ec8fffb16ec9a7f262e60321bf5aad172d153d8` (2,542,866 chars), AGENTS.md, CODEX.md, project skill, all latest TMR handoffs, latest issue #3 comments, originals for TMR-3/023, TMR-4/023, TMR-2/022 and TMR-5/019. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root main.tex requires TMR-5-only synthesis of restricted findings, without promoting any OPEN node. No schedules altered.

## Sources

1. TMR-3/023, `research/agents/tmr-3/2026-11-14_0842_TMR3_GF4_ORACLE_COMPOSITION_FIREWALL023.md` and source/raw listed above.
2. TMR-4/023, `research/agents/tmr-4/2026-11-14_0836_TMR4_MOMENT_CONGRUENCE_AND_QUOTIENT_COUNTEREXAMPLE023.md`.
3. TMR-2/022, `research/agents/tmr-2/2026-11-14_0823_TMR2_MAXSAT_WALSH_SIGN_ROBUSTNESS022.md`.
4. R. Ryan Williams, *Simulating Time With Square-Root Space*, STOC 2025, DOI https://doi.org/10.1145/3717823.3718225, author PDF https://people.csail.mit.edu/rrw/time-vs-space.pdf. Theorem 1.1, Section 3 and Remark 1.6 inspected directly, including rendered page 3.
5. James Cook and Ian Mertz, *Tree Evaluation is in Space O(log n log log n)*, STOC 2024, DOI https://doi.org/10.1145/3618260.3649664. Cited for the original space-efficient Tree Evaluation method as used in Williams; no direct theorem about polynomial-time small-space evaluation is imported.
6. P. Cousot and R. Cousot, *Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints*, POPL 1977. Model-consistent MAY simulations are a methodological restriction, not a resource separation theorem.

END_OF_REPORT::TMR-5::020::2026-11-14_0858_PST
