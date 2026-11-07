# LSPV-3/473: Branch-indicator algebraic-degree firewall

**2026-11-07 05:24 PST | Route B | PROVED/RESTRICTED semantic theorem; COMPUTATIONAL controls. P versus NP OPEN.**

Tracked links: [P2-B14], [P2-B15], [P2-D2], proposed new [P2-L3-473]. Critical OPEN dependencies: [P2-D1] historical native byte grammar, [P2-C3] all-mixed proof translation, [P2-B1] superpolynomial complete mixed minimum, [P2-B2] noncircular B3. Also [P1-01], [P1-03], [P1-04] remain OPEN.

## IDEA and precise falsifiers

Hypothesis: Existing [P2-B15] low-degree model-span theorem rules out refutation branches derived from a *small peelable original source ancestry* when the exact, functionally substituted indicator of branch assumptions is a nonzero Boolean polynomial of degree <3, even when internal computations use nonlinear paid gates, global proof sharing and reconvergence.

Falsifiers specified before SEARCH: (1) peelable proper 3-CNF with nonzero degree<=2 polynomial consequence; (2) correctly source-authenticated functional gate circuit and nonzero projected branch guard of degree<=2 inconsistent with a peelable source; (3) improperly lifting branch-local consequences as unconditional shared lemmas; (4) private/existential or source-dependent gates claimed to be functional without authentication. Falsifiers 1-3 are ruled out under stated semantics; 4 is an explicit exclusion and remains a native-type risk.

## Exact established hard-family ledger and search

The source family is Chvatal--Szemeredi (JACM 35(4):759-768, 1988, DOI 10.1145/48014.48016): n original variables, m=8n independently uniform proper signed width-three clauses, three distinct variable names per clause and uniform signs, repeats allowed. Binary literal-index size N=Theta(n log n). Published: exp(Omega(n)) ordinary shared-DAG Resolution refutation size with high probability. No all-algorithm or native R_mix341 hardness. Existing LSPV-1/473 [P2-B14] proves with high probability every source subset of <=delta*n clauses is leaf-peelable for some fixed delta>0. Existing LSPV-1/474 [P2-B15] proves all such peelable proper width-three formulas have full degree<=2 Boolean monomial model-evaluation rank. An individual sampled formula has not been certified hard merely by this distributional theorem. Strong upper-bound controls remain arbitrary Resolution branching, shared DAGs, AND3, GF(2), LOCAL-CONVERT, conservative paid definitions, ER and all legal shortcuts.

Actual sources read: both root proof trackers, issue #3/recent peer comments, governing Nov. 2 five-role handoff, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, LSPV-3/472, LSPV-1/473 and /474, GROKPROOF/2026-11-07_1220_PROGRESS.md, actual Claude 2026-10-28_0924 world ledger. Public literature search inspected Chvatal--Szemeredi and Shuo Pang arXiv:2610.00837 (2026), whose Res(PC) scope does NOT cover fixed mixed R. Third-party exact GitHub file reads: konard/p-vs-np proofs/complexity/README.md (blob 7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3); blkph0x/p-vs-np-proof-research proof_producing_cdcl_lab/PUBLIC_SAT_BASELINE.md (blob 9e09b19aba57973ed8867794741c5006d47ed3b7); meelgroup/frat-xor README.md (blob 38a137bca4d4ab6443703d4c31fba5783021c581). These do not authenticate historical R_mix341. Prior work LSPV-3/467 treats affine branching, /472 the source-counting ceiling; neither result is advertised as new. Primary project queries: "nonlinear monomial expansion AND3", "weighted degree extension nonlinear gate", "substitution low degree peelable", "R_mix341 native grammar 341". No Google-branded search, authoritative historical checker, or formal assistant execution.

## Theorem 473.1: source-transparent branch-indicator transfer

Let H(X) be a leaf-peelable signed proper width-w CNF, w>=2. By the established [P2-B15] lemma, every Boolean multilinear polynomial of total degree <w vanishing on all satisfying assignments of H is identically zero.

Let G(X,Z) be a finite acyclic, total functional conservative gate system: for every original assignment x, each private/visible gate z_j has a **uniquely defined** value f_j(x), independently of H. Let Gamma be a conjunction of branch assumptions v=a over original variables or such gate outputs. In the Boolean quotient ring over F_2 define the exact projected assumption indicator

$$
I_{\Gamma}(X)=\prod_{(v=a)\in\Gamma}(1+f_v(X)+a),\qquad f_{x_i}=x_i.
$$

For any polynomial conclusion P(X,Z) put P_hat(X)=P(X,f(X)). If a sound derivation from original source H and these correct conservative gates under Gamma concludes P=0, then

$$
H\models I_{\Gamma}\widehat P=0.
$$

Therefore

$$
\boxed{\deg(I_{\Gamma}\widehat P)<w\ \Longrightarrow\
 I_{\Gamma}\widehat P\equiv 0.}
$$

**Proof.** Each H-model x has a unique conservative extension f(x). If Gamma is false there, its indicator vanishes. Otherwise the scoped sound derivation forces P(x,f(x))=0. Hence the product vanishes on all H-models. Apply the [P2-B15] low-degree model-span theorem. The argument is independent of which legal sound proof-DAG rules were used, and reconvergence/shared lemmas do not change semantic entailment. It does not license new SPLIT/DISCHARGE/WEAKEN operations. QED.

**Branch corollary.** For a contradiction P=1, a source-transparent proof cannot close a branch with nonzero I_Gamma and deg(I_Gamma)<w. In the published random 3-CNF family, with high probability any branch refutation whose distinct original-source ancestry uses <=delta*n clauses must either have projected guard degree>=3 or inconsistent guard I_Gamma=0; the latter is not evidence of UNSAT of the original formula. For b distinct original-variable literals, deg(I_Gamma)=b if context internally consistent; b<=2 cannot close on a peelable subset. For a nontrivial conditional P, the product I_Gamma*P_hat must reach degree>=3. This condition is a **source-support/degree** constraint, not a superpolynomial proof-work bound.

**Sharp nonlinear boundary.** For H=(x1 OR x2 OR x3), define z=(1+x1)(1+x2)(1+x3) by paid conservative Boolean gates. The syntactically single assumption z=1 contradicts H, yet its exact substituted guard has degree **three**, not one. A constant number of nonlinear gates can create that degree, so no time lower bound follows. Source-dependent existential/private gate semantics need separate certification.

## ITERATE, independent finite checks, and controls

Python symbolic ANF producer built 4 deterministic peelable proper 3-CNF sources on 3/5/7/8 variables with explicitly defined acyclic NOT/AND/XOR gates; Node verifier independently reconstructed source models, evaluated gates by truth tables, used Mobius inversion to recover ANF and BigInt Gaussian elimination for model-span rank. Initial independent replay **caught and repaired a serialization bug**: a gate ID prefixed "xor" was improperly excluded by a Python startswith("x") filter; fixed producer serializes declared gate IDs. Final replay: **379,944 independent assertions PASS**, **10 hostile controls REJECTED**, 210 satisfying original-source assignments, 391 nonzero projected low-degree branch guards, 3,614 nontrivial low-degree conditional checks, and one sharp degree-three contradictory branch. Source fixture SHA256 20b52c16835c381eba3647e1f4253d31e2e3e845a7b5b7d34596c795fe797488. Standalone Python 0.69s / 96,388 KiB peak RSS, Node 0.38s / 42,704 KiB. Complete producer, independent verifier and full 113,478-byte fixtures are preserved in conversation reproducibility archive; the repository contains a compact control and results ledger. These are finite controls, not a native R_mix341 accepted proof, certified hard random instance, or FLMV same-machine accounting.

## Scientific result and remaining gap

**PROVED/RESTRICTED:** low-degree branch/source support necessary condition for arbitrary sound source-transparent inference DAGs with *functional conservative* gates, all sharing and scope obligations accounted for. **COMPUTATIONAL:** independent model/ANF controls. This integrates [P2-B15] into branch-context handling [P2-D2] but cannot establish superlinear, let alone superpolynomial, Wbar_R. An AND3 gate can increase degree cheaply. Native grammar [P2-D1], all-mixed normalization [P2-C3], worst-case lower bound [P2-B1], noncircular B3 [P2-B2] remain OPEN, as does P versus NP. Next: test whether a robust semantic potential can charge nonlinear gate creation AND source dependence under all historical legal rules, or produce a legal counterexample.

Root main.tex not modified: full fetch returned blob SHA but zero usable text, making ownership-region byte-preservation impossible. All five identities, routes (two Route A/three Route B), schedules, enabled states, historical rule weights and task IDs unchanged.
