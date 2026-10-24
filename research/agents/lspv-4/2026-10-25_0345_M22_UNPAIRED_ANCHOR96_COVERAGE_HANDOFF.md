# LSPV-4 M22-UNPAIRED-ANCHOR96: additive five-role transport handoff
Date: 2026-10-24 UTC / 2026-10-25 03:45 Asia/Seoul. ARC-EDGE-90 OPEN; P versus NP OPEN.

## Exact receiving target and source
Canonical C_M22 means unique, proper three-distinct-variable, clausewise all-positive or all-negative CNFs, exactly two positive and two negative occurrences per active variable. C_star excludes only formulas for which **every** clause has its literalwise sign reversal as an OR-clause. Partial pairs remain permitted. k is original active variable count; m=4k/3; N is full encoding bits. Never transport the TWO-SIGN-SWAP64 mixed-clause SAT mutant into C_star.

Döcker, arXiv:1912.08032v1, Proposition 1/Theorem 1, printed p.7, gives UNSAT U with k=198,m=264 and NP-completeness. Corollary 2 pp.8-9 establishes full pairing implies SAT. Verified source file: research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt, Git blob f9dda41a810ad8e02bd553f2711a26a4050861f9. LSPV-4 separately validated all 264 U clauses are proper and clausewise monotone with 2+/2- per active variable, and none has a complementary partner. Its UNSAT status is imported from Döcker/DOECKER-CORE-CERT61, not freshly enumerated.

## FILLED, exact grammar and reduction
P positive triples: 123,145,246,356. Q negative supports: 124,136,235,456. Let H use positive P and negative P, Y use positive P and negative Q. Both valid C_M22; #SAT(H)=18, #SAT(Y)=20. H fully paired; Y has eight unpaired clauses, witness 111000.

For every valid F in C_M22, output fresh-variable F disjoint-union Y. It lies in C_star whether F is paired or not, preserves the SAT bit, multiplies model count by 20, and has transparent witness projection/extension. No pairing search is required on valid inputs. This is a sharper specialized adapter than a decide-pairing-and-replace-Y rule. General disjoint-product closure is old archive knowledge.

With k active variables and m=4k/3 clauses, in the declared encoding w=ceil(log2(k+1)), N=3w+2+3m(w+1). Anchored k'=k+6,m'=m+8,w'=ceil(log2(k+7)) gives exactly N'-N=3(m+1)(w'-w)+24(w'+1), with w'-w in {0,1}, so N'=N(1+O(1/log k)). Valid-promise virtual output bit access polylog work, O(log N) live writable/index bits. For a **total** many-one reduction, malformed source must be recognized; an explicit deterministic nested-scan validator is O(N^2 polylog N) bit work and O(log N) writable bits. Invalid source maps to the malformed single bit 0. An all-input target solver pair (t,s) transports to C_M22 at best by the proven conservative bound (max{2,t},s) up to o(1), not automatically to FLMV's ordinary-SAT forbidden region. Any explicit child buffer costs Theta(N') writable bits. Ordinary-SAT-to-C_star fine-grained transport remains OPEN.

## New matched opposite-label hostile family
For p>=0 set A_p=H^(p+33) disjoint-union Y (SAT), B_p=U disjoint-union H^p disjoint-union Y (UNSAT). Both lie in C_star with identical k=6p+204,m=8p+272 and the same N. Exact model counts are 20*18^(p+33) and 0. Define D(F)=number of clauses whose sign-reversed clause is absent: D(A_p)=8,D(B_p)=272. The defect densities are 1/(p+34) and 34/(p+34), both tending to zero. A source-aware exact template scan decides this **restricted** family in O(N polylog N) bit work and O(log N) live writable/index bits, charging all source access and selection. Neither nonpairedness nor vanishing density forces hard work on every input.

Finite verified checks include H=18 models, Y=20 models, H disjoint-union Y=360 models, source U grammar and p in {0,1,8,64,512}; matching N respectively 7370,7586,9098,25904,170390. No finite experiment proves the arbitrary-decider statement.

## Rejection ledger and model mismatch
FALSIFIED: every C_star formula has a positive fraction of unpaired clauses. FALSIFIED: full-pair testing is needed for the reduction from valid C_M22. REJECTED AS UNSOUND: a signed exact-(2,2) two-sign-mutant is automatically strict monotone. OPEN: any conversion of these counting/grammar facts into superpolynomial T_finish for every total adaptive exact decider; ARC-EDGE-90 fully charged all-input exponent contraction; original ordinary-SAT FLMV transport.

A single-variable pin typically breaks the 2+/2- grammar. SAT children that leave C_star need a paid adapter, with all headers, witness compatibility, reconstruction, cache/replay and peak live space. The successful fast recognizer is a restricted policy, not all-decider coverage. Track T_A=C_A+T_finish, independent measured R, and primitive bit work, traffic, flips, peak live bits, cumulative bit-time and hardware size separately.

## Role handoffs
Role 5: independently verify the no-pair-test reduction, p-family exact grammar and dense size formula; maintain source distinction from the FLMV all-ordinary-input model.
Roles 1-3: use both A_p and B_p as equal-length grammar-valid hostile controls for any proposed M22-wide residual, rank, defect, endpoint or post-acquisition potential. Verify that recognition does not silently become a free SAT label oracle. Test a genuine interacting target family after this easy island is passed.

## Incremental archive coverage and queue
Repository main tree enumerated at 5,231 paths (not truncated) during this run; this is an **inventory**, not complete manual reading. Original full/section sources checked: root main.tex/main13.tex, AGENTS.md, CODEX.md, pnp-research skill, TASK-002/004, current verified LSPV-1/3/4/5 reports, DOECKER61 original U, TWO-SIGN-SWAP64, earlier balanced/disjoint audit, RT-0012 nonpaired rank guard, arXiv:1912.08032 and FLMV primary PDF. Earlier 3,532-file hash/keyword survey is inherited, not repeated here. Search terms included nonpaired, M22, fully paired components, disjoint satisfiable gadget, paired defect density, 111000 and TWO-SIGN-SWAP64. The finite bounded code-search results are not described as exhaustive. Remaining queue: old Drive LOG/PROVED_EXACT/BOOL/SIL full bodies, more revisions under research/review/manuscripts, and the fine-grained original-SAT-to-M22 reduction.

## Published verified paths
research/agents/lspv-4/2026-10-25_0345_LSPV-4_M22_UNPAIRED_ANCHOR96.tex
research/agents/lspv-4/2026-10-25_0345_M22_UNPAIRED_ANCHOR96_MINI.py
research/agents/lspv-4/2026-10-25_0345_M22_UNPAIRED_ANCHOR96_RAW.json

No automations were created, modified or rescheduled. No messages or emails to third parties.
<!-- END_OF_VERIFIED_HANDOFF::LSPV-4::M22-UNPAIRED-ANCHOR96 -->
