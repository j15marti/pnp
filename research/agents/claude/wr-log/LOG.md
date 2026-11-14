# Living log: worst-case derivation directive (Claude scheduled routine)

Append-only log for the scheduled Claude routine working on the shared target
`Wbar_R(N) = max_{F UNSAT, |F|<=N} min_{pi: F |-_R false} cost_R(pi)` and the bridge
`SAT in P => Wbar_R(N) <= poly(N)` (B3). This routine is not one of LSPV-1..5 and
owns no region of root `main.tex`. **P versus NP remains OPEN.**

---

## 2026-11-14 — WR-0001

- **Report:** `research/agents/claude/2026-11-14_CLAUDE_WR-0001_PV_FEASIBLE_B3.tex`
- **Question:** what does B1 buy without B3, and how close is B3 to a known theorem?
- **Found:**
  - Theorem 1 (KNOWN THEOREM, Cook 1975): if PV proves `forall x,y [Sat(x,y) -> Sat(x,f(x))]` for some poly-time f, then every UNSAT CNF has an EF refutation of size poly(N), and a poly-time map builds it.
  - Theorem 2 (CONDITIONAL on the LSPV-1/592 hypotheses, P2-D1): combining Theorem 1 with the 592 simulation, the same hypothesis gives the constructive same-R B3 generator.
  - Corollary 3: B1 alone, for any ER-simulating R, would prove Bydžovský–Krajíček–Oliveira Conjecture A.1 (P != NP is consistent with PV). This consequence holds without B3.
  - The remaining B3 gap is exactly truth versus PV-provability of `phi_{P=NP}(f)`. LSPV-1/357's per-algorithm firewall does not close it.
- **Literature this run:**
  - BKO LMCS 2020 App. A, read in the primary source.
  - Res(⊕) status: arXiv 2507.23008 and arXiv 2511.20023. DAG-like Res(⊕) is still open. This is a failed transfer to full R, because paid DEF gives R the strength of ER.
  - The Cook–Krajíček 2007 equivalence could not be fetched (HTTP 503) and is not used.
- **Ledger:** added world-ledger rows L41 (Conjecture A.1, half-win if P != NP) and L42 (EF p-bounded, undetermined by P vs NP).
- **Not done:** no lower bound and no B3 proof; root `main.tex` was not edited. A stale timestamp was found at `main.tex` line 4.
- **Next:** screen candidate B1 families against known polynomial EF proofs before spending R_mix341 search on them.
