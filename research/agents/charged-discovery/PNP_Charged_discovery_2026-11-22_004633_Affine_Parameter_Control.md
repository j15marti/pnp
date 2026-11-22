# Dense affine sources defeat a compulsory factor-parameter transfer

22 November 2026, 00:46:33 PST. Charged Discovery.
**DYNAMIC-AFFINE-PARAMETER-CONTROL1**, under DYNAMIC-COMPATIBILITY-OBLIGATION1.
**PROVED/EXACT restricted bypass; FALSIFIED/RETIRED transfer from large local factor parameter to compulsory exponential decision work. COMPUTATIONAL finite checks. Independent review pending. P versus NP OPEN.**

Construction's local acquisition theorem at revision 3757eba746904cbe2983b6cbdda9f8a3bf9b0f07 is an upper bound. This run tests the distinct proposed inference that its large parameter forces costly decision work across solvers. Dense affine sources provide a both-label counterexample even with no private leaves or pure literals. This is a new test of that specific parameter. Gaussian elimination and the general affine safeguard are established methods.

## Exact family and fixed algorithm

For every d>=5 and binary vector b indexed by the q=binom(d,3) triples S of {1,...,d}, generate the equations XOR_(i in S) x_i=b_S. Encode each equation with its four proper ternary clauses excluding the wrong parity rows, in lexicographic support/assignment order. Thus c=4q, every name occurs in binom(d-1,2) original support groups, and every literal polarity appears in each parity block. No exponential table is hidden; each group has eight rows.

For Construction's precise certificate, every name on more than two original supports is compulsory in B. Hence h=d for every b. Full pinning qualifies, proving equality. This statement concerns the declared syntactic certificate, including unsatisfiable instances; global simplification could give a different parameter.

Fix A before d,b. Authenticate the canonical compiled input through extraction and exact regeneration. Group source clauses by exact unsigned support and admit only tables equal to one ternary parity relation. For admitted sources, form the augmented binary matrix and perform deterministic Gaussian elimination in increasing pivot-column order. A row operation preserves the solution set because adding one equation to another over GF(2) is invertible. An all-zero left side with right side one proves UNSAT. Otherwise choose free variables zero and back-substitute, producing a witness and proving SAT. Failed admission yields UNKNOWN internally and exhaustive decision on the retained original. This is one globally correct total solver with a polynomial admitted path.

Both labels occur for every d>=5. All-zero b is satisfied by all-zero x. Set only b_123=1 and the remaining b entries zero. XOR the four equations on 123,124,135,145: each variable appears an even number of times, while the right sides sum to one. This proves UNSAT. Both formulas have identical c,d and compiled N. No all-UNSAT promise is used.

Three falsifiers are a missing parity clause silently accepted, a right-hand-side contradiction misreported as UNKNOWN, or a restriction on A that forbids joint elimination while importing an unrestricted conclusion. Exact eight-row recognition handles the first. Elimination's contradiction test handles the second. The third is rejected by the stated model.

## Same-encoding cost and implication

Use the deterministic finite-alphabet single writable tape, one locally moving head, fixed-origin output and terminated decision of the transport report. Original input, copies, address bits and retained source count toward span. With r the least odd integer greater than c, at least three, the inherited canonical compiler has

    n0=d+(10c+1)r+2, m0=(20c+4)r,
    n=n0+m0+3, m=2m0+4, w=ceil(log2(n+1)),
    N=3n+2+2 floor(log2(m+1))+3m(w+1)+w.

The ordered stream contains unary n and delimiter, gamma(m+1), m signed width-w triples, two n-bit assignments and the w-bit release ID. N=Theta(c² log(c+1))=Theta(d^6 log d) on this family. The existential compiler equivalence and adjacent local Horn/dual-Horn witness properties retain their existing internal-review scope.

Authentication and failed candidates cost O(N³) time, O(N) span using the existing extraction/regeneration procedure. Pairwise group comparisons and exact tables cost O(c²) word operations. At most qd row additions of d+1 bits give O(qd²)<=O(c³) elementary bit operations. The matrix has q(d+1)<=O(c²) bits. Indices, row labels, retained input, copies and counters use O(c² log N)=O(N) cells under THIS expanded encoding. Every actual indexed access and binary arithmetic operation can conservatively be implemented in O(N²) transitions by shuttling. Thus T=O(N³+c³N²)=O(N^(7/2)) and S=O(N). Initialization, pivot searches, failed pivots, conversion, row sharing, relocation, recomputation, back-substitution, cleanup and origin output are included. Current matrix storage is reused. Target production, if requested separately, costs O(N³), O(N) span. Generic fallback can use O(2^n N³) time and O(N) span.

Physical CM is O(N^(9/2)) by summing span along this execution. Independently, full input plus time replay gives CM_min=O(N^(9/2)); no assumption of efficient minimum-description discovery is made. A fixed cap KN^a still entails S=O(N^a), physical CM=O(N^(2a)), descriptive CM=O(N^(a+1)) and the separate count-map circuit ceiling O(N^a log N).

Since h=d and log N=Theta(log d), h/log N is unbounded. Nevertheless the same fixed A handles every b in polynomial time. Therefore a universally compulsory 2^h or 3^h decision-demand transfer from this local parameter is false. Construction's parameterized upper bound remains valid. The missing lower-bound theorem would have to derive actual required events for every permitted solver despite paid elimination. Failure of this transfer resolves neither direction of P versus NP.

## Actual decoder boundary

Choose equal probability on the all-zero and single-flip RHS pair for a fixed d. Let U=D be the final label, B specify the public pair and A, Pi be the one bit read from a fixed origin cache after cleanup, and E be precisely that actual read transition. Conditional words 0 and 1 are prefix-free, identity decodes, b=1, framing h_j=0 and rho=1. All prefix acquisition and retention costs were paid above. The shared formula yields E T>=1. Repeating this event increases rho. Free retained-source side information makes label entropy zero. No correctness requirement forces A to enumerate all assignments to the high-incidence variables or service virtual residual queries. Accounting's residual-entropy debit applies to any stronger proposed obligation.

## Primary-source search and transfer

Two directly relevant primary results were examined.

Nishimura, Ragde and Szeider, SAT 2004, defines a strong backdoor through every assignment entering the specified base class, and establishes fixed-parameter discovery for Horn and 2-CNF. Its parameter is relative to that class. No statement turns failure of one base-class method into a lower bound against other decision algorithms. Fresh queries used “Nishimura Ragde Szeider detecting backdoor sets Horn binary clauses strong backdoor parameter algorithms pdf”. [Primary manuscript](https://www.satisfiability.org/SAT04/programme/51.pdf).

Pătraşcu and Demaine, SIAM J. Computing 35(4), 2006, theorem 2.4, proves logarithmic amortized operation lower bounds for dynamic connectivity in the cell-probe setting with logarithmic cell size, even on disjoint paths. Fresh query used “Patrascu Demaine logarithmic lower bounds cell probe dynamic connectivity disjoint paths pdf”. Its update/query interface requires answers during the operation sequence. Our single offline SAT decision has no such service or imposed deadlines. The missing transfer is a simulation that makes those answers compulsory on every solver's actual execution with bounded overhead/reuse. Our new large-h affine example gives a concrete joint-processing route that such a proposed simulation must survive. [Author-hosted paper](https://erikdemaine.org/papers/DynamicConnectivity_SICOMP/paper.pdf).

Schaefer's 1978 affine classification was also searched by title, but only bibliographic/abstract material was retrieved, so no detailed theorem is imported from that inaccessible full text. The elimination correctness needed here is proved above.

Fresh GitHub query '"Gaussian elimination" "SAT"' covered all six official scopes. xai-org and google-research returned no hits. Anthropic succeeded after 429 retry and returned cryptography-research-demo canon_even.h at fa01c398b42bb7d94eadff75a42dfb45da484457, an eight-bit GF(2) elimination excerpt. OpenAI/math returned finite.tex in the Min-UnCut preprint at 4eaee87548250b2682affda7d05d947c05554bae, involving binary elimination within a reduction. Google/or-tools returned zero_half_cuts.cc at 4782dbd0aa85621c8115cf33de1574a2e6757004. Google DeepMind/mujoco returned engine_util_solve.c at c34af663c1de1a778e2a2c73c809841eec6d2141, a numerical 3x3 routine. Only relevant search excerpts were inspected; none proves all-input SAT tractability or compulsory decoding. No code imported. Official scope checks in this session used the Anthropic/OpenAI/DeepMind GitHub profiles, x.ai/news/grok-os, Google's official organization guidance and research.google/resources. Null results express bounded coverage.

## New evidence and handoff

[Complete code](../../../experiments/dynamic_discovery_affine_parameter_20261122.py) and [raw](../../../results/raw/dynamic_discovery_affine_parameter_20261122.json). Run python experiments/dynamic_discovery_affine_parameter_20261122.py. All 1024 RHS vectors on five variables were independently checked by assignment enumeration against elimination: 32 SAT, 992 UNSAT. Eight further d=5,6,8,12 cases checked the explicit opposite-label family. Code SHA256 8800773bf24e442f482aec569c1f6105d38de21430cb0aec0daa060f3cf4aceb. The experiment tests the new certificate connection; it does not repeat Construction's cycle sweep, materialize compiled targets, or measure tape costs.

Recovered current directive, transport, AGENTS.md, CODEX.md, research skill and relevant T5 definitions, Discovery's degree-factor report/handoff, Construction's new report/code/raw and current coordination issue. Selected files only are present locally, so full-checkout preflight and LaTeX compilation were unavailable. No historical manuscript ownership acquired. Affine/Tseitin, complement, forced-domain, private-leaf and decision-witness controls remain permitted. DISJ/equality and same-execution DTISP gates pass in scope. Deterministic configuration replay is an upper bound. No relativization, Natural Proofs or algebrization barrier bypass is claimed.

**One next dependency, Construction/Discovery with Bounds and Synthesis receiving.** Prove a paid acquisition rule whose residual class includes both affine systems and degree factors, with per-branch admission and total costs, or give a counterexample to that combined rule. Mixing these constraint types in one connected residual requires a new solver proof; separate tractability does not establish tractability of their conjunction. Bounds must identify actual compulsory events surviving this expanded solver choice. P versus NP OPEN.
