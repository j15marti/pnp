% CLAUDE REPORT::WCD-0001::2026-11-07
# WCD-0001: free-strategy trilemma for W_R

Status: elementary PROVED/EXACT statements plus KNOWN THEOREM citations. P vs NP OPEN.

**Setup.** A derivation system R: derivations pi are finite DAGs of steps; cost_R(pi) a measure; W_R as in LOG.md. Minimisation over pi is free (not charged).

**Prop 1 (Cook-Reckhow case).** If the map (F,pi) -> accept is poly-time and cost_R(pi) >= |pi|^{Omega(1)}, then W_R superpoly implies R is not p-bounded for UNSAT. R is a Cook-Reckhow system when also complete and sound; p-bounded R exists iff NP = coNP (Cook-Reckhow 1979). So a superpoly W_R lower bound for a *fixed* such R gives only "R not p-bounded", which does not alone give NP != coNP (another system could be p-bounded). Correction of the log summary: lower bounds for a fixed R yield P != NP only through a bridge B_R (SAT in P => R p-bounded). So the bridge is needed, and it is exactly a simulation statement "P = NP => R p-bounded".
**Prop 2 (bridge status).** B_R holds vacuously if P != NP. If P = NP, B_R says R is p-bounded; since P = NP gives NP = coNP, some Cook-Reckhow system is p-bounded, but KNOWN: no result gives it for Frege/EF (Krajicek-Pudlak: optimal proof system equivalent to fast consistency provers; open). Extended Frege + soundness axioms of any P simulates P, so B_EF is equivalent to a provability statement: EF proves the correctness of the (unknown) poly algorithm. Thus B_R for natural R is itself a strong open statement (not weaker than needed in any known way).
**Prop 3 (semantic collapse).** If a step "assert bottom" is allowed whenever F is semantically unsatisfiable (no poly check), then for every UNSAT F, min_pi cost = O(1) or O(|F|); W_R = O(N). Proof: pi = single step. Retired route, consistent with repo ("free semantic SAT answers").
**Prop 4 (uniform soundness).** Charging steps by time and requiring one fixed program D, sound on all inputs, makes min over D = decision time of SAT; W_R lower bound is a SAT time lower bound. This is the ARC/FLMV spine; OPEN, with Buss-Williams barrier for alternation trading (ledger L13).

**Consequence for the allocation.** The "weakest bridge" B_R is not weak for any known strong R; the viable targets are (a) unconditional size lower bounds for stronger R than known (Frege depth/size, Res(parity), PC-with-roots per Alekseev 2026), which attack NP vs coNP for p-bounded-ness of R only; (b) the uniform time-space route. Hostile test list for the other four roles: any proposed hard family must be checked against Res, PC, CP, Res(parity) simulations; any proposed multisign-hypergraph measure must be shown not to be bounded by a known poly simulation.

Sources: Cook-Reckhow 1979; Krajicek-Pudlak 1989; Alekseev, Theory of Computing 22 (2026) v022a004; Filmus-Pitassi-Santhanam; Pich-Santhanam ECCC TR23-199; Mertz-Pitassi-Wei ICALP 2019.
% END_OF_VERIFIED_REPORT::CLAUDE::WCD-0001
