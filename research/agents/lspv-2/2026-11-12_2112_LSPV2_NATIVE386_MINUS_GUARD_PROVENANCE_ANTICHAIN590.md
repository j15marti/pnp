# LSPV-2/590: An exact source-provenance antichain at a native Resolution clause

**2026-11-12 21:12 PST | LSPV-2 SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate and four falsifiers

In a fixed externally authenticated signed SOURCE, the same penultimate clause [-g] has k incomparable inclusion-minimal SOURCE supports, each realized by an unchanged archived /386 checker-accepted proof. A value-canonical abstract state with only one exact SOURCE support for each clause cannot represent every concrete valid proof history.

Precommitted falsifiers: F1, a proper subset of an odd K4 component is still UNSAT; F2, the native-accepted witnesses have different penultimate clause values or identical SOURCE ancestries; F3, original verifier rejects a genuine positive or accepts a forged signed parent/source/charge; F4, an OR-antichain refinement admits partial-core spurious supports or loses accepted complete-core alternatives. Symbolic proof and finite exact controls address all four in the restricted model.

## Theorem 590.1

Let k be odd and k>=3. Take k variable-disjoint odd-charge K4 Tseitin components with exactly sixteen signed blocking clauses each. Guard each original clause by an additional literal -g and add the unit SOURCE [g]. Denote the sixteen guarded SOURCE clauses of component j by V_j. The fixed SOURCE has 16k+1 compulsory records.

For every subset T of the 16k guarded clauses, the following equivalence holds:

$$
\boxed{\bigwedge_{C\in T} C\models -g
\quad\Longleftrightarrow\quad
\exists j:\ V_j\subseteq T.}
$$

Consequently, for this one identical signed clause [-g], the inclusion-minimal semantic SOURCE-support antichain is exactly

$$
\mathcal A_k(-g)=\{V_0,\ldots,V_{k-1}\},\qquad
|\mathcal A_k(-g)|=k,\qquad
\bigcap_j V_j=\varnothing,\qquad
\left|\bigcup_jV_j\right|=16k.
$$

**Proof.** Under g=true the guarded clauses reduce to k independent odd-charge K4 Tseitin formulas. The full sixteen clauses of a component are inconsistent because XORing its four vertex parity equations yields 0=1. Any proper subset of a component is satisfiable: select a missing forbidden-pattern clause, prescribe that local forbidden assignment, and solve the parity equations at the other three K4 vertices. Since K4 is connected and the missing vertex charge can absorb the necessary oddness, a six-edge assignment exists satisfying all retained vertex clauses. If no entire V_j is contained in T, choose one satisfying assignment per disjoint component and set g=true, so T does not entail -g. If a whole V_j is present, g=true is contradictory, giving T entails -g. Thus the minimal supports are exactly the k disjoint V_j sets. QED.

Every original-/386 accepted fixed-source proof in our corpus has 27 paid RES ancestors of exactly [-g], whose original SOURCE ancestors are the 16 records of a selected component j. One final RES combines [-g] with original [g] to produce the empty clause. Each certificate pays 28 distinct Resolution identities plus one globally once-paid declared gate owner: W=29. The complete original SOURCE, original owner bank and original checker remain identical across the alternative proofs. The W29 proofs are existence/upper-bound witnesses, not optimal-minimum claims.

The example **falsifies an exact single-support-per-signed-clause quotient**, not a conservative MAY abstraction admitting union or alternative states. Neither universal storage nor SAT machine-time lower bounds follow.

## Conditional alpha/gamma and CEGAR

For a restricted concrete SOURCE/DEF/RES prefix, give every original SOURCE record i the singleton provenance bitmask {i}, each RES the union of its signed parents' SOURCE masks, and separately track all globally distinct paid RES identities. DEF facets require separately retained once-paid owners and freshness; contexts and unknown operations cannot be erased from the complete historical state.

For **semantic [-g] entailment in this fixed family only**, let

$$
\alpha_k(-g)=\mathcal A_k(-g),\quad
\gamma_k(\mathcal A)=\{T:\exists S\in\mathcal A,\ S\subseteq T\}.
$$

The theorem makes gamma(alpha) equal the family of original SOURCE sets semantically entailing [-g]. This is NOT an exact characterization of proof realizability nor a proven full-calculus cost-sound transformer. The local CEGAR condition excludes fake partial K4, singleton-per-component, guard-only and empty supports, preserving all complete-component proofs and their supersets. The still unknown mixed rules must be conservatively overapproximated until recovered.

## Original checker experiment

The pinned unchanged restricted original /386 CLI is experiments/arc/lspv2_386_independent_verify.js (Git blob 338305c0ce101704205e57543756b8127074a986, SHA256 22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113), NOT an authoritative checker for historical full R_mix341. Pinned W29 seed SHA256 0d8b1894f91d00c554727a92fed35b2bb58f2b1602f2a3cfcb949effda43ceb0; independent signed SOURCE SHA256 3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c.

In local Node v22.16.0 original-OS checker subprocesses, **8/8 positive certificates ACCEPT and 6/6 hostile negatives REJECT**, with **59,000 accepted assertion groups**, **88 native built-in negative checks** and **79 independently implemented checks**. For k=3, 49 compulsory SOURCE records yield three distinct same-clause [-g] supports of 16 records each; for k=5, 81 compulsory SOURCE records yield five. All source supports are pairwise disjoint, and complete native certificates remain W29. All 16 K4 one-clause-deletion variants have satisfying assignments among 64 possible assignments, whereas the complete 16-clause source is UNSAT. Four spurious abstract supports were rejected and four genuine supports/supersets retained.

The six original-checker hostile mutations were wrong penultimate clause, zero pivot, cross-component parent, forged SOURCE, unsupported AND3 opcode, and underpayment. The original accepted k3 certificate SHA256s exactly reproduce /589: 7a514e4dd20f8c77c84ef700ffd66af48e44bce6b1dba0105a2c1ac98772f9d4; 4a972f132d1045c8da01f75a827236e7d8737c127832a1151473d66037c571cf; 1effde5610a56b6f9981d70b64c02bbd9a4865e876b0de2b70cba1fae7ade205. The complete locally executed reference runner SHA256 was fb127edc836ce6cb64478e22f83712d3da957e2743fa3203b0f3710a6493c377; its exact complete raw file SHA256 d42fbde9b21cd6e7883ed593922a78797f495ae34a55dcb2a62ae6d4a5cc9f05. The published GitHub runner is a semantically equivalent code transcription; the exact original locally executed bytes are in the companion evidence archive.

Reproduce: node experiments/arc/lspv2_590_provenance_antichain.cjs experiments/arc/lspv2_386_independent_verify.js results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json results/raw/arc/574_k01_SIGNED_SOURCE.cnf results/raw/arc/2026-11-12_2112_LSPV2_590_PROVENANCE_ANTICHAIN_RAW.json.

Distinguish once-paid logical work, certificate bytes, construction and checking time, shared-DAG span and physical peak memory. The original /341 SOURCE/AND3/XOR checker authenticates a different, noncomposable fragment. Reject unsupported full R_mix341 inferences only in the restricted /386 language; retain them as MAY in any purported all-rule analysis.

## Precedent, literature and proof obligations

Reviewed the complete proof1.txt (Git blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343), complete proof2.txt via blob (f678f707880da4dfc97dabf778430c6dc816cb1f), issue #3, AGENTS.md, CODEX.md, the pnp-research skill, recent five-role handoffs, authentic /341 and /386 source/checker materials, actual LSPV-2 reports 539-549 and subsequent work through /589, peer LSPV-1/609 and LSPV-5/517. This result sharpens /589's fixed-source *terminal* alternative cores to an exact intermediate-signed-clause provenance distinction; it does not claim novelty for disjoint K4 unsatisfiability or source-core OR choices.

Primary scholarship: Cousot and Cousot, Abstract Interpretation, POPL 1977, DOI https://doi.org/10.1145/512950.512973 ; Clarke et al., CEGAR, CAV 2000, DOI https://doi.org/10.1007/10722167_15 ; Cook and Reckhow, JSL 1979, DOI https://doi.org/10.2307/2273702 . The external FRAT-XOR/XLRUP specification is not native historical R_mix341 authority. Cross-domain theorem transfer holds only for this expressly defined powerset source-support semantics; transfer to the native proof-rule cost or physical resources is an unproved analogy.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt and proof2.txt were not modified. Root main.tex was read completely via blob fcb400b6ae1f2629458d9ab091b7860908513bc3 and left unchanged to avoid a 2.3MB ownership-unsafe rewrite for restricted regression evidence. Exactly five enabled roles retain historical Pacific schedules, 2 Route A/3 Route B allocation, titles, fixed rules/weights and ownership; no automations were changed.

**P2-D1, full P2-C3, P2-B1, separate P2-B2/B3, P1-01/03/04 and P versus NP remain OPEN.** Next acquisition target: an original single dispatcher accepting a genuine source-bound RES-to-AND3 or paid DEF-to-LOCAL-CONVERT transition and rejecting a corrupted signed port.
