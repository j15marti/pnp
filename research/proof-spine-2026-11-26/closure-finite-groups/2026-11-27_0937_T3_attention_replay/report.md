# T3 / Closure Finite Groups: finite-precision attention simulation and indexed native replay

**2026-11-27 Pacific. PROVED (model simulation and supplied-certificate checker); COMPUTATIONAL (two exact replays); OPEN (universal aggregate contraction, P vs NP).**

## Model and lemma
Fix a uniform controller whose entire state (including weights, indices, intermediate arithmetic, all tracks and cache) has a fixed polynomial bit bound in original input N. Each step comprises polynomially many b-bit integer/fixed-point operations, with prescribed rounding and overflow semantics, exact hard selection with deterministic tie breaking, or a polynomial-time implementable finite-precision softmax/other operation. Polynomial depth, width, number of invocations, precision and parameter generation are all charged. A deterministic bit machine simulates each operation by its bit algorithm. Dense hard attention over W records of dimension d costs O(W^2 d poly(b,log d)) bit arithmetic plus indexing, copying and output, not one unit of work. A serial deterministic tape simulation of a bounded explicit array computation can scan a serialized workspace of S bits for each indexed access, charging O(S poly(log S)) bit work per access. Thus any fixed-polynomial-work realization in this exact model is simulable in P; the converse follows by allowing ordinary bit operations and random access. This does not establish that a learned attention model, arbitrary exact-real softmax, nonuniform parameters, or any polynomial-depth but unbounded-fan-in opaque operation has these properties. A fixed-power tape transport bound cannot be transferred as an all-polynomial lower bound for unrestricted indexed models.

**Exact lookup lemma.** Encode addresses as d=ceil(log2(max(2,W))) signed binary coordinates, each +/-1. The score q_i dot k_j=d-2Hamming(i,j) has a unique maximum d for the requested existing address, with gap at least two. Integer scores need O(log(d+1)) bits. A hard maximum fetch returns the exact value (no softmax approximation), including a pointer or sign bit. Invalid addresses and duplicate IDs must be rejected. For a rooted signed forest use p_{t+1}(v)=p_t(p_t(v)), s_{t+1}(v)=s_t(v) XOR s_t(p_t(v)). Inductively these encode a path of 2^t edges, padded by root self-loops with zero sign. After ceil(log2(max(1,h))) rounds for forest height h, all pointers reach the component root and carry the XOR phase. Forest construction, cycle consistency and the proof of root/minimum-label identity are separate charged tasks. This run uses BFS construction followed by independent doubling and comparison, not a new parallel BFS algorithm.

**Unordered local proof check.** For a supplied explicit native-normalized resolution proof of L bits, reject duplicate IDs, check each native B axiom from exact signed roots or a valid whole-network complement symmetry gauge, check each resolution node against its two parent clauses (both IDs strictly smaller), and require an empty terminal. Induction on ID proves soundness even if validation is performed simultaneously. After normalization, a uniform bounded-fanin Boolean checker can compare all explicit padded literal pairs and IDs, check memberships, resolvent set equality and clause validity with parallel AND/OR reductions in O(log(N+L)) depth and polynomial size; it need not follow the derivation's depth. This is verification of a supplied proof, not polylog-depth discovery, nor a claim that source hashing and forest acquisition share that depth. Indexed execution avoids dense score materialization; dense alternative is charged. Space and CM: for explicit input+proof length M=N+L, conservative fixed polynomial bounds by simulation, with CM <= T*S on the same serial implementation. No measured bit-time, space or CM claimed.

Falsifiers: mismatched pinned hash; disagreement of BFS and doubled root/phase; accepted malformed parent or zero pivot; treating an unverified guarded theorem as unconditional; hidden nonuniform parameters or resetting the original N budget. Both instance hashes and proof hashes verified, both corrupted zero pivots rejected.

## Shared inputs
Read the pinned E/B, identifier, UNSAT and release directives, AGENTS/CODEX and skill, communicating roster and issue #328. No checkout available in the connector isolate; preflight and manuscript build not executed. Pinned corpus and exact compiler are recorded in the certificates. Source DIMACS IDs and native IDs recomputed with SHA-256 tested against empty and abc vectors. Map hash checked but map not supplied to native analysis. Same empty guard, ROOT residual in both. Source-only exact equality, local balance table support and deduplication (no full affine/2SAT closure implemented) yield UNKNOWN; independently replayed T4/X01 proof makes hybrid UNSAT. Discovery of parent proof not rerun; import/read/verify cost must be added to its original discovery, not counted as a new independent native decision procedure. No reference proof or label used as a solver primitive. No fresh MFC-13/Nov 26 replay or transport family experiment completed; shared cases took priority. No role manuscript reconciliation claimed.

### EB-JOINT-24@e84a0ab6dc6f
{
  "instance": "EB-JOINT-24@e84a0ab6dc6f",
  "instance_id": "STRICT-EB4-v1:sha256:e84a0ab6dc6f74deb8daeea2ccd41cca90e3d1294411877a813471760897c209",
  "N": 5363624,
  "CNF": {
    "alias": "JOINT-24",
    "instance_id": "DIMACS-CNF-v1:sha256:68d21d234f32956200617b3a714d9f81f992cf2fa373f1285d639d6a703fa22b",
    "short_id": "CNF-JOINT-24@68d21d234f32",
    "sha256": "68d21d234f32956200617b3a714d9f81f992cf2fa373f1285d639d6a703fa22b",
    "N_bits": 13416
  },
  "sha256": "e84a0ab6dc6f74deb8daeea2ccd41cca90e3d1294411877a813471760897c209",
  "source_map_sha256": "dd44a7eee2ade0cb42bf9e29c08bd1bc96dad43dfe2a5e06b02f1d09fd97c998",
  "guard": "EMPTY",
  "residual": "ROOT",
  "sourceOnly": {
    "ports": 75724,
    "components": 643,
    "forestMaxDepth": 1575,
    "adjacencyVisits": 184582,
    "pointerRounds": 11,
    "pointerGathers": 832964,
    "denseScorePairs": "63075365936",
    "localBalanceRows": 12608,
    "nonfullFactors": 788,
    "distinctTables": 394,
    "unconditionalSingletons": 0,
    "decision": "UNKNOWN (local equality and balance-table deduplication only)"
  },
  "cooperative": {
    "records": 292,
    "axioms": 137,
    "resolutionRows": 155,
    "parentGathers": 310,
    "parentLiteralReads": 1177,
    "maxWidth": 9,
    "valid": true,
    "decision": "UNSAT",
    "parent": "CERT-v1:sha256:90e124b67e0ca91753386857a0b47edb4f8d82c75285edc0b34b710cc6dc9dc9",
    "mutatedPivotRejected": true
  }
}

Certificate: https://github.com/j15marti/pnp/blob/d9baaac88d16f17ef406ac7795cdfe493280e6bc/research/proof-spine-2026-11-26/closure-finite-groups/2026-11-27_0937_T3_attention_replay/JOINT-24-attention-replay.json
Broadcast: https://github.com/j15marti/pnp/issues/328#issuecomment-7224664031

### EB-RANDOM-3CNF-40@8a18e86479df
{
  "instance": "EB-RANDOM-3CNF-40@8a18e86479df",
  "instance_id": "STRICT-EB4-v1:sha256:8a18e86479df916ea5c7fdd760ccd561e4fea3737a94517ab8dc2d28cc7e6bdb",
  "N": 5027816,
  "CNF": {
    "alias": "RANDOM-3CNF-40",
    "instance_id": "DIMACS-CNF-v1:sha256:cfaccaa692ef736e2b5eaadde2eda83ca7351e30cf066237fbe5c63eedb55e67",
    "short_id": "CNF-RANDOM-3CNF-40@cfaccaa692ef",
    "sha256": "cfaccaa692ef736e2b5eaadde2eda83ca7351e30cf066237fbe5c63eedb55e67",
    "N_bits": 17480
  },
  "sha256": "8a18e86479df916ea5c7fdd760ccd561e4fea3737a94517ab8dc2d28cc7e6bdb",
  "source_map_sha256": "3a3dc143d60bd7b6b2f2d17b1eaa32ccdb2d3613d23d68489c48abd40ca219c3",
  "guard": "EMPTY",
  "residual": "ROOT",
  "sourceOnly": {
    "ports": 71060,
    "components": 593,
    "forestMaxDepth": 1471,
    "adjacencyVisits": 173234,
    "pointerRounds": 11,
    "pointerGathers": 781660,
    "denseScorePairs": "55544759600",
    "localBalanceRows": 11776,
    "nonfullFactors": 736,
    "distinctTables": 368,
    "unconditionalSingletons": 0,
    "decision": "UNKNOWN (local equality and balance-table deduplication only)"
  },
  "cooperative": {
    "records": 594,
    "axioms": 203,
    "resolutionRows": 391,
    "parentGathers": 782,
    "parentLiteralReads": 4206,
    "maxWidth": 18,
    "valid": true,
    "decision": "UNSAT",
    "parent": "CERT-v1:sha256:2bd9984cb03aaf7fd82f89c3239038a40782b837e561713778bca3d09508dd2c",
    "mutatedPivotRejected": true
  }
}

Certificate: https://github.com/j15marti/pnp/blob/3c19d3e8d658eddfa8ae6831d5ce6615827582ae/research/proof-spine-2026-11-26/closure-finite-groups/2026-11-27_0937_T3_attention_replay/RANDOM-3CNF-40-attention-replay.json
Broadcast: https://github.com/j15marti/pnp/issues/328#issuecomment-7224665791

## Research checks
Merrill and Sabharwal, TACL 2023, https://aclanthology.org/2023.tacl-1.31/ log-precision constant-depth transformer simulation under their hypotheses, not arbitrary polynomial depth. Svete et al., 2026 preprint https://arxiv.org/abs/2605.30523 on padded/looped transformer expressivity, not a SAT discovery theorem. Fresh searches: official GitHub openai/gpt-2 src/model.py blob 230b83cc2ac7582b4a22e9db3c2d8916dfe2ea9a; xai-org/grok-1 model.py blob 87d700d9b5fde6d86dda2883192861195b7312ae; google-deepmind/transformer_grammars README blob fb99381397a6aeb4f3affe25635ba0bae1466822; lammich/lrat_isa README blob 9a0da1d6b8c59338322a896efe878363eea34474 (formally verified LRUP checker, not used in experiment). Anthropic official connector lookups anthropics/transformer-circuits and anthropics/circuit-tracer README returned 404; org search circuit tracer empty. No external implementation executed. Internal searches MFC-13 reciprocal fibers, free attention simulation, CHARGED-UNSAT-TRANSPORT1 and relevant issues found prior static-ratio reports and dynamic replay notes at search snapshot f0e4249167d2a3ef2a8c1c2ddc77d09ca831ca04; finite branch search empty, general branch listing first page inspected, no branch checkout. No new relevant external theorem completing the universal step.

DISJ: N/A to positive simulation lemma (no communication LB). Relativization: simulation works for explicitly implementable operations, not opaque oracles; no separation. DTISP: compatible with polynomial simulation, no improved simultaneous bound asserted. Configuration counting: polynomial-space gives exponential configuration upper bound, not a polynomial-time lower bound. Natural proofs/algebrization: no circuit lower bound or separation advanced. Exact counts in results.json, execution was V8 indexed serial; Node replay.js provided, standalone Node execution not run. Publication gate not met; no public resolution claim.

## Next target
Replace supplied proof parent queries with a uniform affordable *acquisition* rule, or prove a restricted obstruction to that rule. Test whether a logarithmic-depth local orientation hierarchy produces an explicit certificate of polynomial total size on an infinite family, not merely a shallow checker. Preserve all branches and charge the search.
