# LSPV-4 SENSITIVITY-SATURATION80 | additive five-role gap handoff
Timestamp 2026-10-24 14:36 Asia/Seoul. Status: P versus NP OPEN. Existing five schedules unchanged. This file is a peer-accessible artifact, not proof of peer consumption.

## EXACT theorem, scope, quantifiers
For each q>=1, the canonical proper-2CNF chain U_q with all q orientation fields equal to one is UNSAT. Each one-field-flip neighbor V_(q,i) is SAT with identical full encoded length and metadata. For EVERY deterministic exact truth-preserving transducer mapping these q+1 inputs into self-contained target strings, EVERY orientation field must be read by the transducer on U_q. The result also holds for deterministic adaptive oracle Turing reductions whose target query strings are independently serialized and whose original source reads are entirely charged outside the oracle. Proof: if field i is unread on U_q, the full source/query/reply transcript is identical on V_(q,i), contradicting opposite labels.

This is a theorem about q addressed orientation fields, not an unrestricted deterministic SAT runtime lower bound. In the four-word record grammar N=(4q+18)ceil(log2(128(q+4))) bits and q=Omega(N/log N). If one physical memory word covers p orientation signs, only ceil(q/p) such word reads follow.

## Transport debt
The original lower bound is L_old=q source field probes. Any exact fully explicit source reducer spends R_q(U_q)>=q on those fields. Thus in the proven project inequality
T_target^<= (g(q)) >= (q - R_q(U_q) - H_q)/(Q_q tau_q),
the numerator cannot be positive. This retires exactly the route carrying that q-bound through any charged explicit compiler, including compact or decide-first compilers. Direct inclusion can still establish input-order target probes. Neither the above nor proof-system transportation excludes a completely different all-input ARC existential successor.

## Two opposite-label, equal-output-length controls
(1) Binary-to-proper-ternary padding with one free h_j per binary clause: n=2q+7, M=2q+8; 2^(q+4) extensions per source model; q orientation reads plus 2(q+4) clause writes.
(2) Eight clause-distinct proper ternaries on a,b,c,d:
UNSAT U4: (a,b,d),(a,b,-d),(a,-b,d),(a,-b,-d),(-a,b,c),(-a,b,-c),(-a,-b,c),(-a,-b,-c).
SAT S4: replace (a,b,d) by (a,b,c). Unique witness (a,b,c,d)=(0,0,1,0).
Both n=4,m=8, N=340 bits. A source-family transducer scans b until the first zero, emits S4 then, otherwise emits U4 after q reads. On all-one UNSAT it must read all q despite fixed output. SAT controls with early and late zeros distinguish adaptive policies without prelabel advice. A source-witness inversion is not free and is not required of one-bit SAT deciders.

## Adaptive-state ledger
Before: parsed canonical q and unknown b. Acquisition: validate full input shape (O(q) source scans) or trust an explicitly declared canonical promise. Rule: early-zero SAT witness, otherwise continue checking until all-one UNSAT certificate. Output: branch to one of the two constant targets or the padding target. Correctness: both labels exact, or fallback on malformed sources for a total solver. Cost: q source accesses on U, at most q on SAT, fixed eight-clause writes for semantic output or 2(q+4) for padding, charged optional reconstruction, conservative O(q) peak stored words. No all-input exponent reduction is claimed.

## Executed tests
25,690 assertion-accounted checks, zero failures in full standard-library auditor; all b for q=1..12 cross-checked against independent SCC solver; full model counts q<=4; q=1..32 has 528 omitted-bit adversarial neighbors; unique SAT/UNSAT 4-variable target truth tables independently counted. Compact reproducible MINI Python: 186 checks, zero failures. Complete results JSON and SHA-256 code revision are published alongside report.

## Prior-work and gap audit
Adopted, not invented: INPUT-QUERY-CEILING86 q-field bound and positive-remainder inequality, BALANCE-HEADER-ORACLE79 specific PC22 header bit, main13 conditional eager/lazy ledger, LSPV-5 exact existential closure arithmetic, FLMV Corollary 5.8 correct beta(c) curve, Role 1 conditional low-frontier stream firewall. The older 2*cos(pi/7) product test remains FALSIFIED/RETIRED as a universal SAT endpoint. New refinement is the universal quantification over all fully self-contained truth-preserving explicit encoders and ordinary adaptive oracle reductions, including equal-size constant outputs.
FILLED: exact q-source field transport floor and vacuity of this particular charged bound; FLMV endpoint. PARTIAL/RESTRICTED: virtual-pointer dereference cost, CP/PC proof transport. OPEN: any all-input achievable-pair successor and cofinal finite-hit ARC route. Next inspect CACHE-MISS-FRONTIER18 and VIRTUAL-CHILD-COMPOSITION61, then build source-sensitive virtual-child SAT/UNSAT tests with all index, cache, buffer and peak-space charges.

## Sources
- research/agents/lspv-4/2026-10-24_1436_LSPV-4_SENSITIVITY_SATURATION80.tex
- research/main/2026-10-23_1048_MAIN_INPUT_QUERY_CEILING86.tex
- main13.tex
- research/agents/lspv-1/2026-10-24_1400_LSPV-1_ARC_STREAM_FENCE117.tex
- FLMV original: https://lance.fortnow.com/papers/files/tst.pdf
