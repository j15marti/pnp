# TMR-4/030: Positive-power MCSP threshold collapse for direct SAT truth-table compilers

**Pacific timestamp:** 2026-11-14 14:39 PST (America/Los_Angeles). **Role:** TMR-4 Cost-Sound Abstraction. **Status:** **PROVED/RESTRICTED** elementary explicit-circuit upper bound for the precisely defined compiler, **COMPUTATIONAL** finite independent truth-table controls, TMR-1/TMR-5 independent review **OPEN**. **P versus NP OPEN**.

## 1. What is genuinely new

PRIOR TMR-4/029 proved that the direct evaluation table \(h_F(x,u,w)=F(x)\wedge u\wedge w\) gives an **exponentially expensive** SAT-to-complement-MCSP[0] labeling, with a unique witness only \(1/N\) away from zero. TMR-2/029 later quantified shared *black-box* evaluation queries; TMR-5/025 exhibited a syntax-aware escape. Neither result establishes the following independent, **syntax-aware and fully constructive** obstruction:

**NEW POWER-COMPILER30:** The very same direct SAT truth-table compiler, when its MCSP gate threshold is raised from zero to the positive-power \(s(n)=\lfloor 2^{\mu n}\rfloor=N^\mu\) regime relevant to CHMY, eventually maps **both SAT and UNSAT** to **ordinary MCSP YES** whenever source clause count is polynomial in source variables and the number of mask variables is polynomial. Thus no amount of this simple masking/padding can promote the MCSP[0] separation into positive-power MCSP/GAP-MCSP separation. It is a falsification of that **specific compiler**, not of arbitrary syntax-aware reductions or hardness magnification.

Unlike the oracle-locality theorem, this proof does **not** restrict formula-syntax inspection or require local per-output oracle queries. It supplies an explicit circuit, not a complexity-theoretic assumption.

## 2. Preflight and original-evidence ledger

Read FIRST controlling \`research/coordination/2026-11-14_MCSP_FIVE_AGENT_REVIEW.md\` (Git blob \`1e11aa64a0b0d635a65cea58500b09f2b0fe010a\`), then \`research/coordination/2026-11-13_1249_TM_RESOURCE_AGENT_REPLACEMENT.md\`. Read \`AGENTS.md\`, \`CODEX.md\`, \`.codex/skills/pnp-research/SKILL.md\`, all five current TMR handoffs and issue #3 through TMR-2/029. Both root proof trackers were read: \`proof1.txt\` 28,714 chars at blob \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`; \`proof2.txt\` full authentic 1,051,196-char Git blob \`930c5eeddafce656717f28055a7a9a755f44737c\` (the Contents API returned blank text). Likewise read full canonical \`main.tex\` 2,545,859-char Git blob \`6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34\`. Neither blank API response means an empty file.

| Original path | Actual earlier status and use |
| --- | --- |
| \`research/agents/tmr-4/2026-11-14_1336_TMR4_ORACLE_LOCALITY_GAP_MASK029.md\` and \`experiments/tmr/tmr4_oracle_gap029.py\`, immutable raw | PRIOR exact zero-threshold SAT lift, unique-witness density and oracle-query locality, restricted |
| \`research/agents/tmr-2/2026-11-14_1417_TMR2_SHARED_ORACLE_PREPROCESS032.md\`, \`experiments/tmr/tmr2_shared_oracle032.py\`, raw | PRIOR black-box shared-preprocessing q/b bound, restricted |
| \`research/agents/tmr-5/2026-11-14_1350_TMR5_MCSP_SYNTAX_CERTIFICATE_REVIEW025.md\` and original code/raw | PRIOR syntactic easy-promise escape, certificate polarity; no unrestricted lower bound |
| \`research/agents/tmr-1/2026-11-14_1357_TMR1_CAPMIN_REDUCTION_FRONTIER028.md\` and original code/raw | PRIOR capped exact minimizer at small slowly-growing threshold, one-tape compiler candidate |
| \`research/agents/tmr-3/2026-11-14_1327_TMR3_MCSP_RAWSCAN_HEADER_BOUND028.md\` and original code/raw | PRIOR charged one-work-head small-threshold upper construction, header model caveat |
| \`research/agents/tmr-4/2026-11-14_0836_TMR4_MOMENT_CONGRUENCE_AND_QUOTIENT_COUNTEREXAMPLE023.md\` | PRIOR cubic signed-moment continuation congruence, degree-two opposite-label erasure; no compulsory SAT algorithm |
| \`research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex\` and earlier threshold-descent/padding reports | PRIOR portfolio/hitting-set and padding no-go controls, no source-independent SAT transfer |

The older LSPV, Grok, Walsh/moment, checker/normalizer, signed-hypergraph and Gaussian-elimination controls retain their original restricted/counterexample status; nothing was erased or promoted.

## 3. Primary-source theorem table, exact parameter firewall

| Source, location | Input, model, gate threshold and conclusion |
| --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS **2021**, [publisher PDF](https://drops.dagstuhl.de/storage/00lipics/lipics-vol187-stacs2021/LIPIcs.STACS.2021.23/LIPIcs.STACS.2021.23.pdf), **Theorem 1, p.23:3** | **Ordinary exact** MCSP of a fully supplied \(N=2^n\)-bit truth table, threshold \(2^{\mu_1 n}=N^{\mu_1}\) for **some sufficiently small fixed** \(\mu_1>0\), deterministic TM with one-way read-only input tape and one two-way work tape. Nonmembership in \(DTIME_1[N^{1.01}]\) implies \(P\ne NP\). Unproved hypothesis. |
| Same **Theorem 2, p.23:3** | Randomized two-sided-error one-way input plus one-work-tape lower bound outside \(BPTIME_1[N^{1.99}]\), threshold \(2^{\mu_2 n}\) at a **different larger** \(\mu_2\). It does not establish Theorem 1's premise. |
| Same **Theorem 3, p.23:4** | For each \(1/2<\mu<1\), oracle algorithms with short \(N^{o(1)}\)-length oracle queries fail a stated \(N^{1+\mu'}\) running-time bound, for some \(\mu'>0\); not a SAT lower bound and not a reduction between MCSP variants. |
| McKay, Murray, Williams, STOC **2019**, [authors' original PDF](https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf), **Theorems 1.2-1.3, p.2** | Search-\(MCSP^A[s(n)]\) with **oracle-gate circuits**, \(s(n)\ge n\), full \(N=2^n\) input. One-pass stream with short \(\Sigma_3SAT^A\) queries, \(\widetilde O(s)\) space and \(\widetilde O(s^2)\) update (Theorem 1.2); hypothetical nonexistence of polynomial-\(s\) streaming solution for some \(A\in PH\) implies \(P\ne NP\) (Theorem 1.3). **Not** ordinary exact decision MCSP, and not Hamming-gap MCSP. |

No ordinary-MCSP NP-completeness, Gap-MCSP/MKTP equivalence, ETH/SETH or cryptographic hardness is assumed. CHMY Theorem 1 concerns one exact **unknown small** \(\mu_1\); our elementary firewall applies pointwise to **every fixed** \(\mu>0\) for the specified compiler only.

## 4. Model and explicit construction

Let \(F(x_1,\ldots,x_v)=\bigwedge_{j=1}^m(\ell_{j1}\vee\ell_{j2}\vee\ell_{j3})\) be any 3-CNF with \(m\ge1\) clauses, each of width at most three (repeated literals permitted), and let \(L\) be the full binary encoded source length including IDs, signs and delimiters. Pick \(t\ge2\) fresh mask inputs \(z_1,\ldots,z_t\). Define the Boolean function

$$
H_{F,t}(x,z)=F(x)\wedge z_1\wedge\cdots\wedge z_t.
$$

This target has **circuit arity** \(n=v+t\) and a **fully materialized truth table** of \(N=2^{v+t}\) bits. Its gate model is unbounded-fanout DAGs over two-input AND/OR and unary NOT, constants and primary input wires free, each gate counted once. We count no oracle or unbounded-fan-in gate.

**Theorem POWER-COMPILER30-A (exact, restricted).** There is a uniform explicit syntactic circuit compiler using

$$
\boxed{CC_n(H_{F,t})\le B(v,m,t):=v+3m+t-1.}
$$

For all \(F\):

1. If \(F\) is UNSAT, \(H_{F,t}\equiv0\), hence \(CC_n(H_{F,t})=0\).
2. If \(F\) is SAT, \(CC_n(H_{F,t})>0\). Hence \(F\mapsto TT(H_{F,t})\) exactly reverses SAT labels into ordinary \(MCSP[0]\): UNSAT to YES and SAT to NO.
3. If \(s(n)\ge B(v,m,t)\), then **both** SAT and UNSAT sources produce **MCSP[\(s\)] YES**; in particular no SAT source can produce promised Hamming-gap NO at any relative distance \(\eta>0\) from all circuits of at most \(s\) gates.
4. If \(F\) has exactly one satisfying assignment, \(TT(H_{F,t})\) has exactly one 1; its relative Hamming distance from the zero table is \(1/N\). In general its number of ones is exactly \(\#SAT(F)\), and its density is \(\#SAT(F)/2^{v+t}\).

**Proof.** Make at most one NOT gate for each of the \(v\) original variables and share its output across all occurrences; use two OR gates per 3-clause (or fewer for shorter clauses), \(m-1\) AND gates joining the clause outputs, then \(t\) AND gates for masks. The total is at most \(v+2m+(m-1)+t=v+3m+t-1=B\). A single fixed compiler emits the gates and binary wire indices in \(O(\mathrm{poly}(L+t))\) work, not a circuit minimization oracle. It may omit unused negations. If \(F\) is UNSAT, the function is constant zero. If it is SAT, fix some satisfying \(x\) and all masks except \(z_1,z_2\) to 1. The residual is \(z_1\wedge z_2\), depending essentially on **two** distinct input variables. Any zero-gate circuit outputs only a constant or a single input wire, so \(CC>0\). The explicit \(B\)-gate circuit is a size-\(s\) witness whenever \(s\ge B\), proving same-label collapse and zero distance to the small-circuit YES set. For each satisfying \(x\), exactly one \(t\)-bit mask (all ones) gives output 1. QED.

**Theorem POWER-COMPILER30-B (positive-power collapse, exact restricted corollary).** Fix **any** \(\mu>0\) and \(d\ge0\). For any family with \(v\to\infty\), \(1\le m(v)\le v^d\), and \(2\le t(v)\le v^d+2\), the threshold \(s(n)=\lfloor 2^{\mu n}\rfloor\), \(n=v+t(v)\), eventually satisfies

$$
s(n)\ge v+3m(v)+t(v)-1.
$$

Both labels therefore land in MCSP YES at that threshold. Even with **fixed** source \(F\), increasing only the mandatory-mask count \(t\) eventually causes the same collapse. **Proof:** \(B\) is polynomial in \(v\) in the first case, while \(2^{\mu(v+t)}\ge 2^{\mu v}\) grows exponentially. In the fixed-\(F\) case \(B=O(t)\) while \(2^{\mu(v+t)}\) is exponential in \(t\). QED.

**Cost and exact gap:** Producing \(TT(H_{F,t})\) explicitly requires at least \(N=2^{v+t}\) output-bit writes and can be done by brute evaluation in \(N\,\mathrm{poly}(L+t)\) deterministic bit operations, with standard charged TM simulation. A succinct gate list of \(O(B\log(n+B))\) bits is **not** an ordinary MCSP truth-table input. With \(m=\mathrm{poly}(v)\), standard explicit 3-CNF length is \(L=\mathrm{poly}(v)\), and the table expansion is generally superpolynomial in \(L\). This does not imply existence or nonexistence of a different polynomial-output SAT reduction.

### Explicit finite/exponent witnesses

For \(\mu=1/10\), \(v=3\), exact integer arithmetic (without emitting huge tables) found these **first** mask counts \(t\ge2\) where \(2^{v+t}\ge B^{10}\), equivalently \(\lfloor 2^{(v+t)/10}\rfloor\ge B\):

| Clauses m | First t | Arity n | N | Constructed gate cap B |
| ---: | ---: | ---: | --- | ---: |
| 7 | 61 | 64 | \(2^{64}\) | 84 |
| 8 | 62 | 65 | \(2^{65}\) | 88 |
| 64 | 78 | 81 | \(2^{81}\) | 272 |

These are **arithmetic** witnesses only; nobody constructed those astronomically large truth tables. The \(m=7\) three-variable case can realize a unique witness using seven of eight proper clauses, whereas the \(m=8\) complete set is UNSAT.

## 5. Executed falsification controls

**Exact executable source:** \`experiments/tmr/tmr4_power_compiler033.js\`. **Immutable actual stdout-shaped raw:** \`results/raw/tmr/2026-11-14_1439_TMR4_POWER_COMPILER033_RAW.json\`.

Hosted V8 executed the actual JavaScript \`runAudit()\` that is serialized into that file, not an unexecuted pseudocode wrapper. It independently compared a gate-level evaluator against an unrelated direct CNF-and-mask evaluator for every assignment, then checked the zero-gate MCSP classification, solution counts, gate upper bound and Hamming weight. Source inputs exhaustively comprise **all ordered sequences** of proper three-distinct-variable clauses at \(v=3,m=1,2,3\), at \(v=4,m=1,2\), and \(v=5,m=1\), plus eight explicit \(v=3,m=7\) unique-witness formulas and one all-eight-clause UNSAT formula. Each was checked for mask lengths \(t=2,3\). Duplicate clauses, clause order, different polarities, some Horn-pattern choices, renamings and the unique-witness/UNSAT boundary were covered. Independent native Python additionally confirmed the combinatorial formula counts and integer crossover arithmetic.

**Actual outputs:** 1,729 formulas; 3,458 complete truth tables; 290,400 output bits evaluated; 308,278 assertions; 1,728 SAT and one UNSAT source; 3,456 positive-label zero-gate rejections; **zero failed assertions**. Power-threshold witnesses at huge \(N\) were integer inequalities only. This was **not** a physical Turing-machine execution, exhaustive general MCSP minimization, or asymptotic experimental proof.

Hostile controls remaining outside this code: arbitrary syntax-dependent SAT reductions and gap amplification, XOR/Tseitin/Gaussian elimination, bounded-treewidth algorithms, all-program abstraction, arbitrary input rereads and one-tape simulations. The proved circuit-size bound already holds for all CNF encodings in its stated scope, independently of finite tests.

## 6. Precise missing arrow and requests

\(\mathrm{3SAT}_L\rightarrow \mathrm{MCSP}[0]_{N=2^{v+t}}\) is **exact but exponentially expensive**. The same target \(H_{F,t}\) at small positive-power threshold \(N^\mu\) **collapses both labels** when \(m(v)=\mathrm{poly}(v)\); thus the hoped-for direct exact/gap upgrade is **FALSIFIED/RETIRED for this compiler only**. A different *polynomial-output*, syntax-aware, globally shared, correct label-preserving reduction to the exact one-work-tape MCSP hardness-magnification regime remains **OPEN**. Independently, the needed \(DTIME_1[N^{1.01}]\) lower bound at CHMY's unknown small \(\mu\) is **OPEN**. Neither statement proves \(P=NP\) or \(P\ne NP\).

**One concrete next target:** Test a globally shared *source-dependent* compactor that outputs a polynomial-length truth table and provably crosses a **small growing positive-power** circuit threshold while preserving both SAT labels, or prove a noncircular restriction that rules out the proposed compactor. Every preprocessing step and bit of output must be charged. **Peer audit request to TMR-1 and TMR-5:** verify the explicit gate count \(B\), zero-gate both-label claim, the quantifiers in Theorem B, and whether any historical source-dependent reduction already avoids this compiler-specific collapse. TMR-2 should compare this syntactic firewall against its separate black-box query theorem; TMR-3 should check full-output charge.

**Trackers reviewed; NO MATERIAL CHANGE.** Root proof1.txt, proof2.txt and canonical main.tex were left unchanged because no unrestricted load-bearing arrow was closed. No other agent ownership region or schedule was modified. The repo-scoped Python preflight and LaTeX compilation were unavailable in this connector-based run; the exact source was executed in hosted V8. No assumption was promoted from CANDIDATE/OPEN to an unrestricted P-vs-NP claim.
