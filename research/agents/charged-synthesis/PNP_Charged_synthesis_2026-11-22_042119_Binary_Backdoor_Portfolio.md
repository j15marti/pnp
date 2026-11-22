# Paid binary admission and backdoor composition

22 November 2026, 04:21:19 PST. PNP Charged Proof Synthesis. **DYNAMIC-BINARY-BACKDOOR-COMPOSITION1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1.

**PROVED/EXACT** symbolic decision composition, conditional on the pinned compiler and authentication implementation tariffs at the physical-machine level. The new composition has not received independent adversarial review or been executed as an integrated solver. Existing binary decisive-return semantics have Redteam's internal reconstruction support. This is no claim of external independent verification. P versus NP remains **OPEN**.

## Five-peer integration

| Pinned source | Result incorporated and limit |
|---|---|
| [Construction](https://github.com/j15marti/pnp/blob/6dc52153d4e0c60fa778a44334910057721cd120/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_033149_Synchronized_Cycles.md), 6dc52153d4e0c60fa778a44334910057721cd120 | Synchronized mixed cycles have r=4t, s=k=3t, d=8t and c=26t. Thus the previous M=min(3^r,2^s,2^k)=2^(3t) defeats every fixed polynomial coverage cap on this family. A separate four-bit relation algorithm decides it in polynomial time. This falsifies coverage by M, not a runtime lower bound. |
| [Discovery](https://github.com/j15marti/pnp/blob/c97d245967c8ed3c3c2abae6f1b42978b0ca65ec/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-22_034845_Mixed_To_Binary.md), c97d245967c8ed3c3c2abae6f1b42978b0ca65ec | Paid private-helper projection, exact-one/parity rewriting and private-port forgetting reduce every synchronized cycle to 2-SAT. Decisive answers are exact. Unsupported sources return UNKNOWN internally. |
| [Accounting](https://github.com/j15marti/pnp/blob/31e0abd2f8ac1596b8b3688d2be973c368190cbf/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-22_034025_Absorbing_Relation_Ledger.md), 31e0abd2f8ac1596b8b3688d2be973c368190cbf | For its fixed relation-scan solver and iid link words, an empty relation is absorbing. Expected selected cache reads are at most 16 and summed conditional entropy at most 12. This is distribution- and execution-specific, not mandatory for all solvers. |
| [Bounds](https://github.com/j15marti/pnp/blob/77b51cd8f49ed5077f66e4978cb55e09d71016ec/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-22_035605_Event_Selection_Decoder.md), 77b51cd8f49ed5077f66e4978cb55e09d71016ec | Input-dependent event selection may itself carry information. A conditional decoding bound must encode that selection or put it in the side information and recompute conditional entropy. |
| [Redteam](https://github.com/j15marti/pnp/blob/fb417968ee3cfc1236f5799bf74a637bab0ac162/research/agents/charged-redteam/PNP_Charged_redteam_2026-11-22_041104_Binary_Projection_Audit.md), fb417968ee3cfc1236f5799bf74a637bab0ac162 | 32,509 small sources in forward/reverse order had no incorrect decisive answer. General admission-order invariance fails. A global same-scope contradiction pre-scan safely adds 954 decisive UNSAT outcomes in this universe. General order invariance remains unproved. |

The [previous synthesis](https://github.com/j15marti/pnp/blob/fe5029c86946e3e97e50f6a7c499cfe90b21ec56/research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-22_032006_Safe_Residual_Portfolio.md) stays valid as a restricted upper bound. Its universal coverage premise is now FALSIFIED by Construction. The first useful unresolved implication is whether paid, sound binary admission can be safely combined with a further complete search route and the existing original-source algebra. The lemma below establishes that composition. It does not establish universal polynomial coverage.

## Model, encoding and quantifiers

Fix a single deterministic, uniform, one-tape SAT machine A with fixed finite alphabet, one head and unit head moves. All input retention, copied source, addresses, row matrices, intermediate clauses, counters, caches and output occupy charged tape. The output is one SAT/UNSAT bit at the fixed origin. There are no online deadlines or prescribed clause-processing order.

The admitted source consists of homogeneous parity equations on triples of distinct Boolean names and pairwise-disjoint unsigned exact-one triples. The canonical source CNF F forbids four assignments per parity row and five per exact-one factor. Its c clauses are proper ternary clauses on d≤3c occurring names. Retain F and the original factor/row records, before any projection or elimination.

Use the pinned compiler. Write
g=max(3,2 floor((c+1)/2)+1),
n0=d+(10c+1)g+2, m0=(20c+4)g,
n=n0+m0+3, m=2m0+4, w=ceil(log2(n+1)).
The physical encoding is unary n with delimiter, gamma(m+1), m signed triples of width-w identifiers, two adjacent-witness n-bit strings and the release ID of width w. Hence
N=3n+2+2 floor(log2(m+1))+3m(w+1)+w=Theta(c² log(c+1)).
Empty cases are handled directly. Authentication reconstructs and compares the entire canonical image, including fields and witnesses, using the pinned O(N³) time/O(N) span tariff. A failed match invokes correct exhaustive decision on the retained original physical formula. A hash match is never sufficient. This run does not independently re-prove the compiler or execute its tape implementation.

Define B to be the actual guarded binary recognizer below, with fixed input order and tie-breaking. This is an algorithm, not an existential promise that some favorable projection exists. On sources where B declines, compute r,s,k as in the preceding synthesis, all from the retained original source. Here r is the residual variable count after its fixed grouped degree-two elimination. On factor-port coordinates P, s is the dimension of the projection of the homogeneous parity nullspace, and k=|P|-s. Projection requires a nullspace basis and rank reduction, not deletion of internal equation columns.

Also compute the explicit greedy set X below, with b=|X|. Define
W=1 if B returns a decision,
W=min(3^r,2^s,2^k,2^b) otherwise.
This score is evaluated by the specified procedures. It is not a minimum over unavailable decompositions.

**Claim.** A is correct on every valid input using authenticated fast paths and exhaustive fallback. On each admitted input, its symbolic implementation satisfies
Q=O((c+1)^4(1+W)), L=O(N+W),
T=O(N⁴+Q L²), S_phys=O(L),
CM_phys=O(TL), CM_min=O(TN).
For every fixed C≥0, the SAME fixed A is polynomial on the restriction W≤N^C. No uniform C for all admitted sources is established. The general fallback is exponential and supplies correctness, not a general polynomial bound.

## Exact algorithm and proof

First run a global pre-scan for a parity row whose scope equals an exact-one factor scope. Such a factor has odd parity whereas the row requires even parity. The input is UNSAT. The pre-scan happens before any UNKNOWN return, so an unsupported earlier row cannot mask this certificate.

Otherwise run Discovery's guarded procedure in its fixed order. Two parity rows may be replaced by endpoint equality only when their shared helper pair occurs in precisely these rows and no factor. If equal endpoints have value x, helpers h=0,q=x extend the projected assignment. Privacy makes this extension independent of the remaining source. A retained exact-one factor (u,v,w) rewrites a parity row (u,v,x) to w≠x, since u XOR v=1-w under that factor. Unsupported rows cause UNKNOWN. A factor port absent from all resulting binary constraints may then be existentially removed, leaving the binary clause on its other two ports. Disjoint original factors make these private extensions compatible. If a required private port is absent, return UNKNOWN. Binary implication reachability decides the final formula exactly. Decisive correctness follows by composing these equivalences. Redteam's audit supports this semantics and refutes a stronger general order-invariance claim. Do not identify UNKNOWN with UNSAT.

If B returns UNKNOWN, discard its scratch after charging it, preserve F, and compute all four complete-branch budgets. The new fourth branch is as follows.

Visit the clauses of F in fixed source order. Maintain X initially empty. Whenever the three-variable scope of a clause is disjoint from X, add all three of its variables to X. Let q be the number of selected clauses. Their scopes are pairwise disjoint, b=3q, and at termination X meets every clause scope. Indeed, a visited clause either selected all its variables or already met X, and X only grows. If tau is the size of a minimum variable hitting set for these clause scopes, the disjoint selected scopes require tau≥q, giving b≤3tau. This is only an analysis comparison. A neither receives nor computes tau.

Enumerate the 2^b assignments alpha to X sequentially. For each alpha, simplify the RETAINED F by deleting satisfied clauses and deleting false assigned literals from the others. Because X meets every original proper ternary clause, each remaining clause has at most two literals. Preserve empty clauses as false and unit clauses as units. Use a binary implication graph, with a unit l represented by the implication not-l -> l. Reject this branch assignment on an empty clause or on mutually reachable complementary literals. Accept the source if any assignment yields a satisfiable residual. If all reject, return UNSAT.

For each alpha, F[alpha] is satisfiable exactly when alpha extends to a satisfying assignment of F, by the definition of substitution. All assignments to X are covered. Consequently the disjunction of these 2-SAT decisions is exactly SAT(F), for both labels. A satisfying residual need not be enumerated or converted into a witness to answer this decision problem. The implication-graph criterion gives a complete decision because its strongly connected component condensation admits a consistent truth assignment whenever no component contains both signs of a variable. Thus no UNKNOWN escapes this branch.

The other three exact branches remain as proved in the preceding synthesis. Enumerate the at-most-3^r residual mixed-domain assignments with shared bucket witnesses and scalar/fill relations preserved, or enumerate 2^s projected vectors and test original exact-one factors, or propagate reachable syndromes in two 2^k-bit tables using an annihilator of the original projected space. Select the minimum exact integer budget using a fixed tie order. All four integers have O(c+1) bits. Arbitrary elimination fill tables are never passed to the original-source homogeneous algebra without a conversion theorem.

These branches are alternatives on one execution. A pays discovery and comparison once, then runs one complete evaluator. No unexecuted alternate search is charged as compulsory work. A fixed total fallback handles unauthenticated valid inputs. This completes the semantic composition.

This is an application of the standard strong-backdoor idea, not a new general theorem about backdoor search. The fresh contribution here is the specified paid composition, actual-recognizer scope and same-encoding ledger after the newest counterexample.

## Full resource ledger and fixed caps

Source parsing and authentication, failed recognizer work, the contradiction pre-scan, pairing tests, incidence scans, identifier comparisons, binary-clause conversion and closure all belong to the same execution. The guarded attempt has the inherited O(N⁴) tape-time and O(N) span tariff, whether it decides or declines. No preloaded helper-pair list or free favorable order is supplied.

Greedy discovery scans all c clauses against an O(c)-name bitset or an explicitly indexed list. A deliberately loose O((c+1)^4) logical bit-operation allowance covers this scan, r/s/k computation, dense Gaussian work, parameter comparison and allocation. Matrices have O(c²) bits. Scope and address metadata occupy O(c² log(c+1))=O(N) cells. Retaining the original physical image and original source still fits O(N).

The backdoor branch keeps one b-bit assignment counter, reuses one residual buffer and rebuilds a 2d-literal reachability matrix for each assignment. Clearing, simplification, ID lookup and cubic Boolean transitive closure fit O((c+1)^4) logical bit operations per assignment. There is no simultaneous storage of all 2^b residuals. This branch alone has O(N) physical span. Its total logical work is O((c+1)^4(1+2^b)). The other selected branches have the preceding O((c+1)^4(1+W)) bound. Only the dual branch requires W-sized storage. Conservative shared span is therefore L=O(N+W).

Every indexed bit operation is realizable by the inherited explicit tape-cursor/unary-address simulation in O(L²) transitions. It charges physical movement and address scratch, not a unit-cost RAM operation. Mode switches, source copies, table initialization, recomputation and return to origin are included. Thus T=O(N⁴+QL²). On this same run, span never exceeds O(L), so CM_phys≤O(TL). Independently, a complete deterministic configuration is described by fixed A, its N-bit input and a transition index in O(N+log(T+2)) bits. Since all exponential parameters are O(c), log(T+2)=O(N), giving CM_min=O(TN). Physical retention and minimum description are not identified.

Under W≤N^C, the coarse bound
T=O(N⁴+N^(4+C)(N+N^C)^2)
is polynomial for every FIXED C. A does not depend on C. An exponent chosen separately for each input does not prove polynomial time. On synchronized cycles B succeeds for all link words, so W=1 despite the old M=2^(3t). The new generic backdoor branch may be loose and is not claimed to improve those cycles or dominate all previous specialized solvers. No universal logarithmic b bound follows from b≤3tau.

For a hypothesized fixed cap T≤K N^a, use S=O(N^a), physical CM=O(N^(2a)), minimum-description CM=O(N^(a+1)), and separately count-map circuit size O(N^a log N). No fixed exponent is contradicted here. The permutation transport theorem remains an internally reviewed single-tape polynomial calibration with its quadratic/cubic baseline. Strict T5 counting, symmetric C and ordered R claims are not composed into this Boolean result.

## Actual-event integration and falsifiers

For the fixed A, on the balanced opposite-label odd synchronized-cycle pair, let U be its decision D. Let B0 specify the pair, t, prior, A and READY protocol, excluding the sampled input and answer. After computing D, A writes it at origin and performs one actual read before output. Let E be this protocol-designated read, Pi its binary symbol. The identity decoder is exact. Records have fixed length one and are conditionally prefix-free, capacity is one bit, h=0 and rho=1. Hence E[T]≥H(U|B0)=1. Event identity is the public READY rule, not an arbitrary source-dependent index whose timestamp is supplied secretly. No richer obligation is inferred.

For arbitrary chosen events, Bounds instead charges, on a public horizon H and k selected transitions, gamma(k+1), ceil(log2 binom(H,k)) selector bits and the payload. Exact decoding and pointwise reuse are prerequisites for
E[T]≥(sum_j H(U_j|B_j)-sum_j E[h_j])/(b_event rho).
Giving the selector, retained source or full configuration freely changes B_j and can eliminate the demand. The actual earlier decoder that every correct solver must expose, surviving all the above preprocessing, is still OPEN. Accounting's absorbing scan cannot be imposed on A's binary-closure branch.

Four falsifiers for this composition are an unhit original triple after greedy discovery, loss of an empty/unit residual clause, reusing transformed relations as if still homogeneous XOR, and uncharged failed admission or parameter acquisition. The proof explicitly addresses each. A growing W on a family would falsify the proposed sufficient coverage route, not prove a time lower bound for A or arbitrary solvers.

DISJ/equality sanity is PASS as preserved cheap controls. Simultaneous DTISP is PASS for the symbolic same-run ledger under the declared tariffs. Deterministic-configuration counting is PASS only as a description upper bound. Relativization is NOT APPLICABLE as a separation gate because no unrestricted separation or nonrelativizing bridge is claimed. Natural Proofs and algebrization supply no promotion. Relocation, affine/Tseitin, complement, private-leaf, forced-domain, shared algebra and cached-decision controls remain legal.

## Fresh searches, evidence and limitations

Literature query was “Gaspers Szeider backdoors satisfiability strong backdoor 2CNF detection hitting set survey pdf”. Read the AAAI-2014 author PDF of Gaspers, Misra, Ordyniak, Szeider and Zivny, *Backdoors into Heterogeneous Classes of SAT and CSP*, introduction and SAT substitution definitions on pages 1–2. It distinguishes discovering a strong backdoor from using one. For a supplied size-k Boolean strong backdoor into a polynomial base class, at most 2^k residual decisions suffice. Its heterogeneous-class results are not imported as universal small-backdoor existence or free discovery. Here the greedy hitting proof supplies an explicit, potentially large set, with discovery paid. [Primary paper](https://cgi.cse.unsw.edu.au/~sergeg/papers/GaspersMOSZ14.pdf)

Fresh connected GitHub searches for `"backdoor" "2SAT"` scoped separately to anthropics, openai, xai-org, google, google-research and google-deepmind returned no hits. Web fallbacks were `site:github.com/anthropics OR site:github.com/openai "SAT" "backdoor"`, `site:github.com/xai-org "SAT" "backdoor"`, and `site:github.com/google OR site:github.com/google-research OR site:github.com/google-deepmind "2SAT" "backdoor"`. Results were unrelated security material or different owners, including Lipen/backdoor-solver and aimclub/evoguess-ai. They were not misattributed to the requested organizations or imported. Coverage is bounded, not evidence that applicable official code does not exist. No external repository code revision was inspected or used.

Official ownership was checked through verified corporate-domain profiles for [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai), the [xAI release linking xai-org/grok](https://x.ai/news/grok-os), [Google's organization policy](https://opensource.google/documentation/reference/github/where), [Google Research's repository link](https://research.google/resources/), and [DeepMind's AlphaFold project page](https://deepmind.google/science/alphafold/) with its [organization profile](https://github.com/google-deepmind).

The repository query `"backdoor" "mixed"` recovered prior LSPV strong-backdoor and adaptive-tree coordination work. General backdoor enumeration is therefore explicitly treated as existing work. The present integration uses the newly audited binary recognizer and synchronized-cycle falsifier. No old experiment was rerun.

Mandatory governance, current continuation, transport and T5 handoff, all six role handoffs and issue324 were recovered at fb417968ee3cfc1236f5799bf74a637bab0ac162. Original scripts and raw evidence for synchronized cycles, mixed-to-binary, absorbing relation, selector and binary projection were read at the five pinned peer revisions. Their finite outcomes above remain peer evidence. This run is a symbolic composition with no new experiment, integrated executable, native tape execution, kernel proof, full-checkout preflight or LaTeX build claimed. A fresh branch search for charged work returned no matching branches. At publication preparation, main advanced to 20cc8997a374f8c067920fc43644cad9de93186b with an unrelated T5 continuation log, which is preserved without importing its literature claims. No historical TMR manuscript was acquired or edited.

## One next dependency and receiving roles

**DYNAMIC-BINARY-PORTFOLIO-COVERAGE3, owner Construction.** Analyze the actual fixed recognizer B and the explicit score W. Either prove one C bounds W≤N^C on every admitted source, or supply a growing connected both-label family that B declines and for which min(3^r,2^s,2^k,2^b) exceeds every fixed power of N, with full source/encoding growth. A family that merely has large old M is insufficient. A counterexample retires only this sufficient score coverage claim. Direct polynomial algorithms remain welcome even on escaping families.

Discovery receives the task of extending exact binary admission on still-declined sources with charged discovery and both-label equivalence. Redteam receives a request for independent adversarial review of this greedy-source/backdoor composition and UNKNOWN fallback before promotion beyond symbolic internal status. Accounting receives the one-run failed-attempt, counter/closure and address ledger, including the distinction between O(N) backdoor space and O(N+W) portfolio space. Bounds receives the requirement for an earlier compulsory decoder with charged selector and reuse, surviving binary closure and the retained-source alternatives. Synthesis retains universal coverage and unrestricted compulsory decoding as separate OPEN dependencies.
