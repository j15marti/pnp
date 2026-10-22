# COVER-SPLIT-RANK76

Timestamp: 2026-10-22 24:48 KST (hourly scheduled check)

**Global status: P versus NP OPEN; P versus RP OPEN.**

## Check summary
Repository accessible. Newest verified work: MINIMAL-CORE-SOURCE-COVERAGE75 (23:48) and the Grok 4.7 review of 00:16 KST. No new PRs/commits after `ca49b07b`. No load-bearing arrow closed. Open item chosen from the 75 ledger (":24 ARC/FLMV: attempt one non-subset derived constraint"): test **independently compressed halves** of the source.

## Corpus reviewed
`AGENTS.md`, root `main.tex`, MAIN 74 and 75, Grok review 2026-10-23 00:16, existing disjointness references (DISJPOWER40, BLOCKCONTRACT1, VIEWSEP1). Duplication audit: set-disjointness appears earlier in the corpus in other settings; its use as a barrier to *split-source digests of the Firewall74/75 cover family* is not stated in MAIN 70-75. No contradiction found with 74/75.

## Setup
Family `F_k` of 75 (blocks `C_a`, `a in U={0,1}^k`, `m=2^k`), but now an arbitrary source is a list of blocks, duplicates allowed. Split the block list between two parties (or two halves of a stream) with forbidden-value sets `T_A, T_B subseteq U`. Then `F` is UNSAT iff `T_A ∪ T_B = U`, i.e. iff the complements are disjoint.

## Lemma 76A (KNOWN THEOREM transfer, exact in the split model)
The cover matrix `M[A,B]=[A∪B=U]` is the set-disjointness matrix with columns complemented. It has full real rank `2^m` (audited for `m<=8`; general: DISJ matrix is a Kronecker power of `[[1,1],[1,0]]`, nonsingular). Hence deterministic communication is `m` bits and the fooling set `{(A,U\A)}` has size `2^m`; randomized communication is `Omega(m)` (Kalyanasundaram-Schnitger, Razborov).

## Consequence (RESTRICTED, ESTABLISHED in model)
Any child/digest scheme in which the two halves are compressed independently to `s(N)` bits and then combined (including one-pass streaming with memory `s`, and every "merge of two short children" hereditary rule) needs `s >= m = N/Theta(log N)` to decide the label exactly, with randomization too. This extends Firewall74 (pure block *conjunction* grouping) to **arbitrary** independent compression of halves, and complements 73 (detached interface queries). Fixed-power children `N^beta`, `beta<1`, are impossible in this model.

## Scope firewall
- No lower bound against arbitrary algorithms: a single machine that sees both halves jointly may recognize the cover by source inspection (poly time for this family).
- Halves must be treated adversarially (arbitrary duplicates/order); a canonical sorted cover escapes, and that escape must be charged to source acquisition.
- Natural-proofs/relativization/algebrization: not engaged; this is a communication statement about a restricted model.
- ARC remains: a derived constraint must depend jointly on both halves *before* compression, so its construction must charge a cross-half pass.

## Finite audit
`experiments/review/2026-10-22_cover_split_rank76_audit.py`: full rank mod 1000003 (implies over Q) for `m=1..8`, fooling-set property verified; 0 failures; runtime 0.12 s, no chunking needed. Raw: `results/review/2026-10-22_2448_COVER_SPLIT_RANK76.json`. Finite check only; the lemma is the cited theorem.

## Ledger deltas
- ARC/FLMV: independent half-compression and streaming digests **RETIRED generically** (ESTABLISHED restricted). Highest-value target unchanged: exact, all-input, hereditary, source-aware derived constraint of length `N^beta`, fully charged.
- SAT->MKTP and P vs RP: unchanged, OPEN.

Root `main.tex`, ownership regions and automations were not modified.
