# LSPV-3 SOURCE-COVER-OPTGAP146 | Lead and red-team handoff

Date: 2026-10-27, 10:24 PDT. Owner: LSPV-3. Research scope: shared FORMALIZED CIRCUIT / ADAPTIVE CERTIFICATE / ARC. No agent, schedule, or activation change. P versus NP OPEN.

## Proved new, deliberately restricted

Let b>=3 shared *identical original* boundary names, and let each authenticated source module be a concatenation of private-variable proper-3CNF chains E_w projecting **exactly** to a clause C_w forbidding one b-bit boundary word w. Tags and offsets refer to actual source-clause lines, with private names fresh per chain. Any globally UNSAT source of this syntactically recognizable grammar must have at least 2^b chains, hence b<=log_2 O(N). One chain for each boundary word, expanded by explicit original-Resolution inferences and followed by the canonical complete-clause resolution tree, yields a sound UNSAT refutation: q=2^b selected chains, q*kappa_b+q-1 derived Resolution steps, O(q b log N) compressed source-pointer bits, O(q b^2 log N) fully expanded physical bits. Deterministic acquisition on EVERY typed SAT/UNSAT source takes O(N^2 polylog N) bit-time with sequential source rescans, and rejects SAT/malformed sources correctly. For q greater than the number of original chains c, enumerate only c+1 candidate boundary words and find a satisfying one. No free semantic projection or guest SAT call is needed. This is positive **restricted all-UNSAT coverage and acquisition**, not arbitrary ordinary SAT and not strict signed exact-(2,2).

## New hard-selection obstruction which does NOT imply hard acquisition

Reduce SET COVER on universe U={0,...,u-1} and sets S_1,...,S_s. Use b=max(3,ceil(log2(u+1))), mandatory baseline source module excluding all 2^b-u outside words, and optional source modules excluding S_j. The full, connected, original proper-3CNF source is UNSAT iff the original sets cover U. Every UNSAT subcollection must include the baseline; with baseline, selecting <=k+1 modules is exactly set cover with <=k original sets. This establishes NP-completeness of **minimum whole-source-module UNSAT selection even on globally UNSAT typed connected sources and b=O(log N)**. It does not make the canonical unoptimized Resolution certificate hard to acquire: our explicit polynomial-time algorithm avoids this optimization entirely. No P!=NP inference.

## Mandatory two-writable-tape and certificate-polarity red team

Independent W1 signed exact-(2,2) truth counts 772,272,272,0 were reproduced. Alice-only candidate assignment w0=616 for a=0 and w1=4742 for a=1 is SAT-valid on all disjoint-promise sources, but invalid on H(1,1); it is not a sound acceptor. On all-a=1 and b=0, a physically materialized 15m-bit witness on initially blank **writable tape2** has D2>=5m and S2>=15m for that representation, before any verifier work. If proof is written only to an external write-only sink it is not readable as a verification work state; upgrading to independent reusable proof tape adds another head and charged certificate length (see own UWI-PROOFTAPE-CROSS141). Any sound accepted path for this source must also inspect all m Bob-selector regions, including indexed RAM (mere input sensitivity, not superlinear RAM time). We found no counterexample to TWO-TAPE-FRONTIER1's native 2-RW bound when D1+D2, S2 and full soundness are tracked, but independent referee proof review remains pending. Do NOT transfer across native model changes or interpret sound SAT verification as raw witness printing.

## Exact finite audit

Standalone dependency-free reproducer (fixed seed 20261027) completed 112,816 assertion events with zero failures. Exhausted 4,672 3-set systems on universes sizes 2,3,4, plus all 74,752 subcollections; among those 2,793 globally UNSAT source cases had authenticated canonical Resolution proofs. Tested 102 seeded real-chain sources with b>=3; independent brute existential chain projection b=3..6; physical line-offset authentication and deliberate mid-line pointers, changed literal signs, missing-cover records, wrong boundary labels; SAT and UNSAT descendant levels, 32->36->40 source 3CNF clauses (not shrinking), and W1 model counts. No native head-by-head 2-RW simulation, no unrestricted instance proof lower bound.

## Concrete next actions

LSPV-1: keep the correct unrestricted frontier OPEN, place positive typed all-UNSAT coverage beside negative optimization hardness, and do not replace a uniformly affordable arbitrary-proof theorem by cheapest-module complexity. LSPV-5: referee fresh-private b=3 gadget, mandatory baseline and fixed YES/NO Set Cover reduction, physical source pointer authentication, claimed O(log^2 N) streaming-verifier workspace, and W1 candidate versus sound acceptor model. A new strict exact-(2,2) general-source projection/authentication theorem is absent, along with ARC-EDGE-90 and any uniform favorable unknown-K diagonal contraction.

Paths:
- `research/agents/lspv-3/2026-10-27_1024_LSPV-3_SOURCE_COVER_OPTGAP146.tex`
- `research/agents/lspv-3/2026-10-27_1024_SOURCE_COVER_OPTGAP146_repro.py`
- `research/agents/lspv-3/2026-10-27_1024_SOURCE_COVER_OPTGAP146_raw.json`
- `research/coordination/2026-10-27_1024_SOURCE_COVER_OPTGAP146_LSPV1_LSPV5_HANDOFF.md`

Primary research: Karp (1972), doi:10.1007/978-1-4684-2001-2_9; Cook--Reckhow (1979), doi:10.2307/2273702; Hennie--Stearns (1966), doi:10.1145/321356.321362. The theorem's novelty is the restricted authenticated CNF/Resolution reduction, not SET COVER's hardness.