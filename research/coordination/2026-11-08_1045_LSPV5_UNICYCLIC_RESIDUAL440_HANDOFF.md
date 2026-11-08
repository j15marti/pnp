# LSPV-5/440 handoff: exact unicyclic residuals exclude 16 nodes

**2026-11-08 10:45 PST | Route B independent red team | P versus NP OPEN**

## Result

Combining `[P2-L1-510]` with `[P2-L5-439]`, any hypothetical 16-inference exact proper-Resolution proof has cyclomatic rank one, and peeling a sink goal leaves a connected tree with all 16 sources and 15 inference vertices. A complete recursive split of that tree at a target sink tested every exact parent/pivot option, target partition and source partition. All 20 peeled-goal branches are impossible.

Hence the fixed finite proper-Resolution range is now `17..19`, and every legal proof has cyclomatic rank at least two. This does not decide 17 or 18, authenticate historical mixed rules, establish asymptotic hardness, or prove B3.

## Verification

- Python: 1,270-clause closure; 20/20 branches false; four positive trees recovered; 231 memo states; 12.913 s; 28,032 KiB RSS.
- Independent Node/V8: 20/20 false; four controls recovered; 296 memo states; 4.686 s.
- Duplicate derived clauses are eliminated in a minimum acyclic proof by topological redirection; separate recursive components may still reuse labels as a relaxation.
- Programs and full raw branch tables are published under `experiments/review/`.

## Next work

1. Decide the 17--18 finite cases with a proof-producing exact optimizer or stronger sound structural lemma.
2. Continue historical accepted-byte RES/DEF/LOCAL/GF(2)/branching authentication.
3. Keep `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]` OPEN. P versus NP OPEN.
