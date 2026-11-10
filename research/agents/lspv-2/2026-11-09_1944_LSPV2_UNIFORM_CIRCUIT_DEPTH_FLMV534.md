# LSPV-2/534: Uniform on-demand circuits, cost-sound depth evaluation, and an FLMV structural exclusion

**2026-11-09 19:44 PST | SAT-Circuit Reduction Builder | Route A | KNOWN THEOREM consequence + PROVED/RESTRICTED evaluator + COMPUTATIONAL controls | P versus NP OPEN**

## IDEA, scope, and 4 falsifiers

Candidate: rather than posit that an assumed polynomial SAT time bound automatically compresses work space, isolate a *sufficient structural condition* for actual deterministic space reduction: on-demand, uniformly navigable, bounded-fan-in **logarithmic-depth** circuits for the complete all-input SAT/malformed decision function. Give an executable stack evaluator and use the matched native FLMV lower bound to exclude a particularly shallow SAT family.

(F1) **Unproved navigation:** an arbitrary polynomial-time deterministic decider may have polynomial-depth dependencies and need polynomial work to generate a gate, and need not yield this circuit representation. Hence the theorem is conditional on a separate, explicit **uniform navigator**. (F2) **Shared-path explosion mistaken for inherent hardness:** a two-vertex-per-layer diamond has exponentially many DFS calls but a linear-work forward memo evaluator; this is a policy-relative cost, not a computation lower bound. (F3) **Uncharged resource/machine conversion:** each input bit access, child-index lookup, return-stack manipulation, scratch and result is charged on the same indexed random-access machine. (F4) **Invalid NP or proof-system transfer:** an existential SAT witness branch is not a deterministic UNSAT decider; a large abstract configuration set or expensive proof DAG is not work space.

## Primary literature, source and model authentication

1. Fortnow, Lipton, van Melkebeek, Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, DOI 10.1145/1101821.1101822, author manuscript https://lance.fortnow.com/papers/files/tst.pdf . The deterministic indexed random-access SAT lower bound applies to **simultaneous time and space** on one machine. The conservative explicit exponent is $$\beta(c)=\frac12\left(\frac{c+2}{c^2}-c\right).$$ Its positive region is $1\le c<c_0\approx1.52138$; at $c=6/5$, $\beta=23/45$.
2. Fortnow and van Melkebeek, DIMACS 2000-06, https://archive.dimacs.rutgers.edu/TechnicalReports/abstracts/2000/2000-06.html (explicit exponent above).
3. Williams, *Inductive Time-Space Lower Bounds for SAT and Related Problems*, Computational Complexity 15, 2006/2007, https://doi.org/10.1007/s00037-007-0221-1 . Later endpoint results exclude stronger $c$ with **subpolynomial space**, but do not automatically authenticate an arbitrary numerical product bound $c+s\ge 2\cos(\pi/7)$; see LSPV-3/548.
4. Bennett, *Time/Space Trade-Offs for Reversible Computation*, SIAM J. Comput. 18(4), 1989, DOI 10.1137/0218053 . Reversible pebbling has a different target, and its $S\log T$ upper bound is not a generic simultaneous decrease of arbitrary SAT time *and* space.
5. D'Silva, Haller, Kroening, *Abstract Conflict Driven Learning*, POPL 2013, https://www.kroening.com/papers/popl2013.pdf ; *Abstract Satisfaction*, POPL 2014, https://www.kroening.com/papers/popl2014.pdf . The circuit evaluator below is a separately declared exact concrete/abstract machine class, not a completeness claim for arbitrary ACDCL operators.

**Known hard-family baseline:** on odd-charge cubic-expander Tseitin proper signed 3-CNFs, with $h$ vertices, $3h/2$ variables and $4h$ clauses, ordinary Resolution has exponential proof-size lower bounds. This is **not** an inference about the uniform depth of an arbitrary SAT circuit. Source-proven GF(2) Gaussian-elimination shortcuts remain legal; replacing a circuit by a Resolution DAG would be an invalid model conversion. The finite test corpus below intentionally includes easy proper signed 3-CNFs, *not* claimed expander hardness.

## Exact all-input uniform circuit/navigation hypothesis

For **every** binary length $N\ge N_0$, assume a fixed, input-independent **single finite deterministic native-machine program** NAV which, given $(N,u)$, returns a bounded-fan-in two-input Boolean gate's kind, earlier child identifiers or a read-only original-input bit address; also returns the two designated output roots for the three-label SAT/UNSAT/malformed classifier. The complete reachable circuit $C_N$ is acyclic, has $G(N)\le N^g$ nodes with $O(\log N)$-bit IDs for a fixed $g$, has fan-in at most two and maximum root-to-input depth

$$
D(N)\le\lfloor \delta\log_2 N\rfloor.
$$

The navigator, including parsing its own parameter records, retrieving gate descriptions, accessing input bits, scratch reset, and returning control, runs in $O(\log^a N)$ **native** indexed-machine steps and $O(\log^b N)$ native indexed work-space high-water, uniformly for **all gate calls**, for fixed finite $a,b$. NAV may not use the SAT label as a semantic oracle, input-specific precomputed truth table, advice or nonuniform hardcoded circuits. Its two root bits distinguish SAT, UNSAT and malformed on **every** binary input, not merely a promised original CNF subclass.

This hypothesis is MUCH stronger than a hypothetical deterministic $A_P$ with $T_P(N)=O(N^c\operatorname{polylog}N)$. Neither $c$ nor $\delta$ is assumed to equal $6/5$ for an arbitrary polynomial SAT algorithm.

## Exact simulator and all-phase resource certificate

EVAL recursively evaluates a gate by requesting its descriptor from NAV, recursively evaluating each predecessor, retaining one child result when evaluating the second, and returning the Boolean result. The call stack explicitly stores every ancestor gate ID, phase and partial truth value. The read-only binary source remains unchanged and is not counted as writable work memory.

Complete concrete states include $(M,x,N)$, input/output heads and label, NAV program counter and scratch, index tape and head, main work tapes and heads, gate call/return stack, current gate, first-child result, deterministic phase, cumulative native time, maximum indexed work address, simultaneous live work storage and peak live storage. An ordinary NP verifier $A_{NP}$ instead has a *separate choice/certificate interface*, accepting on at least one legal SAT branch and accepting on **none** for UNSAT. It is not substituted for EVAL's deterministic all-label machine.

For the declared EVAL implementation, $\iota$ converts a concrete native evaluator state into its entire exact explicit stack/guest/control/read/index/counter record; for any set $X$ of states set $\alpha(X)=\{\iota(\sigma):\sigma\in X\}$ and $\gamma(Y)=\{\sigma:\iota(\sigma)\in Y\}$. With full records, transitions correspond exactly:
$$
\iota(\operatorname{Post}(\sigma))=\operatorname{Post}_{\rm eval}(\iota(\sigma)).
$$
The may collecting transformer $\operatorname{Post}^{\#}=\alpha\circ\operatorname{Post}\circ\gamma$ overapproximates every declared legal step. Any coarser resource abstraction must charge **lower abstract path costs** for negative proof nonreachability and valid **upper all-phase peaks** for implementation feasibility; merely counting represented configurations, candidate subcalls or shared gate nodes proves neither actual machine-space bound. The exact schematic transformer is not itself an efficiently computed SAT algorithm.

For a recursive call at depth $D$, the stack holds $O(D\log G)$ bits; at most one NAV frame and a constant number of return values are live. Using contiguous indexed addresses, the fully charged native peak is
$$
S_{\rm eval}(N)=O(D\log G+\log^bN)=O(\operatorname{polylog}N).
$$
The full binary recursion tree has at most $2^{D+1}-1$ visits, **including repeated shared gates**, so even without caching,
$$
T_{\rm eval}(N)=O(2^D\operatorname{polylog}N)=O(N^{\delta}\operatorname{polylog}N).
$$
The overhead absorbs input bit reads, NAV invocation, index preparation, gate lookup, stack push/pop, output encoding, scratch reset, and the two output roots. The same contiguous-work indexed machine can implement all of these within the assumed polylog per-call bound, without an unproved cross-model exponent conversion.

**FLMV corollary (KNOWN THEOREM consequence, not a new unconditional lower bound):** If $1\le\delta<c_0$ and the above all-input circuit and native NAV exist for SAT, then a fixed deterministic SAT decider has time $N^{\delta+o(1)}$ and work space $N^{o(1)}$. Taking any constant $0<s<\beta(\delta)$ contradicts the cited deterministic FLMV tradeoff. In particular **there is no such family with $D(N)\le(6/5)\log_2 N$** and polylog native navigation. This excludes only the precisely defined *uniform shallow-navigable circuit architecture*. It cannot exclude general SAT circuits, nonuniform depth-$O(\log N)$ families, polynomial-depth succinct circuits or a hypothetical $A_P$ with unknown $c$.

## Explicit sharing/recomputation falsifier

Let diamond $D_d$ have inputs $u_0,v_0$ and for $i=1,\ldots,d$ let
$$
u_i=u_{i-1}\wedge v_{i-1},\qquad v_i=u_{i-1}\vee v_{i-1}.
$$
It has only $2d+2$ distinct nodes and depth $d$. The stipulated no-memoization DFS of $u_d$ performs **exactly** $2^{d+1}-1$ node visits, with a peak of $d+1$ call frames. In contrast, a forward topological evaluator computes both outputs at each stage, storing two live bits plus indices, in $O(d)$ gate operations and $O(\log d)$-bit counters. Hence path multiplicity is a property of the selected evaluator, not a lower bound on the function's intrinsic time or memory. Known algebraic optimization may simplify this particular easy family further.

## Independently replayed computational controls

Two independent implementations (Python and Node.js) agree on **256 original proper signed width-three 3-CNF sources**, defined by 24 source sign bits for eight clauses on three distinct variables: **254 SAT, 2 UNSAT** under independent complete 8-assignment truth-table enumeration. They also agree on all **four SHA-256 source fingerprints** (first, second, third and last fixture), and each rejects six malformed sign encodings. Both perform **1,176** assertion groups. The GitHub-published Node.js source was fetched and reexecuted in an independent V8 runtime, passing **1,176 semantic checks**, with cryptographic hashing deliberately stubbed there. The independent local Python/Node tests used genuine SHA-256.

For all diamond depths $1\le d\le16$ and four input pairs, recursive and memoizing evaluators return identical results; visits match $2^{d+1}-1$ and peaks $d+1$. At $d=16$, exactly **131,071** DFS visits and **17** frames occur for a circuit with **34** distinct nodes. This validates executable policies, not an all-input SAT circuit family or native FLMV simulator.

Original/source data and raw: `results/raw/arc/2026-11-09_1944_LSPV2_534_UNIFORM_DFS_RAW.json`. Published verifier: `experiments/arc/lspv2_534_uniform_circuit_dfs_independent.mjs` (blob `7dec182d539182311db9088e9df05051f72d7243`). Independent local Python/Node reproducer is retained in the current-run archive. No randomness; test generator deterministic.

## Assumed-time exponent and numerical controls

For hypothetical fixed uniform deterministic $A_P$ with *assumed* all-input $T_P(N)=O(N^c\operatorname{polylog}N)$, no small-space upper follows without NAV or some other proved compression. FLMV instead requires an eventual space exponent not below its positive lower-threshold $\beta(c)$ on the matched model. $A_{NP}$ has existential acceptance and does not provide deterministic UNSAT. At $c=6/5$:
$$
\beta(6/5)=23/45,\qquad\beta(6/5)-1/2=1/90.
$$

| Input length | $N^{6/5}$ exponent-only | $N^{23/45}$ exponent-only | $N^{1/2}$ exponent-only | ratio $N^{1/90}$ |
| --- | --- | --- | --- | --- |
| $10^6$ | $10^{7.2}$ | $10^{3.066667}$ | $10^3$ | 1.16591 |
| $10^{12}$ | $10^{14.4}$ | $10^{6.133333}$ | $10^6$ | 1.35936 |
| $10^{24}$ | $10^{28.8}$ | $10^{12.266667}$ | $10^{12}$ | 1.84785 |
| $10^{60}$ | $10^{72}$ | $10^{30.666667}$ | $10^{30}$ | 4.64159 |

These are **symbolic exponent-only comparisons**, not actual bytes, memory cells, physical storage, run times or finite-$N$ contradictory measurements. Constants, polylogs, fixed programs and sufficiently-large-$N$ thresholds matter.

## Corpus reviewed, duplicate/contradiction and transfer audit

Governing 2026-11-09 16:24 handoff SHA `644b0d4745f2edeb8718c7e536a7da995b36b36f`; older abstract-negative handoff; AGENTS.md; CODEX.md; repo skill; both entire root proof trackers; issue #3; earlier LSPV-2/532 and /533; LSPV-1/551's coNP-verifier firewall; LSPV-3/548's Williams quantifier audit; LSPV-3/373's **proof-DAG** depth lower bound (distinct from evaluator circuit depth); relevant Grok 2026-11-09 progress and MODELBRIDGE-0010. The /0010 generic static fixed-exponent normalizer remains **FALSIFIED/RETIRED**. Mandatory external repository source reads: konard/p-vs-np README (finite-machine, explicitly not all conventional models); blkph0x/p-vs-np-proof-research README (restricted results, P-vs-NP open). No external repository supplies the demanded NAV from arbitrary $A_P$.

**What changed relative to root main:** explicit narrow criterion for a fully costed on-demand circuit evaluation, a direct FLMV-derived *negative theorem for its shallow uniformly navigable SAT subclass*, and independent shared-DAG DFS/forward countercontrols. This is not an independent proof of any unrestricted SAT lower bound and does not improve FLMV. The project already knew sparse normalization (/533) and mixed-proof balanced depth (/373); those do **not** imply this NAV hypothesis. Transfer classification: FLMV to the **declared, same-machine** EVAL is a THEOREM TRANSFER; generic pebbling/reversible arguments are an ANALOGY unless hypotheses match; automatic compilation of $A_P$ into shallow NAV is a FAILED/UNPROVED TRANSFER.

## Proof node/status implications and next target

The conditional-circuit obstruction is **PROVED/RESTRICTED as a corollary of a KNOWN THEOREM**; finite controls are COMPUTATIONAL. [P1-01], [P1-03], [P1-04], [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2] and same-$R$ B3 remain **OPEN**. [P2-A1] is a theorem/model audit and [P2-A3] remains conditional arithmetic.

**Next:** search for an effective uniform all-input (A_P\to C_N\) representation with a *provable* navigator and a **strict joint time-and-space improvement** despite polynomial-depth dependencies; charge the NAV construction itself, every call, caching, recomputation and native peak. Such a representation is precisely the missing load-bearing arrow, not an assumption available from SAT in P. Do not edit any automations, historical R_mix341 grammar/weights or peers' owned regions. **P versus NP remains OPEN.**
