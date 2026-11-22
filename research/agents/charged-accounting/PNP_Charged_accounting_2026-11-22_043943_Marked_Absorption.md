# Marked parity preserves absorption with charged marker acquisition

22 November 2026, 04:39:43 PST. PNP Charged Accounting. **DYNAMIC-MARKED-ABSORPTION-LEDGER1** under DYNAMIC-COMPATIBILITY-OBLIGATION1. **PROVED/EXACT** for the fixed solver and distributions defined here. Physical implementation retains the inherited symbolic compiler/authentication tariffs. **COMPUTATIONAL** for the finite audit. Independent review and full tape implementation are pending. P versus NP is **OPEN**.

## Quantified result and pinned evidence

Fix a uniform deterministic one-head finite-alphabet writable-tape SAT solver A before choosing any input. It authenticates Construction's two synchronized cycles with one parity row on three distinct top-row z ports. It then runs the eight-bit reachable-set scan described below, stopping on the empty set. It returns the even-parity closed-walk decision after the last column if still active. Valid nonmatches use exhaustive decision on the retained formula. Both labels occur for every odd t≥3.

For each t and each fixed three-element mark set M, choose the two link words independently uniformly in {A,C}^t. Then the number of selected link-cache reads has exactly the same distribution as in the unmarked absorbing scan, and
sum_(j=1)^t H(S_j | t,j,M,S_(j−1),protocol) ≤ 12,
E[number of selected link reads] ≤16.
These are statements about this scan after paid authentication.

For the second distribution let M be uniform over the binom(t,3) triples, independent of the link words. Include one explicit acquisition record for M. With ell=ceil(log2 t), the complete selected-read ledger satisfies
sum_(j=0)^t H(U_j|B_j) ≤ log2 binom(t,3)+12,
E[selected reads] ≤3ell+16.
The event inequality itself is
E[T_A] ≥ sum_(j=0)^t H(U_j|B_j),
with capacity b_event=1, framing h_j=0 and maximum reuse rho=1 under the stated protocol. Initialization and all other transitions remain in T_A.

This extends the previous four-bit relation ledger to the decision-sensitive marked-parity construction and charges varying marker information explicitly. The obligation values are source-defined reachable sets and the explicit input mark set. They are defined independently of a desired hardness conclusion. [Construction and source semantics](https://github.com/j15marti/pnp/blob/009932ebaf093a18c19378261d0123f0c0c3297e/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_043212_Three_Marked_Columns.md) · [Previous accounting](https://github.com/j15marti/pnp/blob/009932ebaf093a18c19378261d0123f0c0c3297e/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-22_034025_Absorbing_Relation_Ledger.md)

## Projection and absorption proof

The local relation is A={(0,0),(1,1),(1,0)} for an AA column, C={(0,1),(1,0)} for CC, and D={(1,0)} for either mixed column. Their probabilities are 1/4,1/4,1/2, respectively. Let S_0={(0,0,0),(1,1,0)}. A tuple (v,x,p) records initial z, current z and accumulated parity. For each allowed edge (x,y), the next tuple is (v,y,p XOR x) on a marked column and (v,y,p) otherwise. Union all successor tuples into a fresh set S_j. Empty sets have empty successors. At the end accept iff (v,v,0) occurs for some v. Construction's extension proof gives exact SAT and UNSAT semantics.

There are eight possible tuples. The summary is a subset of those tuples encoded in eight bits, and may therefore have 256 possible values. Let P(S) discard parity from each tuple. For every subset S, each local relation L and either mark flag,
P(update(S,L,flag)) = P(S) composed with L.
Every successor projects to an allowed relation step. Conversely every projected step has some predecessor parity and its deterministic parity update produces a successor. This proves equality without a reachability assumption. By induction P(S_j)=R_j for the original four-bit relation scan on the same words. Therefore S_j is empty exactly when R_j is empty, pointwise on every input and for every mark placement. The stopping times and selected link-read counts coincide exactly.

Two consecutive D columns force R empty because D composed with D is empty. Surviving n columns requires avoiding DD within each of the disjoint pairs (1,2),(3,4),... . Independent words give
Pr(S_n nonempty) ≤ (3/4)^floor(n/2).
For every fixed mark set the next local relation is independent of the previous set. Its entropy is 3/2 bits, and update is deterministic. Thus
H(S_j|S_(j−1),M,t,j) ≤ (3/2) Pr(S_(j−1) nonempty).
Summing the survival bound gives at most 8 active columns in expectation, at most 16 selected link reads, and at most 12 bits of conditional demand. Averaging over independently sampled M preserves the estimates. This proof uses the declared iid input distribution. Adversarial words can keep all t columns active.

The marked check can change SAT to UNSAT even though the absorption times coincide. The final parity acceptance test accounts for that difference. At t=3, AAC/CAC has one closed z sequence of odd weight and becomes UNSAT when all columns are marked. The unmarked relation remains nonempty. This prevents conflating absorption with the full terminal decision.

## Actual records and selector costs

After exact admission A stores M as three increasing zero-based indices in separate ell-bit binary fields. It explicitly reads these 3ell bits once into charged scratch before the link scan. For the random-marker distribution set U_0=M and B_0=(t,A,prior,protocol). E_0 is those 3ell distinguished physical read transitions and Pi_0 their concatenation. The decoder splits the fixed-width fields and recovers M. All records have length 3ell for fixed B_0, hence are prefix-free. H(U_0|B_0)=log2 binom(t,3). Unused binary codewords cause no problem. This cache was built from the authenticated input at paid cost, and the index-read pass is additional paid work by this fixed solver.

For j≥1 define U_j=S_j and B_j=(t,j,M,S_(j−1),A,prior,protocol). When S_(j−1) is nonempty, E_j contains the two distinguished reads of the top and bottom link bits of column j. Pi_j is the ordered two-bit payload. The decoder forms the local relation, applies the public mark flag from M and computes the next set. When the previous set is empty, E_j is empty, Pi_j is empty and U_j is the empty sentinel. There is no further column service on the actual execution after absorption. Conditional on B_j the code is either fixed length two or the singleton empty code, so it is prefix-free.

The protocol identifies which data are consumed, and the decoder needs no absolute timestamp, head address, hidden selector or elapsed time. Marker acquisition and all column events are disjoint. Each transition contributes one bit, h_j=0 and rho=1. Other visits to the same cells are paid in T but excluded from these records. Thus exact decoding and conditional prefix coding give H(U_j|B_j)≤E|Pi_j|=E|E_j|, and disjointness gives the stated summed inequality. It follows algebraically that its right side is bounded by log2 binom(t,3)+12. This upper bound on a lower-bound certificate is not a lower bound of that magnitude.

The earlier data-bearing side information in B_j consists of M and the previous summary. Their acquisition and storage are charged. The first record accounts for marker entropy once. Giving the entire retained source freely changes the conditional entropy problem. The actual machine keeps its source on tape, and the model permits reading it and other legal preprocessing. Consequently decision correctness alone does not compel every solver to expose these particular events. Arbitrary input-dependent selected times require the explicit selector debit in Bounds unless a sufficient decoder is supplied without them. [Selector theorem](https://github.com/j15marti/pnp/blob/009932ebaf093a18c19378261d0123f0c0c3297e/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-22_035605_Event_Selection_Decoder.md)

## Physical ledger and polynomial caps

Use Construction's d=8t, c=26t+4 proper source clauses. With g=max(3,2 floor((c+1)/2)+1), n0=d+(10c+1)g+2, m0=(20c+4)g, n=n0+m0+3, m=2m0+4 and w=ceil(log2(n+1)), the full encoded length is
N=3n+2+2 floor(log2(m+1))+3m(w+1)+w=Θ(t² log t).
These terms charge the unary header, gamma clause count, signed literal fields, two adjacent-witness strings and release ID. The compiler's exact Boolean equivalence and adjacent witnesses are inherited, and source clause order grants no final-tape adjacency.

A retains input and source, word caches, normalized marker fields, two eight-bit summary buffers, loop counters, address scratch and output in O(N) span. Authentication regenerates the full image and compares every field. Discovery of t and marks, failed candidates, indices, initialization, copying, representations and full consumption are included in the pinned O(N³) tariff. The scan and marker acquisition use O(t log²(t+1)) bounded indexed operations. At O(N²) tape transitions per indexed operation this fits O(N³) for the declared encoding. Reading marker scratch, shifting cursors, clearing buffers, recomputation, switching modes and returning output to origin are charged. A valid nonmatch keeps correct exhaustive fallback with O(2^n N³) time and O(N) span.

On admitted inputs, the same run has T=O(N³), peak physical span O(N), physical CM O(N⁴). Independently, the original input and a self-delimiting step index describe any deterministic configuration in O(N+log(T+2)) bits. This gives minimum-description CM O(N⁴). The expected selected-event bound leaves the full authentication and tape-motion costs intact.

Against a fixed cap T≤KN^a, the exact demand of this ledger is at most log2 binom(t,3)+12=O(log N), compared with b_event rho KN^a=KN^a. It excludes no fixed polynomial exponent. Generic same-execution ceilings remain S=O(N^a), physical CM O(N^(2a)), minimum-description CM O(N^(a+1)), and separately count-map circuit size O(N^a log N). The internally reviewed permutation transport theorem retains its single-tape quadratic/cubic calibration. No strict T5 counting, symmetric C or ordered R transfer is asserted.

Four falsifiers are random markers omitted from acquisition and conditioning, free data-bearing event indices, a parity filter applied before the final column invalidating the projection equality, and extending the iid expectation to worst-case inputs. The fixed solver and records above address them. DISJ/equality and shared-computation controls are preserved. Simultaneous DTISP is verified for this symbolic same-run ledger. Configuration counting gives only an upper description bound. Relativization, algebrization and Natural Proofs supply no unrestricted implication. Affine/Tseitin, complement, forced-domain, private-leaf and relocation remain legitimate controls.

## Experiment and fresh searches

The new checker exhausts all 256 summary masks, three local relations and two mark flags, verifying 1,536 projection identities. It then propagates exact rational distributions for 13 length/mark schedules at t=3,4,8,16,100. Conditional entropies are floating diagnostics. All schedules at a fixed t have identical exact read expectations. At t=3 the expectation is 11/2 and the SAT probability is 13/64. At t=4 it is 53/8, while the entropy sum varies with marker placement. At t=100 the displayed entropy sums are approximately 6.629124, 6.625336 and 6.625336. The symbolic bounds above hold for all t. This extends the previous experiment to parity-labelled summaries and tests the new projection premise. [Checker](../../../experiments/dynamic_accounting_marked_absorption_20261122.py) · [Raw](../../../results/raw/dynamic_accounting_marked_absorption_20261122.json)

Fresh literature query “Shannon 1948 mathematical theory communication conditional entropy finite state transducer theorem 7 pdf” recovered the corrected 1948 Bell System Technical Journal reprint. Section 8/Theorem 7 concerns entropy rate of finite-state transducers driven by finite-state statistical sources. It motivates testing information loss but supplies no finite-horizon compulsory SAT cost. The present nonstationary marked scan uses the explicit decoder and finite-length proof above. [Primary paper](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf)

Fresh official GitHub query `"entropy" "absorbing" "Markov"` in anthropics, openai, xai-org, google, google-research and google-deepmind returned five empty results. OpenAI was retried after HTTP429 and returned a reversible Markov Dirichlet-form/log-Sobolev excerpt at revision 4eaee87548250b2682affda7d05d947c05554bae. Its assumptions and energy inequalities supply no actual SAT-event decoder, so no theorem or code was imported. Web fallback used the same absorbing/entropy terms with the six organization paths. Google Research diffusion and replay-buffer files surfaced. Their absorbing-state terminology does not verify the projection identity here. No external code was executed. [OpenAI excerpt](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/preprints/Critical-mixing-in-the-Sherrington-Kirkpatrick-model-September-25-2026/build/sections/cap-entropy.tex) · [Google Research diffusion result](https://github.com/google-research/google-research/blob/master/d3pm/images/diffusion_categorical.py)

Ownership was checked with corporate-domain organization profiles and official project links. [Anthropic](https://github.com/anthropics) · [OpenAI](https://github.com/openai) · [xAI](https://x.ai/news/grok-os) · [Google](https://opensource.google/documentation/reference/github/where) · [Google Research](https://research.google/resources/) · [DeepMind](https://deepmind.google/science/alphafold/)

Mandatory governance, continuation, transport and T5 documents, current role handoffs, original code/raw and issue324 were recovered at 009932ebaf093a18c19378261d0123f0c0c3297e. A repository search for marked/absorption surfaced unrelated historical portfolio passages. A charged-branch search returned no branches. Full-checkout preflight, compiled tape execution, LaTeX build and kernel verification were unavailable in the selected-file environment. Report status is a symbolic restricted theorem plus finite computational checks, pending independent review.

**One next dependency for Bounds and Synthesis.** Identify an earlier observation that is compulsory for every correct solver and prove surviving conditional demand after joint input/marker acquisition. The exact ledger here gives a concrete obstruction to charging every parity-labelled stage afresh. Redteam receives a bypass target that aggregates the eight-bit summary during authentication, removing the separate scan and normalized-marker replay. Discovery receives the requirement to charge and condition all live-syndrome basis metadata when extending to several parity checks.
