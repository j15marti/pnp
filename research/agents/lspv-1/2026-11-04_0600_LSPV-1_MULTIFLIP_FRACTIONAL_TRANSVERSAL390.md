# LSPV-1/390: Exact multi-flip signed-neighbor transversal
**November 4, 2026, 06:00 PST. PROVED/EXACT elementary lemmas, independent specialist review pending. COMPUTATIONAL independent controls. B1/B2/B3 and P versus NP OPEN.**

## Published-hard-family anchor; no false computational transfer

Haken (1985, The Intractability of Resolution, TCS 39:297-308, DOI 10.1016/0304-3975(85)90144-6) established: for constants c>0,h0 and every h>=h0, **every** ordinary unrestricted shared-DAG Resolution refutation of standard explicit unary PHP(h+1,h) has >=2^(ch) proof lines. It has h(h+1) variables, (h+1)+h*binom(h+1,2) clauses and a Theta(h^3 log(h+2)) bit conventional explicit signed indexed encoding. Free source axioms leave at least 2^(ch)-m derived nodes. This is NOT an Extended Resolution, Res(oplus), fixed mixed R, or all-algorithm SAT lower bound. Cook (1976) gives polynomial Extended Resolution PHP proofs; odd Tseitin has polynomial GF(2) shortcuts. Braun (arXiv:2609.23015, September 19, 2026), reports >exp(n/(32768 ell^2)) unrestricted DAG Res(oplus) lines on bit-PHP for n=2^ell and ell>=32, with a Theta(n^3 ell^2)-bit indexed source; this excludes ER extensions and does not give SAT machine hardness. Independent specialist review of Braun is not asserted.

Our preselected R_mix341 is unchanged from LSPV-2/341 blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb: free source-labelled clauses, unit-paid RES, AND3 on at most 3 original variables, binary GF(2) XOR, locally authenticated LOCAL-CONVERT, conservative unit-paid binary DEF, at most two antecedents per paid node and shared DAG counted once. Ambiguous full LOCAL-CONVERT typed coercion/public-port semantics remain unresolved.

## Theorem 390A: fractional neighbor-query lower bound

Fix a valid N-bit UNSAT encoding x and a set Y of valid same-length SAT encodings. For each y in Y let D_y be the positions at which y differs from x. Define tau*(x,Y) as the linear-program minimum sum_i z_i subject to 0<=z_i<=1 and sum_(i in D_y) z_i>=1 for every y. Define integral tau likewise with z_i in {0,1}.

**PROVED/EXACT:** Every one fixed total uniform adaptive randomized SAT/UNSAT/malformed decider A, correct on every binary input with error at most epsilon<1/2, obeys
$$
E[distinct original input bit positions read on x] >= (1-2epsilon) tau*(x,Y).
$$
For deterministic exact A the read set has cardinality >=tau(x,Y). If one paid source probe reveals at most b original bits, the expected probe count is >=(1-2epsilon)tau*/b.

**Proof:** Couple the runs of A(x) and A(y) with the identical random tape. They see the same answers and execute identically until a bit in D_y is queried. Their probabilities of outputting UNSAT differ by >=1-2epsilon, so the probability of inspecting some bit of D_y on x is >=1-2epsilon. Put p_i=Pr[i queried on x]. The union bound gives sum_(i in D_y)p_i>=1-2epsilon for every y. z_i=min(1,p_i/(1-2epsilon)) is feasible. Therefore sum_i p_i >=(1-2epsilon)tau*. For exact deterministic A, failure to hit one D_y would produce identical outputs on opposite labels. No assumption about internal representation, adaptivity, GF(2), lazy circuits or paid auxiliaries enters except that input access is charged. The same argument holds for a sound randomized UNSAT verifier given the **same alleged certificate** against x and each SAT neighbor, assuming completeness on x and soundness on every y. QED.

This generalizes the prior single-sign sensitivity result LSPV-3/390 and is a specialization of classical decision-tree adversary/hitting-set methods, not a novelty claim in complexity theory. It is relative to the declared source encoding, NOT invariant under arbitrary source recodings.

## Theorem 390B: exact all-neighbor sign-only radius and transversal

Let F=AND_j C_j be clause-minimally UNSAT, with no empty clauses, m labelled clauses and L=sum_j |C_j| signed literal occurrences. D_r(F) contains r verbatim but separately labelled copies of each clause. Fix the entire grammar layout, literal variable IDs and clause order; only rL independent sign bits can change. Let Y_r include **every** SAT sign-only variant of this fixed layout. For every integer r>=1,
$$
boxed{ d_sign(D_r(F),SAT)=r, \quad tau(D_r(F),Y_r)=tau*(D_r(F),Y_r)=L. }
$$
More generally for any nonempty-clause F, d_sign(D_r(F),SAT)=r * mu(F), where mu(F)=min_a #{j:C_j(a)=0}.

**Radius proof:** An assignment a falsifying t original clauses requires >=1 sign change in each of the r copies of each such clause, and exactly rt changes suffice by negating one currently false literal in each copy. Minimize over a. Minimal UNSAT ensures some assignment falsifies exactly one original clause, since deleting any clause is SAT. Thus mu=1 and radius=r.

**Transversal proof:** For each original literal occurrence (j,k), choose an assignment satisfying all original clauses except C_j; every literal of C_j is false on it. Flip the sign at (j,k) in all r copies. The resulting formula is SAT under that assignment. These L SAT-neighbor difference supports are pairwise disjoint r-element sets, forcing every fractional hitting solution to have total weight >=L. Conversely select the sign bit of just the first copy of every one of the L original occurrences. Any variant leaving all those selected bits unchanged contains an unchanged original UNSAT F as its first-copy subformula, hence is UNSAT. These L bits hit every sign-only SAT neighbor, giving tau<=L and tau*<=L. QED.

**CRUCIAL SCOPE:** The upper equality tau=tau*=L is about sign-only fixed-layout variants. A SAT neighbor with changed header, variable indices, clause structure or other binary fields need not be hit by those L positions. Yet the L explicit sign-only SAT neighbors remain valid **full encoded** SAT inputs, so any all-input-correct A still has the lower bound (1-2epsilon)L on reads of their signed polarity positions. The same source trace cannot be used as an UNSAT certificate on a SAT neighbor.

## Exact existing mixed-calculus control and new combined identity

LSPV-2/341 proved for odd-charge connected bridgeless cubic Tseitin F_h: 4h original indispensable three-literal clauses, 12h sign occurrences, and W_Rmix341(F_h)=4h-1. LSPV-3/393 blob 56cab30fa9bd751586c682cebd7131341493d77f **already proved** the global fixed mixed minimum survives r-fold literal-preserving source duplication: W_Rmix341(D_r(F_h))=4h-1. This run does not re-prove or relabel that old optimum.

For every h,r in this family, new Theorem 390B together with the prior verified results gives:
$$
(d_sign, tau*_sign, W_Rmix341)=(r,12h,4h-1).
$$
An arbitrary increase of nearest-SAT sign Hamming distance need not increase either the exact claimed input-read transversal or the shortest paid refutation DAG. For r>1, no single sign bit is pivotal, but multi-bit opposite-label witnesses still imply unavoidable sign reads by any correct adaptive solver. The actual explicit indexed original encoding is Theta(r*h*log(h+2)+log(r*h+2)) bits under implicit source order; any added explicit source label fields must be charged. This is a **linear input-access floor**, never a superpolynomial machine lower bound. Do not confuse this source statistic with arbitrary machine space, program acquisition or B3.

## Falsifiers (exact status)

F1 **FALSIFIED/RETIRED:** nearest-SAT sign radius r forces >=r paid derivation nodes. Hold h=4 and let r grow; R_mix341 minimum stays 15.

F2 **FALSIFIED/RETIRED:** if no sign bit is singly pivotal, there is no representation-agnostic input-bit acquisition bound. The L disjoint r-bit SAT-neighbor supports force >=(1-2epsilon)L expected distinct reads even at r>1 in the charged source-bit model.

F3 **FALSIFIED under charged access:** Gaussian elimination, compact circuits, randomness, or auxiliary wires can reliably distinguish all opposite-label neighbors without reading a bit where they differ. Identical-randomness coupling precludes that, irrespective of subsequent computation.

F4 **FALSIFIED AS A TRANSFER:** the fractional neighbor invariant yields B3 or a superpolynomial SAT runtime lower bound. The all-ones fractional cover gives tau*<=N; no writable-space or paid-node lower bound follows.

## Verification and physical ledger

**COMPUTATIONAL:** public no-seed Node producer tested K4 and 6-vertex triangular prism, with duplication r=1,2,3,4. Every odd source was UNSAT and even control SAT. Every original clause deletion had a satisfying witness. For each source literal occurrence, all r identical-sign flips produced SAT with an explicit witness; at r>1 one-flip and (r-1)-flip controls remained UNSAT. The producer completed 2,134 assertions. Exhaustively enumerating all sign-only assignments for duplicated contradictory unit pairs at r=1,..,5 yielded exact distance r and two SAT variants each. An independently authored Python verifier independently reconstructed both graphs and clause signs and passed 1,636 assertions on the published raw results. Malformed source strings were rejected. This does NOT verify a generic native R_mix341 transcript, certify an asymptotic proof by finite checks, or equate best proof nodes with machine time.

For actual T/S, separately charge parsing, input bit/index/head access, failed policies, switching, circuit construction/conversion, source updates, serialized proof and output bytes, verifier work, cache size, temporaries and all-phase peak memory. A compact logical proof does not imply that authenticating all r copies is free, and a large presentation need not be materialized if a sound lazy alternative exists. The FLMV envelope s'<=max{rho,eta,lambda,lambda*s} must include every local phase. No same-machine FLMV implication is derived.

## Corpus / duplication / external audit

READ: controlling refocus research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, Git blob c3889a3e; issue #3 through November 4 05:36 PST; AGENTS.md blob 19656af1; CODEX.md blob 754999f5; repository pnp skill blob b8df83a7; LSPV-1/389 blob 45b660c3; original LSPV-2/341 c87acd11; LSPV-3/393 56cab30f; LSPV-2/390 affine clause spectrum; LSPV-4/385 streaming equality; Red Team/336 642652d2. The grouped deletion theorem /393 and earlier sign-sensitivity /390 are credited; the increment here is **exact fractional all-neighbor cost and duplication radius**.

GROK ACTUAL: GROKPROOF/2026-11-04_1322_PROGRESS.md, blob 0850246c1a1ea9a511d12a4de041b8752f69922a, no all-input charged resource contraction. CLAUDE ACTUAL: research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67, restricted alternation trading, no B3 bridge. Checked project code search for B3/reflection and github.com/openai/math Cook-Reckhow, with no applicable missing simulation. Literature queries: Haken PHP 1985, Cook PHP ER 1976, Braun September 2026 Res(oplus), Cook-Reckhow 1979, and classical decision-tree fractional adversary. No new formula is proposed as a hard SAT family.

## Quantifier discipline and next gap

Fix one effective unchanged R=R_mix341. For all uniformly total correct A on SAT, UNSAT and malformed:
B1: forall A exists polynomial p_A forall UNSAT F, W_R(F)<=p_A(|F|+T_A(F)).
B2: forall A exists polynomial p_A forall N, Wbar_R(N)<=p_A(N+T_A^wc(N)), where T_A^wc maximizes over ALL binary strings through length N.
B3: SAT in P => Wbar_R(N)=N^O(1) in this SAME R.
All remain **OPEN**, as does superpolynomial worst-case Wbar_R and P versus NP. B1=>B2=>B3. The present input-query lower bound addresses neither B3 nor hard all-mixed minimum. Next: LSPV-3 test multi-neighbor transversals on established nonaffine minimal UNSAT; LSPV-2 audit sign-bit encoding and GF(2) shortcuts; LSPV-4 charge adaptive block reads/recomputation and verifier model; LSPV-5 audit full-input neighbor set and universal quantifiers; LSPV-1 continue formal B3/reflection audit and original LOCAL-CONVERT grammar. No tasks or schedules are changed.