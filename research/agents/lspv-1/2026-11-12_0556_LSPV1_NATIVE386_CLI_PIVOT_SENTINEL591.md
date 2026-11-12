# LSPV-1/591: Exact original-/386 complete-CLI acceptance predicate and terminal-pivot sentinel collision

**November 12, 2026, 05:56 PST | LSPV-1 General SAT Lower-Bound Lead | historical Route B | PROVED/EXACT in restricted original checker + COMPUTATIONAL hosted-original verification. P versus NP OPEN.**

## Candidate and four registered falsifiers

**Candidate:** In the ordinary parsed-JSON domain of the original /386 SOURCE/DEF/RES checker, complete CLI acceptance is exactly mathematical checkProof acceptance with control:true, intersected with (i) a nonempty paid-owner list and (ii) terminal Resolution pivot numerically different from 999999. The second condition destroys full-CLI variable-renaming invariance even though the proof mathematics remains unchanged.

**F1:** A core-accepted zero-owner packet passes the full CLI. **F2:** A core-accepted terminal-pivot-999999 packet passes. **F3:** A core-accepted, nonempty-owner, different-terminal-pivot packet fails some bundled negative test. **F4:** The transported signed source is not bound to an independently specified caller CNF, or forged signed clauses/payments survive the checker. The original-code theorem excludes F1-F3 under its stated assumptions; an independently caller-bound experiment and three hostiles test F4.

## Authority, corpus and literature

Original immutable restricted checker: experiments/arc/lspv2_386_independent_verify.js, Git blob **338305c0ce101704205e57543756b8127074a986**. Original accepted W29 certificate: results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json, blob **318c52d99977ea4e91bc8554051138a700c1dc94**. Independent signed source: results/raw/arc/2026-11-11_0812_LSPV2_559_EXTERNAL_K4_SIGNED_SOURCE.cnf, blob **e8bc4300f1f4518cb447edaf3f699bcee4839803**.

Reviewed both complete root trackers (proof1.txt and proof2.txt), issue #3, AGENTS.md, CODEX.md and the repo pnp-research skill; latest role handoffs and actual LSPV-1/539, /541, /549, /559, /590, LSPV-2/574, LSPV-3/588, LSPV-4/561 and LSPV-5/503 coordination findings. Earlier LSPV-1/571, LSPV-4/542, LSPV-5/491, LSPV-1/590 and LSPV-2/574 already established the **ownerless** embedded shift mutation defect. The **additional result** here is the terminal-pivot fixed-number collision and the complete necessary-and-sufficient characterization of all eleven original negative tests, not a claim to have discovered mutation testing or alpha renaming.

Primary research: [1] Cook and Reckhow, JSL 44 (1979) 36-50, https://doi.org/10.2307/2273702; [2] Cousot and Cousot, POPL (1977), https://doi.org/10.1145/512950.512973; [3] Clarke et al., CEGAR (2000), https://doi.org/10.1007/10722167_15; [4] Urquhart, Hard Examples for Resolution, JACM 34 (1987) 209-219, https://doi.org/10.1145/7531.8928. These provide methodology and restricted complexity results, not authority to fill historical mixed-rule grammar gaps.

## Theorem 591.1: Exact acceptance predicate for the complete /386 CLI

Let $D$ be any ordinary JSON packet considered by the pinned original checker. Let $C(D)$ mean that the unchanged original mathematical function checkProof(D,{control:true}) succeeds. Let $G(D)$ be its declared paid gate-owner array, and let $p_{\rm last}(D)$ be the last proof record's pivot. Let $\operatorname{CLI}_{386}(D)$ be success of the *whole* original command-line executable, including its eleven internal hostile mutations.

$$
\boxed{\operatorname{CLI}_{386}(D)=\mathrm{ACCEPT}
\iff C(D)\land |G(D)|\ge1\land p_{\rm last}(D)\ne999999.}
$$

**Proof:** The original runner checks $C(D)$ before generating mutations. In any core-accepted packet the last record is a strict binary Resolution with empty conclusion: no authenticated SOURCE is empty and no conservative AND2 defining facet is empty. For a strict resolvent to be empty, the parents must be opposite singleton clauses $[p]$ and $[-p]$. Hence the first hostile mutation assigning terminal pivot 999999 is accepted by the mathematical core precisely if the original pivot was already 999999; in every other case its signed pivot test rejects. The fourth hostile mutation removes the first paid owner. It is a no-op precisely when no owner exists; otherwise the remaining owner count disagrees with the unchanged paid_gates summary and mathematical checkProof rejects (possibly at an earlier dependency check).

Every one of the other nine hostile mutations **always** fails on a core-accepted packet. Replacing the final empty clause by [123456] loses terminal contradiction; changing the first record to [-guard] violates its original SOURCE or DEF typing (and the first record cannot be RES); replacing the last parent index by records.length+1 violates prior-parent ordering; decrementing paid_total violates its exact equation; toggling charge[0] changes required odd total charge parity to even; relabeling the terminal empty RES as SOURCE violates source authentication; replacing graph edge zero by edge one creates an illegal duplicate; replacing the first clause by [0] fails the canonical clean-clause predicate; and setting guard equal to the number of graph edges fails guard>edgecount. These are exactly all eleven original hostile mutations. Therefore their universal rejection, conditional on core acceptance, is equivalent to both additional displayed predicates. The unchanged runner has no further acceptance tests. QED.

The theorem concerns *implementation acceptance*, not logically necessary paid definitions. Do not turn a nonempty-owner CLI sentinel into a mathematical minimum-work bound.

## Corollary 591.2: Source-isomorphic guard labels with a sharp rejection hole

Let the pinned original odd-K4 source $F_7$ have six edge variables, independent source guard 7, 17 source occurrences, 28 terminal-live RES records, one terminal-dead but actually paid AND2 owner $(0,8,1,4)$ and $W=29$. For every safely represented integer $g>6$, $g\ne8$, independently define the caller signed CNF $F_g$ by consistently replacing *every* literal $\pm7$ with $\pm g$ and retaining the external occurrence list and all signed original edge literals. Let $P_g$ be the corresponding complete certificate renaming; normalize signed clause order, rebase the terminal Resolution pivot and preserve the same paid owner, its definition and all proof parent indices.

The external-source signed match is checked separately, not inferred from the certificate. All these CNFs are equivalent under variable renaming, plus irrelevant dummy identifier slots when $g$ is large. Direct inspection of the original core shows that $C(P_g)$ succeeds, with exactly 28 paid RES and one paid owner, for every such $g$: the source graph, charges, parity enumeration, source occurrences and strict RES rule are preserved. By Theorem 591.1,

$$
\boxed{\operatorname{CLI}_{386}(P_g)=\mathrm{ACCEPT}\iff g\ne999999.}
$$

The independently rebased $P_{999999}$ is a concrete core-valid W29 refutation rejected only by the original **wrapper** because the first hostile mutation writes the same terminal pivot that is already there. By contrast $P_{999998}$ and $P_{1000000}$ are full-CLI accepted at precisely the same charged work. This is cross-source alpha equivalence, **not** byte-identical fixed-source root substitution. The prior conditional LSPV-1/541 nominal theorem fixes its original source and assumes equivariance, so its theorem is not contradicted.

## Actually executed replay and reproducible artifacts

The exact original checker was invoked in hosted V8 with only file-read, console and output-only digest adapters; its mathematical checking and eleven CLI hostiles were unmodified. **23/23** independent source-rebased guard cases passed the original mathematical core at W29. The original complete CLI accepted **22/23** and rejected precisely guard 999999 as predicted. Every positive CLI replay passed its eleven negative tests and reported 3,542 original assertion groups. Zero-owner W28 remained core accepted but CLI rejected; signed-source corruption, underpayment and wrong guard binding were all rejected.

- Reproducer: experiments/arc/lspv1_591_native386_cli_sentinel_domain.cjs. Syntax verified; **real operating-system Node subprocess execution has not been performed in this run**. Its future executions require the exact two known original Git blobs and perform OS Node subprocess calls.
- Hosted-original raw data: results/raw/arc/2026-11-12_0556_LSPV1_591_NATIVE386_SENTINEL_DOMAIN_HOSTED_RAW.json.
- Exact JSON core-valid/CLI-rejected packet: results/raw/arc/2026-11-12_0556_LSPV1_591_GUARD999999_CORE_ACCEPT_CLI_REJECT.json.
- Independently transported signed source: results/raw/arc/2026-11-12_0556_LSPV1_591_EXTERNAL_GUARD999999_SIGNED_SOURCE.cnf.

## Dependency and falsification ledger

**P2-D1 OPEN:** this adds one exact native accepted-byte restriction to the archived /386 sibling checker. That checker recognizes SOURCE, conservative paid AND2 owners, zero-extra-cost DEF facets and strict RES only. The separately archived /341 SOURCE/AND3/GF(2) fixture checker does not complete it; neither handles all historically declared LOCAL-CONVERT, cross-rule transitions, private/exported wires, branch assumptions, discharge, joins, deletions or context rules. Unknown genuine actions remain MAY, not silently excluded or replaced by CANON1/2/2R.

**P2-C3 OPEN:** if the analysis goal is *full CLI acceptance*, abstract states must include predicates tracking nonempty paid-owner bank and the terminal-pivot sentinel, or conservatively overapproximate missing distinctions. If the analysis goal is mathematical refutation, it must use a sound, complete semantic rule system and **not** charge ancillary CLI hostiles as logically required. CEGAR can discard a refuted cheap path only upon genuine checker replay and sound refinement; it must retain real proof shortcuts.

**P2-B1 OPEN:** no full-calculus superpolynomial minimum follows. **P2-B2/B3 separately OPEN:** no polynomial same-calculus transfer or deterministic SAT decision-time lower bound is shown. Free optimal choice of whole shared paid DAGs, paid-node identity charged once, AND obligations and assumption discharge remain mandatory. This test's W29 is logical work, not evidence bits, proof discovery, checker time, span or peak memory.

**Proposed tracker addition:** P2-L1-591 exact restricted original CLI acceptance predicate; P2-D1/P2-C3/P2-B1/B2/B3 stay OPEN. **Independent LSPV-5 falsifier:** run the published original-checker OS reproducer and find any ordinary core-accepted live-owner-chain packet violating the two-condition CLI criterion. No role, original schedule, historical weight or 2 Route A / 3 Route B assignment was changed.

**P versus NP remains OPEN.**
