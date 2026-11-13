# LSPV-4/591: A complete correct SAT decider defeats per-instance transfer to ordinary Resolution

**2026-11-13 11:39 PST | historical Route A | PROVED/RESTRICTED symbolic, COMPUTATIONAL finite audit | P versus NP OPEN**

## Candidate and falsifiers

Candidate: There exists a fixed total correct deterministic SAT decider A which runs in polynomial time on an explicit infinite unsatisfiable proper-3CNF family but on which the *minimum* source-bound ordinary shared-DAG Resolution refutation cost grows exponentially. This defeats an arbitrary-algorithm per-instance transfer into **ordinary Resolution**, not into the full historical R_mix341.

F1: the fast parity recognizer misclassifies a source or implicitly assumes a promise. F2: global shared-DAG Resolution can bypass the hard-family bound. F3: an XOR/extension/learning/branch/compact representation shortcut is illegally excluded from historical R_mix341. F4: the per-instance bound is silently replaced by a worst-case-runtime bound, or the parser/fallback is incorrect. F1 addressed by exact proof and 106 finite controls, F2 by the published general-DAG theorem, F3 intentionally remains a blocker for historical R, and F4 is distinguished explicitly below.

## Exact total algorithm and proof of correctness

Parse arbitrary encoded CNF, returning a deterministic malformed-input classification on invalid inputs. For every valid CNF, group clauses by their *original signed* unordered triple of distinct variable IDs. Recognize the special form only if each triple-support occurs in exactly four clauses, the four distinct falsifying assignments all have the same parity p, and each occurring variable belongs to exactly two different triple-supports. If recognition fails, use exhaustive assignment enumeration over the **occurring** variables, so the algorithm remains correct and total on arbitrary formulas and both SAT labels.

For a recognized support v, four clauses forbid precisely the four 3-bit patterns with parity p_v. Their conjunction is exactly the affine equation XOR_{e in I(v)} x_e = chi_v, where chi_v=1-p_v. Each variable occurs in exactly two such equations, giving a graph with one edge-variable between the two groups containing that variable. Solve each connected component by XORing its right-hand sides: UNSAT exactly when a component has odd total chi. Necessity holds because each edge appears twice and cancels; sufficiency holds by assigning non-spanning-tree edges zero and solving tree-edge values by leaf elimination. Consequently, the recognized branch is exact for all inputs passing the syntactic test; the nonrecognized branch is correct by exhaustion. A straightforward fixed bit implementation takes at most O(N^3) time for recognition on N encoded input bits. The same A is deterministic, total and correct on **every** valid CNF. It may take exponential time outside the recognized class.

## Theorem 591.1: unconditional restricted per-instance compiler obstruction

Fix an explicit infinite family of cubic edge-expanders G_h with h vertices. Form the original signed strict-3CNF Tseitin contradictions F_h by emitting the four local forbidden-parity clauses at each vertex and choosing odd total charge. There are 3h/2 variables, 4h clauses and encoded length N_h=Theta(h log h). The recognizer identifies F_h and decides UNSAT in at most C(N_h+1)^3 bit operations for one fixed C.

By the established Urquhart/Ben-Sasson-Wigderson general (not tree-only) Resolution lower bound on bounded-degree expander Tseitin CNFs [1,2], every source-bound ordinary Resolution refutation has at least 2^(c h) lines for a fixed positive c on the expander family. Define R_RES as ordinary chronological binary source-bound Resolution with zero-cost original SOURCE rows, unit cost per distinct actual paid inference occurrence, shared nodes counted once, and **no** XOR, extensions, new semantic axioms or free discharge. Omitting the 4h original clauses from the charged count can subtract at most 4h, so

    W_RES(F_h) >= 2^(c h) - 4h.

Thus for this one *correct total deterministic* A, every proposed constants c_A,r_A>0 fail on some UNSAT F_h:

    W_RES(F_h) > c_A (N_h+T_A(F_h))^r_A.

Proof: the right-hand side is polynomial in h log h; the left is exponential in h. This contradicts the desired **per-instance** upper bound for fixed R_RES even after all possible Resolution DAG sharing, lemma reuse and choice of branching order. It says nothing about the full mixed R_mix341 minimum. This is the explicit arbitrary-decider transfer obstruction sought by the latest user directive, within the sharply restricted proof system.

The theorem's result is *not* a counterexample to a Wbar_RES(N) bound expressed using worst-case time T_A^wc(N): A's exhaustive fallback is exponential on some inputs. Conditional on SAT in P, replacing the fallback by a polynomial correct SAT machine would yield a polynomial all-input A without making Resolution polynomially bounded, but that conditional thought experiment does not transfer to historical R_mix341. Cook-Reckhow's existence of SOME short-proof system is not a simulation by a fixed preselected system [3].

## Native interface and source-bound status

The original archived /386 SOURCE+DEF+RES checker was inspected as its actual accepted-byte source, Git blob `338305c0ce101704205e57543756b8127074a986`. LSPV-2/604 has now compiled complete **DPLL conflict trees** into accepted /386 Resolution packets at W=R+1<=I+1, where R counts paid resolutions and I is the actual DPLL tree's internal node count; the extra unit is an explicitly paid unused conservative owner needed for the archived CLI's mutation self-test. That is a positive source-bound compiler for one representation, *not* a polynomial bound in the runtime of a different Gaussian-elimination algorithm. In particular the restricted R_RES theorem must not silently count /386 paid DEF as prohibited, nor treat the /386's odd-Tseitin source promise as coverage for general CNF.

The /341 accepted-byte checker, Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`, is a different SOURCE/AND3/XOR fixture system. LSPV-3/620 independently replayed an original /341 accepted fixture whose in-band signed source has 64 satisfying assignments, and identified lack of external source authentication for /386. Neither sibling authenticates a complete source-bound historical mixed R_mix341 rule dispatcher or its fixed weights. A real GF(2) local conversion can be a legitimate cheap escape on parity sources; never refine it away to preserve a proposed Resolution lower bound.

## Whole-DAG C3 charge-soundness lemma 591.2

For any *authenticated* native rule system, distinguish live identities L_t from monotone paid history H_t. If step t presents identity tokens J_t, with exact native weights w(j)>=0, set H_{t+1}=H_t union J_t, and charge c_t=sum_{j in J_t\H_t}w(j). The identity semantics must be read from the original rule: a distinct paid Resolution occurrence is distinct even if it repeats a clause, while a paid definition owner is globally once-paid despite multiple legal free facets. Deleting a node alters L_t, **not** H_t; recomputation and branch reconvergence use the actual native identities.

Conditional lemma: if each concrete step has an abstract successor, original signed source and initial state are preserved, a closed concrete goal maps to a closed abstract goal, and each edge has abstract charge at most the corresponding concrete **whole-DAG** charge, induction on path length gives sum(c_abs)<=sum(c_concrete). Minimizing over accepted concrete refutations gives W_abs(F)<=W_R(F). A shared owner cannot be charged twice across components; a new paid occurrence cannot be erased from the accounting. Independently minimizing area and peak or components is not a realizable joint-cost witness. The lemma supplies a precise *conditional* rule-by-rule firewall; no claim is made that all full historical operations have yet been authenticated or simulated. An infinite/coarse MAY abstraction may be sound: failure of a finite exact quotient is not impossibility of all abstract interpretations.

Separate logical W_R, evidence-bit count, reference lookup, sequential verification, parallel span, live retention, retrieval, recomputation, and peak writable space. An efficient verifier, external correctness certificate, SAT recognition algorithm, or accepted packet without source/goal soundness supplies none of the missing same-calculus B2/B3 steps.

## Executable evidence and reproducibility

`experiments/arc/lspv4_591_affine_transfer_obstruction.cjs` is a standalone dependency-free original signed 3CNF producer, parity recognizer, and brute-force independent label oracle. It was executed in hosted V8, including fresh execution of the exact GitHub-readback code. All **106 assertions passed**. Tested 15 source graphs/charge cases (K4, K3,3, 6-vertex prism, cube, disjoint K4+K4; each with zero, one, or two charged vertices), their 15 reversed-literal aliases, and eight hostile nonrecognized controls. All 30 intended fast cases selected the affine solver; all eight corrupted/unrelated cases selected exhaustive fallback; all SAT/UNSAT statuses and exact model counts agreed with direct enumeration. No randomness; no finite observation is asserted to prove the asymptotic Resolution lower bound. Raw machine-readable ledger: `results/raw/arc/2026-11-13_1139_LSPV4_591_AFFINE_TRANSFER_AUDIT_RAW.json`.

Exact script Git blob `464a9deacf29eadc22fa28f51372819058d0b820`; raw blob `0b2f2b41a56b881f9853a36064877cb9c3fdcc5c`; readback contents reproduced the stored result. This new script is not an original /341 or /386 checker replay, and Node OS execution and repository-wide preflight were not completed here.

## Corpus, node status, and handoff

Read both root trackers, including the **full 1,051,196-character proof2.txt** from immutable blob `930c5eeddafce656717f28055a7a9a755f44737c` after the ordinary file interface returned zero body; proof1.txt blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`. Reviewed issue #3, AGENTS.md, CODEX.md, project research skill, two unchanged archived sibling checker sources, /539-549 preceding material including LSPV-2/539 and /549 and LSPV-4/539 and /549 references, latest LSPV-2/603-604, LSPV-3/617-620, LSPV-1/462-463/623 and LSPV-5/409/523. This report gives a more explicit correct-total-decider version of a known Resolution versus affine-decision contrast. No novelty is claimed for the underlying Resolution lower bound, parity-solving algorithm or generic Cook-Reckhow logic.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** P2-D1, full P2-C3, P2-B1, separately P2-B2/P2-B3, and P1-01/03/04 remain OPEN. The five existing task identities, titles, Pacific hourly schedules, ownership boundaries, historical weights and 2 Route A/3 Route B labels were not changed. P versus NP remains OPEN.

**Next:** demand a genuine historically source-bound mixed RES-to-AND3 or paid DEF-to-LOCAL-CONVERT accepted-byte transition from LSPV-2/3, and test whether *that same fixed native system* can compile the polynomial affine branch with actual weights, evidence, paid identity, verifier operations and peak memory. If not, publish the first rule-specific obstruction rather than an invented grammar.

## References

[1] Ben-Sasson E, Wigderson A. Short Proofs Are Narrow: Resolution Made Simple. J ACM. 2001;48(2):149-169. https://doi.org/10.1145/375827.375835 ; author manuscript https://eccc.weizmann.ac.il/eccc-reports/1999/TR99-022/

[2] Urquhart A. Hard Examples for Resolution. J ACM. 1987;34(1):209-219. https://doi.org/10.1145/7531.8928

[3] Cook SA, Reckhow RA. The Relative Efficiency of Propositional Proof Systems. J Symbolic Logic. 1979;44(1):36-50. https://www.cs.utoronto.ca/~sacook/homepage/cook_reckhow.pdf

END_OF_VERIFIED_REPORT::LSPV-4::591
