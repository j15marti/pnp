# Worst-case minimum-derivation living log

Status: P versus NP OPEN. Entries are research notes, not proofs. Directive: 2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md

## 2026-11-09 scheduled run (routine, single agent)
Status: NO NEW THEOREM. Repository survey + literature check only.

**Bridge bookkeeping (KNOWN/duplicate, not new).** If a superpolynomial lower bound on Wbar_R is proved unconditionally (e.g. Resolution via Haken), then B3_R is equivalent to "SAT not in P", so it cannot be a weaker, independent bridge. Already recorded at research/agents/lspv-1/2026-11-04_1300_LSPV-1_B3_RESOLUTION_BACKTRANSLATION_FIREWALL398.tex. B3 is only non-circular for an R where polynomial simulation of every poly-time SAT decider (reflection/soundness of A, provable in R) is argued independently of the separation. That is still unproved for R_mix341.

**Literature check (queries and findings).**
- Pich-Santhanam, arXiv:2312.08163: EF lower bounds conditionally imply P != NP-type consequences; relevant to which R can carry B3. Not verified in detail this run.
- arXiv:2506.16956 (rev. May 2026): automatability of EF-type systems under P = NP. Not read in detail; check whether its simulation hypotheses help B3.
- de Rezende et al., arXiv:2604.28172 / ECCC TR26-078: superpolynomial lower bounds for tree-like semantic proof systems with bounded line size. Tree-like, so it does not touch shared-DAG R_mix341; control only.
- Theory of Computing v22a004 (2026): exponential lower bound for polynomial calculus with extension on the binary value principle; p-simulates Res-Lin. Candidate comparison for algebraic shortcuts.
- No 2026 Frege/Res(lin) general breakthrough found. AC0[p]-Frege lower bounds remain open.
- Search snippets only; no primary source was fully read, so none is cited as a theorem here.

**Next missing implication (unchanged).** (i) a growing superlinear W_R family in the same fixed combined calculus; (ii) a noncircular B3 for that same R.
