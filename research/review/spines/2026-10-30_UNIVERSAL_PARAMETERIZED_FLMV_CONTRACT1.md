# UNIVERSAL-PARAMETERIZED-FLMV-CONTRACT1
Date: 2026-10-30, America/Los_Angeles.

**Global proof status: P vs NP OPEN.** Known FLMV theorem; exact algebraic *conditional* contractor criterion; implementation/experiment-level stagewise controller design; no uniform all-input ARC transformation constructed. Independent review required before promotion.

## Research decision and prior work examined

The new `AFFINE-SMALLBIAS-DESCENT-GATE2` proves a source-independent *affine* truth-table reduction from MCSP[N^mu] to a strictly lower absolute threshold cannot preserve all YES/NO inputs with bounded error. This is a significant restricted semantic no-go, not a lower bound on unrestricted SAT. It weakens public-source-masking threshold descent as our main constructive spine, without excluding nonlinear MCSP reductions.

The newer `CONSTRUCTION-STRENGTHEN17` gives a SAT-preserving existential sorting-network normalization, but its implemented output is materialized, the final strict-(2,2) arbitrary-bit emitter is missing, and it does not lower a polynomial SAT solver's own workspace. `HITTING-TREE-COMPOSITION-REFEREE222` gives correct full-interface DP only with a supplied/obtained decomposition and bounded interface; `MONOTONE-PROBE-RESUME254` shows state-dependent reuse with charged wins and losses, not a global runtime upper/lower bound; `ARC-LINEAR22-SATURATION1` shows local clause-elimination size increases on a connected exact-(2,2) family, yet global bounded-degree isomorphism recognizes it in polynomial time. Thus local nonshrinking and high connectivity are not arbitrary-algorithm lower bounds. Existing complete histories, SIL parameter vectors, signed hypergraph and source-exposure work remain controls, not mandatory costs for every solver.

**Selection:** one integrated spine: a charged universal *parameterized residual-controller semantics* supporting a search for an arbitrary-decider `A -> Phi(A)` ARC resource contraction into the independently established FLMV forbidden time-space region. Competing MCSP reduction ideas remain secondary counterexample/constructive tests. Do not try to enumerate all polynomial algorithms or assume a fastest correct selector.

## Four falsifiers

1. **Policy discovery:** show whether the controller can identify a strong branching/backdoor/decomposition action with uniformly bounded source scans, failed trials and cache; test equal-score ties and adversarial renamings. A perfect semantic selector is itself a SAT oracle and cannot be free.
2. **All-input hereditary contraction:** on each residual, produce exact ordinary SAT children, including both YES and NO, with multiplicity <=N^gamma, length <=N^lambda, paid locally accessible descriptions and ancestor/live workspace. Test rigid signed-(2,2) instances, mixed Horn/XOR, high-width expanders, and easy high-width orbit families. A good local model is insufficient without global coverage.
3. **Uniform arbitrary-decider compatibility:** insert an unknown correct polynomial SAT decider A of time exponent K, space exponent L; test DELAY/COPY/RECOMP/INTERP wrappers. Any mandatory full-parent A(F) call retains exponent K and defeats the intended contraction.
4. **Forbidden-region model transfer:** optimize the actual FLMV Theorem 5.7 curve with certified infinite tail; require the *same* uniform deterministic total ordinary-SAT machine and simultaneous time and writable space, not pooled bounds, oracle gates, nonuniform data, free parent representations or a restricted problem's lower bound.

## Universal adaptive residual-controller object

Define a finite deterministic source-encoded state `z=(F,partial assignment,source-index/read position,authenticated derived clauses,branch/certificate stack,cache,policy history,representation descriptors)` together with an evolving *measured* parameter vector

`kappa(z)=(residual length, variables, clauses, certified tractable class, discovered backdoor size/depth, discovered treewidth/interface, affine rank, occurrence structure, child size, source/target access cost, source-exposure history, cache/replay, failed tests, peak live bits)`.

`kappa` is a **state description**, not a promised free oracle. Computing class membership and actual decompositions is charged. SAT and UNSAT may require different certified actions. Permitted actions include unit-propagation, 2SAT, Horn/dual-Horn, full-equation XOR Gaussian elimination, authenticated small-interface DP, exact branching/cofactor, genuine solver `A` calls, witness verification, finite proof/certificate validation, source-aware memo, and exhaustive fallback. A failed bounded repair has no UNSAT authority. Each action must preserve full original-source semantics and have explicit local run/access/source-read/output/replay/space costs. A deterministic correct policy over the actions defines a total SAT algorithm because it has a complete fallback; no polynomial worst-case bound is inferred from fallback correctness.

The selector is **inside** the machine. The existence, for each instance, of a cheap action/policy does not imply a uniform fast selection algorithm. E.g., the branch `return SAT with checked witness` is cheap on every satisfiable instance once the witness is supplied, yet finding which witness works is SAT search; UNSAT cannot be established by absence of a found witness in a bounded search. Perfect per-instance oracle selection is circular.

## Exact conditional FLMV contraction criterion

Let A be an arbitrary fixed uniform deterministic total exact ordinary-SAT decider on the FLMV indexed read-only-input random-access Turing model, running jointly in `T_A(N)<=N^(K+o(1))`, `S_A(N)<=N^(L+o(1))` on **all** N-bit inputs. Assume a single fixed **uniform compiler** `Phi` applicable to all such correct A (unknown K,L, not hardcoded) makes a total exact ordinary SAT decider, hereditary under repeated application, and proves on the SAME machine and source encoding

`K' <= max(alpha, gamma+lambda K)`,
`L' <= max(sigma, lambda L)`

for constants `0<=lambda<1`, alpha,gamma,sigma independent of A and K,L. All policy discovery, source bit probes, failed trials, child construction/multiplicity, transcript/replay, output, controlled random bits (if any), and ancestor/live storage are included. These are **unproved premises**, not automatic properties of dynamic programming.

Set `Kstar=max(alpha,gamma/(1-lambda))`, `Lstar=sigma`. Iteration has

`K_j <= Kstar + lambda^j max(0,K_0-Kstar)`,
`L_j <= Lstar + lambda^j max(0,L_0-Lstar)`.

Proof: substitute each inequality into the recurrence, use alpha<=Kstar, gamma+lambda*Kstar<=Kstar, sigma<=Lstar, and lambda*Lstar<=Lstar; induction. Fix any FLMV exponent `1<c<phi=(1+sqrt(5))/2` with `Kstar<c`, `Lstar<d_FLVM(c)` (strict). For every unknown finite K0,L0 some finite j yields `K_j<c`, `L_j<d_FLVM(c)`. Theorem 5.7 forbids the same deterministic total SAT algorithm with those simultaneous exponents. Hence under P=NP, a fully realized such compiler would give a contradiction. The missing mathematical work is **constructing Phi**, not rearranging the inequalities; this paragraph is a conditional criterion, not P!=NP.

FLMV Theorem 5.7: define f_0=1, f_k=c*f_(k-1)/(1+f_(k-1)), and `d_k(c)=min((1/f_k-c)/k, c^(-k))`. Set `d_FLVM(c)=max_{k>=1}d_k(c)`. If a positive best d was found after index k and `c^(-(k+1))<best`, all later indices have d_j<=c^(-j)<best and are certified irrelevant. A polynomial bound O(N^s) lies inside the exclusion `o(N^d)` only when s<d.

Numerical certified values: `d_FLVM(6/5)=23/45=0.511111111`, `d_FLVM(241/200)=11642479/23232400=0.501131136`, `d_FLVM(7/5)=949/5145`, `d_FLVM(3/2)=49/648`, `d_FLVM(8/5)=2145161/335544320`. These are KNOWN FLMV boundary computations already present in project, not new lower-bound theorems.

With the proposed (unconstructed) ARC coefficients alpha=11/10, gamma=3/5, lambda=1/2, sigma=1/2, the formal fixed point is `(Kstar,Lstar)=(6/5,1/2)`. The strict forbidden box at c=241/200 has available time slack `1/200` in exponent and workspace slack `11642479/23232400 - 1/2 > 0`. If each one of N^gamma child calls requires an additional parent-scale N^delta strategy-selection charge, replacing gamma with gamma+delta increases the formal fixed time to `6/5+2delta`; at fixed c=241/200 the strict test requires delta<1/400. Choosing c anywhere with d_2(c)>1/2 gives the larger absolute optimum delta<(c_half-6/5)/2≈0.00278471520, where `c_half≈1.20556943040059` is the positive root of `c^3+c^2-c-2=0` near 1.2. These margins are very narrow; all collection and acquisition costs must be explicit.

### Why the all-input requirement is load-bearing

A source-only A-independent rule which recursively creates <=N^gamma exact power-smaller children in N^alpha local time and N^sigma local space, with parameters in the strict FLMV region and no remaining A calls, would itself give a forbidden unconditional SAT algorithm. Thus asserting a universally cheap source-only splitter simply assumes the missing contradiction. An A-assisted stage can hypothetically evade this immediate objection, but has to query A only on strictly smaller ordinary instances or otherwise quantitatively control its dependence on K; an uncharged A(F) decision at parent size is not acceptable. DELAY wrappers are a decisive control on full-parent A calls.

## Exact computational audit (not a proof of the compiler)

`forbidden_envelope_audit.py` uses exact Python Fractions for all sampled c and recurrence iterations, with a certified infinite tail via `c^(-(k+1))<best`. For starting (K,L) in {(2,1),(4,3),(10,8),(100,50)}, under the hypothesized recurrence the first finite levels entering the strict c=241/200, d=d_FLVM(c) box are respectively j=8,10,11,15. This is only *numerical compatibility* of the asserted recurrence with FLMV. It does not establish the ARC edge or prove a real SAT machine achieves any of these points. Multiplicity, physical source bit access and per-instance selectors remain unconstructed.

## Primary literature

1. Fortnow, Lipton, van Melkebeek, Viglas. *Time-Space Lower Bounds for Satisfiability*. JACM 52(6), 2005, Theorems 3.1, 5.7, Corollary 5.8. https://lance.fortnow.com/papers/files/tst.pdf .
2. Dreier, Ordyniak, Szeider. *SAT backdoors: Depth beats size*. JCSS 142, 2024. https://doi.org/10.1016/j.jcss.2024.103520 . This supports state-dependent certified parameterized methods, not a global fast decider.
3. Gaspers, Szeider. *Backdoors to satisfaction continued*. Computer Science Review 60 (2026), article 100868. https://doi.org/10.1016/j.cosrev.2025.100868 .
4. CHMY STACS 2021 https://doi.org/10.4230/LIPIcs.STACS.2021.23 ; project AFFINE-SMALLBIAS-DESCENT-GATE2, 2026-10-30. Model mismatch with arbitrary SAT remains explicit.
5. Oliveira, Pich, Santhanam. *Hardness Magnification Near State-of-the-Art Lower Bounds*, Theory of Computing 17 (2021), https://theoryofcomputing.org/articles/v017a011/ .

## Single open arrow and role handoff

**OPEN: A uniform all-input, arbitrary-A total SAT-to-SAT successor Phi with fully charged local operations, genuinely smaller ordinary child sizes and multiplicities, recursively preserved correctness, and simultaneous source machine space below the FLMV threshold.** No other restricted lower bound can replace this bridge without a model-preserving theorem.

LSPV-1 lead quantifier/machine contract; LSPV-2 implement genuine state-dependent certified strategy portfolio and cost ledger; LSPV-3 adversarial residual/selection controls, high-width easy instances and separate SAT/UNSAT measurements; LSPV-4 exact FLMV curve, strict22 normalizer/accessor and matched model; LSPV-5 independently refute the ARC arrow, audit both labels, quantifier order, machine model and new affine lemma, synthesize status. No additional agent or schedule required. Preserve paused/enabled status as encountered unless explicitly asked to change it. Root main.tex is not rewritten without valid ownership.

END_OF_VERIFIED_REPORT::UNIVERSAL_PARAMETERIZED_FLMV_CONTRACT1::P_VS_NP_OPEN