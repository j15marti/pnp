# TMR-1/055: Complete-source promise totalization for the pinned #SAT-to-hierarchy pipeline

**2026-11-15 16:11 PST.** Role: TMR-1 / PNP Machine Model Lead. Current authority: [end-to-end agent-owned manuscripts](../../coordination/2026-11-15_END_TO_END_AGENT_MANUSCRIPTS.md), source blob `8451d955f6cd5397de0895f8ebb46e30818842c3`. **P versus NP remains OPEN.**

## Named dependency and candidate, before source audit

**Candidate C1-PROMISE:** A single deterministic bit-time compiler, on every authentic encoded binary-gate shared-circuit input, can construct a width-at-most-three CNF meeting **all** hypotheses of Anthropic's pinned formal counting statement, including (n\ge4), (m\ge2), outer clause-list NoDup, and AllOccur, while preserving the exact number of original satisfying assignments and (m\le4n). This fills the small-instance and all-formula promise gap left by TMR-1/054. It is a *compiler lemma*, not a proof of the source counting theorem or an NP-level lower bound.

Four explicit falsifiers: (F1) new unconstrained variables multiply the count or auxiliary gate assignments cease being unique; (F2) empty/duplicate clauses, tiny (n), missing variables, or tautologies violate the actual Lean predicates; (F3) low-bit-first slot numbering or malformed circuit decoding fails; (F4) authentic parsing/encoding, arithmetic, physical stack simulation or output costs exceed the claimed resource transfer.

### Exact source model and quantifiers

For every (q\ge1), (G\ge0), and well-formed acyclic shared fan-in-two circuit (D) with (q) original input wires, (G) topologically ordered arbitrary 4-bit binary truth-table gates, and one output, one fixed compiler emits (H_D). The source binary encoding is (1^q0\,1^G0), followed by two low-first predecessor indices and a 4-bit truth table per gate, and one low-first output address. With (V=q+G) and (w_C=\lfloor\log_2(\max(2,V))\rfloor+1), source length is
[
B_C=q+G+2+G(2w_C+4)+w_C.
]
Reject out-of-range, forward or missing predecessor addresses, invalid delimiters, nonbinary or truncated words. No graph is preloaded for free. The answer is the integer (# D=|\{x:D(x)=1\}|).

## PROVED/EXACT restricted compiler and all-input normalizer

**Previously verified functional gate step, reconciled from TMR-1/054.** For every real gate (z=f(a,b)), emit the four clauses ((a\ne u)\lor(b\ne v)\lor(z=f(u,v))), (u,v\in\{0,1\}). Exactly one clause forces (z=f(a,b)) for the realized predecessor values. Sharing, repeated operands, constant gate functions, and dead gates do not alter the unique topological gate extension. Add a positive output pin and a tautology on each entirely unused *original input* (which remains counted as an original variable), remove only exact duplicate ordered clause lists. With (u\le q) unused inputs, this yields (n=V\), (m\le4G+1+u\le4V), AllOccur and exact count (# H_D=# D). Clause width at most three, not strict proper three-literal CNF.

**New all-input promise totalization, proved here.** For ANY declared-width-three CNF (H) with (n\ge0) variables, any number of clauses (including empty clauses, duplicate clauses and zero clauses), remove exact duplicate ordered lists, add the two-literal tautology ((x_i\lor\neg x_i)) for each old variable missing from every clause, and set (d=\max(1,4-n)). Add fresh (t_1,\dots,t_d), each forced to zero by ((\neg t_j)), and one distinct tautology ((t_1\lor\neg t_1)).

The output (\widehat H) has
[
n'=n+d\ge4,\quad 2\le m'\le m+n+d+1,\quad \#\widehat H=\# H.
]
Every old assignment has exactly ONE fresh-variable extension, because the (t_j) are all forced zero. Every declared variable occurs, the new clauses are distinct from old clauses because they contain new names, outer duplicates were already removed, and at least (d+1\ge2) clauses remain. For an incoming circuit encoding with (m\le4n),
[
m'\le4n+d+1\le4(n+d)=4n'.
]
This simultaneously covers previously excluded (n=1,2,3) circuits and tiny or unusual CNFs. A missing originally declared variable must *not* simply be deleted: its assignments contribute a factor two to the count. In particular, a tautology is an admissible syntactic coverage obligation, not a forced value.

**Precise formal source word.** Anthropic's pinned `MainResults.encInput` for (k=3) encodes (1^3 0\,1^{n'}0), followed by (m') padded three-slot clauses. Each slot has (w_A=\lfloor\log_2(2n')\rfloor+1) low-bit-first bits; zero is padding, (2i+1) is negative and (2i+2) positive. The exact bit length is
[
B_A=n'+5+3m'w_A\le n'+5+12n'w_A=O(n'\log n').
]
The count is (\le2^{n'}) and the formal output has (n'+1) low-first bits. This is an exact integer count, not merely a YES/NO oracle result.

## Actual source inspection and conditional end-to-end consequence

Read from commit `16a5ce41304fcdaea4e0be7c132e1c361dc26da5` of Anthropic `formal-math`: `eth/MainResults.lean`, `eth/Solution.lean`, `eth/lakefile.toml`, `eth/lean-toolchain`. `MainResults.lean` contains *definitions* rather than a proof and states one finite-alphabet fixed FinTM2 machine (M), one constant (C), and all (k\ge1,n\ge4,m\ge2) admissible formulae. `IsKCNF k` permits clauses shorter than (k) and tautological/repeated literals *within* a clause but requires the outer list `Nodup`. `AllOccur` is syntactic. Time bound:
[
2^{C\min\{km/\sqrt{\log_2 m},\ k^2n\log_2\log_2 n/\sqrt{\log_2n}\}}.
]
`Solution.lean` supplies top-level terms `MainResults.mainTheorem := CountedRoute.mainTheoremHolds` and `MainResults.ethIsFalse := ...`. Its top-level text contains no `sorry` or `axiom`, **but this does NOT independently establish a successful kernel build or the safety of all transitive imports**. Lean is pinned at v4.33.1 and Mathlib at `0df444a360eaa60ab8c11dca51a86af692955474`. Source theorem status: PINNED FORMAL SOURCE CLAIM, independent kernel replay OPEN.

**One-realization transfer, conditional on the pinned counting theorem.** One standard physical multitape machine performs the source authentication, shared circuit->CNF compiler, promise totalizer, low-bit-first encoding, fixed finite-stack TM2 simulation, and exact count output. A fixed finite-state TM2 block has boundedly many push/pop operations over fixed finite alphabets, so physically simulating (T_M) such blocks takes (O(T_M)) local tape actions after conservative (O(B_A^2)) input-stack preparation. We deliberately bound all deterministic parsing, clause comparisons and index arithmetic by (O((B_C+B_A)^4)) bit steps. Thus for the SAME implementation,
[
T_{\rm phys}=O((B_C+B_A)^4+T_M),\qquad
S_{\rm peak}=O(B_C+B_A+T_M).
]
This bound is in all circuit gates, not just original input bits. Since (m'\le4n') and AllOccur gives (n'\le3m'), the (k=3) first exponential arm is at most ((12C+o(1))V/\sqrt{\log_2V}). An original (q)-input circuit with (G=q^4) is **not** thereby handled in (2^{o(q)}) time. No polynomial/sublinear-space guarantee or simultaneous FLMV forbidden pair is established.

**Conditional hierarchy target.** TMR-1/053's Jahanjou–Miles–Viola local-reduction hierarchy witness, if all its source premises and the pinned counting result hold, uses three copies of a size-(s) guessed assignment circuit and (O(n)) decoder gates. For (s=\eta n\sqrt{\log_2n}), the normalized CNF has (n'=3s+O(n)), and count-solver exponent ((36C\eta+o(1))n). Setting (0<\eta<1/(72C)) gives a sub-(2^{n/2}) nondeterministic decider contradiction with a chosen unary nondeterministic hierarchy language. The output is an **infinitely-often \(\Omega(N\sqrt{\log N})\) circuit lower bound for some \(E^{NP}\) language**, not NP, not superpolynomial, not P!=NP. The hierarchy route itself was not independently rebuilt here.

### Same-execution accounting

| Stage | Paid bit-time | Peak live writable bits, same physical run |
|---|---:|---:|
| Source parser, grammar and graph authentication | (O((B_C+1)^2)) | (O(B_C)) |
| Shared gate constraints, normalizer, dedup and encoder | (O((B_C+B_A)^4)) | (O(B_C+B_A)) |
| FinTM2 simulation, paid stack top and output conversion | (O(T_M+B_A^2)) | (O(T_M+B_A)) |
| Decode exact ((n'+1))-bit answer / emit result | (O(n'+B_A)) | (O(n')) |

All failed parse work, indices, addresses, repeated source reads, integer bits and shared identities are included. No network or hidden parallel span. The bound on memory is conservative since the formal source supplies no separate small-space bound.

### Four mandatory gates and hostile controls

| Gate | Status |
|---|---|
| **DISJ sanity** | **PASS (restricted).** DISJ has exponential static cut rank but a compact (O(q))-gate circuit; the compiler preserves the cheap gate count and infers no circuit hardness from rank |
| **Relativization** | **PASS compiler; OPEN NP-level separation.** This source syntactic compiler is compatible with relativization. No nonrelativizing NP-level arrow, algebrization or Natural Proofs closure supplied |
| **Simultaneous DTISP** | **PASS same-run cost ledger; NOT APPLICABLE to an FLMV contradiction.** The only certified workspace is (O(T_M+B_C+B_A)), not a strict sublinear-space bound |
| **Deterministic configuration counting** | **PASS upper-bound control.** On fixed total deterministic read-only-input machines, (T\le2^{O(S+\log N)}), never a work lower bound or an unqualified randomized/quantum bound |

Horn, dual Horn, 2-SAT, affine/Gaussian, treewidth, equality, autarkies, products, padding, selectors, unique-witness rank-one, basis/field effects, compact circuits and cache/sharing remain legal cheap controls. Historical `/341` FAIL as unrestricted UNSAT authority; `/386` RESTRICTED. Unknown operations conservative MAY.

## Actually executed and published evidence

Local Node v22 executed source revision `totalizer055.v2` with xorshift32 seed `20261115` and actual source encoded/decoded. **508 direct CNFs**, **215 source circuits**, **4,675 original valuations**, **32,128 complete valuations including auxiliaries**, **22,728 assertions**, **4 invalid words rejected**, **0 failures**. This finite audit is **COMPUTATIONAL**, not proof of an asymptotic counting algorithm. Exact executed code Git blob `b3e4e6f2c1b9280e45cc4c523b3b6c45fd063536`, immutable raw Git blob `a79e584c2a888f03fd94b690b542b2d3c5b38b7a`, each read back byte-identically on research branch. Source `experiments/tmr/tmr1_totalizer_e2e055.js`; raw `results/raw/tmr/2026-11-15_1611_TMR1_TOTALIZER055_NODE_RAW.json`. The owned LaTeX manuscript compiled locally with pdfLaTeX (five pages), but no Lean build, repository checkout or preflight was executable; no independent mathematical peer review is claimed.

Originals reconciled: TMR-1/053 and /054 reports, executable and original raw, current five peer handoffs, own complete initial manuscript, selected peer manuscripts, issue #3 through November 15 15:51 PST, and the original pinned Anthropic statement/proof-term files. TMR-3 pending PR #164 and TMR-5/051 independent sequential-source audit inspected; neither bridges arbitrary 3-SAT inputs to an improved evaluator. All retired proof trackers untouched. All five agents/titles/schedules unchanged.

**ONE NEXT LEMMA:** Independently rebuild Anthropic's pinned `Solution.lean` with Lean v4.33.1 and pinned Mathlib, validate complete transitive `#print axioms`, confirm the machine semantics and source bit encoding. If any proof term, build, or hidden axiom fails, record a precise counterexample without transferring the advertised claim. Only afterward revisit the separate nonrelativizing NP-level implication.

References: [1] [Pinned Anthropic formalization](https://github.com/anthropics/formal-math/tree/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth), `MainResults.lean`, `Solution.lean`; [2] [Jahanjou–Miles–Viola, Local Reductions](https://eccc.weizmann.ac.il/report/2013/099/), rev. 3 (2014); [3] [OpenAI October 2026 manuscript and documented formalization scope](https://github.com/openai/math/tree/42907c9e999cc00d6abe7a50bfc1023250edd1b9); [4] Williams, [Thinking Algorithmically About Impossibility](https://doi.org/10.4230/LIPIcs.CSL.2015.14).

**Scientific status:** new promise compiler PROVED/EXACT RESTRICTED (independent review OPEN); finite Node evidence COMPUTATIONAL; full #SAT solver-to-hierarchy conclusion CONDITIONAL; NP-level implication OPEN. **P versus NP OPEN.**
