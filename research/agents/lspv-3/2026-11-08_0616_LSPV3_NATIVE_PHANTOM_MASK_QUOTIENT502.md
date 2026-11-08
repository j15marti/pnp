# LSPV-3/502 | Exact affine-mask quotient normalizes accepted historical-core proof DAGs

**2026-11-08 06:16 PST, America/Los_Angeles | Route B | PROVED/RESTRICTED + COMPUTATIONAL. All-rule R_mix341 and P versus NP OPEN.**

## Proof-chain and governance ledger

This result creates candidate evidence node **[P2-L3-502]**, directly refining **[P2-L3-499]**, **[P2-D3]** and the accepted subgrammar audit **[P2-D1]**. Full mixed translation **[P2-C3]**, all-legal-rule superpolynomial minimum **[P2-B1]**, noncircular same-fixed-calculus B3 **[P2-B2]**, and Route A all-input obligations **[P1-01]**, **[P1-03]**, **[P1-04]** remain **OPEN**. Read both full trackers, proof1 blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and proof2 initial blob `ca37d315d6713c8605a586c6188b2bc15bcd7d74`; issue #3 and recent peer reports. Do NOT confuse this theorem with historical complete grammar authentication.

## IDEA, pre-search falsifiers

**Hypothesis.** On any packet accepted by the recovered original LSPV-2/341 SOURCE/AND3/XOR checker, all affine-mask bits beyond its source-variable universe can be erased by projection, with no changed inference DAG, original source, parent graph, node charges or checker acceptance. Thus phantom mask bits do not reduce minimum paid logical work in this **accepted restricted checker language**, although untrusted raw packets must be checked BEFORE projection.

**Falsifiers:** (F1) an accepted AND3 affine alias depends on a bit outside the original E variables; (F2) mask projection changes a valid GF(2) XOR step or terminal zero-mask contradiction; (F3) a valid accepted input with negative masks fails normalization; (F4) projection before acceptance is incorrectly promoted as a safe verifier or full historical R_mix341 rule.

## SEARCH and source authentication

Read the complete November 2 five-role governing handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, AGENTS.md, CODEX.md, project skill, latest issue #3, LSPV-3/499 and /501, and current LSPV-1/503, LSPV-5/434, LSPV-4/494 discussion. Actual Grok report `GROKPROOF/2026-11-08_1130_PROGRESS.md` (blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`) and Claude `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` (blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`) were read as status critiques, not grammar authority.

Independently fetched the **exact original checker** `experiments/arc/lspv2_341_independent_verify.js`, blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`, full accepted balanced packet `results/raw/arc/2026-11-07_2224_LSPV3_491_BALANCED_341_PACKET.json`, blob `481423a2f5271ab600bbc2f9a526fe62523239a9`, and source-binding adapter `experiments/arc/lspv3_490_external_source_bind.cjs`, blob `b113119b7b87dac7510603804d91918e80f301b0`. The recovered checker is **instance-specific** and includes the hardcoded signed cubic-Tseitin SOURCE grammar and proof length; it is not a generic historical RES/DEF/LOCAL-CONVERT verifier.

Required external change-aware inspected documents: `konard/p-vs-np/scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; `tanyongkiam/cake_lpr/README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; `peitl/short-proof/README.md` blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab`; `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`. These describe independent proof-status, verified-checking, and minimum-proof mechanisms but **none authenticates missing /341 RES/LOCAL/DEF bytes**.

Primary literature: Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, revised 2026-10-24, Theorem 7.2 (syntactic `Res(PC_r/F_p)` restricted-family hardness); Haken, *The Intractability of Resolution*, TCS 1985 (ordinary Resolution PHP); Cook's Extended Resolution shortcut as a mandatory proof-system comparison. See https://arxiv.org/html/2610.00837v2 and https://github.com/meelgroup/frat-xor/blob/main/format.md . These are **proof-system-qualified** bounds, NOT historical R_mix341 or all-algorithm bounds. GitHub repository tool and public web searches were used; a separate Google-branded client was not available.

## ITERATE: exact accepted-language quotient normalization

Let E be the number of original edge variables in one accepted original-source /341 fixture. The original checker represents each affine equation as `mask` (arbitrary BigInt-parseable signed string) and RHS in {0,1}; AND3 tests its truth-table equivalence **only for E original coordinates**, XOR checks bitwise BigInt XOR equality, and its sink requires mask 0 and RHS 1. It currently **does not range-check all mask bits**.

Define the projection

$$
\pi_E(m)=m\mathbin{\&}(2^E-1),\qquad
\pi_E(a\oplus b)=\pi_E(a)\oplus\pi_E(b).
$$

**Theorem 502.1 (PROVED/RESTRICTED).** Given any accepted packet P in the exact recovered /341 SOURCE/AND3/XOR checker language, replace the mask of **every** affine-annotated node by the canonical nonnegative decimal numeral for `pi_E(mask)` within its own fixture. Leave every clause, charge, factor truth table, node ID, rule, premise, context, source witness, and RHS unchanged. The resulting packet P' is also accepted by the same recovered checker, has identical original source and identical charged proof DAG, and uses at most E bits per affine mask (plus O(1) for the numeral zero). This result does not assert a bounded normalization of RES/DEF/LOCAL/branches, which that checker does not implement.

**Proof.** SOURCE and all non-affine validations are unchanged. At an AND3 node, each relevant checker test consults only bits 0,...,E-1, so replacing the mask by its E-bit truncation leaves the support-membership test and all eight-or-fewer truth-table comparisons unchanged. At an XOR node, if the accepted masks satisfy `m=m1 XOR m2`, the ring-of-bitvectors homomorphism above gives `pi_E(m)=pi_E(m1) XOR pi_E(m2)`; the RHS is unchanged, so the derived node still passes. The final sink was originally mask zero and remains zero. By induction in the existing acyclic proof order, all accepted nodes stay accepted. No antecedent is duplicated, created or deleted. QED.

**Corollary 502.2.** For this accepted-language checker, the optimum fixed weighted cost over all accepted packets equals the optimum over E-supported affine-mask packets, since the latter are a subset and the theorem maps every member of the former to one of the latter at exactly the same weighted nodes. For q affine annotations, normalized mask payload has O(qE) bits, independent of originally extraneous phantom bits. The *whole* certificate also has source/ID/table/witness/provenance fields, so this is NOT a proved polynomial whole-certificate normalization for the full R_mix341 system.

**CRITICAL validation boundary.** The projection is **only a post-acceptance normalization for proof-theoretic analysis**. Projecting a *rejected* packet before checking can erase an invalid unmatched high bit and make it accepted. Thus an accepting adapter must first run the raw unchanged historical verifier, then source-bind, then optionally project an already accepted proof; never repair unknown evidence silently. The earlier /499 range firewall remains a safe reject-only guard.

## Reproduction and deliberate falsifiers

Actual unchanged original checker validation logic was fetched and executed in V8, changing only its Node file-input/output stubs. Original balanced 7-fixture source packet passed **30,714 assertions**. For each fixture, changed both direct AND3 parents of a genuine XOR join by the identical extra bit at `E+13`. The recovered checker **accepted**, again 30,714 assertions. The projected 157 affine row annotations were checked and **accepted**. Independently changed those two masks to `m-2^E` (negative BigInts with identical low E bits): again all fixtures accepted, and all normalized packets accepted, preserving 30,714 checks. A **single-parent** extra bit was rejected by the raw checker but its **premature projection was accepted**, establishing the essential hostile-control ordering. Exact original source and source-binder controls were unchanged; the existing /499 suite contains 324 same-length satisfiable source replacements rejected. The standalone published Node CLI is **not claimed executed here**.

The bridge uses two independent original AND3 row parents, so no hidden extension variable or branch assumption is reused. It is not a proof of any new UNSAT result or a hard-family lower bound. Negative tests rule out F1-F3 in the tested source packet; F4 is explicitly barred in the theorem statement. The general lemma follows from the checker code's exact local tests, not finite extrapolation.

Source provenance: 7 original signed cubic-Tseitin fixtures (6 bridgeless, 1 bridge negative control); original `K4` is 4 vertices, 6 variables, 16 strict 3-CNF clauses, UNSAT for odd charge and SAT for even. The proven exact restricted binary-premise cost 4h-1 is prior /491,/499 evidence; this run proves the new quotient equivalence on all accepted packets of that checker, not a stronger cost lower bound.

## Separate logical and implementation resource ledgers

Logical work: q paid inference nodes unchanged, same rule weights; all branch/AND dependencies and shared nodes retained. Logical span and DAG dependency edges unchanged. Affine evidence: E original-variable bits per normalized mask, O(qE) row-bit payload; can be **larger** than original signed short negative numeral, so do not claim non-increasing encoded length for every accepted input. Constructed normalizer: O(q) row visits, integer bit-projection O(E) bit work per row plus input parsing and output serialization; peak space includes the loaded packet and a complete copy (O(|P|+qE) bits), not an FLMV small-space claim. Original verifier execution, parsing, full source checking, certificate construction, all sibling and failed checks, file reads, GitHub fetches, publication/readback and transient allocations are separate from ideal W_R. No code-level same-machine time-space transfer is asserted.

**Published artifacts**: executable `experiments/arc/lspv3_502_phantom_projection.js`, blob `67db4ecb0d0ae895f50f48b0aadc0378b7c348a7`; raw `results/raw/arc/2026-11-08_0616_LSPV3_502_PHANTOM_QUOTIENT_RAW.json`, blob `f1ea0676920b46ea887e8362bef462540d6e8bf4`. Source-vs-raw packet acceptance does NOT itself fill an absent RES/DEF/LOCAL interface. Full readback was performed for these two paths.

## Next exact obligation

**[P2-D1]** still needs original historical accepted-byte syntax and weights for RES, DEF facets, LOCAL-CONVERT, private/exported wires and assumption discharge, including original-source provenance and paid cross-type conversion. **[P2-C3]** needs source-retracting polynomial translation of every such legal rule or a typed LEGAL counterexample; **[P2-B1]** requires a superpolynomial worst-case minimum over ALL permitted mixed DAGs and shortcuts, and **[P2-B2]** needs noncircular B3 for this same fixed calculus. All remain **OPEN**. Root `main.tex` not modified, historical grammar and weights unchanged, no task or 2A/3B allocation changes. **P versus NP remains OPEN.**
