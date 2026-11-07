# LSPV-1/488: Paid 3-CNF Resolution certificate for a nonaffine three-template guard cover

**2026-11-07 America/Los_Angeles (PST) | Route B | PROVED/RESTRICTED symbolic construction; COMPUTATIONAL certificate replay | P versus NP OPEN.**

**Proof-chain nodes:** Material evidence for [P2-F13] (narrow syntactic closure of one /487 guard-cover obligation); [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. No fixed historical R_mix341 rule or weight is changed. This is a **distinct** fully explicit 3-CNF definitional extension + ordinary Resolution control, not a historical accepted-byte certificate.

## IDEA, falsifiers, searched evidence, revision

**Initial hypothesis:** LSPV-1/487's abstract three-affine-template cover of two independent AND outputs has a *paid syntactic cover certificate* requiring only conservative 3-CNF gate definitions and ordinary oriented RES, without giving case-split/discharge for free.

Precommitted falsifiers: (F1) a valid input to the named AND gate escapes all three guards; (F2) the supposed guard-cover clause is not derivable from the stated definition axioms using RES alone; (F3) the derivation implicitly reuses an incompatible branch-local lemma or omits an AND case; (F4) the syntactic construction needs unbounded hidden source work or fails the permitted 3-clause-width control. F1 is excluded by a Boolean case proof and exhaustive 16-input replay; F2 and F3 are excluded for the **named distinct calculus** by the explicitly checked 30-node ancestor DAG, all 18 RES pivots and six hostile tests. F4 is excluded for this **constant local gadget**, with 24 authentic 2/3-literal defining facets and 18 RES steps. Historical admissibility of paid definitions, guards and RES->AND3 links remains OPEN.

**SEARCH and reuse:** Read both full root trackers (initial blobs proof1 `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, proof2 `babe439424d871c5f80c5627af549d1aabb14047`), the governing November 2 five-role handoff, AGENTS.md, CODEX.md, the pnp-research skill, current issue #3 and latest peer comments. Reused LSPV-1/485, /487; LSPV-3/483; LSPV-5/417; actual Grok `GROKPROOF/2026-11-07_1920_PROGRESS.md` blob `231561ce216699f286b705a0056584789ba9ee99`; and Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`. The latter concern separate machine-model barriers. Current required external reviews: `konard/p-vs-np/scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`. Their formats, bounded results and formalization percentages provide **no** native R_mix341 rule.

Primary references actually inspected: Pang, arXiv:2610.00837v2, 24 Oct 2026, Section 1 and Theorem 7.2(a) (syntactic Res(PC_r/F_p), a DIFFERENT proof system); Cook and Reckhow (JSL 1979, Section 1 and Section 4) on proof-system distinctions and paid abbreviations. Public indexed web search was used; a distinct Google UI was unavailable. No inference beyond their stated models was imported.

## Exact distinct syntax and construction

Use Boolean inputs `p,u,v,q` with **one** original nonlinear relation `q=u AND v`. In the two-gate LSPV-1/487 setting, `p` is the output of the *other* independent AND gate, but its gate law is not needed for the cover theorem. Define three affine predictions:

$$
A_0=(0,0),\qquad A_1=(1,u),\qquad A_2=(1\oplus v,v).
$$

Let `t_j` be a PAID Boolean output claiming `(p,q)=A_j`. Implement the exact claims by six conservative named gates, with ordinary 3-CNF Tseitin facets:

$$
t_0=\neg p\land\neg q,\qquad r_1=[q=u],\qquad t_1=p\land r_1,
$$

$$
r_2=p\oplus v,\qquad r_3=[q=v],\qquad t_2=r_2\land r_3.
$$

The original AND relation has three signed 2/3-literal clauses, each AND definition has three, each XOR/equality definition four. In total the packet contains **24 defining/source facets**, all width at most 3. All added variables have unique conservative defining values for every original assignment; none is a SAT-oracle, an instance-specific UNSAT axiom, or a free hidden port. That conservative-definition permission is granted ONLY in this proposed control calculus, NOT in historical R_mix341.

**Syntactic certified theorem:**

$$
q=u\land v\;\vdash_{\mathrm{paid\ Tseitin+RES}}\;t_0\lor t_1\lor t_2.
$$

The direct Boolean proof is short. If `p=0,q=0`, use `t0`. If `p=1,q=u`, use `t1`. In all other cases with `q=u AND v`, `p=1 XOR v` and `q=v`; hence `t2`. This is an OR of three legal **alternative guard choices**, not a license to omit required proof branches. The non-Boolean syntactic step is supplied by **18 oriented ordinary Resolution inferences**, checked from actual earlier clauses, no semantic inference axiom or branch assumption.

After pruning unused proof-search nodes the dependency DAG has **30 distinct nodes: 12 authentic source facets + 18 RES inferences**. It derives `[5,6,7]`, the exact positive cover clause `t0 OR t1 OR t2`. Final RES node #30 combines #27 `[5,6,10]` with #29 `[5,6,7,-10]` on pivot 10. The other 16 inferences and all pivots/parents are preserved in the full executable verifier, not merely described. The derivation contains no branch-assumption leakage, no uncharged weakening and no added case-split rule.

## Existing hard-family control and scope

Use the **published** random signed proper width-three CNF model `F ~ mathcal{F}(n,3,8n)` (uniform legal triples with signs under the author's sampling convention; n original variables, 8n clauses, encoded bits dependent on variable-ID convention). Pang Theorem 7.2(a) gives `exp(Omega(n))` lower bound asymptotically almost surely for fixed `Res(PC_r/F_p)` and fixed prime p, using the established PC degree bound. A certificate of UNSAT for a selected finite sample is separate from that high-probability family statement. This run **does not** instantiate a random hard sample, prove transfer through 3-CNF conversion, or reprove Pang's lower bound. The local cover gadget is a focused test of the *candidate mixed-to-affine translation* against the existing hard benchmark, not a newly proposed hard SAT family. The known GF(2) Tseitin and Extended Resolution shortcuts remain mandatory upper-bound controls.

The new local certificate makes it possible to certify one three-template guard tautology **if** fully charged conservative definitions and Resolution are legal. It does **not** provide a full per-branch normalization of arbitrary mixed AND3/LOCAL-CONVERT/DEF/GF(2) proof records, the necessary assumption-scope discharge, or a polynomial simulation for every legal historical inference. LSPV-1/487's abstract cover lower/upper bounds remain valid, but a 3-template cover need not be a 3-branch *native proof*.

## Independent computation, costs, and hostile controls

Executable `experiments/arc/lspv1_488_guard_tseitin_resolution.js` was evaluated in V8 before publication. It checks all 24 clause facets, the exact 30-node dependency trace, every signed parent/pivot, the final conclusion, all 16 assignments of (p,u,v,q) (8 satisfy q=u AND v), and rejects six distinct corruptions: flipped source polarity, wrong RES pivot, nonexistent AND parent, missing last joined case, forged cross-branch consequence, and duplicate node ID. Independent Python direct Davis-Putnam elimination from the same 24 facets found the exact guard-cover clause and produced the same 12/18 ancestor count. Source/identity tests prove **local** logical fidelity, not the full historic byte parser.

**Logical ledger:** paid defining/source facets 24; distinct used source ancestors 12; distinct RES inferences 18; complete facet-plus-RES output 42 records; pure ancestor union 30; ideal unit-RES critical-path depth 6. If a target calculus separately charges six new named definitions, add its own explicit weights; this run does not set or silently change historical R_mix341 weights. Certificate JSON for the 30-node DAG occupies 555 ASCII bytes. Output bits also include the 24-facet packet, metadata and source/certificate references, not just those 555 bytes. Certificate discovery cost is *excluded from the ideal minimum* but is included in measured local generation.

**Physical resource control:** one independent, unoptimized local Python search/trace run measured 0.67 seconds wall, 1.01 seconds user, 0.07 seconds sys and 95,880 KiB max RSS (Python process); this is **not** the machine cost of the published JavaScript nor an asymptotic guarantee. Actual full solver cost would include source parsing, all head/index reads, clause allocation/frees, proof search and failed choices, definition creation, retrieval/recomputation, proof serialization, verification, and all-phase peak simultaneous memory. Optimally shared logical work, work/span and realizable schedules must remain separate.

## Status and next target

**PROVED/RESTRICTED:** 18-step original-facet-authenticated Resolution derivation of the nonaffine three-template guard-cover clause in a DISTINCT paid 3-CNF definitional extension system. **COMPUTATIONAL:** 16 input tests, six corruption rejections, independent Python DP rediscovery. **OPEN:** accepted historical full grammar [P2-D1], full mixed-rule translation [P2-C3], all-rule superpolynomial minimum [P2-B1], noncircular B3 [P2-B2]. Next: obtain a historically accepted guard/DEF and a legal assumption-scoped RES->AND3 port, or a typed counterexample, then test whether the three-template cover actually improves the fully charged /485 compiler. Do not infer any new all-input time/space bound. P versus NP OPEN.

### Source bibliography

1. Pang S. *A Degree–Size Relation for Resolution over Polynomials*. arXiv:2610.00837v2, October 24, 2026, Sections 1, 7, Theorem 7.2(a): https://arxiv.org/html/2610.00837v2 .
2. Cook SA, Reckhow RA. *The Relative Efficiency of Propositional Proof Systems*. J Symbolic Logic. 1979;44(1):36-50. https://www.cs.utoronto.ca/~sacook/homepage/cook_reckhow.pdf .
3. LSPV-1/487: `research/agents/lspv-1/2026-11-07_1410_LSPV1_NONAFFINE_AFFINE_TEMPLATE487.md`.
4. LSPV-1/485: `research/agents/lspv-1/2026-11-07_1158_LSPV1_TWO_BRANCH_SYNTACTIC485.md`.
