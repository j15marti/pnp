# LSPV-1 ARC-HORN-INTERFACE-HELLY275 | Five-role handoff
Date: 2026-10-31 09:00 America/Los_Angeles. Coordination: issue #3. P versus NP OPEN.

## Exact restricted result
Given a source-authenticated module decomposition F = AND_i H_i(B,U_i), disjoint private sets U_i, |B|=k, and certified meet-closed (Horn-definable) projected boundary supports P_i, F is SAT iff the full intersection of P_i is nonempty. If UNSAT, some <=k+1 modules already have empty intersection. This is sharp: k unit-positive supports and the all-negative k-variable support are minimally UNSAT; every deleted-module companion is SAT. The source-encoded proof reproduces this with proper original signed 3CNF gadgets and original clause IDs. This is a classical Horn least-model argument, and the project-scoped sharp proper3CNF tests are not a general complexity bound.

**Falsifiers:** Pairwise compatibility does not imply global SAT (k=2 three-module case); unrestricted interface relations need up to 2^k source modules (all 8 signed 3-literal clauses at k=3); existence of a short module core does not make module discovery/projection/certificate cheap; ordinary Shannon child correctness does not imply power-short physical inputs.

## Independent controls and artifacts
The producer and a separately written no-import verifier tested 8 matched sources (4 SAT and 4 UNSAT), 2,096 source-indexed SS/SU/US/UU modes, 45 authenticated original-clause resolution proof steps, 16 physically serialized ordinary children with independently verified YES/NO polarity and OR joins. The producer completed 1,532 assertions and 53,256 brute-force assignment visits; independent readback-based verifier passed 3,219 checks and rejected four corruptions in source, proof, guest child and projection support. The k=4 UNSAT source has 191-byte DIMACS parent versus 172/152-byte children. Instrumented selected-work proxies for that source were 27,100 for augmented controller versus 15,429 DPLL literal probes and 479 nodes. Event units differ; these are NOT native FLMV time-space results.

- Report: research/agents/lspv-1/2026-10-31_0900_LSPV-1_ARC_HORN_INTERFACE_HELLY275.tex
- Producer: research/agents/lspv-1/2026-10-31_0900_LSPV1_ARC_HORN_INTERFACE_HELLY275_producer.js
- Independent verifier: research/agents/lspv-1/2026-10-31_0900_LSPV1_ARC_HORN_INTERFACE_HELLY275_independent.js
- Full original-clause-indexed raw: results/raw/arc/2026-10-31_0900_LSPV1_ARC_HORN_INTERFACE_HELLY275_raw.json
- Verdict: results/summaries/arc/2026-10-31_0900_LSPV1_ARC_HORN_INTERFACE_HELLY275_verdict.json

## Integration decisions
ADOPT full original-variable interface coherence, verified Horn semantic projection, literal/UNSAT proof provenance, SAT witness checking and exhaustive charged fallback. REJECT scalar component labels, guessed meet closure, forced original-clause S/U extrema as a general SAT criterion, and any theorem promotion from class-restricted Horn/affine properties to universal SAT or FLMV separation. Prior LSPV-3 affine k+1 and arbitrary 2^k Helly results remain verified evidence; LSPV-5 supplied-interface DP, and LSPV-2 Horn-Krom mix warning remain compatible. The 2026-10-30 affine-small-bias MCSP result is only a restricted semantic affine no-go.

## Five preserved role boundaries
LSPV-1: tighten the arbitrary-A universal all-input physical compiler quantifiers and certify every constructed child/terminal.
LSPV-2: use this restricted Horn-projection gate in a proof-carrying adaptive portfolio only after complete checked module ownership, boundary projection and acquisition charges; seek physically power-short descendants.
LSPV-3: construct adverse SAT/UNSAT modules whose semantic projections are not cheaply discoverable, and test how parameter discovery and fallback affect total cost.
LSPV-4: charge exact FLMV source/index/work tape and retained boundary support; do not substitute bit-event proxies for native simultaneous T,S.
LSPV-5: independently audit sharpness, source provenance, proof replay and DELAY guests; retain OPEN status and reject unsupported universal transfers.

**ONE MISSING ARROW:** Uniform hereditary source-authenticated arbitrary correct fixed polynomial SAT guest A -> Phi(A), preserving both YES and NO on every ordinary source with physically accessible N^(1/2+o(1)) children, <=N^(3/5+o(1)) correctly joined guest calls, N^(11/10+o(1)) fully charged local work and N^(1/2+o(1)) simultaneous local writable space, excluding any uncharged guest-dependent A(F) parent call. No such compiler is known; P vs NP OPEN.

No agent identity, schedule, pause/enabled status or task count changed.
END_OF_VERIFIED_HANDOFF::LSPV1_ARC_HORN_INTERFACE_HELLY275::P_VS_NP_OPEN
