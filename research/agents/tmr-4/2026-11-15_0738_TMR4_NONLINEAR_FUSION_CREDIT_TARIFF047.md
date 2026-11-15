# TMR-4/047: State-dependent fusion credit restores a tight tariff in the last-gate batch calculus

**2026-11-15 07:38 PST | TMR-4 PNP Cost-Sound Abstraction | FUSCREDIT128**

**Scientific status:** PROVED/EXACT for the **explicit preauthenticated shared-gate batch-record transition system** below, independently checked finite cases COMPUTATIONAL. Independent mathematical peer review OPEN. There is **no unrestricted SAT-machine result** and **P versus NP remains OPEN**.

## 1. Candidate and four falsifiers (before focused corpus/literature review)

**Candidate:** TMR-3/046 proved that a state-independent linear tariff on independently counted Gamma and SEP collapses to \(1+\max\{G,\tau^*(E)\}\) when one genuine price-one FUSE checks the last gate and activates a batch. Instead of charging two obligations on that edge, pre-credit **exactly one still-unpaid gate** while fusion remains available and replace fixed per-scale coordinates with the *dynamic minimum residual cover*. This yields a non-separable, state-dependent reduced-product with exact per-transition tariffs. Test both integer and fractional residual cover.

Falsifiers: (F1) free VIEW/NOP changes paid identities or pending obligations; (F2) FUSE decreases the corrected Gamma and SEP components by a combined amount >1; (F3) any cheap second fused gate, bulk free activation or authentic compact affine shortcut defeats the tariff; (F4) the record authority is silently treated as an original-source multitape SAT decider. F1/F2 are excluded by the complete legal transition audit; F3 becomes an **explicit model-changing counterexample** and remains MAY outside the qualified system; F4 is a strict OPEN transfer gate.

## 2. Recovered source scope and novelty

First read the governing 2026-11-14 fusion-Lipschitz directive (blob \`54c9177fc211dfca6c94d89d6ebbf3f3908809d6\`), then the 2026-11-13 TMR replacement, both proof trackers, root \`main.tex\`, \`AGENTS.md\`, \`CODEX.md\`, repo research skill, all five active TMR handoffs, issue #3 (2153 comments through TMR-3/046), and original LEAD-0029, TMR-4/037 paid-Bellman envelope, TMR-2/046 exact fractional-cover and TMR-3/046 authentic FUSE source/code/matrix. The GitHub Contents API returned empty *bodies* for large root proof2/main: authentic Git blob retrieval recovered **1,051,196** and **2,545,859** characters respectively, without treating them as empty. Root hashes: proof1 \`06f7ebc8c2283304a0f5200b518c6e48fa41e343\`, proof2 \`930c5eeddafce656717f28055a7a9a755f44737c\`, main \`6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34\`.

**Prior, not new:** TMR-2/046 fractional-cover LP, TMR-3/046 actual fused final CHECK plus batch and its state-independent tariff collapse; TMR-4/037 generic greatest cost-sound paid Bellman closure. **New this run:** explicit factorized *state-dependent* correction, exact all-state all-step proof and zero-SCC simulation, exact integer-cover Bellman value, fractional rational certificate, and independent exhaustive Fano/triangle/singleton/full/tiny replay. Background for abstract interpretation: Cousot & Cousot (1977), DOI 10.1145/512950.512973. Background for fractional covers: Lovász (1975), DOI 10.1016/0012-365X(75)90058-8. These sources do not prove our specific tariff statement.

## 3. Concrete and abstract systems: same TMR-3/046 authority, no new free action

Fix \(G\ge1\) globally distinct authenticated gate identities \(D\), \(J\) the finite pending-scale index set, and \(E\) a finite set cover of \(J\) by nonempty batches. The immutable authenticated source \(F\), original finite shared gate DAG \(D\), source-specific batch grammar \(E\), paid identity ledger \(P\subseteq D\), unresolved conjunctive scale obligations \(U\subseteq J\), terminal flag \(h\in\{0,1\}\), and reversible metadata \(v\in\{0,1\}\) define concrete states \(C=(F,D,E,P,U,h,v)\). Here \(h=0\) is legal only at \(P=D,U=\varnothing\), the completed conjunctive goal. No machine tapes/heads or proof serialization outside this preauthenticated record grammar are claimed.

The complete genuine transition inventory is unchanged from TMR-3/046:

| Concrete rule | Exact precondition | Cost | Genuine effect |
|---|---|---:|---|
| VIEW / NOP | any state | 0 | toggle \(v\), or do nothing |
| CHECK(g) | \(h=1,\ g\notin P\) | 1 | add **one** new globally unique paid gate |
| BATCH(S) | \(h=1,P=D,S\in E,S\cap U\ne\varnothing\) | 1 | remove \(S\) from \(U\) |
| FUSE(g,S) | \(h=1,D\setminus P=\{g\},U=J,S\in E\) | 1 | **same** step checks final g AND removes S from U; remains nonterminal |
| HALT | \(h=1,P=D,U=\varnothing\) | 1 | changes h to zero, separately |

The exact zero-price SCCs are the pairs \((P,U,h,v=0)\leftrightarrow(P,U,h,v=1)\), including NOP loops. **No** zero-price operation changes \(P,U,h\). Define \(\mathrm{cl}_0(C)\) as the reversible SCC of C and use its canonical projection \(\alpha(C)=(P,U,h)\). Every concrete VIEW/NOP corresponds to an abstract empty path of price zero, every genuine paid step to one quotient edge of exactly the same price, and \(\alpha\) retains every completed goal. This is a **cost-underestimating all-step simulation**, with identity on \(F,D,E\) and provenance, rather than an illicit simulation of arbitrary physical SAT instructions. All unknown physical shortcuts remain MAY.

## 4. State-dependent fusion-credit theorem

For any \(U\subseteq J\), let \(\tau(U)\) be the minimum number of batches in \(E\) covering \(U\), and \(\tau^*(U)\) its fractional set-cover LP optimum. Thus \(\tau(\varnothing)=\tau^*(\varnothing)=0\), both are nonnegative, and for every \(S\in E\),
\[
0\le H(U)-H(U\setminus S)\le 1,\qquad H\in\{\tau,\tau^*\}.
\]
For \(\tau\), append S to a minimum residual integral cover; for \(\tau^*\), add one unit of its batch variable to a minimum residual fractional cover. Monotonicity gives the left inequality.

Write \(u(C)=G-|P|\) and define a **single overlap credit**
\[
\chi(C)=\mathbf1\{h=1,\ u(C)>0,\ U=J\}.
\]
This is one credit regardless of \(G\), batch size, and number of scale ranks. It is never an unpriced operation: it reflects precisely that one **last CHECK** may legally fuse with one BATCH while no batch has yet occurred.

For each \(H\in\{\tau,\tau^*\}\), define the nonlinear seven-column reduced product
\[
\mathbf p_H(C)=(0,0,H(U),0,u(C)-\chi(C),0,h).
\]
All three nonzero coordinates are nonnegative, every goal has zero vector, and both the complete state and projection explicitly retain the paid identity set and conjunction of pending scales. The rational **seven-column certificate** is
\[
\boxed{\lambda=(0,0,1,0,1,0,1)},\quad
\Phi_H(C)=u(C)-\chi(C)+H(U)+h.
\]

**All-step proof:** CHECK has \(\Delta_\Gamma=1\) except when it checks the last gate with \(U=J\), when the credit disappears and \(\Delta_\Gamma=0\). BATCH occurs only when \(u=0\), so \(\Delta_{\rm SEP}=H(U)-H(U\setminus S)\le1\) and all other charged deltas are zero. FUSE is legal only for \(u=1,U=J\): the genuine last-gate decrease \(u:1\to0\) is offset by \(\chi:1\to0\), making \(\Delta_\Gamma=0\); the *only* charged decrease is \(\Delta_{\rm SEP}=H(J)-H(J\setminus S)\le1\). HALT decreases \(h\) by exactly one. VIEW/NOP leave all coordinates constant. Consequently **every legal** \(C\to C'\) satisfies
\[
\lambda^\top(\mathbf p_H(C)-\mathbf p_H(C'))\le w(C,C').
\]
Summation on every genuine completion path gives \(\Phi_H(C_0)\le W(C_0)\). No shared gate identity is counted twice and no AND-scale obligation is omitted.

**Tightness for integer cover, for every legal state:** For \(h=1\), the exact minimum remaining record cost is
\[
W(C)=
\begin{cases}
u+\tau(J),&u>0,\ U=J;\\
u+\tau(U)+1,&u>0,\ U\ne J;\\
\tau(U)+1,&u=0.
\end{cases}
\]
For a completed goal \(W=0\). These cases exactly equal \(\Phi_\tau\). For \(u>0,U=J\), CHECK all but the final gate, FUSE the last gate with the first batch of an optimal integer cover, activate the rest, then execute distinct HALT; the cost is \(u+\tau(J)\). For \(U\ne J\), the initial FUSE precondition can never recur because U only decreases, so all remaining checks, covering batches and HALT must be separately paid. For \(u=0\), only covering batches and HALT remain. This proves a *global Bellman equality* for this particular calculus, not a lower bound on the full physical cost of 3-SAT.

For initial \(P=\varnothing,U=J,h=1\),
\[
\boxed{\Phi_{\tau^*}(C_0)=G+\tau^*(J),\qquad
\Phi_\tau(C_0)=W(C_0)=G+\tau(J).}
\]
The nonlinear fractional basis is still a genuine exact-rational tariff LP: each residual fractional cover is solved with exact rational simplex, both primal fractional cover and dual packing are independently checked on **every** subset U, and all local signed rows are verified. For \(G\ge2\), the CHECK, BATCH and HALT rows independently force the three corresponding basis weights to be at most 1, so \(\lambda=(1,1,1)\) is also optimal in this new restricted three-coordinate basis. This is **not** the old linear basis: the coordinates changed to include an authentic state-dependent interaction and a residual set-cover optimization.

## 5. Exact finite audits and hostile controls

| System | Gates | \(\tau^*(J)\) | \(\tau(J)\) | Old state-independent LP | New fractional tariff | New exact integer tariff / work |
|---|---:|---:|---:|---:|---:|---:|
| Fano seven scales | 3 | \(7/3\) | 3 | 4 | \(16/3\) | 6 |
| Fano seven scales | 1 | \(7/3\) | 3 | \(10/3\) | \(10/3\) | 4 |
| Triangle | 2 | \(3/2\) | 2 | 3 | \(7/2\) | 4 |
| Four singleton batches | 2 | 4 | 4 | 5 | 6 | 6 |
| One full batch | 3 | 1 | 1 | 4 | 4 | 4 |
| Tiny one gate/one scale | 1 | 1 | 1 | 2 | 2 | 2 |

**Executed native V8:** 137,231 assertions, **404** full exact-rational subset LP primal/dual solves, **19,832** legal all-state tariff rows and **9,640** zero-price checks, zero failures. Generic Tarjan SCC quotient verified every zero SCC is exactly the two metadata views; no free transition exits its SCC. For each laboratory, a separate real shortest-path enumeration and complete CHECK/FUSE/BATCH/HALT witness match \(G+\tau(J)\). The tiny full signed seven-column row list and per-family rule aggregation are published in JSON; the exact self-contained JavaScript emits the same raw JSON and matrix with \`node experiments/tmr/tmr4_fusion_credit128.js\` and \`node ... --matrix\`.

Hostile cases preserved rather than filtered: (i) TMR-3's real price-one last-gate FUSE rejects independent old unit weights (\(2>1\)); (ii) if a model-changing **FUSE_TWO** checks two final identities and one batch in one price-one action, the corrected potential falls **2>1**, so the theorem does not survive; (iii) a truly free whole-cover affine/compact batch in the Fano model produces an integer-potential fall of **2>0** and invalidates the model; (iv) a real price-one full batch is retained and yields the correctly smaller minimum 4. Malformed or adversarial physical source authentication, general Gaussian elimination, learning, compact circuits, preprocessing, sharing, caching, rereading, recomputation and unbounded machine primitives remain MAY outside this authority, not CEGAR-deleted. No logical UNSAT checker is invoked.

## 6. Resource ledger and remaining proof gates

**Logical paid work:** one price per globally new CHECK, one per batch activation, one for the single genuine FUSE, and a **different** nonterminal-to-HALT step; a checked identity belongs to P once and only once. **Elapsed sequential work/span** is minimum \(G+\tau(J)\). **Description size/retained information** is \(G+q+2\) bits for the P/U/h/v bookkeeping, not a machine-space *lower bound* or physical cost. **Interfaces, actual original input access, full checked DAG construction, machine control/head/tape movements, proof serialization, computations of \(\tau(U)\), and required physical source authentication** are not compiled and no uncharged bridge is asserted. \(\tau(U)\) may itself be computationally difficult: encoding it in an analytic potential does **not** supply a polynomial algorithm or establish SAT hardness.

The real *limitation* is decisive: for every q-scale cover, \(\tau(J)\le q\) (select one batch per scale); for TMR-2's inherited shared compact family \(G_m=O(m^3)\), q=m-4. Therefore even the **exact** integer value is only \(O(m^3)\), not superpolynomial. The new success is an exact cost-sound *restricted* abstraction and identification of a one-time fusion-credit structure, **not** the needed asymptotic SAT obstruction.

**Same-system transfer gate: OPEN** for every correct fixed finite total deterministic multitape SAT decider. TMR-1/046's genuine uniform efficient recognition of an explicitly poly-labeled family is an independent hostile ceiling, not removed by this theorem. Historical \`/341\` remains **FAIL** on its full logical UNSAT accepted language; \`/386\` remains **RESTRICTED**. Neither was repaired or relabeled.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** proof1.txt, proof2.txt, root main.tex unchanged and ownership preserved. Five existing hourly schedules unchanged. **P versus NP remains OPEN.**

## 7. Reproducibility and next falsifier

- **Complete runnable source:** \`experiments/tmr/tmr4_fusion_credit128.js\`.
- **Exact native V8 raw results:** \`results/raw/tmr/2026-11-15_0738_TMR4_FUSCREDIT128_V8_RAW.json\`.
- **Full seven-column rule schema, tiny all-edge rows, per-case counts, exact rational cover/packing and matching path certificates:** \`results/raw/tmr/2026-11-15_0738_TMR4_FUSCREDIT128_TARIFF_MATRIX.json\`.

**Peer next:** TMR-5 independently replays the changed-coordinate certificate and tries a genuine cheaper physical multi-fusion. TMR-3 checks whether last CHECK+activation can *also* output/HALT in a true native machine, noting this record calculus's separate HALT. TMR-1 preserves the same-system boundary. TMR-2 seeks a residual obstruction in a *real SAT input* that cannot be disposed of by a polynomially recognizable witness or cheap affine/compact code.

END_OF_REPORT::TMR4::FUSCREDIT128::2026-11-15_0738_PST
