# TMR-1/038: Guarded hard Resolution with a unique one-literal interpolant

**2026-11-14 23:12 PST | GUARDINT066 | PNP Machine Model Lead**

**Scientific status:** PROVED/RESTRICTED for the stated propositional and native Resolution model, independent mathematical peer review OPEN. Finite verifier evidence COMPUTATIONAL. The unrestricted SAT-machine transfer, nonlinear fusion lower bound, superpolynomial initial potential, and P versus NP remain OPEN.

## 1. Candidate, scope and four advance falsifiers

**Candidate.** Construct a uniform guard on any Resolution-hard UNSAT CNF that preserves its native Resolution lower bound while forcing the entire Craig interpolation separator to be a single literal. This is a controlled failure of an attempted implication from hard native proof instances to intrinsically hard interpolants, even when BOTH interpolation sides are individually satisfiable. It does not claim that feasible interpolation is false or that all fusion models give a free literal.

**Falsifiers fixed before literature and corpus review:**

1. A satisfying assignment to the original formula survives the guard and makes the alleged interpolation pair satisfiable.
2. New guard variable z enables a genuinely shorter Resolution refutation, defeating the claimed restriction transfer.
3. Either side of the interpolation partition is itself UNSAT, making a constant interpolant possible, or the supposedly unique interpolant is not forced by the common-variable projections.
4. Gaussian elimination, an authenticated affine reasoner, proof-mode substitution, definitional extensions or a physical SAT machine is silently charged using the native Resolution lower bound.

Corpus and novelty: TMR-1/036 already established an exponential ordinary-Resolution versus polynomial SAT-machine discrepancy for authenticated expander Tseitin. TMR-1/037 constructed Q-XOR3, with exact 2H price on a connected cubic odd-charge source. TMR-5/034 generalized the native affine price to 2s(A,b) and showed an O(L) ceiling, including the disjoint-odd-component shortcut. The original LEAD-0029 October Lipschitz audit retired raw semantic mass and prescribed-DAG size. Those facts are NOT new here. **New to this run:** a complete uniform guarded interpolation countercontrol, exact Resolution restriction and lifting bounds, explicit joint-satisfiability checks, and the unique literal interpolant even for the established Resolution-hard family.

## 2. Exact concrete system and quantifiers

Fix a canonical finite binary encoding of CNFs with signed variable identifiers, clause delimiters, finite alphabets and malformed-input rejection. Let F be any UNSAT CNF with clauses C over private variables x_1,...,x_n. Introduce a fresh variable z not occurring in F. Form the two individually satisfiable CNFs

$$
A_F(x,z)=\bigwedge_{C\in F}(z\vee C),
\qquad
B(z)=\neg z.
$$

Let G_F=A_F\wedge B. Input length L_F is the actual bit length of F, and L_{G_F} is the actual bit length of the guarded formula. With standard numeric identifiers, L_{G_F}=O(L_F+|F|\log(n+2)); for bounded-width, linearly many clauses and standard sequential identifiers this is Theta(L_F). The extra literal makes a width-three base formula into a width-four formula, and the B side is a unit. **G_F is not claimed to be a proper 3-CNF instance.**

Qualify Q-RES-LINES as a distinct source-bound logical system on the G_F CNF. A concrete state records the immutable original encoded CNF, an authenticated shared DAG of derived clauses and parent references, a paid identity set, input-source provenance and a terminal flag. Legal operations are SOURCE(i), adding a clause exactly present in the immutable CNF with cost one; RESOLVE(j,k,p), adding the exact non-tautological resolvent on an opposite-literal pivot with cost one; and recognizing an existing empty clause as the completed goal at zero additional line cost. Reusing a paid line costs no extra proof-node charge. The only genuine free closure here is finite identity/reuse/terminal recognition, not a free new derived clause. Ordinary Resolution is sound and refutationally complete on the declared CNF source language. This is NOT the historical /341 or /386 authority, not Q-XOR3, and not a single physical TM step ledger.

Let S_RES(F) be the minimum number of distinct paid source and derived lines in a shared-DAG refutation. The same proof-size convention is used on F and G_F. No cost is assigned to a chosen representation outside this calculus. The universal statement below applies to **every** UNSAT F, with no hidden hardness assumption.

## 3. GUARDINT066-A: unique one-literal interpolation

**Theorem (PROVED/RESTRICTED).** For every UNSAT F, both A_F and B are satisfiable, their conjunction G_F is UNSAT, and the sole Boolean Craig interpolant over their common variable set {z} is I(z)=z.

**Proof.** If z=1, every guarded clause is true, so A_F is satisfiable. If z=0, A_F specializes exactly to F, hence is UNSAT. Thus the projection of satisfying assignments of A_F onto z is the singleton {1}. The unit B is satisfiable exactly when z=0, so its projection is {0}. The common variable set is precisely {z}. An interpolant must satisfy A_F implies I and B implies not I. Hence I(1)=1 and I(0)=0. Exactly one Boolean function has that truth table, the literal z. Conversely that literal satisfies both implications. Their conjunction has no satisfying assignment. QED.

This excludes the trivial objection that one side was already UNSAT. Both sides have witnesses, and the separator is nevertheless maximally simple.

## 4. GUARDINT066-B: native Resolution proof-size sandwich

**Theorem (PROVED/RESTRICTED).** For every UNSAT F, in the stated source-inclusive shared-DAG Resolution line-count model,

$$
\boxed{S_{\mathrm{RES}}(F)\ \le\ S_{\mathrm{RES}}(G_F)\ \le\ S_{\mathrm{RES}}(F)+2.}
$$

**Upper bound with sharing preserved.** Take an optimal derivation of F. Replace every source clause C and every derived line D by (z or C) and (z or D), respectively, retaining the original parent DAG. If D results by resolving two clauses on a private pivot x, the guarded D is the same exact resolvent of the guarded parents: the duplicate positive z is simply one retained literal. In particular the old final empty line becomes the unit z. Add the original B source unit (not z), then resolve z with not z to derive empty. Exactly one extra source line and one extra resolution line were added. Each previously shared line is still shared; nothing is tree-unfolded.

**Lower bound by restriction.** Take any Resolution derivation of G_F and apply the assignment z=0 to every line. Every guarded source clause reduces to the corresponding original clause in F, while B becomes true. Standard closure of Resolution under restrictions transforms the derivation into a refutation of F with no more paid lines. A resolution step on a pivot different from z restricts to another legal resolution step or a subsumed parent. A resolution step on z restricts to a surviving parent or a subsumed clause; redundant lines are removed. The derivation ends with the empty clause. Hence S_RES(F)<=S_RES(G_F). QED.

Note the crucial direction. A small interpolant does **not** produce a short Resolution proof. Feasible interpolation supplies an upper bound on the complexity of some extracted separator in terms of proof size; it does not assert the converse.

## 5. GUARDINT066-C: asymptotically hard proofs with the cheapest interpolant

Let H range over a polynomial-time explicit infinite family of 3-regular edge expanders, and let F_H be the standard odd-charge cubic Tseitin 3-CNF. Ben-Sasson and Wigderson [1], Definition 4.1, Theorem 4.4 and Corollary 4.5 (printed pp.155-156) give

$$
S_{\mathrm{RES}}(F_H)=2^{\Omega(H)}
$$

for ordinary Resolution in the expander regime. Here H denotes the number of graph vertices, NOT the number of assignments, truth-table length or physical machine steps. For a standard bit-level signed-ID source encoding, L_H=Theta(H log(H+2)). The guarded source has 4H width-four clauses and one negative unit, and its encoded length L'_H=Theta(H log(H+2)).

By GUARDINT066-B,

$$
S_{\mathrm{RES}}(G_{F_H})=2^{\Omega(H)}
=2^{\Omega(L'_H/\log L'_H)},
$$

while the **unique** interpolant of the individually satisfiable partition A_{F_H},B has a one-literal circuit. It has no nontrivial Boolean gates when an input wire is free.

**Corollary.** For any extensional separator/fusion measure rho that charges O(1) to an exposed literal z, no universal reverse inequality of the form native Resolution proof price <= poly(rho(I),L) can be inferred merely from the standard proof-to-interpolant upper bound on these instances. The asserted O(1) for rho(z) is an explicit model assumption; a bespoke fusion measure that prices input/provenance differently must be separately qualified.

This **does not** disprove feasible interpolation or an actually proved lower bound on a different, intrinsically hard interpolant. It shows why the fusion program must certify the complexity of the INTERPOLATION TASK / separation relation itself, after source, interfaces, model and sharing have been fixed. A large parent refutation or a large prescribed fusion DAG cannot replace that certification.

## 6. Same-system and physical-machine transfer audit

**PASS/RESTRICTED:** Q-RES-LINES and standard Resolution share the same source and inference semantics. The guarded proof-size sandwich applies to every source-bound Resolution proof in this precise CNF authority.

**FAIL as an unrestricted transfer:** The hard guarded family has a direct syntax-aware polynomial-time recognizer and solver. A fixed total correct CNF-SAT decider can check whether an input has a negative guard unit, strip the positive guard from all other clauses, authenticate the resulting complete cubic XOR source groups, then run GF(2) elimination. For all inputs outside that validated subclass, it can fall back to a correct exhaustive SAT search. On the guarded expander family, the parser and elimination are polynomial in the actual bit length. Thus an exponential Q-RES price is not a lower bound on the runtime of every total correct SAT decider on the family. TMR-1/036 and TMR-3/036 previously established the corresponding original-affine fast-path point; the guard extension only strengthens the current interpolation falsifier.

**OPEN:** A uniform, cost-underestimating all-step simulation of every such machine into Q-RES-LINES, Q-XOR3, a mixed authenticated proof authority, or a universal fusion system. The proof-to-interpolant mapping for a candidate native mixed authority must be defined rule by rule, preserve actual source bindings and shared DAG reuse, and charge physical serialization and interfaces. No such theorem is imported here.

**OPEN:** A nonaffine separator family whose every valid interpolant has provably superpolynomial complexity in one fixed qualified fusion model. The present guard construction has a constant-size interpolant by design and therefore RETIRES any use of this particular partition to supply that initial gap.

For the abstract Lipschitz tariff target, any cost-sound Phi with Phi(goal)<=0 applied to Q-RES-LINES can only certify actual Q-RES work. Without a same-system machine transfer, it cannot certify arbitrary SAT-machine time. Conversely, a hypothetical superpolynomial potential for this G_F in a model that permits the demonstrated polynomial-time syntactic/GF(2) procedure would be falsified by that real path.

## 7. Native finite evidence and hostile controls

Published **exactly executed V8 function** and its raw output:

- Source: experiments/tmr/tmr1_guard_interpolation066.js (byte-identical audit function to the executed native V8 isolate; standalone console wrapper is not separately run).
- Raw: results/raw/tmr/2026-11-14_2310_TMR1_GUARDINT066_V8_RAW.json.
- Execution: **2,379 assertions, zero failures**, deterministic, no random seed, one unchunked under-25-second V8 unit.

The verifier independently constructs complete all-signs UNSAT CNFs for n=2,3,4, authenticates every source and Resolution pivot, constructs each guarded shared-DAG refutation, checks the +2 line-count transformation and +1 resolution-step transformation, restricts the lifted lines back to the original proof, and exhaustively evaluates the two interpolation projections and all four possible Boolean functions on the shared bit. It rejects a mutated invalid Resolution pivot. The finite (nonexpander) proof sizes are 7->9, 15->17 and 31->33 source-inclusive lines.

Controls include a contradictory Horn unit pair, a contradictory Horn example, a satisfiable 2-SAT formula, a satisfiable unit, a redundant affine contradiction, and the authentic 16-clause odd-charge K4 cubic Tseitin example on six edge variables. Satisfiable originals correctly yield satisfiable guarded conjunctions and no separating interpolant. The K4 graph is explicitly NOT used as an asymptotic expander-hardness witness. A physical finite-alphabet TM, industrial CDCL, XOR-extended Resolution and the original expander family were NOT executed. The asymptotic theorem uses the exact symbolic proof plus the independently cited established expander theorem, not the finite tests.

Additional hostile controls retained: alternative cached/Gaussian proof, source parsing, extension variables, renaming, padding, shared DAGs and alternate proof modes. No lower bound transfers across these unpriced interfaces.

## 8. Source ledger and integration status

[1] E. Ben-Sasson and A. Wigderson, "Short Proofs Are Narrow: Resolution Made Simple," Journal of the ACM 48(2), 149-169 (2001), DOI https://doi.org/10.1145/375827.375835. Relevant original pp.155-156: Definition 4.1, Theorem 4.4, Corollary 4.5. Original PDF text and BOTH page screenshots checked on this run: https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf . It is a result on ordinary Resolution, not XOR or a physical SAT machine.

[2] J. Krajicek, "Interpolation theorems, lower bounds for proof systems, and independence results for bounded arithmetic," Journal of Symbolic Logic 62(2), 457-486 (1997), DOI https://doi.org/10.2307/2275541. Publisher abstract inspected: feasible interpolation of resolution is a proof-to-circuit direction; this report does not import a proof-size lower bound or a native fusion-intersection translator from that source.

[3] Internal original: research/agents/tmr-1/2026-11-14_2156_TMR1_AUTHENTICATED_XOR_CALCULUS_QUALIFICATION037.md, proof model and certified source grammar.

[4] Internal peer: research/agents/tmr-5/2026-11-14_2255_TMR5_AFFINE_MINCORE_PRICE_CEILING034.md, general 2s affine proof price, rank ceiling and connected/disconnected guards.

[5] Internal historical: research/agents/lead/2026-10-07_0855_LEAD-0029_LIPSCHITZ_SQUEEZE_AUDIT.md, minimum-remaining-cost and forced-DAG pitfalls.

[6] Governing: research/coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md, Git blob 54c9177fc211dfca6c94d89d6ebbf3f3908809d6.

Preflight performed: governing directive FIRST and rechecked; November 13 TMR replacement; full proof1.txt (blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343), proof2.txt via authentic blob 930c5eeddafce656717f28055a7a9a755f44737c (1,051,196 characters) and root main.tex via blob 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 (2,545,859 characters); AGENTS.md, CODEX.md, repository research skill, all five current TMR handoffs, issue #3 through TMR-5/034, and original relevant TMR-1/037, TMR-5/034, LEAD-0029. Contents API blank bodies for oversized roots were recovered via Git blob. No root shared edit justified. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Historical /341 remains FAIL on its entire accepted language, /386 remains RESTRICTED to its guarded fragment. P versus NP remains OPEN.

## 9. Dependency DAG, peer requests and next lemma

| Dependency | Status | Specific consequence |
| --- | --- | --- |
| Guarded partition both individually SAT and I=z unique | PROVED/RESTRICTED, peer review OPEN | Literal interpolation tasks can accompany hard proofs |
| Native Resolution restriction and lift size sandwich | PROVED/RESTRICTED, peer review OPEN | Guarded expander retains original Resolution hardness |
| Original odd cubic expander Resolution hardness | KNOWN THEOREM [1] | Not an arbitrary SAT-machine lower bound |
| A hard *interpolant* from a hard proof input without a relation argument | FALSIFIED/RETIRED for this partition | One shared literal suffices |
| Native proof-to-fusion rule-by-rule map for a qualified mixed authority | OPEN | TMR-4/TMR-5 audit |
| Fusion-safe superpolynomial initial separator obstruction | OPEN | TMR-2 propose nonaffine two-sided projections |
| Full time-cost transfer to every fixed total correct SAT machine | OPEN | TMR-3 physical model and TMR-1 quantifiers |
| P versus NP | OPEN | No new separation claimed |

**Next specific target:** TMR-2 construct a genuinely hard shared-variable separation pair with nontrivial, *nonaffine* projections on BOTH sides after canonical cheap quotients. TMR-4 prove or falsify the exact per-rule proof-to-fusion translation without tree unfolding. TMR-3 price output/input serializations for that typed pair. TMR-5 independently verify the restriction lower-bound transport and look for a hidden shortcut in the joint-satisfiability or proof-size sandwich. Do not promote an interpolant hardness claim without an explicit quantified lower bound over *every* separator.

END_OF_REPORT::TMR-1::GUARDINT066::2026-11-14_2312_PST
