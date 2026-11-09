# Living log: worst-case minimum-derivation cost  \overline W_R(N)

Directive (user, 2026-11-09): study
  W_R(N) = max_{F in UNSAT, |F|<=N}  min_{pi: F |-_R bot} cost_R(pi),
with the optimal derivation chosen for free (strategy search is not charged, which is valid for lower bounds on executing it).
Priority bridge:  SAT in P  =>  W_R(N) <= poly(N).   Secondary: pointwise / worst-case simulation theorems.
Five roles: General SAT Lower-Bound Lead; SAT-Circuit Reduction Builder; Hypergraph & Proof Certificates; Time-Space Resource Auditor; Independent Proof Red Team.
Status labels: PROVED/EXACT, KNOWN THEOREM, COMPUTATIONAL, CONDITIONAL, CANDIDATE, OPEN, FALSIFIED/RETIRED. **P vs NP remains OPEN.**

## Entry 2026-11-09 (scheduled run 1)

### Corpus touched
Repo tree survey; AGENTS.md; latest LSPV-3/532 commits (pinned-path linear Resolution upper-control certificates, 2026-11-09 04:3x). No file previously stated this directive, so this log is its first home. Prior RES-control evidence (LSPV-3 516-518, 532) is reusable as hard-family upper controls only.

### Analysis (red-team first)
1. **W_R is a Cook-Reckhow proof-size quantity.** With size/time cost, min_pi cost_R(pi) is the shortest R-refutation (up to verification time). [KNOWN THEOREM, Cook-Reckhow 1979] a polynomially bounded proof system for UNSAT exists iff NP = coNP. So "W_R superpolynomial for a fixed R" is only a *lower bound for that R*; it implies NP != coNP only if R is p-bounded-universal, otherwise it implies nothing.
2. **The bridge as stated is false for natural fixed R.** SAT in P does not give W_R <= poly for R = Resolution, Cutting Planes, Frege-like etc.: Resolution has exponential-size refutations of PHP/Tseitin/random-CNF families (Haken, Urquhart, Chvatal-Szemeredi) unconditionally, while SAT in P is not contradicted. [KNOWN THEOREM + trivial logic] So the bridge needs R to be *rich enough that every polynomial-time SAT decider has a polynomially short R-certificate of its UNSAT answers*.
3. **Weakest sufficient R (CONDITIONAL).** Let D be a poly-time SAT decider. Define R_D: a refutation of F is the empty string, accepted iff D(F)=0. This is a Cook-Reckhow system, poly-bounded when SAT in P (indeed W_{R_D} <= poly). For the bridge to hold for a *single fixed* R independent of D, R must p-simulate R_D for every poly-time D, i.e. R must be (at least) optimal among systems of the form R_D. A fixed R with this property is an **optimal / p-optimal proof system for TAUT restricted to P-decidable-complement cases**. [KNOWN: existence of optimal proof system for TAUT is the open Krajicek-Pudlak question; it follows from NE=coNE, p-optimal from E=NE; Egidy ICALP 2026 and arXiv 2602.02294 revisit this.] Consequence [CANDIDATE reformulation]: the bridge for fixed R is a *hypothesis on R* ("R is optimal on the P-decidable part"), and proving it unconditionally is the same difficulty as the optimal-proof-system problem. Escape routes: (a) let R be uniform-parameterized by the decider (R = R_D family, bridge becomes trivial but then the lower bound is not a single-system statement); (b) use **time-space cost** (the directive's "work") with a *machine-model* system whose derivation steps are TM transitions: then R_TM-trace is complete and W_R(N) is the deterministic-time complexity of refuting, bridge holds trivially but W_R superpoly is exactly SAT not in P restated (an EQUIVALENT of P != NP, i.e. a reformulation, no progress; cf. world ledger rule).
4. **Dichotomy for the programme (CANDIDATE, to be formalised):** for any cost model, either R is *weak* (lower bounds provable, bridge false) or *machine-complete* (bridge true, lower bound = P != NP). A useful target is an *intermediate* R with a proved transfer "SAT in P => W_R poly" via a **simulation theorem** (every poly-time decider's computation on UNSAT F can be compiled into an R-derivation of poly size) that holds for a structured but non-trivially-complete R, e.g. extended Frege/bounded-arithmetic S^1_2 style (Cook's PV translation gives exactly this under the hypothesis that PV *proves* the decider correct; unconditional version needs correctness proof, **OPEN**).
   Sharper statement: [CONDITIONAL] if SAT in P via decider D and PV (or S^1_2) proves D sound, then extended Frege polynomially refutes all UNSAT F (Cook 1975 translation). The gap is provability of soundness, the standard obstruction (Krajicek, "Bounded Arithmetic, Propositional Logic and Complexity Theory").
5. **Free choice of optimal sequence** is harmless for lower bounds but also *erases* the usual dichotomy hardness: min over sequences = proof size, the quantity whose superpolynomial lower bound for strong R (Frege, EF) is OPEN; best known: Frege lower bound only quadratic-ish (Krajicek, Bonet-Buss-Pitassi style), super-polynomial known only for Resolution, bounded-depth Frege, Cutting Planes (monotone interpolation), polynomial calculus.
6. **Hard-family survival test (Hypergraph & Proof Certificates):** a family surviving resolution, algebraic (PC/SoS), circuit compression and shared-DAG sharing must beat: Tseitin on expanders (PC over F_2 fails parity but over other fields not; also easy for Gaussian-elimination-aware systems), PHP (poly in EF/Frege), random k-CNF (hard for Res/PC/CP, open for EF/Frege). Only random-CNF-style families remain plausible against strong R, and no technique applies to Frege. [KNOWN]

### Role assignments for next cycles
- Lower-Bound Lead: state precise transfer theorem T(R): "SAT in P => W_R <= poly" as a property of R; classify known R by it (Res: false; EF under soundness-provable: conditional true; R_TM: trivially true).
- Reduction Builder: define a fixed combined system R* = Res + PC + CP + EF-shared-DAG; certify shortest-DAG on small N by SAT-solver DRAT/LRAT proofs (computational, chunks <=30 s).
- Proof Certificates: audit existing LSPV-3/532 pinned-path families against this W_R definition; report which are only upper controls.
- Time-Space Auditor: fix cost_R = (steps, peak DAG width) and show the verification overhead is poly in |pi|.
- Red Team: attack item 3's claim that bridge for fixed R collapses to optimal-proof-system existence; seek an R that is not optimal yet satisfies T(R) via a non-uniform argument.

### Status
Nothing new proved toward P != NP. New CANDIDATE: reformulation items 3-4 (bridge ≡ optimality/soundness-provability hypothesis; machine-complete R gives equivalent of P != NP). All load-bearing arrows OPEN.

### Literature clues checked
Cook-Reckhow 1979; Krajicek-Pudlak 1989 (optimal systems); Egidy, ICALP 2026 (LIPIcs 374, paper 88) and arXiv 2602.02294; Cook 1975 / Krajicek bounded arithmetic translation. Not yet read in full: the two 2026 Egidy papers (only titles/snippets seen); next run should read them for recursive-jump/optimality results bearing on item 3.

END_OF_ENTRY 2026-11-09
