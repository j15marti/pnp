# User-directed total proof review and two-gate refocus

Date: 2026-11-13, America/Los_Angeles. Owner: LSPV-1. Status: PROVED conditional composition theorem; COMPUTATIONAL independent source satisfiability check; unrestricted conclusion OPEN.

This is a project review and coordination directive requested by the user, not a claim that any principal proof-chain node has closed. Preserve exactly the five current identities, titles, schedules, timezones, ownership regions, historical rules/weights and two Route A / three Route B allocation. No new calculus is authorized by this review.

## Candidate and falsifiers

Candidate: a full native cost-sound abstraction plus a family-restricted same-calculus transfer theorem and a superpolynomial abstract lower bound suffice to separate P from NP. Neither a fixed-calculus lower bound alone nor expensive encodings of one cheap proof suffice.

Falsifiers of an attempted application: (1) a legal cheap native refutation of the proposed hard family; (2) an omitted accepted operation or unsound original-source inference; (3) abstract overcharging of shared nodes, lost assumptions or unfulfilled AND obligations; (4) a nonpolynomial, circular or different-calculus algorithm-to-proof translation.

## Progress assessment

The reviewed ledger retains P2-D1, P2-C3, P2-B1 and the independent P2-B2/B3 obligations as OPEN. proof1.txt remains a conditional model-specific route, not a polynomial-time SAT algorithm. Historical restricted lemmas and accounting counterexamples are useful controls, not a completed unrestricted chain.

The most decisive current source is research/agents/lspv-3/2026-11-13_1128_LSPV3_620_D1_QUALIFICATION_DUAL_CHECKER_GATE.md, read at blob 17ed3d10ec41d940af0e5138b1a77057968d51e6. It reports that the unchanged recovered /341 checker accepts a packet containing a satisfiable in-band 48-clause source. It distinguishes this from /386, which checks a guarded odd-charge cubic Tseitin source domain, not arbitrary 3-CNF. The complete historical mixed dispatcher remains unidentified. Acceptance, original-source entailment, closed refutation and input coverage are four separate claims.

Independent execution in this review authenticated the exact signed CNF at results/raw/arc/2026-11-13_1128_LSPV3_620_ACCEPTED_341_SAT_SOURCE.cnf, Git blob c6f8bbf09baf6547de6fea04ac74dd0ecb32f6bd. Exhaustive enumeration of all 262144 assignments found exactly 64 models and verified x1-through-x18 witness 101001000000100000. SHA256 of the CNF is 40b5b52d276bfe17edfe8eb82be7fd5c58a735304263dbb5b0097f9d860110c7. This independently verifies SAT, not native checker acceptance. The latter is evidence reported by /620 and remains an immediate independent replay assignment.

An abstraction that preserves a genuinely accepted SAT-source refutation cannot simultaneously interpret every such acceptance as a sound UNSAT proof. That is a semantic qualification failure, not a spurious abstract path that CEGAR may delete. If the unsound program is definitively the frozen authority, reject that candidate for the intended logical route. Recovery of a different authentic historical authority must be demonstrated; repairs or new systems must never be relabeled as the old one.

Results 621-623 distinguish logical work from raw-index languages, lexical bytes and byte-query costs. Even correct versions do not establish growth of optimal whole-DAG work on growing source instances. If one proof of F costs c, arbitrary padding of its encodings leaves the bound Wbar_R(F) <= c intact. Stop standalone padding variants unless they close a named prerequisite.

## Best remaining chain: two early gates

Gate S: P2-D1, authenticate the exact native calculus, complete accepted operations, source domain, original-input binding, soundness and proof coverage for the selected family. Conservatively include genuinely unknown operations in abstraction, but do not certify semantic soundness from provenance alone.

Gate T: P2-B2/B3, independently prove transfer to that SAME fixed calculus from a hypothetical arbitrary polynomial-time SAT decider. Investigate this in parallel with Gate S. Do not wait for a difficult calculus lower bound before discovering that it has no implication for arbitrary algorithms.

After Gate S, P2-C3 must cover all legal source-authenticated shared-DAG transitions at no greater abstract cost. P2-B1 must lower-bound every abstract accepting path on an explicit family and exact input encoding. Combine only with Gate T. The algorithm branch remains open to a correct all-input polynomial-time SAT algorithm with a complete bit-time analysis; a quasipolynomial algorithm alone does not settle the equality question.

## Conditional theorem with the weakest necessary family bridge

Fix one sound native calculus R with its authentic fixed tariff. Let F_n be explicit unsatisfiable 3-CNFs of encoded lengths N_n tending to infinity. Require at least one legal closed R-refutation for each F_n; lack of expressibility is not hardness. Define

$$
\overline W_R(F_n)=\inf_{\pi\text{ legal closed R-refutation of }F_n}\sum_{v\in\operatorname{Paid}(\pi)}w_R(v).
$$

Each distinct shared paid identity is counted exactly once, with free optimal proof selection. Concrete configurations retain the full source-authenticated DAG, definitions, paid history, freshness, source provenance, active/discharged assumptions and all native obligations. Costs of deletion, reuse or recomputation must follow authentic identity semantics, not a convenient invented schedule.

Assume an initial-state relation and an abstract transition system such that, for every related concrete/abstract pair and every concrete transition, a finite abstract path reaches a related successor at cost no greater than that concrete transition. Every completed concrete refutation must map to an abstract accepting goal. This quantifies over all native transitions, not just those used by a preferred proof search. Zero-cost transitions and sharing are included.

Suppose a real-valued abstract potential satisfies, for every abstract edge a -> b of nonnegative cost d,

$$
\Phi_n(a)\le d+\Phi_n(b),
$$

and every abstract accepting goal g satisfies Phi_n(g) <= 0. Suppose the initial potential exceeds every polynomial infinitely often:

$$
\forall k\in\mathbb N\ \forall n_0\ \exists n\ge n_0:\quad \Phi_n(a_{0,n})>N_n^k.
$$

Finally require the separate family-restricted bridge

$$
\mathrm{SAT}\in\mathrm P\ \Longrightarrow\ \exists C,d,n_0\ \forall n\ge n_0:\quad \overline W_R(F_n)\le C N_n^d.
$$

Then P != NP.

Proof. Simulate any finite concrete refutation by concatenating the step-simulation paths. Telescoping the potential inequality gives initial potential <= abstract path cost + final potential <= abstract path cost <= concrete whole-DAG cost. Taking the infimum over all legal concrete proofs gives Phi_n(a_0,n) <= Wbar_R(F_n). If SAT were in P, the bridge supplies constants C and d. Choose integer k>d and an arbitrarily large n from the potential condition, with N_n^(k-d)>C. Then Wbar_R(F_n)>N_n^k>C N_n^d, a contradiction. SAT's NP-completeness yields P != NP. QED, conditional on all stated premises.

The proof of this implication is complete; the native soundness/coverage, all-step simulation, superpolynomial potential and bridge premises are not proved. It is a proof-obligation specification, not a new complexity separation.

The family bridge is weaker than a universal compiler for all formulas or a p-optimal proof system. A sufficient stronger constructive target is: for every correct deterministic SAT decider A, constants c_A,r_A independent of F_n and same-R proofs satisfying Wbar_R(F_n) <= c_A*(N_n+T_A(N_n))^r_A. A verified computation transcript does not by itself prove that the transcript's rejecting output entails UNSAT in R. An external correctness theorem, uncharged truth table, oracle or different proof system cannot fill that step. Existence of suitable short native proofs suffices for the contradiction; efficient discovery is a separate stronger claim.

## Growth target

For fixed c>0, N^((log N)^c)=exp((log N)^(c+1)) is quasipolynomial and superpolynomial. These are not competing categories. A proven lower bound of that form would suffice with the bridge. An upper bound of that form does not exclude a polynomial algorithm. A fixed N^(1+epsilon) lower bound also does not exclude all polynomial algorithms. Input bit length must not be silently exchanged with variable or clause counts. Exact optimal running-time classification is not needed to prove P != NP.

## Five-role assignments, boundaries unchanged

LSPV-1, Route B: own the exact master theorem, family/encoding, quantifiers, potential target, dependency ledger and contradiction. Require independent review before any gate promotion. Target a genuine whole-calculus potential or a legal counterexample, not another byte-padding lemma.

LSPV-2, Route A: own executable same-calculus compiler/transfer constructions and shortcut controls. Pin every native rule implementing each translated inference. Attack the missing reflection step from a correct decider's rejecting computation to a source-bound refutation. A family-restricted bridge is sufficient; do not silently demand or assume global proof-system optimality.

LSPV-3, Route B: retain ownership of P2-D1 and the accepted-byte corpus. Reconcile /620 against unchanged originals and recover the actual mixed authority, or publish a precise qualification failure. No repaired checker or independent reference implementation may be substituted. Establish source binding, local soundness and domain coverage separately.

LSPV-4, Route A: retain resource-audit ownership. Prove all-step cost-underestimating simulation, potential telescoping and whole-DAG count-once accounting, including zero-cost closure and deletion/reuse. Audit the quantitative bridge and distinguish proof work, evidence bits, discovery, verification time, span and peak space.

LSPV-5, Route B: independently execute the original /341 and /386 controls in an OS process where available; verify source hashes and reproduce minimal SAT-source false acceptance. Independently attack every soundness, all-step, potential and transfer claim. A real legal cheap proof is retained as a falsifier; only a proved-spurious abstract path may be refined away.

## Retained mandatory workflow

Every run read both root trackers, issue #3, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, current five-role handoffs and actual relevant reports including 539-549 and later work. State one candidate plus 2-4 falsifiers before searching primary literature and project corpus. Produce a substantive theorem, counterexample, native certificate or independent verification. Keep accepted-byte grammar, fixed weights, shared paid identity, AND obligations, assumption discharge and free optimal proof choice intact. Include all legal GF(2), extension, learning, preprocessing, branching, sharing, reconvergence, compact-circuit and algebraic shortcuts. No uncharged oracle, answer table or model switch.

Publish dated role-owned report, reproducible code/raw evidence and concise handoff; post exact affected IDs to issue #3. Update trackers only for material changes using complete current contents and SHA, conflict-safe merge and full readback. Respect main.tex ownership. Explicitly disclose absent sources and tests not run.

TRACKERS REVIEWED; NO MATERIAL CHANGE. This review leaves proof1.txt, proof2.txt and main.tex unchanged. It does not certify an exhaustive independent rerun of the historical report corpus. The independent execution is the source-SAT check above; full historical-checker replay and repository-wide preflight/LaTeX compilation were not performed here.

## Primary references consulted

1. Cook SA, Reckhow RA. The Relative Efficiency of Propositional Proof Systems. Journal of Symbolic Logic. 1979;44:36-50. doi:10.2307/2273702. Author-hosted original, including definition of polynomially bounded proof systems. A short-proof system existing under NP=coNP is not automatically this fixed R.
2. Cousot P, Cousot R. Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints. POPL. 1977:238-252. doi:10.1145/512950.512973. Primary author publication page.
3. Clarke EM, Grumberg O, Jha S, Lu Y, Veith H. Counterexample-Guided Abstraction Refinement. CAV. 2000:154-169. doi:10.1007/10722167_15. Primary CMU repository description of spurious-counterexample refinement.
4. Clay Mathematics Institute. P vs NP, official current unsolved-problem page, consulted 2026-11-13.

END_OF_REVIEW::LSPV-1::2026-11-13::TWO-GATE
