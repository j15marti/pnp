# EXTENSION-SIMULATION-BARRIER-REFEREE299

**PNP Independent Proof Red Team — November 2, 2026, 16:48 PST**

**Status.** **PROVED/EXACT** for the syntactic simulation theorem under the already fixed Rmix341 rule syntax and aligned weights; **COMPUTATIONAL** for the finite replay and hostile controls; **KNOWN** for Cook's polynomial Extended-Resolution pigeonhole proof; **EXTERNAL PREPRINT CLAIM** for Braun's 2026 Res(XOR) lower bound; **OPEN** for a superpolynomial mixed minimum, B1, B2, B3, and P versus NP.

## Claim card

- **Claim ID:** EXTENSION-SIMULATION-BARRIER-REFEREE299.
- **Desired conclusion:** determine whether candidate Resolution/Res(XOR)-hard families can remain hard in the same preselected mixed calculus.
- **Quantifiers:** for every valid UNSAT CNF \(F\), for every legal binary-gate Extended-Resolution refutation \(\pi\) of \(F\), construct a legal Rmix341 refutation \(\tau(\pi)\).
- **Fixed model:** original labelled CNF sources cost zero. Each binary RES node costs one. Each conservative two-input DEF instruction costs one and exposes its authenticated constant-size defining CNF slots to later RES nodes. All other Rmix341 rules remain legal but are unused by the translation.
- **Resource measured:** distinct inference nodes in a shared contradiction DAG. Best legal proof selection is free. Proof search, encoded certificate bits, checking work, and scheduled machine space are reported separately.
- **What falsifies it:** an Extended-Resolution instruction whose gate relation is outside the declared DEF basis, a defining slot that cannot legally feed RES, a hidden uncharged extension axiom, or a translated dependency/pivot rejected by the fixed checker.

## Exact theorem: Rmix341 simulates its binary-gate ER fragment

Let \(ER_2\) be Extended Resolution over exactly the same fixed finite basis of two-input Boolean gates as Rmix341.DEF. An \(ER_2\) derivation has original source clauses, fresh-variable extension instructions, and ordinary binary resolution. Give each extension instruction and each resolution instruction unit weight. A fresh gate instruction

$$
y\leftrightarrow g(a,b)
$$

provides the constant defining CNF prescribed for \(g\). In the usual clause-count convention, charge its defining clauses separately; this only increases the \(ER_2\) cost by a constant factor.

**Theorem.** For every UNSAT CNF \(F\) and every legal \(ER_2\) refutation \(\pi\) of \(F\), there is a legal Rmix341 refutation \(\tau(\pi)\) with the same shared dependency DAG and

$$
\operatorname{cost}_{Rmix341}(\tau(\pi))
\leq \operatorname{cost}_{ER_2}(\pi).
$$

Consequently,

$$
W_{Rmix341}(F)\leq W_{ER_2}(F)
$$

under the aligned instruction-unit convention, and the inequality still holds up to a fixed constant under standard extension-clause counting. Hence

$$
\overline W_{Rmix341}(N)\leq \overline W_{ER_2}(N).
$$

**Proof.** Process \(\pi\) in topological order. Map every source clause to its identically labelled Rmix341 source. Map every fresh \(ER_2\) extension instruction to one charged DEF node with the identical output, inputs, gate tag, and authenticated defining slots. Freshness and acyclicity are preserved. Map every resolution instruction to one RES node with the same two antecedents and pivot; an antecedent that is a defining clause names the corresponding slot of the already charged DEF node. The resolvent is syntactically identical. Sharing is preserved because each source, DEF instruction, and derived clause is mapped once. The final empty clause therefore maps to a legal contradiction. No semantic SAT query, correctness axiom, instance-specific rule, or proof-search optimizer is used. Each mapped instruction has weight at most its source instruction, proving the cost inequality. Taking minima and then maxima gives the stated inequalities. QED.

This theorem is deliberately syntactic. It does not assert that all versions of Extended Resolution are identical, nor that Rmix341 simulates arbitrary semantic gates. It covers the standard finite binary basis precisely because the fixed DEF rule was declared to support that basis with accessible authenticated clauses.

## Four falsifiers and dispositions

1. **BPHP remains mixed-hard because it is hard for Resolution or Res(XOR). — FALSIFIED as a family candidate.** Cook gave polynomial Extended-Resolution proofs of the pigeonhole principle. The theorem above imports every same-basis binary-gate ER proof. The peer BPHP-FULL-COOK-CERTIFICATE346 independently supplied an explicit legal Rmix341 compiler with polynomial upper bound and complete replays for \(h=4,8,16\).
2. **Braun's BPHP Res(XOR) lower bound transfers to Rmix341. — FALSIFIED.** Braun's stated theorem is for unrestricted DAG-like Res(XOR), not for an extension-enabled calculus. A stronger target calculus may have shorter proofs; the displayed simulation and Cook escape make the missing transfer concrete.
3. **Peitl–Szeider finite Resolution maxima or random-3-CNF Resolution lower bounds are automatically mixed minima. — FALSIFIED as an inference.** Their certificates optimize a specified Resolution measure. A mixed lower bound must survive DEF, XOR, AND3, and conversions in the same preselected system. No such transport theorem was found.
4. **The simulation proves B3. — FALSIFIED.** The inequality is in the proof-system-strength direction: Rmix341 proofs are no longer than \(ER_2\) proofs. SAT in P is not known to make this same \(ER_2\), or this same Rmix341, polynomially bounded. A rejecting computation trace is not automatically an ER correctness proof.

The weakest plausible repair is to choose a growing nonaffine family and prove a lower-bound invariant against **all** Rmix341 rules, including every legal DEF use. By this theorem such a lower bound would also give a superpolynomial lower bound for the aligned \(ER_2\) system. Independently, B3 must still be proved for this same fixed calculus.

## Independent finite replay

The producer and a separately implemented no-import verifier replayed the UNSAT source

$$
(a)\wedge(b)\wedge(\neg a\vee\neg b)
$$

with the paid definition \(y\leftrightarrow(a\wedge b)\). The three authenticated slots are

$$
(\neg y\vee a),\quad(\neg y\vee b),\quad(y\vee\neg a\vee\neg b).
$$

Five checked RES nodes derive \(y\), derive \(\neg y\), and resolve them to the empty clause. Together with one paid DEF this is a legal six-node **upper certificate**, not a minimum claim; the source itself has a two-resolution refutation. This explicitly checks that a DEF slot can feed later RES steps without three hidden free inference nodes.

Hostile controls passed:

- the one-clause sign neighbor has the all-ones SAT model;
- deleting any of the three source clauses gives SAT;
- all eight malformed line-DIMACS controls were rejected;
- all four corrupted proof controls were rejected;
- BPHP with three pigeons/two holes is UNSAT, and all 12 single occurrence-sign flips have exactly one model;
- odd-charge \(K_4\) Tseitin is UNSAT while the even control has eight models. The prior exact Rmix341 XOR upper/minimum is 15 nodes, so it remains the mandatory algebraic-easy control.

The independent verifier performed 44 explicit checks. Raw SHA-256 is e9815dc50a26b5e3dd38cc8a5ef93fcd58ab2e73905a7d003197b4be9daa7997.

## B1/B2/B3 classification

This run proves neither B1 nor B2 nor B3.

- It does **not** translate arbitrary decider traces into proofs, so B1 remains open.
- It gives no bound from worst-case runtime to \(\overline W_R\), so B2 remains open.
- It does not show that SAT in P makes the fixed Rmix341 polynomially bounded, so B3 remains open.

What it does prove is a **difficulty transfer for lower bounds**: a superpolynomial Rmix341 minimum lower bound would automatically be a superpolynomial lower bound for its embedded binary-gate Extended-Resolution fragment. This correctly retires BPHP and pure parity as mixed-hard candidates without claiming that no hard family exists.

## Acquisition, work, and all-phase space ledger

The mathematical translator is a single topological pass over an already supplied \(ER_2\) DAG. Its logical output has one mapped node per instruction. Materializing the translated certificate requires linear output work and linear encoded output bits; a verifier must additionally parse the original CNF, check freshness, gate slots, references, pivots, and the final ancestry. A streaming producer can avoid retaining all clause bodies, but random dependency validation may require an index or rereads; no sublinear-space theorem is claimed.

The finite Python producer charged parsing, exhaustive model enumeration, gate conversion, certificate construction, corruptions, checking, JSON output, and process overhead. It used 0.0203 seconds and peak host RSS 12,672 KiB in the recorded run. The independent verifier was separate. These host figures are upper measurements, not logical lower bounds or a matched Turing/RAM theorem. Any recursive machine application must retain the corrected envelope

$$
s'\leq\max\{\rho,\eta,\lambda,\lambda s\},
$$

with \(\rho\) covering every local phase, including parsing and conversion. This experiment makes no FLMV exponent claim.

## Literature and project audit

Primary/current searches used: “bit pigeonhole principle DAG Res(XOR) Braun”, “Cook short proof pigeonhole extended resolution”, “Extended Resolution lower bounds open problem”, “Peitl Szeider hardest formulas resolution”, project searches for Rmix341, DEF, BPHP, and Extended Resolution, and “github.com/openai resolution proof”. Relevant findings:

- K. Braun, *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015 (2026), states a \(2^{\Omega(n/\log^2 n)}\) lower bound for DAG-like Res(XOR), with a Lean formalization: <https://arxiv.org/abs/2609.23015>. This external claim was not locally kernel-replayed.
- S. A. Cook, *A short proof of the pigeon hole principle using extended resolution*, SIGACT News 8(4), 28–32 (1976), DOI <https://doi.org/10.1145/1008335.1008338>. A modern explicit description records the \(O(n^4)\) proof: <https://www.cs.cmu.edu/~mheule/publications/PoS22-PHP.pdf>.
- T. Peitl and S. Szeider, *Finding the Hardest Formulas for Resolution*, JAIR 72 (2021), 69–97, DOI <https://doi.org/10.1613/JAIR.1.12589>. Its finite hardness numbers concern Resolution, not the fixed mixed calculus.
- J. Krajíček, *The Case of ER*, in *Proof Complexity Generators* (2025), DOI <https://doi.org/10.1017/9781009611664.009>, treats Extended-Resolution lower bounds as a central proof-complexity problem.

Project audit read the November 2 12:04 worst-case/B3 handoff, the 16:00 hardest-instance atlas, issue #3, AGENTS.md, CODEX.md, the pnp-research red-team protocol, and the newest LSPV-1–4 BPHP reports. The OpenAI GitHub search returned no relevant proof-complexity implementation. The public browser could not authenticate private project pages; the connected GitHub reader succeeded. No novelty is claimed for the classical ER simulation idea.

## Exact next gap

Select one growing, explicit, nonaffine signed CNF family and prove an invariant that is monotone under every legal RES/AND3/XOR/CONVERT/DEF inference in Rmix341, or exhibit a shorter mixed proof that retires it. In parallel, B3 requires a separate conditional theorem tying SAT in P to polynomial worst-case minimum proofs in this exact preselected calculus. **P versus NP remains OPEN.**
