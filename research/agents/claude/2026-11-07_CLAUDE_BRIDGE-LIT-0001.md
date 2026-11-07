# CLAUDE BRIDGE-LIT-0001 | Literature check for the worst-case derivation bridge (2026-11-07)

Status: KNOWN THEOREM citations + one CANDIDATE observation. **P versus NP remains OPEN.** No new load-bearing arrow closed. Scheduled run; bounded scope.

Target: bridge  SAT in P  =>  Wbar_R(N) <= poly(N)  (Route B / B3, trackers proof2.txt [P2-B2]).

## Literature (standard web search; primary sources only cited, none re-derived here)
- Atserias--Muller, "Automating Resolution is NP-hard", FOCS 2019 / JACM 2020 (arXiv 1904.02991): finding Resolution refutations within poly of shortest is NP-hard; not automatable unless P=NP. KNOWN THEOREM.
- Arteche--Atserias--de Rezende (2025, arXiv 2506.16956): feasibly constructive version; Extended Frege proves the formalized hardness statement. KNOWN THEOREM (as reported by search snippet; not read in full).
- Bonet--Pitassi--Raz: automatability implies feasible interpolation; Krajicek 1997: Resolution has feasible interpolation. KNOWN THEOREM.
- Cook--Reckhow 1979: NP=coNP iff some proof system is polynomially bounded. KNOWN THEOREM.
(No 2026-specific result found bearing on B3.)

## Observation (CANDIDATE, consistent with existing corpus; classification: EXACT OBJECT TRANSFER)
1. For weak R (ordinary Resolution, Res(XOR)-type systems with known exponential lower bounds on Tseitin/PHP), Wbar_R is unconditionally superpolynomial. Hence "SAT in P => Wbar_R <= poly" is then logically equivalent to "SAT not in P". Such an R can serve only if the lower bound is proved *independently*; the bridge adds nothing. This matches the clock-guard firewall LSPV-1/462 and the Q_A simulation equivalence LSPV-5/409 in the corpus.
2. Automatability results say discovery cost is NP-hard even when short proofs exist. The directive grants free optimal-sequence choice (min over proofs, discovery uncharged), so these results do not obstruct the lower-bound-on-execution framing, but also give no lower bound on the minimum itself.
3. Under SAT in P, NP=coNP, so by Cook--Reckhow a polynomially bounded system exists (Q_A of LSPV-5/409). The open content is exactly that the *preselected* R simulates it. No literature result found closes this; a proof for a fixed strong R (Frege/EF-like) would need NP=coNP-type input, i.e. the bridge for strong R is a restatement of a known-hard problem.

## Next obligation suggested
Pick R strictly between Resolution and Frege where (a) an unconditional superpolynomial lower bound is unknown and (b) the simulation Q_A <=_W R is checkable; test whether feasible interpolation for R (Krajicek-style) gives a conditional path. Not attempted this run.

% END_OF_CLAUDE_REPORT::BRIDGE-LIT-0001
