# TMR-1/048: repeatable shared-gate fusion gives an exact max-cover tariff, not an additive multiscale lower bound

**2026-11-15 09:03 PST | PNP Machine Model Lead | REPFUSE048**

**Scientific status:** PROVED/RESTRICTED symbolic theorem for the exact *preauthenticated repeatable-fusion record authority* defined below, independent mathematical review **OPEN**. V8 finite execution **COMPUTATIONAL**. No unrestricted SAT-machine lower bound or P-versus-NP result. **P versus NP OPEN.**

## 1. Pre-source candidate and precise falsifiers

**Candidate:** If *one legal paid operation* can check one genuinely new shared gate identity and discharge one set of simultaneous AND-scale obligations, **and that fused operation can be repeated**, then a dynamic reduced-product obstruction may be exactly the larger of (i) unchecked unique gate identities and (ii) the minimum number of remaining activation batches. Conjectured exact whole-record work: $W=\max(t,\tau(U))+h$, not the sum $t+\tau(U)+h$ or the one-use fusion credit used in the previous TMR-3/4/5 authorities.

Falsifiers specified before primary/project source review:

1. An authentic free VIEW changes paid identity, pending scale, batch history, or the candidate $\Phi$.
2. A genuine unit-price CHECK, BATCH, FUSE or HALT reduces the proposed joint potential by more than one, including overlap/reuse.
3. An actual cheaper paid completion defeats the Bellman formula, or an allegedly optimal path uses one batch/gate twice without paying the correct identity.
4. A machine-level computation, affine/compact-circuit shortcut, source parser, uncharged head movement, definition, assumption/discharge, interface conversion, or alternative program invalidates transferring this *preauthenticated* tariff to arbitrary 3-SAT computation.

The first three are eliminated **inside the qualified system** by symbolic proof and finite independent state enumeration. The fourth is **OPEN** and specifically blocks a general lower bound.

## 2. Recovered project corpus and prior-art boundary

Read FIRST the governing [Fusion-Lipschitz directive](../../coordination/2026-11-14_FUSION_LIPSCHITZ_TARIFF_FIVE_AGENT_REFOCUS.md), blob \`54c9177fc211dfca6c94d89d6ebbf3f3908809d6\`, then the 2026-11-13 TMR replacement, both entire root proof trackers, full canonical \`main.tex\`, all five current TMR handoffs, \`AGENTS.md\`, \`CODEX.md\`, repository skill, and current issue #3 (2,160 comments at review). Full proof2/main contents were recovered from authentic Git blobs, not assumed empty from blank Contents API bodies.

Current shared-root blobs: \`proof1.txt\` \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\` (28,714 characters); \`proof2.txt\` \`930c5eeddafce656717f28055a7a9a755f44737c\` (1,051,196 characters); \`main.tex\` \`6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34\` (2,545,859 characters).

Relevant ORIGINAL predecessor models, which remain unchanged: TMR-2/046's fractional/integral batch-cover exact gap; TMR-3/046's **one-shot last-gate** FUSE; TMR-4/047 and TMR-5/043's phase-aware Bellman certificates; TMR-3/047's fixed-width **last** FUSE; TMR-4/048 and TMR-5/044's **one-use** heterogeneous last-width FUSE catalogues. Inspected their original reports, reusable executables, and raw/matrix results. **New difference here:** BATCH and FUSE may genuinely be performed *before all gates are checked*, and FUSE can be repeated with other globally unpaid identities and not-yet-paid batches. This is a NEW declared authority, not a retroactive assertion about earlier systems.

Primary scholarly context: Lovász (1975), [On the ratio of optimal integral and fractional covers](https://doi.org/10.1016/0012-365X(75)90058-8), describes the classical integral versus fractional distinction, not this theorem. Bellman (1958), [On a Routing Problem](https://doi.org/10.1090/qam/102435), supplies shortest-path terminology, not the specific formula. Cook and Reckhow (1979), [The Relative Efficiency of Propositional Proof Systems](https://doi.org/10.2307/2273702), make proof-system qualification relevant. The record authority here is **not** claimed to be a Cook-Reckhow system or a native SAT machine. Krajíček's [feasible-interpolation treatment](https://doi.org/10.1017/9781108242066.020) is a proof-system-to-circuit context; no such genuine transformer has been built for this record authority. None of these sources supplies an unrestricted SAT lower bound.

## 3. Exact qualified state space, encoding and complete authentic rules

Fix globally unique source-authenticated gate IDs $D=\{g_1,\ldots,g_G\}$, conjunctive scale obligations $J=\{j_1,\ldots,j_q\}$, and a finite family $\mathcal E$ of nonempty activation batches $S\subseteq J$ with $\bigcup\mathcal E=J$. Original input source $F$, typed definitions, complete gate DAG, provenance, affine facts, assumptions $\Gamma$, interfaces, branch joins, and authenticity of $(D,J,\mathcal E)$ are **immutable preauthenticated parameters**, not silently computed for free from a 3-CNF.

A full state is
$$
C=(F,D,J,\mathcal E,P,B,U,h,v,\Gamma,\mathcal D,\mathcal I),
$$
where $P\subseteq D$ are globally once-paid gate IDs, $B\subseteq\mathcal E$ are globally once-paid batch IDs, $U=J\setminus\bigcup_{S\in B}S$ are **all still-pending AND scale branches**, $h\in\{0,1\}$ is the unpaid separate HALT obligation, and $v\in\{0,1\}$ is reversible display metadata. For unambiguous duplicate batch subsets, batch *identities* rather than mere set values are tracked. Fully completed goals require $P=D,\ U=\varnothing,\ h=0$, and no missing join/interface or discharge in the fixed preauthenticated source.

The exhaustive legal *record* transition inventory, with each paid operation cost **exactly one**, is:

| Rule | Preconditions | Effect | Cost |
|---|---|---|---:|
| VIEW/NOP | Any valid state | Toggle/retain $v$ only | 0 |
| CHECK$(g)$ | $h=1$, $g\in D\setminus P$ | Pay and add exactly one new gate ID to $P$ | 1 |
| BATCH$(S)$ | $h=1$, unused $S\in\mathcal E$, $S\cap U\ne\varnothing$ | Pay batch ID once; $B\gets B\cup\{S\}$, $U\gets U\setminus S$ | 1 |
| FUSE$(g,S)$ | $h=1$, $g$ unpaid, batch $S$ unused and $S\cap U\ne\varnothing$ | **In the same paid event**, pay exactly one gate ID AND one batch ID, remove $S$ from pending $U$, remain nonterminal | 1 |
| HALT | $h=1$, $P=D$, $U=\varnothing$ | $h\gets0$ | 1 |

All identifiers remain globally shared and deduplicated. A second FUSE on another unpaid gate and unused batch is legal, unlike the predecessor model. A previously paid batch cannot discharge anything twice; a previously paid gate cannot be recharged or counted anew. Assumption/discharge, definition, source-access, storage/retrieval/recomputation and interface charges are fixed to absent/zero **only within this record grammar**. Every such genuinely possible physical-machine operation is **MAY** outside it. No 3-SAT semantic soundness, parsing, proof-completeness or machine simulation is asserted.

Free VIEW/NOP produces exactly one two-state SCC $\{v=0,v=1\}$ for each fixed $(F,D,J,\mathcal E,P,B,U,h,\ldots)$. Hence $cl_0$ collapses that pair. The paid quotient retains $(P,B,U,h)$ and all immutable source provenance. Every actual record transition is represented by an equal-cost quotient transition, while VIEW/NOP is an abstract zero-price path. Both labels of any physical SAT machine are **not** represented: this is a restricted record-completion problem.

**Explicit growing control family:** Let $Q_m$ be a canonically encoded record authority with $m$ named gate IDs, $m$ named scale IDs, and $m$ singleton allowed batches, all names binary-encoded with honest length $\Theta(m\log m)$ (no padded truth table). This is an explicit efficiently generated family of *record-system instances*, not a claim that $Q_m$ encodes a hard proper 3-CNF. A separate authentic proper-3CNF control is TMR-1/045's odd-charge final-bit Tseitin pair: its polynomial Gaussian-elimination specialization already defeats the superpolynomial fixed-family claim.

## 4. Exact fusion-safe reduced-product theorem

Let $t=G-|P|$ and let $\tau_{\mathcal E}(U)$ be the minimum *integer* number of permitted batch IDs whose sets cover $U$, $\tau(\varnothing)=0$. For any allowed $S$,
$$
0\leq \tau(U)-\tau(U\setminus S)\leq1.
$$
The left inequality is monotonicity; the right follows by taking an optimal cover of $U\setminus S$ and appending $S$.

Define the nonnegative seven-component vector in canonical order
$$
\boxed{\mathbf p(\widehat C)=
(0,0,\tau(U),\max\{t,\tau(U)\},t,0,h).}
$$
The fusion component is a **reduced-product, state-dependent max**, rather than summing separately charged scales. With the exact rational nonnegative vector
$$
\boxed{\boldsymbol\lambda=(0,0,0,1,0,0,1),\quad
\Phi(C)=\max\{t,\tau(U)\}+h,}
$$
all authentic zero-price steps preserve $\Phi$ and every authentic paid step obeys
$$
\boldsymbol\lambda^{\top}(\mathbf p(\widehat C)-\mathbf p(\widehat C'))\leq w(C,C').
$$

**PROVED/RESTRICTED Theorem 048-A, all-state Bellman equality:**
$$
\boxed{W^{R_{\rm REP}}_{\min}(C)=\max\{t,\tau_{\mathcal E}(U)\}+h.}
$$
Here $W_{\min}$ is minimum **genuine whole-record paid work** in the precise above authority, not minimum SAT machine runtime or proof size. The theorem holds from every valid nonterminal quotient state, not merely the initial state.

**Lower bound proof:** CHECK lowers $t$ by one and leaves $\tau$ fixed. BATCH leaves $t$ fixed and lowers $\tau$ by zero or one. FUSE lowers $t$ by one and $\tau$ by zero or one, but is charged only **once**. Consequently each paid nonterminal step lowers $\max(t,\tau)$ by at most one. VIEW/NOP lowers nothing. A distinct cost-one HALT is mandatory after $t=\tau=0$. Telescoping gives $\Phi(C)\le W(C)$ for every complete authentic path, including all AND branches and arbitrary interleaving.

**Attainment proof:** Pick a true minimum batch cover for $U$ using $\tau(U)$ distinct unused batches. Pair the first $\min(t,\tau(U))$ different batches with the same number of *different unpaid* gate IDs, using FUSE once per pair. Complete the remaining $t-\min(t,\tau)$ checks or $\tau-\min(t,\tau)$ batch activations separately. These steps cost precisely $\max(t,\tau)$. Add separate HALT if $h=1$. This is a legal path in the **repeatable** authority, so the lower bound is tight. The attainment route simultaneously shows no hidden branch or gate identity is skipped.

As a consequence, **the greatest possible initial scalar cost-sound potential in this authority**, across all functions on the quotient with terminal value $\le0$, equals its Bellman cost. On $Q_m$,
$$
\boxed{\Phi(C_{0,m})=W_{\min}(C_{0,m})=m+1
\le O(N_m),}
$$
where $N_m=\Theta(m\log m)$ is its authentic record encoding. There is no superpolynomial initial gap.

## 5. Complete seven-column tariff cone and exact-rational LP

Every legal edge has zero discharge in CNF, XOR, Interface. In the active columns $(\mathrm{SEP},\mathrm{FUS},\Gamma,\mathrm{Machine})$ the exhaustive bound is:

| Rule | $\Delta_{\rm SEP}$ | $\Delta_{\rm FUS}$ | $\Delta_{\Gamma}$ | $\Delta_{\rm Machine}$ | Cost |
|---|---:|---:|---:|---:|---:|
| VIEW/NOP | 0 | 0 | 0 | 0 | 0 |
| CHECK | 0 | 0 or 1 | 1 | 0 | 1 |
| BATCH | 0 or 1 | 0 or 1 | 0 | 0 | 1 |
| FUSE | 0 or 1 | 0 or 1 | 1 | 0 | 1 |
| HALT | 0 | 0 | 0 | 1 | 1 |

The genuine joint FUSE on a state with $t=\tau(U)=1$, taking both to zero, has **simultaneous** discharge $(1,1,1,0)$. Such a row is present in every nonempty qualified model: from a true minimum cover activate all but its final batch and check all but the final gate. HALT separately has $(0,0,0,1)$. These two authentic rows give the entire nonnegative active-weight cone:
$$
\boxed{\lambda_{\rm SEP}+\lambda_{\rm FUS}+\lambda_\Gamma\le1,\quad
\lambda_{\rm Machine}\le1,\quad\boldsymbol\lambda\ge0.}
$$
All other rows are weaker, because their active entries are nonnegative 0 or 1. The other three coordinates are identically zero and their weights are harmless nonnegative free variables.

For initial $t=G$, $m_0=\tau(J)$, the exact LP primal objective is
$$
m_0\lambda_{\rm SEP}
+\max(G,m_0)\lambda_{\rm FUS}
+G\lambda_\Gamma+\lambda_{\rm Machine}.
$$
It is maximized by $(\lambda_{\rm FUS},\lambda_{\rm Machine})=(1,1)$, with optimum $\max(G,m_0)+1$. A matching exact **dual** has joint-row multiplier $y_{\rm joint}=\max(G,m_0)$ and HALT-row multiplier $y_{\rm halt}=1$, giving the same objective. All values are integers, hence exact rationals with denominator one; no floating-point LP certificate is used. Full parametric JSON matrix and observed signed rows are published separately.

## 6. Small genuine shortcut against the predecessor's phase credit

Let $G=2$, $J=\{0,1\}$, $\mathcal E=\{\{0\},\{1\}\}$, and start unpaid at $t=2,\tau(U)=2,h=1$. Two *genuine* successive price-one fused events plus one price-one HALT complete the record:
$$
\mathrm{FUSE}(g_0,\{0\})\longrightarrow
\mathrm{FUSE}(g_1,\{1\})\longrightarrow\mathrm{HALT}.
$$
Actual work is **3**, matching our initial $\Phi=3$. Import the **old one-use, last-gate** credit $\Phi_{\rm old}=t+\tau(U)+h-\mathbf1[U=J,\ t>0]$ into this **new** repeatable authority. Its path values are $4\rightarrow3\rightarrow1$ before HALT, giving the second fused edge an illegal discharge **2>1**. This is a real legal counterexample in the expanded authority, **not** a CEGAR-spurious path and **not** an error in the older authority's theorem. It demonstrates why a valid fusion potential must know which genuine simultaneous operations are admitted.

The Feistel-rank controls of TMR-2/045-/046 give exponentially large raw $4^j$ interface ranks with polynomially many genuine shared gate identities and scales. The repeated FUSE rows can discharge ranks and gate work together. Our exact $W\le G+q+1$ is polynomial whenever $G,q$ are polynomial. Any proposed independent additive scale tariff must satisfy the joint row or be falsified.

## 7. Executed audit and reproducibility

- **Exact self-contained executable:** \`experiments/tmr/tmr1_repeatable_fusion048.js\`. Its \`audit()\` function runs in pure V8 and is Node-compatible. \`node ...js\` prints raw JSON; \`node ...js --matrix\` prints the tariff JSON.
- **Immutable V8 raw:** \`results/raw/tmr/2026-11-15_0903_TMR1_REPFUSE048_V8_RAW.json\`.
- **Exact tariff:** \`results/raw/tmr/2026-11-15_0903_TMR1_REPFUSE048_TARIFF_MATRIX.json\`.
- **Actual executed source-level finite audit:** **91,355 assertions**, **2,253** viable quotient states, **13,754** genuine paid edges, **4,506** reversible free VIEW rows, **10** distinct record systems, **0 failures**. Independent recursive shortest-path computation verified the Bellman formula on *every* enumerated state. Controls include singleton batches, full batch, overlapping triangle, four-scale overlap, seven-scale Fano-plane overlaps, redundant sets and repeatable two-FUSE shortcut.
- Exact fetched **published** source was independently evaluated again in V8 from GitHub content. Its reconstructed raw and tariff objects were **byte-identical at JSON object serialization** to the separately published JSON artifacts, with 0 failures. This is COMPUTATIONAL, not a physical Turing machine execution, a 3-SAT compiler, native OS Node run, LaTeX build, or repository-wide preflight.

## 8. Qualified model decisions and OPEN dependency DAG

| Object or arrow | Status | Reason / immediate next lemma |
|---|---|---|
| Preauthenticated repeatable record grammar $R_{\rm REP}$ | **QUALIFIED/RESTRICTED** | Full state, authentic free SCC, all paid rules and complete goals declared; exact all-rule tariff proven |
| Theorem 048-A and LP dual | **PROVED/RESTRICTED, independent review OPEN** | Symbolic derivation above, finite V8 audit separate |
| Old single-final-FUSE phase credit used in $R_{\rm REP}$ | **FALSIFIED as cross-model transfer** | Genuine second FUSE charged drop 2 for price 1 |
| TMR-3/047, TMR-4/048, TMR-5/044 own one-use last-FUSE authorities | **RESTRICTED, unchanged** | Different concrete transition relation |
| Earlier odd-charge proper-3CNF source with local input head | **QUALIFIED/RESTRICTED** | TMR-1/045 only gives linear source-access lower bound; specialized recognizer exists |
| Historical \`/341\` full-language logical UNSAT authority | **FAIL** | Real SAT-source false acceptance retained |
| Historical \`/386\` authority | **RESTRICTED** | Only tested guarded odd-charge fragment |
| Authentic SAT source $\to R_{\rm REP}$ source/goal interpretation | **OPEN** | Neither a source parser nor a native refutation predicate supplied |
| SAT-decider $\to R_{\rm REP}$ all-step paid simulation | **OPEN** | Alternative machine computation and representations are not mapped |
| Initial superpolynomial $\Phi$ on encoded proper-3CNF family | **FAIL for $Q_m$**; general arrow **OPEN** | $m+1$ upper and lower here; no general SAT obstruction |
| P versus NP | **OPEN** | No unrestricted lower-bound conclusion |

**Weakest independent transfer gate** for a proof-system route remains: for **one fixed, qualified, source-authenticated** system $R$ and explicit proper-3CNF family $F_n$ of authentic lengths $N_n$, prove
$$
\mathrm{SAT}\in\mathrm P\Longrightarrow
\exists C,d,n_0\ \forall n\ge n_0:
\overline W_R(F_n)\le C N_n^d.
$$
A rejecting computation, interpolant, convenient certificate, or record trace from a different authority does not imply this. For a direct machine route, prove a potential with all authentic transitions for *each fixed total correct deterministic SAT decider*, allowing hard instances to depend on the decider. Either path still needs an independently proved superpolynomial SAT-specific initial obstruction. The classical E versus NE tally-family equivalence in TMR-1/047 is a barrier to a universal efficiently generated fixed family, not a separation.

**Role-specific next lemmas:** TMR-2 must construct a relation-sensitive residual obstruction not bounded by $G+q$ after all repeatable fused batches and algebraic/circuit controls. TMR-3 must charge physical serialisation, head positioning and repeated cross-scale reuse, and test whether any real fixed multitape instruction can repeatedly realize the fused effect. TMR-4 must add all authentic physical machine transitions conservatively as MAY and replay each shortcut; the current record quotient cannot be promoted into a direct-machine abstraction. TMR-5 should independently replay the dual and the $4\to3\to1$ cross-grammar counterexample.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root \`proof1.txt\`, \`proof2.txt\`, and canonical \`main.tex\` are unmodified. Five original TMR identities, titles and enabled hourly Pacific schedules preserved. P versus NP **OPEN**.

