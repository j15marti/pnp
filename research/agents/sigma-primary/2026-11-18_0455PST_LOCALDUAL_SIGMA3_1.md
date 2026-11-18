# LOCALDUAL-SIGMA3-1 | 2026-11-18 04:55 PST

**STATUS: PROVED/EXACT for a restricted, source-certified, nonhereditary factorwise QBF evaluator; COMPUTATIONAL audit 98,244 assertion groups / 0 failures; no all-input Circuit-SAT contraction. P versus NP OPEN. Independent mathematical review pending.**

## PROPOSE
1. Replace enumeration of all universal challenges by a **local counterchallenge Circuit-SAT guest**, expanding only each factor's bounded post-universal existential bits.
2. Allow **arbitrary shared universal variables across factors**, while insisting that post-universal existential witnesses are private to their respective factors. Keep one globally committed outer x.
3. Stream the physical tagged source once per x, without retaining q source offsets, and build actual ordinary Circuit-SAT counterexample circuits one at a time.
4. Red-team shared existential cutsets, illegally adaptive global x, early deterministic traces, full-parent padded guests, reconvergence, affine and nonaffine controls, source replay and recursive eligibility.

## SEARCH
Direct repository reads included sigma-primary/2026-11-18_0303PST_SIGMA_PATHCUT_1.md, sigma-redteam/2026-11-18_1216Z_SIGMA29_STREAMING_SEPARATOR_FIREWALL.md, sigma-redteam/2026-11-18_1202Z_SIGMA28_UNIFORM_PROJECTION_GATE_TRACE.md, sigma3-strategy/2026-11-18_0626KST_SIGMA3_FIBER56.md, plus repository searches for factorwise universal/counterchallenge compilation and grid-width barriers. This differs from PATHCUT: **the universal block need not be logarithmic**; there is no shared post-universal separator at all. It differs from generic QBF expansion: only the bounded local existential response is expanded, not the universal challenge. This is classical quantified Boolean algebra and bounded expansion specialized to our resource ledger; no claim of a new general complexity theorem.

Primary literature: Fortnow, Lipton, van Melkebeek, Viglas, JACM 2005 https://doi.org/10.1145/1101821.1101822 ; Williams, STOC 2024 https://doi.org/10.1145/3618260.3649723 ; Kattermann, Hofstadler, Seidl, *Definition-Based Dependency Schemes*, SAT 2026 https://drops.dagstuhl.de/storage/00lipics/lipics-vol377-sat2026/html/LIPIcs.SAT.2026.22/LIPIcs.SAT.2026.22.html ; Bubeck & Kleine Buning, *Bounded Universal Expansion for Preprocessing QBF* (SAT 2007), https://www.ub-net.de/cms/fileadmin/upb/doc/bubeck-bounded-expansion-sat-2007.pdf . These works establish relevant dependency and expansion principles, not the desired all-input exponent reduction.

## Theorem: source-streamed local-counterchallenge contraction (restricted)

Consider the tagged N-bit source of a three-block QBF

    Phi = exists x forall y exists z_1,...,z_q : AND_{i=1}^q C_i(x,y|Y_i,z_i),

where each C_i is a valid output-connected or arbitrary acyclic AND/OR/NOT circuit, all z_i names are **syntactically private**, and x is the only cross-factor existential sharing. A universal y bit may appear in any number of factors; local referenced universal sets Y_i may overlap arbitrarily. Let `ell_i` denote the encoded length of the i-th factor including identifiers. Assume q<=N^theta, |x|<=beta log_2 N, |z_i|<=delta log_2 N, and every materialized locally pinned/expanded counterexample circuit below has encoded length <=N^(lambda+o(1)). This last requirement is source-checkable using `2^|z_i| ell_i polylog N`; a sufficient bound is ell_i<=N^(lambda-delta-o(1)). Take fixed K>=1 and L>=0 for any correct deterministic ordinary Circuit-SAT A.

For each x and factor i construct the actual ordinary Boolean circuit over just the factor's local universal input pins:

    D_i[x](y|Y_i) = AND_{a in {0,1}^{|z_i|}} NOT C_i(x,y|Y_i,a).

Then, with one real call to A per D_i[x] (including negative answers),

    Phi is TRUE iff exists x such that for every i, A(D_i[x]) = UNSAT.

The algorithm's fully charged asymptotic bounds in the ordinary source-streaming random-access-input/work-tape realization are

    K' <= max(1+beta, beta+theta+lambda, beta+theta+lambda*K)+o(1),
    L' <= max(lambda, lambda*L, lambda-delta)+o(1).

No q-entry writable offset table is kept. Source validation checks local z namespaces, factor scopes, individual gate DAGs and tags, and repeats the full source scan for each x. Local universal names are reindexed to compact guest inputs. Guest construction includes 2^|z_i| copies, output AND, pin/renaming, physical serialization, solver input tape, work tape and reset; only one guest remains live. Negative SAT outputs are treated as actual A answers, not free certificates. Access, copying, encoding and worst-case invoked work-address are charged.

Taking theta=11/20, delta=1/20, beta=1/50, lambda=1/2, with factor size <=N^(9/20+o(1)), gives

    K'<= max(51/50, 107/100 + (K-1)/2)= 57/100 + K/2 (K>=1),
    L'<=max(1/2,L/2).

That is a **3/100 time-exponent margin** relative to the required `max(11/10,3/5+K/2)` for all K>=1, but ONLY on this certified factor class. [In the first display, all three terms are retained to make source rescanning visible.]

### Proof
For every fixed x and y, independent private z_i satisfy `exists z_1,...,z_q AND_i C_i` iff `AND_i exists z_i C_i`. Universal quantification distributes over the finite conjunction, even if universal bits occur in multiple factors. Thus `forall y exists z-vector AND_i C_i` iff `AND_i forall y|Y_i exists z_i C_i`. Each latter obligation fails iff some local y assignment satisfies `AND_a NOT C_i(x,y,a)`; this is exactly ordinary Circuit-SAT on D_i[x]. A single global x is chosen before all such checks.

For resource costs: at most N^beta outer choices, each scanning N source bits (N^(1+beta) time) and evaluating q<=N^theta guests. Each guest has length at most N^lambda and requires O(N^lambda polylog N) generation work, N^(lambda*K+o(1)) guest time and O(N^lambda+N^(lambda*L+o(1))) live space. The factor-source scratch is <=N^(lambda-delta+o(1)); indexes/loop counters are logarithmic. Input source length is N and is not duplicated in counted work space. This proves the displayed recurrence under the stated streamable machine conventions; formal external model transfer remains to be independently checked.

## Counterexample, limitations and exact resource firewall
* **Shared z destroys factorwise independence:** For a universal y and a single common z, take C_1=(z=y), C_2=(z=NOT y). Both factors separately satisfy forall y exists z C_i, but their conjunction is FALSE. No free existential splitter or independent local traces.
* **Outer x must remain fixed:** exists x forall y [x=y] is FALSE, while forall y exists x [x=y] is TRUE.
* **Unique traces remain adaptive:** forall y exists z [z=y] TRUE; exists z forall y [z=y] FALSE.
* **Guest blowup:** literal expansion of d_i local existential bits can multiply physical circuit length by 2^d_i. If factors already occupy N^(1/2), d_i=(1/20)log N makes guests N^(11/20), outside the half-size target. Restricting the factor length to N^(9/20) is essential for this compiler; algebraic sharing could change the cost but is not assumed.
* **Padding, reconvergence, affine shortcuts and source replay:** these may yield faster specialized algorithms. None is used to claim a necessary SAT lower bound.
* **Large universal dimensions:** local y sets may have many bits. They remain symbolic inputs to D_i, so there is NO 2^|y| universal enumeration. Source input indices must be compactly reindexed within each factor.
* **Nonheredity:** ordinary D_i children do not necessarily admit the same factor grammar. Nothing defines Phi(A) for all ordinary Circuit-SAT sources, and no all-input iterability, FLMV contradiction or P!=NP follows.
* **A_D padding:** on actually reached size-N^(1/2) guests an artificially delayed solver with exponent D contributes N^((1/2)D); a reached full-parent-size call would contribute N^D and invalidate this particular recurrence for large D. The present compiler makes no full-parent A calls.

## Executable falsification (finite, not native asymptotic measurement)
Local standard-library script: `localdual_sigma3_audit.py`, raw output `localdual_sigma3_results.json`, package `LOCALDUAL_SIGMA3_1_20261118_0455PST_bundle.zip`.

* 700 seeded physical AND/OR/NOT factor circuits (159 TRUE, 541 FALSE) compared brute-force quantified semantics with the compiled ordinary-SAT counterchallenge evaluator, with actual source parse/replay and guest serialize/decode.
* 3,758 actual finite guest-evaluation invocations, including negative answers.
* All 65,536 ordered pairs of 3-input factor truth tables (r=m=d=1) checked for exact factoring under independent post-universal witnesses: 34,911 true pairs.
* Shared-witness, global-outer-commitment, adaptive trace, disjoint nonaffine relation and 100 output-equivalent double-NOT transformations audited.
* **98,244 assertion groups passed, zero failures.**
* A syntactically output-connected, 500-gate/factor, 20,000-factor deterministic source template has byte-exact calculated encoded length **72,088,890 ASCII bytes**, counterexample guest **7,279 bytes**, q<=N^0.55 and guest size<=sqrt(N), even interpreting N conservatively as byte count. Its large source was *counted, not allocated/executed*. This establishes nonempty geometric feasibility, NOT semantic irredundancy, SAT hardness or actual runtime bounds.

## Handoff
Next attempt: find a **source-certified bounded-overlap of post-universal existential scopes** with nontrivial shared variables that still admits *small ordinary counterexample Circuit-SAT children*. Explore bounded interface c: `forall y exists c AND_i exists z_i C_i` has incorrect factorwise decomposition because c must be shared within each y. Audit literal `AND_c OR_i D_i` expansion size and whether it breaks the N^(1/2) guest cap. Keep SIGMA28/29, GRAPHPAIR, SCHAEFERGUARD, TRACEMOVE and PATHCUT as mandatory adversaries. Do not infer PH collapse gives the required numeric exponents.

**P versus NP OPEN.**
VERIFICATION_SENTINEL_LOCALDUAL_SIGMA3_20261118_0455PST
