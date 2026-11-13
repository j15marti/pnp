# LSPV-1: User-directed full-chain review

Date: 2026-11-13, America/Los_Angeles (PST).
Role: LSPV-1 General SAT Lower-Bound Lead, Route B.
Status: CONDITIONAL COMPOSITION LEMMA PROVED; native hypotheses OPEN.
User request: review total progress, formulate the best remaining proof chain, and redirect the existing five roles toward a complete P versus NP proof.

## Scope and evidence discipline

This is a supervisory synthesis of the root proof ledgers, repository instructions, issue #3, and selected recent reports and ledger entries. It is not a fresh independent execution of every historical artifact, nor a claim that every line of the large historical corpus was inspected. No source-code experiment was rerun for this review. Reported historical executions retain the scope and limitations in their original reports. P versus NP remains OPEN.

Core evidence reviewed includes proof2.txt blob 930c5eeddafce656717f28055a7a9a755f44737c and the actual report research/agents/lspv-3/2026-11-13_0924_LSPV3_617_NATIVE386_SOURCE_DOMAIN_SOUNDNESS_NO_GO.md, blob 6dc55529fe8b501a95be12e779f747a537167e5dda. The ledger includes subsequent LSPV-2/619 and LSPV-1/621-623 entries. The substantive result here is the precise conditional composition theorem and its proof, not a new native-calculus lower bound.

## Candidate and falsifiers

Candidate: a lower bound on minimum abstract refutation cost separates P from NP if every native proof is represented at no greater abstract cost and every polynomial-time SAT decider yields polynomial-cost proofs in that same native calculus on the hard family.

Falsifiers to test before further invariant development:
1. Accepted bytes do not denote a valid source-bound closed refutation, because of source substitution, ignored source, handle rebinding, or undischarged assumptions.
2. A legal GF(2), extension, learned-clause, preprocessing, compact-circuit, sharing, or reconvergence proof has lower cost than the proposed invariant permits.
3. The proposed abstraction omits a legal transition, forgets a required context distinction, or charges a shared paid identity more than its authentic concrete charge.
4. The algorithm-to-calculus bridge assumes the lower bound, assumes short correctness proofs for arbitrary algorithms, restricts algorithms to a convenient portfolio, or changes proof systems without a proved transfer.

## Assessment of accumulated progress

The project has developed useful definitions, replay infrastructure, negative controls, and counterexamples to invalid inferences. These are not interchangeable with closure of the main separation dependencies.

The reviewed ledger still leaves P2-D1, P2-C3, P2-B1, and P2-B2/B3 open. No unrestricted superpolynomial minimum-work theorem or arbitrary-algorithm transfer was established by the reviewed recent results.

Report 617 establishes the source-domain limitation of strict archived /386: sourceCNF enforces odd-charge 3-regular Tseitin inputs. These accepted source instances are already UNSAT by parity. Rejecting a satisfiable even-charge input before proof verification does not demonstrate general-CNF source soundness. This does not itself establish that /386 is unsound. It limits what the tests establish. Its authenticated SOURCE/DEF/RES fragment also does not authenticate all historical mixed operations.

The same report and ledger record separate source/context failures for mixed candidates /421, /547, and /553. These remain reported historical findings in this review, not newly rerun experiments. A source-unbound or semantically unsound archived checker cannot silently be relabeled a sound fixed calculus. Repair or replacement would be a distinct version with fresh obligations.

Results 621-623 distinguish exact raw-index languages, certificate byte lengths, and byte-reading complexity from logical proof work. Their contribution is a resource firewall. They do not lower-bound minimum native proof work or arbitrary SAT decision time. If many encodings denote one proof pi of work w, then W_R(F) <= w regardless of their maximum byte length. Failure of a finite exact raw-byte quotient does not rule out all cost-sound MAY abstractions.

## Exact objective

Fix a single authenticated native calculus R, its source domain, checker semantics, and original nonnegative weights. For a formula F let Ref_R(F) contain all legal closed source-bound shared-DAG refutations, not merely the outputs of a particular search algorithm. Define

$$
W_R(F)=\inf_{\pi\in\mathrm{Ref}_R(F)}\sum_{v\in\mathrm{Paid}(\pi)} w(v).
$$

Each distinct authentic paid-node identity is counted once. Discovery, parsing, certificate bits, verification time, span, and peak space are separate resources. Missing refutations cannot be counted as hardness: an infinite value due to absent coverage is not a lower-bound achievement.

The concrete configuration must retain the whole relevant shared DAG, paid-history identities, source provenance, active and discharged assumptions, definitions, freshness state, exported/private interfaces, and any authentic deletion/recomputation semantics. A replay of a whole DAG must realize exactly its native logical charge. This is an obligation, not an already established fact for the incomplete historical mixed target.

## Conditional composition theorem

Let H = {F_i} be a family of UNSAT 3-CNF formulas with encoded bit lengths n_i tending to infinity. Fix R independently of the algorithm or input. Assume the following.

### S: Source and semantic qualification

R is source-bound and sound on its advertised domain, every F_i is in that domain, and every F_i has a finite R-refutation. Every genuinely accepted operation is included in the native relation, with its exact weights. No convenient replacement calculus is substituted.

### A: All-proof cost-sound abstraction

Initial configurations are represented. Every legal concrete step is simulated by an abstract transition or finite path, preserving the representation relation and with abstract cost no greater than the authentic incremental concrete logical charge. Every closed concrete refutation maps to an abstract accepting state. Define W_abs(F) as the infimum of costs of abstract accepting paths.

These requirements imply

$$
W_{\mathrm{abs}}(F)\leq W_R(F).
$$

Proof: take any finite legal whole-DAG refutation and a native replay realizing its logical cost. Starting with the represented initial state, apply step simulation inductively. Concatenate the abstract simulating paths. Goal preservation makes the final abstract state accepting. Summing the local inequalities gives an abstract accepting path of cost at most the original proof's work. Taking the infimum over all concrete refutations gives the inequality. A single proof-search strategy or selected corpus is insufficient for this argument.

### T: Independent same-calculus algorithm transfer

For each correct deterministic SAT decider M, there are constants c_M > 0 and r_M > 0, independent of i, and a source-bound native proof construction such that

$$
W_R(F_i)\leq c_M\bigl(n_i+T_M(n_i)\bigr)^{r_M}.
$$

Here T_M(n) is worst-case running time on inputs of length at most n in one fixed standard machine model. Every compiler step must be implemented by an authenticated native operation. A verified rejection transcript alone is not a native derivation from the input clauses. Any correctness premise for M must be discharged or explicitly accounted for, not supplied as an uncharged oracle.

Quantifier economy: an all-UNSAT-input transfer is a useful stronger target, and the automation directives retain it as the default. The separation theorem only needs transfer on H. Likewise, R need only have the required sound coverage on H for this theorem, although the project may not call a promised fragment the complete historical mixed calculus. A family-scoped result must still cover EVERY putative polynomial-time decider correct on arbitrary SAT inputs, not just algorithms specialized to H. This narrower sufficient target is not a model switch or permission to omit legal rules.

### L: Superpolynomial abstract lower bound

For every fixed k > 0, eventually

$$
W_{\mathrm{abs}}(F_i)>n_i^k.
$$

The weaker condition of such violations at arbitrarily large i for every k is also sufficient. A fixed superlinear exponent is not sufficient.

### Conclusion and proof

If a correct SAT decider M ran in time O(n^d), then A and T would imply

$$
W_{\mathrm{abs}}(F_i)\leq W_R(F_i)\leq C_M n_i^{r_M\max(1,d)}
$$

for a fixed constant C_M. Choosing k strictly larger than that fixed exponent contradicts L at sufficiently large n_i. Thus SAT is not in P, and NP-completeness of 3-SAT yields P != NP.

This proves the conditional composition, not S, A, T, or L for R_mix341. Those global native hypotheses remain OPEN. The final algebra is short; the hypotheses contain the actual difficulty.

## Growth target

Quasipolynomial and superpolynomial are not mutually exclusive. For fixed c > 0, n^((log n)^c) is quasipolynomial and exceeds every fixed polynomial. A quasipolynomial upper bound on SAT would not prove the absence of a polynomial algorithm. A suitable superpolynomial lower bound, even far below exponential, is sufficient after the transfer. No exact optimal runtime classification is necessary for separation.

All comparisons use encoded bit length, not unconverted variable counts, clauses, graph vertices, or padded certificate length. The current record does not justify choosing between quasipolynomial and exponential worst-case SAT complexity.

## Best remaining research organization

Retain the logical dependence D1 -> C3 -> B1, but run TWO early qualification gates in parallel:

Gate 1: D1, one authentic source-bound semantically sound calculus with the precise coverage needed by the theorem.
Gate 2: B2/B3, feasibility of a noncircular algorithm-to-that-calculus transfer.

Do not wait for a very strong proof-system lower bound before discovering that the system has no applicable algorithm bridge. Cook-Reckhow gives an existential statement about proof systems; it does not make an arbitrary fixed calculus polynomially bounded under SAT in P. Likewise, proof correctness in another formal system is not itself a transfer theorem.

For C3, require source/goal preservation and all-transition simulation. Conservative unknown operations may create cheap abstract paths. A real native shortcut must remain and defeats the corresponding candidate bound; only proved-spurious paths justify refinement. Finite experiment success is not an all-input lower-bound proof.

For B1, begin with explicit published encodings and their scoped lower bounds, then test all native shortcuts before investing in an invariant. In particular, a family difficult for Resolution may fail immediately under authenticated GF(2) or extension rules. The family is rejected as a candidate when a genuine cheap proof is found; the legal rule is not removed.

## Executed five-role redirection

The five existing automations were updated successfully by changing prompts and preserving enabled state. No title, identity, schedule, timezone, ownership boundary, historical rule/weight, or Route label was changed. No automation was created or duplicated.

- LSPV-1, Route B: exact theorem, quantifiers, dependency ledger, two early gates, and independent falsification requirements.
- LSPV-2, Route A: source-bound native compiler/replayer infrastructure and legal cheap-proof controls.
- LSPV-3, Route B: D1 qualification, accepted-domain and soundness manifest, cross-rule fixtures, original-source failure reproduction.
- LSPV-4, Route A: quantitative same-calculus transfer audit and all-step whole-DAG cost soundness.
- LSPV-5, Route B: independent adversarial audit of source soundness, transfer quantifiers, legal shortcuts, and abstract simulation.

The exact existing automation IDs are, respectively: 6ad6f02da1bc8191bfd844daded8e1ec; 6ad6f04620a881918aecb8078ce2f2d1; 6ad6f05603248191abb281a5b43b3fc2; 6ad42a1f03448191b8ded0c1f2dfa791; 6ad42a2a9a088191ab9042245f3b4393. The original hourly schedules and America/Los_Angeles timezone were retained.

Standalone lexical padding, large identifier, redundant zero-cost record, and byte-query variants are deprioritized unless they close a named main-chain obligation. A useful next result must be a proved native component, explicit legal counterexample, or decisive transfer obstruction, not another survey or relabeling of a restricted result.

## Publication and status

Affected IDs: P2-D1, P2-C3, P2-B1, P2-B2, P2-B3; P1 transfer/quantifier controls remain secondary.
TRACKERS REVIEWED; NO MATERIAL CHANGE. No load-bearing node is promoted. Root proof1.txt, proof2.txt, and main.tex are not edited by this review. Full independent historical replay and repository-wide preflight/LaTeX compilation were not performed.

## Primary references

1. Cook SA, Reckhow RA. The Relative Efficiency of Propositional Proof Systems. Journal of Symbolic Logic. 1979;44(1):36-50. Section 1, especially Propositions 1.1, 1.4, and 1.6. https://www.cs.utoronto.ca/~sacook/homepage/cook_reckhow.pdf
2. Cousot P, Cousot R. Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints. POPL. 1977:238-252. https://cs.nyu.edu/~pcousot/COUSOTpapers/POPL77.shtml
3. Clarke EM, Grumberg O, Jha S, Lu Y, Veith H. Counterexample-Guided Abstraction Refinement. CAV. 2000:154-169. DOI 10.1007/10722167_15. Author-institution archive: https://doi.org/10.1184/R1/6604547

The weighted conditional composition above is stated and proved here. These references establish the background framework, not the missing native-calculus premises.
