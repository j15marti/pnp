# Closing the residual-type gap before searching for factor backdoors

22 November 2026, 00:20 PST. PNP Charged Proof Synthesis.
**DYNAMIC-RESIDUAL-FACTOR-CLOSURE1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1.
Recovery **7962e8fd645db04d0168eb90c8a2449b13a1e073**.
**PROVED/EXACT restricted** closure and solver integration; **COMPUTATIONAL** finite tests. Independent adversarial review requested, pending. Same-conversation derivation is not external certification. P versus NP **OPEN** in either direction.

## Reconciliation and selected implication

Current common model is deterministic finite-alphabet one-head/one-writable-tape Boolean compatibility decision with charged input, addresses, copies, caches and origin output. Each row describes its own fixed execution; lower demands from one are not added to another's costs.

| Latest role/source recovered at the snapshot | Established scope | First unresolved implication |
|---|---|---|
| [Construction 23:31](../charged-construction/PNP_Charged_construction_2026-11-21_233100_Degree_Flow.md), original 98bad277e88aa3c096c4f857dc4323fb910e398a | Degree sources make the fixed projection/pivot search expensive but admit paid flow, T=O(N^5), span O(N). | Paid broader conditioning/coverage. |
| [Accounting 22:45](../charged-accounting/PNP_Charged_accounting_2026-11-21_224500_Paid_Backdoor_Ledger.md), original fb7328bfe25d076334e72be583de1f04cfc2393b | Strong 2-CNF acquisition T=O(3^h N^5), span O(N), distinct CM bounds O(3^h N^6). | No universal logarithmic h; its branching theorem is specific to ternary hitting. |
| [Discovery 23:51](../charged-discovery/PNP_Charged_discovery_2026-11-21_235100_Degree_Factor_Admission.md), original 5c68647aae3b7e5295990235bc8313732edeb04b | General matching admits unsigned exact weight-one/two ternary support groups, each name in two groups. T=O(N^4), span O(N), each CM separately O(N^5). | Conditioned formulas need a broader residual type before applying this admission literally. |
| [Bounds 00:05](../charged-bounds/PNP_Charged_bounds_2026-11-22_000500_Phase_Endpoint_Debit.md), original ad3c2add6c08b6b51a2e31a076593cef9027edad | CONDITIONAL finite-phase splicing/list decoder with endpoint entropy debit, ambiguity and real event reuse. | Later reachable conflict families with positive net demand after all debits. |
| [Redteam 00:15](../charged-redteam/PNP_Charged_redteam_2026-11-22_001500_Blossom_Execution_Audit.md), original recovery revision | Separately coded source-level blossom test:1024 new demand cases agree; polynomial shortcut survives. | All-input acquisition remains open; no complete target implementation certification. |

Own previous [local projection report](PNP_Charged_synthesis_2026-11-21_232400_Local_Projection_Repair.md) and original peer evidence were recovered. The strongest constructive candidate is the paid factor shortcut. This run closes its residual-type implication. The result is an integration of classical factor methods; the broader signed interval mechanism already occurs in historical INTERVAL-FACTOR134, read in full. [4] No novelty in graph factors or parameterized branching is claimed.

The literal old admission is NOT closed under assignments: on the K4 all-one source, set the variable for edge01 to zero. Two groups now enforce exact-one on two names. The residual is SAT, but a routine requiring every clause to have exactly three literals rejects it. This is an explicit type counterexample, not a false-decision allegation against Discovery, which returns UNKNOWN and has a correct fallback.

## Fixed algorithm, exact class and falsifiers

Let C consist of clause lists with width at most three whose groups on identical unsigned supports have exactly a cardinality relation sum(x in S)=b, with 0<=b<=|S|, and where every remaining name belongs to at most two distinct groups. Include an empty conjunction as SAT and any empty local relation as immediately UNSAT. Support means actual variable IDs, not a hash. An empty relation can be detected before the occurrence test because it already makes the conjunction false.

Fix R before the input: authenticate the canonical target once, extract its source, restrict it when a branch specifies actual variable values, and compute each support's exact at-most-eight-row table. Admit C, including zero and saturated demands and one-occurrence names; otherwise return UNKNOWN from this shortcut. Decide admitted constraints by the construction below. A total solver uses a correct exhaustive decision fallback on the original input whenever admission fails. This preserves all-input correctness, with a polynomial runtime guarantee only on the admitted path.

For every F in C and every partial assignment tau, literal restriction F|tau either exposes a false group or remains in C after merging equal supports. The admitted path can be implemented with T=O(N^5), S=O(N), CM_phys=O(N^6) and separately CM_min=O(N^6), in the ORIGINAL canonical target length N. The finite library implementation is evidence about semantics, not a measurement of these tape costs.

Four falsifiers: a restriction losing a clause rather than satisfying/removing it; colliding supports with unequal demands being silently merged; free treatment of a one-occurrence variable; or importing the 2-CNF 3^h acquisition bound for this different class. The proof handles the first three. The fourth is expressly rejected.

## Restriction closure

A group on S enforcing sum_S x=b, after assigning tau on S intersect dom(tau), becomes

    sum_(S minus dom(tau)) x = b - sum_(S intersect dom(tau)) tau(x).

A right-hand side outside [0, remaining arity] is false. At arity zero the relation is true exactly when the adjusted demand is zero. Otherwise it is another admitted cardinality relation.

This also holds for the literal clause representation used here: every clause in one support group contains all of that support's names. Restriction either satisfies the clause or leaves precisely the common remaining support. Its conjunction gives the displayed adjusted relation. If two distinct old supports become equal, equal adjusted demands are redundant and unequal demands make the group empty. No variable acquires a third distinct support: deletion and merging cannot increase its support incidence count. This proves closure, including tautological empty groups and forced domains.

The theorem does not cover arbitrary signed cardinality or interval tables; those have broader historical algorithms but are unnecessary for this precisely implemented unsigned extension. Nor does it claim closure under general existential join/projection, which may produce a noncardinality relation.

## Optional incidences without exponential choices

Build a loopless multigraph with one vertex per nonempty group and exact demand b_v. A name in two groups is an identified edge between them. Keep parallel names distinct. For every name appearing only once, add an edge from its group to ONE new reservoir vertex s. Let D be the number of these names. Try exact reservoir demands t=0,1,...,D, sequentially reusing storage.

A satisfying assignment selects exactly the true-variable edges and hence gives one of these factors with t equal to the number of true single-occurrence names. Conversely any factor in any trial gives consistent Boolean values on all names and meets every original group demand. Unused source names may take either value for decision. This proves both SAT and UNSAT equivalence, without trying all 2^D patterns of dangling names.

For each trial use the incidence gadget: one port per edge end, paired across that edge; at a vertex of degree d add d-b private dummies adjacent to all its ports. In a perfect matching d-b ports are consumed by dummies and exactly b by external edges. Conversely any demanded-degree edge subset extends locally to a perfect matching. This direct proof handles b=0 and b=d, as well as the empty graph, without importing the positive-demand convention of Tutte's paper silently. [1] A deterministic maximum-cardinality algorithm decides the resulting finite graph. [2]

If q is the number of support groups, there are at most3q names, O(q) edges/ports, O(q) gadget vertices and O(q^2) gadget edges. The quadratic term is the reservoir's dummy-port bipartite graph. At most3q+1 reservoir trials are necessary. Storing all trials simultaneously is not required.

## Exact encoding and full charged ledger

Retain the existing compiler equivalence and internal-review status. For c>=1 original proper source clauses on d<=3c densely named occurring variables, let r be the least odd integer greater than c, at least three:

    n0=d+(10c+1)r+2, m0=(20c+4)r,
    n=n0+m0+3, m=2m0+4, w=ceil(log2(n+1)),
    N=3n+2+2 floor(log2(m+1))+3m(w+1)+w.

The physical input has unary n and delimiter, gamma(m+1), ordered signed target triples, two n-bit supplied assignments and a w-bit release ID. N=Theta(c^2 log(c+1)). The target is Boolean existential decision, not strict C/R counting. Restrictions operate on the authenticated extracted source, so no new target encoding is substituted inside a branch. N always includes the original retained input.

| Stage | Cost charged on this execution |
|---|---|
| Parse/extract/regenerate source image | Inherited O(N^3) time and O(N) span; dimensions and lengths bounded before allocation; all failed checks paid. |
| Restrict, compare names, merge supports, compute exact tables | O(c^2) record operations, at most eight rows per support, no semantic oracle or exponential truth table. |
| Build reservoir and gadgets | O(c^2) index entries, each O(log N) bits; distinct edge identities and all address storage included. |
| Each deterministic matching trial | Classical O(c^4) elementary operations, O(c^2) memory entries. |
| All reservoir trials | O(c^5) operations with in-place rebuild; failed trials are included. |
| Actual one-tape access | At most O(N^2) transitions per record operation by indexed shuttling, finite-word arithmetic and physical head travel. |
| Storage and cleanup | O(c^2 log N)=O(N) bits under THIS compiler; retain input/source/current graph, not previous trials. Cleanup, cache placement and origin output included. |

Thus O(N^3+c^5 N^2)=O(N^5), conservatively, since c^2=O(N). Physical CM sums actual occupied spans and is O(N^6). Separately a self-contained input-plus-time replay description uses O(N+log(T+2))=O(N) bits per complete configuration, so CM_min=O(N^6). These equal orders have different proofs. The source alone has length M=O(c log c); no O(M) matching-space claim is made. Target production, if needed, costs O(N^3), O(N) span separately. The generic exhaustive fallback remains exponential.

For a supplied or actually acquired set B of h source names such that every restriction belongs to C or exposes a false relation, OR the at most2^h exact residual decisions. Sequential traversal retains only source, B, assignment counter and current graph. Time after acquisition is O(2^h N^5), space O(N), each CM separately O(2^h N^6). If acquisition takes G(N) transitions and has O(N) span, add G(N) to time and O(N G(N)) to each cumulative upper bound; otherwise charge its actual space separately. For h<=C0 log2 N, residual evaluation is polynomial with exponent 5+C0. Neither small h nor polynomial G is proved universally.

Nishimura-Ragde-Szeider's strong-backdoor quantifiers justify evaluating every assignment of an acquired set, but their specialized Horn/2-CNF acquisition theorem does not supply G for this class. [3] Even straightforward subset enumeration can take N^h before residual checks. Closure repairs evaluation; it does not solve acquisition.

## Evidence and its limits

[Code](../../../experiments/dynamic_synthesis_residual_factor_20261122.py), [raw](../../../results/raw/dynamic_synthesis_residual_factor_20261122.json), NetworkX3.5. Run the complete script with Python after installing that exact version.

All3^6 partial assignments on each of three six-variable K4 sources were checked: all-one demands, all-two demands and demands(2,1,1,1). These are **2187 new restriction cases**, with **362 SAT and1825 UNSAT**. None returned UNKNOWN, and each result agreed with direct Boolean enumeration of its residual. The earlier full-source matching sweep was not repeated; the new purpose is restriction closure, forced demands and reduced arity. Five additional cases check single incidence, zero demand, saturated demand, equal-support merging and conflicting-support rejection. A positive single clause remains SAT-but-UNKNOWN, preserving the admission boundary.

Script SHA256:6da16829307a0a53367960549d3b1397f3bde01cbc6590c038cfbc7b23826c30. The final run completed in about0.95 seconds within a30-second cap. The checks were rerun after moving detection of any empty support table ahead of noncardinality rejection, matching the stated admission order. Raw JSON was losslessly compacted after execution; mathematical values were unchanged. No new target materialization, compiled-image SAT solve, TM timing or formal kernel build occurred. This is finite validation alongside the symbolic proof.

## Lower-bound integration without combining executions

Bounds' finite-phase premise concerns an arbitrary fixed correct A, actual reachable UNSAT checkpoint family, SAT mixed-half conflicts, and a public first left-side endpoint. Its U_j is the sampled checkpoint index; B_j gives the public codebook/model/cut, not the sampled retained source. Pi_j is gamma(L_j+1) followed by ell-bit arrival states; E_j contains real crossings, ell=ceil(log2 Q), h_j=2floor(log2(L_j+1))+1. The actual external list decoder additionally needs retained endpoint right tape R_j and leaves at most log alpha(G_j) index ambiguity. Its runtime is not asserted efficient. With real overlap rho the CONDITIONAL implication is

    E[T] >= max(0, sum_j[H(U_j|B_j)-E log2 alpha(G_j)
                        -H(R_j|Z_j,B_j)-E h_j]/(ell rho)).

No accepted fast path here is forced to preserve those conflicts or produce a positive net numerator. The first open lower-bound arrow is still recurrence of such reachable families after all paid algebra, flow, factor computation and caching. We do not certify the Bounds proof independently; it was authored in this conversation and retains pending review.

For the present solver, after paid solving and erasure, U=decision, public B specifies equal-prior same-length SAT/UNSAT inputs and A, E is one fixed-origin cache read, Pi its bit, h=0,b=rho=1, and identity decoding gives only one bit. Reuse raises rho; free cached-label side information makes entropy zero. No virtual residual-query service is compulsory.

For a fixed cap T<=KN^a, the net actual demand must exceed ell rho KN^a. Keep S=O(N^a), CM_phys=O(N^(2a)) and CM_min=O(N^(a+1)) distinct. Count-map circuit size O(N^a log N) concerns another output. The permutation transport control retains quadratic-time/cubic-CM matching upper bounds and static ceilings N^2/8,N^3/27 on its own ordered layout. Excluding one exponent or one algorithm is insufficient for P!=NP.

## Sources, fresh search and receiving tasks

1. Tutte, *A Short Proof of the Factor Theorem for Finite Graphs*, Canadian J. Math.6(1954),347-352, pp.348-349. [Primary PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/3785657C35F370E32E5AEAFC3D1B84CE/S0008414X00023774a.pdf/short_proof_of_the_factor_theorem_for_finite_graphs.pdf). Read the exact incidence construction; zero-demand extension proved above.
2. Edmonds, *Paths, Trees, and Flowers*, Canadian J. Math.17(1965),449-467. [Published PDF](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/08B492B72322C4130AE800C0610E0E21/S0008414X00039419a.pdf/paths-trees-and-flowers.pdf). Polynomial general-graph matching, with its elementary-operation model repriced here.
3. Nishimura, Ragde, Szeider, *Detecting Backdoor Sets with Respect to Horn and Binary Clauses*, SAT2004 original manuscript, p.96-97 strong-backdoor definition and acquisition distinction. [Primary PDF](https://www.satisfiability.org/SAT04/programme/51.pdf). No factor-backdoor discovery theorem imported.
4. Historical [INTERVAL-FACTOR134](../lspv-1/2026-10-25_0058_LSPV-1_INTERVAL_FACTOR134.tex), read at recovery revision, already proves broader signed degree-two interval feasibility and source-high-degree branching. This run supplies a bounded-arity residual recognizer, direct exact-demand implementation and current one-tape cost integration, not a new general-factor theorem.

Fresh literature queries: “Tutte f factor prescribed degree zero degree one vertices perfect matching reduction” and “strong backdoor sets cardinality constraints degree two SAT conditioning matching”. A two-occurrence-backdoor paper and heterogeneous-backdoor context surfaced, but their full hypotheses were not imported: clause occurrence and group occurrence are distinct. Promising primary papers above were read for the actual transfer.

Fresh GitHub query '"f-factor" "degree"' covered anthropics, openai, xai-org, google, google-research and google-deepmind. Five scopes yielded no hits, xAI after one429 retry. OpenAI returned 10-f-factors.tex at4eaee87548250b2682affda7d05d947c05554bae. Its excerpt refers to a more elaborate reduction; prior logs already record the unreviewed randomized parent theorem, so no duplicate deep review or theorem import. Two official-scope web fallback queries with the same terms returned that preprint, unrelated factor code and unrelated broad claims. None supplies the missing acquisition theorem. Organization ownership was checked in this session through verified Anthropic/OpenAI profiles, x.ai/news/grok-os, opensource.google/documentation/reference/github/where, research.google/resources and DeepMind's official Tracr release. Bounded no-hit searches do not prove absence.

Current directive/transport, governance/skill, applicable T5 definitions, own latest report and the five peer claims plus relevant original evidence were recovered. Selected files are available, not a full checkout; manuscript preflight/LaTeX builds were not run. DISJ/equality sanity and simultaneous accounting PASS scoped; deterministic replay is only an upper bound. No relativization, Natural Proofs or algebrization bypass is claimed. Affine/Tseitin, complement, private-leaf, forced-domain, decision-witness, relocation and caching controls remain legal. No roles, schedules or historical TMR ownership changed.

**One next mathematical dependency: PAID-FACTOR-BACKDOOR-ACQUISITION1**, owner Discovery with Construction: specify a uniform acquisition procedure for sets whose all restrictions enter the declared residual class, charge unsuccessful choices and all branches, then prove its parameterized bound or provide a legal counterexample. Accounting receives the O(c^5) operations/O(N) span ledger and acquisition/evaluation separation. Redteam receives closure under colliding supports, reservoir trial completeness and the three-status recognizer for adversarial review. Bounds receives the obligation to survive this expanded paid shortcut. Synthesis keeps all-input polynomial coverage and all-solver superpolynomial recurrence OPEN.
