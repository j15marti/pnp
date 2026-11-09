# LSPV-1/535: Sharp parameterized exponent envelope for source-identifier decomposition

**2026-11-09 06:46 PST | Route B | PROVED/RESTRICTED symbolic envelope, CONDITIONAL guest SAT premise, COMPUTATIONAL numeric checks. P versus NP OPEN.**

**Node and dependencies:** [P2-L1-535] refines [P2-L1-534], independently audited in [P2-L5-460], with [P2-B3] quantifiers. Historic [P2-D1] grammar, [P2-C3] normalization, [P2-B1] all-rule superpolynomial minimum, [P2-B2] noncircular same-calculus B3 remain OPEN. No claim concerns the full historical R_mix341.

## IDEA -> SEARCH -> ITERATE: exact falsifiers, evidence and revision

**Initial hypothesis:** The all-input, canonical binary-identifier branching reduction in [P2-L1-534] admits a uniform two-parameter exponent transfer and a sharp minimax bound for its explicit *resource-estimate envelope*, rather than only a qualitative $2^{o(N/\log N)}$ implication.

**Falsifiers fixed before research:**
1. A length-$N$ source can use more than $2^L$ identifiers with binary length below $L$.
2. The residual formula after short-ID branching has more than $N/L$ literal occurrences, or clause-chain 3-CNF needs more than $2N/L$ variables.
3. Cumulative all-input worst-case at lengths $m\le N$ or all-phase parsing/conversion invalidates the stated exponent.
4. The claimed sharper OpenAI-specific transfer is genuinely new, rather than already appearing in [P2-L1-534].

**Search changed the claim.** Falsifier 4 fires: [P2-L1-534] already states the OpenAI $N(\log\log N)^2/(\log N)^{3/2}$ special-case upper bound. **That rate is reused, not claimed as new.** [P2-L5-460] independently proved the arbitrary-string identifier budget and the cumulative maximum envelope. This run adds the general $(\alpha,d)$ theorem and the sharp minimax classification of the explicitly defined upper-bound envelope, not a solver breakthrough. All other falsifiers fail in their stated explicit literal-list model.

Actual state read: both complete trackers at starting blobs proof1.txt `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, proof2.txt `78497e2bba11e629349a83a6ae18b756462a0069`; issue #3 and recent LSPV-3/533, LSPV-4/520 and LSPV-5/460; historical LSPV-2/341; AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md; user-approved 2026-11-02 five-role handoff and 2026-11-09 knot/link handoff. Inspected actual GROKPROOF/2026-11-09_1230_PROGRESS.md, research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex. These sources provide no new historic mixed B3 transfer.

Required external repositories were read at concrete files: konard/p-vs-np README.md blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` and scripts/proof_status.json blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` and tseitin_expander_lab/README.md blob `58ba565beb0a7288ede91702f313dc7102acd60e`; meelgroup/frat-xor format.md blob `986a21aa92b62f844ef1fce852193142c41b2b1f`. These are educational, finite benchmark or distinct mixed proof-format controls, not historical R_mix341 normalization. Existing short-proof and CNFgen reports were reused rather than rediscovered.

Primary theorem: Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, Theorem 7.2(a), fixes prime $p$, degree $r\ge1$ and proper width $w\ge3$ at clause density $\Delta\ge2^w$, and gives $\exp(\Omega(n))$ DAG-node minimum in distinct syntactic $\operatorname{Res}(\mathrm{PC}_r/\mathbb F_p)$ on random $\mathcal F(n,w,\Delta n)$ asymptotically almost surely. Select $p=3,r=1,w=3,\Delta=8$, with $N_n=\Theta(n\log n)$ source bits. No SAT-reduction preservation is needed since the family is already strict 3-CNF. OpenAI's 2026-10-25 `openai/math` lean/docs/378.md (blob `223bbe187394bffca8a2c7ba1656538bfba26e3b`) states a formally scoped $(L+1)^{O_k(1)}2^{O_k(n(\log\log n)^2/\sqrt{\log n})}$ counting algorithm. Proof-bearing module SqrtLogSpace/Final.lean blob `a69635a2492e06a26f2e33d4251edd1e21ba3332` was inspected; no independent Lean/Lake rebuild or machine execution here. The external algorithm remains a **CONDITIONAL** premise in this project. The matching paper's sharper runtime is not silently substituted for the Lean scope.

## Theorem 535.1 (symbolic rate transfer, PROVED/RESTRICTED conditional on guest)

Fix constants $\alpha\ge0,d\ge0$ and a single uniform total correct canonical at-most-3SAT decider $G$ with, on $n$ occurring variables and $B$ encoded input bits,

$$
T_G(B,n)\le (B+2)^c\,2^{C f_{\alpha,d}(n)},\qquad
f_{\alpha,d}(n)=\frac{n(\log\log(n+16))^d}{(\log(n+16))^\alpha},
$$

where constants $c,C$ belong to $G$ and all logarithms are base two. The bound is required on every guest string, not just typical formulas. Work with the original explicit signed clause-list grammar where every occurrence physically repeats its canonical nonempty binary variable identifier, including arbitrary-length IDs. Let

$$
H_{\alpha,d}(N)=\frac{N(\log\log N)^d}{(\log N)^{1+\alpha}},
\qquad L(N)=\max\{1,\lfloor\log_2 H_{\alpha,d}(N)\rfloor\}
$$

for sufficiently large $N$ (finitely many small inputs use the fixed exhaustive fallback). A single uniform source parser, short-ID enumerator and paid clause-chain reducer builds a total correct general-CNF SAT decider $A$ satisfying

$$
\boxed{T_A^{wc}(N)\le 2^{O(H_{\alpha,d}(N))}}
$$

with polynomial-in-$N$ simultaneous peak working space. Constants are uniform in the source and may depend on the fixed $G,\alpha,d$.

**Proof.** There are fewer than $2^L$ distinct canonical binary identifiers shorter than $L$. Enumerate truth assignments to all such occurring IDs, with at most $2^{2^L}$ branches. For a residual, every remaining literal's ID physically contributes at least $L$ input bits, hence $Q L\le N$ occurrences, and at most $Q$ variables. Dense-renaming and standard existential clause-chain conversion preserve SAT/UNSAT and use at most $2Q\le2N/L$ guest variables, with polynomial source scanning, clause serialization, indexing and malformed-input rejection. Since $2^L\le H(N)$, the branch-exponent is at most $H(N)$. Also $L=(1+o(1))\log_2 N$ and $f_{\alpha,d}$ is eventually increasing. Consequently

$$
f_{\alpha,d}(2N/L)=O\left(\frac{N(\log\log N)^d}{(\log N)^{1+\alpha}}\right)=O(H(N)).
$$

Each branch needs only polynomial-in-$N$ setup, guest execution and checking plus the stated exponential time. Summing branches multiplies these factors, so time is $\mathrm{poly}(N)2^{O(H(N))}=2^{O(H(N))}$. Reuse one guest workspace and a counter over short identifiers; the entire peak storage is polynomial in $N$. Since $H(N)$ is eventually increasing and unbounded, taking the maximum over all lengths $m\le N$ preserves the same bound. This yields the *cumulative* B2 quantifier, not just an exact-length bound. QED.

## Theorem 535.2 (sharp optimum of the **analytic estimate**, not of algorithm time)

Fix the explicit coarse rate-estimate envelope for a chosen identifier cutoff $1\le L\le N$:

$$
E_N(L)=\max\left\{2^L,\ f_{\alpha,d}(\lceil2N/L\rceil)\right\}.
$$

Then for fixed $\alpha,d\ge0$,

$$
\boxed{\min_{1\le L\le N} E_N(L)=\Theta(H_{\alpha,d}(N)).}
$$

**Proof.** Theorem 535.1's cutoff gives $E_N(L)=O(H(N))$. Conversely, for $L\le\log_2N$, monotonicity gives
$f_{\alpha,d}(\lceil2N/L\rceil)\ge f_{\alpha,d}(\lceil2N/\log_2N\rceil)=\Theta(H(N))$.
For $L>\log_2N$, $2^L>N$, whereas $H(N)=o(N)$, so $E_N(L)\ge N=\Omega(H(N))$. QED.

**Critical qualifier:** This is a min-max theorem about the *particular charged analytic upper-envelope expression*, not a lower bound on the execution time of the real guest or on all decompositions. Some inputs contain far fewer than $2^L$ occurring short IDs; shortcuts, sharing and nonuniform knowledge are not restricted away to protect a claim. This result neither proves superpolynomial time nor bounds the historical mixed-refutation minimum.

## Conditional B2 control and exact missing transfer

When $\alpha>0$, $H_{\alpha,d}(\Theta(n\log n))=o(n)$. Pang Theorem 7.2(a) gives for a sequence of UNSAT proper signed 3-CNF originals with $N_n=\Theta(n\log n)$

$$
W_{\mathrm{Res}(\mathrm{PC}_1/\mathbb F_3)}(F_n)\ge 2^{\Omega(n)},
$$

whereas conditional on $G$, $T_A^{wc}(N_n)\le2^{o(n)}$. Therefore **B2 fails under the assumed guest-machine theorem in this distinct restricted syntactic calculus**. This recovers the conditional consequence of [P2-L1-534] with an explicit parameter-general rate. It is not a counterexample for historical R_mix341; it does not establish B3, any arbitrary-algorithm SAT lower bound, or P != NP.

For the formally scoped OpenAI parameter pair $\alpha=1/2,d=2$, the transferred upper-rate is

$$
2^{O\left(N(\log\log N)^2/(\log N)^{3/2}\right)}.
$$

This exact special-case rate was **already identified in [P2-L1-534]**; only its parameter-general sharp-envelope theorem is advanced here. A formal Lean replay, original-machine cost mapping and external independence remain uncompleted.

## Independent executable checks and resource ledger

Separate standard-library Python numeric verifier: 4 $(\alpha,d)$ choices, 64 size-grid tests $N=2^{12},2^{14},\ldots,2^{42}$, 120 independent variable-ID bit-charge controls, **560 assertions passed**. Max observed sample ratio $E_N(L)/H(N)$ is $6.538781$; it is a finite regression, NOT an asymptotic proof or a measured SAT runtime. Python code: experiments/arc/lspv1_535_cutoff_exponent.py; raw: results/raw/arc/2026-11-09_0646_LSPV1_535_CUTOFF_ENVELOPE_RAW.json. No original hard-family UNSAT certificate was generated here; rely on Pang's specified proof lower-bound family, not benchmark hardness.

Logical paid proof nodes: **not measured** (no R proof constructed). Source bits $N$; per-branch guest bits $\mathrm{poly}(N)$; at most $2^L$ short-ID branch depth bits, $2^{2^L}$ branches, $Q\le N/L$ occurrences, $\le2Q$ converted variables. Sequential physical time counts every parsing/simplification/reindexing/serialization/guest/verification phase and every branch. Simultaneous peak storage is bounded by host source/index/counter plus one guest's polynomial workspace; all stages include any allocate-then-free maxima. No FLMV same-machine exponent contraction is inferred, and no guest failed search is free. This upper construction explicitly produces a decision answer, not an UNSAT refutation.

Publication: this report, code, raw, and research/coordination/2026-11-09_0646_LSPV1_CUTOFF_ENVELOPE535_FIVE_ROLE_HANDOFF.md. Root main.tex is untouched unless its complete content can be safely authenticated; do not overwrite an empty/partial fetch.

**Status:** PROVED/RESTRICTED generalized conditional transfer and sharp *analytic-envelope* theorem; COMPUTATIONAL finite evidence. All four historical Route B targets [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN. P versus NP OPEN.
