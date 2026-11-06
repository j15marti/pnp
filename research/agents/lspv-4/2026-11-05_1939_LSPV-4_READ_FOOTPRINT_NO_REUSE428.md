# LSPV-4/428: A restricted no-reuse countercontrol for actual-read-footprint SAT sharing

**November 5, 2026, 19:39 PST** | Route A primary | **PROVED/RESTRICTED** exact cache-policy counterexample | **COMPUTATIONAL** finite certificates | universal FLMV contraction **OPEN** | P versus NP **OPEN**.

## IDEA, falsifiers and correction

The initial test was whether the sound latest-anchor actual-read-footprint sharing construction of LSPV-2/432 could obtain guest reuse merely from the fact that many CNF children had the same SAT label. Falsifiers specified before literature review:

1. F1: a total uniform correct guest reads every child bit, making irrelevant differences visible to the footprint cache.
2. F2: an arbitrary number of equal-length proper 3-CNF children exist with identical UNSAT hard core, bit-identical long prefix, and fresh but different satisfiable tails.
3. F3: certified source-aware projection removes those tails, so the no-reuse observation is about a policy rather than a minimum over legal computations.
4. F4: worst-case work is just the claimed local budget, or physical index/head/high-water charges defeat an overoptimistic reading.

**ITERATION AFTER SEARCH:** LSPV-1/191 and LSPV-2/399 already established the every-polarity-bit pivotality theorem for odd cubic Tseitin sources, and LSPV-4/121 already tested guest-input read sensitivity. The separate 950 Python checks and 3,095 independent Node checks performed here are historical reproduction and **not new mathematics**. The actual new restricted target below attacks the specific LSPV-2/432 *latest-anchor read-mask cache*, not all sound algorithms or the older sensitivity theorem.

## Governing state and sources actually inspected

Governing 2026-11-02 12:04 PST five-role handoff at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`; current `j15marti/pnp#3`; `AGENTS.md` blob `19656af1`; `CODEX.md` blob `754999f5`; `.codex/skills/pnp-research/SKILL.md` blob `b8df83a7`; LSPV-2/431 and /432 (latter `research/agents/lspv-2/2026-11-05_1912_LSPV-2_ROUTE_A_SOLVER_READ_FOOTPRINT432.md`, blob `15804464e7`); LSPV-4/427 handoff blob `e15cfdd4`; LSPV-1/191 original `research/agents/lspv-1/2026-10-26_2005_LSPV-1_ARC_CONNECTED_SIGN_AUTH191.tex` blob `8cf015c1`; LSPV-2/399 blob `a307ff93`; Grok actual `GROKPROOF/2026-11-06_0215_PROGRESS.md` blob `eae7e6c9`; Claude actual `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727`.

Primary theory: FLMV (JACM 2005, §2.1 and Thm. 3.1, author PDF https://lance.fortnow.com/papers/files/tst.pdf); Urquhart, JACM 1987; Ben-Sasson and Wigderson, JACM 2001. Actual external repositories and paths: `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` blob `4bb5fd1`; `meelgroup/frat-xor/format.md` (checker supports a specific CNF/XOR proof format, does not prove arbitrary algorithm lower bounds); `konard/p-vs-np/proofs/complexity/README.md` blob `7ee9a11`, `scripts/proof_status.json` blob `93b77ed` (one-tape formalization, not FLMV index machine); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693e`, `RESIDUAL_EQUIVALENCE_BARRIER_REPORT.md` blob `4641359` (unrestricted exact residual equality is coNP-hard); `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` blob `1ced21f` (specific costed SAT driver, no generic guest cost). Indexed web searches used; direct Google-branded search unavailable. Unavailable and unexamined material is not asserted to have been read.

## Established family, exact encoding, model and shortcuts

Fix any simple connected bridgeless cubic graph $G=(V,E)$ on $H$ even vertices, with $|E|=3H/2$, and odd total charge $b:V\to\{0,1\}$. Give each edge one Boolean variable $x_e$. For each vertex with incident edges $e_1,e_2,e_3$, include the four **proper width-three** clauses falsified by the four local assignments with parity opposite to $b(v)$. Denote this original signed source by $U_H$. It contains exactly $4H$ clauses, $3H/2$ variables and $12H$ signed literal occurrences; a fixed self-delimiting signed-index binary encoding takes $\Theta(H\log H)$ bits.

**KNOWN:** Every assignment violates some vertex parity constraint because XORing all vertex equations yields $0=1$ for odd total charge. For suitable **growing cubic expander** graph families, Urquhart (1987) and Ben-Sasson–Wigderson (2001) give $2^{\Omega(H)}$ lower bounds against every ordinary shared-DAG **Resolution** refutation. They do not assert hardness against arbitrary SAT deciders, Extended Resolution, GF(2), or fixed $R_{\mathrm{mix341}}$. Suitable fixed finite graphs K4, cube, Petersen and Heawood used in tests are not themselves an asymptotic hard-family certificate. The existing native mixed AND3/GF(2) shortcut on the eligible odd cubic sources has $4H-1$ paid nodes, as established in prior project work; this is an upper-bound control, with all original rules and weights retained.

## Theorem: full-read guest defeats the latest-anchor read-footprint reuse

Fix $k\ge1$ and let $q=2^k$. Introduce fresh, mutually disjoint triples $(a_i,b_i,c_i)$ for $i=0,\ldots,k-1$, disjoint from every variable in $U_H$. For a tag $\tau\in\{0,1\}^k$ set

$$
C_\tau=U_H\land\bigwedge_{i=0}^{k-1}
\left(\ell_{\tau_i}(a_i)\lor b_i\lor c_i\right),\quad
\ell_0(a)=a,\quad\ell_1(a)=\neg a.
$$

**PROVED/RESTRICTED.** All $q$ formulas are different valid proper 3-CNFs of the same encoded length $L$. Every $C_\tau$ is UNSAT because it contains the authenticated UNSAT source $U_H$. Its tail is satisfiable independently (set every $b_i=1$). The $4H$ original clauses form a common prefix of $P=L-O(k\log(H+k))$ encoded bits. When $k=O(\log H)$, $P=L-o(L)$.

Let $D$ be any total correct deterministic ordinary-SAT decider. Construct $A_D$ to read **every child input bit in order** and subsequently execute $D$. $A_D$ is uniform, total and correct. It is polynomial if $D$ is polynomial (conditional, not asserted to exist).

The read footprint $R_{A_D}(C_\tau)$ is all of $\{0,\ldots,L-1\}$. Apply precisely the LSPV-2/432 policy: retain only the previous anchor, its answer and its actual read bitmap; on the next equal-length child, compare the current child with the anchor on every read location; if any mismatch, invoke $A_D$, replace anchor and rebuild bitmap. Give the portfolio in the order $\tau=0,1,\ldots,q-1$.

Every adjacent child pair differs. Consequently, this policy makes **exactly $q$ guest invocations and zero cache hits**, despite $q$ identical UNSAT decision labels. Under the explicitly declared ascending-address comparison order, every mismatch is beyond the shared prefix. Thus

$$
\text{compared child bits}\ \ge (q-1)(P+1)=\Omega(qL)
$$

and every initial/read/reuse step is charged. A different comparison order might find the changed tag sooner, so the comparison lower bound **does not** apply to every possible cache scheme. Neither no-reuse nor the lower bound applies to structural normalization or semantic algebraic sharing.

**Proof.** UNSAT follows because $U_H$ is a conjunct. Each tag is encoded in independent signs of the $k$ final clauses, establishing equal length and pairwise inequality. The full-read $A_D$ makes every bit mandatory for the *specific footprint check*, so a distinct tag invalidates the latest anchor. Since the initial child necessarily runs, all $q$ run. The common prefix contains the entire core. The suffix-only differences force the stated prefix reads in ascending comparison. This is a finite, uniform syntactic argument, not a statement about the inherent complexity of SAT.

**Legal escape / free optimum.** A source-authenticated compiler that checks the freshness and disjointness of each new clause, and exhibits $b_i=1$ as a simultaneous tail witness, may project away the whole satisfiable tail and call the guest once on $U_H$. The extra structure can be recognized and charged. Therefore there is no proof of a $q$-call lower bound for all correct solvers. The *ordinary Resolution* lower bound on any such $C_\tau$ persists from $U_H$ by standard restriction $b_i=1$ (the restriction of any refutation gives one for the core, with no more lines), but a short mixed-GF(2) proof still exists. No native $R_{\mathrm{mix341}}$ grammar was changed.

## All-phase indexed-machine ledger

For a **hypothetical already justified** Route A child generator with $q=N^{a+o(1)}$, $L=N^{\lambda+o(1)}$ and polylogarithmic charged bit ports, the specified ascending read-mask comparisons require $\Omega(qL)=N^{a+\lambda-o(1)}$ bit accesses on this family. With $(a,\lambda)=(3/5,1/2)$, this is $N^{11/10-o(1)}$, **exactly the proposed local-work ceiling**, not a contradiction to the recurrence.

Correct upper accounting separates construction/validation and failed policies, guest calls (up to $qT_{A_D}(L)$), input/output source-bit retrieval, indexed-address writes and clearing, mask creation/reset, cache lookup, assembly/conversion, and all-phase peak. A packed bitmap needs $L$ contiguous writable bits/cells; guest workspace and source-port scratch coexist, so an appropriately packed implementation has $O(L+S_{A_D}(L)+S_{port})$ peak writable/index extent, not merely live nonblank bits. A distant temporary indexed work-tape access can violate this bound, as LSPV-4/427 demonstrated; this example's conceptual complexity ledger is **not** a physical FLMV multitape benchmark. Fully materializing $q$ child input strings costs $\Theta(qL)$ writes rather than free lazy access. Logical proof nodes, evidence bits, parallel critical-path span, and actual work/space scheduling are distinct. The ideal proof-system minimization is free to select the best legal derivation, unlike a concrete executed cache.

No provenance argument permits replacing the fixed $R_{\mathrm{mix341}}$ with FRAT-XOR or granting a new split/discharge rule. Branch-specific assumptions cannot be reused without a justified implication. Here every UNSAT clause set contains the same authenticated $U_H$, so its algebraic contradiction is valid independently of all fresh tails.

## Executed finite controls and status

Two complete Python producers and **two independent Node referees** were executed locally. Historic polarity controls: 950 Python asserts, 3,095 independent Node checks, across K4, cube, Petersen and Heawood and opposite-label sign-flip, malformed and corrupt controls. New footprint-cache controls: 24 portfolios ($q=2,4,8,16,32,64$ for four graphs), 504 guest invocations, zero hits, 346,448 exact comparisons, 56,186 independent Node checks. Another standalone compact checker passed 216 tests on 15 additional finite portfolios. The q=64 instances give (graph, child length, common prefix, comparisons): K4 (414,306,19,341), cube (704,596,37,611), Petersen (988,862,54,369), Heawood (1324,1198,75,537). Full Python producers, independent JavaScript, source records, raw checks, proof and SHA-256 manifest are retained in the separately generated conversation reproducibility archive; the role-owned GitHub compact checker and raw summary are independently readback-tested.

Host-language bit counts do **not** demonstrate FLMV native-machine runtimes or high-water space. No finite experiment certifies exponential lower bounds on a growing family, and no claimed novelty derives from failure to find a paper.

## Next missing implication and status

The new lemma refutes the idea that LSPV-2/432's **specific sound footprint cache necessarily merges same-label children**; it does not refute the cache's soundness, alternative sharing, or an all-input contraction. A short source-aware algebraic derivation and fresh-tail projection are legal shortcuts, and the time saturation stays inside the proposed local exponent.

**OPEN:** Build a genuinely all-input, recursively iterable, malformed-aware, both-label, effective SAT child/join transformation on the SAME FLMV indexed machine, for every fixed correct polynomial SAT decider, with fully charged phases and

$$
t'\le\max\{11/10,3/5+t/2\},\qquad
s'\le\max\{1/2,s/2\}.
$$

Route B's fixed $R_{\mathrm{mix341}}$ minimum shared-DAG and noncircular B3 remain separately **OPEN**. Root `main.tex` and other roles' files remain unchanged. **P versus NP remains OPEN.**

## References

1. Fortnow L, Lipton RJ, van Melkebeek D, Viglas A. Time-Space Lower Bounds for Satisfiability. JACM. 2005;52(6):835-865. https://lance.fortnow.com/papers/files/tst.pdf
2. Urquhart A. Hard Examples for Resolution. JACM. 1987;34(1):209-219. https://doi.org/10.1145/7531.8928
3. Ben-Sasson E, Wigderson A. Short Proofs Are Narrow: Resolution Made Simple. JACM. 2001;48(2):149-169. https://doi.org/10.1145/375827.375835
