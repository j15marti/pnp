# LSPV-4 bottom-up SAT construction handoff 349

November 2, 2026, America/Los_Angeles. User requested experimenting with building SAT from the ground up. Additive to the 12:04 worst-case minimum derivation handoff. No task changes. P versus NP OPEN.

## Exact fixed-system results

Keep R_mix341 unchanged. For ordinary binary non-tautological DAG resolution R_res, free source clauses and unit derived-node weights, let C be indispensable in UNSAT F and z be fresh. Replacing C by C OR z and C OR NOT z produces F' with **W_res(F')=W_res(F)+1**. The upper bound reverses the split. The lower bound restricts any refutation to z=0 and removes at least one necessary z-pivot inference. Minimal UNSAT is preserved. No optimizer is charged to the ideal minimum.

Repeated fresh splitting from the empty-clause singleton gives exact **W_res=W_mix341=m-1**, by reversal plus the source-explicit binary-ancestry lower bound. This is linear, not a superpolynomial lower bound.

## Exhaustive finite experiment

All minimally UNSAT sets of nonempty, non-tautological clauses drawn from three named variables, with unused variables allowed: **869 labelled formulas, 43 signed-variable symmetry classes**. Empty-clause singleton has cost zero and is excluded. Python and no-import JavaScript independently enumerate the corpus and redo exact available-clause-set BFS for shortest DAG resolution. All mixed optima equal m-1, since AND3 can conjoin the entire three-variable source in m-1 binary steps.

Exactly eight labelled formulas, one symmetry class, have resolution excess one. Representative:

    (-b OR -c), (-a OR b), (a OR c),
    (-a OR -b OR c), (a OR b OR -c).

Its successive clause prefixes have 8,6,4,2,1,0 models. Exact W_res=5 and W_mix341=4. A four-resolution proof would have to use each of five sources once in a tree, but its complementary-unit subproofs each require at least three leaves. A five-resolution proof exists.

After s fresh splits of this seed: n=3+s, m=5+s, W_res=5+s, W_mix341=4+s. The construction preserves excess rather than amplifying it. Existing-variable splitting need not add one; adding any source-variable unit to the seed reduces resolution minimum from five to three.

## Independently rerun evidence

JavaScript referee: **25,594 assertions**, all 869 sources and 43 symmetry classes, 114 proof DAGs, 4,420 source-deletion SAT cases, 9,924 sign-flip SAT cases, 8,192 split-identity assignment checks over 95 SAT and 161 UNSAT two-variable formulas, eight malformed binary encodings and five corrupt proofs rejected. Independent four-variable BFS certifies first fresh split minimum six. Odd/even K4 models: zero/eight. Full data and both implementations are in the user-facing reproducibility archive.

## Next target and scope

Search a finite nonaffine minimally UNSAT seed using more than three variables with a proved mixed-system minimum strictly above m-1, then seek a growth operation amplifying that excess under EVERY permitted rule. Failure to find a short proof in a bounded search is not a lower bound. A construction history supplies only an upper bound without an independent lower argument. B3 and superpolynomial worst-case mixed cost remain open. Encoded size, proof bits, validation work and all-phase space remain distinct; source materialization is not square-root-space implementation.

## Readback-verified public artifacts

- Report: ../agents/lspv-4/2026-11-02_2055_LSPV-4_BOTTOM_UP_SPLIT_VS_OVERLAP349_PUBLIC.tex
- Standalone census/minimum reproducer: ../../experiments/arc/lspv4_349_bottom_up_compact.py
- Summary: ../../results/raw/arc/2026-11-02_2055_LSPV4_BOTTOM_UP_SPLIT_VS_OVERLAP349_summary.json

Root main.tex returned empty text with a nonempty blob SHA, so no root overwrite was attempted. No full root reconciliation is claimed. No research originality claim: minimal-unsatisfiability splitting, DP lifting and exact resolution optimization have established literature.
