# Allender MajMajSAT integration: five-agent directive

Date: 2026-11-15, America/Los_Angeles.
Status: user-authorized research priority. P versus NP remains OPEN.

## Priority and continuity
All five existing TMR agents must investigate potential solutions incorporating Allender et al.'s time-space lower bound and its bounded-error quantum extension. This is the first scientific priority on upcoming runs. Integrate the existing fusion-Lipschitz program wherever an explicit mathematical connection exists. Unconnected toy-calculus variants are not the main deliverable.
Read this directive FIRST, then the 2026-11-14 fusion directive, the 2026-11-13 TMR replacement, current root trackers/main, all current handoffs, issue #3 and repository protocols. Preserve identities, titles, enabled states, ownership, history and Pacific hourly offsets :00/:12/:24/:36/:48. Do not create or revive scheduled agents. This priority supersedes conflicting older allocations; all scientific and publication safeguards remain.

## Verified starting points
Allender, Koucky, Ronneburger, Roy and Vinay, Time-Space Tradeoffs in the Counting Hierarchy (CCC 2001), Theorem 7: for every fixed 0<sigma<1 there exists gamma(sigma)>0 such that MajMajSAT is not in PrTiSp(N^(1+gamma),N^sigma). N is encoded input length. This is uniform unbounded-error probabilistic simultaneous-resource class noncontainment, not a universal pointwise or almost-everywhere runtime assertion. Section 3.2 uses quasilinear-size locally computable reductions. Majority means at least half in this paper.
Source: https://people.cs.rutgers.edu/~allender/papers/tradeoff.pdf
Record: https://eccc.weizmann.ac.il/report/2001/041/

Van Melkebeek and Watson, Time-Space Efficient Simulations of Quantum Computations (Theory of Computing 8, 2012), Theorem 1: bounded-error quantum time t, space s is simulated in unbounded-error probabilistic time O(t log t), space O(s+log t), with the stated constructibility/amplitude assumptions; algebraic amplitudes suffice. Fixed exponent slack absorbs logarithmic overhead. The quantum extension is theirs, not originally Allender et al.'s; arbitrary unbounded-error quantum machines are not covered automatically.
Source: https://www.cs.memphis.edu/~twwtson1/papers/qts.pdf
Record: https://theoryofcomputing.org/articles/v008a001/

Reconstruct primary proofs before relying on exact parameters; do not invent numerical gamma.

## Common objectives
1. Reconstruct the arithmetic Nepomnjascii speedup and hierarchy contradiction, seeking a stronger speedup, valid transfer, or precise bottleneck lemma.
2. Use MajMajSAT as an external calibration target for model coverage and cost soundness. Known hardness does not construct local tariffs, a large abstract potential or an explicit hard family.
3. Develop a fully charged conditional compiler from a stated SAT algorithm hypothesis to a forbidden MajMajSAT resource pair. SAT -> MajMajSAT is the wrong reduction direction for transferring this hardness to SAT.
4. Investigate amplification only with complete induction, same-realization resources and explicit losses. A fixed superlinear exponent is still polynomial; the small-space restriction cannot be discarded.

## Role assignments
### PNP Machine Model Lead
TMR-1: Reconstruct Allender Theorems 3-7: arithmetic Nepomnjascii speedup, counting-hierarchy collapse, diagonalization and local completeness reductions. Verify exact models/quantifiers and gamma dependence. Develop the weakest explicit conditional bridge from a stated SAT algorithm hypothesis to a forbidden MajMajSAT time-space pair. First deliverable: sourced dependency ledger and one proved bridge fragment or falsifier.

### PNP Information Necessity
TMR-2: Investigate threshold-preserving MajMajSAT-to-SAT constructions and counting obstructions connected to fusion. Preserve both majority blocks, denominators and ties. Test auxiliary variables, unique-extension dilution, affine controls, padding and compact representations. First deliverable: one exact construction with resource ledger, or a minimal counterexample and narrowed bridge. Do not assume hardness survives a restricted family.

### PNP Time-Space Tradeoffs
TMR-3: Derive reduction/simulation exponent budgets, including query generation, virtual-input accesses, retained state and aggregate network workspace. Audit quantum simulation O(t log t), O(s+log t), with exponent slack. Separate parallel span from sequential work. First deliverable: checked quantitative forbidden-region ledger and one source-justified speedup/slowdown chain or exact obstruction.

### PNP Cost-Sound Abstraction
TMR-4: Connect configuration-path arithmetic and hierarchy speedup to the vector-tariff/zero-cost framework. Preserve majority/probability semantics. Separate concrete-to-abstract undercharging from the reverse reconstruction needed to infer abstract hardness. First deliverable: explicit scoped simulation lemma or legal shortcut; do not extract local tariffs or explicit hard families from class noncontainment.

### PNP Machine Bottleneck Redteam
TMR-5: Independently reproduce and challenge the other four integrations. Audit reduction direction, fixed exponent versus superpolynomial claims, quantum error/amplitude assumptions, padding, shared work, aggregate space, uniformity, hardwired families and potential circularity. First deliverable: independent reproduction or counterexample, ranked dependency map and strongest surviving next lemma.

## Quantitative starting ledger, CONDITIONAL
For a deterministic exact sequential reduction using at most N^b calls of length at most N^a to a target solver with exponents (t,s), total overhead time N^r and retained reduction space N^u:
- Materialized queries: time exponent max(r,b+a*t), space exponent max(u,a,a*s).
- Virtual queries: if each input access costs N^h and the evaluator/state/address space is included in u, time exponent max(r,b+a*t+h), space exponent max(u,a*s), plus logarithmic bookkeeping.
These are conditional bookkeeping templates, not established compilers. Account separately for all model simulation overhead. With suppressed logarithms, seek strict time exponent <1+gamma(sigma) and space exponent <sigma for the SAME execution. Probabilistic/quantum subroutine composition requires an additional error-semantics theorem; tiny unbounded-error biases cannot simply be amplified for adaptive calls.

For processor networks, count total work and all live work tapes, buffers, scheduler state and messages. Per-processor space and parallel span cannot stand in for aggregate space and sequential simulation time. A single-tape simulation may have substantial extra cost.

## Mandatory falsifiers
- P=NP alone supplies neither exact majority counting nor the required near-linear/sublinear-space implementation.
- Count-preserving unique extensions need not preserve majority fractions. Preserve both quantifier blocks and tie conventions.
- Polynomial padding changes time and space exponents and the language; it does not manufacture amplification.
- Do not interchange forall algorithm / exists hard input with one common explicit family. Retain finite-hardwiring and efficiently labeled-family controls.
- Keep quantum bounded error, amplitude precision, uniformity and constructibility explicit.
- Class noncontainment does not certify that an overapproximating abstraction has no cheap spurious path. A free answer edge is a useful reverse-reconstruction falsifier.
- A probabilistic shortest accepting branch does not capture majority acceptance; a quantum extension must respect interference through a valid simulation.
- Minimum remaining work is a circular potential unless its initial value is independently bounded.
- Keep real compact algebra, sharing, caching, recomputation and all legal transitions.
- Historical /341 remains FAIL as a full UNSAT authority; /386 remains RESTRICTED.

## Deliverables and publication
Each run states one candidate and 2-4 falsifiers, reviews primary sources and relevant project originals, and produces a substantive lemma, quantitative tradeoff, construction, counterexample or independent reproduction. Surveys alone are insufficient.
Publish Pacific-timestamped work under existing research/agents/tmr-i paths, with separate executable/raw evidence where relevant; update handoffs, verify readback and follow existing issue #3 practice. Preserve SHA-safe shared edits and ownership. Change root main/proof trackers only for verified material changes; otherwise TRACKERS REVIEWED; NO MATERIAL CHANGE.
This is a coordination update, not a theorem-promotion report. Current five handoffs were consulted; their fusion, Cartesian-mutant and physical-frontier results remain restricted. Full research preflight/corpus reconciliation belongs to substantive agent runs. No repository-wide preflight or test execution is claimed here.
