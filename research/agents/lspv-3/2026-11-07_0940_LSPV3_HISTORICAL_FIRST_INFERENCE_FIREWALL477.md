# LSPV-3/477 | First-inference obstruction in the authenticated /341 checker fragment

**2026-11-07 09:40 PST | Route B | PROVED/RESTRICTED structural theorem, KNOWN published random 3-CNF Resolution lower bound, COMPUTATIONAL finite controls | Full historical R_mix341 grammar OPEN | P versus NP OPEN.**

**Exact tracker nodes:** [P2-D1] (historical byte grammar OPEN), [P2-C3] (whole-mixed transfer OPEN), [P2-D2] (shared-proof minimum), [P2-B1] (whole-mixed hardness OPEN), [P2-B2] (noncircular B3 OPEN), [P2-L5-413] (exact historical restricted-checker replay), [P2-L3-476] (ordinary Resolution scope). New evidence: **[P2-L3-477]**. Proof1 nodes [P1-01], [P1-03], [P1-04] remain OPEN.

## IDEA: exact hypothesis and falsifiers

**Hypothesis.** Even if the historical /341 verifier's two rule schemas are generously applied to arbitrary proper signed strict-3CNF input sources, they cannot derive a *first inference* on any formula whose clauses have pairwise distinct unordered variable triples. Published ordinary-Resolution-hard random 3CNF at fixed clause density is overwhelmingly of this form.

Four predeclared falsifiers: (F1) a historical source clause already carries an independently authenticated affine row; (F2) historical AND3 accepts union support of four or more original variables; (F3) historical XOR can consume two unannotated factor parents; (F4) the chosen established random-clause distribution has non-vanishing probability of repeated triples at linear density. None fired in the stated restricted model. Legal Resolution, LOCAL-CONVERT, or charged DEF in the *declared full mixed calculus* **does** bypass the first-inference barrier and is an explicit control, not an excluded shortcut.

## SEARCH: exact historical bytes, peers and outside sources

Both complete current root trackers and issue #3 were read. The governing November 2 five-role handoff, AGENTS.md, CODEX.md, pnp-research SKILL.md, LSPV-3/476, LSPV-5/413, LSPV-1/480, current Grok and Claude assessments were reviewed. LSPV-5/413 independently recovered and replayed the *actual* historical /341 producer, source packet and verifier. Its authoritative checker code at `experiments/arc/lspv2_341_independent_verify.js` has blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0` and implements only original-source coercion `kind:"factor"`, AND3 factor-to-factor with union support at most three, and XOR of two row-bearing parents. It rejects RES, LOCAL-CONVERT and DEF as unknown tags. The historic successful checker's 30,714 checks are genuine **only for that restricted sublanguage**, correcting LSPV-5/412 as already documented in [P2-L5-413]. The full declared mixed grammar has RES, and Resolution alone makes it complete, so one must not silently identify the checker sublanguage with all of R_mix341.

Published established family: Chvátal and Szemerédi, *Many Hard Examples for Resolution*, J. ACM 35(4):759–768 (1988), DOI 10.1145/48014.48016. For fixed integers k >= 3 and c with c 2^{-k} >= 0.7, random CNF with cn independent uniformly sampled proper k-clauses is UNSAT with high probability and requires at least (1+epsilon)^n clauses in any ordinary Resolution refutation for some epsilon>0 (at the theorem's asymptotic scope). Choose **k=3, c=6**. Exact source encoding: n original Boolean variables and m=6n clauses; each clause independently selects an unordered 3-element variable support from the binomial(n,3) possible supports, then assigns one of eight sign vectors uniformly. The encoded bit size is Theta(n log n) with binary variable IDs and standard signed literals. This is a *published random family* and its hardness is for ordinary Resolution only, not all proof calculi or algorithms.

For this distribution, by union bound,

$$
\Pr[\exists i<j:\operatorname{supp}(C_i)=\operatorname{supp}(C_j)]
\le \frac{\binom{6n}{2}}{\binom n3}=O(1/n).
$$

Therefore with probability 1-o(1) the published random family is simultaneously ordinary-Resolution-hard, UNSAT and has distinct three-variable supports. The complement of the displayed event includes no duplicate supports even with different signs.

Required external repository change-aware reads: `konard/p-vs-np/scripts/proof_status.json` SHA `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` SHA `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `meelgroup/frat-xor/format.md` SHA `986a21aa92b62f844ef1fce852193142c41b2b1f`; `tanyongkiam/cake_lpr/README.md` SHA `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; `peitl/short-proof/README.md` SHA `93d2090dba9739bc4983c65ea639a24e1f5e0fab`. FRAT-XOR's `i cx` and `i x` source-indexed mixed conversions (format.md lines 233-273) are **not** an authorization to add them to historical /341. No external project's claimed P-versus-NP proof was treated as authority. Ordinary indexed web search checked the published Chvátal–Szemerédi theorem and new Pang/Braun Res(XOR) controls; no separately identified Google-branded interface was used.

## ITERATE: theorem 477.1 (PROVED/RESTRICTED)

Let H be the **source/AND3/XOR rule-schema fragment**, not the full declared R_mix341. Original proper three-literal clauses enter H as factors with exactly their three named original variables and **without** affine row annotations. Each paid AND3 node takes **two distinct antecedent identifiers** (the recovered historical verifier explicitly rejects duplicate parent IDs), both existing factor nodes, and has combined support of at most three original variables. Each paid XOR node requires two already existing row-bearing nodes. No other axiom or inference is permitted.

**Theorem.** For every strict 3CNF F whose source variable triples are pairwise distinct, H has no legal first paid inference node, regardless of F's satisfiability. In particular, if F is UNSAT then H has no refutation. For the established Chvátal–Szemerédi random strict-3CNF family at c=6, this absence holds with probability 1-o(1).

**Proof.** In any finite derivation DAG pick the earliest paid node in a topological ordering. Both its parents must be original source factors. Two distinct source triples have union cardinality at least four, so AND3 is impossible. Neither original source factor bears a row, so XOR is impossible. These exhaust H's paid rules, contradiction. For the random-family probability, apply the duplicate-support union bound above and intersect with Chvátal–Szemerédi's high-probability UNSAT/Resolution-hard event. The argument already grants arbitrary optimal DAG choice and sharing; reconvergence cannot create a first node. QED.

**Typed obstruction:** An accepted historical AND3/XOR proof for an *odd cubic Tseitin* input begins with two clauses having the **same** three-variable incidence support, so the actual /341 certificates legitimately escape this restriction. Ordinary RES on arbitrary sources or paid gates likewise bypass it if their exact native implementation exists. Therefore the result is **incompleteness of the authenticated /341 fragment when generalized to arbitrary sources**, NOT a superpolynomial lower bound on full R_mix341. Defining the minimum over this incomplete H would give infinity for many UNSAT sources and is **not** a legitimate replacement for W_R of a sound, complete fixed calculus.

## Original-source finite control, independent replay (COMPUTATIONAL)

A deterministic seed-20261107 sample *without replacement* of supports (a deliberate validation control, not a new hard-family theorem) produced n=9, m=54 signed proper 3-clauses with **54 distinct triples**. Exhaustive evaluation of 512 assignments found zero satisfying assignments. A source-indexed original-Resolution Davis–Putnam derivation produced an empty clause; 474 inference candidates were generated during proof discovery, with **24 distinct live paid RES nodes** and **21 live source ancestors** after root-reachable pruning. The raw source SHA-256 is `0f12b337d0a721ec55c7cd3e5bebb117377d7ea4473ec1edf8d5f58346516b96`.

Independent Node.js verifier: 4,866 checks, 12 deliberately corrupted controls and 5 malformed-DIMACS controls rejected. Published standalone Node replay: 2,102 checks, one corruption control, confirms 24 live RES nodes and zero possible first H inference. The original-source Resolution proof is a **known legal shortcut in the full declared RES-containing calculus**; it was not excluded to preserve the H obstruction. Finite n=9 is not certified asymptotically hard. The *actual historical checker* was **not run in this /477 experiment** (its accepted raw source fixtures are specialized odd-cubic Tseitin), although LSPV-5/413 did authentically replay it.

Measured producer: 1.24 s wall, 96,260 KiB peak RSS; independent Node verifier: 0.05 s wall, 30,832 KiB peak RSS. Source/derivation JSON 11,361 bytes. The optimal proof minimum was **not** computed: 24 is a construction upper bound for ordinary Resolution, not an exact minimum. Actual generation charged all 474 discarded discovery nodes, CNF scans, SAT enumeration, source parsing, proof pruning, and output; the ideal W_R minimization legitimately does not charge search. No FLMV transfer is asserted.

## Consequences, safeguards and OPEN arrows

This makes the native-interface task more precise: the accepted historical bytes authenticate a specialized fast Tseitin parity proof, but cannot be treated as a complete general 3SAT certificate system. The missing artifact for [P2-D1]/[P2-C3] remains a historically authorized full mixed parser or authenticated accepted **RES-produced-clause -> AND3-factor** trace, including type, position, paid definitions, provenance and private/exported port scope. Any proposed replacement grammar must be marked DISTINCT. The new theorem says nothing about the minimum over **all** mixed legal derivations, and neither a random Resolution lower bound nor a no-first-node fragment obstruction establishes [P2-B1] or noncircular B3 [P2-B2]. Haken PHP, Cook ER and odd-Tseitin GF(2) remain mandatory controls.

No schedules, identities, role allocations (two Route A, three Route B), historical rules/weights or protected manuscripts were altered. Root `main.tex` fetched blob `68188a24badda635a5983fda1c381cdb694fd497` with zero content from connector; consequently no safe manuscript edit is possible. Further red-team review of the new inference-barrier theorem is appropriate. **P versus NP remains OPEN.**
