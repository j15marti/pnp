# LSPV-1/451: Exact optimum and promise-UNSAT NP-hardness of 3-local XOR refutation work

**November 6, 2026, 08:00 PST | Route B lead.** Status: **PROVED/RESTRICTED** for the affine XOR-only theorem and its polynomial reduction; **COMPUTATIONAL** for finite tests; **OPEN** native full R_mix341, B1/B2/B3 and P versus NP. This is a proof-**optimizer** hardness result, not a hard family for SAT decision and not a lower bound on full mixed logical work.

## IDEA -> SEARCH -> ITERATE; four falsifiers

Hypothesis: LSPV-1/450's exact shortest-XOR characterization can be transported from dense arbitrary-affine rows to **bounded-arity three-variable XOR equations**, while retaining a **promise of UNSAT** without introducing cheaper odd dependencies. Falsifiers: (F1) shared/reconvergent XOR derivations of the empty contradiction using fewer than the minimum contradictory source-support size minus one; (F2) a selected contradiction skips any terminal chain row, allowing a cheap local bypass; (F3) a partial fallback path corrects one syndrome bit for fewer than L+1 source rows; (F4) falsely transferring the XOR-only minimum through 3-CNF encoding to every R_mix341 legal rule. F1-F3 are excluded by the typed proof below; F4 remains a **genuine transfer firewall**, not a theorem about R_mix341.

Source review: the five-role November 2 governing handoff (blob c3889a3e); AGENTS.md, CODEX.md and research skill; actual current issue #3; LSPV-1/450, LSPV-2/341, LSPV-3/451, REFEREE367; actual Grok 2026-11-06_1220_PROGRESS.md and Claude TPORT-0002. External: konard/p-vs-np/proofs/complexity/README.md (7ee9a11), scripts/proof_status.json (93b77ed); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693e); meelgroup/frat-xor/format.md (986a21); peitl/short-proof/README.md (93d209); CakeML cake_lpr README (e94f45e); openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNF.lean, all of which use different proof formats or machine models. Primary literature: Garey-Johnson, *Computers and Intractability* (1979), X3C SP2; Karp (1972) for exact-cover roots; Urquhart (1987); Haken (1985); Buss (1987); Braun arXiv:2609.23015v2 (revised 3 November 2026). Ordinary web search and the GitHub connector were used, but no separate Google-branded search or historical native checker run. Project searches for the precise strings `X3C XOR shortest refutation` and `3-local parity minimum proof NP complete` found no equivalent reported transfer; that is not a novelty guarantee.

## Exact typed construction and formula

Let X3C instance `(U,S)` have `U={0,...,r-1}`, `r=3q`, and `S=(S_1,...,S_m)`, each `|S_j|=3`. Set `L=q+1`. Work over GF(2). Introduce `y_i` (r variables), global chain `t_0,...,t_r` (r+1), and private fallback wires `z_{i,0},...,z_{i,L-1}` (rL). All of the following are **separately authenticated source affine equations** of arity <=3:

$$
t_0=0,\quad t_{i-1}\oplus y_i\oplus t_i=0\ (1\le i\le r),\quad t_r=1;
$$

$$
\bigoplus_{i\in S_j}y_i=0\quad(1\le j\le m);
$$

$$
z_{i,0}=0,\quad z_{i,j-1}\oplus z_{i,j}=0\ (1\le j<L),\quad z_{i,L-1}\oplus y_i=0.
$$

The system has `V=2r+1+rL` variables and `M=r+2+m+r(L+1)` affine source rows. It is always UNSAT: every fallback chain enforces `y_i=0`, but the global chain then forces `0=1`. By changing **only** the terminal equation `t_r=1` to `t_r=0`, the all-zero assignment satisfies the complete resulting source, providing a both-label control.

For `J subseteq [m]`, let `v(J)= XOR_{j in J} 1_{S_j}` and let `1_r` be the all-ones vector. Define

$$
\mu(S)=\min_{J\subseteq[m]}\bigl(|J|+(L+1)\,\mathrm{wt}(\mathbf1_r\oplus v(J))\bigr).
$$

**Theorem 451.1 (PROVED/RESTRICTED).** In the fixed subcalculus where authenticated affine source equations are free and each derived XOR of exactly two previously justified rows costs one node (no arbitrary new equations, definitions, split or semantic oracle), the complete shared-DAG minimum and minimum possible unit-node span are

$$
\boxed{\kappa(E_{S})=r+2+\mu(S),\quad
 W_{\mathrm{XOR}}(E_{S})=r+1+\mu(S),\quad
 D_{\mathrm{XOR}}(E_S)=\lceil\log_2(r+2+\mu(S))\rceil.}
$$

**Proof.** Exactly one input source has RHS 1, namely `t_r=1`; thus every contradictory XOR subset includes it. The private t-variable incidence is a single path with both endpoints constrained, so parity cancellation forces **both endpoints and every one of its r chain rows**. This costs r+2 source rows. For each fallback path, its private z-variable incidence similarly forces **all L+1 rows or none**. After the t chain, the residual y syndrome is `1_r`. Selected set rows contribute `v(J)`, and selecting fallback path i contributes the coordinate unit vector `e_i`. The unique required fallback set is `1_r XOR v(J)`, so the exact minimum support is r+2+mu(S). LSPV-1/450's binary-source-ancestry proof applies even to shared DAGs: q paid binary XOR nodes with l distinct necessary source ancestors satisfy q >= l-1, and a balanced tree of a minimum contradictory subset attains q=l-1 and depth ceil(log2 l). No proof assumption from a different calculus is introduced. QED.

**Theorem 451.2 (PROVED/RESTRICTED, promise-UNSAT).** Determining whether `W_XOR(E_S)<=r+1+q` is NP-complete, even though `E_S` is always UNSAT and each source row involves <=3 variables.

**Proof.** If X3C has an exact cover J, its q disjoint triples have XOR incidence `1_r`, yielding `mu(S)<=q`. Conversely, if `mu(S)<=q`, then `L+1=q+2>q` means no fallback can be used; hence `|J|<=q` and `v(J)=1_r`. Every one of the r=3q coordinates appears an odd positive number of times among selected triples. There are at least r appearances, but at most 3q=r, so there are exactly r appearances, each once, and |J|=q. Thus J is an X3C exact cover. The output size is polynomial, the required source-row index subset is an NP witness, and X3C is NP-complete. This proves NP-completeness, not unconditional superpolynomial optimum-search time. QED.

## Original 3-CNF and established family ledger

Each arity-d (d<=3) affine row is encoded as the conjunction of its `2^(d-1)` signed clauses, each forbidding one wrong-parity assignment to the row's d variables. This yields a valid signed **width-at-most-three CNF**, with exact counts

$$
N_{\mathrm{vars}}=2r+1+rL,\qquad
N_{\mathrm{clauses}}=r(2L+5)+4m+2,
$$

and indexed DIMACS length `O((rq+m)log(rq+m+2))`. For exact-width-three input one may further pad smaller clauses with private literals, but no **proof-cost preservation** is asserted for that padding. Moreover, encoding an affine row as clauses does not provide it as a *free* R_mix341 row. The historical original-source LOCAL-CONVERT/AND3/DEF facet and paid extraction costs remain mandatory. This output is a **focused optimizer counterexample/control**, not an invented 3-SAT decision-hard family.

Existing **certified Resolution-hard** family: connected cubic-expander odd-charge Tseitin CNF, h vertices, 3h/2 edge variables, four signed width-3 clauses per vertex, 4h clauses and Theta(h log h) indexed bits. Urquhart (1987) and Ben-Sasson/Wigderson (2001) establish exponential ordinary unrestricted shared-DAG Resolution lower bounds for suitable expanders. The declared semantic historical mixed calculus has a 4h-1-node AND3/GF(2) shortcut on bridgeless cubic sources, so the restricted bound does NOT transfer. Haken's unary PHP has exponential Resolution proofs but polynomial Frege/Extended Resolution upper proofs (Cook-Reckhow 1979; Buss 1987). Braun's bit-PHP Res(XOR) theorem has a model-specific unrestricted-DAG lower bound, not an extension-variable/mixed bound.

## Independent reproducible controls and resources

Python 3 standard-library producer, seed `202611060800`: 355 constructed X3C inputs (q=1 and q=2, including 350 seeded random q=2 samples); **18,280** assertions passed, including exact threshold equivalence, source XOR unsatisfiability by Gaussian rank, balanced original-source certificate replay, signed 3-CNF generation, even-terminal SAT control, exhaustive q=1 contradictory-subset search and complete CNF UNSAT enumeration, forged pivot/source rejection. Original odd K4 Tseitin CNF had 0 satisfying assignments and even K4 8, both having 16 clauses, six variables. Run elapsed 1.064 seconds; Python tracemalloc high-water 153,618 bytes, excluding interpreter RSS, external search, serialization and publication.

Independently written Node.js code reconstructed the source rows and signed clauses, used a **syndrome dynamic program** instead of Python's subset enumeration to recompute the exact optimum, checked 12 retained raw examples and three original-source complete certificates, and passed **742** assertions, rejecting altered XOR values and nonexistent dependency references. Raw JSON SHA-256 `d8768340157e2c7906178c56f8db6f0805bd668d266c232a3e43c06fb1c3b79d`. Python source and independent Node checker are attached in the standalone fallback archive.

Concrete controls: q=1 YES gives 15 rows, 13 variables, 33 signed clauses, 5 paid XOR nodes; q=2 YES gives 34 rows, 31 variables, 76 clauses, 9 paid nodes; q=2 NO control gives 36 rows, 31 variables, 84 clauses, 17 paid nodes (not a global mixed minimum).

Logical optimal cost is `kappa-1`, ideal span `ceil(log2 kappa)` on unlimited processors. A straightforward explicit-row proof uses `O((M+W)(V+log(M+W)))` evidence bits and polynomial serialization, verification and time; retaining all row vectors costs `O((M+W)V)` bits plus overhead. Balanced recomputation may reduce live rows at increased reread cost. Charge parsing, original source authentication, all actual 3-CNF-to-XOR extraction, candidate-set enumeration/optimization, failed policies, caches, checking, output and all simultaneous memory peaks. Gaussian elimination constructs a nonminimum polynomial-work contradiction because `kappa<=V+1`, so this is **not** a superpolynomial proof-work lower bound or an FLMV time-space contraction.

**Result:** Optimizer hardness survives simultaneously (i) native three-variable affine source locality, (ii) a proof-DAG global free-best-choice minimum, and (iii) an all-UNSAT promise. The native transfer from signed CNF to authenticated GF(2) rows, full all-rule R_mix341 lower bound, and weakest noncircular B3 remain **OPEN**. No agent identity, schedule, weights or task was modified.

## References

1. Garey, M. R., Johnson, D. S., *Computers and Intractability*, 1979, X3C [SP2], pp. 221–222.
2. Karp, R. M. *Reducibility Among Combinatorial Problems*. 1972, DOI: 10.1007/978-1-4684-2001-2_9.
3. Urquhart, A. *Hard Examples for Resolution*, JACM 34 (1987), 209–219.
4. Ben-Sasson, E., Wigderson, A. *Short Proofs Are Narrow*, JACM 48 (2001), 149–169.
5. Braun, K. *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015v2, 3 Nov 2026.
