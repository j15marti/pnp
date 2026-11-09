# LSPV-3/528: Source-shared, paid two-copy reconvergence in declared ER2-OWNER

**2026-11-09 00:55 PST, Route B. PROVED/RESTRICTED symbolic composition lemma; COMPUTATIONAL certificate replay. P versus NP OPEN.**

**Affected new proof-chain node:** [P2-L3-528]. Depends on [P2-L3-523] and [P2-L3-526], refines [P2-D1], [P2-C3] and [P2-F6]. [P2-B1] and [P2-B2] remain OPEN. [P2-L1-528] is an existing *different* spectral result.

## IDEA, falsifiable prediction, and four precommitted falsifiers

Hypothesis: Two source-authenticated copies of the existing 21-original-clause modulo-three CORE-to-zero-adder module, with identical original sources and common unconstrained inputs but globally fresh private AND2 DEF owners, can be joined using exactly **two oriented binary RES steps per output bit**. The join must derive the two implications rather than invoke an equality/semantic oracle. Falsifiers: (F1) duplicated/foreign source or padded AMO axiom, (F2) colliding gate IDs/owners or unowned facets, (F3) an invalid RES pivot/consequent or false output equality on a source model, (F4) silently treating a declared ER2 owner-facet trace as historical R_mix341 accepted bytes. F1-F3 were tested and not observed, while F4 remains an explicit model boundary.

## SEARCH, authenticated scope, and reuse

Read *complete* root proof1.txt (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (pre-run blob 98d1e6df14f43fe359f649ac79506731526a3e32), current issue #3 and LSPV-5/454, AGENTS.md (19656af102604d5f0a721d548cf2e4e72a063561), CODEX.md (754999f50de93cdb693ed37bc8110d31e9e698ef), project research skill (b8df83a7b0b1428f349b0e02ce1387d979e8db7f), governing five-role refocus (c3889a3e514ddbd747150dcb68607013a3b2d154), and frozen historical R_mix341 prose at research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (c87acd11d32ccfc3b7acd3667ef11daeb60079cb). Read specific historical local modules /523 and /526, /527 finite Resolution upper control, LSPV-1/528, Grok's actual GROKPROOF/2026-11-06_2316_PROGRESS.md (a20fb8b3640d7574faf238a4a83a021bb0984808), and Claude world-ledger README (de75a371ce3143a4495e6892df7fb04794a6b708). The preceding modules are *reused*, not claimed as discoveries.

External repositories inspected at actual paths/blobs: konard/p-vs-np README.md (0e0ec77f83ad6eec1719a96066108b96ac1c2a95) and proofs/p_not_equal_np/README.md (3a0304116e719948122302849ccae38d3890e410), conditional finite-machine conclusions only; blkph0x/p-vs-np-proof-research README.md (f397a7747eaca82df3d754d0a4b4bab1fe10f814), bounded/conditional results; meelgroup/frat-xor format.md (986a21aa92b62f844ef1fce852193142c41b2b1f), XLRUP high-arity source hints with distinct grammar; tanyongkiam/cake_lpr README.md (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c), final 2026-11-01 LPR release; peitl/short-proof README.md (93d2090dba9739bc4983c65ea639a24e1f5e0fab), bounded shortest-Resolution proof search. Targeted openai/math search located proof-assistant and complexity work, but no exact accepted-byte R_mix341 grammar. Google-type web search returned Pang's relevant primary paper; no claim of exhaustive literature search.

**Established hard-family ledger:** Shuo Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (24 October 2026), [Theorem 7.2(b)](https://arxiv.org/html/2610.00837v2) proves $\exp(\Omega_{p,r}(N))$ refutations for modulo-$q$ Tseitin formulas on fixed-degree regular edge-expander families, in $\mathrm{Res}(\mathrm{PC}_r/\mathbb F_p)$ with fixed prime $p\ne q$ and fixed $r$. His Corollary 7.3 exhibits $O(N)$ proofs in matching-field $\mathrm{Res}(\mathrm{lin}_{\mathbb F_q})$. This project's **local**, strict-3CNF CORE is not itself an asymptotically hard expander formula. It has 21 source clauses over 9 CORE one-hot indicator variables, plus 3 unconstrained input indicator variables shared by the two proof modules. The 21 clauses comprise 18 signed forbidden ternary assignments for a specified mod-3 charge/sign pattern and 3 ALO original clauses. The certificate is in separately defined signed DEF_AND2+owner facets+binary RES, *not* the polynomial calculus or R_mix341 native grammar.

## PROVED/RESTRICTED lemma: paid source-preserving two-copy port equivalence

Suppose a **supplied valid** proof DAG $\pi$ from original source $S$ derives, for each $j\in[m]$, both $(\neg o_j\lor a_j)$ and $(o_j\lor\neg a_j)$. Construct a second copy $\alpha(\pi)$ by fixing all original SOURCE references and $a_j$, injectively renaming every fresh private DEF variable and its owner/facet references, and leaving the legal inference grammar unchanged. Then the union of both DAGs with source leaves shared derives two cross-copy equivalence directions by ordinary oriented binary resolution:

$$
\frac{(\neg o_j\lor a_j)\qquad(o'_j\lor\neg a_j)}{\neg o_j\lor o'_j},
\qquad
\frac{(\neg o'_j\lor a_j)\qquad(o_j\lor\neg a_j)}{\neg o'_j\lor o_j}.
$$

Both branches of the proof of each equivalence remain present as AND obligations. No branch-local assumption crosses contexts. If each base proof has $W$ paid nodes and $L$ serialized records containing $s$ identical original SOURCE records, the explicit disjoint-private construction has $2W+2m$ paid nodes and $2L-s+2m$ total records; reuse of other legal identical subproofs may reduce these upper bounds. The construction assumes a *given proof*, not a general proof-search algorithm and not an all-input B3 implication.

## ITERATE: exact certificate, negative controls, resource ledger

Starting from the archived /523 and /526 Python generators, second-copy private gate IDs 13..46 are renamed injectively to 47..80, with paid DEF owner IDs 0..33 renamed to 34..67 and exact positional facets remapped. The 21 original sources occur **once**. Six new RES inferences produce both directions of three private output-bit equalities, with source-indexed provenance. The independently written Python checker reconstructs the original 21 strict-three source clauses, verifies every owner/facet and oriented pivot/resolvent, and rejects forged sources, colliding defs, bad owner tags, future premises, false pivots, missing records and altered outputs.

| Resource | Verified |
|---|---:|
| Unique original SOURCE clauses; original variables | 21; 12 |
| Paid DEF_AND2 owners; owner-facet records | 68; 204 |
| Paid RES; new cross-copy joins | 234; 6 |
| Distinct paid logical work | **302** |
| All explicit records | **459** |
| RES premise references; DEF input-literal references | 468; 136 |
| Ideal weighted dependency span, DEF inputs and RES; unlimited processors | 19 |
| Python compact reference certificate | 40,015 bytes |
| Python compact certificate SHA-256 | 0589a729a885d0d32061db439e723bdf9766c1deb65dfe61d15f1f59894a0f67 |
| Complete Python local replay: wall time; maximum RSS | 4.69 seconds; 97,928 KiB |

24 distinct sign/charge combinations have valid syntactic certificate replays. For two configurations, the independently written semantic checker tested all $2^{12}=4096$ original assignments, including 72 satisfying source assignments per configuration, with no erroneous output equalities. Twelve deliberately malformed/corrupted certificate variants were rejected. An independent Node.js implementation was also run against a faithfully reconstructed base /526 packet and reproduced the 459-record, 302-paid counts and six independent negative checks. The published Node.js script uses the repository's actual /526 producer and that producer's existing pinned /523-/524 upstream blobs; its own directly executed readback using the live repository dependencies was not performed in this run.

The logical optimum gives **free choice of legal derivation** and excludes offline discovery costs. Our measured Python host execution includes certificate construction, checking and negative controls only; remote source/index/head reads, publication, network requests, multiple-agent search and external checker costs are distinct and additional. Neither the 19-level dependency span nor the 302-node work converts automatically into Turing time or FLMV peak space. No official CakeML/XLRUP or historical R_mix341 checker was executed.

**Result:** a genuine separately-scoped, original-source-authenticated *congruence/reconvergence* control. Not established: native historical [P2-D1] accepted DEF facets, private/exported port grammar or LOCAL-CONVERT; complete all-rule mixed normalization [P2-C3]; superpolynomial [P2-B1]; noncircular same-calculus [P2-B2]; global odd-Tseitin UNSAT proof from these local modules; or P-versus-NP resolution. Next port: compose two *different* incident-vertex modules with shared original edge inputs and charged congruence/cancellation, then validate against the historical byte grammar. No rules/weights, task identities, schedules, enabled states, or two Route A / three Route B allocation changed. Root main.tex returned zero content bytes at blob fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba and was left untouched. P versus NP OPEN.
