# LSPV-2 to LSPV-1 Formal Lead and LSPV-4 Resource Auditor: CIRCUIT-PRIMARY-SOURCE-SELECT174

Timestamp: 2026-10-27 05:12 UTC. This is an additive, architecture-scoped result; P versus NP and ARC-EDGE-90 OPEN. No roles, tasks, enabled states or staggered schedules changed.

## New proof with an independent finite audit
For fixed q>=3,m>=1, w=ceil(log2(q+1)), N=m[1+3(w+1)], K=next-power-of-2(q+3m), J=h(h+1)/2, the exact fixed oblivious-sort SAT *witness verifier* has G=Gf+Gs+Gr+Gc Boolean gates, where Gf=K*J*(13*w+32)/2, Gs=19+(K-1)*(4*w+18), Gr=3*K*J and Gc=m*(36*w+15)+m-1.

**New primary-input inverse:** every original clause-source x bit and witness z bit has a table-free signed direct consumer list. Direct fanout is exactly 1 (active), 13 (identifier bit), 4 (polarity bit), or 2 (witness bit). Each source bit also has four own physical pin clauses, while witness bits do not. Thus physical source-CNF occurrence counts are respectively 8, 56, 20, 8, not identical to Boolean fanout. Uniform arithmetic computes ordered signed GateSelect/Rank and source OccSelect/Rank in O(log^3 G) bit operations and O(log G) live register/index bits. Original x-pin literal *sign* requires actual source bit read at virtual evaluation.

**New compiler-local inverse:** all G Boolean gate AND/OR opcodes are recovered from sector/offset arithmetic. The two argument-clone variables in each 13-row proper ternary compiler gate appear seven times each, in exact signed clause slots. Six local padding names appear exactly twice each. The 2N+6 primary/final pin auxiliaries each appear four times. These ranges are disjoint and support full source OccSelect/Rank without the gate list or occurrence table. Gate OUTPUT variables are a separate class and remain partly open.

**Executed:** seven (q,m) circuits (3,1),(4,1),(3,2),(5,2),(7,2),(6,3),(9,2). Independent ground truth verified 38,528 Boolean gate opcodes, 1,725 signed primary references, 7,564 primary source-CNF literal occurrences and 1,003,224 local clone/pad/pin source occurrences, zero failures. The 173 exhaustive 8,192 source/witness semantic controls and eight-clause UNSAT control were rerun with exact same raw SHA256 5eff02d7d9abc9eb2d1b0efb54a15770d5f71cfeca6f2f8a7dd2290fb7c4ccc4. The 171 tape simulation/equality controls (340 pairs, 9,320 matching source/simulated states) reproduced raw SHA256 3543f3695f2990c4586168ba4cf8cf1e2adecd5d40244f1700bc00419349b80b.

## Boundaries and no illicit transfer
Source compiler n0=9G+3N+q+8, m0=13G+4N+12; actual two-level signed exact-(2,2) regularizer has m2=4048m0+5888n0. This is EXPANSION, not ordinary-SAT contraction. Signed exact-(2,2) does not imply stricter clause-monotonicity. The uniform *witness* verifier is not full all-N-bit SAT decision circuit C_{A,N}. P=NP only supplies some unknown finite exponent K, not d=1.802,s=o(1).

Preserve separate machine ledgers. M1 initial footprint P1>=N; Mk read-only sequential source input plus work space Sk; RAT indexed read-only input and writable/index space. The fixed-k rescan construction is T1=O(Tk*(N+Sk+log(Tk+2))), P1=O(N+Sk+log(Tk+2)), including every head crossing and virtual output bit, not an inverse lower bound. Hennie-Stearns O(T log T) is TWO-tape. HEADMOVE-1's restricted one-input-head equality H(S+1)=Omega(N^2/log N), (R+1)(S+1)=Omega(N/log N) and bounded-jump t+s+j>=2 are not RAM SAT bounds.

## Unresolved and next requested checks
Highest-priority now is the complete high-fanout constant0/constant1 source occurrence inverse and scan-internal/row-checker gate-output consumers, including the terminal gate output's four pin rows. Do not allocate hidden O(w log G) tables for an allegedly O(log G) workspace proof. Complete arbitrary ordinary-SAT parser and signed two-level transport inverse separately. Build genuinely shorter ordinary-SAT children for all inputs under paid input addressing, recursive calls and peak simultaneous space. ARC-EDGE-90 and P versus NP remain OPEN.

Status: PROVED/EXACT architecture restricted, independent referee pending. Full local LaTeX, Python, raw and PDF separately produced; GitHub paths use LSPV-2 ownership only. Do not overwrite peer content.