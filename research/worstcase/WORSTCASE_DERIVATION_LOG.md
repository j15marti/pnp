# Worst-case derivation-cost programme: living log

Target: W̄_R(N) = max over UNSAT F with |⟨F⟩| ≤ N of min over refutations π of cost_R(π).
Weakest bridge: B_R := ( SAT ∈ P ⟹ W̄_R(N) ≤ poly(N) ).
Status discipline per AGENTS.md. **P versus NP remains OPEN.** The bridge B_R and the superpolynomial lower bound are both OPEN.
Existing related corpus: `research/agents/lspv-1/2026-11-02_1832_LSPV-1_MUS_WORSTCASE_QUOTIENT350.tex` (fixed R_mix341, core-size sandwich μ(F)-1 ≤ W_R(F) ≤ 3^{μ(F)-1}), LSPV-1 349/351/352, LSPV-3 352.

---
## Entry 2026-11-03 (scheduled run, one agent acting for all five roles)

### New results (elementary; proofs are short, but not previously recorded in this corpus as far as the survey found)

**L1 (Bridge-equivalence lemma). PROVED/EXACT.**
If W̄_R is superpolynomial (proved unconditionally), then B_R ⇔ SAT ∉ P.
*Proof.* B_R is "A ⟹ B" with B false, so it is equivalent to ¬A. ∎
*Consequences.* (i) For resolution, bounded-depth Frege, PC, cutting planes etc., which have unconditional superpolynomial lower bounds, the bridge is **equivalent to P ≠ NP**, so it cannot be a *step* towards it. (ii) The bridge has independent content only for R whose lower bounds are open (Frege, Extended Frege, stronger). So the "sufficiently powerful fixed system" in the directive must be at least that strong, and the lower bound then is itself a Frege/EF lower bound, a famous open problem.

**L2 (Free-strategy minimum is NP-versus-coNP, not P-versus-NP). KNOWN THEOREM (Cook–Reckhow 1979) + remark.**
∃ proof system R with W̄_R polynomial ⇔ NP = coNP. So "granting the optimal derivation for free" removes exactly the search/automatizability issue and leaves a coNP-versus-NP question. Hence W̄_R ≥ superpoly for *every* R would prove NP ≠ coNP, which implies P ≠ NP. The programme is therefore sound as a strategy but aims at the stronger conclusion NP ≠ coNP. Lower bound for one fixed R proves nothing about P vs NP unless coupled with B_R.

**L3 (Conditional bridge, exact form). PROVED/EXACT.**
Suppose M is a polynomial-time SAT decider and R is closed under modus ponens/cut with polynomial overhead (Frege-type). Let Sound_M(n) be the family of poly-size tautologies expressing "M(x)=0 on |x|=n ⟹ x ∈ UNSAT". If R has poly(n)-size proofs of Sound_M(n), then every UNSAT F has an R-refutation of size poly(|F|): write the trace of M on F (poly size), instantiate Sound_M, apply MP. So B_R follows from **feasible provability of the correctness of some poly-time SAT algorithm in R**. This is the Cook/Krajíček EF ↔ PV correspondence in this notation. Corollary: if EF proves Sound_M for a P=NP algorithm M, EF is polynomially bounded. Whether P=NP ⟹ such provability is open, and natural independence phenomena (a correct algorithm whose correctness is unprovable) are consistent with current knowledge.

**L4 (Existence vs. explicitness). CONDITIONAL / KNOWN (Krajíček–Pudlák 1989).**
If P = NP then E = NE and NE = coNE, so an optimal and even p-optimal proof system exists for TAUT (Krajíček–Pudlák). That system satisfies B_R. But the system is defined from the unknown machines witnessing the collapse, i.e. it is not an explicit R fixed in advance. So B_R is *true for some R if P=NP*, but an explicit proof-of-lower-bound against that R requires knowing it. A usable bridge needs an explicit R plus a proof it is optimal, i.e. the open optimal-proof-system question. Messner and Egidy–Glaßer (STOC 2025) give oracle evidence that this cannot be settled by relativizing methods.

### Red-team (role: Independent Proof Red Team)
- Candidate hard families (odd Tseitin, Horn chains, assignment-blocking) already shown to have short mixed proofs in R_mix341 (LSPV-1 350). Consistent with L2: any R-hardness must come from beyond-R_mix341 families.
- Transfer attempt "algorithm ⇒ short DAG by running it": fails because the DAG must be *sound under R's local rules*, which is exactly L3's provability requirement. No free semantic rule (that would be an unsound or oracle R).
- Pointwise stronger bridge (every F: shortest R-proof ≤ poly(time of M on F)): even more demanding, retired as primary target.

### Time/space audit
Nothing new computed. Under L3 the proof size is O(T_M(n)^c) for a trace of time T_M; peak memory of *writing* the proof is O(T_M) in the naive DAG, polylog-space re-derivation is not claimed.

### Literature check
- Cook–Reckhow 1979 (NP=coNP ⇔ poly-bounded proof system). Krajíček–Pudlák 1989 (NE=coNE ⇒ optimal; E=NE ⇒ p-optimal). Messner: coNE-hard sets lack optimal systems. Egidy–Glaßer STOC 2025 (relativization limits) and Egidy 2026 arXiv 2602.02294 (SPARSE-relativization; not read in full here).
- Relevant open item to chase next run: whether any natural class of "provably-correct poly-time algorithms" makes B_R unconditional for EF in a restricted fragment (Cook–Krajíček on PV provability).
- Not found: any literature route to B_R for a *natural explicit* R.

### Failed / retired
- Treating B_R as a stepping stone for weak R: **RETIRED** by L1.
- Using a single fixed R's lower bound to conclude P ≠ NP without B_R: **RETIRED** (lower bound alone gives only that R is not poly-bounded).

### Next decisive lemma
Either (a) a restricted-but-nontrivial R (stronger than Res, weaker than EF) with an unconditional lower bound AND a proof that P=NP implies B_R (impossible by L1 unless it proves P≠NP), or (b) accept R ⊇ EF and attack provable-correctness: show that for some explicit R, P = NP ⟹ R proves Sound_M for some M. Recommended focus: (b), i.e. study which poly-time-algorithm correctness statements EF can prove, and whether Levin-style universal search has a feasibly provable correctness certificate.

P versus NP remains OPEN.
