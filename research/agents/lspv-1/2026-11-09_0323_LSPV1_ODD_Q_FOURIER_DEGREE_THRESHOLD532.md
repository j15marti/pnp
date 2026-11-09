# LSPV-1/532 | Exact odd-modulus charge-fiber GF(2) degree threshold

**Research run initiated 2026-11-09 03:23 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE and falsifiers

**Idea.** Extend the exact affine-hull blindness theorem [P2-L1-530] and its pure-affine auxiliary control [P2-L5-457] to fixed-degree nonlinear polynomials on the ORIGINAL q-state one-hot boundary indicators. Determine the exact minimum degree of a parity polynomial which vanishes on every valid signed-charge assignment but excludes at least one wrong charge.

Predeclared falsifiers: (F1) q=3,b=5 admits a quadratic separating polynomial; (F2) two Fourier characters in the same charge-hyperplane restriction class have support weight below ceil(b/2); (F3) an even-q analogue also requires ceil(b/2); (F4) q=3,b=4 cannot be separated by quadratic polynomials. The finite checks reject F1/F2; F3 and F4 correctly delimit the theorem.

**Search.** Read both complete root proof trackers, latest issue #3, AGENTS.md, CODEX.md, repository PNP skill, governing Nov 2 five-role handoff and Nov 9 knot/link handoff. Audited previous [P2-L1-530], [P2-L3-530], [P2-L5-457], LSPV-1/531, current Grok progress and REWIRE, and Claude TPORT. Reviewed current READMEs and fixed scope of konard/p-vs-np (0e0ec77f83ad6eec1719a96066108b96ac1c2a95), blkph0x/p-vs-np-proof-research (f397a7747eaca82df3d754d0a4b4bab1fe10f814), meelgroup/frat-xor (38a137bca4d4ab6443703d4c31fba5783021c581), tanyongkiam/cake_lpr (e94f45e9aa000cd9ada12f4c771ac9daf28fe53c), peitl/short-proof (93d2090dba9739bc4983c65ea639a24e1f5e0fab), and openai/math (cc5b0a03bca6c742f045d683b6647a6f44ef2cae). Primary literature checked: Pang (2026) arXiv:2610.00837v2, Koenig-Tsvietkova (2021) Trans. AMS B DOI 10.1090/btran/71, and Cheng et al. (2025) arXiv:2509.13120. Public web search for an identical degree-half result did not find an exact predecessor; **absence of a result is not a novelty claim**. No Google-specific engine was independently verified.

**Iterate.** The correct threshold is exactly ceil(b/2), not degree 1 or always degree 2. A quadratic six-monomial separator exists at q=3,b=4; for b>=5 direct original-indicator quadratic parity constraints cannot exclude wrong-charge tuples. Auxiliary gates and nonlinear topological algorithms are not covered.

## Theorem 532.1 (PROVED/RESTRICTED)

Let q>=3 be odd, b>=2, epsilon_i in {+1,-1}, c in Z_q, U=[q]^b, and

$$
S_c=\{x\in U:\sum_{i=1}^b\epsilon_i x_i=c\pmod q\}.
$$

Represent functions f:U->GF(2) by polynomials in the ORIGINAL one-hot indicators x_{i,a}=[x_i=a]. Let deg_1hot(f) be the least Boolean polynomial degree of such a representation on U. Then

$$
\boxed{\min\{\deg_{\mathrm{1hot}}f:f|_{S_c}=0,\ f\not\equiv0\text{ on }U\}=\left\lceil\frac b2\right\rceil.}
$$

In particular, any number of degree d<ceil(b/2) parity polynomial equations which hold for ALL valid S_c tuples also hold on ALL q^b one-hot tuples. This is not a statement about mixed Boolean gates, existential nonlinear auxiliaries, general field proofs, link isotopy, or historical R_mix341.

### Lower-bound proof

Because q is odd, choose finite extension K of GF(2) containing a primitive qth root omega. Fourier characters on Z_q^b are chi_alpha(x)=omega^(alpha dot x). A monomial of degree at most d in original one-hot indicators depends on at most d q-ary groups, so its Fourier transform has support only at alpha with Hamming weight <=d; sums preserve that support restriction.

On S_c, characters alpha and alpha+t epsilon differ by scalar omega^(tc). Thus the restricted character classes correspond to orbits alpha+<epsilon> and are linearly independent across distinct orbits. For t!=0, alpha and alpha+t epsilon cannot BOTH be zero at any coordinate; therefore

$$
\mathrm{wt}(\alpha)+\mathrm{wt}(\alpha+t\epsilon)\ge b.
$$

If 2d<b, at most one Fourier coefficient in each orbit can be nonzero. If f vanishes identically on S_c, the restricted coefficient sum for every orbit must be zero, so each coefficient individually vanishes. Fourier inversion gives f identically zero on U. Thus d>=ceil(b/2).

### Matching upper construction

Partition boundary groups A disjoint B with |A|=floor(b/2), |B|=ceil(b/2), and write L=sum_A epsilon_i x_i, R=sum_B epsilon_i x_i (mod q). Set

$$
f(x)=[L(x)=0]\oplus[R(x)=c].
$$

On S_c, L=0 iff R=c, so f=0. At L=0,R!=c, f=1. Each block-sum indicator expands as XOR of q^(|block|-1) one-hot monomials of degree |block|. Therefore deg_1hot(f)<=ceil(b/2), completing exactness.

For b=4, q=3, this is a SIX-term quadratic witness; for b=5 it is a 12-term cubic witness. Even-q countercontrol: parity of the total charge is already a degree-one test, so the odd-q assumption is necessary.

## Independent verification and resources

Python (bit-packed GF(2) evaluation rank) checked 11 q,b,sign,charge configurations and 37 degree stages, including q=3 b=2..7, q=5 b=3..4, q=7 b=3; exact ranks. For q=3,b=5, degree 2 ranks: 51 on all U versus 51 on S_c (blind). Degree 3: 131 versus 81 (separation possible). For q=3,b=4, degree 2: 33 versus 27. Python 7.14 seconds wall, 97,676 KiB peak RSS. Independent JS checked 55,984 assertions over Fourier-orbit weight separation and complete explicit XOR witness, including q=3 b=2..7, q=5 b=3..5, q=7 b=3, plus q=2 parity hostile control. JS 0.13 seconds wall, 35,452 KiB peak RSS. Programs and raw details under experiments/arc and results/raw/arc; no authoritative historical R_mix341 execution. Machine timings are finite experiment costs, not SAT bounds.

## Topology and selected hard family

For fixed pairwise mod-2 linking data computed DIRECTLY from independently selected components, a parity expression in original component-selection indicators has Boolean degree <=2. Under the additional assumption that those original indicators ARE exactly the q-state boundary variables and each parity test must vanish on every valid S_c, no such direct parity equation can distinguish wrong mod-3 charge at b>=5. **This does not apply to nonlinear processing of a vector of pairwise linking values, auxiliary components/gadgets, nonlocal isotopy, higher linking invariants, or arbitrary algorithms.** Cheng et al. (2025) show trivial-sublink NP-hardness can be encoded with mod-2 pairwise linking, so one must not infer global topological ease from this restricted obstruction.

Established hard-family control remains odd-modulus Tseitin on suitable cubic expanders, with rigorously scoped fixed-r Res(PC_r/F_2) lower bounds in Pang 2026. This boundary theorem is neither a full original-source refutation nor a lower-bound-preserving transfer from that restricted proof system to the historical mixed calculus. Linear-size ternary auxiliary adders from [P2-L3-530] are mandatory hostile controls.

**Proof-chain effect:** new restricted evidence [P2-L1-532], refining [P2-L1-530] and [P2-L5-457] and informing [P2-C3]. The principal [P2-D1] (native grammar), [P2-C3] (complete mixed transfer), [P2-B1] (all-rule superpolynomial minimum), [P2-B2] (noncircular B3) remain OPEN. B1/B2/B3 hierarchy unchanged; SAT in P alone does not supply R_mix341 correctness/reflection certificates or short proofs. No claim of P=NP or P!=NP.

**Publication/safety:** role-owned report, verifier, raw data, five-role handoff; no edit to main.tex, tasks, other role manuscripts, historical weights, native rule grammar, task identities, schedules, enabled states or two Route A/three Route B allocation.

### Exact consulted repository paths

- j15marti/pnp: proof1.txt, proof2.txt, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md
- research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md
- research/coordination/2026-11-09_KNOT_LINK_TOPOLOGY_SAT_FIVE_ROLE_HANDOFF.md
- research/agents/lspv-1/2026-11-09_0255_LSPV1_CROWN_ONEHOT_PERMUTATION531.md
- research/agents/lspv-3/2026-11-09_0224_LSPV3_OPTIMAL_TERNARY_SIGNED_BOUNDARY530.md
- research/agents/lspv-5/2026-11-09_0253_LSPV5_AFFINE_AUX_PROJECTION_BARRIER457.md
- GROKPROOF/2026-11-08_1130_PROGRESS.md
- research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex
- research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex

P versus NP remains OPEN.
