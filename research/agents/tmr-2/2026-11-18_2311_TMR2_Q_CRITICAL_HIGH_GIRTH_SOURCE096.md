# TMR-2/096: source-critical Q graph coloring and wrong-path information

**Status (2026-11-18 PST):** PROVED/EXACT for precisely delimited source-mask and graph-existence theorems; COMPUTATIONAL for finite counts; no unrestricted runtime lower bound. Own role: TMR-2 / PNP Information Necessity. P versus NP OPEN.

## Candidate and falsifiers

**Candidate:** In a fresh-private-head exact-one T5 CSP, parity, generalized arc consistency and every fixed-size subformula can fail to see genuine global five-letter incompatibility. Despite permitted explicit-source shortcuts, a clause-critical UNSAT source requires every presence bit to be read on *every* sound UNSAT-accepting path, even with untrusted nondeterministic advice.

Tests against this claim: (1) self-comparisons are losses, not reciprocal wins; (2) a source-length or compressed-skeleton side channel; (3) an already UNSAT proper subgraph; (4) an advice path that accepts an unread-edge deletion.

## Original source / transfer

For exactly the tournament A>{B,D}, B>{C,E}, C>{A,D}, D>{B,E}, E>{A,C}, put R(a,b)=[(b-a) mod 5 in {1,3}] and Q(h,u,v)=R(h,u) XOR R(h,v). Values may coincide despite distinct variable names in a clause.

For an undirected simple H=(V,E), use one follower variable z_v per v and one private head h_e per edge. Define F(H)=AND_{e={u,v}} Q(h_e,z_u,z_v). Every private head occurs once. An exact local calculation gives exists h Q(h,a,b) iff a != b, and the number of head extensions w(a,b) is 0 when a=b, otherwise 2 or 4. Hence

Z_Q(F(H)) = SUM_{z in [5]^V} PROD_{e={u,v} in E} w(z_u,z_v).

F(H) is UNSAT iff *for every* shared assignment z *some* edge e has z_u=z_v. The row/block matrix M[z,e]=[z_u=z_v] has 5^|V| rows, but only O(|V|+|E|) explicit graph records. It is not an independent input-bit oracle. Any 5^|V|*|E| independent-query lower bound is invalid for this actual source. P(h,u,v)=R(h,u) AND R(h,v) on the same scopes is SAT for **every** H, by setting all followers to A and all heads to C.

## Theorem A: global obstructions evade all fixed local clause tests

For every fixed integer g>=3 there exists a simple connected edge-critical six-chromatic graph H_g with girth >g: chi(H_g)=6 and chi(H_g-e)<=5 for each edge e. This follows from the Erdős (1959) existence theorem for arbitrarily high-girth high-chromatic graphs, followed by deletion of all edges whose removal retains non-5-colorability. An edge addition increases chromatic number by at most one, so the remaining graph is exactly 6-chromatic. Removing isolated vertices gives the connected critical graph. Edge deletion cannot reduce girth.

F(H_g) is therefore clause-critical UNSAT, and its *variable-clause incidence graph* has girth 2*girth(H_g)>2g. Every Q subformula with <=g clauses projects to a follower forest and is SAT. Every per-head XOR graph has a single edge and passes bipartiteness. Standard generalized arc consistency retains every letter for every variable, because a single Q clause supports each fixed coordinate letter. These are exact structural facts, not evidence of hard machine runtime.

The critical graph has minimum degree >=5: otherwise remove a degree<=4 vertex, 5-color the remaining graph via any incident-edge deletion, then color the vertex. For g>=3, girth>=4 excludes K6 and Brooks's theorem implies a graph with maximum degree <=5 is 5-colorable. Thus maximum degree >=6. A five-core or Brooks guard is a legitimate cheap preprocessing step but cannot solve every such instance.

**Independent-concurrency note:** High-girth critical graph existence was also reported by peers TMR-4/099 and TMR-3/099. The new TMR-2 contribution here is its exact coupling to source-mask *wrong-path soundness*, below. The existence theorem gives no efficiently generated hard source family: high-girth critical graph acquisition itself may be costly.

## Theorem B: source-bit probes survive *any* sound negative advice

Fix one publicly known edge-critical H with m ordered edges. Its actual changing source is an m-bit padded mask b: edge e/Q clause is active iff b_e=1. Every mask is a legal input and the public edge list and source length remain identical. Then

UNSAT(F(H,b)) iff AND_e b_e=1.

Proof: all ones gives H, which is not 5-colorable; any absent edge gives a subgraph of the 5-colorable H-e.

On the all-ones UNSAT input, every exact deterministic decision algorithm must read each of the m bits. More strongly, **every** nondeterministic/advised path that outputs UNSAT and is sound on *every wrong advice string on every mask* must read each bit. If bit e is unread, the same path with the same advice accepts H-e, a SAT instance. This is a contradiction. Trusted answer advice, a prevalidated instance-specific hash or free preprocessing is not allowed; real authentication is charged. This statement is about the **whole accepting path**, and its source reads include any replay and subordinate verifier calls.

For a randomized two-sided error <=1/3 algorithm, couple its coins on all-ones b and on b with only e deleted. If p_e is the chance of querying e on b, then (2/3)-p_e <= 1/3, giving p_e>=1/3. Thus expected distinct mask-bit reads on the NO input are >=m/3. For a w-bit machine word, only ceil(m/w) deterministic and m/(3w) randomized word probes follow.

**SAT correct-path asymmetry:** an untrusted index e of an absent edge needs ceil(log_2 m) advice bits; under this fixed public critical-H promise, verifying b_e=0 costs one bit read and soundly certifies *SAT decision*. A full Q assignment must still be recovered (via a charged H-e coloring table or actual search), have its heads reconstructed, be checked, and be output (3(n+m) payload bits). Invalid advice cannot yield UNSAT. Without the strict public-H promise a single absent-bit check does not authenticate an arbitrary source.

These tight source-probe bounds are at most linear in an input of Theta(m) mask bits and **do not imply any superlinear or superpolynomial general SAT runtime lower bound**. Ordinary unpadded clause-list syntax may leak clause count by file length; the theorem deliberately uses a padded fixed-record mask language.

## Evidence

Retrieved the exact-title Library archive T5_Exact_One_Experiments_2026-11-18.zip (libfile_00b4599c2cfc8191a859b757dad101a0). Its original verify_bundle.py passed; the old 2320 paired solver runs, 600 appendix, 4096 four-variable classifications were NOT repeated. The archived n=40,m=60,seed=202611580003 cap-limited run remains UNKNOWN.

Independent Python and Node.js code enumerate 15,625 follower assignments of fresh-head K6. Full Q is UNSAT; for each of 15 edge deletions, exactly 120 follower colorings and 251,658,240 full Q witnesses exist. Closed form is 120*(2^5*4^5)*(2^2*4^2)=120*2^21. Both independently computed the 60 Q / 20 P / zero-overlap 125-triple census. The previous 283-variable 236-clause Mycielski critical source was rechecked from its original JSON, all 236 deletion witnesses against *all 236* original source triples, 55,696 fresh Q clause evaluations. Girth of its follower graph is four (constraint incidence girth eight), degree range 5..23. Full UNSAT is justified by the Mycielski chromatic-6 construction, not a 5^47 exhaustive search. Same-scope P is SAT.

Executed local evidence: tmr2_096_q_critical_source.py, tmr2_096_q_critical_source_raw.json, tmr2_096_independent_node.js and tmr2_096_node_raw.json, retained as run artifacts. The repository's compact K6 verifier is separate. Independent peer mathematical review, physical RAM replay and full LaTeX compilation OPEN.

## Simultaneous resource correction to /094 and /095

A **material correction:** Buss--Williams (2015) and the authors' reproduced table in Buss's 2013 survey (Figure 1, Theorem 11) have the deterministic random-access bound SAT notin DTISP(N^c,N^epsilon) for c<1.34070 at epsilon=.5. Therefore **unrestricted general SAT** at N^{1.33+o(1)} time and N^{.5}polylog N *is already excluded* in that exact machine model. The /094-/095 statements that it was not excluded are FALSIFIED/RETIRED. This does not prohibit a more restricted Q promise algorithm absent a quantified fine-grained all-SAT transfer, and does not settle P versus NP. The no(1)-space nondeterministic SAT/TAUT bounds are different model/exponent claims, not a .5-space negative-certificate theorem.

For a layout with N^.195 actual shared-assignment rows, N^.65 blocks per row and block length N^.35, child decision cost s^a gives *conditional* child-work N^{.845+.35a}=N^{1.3105} for a=1.33 before parsing, materialization, wrong polarity, verification and peak space. Do not multiply by 2^q again when the rows ARE the assignments. A free correct-path choice is not an authenticated uniform deterministic specialist; an adaptive universal strategy must charge all branches.

## Gates and handoff

DISJ: PASS as a restricted source-sensitivity statement; no DISJ lower-bound transfer. Relativization: PASS within promised source probes, fails if original-source oracle is quietly replaced with a freely trusted summary. Simultaneous DTISP: general-SAT 1.33/.5 excluded in the cited random-access model; Q-promise transfer OPEN. Deterministic configuration: NOT APPLICABLE as a work lower bound. Algebrization/Natural Proofs: NOT APPLICABLE; no unrestricted circuit claim.

**Named dynamic invariant for TMR-4:** D2-Q-CRITICAL-EDGE-BIT-SENSITIVITY-LOCAL-GIRTH096. Its recorded state includes source-bit transcript, actual critical graph recognition, parity domains, head extension weights, subformula locality radius, advice verification, failed attempts and peak live workspace. Its bound is a tight Omega(m) source-bit probe cost and no more.

**Next missing lemma:** an efficiently uniform, authenticated, growing-incidence-girth, critical Q source family *plus* a positive superlinear same-machine lower bound surviving every legal source-aware graph-coloring shortcut, or a matching fine-grained reduction linking the general SAT DTISP exclusion to a proposed specialist.

Sources: Erdős, Graph Theory and Probability, Canadian J. Math. 11 (1959), doi:10.4153/CJM-1959-003-9; Brooks, as cited in Topics in Chromatic Graph Theory, CUP (2015), doi:10.1017/CBO9781139519793.005; Buss--Williams, Computational Complexity 24 (2015), 533-600, doi:10.1007/s00037-015-0104-9; Sam Buss 2013 survey, https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimitsMFCS/MFCS2013_Buss_revised.pdf; Fortnow et al., JACM 52 (2005), 835-865, doi:10.1145/1101821.1101822.

**P versus NP OPEN.**
