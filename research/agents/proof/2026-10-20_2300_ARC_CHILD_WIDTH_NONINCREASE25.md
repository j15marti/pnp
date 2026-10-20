# ARC-CHILD-WIDTH-NONINCREASE25 (2026-10-20 23:00 Asia/Seoul)
Status: PROVED/EXACT lemma for the stated child builder (pure construction, no hardness); COMPUTATIONAL audit; P versus NP remains OPEN.

## Target (from FINITE-DEPTH-WIDTH-MARGIN24, :24 role test)
Is width(child) <= width(parent) for the pinned child of ARC-INTERFACE-PROJECTION8? If yes, the finite-depth margin lemma applies to the peer contractor on the scoped class.

## Lemma
Builder: pin every variable of S_{j-1} u S_j; drop satisfied clauses, delete falsified literals; pad each clause of size 3-k (k=1,2) with k fresh aux variables (all 2^k sign patterns) opened immediately before and closed immediately after that clause; re-scope each surviving variable to its first..last surviving occurrence; renumber. If a clause becomes empty, answer UNSAT directly (or emit the fixed 8-clause UNSAT formula, width 3 <= w because any proper clause needs w>=3).
Claim: max live width of the child <= max live width of the parent block (incl. incoming live set).
Proof: child lifetimes of surviving variables are sub-intervals of parent lifetimes. At any moment, unpinned live <= w - (pinned live). At a padded clause with k removed literals, those k variables are pinned and live in the parent at that clause (a clause's variables are open), so child live <= (w-k)+k = w. Elsewhere child live <= w. QED.
Consequence: the +O(1) worry in MARGIN24's "Adversarial challenge" is removed for this builder; width persists (does not grow), so the sharp margin w <= (1/20 - eps) 2^-r log2 N is the right sufficient condition at depth r. The persistent-frontier counterexample (MARGIN24) shows it cannot be weakened. Unchanged OPEN: all-input normalizer into the class (FLMV barrier in ARC-PROJECTION8), encoded child length N^{1/2+o(1)} on recursion, charging of live ancestors.

## Audit
experiments/review/2026-10-20_arc_child_width_audit25.py (seeded, 0.13 s, one stage): 63 streams (60 random width 3-5, 3 cyclic persistent), exact join checked against brute-force SAT, two recursion levels, 4,920 child records, 4,983 checks, max(child width - parent block width)=0, zero failures. Finite evidence only; the proof is the lemma above.

## Literature note
No new search this run (hourly budget); relied on peers' verified FLMV (JACM 2005, Thm 3.1, Cor 5.8) citations. Not re-verified here.

## Classification
Transfer from circuit/VLSI "locality of live wires" intuition: structural analogy only. Corpus check limited to newest MAIN (FINITE-DEPTH-WIDTH-MARGIN24), ARC-INTERFACE-PROJECTION8 status/code, and recent commit log; root main.tex untouched (no ownership markers; it carries peer edits). Next: instrument child encoded length per level, then attack the all-input normalizer.
% END_OF_VERIFIED_REPORT::ARC-CHILD-WIDTH-NONINCREASE25
