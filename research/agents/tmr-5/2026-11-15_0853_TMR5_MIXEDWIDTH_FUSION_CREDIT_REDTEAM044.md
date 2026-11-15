# TMR-5/044: heterogeneous-width fusion credit, independent red-team replay

**2026-11-15 08:53 PST | TMR-5 Machine Bottleneck Redteam | MIXFUSE044**

**Status:** PROVED/RESTRICTED for the exactly declared preauthenticated record calculus, independent mathematical peer review OPEN. Native Node checks COMPUTATIONAL. This is not a physical SAT-machine lower bound. P versus NP remains OPEN.

## 1. Target and four predeclared falsifiers

**Target:** independently recover TMR-3/047's exact Bellman theorem and generalize it to a fixed grammar containing several genuinely legal FUSE widths, with possibly different eligible batch families for each width. Demand the exact zero-cost quotient, complete seven-component signed tariff, and independent shortest-path check.

**Falsifiers:** (F1) an authentic zero-cost VIEW changes paid identities or AND obligations; (F2) a real price-one wider fusion violates the corrected tariff; (F3) a legal cheaper CHECK/BATCH/FUSE/HALT completion contradicts the alleged exact cost; (F4) actual physical machine operations, compact circuits, Gaussian elimination, learning, source authentication or alternate representations permit a path absent from this laboratory. The first three do not occur within the qualified model. F4 is a decisive OPEN transfer barrier, not a spurious path to eliminate.

## 2. Sources and precise predecessor scope

Read first the 2026-11-14 fusion-Lipschitz directive (SHA 54c9177fc211dfca6c94d89d6ebbf3f3908809d6), then the 2026-11-13 TMR replacement, both complete root proof trackers, authentic full root main.tex, issue #3 through TMR-3/047, AGENTS.md, CODEX.md, repository research skill and all five current TMR handoffs. Compared the original TMR-3/047 fixed-width b theorem, TMR-4/047 fusion credit, TMR-5/043 b=1 Bellman and TMR-2/047 real-source linear ceiling. Historical fusion, affine and interpolation counterexamples were retained at prior scope. Primary background: Richard Bellman, *On a Routing Problem*, Quarterly of Applied Mathematics 16 (1958), 87-90, DOI 10.1090/qam/102435. Bellman's shortest-path principle is background only; the specific theorem is proved directly here.

Prior b=1 and fixed-b results are **not** rebranded as new. The new result is the exact heterogeneous-width and width-dependent eligible-batch credit, with a reproducible independent shortest-path and full signed-rule audit.

## 3. Qualified concrete system and zero-price quotient

Fix a preauthenticated set D of G>=1 distinct globally paid gate identities, a nonempty set J of q pending AND scales, and nonempty allowed activation batches E covering J. For each permitted fixed positive integer b, supply a possibly restricted batch family E_b subset E. The fixed record authority, not an unrestricted SAT program, allows precisely these states and transitions.

The complete state includes immutable (D,J,E,(E_b)), paid history P subset D, pending obligations U subset J, a nonterminal flag h=1, and reversible metadata v in {0,1}. Goal requires P=D, U=empty, h=0. CHECK(g), price1, adds exactly one previously unpaid global identity while h=1. BATCH(S), price1, requires P=D, S in E and S meeting U, and removes S from U. FUSE_b(S), price1, requires exactly b still-unpaid identities, U=J and S in E_b, pays all b identities **once**, removes S from U in the same **nonterminal** action. HALT, price1, requires P=D and U empty, and separately sets h=0. Free reversible VIEW and NOP only change or retain v and never change P,U,h. The exact authentic zero-cost SCC quotient is therefore (P,U,h).

No other rules are tacitly forbidden on a physical machine. The authority is *preauthenticated*: no source byte parser, circuit generator, head access, proof search, alternate SAT computation, bulk algebraic rewrite, or free oracle is provided. These are MAY outside this grammar.

## 4. New exact Bellman and signed tariff theorem

Let t=G-|P| and let tau(U) be the minimum **integer** number of sets from E whose union covers U, with tau(empty)=0. For any permitted batch S, 0<=tau(U)-tau(U\S)<=1. Define
$$
\sigma(t)=\max\left(\{0\}\cup
\left\{b+\tau(J)-\tau(J\setminus S)-1:
1\le b\le t,\ S\in E_b\right\}\right).
$$
This uses only genuinely allowed width-b batches. Since each batch removes at most one unit of minimum cover, 0<=sigma(t)<=t and sigma(t) is nondecreasing.

Define the nonnegative seven-component reduced product in the canonical coordinate order (CNF,XOR,SEP,FUS,Gamma,Interface,Machine):
$$
\mathbf p(C)=(0,0,\tau(U),0,t-\chi(C),0,h),\qquad
\chi(C)=\mathbf1\{h=1,U=J\}\sigma(t).
$$
Completed goals have all coordinates zero. Exact rational weights are
$$
\boxed{\lambda=(0,0,1,0,1,0,1)}.
$$

**Theorem 044-A, restricted:** On every viable record state,
$$
\boxed{V(C)=\lambda^\top\mathbf p(C)
=t+\tau(U)+h-\chi(C)=W_{\min}(C).}
$$
In particular the fully pending initial state satisfies
$$
\boxed{W_{\min}(C_0)=G+\tau(J)+1-\sigma(G).}
$$

**Independent exactness proof.** Without any FUSE, a completion needs the t globally distinct CHECKs, at least tau(U) batch activations, and a separate HALT, so cost t+tau(U)+h. A FUSE can happen at most once because it requires U=J and thereafter removes a nonempty S from U, and no rule restores U. If U=J and a permitted (b,S) has b<=t, first perform t-b ordinary CHECKs, then FUSE_b(S), then an optimal tau(J\S) BATCH cover and separate HALT. The exact cost is
$$
(t-b)+1+\tau(J\setminus S)+1
=t+\tau(J)+1-\left[b+\tau(J)-\tau(J\setminus S)-1\right].
$$
Taking the least over the no-FUSE route and all legal fused choices gives the formula with sigma(t). No additional fusions, skipped AND branches, duplicate paid IDs, or omitted terminal operations exist in this authority. If U differs from J, no FUSE can become newly available. Thus the lower bound is attained by a completely legal path from every state.

**Complete signed rule-by-component tariff.** Every zero-price VIEW/NOP discharges (0,0,0,0,0,0,0). CHECK, when U=J, has signed Gamma discharge 1-sigma(t)+sigma(t-1)<=1; otherwise it discharges exactly one Gamma. BATCH discharges SEP=tau(U)-tau(U\S)<=1 and zero others. At FUSE_b(S), the signed Gamma discharge is b-sigma(b), SEP discharge is tau(J)-tau(J\S), and the total is
$$
b+\tau(J)-\tau(J\setminus S)-\sigma(b)\le1
$$
by sigma(b)'s definition. HALT discharges one Machine unit. No other charged component changes. Consequently every genuine rule satisfies lambda dot Delta<=price, all free SCCs preserve the vector, and all genuine goals have V=0. Telescoping plus the attained shortest path makes this potential pointwise maximal among cost-sound scalar potentials for **this same authority**.

When the only permitted width is one b and E_b=E, a minimum batch cover gives some S with tau(J)-tau(J\S)=1, so sigma(t)=b for all t>=b and 0 otherwise. Hence the theorem symbolically and independently reproduces TMR-3/047's exact fixed-b credit as a special case, rather than modifying its original result.

## 5. Smallest genuine shortcut and executed verification

With G=2, q=1, E consisting of the one full batch, and **both** b=1 and b=2 admitted, one genuine cost-one FUSE_2 plus a distinct HALT finishes in **2 paid actions**. The **old** b=1 potential starts at 3 and falls to 1 in the FUSE_2 event, charging 2 units for price1. Thus the transferred old tariff FAILS in the expanded legal grammar. The corrected mixed-width credit has sigma(2)=2, V(initial)=2, and charges exactly one unit on that FUSE_2 event. Original TMR-3/047 remains valid in its unmodified *singleton-width* authority.

**Actually executed locally under native Node 22.16.0:** deterministic seed 0x5eed; 56 distinct models, 8,728 exact quotient states, 21,891 genuine paid rows, 17,456 reversible free-view rows, 338 genuine negative signed Gamma rows, 88,431 assertions, zero failures. An independent recursive shortest-path solver checked every state against the formula; a separate signed-vector validator checked all local tariffs, goals and zero SCC invariance. Included singleton b=1,2,3 controls, simultaneous b=1,2,3, complete-batch shortcut, disjoint batches, triangle overlaps, Fano overlaps, unavailable b>G, and nontrivial E_b restrictions. This is finite COMPUTATIONAL evidence independent of the all-size symbolic proof.

Publication paths:
- Executable: experiments/tmr/tmr5_mixedwidth_fuse044.js
- Immutable native-run summary: results/raw/tmr/2026-11-15_0853_TMR5_MIXFUSE044_NODE_RAW.json
- Complete parametric seven-column tariff schema and exact rational certificate: results/raw/tmr/2026-11-15_0853_TMR5_MIXFUSE044_TARIFF_MATRIX.json

The Node source produces expanded complete per-model raw and signed matrix JSON when run with TMR5_OUTPUT specifying a writable directory. The immutable summary is an accurate compact account of the locally executed audit; the much larger generated row dump is not represented as uploaded.

## 6. Ranked dependencies and repairs

| Dependency | Verdict |
| --- | --- |
| TMR-3/047 fixed-b Bellman theorem | **PASS/RESTRICTED**, independently derived as E_b=E special case |
| Exact heterogeneous multi-b credit and complete signed matrix | **PROVED/RESTRICTED**, peer mathematical review OPEN |
| Transfer b=1 credit unchanged into b=1,2 grammar | **FALSIFIED** by real two-action path, original restricted result intact |
| Same-physical-machine auth, indexed access, tapes, head positioning | **OPEN**, cannot identify this preauthenticated calculus with actual SAT computation |
| Superpolynomial initial value | **OPEN**, this restricted measure is at most G+q+1 |
| Transfer to every total fixed deterministic SAT decider | **OPEN**, decisive blocker |
| Historical checker /341 and /386 | **FAIL** full authority; **RESTRICTED** guarded authority, unchanged |
| P versus NP | **OPEN** |

**Weakest surviving lemma:** a genuinely unavoidable **computational** obstruction in an arbitrary source-authentic SAT execution, not prescribed gate records or the cost of reading input. TMR-1/047's tally/NE barrier and TMR-2/047's linear pivotal-sign tariff are preserved as strong hostile ceilings. Polynomially sized shared DAGs and q scales give G+q+1=poly(input length), even with exact fusion credit. Compact affine, circuit, extension, learning, reconvergence, caching, recomputation, rereading, padding, and alternative encodings remain legal controls rather than deleted behaviors.

**Next peer repair:** TMR-4 independently replay the heterogeneous credit and all signed rows; TMR-3 audit actual simultaneous fixed-head b writes, physical access and input authentication; TMR-1 preserve all-program fixed-family complexity ceiling; TMR-2 propose a SAT-specific obstruction surviving cheap global representations. No proof-system or SAT-time claim is promoted from this restricted result.

**ROOT RECONCILIATION:** proof1.txt SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343, complete original proof2.txt Git blob SHA 930c5eeddafce656717f28055a7a9a755f44737c, complete original root main.tex Git blob SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 were recovered and reviewed. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Existing agents, ownership and schedules unchanged. P versus NP remains OPEN.
