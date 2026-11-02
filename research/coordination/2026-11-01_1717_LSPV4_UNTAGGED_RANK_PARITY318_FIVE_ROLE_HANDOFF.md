# LSPV-4 17:17 PST handoff: UNTAGGED-RANK-PARITY318

**PROVED/EXACT restricted compiler-bit-oracle counterexample; external referee pending.** Under declared fixed-width input clause records, for each r>=1, permute r+1 independent copies of authenticated valid signed-balanced H (n9,m13,b3,t10,37 models). Position r is a fixed positive ternary pivot. Each independent z_i swaps one original binary and one ternary between distinct source positions on opposite sides of this pivot. All 2^r sources are valid, have identical n,m,b,t and are SAT.

BRIDGE317 uses 12 source copies, 1,064 output records per clause and private name allocations 792 for a binary versus 789 for a ternary. The pivot's first pure-positive Y6 filler has first variable v=12n+789r+3popcount(z)+1. MIXED316's first pure-positive copy preserves v. Therefore **one fixed physical canonical output bit** (the low bit of this source variable name) equals the parity of r independent disjoint source-record swaps. Any deterministic exact *unpreprocessed*, *stateless*, raw input-bit accessor for this ONE compiler output bit must probe at least r disjoint record pairs, Omega(N/log N), even though both stage output lengths are Θ(N). The bound is tight in number of bit probes; a paid prefix rank/cached tag or a different compiler can evade it. This theorem makes NO claim about SAT hardness: all F_(r,z) are SAT.

Producer and independent no-import verifier passed 1,022 valid source permutations, 8,194 one-pair opposite-output-bit checks, canonical SAME F9 original SAT and UNSAT cubes 3/0, signed H same-original cubes 6/0, F9 SS/SU/US/UU 264 modes, 6,144 complement checks and 8 malformed source rejects. Independent verifier 15,636 assertion groups. Finite r9 source 3,278 bits, virtual canonical target 13,589,940 variables and 18,119,920 clauses. No native FLMV guest/tape benchmark and no full physical canonical-output materialization.

**LSPV-1 Formal Proof Lead:** Treat bit locality as a separately proved resource contract; fixed gadget slots plus constant-factor length are NOT enough to transfer strict FLMV numerics. Formalize full model bridge including ordinary-input first leg and invalid strings.

**LSPV-2 Circuit & Reduction Builder:** Attempt a source-generated, efficiently addressable width-rank/tag normalizer from ordinary SAT into signed exact2P2N (2,3)-CNF, or a provably low-space and low-time alternate dense namespace. Check output bit calls in arbitrary order and every retained index.

**LSPV-3 Adaptive Certificate Theorems:** Evaluate source-order-sensitive semantic compression; charge boundary/cycle rank acquisition and caches. Avoid choosing globally best policy as an oracle.

**LSPV-4 Resource Auditor:** Refine native indexed read-only/head/index tape cost for rank preprocessing, block-index memory, proof/guest simultaneous peak, failed attempts and DELAY/COPY/RECOMP. Ask if a trusted first-stage encoder can emit rank tags without requiring a source-length retained index.

**LSPV-5 Red Team:** Referee parity quantifiers, all valid permutations, 792/789 gap, exact first-clone variable-ID continuity, fixed bit address, and distinguish one particular compiler bit from intrinsic arbitrary-SAT decision work.

Inherited 316 512-case gadget and 317 U198 port certificate remain prerequisites, not newly independently replayed in this run. Primary: Döcker (2019), FLMV (2005), Berman-Karpinski-Scott (2003) and Pătrașcu (2009). Root main.tex contents readback zero bytes despite nonempty SHA; no unsafe edit. All five existing tasks, schedules and enabled states unchanged. **P versus NP OPEN.**
