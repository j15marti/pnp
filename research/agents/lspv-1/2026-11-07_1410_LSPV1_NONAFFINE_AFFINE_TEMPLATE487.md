# LSPV-1/487: Fourier agreement cap and non-affine three-template escape

**November 7, 2026, 14:10 PST | Route B | PROVED/RESTRICTED symbolic and COMPUTATIONAL finite checks. P versus NP OPEN.**

**Exact tracker:** [P2-F13] material scope qualification of LSPV-1/486. OPEN: [P2-D1] historical grammar, [P2-C3] whole-rule transfer, [P2-B1] all-rule superpolynomial minimum, [P2-B2] noncircular B3. Route A [P2-A2]/[P2-A5] remains separate. No change to any native rule, weight, agent, title, schedule or enabled state.

## IDEA before SEARCH and falsifiers

Hypothesis: the /486 exactly tight $2^g$ *affine-subspace* bound can be beaten if each branch region need only be a set where all AND outputs match a globally affine vector function, but the branch region itself need not be affine. Separately, any global affine prediction agrees on at most $3^g$ of $4^g$ complete inputs.

Four falsifiers: (F1) find an affine predictor with more than $3^g$ matches; (F2) find a missed assignment for the proposed three-map two-gate cover; (F3) find two predictors covering all 16 two-gate inputs; (F4) discover that the alleged smaller cover uses affine-subspace cells and actually contradicts /486. F1 fails by the symbolic character-sum proof; F2 and F3 fail under complete finite verification; F4 fails since the first validity cell has 9 elements, not a power of 2. This is a transfer-grammar falsifier, not an invented hard SAT family.

## SEARCH: exact source evidence and prior work

Read both *complete* root trackers: proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2.txt blob 1970ea10459a6318330a6b8a7f864d816405b1bb at pre-report review. Read the governing Nov 2 five-role handoff, issue #3 recent peer comments, AGENTS.md, CODEX.md, pnp-research SKILL.md, LSPV-1/485 and /486, actual LSPV-3/482 historical-grammar report, LSPV-2/476 and LSPV-4/478 (Route A), actual GROKPROOF/2026-11-07_1920_PROGRESS.md blob 231561ce216699f286b705a0056584789ba9ee99 and actual Claude ONETAPE-0001.tex blob 9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a. Existing /486 *affine-subspace* theorem is retained unchanged.

External repository checks: konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (finite-model checked P subset NP only); blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 and README.md blob f397a7747eaca82df3d754d0a4b4bab1fe10f814 (restricted/promise results and barriers); meelgroup/frat-xor format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f (actual source-ID/XOR hint syntax, NOT /341); openai/math README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae (mixed verification levels). No external P-versus-NP claim was promoted.

Indexed literature queries: quadratic Boolean Walsh spectrum/rank, vector-affine approximation of independent AND, multiplicative complexity and affine equivalence. Relevant sources: Rothaus, "On Bent Functions", JCTA 20:300-305 (1976), DOI 10.1016/0097-3165(76)90024-8; Calik, Sonmez Turan, Peralta, "Boolean Functions with Multiplicative Complexity 3 and 4" (2020), DOI 10.1007/s12095-020-00445-z. The requisite two-bit Fourier identity is proved independently here. No branded Google UI, external PDF, native historical checker, or general SAT algorithm was executed.

## Exact model

For $g\ge1$, let $x=(u_1,v_1,\ldots,u_g,v_g)\in\mathbb F_2^{2g}$, and let the named nonlinear gate output vector be $Q(x)=(u_1v_1,\ldots,u_gv_g)\in\mathbb F_2^g$. A *globally affine prediction* is a fixed vector map $A(x)=Mx+b$, with $M\in\mathbb F_2^{g\times2g}$ and $b\in\mathbb F_2^g$. Its *agreement region* is $Z_A=\{x:Q(x)=A(x)\}$. A collection of templates $A_j$ covers if $\cup_j Z_{A_j}=\mathbb F_2^{2g}$. Here the regions $Z_A$ are NOT required to be affine subspaces, in contrast to /486.

## Theorem 487.1: sharp agreement cardinality bound (PROVED/RESTRICTED)

For every $g$ and every globally affine prediction $A$,
$$
\boxed{|Z_A|\le3^g.}
$$
Equality is attained by $A=0$ since $u_iv_i=0$ on precisely three of four inputs per gate.

**Proof.** For $\chi(z)=(-1)^z$, character orthogonality gives
$$
|Z_A|=2^{-g}\sum_{\lambda\in\mathbb F_2^g}\sum_{x\in\mathbb F_2^{2g}}
(-1)^{\lambda\cdot(Q(x)+Mx+b)}.
$$
For $\lambda$ with $k$ nonzero entries, the inner sum factors across the $g$ disjoint input pairs. If $\lambda_i=0$, the two-bit linear character sum has magnitude at most $4$. If $\lambda_i=1$, the quadratic sum $\sum_{u,v}(-1)^{uv+\alpha u+\beta v}$ has absolute value exactly $2$: sum first over $v$, leaving only $u=\beta$ and contribution $\pm2$. All cross-gate dependencies in $M$ only change the linear coefficients, so factorization is valid. The triangle inequality and binomial theorem yield
$$
|Z_A|\le2^{-g}\sum_{k=0}^g\binom gk4^{g-k}2^k
=2^{-g}(4+2)^g=3^g.
$$
QED.

**Corollary, PROVED/RESTRICTED:** any cover by such agreement regions, even with overlap and arbitrary non-affine region shapes, requires
$$
\boxed{K\ge\left\lceil(4/3)^g\right\rceil}.
$$
This is an abstract template/cell count, NOT proof-node work or an algorithmic lower bound.

## Theorem 487.2: three templates for two gates and general tensor upper bound

For $g=2$, take the following three *globally affine* predictions of $(u_1v_1,u_2v_2)$:
$$
A_0=(0,0),\qquad A_1=(1,u_2),\qquad A_2=(1\oplus v_2,v_2).
$$
For each pair $(u_2,v_2)\in\mathbb F_2^2$, at least two of these three maps match the second output $u_2v_2$, and their first coordinates are $0$ and $1$. Hence *for either actual first-gate value* one of them matches both gate outputs. Therefore the three agreement regions cover all $16$ input assignments. The $A_0$ agreement region contains $9$ elements and is non-affine, so this does NOT contradict /486's exact four-*affine-subspace*-cell bound.

The independently exhaustive finite enumerator checks all $1024$ affine maps $\mathbb F_2^4\to\mathbb F_2^2$ and all $1,048,576$ ordered pairs. No pair covers all 16 inputs, while the displayed triple does. The **minimum of three templates at $g=2$** is therefore a COMPUTATIONAL exhaustive finite result, not claimed as a new symbolic all-$g$ lower bound.

Block-tensor these two-gate predictions, adding two affine templates for an unmatched final gate. Their product validity regions cover the full cube, yielding
$$
\boxed{K_{\rm template}\le3^{\lfloor g/2\rfloor}2^{g\bmod2}}
$$
for every $g$. This is a strict improvement over $2^g$ whenever $g\ge2$ IN THIS DISTINCT, WEAKER ABSTRACT REGION MODEL.

## ITERATE: verification and falsification

The actual independently executed and published pure JavaScript tests are at experiments/arc/lspv1_487_nonaffine_cover.cjs; exact raw results at results/raw/arc/2026-11-07_1407_LSPV1_487_NONAFFINE_COVER_RAW.json. At $g=2$: 1024 maps, 832 different validity masks, maximum agreement 9, 1,048,576 ordered pairs, no covering pair, and an explicit triple covering all 16 inputs. Full tensor-product covers passed for each $g=1,\ldots,8$ with respectively 2,3,6,9,18,27,54,81 templates and at most 65,536 inputs. All 1,984 additional Walsh-bound coefficient tests passed. Removing one of the three witness maps makes coverage fail; empty template set fails. A separately written local Python enumeration independently found 832 masks, max 9, no pair and a covering triple. These are *combinatorial finite* tests. They do not authenticate original SAT source encodings or native historical R_mix341 certificates, and no malformed SAT/corrupted native-certificate test is claimed.

**Critical revision:** the universal extension of /486 from AFFINE CELLS to arbitrary agreement regions is **falsified** by three cells for $g=2$ rather than four. The correct remaining theorem is the weaker $(4/3)^g$ bound in the expanded abstract model. Quadratic validity predicates $Q(x)=A(x)$ require legal and paid proof rules to establish membership, and the three region cases demand ALL branch obligations. Merely naming these sets or counting their elements is not a native shortcut, a SAT oracle, or a refutation proof.

## Established hard 3-CNF / encoding / theorem / shortcut ledger

**Random proper strict 3-CNF:** $F\sim\mathcal F(n,3,8n)$ with exactly $m=8n$ signed ternary source clauses and $n$ variables, standard literal-ID binary length $N=\Theta(n\log n)$. Pang, arXiv:2610.00837v2, 2026, Theorem 7.2(a) states with high probability $\exp(\kappa n)$ **syntactic shared-DAG Res(XOR)** proof-size hardness for some $\kappa>0$ in its exact model. LSPV-1/485's distinct typed 3-exposed-wire fragment has a restricted syntactic compiler output upper bound $C(n+1)2^g(m+q+1)$ using **affine-subspace specialization**. Present *semantic* agreement covers do not improve that bound without native proof of quadratic guards and original-source certificates. No new 3-CNF proof-size transfer is asserted.

**Cubic-expander odd-charge Tseitin strict 3-CNF:** $H$ cubic vertices, $3H/2$ original edge variables, four proper signed 3-clauses per vertex encoding local charge XOR, total $4H$ strict 3-CNF clauses, $N=\Theta(H\log H)$ encoded bits. Odd total charge certifies UNSAT. Ben-Sasson and Wigderson, JACM 2001 Theorem 4.4/Corollary 4.5 (following Urquhart) establish $2^{\Omega(H)}$ *ordinary shared-DAG Resolution* size on expander instances, not all algorithms or R_mix341. Cheap GF(2) summation is an admitted mixed-system upper-bound control and defeats naively transported Resolution hardness. Cook ER extension shortcuts and source-aware FRAT-XOR are additional controls, not excluded for convenience.

LSPV-3/482 demonstrates a polynomial shared OR-DEF export in a distinct owner-indexed FACET-A proposed system, but not native accepted-byte R_mix341 rule authority. The current proof-family ledger is not changed.

## Logical work vs machine cost

The cell/template cover numbers are not paid logical DAG counts or critical-path depths. The template coefficient matrix alone has $O(g^2)$ bits; fully expanded tensor template descriptions take $O(g^2 3^{g/2})$ bits before deduplication. Actual refutations would charge original source/index/head reads, proof discovery, gating assumptions, all mandatory AND cases, paid join/reference inference nodes, retention versus recomputation, failed branches, evidence construction, output verification, and peak simultaneous space. The ideal proof lower-bound minimum intentionally grants free optimal derivation selection, while an implemented translator must pay construction/search and all phases. No known simulation from these nonaffine regions into the historical fixed calculus is provided. No fixed-machine FLMV timing or space implication.

## Publication and gap status

Exact code and raw data were created on main and independently fetched with byte-equality readback (code blob 4a7614a2a4b58498ec3ea444a7a2c61dedd9a616; raw blob 8c98f2d2e860cc28caee2b167b7c1af1bcb84fc8). Complete report, handoff and trackers are separately readback-audited. Material affected tracker [P2-F13] only. Remain OPEN: [P2-D1], [P2-C3], [P2-B1], [P2-B2]. No historical calculus edits. P versus NP OPEN.

## Verified publication/readback addendum (2026-11-07 14:12 PST)

The complete shared P=NP tracker proof1.txt was reviewed and unchanged (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b). Immediately before the [P2-F13] material evidence insertion, the complete P!=NP tracker proof2.txt had SHA dd66f186cd3d617be90a6b1c16281965041a5f64 and 244,059 characters. Its exact-byte prewrite copy is saved and readback-verified at research/agents/lspv-1/outbox/2026-11-07_1410_LSPV1_487_PROOF2_PREWRITE_EXACT.txt (matching old blob SHA). Conflict-safe main update commit 02ea03bf8d5d481bd5ac022e3ebd423e18b7de4e produced blob 1f8592681a2b5756edf4a73a33182f16b4af91cc (246,320 characters); complete readback and preservation of the preceding tracker text passed. Coordination issue #3 comment 6713725744 was posted and its complete contents fetched and verified identical.

Root main.tex was refetched through the available GitHub connector with blob SHA 68188a24badda635a5983fda1c381cdb694fd497 but *zero content bytes*. Therefore no safe authorized-region reconciliation was possible; root main.tex was **not modified**. This is a readback/content availability blocker, not evidence the root file is empty. The report/code/raw/handoff/trackers/issue were separately published successfully. Python/Node/V8 tests do not constitute a check of historical R_mix341 accepted-byte grammar. All five role identities, titles, offsets, enabled states and two Route A/three Route B allocation remain unchanged. P versus NP OPEN.
