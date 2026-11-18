# SIGMA2 UNIFORMBARRIER28 | 2026-11-18 America/Los_Angeles

STATUS: EXACT uniform/nonuniform candidate-fiber compiler equivalences; independent finite controls PASS. This is a synthesis of known complexity theory into the j15marti/pnp QBF compiler program, NOT a new P vs NP proof. P vs NP OPEN.

## PROPOSE BEFORE SEARCH
1. All-source uniform candidate-preserving eliminator for polynomial-length universal seeds.
2. Uniform vs nonuniform universal-response programs and P/poly barrier.
3. Hypothetical P=NP adversarial SAT service with every query and compilation cost charged.
4. Small selector versus genuinely long universal seed, common-X and gate-trace quantifier obstructions.
5. Mixed Horn/dual-Horn gluing counterexample to clause-local tractability dispatch.

## SEARCH
Direct GitHub reads: research/agents/sigma-primary/2026-11-18_CANDREN_HORN27.md; research/agents/sigma-primary/2026-11-17_COVERMITER24.md; research/agents/sigma-primary/2026-11-17_IMPLIESCC25.md; root proof1.txt, proof2.txt. COVERMITER24 already discussed nonuniform response concerns. This report makes an all-source compiler equivalence explicit.
Primary literature Cook STOC 1971 DOI 10.1145/800157.805047; Karp-Lipton STOC 1980 DOI 10.1145/800141.804678; Schaefer STOC 1978 DOI 10.1145/800133.804350; Williams STOC 2024 DOI 10.1145/3618260.3649723.

## THEOREM U: UNIFORM POLY ELIMINATION IFF P=NP
Let G(X,W) be any explicit bounded-fan-in Boolean circuit of encoded size N with |X|,|W| <= N. An all-input uniform polynomial-time compiler E returning an X-only polynomial-size circuit H_G with
  FOR ALL x: H_G(x) = EXISTS w G(x,w)
exists IFF P=NP.

Forward: for each length n, compile the uniform polynomial-size universal 3SAT verifier V_n(X,W), where X encodes an n-bit 3CNF input and W its guessed satisfying assignment. The uniformly constructed H_{V_n}(X) decides 3SAT in polynomial time. Hence P=NP.
Reverse: if SAT has a deterministic polynomial-time decider A, construct the length O(N log N) pinned functional Tseitin CNF for EXISTS W G(x,W) as a uniform function of x. Unroll A on the pinned input template, hardwiring G and keeping X as the circuit inputs. The result is a polynomial-size uniformly constructible circuit H_G(X). Note this applies even if W=(I,B), the only legal selector is I=0 with |I|=1, and |B| is polynomial: a logarithmic selector does not dispose of the seed.
Quantifiers are essential: FOR ALL original x the resulting H agrees with the existential fiber, not just the final EXISTS X QBF truth value. The equivalence does not prove either P=NP or P!=NP.

## THEOREM N: NONUNIFORM POLY SIZE IFF NP SUBSET P/poly
With one fixed polynomial bound N^c for all source circuits, the existence (no efficient construction promised) of H_G(X) computing EXISTS W G(X,W) for each source G is equivalent to NP subset P/poly.
Forward: select the uniform SAT-verifier circuit V_n; the candidate-fiber circuits yield polynomial SAT circuits for each input length n. Reverse: compose a nonuniform polynomial SAT-decision circuit at the padded pinned-CNF length with a uniform x-to-CNF template for any given G. By Karp-Lipton, NP subset P/poly would collapse PH to Sigma2. Neither assumption is known.
The analogous source-dependent response program f_G(X) satisfying FOR ALL x: [EXISTS w G(x,w)] IFF G(x,f_G(x)) has the same implications by composition and SAT self-reduction. Distinguish a nonuniform EXISTS family of circuits from a uniformly constructible family.

## HYPOTHETICAL P=NP SERVICE, ALL COSTS CHARGED
Under exact SAT decision runtime O(L^d), d>=1, let q=|W|=k+b with k=O(log N), b polynomial and L=O(N log N) pinned-Tseitin-CNF bits. For candidate x first ask SAT of G(x,W); if SAT, for each of q universal bits ask SAT for prefix extended by 0 and choose 0 if possible, otherwise 1. At most q+1 solver calls, per-candidate O((q+1)(N log N)^d + poly(N)) including pinning/serialization. Under the unproved P=NP hypothesis this yields a complete candidate-dependent response.
A conservative direct time-T Turing machine to bounded-fan-in Boolean circuit simulation uses O(T^2) gates. An unrolled decision-only H_G has O((N log N)^(2d)) gates, and witness circuit O(q (N log N)^(2d)) gates. Refeeding compiled H_G to the same SAT solver can cost O(N^(2d^2) polylog N), not a decrease f(d)<d. No free UNSAT certificate or Williams-style exponent contraction is claimed.

## QUANTIFIER AUDIT
Original QBF: EXISTS X FORALL I,B NOT G(X,I,B). The valid trace form is EXISTS X FORALL I,B EXISTS T [Trace_G(X,I,B,T) AND NOT t_out]. T depends on universal inputs.
Counterexample: C(X,Y)=X OR (Y AND NOT Y), traces T1=NOT Y, T2=Y AND T1, T3=X OR T2. EXISTS X FORALL Y EXISTS T [Trace_C AND T3] TRUE (X=1); hoisted EXISTS X,T FORALL Y [Trace_C AND T3] FALSE (T1 cannot equal NOT Y for both Y).
Shared-X counterexample G(X,I,B)=[I=0] AND [B=X] for n=|X|=|B|>=1: EXISTS X FORALL I,B NOT G is FALSE, but FORALL I,B EXISTS X NOT G is TRUE. Tested for n=1,2,3,4.

## MIXED SCHAEFER OBSTRUCTION
Any normalized 3CNF clause is Horn OR dual-Horn, since a clause of width <=3 cannot contain >=2 positive AND >=2 negative literals. Hence every arbitrary 3CNF partitions into two individually tractable subformulas. The conjunction is still arbitrary 3SAT.
Explicit 3-bit counterexample: the eight distinct full-width clauses D_a, each falsified by a distinct B=a. The four Horn clauses SAT, the four dual-Horn clauses SAT, but the eight-clause union UNSAT. Exact DIMACS sizes: Horn 4 clauses / 51 bytes, dual-Horn 4 / 45 bytes, union 8 / 86 bytes. This invalidates independent subtheory satisfiability tests without a charged whole-fiber combination method. This is not a lower bound against arbitrary SAT machines.

## EXECUTED AUDIT (STANDARD-LIBRARY PYTHON, INDEPENDENT CNF VERIFIER)
Primary executable controls: 65,812 indexed-verifier candidate fibers across universal b=1..4; 2,101,392 direct candidate/selector/challenge evaluations; 328,750 finite self-reduction oracle queries; 65,808 SAT and 4 UNSAT candidate fibers; 5,116 random guarded-CNF candidate fibers; 398,592 functional gate-clause evaluations; 6 trace/common-X semantic controls; 4,100 long equality evaluations. All passed.
Independent DIMACS parser + unit-propagation/DPLL: source 4,096 pinned input cases, 1,024 SAT and 3,072 UNSAT; compiled winning 256 pinned X, exactly 1 SAT; 300 independently pinned long-seed equality cases. All passed.
Fixture b=3, X=8, selector k=1, genuine B=3: 16 universal assignments per x. Source 3CNF 44 vars / 97 clauses / 967 ASCII DIMACS bytes. Winning circuit CNF (AND of 8 existential X) 15 vars / 22 clauses / 213 bytes. Exactly X=11111111 wins.
Long-seed fixture n=20: G(X,I,B)=[I=0] AND [B=X], universal challenges per x = 2^21=2,097,152; 20-wire response f(X)=X. Source CNF 41 vars / 41 clauses / 361 bytes. No exhaustive 20-bit challenge enumeration claimed; algebraic identity, 4,100 sampled/control evaluations, and 300 pinned CNF controls only. Byte sizes are for the actual emitted DIMACS encodings.

## HANDOFF
1. A proposed all-source uniform compiler is already as strong as P=NP. A merely nonuniform general small-fiber conjecture is as strong as NP subset P/poly. Neither may be assumed to complete a Sigma2 proof.
2. Seek WHOLE-FIBER structural parameters that survive arbitrary Horn + dual Horn mixtures, nonlinear reconvergence, indexing, and restrictions; clause-local decompositions are insufficient.
3. Audit genuine long seed size, index length, candidate-common X, trace quantifier placement, source-to-target size, synthesis, certification, and all SAT queries.
4. Strictly require all-input f(d)<d before claiming iterable SAT-exponent contraction. No such contraction or P vs NP proof presently exists.

References:
[1] Cook (1971) https://doi.org/10.1145/800157.805047
[2] Karp-Lipton (1980) https://doi.org/10.1145/800141.804678
[3] Schaefer (1978) https://doi.org/10.1145/800133.804350
[4] Williams (2024) https://doi.org/10.1145/3618260.3649723

UNIFORMBARRIER28_VERIFIED_SENTINEL_20261118
