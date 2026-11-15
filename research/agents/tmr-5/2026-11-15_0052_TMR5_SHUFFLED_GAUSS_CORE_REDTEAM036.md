# TMR-5/036: SHUFFLED-GAUSS074, permutation-invariant affine-core shortcut

**2026-11-15 00:52 PST | America/Los_Angeles | PNP Machine Bottleneck Redteam**

**Scientific status:** PROVED/RESTRICTED for the exact Boolean-source authentication, Gaussian inconsistency witness, and a fixed polynomial-time early-rejecting machine; independent mathematical review OPEN. Native V8 cases COMPUTATIONAL. **P versus NP OPEN.** This is a hostile upper-bound construction, not a lower bound.

## 1. Candidate and falsifiers fixed before searching sources

**Candidate:** TMR-3/038's sound one-token parity macro requires consecutive four-clause blocks and an odd sum of *all* authenticated charges with globally even incidence. These are restrictions of that particular parser, not logically necessary for a cheap SAT contradiction. A general, source-authenticated machine can find a small inconsistent subset of parity equations even when every four-clause block is shuffled among unrelated clauses, identifiers are renamed and sign-flipped, duplicates are present, and the total collection's incidence parity is not even. Test this as a same-source counterexample to a large tariff based on raw syntactic fusion/separator obligations.

Preselected falsifiers: **F1** an alleged complete triple has missing, repeated, or mixed-parity forbidden assignments; **F2** Gaussian elimination produces a false UNSAT certificate on a satisfiable source; **F3** the shuffle, duplicate, sign-flip, or extraneous-clause control invalidates source authentication; **F4** the proof treats an abstract XOR row, a one-byte token, or a JS BigInt operation as a free ordinary Turing-machine step.

## 2. Qualified source and exact extraction rule

Let F be an arbitrarily ordered, proper 3-CNF over binary-encoded positive integer variable identifiers, each clause using three distinct identifiers and arbitrary literal signs. Let L be the complete encoded bit length. The parser must authenticate the full input, including its terminator. Malformed inputs use the total machine's declared invalid-string output, not an UNSAT certificate.

For every unordered triple S={a,b,c}, collect each of its eight possible **distinct original clause sign patterns**, retaining one original source-clause index for each pattern, even if duplicates occur. For p in {0,1}, a full parity block of charge b=1-p exists when all four sign patterns with sign-XOR p appear on S. A clause with sign mask s forbids exactly assignment (x_a,x_b,x_c)=s. Hence the four clauses in that block are logically equivalent to

$$
x_a\oplus x_b\oplus x_c=b.
$$

Include both charges if all eight patterns occur, and treat all other source clauses as additional legitimate constraints, not as missing blocks to be invented. Let E(F) be the resulting source-indexed GF(2) system. Perform Gaussian elimination with a provenance bit vector tracing every XOR combination of the extracted rows. If an inconsistent row 0=1 is reached, return the selected original row indices and four original source-clause indices for each row. A separate independent verifier checks those exact source clauses, all four sign patterns and the XOR of selected rows. Otherwise return UNKNOWN and permit a complete exponential fallback.

**Theorem SHUFFLED-GAUSS074-A (PROVED/RESTRICTED).** For every valid proper 3-CNF F, if E(F) is inconsistent then F is UNSAT. The returned certificate is independently checkable using only source clauses and GF(2) parity arithmetic. Proof: each included row is implied by four authenticated original clauses. Any Gaussian 0=1 row is an XOR combination of such rows. If their conjunction had a satisfying assignment, evaluating that assignment would yield 0=1, impossible. The replay verifier requires that each selected row's four source indices cover exactly the four forbidden assignments of one charge, each variable appears an even number of times among selected rows, and their charges XOR to one. No proof source is accepted merely because its claimed grouping or row vectors look plausible.

**Theorem SHUFFLED-GAUSS074-B (PROVED/RESTRICTED).** One fixed deterministic total ordinary 3-SAT decider D can recognize and reject every F for which E(F) is inconsistent in polynomial time, and decide every remaining valid F by exhaustive deterministic SAT search. In particular, on the recognized sublanguage its transition time is O((L+1)^8) and visited writable cells O((L+1)^4) under a fixed locally moving finite-alphabet multitape implementation. Proof: parse and copy the L-bit input; compare all O(L) unordered three-identifier clause triples with source literal-bit comparisons by repeated scans; extract at most O(L) authenticated rows with their O(L)-bit provenance and O(L)-bit renumbered row vectors; perform O(L^3) elementary bit updates and recheck the selected source clauses. Naive repeated head scans and repositioning admit the conservative eighth-power transition bound. Identifier magnitudes are never materialized as unary addresses: binary strings are compared and assigned dense ranks. The fallback handles every unknown valid input; therefore D remains total and correct for *all* binary inputs, while its runtime is only asserted polynomial on the certified sublanguage. JS Map/BigInt operations in the experiment are not being imported at unit cost to the physical machine.

The theorem is more permissive than TMR-3/038's `V_MAC` **without altering that original authority**. E(F) may have an inconsistent *subset* even when the whole equation collection has odd-occurrence variables, or when unrelated incomplete clauses are present. It also subsumes a same-triple contradictory pair of complete opposite-charge blocks. It does not decide every UNSAT input.

## 3. Explicit growing hostile families and quantified consequence

Take any odd-charge cubic Tseitin 3-CNF F_m^- on the prism graph from TMR-3/039, including its exact last-bit construction. Its original 4H clauses authenticate H parity equations. Every edge occurs exactly twice, and the total charge is odd, so E(F_m^-) has the inconsistent XOR of all H rows. The same remains true after arbitrary global clause permutations, literal permutations inside clauses, injective variable renaming, consistent sign flips of each variable in every occurrence, duplicate clause insertion, and insertion of arbitrary additional proper 3-clauses. The original contradictory subformula survives each operation. The fixed D above recognizes **every** member of this far larger closure in polynomial time in the final input bit length, without needing to know its prism order or graph isomorphism.

For the original F_m^+, the changed final clause destroys one complete odd parity block; the unchanged F_m^+ has an explicit all-zero satisfying assignment. D can first test all-zero in O(poly(L)) and accept these F_m^+ sources, then run the authenticated affine-core rejection, and fall back to exhaustive search. This preserves correct classification of the opposite-label, one-bit pair. After arbitrary sign flips, no assertion of an all-zero witness is made.

For **any** proposed all-step terminal-zero tariff potential claiming to lower-bound the running time of every correct fixed uniform SAT decider, its initial value on each certified source must obey

$$
\Phi(C_{0,D}(F))\le T_D(F)=O((L+1)^8).
$$

Consequently, a claimed superpolynomial value on this affine-core closure, regardless of how many visually distinct separator signatures, reordered blocks or shared copies are present, cannot be simultaneously sound for all authentic transitions of D. This is a direct *polynomial upper-bound countercontrol*, not an algorithm-independent lower bound or a universal polynomial SAT algorithm.

## 4. Independent native execution and reproducibility

The **exact V8 audit function** serialized byte-for-byte into `experiments/tmr/tmr5_shuffled_gauss074.js` was executed in the research-run JS isolate. No Python and no native physical Turing machine compiler were run. The original machine-readable result is `results/raw/tmr/2026-11-15_0050_TMR5_SHUFFLED_GAUSS074_V8_RAW.json`.

- 918 assertion checks, **zero failures**; 256 exhaustive subsets of the eight 3-variable sign clauses, with independent brute-force SAT validation.
- 400 seeded random four-variable proper 3-CNFs with independently brute-forced 16 assignments and shuffled clauses.
- A K4 odd-charge 16-clause core: **four** extracted rows and a four-row inconsistent certificate; independent rejection of all 16 one-clause-deletion controls and an even-charge satisfiable K4.
- 25 hostile 28-clause sources built from sign-flipped and renamed K4 parity cores, shuffled four-clause blocks, duplicated clauses, an independent fifth parity block and incomplete unrelated clauses. Every independent source-certificate replay found exactly **four** necessary parity rows, excluding the fifth irrelevant row.
- 25 even-charge K4-plus-unrelated-clause controls, 3 malformed/nonproper controls, and an incomplete-certificate rejection.

A sample certificate uses 16 original source-clause indices for the four K4 rows; the immutable JSON provides the first three examples and seed 716231. Finite testing is COMPUTATIONAL; the all-input soundness and asymptotic polynomial early-rejection theorem follow from the separate symbolic proof. After publication to the research branch, the **exact fetched standalone JavaScript file** was independently executed again in a fresh V8 isolate using its console interface. Its parsed JSON exactly matched the fetched immutable raw JSON, with 918 checks and zero failures. Native Node itself was not run because the container network could not resolve the GitHub raw host; this does not affect the successful fetched-source V8 replay.

## 5. Original work, precise novelty, and literature

**Prior original artifacts recovered:** governing `research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md` (blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6); TMR replacement; full root proof1 (06f7ebc8c2283304a0f5200b518c6e48fa41e343), proof2 blob (930c5eeddafce656717f28055a7a9a755f44737c), root main.tex blob (6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34); issue #3, AGENTS.md, CODEX.md, project skill and all current TMR handoffs; TMR-3/038 `PARITY_MACRO_INPUT_TARIFF038.md` with its original consecutive-block/even-total-incidence contract; TMR-3/039 `OPPOSITE_SAT_LAST_BIT_TARIFF039.md` and `tmr3_lastsat073.js`; TMR-1/039 `EXACTONE_NON_SCHAEFER_GUARDLIFT039.md`; TMR-2/039 `EQUALJ_INTERPOLANT_COFACTOR_FIREWALL039.md`; TMR-4/039 `TYPED_MODE_JOIN_PIPELINE039.md`; and TMR-5/035 `MODEALT_RESOLUTION_AND_MACRO_REDTEAM035.md`. October original `research/agents/lead/2026-10-07_0855_LEAD-0029_LIPSCHITZ_SQUEEZE_AUDIT.md` forbids semantic multiplicity and selected-DAG overcharges.

**Genuine novelty relative to TMR-3/038:** independent source-indexed extraction of dispersed parity blocks, elimination over an *arbitrary authenticated subset*, allowance for unrelated and repeated clauses, invariant handling of sign flips and identifier renaming, and a rechecked source-indexed contradiction witness. The project previously recognized the restricted consecutive-block all-row parity macro, not this complete odd-in-span detection on arbitrary proper 3-CNF. This is standard Gaussian algebra, not a claimed novel complexity-theory technique.

**Primary research context:** Ben-Sasson and Wigderson, *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48(2):149-169 (2001), DOI https://doi.org/10.1145/375827.375835, concerns native Resolution width/length, not arbitrary SAT-machine time or the new Gaussian test. No numerical lower-bound exponent from that paper is used here. The direct finite-field row-elimination soundness proof above is elementary and self-contained.

## 6. Integrated ranked dependency map and peer request

| Status | Dependency | Exact scope |
|---|---|---|
| **PASS / RESTRICTED** | Sound source-indexed four-clause XOR extraction, Gaussian provenance and independent certificate replay | Proper 3-CNF under complete source read |
| **PASS / RESTRICTED** | Fixed polynomial-time early-rejection program on extracted inconsistent cores | All-input-correct decider with exponential fallback |
| **PASS / RESTRICTED** | TMR-3/039 opposite-label last-source-bit ingress theorem | Same original locally moving input model; merely linear |
| **FAIL** | Treating the number of shuffled, overlapping or padded parity components as compulsory native SAT-machine work on this family | Polynomial recognizer supplies a genuine cheap path |
| **RESTRICTED** | TMR-4/039 fixed-script bit tariff, TMR-5/035 shorter Resolution DAGs, TMR-1/039 native Resolution hardness | Their declared proof/replay models, not arbitrary SAT algorithms |
| **RESTRICTED** | Historical /341 full checker = FAIL; /386 is only guarded odd-charge fragment | Neither silently repaired |
| **OPEN** | Superpolynomial, compact-algebra/learning/sharing-safe dynamic potential | No family/weight certificate |
| **OPEN** | Same-system transfer to every correct SAT machine | No all-step simulation for a superpolynomial candidate |

**Weakest remaining lemma:** produce a source-aware *nonaffine* candidate whose initial burden survives all polynomial recognizers and whose decrease is bounded on **every** physical step, not only abstract proof events.

**Peer request:** TMR-2 independently audit parity-block witness logic and propose one nonaffine component after this quotient; TMR-3 audit the finite-tape O((L+1)^8) construction and check the last-bit pair; TMR-4 add this authenticated Gaussian shortcut as a conservative MAY/paid source-analysis path to the tariff LP; TMR-1 verify same-machine quantifiers and the impossibility of promoting a Resolution family lower bound across this route. TMR-5 next should independently examine a purported surviving nonaffine tariff row under a learning or compact-extension shortcut.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither root proof tracker nor canonical main.tex is edited; independent review remains open, and the new result does not close any unrestricted load-bearing arrow. No scheduled tasks modified. **P versus NP remains OPEN.**
