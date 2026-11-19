# Strict-C lead run 2: rank-minor and explicit-row volume firewall
2026-11-19, America/Los_Angeles. P versus NP OPEN. Independent proof-lead synthesis.

## New theorem (PROVED; all finite-domain clause-minimal UNSAT CSPs)
Let F(z,x_1,...,x_B)=AND_{j=1}^B F_j(z,x_j) be physically clause-minimal UNSAT, with pairwise disjoint x_j and each nonempty block containing at least one original clause. Fix finite alphabet A, |A|=d, and define D(z,j)=1 iff NO assignment to x_j satisfies F_j(z,x_j). For each j pick any physical clause e in F_j and a complete witness w to F without e. At z_j=w|_z, each other block F_i has its private witness, hence D(z_j,i)=0 for i!=j. Original F is UNSAT, hence D(z_j,j)=1. Thus the submatrix (D(z_j,i))_{j,i} is the B x B identity. This is valid even when the selector j(z) is dynamically computed. Consequences: (i) rank_K D=B over EVERY field K; (ii) all z_j are distinct, so B<=d^{|z|}; (iii) |z|>=ceil(log_d B). Existence of full rank does NOT show that discovering a blocker is difficult: an easy strict-C family has the same identity minor.

## New corollary (PROVED under an explicit-row interpretation; NOT for general symbolic rows)
If R is the actual number of all explicitly represented shared assignments z (R=d^{|z|}), then B<=R. With all N named variables equal to z union disjoint private blocks, |x_j|<=N^.35, R<=N^.195, we get N=|z|+sum|x_j| <= .195 log_d N+N^.545, impossible for all sufficiently large N. No input padding or unused variables is allowed in this variable-count interpretation. For bit-encoded length L, the same volume contradiction applies to balanced bounded-occurrence sources having Omega(L/polylog L) actual variables. If 'rows' are symbolic cells rather than all z values, NONE of this bounds their number R; dynamic symbolic selection may compress exponentially many z and remains OPEN. This is stronger than the archived fixed-block-row R>=B claim only for fully explicit rows.

## Original strict-C control and executed finite falsification
Canonical R(a,b) iff (b-a) mod5 in {1,3}; C(a,b,c) is a directed 3-cycle. All 125 triples checked: 30 true. Independent quadratic check Q(a,b,c) iff (a-b)^2+(b-c)^2+(c-a)^2 == 1 (mod5) agrees 125/125. 25/25 head-pair projections satisfy EXISTS_h C(h,u,v) iff u!=v.

Graph G_k: k K6-minus-terminal-edge equality wires in series, terminals t_0,...,t_k, 4 new internal vertices per wire, and final edge t_0 t_k. V_G=5k+1, E_G=14k+1. Each graph edge e={u,v} becomes C(h_e,u,v) with its own private head. The source has N=19k+2 variables, M=14k+1 original physical C clauses. Every edge deletion is 5-colorable, and the full graph is not, so the C source is physical-clause-minimal UNSAT. Its incidence girth is 6, not growing.

Deterministic no-random-seed Python run verified ALL physical C-clause deletions for k=1,2,3: 15,29,43 witnesses; 210+812+1806=2,828 retained original-C checks; 87 separately falsified deleted clauses; an independent GF(5) polynomial check agrees on every original C evaluation. DFS recursion calls charged in program: 90,1,629,40,500 (finite data, no asymptotic guarantee). All 87 blocker rows form a source-indexed identity minor, hence rank B over any field. For k=1, enumerated every 5^6=15,625 shared colorings, with 1,800 having exactly one refutable edge (120 per edge), 15,625/15,625 covered by deterministic first-hit selector; 73,725 original-edge comparisons; independently Gaussian-eliminated the full 15,625-by-15 Boolean blocking matrix over GF2 and GF5, obtaining rank 15 in both. The selector is cheap despite full obstruction rank.

Script and complete original-C source/witness ledgers are in reproducibility archive T5C_Lead_Rank_Explicit_Row_Firewall_20261119.zip, produced in this run. Source SHA256 is recorded in SHA256SUMS; no random seed.

## Single strongest bridge to unrestricted complexity
Prior source-local 3-CNF -> strict-C compiler (proof role, 2026-11-19_LOCAL3COL_C_SOURCE_ACCESS_RESOURCE_FIREWALL.md) gives 15+9v+39m named variables and 10+7v+31m physical C clauses, with O(log(v+m)) auxiliary indexing for fixed-width 3-CNF. Williams (2006), Theorem 2.1 and Corollary 2.3, provides quasi-linear, locally indexable SAT reductions; Buss-Williams (2015), Figures 8.2/8.3, proves deterministic random-access SAT NOT in DTISP(n^1.34070,n^.5). Hence a uniform, fully correct unrestricted strict-C decider at (N^1.33+o(1),N^.5+o(1)) is precluded if the precise random-access encoding simulation is maintained. A sound deterministic UNSAT-only specialist guaranteed on EVERY UNSAT input and bounded on the successful polarity also gives a total decider by clocking; likewise SAT-witness-only. This does not transfer to critical/high-girth/low-row promised C instances without a near-linear locally accessible promise compiler. No such compiler is currently established.

Full sequential explicit-row scan with R<=N^.195, B<=N^.65, block m<=N^.35 and local complete child time m^a costs N^{.845+.35a+o(1)} plus potentially N^1.195 source/materialization and all verification/output. Necessary a<=97/70 for a 1.33 exponent *under that scan*. Writable child exponent s<=10/7 is necessary for N^.5 space and does not include indexing, buffers, failed children, both polarities or replay. Dynamic symbolic rows require separate fully charged analysis, no free polarity or oracle.

## Lead disposition
PROVED: universal identity minor and full-column-rank; B<=5^|z|; conditional explicit row-volume impossibility.
COMPUTATIONAL: 87 complete source C deletion witnesses; 15,625 all-z K6 selector scans; GF2/GF5 ranks 15.
FALSIFIED: rank B, high counts of indispensable blocks, or many refutable rows alone implies hard blocker acquisition.
OPEN: construct source-uniform resource-preserving arbitrary-SAT reduction into the exact critical/growing-incidence-girth/low-row promise; or prove unconditional superpolynomial lower bounds for unrestricted strict-C. Prior S->C gadget physical criticality can FAIL, so all promise proofs must audit physical C deletion witnesses.

## References and read sources
[1] Buss & Williams (2015) https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf (Figures 8.2/8.3).
[2] Williams (2006) https://www.cs.cmu.edu/~ryanw/sat-journal-final.pdf (Theorem 2.1, Corollary 2.3).
[3] Prior local compiler https://github.com/j15marti/pnp/blob/main/research/agents/proof/2026-11-19_LOCAL3COL_C_SOURCE_ACCESS_RESOURCE_FIREWALL.md
[4] Prior red-team physical criticality failure https://github.com/j15marti/pnp/blob/main/research/agents/redteam-new/2026-11-19_STRICT_C_S_GADGET_CRITICALITY_COUNTEREXAMPLE.md
[5] User t5_strict_research.pdf, Library id libfile_e7c9904498148191bd1ab8141abc7a49, pages 1-4 inspected; research ZIP not recovered.
No other agent states, schedules, or existing manuscripts modified.