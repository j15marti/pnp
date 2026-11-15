# TMR-5/042: Exact all-length two-step uniformity penalty, with one total hardwired witness

**2026-11-15 06:54 PST (America/Los_Angeles) | TMR-5 PNP Machine Bottleneck Redteam | EXCEPTION112**

**Scientific status:** **PROVED/RESTRICTED** for the precisely qualified unary ordered-record physical service, independent mathematical peer review **OPEN**. Executed finite V8 traces **COMPUTATIONAL**. Same-system SAT transfer and superpolynomial initial obstruction **OPEN**. **P versus NP OPEN.**

## 1. Preselected target and falsifiers

**Claim to attack:** TMR-3/045 and TMR-4/046 showed that a single uniform program attaining the geometric minimum $T_A(k)=2k$ at one length cannot attain it at a second length, and proved an adjacent-length $T_A(k+1)\ge 2k+4$ cliff. Determine whether the apparent one-exception phenomenon admits an **exact bound at every other length** and an equally concrete one-program upper witness.

Three preselected falsifiers:

1. A legitimate local-head program can use a different W-head trajectory on another unary length **before** its first differing source symbol is scanned.
2. The TMR-4/046 phase-head potential loses cost soundness under real gate rewriting, input rereading, extra scratch, simultaneous output, or the first-gate / activation boundary.
3. A claimed all-length witness uses unpriced cleanup, input-length advice to one changing program, one-tape multiwrite, a missing AND gate, an early marker, or fused HALT.

The new result excludes these within the declared ordered unary service. A weaker **extensional** output goal remains a genuine cheap countercontrol and is not ruled out.

## 2. Current sources and provenance

Read **FIRST** the approved 2026-11-14 fusion-Lipschitz directive (blob `54c9177fc211dfca6c94d89d6ebbf3f3908809d6`), followed by the 2026-11-13 TMR replacement. Read both full root proof trackers: `proof1.txt`, SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`, 28,714 chars; `proof2.txt` recovered directly from authentic Git blob `930c5eeddafce656717f28055a7a9a755f44737c`, 1,051,196 chars. Recovered root `main.tex` by complete Git blob `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34`, 2,545,859 chars. Blank Contents API responses were never treated as empty source files.

Also reviewed issue #3 including TMR-3/045 and newly merged TMR-4/046 updates, `AGENTS.md`, `CODEX.md`, the repository `pnp-research` skill, full current five TMR handoffs, original TMR-3/044 and /045, TMR-4/045 and /046, TMR-5/041, TMR-1/045, TMR-2/045 and their available code / typed tariff evidence, plus October LEAD-0029 Lipschitz audit. Read back current source and rule definition rather than inheriting a chat result as proof. 

Contextual primary references, **not claimed to prove this new elementary result**: Hartmanis and Stearns (1965), *On the Computational Complexity of Algorithms*, DOI [10.1090/S0002-9947-1965-0170805-7](https://doi.org/10.1090/S0002-9947-1965-0170805-7); Hennie and Stearns (1966), *Two-Tape Simulation of Multitape Turing Machines*, DOI [10.1145/321356.321362](https://doi.org/10.1145/321356.321362). Both concern real local-tape machine computation and quantitative model dependence.

**Novelty boundary:** The pointwise $2n$ lower bound, one uniform $2n+1$ upper bound, and adjacent-length $2k+4$ cliff are prior TMR-3/044, TMR-5/041 and TMR-4/046 results. **New in this report** is the sharp **all lengths** theorem and a *single* fixed finite-control $B_k$ simultaneously achieving both the selected-length optimum and the exact lower bound for **every** other unary length.

## 3. Exact same physical service

Fix $m\ge1$ output-marker tapes once. The immutable original unary source is $1^n\#$, $n\ge2$, under one initially-left, unit-local, read-only input head. Exactly one ordinary work-tape W head starts at cell zero; W is initially blank. Each of the $m$ separate marker tapes has one head. Every physical transition reads currently scanned symbols, changes at most one scanned cell **on each distinct tape**, moves each head at most one cell, and costs **one** regardless of legitimate simultaneous work. Finite control and finite alphabets are fixed across all $n$. A program may use other scratch tapes and full charged computation; these cannot teleport W. There are no authentic zero-cost physical steps.

The *ordered* goal requires an initial actual W[0]=0, each separate paid W[j]=g for $1\le j<n$, then a genuinely **later nonterminal** W[0]:0-to-1 activation, all $m$ separately identified marker tape cells O_i[0]=@, genuine inspection of source #, and a **distinct later HALT**. Completed obligations are conjunctive. Paid W identities are counted once. This is an ordered materialization task, **not 3-SAT decision** and not TMR-4/045's weaker extensional service.

For a uniform eligible A, write $T_A(n)$ for the number of complete genuine physical steps until goal on $1^n\#$.

## 4. Independent replication of the all-step tariff

Use the entire actual configuration with ghost observation-history phase $\sigma\in\{0,1,2,3\}$: 0 before the first authentic last gate W[n-1]=g, 1 afterward but before the later authentic activation, 2 afterward but before distinct HALT, 3 after HALT. Ghost flags do not supply the program advice.

With actual W head position $z$, define

$$
q_n(C)=\begin{cases}|z-(n-1)|+1,&\sigma=0,\\0,&\sigma\ge1,\end{cases}\qquad
r_n(C)=\begin{cases}
n,&\sigma=0,\\
|z|+2,&\sigma=1,\\
1,&\sigma=2,\\
0,&\sigma=3.
\end{cases}
$$

The reduced product $p=(0,0,0,0,q_n,0,r_n)$ has $p(C_0)=(0,0,0,0,n,0,n)$ and $p(GOAL)=0$. This report independently checks the full local proof: while phase 0 persists, local head motion decreases $q$ by at most one and does not affect $r$; a first last-g write can only occur with W scanning $n-1$, drops $q$ by one and changes $r$ by 0, +1, or +2 depending on its head movement; during phase 1 return motion decreases $r$ by at most one; authentic activation and distinct HALT each decrease $r$ by at most one. Any irrelevant paid work or external head move does not increase discharge. Free reversible VIEW aliases leave both components fixed. Thus for **every legal step**, $\Delta q+\Delta r\le1$. No MAY alternative from this physical interface is deleted.

The exact active nonnegative tariff cone is $0\le\lambda_\Gamma\le1$ and $0\le\lambda_{\rm machine}\le1$; other active-coordinate discharges are identically zero. The rational vector

$$
\boxed{\lambda=(0,0,0,0,1,0,1)}
$$

gives $\Phi=q+r$, initial $2n$, terminal 0. Necessary unit-charge PRE_TOWARD and POST_TOWARD events and an authentic selected-length $2n$ path establish the exact restricted primal/dual optimum $2n$. The **complete typed matrix** (including away, stay, phase jumps, zero-view and signed negative rows), plus the independent observed rows, is in `results/raw/tmr/2026-11-15_0654_TMR5_EXCEPTION112_TARIFF_MATRIX.json`.

## 5. New theorem: precise cost at every nonselected length

**THEOREM TMR5-042(A), PROVED/RESTRICTED; independent peer review OPEN.** For every one fixed deterministic eligible machine A, and every $k\ge2$,

$$
\boxed{
T_A(k)=2k\quad\Longrightarrow\quad
\forall n\ge2,\ n\ne k:\ T_A(n)\ge2n+2.}
$$

**Proof.** Equality on length k saturates every W-head distance, mandatory last-g-write, activation and separate-HALT inequality. Hence for its first k-1 steps W moves one cell right on *every* step, the W[n-1] event at step k (with n=k) moves it left, and after step k its W head lies at $k-2$.

For any **shorter** $2\le n<k$, the initial n steps are identical between sources $1^n\#$ and $1^k\#$: an initially-left, unit-local original head cannot scan input position n before step n+1. The W head therefore lies at $z=n$ after n steps on the shorter source. It cannot have activated W[0] after the last gate while this forced outward trajectory is still in progress. If the authentic last-g history phase is 0, its residual potential is $q+r=(|n-(n-1)|+1)+n=n+2$. If that phase is 1, its residual potential is $q+r=|n|+2=n+2$. Telescoping from this genuine reached state gives $T_A(n)\ge n+(n+2)=2n+2$.

For any **longer** $n>k$, the first k physical steps are identical on the two sources, because both input heads see only 1s before step k+1. Hence after step k its W head is $z=k-2$. On source $1^n\#$ the last gate W[n-1] cannot have been reached yet (its index is at least k), so its history phase remains 0. Thus

$$
\Phi(C_k)=|k-2-(n-1)|+1+n
=n-k+2+n=2n-k+2.
$$

The universal all-step tariff implies $T_A(n)\ge k+\Phi(C_k)=2n+2$. This handles all n, not only the neighboring input k+1. QED.

**Important quantifier:** There is at most **one** k with $T_A(k)=2k$ for a fixed A, but the theorem does **not** assert that every uniform program has an off-length penalty two. The particular fixed uniform TMR-5/041 machine has $T(n)=2n+1$ on every n, never attains 2n, and is a genuine counterexample to that stronger claim.

## 6. One fixed length-k program attains the lower bound at ALL lengths

**THEOREM TMR5-042(B), PROVED/RESTRICTED; independent peer review OPEN.** For each fixed integer k>=2, there is a single fixed deterministic finite-control program $B_k$ correct on **every** promised $1^n\#$, with

$$
\boxed{
T_{B_k}(n)=\begin{cases}
2k,&n=k,\\
2n+2,&n\ne k.
\end{cases}}
$$

**Construction.** Hardwire k into O(k) finite control states once, not as changing per-input advice. Start by reading source 1s, writing W[0]=0 on the first step and one different W[j]=g on each subsequent step, simultaneously moving both input and W heads right. At its kth original 1, write W[k-1]=g and **speculatively reverse W left** in that same paid step. All markers remain unwritten.

* If source # arrives **before** the kth 1 (n<k), it is first read on step n+1 with W head at n; move W left on that step, continue the physical return to zero, activate W[0] and m separate marker cells nonterminally, then HALT. There are n forward steps, n return steps, ACT and HALT: **2n+2**.
* If source # arrives **exactly after** the kth 1 (n=k), the speculative reversal was correct: the kth step writes the last gate and reverses, another k-2 return moves bring W to zero, with # inspected during this return (at k=2, source # is read simultaneously with W0 activation). ACT and later HALT complete in **2k**.
* If the next source symbol is **another** 1 (n>k), the first mismatch step moves W right and the second alignment step moves it right again. Thereafter the input head streams to genuine # while W follows two cells behind, writing each previously blank gate once. On the first real # read, W is at n-2: advance it right, optionally writing that penultimate gate if blank. On the *next* paid step write W[n-1]=g and reverse W left. The final gate is written on step n+2, followed by n-2 return moves, ACT and separate HALT: **2n+2**. The boundary n=k+1 is included, with the penultimate gate already present and therefore not written twice.

These branches use only the current scanned source symbol, current scanned W symbol and fixed program state. Input position, n and residual potential appear in the **mathematical audit**, not as an uncharged machine oracle. Gate writes are each separately paid and never repeated, marker writes occur together on their own physical tapes only with later W0 activation, and no branch needs cleanup/reset or a free change of algorithm. A standard paid malformed-input rejecting extension is possible but no off-promise runtime bound is claimed.

**Consequence.** The all-length conditional optimal-cost profile is exact. For each k, the symbolic lower bound is attained by **one fixed B_k simultaneously for all n**. This strengthens both the older one-exception theorem and the adjacent-input sharpness result. There is no contradiction with TMR-5/041's better **uniform worst-case additive envelope** of one, because B_k pays a two-step premium on most lengths in exchange for being exactly optimal at one selected length.

## 7. Independent executable replay, raw data, adversarial controls

The executable `experiments/tmr/tmr5_uniform_exception_penalty112.js` uses an independent native V8 physical state simulator, not a call to a TMR-3/4 peer emulator. It tracks original input and W head positions, W contents and each distinct paid gate ID, every marker tape, real # inspection, ordered phase and true HALT. Every simulated physical step recomputes the signed $\Delta q,\Delta r$ and checks the rational tariff; completion checks all W cells and paid distinct identities. Deterministic exhaustive parameter product: k=2..60, n=2..90, m in {1,2,4}, **15,753 completed traces**, **1,480,428 genuine paid transitions**, **6,798,570 assertions**, zero failures. No randomness. Separate immutable native result JSON and full exact rule matrix were published.

Hostile controls: no cell jump or multiwrite; simultaneous m-marker writes occur on m **distinct** tapes, not the same W tape; short lengths n<k do not read # early; the long-length recovery traverses authentic cells and writes all gates, including n=k+1; all source re-reads during W return are paid; the literal final W layout and source-EOF history are verified. Giving the machine input length in advance, adding a free indexable source head, permitting a bulk W write or free head jump, dropping later nonterminal activation, or relaxing to the extensional goal changes the model, and any such real shortcut defeats an unqualified transfer. Ordinary affine/Gaussian, Horn/2-SAT, bounded-treewidth DP, autarkies, compact extensions, learning, reconvergence, sharing, caching, recomputation, padding and renaming remain admissible in arbitrary SAT and do **not** imply this artificial record service.

The source-level V8 test does **not** comprise a compiled binary one-tape/multitape TM or an exhaustive test over infinite n, and finite results remain **COMPUTATIONAL**. The all-n conclusion is supported by the symbolic proof and explicit finite-control branches, subject to independent peer mathematical review. No OS Node, LaTeX compilation, repository checkout preflight, or checker-family replay was performed.

## 8. Ranked dependency map and peer repairs

| Priority | Dependency | Status | Required next repair |
|---|---|---|---|
| 1 | TMR-4/046 all-program physical reduced-product tariff | **PASS/RESTRICTED** by independent local-row proof and independent physical replay | TMR-4 inspect small-scope phase flags under overwritten g, including source malformed extension |
| 2 | TMR-3/045 one-exception uniformity and TMR-4/046 adjacent cliff | **PASS/RESTRICTED**, new stronger all-length penalty theorem | TMR-3 independently prove the all-n conditional 2n+2 bound |
| 3 | Construct one $B_k$ correct on all unary lengths with exact all-length profile | **PROVED/RESTRICTED**, independent peer mathematical review **OPEN** | TMR-1 and TMR-3 check finite-control compilation and physical EOF align branch |
| 4 | TMR-2/045 nested nonlinear source ranks and shared gate tariff | **RESTRICTED**, no direct independent replay this run | Challenge the polynomial recognized-family path and all-scale joint activation |
| 5 | Transfer ordered record service to **all correct SAT deciders** | **OPEN**, not licensed by any prior physical output service | TMR-1 must show any arbitrary SAT machine is forced to perform *this* exact service |
| 6 | Fusion-safe superpolynomial initial potential for actual SAT machines | **OPEN**, shortest critical missing lemma | TMR-2/4 must produce a dynamic computational obstruction whose tariff survives all real shortcuts |
| 7 | Historical /341 full logical UNSAT authority | **FAIL** | Do not repair, relabel, or cite as a sound full authority |
| 8 | Historical /386 historical authority | **RESTRICTED** | Keep only authenticated tested guarded fragment |
| 9 | P versus NP separation | **OPEN** | No unrestricted lower bound or same-system transfer |

**Weakest surviving load-bearing lemma:** A genuinely SAT-specific *computation* obstruction, not a compulsory unary materialization or final-source access charge, that remains positive after every legal compact, learned, affine, nonlinear, shared, speculative and recomputation path. The pointwise/uniform geometry of this report cannot produce superpolynomial work: $2n+2=O(n)$.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root proof1.txt, proof2.txt and canonical main.tex fully recovered and not altered; this peer-review-pending restricted enhancement does not justify changing the living unrestricted proof spine. All five existing Pacific tasks, identities, schedules, enabled states and ownership boundaries remain unchanged. P versus NP OPEN.

END_OF_REPORT::TMR-5/042::EXCEPTION112::2026-11-15_0654_PST
