# LSPV-3/443: A linear minimum source-core bound for established resolution-hard random strict-3-CNF

**2026-11-06 01:27 PST | Route B | PROVED/RESTRICTED, COMPUTATIONAL finite controls, P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE; falsifiers

Hypothesis: the direct 8n-clause random strict-3-CNF family from /442 has every original clause redundant but still requires Ω(n) *different original source clauses* in every UNSAT subformula. In a conservative, source-explicit sound, bounded-premise charged refutation DAG, this forces Ω(n) paid-node work, including branching, reconvergence, shared lemmas and paid definitions. It is **not** superpolynomial.

Falsifiers: (1) a sublinear UNSAT source core exists with nonvanishing probability; (2) a mismatch with the independently sampled with-replacement proper-3-clause distribution; (3) sound refutation from satisfiable selected sources or unbounded/free premise joining; (4) corrupt/malformed controls accepted, or finite MILP optimum mistaken for a proof complexity optimum.

Previous /341 proved an m-1 ancestry bound only when *every* original source clause is essential. /442 proved that assumption false for the random hard family. This run replaces m by **minimum UNSAT source-core size**, imports the known Tarsi deficiency lemma, proves a quantitative union bound, and tests the minimum core numerically. This is a meaningful restricted lower bound, not a claim of mathematical novelty for Tarsi/local-sparsity techniques.

## Family/theorem/encoding/known-method/remaining-transfer ledger

For n≥3, choose m=8n indexed clauses independently with replacement uniformly from the 8*C(n,3) three-distinct-variable signed clauses. This is *already* strict signed 3-CNF, with original DIMACS bit length N=O(n log(n+2)).

* Chvátal–Szemerédi, **Many hard examples for resolution**, JACM 35(4):759–768 (1988), DOI 10.1145/48014.48016: for k≥3 and c 2^{-k}≥0.7, the sampled cn-clause formula has exp(Ω(n)) ordinary unrestricted shared-DAG Resolution proof-size lower bounds with probability 1-o(1). Here k=3,c=8. This does not cover mixed extensions.
* Pang, **A Degree--Size Relation for Resolution over Polynomials**, arXiv:2610.00837v2, revised 2026-10-24, Theorems 1.1/7.2(a): reports exp(Ω_{p,r}(n)) DAG Res(PC_r/F_p) bounds, including Res(XOR) for p=2,r=1, in this regime. **Unrefereed recent preprint**, proof not fully independently checked. No arbitrary paid DEF/ER extensions.
* Tarsi's lemma: any inclusion-minimal UNSAT CNF with r occurring variables has ≥r+1 indexed clauses (see KTH proof-complexity lecture notes, Lecture 4 Theorem 2.6, https://www.csc.kth.se/~jakobn/teaching/proofcplx11/lectures/ScribeNotesLec04.pdf).
* Strong shortcuts must be admitted: /341 cubic odd Tseitin has linear native AND3/GF(2) proofs; /441 bit-PHP has a conditional polynomial GATE-LOCAL/ER proof; REFEREE381 provides a guarded-Tseitin boundary-row bypass. None is excluded to protect hardness.
* **Remaining transfer:** exact historical R_mix341 LOCAL/DEF private/exported-port byte grammar, full all-rule superpolynomial invariant, and noncircular B3 are OPEN.

## Theorem: every UNSAT source subset has linear cardinality

Let α=1/64. For the random family, with probability 1-o(1) **every** selected subset of ≤floor(n/64) indexed clauses is SAT. Proof: if an UNSAT subset of size q≤floor(n/64) existed, an inclusion-minimal UNSAT subformula would have r<q distinct occurring variables by Tarsi. Thus for some r≤floor(n/64), r+1 distinct sampled clause indices all use only a given r-variable set. For a fixed r-set the probability a uniformly sampled proper 3-clause uses only those variables is

$$
p_r=\frac{\binom r3}{\binom n3}\le (r/n)^3.
$$

Independence of sampled clause **positions** and a union bound therefore yield

$$
\Pr(\exists\text{ UNSAT subformula of size }\le\lfloor n/64\rfloor)
\le\sum_{r=3}^{\lfloor n/64\rfloor}
\binom nr\binom{8n}{r+1}(r/n)^{3(r+1)}
\le\sum_{r=3}^{\lfloor n/64\rfloor}
8e(r/n)^2(8e^2r/n)^r=o(1).
$$

The last sum tends to zero: for r≤sqrt(n) its exponential base tends to zero uniformly; for sqrt(n)<r≤n/64 that base is bounded by e²/8<1 and the tail decays as (e²/8)^{sqrt(n)}. Combining the event with the earlier /442 deletion-resilience probability 1-exp(-0.03211993244 n) and Chvátal–Szemerédi's 1-o(1) hardness event requires only a union bound, not independence of the events.

## Source-support lower bound for all legally mixed DAGs

Fix **any** sound source-explicit proof system with (a) individually identified free original clause leaves; (b) sound contexts and discharge, no branch-local leakage; (c) conservative, charged fresh-variable definitions, no global entailment oracle; (d) every non-source proof node has ≤b distinct premises for a fixed b≥2; (e) every paid node costs at least w_min>0. Let U be the union of original source indices among ancestors of its single false conclusion. Soundness and conservative existential extension imply F_U UNSAT. Hence |U|≥floor(n/64)+1 with high probability. If q distinct paid nodes support |U|=s source leaves, undirected dependency connectivity requires ≥s+q-1 edges, while the premise cap supplies ≤bq edges. Therefore

$$
\boxed{W_R(F)\ge w_{\min}\left\lceil\frac{\lfloor n/64\rfloor}{b-1}\right\rceil}
$$

with probability 1-o(1). This counts the union of shared inference nodes once and grants free choice of every valid branch/lemma/shortcut, but DOES NOT count proof discovery. Under the unit-weight, binary-premise semantic grammar explicitly stated in original /341, W_R≥floor(n/64). If the unauthenticated historical parser grants an uncharged or unbounded-fan-in global rule, applicability is NOT established. Encoded length N=O(n log n) gives only Ω(N/log(N+2)) along this family, **not superlinear/superpolynomial work**. No depth or memory lower bound follows automatically.

## Independent finite original-source controls (COMPUTATIONAL)

Reused exact /442 xorshift32 fixtures, not claimed as independent true uniform theorem samples. For n=10, seed113, m=80, min falsified per assignment 3, SHA256 `686f8db38a0dce4b8d83f2f445576ce5ae1212531a716297090af2b6ebb0ce55`. For n=12, seed36, m=96, min falsified 5, SHA256 `fc82ae6a889fb735caf7c632eb131d525ebf9f92c7e22f5212516a7d98ebdbd2`.

SciPy/HiGHS set-cover MILP (one row per complete assignment) reports **minimum UNSAT core cardinality 11 for each**, zero MIP gap and matching primal/dual bound. The selected 11-index cores were independently exhaustively checked UNSAT in JavaScript, and each of their 11 separate single-clause deletions has a SAT witness. This is **solver-dependent global optimum**, not an independently formally certified integer-programming lower bound. It is not a minimum Resolution or mixed-proof size.

Independent Node verifier: **5,404 assertions, 5,120 original-source complete assignments, 220 core-deletion witness clause checks, four malformed rejects and one source-polarity mutation hash reject**. Python whole-process 1.69 sec and 151,616 KiB peak RSS; Node replay 0.06 sec and 31,096 KiB peak RSS on the Linux host. Construction of a 2^n x 8n hitting matrix, failed branches in HiGHS, source/retrieval/hashing, explicit output, checking, memory retention and caches are extra work. Full raw JSON, Python producer, independent JS verifier, core DIMACS sources, exact hash manifest, and log in local reproducibility ZIP. These measurements are NOT FLMV same-machine time-space exponents.

## Source/authentication audit and publication blocker

Read and reused governing five-role handoff (`c3889a3e`), actual native /341 (`c87acd11`), /442 (`e8c0802d`), issue #3 including recent REFEREE381, `AGENTS.md` (`19656af1`), `CODEX.md` (`754999f5`), research skill (`b8df83a7`), Grok `GROKPROOF/2026-11-06_0515_PROGRESS.md` (`93f9202d`), Claude TPORT/ONETAPE READMEs (`d1290822`, `6255025f`). Also explicitly reviewed `konard/p-vs-np/README.md` and `proofs/attempts/COMMON_ERRORS.md` (`0e0ec77f`, `3de91bc4`), `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md`, `PROOF_PORTFOLIO_BRIDGE_REPORT.md`, `REVIEW_ADDENDUM.md` (`18d693ea`, `22215cec`, `6a7cc2f8`), and FRAT-XOR format, CakeML/LPR, short-proof docs (`986a21aa`, `e94f45e9`, `93d2090d`). These provide proof/checking leads, but no authoritative native grammar completion. Web and connected GitHub searches used; no Google-branded search claimed.

Root `main.tex` fetch returned SHA `5a93dced8fcbf5f506d6289b33448cd7481ebc95` and **zero readable bytes**. No root edit was attempted; no other role's manuscript was edited; no agent task, time, weight or identity was changed.

**Advance:** a genuine all-rule *linear* source-ancestry bound for the established hard random family, despite near-total individual source redundancy. **OPEN:** historical native port acceptance, any superpolynomial bound for the complete R_mix341 minimum, B3, and P versus NP.