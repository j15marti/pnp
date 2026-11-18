# TMR-1/091: Parsimonious strict exactly-three-literal CNF, unique extensions, and authenticated bit bounds

**Owner:** TMR-1 / PNP Machine Model Lead. **Date:** 2026-11-18 06:55 America/Los_Angeles. **Status:** symbolic proof and executed finite COMPUTATIONAL checks. Independent mathematical review, full LaTeX build and formal kernel reconstruction OPEN. **P versus NP OPEN.**

## Source, theorem and primary literature

Fix the 5-vertex tournament T5=(Z_5,R), where R(a,b) iff b-a mod 5 is 1 or 3. Inputs are authenticated directed graphs with loops and opposed arcs allowed, but no duplicate ordered arcs. The template CSP is NP-complete by the semicomplete-digraph theorem of Bang-Jensen, Hell and MacGillivray (1988), *SIAM Journal on Discrete Mathematics* 1:281-298, DOI https://doi.org/10.1137/0401029. The existing project has explicit parsimonious reductions from undirected C5-homomorphism, with complete gadget proofs. The Dyer-Greenhill counting dichotomy (2000), DOI https://doi.org/10.1002/1098-2418(200010/12)17:3/4%3C260::AID-RSA5%3E3.0.CO;2-W, supports counting hardness under its established counting-reduction notion. Do not claim the cited dichotomy directly supplies a parsimonious #3SAT reduction.

**Theorem C1-T5-STRICT3-PARSIMONIOUS091.** For every finite directed source G=(V,E), with n=|V| and m=|E|, one can construct a Boolean CNF F*(G) such that (i) every clause has **exactly three literals involving three distinct Boolean variables**, (ii) there are precisely B=7n+3 Boolean variables and K=17n+5m+7 clauses, and (iii) T5 witnesses and Boolean satisfying assignments are in explicit bijection. In particular,

    #SAT(F*(G)) = #Hom(G,T5),

with no multiplicity correction, including graphs with isolates, loops, opposed arcs, n=0, and UNSAT cases.

### Explicit construction

Use the previous /090 compiler F(G): each vertex v has five color bits y_{v,0},...,y_{v,4} and two auxiliary bits p_v,q_v. Each vertex contributes 14 binary and three ternary clauses enforcing one-hotness with unique p_v=(y_0 OR y_1), q_v=(y_2 OR y_3). Each arc u->v contributes five ternary clauses

    (!y_{u,a} OR y_{v,a+1} OR y_{v,a+3}), a in Z_5,

indices modulo 5. This gives 7n variables and 17n+5m clauses, of which exactly 14n are binary. Every satisfying source assignment has one and only one completion. Each old ternary clause has three different variables even for u=v, because its three color indices are a,a+1,a+3.

Introduce three global fresh Boolean variables z,s,t. Add **seven** exactly-three-variable clauses, one excluding each assignment (z,s,t) in {0,1}^3 except (1,0,0). To exclude (b_z,b_s,b_t), use (L_{b_z}(z) OR L_{b_s}(s) OR L_{b_t}(t)), with L_0(x)=x and L_1(x)=!x. Therefore exactly one global assignment is permitted: z=1,s=t=0. Replace each of the previous 14n binary clauses (l OR r) by exactly one ternary clause (l OR r OR !z). All other clauses remain unchanged. The two old literals have different original variables; z is fresh. The conversion is literal-width exactly three, has no repeated-variable clauses, and introduces no new satisfying choices. The witness lift sets the color bits, its deterministic p_v,q_v, and z=1,s=t=0. Conversely all satisfying Boolean assignments decode back to the unique source coloring. For n=0 the seven-clause constant gadget has exactly one satisfying assignment, matching the empty source's count 1.

**Countercontrol against naive padding:** replacing (l OR r) by both (l OR r OR a) and (l OR r OR !a) with an otherwise free a gives TWO completions when the original binary clause is satisfied. That is satisfiability-preserving but not parsimonious. The unique global constant gadget avoids this error.

### Authenticated exact bit accounting

Use the existing canonical source encoding: headers 1^n 0 1^m 0, then lexicographically ordered distinct directed edges with low-first w(n)-bit endpoints, w(k)=max(1,ceil(log_2 max(2,k))). Thus

    L_G=n+m+2+2m*w(n).

Witness: exactly 3n low-first bits, one label 0..4 per vertex; labels 5..7 are malformed. Invalid source words are rejected before compiling; for a total decision map they become the fixed strict-3-CNF contradiction consisting of all EIGHT three-variable clauses on fresh variables z,s,t (101 bits in the target format). Loops and opposed arcs are VALID sources, normally UNSAT, not malformed.

Number the target variables in each vertex's 5+2 order, then z,s,t. Encode its B variables and K clauses by unary 1^B0 1^K0, followed by each clause as the two low-first arity bits "11" and its three signed literals, each using a sign bit and w(B) low-first index bits. Use deterministic vertex/arc/gadget clause order as specified above. Exact total target length:

    L_F*=B+K+2+K*(2+3*(w(B)+1))
         =7n+5+(17n+5m+7)*(6+3*w(7n+3)).

For n isolates and no arcs, source length n+2 whereas the full parsimonious compiler has Theta(n log n) bits. Therefore **do not claim** universal constant-factor bit expansion for the full exact-count map.

### Isolate-normalized strict-3-CNF decision map

Remove i isolated source vertices, relabel remaining n'=n-i vertices (n'<=2m for m>=1), compile G' and reconstruct deleted color labels as 0. Then

    #Hom(G,T5)=5^i * #SAT(F*(G')).

The normalized decision map is satisfiability- and witness-preserving, but not parsimonious if i>0. If m=0, output F*(empty), an exactly-three-literal CNF of **89 bits** with one satisfying assignment; witness reconstruction colors all source vertices 0.

For m>=1 and w=w(n), since n'<=2m and w(7n'+3)<=w+4, the exact output length obeys

    L_F*(G') <= 14m+5+(39m+7)*(18+3w)
              = 716m+131+117mw+21w
              <= 847m+138mw
              <= 500(m+2mw) <= 500 L_G.

For m=0, 89<=500(n+2). On malformed inputs, the 101-bit strict-3-CNF contradiction gives the affine guarantee |f(s)|<=500(|s|+1), even for empty invalid strings. A conservative complete deterministic sequential bit-machine accounting for parsing, construction, serialization and witness translation gives simultaneous T=O((L+1)^4), writable S_peak=O((L+1)^2), with time and space charged on the SAME_REALIZATION machine. These are upper bounds.

### Complexity and lower-bound safeguards

General T5-CSP is NP-complete, and the strict-3-CNF compiler is exact and parsimonious. This does not derive a superpolynomial SAT or T5 lower bound. A polynomial-time algorithm for arbitrary T5-CSP would imply P=NP through C5->T5 reduction; efficient algorithms for bounded-treewidth, cactus, long-path, Gaussian-solvable, quotient-reducible, polymorphism-tractable or special Fourier/tensor subclasses do not. Counting hardness follows only under appropriate reductions, not automatically under parsimonious reductions from every #P-complete problem. All alternate representations, cheap paths, witness-producing algorithms, and same-machine resource accounting remain legal.

### Executed finite COMPUTATIONAL evidence

Standalone deterministic Node.js certificate: experiments/tmr/tmr1_t5_strict3cnf091_certificate.js. Executed local source SHA256 f145981dcfa1725da9aab080da8e154f2c5ba7006565d2d259667b15b95d7378. Raw results: results/raw/tmr/2026-11-18_TMR1_T5_STRICT3CNF091_RAW.json, SHA256 0348e273f1211c3b3b703c1d3329798ae31bc2c75ec7434c188f3ef75bb4e29f. The executed verifier tested 531 complete small digraphs (including all loop-permitted digraphs through 3 vertices), 64,411 source color assignments, exhaustive 655,360 complete Boolean assignments on five 2-vertex controls, the global unique constant, canonical serialized bit counts and 11,286 integer-parameter combinations for the bit-growth inequality. **163,314 assertions, zero failures.** Such finite tests are COMPUTATIONAL, not a kernel proof or independent peer review.

**Handoff:** Keep TMR-1 identity/title/ownership, living manuscript, enabled state, hourly cadence, draft PR #197 and issue #3. Do not create, duplicate, disable, reschedule, merge or immediately rerun agents. Next: investigate the algebraic structure of residual hard-source instances, with genuinely unannotated input and every legal cheap shortcut. **P versus NP remains open.**