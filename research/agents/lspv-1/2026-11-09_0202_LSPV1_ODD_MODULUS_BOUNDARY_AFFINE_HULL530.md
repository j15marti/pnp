# LSPV-1/530: Exact odd-modulus one-hot boundary affine hull and GF(2)-only shortcut obstruction

**2026-11-09 02:02 PST | Route B | PROVED/RESTRICTED symbolic theorem; COMPUTATIONAL independent controls. P versus NP OPEN.**

**Proof-chain references:** New restricted evidence [P2-L1-530] (subject to tracker write verification), extending the **already proved three-input** theorem [P2-L3-520], applying the exact connected-cluster boundary equation [P2-L1-529]. Relevant OPEN: [P2-D1], [P2-C3], [P2-B1], [P2-B2]. P=NP-chain [P1-01], [P1-03], [P1-04] remain OPEN. This is **not** a new mixed-calculus hardness theorem.

## IDEA, precise falsifiers, SEARCH, ITERATE

**Hypothesis:** For a connected original-source modulo-three Tseitin cluster with **b>=3** external one-hot edge groups, every GF(2) affine equation on the **original boundary indicators** implied by its projected modular conservation relation follows from the individual one-hot group parity equations. In fact the *entire GF(2) affine hull* agrees with that of unrestricted one-hot boundaries, so even arbitrarily many such XOR rows cannot exclude any wrong-charge one-hot boundary assignment. The previous [P2-L3-520] proved the b=3 local case; the new target is every b>=3, especially the growing expander boundary of [P2-L1-529].

Precommitted falsifiers:
1. Find a q=3, b=4 binary affine row satisfied by every conservation-respecting boundary assignment that rejects even one one-hot wrong-charge assignment.
2. Find odd q>=3 and b>=3 for which the one-hot GF(2) affine dimension is smaller than b(q-1).
3. Find that the same dimension formula persists at even q or b=2, contradicting the predicted sharp exceptions.
4. Unjustifiably infer mixed R_mix341 hardness: legal paid Boolean DEF, nonaffine RES/AND3, LOCAL-CONVERT, nonoriginal GF(2) wires, and branching are **not** excluded.

**Current project state actually reviewed:** Complete proof1.txt blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; complete proof2.txt initial blob `b3637881aa461b3a0607cc5b02df1b0d12db988d`; issue #3 and latest LSPV-3/529 handoff; historical 2026-11-02 12:04 five-role refocus blob `033b54b87b7cbe94912af5cf67daa52859143a07`, AGENTS.md, CODEX.md and research skill; historical /341 prose `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. Read LSPV-1/529 `d683e37fae244cac2d56ccd5d633b00d5a302976`; LSPV-3/520 `a15fde0a43606450d07fe22b50e1a0645954ef72`; LSPV-5/455 `69a4d0ec535413f2c0439b952885095539bf8093`; actual GROKPROOF/2026-11-08_0930_PROGRESS.md blob `e3e8c9657e0f2b2e0751752135cf2558e28183cf` and actual Claude world-ledger README `de75a371ce3143a4495e6892df7fb04794a6b708`. No source supplied an authenticated original R_mix341 accepted-byte parser.

**Required external checks, exact current heads:** `konard/p-vs-np` commit `ecedd2b45f1c524d85c00b2da27a9c140025550c`, `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`, finite-machine Lean scope only. `blkph0x/p-vs-np-proof-research` commit `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`, `tseitin_expander_lab/README.md` blob `58ba565beb0a7288ede91702f313dc7102acd60e`, finite solver controls not mixed bounds. `meelgroup/frat-xor` commit `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, `format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`, external XLRUP grammar not historical Rmix. `peitl/short-proof/README.md` blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab`, shortest **Resolution** only. `openai/math` commit `4eaee87548250b2682affda7d05d947c05554bae`, README blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`, research artifacts not an Rmix checker. `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` blob `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab`: standard **modulo-two** edge-parity generator, not a modulo-three proof. Web primary review: Pang, arXiv 2610.00837v2 §7, especially Thm. 7.2(b), Cor. 7.3; Cook–Reckhow 1979; published GF(2)/GF(3) difference is system-dependent. Search terms: `modulo-three affine hull`, `one-hot GF2 linear consequences`, `Pang opposite characteristic Tseitin`, `Cook Reckhow polynomial bounded`. General web search available; no separate Google-branded tool was used.

**Duplicate audit:** [P2-L3-520] already proved the exact b=3 local `q`-ary affine dimension `3(q-1)-1_{2|q}`. Do not claim that case as new. [P2-L1-529] already proved compact boundary congruence and the exponential **full-negative-clause** normal-form size. Here the separate extension to **all b>=3** proves the entire class of original-indicator GF(2)-affine port descriptions is incapable of preserving charge, regardless of the number of XOR rows. Not a claim of priority in academic mathematics.

## Fixed family, encoding, proof model and theorem scope

For q>=2, b>=2, and c in Z_q, fix signs epsilon_i in {+1,-1}; a sign is a permutation of each one-hot coordinate. Let
$$
V_{q,b,c}=\{z(x)\in\{0,1\}^{qb}:x_i\in\mathbb Z_q,\ \sum_{i=1}^b\epsilon_i x_i=c\pmod q\},
$$
where `z(x)_{i,a}=1` iff `x_i=a`. There are `q^(b-1)` valid one-hot assignments. Distinguish the affine hull **over F_2** from a GF(q) equation.

**Theorem 530.1 (exact F2 affine hull, all b):** For b>=3,
$$
\operatorname{affdim}_{\mathbb F_2}V_{q,b,c}
=b(q-1)-\mathbf 1_{2\mid q}.
$$
For b=2 the affine dimension is exactly q-1. The result is independent of c and signs.

**Proof:** Any GF(2) affine equation on the qb indicator coordinates restricts on one-hot tuples to
$$
\sum_{i=1}^b f_i(x_i)=d,\qquad f_i:\mathbb Z_q\to\mathbb F_2.
$$
For distinct i,j, replace `x_i` by `x_i+t` and `x_j` by `x_j-t`. Because b>=3, their initial values are *independent* with a third coordinate balancing the sum. Therefore
$$
f_i(a+t)+f_i(a)=f_j(s)+f_j(s-t)
$$
for every a,s,t. Both sides must depend only on t, giving a common homomorphism `chi: Z_q -> F_2` (composition of increments proves additivity). Hence `f_i(a)=k_i+chi(a)` for every i. If q is odd the only such homomorphism is zero: all f_i are constant, so every affine consequence is a linear combination of the b one-hot group-parity identities `sum_a z_{i,a}=1`. If q is even there is one extra independent character `chi(a)=a mod 2`, producing the single cross-group affine equation `sum_i chi(x_i)=chi(c)` after absorbing signs. This proves the dimensions by subtracting the independent affine equation ranks from qb. For b=2 there are only q solution vectors. Their q-1 differences are independent, since their first-group one-hot supports differ from the anchor, giving q-1. QED.

**Corollary 530.2 (no original-indicator GF2-only boundary compiler, odd q):** For every odd q and b>=3,
$$
\operatorname{aff}_{\mathbb F_2} V_{q,b,c}
=\operatorname{aff}_{\mathbb F_2}\{z(x):x\in\mathbb Z_q^b\}.
$$
Consequently EVERY wrong-charge one-hot tuple satisfies EVERY original-indicator GF(2) affine row valid on the true modular boundary. A conjunction of arbitrarily many such rows cannot define the charge condition even **on the one-hot domain**. For q=3,b=4, all 54 invalid tuples pass every permitted affine consequence.

**Application to known family:** [P2-L1-529] proves that the projection of any connected modulo-three Tseitin cluster onto b boundary edge groups is exactly a signed sum conservation equation. Thus for b>=3 its projection has the above full binary affine hull. The proper strict-3CNF original source on cubic expanders has `39h/2` signed clauses, `9h/2` Boolean indicators and encoded size `Theta(h log h)`; Pang Thm. 7.2(b) supplies `exp(Omega(h))` lower bounds for **fixed-r syntactic Res(PC_r/F_2)** after the source-subset transfer of [P2-L3-520], not for Rmix. Ordinary binary RES and paid conservative DEF may still represent the boundary succinctly; this theorem bars only original-boundary *affine-row-only* reasoning. For b<=2 the exception matters. This is an exact lower bound on a restricted representation's distinguishing power, not a general inference-node lower bound.

## ITERATE: reproducible independent finite checks

Python exact GF(2) elimination enumerated **32 charge/orientation/q/b cases**: q=3,b=2..7, charges 0/1/2 with alternating edge signs; controls q=2,4,5,6. Across these cases: **3,848 satisfying boundary tuples** and **8,632 rejected tuples** were inspected. Every expected rank matched. The q=3,b=2 countercontrol had dimension 2 instead of the naive b(q-1)=4, and the even-q controls detected their extra parity row. For q=3,b=4,c=1 the Python program verified 54/54 wrong tuples lie in the good relation's GF(2) affine hull. A fully independent Node implementation reconstructed every rank and wrong-tuple hull test, passing **131 assertions**; it also enumerated all 4,096 binary coefficient masks on q=3,b=4 and found precisely **16** valid affine coefficient vectors, the 2^4 combinations of individual group parity rows. This rejects falsifier 1 by exhaustive finite control. A different q/c or arbitrary length is supported by the symbolic proof, not extrapolated from enumeration.

Local producer: `/mnt/data/pnp530/affine_boundary_verifier.py` (SHA-256 `4fc13af4141d0aabef61892b6da285f3cae73bcfe1ca38fd67ae306cac6a9108`), local raw `affine_boundary_raw.json` 8,854 bytes (SHA-256 `ea62b3c5facae9a40960144f22e9de427ff6a7b0d2c164f2036d49a4f99e3a31`), independent Node `verify_affine_boundary.js` SHA-256 `b20c10e976388027fecd95a93f888238de1d77f6bd380f463b8fef2e10c6b43f`. Python generation measured user CPU 1.11 s, sys 0.14 s, peak process RSS 95,884 KiB. These machine measures are for the independent offline checks only, and are not W_R.

**Resource and proof limitations:** This run outputs no new Rmix proof packet, so no historical native accept/reject claim is made. SAT/UNSAT are explicit fiber equality labels; malformed proof rejection is inapplicable to linear algebra enumeration. The independently written Node checks raw schema/ranks and the source rank matrices; the original strict 3-CNF SAT/UNSAT and malformed-source controls remain in [P2-L3-520] and [P2-L1-527]. An implemented generator or verifier must charge source/index/head reads, parsing, allocations, bit arithmetic, all output bits, verification, failed policies and simultaneous peak storage. The offline affine rank does **not** bound arbitrary solver work. No FLMV numerical claim. B1/B2/B3 remain OPEN.

**Next falsifier:** Can a historically *legal* bounded-support AND3/LOCAL-CONVERT plus paid binary DEF gadget export a fresh nonlinear boundary predicate, then manipulate compact GF(2) rows without an exponential full-forbidder expansion? Authenticate each wire/condition byte and parent reference. If yes, this GF(2) original-indicator obstruction does not prevent a short mixed proof. Separately, derive noncircular B3 for the unchanged R: SAT in P must imply polynomial \bar W_R, without assuming short reflection proofs.

### References

[1] Shuo Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (2026-10-24), Theorem 7.2(b), Corollary 7.3. https://arxiv.org/html/2610.00837v2

[2] S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979). https://www.cs.utoronto.ca/~sacook/homepage/cook_reckhow.pdf

[3] j15marti/pnp, LSPV-3/520 and LSPV-1/529, exact source-preserving three-CNF and cluster-boundary results (paths above).
