# LSPV-3/456: PC-degree versus paid-DEF exposure on established hard strict-3-CNF

**2026-11-06 10:24 PST | Route B primary | DERIVED/CONDITIONAL (cited 2026 preprint), PROVED/RESTRICTED combination with prior scoped compiler, COMPUTATIONAL finite control.** P versus NP OPEN; B1/B2/B3 and an all-rule superpolynomial full \(R_{\mathrm{mix341}}\) minimum OPEN. No changes to the fixed original grammar, paid weights, task IDs, schedules, enabled roles, or Route A/B allocation.

## 1. IDEA, falsifiers, actual revision

**Hypothesis before SEARCH:** Apply the previously proved LSPV-2/369 GF(2)-preserving *same-source* definition-exposure compiler to the already published **random proper strict-three CNF family**, rather than Braun's width-\(2\ell\) bit-PHP. Combine with Pang 2026's quantitative Polynomial Calculus degree--Res(PC) size theorem to obtain a parameterized charged-work / definition-exposure tradeoff. This avoids an unproved strict-three gadget lower-bound transfer, but may remain restricted by historical LOCAL/DEF export typing.

Four falsifiers:

1. Pang's published family is not exact strict 3-CNF, not hard for unrestricted shared-DAG Res(PC1/F2), or requires \(n\)-dependent \(r\). **Rejected:** author HTML v2 Theorems 1.1 and 7.2(a), Section 7.1 confirm the family and model.
2. The /369 compiler applies only to bit-PHP or expands global parity rows exponentially. **Rejected:** its exact theorem applies to *any* original CNF under a specified locally opaque, wire-defined proof subgrammar, and simulates arbitrary-width XOR natively.
3. The sharp literal constant \(2048\) in Pang's **syntactic** lower bound transfers unchanged through /369's semantic-weakening proof without a conversion charge. **This falsifier FIRED:** Pang's formal Theorem 1.1 uses syntactic rules; /369 uses semantic weakening. His Remark 1.2 notes a polynomial syntactic simulation, not a no-overhead identity. We consequently retain a uniform existential constant \(c>0\) and charge explicit proof evidence instead of advertising a false sharp 2048 bound for the mixed source.
4. A source-unbound finite proof, incorrect RES pivot, SAT source incorrectly UNSAT, or malformed/corrupt input passes reproduction. **Rejected in finite tests:** independently implemented Node replay and adversarial controls passed.

**Duplication audit:** LSPV-2/369 already proves the generic \(2^b\) compiler and its application to Braun bit-PHP. LSPV-3/442 already records Pang's random-3CNF hardness, exact distribution, and deletion resilience. Their **composition into an explicit PC-degree work/exposure invariant on strict-three ORIGINAL sources** was not found in targeted project searches ("Pang 2^b", "Pang 64q", "random3 backtransfer", "D^2/(2048"). No academic originality claim follows from this non-exhaustive search. The present run independently checked the **direction** and syntactic-overhead caveat and produced a new finite original-source RES control.

## 2. Exact published source and lower-bound ledger

For every integer \(n\ge3\), let \(F\sim\mathcal F(n,3,8n)\): independently choose **8n clause indices with replacement** from all \(8\binom n3\) proper signed three-literal clauses. There are \(n\) occurring variables, \(8n\) source indices, each clause has exactly three distinct variables, and ordinary normalized DIMACS occupies \(N=O(n\log(n+2))\) binary bits. The distribution, including repetitions, is exactly Pang's Section 7.1 \(w=3,\Delta=8\) specialization. Unsatisfiability holds with probability \(1-o(1)\). Certified hardness is asymptotic/with high probability in a particular proof model, **not** certified difficulty of our finite 10-variable fixture.

**Published input-degree result:** Alekhnovich--Razborov (2003), as used in Pang v2 Section 7.1, establishes \(D\ge\delta n\) for some fixed \(\delta>0\) in polynomial calculus over the selected prime field, a.a.s., for this distribution.

**Published proof-size result:** Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, dated **24 October 2026** (preprint, not promoted to peer-reviewed authority), Theorems 1.1 and 7.2(a). For \(p=2,r=1\), lines are disjunctions of affine GF(2) equations; native rules are **syntactic** weakening, contraction, deletion of false constants, linear-combination inference and bounded-degree multiplication. DAG-like sharing is permitted; no paid conservative extension variables. If \(\mathcal Q(F)\not\vdash_D1\) and \(D\ge\max\{32,8w(F)\}\), then EVERY syntactic proof with \(S\) nodes satisfies

$$
\ln S\ge\frac{D^2}{2048n}.
$$

For \(w(F)=3\), \(D\ge32\) is sufficient to meet the displayed theorem's numerical threshold. The proof and random-family application are separate statements. Asymptotically almost surely, this gives \(\exp(\Omega(n))\) DAG Res(PC1/F2) proof size (Theorem 7.2(a)).

**Known shortcuts and guards:** ordinary DAG Resolution includes native RES; algebraic XOR can drastically shorten expander Tseitin proofs despite ordinary Resolution hardness (LSPV-2/341 proves mixed optimum \(4h-1\) for bridgeless cubic odd Tseitin). Cook's Extended Resolution PHP gives polynomial proofs in a stronger grammar even where Haken ordinary Resolution is exponential; LSPV-1/453 independently makes ER bit-PHP backtranslation impossibility precise. Every actual native shared/branching/paid-DEF shortcut on random 3CNF remains legal and cannot be excluded to protect a hardness claim. The random family is **not** claimed to be hard for the full mixed calculus.

## 3. Already proved source-preserving scoped compiler (LSPV-2/369, cited not newly claimed)

Fix the historic semantic \(R_{\mathrm{mix341}}\): free original clauses; unit-charge native oriented binary RES, original-3-variable exact AND3/LOCAL, arbitrary-support native GF(2) XOR, charged conservative fresh binary DEF. Restrict to the previous \(\mathcal R_{\rm opaque}\) subgrammar: no uncharged internal LOCAL wire exports, every non-RES/non-XOR condition has exact extensional support <=3 original variables, and DEF outputs are fresh paid owners with named arity-two dependencies. Set \(q\) equal to distinct charged nodes in a refutation \(\pi\); let \(B\) be the **set of distinct original variables occurring directly as DEF input wires**, and \(b=|B|\). The after-the-fact ideal minimum still optimizes over all legal derivation DAGs within the fragment and counts shared nodes only once.

**LSPV-2/369 theorem:** The original **same** source \(F\) has a DAG Res(XOR) proof with semantic weakening of at most

$$
T=2^b(2m+64q+2)
$$

lines, where \(m\) is the number of authentic source clauses. Proof: fix each of \(2^b\) assignments to the exposed original variables, evaluate paid unique DEF gates, translate each restricted source/LOCAL factor/RES/XOR derivation (global affine rows remain native), prefix each branch with its forbidden assignment clause and combine all \(2^b\) branches using paid ordinary cuts. Input-to-output proof bits and machine costs are separate. It is a **given-proof transformation**; no free split or discharge rule was added to historic \(R_{\mathrm{mix341}}\).

**Crucial mismatch**: Pang's exact numeric \(2048\) theorem applies to **syntactic** Res(PC1/F2); the bound \(T\) above is on **semantic weakening**. Pang §1 Remark 1.2 states semantic weakening admits polynomial syntactic simulation (citing Itsykson--Sokolov). Therefore for some fixed polynomial \(P\), the translated semantic certificate of \(T\) lines and polynomial-per-line explicit bits yields a syntactic certificate of at most \(P(n+T)\) nodes. In our original strict-3 encoding, the source length is polynomial in \(n+m\), and each line uses polynomially encoded signed and affine masks plus at most \(b\) branch guards. As \(b\le n\), the total evidence is at most \(T\,\mathrm{poly}(n+m+q+1)\). A fixed polynomial syntactic compiler yields, for **some** universal \(C>0\),

$$
\ln S_{\rm syn}\le C\left(b+\ln(n+m+q+2)+1\right).
$$

The exponent and coefficients of \(P\) have NOT been independently optimized or certified; hence the finite sharp numeric comparison is only diagnostic. Use the asymptotic result, not the uncharged \(2048\) constant.

## 4. New composed theorem: PC-degree/DEF-exposure charge (PROVED/RESTRICTED GIVEN CITED THEOREMS)

**Theorem 456.1 (conditional on Pang 2026 and the previously proved scoped /369 compiler).**
There is an absolute constant \(c>0\) such that for every UNSAT proper strict 3-CNF \(F\) with \(n\) occurring variables and \(m\) authentic source clauses, any integer \(D\ge32\) for which \(\mathcal Q(F)\not\vdash_D1\), and EVERY paid shared-DAG refutation \(\pi\) belonging to the **locally opaque wire-defined** fragment, with \(q\) paid distinct nodes and \(b\) original DEF input exposures, one has

$$
b+\ln(n+m+q+2)+1\ge c\,D^2/n.
$$

**Proof:** Pang Theorem 1.1 yields \(\ln S_{\rm syn}\ge D^2/(2048n)\). From the exact original-source proof \(\pi\), the cited LSPV-2/369 compiler gives a semantic-weakening Res(XOR) certificate of \(T=2^b(2m+64q+2)\) lines. Pang's explicitly stated semantic-to-syntactic polynomial simulation gives a syntactic certificate of size \(\mathrm{poly}(n+T)\), since the translator's line arity, row masks, source references, and branch blocker bits are each polynomial in \(n+m+q+b\), and \(b\le n\). Thus \(\ln S_{\rm syn}=O(b+\ln(n+m+q+2)+1)\). Combine the inequalities. This is **not** a new independent proof of Pang's PC-degree theorem or LSPV-2/369's scoped proof translation.

**Corollary 456.2 (hard original strict 3-CNF families):** For \(F\sim\mathcal F(n,3,8n)\), Pang's 7.2(a) and its cited linear PC-degree antecedent imply that for a.a.s. such \(F\), EVERY \(\mathcal R_{\rm opaque}\) mixed refutation satisfies

$$
b+\ln(n+q+2)=\Omega(n).
$$

For a fixed sufficiently small \(\epsilon>0\), every such proof with \(b\le\epsilon n\) has

$$
q\ge\exp(\Omega(n)).
$$

In particular **all DEF-free proofs within the scoped calculus** have exponential paid mixed logical work on this family, even with arbitrary global GF(2) XOR, exact 3-local transformations, shared proof DAGs, and optimal after-the-fact rule choice. A polynomial-\(q\) proof, if it exists in this fragment, must have \(b=\Omega(n)\) (linear distinct original variables explicitly feeding paid definition owners). With normalized original bit length \(N=O(n\log n)\), \(\exp(\Omega(n))\) implies \(\exp(\Omega(N/\log N))\) along the family, *within this fragment only*.

The exact coefficient in the degree term is NOT claimed through the semantic-to-syntactic converter. The finite \(n=10\) original is NOT certified to have PC degree \(D\ge32\), so the asymptotic theorem does not predict or exclude its short exhibited proof.

## 5. Independently executed finite control

A new Python source generator (seed **261000837**) drew 80 proper signed 3-clauses with replacement on **n=10** original variables (finite PRNG fixture only), enumerated all \(2^{10}\) assignments, and produced an actual original-source authenticated strict-RES refutation via Davis--Putnam projection. It generated **989 candidate RES nodes**, but the final original-source-indexed goal ancestry prunes to **19 paid RES nodes and 19 used original sources**. This is a legal shortcut and **upper bound**, not a minimum or a hardness certificate. The original has **0 models** and at least **3 falsified source indices under every assignment**, so deletion of any two indexed source clauses retains UNSAT. Separately generated planted-zero SAT control has **exactly one** model.

Independent Node.js checker separately implemented strict DIMACS parsing, original SHA256 source authentication, complete SAT/UNSAT enumeration, oriented pivot RES verification, exact output clauses, acyclic references, full root ancestry and node accounting. It passed **164,451 assertion groups**, rejected **six corrupted source/proof mutations** and **five malformed original inputs**. Original source byte length **799**, proof JSON **2930** bytes. Original SHA256 **cbd93d74d9716741b69db9203a34a4c2818a112131306020d681b40da3142a9c**; SAT source SHA256 **9f38aabb14af1d1a3a5a6b93df5ac3caf21a644acf0f9c6dee230d340d244a40**; proof JSON SHA256 **4b4c723f82b6245b769a7579aca098b6da845a7e8df24f7753006421f5923c4a**. The finite sample is **not** a peer-certified hard individual formula and does not validate Pang's asymptotic theorem.

Host Linux physical ledger: Python producer approximately 1.12 s wall and peak RSS **96,656 KiB** (embedded source-to-output timer ~0.129 s; process/tool overhead additional). Independent Node checker ~0.08 s wall, peak RSS **32,116 KiB**. All \(2^{10}m\) assignment-clause checks, candidate-resolution generation, ancestry pruning, parsing, hash comparisons, output serialization and failed controls were paid by the actual programs and are **not** included in ideal \(W_R\). Remote GitHub/web/source acquisition, administrative I/O, and combined all-phase simultaneous peak are not measured; no same-machine FLMV exponent is asserted.

**Full reproducibility ZIP** in this conversation: \`LSPV3_456_PANG_PC_DEGREE_DEF_EXPOSURE_REPRO.zip\` with \`producer.py\`, independent \`verify.js\`, source DIMACS, raw root certificates, machine result JSON, analysis diagnostic \`exposure_bound.py\` and SHA256 manifest. The code running the numeric \(2048\) inequality explicitly warns that **semantic versus syntactic overhead must be charged**; it does NOT certify PC degree or source hardness.

## 6. Literature, project, repo and actual access audit

Primary author HTML checked: \`https://arxiv.org/html/2610.00837v2\`, Theorems 1.1/7.2(a), §7.1 and Remark 1.2, arXiv v2 dated **24 October 2026**; Alekhnovich--Razborov PC-degree primary result cited by Pang; Itsykson--Sokolov, *Resolution over Linear Equations Modulo Two*, APAL 171 (2020) 102722; Chvátal--Szemerédi, *Many hard examples for resolution*, JACM 35 (1988) 759--768; Haken TCS 39 (1985) 297--308; Cook 1976 ER PHP; Braun arXiv:2609.23015v2 revised 2026-11-03 (Res(XOR) restricted). Pang gives a stronger \(\exp(\Omega(n))\) Res(XOR) bit-PHP lower bound than Braun's \(\exp(\Omega(n/\log^2n))\) for that separate non-3CNF source; this was not silently transported to strict three.

Project sources read: governing Nov2 five-role handoff blob c3889a3, issue #3 current; original /341 blob c87acd11; LSPV-2/369 \`research/agents/lspv-2/2026-11-03_1212_LSPV-2_BRAUN_GF2_NATIVE_BACKTRANSFER369.tex\` blob 927ba217; LSPV-3/442 blob e8c0802d; LSPV-3/455 blob a12eab9; LSPV-1/453 blob e906758; LSPV-5 REFEREE390 blob ac73d0f; LSPV-3/406 blob 4d2abf9; LSPV-3/415 blob d6a22f3; LSPV-3/453 branch discharge blob 760cce9; LSPV-5 REFEREE367 blob 7bb7dcf; LSPV-5 REFEREE371 blob c00d39e; AGENTS.md, CODEX.md and \`.codex/skills/pnp-research/SKILL.md\` (read in previous project runs). **The earlier /453 width theorem is a duplicate of sharper /361** as already corrected in /455; not presented as a new result.

Independent external actual texts reviewed: \`konard/p-vs-np/scripts/proof_status.json\` blob 93b77ed (formal theorem manifest, no fixed-R bridge); \`blkph0x/p-vs-np-proof-research/METHOD_INDEX.md\` blob 18d693e and \`resolution_width_lab/THEOREM.md\` blob b903042 (Resolution-only width closure); \`meelgroup/frat-xor/format.md\` blob 986a21a (different XLRUP/FRAT-XOR checker); \`tanyongkiam/cake_lpr/README.md\` blob e94f45e (CakeML LPR, new version announced 1 Nov 2026, not native /341); \`peitl/short-proof/README.md\` blob 93d2090 (Resolution-only optimizer); \`MassimoLauria/cnfgen/cnfgen/families/tseitin.py\` blob 4bb5fd1 (published fixture generator); \`openai/math/README.md\` blob cc5b0a (raw research repo, not a /341 compiler). Grok actual \`GROKPROOF/2026-11-06_1617_PROGRESS.md\` blob b931933; Claude actual \`research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex\` blob b7150b9. Neither supplies B3. Actual indexed web and GitHub connector searches performed; no Google-branded UI was available/used. No local full-git-project preflight or Pang formal proof kernel replay, and no historically authoritative R_mix341 accepted-byte checker run. Do NOT interpret independent finite RES replay as native all-rule checker acceptance.

## 7. Remaining exact bridge and ownership

The fixed calculus historical **accepted byte** language for paid DEF defining facets, LOCAL private/export wires and their subsequent consumer scope remains incomplete in prose. The theorem does not include every possible full-R proof, because an untyped internal-wire LOCAL shortcut or nested facet consumer may evade \(\mathcal R_{\rm opaque}\). The new tradeoff **permits** strong definitions and specifies the necessary exposure; it does NOT prove every legal R proof has \(b=o(n)\), which would be contradicted by known ER-style bypasses in other families. No superpolynomial \(\overline W_{R_{\mathrm{mix341}}}\) has been established, nor B1/B2/B3. A preselected refutation system's proof-size lower bound cannot be interpreted as all-algorithm SAT hardness without B3. P versus NP remains OPEN.

**Next attempt:** Extend the exact same-source proof compiler /369 across the *historical* owner-qualified DEF facets and private/exported LOCAL circuit ports with polynomial normalization and no free answer oracle; or supply a legal typed counterexample that violates the claimed source retraction. If a full export interface is not specified, mark the ambiguity instead of choosing CANON1/2. Then test whether the genuine all-rule minimum can beat the degree/exposure bound via known ER, shared branch and reconvergent circuit shortcuts. Original root \`main.tex\` remains untouched because complete authorized content was unavailable; no other role's manuscript modified.
