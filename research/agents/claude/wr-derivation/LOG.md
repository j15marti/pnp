# Living log: worst-case derivation-cost program (W_R bridge)

Target: W_R(N) = max_{F in UNSAT, |F|<=N} min_{pi: F |-_R bot} cost_R(pi); free choice of pi (search not charged).
Bridge sought: SAT in P  ==>  W_R(N) <= poly(N).   P versus NP remains OPEN. Nothing below is a proof of P != NP.
Status labels: PROVED/EXACT, KNOWN THEOREM, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED.

## Entry 2026-11-08 (Claude, run WR-0001) — structure of the bridge

Corpus note: no prior W_R log existed; many LSPV-1 reports mention min-cost derivations (e.g. 2026-11-02_1657 SIGNED_ORBIT_MINCOST348) but none formalizes the bridge. Not re-read in full this run.

Setting. Call R a *local* system if every step is checkable in time poly(|state|) (a multisign DAG-hypergraph rewrite system with local steps is local) and cost_R = total step cost (size). Then R is a Cook–Reckhow proof system for UNSAT.

T1 (PROVED/EXACT, trivial logic). If W_R is unconditionally superpolynomial (resolution, cutting planes, bounded-depth Frege, etc.), then Bridge(R) is logically equivalent to "SAT not in P". So for every system with a known lower bound, the bridge is *exactly as hard as P != NP*, not weaker. The bridge only has independent content for systems whose W_R lower bound is open (Frege, Extended Frege).

T2 (KNOWN THEOREM / standard, Cook–Reckhow). For local R: W_R poly  <=>  R polynomially bounded  =>  NP = coNP. Conversely SAT in P gives NP = coNP, hence a polynomially bounded system R_A ("trace of A") exists — but it depends on A.

T3 (PROVED/EXACT from T2). Bridge(R) for a fixed uniform R is equivalent to "P=NP => R p-bounded". Obtaining it needs R to p-simulate R_A for the unknown correct A, i.e. R must prove (in poly size) soundness instances of an arbitrary correct SAT algorithm. Known sufficient case: A provably correct in PV/S^1_2 and R = EF. In general OPEN (this is the Krajíček–Pudlák optimal-system territory).

T4 (PROVED/EXACT). Free choice of derivation does not weaken the problem: with local checkable steps, min over sequences = proof size, so "W_R superpoly for ALL local R" would give NP != coNP (stronger than P != NP). Single fixed R is the only route that can target P != NP alone, via LB(R) + Bridge(R).

T5 (CANDIDATE barrier). To make the bridge provable, R must contain reflection for poly-time algorithms; lower bounds for such R are the EF-lower-bound problem, widely believed hard to prove in weak theories (Pich–Santhanam line). Not claimed as a theorem here.

Consequence for the five roles:
1. Lower-Bound Lead: aim Bridge at R = EF (or Frege) with the PV-provable-correctness hypothesis made explicit; this is a CONDITIONAL bridge. Do not seek a bridge for resolution-like R (T1).
2. Reduction Builder: any multisign DAG hypergraph system with local steps is local (T2); to exceed Frege it must simulate EF-style extension/abbreviation.
3. Hypergraph/Certificates: hard families for weak R (resolution, ACC-like algebraic) are consistent with everything but cannot feed the bridge (T1); useful only as controls for the red team.
4. Resource Auditor: charge each step by encoding size; peak memory = max state size along the DAG; for time-space, bound min over pi of (size, width) jointly.
5. Red Team: attack T3 (is there a known fixed R with Bridge(R) provable unconditionally?) and any claim that "free sequence" yields a P-vs-NP-only bound.

## Literature check (this run)
- Pich–Santhanam, "Towards P != NP from Extended Frege lower bounds" (arXiv 2312.08163): conditional implications from EF non-p-boundedness to P != NP — same shape as Bridge + LB. Details not re-verified here. https://arxiv.org/abs/2312.08163
- Haastad, small-depth Frege PHP bounds (TheoretiCS 2025); Haastad–Risse Tseitin on grids (rev. Oct 2025): restricted-depth only, fall under T1 (no bridge).
- Jerabek (BSL 2025): for unrestricted Frege only linear line / quadratic size lower bounds known.
- Search did not surface any 2025–26 general Frege/EF lower bound.

## Open next steps
- Formalize "multisign DAG hypergraph" step set and prove it simulates / is simulated by a standard system (determine its strength class).
- Write out T3 carefully with the PV-correctness hypothesis; check against Krajíček's monograph.
- Verify the Pich–Santhanam statement before citing as more than a pointer.

END_OF_ENTRY::WR-0001
