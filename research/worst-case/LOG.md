# Living log: worst-case derivation cost W_R(N)

## Entry 1 — 2026-11-10 (CLAUDE, WORSTCASE-0001)
Status of everything below: PROVED/EXACT unless labelled; P vs NP OPEN.

### Facts (all short, standard-technique proofs)
- F1 (Cook–Reckhow, KNOWN). R poly-time verifiable. W_R poly <=> R is p-bounded; some R is p-bounded <=> NP = coNP. Free search of the optimal sequence makes W_R exactly proof length, so the "free search" convention loses nothing and adds nothing.
- F2 (PROVED). B(R) and W_R superpolynomial together imply SAT not in P. (contrapositive of B.)
- F3 (PROVED, circularity). If W_R is superpolynomial is already known (e.g. Resolution, Haken; bounded-depth Frege), then B(R) is logically equivalent to SAT not in P. So the bridge cannot be proved separately for any system with an unconditional lower bound without proving P != NP. The bridge is only informative for strong R (EF, Frege) whose lower bounds are open.
- F4 (PROVED). If R is p-optimal (p-simulates every proof system) then B(R) holds: SAT in P => NP = coNP => a p-bounded Q exists => R p-bounded. Existence of a p-optimal system is OPEN (Krajíček–Pudlák), so this does not discharge B for a concrete R.
- F5 (KNOWN, Cook 1975 / Krajíček–Pudlák; to be re-verified at source). If SAT is decided by a poly-time M whose correctness is provable in PV (equivalently, the propositional translations of that correctness statement have poly-size EF proofs), then EF has poly-size refutations, so B holds on that branch for EF. Gap: correctness of M need not be provable.
- F6 (PROVED, consequence). A "weakest sufficient bridge" is therefore: R poly-simulates the propositional translation of Corr(M_e) for the polynomial algorithm e. Any proof of B(R) for concrete R must supply a uniform argument for provability of correctness, which is a meta-mathematical (unprovability) obstruction, not a combinatorial one. Pich–Santhanam (arXiv:2312.08163) give conditional links between EF lower bounds and P != NP; I did not verify their theorem statements here.

### Consequences for the five roles
- Lower-Bound Lead: aim only at systems where lower bound is open AND B is plausible (EF-like, with extension/definitions). Lower bounds for Resolution/AC0-Frege families cannot feed the bridge (F3).
- Reduction Builder: the combined system must be at least as strong as the bridge needs (F5/F6); R_mix341 without extension cannot rely on F5.
- Hypergraph/Certificates: hard-UNSAT families must resist EF-style extension and GF(2)/F3 algebra; Tseitin on expanders is GF(2)-easy.
- Time-Space Auditor: charge certificate bits and Corr(M_e) translation size.
- Red Team: attack F5 hypotheses (what exactly is provable in PV), and check whether R_mix341 simulates enough of EF.

### Literature check this run
Search found Pich–Santhanam, arXiv:2312.08163 (Towards P != NP from Extended Frege lower bounds) and Messner's results on p-optimal systems under P = NP; no source found that P = NP alone implies EF is p-bounded. Not independently verified.

### Not done / open
No lower bound on any fixed system, no transfer theorem for R_mix341. No repository tex/main.tex change made (this run was not an LSPV run).
