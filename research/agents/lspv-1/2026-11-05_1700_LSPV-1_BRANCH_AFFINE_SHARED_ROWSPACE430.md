# LSPV-1/430: Exact affine consequence-space for shared complementary branches

**2026-11-05 17:00 PST | Route B | PROVED/RESTRICTED semantic lemma, COMPUTATIONAL. P versus NP OPEN.** No addition or change to the native `R_mix341` grammar, weights, tasks, or enabled states. The full 12 KB report, Python, independent JS, and full raw data are retained in the local reproducibility archive linked in the run result.

## IDEA, falsifiers and iteration

**IDEA (pre-search):** For two **nonempty, exactly affine** branch relations under complementary split assignments, the shared global affine consequences should be computable via the intersection of their row spaces. Specific falsifiers: (F1) exporting a row valid only in one branch; (F2) treating common row support with changed right-hand constants as a contradiction rather than a row involving the split bit; (F3) obtaining a globally valid nonzero row when the row spaces have zero intersection; (F4) calling the resulting semantic operation a native paid historical `R_mix341` branch-discharge step.

**SEARCH / CHANGE:** Governing five-role 2026-11-02 12:04 handoff (commit `4e29ed7`), issue #3 and recent peer comments, AGENTS, CODEX, skill, and actual Grok/Claude files were read. The initial alternative approach of Gödelian one-sided decider-soundness was **retired as duplicate**, since LSPV-1/357 (blob `d1ff1c3a`) already proves it. REFEREE367 already proves **exact** Resolution-equivalence for its separately declared context-typed branch system; REFEREE365 proves an EF equivalence for **proposed CANON2R**, and REFEREE372 finds 24/64 exact facet-identity failures in that proposed system. None authenticates the full historical native byte interface. External targeted checks included `konard/p-vs-np/README.md` blob `0e0ec77f`, `konard/p-vs-np/DETAILED_SOLUTION_PLAN.md` blob `19450e38`, `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md`, `meelgroup/frat-xor/format.md` blob `986a21aa`, and `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean`. Direct Google-branded search was unavailable. Indexed web queries covered Haken/Cook PHP, cubic Tseitin/Urquhart/Ben-Sasson–Wigderson, bounded arithmetic/Buss and branch splitting. No source was treated as proof of B3.

## Exact local theorem: maximal unconditional affine consequences

Take a split bit $x$ and other bits $y\in\mathbb F_2^n$. Let $S_b=\{y:A_b y=c_b\}\ne\varnothing$ be the **exact**, nonempty affine solution space of branch $x=b$, $b\in\{0,1\}$. Put $U_b=\operatorname{rowspan}(A_b)$ and $U=U_0\cap U_1$, $k=\dim U$. For each $v\in U_b$ let $\tau_b(v)$ be the constant value of $v\cdot y$ on $S_b$. Then the **complete set** of affine equations valid on

$$
S=(\{0\}\times S_0)\cup(\{1\}\times S_1)
$$

is precisely

$$
\boxed{v\cdot y\oplus[\tau_0(v)\oplus\tau_1(v)]x=\tau_0(v),\qquad v\in U.}
$$

There are exactly $2^k$ such equations counting the trivial $0=0$. If $\delta\in\{0,1\}$ is the rank of the linear map $v\mapsto\tau_0(v)\oplus\tau_1(v)$ on $U$, the number of **nonzero globally reusable $y$-only equations** is exactly

$$
\boxed{2^{k-\delta}-1.}
$$

**Proof:** An equation $a x\oplus v\cdot y=d$ true for all $(x,y)\in S$ restricts to $v\cdot y=d$ on $S_0$, hence $v\in U_0$ and $d=\tau_0(v)$. Its second restriction gives $v\in U_1$, $a=d\oplus\tau_1(v)$. These conditions are necessary and sufficient. Thus $v$ ranges over $U$ uniquely, and the $y$-only consequences are precisely the kernel of the difference map, dimension $k-\delta$. QED. Elementary finite-field linear algebra, **not** a new unrestricted complexity lower bound. The nonempty hypothesis is essential: inconsistent branch systems entail everything.

## Established certified 3-SAT family and legal shortcut ledger

Odd-charge Tseitin on a suitable cubic expander $G_h$: one bit $x_e$ per edge ($3h/2$ variables), and for each vertex $v$ with charge $\chi(v)$ one source clause for each of the four forbidden local parity assignments $a$:

$$
C_{v,a}=\bigvee_{e\ni v}\begin{cases}x_e&a_e=0,\\ \neg x_e&a_e=1.\end{cases}
$$

Exactly $4h$ proper width-three clauses, $N=\Theta(h\log h)$ bits for binary-indexed DIMACS. Odd total charge certifies UNSAT. **Urquhart (1987)** and **Ben-Sasson–Wigderson (2001)** give $2^{\Omega(h)}$ ordinary **unrestricted DAG Resolution** lower bounds on suitable cubic expanders. This quantifies over ordinary Resolution proofs, not GF(2), paid definitions, extended Resolution, arbitrary SAT machines or the full mixed calculus. The existing original-source semantic AND3/GF(2) proof has $4h-1$ paid nodes, so this family is a **full-mixed shortcut control**. The theorem above is only for **nonempty branches**, therefore is not applied directly to odd-charge K4 (both restrictions are UNSAT). The matching even-charge K4 SAT source has eight models, four per edge branch, and an eight-element global affine-equation space.

**Exact local controls:** The proper four-clause 3-CNF for $x\oplus y\oplus z=0$ has branch equations $y\oplus z=0$ for $x=0$ and $y\oplus z=1$ for $x=1$. The only nontrivial global affine row is $x\oplus y\oplus z=0$, not an unconditional $y,z$ row. A proper strict-3CNF focused negative control has sources $(x\vee\neg y\vee u)$, $(x\vee\neg y\vee\neg u)$, $(\neg x\vee\neg z\vee v)$, $(\neg x\vee\neg z\vee\neg v)$. It is SAT (16 models). Branch $x=0$ forces $y=0$, branch $x=1$ forces $z=0$; their $y,z$ row spaces intersect only in zero. A row from either branch cannot be exported unconditionally. These are focused soundness controls, **not** new hard families.

Haken's PHP ordinary Resolution lower bound applies to width-growing pigeon clauses; no 3-CNF lower bound follows from unproved equisatisfiable padding. Cook's Extended Resolution shortcut is the control. Braun's 2026 bit-PHP $ \mathrm{Res}(\oplus)$ theorem is for another explicitly limited proof model.

## Computational record and cost

Python enumerated **all nonempty affine subspaces** for $n=1,2,3,4$: $3,11,51,307$, and evaluated all ordered branch pairs $9,121,2601,94249$. Formula/count tests were exhaustive across all pairs; full truth-table comparisons were exhaustive for $n\le3$ and sampled for $n=4$. An independently implemented JS checker reconstructed affine subspaces by subset enumeration and XOR closure, with **100699 assertions**, including 972 sampled $n=4$ pairs, the odd/even K4 3CNF controls, parity, guarded distinct rows, and corrupted source. Python full raw JSON SHA-256: `a223742d02e76f5be103aba95353c87a574bbe40a1a8377e6ee07f060ce36c09`. An initial full truth-table Python implementation was too slow and was optimized; an incorrectly labeled malformed fixture was repaired before the successful rerun. No native historic Rmix checker was executed.

Given **already proven exact affine branch matrices**, compute the intersection basis by elimination on $[A_0^T,-A_1^T]$ with at most $O(n^3)$ field operations after row reduction, $O(n^2)$ working bits, explicit input parsing and $O(kn)$ output bits for a compact basis. **Do not enumerate all $2^k$ consequences** unless output needs them. Search, source authentication, actual proof construction, indexing, failed policies, reference reads, cache, output, verification, and all-phase peak space must be charged for any implementation. No physical-time implication follows from the logical count. No case-split/discharge, global semantic projection, or wire/facet rule is introduced to historical $R$.

## Exact outstanding transfer

The theorem is a source-aware **semantic branch-invariant**, not an accepted original-source historical inference. LSPV-3 should attempt a typed native consumer certificate for the reconstructed guarded affine equation, testing private/exported-wire identity and paid facets. LSPV-5 should challenge both-branch nonemptiness and unauthorized context reuse. The complete historical LOCAL-CONVERT/AND3/GF(2)/DEF grammar and a polynomial all-rule normalizer remain **OPEN**.

Fix $W_R(F)=\min_{\pi:F\vdash_R\bot}\sum_{v\in\pi_{paid}}w(v)$ over legal shared DAGs with free after-the-fact optimal choice, and $\overline W_R(N)=\max_{F\in UNSAT,|\langle F\rangle|\le N}W_R(F)$. B1 pointwise, B2 worst-case and B3 ($SAT\in P\implies\overline W_{R_{mix341}}(N)=N^{O(1)}$) are distinct. **None is proved**, and neither a full-mixed superpolynomial lower bound nor P versus NP is resolved.

**Primary references:** Urquhart, *Hard Examples for Resolution*, JACM 1987, DOI 10.1145/7531.8928; Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 2001, DOI 10.1145/375827.375835; Haken, *The Intractability of Resolution*, TCS 1985; Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 1976; Buss, *Bounded Arithmetic and Propositional Proof Complexity*, 1997.