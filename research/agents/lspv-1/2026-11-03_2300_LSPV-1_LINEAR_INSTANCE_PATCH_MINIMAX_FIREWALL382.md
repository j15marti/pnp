# LSPV-1/382: Linear-instance patch minimax firewall

**November 3, 2026, 23:00 PST (America/Los_Angeles).** **PROVED/EXACT elementary quantifier counterexample**, subject to independent specialist review; **COMPUTATIONAL** finite patch controls; **KNOWN THEOREM** Hartmanis–Stearns deterministic time hierarchy and Haken's Resolution PHP lower bound. **OPEN**: B1, B2, B3, superpolynomial minimum for the complete fixed R_mix341, P versus NP. No rules, weights, tasks, identities, schedules or enabled states were modified.

## Preselected SAT and proof models

The unchanged project `R_mix341` has authenticated free input-clause leaves and unit-charge distinct derived shared-DAG nodes under binary RES, at-most-three-support AND3/local factors, authenticated GF(2) row combination, paid conservative signed two-input auxiliary definitions, and the actually justified LOCAL-CONVERT rules. The general opaque public-wire/payload grammar remains incompletely certified, so no claim is made about its normalization here. For valid UNSAT CNF `F`, `W_R(F)` is the minimum node weight of any legal refutation, and `Wbar_R(N)` is its maximum over valid UNSAT encodings of length at most N, zero if the set is empty. Malformed strings are rejected by the total SAT language, rather than treated as UNSAT refutation sources. This run does not infer physical time from W.

**Published certified hard anchor, EXACT model:** Haken (1985), for constants `c>0,h0`, every `h>=h0` and *every unrestricted ordinary shared-DAG Resolution* refutation of standard signed unary pigeonhole CNF `PHP(h+1,h)`, requires at least `2^(ch)` proof lines. It has `h(h+1)` source variables, `(h+1)+h*binom(h+1,2)` original clauses, and standard explicit signed DIMACS length `N_h=Theta(h^3 log(h+2))` bits. Converting total lines to paid derived nodes subtracts at most the number of source clauses. This theorem **does not** concern arbitrary uniform SAT deciders, nonuniform circuits, Extended Resolution, Res(oplus), or the full R_mix341. Cook's polynomial ER refutations of PHP and R_mix341's linear GF(2) odd-Tseitin refutations are mandatory countercontrols.

## Precise falsification target

Let `L subset {0,1}^*` be an arbitrary **decidable total binary language**, let `U_L` be one fixed ordinary deterministic total correct decider, and let `ell(A)` denote the bit length of a self-delimiting ordinary program on a fixed reasonable universal machine. The proposed misleading 'algorithm-independent pointwise optimum with description cost' is

$$
M_L(N)=\max_{|x|\le N}\;\min_{\substack{A\text{ one total correct uniform decider of }L\\\ell(A)\le c(N+1)}} \left[\ell(A)+T_A(x)\right].
$$

Here `A` is one genuine total correct uniform program on **all** input lengths, not a partial algorithm; but the MINIMUM may choose a **different A for each x**. This quantifier issue survives charging *linear program description length* and every run's source read and answer.

### Theorem 382: linear-description single-instance patch collapse (PROVED/EXACT)

For every decidable binary language L, there are constants c,C independent of input x and horizon N such that **for all N**, 

$$
M_L(N)\le C(N+1).
$$

More explicitly: 

$$
\forall L\text{ decidable}\;\exists c,C\;\forall N\;\forall x\in\{0,1\}^{\le N}\;\exists A_x:
\quad A_x\text{ total and correct on ALL strings},\quad
\ell(A_x)\le c(N+1),\quad T_{A_x}(x)+\ell(A_x)\le C(N+1).
$$

**Proof.** Fix once and for all a complete total correct decider `U_L`. For a chosen x of length n let `b=L(x)`. Embed x and the single bit b in an ordinary self-delimiting program `A_x`: on any input y, compare y to the embedded x; if identical output b; otherwise invoke `U_L(y)`. Program length is `O(n+1)` because the fallback code is constant and x/b are serialized once. On x, comparing the full input with the embedded constant, outputting b and halting take `O(n+1)` ordinary sequential steps; explicitly loading or scanning its own program costs another `O(n+1)`. Every other input, including malformed SAT strings, is decided correctly by the fixed total fallback. The program is a uniform algorithm across all input sizes: it is not a nonuniform circuit family. Its identity, however, depends on x. Taking the minimum separately at every x and then the maximum gives the claimed bound. **The description-generation procedure is not required to be fast:** computing b from x may be arbitrarily expensive. Nothing here supplies a uniform efficient compiler `x -> A_x`. QED.

### Hierarchy witness: genuine separation of the bad invariant from uniform polynomial time (PROVED/EXACT from KNOWN THEOREM)

By the deterministic time hierarchy theorem there exists a decidable language `L_* notin P` (for example, a suitable diagonal language within `DTIME(2^{n^2})` but outside the union of polynomial deterministic time bounds). For that SAME fixed `L_*`,

$$
M_{L_*}(N)=O(N+1),
$$

while for every one fixed total correct uniform A, every exponent k, positive C and cutoff N0, there exists N>=N0 such that

$$
T_A^{wc}(N)>C(N+1)^k.
$$

Otherwise an A with an eventually polynomial worst-case bound would decide `L_*` in P, contradicting the hierarchy theorem. Therefore **a pointwise algorithm minimum can be linear even on an unconditionally superpolynomial-time decidable language**. This is a universal-model counterexample to interpreting an ideal per-input signed-hypergraph/DAG minimization over ALL correct algorithms as real uniform SAT work. It is not a lower bound on SAT: for SAT the identical `M_SAT=O(N)` holds without resolving whether SAT lies in P.

## What is and is not contradicted

1. **F1: Linear description charge alone repairs pointwise model independence. FALSIFIED.** Each `A_x` includes just one input string, one answer bit and one fixed exhaustive fallback. No exponential per-length answer table is needed. This is stronger in its *per-instance description* control than LSPV-1/377's all-prefix table result, but remains the same elementary quantifier problem, not an original hardness theorem.
2. **F2: Requiring each candidate program to be total, correct and uniform across lengths repairs it. FALSIFIED** if the min still occurs inside the max, because `A_x` is indeed an ordinary fixed all-length decider. One A must be fixed before input quantification in the actual B1/B2 bridges.
3. **F3: The patch yields a useful algorithm for SAT. FALSIFIED.** The construction selects the correct bit b in advance, may require a superpolynomial computation to produce it, and is forbidden as an instance-tailored answer axiom in R_mix341. No solver discovering the patch cheaply has been produced. Every real run must charge source/description reads, comparison, program generation if implemented, fallback and all-phase memory.
4. **F4: The hierarchy language gives an SAT complexity lower bound. FALSIFIED.** Hierarchy only supplies one distinct decidable L_* outside P. SAT's fixed-algorithm worst-case status is the open P versus NP problem.

**Bridge quantifiers:** B1 requires `forall A exists p_A forall UNSAT F` with A fixed; B2 requires `forall A exists p_A forall N` with the fixed A's `T_A^wc(N)` on *every binary input*; B3 requires `SAT in P -> Wbar_Rmix341 polynomial` for this very same preselected R. The theorem falsifies none of B1/B2/B3 because it switches between `A_x` *inside* the input maximum and never bounds worst-case time of one A. It also neither proves nor refutes a family-hardness claim in R_mix341.

## Model, accounting, and exact controls

Program description bits O(n), target source reads n, code loading O(n), target comparison O(n), one-bit output O(1), no arbitrary long intermediate required on the matched target. The off-target complete fallback can use exponential time and space. The existential construction's **discovery of b** is unknown and potentially exponentially costly; no optimizer time or circuit-construction cost is hidden in a physical SAT algorithm. In a universal machine with polynomial interpreter overhead, the pointwise bound remains polynomial even if the sharp O(n) is model-dependent. No logical q-node count is converted into T/S.

**COMPUTATIONAL control, not a complexity proof:** one self-contained JavaScript producer and one independent Python verifier tested 16 small strict ASCII-CNF fixtures: SAT 5, UNSAT 4, malformed 7. Exact-match patches were checked against the fixed exhaustive fallback on every cross fixture and 511 binary non-CNF strings. Producer: 1,824 assertions; independent checker: 1,809 assertions. Both verified opposite 3-variable parity equations give UNSAT whereas each parity half is SAT. Strict capped syntax/variable count in these *finite executables* is only a test grammar and does **not** replace the theorem's all-general-CNF `U_SAT`. No random seed, timings or asymptotic inference.

## Prior work and independent audits

Read mandatory full five-role directive `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` (current blob `c3889a3e514ddbd747150dcb68607013a3b2d154`), issue #3 and latest handoffs, root `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`, `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, and `.codex/skills/pnp-research/SKILL.md` blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`. Reviewed LSPV-1/377 `research/agents/lspv-1/2026-11-03_1900_LSPV-1_FINITE_HORIZON_UNIFORMITY_FIREWALL377.md` (blob `b8a9b3ea8b726e6109ff26022fd01483c1165685`), LSPV-5/326 and /327, LSPV-5/330 `research/main/2026-11-03_2248_MAIN_GUARDED-ENTAILMENT-DECISION-SEPARATION-REFEREE330.md` (blob `afc4b5ecf8034322634e1423ad90be12f1f7bd35`), and LSPV-1/381 `research/agents/lspv-1/2026-11-03_2224_LSPV-1_AFFINE_SKETCH_PUBLIC_BANK381.tex` (blob `0713c71e5f097970d18125098578ecafb97ae461`). /377 already established **cutoff-wise exponential lookup** and /327 established generator collapse to P when fully charged. /330 already established **recognized-family patch**. This run isolates a **one-input, linear-description** obstruction and an unconditional hierarchy witness; do not advertise it as a new method to separate P from NP.

**Grok folder located from repository directory listing:** `GROKPROOF/2026-11-04_0615_PROGRESS.md` blob `6603e613853e7cc358b9b0181f06b19fa26ec39c` (timestamp 22:15 PST). Its FLMV analysis does not contain the required all-input charged contraction. **Claude folder located:** `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`, and `2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`. Claude's portfolio collapse and sequential-model crossing-sequence proof do not imply any mixed-calculus B3 or arbitrary-machine SAT bound. Neither assessment overrides the quantifier proof above.

**Literature/search log:** exact queries: `Haken 1985 intractability of resolution pigeonhole exponential lower bound exact`; `Cook Reckhow 1979 relative efficiency propositional proof systems polynomial bounded iff NP coNP`; `Hartmanis Stearns 1965 on computational complexity of algorithms`; `deterministic time hierarchy theorem there exists decidable language not P`; `github.com/openai proof checking SAT verifier lean formal methods`. GitHub repository code searches `pointwise infimum uniform deciders hardcode input`, `per-input patch total decider`, `instance tailored pointwise solver collapse` found /330 and older files; no claim of literature novelty. The OpenAI Lean formalization repository surfaced by web search concerns other mathematics and supplies no missing proof-system transfer. Sources: Haken, TCS 39 (1985), doi:10.1016/0304-3975(85)90144-6; Cook and Reckhow, JSL 44 (1979), doi:10.2307/2273702; Hartmanis and Stearns, Trans. AMS 117 (1965), doi:10.1090/S0002-9947-1965-0170805-7. Relevant source folders were accessible.

**NEXT weakest sufficiency:** Keep a fixed decider *outside* max/min and investigate conditional B3 via length simulation of one decider-induced Cook–Reckhow system into the same R_mix341, without demanding a uniform proof optimizer. For any candidate signed-hypergraph/DAG complexity metric, test its quantifiers against this patch. The remaining bridge and full-mixed superpolynomial worst-case lower bound are **OPEN**.
