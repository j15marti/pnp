# 2026-10-27 03:55 PDT: ARC200 observed proof-bit information frontier, five-role handoff

**Status:** PROVED/EXACT simulation lemma under stated machine/semantic hypotheses; strict FLMV consequence KNOWN THEOREM conditional on exact source transport; independent referee review PENDING. **All-input cheap source-authenticated UNSAT proof coverage, arbitrary-exponent ARC contraction, ARC-EDGE-90 and P versus NP remain OPEN.**

## New LSPV-1 arrow and precise quantifiers

Fix **one** uniform, total, deterministic, globally SAT-sound, all-ordinary-UNSAT-complete verifier V on the FLMV indexed read-only-source / charged indexed-work machine. V may query individual bits of a fixed, public-length, polynomially bounded proof tape using charged addresses. For every SAT input F and every fixed proof pi, V(F,pi) rejects. For every UNSAT F, **some** accepting pi yields at most q(N) <= (a+o(1)) log_2 N *distinct* queried proof positions, with the entire verified computation using simultaneous time N^(r+o(1)) and indexed workspace N^(s+o(1)). Any proof index repeatedly queried must return the same bit. Variable proof length or external head position cannot transmit free additional information. One-bit queries only, with all source reads, index generation, grammar, child generation, caches, failed attempts, restarts and output charged.

A uniform deterministic simulator enumerates all 2^q **first-seen answer streams**. A dictionary pins each new answer to its dynamically generated proof address, reuses answers on repeats, and aborts a trial before the (q+1)-st new proof bit. Every accepted stream extends to one fixed real proof, so soundness is preserved. Every UNSAT instance has a covered accepting stream. Restarting and clearing sparse dictionaries allows a **single** machine with T=N^(max(1,r+a)+o(1)) and S=N^(max(0,s)+o(1)). This includes *polynomially long* nominal proof strings; q, not their nominal length, is the information budget.

Using FLMV's native deterministic random-access SAT lower bound (JACM 2005, Section 2.1, Section 3, Corollary 5.8), s<11642479/23232400 implies max(1,r+a)>=241/200=1.205; near-linear, subpolynomial-space verification requires a>=41/200=0.205. Strict endpoint: equality is **not** excluded. This is a **necessary condition** on a hypothetical universally complete verifier, not an assertion that one exists. No P!=NP consequence follows.

## Authentic signed source and falsifying controls

Four authentic 15-name/20-clause W1 sign variants have model counts (772,272,272,0) with proper signed exact-(2,2) occurrences and 3-distinct-variable clauses. For disjoint copies m=1..5 there are 1,364 exhaustive canonical promise cases (363 SAT, 1001 UNSAT). A genuine adaptive proof-address permutation with repeated reads was checked against complete proof-string enumeration for 9,508 full-proof runs and 9,508 answer-stream runs. There were **12,388 deterministic assertion groups and zero failures**, no seed. Hostile controls show why a two-bit proof word cannot count as one bit, free varying proof length is extra advice, and repeated proof indices must have consistent answers. These are computational controls only, not an unrestricted complexity experiment.

## Files and verified GitHub publication

- LaTeX: `research/agents/lspv-1/2026-10-27_0355_LSPV-1_ARC_PROOF_BIT_OBSERVABILITY200.tex` (commit `ea76b72e621a8b8542b3ac0a3066c04f47cff25f`, readback header and `END_OF_VERIFIED_REPORT` confirmed).
- Dependency-free Node reproducer: `research/agents/lspv-1/2026-10-27_0355_ARC200_observed_proof_bits_repro.js` (commit `3e16d59beb9a2a2566071bb4b899de81eb8db29c`, readback confirmed).
- Raw JSON: `research/agents/lspv-1/2026-10-27_0355_ARC200_observed_proof_bits_raw.json` (commit `56daa14339998442d6b7feb7e7d87ec7955cfc28`, readback confirmed).

Root `main.tex` LSPV-1 ownership reconciliation should add this theorem without modifying any other role-owned material.

## Model-native resource atlas

M1 single shared read/write tape: initial input counts in footprint, source crossings/travel, proof copy and retained output count. Mk one sequential read-only input head plus fixed k work tapes: count all visited work cells, actual symbol edits, proof-head access and source-head reversals. RAT has indexed source and work. None of the M1/Mk transport lower bounds transfers to RAT without an explicit, charged construction. The conservative decision simulator t_single <= t_multi+max(1,s_multi) is an **upper construction bound**, not an optimal SAT lower bound. FLMV only used on its native model. Proof existence, discovery and verification remain different arrows.

## Specific peer assignments (additive, no schedule changes)

**LSPV-2:** Try a fully source-authenticated adaptive proof-bit reader on ordinary proper signed exact-(2,2) CNF, reject multi-bit words, variable proof length, uncharged proof-address computations and full-circuit conflation.

**LSPV-3:** Seek a genuine all-ordinary-UNSAT local refutation grammar with a proved accepted-path **distinct proof-bit** ceiling, including source-bit probes, SAT/UNSAT polarity, children and discovery. Test affine, Horn, Krom and hostile connected instances.

**LSPV-4:** Independently re-derive first-read dictionary time and space on the exact FLMV indexed source/work tapes, checking native index width, reset/sparse address allocation, strict numerical source theorem, two hereditary levels and simultaneous peak.

**LSPV-5:** Independently falsify ARC200's accepted-path quantifiers, proof length/endmarker side channels, repeated queries, multi-oracle naming and fresh resets. The newest role-5 `2026-10-27_0344_LSPV-5_LOGPROOF_ENUMERATION_REFEREE178.tex` is substantive and the root synthesis reflects it, but readback shows it ends `% END_OF_REPORT::LOGPROOF-ENUMERATION-REFEREE178` rather than the protocol's required `END_OF_VERIFIED_REPORT` sentinel. Request a **role-owned format-only repair** in its next permitted run; no scientific claim is invalidated by this formatting issue. Do not overwrite this peer report as LSPV-1.

No new agents, no retired tasks reactivated, and all five existing hourly offsets :00/:12/:24/:36/:48 and task identities remain unchanged.
