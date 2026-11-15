# TMR-4/046: Exact universal ordered-service potential and a sharp adjacent-length uniformity cliff

**2026-11-15 06:42 PST (America/Los_Angeles).** Governing fusion-Lipschitz directive blob `54c9177fc211dfca6c94d89d6ebbf3f3908809d6`. **PROVED/RESTRICTED** for the explicitly qualified physical ordered-record service; independent mathematical peer review **OPEN**. Deterministic executed V8 calibration **COMPUTATIONAL**. **P versus NP OPEN**.

## 1. Candidate and four falsifiers declared before focused project/literature review

**Candidate:** A program-independent phase-and-head-location tariff yields the exact **pointwise** physical lower bound $2n$ for an ordered unary record service, but **no one fixed uniform deterministic program can attain $2n$ simultaneously at every input length**. More sharply, any such program satisfying $T_A(k)=2k$ must satisfy $T_A(k+1)\ge2k+4$. A previously published fixed uniform program achieves $2n+1$ for all $n$, so the optimal uniform worst-case *additive overhead* is exactly one. This is a quantified statement about physical local-head order, not SAT complexity.

F1: A purported W operation jumps its sole W head, writes multiple W cells in one price-one step or makes a free physical move. F2: a putative $2k$ trace writes the final gate later than transition $k$ or fails to reverse W on that same step. F3: a fixed program can inspect the difference between $1^k\#$ and $1^{k+1}\#$ before transition $k+1$, by an undeclared head, advice or syntax oracle. F4: the argument conflates a mandatory ordered W[0]:0-to-1 activation and distinct HALT with the weaker extensional final-state service or any arbitrary SAT decision. The qualified model excludes F1/F3, a direct geometry proof excludes F2, and F4 remains a strict model/transfer gate.

## 2. Corpus, status and primary-source audit

Read first the approved 2026-11-14 fusion directive; then 2026-11-13 TMR replacement; complete root proof1.txt blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343` (28,714 characters), full authentic proof2.txt Git blob `930c5eeddafce656717f28055a7a9a755f44737c` (1,051,196 characters), and full root main.tex Git blob `6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34` (2,545,859 characters). The ordinary large-file Contents API returns blank bodies for the latter two; these **were not treated as empty files**. Reviewed issue #3 with newest five role updates, AGENTS.md, CODEX.md, repository pnp-research skill, current five TMR handoffs, historical LEAD-0029 Lipschitz audit, original TMR-4/035 exact zero SCC/LP, /036 directed zero-closure and /037 paid-path envelope, TMR-1/045 physical SAT last-bit tariff, TMR-2/045 overlapping multiscale nonterminal shortcut, TMR-3/043 and /044 physical fusion controls, and TMR-5/041 complete ordered EOF-write program and its raw tariff data.

Primary **methodology**, not a claimed source of this elementary result: Cousot & Cousot, POPL 1977 abstract interpretation, https://doi.org/10.1145/512950.512973 ; Hennie & Stearns, JACM 1966 local-head multitape modeling, https://doi.org/10.1145/321356.321362 ; Tarjan, 1985 potential methods, https://doi.org/10.1137/0606031 . The exact adjacent-length statement and dual tariff below are independently derived from the declared machine rules. Historical `/341` is FAIL as full logical UNSAT authority; `/386` is RESTRICTED to its authenticated fragment.

**Nonduplication:** TMR-3/044 supplied $2n$ as a restricted geometry lower bound; TMR-5/041 supplied a uniform $2n+1$ upper bound but left sharpness OPEN. This run contributes (i) a **single all-program valid explicit reduced-product potential** with a complete exact cone and all-step cost-underestimating simulation and (ii) the **sharp neighboring-length cliff** and corrected pointwise-versus-uniform optimization quantifiers.

## 3. Qualified concrete state and complete physical operations

For fixed $m\ge1$, input $x_n=1^n\#$ ($n\ge2$), a single original read-only input tape has its sole locally moving head at cell zero. One originally blank work tape W has **exactly one** locally moving W head at zero. The fixed $m$ separate marker tapes each have their own local head. Control/program is one fixed finite deterministic transition table for all $n$, finite alphabets, and each **genuine physical** step costs one, reads the scanned symbols, writes at most one cell on each *distinct* tape and moves each head by at most one position. In the full concrete configuration retain $(x_n,A,\mathrm{control},\mathrm{all\ tapes/heads},\mathrm{paid\ W\ identities},\mathrm{read\ history},\mathrm{flags},\mathrm{interfaces},\mathrm{ledger})$. No source-length oracle, multi-cell write, unpriced jump, or preloaded transcript. Source rereads, scratch memory, algebra, caching and arbitrary paid computations are permitted but cannot defeat the W-head distance for this service.

The **ordered goal** requires W[0] was written 0, W[j] was separately physically written g for all $1\le j<n$, a genuine subsequent nonterminal W[0]:0-to-1 rewrite **after all those gates**, $m$ genuine marker writes O_i[0]=@, a real observation of original # at source cell $n$, and a **distinct later** true HALT. All shared identities count once. This is not the weaker final-state-only service of TMR-4/045 and not a SAT/UNSAT semantics authority.

There are no authentic zero-cost physical transitions, so the zero SCC quotient is identity. Optional reversible zero-cost VIEW/metadata aliases may be included only if the projection below is invariant under them. An unknown free W movement remains MAY and immediately invalidates this potential in the enlarged model; no CEGAR deletion of a genuine shortcut is permitted.

## 4. All-program two-component reduced product and tariff theorem

For the *same fixed source length $n$*, add monotone **observation** history phase $\sigma(C)$ (not a machine oracle):

- $\sigma=0$: no authentic write of the final W[n-1]=g gate yet;
- $\sigma=1$: that paid final-gate event occurred, no subsequent W[0]:0-to-1 rewrite;
- $\sigma=2$: such a subsequent physical activation occurred, no later separate authentic HALT;
- $\sigma=3$: such a later HALT occurred.

If a program executes earlier irrelevant or invalid writes, they do not falsely discharge the required *ordered* events. If records are later erased, this coarse phase may underestimate residual work, which is sound. The full history remains in C, not discarded. Let $z(C)$ denote the actual work-head integer position. Define

$$
q_n(C)=\begin{cases}|z-(n-1)|+1,&\sigma=0,\\0,&\sigma\ge1,\end{cases}
\qquad
r_n(C)=\begin{cases}
n,&\sigma=0,\\
|z|+2,&\sigma=1,\\
1,&\sigma=2,\\
0,&\sigma=3.
\end{cases}
$$

Use the seven-coordinate vector

$$
\mathbf p(C)=(0,0,0,0,q_n(C),0,r_n(C)),\quad
\lambda=(0,0,0,0,1,0,1).
$$

Thus $\Phi(C)=q_n(C)+r_n(C)$, $\Phi(C_{0,n})=n+n=2n$, and $\Phi(\mathrm{GOAL})=0$.

**THEOREM TMR4-046(A), PROVED/RESTRICTED:** For every eligible fixed finite deterministic multitape program A, every complete physical configuration C reached on $x_n$, and every genuine physical step $C\to C'$ (including rereads, scratch writes, shared work, stale records and arbitrary simultaneous writes on different tapes), the exact signed discharge satisfies

$$
\boxed{\Delta q_n(C)+\Delta r_n(C)\le1=w(C\to C').}
$$

**Proof by exhaustive physical event classes:** Before the last gate, a legal W-head move changes $|z-(n-1)|$ by at most one; r remains n. The event writing last g can occur only with W scanning n-1, for which q drops exactly one; after that step W is at n-2, n-1 or n, so r goes from n to n, n+1 or n+2, and its discharge is respectively 0,-1,-2. After the gate, moving the one W head changes $|z|$ by at most one. An authentic activation occurs only with W scanning cell zero, so r decreases exactly from 2 to 1, and the subsequent true HALT decreases r exactly from 1 to 0. Every other operation leaves phase unchanged or merely changes the physical head by at most one. Each case is at most unit total positive discharge. A zero VIEW changes neither q nor r. QED.

**All-step cost-underestimating simulation:** Abstract state is $(n,A,\sigma,z,\mathrm{authenticated\ source/output\ labels})$ in relation to complete C, with full C retained in the fiber. Each **actual** concrete physical transition maps to one corresponding abstract step of the same price one and a related successor; genuine zero VIEW maps to a zero-cost self-loop. Thus no legal concrete path is removed; malformed and alternative program states are not assigned fictitious goal status. Valid ordered goals map to phase 3 with potential zero. Telescoping proves **$T_A(x_n)\ge2n$** for every fixed A implementing the ordered service for all n. It is linear and model-dependent.

**Exact rule-by-component tariff matrix:** In column order CNF,XOR,SEP,FUS,Gamma,Interface,Machine, all but Gamma and Machine are zero. PRE_TOWARD $(+1,0)$; PRE_AWAY $(-1,0)$; PRE_STAY $(0,0)$; LAST_G_LEFT $(1,0)$; LAST_G_STAY $(1,-1)$; LAST_G_RIGHT $(1,-2)$; POST_TOWARD $(0,+1)$; POST_AWAY $(0,-1)$; POST_STAY $(0,0)$; ACTIVATE $(0,+1)$; DISTINCT_HALT $(0,+1)$, all at price 1. Authentic zero VIEW has $(0,0)$ at price 0. Output writes, source reads, affine computation and other simultaneously performed actions do not separately multiply the price.

The **exact full nonnegative active LP cone** for this universal physical action grammar is

$$
0\le\lambda_{\Gamma}\le1,\qquad0\le\lambda_{\mathrm{Machine}}\le1.
$$

Necessity is witnessed by a genuine PRE_TOWARD edge and a genuine POST_TOWARD edge, each independently discharging one unit at price one. Sufficiency follows from every signed row above, including the genuine last-g-and-left fusion. Exact-rational primal $(\lambda_{\Gamma},\lambda_{\mathrm{Machine}})=(1,1)$ gives objective **$2n$**. A matching dual comprises $n$ positive Gamma unit charges while reaching/writing W[n-1] and $n$ positive Machine unit charges while returning, activating and halting in the $n$-special program constructed below. Both primal and dual cost $2n$; no finite sampling is used in the symbolic optimality claim.

## 5. Sharp adjacent-length uniformity cliff and optimal uniform surcharge

**THEOREM TMR4-046(B), PROVED/RESTRICTED:** Fix **one** deterministic program A, initial heads and tapes as above, correct for the ordered service on every $1^n\#$, $n\ge2$. For any $k\ge2$,

$$
\boxed{T_A(k)=2k\ \Longrightarrow\ T_A(k+1)\ge2k+4.}
$$

**Proof:** Completion in $2k$ forces the final required W[k-1]=g write to occur at physical transition **exactly $k$**, because reaching W[k-1] from zero takes at least $k-1$ prior head moves, while returning to W0, performing a later activation and a distinct HALT needs at least $k$ further steps after the final gate. Equality therefore also forces the W head to move **left** from k-1 to k-2 on transition k. On sources $1^k\#$ and $1^{k+1}\#$, the scanned original-input symbol before each of physical transitions 1..k is identical, even with arbitrary adaptive local head moves, since the input head starts at cell zero and cannot reach position k before transition k+1. Determinism and initially identical work/control imply the entire first k physical steps are identical on both sources. Thus in the longer computation the W head is at k-2 after transition k. A subsequent authentic W[k]=g write cannot occur before transition **k+3**: W is at k-2 at the beginning of transition k+1 and needs two rightward moves before it can scan k. From a last write at W[k], the distinct later W0 activation and HALT cost at least an additional k+1 steps. Hence $T_A(k+1)\ge(k+3)+(k+1)=2k+4$. QED.

The bound is **sharp** for adjacent inputs. For each *fixed* k there exists a finite-control program A_k (k hardwired into its finite control, not given as free runtime advice to a single universal program) that writes W0=0 at transition 1, writes gates W1..W[k-1] during transitions 2..k, and speculatively turns W left during the k-th gate step. If the next input symbol is #, it returns, activates and halts in **2k** transitions. If instead there is one further 1 followed by #, it reverses, moves W right twice, writes the genuine last gate W[k]=g on transition k+3, returns, activates and halts in **2k+4**. On any other unary length, finite-control mismatch handling can clear the finitely many speculative W cells, rewind the source, and run TMR-5/041's correct fixed uniform EOF-write program. All reset, scanning and fallback work is paid; no separate free oracle or input-dependent change of the program occurs *within* a run. Thus each A_k is one fixed machine correct on the full unary promised service.

Consequently, the **pointwise** and **single-uniform-program** minimizations differ:

$$
\boxed{\forall n\ge2:\min_A T_A(n)=2n,}
$$

$$
\boxed{\min_{A\ \mathrm{fixed,uniform}}\ \sup_{n\ge2}(T_A(n)-2n)=1.}
$$

The latter equality follows because zero overhead at every length contradicts the adjacent-length cliff, while TMR-5/041's single fixed M_EOFWRITE attains $T(n)=2n+1$ for all n. In particular the proposed global $2n$ optimal uniform schedule is **FALSIFIED/RETIRED** in this model. This argument does **not** claim a pointwise $2n+1$ lower bound for all programs; the hardwired A_k is a genuine counterexample.

## 6. Executed independent finite audit and hostile controls

The exact published JavaScript audit() was executed in native V8. It independently implements physical source and W head positions, real W cell writes, paid gate identities, all distinct marker tapes, source EOF observation, four history phases, signed component differences, telescope checks, uniform EOF_WRITE runs and the hardwired adjacent-length pair. It also enumerates synthetic legal one-step W movements across phases, verifies all LAST_G movement variants, and checks candidate quarter-rational weights with BigInt arithmetic. **386,317 assertions, 53,919 genuine paid transitions, 663 complete traces, 2934 geometric controls, zero failures**. Uniform $2n+1$ traces for n=2..96, hardwired pairs k=2..64, marker tape counts m=1..3. All finite checks **COMPUTATIONAL**, and the symbolic proof has not received independent peer mathematical review.

A separately defined zero-price head jump from W0 to W[n-1] on n>=3 discharges n-1 Gamma units for zero cost and **FAILS**; it is a true *model-changing* shortcut, not an authorized CEGAR spurious path. Writing many W gate cells by one opaque SIMD operation, a second W head, input advice, omitting actual late activation/HALT, or importing an ordinary SAT decision objective changes the system. The usual Horn, dual-Horn, Krom, affine/Gaussian/Tseitin, separator DP, compact circuit/extension, autarky, equality, renaming, padding, branching, shared-DAG, learning, rereading and recomputation mechanisms are not declared forbidden for SAT, and cannot promote this unary-service theorem into SAT hardness. Historical /341 FAIL full accepted language and /386 RESTRICTED are unchanged.

## 7. Dependency/status and next target

TMR-3/044 $2n$ ordered-service physical lower bound **PASS/RESTRICTED**, now accompanied by an all-program exact rational potential. TMR-5/041 $2n+1$ one-uniform-program construction **PASS/RESTRICTED**. Sharp new adjacent-input cliff and exact uniform worst-case additive premium **PROVED/RESTRICTED; independent peer review OPEN**. Published finite physical replay **COMPUTATIONAL**. **Superpolynomial SAT-specific initial obstruction OPEN**. **All-correct-SAT-machine same-system transfer OPEN**. The latter cannot be inferred from record-output services.

**Next target:** Ask TMR-5 and TMR-3 to independently attack the sharp cliff with variable W contents, speculative gate writes, extra independently headed scratch tapes and source rereads. TMR-1 should adopt the pointwise-vs-uniform quantifier firewall. Then apply the full-configuration phase tariff to TMR-1/045's actual strict-3CNF last-bit pair with genuine SAT/UNSAT decisions, without inventing mandatory proof records.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** No root tracker/main edits or schedule modifications.

END_OF_REPORT::TMR-4/046::2026-11-15_0642_PST
