# TRACE-CORRECTNESS-FIREWALL-REFEREE294

**Role:** LSPV-5 Formal Proof Red Team  
**Time:** 2026-11-02 11:48 PST, America/Los_Angeles  
**Status:** PROVED/EXACT trace-soundness and fixed-theory coverage barriers; COMPUTATIONAL finite optima; universal derivation simulation, superpolynomial generalized proof lower bounds, and P versus NP remain OPEN.

## Claim card and accepted model

Fix before all instances one effective sound refutation system \(R\), including encodings, legal inference rules, justification checks, and nonnegative weights. For an UNSAT CNF \(F\), \(W_R(F)\) is the minimum total weight of distinct inference nodes in an acyclic refutation DAG. Shared derived nodes count once. Temporary growth, auxiliary variables, nonmonotone steps, memoization, recomputation, algebra, and representation switches are permitted when declared by \(R\). The best legal path is selected for free. This run does **not** charge proof search to \(W_R\).

The desired transfer is

\[
 \forall A\in\mathsf{TotalCorrectSAT}\;\exists p_A\;\forall F\in\mathsf{UNSAT}:
 \quad W_R(F)\le p_A(|F|+T_A(F)). \tag{TR}
\]

The obstruction is not optimizer discovery. It is the missing sound bridge from an arbitrary rejecting computation to an \(R\)-derivation.

## The trace-certificate trilemma

### 1. Trust a rejecting trace without a correctness premise

This rule is unsound. Let \(M_0\) immediately output UNSAT on every input. On satisfiable \(S=(x\vee y)\), its one-step trace is well formed. A rule accepting every rejecting trace derives contradiction from \(S\). Free optimal selection cannot repair an invalid rule.

### 2. Require a correctness proof in one fixed theory

This is sounder but cannot cover every extensionally correct decider.

**Theorem (fixed-theory coverage barrier).** Let \(T\) be a consistent, effectively axiomatized theory strong enough to formalize finite proof checking, bounded machine computations, CNF padding, and the standard derivability conditions. Let \(B\) be a fixed total correct SAT decider, including malformed-input behavior. There is a fixed total machine \(A_T\) such that:

1. externally, if \(T\) is consistent, \(A_T\) has exactly the same answers as \(B\) and is correct on SAT, UNSAT, and malformed inputs;
2. \(T\) cannot prove the standard all-input correctness statement for \(A_T\).

**Construction.** On input \(z\) of length \(n\), \(A_T\) simulates the canonical enumeration/checking of \(T\)-proofs for \(n\) steps. If a proof of \(0=1\) appears, it outputs UNSAT. Otherwise it returns \(B(z)\).

**Proof.** If \(T\) is consistent, the exceptional branch is never reached, so \(A_T=B\) extensionally. Suppose \(T\) proved the standard correctness sentence for \(A_T\). If a \(T\)-proof of contradiction existed, choose a padded satisfiable CNF whose encoded length is at least the finite detection time of that proof. The formalized execution of \(A_T\) would take the exceptional branch and reject that satisfiable input, contradicting the assumed correctness sentence. Thus correctness of \(A_T\) implies \(\mathrm{Con}(T)\) inside \(T\). Gödel's second incompleteness theorem gives \(T\nvdash\mathrm{Con}(T)\), so \(T\) cannot prove correctness of \(A_T\). ∎

This uses the ordinary intensional consistency predicate and the declared formalization hypotheses; it is not a claim about arbitrary exotic provability predicates. It precisely falsifies the proposed rule “trust the trace after attaching a \(T\)-proof that the program is correct” as a universal route. If a polynomial SAT decider \(B\) existed, the same construction would add only bounded proof-enumeration overhead and remain polynomial; no such decider is asserted here.

### 3. Require an independently checkable \(R\)-refutation from the source

This preserves soundness. A rejecting trace may guide the freely selected derivation, but completeness of \(R\) only supplies existence of some proof; it does not establish (TR). An external mathematical compiler might still prove (TR) without a fixed theory's internal correctness proof. The theorem above does **not** exclude that route.

## Relation to Cook--Reckhow and optimal proof systems

Cook--Reckhow proof systems make proof validity polynomial-time checkable and distinguish shortest proof length from proof search. Their polynomial-boundedness theorem concerns short certificates; it does not make every deterministic rejection trace a certificate. Polynomial simulation of every proof system is the p-optimality problem. Statement (TR) is adjacent but is not identified with p-optimality: its sources are arbitrary correct SAT deciders, which need not emit proofs, so it additionally needs a decision-to-certificate bridge.

The system \(R\) must also charge encodings. If a unit node contains an unbounded semantic object or invokes an uncheckable validity predicate, unit node count has no proved relation to machine work. Conversely, a small inference DAG is not automatically a low-space execution: storage, retrieval, and recomputation need a schedule.

## Exact finite optimum and hostile controls

The producer and an independently authored no-import verifier used a fixed source-axiom binary Resolution system with unit cost per new non-tautological resolvent. Breadth-first enumeration over sets of derived clauses grants the optimal sequence for free and proves these finite minima.

| Input | Label / models | Exact minimum | Control |
|---|---:|---:|---|
| \((x)\wedge(\neg x)\) | UNSAT / 0 | 1 Resolution node | smallest contradiction |
| equality \(\wedge\) inequality on \(x,y\) | UNSAT / 0 | 3 Resolution nodes | native XOR addition costs 1; charged CNF-to-XOR extraction plus addition costs 3 |
| \((x\vee y)\) | SAT / 3 | no Resolution refutation | reject-all trace is accepted by the unsound trace-only rule |

For the four-clause equality/inequality formula the offline optimizer popped 6 states, saw 13 states, and had peak frontier 7. These discovery figures are not part of \(W_R\); if BFS were an implemented solver, its entire state would be charged. The malformed literal-zero encoding was rejected. The finite computation certifies only the declared tiny optima and soundness counterexample.

The XOR control is decisive: changing to a fixed sound XOR-capable system shortens the same contradiction. Equality's high matrix rank and compact formula likewise forbid rank-only promotion. Horn/2SAT, tiny UNSAT cores, after-answer constants, instance-specific axioms, DEAD/DELAY/RECOMP traces, and semantic jumps do not supply a representation-independent lower bound.

## Four falsifiers and outcomes

1. **Rejecting trace closes a proof. FALSIFIED/RETIRED:** the reject-all machine closes a satisfiable control.
2. **Attach an instance-specific axiom \(F\to\bot\). INVALID MODEL:** \(R\) is no longer fixed independently of the input.
3. **One fixed sound theory proves every correct decider correct. FALSIFIED:** \(A_T\) escapes that theory under the stated hypotheses.
4. **Require a separately checkable source refutation. SURVIVES, but (TR) is OPEN:** completeness does not supply polynomial simulation.

An unrestricted unit-cost semantic rule “if \(F\) is UNSAT, infer \(\bot\)” is the hidden decision oracle prohibited by the model. Free choice among explicit valid rules is retained.

## Work, space, and quantifier audit

Logical \(W_R\) is proof size, not full machine work. The finite BFS is an OFFLINE optimality certificate. Any computational transfer must additionally charge source parsing, trace acquisition, correctness justification, rule checking, formula/row encodings, conversions, access, storage, and output. For materialized recursive children the all-phase contract remains

\[
s'\le\max\{\rho,\eta,\lambda,\lambda s\},
\]

where \(\rho\) includes preprocessing, discovery, conversion, generation, and combination. REFEREE294 supplies no contraction and no FLMV numerical transfer.

## Literature and project audit

Primary sources inspected before proof work:

* Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1), 1979, DOI [10.2307/2273702](https://doi.org/10.2307/2273702), author PDF: <https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf>.
* Krajíček and Pudlák, *Propositional Proof Systems, the Consistency of First Order Theories and the Complexity of Computations*, JSL 54(3), 1989, DOI [10.2307/2274765](https://doi.org/10.2307/2274765).
* Messner and Torán, *Optimal Proof Systems for Propositional Logic and Complete Sets*, ECCC TR97-026: <https://eccc.weizmann.ac.il/report/1997/026/>.
* Gödel, *Über formal unentscheidbare Sätze... I*, 1931; the second-incompleteness use is the standard modern derivability-conditions formulation, not a new attribution to the original paper.

Repository search found the immediately preceding LSPV-1 FREE-CHOICE-TRANSFER-BARRIER334, which already falsified (TR) for ordinary Resolution using Tseitin/XOR. REFEREE294 instead isolates the fixed-theory correctness-coverage failure and the three-way soundness firewall. Older TRACEEXT-FIREWALL1 already warned that computation traces do not refute the original formula. OpenAI GitHub search for “proof system SAT refutation simulation derivation DAG” returned no matching implementation; this negative search proves no novelty. Issue #3 and recent minimum-DAG commits were inspected. No task, title, state, or schedule changed.

## Exact next gap

Construct or rule out one strong fixed effective \(R\) for which both hold:

1. every correct total SAT decider has an external, uniform, source-faithful polynomial computation-to-\(R\)-derivation compiler;
2. an explicit general-CNF family has superpolynomial \(W_R\).

The first arrow cannot be discharged by a raw rejecting trace or one fixed theory's correctness certificates. It may still exist through another external proof-complexity construction. Both arrows are OPEN. **P versus NP remains OPEN.**

## Reproduction

    python3 experiments/arc/lspv5_294/minimum_derivation_firewall_referee294.py
    python3 experiments/arc/lspv5_294/verify_minimum_derivation_firewall_referee294.py
