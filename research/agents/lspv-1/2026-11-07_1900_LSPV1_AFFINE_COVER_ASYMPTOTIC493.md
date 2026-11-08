# LSPV-1/493 | Exact exponential rate of optimal global affine-prediction covers for independent AND gates

**2026-11-07 19:00 PST | Route B | PROVED/RESTRICTED (symbolic) and COMPUTATIONAL (finite) | P versus NP OPEN.**

**Affected proof-chain node:** [P2-F13]. **Still OPEN:** [P2-D1], [P2-C3], [P2-B1], [P2-B2]. Cross checks [P2-F9], [P2-B3], [P1-01]. No historical native rule, weight, agent task, allocation, title or schedule is changed.

## IDEA: initial falsifiable hypothesis

A local four-function affine palette may beat the prior three-template-per-two-AND tensor construction from LSPV-1/487. The initial concrete conjecture was a four-template cover of three independent AND gates, improving the current upper base from sqrt(3). Four falsifiers: (F1) an input assignment missing from all four diagonal predictions; (F2) some local Boolean assignment disagrees with more than one of the four affine predictors; (F3) any proposed probability/greedy upper bound fails on a residual uncovered input set because template incidences are not uniform; (F4) a claimed source-preserving syntactic proof requires uncharged membership, case-split, weakening, definition, or assumption-discharge rules. F1-F3 are resolved symbolically and checked finitely. F4 remains OPEN, so no historical R_mix341 proof translation is claimed.

## SEARCH / continuity / duplication

Read both full current trackers, issue #3 and newest relevant role comments, Nov. 2 five-role refocus, root AGENTS.md, CODEX.md, pnp research skill, LSPV-1/487/491/492, LSPV-3/487, LSPV-5/423, actual GROKPROOF/2026-11-08_0118_PROGRESS.md and research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex. Full root main.tex cannot be retrieved through the connector: it returns SHA 68188a24badda635a5983fda1c381cdb694fd497 with **zero content bytes**. Therefore it is untouched; no outside-region preservation can be certified.

Required changed-aware source checks: konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (finite-model formalization, P vs NP unresolved); blkph0x/p-vs-np-proof-research README.md blob f397a7747eaca82df3d754d0a4b4bab1fe10f814 and METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5 (restricted optimization/relaxations, not unrestricted SAT lower bounds); meelgroup/frat-xor README.md blob 38a137bca4d4ab6443703d4c31fba5783021c581; tanyongkiam/cake_lpr README.md blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c (external certificate formats, not the historical grammar); openai/math README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae. No third-party repository is taken as an R_mix341 axiom. Web searches inspected Pang arXiv:2610.00837 (original proof-model lower-bound context), Chvatal (1979), *A Greedy Heuristic for the Set-Covering Problem* DOI 10.1287/moor.4.3.233 (classical set-cover control), and bounded-arithmetic/reflection literature. Standard union-bound/greedy-set-cover facts are credited, not presented as new mathematics; the restricted application and exact rate may duplicate unlocated prior art. No direct Google-branded interface, original Lean kernel or native R_mix341 checker was run.

**Duplication audit:** /487 already proves the per-affine-predictor ceiling 3^g and a 3^floor(g/2) 2^(g mod 2) semantic covering; /490 proves an additional cross-gate penalty; /491 generalizes the lower bound using polar rank. /488 paid guard certificate concerns **two** gates, not this new all-g construction. New here is the matching **asymptotic exponential base 4/3** across all globally affine vector predictions using ordinary set-cover averaging, plus an exact four-template g=3 separable construction.

## THEOREM 493.1: exact exponential base in abstract semantic-cover model

For every integer g >= 1, let original Boolean inputs be x=(u_1,v_1,...,u_g,v_g), and define Q(x)=(u_1 v_1,...,u_g v_g) in F_2^g. A candidate A(x)=Mx+b is a *globally affine* vector function, with arbitrary permitted cross-gate linear coefficients. Its agreement set is E_A={x:Q(x)=A(x)}. Set

$$
K_g=\min\left\{K:\exists A^{(1)},\ldots,A^{(K)}\text{ globally affine};\ \bigcup_{j=1}^K E_{A^{(j)}}=\mathbb F_2^{2g}\right\}.
$$

Then

$$
\boxed{
\left\lceil(4/3)^g\right\rceil\le K_g
\le\left\lceil(4/3)^g(g\ln4+1)\right\rceil,
\qquad
\lim_{g\to\infty}K_g^{1/g}=\frac43 .
}
$$

The lower bound uses **all globally affine predictors**, including cross-gate terms. The upper bound is witnessed by predictors whose i-th output uses only (u_i,v_i); no cross-gate terms are needed.

**Lower bound proof.** Expand the agreement indicator using all output masks s in F_2^g. The scalar quadratic s·Q has polar rank 2|s| on 2g variables. Adding s·A changes only the affine part and never increases the absolute quadratic Walsh coefficient beyond 2^(2g-|s|). Therefore, for every globally affine A,

$$
|E_A|
=2^{-g}\sum_s\sum_x(-1)^{s\cdot(Q(x)+A(x))}
\le 2^{-g}\sum_s 2^{2g-|s|}
=3^g.
$$

Since |F_2^{2g}|=4^g, K_g 3^g >=4^g.

**Upper bound proof.** At each gate use the four affine scalar predictions

$$
\phi_0=0,\qquad\phi_1=u,\qquad\phi_2=v,\qquad
\phi_3=1+u+v \pmod2.
$$

For each input pair (u,v), **exactly one** of these four differs from uv. Independently choose one of four scalar predictions at every coordinate. For every fixed original input x, a uniformly sampled vector predictor agrees with Q(x) with probability p_g=(3/4)^g. Choosing K predictors independently leaves any fixed x uncovered with probability (1-p_g)^K. A union bound over all 4^g input assignments gives

$$
\Pr[\text{some x uncovered}]
\le 4^g(1-p_g)^K
\le \exp(g\ln4-Kp_g)<1
$$

for integer K=ceil((g ln4+1)/p_g). Thus such a cover exists. Alternatively, a deterministic greedy choice covers at least p_g of the remaining uncovered assignments at each step by the averaging identity; the same count bound follows. The limit is immediate by taking g-th roots.

**Additional exact g=3 certificate.** Four diagonal vectors A_t=(phi_t(u_1,v_1),phi_t(u_2,v_2),phi_t(u_3,v_3)), t=0,1,2,3, cover every input because at most three distinct t-values are forbidden by three gates. The template IDs in little-endian base 4 are [0,21,42,63]. No set of three *coordinate-separable* affine predictions can cover: given three candidate predictions, choose a different gate for each, and set that gate's inputs to one of the assignments on which its assigned candidate differs from AND. (AND is not affine.) This proves exact K_3^separable=4. It does **not** assert K_3=4 when cross-gate affine terms are permitted; that finite optimum is not established.

## ITERATE / finite independent controls

The fresh Python exhaustive-greedy producer constructed full assignments and all 4^g local affine template masks for g=1,...,6; every mask had exactly 3^g matches, and each greedy step met the precise average residual-coverage lower bound. Certificate choices and raw data are in results/raw/arc/2026-11-07_1900_LSPV1_493_AFFINE_COVER_RAW.json. The independently written Node verification rechecked each selected template, every input assignment and the bound, reporting **5664 passing assertions**. K chosen by greedy was respectively 2,3,4,8,13,19 for g=1,..,6. These values are upper controls, **not** all-size optima. Original-source odd-charge K4 parity yielded 0 models and even-charge K4 yielded 8, but neither is a proof-system hardness certificate. Python greedy g=6 used ~16 seconds on this instance; selection is expensive.

The algorithm explicitly enumerates 4^g inputs and 4^g templates. Its mask store has O(16^g) bits, with additional interpreter overhead, and construction/search uses exponential operations. Only the *existential optimal semantic cover* chooses after the fact without cost. An implemented solver or proof builder must pay source reads, construction, search, guards, AND3/DEF facets, accepted records, checking, recomputation, lookup, scheduling, output, and peak simultaneous space. No assertion of polynomial-time cover discovery or polynomial native inference follows from the O(g(4/3)^g) template count.

## Existing hard-family ledger and transfer firewall

Established witness family: Pang, *A Degree--Size Relation for Resolution over Polynomials* (arXiv:2610.00837v2, Theorem 7.2(a)), random proper signed width-3 CNFs F(n,3,8n) with n original variables, 8n sampled clauses and O(n log n) standard binary indexed bits; published w.h.p. exp(Omega(n)) shared-DAG refutation-size lower bound in fixed Res(PC_r/F_p), in particular the distinct Res(XOR) p=2,r=1 system. The theorem is NOT about full historical R_mix341. Its selected source is already proper 3-CNF, so no extra hardness-preserving 3-CNF encoding is silently claimed. Existing methods include XOR, Resolution, paid extension, shared DAGs and proof preprocessing; use all as legal upper-bound controls wherever the native calculus admits them.

This cover theorem concerns an independent-AND semantic prediction subproblem, **not** source-authenticated refutation DAGs for Pang's formulas. Regions E_A are typically **nonaffine**. Inference of guarded predictions and discharge of all AND cases, sharing, parent-view eligibility and explicit evidence bits must be authenticated and charged. Thus substituting (4/3)^g for 2^g or sqrt(3)^g in the /485 syntactic backtranslation is **NOT presently legal**. A putative native proof translation with bounded per-template overhead is a separate falsifiable [P2-C3] hypothesis.

The source-to-calculus direction needed for [P2-B1] remains: a *polynomial-cost simulation from every legal historical R_mix341 proof on the SAME hard 3-CNF source into a proof system with a certified lower bound*. Reverse conversion or equisatisfiability does not suffice. [P2-B2] still needs a noncircular reflection/decision-to-certificate mechanism for the same preselected mixed calculus, not an assumption that SAT-in-P proves arbitrary decider correctness inside that calculus.

## Resource / barrier / governance audit

Logical semantic region count is K_g; this is neither actual distinct paid proof nodes, proof-bit size, weighted critical-path depth nor realizable machine time/space. There are no branch-specific lemmas, case-split rules or free OR joins asserted in historical R_mix341. The averaging proof operates on semantic assignments only; it is consistent with expensive RES or guarded syntactic discharge, and with a shared proof DAG bypassing the cover method. Natural-proofs, relativization and algebrization are not avoided or settled by this restricted combinatorial lemma. Arbitrary output sharing and cancellable quadratic gates remain separate controls under /491. Root main.tex could not safely be reconciled due to zero content returned and is unchanged.

**Actual advance:** sharp asymptotic exponential base 4/3 for a precisely specified abstract global affine-prediction cover; independent g=1..6 checks. **OPEN:** [P2-D1] exact grammar, [P2-C3] full source-authenticated mixed/guard translation, [P2-B1] superpolynomial all-rules minimum, [P2-B2] noncircular B3. P versus NP remains OPEN.

### Sources

1. Pang, S. (2026). *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, Theorems 1.1 and 7.2(a); https://arxiv.org/abs/2610.00837 .
2. Chvatal, V. (1979). *A Greedy Heuristic for the Set-Covering Problem*, *Mathematics of Operations Research* 4(3):233-235, DOI 10.1287/moor.4.3.233. Used as established general greedy-set-cover context, not for a novel complexity claim.
3. Project LSPV-1/487 and /491, paths and SHA in SEARCH section; all broader claims retain their verified, restricted scope.
