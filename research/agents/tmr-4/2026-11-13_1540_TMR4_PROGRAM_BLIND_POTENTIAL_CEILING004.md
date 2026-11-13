# TMR-4/004: machine-blind cost-potential ceiling and independent suffix review

**Date:** 2026-11-13 15:40 PST, America/Los_Angeles. **Role:** NEW TMR-4 Cost-Sound Abstraction. **Status:** New symbolic theorem CANDIDATE pending TMR-5 review; independent review of TMR5-SF2 PROVED/RESTRICTED for the declared-length strict proper 3-CNF grammar; executed tests COMPUTATIONAL. P versus NP OPEN.

## 1. Target and precise machine model

The sought result concerns one fixed finite total deterministic multitape 3-SAT decider $A$ serving every binary input length. Count every physical transition, the read-only source and head positions, finite control and program, all writable tape contents/heads, all visited writable cells, temporary encodings, indices, source rereads, preprocessing, sharing, fallback and recomputation. Let $L=|x|$ be encoded input bits, distinct from variable/clause counts. Malformed sources must be rejected; both valid SAT and UNSAT labels must be correct.

The actual separation obligation is
$$
\forall A\;\forall k\in\mathbb N_{\ge1}\;\forall C>0\;\forall L_0\;
\exists x\in\mathrm{VALID3CNF}:
|x|\ge L_0\quad\text{and}\quad T_A(x)>C(|x|+1)^k.
$$
The new theorem does not establish this obligation. It pinpoints a fatal restriction on **program-blind, input-common abstract initial states**. TMR-1/001 already warned about minimizing over different hardcoded machines; our incremental result formulates a cost-sound-abstract-graph no-go that is not restricted to observation-only graph geometry.

## 2. New theorem TMR4-PB4 (CANDIDATE pending independent review)

Fix any valid binary input $x$ with true SAT/UNSAT label $\ell(x)$ and length $L$. Suppose a single nonnegative-cost abstract MAY graph $G_x$ has an initial state $s_x$ **independent of which correct decider is selected**, with the following exact contracts for **every** eligible correct total deterministic decider $A$:

1. Initial binding relates the concrete initial full configuration $c^0_{A,x}$ to that very same abstract start $s_x$. The concrete relation accounts for fixed program/control, original input/head and all work tapes, even if the abstraction forgets some components.
2. Every related concrete state and **EVERY** legal concrete unit step $c\to c'$ has a **finite abstract path** reaching a related successor of total abstract edge cost no greater than the concrete cost 1. All real executions are included. Stuttering, zero-cost edges, sharing and arbitrary memory behaviors are permitted, with conservative MAY overapproximation.
3. Every correct actual SAT or UNSAT terminal is related to a corresponding label-preserving abstract goal. Every such goal has $\Phi_x\le0$.
4. On **EVERY** abstract edge $a\xrightarrow{w}b$, including zero-cost and spurious MAY edges, a candidate potential obeys
   $$
   \Phi_x(a)\le w+\Phi_x(b).
   $$

**Theorem.** For every valid $x$ these premises force
$$
\boxed{\Phi_x(s_x)\le L+1}
$$
under the standard model with one transition per input-symbol scan, or $L+O(1)$ for an equivalent fixed endmarker/output convention. This precludes a superlinear pointwise abstract lower bound on that graph, even when its internal states model arbitrary computation rather than merely original input observations.

**Proof.** For each **particular** fixed $x$, construct a different machine $B_x$. Hardwire the $L$ source symbols and the mathematically correct one-bit label $\ell(x)$ into a finite chain of $L+O(1)$ control states. The read-only original head compares input symbols sequentially against the chain. An exact $L$-symbol match plus right endmarker causes an immediate halt with the hardwired correct label. At any mismatch, truncated source or extra input, the machine rewinds its real input head with paid moves and invokes one fixed exhaustive total correct SAT parser and solver. Thus $B_x$ is a **single fixed total correct program across all lengths**, and on its designated input it needs only $L$ symbol reads, one endmarker check and a constant halt overhead. No SAT oracle is invoked in execution on $x$. The precomputed label is one finite constant in that *particular program*, not nonuniform advice to a prospective all-input polynomial algorithm.

Apply the premise to the actual $B_x(x)$ execution, concatenate the abstract path for every concrete step, and telescope the potential inequalities through all abstract edges. Initial and both-label terminal binding yield
$$
\Phi_x(s_x)\le d_{G_x}(s_x,\mathrm{goal}_{\ell(x)})
\le T_{B_x}(x)\le L+1.
$$
This is a real cheap concrete execution, **not** a replay-proved spurious path, and deleting it would violate the all-machine MAY contract.

**Coverage firewall.** The theorem does **not** apply when the graph or start is program-dependent, for example when it preserves a program tag, complete finite control or other machine-specific state: then $s_{A,x}$ and $s_{B_x,x}$ need not coincide. A richer program-dependent abstraction might prove strong bounds for the same fixed $A$ on some $x=x(A,k,C,L_0)$; that missing implication remains OPEN. The construction $x\mapsto B_x$ is not a single uniform SAT algorithm and does not disprove P != NP.

**Comparison to prior results.** TMR-4/001 and TMR-5/001 proved the optimal first-observation-only potential is the input-difference hitting-set number $\tau(D)\le L$. TMR4-PB4 has a broader MAY graph but a stronger shared-start hypothesis. Its $L+1$ ceiling comes from a genuine correct machine rather than a graph-invented abstract read shortcut. The older TMR-1/001 hardcoding warning is explicitly credited.

## 3. Independent second review of TMR5-SF2

**Verdict: PROVED/RESTRICTED at the exact declared-length source and sequential-input-head scope.** I independently reconstructed TMR-5/002's logarithmic-suffix speculative wrapper.

For the strict-proper signed binary grammar with two unary headers $1^N0\,1^M0$ and $w=\max(1,\lceil\log_2N\rceil)$ identifier bits, a valid input has declared length
$$
K=N+M+2+3M(1+w).
$$
Before reading the final source bits, a physical source head reads the header, computes $K$, and then copies only the first $K-m(K)$ source bits, where
$$
m(K)=\min(\lfloor\log_2K\rfloor,\ K-(N+M+2)-1).
$$
Thus $m(K)\ge1$, $m(K)=O(\log K)$ and $2^{m(K)}\le K$. Keeping the original head parked, the fixed wrapper performs **paid** virtual simulations on all $2^{m(K)}$ possible suffix completions. It validates each completion and invokes the fixed total correct solver only on valid candidates; this qualification matters if the original solver has a polynomial bound only on valid inputs. It stores all labels on a paid table.

The wrapper then reads the first $m(K)-1$ actual suffix bits, spends paid time locating the two remaining possible output labels, and caches that pair in finite control *before* reading the last real bit. It finally reads that bit, checks the right endmarker and halts with the correct cached answer within $O(1)$ additional transitions on every valid source. The fixed program works over all lengths; invalid/overlong inputs take a paid total fallback. The number of completions is polynomial, and full simulation overhead is polynomial **conditional on a polynomial general SAT algorithm already existing**, not an unconditional SAT algorithm. Speculative work may otherwise take exponential total time.

Hostile controls addressed: header length known before unread suffix, opposite-label last-bit siblings, parser handling of malformed virtual completions, a physically stationary real input head during simulation, fully charged lookup before the final real bit and a physical right-endmarker check. The independent finite emulator tested these semantics but did **not** execute a physical Turing machine. This review confirms only the temporal-order falsification: expensive SAT consistency work cannot be required to occur specifically **after** all original input bits are first observed. It says nothing about unavoidable **whole-trace** cost.

## 4. Executed reproducible controls

**Published/executed source:** experiments/tmr/tmr4_program_blind_ceiling004.cjs (Git blob 0fad5f8df5ef596ca36665a55b88430c4792cba8). **Published exact V8 raw:** results/raw/tmr/2026-11-13_1540_TMR4_PROGRAM_BLIND_CEILING004_RAW.json (Git blob 796d17c507c1bdb14399253f933ccf438d2a0f4f). Both were fetched back and compared byte-for-byte with the executed source and generated raw data.

Deterministic seed 20261113: 45 valid strict-proper 3-CNF examples, 45 exactly matched hardwired fast paths, 180 probe/fallback comparisons (some deliberately identical to a source), 3,888 edge/potential checks, 45 deliberate zero-cost-to-goal inequality falsifiers, 1,976 paid virtual suffix completion classifications, 47 suffix lookup checks, and two valid 14-variable/17-clause opposite-label 288-bit siblings differing only at their last encoded bit. All assertions passed. The graph test was a deliberately small MAY model, and the fast-path finite-state chain was represented symbolically. These checks are **COMPUTATIONAL**, not a physical-machine proof.

An independent local-only Python implementation was also executed with a 25-second timeout: 60 valid sources, 60 fast-path matches, 240 probes, 5,436 inequalities, 2,504 virtual completions and 62 suffix checks passed. Its files are only in the working container at /mnt/data/tmr4/tmr4_program_blind_ceiling004.py and /mnt/data/tmr4/2026-11-13_1540_TMR4_PROGRAM_BLIND_CEILING004_RAW.json, **not** in GitHub. No operating-system Node CLI, physical TM simulator, repository preflight or LaTeX compilation was run.

The theorem's machine class permits Horn, 2-SAT, GF(2)/Tseitin, bounded treewidth, products, renaming, padding, auxiliary variables, compact circuits, caching, arbitrary source rereading, sharing and recomputation. These are not presumed expensive operations; TMR-2/004 provides an explicit cheap affine/high-treewidth counterexample. The finite audit does **not** separately benchmark every listed algorithmic subclass.

## 5. Corpus, citations, status and next target

Read **first** the current 2026-11-13 12:49 PST five-TMR directive, then root proof1.txt (full 28,714 characters, SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), root proof2.txt recovered in full by authenticated blob 930c5eeddafce656717f28055a7a9a755f44737c (1,051,196 characters), and root main.tex recovered in full by blob 7938c144d3538b08e23531b1fa22d2400f3491bb (2,487,713 characters). Also read newest issue #3 comments, AGENTS.md, CODEX.md, pnp-research skill, five current TMR handoffs, original TMR-4/001 and /003, TMR-5/002, TMR-2/004 and historical original accepted-path/normalizer counterexamples LSPV-5/510 and /511. Older checker paths remain genuine; no checker reinterpretation or deletion was attempted. The older LSPV identities/ownership directives are superseded.

Primary literature inspected: [1] Cousot and Cousot, *Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints*, POPL 1977, pp. 238-252, https://doi.org/10.1145/512950.512973 . [2] Hoffmann et al., *Two Decades of Automatic Amortized Resource Analysis*, Mathematical Structures in Computer Science (2022), https://www.cambridge.org/core/journals/mathematical-structures-in-computer-science/article/two-decades-of-automatic-amortized-resource-analysis/9A47A8663CD8A7147E2F17865C368094 . These references provide background on sound abstract executions and cost potentials, **not** the new project theorem; its proof is self-contained above.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither proof1.txt nor proof2.txt requires a claim-status promotion: all original unrestricted separation arrows remain OPEN. TMR-4 edits only its authorized main.tex specialist region, if safely reconciled, never TMR-5's synthesis text. No automation, role or schedule modifications.

**Next target:** construct or falsify a *program-dependent* and nevertheless uniformly valid $\forall A$ cost-sound MAY abstraction of **whole-trace** global-consistency processing, with a noncircular initial potential that survives speculative completion, cheap recognizable subfamilies and arbitrary polynomial workspace. A polynomial all-input general SAT solver remains a legitimate opposite endpoint.

END_OF_REPORT::TMR4-PB4::2026-11-13_1540_PST
