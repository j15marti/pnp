# Living log: worst-case derivation complexity programme (W_R)

Target quantity: W_R(N) = max over UNSAT F (|F|<=N) of min over derivations pi of F |-_R bottom of cost_R(pi).
Weakest bridge sought: SAT in P  =>  W_R(N) <= poly(N).
**Status: P versus NP remains OPEN. Nothing below is a proof of a lower bound or of the bridge.**
Append-only; newest entry at the bottom. Entries cite `research/worst-case-derivation/reports/`.

## 2026-11-07 CLAUDE WCD-0001 (first entry; no earlier W_R log existed in the corpus)
Corpus check: no prior "multisign DAG hypergraph" W_R log found; related retired item "free semantic SAT answers" and the LSPV UWI/ARC spine exist. Nothing in them contradicts the entry.
Result (PROVED/EXACT, elementary; see report, which corrects item 1 below: a fixed-R lower bound needs the bridge B_R to reach P != NP): the free-strategy trilemma.
 1. R poly-time-checkable with cost >= size (Cook-Reckhow): W_R superpoly => NP != coNP => P != NP. Bridge unnecessary, target at least as hard as NP vs coNP (Frege/EF size lower bounds, open).
 2. R with unverified/semantic steps and per-instance minimisation: W_R = O(N) (answer "UNSAT" is sound on the UNSAT instance F). Collapses; same as the retired free-semantic-answer route.
 3. Soundness required uniformly over all inputs: then min over derivations = a fixed-program runtime; W_R lower bound = SAT time lower bound (the ARC/FLMV spine, OPEN).
Consequence: "free choice of the best sequence" adds no strength beyond nondeterminism; any genuine progress target is (1) or (3). Also: the bridge B_R is vacuously true if P != NP, so B_R is only informative when P = NP, i.e. it asks R to be p-bounded then.
Literature (2026-11 search): no superpolynomial Frege/EF lower bound; Alekseev (Theory of Computing 22(4), 2026) exponential bound for a PC-with-roots system simulating Res-Lin (not Frege); Filmus-Pitassi-Santhanam depth reduction; Pich-Santhanam conditional EF/circuit links; Mertz-Pitassi-Wei automatizability under ETH. Classification: all ANALOGY/CANDIDATE, none a transfer theorem.
Next: (a) formalise the multisign hypergraph inference system as a CR system and test lower bounds against known Res/PC/Res(parity) families; (b) check whether any bounded-depth reduction (Filmus-Pitassi-Santhanam) applies to a DAG-hypergraph measure.
