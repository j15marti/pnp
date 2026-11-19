# TMR-5/058 | 2026-11-19 02:48 PST | Pinned formal ETH statement-semantics and trust-surface audit

**Pipeline / dependency:** TMR-1 C1 chain, arrow "pinned Lean proposition => ordinary deterministic machine statement => JMV E^NP consequence". P versus NP OPEN.

**Candidate (before inspection):** At anthropics/formal-math commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5, `MainResults.ETHIsFalse` and `MainResults.MainTheorem` express their prose claims in a bounded-work machine model, and the proof sources have no kernel-trust escape.
Falsifiers: F1 unbounded work per FinTM2 step; F2 infinite state/label/stack alphabet; F3 source escape (axiom, sorry, native_decide, reduceBool, extern, implemented_by, csimp, unsafe, opaque, custom elaborators); F4 an encoding/promise that excludes inputs the JMV consequence needs.

**Sources read (original):** eth/MainResults.lean blob 1c62a550fa1e4cbec65bb7112f92ad67589afddc (full), Challenge.lean 6297ab13…, Solution.lean 176892178e…, comparator.json 85f16dc5…, lake-manifest (Mathlib 0df444a360eaa60ab8c11dca51a86af692955474), .github/scripts/comparator-check.sh head. Mathlib at that rev: Mathlib/Computability/TuringMachine/Computable.lean blob 77722247abc2bc371b6fb435630e06b1bd82fd48, Mathlib/Computability/TuringMachine/StackTuringMachine.lean blob 62501893819aef15b0032a0476a51c6c164dffd0. (Mathlib/Computability/TMComputable.lean is a deprecated re-export at this rev.)

**Findings:** None of the four falsifiers fired.
- F1/F2 closed: FinTM2 has `[Fintype K]`, `[Fintype Λ]`, `[Fintype σ]`; the statements add `∀ i, Finite (M.tm.Γ i)`. `TM2.Stmt` = push/peek/pop/load/branch/goto/halt, so there is no loop. `step` runs one finite term `stepAux (M l)`. So each step makes ≤ d = max_l |M l| stack operations, and a multitape TM with one tape per stack runs t steps in O(d·t + N) time. Halting requires the initial state and empty non-output stacks, which only strengthens the claim.
- F4 closed for the downstream use: `DecidesKSat` quantifies over all Nodup k-CNFs on n variables (non-occurring variables allowed), with the bound in n only. `ETHIsFalse` is exactly ¬(0 < s 3). Repeated JMV clauses need only a poly-time dedup front end. MainTheorem's extra promises (AllOccur, m≥2, n≥4, k≥1) are not used downstream because the chain consumes ETHIsFalse.
- F3 at source level: the scripted scan of 1,052 .lean files / 152,420 lines found 0 hits for every escape pattern. The 3 `sorry` hits are Challenge.lean:8 (comment), :13 and :17 (the two statement placeholders), matching the CI log. The 3 instance attributes (Frag.fin, Stepped.sz, local fintypeFW) are typeclass registrations.

**Status:** Statement reading PROVED/EXACT (scoped to these definitions); scan COMPUTATIONAL (static). Independent review OPEN.
**Not executed:** Local Lean 4.33.1 toolchain install was denied by the environment permission policy, so lake build, comparator, nanoda and #print axioms did not run. Kernel acceptance still rests on the SHA-matched upstream CI run (TMR-1/057). A grep cannot exclude escapes in Mathlib or other dependencies; the comparator allowlist covers those only in CI. No repo preflight and no LaTeX build (no TeX installed).

**Gates:** DISJ NOT APPLICABLE (upper-bound algorithm, not an invariant); relativization OPEN for the bridge (JMV/Williams is non-relativizing via circuit analysis); simultaneous DTISP NOT APPLICABLE (time-only); deterministic configuration counting PASS (consistency only).
**Consequence still only:** conditional i.o. E^NP ⊄ SIZE(O(N)). No NP lower bound.

**Other routine inputs reviewed:** User Google Doc "P vs. NP Proof Attempts": structure plus the full §4 synthesis were read, §§2–3 only by headings. Its locality/magnification frontier matches Track C. GitHub org search: openai/ten-proofs, openai/cdc-lean, google-deepmind/formal-conjectures and alphaproof-nexus-results are candidate formal-statement sources; none are inspected for SAT lower bounds yet. A code search for `ETHIsFalse org:google` returned 0.

**Artifacts:** experiments/tmr/tmr5_formal_eth_static_audit058.py (revision TMR5_FORMAL_ETH_STATIC058_v1, deterministic, no seed); results/raw/tmr/2026-11-19_0248_TMR5_FORMAL_ETH_STATIC058_RAW.json.
**Next lemma:** Do a local pinned build plus comparator/nanoda/#print axioms where the toolchain is permitted. Then match the JMV Cor. 3(1′) hypothesis to ETHIsFalse exactly.
