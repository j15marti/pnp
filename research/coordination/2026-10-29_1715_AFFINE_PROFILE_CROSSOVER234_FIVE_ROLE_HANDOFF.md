# LSPV-2 ADDITIVE FIVE-ROLE HANDOFF: AFFINE-PROFILE-CROSSOVER234

Date: 2026-10-29 17:15 America/Los_Angeles. Priority: exact time-space frontiers, both P=NP and P!=NP universes. No task, schedule, or role changes.

## Verified mathematical restricted result

Build k independent XOR3 four-clause proper strict signed exact-(2,2) parity blocks, left-associatively joining by the previously validated pointwise CONNECTOR231. Add either the fixed 15-variable SAT anchor G or the fixed 15-variable exhaustively UNSAT anchor W1. For each k>=1 the two connected root formulas have n=33k+15, m=44k+20, identical unsigned clause scopes, and only two different literal signs. They retain exact two positive/two negative occurrences per variable. The fully generated SAT witness is checked on every clause. The UNSAT label follows from the original 2^15 W1 enumeration and the connector pointwise conjunction identity. A tree decomposition of width <=35 is constructed and mechanically checked.

Let Y be the 3k original parity-block variables. The SAT root's existential projection is exactly k independent 3-bit even-parity equations, with aggregate GF(2) rank/codimension e=k and 2^(2k) feasible boundary assignments. The UNSAT root projects to empty. All this is an explicitly authenticated grammar; no arbitrary-source discovery claim is made.

## Exact physical crossover, NOT a SAT decision lower bound

For w=ceil(log2(3k+1)) and h=ceil(log2(5k+2)), the exact physically encoded lengths in the fully specified formats are D=2w+2^(3k) bits (dense relation), A=2w+k(3w+1) bits (affine row list), and B=2w+5k(w+2h) bits (ordered ROBDD). The SAT-side ROBDD has exactly 5k nonterminal nodes in grouped variable order. At k=1: (D,B,A)=(12,44,11); k=2: (70,116,26); k=3: (520,218,47). Thus the first dense-vs-BDD size crossing occurs exactly at k=3 and remains so for k>=3. At k=12: D=68,719,476,748, B=1,092, A=240 bits. This crossing concerns a representation choice, NOT measured true SAT time-space or a mandatory artifact for a decision-only algorithm.

For the specified global boundary b=3k and one syntactic private module containing the 30k+15 non-Y variables, there are exactly 39k+20 private-only clauses. Its minimum private clause-hitting number satisfies ceil((39k+20)/4)<=q<=30k+15. An exact-integer MILP solver returned q=11k+5 for k=1..9, with zero reported gap and independently checked primal sets; NO independent lower-bound integer certificates were produced, so the all-k formula is OPEN rather than proved. Distinguish full boundary and semantic rank from syntactic clause-incidence rank.

## Computational scope

Ten sizes k=1,2,3,4,5,6,7,8,9,12 passed all signed quotas, connectivity, unsigned-scope equality, SAT-model replay, affine-rank calculation and tree-decomposition certification. Independently repeated the CONNECTOR231 32,768-source-assignments and 16 gate-case exhaustive test. ROBDD matched all boundary truth-table assignments for k<=4. Three adversarially renamed/reordered SAT roots retained full witnesses, but the intentionally strict canonical recognizer returned UNKNOWN, an explicit coverage limit.

Same-run Python `tracemalloc` benchmarks include full formula generation, clause and incidence validation, canonical SAT+UNSAT template recognition, method selection and output. Generic DPLL was tested on SAT k=1,2 and UNSAT k=1; do not claim full DPLL coverage for larger UNSAT cases. Peak traced Python heap is not native TM space, and measured finite crossings are implementation-specific. Full data are in `_raw.json`; source in `_repro.py`, dependency `connector231.py`, exact source report `.tex`, figure `.png` and compiled report `.pdf`.

## Source/provenance and conflicts

Prior exact AND connector: LSPV-2 CONNECTED-AND-CONNECTOR231 source `research/agents/lspv-2/2026-10-29_1322_LSPV-2_CONNECTED_AND_CONNECTOR231_repro.py`. Prior zero-rank static family: PAIRED-REALIZABLE-FRONTIER233. Prior LSPV-5 AFFINE-MESSAGE-RANK-REFEREE205 already warns that rowwise and aggregate rank differ. Source checks: j15marti/pnp AGENTS.md blob `19656af10260`, CODEX.md `754999f50de9`, `.codex/skills/pnp-research/SKILL.md` `b8df83a7b0b1`, ARC227 `fc4a02dc004e363e28dc78ebc3b969e2c27ad1f7`; `cuddorg/cudd/cudd/cuddBddAbs.c` `62170e3b29aa77e4eaab07d7fb20e20c6063a5a7`, `arminbiere/cadical/src/elim.cpp` `c401152c7a733803d0b407d98e8a295ab44f7e99`, `tulip-control/dd/dd/autoref.py` `4281be2c32f8df507fee49cada3de1e5ad8b5242`. Primary Arvind-Guruswami IPEC 2021 Theorems 2,17,19 were inspected including PDF screenshots; fixed affine codimension is known tractable for 2CNF, logarithmic e is not guaranteed P, and W[1]-hardness is conditional against FPT assumptions. No automatic transfer to general strict22.

Root main.tex was retrieved with 2,690 lines and all owner markers, but then a fresh read returned a 15,446-character truncated file (blob SHA `8ba2d1c620bb1d4f040cc09cdac0401db36aca00`) without an LSPV-2 ownership region. **Do not edit that truncated file.** LSPV-5 should restore verified root before any region-specific reconciliation. Standalone source and this handoff are authoritative only after verified GitHub fresh readback; otherwise distinguish Library-only/PENDING.

## Role-specific next lemma

LSPV-1: find the exact additional premise, if any, by which aggregate affine rank translates to unavoidable post-input-acquisition decision cost, without requiring complete profile emission.

LSPV-2: construct a source-independent, charged recognizer for compact affine or bijunctive messages under variable permutations, or formally falsify a concrete recognizer; separately derive a proof-quality formula for the exact private syntactic hitting number q(k), instead of treating the nine HiGHS optima as proof.

LSPV-3: audit source authentication, failed strategies and the cost of discovering the hidden parity grammar, especially under arbitrary renamings and signing changes.

LSPV-4: audit same-run TM/two-tape/RAM/UTM resource conversion; distinguish polynomial decision work, exponentially long dense profile output, and streamed enumeration with small workspace.

LSPV-5: independently referee the 16-case connector table, 5k BDD node count/bit layout, MILP evidence and restore/reconcile the live root.

**Status: PROVED/EXACT, RESTRICTED** for the connected rank-k twin construction and first BDD-vs-dense *encoded-size* crossover, peer review pending. **COMPUTATIONAL** for finite controls and q values. **OPEN** for uniform arbitrary-source recognition, universal time-space lower bounds, P=NP and P!=NP.