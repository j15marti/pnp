# TMR-3/029: Two-way input header recovery and uniform machine-network serialization

**Pacific timestamp:** 2026-11-14 14:55 PST (America/Los_Angeles). **Role:** TMR-3 Time-Space Tradeoffs. **Proof status:** TWOREWIND32 PROVED/RESTRICTED symbolic access-model transfer, peer review OPEN; NETWORK32 PROVED/RESTRICTED elementary uniform-network simulation, peer review OPEN; source/head tests COMPUTATIONAL. No unrestricted P versus NP proof. 

## 1. What is genuinely new

TMR-3/028 gave a low-space, growing-threshold **annotated** one-work-tape streaming MCSP algorithm, assuming a self-delimiting arity header before the truth table. This run proves a charged conversion to **header-free two-way read-only input**, retaining a *single* work tape and the same asymptotic time/space exponents. It carefully does NOT transfer to the one-way input model in the CHMY magnification hypothesis. The distinct second result explicitly serializes the user's model of polynomially many communicating single-tape machines, including uniform construction and message handling, and identifies the polynomial-versus-superpolynomial machine-count/elapsed-time dichotomy as an equivalent reformulation of P versus NP, not a new lower bound.

The new positive upper bound is **model specific**, not a proof of a lower bound. The new negative resource finding is that an ordinary quadratic network-to-one-tape serial simulation does not carry CHMY's high-threshold $N^{1.99}$ lower bound through to a useful network elapsed-time bound. A nonuniform per-length hardcoded network is a concrete falsifier if uniform construction is omitted.

## 2. Source ledger: original files and guarded statuses

| Original evidence | Relation and scope |
| --- | --- |
| research/agents/tmr-3/2026-11-14_1327_TMR3_MCSP_RAWSCAN_HEADER_BOUND028.md; experiments/tmr/tmr3_rawscan031.py; results/raw/tmr/2026-11-14_1327_TMR3_RAWSCAN031_RAW.json | PRIOR ANNO28 and RAWSCAN28 symbolic MCSP upper bounds; executed Python head-rotation proxies but not a compiled full TM. This run makes the annotated-to-two-way-input bridge explicit. |
| research/agents/tmr-1/2026-11-14_1357_TMR1_CAPMIN_REDUCTION_FRONTIER028.md; experiments/tmr/tmr1_capmin031.py and its original raw JSON | PRIOR exact capped gate minimization for slow thresholds; one-head compiler pending peer audit. |
| research/agents/tmr-2/2026-11-14_1417_TMR2_SHARED_ORACLE_PREPROCESS032.md and its original runner/raw | PRIOR sharp *source-independent evaluation-oracle* shared-query bound. Not a general SAT or machine-time bound. |
| research/agents/tmr-4/2026-11-14_1439_TMR4_POSITIVE_POWER_COMPILER_FIREWALL030.md and original runner/raw | PRIOR direct SAT-mask compiler collapse at positive-power MCSP threshold. |
| research/agents/tmr-5/2026-11-14_1452_TMR5_DUMMY_PADDING_UNIVERSAL_COLLAPSE026.md and original runner/raw | PRIOR exact dummy-input circuit-size invariance, not a separation. |
| research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex; 2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex; 2026-10-28_1326_CLAUDE_TPORT-0001.tex | Historical one-tape, portfolio and access-model limitations, not an unrestricted SAT transfer. |
| research/agents/threshold-descent/2026-10-18_1416_THRES_HASHBRIDGE4.tex; TMR-4 Walsh/moment and TMR-5 compact-summary falsifiers; GROKPROOF/2026-11-13_0526_PROGRESS.md | Historical failed algebraic/summary and selected-representation routes must be preserved; not a source of compulsory storage/time. |

Read first the Nov 14 MCSP directive on main (blob 1e11aa64a0b0d635a65cea58500b09f2b0fe010a), then Nov 13 TMR role replacement, root AGENTS.md/CODEX.md/pnp skill, latest five handoffs and issue #3 through TMR-5/026. The authentic full root proof1.txt, proof2.txt and main.tex were fetched as Git blobs, sizes 28,714, 1,051,196 and 2,545,859 characters respectively. Current root proof status stays OPEN. No root edits or task changes.

## 3. Primary-source theorem/machine matrix

| Original theorem and page | Exact hypothesis, size and conclusion |
| --- | --- |
| Cheraghchi, Hirahara, Myrisiotis, Yoshida, STACS 2021, Theorem 1, printed p.23:3 [1] | *Ordinary decision* MCSP[$2^{\mu_1 n}$] on a complete $N=2^n$-bit table. A fixed small $\mu_1>0$ exists such that deterministic nonmembership in $\mathrm{DTIME}_1[N^{1.01}]$ on a **one-way read-only input and exactly one two-way read/write work tape** implies $P\ne NP$. The specific low-$\mu_1$ premise is OPEN. |
| Same, Theorem 2, printed p.23:3 [1] | For some different larger $\mu_2$ (close to 1 in authors' explanation), ordinary MCSP[$2^{\mu_2 n}$] is outside bounded-two-sided-error $\mathrm{BPTIME}_1[N^{1.99}]$ in the **same source/work-tape arrangement**. This cannot be substituted for Theorem 1's threshold. |
| Same, Theorem 3, printed p.23:4 [1] | For $1/2<\mu<1$, even short-oracle-query randomized one-work-tape algorithms face a restricted $N^{1+\mu'}$-type lower bound. This is an access-model result and not an unrestricted 3-SAT decider lower bound. |
| McKay, Murray, Williams, STOC 2019, Theorem 1.2, printed p.2 [2] | One-pass **search** MCSP with $A$-oracle circuits and time-constructible $s(n)\ge n$, $\Sigma_3SAT^A$ oracle queries, $\widetilde O(s(n))$ workspace and $\widetilde O(s(n)^2)$ update time. Ordinary exact decision without those oracles is different. |
| Same, Theorem 1.3, printed p.2 [2] | For some $A\in PH$ and time-constructible $s(n)\ge n$, *absence* of every suitable $\operatorname{poly}(s)$ space/update deterministic one-pass **search** streamer implies $P\ne NP$. The present slow gate threshold $s_\kappa(n)=\Theta(n/\log n)$ is eventually smaller than $n$, so it cannot simply be inserted into the theorem. |

No theorem here treats a polynomial-output, syntax-aware SAT-to-positive-power-MCSP reduction as proved. No MKTP, Gap-MCSP, partial-function or succinct-table theorem is silently imported. SAT encoding length $L$ is distinct from truth-table length $N=2^n$.

## 4. New restricted theorem TWOREWIND32: charged header elimination with two-way source

Define the bare language
$$
B_s=\{x\in\{0,1\}^{2^n}:CC_n(x)\le s(n)\},\quad n\ge1,
$$
and the *different* annotated language
$$
H_s=\{\gamma(n+1)x:|x|=2^n,\ CC_n(x)\le s(n)\},
$$
where $\gamma$ is a self-delimiting Elias-gamma code. Malformed lengths are NO in both languages. Let $A$ be any fixed finite total deterministic **one-way-read-only input plus one two-way work tape** decider for $H_s$, taking at most $T_H(N)$ time and $S_H(N)$ visited writable work cells on correctly annotated $N$-bit tables.

**Claim.** A fixed finite total deterministic machine $B$ with a **two-way** read-only input and exactly **one** two-way work tape decides $B_s$ with
$$
T_B(N)=O\bigl(N\log(N+2)+(T_H(N)+1)\log(N+2)+\operatorname{polylog}(N+2)\bigr),
\qquad
S_B(N)\le S_H(N)+O(\log(N+2)).
$$
Hidden constants may depend on the fixed simulator, $A$, the alphabet and encoding, not the input table. Input-head movements, length counter operations, synthetic-header accesses and work-head shuttling are included.

**Proof.** On the first physical input pass, copy no source bits: increment a binary length counter on the one work tape while the **two-way read-only input** head advances right until EOF, at $O(\log(N+2))$ work-head moves/bit. Reject unless the length is a positive power of two with $n\ge1$. Retain $n$ (using $O(\log N)$ cells), rewind the physical input head to its first bit at cost $N$ moves. Form $\gamma(n+1)$ in a work-tape auxiliary block. Simulate the fixed guest $A$ with an *imaginary* initial input head reading that synthetic header; keep the real input head parked at the left end. The guest cannot move its one-way head backwards. When it first advances beyond the header, redirect that head to the real source and thereafter simulate its right moves in lockstep. Stationary virtual input symbols can be retained in finite control, and each change of a synthetic-header cell can be serviced by walking the single work head to/from the auxiliary block. There are only $O(\log n)$ such header advances; each shuttle spans at most $S_H+O(\log N)$ visited cells and $S_H=O(T_H+1)$ on the same machine. Thus header-access overhead is bounded by $O((T_H+1)\log(N+2))$ without assuming two work tapes. All actual guest tape steps are preserved with a constant-factor finite-alphabet translation, and both terminal labels are preserved. The auxiliary header/counter takes $O(\log N)$ extra cells. The construction and malformed-input rejection are uniform for all lengths. QED.

**Corollary, input-model-sensitive.** Apply TWOREWIND32 to TMR-3/028's annotated candidate-list machine with
$$
D(n,s)=(s+1)(n+s+2)[3(n+s+2)^2]^s,\quad
T_H=N D(n,s)\operatorname{poly}(n+s),\quad S_H=D(n,s)\operatorname{poly}(n+s).
$$
For a fixed rational $0<\kappa<0.005$ and
$$
s_\kappa(n)=\left\lfloor \frac{\kappa n}{\lceil\log_2(n+1)\rceil}\right\rfloor,
$$
the unannotated **two-way-input** algorithm has
$$
T_B(N)=N^{1+2\kappa+o(1)},\qquad S_B(N)=N^{2\kappa+o(1)}.
$$
The missing ingredient to apply this to CHMY Theorem 1 is **both** (i) a one-way source, with no rewind, and (ii) the far larger fixed-positive-power circuit threshold $s=N^{\mu_1}$. Replacing the source interface or threshold without proof is invalid. The symbolic ANNO28 physical candidate update remains subject to independent finite-state compiler review.

## 5. New restricted theorem NETWORK32: exactly what a polynomial machine network buys

**Declared model.** For each source length $L$, a fixed uniform deterministic constructor (with one-work-tape execution time $C(L)$) emits a network description of $B(L)$ bits with at most $p(L)$ processors. Each processor is a local finite-alphabet one-tape deterministic machine whose program, heads and initial contents are specified in the generated description. Global execution proceeds in at most $t(L)$ synchronous rounds, with each processor taking at most one charged local step per round, one constant-size symbol per interface transfer, and explicit bounded-fanout receiving/reading operations. Every input access, local output read, queue action, global switching and final output must be represented by such an event. A round's message delivery is not a zero-cost broadcast of unbounded contents. The correct network returns the 3-SAT bit on **every** valid $L$-bit encoding.

Let $E(L)\le O(p(L)t(L))$ be total charged local/interface events. In a conservative literal serialized format, the complete input copy, emitted program/graph descriptions, virtual head markers, local work/output tape cells, and message records occupy
$$
M(L)=O\bigl(L+B(L)+(E(L)+p(L)+1)\log(L+B(L)+E(L)+p(L)+2)\bigr)
$$
fixed-alphabet cells. A deterministic one-way-source plus one-work-tape simulator copies all $L$ source bits once, executes the uniform constructor, then simulates each local/interface event by traversing the serialized records. Seeking a virtual head, reading an input coordinate, executing a program rule, shifting a virtual tape boundary, reading a previous output, and updating a queue can each be implemented in $O(M)$ physical steps. Consequently
$$
T_{\mathrm{serial}}(L)\le O(C(L)+L+(E(L)+1)M(L)),
\qquad S_{\mathrm{serial}}(L)=O(M(L)).
$$
This is a safe worst-case bound, not an optimized simulation. It explicitly charges nonconstant-width addresses by bit representation and permits rereads, sharing, caching and recomputation. If $B,C,p,t$ are polynomially bounded in $L$, the **same fixed** serial simulator runs in polynomial $L$ time. No oracle or nonuniform per-length advice appears.

**Equivalence consequence (not a new complexity separation):**
$$
P=NP\quad\Longleftrightarrow\quad
\text{there exists such a uniform 3-SAT network with polynomial }B,C,p,t.
$$
The reverse arrow uses the simulation above. The forward arrow uses a single polynomial-time 3-SAT program, compiled to one work tape at polynomial overhead after copying its read-only source. Thus the proposal that *every* correct uniform network requires either superpolynomially many processors or non-polynomially bounded elapsed time is, in this model, a **restatement of $P\ne NP$**, not a new resource lower bound.

**Nonuniform falsifier and exact repair.** Without the uniform program/constructor charge, for each $L$ a separate one-processor finite-state machine can encode the answers for all $2^L$ source strings in a binary trie of $O(2^L)$ distinct control states. It reads $L$ bits and outputs the correct 3-SAT label in $O(L)$ time with $O(1)$ visited work cells. So per-length polynomial processor count and polynomial elapsed time say nothing when the program description or constructor is uncharged. Fixing one program and charging $B,C$ eliminates this countermodel.

**Quantitative magnification firewall.** In the high-threshold ordinary MCSP setting, CHMY's Theorem 2 says no randomized one-work-tape solver exists within $N^{1.99}$ at its particular $\mu_2$. An $E=\Theta(N)$-event network with $B=O(N)$ has a generic serial bound as large as $N^{2+o(1)}$, which does **not** meet the excluded $N^{1.99}$ regime. Hence that one-work-tape lower bound plus ordinary serialization does **not** force a superlinear $E$ bound. A substantially sharper faithful transfer or direct network proof is still required. In particular, a lower bound on this chosen serialization's transport overhead is not a logical MCSP hardness lower bound. Neither theorem here implies $P\ne NP$.

## 6. Finite executed controls and epistemic limits

**Actually executed hosted V8** on the exact JavaScript source published at experiments/tmr/tmr3_twoway_header032.js. Its exact raw JSON is at results/raw/tmr/2026-11-14_1455_TMR3_TWOWAY_BRIDGE032_RAW.json. It completed **4,715 assertions, zero failures**. Tests included 828 exhaustive truth-table/threshold classifications (n=1,2,3; gate budget 0,1,2), two independent semantic paths (candidate-set membership versus annotated and rewound streaming flags), explicit **19,242 source-head moves**, **23,532 charged binary-counter proxy operations**, **245,168 candidate record/bit comparisons**, 22 malformed-length controls, and 272 charged small-network parity controls (5,040 network local event proxies). Circuit semantics are evaluated as finite V8 bit masks; the source head is a counted integer cursor, **not a native finite-state Turing-machine executor**. NETWORK32 is a symbolic theorem, not empirically established by the toy parity network. No unexecuted suite is claimed as run.

Hostile controls retained: Horn/2-SAT and XOR/Tseitin/GF(2) admit compact algebraic or implication-graph summaries; padding and auxiliary variables can collapse MCSP thresholds; source rewind can remove annotated-input limitations; full-output transduction storage bounds do not automatically bind one-bit decision. No purported bound on every general SAT algorithm is derived.

## 7. Exact remaining gap and next peer request

**OPEN:** ordinary MCSP[$N^{\mu_1}$] outside deterministic $N^{1.01}$ time for the particular **small** $\mu_1$ in CHMY Theorem 1, on one-way input plus one work tape. Also OPEN: any fully charged transfer from unrestricted fixed uniform multitape SAT deciders or arbitrary deterministic machine networks to that hypothesis. Neither the above two-way low-space upper bound nor ordinary network serialization closes either gap.

**Next target:** find or falsify a one-way, header-free, genuinely growing-threshold inherited candidate state representation which does not retain all $N$ input bits, and obtain an explicit model-preserving subquadratic network-to-one-tape simulation if trying to exploit the known large-$\mu_2$ bound. TMR-1 is requested to audit two-way/header and fixed-program quantifiers; TMR-2 the source/continuation barrier; TMR-4 the all-event message/tape mapping; TMR-5 the exact crossing head and resource exponents. No root main.tex or proof tracker promotion with the load-bearing arrow OPEN.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt/proof2.txt and canonical main.tex preserved under TMR-5 ownership; no scheduler/task modifications.

### Original references

[1] Cheraghchi, Hirahara, Myrisiotis, Yoshida. *One-Tape Turing Machine and Branching Program Lower Bounds for MCSP*. STACS 2021, Theorems 1–3, printed pp.23:3–23:4. https://doi.org/10.4230/LIPIcs.STACS.2021.23

[2] McKay, Murray, Williams. *Weak Lower Bounds on Resource-Bounded Compression Imply Strong Separations of Complexity Classes*. STOC 2019, Theorems 1.2–1.3, printed p.2, author's original PDF https://people.csail.mit.edu/rrw/MCSP-MKTP-stoc19.pdf

[3] Earlier network/one-tape manuscript in repository: research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (restricted prior work, not a primary hardness magnification result).
