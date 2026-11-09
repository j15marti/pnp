# LSPV-1/542: source-exact polynomial-evidence macro as a rule-authentication CEGAR control

**2026-11-09 12:08 PST | Route B | PROVED/RESTRICTED (distinct calculus) + COMPUTATIONAL. P versus NP OPEN.**

**Proof-chain nodes:** proposed [P2-L1-542], refining precision/grammar gaps [P2-D1] and [P2-C3]. [P2-B1] (superpolynomial full historical minimum), [P2-B2] (noncircular same-calculus B3), and [P2-C3] remain OPEN. No historic rule/weight or task configuration changes. Both root trackers were read before this report.

## IDEA, precommitted falsifiers, and falsification outcome

**Hypothesis.** Even a source-EXACT abstract proof-cost analysis cannot obtain a general negative certificate from the properties "sound, complete, polynomial-time checker, original-source authentication, positive native node costs" alone: a uniform source-recognizing rule with a polynomial-size witness can collapse an established ordinary-Resolution-hard Tseitin family to ONE paid node in a *different* calculus. This sharpens the earlier [P2-L1-538] external full-source TABLE control, whose witness had exponential bit length. The historical grammar must be used to rule out the macro.

F1: the recognizing checker accepts an even-charge satisfiable source or a modified/malformed source. F2: the certificate necessarily needs exponential bytes or a SAT/UNSAT oracle. F3: the refutation does not authenticate actual source clause occurrences and a globally consistent graph. F4: the rule is already a native accepted inference in historical R_mix341. F1-F3 were rejected by a symbolic argument and finite tests; F4 was **not** established. Indeed the original /341 rule declaration excludes an uncharged multiclause global semantic shortcut, so this is intentionally a DISTINCT calculus. No native R_mix341 proof of cost one is asserted.

## SEARCH: authoritative continuity, duplicates, and research corpus

Read the governing Nov 9 abstract-interpretation coordination handoff (blob 8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b), both complete root trackers (initial proof1 blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2 blob 1a87cf2b7c62641aea2d937ca48249e2477c3acc), current issue #3 through LSPV-3/539, AGENTS.md (4ae90288), CODEX.md (754999f5), and research skill (b8df83a7). Original native semantic declaration LSPV-2/341 is blob c87acd11; LSPV-1/541 auxiliary-name quotient is blob 719cb374; relevant peer review LSPV-3/539 exact 8-bit factor mask, LSPV-5/464 and /465 paid-history retention/finite-label ceiling. Grok's actual GROKPROOF/2026-11-09_1230_PROGRESS.md blob 0ee19c6b and Claude's actual research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex blob 79e4d4e7 provide no full mixed-rule authentication or B3.

**Duplication guard:** LSPV-1/385 (blob 0a43cf70) already proves that unit-paid-node minima may be uncomputable when one rule has unbounded halting-tableau payload, and identifies a computable normalized-witness criterion. LSPV-1/538 (blob 274616ea) already provides a one-paid-node *exponential-evidence* SOURCE_TABLE rule and proves source-side-read dependency. LSPV-2/341 already proves the exact 4h-1 minimum in its declared five-rule calculus. None of those is claimed new here. The specific contribution is an exact **polynomial-evidence** graph/charge recognizer as a hostile control for an entire published Resolution-hard family, with explicit typed source verification, positive cost and executable both-label controls.

Targeted/change-aware actual repository reads: konard/p-vs-np README.md blob 0e0ec77f and scripts/proof_status.json blob 93b77ed3 (finite-machine formalizations, not a general SAT result); blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea and PROOF_PORTFOLIO_BRIDGE_REPORT.md blob 22215cec (scoped bounded projector, not a full-calculus proof); meelgroup/frat-xor format.md blob 986a21aa (distinct theory-step IDs, not native /341), MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd19 (canonical graph-charge encoding), tanyongkiam/cake_lpr README.md blob e94f45e9 (verified format/checker trust boundary), openai/math README.md blob cc5b0a03 (research artifacts with varying verification status). Primary literature: Urquhart [1] proves expander Tseitin exponential lower bounds in ordinary Resolution, not in stronger systems; Cousot-Cousot [2] provides sound overapproximation framework. The tool used general indexed web, not a separate Google-branded interface. No authoritative historical R_mix341 checker was run.

## Established family, exact strict 3-CNF encoding and hard-model statement

Let G=(V,E) be a connected simple cubic graph with h even vertices, n=|E|=3h/2, and a charge vector chi in {0,1}^V with odd parity. Each edge e has one original Boolean variable x_e. For each vertex with incident edges e1,e2,e3, include the four proper signed ternary clauses falsified by each local assignment a in {0,1}^3 of parity different from chi_v:

$$
C_{v,a}=\bigvee_{i=1}^3
\begin{cases}
x_{e_i},&a_i=0,\\
\neg x_{e_i},&a_i=1.
\end{cases}
\qquad \bigoplus_i a_i\ne \chi_v.
$$

The signed source has exactly m=4h clauses, n=3h/2 original variables, and N=Theta(h log(h+2)) explicit indexed bytes on standard graph families. XOR of all vertex equations cancels each edge exactly twice, yielding 0=1, so odd charge is UNSAT. Even charge on connected G has 2^(n-h+1) models.

Urquhart (1987) [1] proves exponential ordinary shared-DAG Resolution lower bounds for appropriate *expanding* graph families using Tseitin constructions. The six tested finite graphs below are semantic/format controls and are **not certified expander-hard instances**. LSPV-2/341 already has a 3h-AND3 plus (h-1)-XOR proof with 4h-1 paid nodes and a matching source-essentiality lower bound for connected simple bridgeless cubic graphs in its DECLARED R_mix341 semantic rules. That existing fast algebraic derivation is mandatory evidence that the ordinary Resolution lower bound does not carry over.

## THEOREM 542.1: polynomial-evidence one-node macro (PROVED/RESTRICTED, distinct calculus)

Define one fixed proof system R_T containing ordinary source-authenticated binary Resolution with unit positive cost and a second unit-positive-cost rule, TSEITIN-CLOSE. The latter has one newly paid conclusion node (false), a witness containing graph endpoints, vertex charges and the ordered list of ALL original clause IDs, and a validator that:

1. parses one original strict signed DIMACS CNF, rejecting malformed header, inconsistent count, nonproper triples, duplicate-variable literals and invalid IDs;
2. checks a connected simple cubic graph with h vertices and 3h/2 edge variables, every edge occurring at exactly two distinct endpoints, and a binary charge at each vertex;
3. reconstructs and compares the complete multiset of 4h original signed clauses against the four forbidden local patterns at each vertex, authenticating every actual source ID, with no free replacement or overlooked clause;
4. verifies the XOR of all vertex charges is 1; only then issues the single paid empty-clause conclusion.

Then, for every such F_(G,chi) with odd charge,

$$
W_{R_T}(F_{G,\chi})=1.
$$

**Proof.** Every vertex's four forbidden-pattern clauses are Boolean-equivalent to its specified parity equation. Every edge appears exactly twice in the XOR of all vertex equations, hence that sum is 0 on the left and 1 on the right. Thus any accepted macro is a sound refutation of the ACTUAL checked source, not a semantic oracle. The graph, charges, clause IDs and all local patterns are finite polynomial-size data; reconstruct, sort, and compare in polynomial time, without performing a SAT decision or trusting unverified hints. Binary Resolution remains sound and refutationally complete for arbitrary UNSAT CNFs and is the fallback. All new conclusions have cost at least one, so a source with no original empty clause cannot have a zero-cost completed proof. The macro supplies a valid single paid empty conclusion for each recognized odd-charge source. Hence the minimum is exactly one. QED.

The graph/witness encoding uses O(h log(h+2)) bits, comparable to the signed source. Sorting/reconstruction and graph tests have conservative polynomial-time upper bounds, for example O(h^2 log(h+2)) word operations for a simple implementation. **One logical inference does not mean one physical machine operation:** source reads, multiset comparison, memory allocation and output remain charged to actual time/space. The rule's proof checker is polynomial in FULL source-plus-certificate bytes, with no oracle.

## THEOREM 542.2: rule-language precision barrier for cost-sound MAY abstractions

Fix the collection C of sound, complete, source-authenticated, polynomial-time-checkable proof systems with positive unit-price derived conclusions, original strict signed CNF sources, and which contains R_T. Suppose an abstract may transition relation A(F) is required to overapproximate proof constructions for **every** system in C and preserve each completed goal with no greater cost. Then on every recognized odd-charge F,

$$
d_A^\#(\alpha(s_F),G^\#)\le 1.
$$

**Proof.** The legal R_T one-step proof is an element of the required concrete union. Cost soundness sends that goal path to an abstract goal path of cost at most one. QED.

This yields a clean *syntax-precision* distinction from prior **source-signature** collision theorems: even retaining the entire exact source is insufficient if the abstract rule universe is weakened to high-level checker/soundness properties. However R_T is **not a verified completion of the fixed historical R_mix341**. R_mix341's historical binary dependency and five-rule grammar, if authenticated, excludes this globally source-reading macro. The theorem applies only to an abstraction intentionally covering the BROADER class C, not necessarily to the narrow fixed R_mix341 abstraction. An attempted abstract unit path must be concretized against the historical checker; if illegal, refine away this rule with an explicit authenticated native-rule exclusion. Never treat an absent rule as a native shortcut.

## ITERATE and computational validation

Published executable source and checked output:

- Executable JavaScript: experiments/arc/lspv1_542_tseitin_source_macro.cjs, blob 2e36a1f9bf60e30661a5f1e0e1aad91f728ef6f1.
- Raw JSON: results/raw/arc/2026-11-09_1204_LSPV1_542_SOURCE_EXACT_MACRO_RAW.json, blob b92dffdf529266e5da32659cb87b988e4295ab62.
- The exact published code bytes were refetched and executed as JavaScript in a separate V8 invocation; 53 assertions passed with zero failures. The implementation compares exact source clause multisets, checks all claimed source IDs, checks the graph/charges, and rejects even-charge, forged charge, forged clause ID, signed literal tamper, missing clause, invalid graph edge and malformed header. No historical native checker was run.
- A separately written Python implementation independently rebuilt the formulae and brute-force evaluated four instances K4, K3,3, cube and Petersen, passing 32 checks, including signed-clause corruption controls. This local independent code is in the reproducibility attachment, not evidence of authoritative historical acceptance.

| Graph control | h | n | m | signed DIMACS bytes | witness JSON bytes | odd models | even models |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| K4 | 4 | 6 | 16 | 163 | 121 | 0 | 8 |
| K3,3 | 6 | 9 | 24 | 239 | 167 | 0 | 16 |
| cube | 8 | 12 | 32 | 340 | 213 | 0 | 32 |
| Petersen | 10 | 15 | 40 | 440 | 259 | 0 | 64 |
| prism(6) | 12 | 18 | 48 | 540 | 311 | symbolically 0 | symbolically 128 |
| prism(8) | 16 | 24 | 64 | 740 | 415 | symbolically 0 | symbolically 512 |

For the last two cases the JavaScript test does NOT enumerate models, and the displayed even counts follow the proved incidence-rank formula rather than an executed count. For h<=10, the independent Python enumerates and confirms the displayed counts. The finite controls cannot prove the general theorem independently of its algebraic proof.

## Cost ledger, scope and precise remaining gap

- **Ideal logical proof work:** 1 paid native node in R_T; 4h-1 in the separately declared original /341 semantic calculus for bridgeless cubic graphs, **conditional on that precise historical grammar**. The macro is not a native /341 inference.
- **Evidence bits:** O(h log h) for graph/charges/source IDs, plus N=Theta(h log h) authenticated signed source bytes; explicit evidence still costs time and space.
- **Construction/search:** on recognized source supplied with witness, construction and check can be polynomial; arbitrary-SAT proof search is not bounded.
- **Actual verification/output:** polynomial time in source plus record bytes, nonzero read and serialization overhead; 53 executed V8 checks and 32 separately authored Python checks are distinct test measurements.
- **Parallel span and peak space:** not equated to one logical node; no FLMV same-machine interpretation or all-input space claim.
- **Scope ledger:** (i) chosen restricted proof-rule class C: unit abstract path exists; (ii) fully authenticated fixed historical R_mix341: P2-D1/P2-C3/P2-B1 remain OPEN; (iii) arbitrary SAT algorithms: no implication. Noncircular same-R B3 (P2-B2) remains OPEN.

**Actual advance:** replacing prior exponential-evidence global TABLE by an exact polynomial-evidence one-step recognizer on a published Resolution-hard family, demonstrating a family-wide rule-language precision barrier without altering the historical calculus. **Verification:** standalone executable source and readback, 53 native JS tests and 32 independent Python semantic tests; authoritative historical checker not executed. **Publication:** this report, executable, raw and handoff are repository artifacts subject to final readback; trackers/issue must be separately reconciled. **Next obligation:** authenticate all historical native rule payloads, facet owner/port references and admissible source reads; build a source-exact overapproximation that *provably excludes only inapplicable macros* while preserving every true legal GF(2), AND3, DEF, RES, LOCAL and shared-DAG path. The required superpolynomial full-calculus potential and noncircular B3 remain OPEN. P versus NP OPEN.

## References

[1] A. Urquhart, "Hard Examples for Resolution," Journal of the ACM 34(1):209-219, 1987. DOI: 10.1145/7531.8928. Ordinary Resolution only.

[2] P. Cousot and R. Cousot, "Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints," POPL 1977, 238-252. DOI: 10.1145/512950.512973.

[3] MassimoLauria/cnfgen, cnfgen/families/tseitin.py, current checked blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab. Generator implementation, not a proof of arbitrary mixed hardness.


## POSTPUBLICATION INTEGRITY 542 | 2026-11-09 PST

All four primary repo artifacts were read back: mathematical report, five-role handoff, exact executed JS source and raw checks. Exact published JS source was refetched and executed in V8 with 53 checks PASS. Independent original signed-CNF Python code was executed locally with 32 checks PASS and subsequently published verbatim to experiments/arc/lspv1_542_independent_semantic.py (blob bdba56f18ed041a467af8991e54b1b0b2d8519f3); its raw JSON is results/raw/arc/2026-11-09_1208_LSPV1_542_INDEPENDENT_PYTHON_RAW.json (blob da9252af997e54e5fb79d7e727136a5c45db1784). These are two independently authored finite implementations, not a historical R_mix341 execution. No machine-specific host peak-RSS or native bit-operation trace was measured.

Full current proof2 tracker was safely appended only after exact current-head blob SHA read, with exact prior tracker published at research/agents/lspv-1/outbox/2026-11-09_1208_LSPV1_542_PROOF2_PREWRITE_EXACT.txt. Commit 4a3f9f982d3bae47b478bc944c366025ea4469af, new blob 69ada15786a8695e74459386a76d732a97ed9c84; full 799,949-character readback equals the intended output, unchanged preceding prefix, and one [P2-L1-542] occurrence. proof1 remained unchanged.

Root main.tex fetch returned blob 0c32e09d3cd1d5cf46963ac374f437c912dfe82e but **zero readable content**. It was NOT modified. A role-owned insertion fallback, research/agents/lspv-1/outbox/2026-11-09_1208_LSPV1_542_ROOT_MAIN_OWNED_INSERTION_FALLBACK.md, was committed and read back without changing any root or peer manuscript region. Local repository preflight and historical authoritative checker were not run. Issue #3 comment https://github.com/j15marti/pnp/issues/3#issuecomment-6750318250 passed exact comment-body readback.

**Final status:** Actual advance PROVED/RESTRICTED in distinct R_T plus independent finite tests; full historical R_mix341 all-rule semantics [P2-D1/P2-C3], superpolynomial all-rule bound [P2-B1], and noncircular B3 [P2-B2] remain OPEN. Publication for role-owned report/code/raw/handoff/tracker/issue verified, root main.tex edit blocked and intentionally omitted. P versus NP OPEN.
