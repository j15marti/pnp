# LSPV-5 to five-role handoff — ORACLE-NO-REPEAT-RANK-REFEREE297

**Timestamp:** 2026-11-02 14:48 America/Los_Angeles  
**Task/status:** exact PNP Independent Proof Red Team identity and enabled
schedule preserved; no task operation performed.  
**P versus NP:** OPEN.

## New exact theorem

For a unique witness, effective independent correct-bit probability \(q\), and
successive product-weighted sampling of assignments without replacement, the
expected witness rank is

\[
 E[R]=1+\sum_{d=1}^n {n\choose d}
 \frac{r^d}{1+r^d},\qquad r=(1-q)/q,
\]

with

\[
 (q^{-n}+1)/2\le E[R]\le q^{-n}.
\]

Therefore no-repeat exclusion improves iid proposals by at most a factor of
two, and every fixed \(q<1\) remains exponential.  Polynomial expected rank
requires \(q=1-O(\log n/n)\) and paid polynomial acquisition of the
witness-correlated advice.

**Classification:** PROVED/EXACT sampling theorem; not a SAT lower bound.

## Interpretation and transfer audit

If a stated \(p\)% means “correct oracle bit with probability \(p\), otherwise
fair random,” then effective accuracy is \(q=(1+p)/2\).  At nine variables,
the exact expected ranks for \(p=66,75,90,95,99\%\) are
\(4.969,3.150,1.563,1.250,1.046\), explaining the strong finite F15 result.
Yet the corresponding million-check crossings are
\(n=75,104,270,546,2757\).

UNSAT has no correct witness bits.  The 12-variable unique-unit SAT control is
solved by source propagation, and its one-clause UNSAT sibling has a one-node
Resolution contradiction.  Hence proposal work is neither \(W_R\) nor an
arbitrary-decider lower bound.  B1, global B2 and B3 remain OPEN.

## Controls

SAT model count one; UNSAT sibling count zero; six malformed DIMACS strings
rejected; 60 exact rate/size rows; ten exact threshold crossings; independent
no-import verifier passed 269 assertion groups.

## Next action

Replace fixed-percentage offline advice with a source-computable predictor and
test whether it can guarantee \(1-q(n)=O(\log n/n)\) on all SAT inputs while
also producing sound UNSAT certificates, with acquisition and all-phase space
charged.  No such controller is known.

## Artifacts

* report:
  \`research/main/2026-11-02_1448_MAIN_ORACLE-NO-REPEAT-RANK-REFEREE297.md\`
* producer/verifier:
  \`experiments/arc/lspv5_297/oracle_no_repeat_rank_referee297.py\`,
  \`experiments/arc/lspv5_297/verify_oracle_no_repeat_rank_referee297.py\`
* raw/verification:
  \`results/raw/arc/2026-11-02_1448_LSPV5_ORACLE_NO_REPEAT_RANK_REFEREE297_raw.json\`,
  \`results/raw/arc/2026-11-02_1448_LSPV5_ORACLE_NO_REPEAT_RANK_REFEREE297_verify.json\`

