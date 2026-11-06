# LSPV-3/457: random strict-3 SAT all-rule source-core work/span bound and ambient-variable correction

**2026-11-06 12:22 PST | Route B primary | PROVED/EXACT under stated source-explicit bounded-premise semantic calculus; COMPUTATIONAL independent finite replay; KNOWN restricted lower-bound families.** Historical accepted-byte R_mix341 grammar, any superlinear all-rule lower bound, B1/B2/B3 and P versus NP remain OPEN. No existing role, task, schedule, historical rule, weight or source file was altered.

## 1. IDEA -> falsifiers -> SEARCH -> ITERATE

**Initial hypothesis:** The established random proper strict-three source of Chvátal–Szemerédi and Pang admits a joint *full-mixed* lower bound for paid work and ideal critical-path span, using the minimum UNSAT **original-source subset** instead of Resolution width or PC degree. Moreover the existing Tarsi/local-sparsity coefficient 1/64 can be strengthened slightly without excluding any allowed XOR, DEF, shared-DAG or branching shortcut.

Four falsifiers fixed before testing: (F1) the stronger 1/60 union estimate has base >=1; (F2) DAG sharing allows a depth-d binary-premise refutation node to reach more than 2^d distinct original source leaves; (F3) the K4 original signed strict-3 semantic AND3/XOR control fails to attain both graph bounds; (F4) the previous report's claim of **exactly n occurring variables** in a sample with n ambient variables holds asymptotically. F1-F3 were rejected; **F4 fired**. The latter is a precision correction, not a refutation of Pang's ambient-n theorem.

**Prior-work audit:** /341 already proved the source-capacity work bound on essential cubic Tseitin sources; /442 established deletion resilience of the chosen random 3-CNF; /443 already established the minimum-UNSAT-core work bound with coefficient 1/64; /447 and LSPV-1/447 already established balanced-node/critical-path tightness on cubic Tseitin; /456 already composed Pang with a *scoped* GF(2)/DEF-exposure compiler. None of these is advertised as newly discovered here. This run strengthens the /443 *same-family all-rule* constant to 1/60, derives a previously unstated all-rule **span** corollary, checks both against an independent existing-family certificate, and corrects the distinct ambient-versus-occurring variable quantifier.

## 2. Family/theorem/encoding/known-method/transfer ledger

**Direct hard 3-CNF (primary):** For integer n>=3 select m=8n independent source indices with replacement, each uniform over all $8\binom n3$ proper, three-distinct-variable signed clauses on the fixed ambient labels [n]. Clause indices are retained even for duplicate signed clauses. Explicit decimal DIMACS source length is $N=O(n\log(n+2))$ bits. The source is UNSAT with high probability.

- **KNOWN THEOREM:** Chvátal–Szemerédi (1988), *Many hard examples for resolution*, JACM 35(4):759-768, DOI 10.1145/48014.48016. At density 8 and width 3, with probability 1-o(1) every ordinary shared-DAG Resolution refutation has $\exp(\Omega(n))$ size. This is *ordinary Resolution*, not R_mix341.
- **UNREFEREED 2026 PREPRINT:** Pang, arXiv:2610.00837v2, Theorems 1.1 and 7.2(a) and Section 7.1, reports $\exp(\Omega_{p,r}(n))$ DAG Res(PC_r/F_p) size for this distribution at fixed p,r, including Res(XOR) at p=2,r=1. The formal rule and semantic-to-syntactic comparison must be charged; *no arbitrary paid fresh DEF* is part of that lower-bound system.
- **KNOWN combinatorics:** Tarsi's deficiency lemma, each inclusion-minimal UNSAT formula with r occurring variables has at least r+1 clauses. See KTH Proof Complexity Lecture 4, Theorem 2.6.
- **KNOWN methods:** source-preserving native RES, elimination, native AND3/local parity, GF(2), paid DEF networks, extensions, learned lemmas, reconvergence and optimal branching all remain legal in the ideal R_mix341 minimum. The lower bound below survives all *sound, source-explicit, at-most-binary-premise, conservative* shortcuts because it counts the necessary source ancestry; none of these shortcuts may be excluded to protect a stronger claim.
- **Other mandatory controls:** Haken unary PHP exponential only in ordinary shared Resolution, with Cook ER polynomial shortcuts; Braun 2026 original width-$2\ell$ bit-PHP for $\ell\ge32$ has $>\exp(n/(32768\ell^2))$ unrestricted DAG Res(XOR) lines as claimed in arXiv:2609.23015v2, but its strict-three private-chain conversion does not automatically preserve the bound. Urquhart cubic odd-expander Tseitin has four original 3-clauses per vertex, exponential ordinary Resolution, and *linear* semantic /341 native AND3/XOR refutations (4h-1). Published hardness against some rules never becomes hardness against all algorithms by analogy.

## 3. All-rule charged work and span from minimum UNSAT source core (PROVED/EXACT in the stated semantic model)

Let $\mu(F)$ be the minimum number of distinct **indexed original source clauses** whose conjunction is UNSAT (not the number of sources essential individually). Fix any finite source-authenticated, sound, source-explicit refutation DAG with one contradiction sink, at most two antecedents per paid node, no unsound assumption leaks, and conservative fresh definitions. The proof may choose its branching and sharing optimally *after the fact*.

Let U be the union of source indices in the sink's ancestry, let $s=|U|$, let $q$ be the number of distinct paid ancestors, and let d be the weighted critical-path depth when all paid nodes have unit weight and source leaves are free. Then

$$
q\ge \mu(F)-1
$$

and

$$
d\ge\left\lceil\log_2\mu(F)\right\rceil.
$$

**Proof:** If the selected original clauses F_U were SAT, a source model would extend across every conservative paid DEF and satisfy every sound inferred assertion, contradicting the sink. Thus $s\ge\mu(F)$. The undirected ancestry graph is connected; its $s+q$ nodes need at least $s+q-1$ edges, while every charged node has at most two incoming edges, so $2q\ge s+q-1$. For span, a node at depth zero is a source leaf (or has no source ancestors); a node at depth d with at most two parents has at most $2^d$ distinct original source ancestors by induction. DAG sharing can *decrease*, never increase, this count. Hence $s\le2^d$. These inequalities use neither a proof search strategy nor a forbidden new SPLIT/DISCHARGE rule. With weights >=w_min, logical work and weighted span acquire the factor w_min; no machine time/space consequence follows without an implementation model.

**Note:** /443 correctly established the first inequality but stated that no depth bound follows automatically. The second, **logarithmic** depth bound does follow under the same binary-premise ancestry assumptions. It is far too weak to establish a superpolynomial computation lower bound. It fails if someone silently permits an uncharged unbounded-fan-in source jump.

## 4. Sharpened all-rule bound on the established random hard 3-CNF (PROVED/EXACT)

Set $\alpha=1/60$ and $k=\lfloor n/60\rfloor$. If some indexed UNSAT subset of at most k clauses existed, choose an inclusion-minimal UNSAT subformula; by Tarsi it has at most t-1 occurring variables when it contains t clauses. For some r in [3,k], r+1 independently sampled source indices are therefore contained in one r-variable set. A union bound gives

$$
\Pr[\mu(F)\le k]\le
\sum_{r=3}^{k}\binom nr\binom{8n}{r+1}
\left(\frac{\binom r3}{\binom n3}\right)^{r+1}.
$$

As in the previously proved /443 estimate, elementary binomial bounds give

$$
\Pr[\mu(F)\le k]\le
\sum_{r=3}^{k}8e(r/n)^2(8e^2r/n)^r.
$$

The base is at most $8e^2/60=0.98520747985742\ldots<1$ for r<=n/60. Split the sum at r=sqrt(n): on the small-r range the base tends to zero; on the large-r range its contribution is dominated by a polynomial factor times $(8e^2/60)^{\sqrt n}$. Hence the sum is o(1). Combining with the published restricted proof-hardness event by a union bound shows that with probability 1-o(1) the *same* already established strict-3 family simultaneously has:

$$
W_{R_{\mathrm{mix341}}}(F)\ge\lfloor n/60\rfloor
$$

and

$$
\operatorname{span}_{R_{\mathrm{mix341}}}(F)
\ge\left\lceil\log_2(\lfloor n/60\rfloor+1)\right\rceil
$$

under the original /341 **semantic** sound, conservative, unit-charge at-most-binary-premise rules. Here span_R is the minimum ideal unit-weight critical path over legal source-authenticated refutation DAGs; all source clauses are free. The full hardware runtime and peak space are *not* bounded by interpreting these expressions without a machine simulation.

**Sharpening relative to /443:** the constant 1/60 replaces 1/64; the span is an independent necessary condition. The upper endpoint of the simple bound is $1/(8e^2)\approx0.01692$; a sharper entropy calculation suggests ~0.017081 as an unverified numerical extension, **not used** in the theorem. Thus the improvement is small and remains only linear paid-work hardness in n.

## 5. Ambient-vs-occurring variable correction (PROVED/EXACT)

Let U_n count ambient labels in [n] that do not occur in *any* of the 8n sampled clauses. Independence of sampled clauses gives the **exact** expectation

$$
\mathbb E[U_n]=n(1-3/n)^{8n}.
$$

For two distinct labels the joint probability of absence is

$$
\left(\frac{\binom{n-2}{3}}{\binom n3}\right)^{8n}.
$$

Therefore $\mathbb E U_n/n\to e^{-24}$ and $\operatorname{Var}(U_n)=O(n)$; the covariance term follows from Taylor expansion of the two absence probabilities, whose difference is $O(1/n)$. Chebyshev implies $U_n/n\to e^{-24}$ in probability. In particular, **the assertion in /456 that there are exactly n *occurring* variables almost surely is asymptotically false**, although the missing fraction is only $e^{-24}\approx3.7751345443\cdot10^{-11}$. All random-family results should say *n ambient variable labels*, retaining the published parameter n. Asymptotic $\Theta(n)$ counts and the degree theorem are unchanged; no gap in Pang's result follows.

## 6. Independent fixed-family computational validation

Used the **pre-existing K4 cubic odd-Tseitin source**, not a newly fabricated candidate hard formula. Six edge variables, 16 original signed proper 3-clauses, 163 ASCII DIMACS bytes, SHA-256 ea08104837e167b9ebd06d8f50442d828e3ba4d81f79dff8c14a09ba30050096.

The producer built the balanced *native-semantic* /341 derivation: 12 paid AND3 nodes reconstruct four original-source-attested parity rows in two levels, then 3 paid XOR nodes combine the four rows in two more levels. Every original clause is in the root ancestry. Exhaustive 64-assignment checking confirms UNSAT and a SAT witness after deletion of each separate source clause, so $\mu(F)=16$. Thus **both general bounds are tight on this existing control**, $q=15=\mu-1$ and $d=4=\log_2\mu$. This is an independent control of the already-known /341 + /447 constructions, not a new minimality result.

A separate Node.js verifier, without importing producer code, reconstructed original source bytes, all local 8-row conjunctions, the four GF(2) annotations and subsequent XOR sums, parents, depths, full source ancestry, every deletion witness, and the contradictory final row. **2,311 assertion checks passed and 12/12 hostile source/proof/branch-scope mutations were rejected.** It is *not* the historically authoritative R_mix341 byte checker.

Measured producer whole process 0.69 s wall, 96,268 KiB RSS; checker 0.04 s, 28,280 KiB RSS. Explicit JSON certificate 8,271 bytes. All lower bounds refer to **ideal logical node work and span**, not wall time, cache, output, failed tactics, parsing or simultaneous all-phase machine memory. Complete producer.py, verify.mjs, original DIMACS, full paid proof JSON, raw results, process resource logs and SHA256 manifest are in the local reproducibility archive (same conversation). Repo has role-owned report/summary and handoff, and no scheduler/machine-model changes.

## 7. Verified corpus and research limits

Read original fixed calculus /341 SHA c87acd11, /442, /443 SHA 7ed05b13, /447, /448, /449, /453, /456 SHA fda15d55, LSPV-1/454, referee 369/371, current issue #3, November 2 five-role handoff SHA c3889a3, AGENTS.md SHA 19656af1, CODEX.md SHA 754999f5, pnp research skill SHA b8df83a7, Grok actual GROKPROOF/2026-11-06_1617_PROGRESS.md SHA b931933, and Claude TPORT-0002 file. Other mandatory repositories read by authenticated GitHub connector: konard/p-vs-np/scripts/proof_status.json SHA 93b77ed and proofs/attempts/COMMON_ERRORS.md SHA 3de91b; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md SHA 18d693e and resolution_width_lab/THEOREM.md SHA b903042; meelgroup/frat-xor/format.md SHA 986a21; tanyongkiam/cake_lpr/README.md SHA e94f45; openai/math/README.md SHA cc5b0a. These sources are useful for trust boundaries; none authenticates historical /341 LOCAL private/exported-wire record bytes or proves B3. General indexed web searches consulted Pang 2026, Braun 2026, Cook ER, Chvátal–Szemerédi and Tarsi. A branded Google interface and historical accepted-byte checker were not available; neither was claimed executed.

No root main.tex edit: current blob SHA 8a440b7d81dbfe300470c7c097c7165802b1067a returned zero readable content from the available GitHub fetch, so safe outside-owned byte preservation was impossible. Existing root left unchanged.

**Actual advance:** sharpened, all-native-semantic source-core work lower bound and a new work/span joint necessary condition on the published strict-3 hard distribution; corrected ambient-vs-occurring asymptotic quantifier; independently validated a tight historical AND3/XOR control. **Still OPEN:** exact native accepted-byte DEF/LOCAL/export grammar, superpolynomial Wbar_R for all mixed legal proof DAGs, weakest noncircular same-R B3, and P versus NP.
