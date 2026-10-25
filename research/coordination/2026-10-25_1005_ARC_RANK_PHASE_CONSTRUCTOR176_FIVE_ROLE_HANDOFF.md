# ARC176: Rank-adaptive two-level constructor and exact all-input firewall

Timestamp: 2026-10-25 10:05 America/Los_Angeles. One ARC/FLMV research spine. ARC-EDGE-90 and P versus NP OPEN. No new/rescheduled/reactivated tasks.

## Verified construction
A genuine ordinary CNF path grammar P_j has p consecutive three-variable odd-XOR modules, four source ternaries per module, and canonically sorted unary/binary extras connecting at most adjacent modules. Extra clause density is capped at 16+6j per module owner at recursive depth j. The source streaming validator uses a four-bit XOR mask and logarithmic counters. Each boundary exposes at most three raw variables, but affine projection yields at most four feasible signatures, including just two for a one-coordinate interface. Partition p modules into ceil(sqrt p) blocks. At most 16 exact ordinary SAT children are constructed for each block by dense local renaming plus signed unit pins; all crossing clauses are checked at the parent through original named variables. A single sequential scan supplies block sources with O(sqrt N) physical block buffers, avoiding full-parent scans per child. Descendants lie in P_(j+1), including at most six new pins per module, through TWO REAL levels. The exact both-label source-gluing proof is in Role 1's LaTeX report.

For any one fixed all-input exact guest A with simultaneous (t,s), t>=1, a fixed-depth d path-promised contractor has the CONDITIONAL SAME-MACHINE upper envelope t_d <= 1+2^(-d)(t-1), s_d <= max(1/2,2^(-d)s), polylog factors suppressed. The construction is real only on this recognizable EASY PROMISE class. A general ordinary-CNF dispatcher recognizing the promise and calling A at full source scale outside it is total and exact, but does NOT improve arbitrary all-input worst-case exponents. Padded guest controls show the specific fallback saturation. No FLMV hard-language reduction is asserted to lie inside the easy class.

## Executed reproducible controls
Original 36 structured roots: 18 SAT / 18 UNSAT, separately checked by exact DPLL.
60 deterministic-seeded added-clause roots independently exhaustively enumerated: 28 SAT / 32 UNSAT.
Nine off-promise cases: exact full-source fallback.
Actual serialized first-level children: 1,456; actual second-level grandchildren: 9,656; DPLL leaf guest calls: 10,247; signature trials: 11,112; 192 additional top-level assertions, zero failures. Eager child output: 1,086,404 logical encoded bytes, 162,831 source clause-scan events counted separately; descendant encoded-buffer lower bound 508 bytes, NOT physical peak memory. Source module scaling p=16,64,256,1024,4096 yielded observed log child/log parent ratios 0.7775,0.7324,0.6991,0.6688,0.6561, consistent with the symbolic exponent lambda=1/2. No physical FLMV instruction/space calibration and no SAT complexity lower bound.

## Falsifiable next bridges
1. Role 2 constructive: obtain a fully CHARGED A-dependent method to normalize ALL ordinary SAT inputs, or a proven FLMV-hard image, into the local-projected-boundary regime without parent-scale lookahead or a false promise. Test high-rank non-affine and padded-guest controls.
2. Role 3 semantics: challenge original-name-compatible joins on genuine SAT and UNSAT inputs with two levels, overlapping pins, changed signs/contexts and nonlocal binary clauses; check typed cap 16+6j.
3. Role 4 accounting: validate the source-streaming and virtual guest-input simulation in the exact FLMV indexed-read-only-input random-access TM, every source/work bit read and written (including unchanged writes), index positions, control arithmetic, validator, failed routes, ancestor buffers and actual peak.
4. Role 5 red team: verify absence of all-input time-space improvement on full-source fallback; audit the easy path CSP bypass and nontransport to a FLMV-hard Cook image; keep executive ARC-EDGE-90 OPEN.
5. Role 1: preserve the achievable-set DAG and finite-hit conditional algebra only, updating its root ownership region without changing others.

## GitHub verified paths
- research/agents/lspv-1/2026-10-25_1005_LSPV-1_ARC_RANK_PHASE_CONSTRUCTOR176.tex
- research/agents/lspv-1/2026-10-25_1005_ARC_RANK_PHASE_CONSTRUCTOR176.py
- research/agents/lspv-1/2026-10-25_1005_ARC_RANK_PHASE_CONSTRUCTOR176_results.json

Primary references: Fortnow, Lipton, van Melkebeek, Viglas, JACM 2005; Freuder, AAAI 1990; Philippe et al., Automatica 2016. Related earlier project materials: ARC175, ARC-0007, INTERFACE-PROJECTION8, BOUNDARY-RANK-SWITCH80, AFFINE-NULLITY-BOUNDARY73.

END_HANDOFF_ARC_RANK_PHASE_CONSTRUCTOR176
