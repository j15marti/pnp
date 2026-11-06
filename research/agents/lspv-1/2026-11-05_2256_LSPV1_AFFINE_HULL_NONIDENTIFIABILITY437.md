# LSPV-1/437: Matched affine hulls with exponentially separated ordinary Resolution work

**2026-11-05 22:56 PST | Route B lead.** Status **PROVED/RESTRICTED** (ordinary strict shared-DAG Resolution, using published graph-expander lower bounds and already proved /434–/435 translations); **COMPUTATIONAL** independently checked finite controls; historical full-mixed R_mix341 lower bound, noncircular B3, and P versus NP **OPEN**. Specialist review pending.

## IDEA → SEARCH → ITERATE

**Initial falsifiable hypothesis.** Complete affine-hull acquisition from /432 may be a dangerously weak proxy for source-authenticated proof cost. Try matching both the *entire model affine hull* and the *exact 3-CNF source-size profile* of a published ordinary-Resolution-hard family to a demonstrably easy formula.

Four falsifiers: F1 proper signed 3-CNF sizes/IDs cannot be matched; F2 additional affine equations or a g=0 model arise; F3 the easy proof relies on an invalid rule or omitted source; F4 lower-bound preservation through guarding and private splitting fails. F1–F3 are rejected symbolically and by two finite programs. F4 is rejected **only for ordinary Resolution** via already published project theorems LSPV-1/434 and /435. Historical mixed-grammar transfer remains OPEN.

## Established hard 3-CNF, published theorem and encoding

Let (G_h) be a suitable connected cubic expander sequence on h even vertices with n=3h/2 edges. For a vertex charge assignment of odd total parity, construct F_h by encoding each local equation XOR(three incident edge bits)=charge as exactly its four signed proper width-three clauses, one excluding each wrong-parity local assignment. Thus F_h has m=4h clauses, n=3h/2 edge variables, encoded size Theta(h log h) under dense binary-indexed IDs. XORing vertex equations yields 0=1: certified UNSAT. Urquhart (JACM 1987) and Ben-Sasson–Wigderson (JACM 2001) give L_Res(F_h)=2^{Omega(h)} for suitable expanding sequences against **ordinary unrestricted shared-DAG Resolution**, not against all SAT algorithms or mixed reasoning.

Define easy E_h of exactly the same m proper width-three clauses on exactly the same n occurring variable IDs. It contains the fixed 16-clause odd-Tseitin K4 contradiction F_0 on variables x_1,...,x_6. Include (x_1 OR x_2 OR x_j) once for every 7<=j<=n, and fill the remaining m-16-(n-6) slots with any distinct proper signed width-three clauses. There are sufficient clauses because m-16 >= n-6 for h>=4. E_h is UNSAT through its fixed K4 core. A native ordinary Resolution proof of that 16-clause core with **31 paid inferences** was generated, checked, and retained as an actual finite proof, not assumed for all hard instances.

For any proper source F=AND_i(a_i OR b_i OR c_i), let the prior /434 guarded proper width-three encoding be

$$
G_3(F)=\bigwedge_{i=1}^m
[(g\vee a_i\vee y_i)\wedge(\neg y_i\vee b_i\vee c_i)].
$$

Every y_i and g is globally fresh. Both H_h=G_3(F_h) and J_h=G_3(E_h) have **8h proper width-three clauses**, **11h/2+1 variables** and Theta(h log h) binary-encoded source bits.

## Theorem 437.1 (PROVED/RESTRICTED)

For every admissible h,

$$
\operatorname{Aff}(\operatorname{Mod}(H_h))=
\operatorname{Aff}(\operatorname{Mod}(J_h))=
\{(g,x,y):g=1\}.
$$

Despite matching these complete affine hulls and exact variable/clause counts, strict ordinary Resolution satisfies

$$
\boxed{L_{\mathrm{Res}}(H_h\vdash g)=2^{\Omega(h)},
\qquad L_{\mathrm{Res}}(J_h\vdash g)\le47.}
$$

**Proof of affine equality.** For UNSAT F, setting g=0 would imply F via the existential private-y projection, hence all models have g=1. All x can vary freely with y=0. For each y_i, choose x with b_i OR c_i true and change only y_i from 0 to 1. These actual model differences span all n+m non-guard coordinates. Therefore the entire affine hull is exactly g=1 on BOTH inputs, not merely a common set of valid equations.

**Proof of hard inequality.** From prior /434, one-sided positive-guard strict Resolution has the proofwise isometry

$$
L_{\mathrm{Res}}(H_h\vdash g)
=L_{\mathrm{Res}}(H_h|_{g=0}\vdash\bot).
$$

Under the fixed signed substitution y_i -> NOT a_i, each first split cofactor clause is tautological and each second becomes EXACTLY its original F_h clause. Prior LSPV-1/435 proves a **whole-shared-DAG strict Resolution compiler** under this substitution with no additional inference nodes, no weakening and no duplicated shared subproof. Consequently

$$
L_{\mathrm{Res}}(H_h|_{g=0}\vdash\bot)
\ge L_{\mathrm{Res}}(F_h\vdash\bot)=2^{\Omega(h)}.
$$

This lower-bound-preservation direction is stronger than equisatisfiability and uses the published family rather than inventing a novel hardness family.

**Proof of easy upper bound.** From each of the 16 guarded blocks corresponding to the K4 core, one strict pivot on its y_i yields (g OR C_i). Lift all 31 inferences of the existing K4 strict Resolution refutation while retaining the positive guard in every clause. Its last clause is (g). Exactly **16+31=47 paid inferences**, source-authenticated and with an acyclic shared DAG; extra easy-filler source leaves are not used. All legal shortcuts remain available to the optimum.

**Scope firewall.** This is an exponential separation of *ordinary Resolution* costs with identical semantic hulls, NOT of complete historical R_mix341. On the unguarded published hard F_h, the preexisting /341 AND3/GF(2) proof already has only 4h-1 paid mixed nodes; guarding may admit other mixed shortcuts. No full mixed or all-machine superpolynomial bound, and no noncircular B3, is inferred. The easy source deliberately contains a tiny unsatisfiable core; that legal shortcut is the actual upper-bound control.

## Independent controls and all-resource accounting

Actual standard-library Python producer constructed original signed odd/even K4, K3,3 and cube Tseitin sources, matched easy sources, and their proper-3 guards. Original source UNSAT was independently brute-forced in n<=12 variables; explicit satisfying witnesses supplied n+m independent affine differences on both guards. It replayed the complete 31-node K4 and **47-node K3,3 easy guarded unit** strict Resolution certificates, rejected wrong-pivot and tampered-source controls, checked an even-charge g=0 model, and stored source SHA256 and complete serialized proof. Independent Node semantic reproducer passed **371 assertions**.

| finite fixture | n original variables | m original clauses each | guard clauses each | identical guarded affine rank | easy proof nodes |
|---|---:|---:|---:|---:|---:|
| K4 | 6 | 16 | 32 | 22 | 47 |
| K3,3 | 9 | 24 | 48 | 33 | 47 |
| cube | 12 | 32 | 64 | 44 | 47 |

Small finite graphs are controls, not proofs of asymptotic expander hardness. Python observed about 0.17s and tracemalloc peak 195,367 bytes; these are host data, not fully charged TM time/peak process space. **Logical work** is the minimum number of *distinct* paid nodes under free proof DAG selection and legal sharing. **Ideal span** on a two-premise unit-time parallel inference model is Omega(h) on the hard ordinary-Resolution member and O(1) for the exhibited easy core. Physical source reads (Theta(h log h) input), parsing, proof discovery, failed branches, caches, evidence bits, references, retention/recomputation, verification and output must be charged for implemented algorithms. The complete certificate and Python producer are saved in the reproducibility ZIP; the repo compact JS and raw JSON reproduce finite semantic controls.

## Continuity, external audit, handoff and OPEN transfers

Actually read governing Nov-2 handoff, issue #3 through LSPV-1/436, original /341, LSPV-1/434–/436, peer LSPV-3/438 and /440 and LSPV-5/REFEREE378, actual GROKPROOF/2026-11-06_0515_PROGRESS.md and Claude 2026-10-28_1521_ONETAPE-0001.tex, AGENTS.md, CODEX.md, and the research skill. Required external current repo files read: konard/p-vs-np proofs/experiments/np_subset_p_proof_attempt.md; blkph0x/p-vs-np-proof-research METHOD_INDEX.md and PROOF_PORTFOLIO_BRIDGE_REPORT.md; meelgroup/frat-xor README; tanyongkiam/cake_lpr README; openai/math README and source-search. Primary-web searches covered Urquhart, width/size, literal substitutions and Pich–Santhanam 2026 self-provability. Direct Google-branded service unavailable; general indexed web and authenticated GitHub were used. No Lean proof or authoritative historical mixed checker was executed.

LSPV-3: independently replay source-bound 47-node certificate and seek typed native guarded-unit proof, auditing assumptions and DEF/LOCAL facets. LSPV-5: attack hidden affine consequences, strict original-source pivots, any legal mixed shortcut, and the distinction from the B3 claim. Route A LSPV-2/LSPV-4: use matched semantic pair only as a hostile control without replacing all-input same-machine FLMV contraction. LSPV-1 retains primary noncircular B3 and historical LOCAL/DEF/facet authentication. The *exact missing implication* is still a SAT-in-P to polynomial \bar W_{R_mix341} transfer for the SAME full fixed calculus. B1, B2, B3 and P versus NP remain OPEN. No task, title, schedule, weight, role, or root main.tex changed.

## References

1. A. Urquhart, "Hard Examples for Resolution", J. ACM 34 (1987), 209–219. DOI 10.1145/7531.8928.
2. E. Ben-Sasson and A. Wigderson, "Short Proofs Are Narrow: Resolution Made Simple", J. ACM 48 (2001), 149–169. DOI 10.1145/375827.375835.
3. S. Cook, "A Short Proof of the Pigeon Hole Principle Using Extended Resolution", SIGACT News 8(4) (1976).
4. S. Cook and R. Reckhow, "The Relative Efficiency of Propositional Proof Systems", J. Symbolic Logic 44 (1979).
5. J. Pich and R. Santhanam, "Towards P≠NP from Extended Frege lower bounds", J. ACM 73(2) (2026), DOI 10.1145/3801091.
