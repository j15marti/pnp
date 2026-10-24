# PROOF-SUPPORT73: source-supported no-goods and prime-interface negative control

Role 2, 2026-10-24 13:12 Asia/Seoul. **P versus NP OPEN.** No arbitrary-algorithm lower bound, all-input polynomial SAT decider, or proof of P=NP/P!=NP.

Verified source: [LaTeX report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-10-24_1312_LSPV-2_PROOF_SUPPORT73.tex), [standalone executable](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-10-24_1312_PROOF_SUPPORT73_minirepro.py), [raw-data summary](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-10-24_1312_PROOF_SUPPORT73_raw_summary.json). Full independently runnable modules/source/checker, per-mode full JSON and SHA256 manifest are in the current conversation archive; do NOT assume another run can read local paths.

## Main exact result

A named-source DPLL tree refuting a local block under boundary assumptions alpha may be annotated with dependency tokens for original assumptions and decisions. Unit reasons and conflicts combine supports; when both children of a split refute, discharge the corresponding split token. The remaining original assumptions beta are sufficient to refute the block; independently replay the SAME tree against the actual signed source clauses under beta. Hence the local learned clause D_beta is a valid source entailment. One source-analysis pass + one checker replaces k repeated checker replays, polynomial in explicit proof length. This is established proof-provenance technology, a new charged integration/test, not a new complexity-theory theorem.

## Key controls

Connected proper 3CNF guarded-XOR SAT/UNSAT family (NOT strict signed exact-(2,2)): rank r=6, k irrelevant boundary sources, formula n=61+2k variables and m=88+2k ternaries. The named DPLL local UNSAT refutation has 127 nodes. On k=4/16/32/64 the greedy repeated checker uses 75,860/385,772/995,212/2,886,860 clause reads; one dependency pass + independent checker uses 37,608/48,120/62,136/90,168, including the correctly retained x assumption. Common local solver, parsing and cache charges are separate. A direct affine recognizer could bypass the XOR refutation; no mandatory cost follows.

Strict source U (198/264, compact SHA256 4ed9031a7a1b1fa9fcb752f9feece1ea7201df6b610059b90793517ecd874001) and two-sign SAT neighbor V: 128-node label-blind direct probe returns SAT witness on V at 104, UNKNOWN on U at 128. The six local projection clauses of U are prime over their own source interface: all 15 single-assumption deletions have checked SAT local witness; extraction retains every assumption. The adaptive policy therefore skips large proofs with support <=3. On U it uses 18 local calls/725 nodes, WORSE than LAZY-BOUNDARY71 16/688. No universal improvement.

Three finite modes ran separately: synthetic 65, random 1306, strict 61 assertion-accounted checks, total 1432, zero failures. Random included 640 local restrictions (202 SAT/438 UNSAT), 12 source-renaming and polarity-complementation controls, and malformed-certificate rejection. All original-source reconstruction and UNSAT root refutations were checked. Only restricted mathematical conclusions are PROVED/EXACT; performance is COMPUTATIONAL.

## Peer-specific next steps

Role 1: Test whether a proposed universal progress potential survives cheap proof provenance and the alternative affine recognizer. Neither proof length nor boundary assignment count is mandatory.

Role 3: Check exact source/encoding/space accounting, test proof certificate transformation under re-encoding, and reject a transfer of an explicit-proof polynomial bound to a polynomial input-time bound.

Role 4: Build a connected strict signed exact-(2,2) opposite-label pair without a fixed UNSAT subcore or supplied small separator. Independently falsify false minimality and any all-decider claim.

Role 5: Preserve the three OPEN arrows: universal policy coverage, independently growing parameter, and necessary charged inequality. Both possible complexity outcomes remain open.

Repository governance: The standalone report, minirepro and raw summary were fetched back. Root main.tex LSPV-2-owned region was reconciled with fresh SHA, only the authorized region changed, five ownership markers remain balanced; verified root blob `f9b42b5038d1b953c52bdc8e08ec410eda47e148`. No schedule/task was created, resumed or changed.