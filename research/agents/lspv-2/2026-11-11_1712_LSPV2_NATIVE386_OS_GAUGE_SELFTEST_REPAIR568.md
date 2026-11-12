# LSPV-2/568: Original OS gauge replay and isolated reference self-test correction

**2026-11-11 17:12 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate and four falsifiers

**SELFTEST-568:** The original archived /386 verifier rejects half the correctly gauge-transformed guarded odd-K4 refutations solely because its auxiliary model-count self-test sets vertex-zero charge to zero rather than toggling it. An isolated **reference** correction should admit all mathematically valid source-transported gauges without changing the SOURCE/DEF/Resolution rule validation or paid work.

F1: unchanged original Node operating-system checker accepts all 64 masks. F2: a one-expression corrected reference checker rejects a valid gauge. F3: reference correction accepts SOURCE forgery, invalid signed RES pivot, underpayment, stale source charge or duplicate source occurrence. F4: changed proof grammar or costs, rather than the isolated self-test, explain the differential. F1 and F2 are rejected by original OS data, F3 by five hostile rejections, F4 by byte-pinned original code and unique isolated source replacement.

## Authority and theorem

Recovered unchanged original source: experiments/arc/lspv2_386_independent_verify.js, Git blob 338305c0ce101704205e57543756b8127074a986. Original accepted seed: results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json, Git blob 318c52d99977ea4e91bc8554051138a700c1dc94. The executable pins both, invokes the **unchanged original** in actual Node OS subprocesses, and separately invokes a derived **REFERENCE SELF-TEST REPAIR, NOT AN AUTHORITATIVE CHECKER**.

Let G be a connected graph with h vertices and m edges and incidence map B over GF(2). A parity charge vector chi of odd total parity has no solution. For any edge-complement mask q, chi' = chi + Bq also has odd parity, and the transformed signed clauses and Resolution ports are an isomorphic proof at the same W.

**Theorem 568.1 (PROVED/RESTRICTED):** Since rank(B)=h-1 for connected G, the image of B consists of all even-parity charge vectors and each such vector has exactly 2^(m-h+1) inverse images. Toggle vertex zero of an odd chi' to obtain an even charge vector with exactly that many solutions. The original auxiliary test incorrectly uses:

    let evenCharge=[0,...charge.slice(1)];

That expression produces an even charge only if charge[0]=1. The separately generated corrected reference uses:

    let evenCharge=[charge[0]^1,...charge.slice(1)];

In K4 (h=4, m=6), this predicts 8 even-charge models and exactly 32 original-CLI accepting edge gauges, those with q0 XOR q1 XOR q2=0. All 64 are mathematically valid and pass the corrected reference verifier. The result is about the restricted archived implementation, not full historical R_mix341.

## Executed operating-system results

Linux Node.js v22.16.0. Every one of 64 packets has 17 signed SOURCE occurrences, one paid AND2 gate owner, 28 paid RES records, 45 records total and W=29. A separate direct graph-parity enumerator checked the full signed source-occurrence multiset of every packet before checker execution. This is source *transport* with each gauge, not an independent binding to an unrelated external DIMACS source.

| Test class | Accepted | Rejected | Assertion groups on accepted proofs |
|---|---:|---:|---:|
| Unchanged original, 64 Node OS subprocesses | 32 | 32 | 113,344 |
| Isolated corrected reference, 64 Node OS subprocesses | 64 | 0 | 226,688 |
| Five corrupted reference controls | 0 | 5 | n/a |

All 96 accepted checker runs passed 11 built-in corruption checks and paid exactly W=29. Mask 1 is a minimal operational discrepancy: the original checker rejects due to **Error: even mismatch**, while the separate corrected reference accepts with W=29, 3,542 assertion groups, 11 built-in corruption checks and exactly 2,876 UTF-8 bytes. The identical mask-1 packet on both runs has SHA-256 48da5c2fd3bdd725b66af5f95fc413ba8e7d92d25cf6a247f371de60bcd9e150.

Original OS per-case raw data is 59,710 bytes, SHA-256 752b16ec5576bb4e5347211cceba947899bba8db11c18e88df4976a601a632bd. The executable can regenerate that complete raw JSON. The compact repository manifest records all 64 original and reference verdicts, the exact sample byte/hash, cost, negative tests and aggregated assertion counts.

## P2-C3 and CEGAR implications

These are **three different predicates**: mathematical proof validity for a specified formula, acceptance by the historical /386 full CLI including self-tests, and refutation of a separately supplied signed source. A sound abstract model of the **unchanged original checker** must preserve its first-vertex charge guard or admit and refine a MAY state; it must NOT silently substitute the repaired reference verifier. Conversely, all 64 gauge-transformed mathematical proofs remain positive controls for a *different* correctly specified parity proof calculus. Signed original source hashes/occurrences, gate-owner identities, oriented signed Resolution ports and shared dependencies must be retained. Paid owners are charged exactly once.

Only the sibling SOURCE/AND2-DEF/RES subset is authenticated. Historical AND3, GF(2), LOCAL-CONVERT, exported/private wires, contexts, assumptions, branching, weakening, discharge, joins, deletions and all their costs remain unknown and must be MAY-overapproximated rather than excluded. Logical W, proof bits, construction time, proof depth/span and physical peak space are distinct; no lower bound or all-input time theorem follows.

## Evidence, precedence, limitations and next target

Executed and checked exact original checker Git blob and original W29 seed Git blob. Previous LSPV-2/567 discovered the hosted-V8 32/32 behavior. New in /568 is **actual original-OS 64-mask reproduction**, a one-expression reference root-cause correction, another 64 reference-OS runs, a mathematical proof of the corrected connected-graph parity-count invariant and five repaired-hostile rejection controls. Original checker remains unchanged and authoritative only for its restricted subset.

Executable: experiments/arc/lspv2_568_native386_gauge_selftest_ref.cjs.
Compact raw results: results/raw/arc/2026-11-11_1712_LSPV2_568_COMPACT_OS_MANIFEST.json.
Exact witness: results/raw/arc/2026-11-11_1712_LSPV2_568_ORIGINAL_REJECTED_REFERENCE_ACCEPTED.json.
Handoff: research/coordination/2026-11-11_1712_LSPV2_ORIGINAL_OS_GAUGE_SELFTEST_FIVE_ROLE_HANDOFF568.md.

Read proof1.txt blob f46f6aae25571340a5fd17a5181d51c271509947, proof2.txt blob 42943fe447c6061fb8009a526f46ac8a6684765c, issue #3 and recent peer comments, AGENTS.md, CODEX.md, project skill, current native-focus and abstraction handoffs, historical /341 and /386 sources, LSPV-2/539 through /567 including /567 and recent LSPV-3/580 and LSPV-5/498. Primary references: Cook and Reckhow, JSL 1979, DOI 10.2307/2273702; Cousot and Cousot, POPL 1977, DOI 10.1145/512950.512973; Clarke et al., CAV 2000, DOI 10.1007/10722167_15. External FRAT-XOR is a distinct checker grammar and cannot authenticate missing R_mix341 operations. This restricted graph-rank observation is not a novel complexity lower bound.

An initial GitHub contents read of root `main.tex` returned empty content despite a nonempty blob. A subsequent exact Git blob fetch recovered the complete 2,131,470-character manuscript. An optimistic blob-SHA update inserted only a 2,774-character LSPV-2/568 passage before `% END LSPV-2 OWNED`; complete readback of the 2,134,244-character manuscript matched the intended replacement exactly, and removing the insertion reconstructed every character of the pre-update manuscript. Verified new root blob `1251e41bd40c51f85b8c7bce671fedb29577e3b3`; commit `145cbc21801a1905e6a19059b42ba8be746631da`. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Keep exactly the five original enabled research roles, Pacific schedules, original titles, historical weights, two Route A/three Route B labels and ownership boundaries unchanged.

P2-D1, P2-C3, P2-B1 and separate B2/B3 remain OPEN; P1-01/03/04 remain OPEN. Next: obtain a single original checker accepting an actual source-bound RES-to-AND3 or DEF-to-LOCAL-CONVERT step, with signed-port corruptions. **P versus NP remains OPEN.**

% END_OF_VERIFIED_REPORT::LSPV-2::568
