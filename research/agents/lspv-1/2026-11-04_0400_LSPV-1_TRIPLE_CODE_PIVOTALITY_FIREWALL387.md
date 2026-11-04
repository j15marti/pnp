# LSPV-1/387: Majority-coded pivotality firewall and encoding-relative all-decider read lower bounds

**November 4, 2026, 04:00 PST (America/Los_Angeles).** PNP General SAT Lower-Bound Lead (LSPV-1).
**Status: PROVED/EXACT elementary encoding counterexample and input-query lemma (specialist review pending); COMPUTATIONAL independent finite controls; OPEN unrestricted hardness and B1/B2/B3.** No changes to the preselected $R_{\mathrm{mix341}}$, its weights, or five agent tasks.

## 1. Published starting point and exact restriction

Haken (1985) establishes constants $c>0,h_0$ such that for **every** $h\ge h_0$, **every** ordinary unrestricted shared-DAG Resolution refutation of canonical unary $\mathrm{PHP}(h+1,h)$ needs at least $2^{ch}$ proof lines. The standard indexed signed CNF has $h(h+1)$ variables, $(h+1)+h\binom{h+1}{2}$ clauses and $N_h=\Theta(h^3\log(h+2))$ input bits. Free source axioms change the derived-node bound only by the polynomial number of source clauses. Cook (1976) gives polynomial Extended Resolution proofs: the lower bound does not cover extension gates or unrestricted algorithms.

Braun's September 19, 2026 preprint arXiv:2609.23015 reports a bound $>\exp(n/(32768\ell^2))$ for **every** unrestricted DAG-like, *extension-free* $\mathrm{Res}(\oplus)$ refutation of standard bit-PHP, for $\ell\ge32$, $n=2^\ell$. The source consists of $M=n\binom{n+1}{2}$ clauses each of width $2\ell$, encoded in $\Theta(n^3\ell^2)$ binary-indexed bits. It is a Lean-reported research preprint with independent specialist review pending. Neither theorem lower-bounds the fully combined $R_{\mathrm{mix341}}$ or arbitrary uniform SAT machine work. Previously checked polynomial paid-DEF pigeonhole and native GF(2) Tseitin proofs are mandatory countercontrols. **No attempt is made here to reprove a published hard-family bound.**

The unchanged $R_{\mathrm{mix341}}$ is fixed by LSPV-2/341, blob **c87acd11d32ccfc3b7acd3667ef11daeb60079cb**: free authenticated original CNF clauses and unit-paid at-most-binary-premise RES, AND3 local factors, binary GF(2) XOR, single-root locally checked LOCAL-CONVERT, and conservative two-input DEF. All DAG inference nodes have unit weight. This run introduces no proof-system rule.

## 2. Precise falsifier: one-bit pivotality is NOT representation invariant

Use the pre-existing LSPV-3/390 guarded bit-PHP source $H_\ell$ and its fixed explicit signed-CNF encoding $x_\ell=E(H_\ell)$ of length $N_\ell$; this is **not** a new hard family. LSPV-3/390 proves that $K_\ell=M(2\ell+1)+1$ designated literal-sign bit positions $p$ are individually pivotal: $x_\ell$ is UNSAT but every $x_\ell^{(p)}$ is a same-length valid SAT CNF. It also proves $K_\ell=\Theta(N_\ell/\log N_\ell)$.

Define another *uniform, linear-time, redundant external input encoding* $E_3$ by replacing **each** original input bit $b$ with the three physical bits $bbb$. On *every* binary physical input of length divisible by three, the fixed decoder takes the majority bit of each consecutive triple and then invokes the original self-delimiting CNF parser. It returns MALFORMED when the physical length or decoded source grammar is invalid. A valid decoded CNF is classified as SAT or UNSAT. Crucially, **all eight physical triple patterns are legal transport representations**, not only $000$ and $111$; the native DIMACS encoding and native mixed proof calculus are unchanged.

**Theorem 387A (representation-relative pivotality).** For every $\ell\ge1$:
1. $y_\ell=E_3(x_\ell)$ has length $3N_\ell$, decodes to UNSAT, and **no physical one-bit flip anywhere** changes its decoded source or SAT label.
2. For each of the $K_\ell$ original critical sign positions, each of the three **two-physical-bit flips within its corresponding triple** decodes to the SAT source $x_\ell^{(p)}$. The resulting opposite-label physical difference sets are the three pairs $\{1,2\},\{1,3\},\{2,3\}$ in that triple.
3. Hence the original statement "there are $K_\ell$ Hamming-distance-one valid SAT neighbors" becomes "there are zero Hamming-distance-one SAT neighbors" after a fixed, uniform, length-three-majority recoding, despite preserving all SAT/UNSAT/malformed distinctions by a linear-time parser conversion.

**Proof.** A triple $bbb$ has majority $b$ after any one physical bit is flipped. Any two flipped bits change the majority to $1-b$. Applying this to the distinguished sign positions reproduces exactly the known SAT original neighbors; all other original bits are unchanged. Encoding and decoding do not require knowing the SAT answer. QED.

The theorem falsifies **single-bit sensitivity as an invariant across sound polynomially intertranslatable encodings**. It does not undermine the fixed original encoding and does not establish that all correct deciders can skip source acquisition.

## 3. Surviving fractional acquisition bound

**Theorem 387B (encoding-relative, uniform all-decider lower bound).** Let $A$ be *one fixed* total randomized classifier, correct with error at most $\epsilon<1/2$ on **every binary physical input**, including malformed encodings. Suppose each charged input probe exposes one original physical bit. On the UNSAT input $y_\ell$,
$$
\boxed{\mathbb E[\text{distinct physical bits read by }A(y_\ell)]
\ \ge\ \tfrac32(1-2\epsilon)K_\ell.}
$$
Every deterministic exact classifier reads **at least $2K_\ell$ distinct physical bits** on that same input. If one charged probe reveals at most $b$ physical bits, divide the respective bounds by $b$ to obtain a probe-operation floor.

**Proof.** Fix one original pivotal sign index $p$. Couple runs on $y_\ell$ and the three two-bit-flip SAT neighbors with the same random tape. Their output distributions on the label UNSAT differ by at least $1-2\epsilon$. Before either of the two changed physical locations is inspected, the executions are identical. For each of the three pairs $(a,b)$ in this triple, therefore,
$$
r_{p,a}+r_{p,b}\ge1-2\epsilon,
\qquad r_{p,a}=\Pr[A(y_\ell)\text{ reads location }(p,a)].
$$
Sum the three pair inequalities: $2(r_{p,1}+r_{p,2}+r_{p,3})\ge3(1-2\epsilon)$. Sum over the $K_\ell$ disjoint sign triples and apply linearity of expectation. Deterministic error-zero executions must hit every two-element pair, which requires reading two of the three coordinates in every triple. This is the classical fractional hitting-set/adversary argument already proved for *general difference sets* in LSPV-1/309 (blob **597e46e5**); the new contribution is its **exact majority-code transformation and collapse-of-one-bit-pivotality countercontrol**, not a new general query-complexity method. QED.

Even though all physical single-bit SAT neighbors disappear, mandatory source-bit acquisition remains $\Omega(N_\ell/\log N_\ell)$, with the physical length $3N_\ell$. This is **only** a near-linear input-observation floor, not a lower bound on post-input computational work, proof-node cost, peak writable memory, or the complexity of SAT.

## 4. Explicit falsifiers and controls

**F1 (FALSIFIED):** The count of single-physical-bit opposite-label neighbors is preserved by any fixed uniform linear-time invertible source encoding. Majority recoding makes the count zero; original pivotality remains in distance-two neighbors. The redundant transport has a fixed decoder but is not injective on all physical strings; it is injective on canonical codewords and has a fixed well-defined semantics on every physical word. Do not silently equate this with the native parser's canonical syntax.

**F2 (FALSIFIED):** With zero one-bit pivotality, any exact solver may skip nearly every source sign position. The two-bit difference hypergraph forces at least two of each three positions on the UNSAT source under exact deterministic all-input correctness.

**F3 (FALSIFIED AS INFERENCE):** The amplified bound gives superpolynomial SAT time. It is at most linear in the new physical encoded length, and the general fractional-transversal bound never exceeds input length. A correct total all-input algorithm may still use exponential fallback; a family recognizer does not establish B1/B2/B3.

**F4 (MODEL CONTROL):** Canonical-only transport requiring exactly $000/111$ would make a one-bit flip MALFORMED, so the collapse of **opposite SAT neighbors** still occurs, but the *three-label* classifier would now have different labels. The actual theorem deliberately defines majority-tolerant transport, where one-bit neighbors have **the same** label. This construction is a different encoding, not a rule change inside $R_{\mathrm{mix341}}$.

Finite controls use the **existing** guarded bit-PHP family only to verify signs, not to search for a new hard example. Separate pure JavaScript implementations check $\ell=1,2$ exhaustively over all designated sign positions, and $\ell=3$ at a deterministic every-17th-position sample. The producer verifies explicit deletion/sign-flip satisfying assignments; the independent verifier uses a separate brute-force SAT evaluator on $\ell=1,2$. Both check triple-majority equivalence, source grammar, SAT/UNSAT and malformed cases. Raw summary and exact code revisions are published under project-standard paths. No random seed.

## 5. Three bridges, cost ledger and why the result is not a separation

For the same preselected mixed system, define $W_R(F)$ as the minimum unit-paid shared refutation-DAG count and $\overline W_R(N)=\max_{\mathrm{UNSAT}\ F,\ |\langle F\rangle|\le N} W_R(F)$ (zero for empty maximum). One total correct uniform $A$ is fixed before input quantification; $T_A^{wc}(N)$ is over **all** binary strings including malformed.

$$
\begin{aligned}
\mathrm{B1}:&\ \forall A\,\exists p_A\,\forall F\in\mathrm{UNSAT}:\ W_R(F)\le p_A(|F|+T_A(F));\\
\mathrm{B2}:&\ \forall A\,\exists p_A\,\forall N:\ \overline W_R(N)\le p_A(N+T_A^{wc}(N));\\
\mathrm{B3}:&\ \mathrm{SAT}\in P\ \Longrightarrow\ \overline W_R(N)=N^{O(1)}
 \quad(\text{same fixed }R).
\end{aligned}
$$

All three remain **OPEN for $R_{\mathrm{mix341}}$**. B1 implies B2 implies B3. The extra physical input coding affects none of these obligations.

The canonical source's $\Theta(N)$ output triples and their linear-time encoding/decoding must be charged. The query lower bound counts input probes only; input parsing, header/index reads, machine branching, decoded bit updates, trace checking, evidence bit serialization, witness/proof construction and eventual output are separate work. Streaming majority decoding can use $O(\log N)$ counters and $O(1)$ bit accumulator, while eager materialization requires $\Theta(N)$ writable bits for the decoded representation. An explicitly generated exponential intermediate incurs its full write/read/verification cost; compact lazy alternatives are legal and must pay construction/query costs. Shared proof nodes and physical scheduling/peak space remain separate. For FLMV recurrence claims, $\rho$ includes **every** local stage in $s'\le\max\{\rho,\eta,\lambda,\lambda s\}$.

**The new result is a hostile encoding/representation control, not B3, not a superpolynomial $R_{\mathrm{mix341}}$ lower bound, and not P versus NP.**

## 6. Review / provenance / duplication / access

Read the governing November 2 coordination directive (original commit 4e29ed7; current shared file blob c3889a3e), issue #3 through peer entries LSPV-5/335 (03:48 PST), original LSPV-2/341 (c87acd11), LSPV-1/309 (597e46e5), LSPV-1/386 (82f85a2d), LSPV-3/390 (c4edb7ad), LSPV-3/391 (816c4732), LSPV-2/387 (b848298a), LSPV-4/383 issue entry, and LSPV-5/335 (d47094c2), as well as AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md. The fractional hitting-set proof is explicitly **prior art** from LSPV-1/309. LSPV-3/390 already proves near-linear randomized input reads for its native code. This result changes the **encoding** to test whether "number of pivotal physical signs" is intrinsic. There is no claimed new general decision-tree theorem.

Actual external assessments inspected: **GROKPROOF/2026-11-04_1217_PROGRESS.md**, blob cae0560d (its 04:17 PST timestamp postdates this report's nominal 04:00 slot and is not used for chronological priority), and **research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex**, blob 1f9fc727, plus **research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex**, blob 9a5b05d6. Grok's proposed cut-width-to-short-child inference is refuted by LSPV-4/382; neither assessment provides B3. Primary literature queries: "Haken intractability Resolution PHP 1985", "Cook 1976 extended resolution pigeonhole", "Braun Res(oplus) bit PHP September 2026", and "fractional certificate complexity classical query adversary". Relevant primary literature is cited below. Project GitHub search queries: "fractional hitting set source reads", "randomized bit probe LP", "majority triples SAT bit flip", "semantic equivalence unsat", "guard cofactor"; the closest previous work was LSPV-1/309 and LSPV-3/390. A github.com/openai implementation was searched for in earlier role audit, but none is required for this elementary lemma. No GitHub-owned or OpenAI-authored checker is represented as independent mathematical authority.

**Publication safety:** the large root \`main.tex\` returned blob SHA \`07f76ecdf0a73c2e8bd8326c56ca274d2cbfba23\` but **zero bytes even on a first-lines request**; no partial or blind overwrite will be attempted. This dated role-owned report and five-role handoff are the safe outbox. The exact normal form and full syntax of LOCAL-CONVERT remain subject to the machine-readable checker gap reported by Red Team/335. No task identity/state/schedule is modified.

## 7. Next precise target

Test whether a **source-authenticated, polynomial-overhead transport of the complete signed difference-hypergraph across all legal original \(R_{\mathrm{mix341}}\) transformations** exists without re-encoding the original input as free semantic data. If it does, quantify what it forces beyond a linear input-read floor; if not, exhibit a legal original-rule counterexample. The required B3 trace-to-fixed-calculus implication and a superpolynomial mixed-system worst-case proof minimum remain OPEN.

**References:** [1] Haken, *The Intractability of Resolution*, TCS 39 (1985), 297–308, DOI 10.1016/0304-3975(85)90144-6. [2] Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4) (1976), 28–32. [3] Braun, *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015 (2026-09-19), https://arxiv.org/abs/2609.23015. [4] Cook–Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), 36–50. [5] LSPV-1/309, randomized source-query fractional transversal (2026-11-01). [6] LSPV-3/390, guarded bit-PHP critical sign probes (2026-11-04). [7] Certificate Games and Consequences for the Classical Adversary Bound, ITCS 2023 (background, no novelty claim).

<!-- END_OF_VERIFIED_REPORT::LSPV-1::TRIPLE_CODE_PIVOTALITY_FIREWALL387 -->
