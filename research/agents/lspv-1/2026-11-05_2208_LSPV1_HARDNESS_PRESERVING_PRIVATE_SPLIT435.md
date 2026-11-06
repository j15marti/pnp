# LSPV-1/435 | Proofwise Resolution-hardness preservation for private clause splitting

**November 5, 2026, 22:08 PST. Route B LSPV-1.** Status **PROVED/RESTRICTED** ordinary binary Resolution; **COMPUTATIONAL** finite source-authenticated tests; **OPEN** full historical R_mix341, B1/B2/B3 and P versus NP. Independent specialist review pending; no originality claim.

## IDEA, SEARCH, ITERATE and four falsifiers

Prior LSPV-1/434 established a satisfiable positive-guard formula with hard-to-prove unit only conditionally: preservation of Resolution hardness under private clause splitting remained unproved. Test explicit signed-literal substitution on the complete shared proof DAG.

(F1) Variable identification breaks a strict Resolution inference. (F2) Tautological images require weakening or proof duplication. (F3) Removing a positive guard leaks branch assumptions or double-counts shared nodes. (F4) AND3/GF(2)/DEF/LOCAL shortcuts make all-rule hardness false. (F1)-(F3) rejected by direct proofwise transformation and independent 43,626-check finite replay. (F4) confirmed for the underlying odd-Tseitin family; no full mixed lower bound is claimed.

## Fixed proof model

Let $L_{\mathrm{Res}}(F)$ be the minimum of the number of *distinct paid* correctly oriented binary Resolution inferences in any source-authenticated acyclic shared DAG refuting F, all proof choices free after the fact, source leaves free, unit cost per inference, no weakening, split/discharge, extension axioms, or semantic oracle. This integer minimum exists by completeness. Ideal dependency depth $D_{\mathrm{Res}}$ is distinct from physical time/space.

### Lemma 435.1: signed-literal substitution of shared DAGs

If $\sigma$ maps every variable to a signed literal (allowing identifications and complements), any strict Resolution refutation DAG of P compiles to a strict Resolution refutation DAG of the nontautological substituted sources $\sigma(P)$ with **no more paid inferences or depth**, retaining sharing and source provenance.

**Proof.** Traverse the original DAG in topological order. For each non-tautological substituted clause C maintain a derived subclause $D_C\subseteq\sigma(C)$. Source images are exact source leaves. For a step $(A\vee z),(B\vee\neg z)\vdash A\vee B$, let $\ell=\sigma(z)$. Discard a tautological child image. For a non-tautological child, if a parent image is tautological then the opposing signed pair must involve the pivot image, since a tautology confined to A or B would persist in the child. The other parent's already derived subclause is therefore a subclause of the child: reuse its node. If one compiled parent has lost the pivot image, similarly propagate that parent. Otherwise the two compiled parents contain $\ell$ and $\neg\ell$ and a single genuine oriented Resolution inference derives a non-tautological subclause of the child. The root is $\sigma(\bot)=\bot$, so the compiled root is exactly the empty clause. No weakening or duplicated shared ancestors, and at most one paid node per original step. QED.

### Theorem 435.2: hard private split, additive work and depth

For UNSAT proper signed width-three $F=\bigwedge_{i=1}^m(a_i\vee b_i\vee c_i)$, introduce one fresh private $y_i$ per clause and put

$$
H(F)=\bigwedge_i[(a_i\vee y_i)\wedge(\neg y_i\vee b_i\vee c_i)].
$$

Then **over all ordinary shared-DAG Resolution refutations**

$$
\boxed{L_{\mathrm{Res}}(F)\le L_{\mathrm{Res}}(H(F))\le L_{\mathrm{Res}}(F)+m,}
$$

and $D_{\mathrm{Res}}(F)\le D_{\mathrm{Res}}(H(F))\le D_{\mathrm{Res}}(F)+1$.

**Lower direction:** substitution $y_i\mapsto\neg a_i$ makes the first clause tautological and the second exactly the original source $a_i\vee b_i\vee c_i$. Apply Lemma 435.1 to any H refutation. **Upper direction:** one paid Resolution on each y_i recovers each original clause; append the optimally selected F proof, paying at most m extra and one depth level.

### Corollary 435.3: genuinely hardness-preserving proper-three-CNF reduction

Pad each $(a_i\vee y_i)$ to its two private-p variants $(a_i\vee y_i\vee p_i)$ and $(a_i\vee y_i\vee\neg p_i)$, keeping the other split clause. The proper width-three formula $P_3(H(F))$ has $3m$ clauses, $n+2m$ occurring variables (assuming consecutive renumbering), and preserves ordinary Resolution proof size in the **required direction**, not merely SAT/UNSAT equivalence:

$$
\boxed{L_{\mathrm{Res}}(F)\le L_{\mathrm{Res}}(P_3(H(F)))\le L_{\mathrm{Res}}(F)+2m.}
$$

Proof: restrict every padding p_i in a padded refutation to constants to obtain an H refutation without increasing Resolution work or depth (prior LSPV-3/433 restricted-padding lemma), then use Theorem 435.2. In the other direction, eliminate each p_i with one paid Resolution, recover each original F clause with another, then reuse the original proof. Depth overhead at most two.

### Corollary 435.4: satisfiable strict-three source with a hard entailed unit

Prior LSPV-1/434 used
$$
G_3(F)=\bigwedge_i[(g\vee a_i\vee y_i)\wedge(\neg y_i\vee b_i\vee c_i)].
$$

For UNSAT F, G is SAT, entails g, and its exact model affine hull is g=1. Because source g appears only positively, strict Resolution $G\vdash g$ has the same minimum work as $H(F)\vdash\bot$ by the earlier one-sided guard isometry. Thus

$$
\boxed{L_{\mathrm{Res}}(F)\le L_{\mathrm{Res}}(G_3(F)\vdash g)\le L_{\mathrm{Res}}(F)+m.}
$$

This proves *ordinary Resolution* hardness of an entailed unit despite a trivial affine semantic description. It does not license a native mixed proof step or a free SAT oracle.

## Mandatory published family / theorem / exact encoding / shortcuts ledger

**Urquhart 1987; Ben-Sasson–Wigderson 2001, Def 4.1, Lem 4.2, Cor 4.5:** On suitable connected cubic edge-expander G_h with h vertices, one variable for each of 3h/2 edges and odd total vertex charge, encode each of h degree-three parity equations by four width-three clauses forbidding opposite-parity triples. Source F_h has 4h proper 3-clauses, $\Theta(h\log h)$ indexed bits, and is UNSAT since summing vertex parities produces 0=1. Published lower bound $L_{\mathrm{Res}}(F_h)=2^{\Omega(h)}$ for **unrestricted ordinary shared-DAG Resolution**, not all SAT algorithms. The proven reverse maps give a derived proper-3 family $P_3(H(F_h))$ with 12h clauses and 19h/2 occurring variables retaining $2^{\Omega(h)}$ ordinary Resolution size, equivalent to $2^{\Omega(N/\log N)}$ in N encoded bits. The SAT guarded G_3(F_h) has 8h proper 3-clauses and hard entailed g.

**Historical mixed shortcut control:** LSPV-2/341 proves exactly 4h-1 paid nodes for original bridgeless cubic odd-Tseitin in a specified semantic R_mix341: 3h AND3 conjunction nodes plus h-1 GF(2) joins, attaining source-indispensability lower bound. These legal shortcuts must be included in the mixed minimum, so **no full R_mix341 hardness follows**. Cook ER and Braun bit-PHP Res(XOR) remain distinct mandatory proof-system controls; facet-port acceptance in historical /341 is still not authenticated.

## Independent finite certificate and hostile controls

Reused original K4 odd-Tseitin 16-clause 6-variable ASCII DIMACS (163 bytes, SHA256 ea08104837e167b9ebd06d8f50442d828e3ba4d81f79dff8c14a09ba30050096) and the preceding 32-clause G3 guarded 23-variable source (336 bytes, SHA256 d6713f4ef056e100c350cab6b51c0f363a4bcb904d079d1c8e838a182c7f3d07). From a *valid* prior 47-node g-unit proof, a new Python compiler produces a **31-node** strict Resolution refutation of the original K4 source: 16 tautological source images removed, 16 derived nodes propagated, 31 genuine remaining inferences. The independently produced 48-clause padded proper-3 source has 38 occurring variables, DIMACS **header bound 39 because unused guard ID 7 remains**, 534 bytes, SHA256 9bcb18a5b92930d6c599b9608704338f48e230e656a1f5a9c2a0cb1cdacbbdd1; a legal strict Resolution certificate uses 63 paid nodes.

Independent Node verification: **43,626 checks** including 27,864 local signed-substitution inference cases (9,792 tautological-parent cases and 14,256 propagation cases), all source identities, oriented pivots, all 16 K4 clause-deletion SAT witnesses, and six rejected malformed/corrupted controls. NOT verified shortest at K4 or native historical checker execution.

Host Python transform 1.49 sec/96012 KiB max RSS; padding 1.24 sec/95632 KiB; Node replay 0.29 sec/38440 KiB. These are observations, not FLMV TM time-space exponents. Paid nodes exclude hindsight optimization/search cost; implemented algorithms must charge parsing, reads, output bits, verification, RAM, caches, failed search, references, retention and recomputation.

## Search and provenance audit

Reviewed governing Nov 2 handoff at 4e29ed7646f484707767acb6e63ec5f38afd98a8, current issue 3, AGENTS.md (19656af1), CODEX.md (754999f5), research skill (b8df83a7), LSPV-1/434 (bce866a5), historical LSPV-2/341 (c87acd11), LSPV-3/433/437 (7cf00853)/438 (63e4318d)/439 (185a8985), actual Grok GROKPROOF/2026-11-06_0515_PROGRESS.md (93f9202d) and Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6). Earlier guard isometry and padding are reused, not asserted new.

Primary research: E. Ben-Sasson and A. Wigderson, Short Proofs Are Narrow, JACM 48(2):149-169, 2001, DOI 10.1145/375827.375835 (read PDF theorem); A. Urquhart, Hard Examples for Resolution, JACM 34(1):209-219, 1987, DOI 10.1145/7531.8928. Search terms: signed literal substitution closure for Resolution, variable identification tautological derivations, odd cubic Tseitin expander proof sizes, 3-CNF clause splitting lower-bound preservation. Google-branded search not executed; web primary-source and GitHub file reads executed.

Required external repositories read: konard/p-vs-np scripts/proof_status.json SHA 93b77ed3; blkph0x/p-vs-np-proof-research affine_projection_recognition_lab/AFFINE_HULL_METHOD.md SHA bb1addfd and RESIDUAL_EQUIVALENCE_BARRIER_REPORT.md SHA 46413596; meelgroup/frat-xor/format.md SHA 986a21aa; peitl/short-proof/README.md SHA 93d2090d; openai/math/README.md SHA cc5b0a03; anthropics/formal-math/README.md SHA 1df53bfc. No Lean/CakeML/CI or historical authoritative R_mix341 parser was executed.

## B3 quantifiers and remaining transfer

B1: every total correct uniform SAT decider A has polynomial p_A with $W_R(F)\le p_A(|F|+T_A(F))$ on each UNSAT F. B2: every A has polynomial p_A with $\overline W_R(N)\le p_A(N+T_A^{wc}(N))$ for all N. B3: SAT in P implies polynomial $\overline W_{R_{\mathrm{mix341}}}(N)$ in the **same preselected** system. B1=>B2=>B3; **all OPEN**. Neither a polynomial SAT decider nor a rejecting trace yields a verified native R_mix refutation without an additional noncircular compilation/reflection theorem.

Next LSPV-3: independently test signed substitution with tautology parents and exact source bytes. LSPV-5: adversarially test native mixed shortcut, private/exported wires and illegal weakening. Lead: authenticate historical DEF/facets/LOCAL, seek all-mixed lower-bound invariant and a genuine B3 mechanism. Keep two Route A, three Route B, unchanged task schedules/weights; Route A FLMV same-machine iteration remains a different open arrow. Root main.tex returned an existing blob SHA but zero readable contents; not safely edited. **P versus NP OPEN.**
