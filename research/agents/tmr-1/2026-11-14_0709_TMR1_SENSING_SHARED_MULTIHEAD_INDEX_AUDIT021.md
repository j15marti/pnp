# TMR-1/021: sensing shared-tape heads, local-view failure and repaired delayed-INDEX lower bound

**Date:** 2026-11-14 07:09 PST (America/Los_Angeles). **Role:** TMR-1, Machine Model Lead. **New mathematical claim:** SMH21, **CANDIDATE/RESTRICTED**, independent TMR-3/TMR-5 review requested. **Small counterexample:** FALSIFIED naive sensing-head extension. **Finite experiments:** COMPUTATIONAL. **General SAT separation:** OPEN.

## 1. Exact question and earlier results

TMR-3/019 proved a candidate local-fingerprint bound for a delayed bit-index service with one nonsensing physical head per tape and arbitrary pre-query work space. TMR-1/020 had handled multiple independently parked nonsensing read-only input heads, but bounded the *total* pre-query visited writable cells. The direct TMR-3/019 argument survives arbitrary stored work because a fixed number of physically moving heads sees only bounded neighborhoods in a short query.

This run independently audited the original statement against its actual transition model, then tested the **different, stronger model** of several physically collocated heads on the same tape, with finite-control access to whether two heads collide. A naive extension that forgets head separation is false. A corrected fingerprint incorporates truncated pairwise head geometry and restores a linear post-query bound without any workspace restriction. This is not an original-input 3-SAT computation theorem.

## 2. Smallest collision-sensing counterexample

Use an all-blank, two-way infinite **single writable tape** with two read/write heads and a fixed initial control state. Compare the post-preprocessing configurations:

- state A: head coordinates (0,0);
- state B: head coordinates (0,1).

Both heads read blank in both states. Their complete separate radius-one symbol windows are identical, as are the control state and every source window. Yet the permitted sensing predicate `head1==head2` is true for A and false for B. A fixed one-transition machine can output different terminal bits in A and B based solely on the sensed collision.

Therefore **equality of all individual local symbol windows is insufficient for transition coupling on a shared, sensing multihead tape**. This does not falsify TMR-3/019, which explicitly assumes ordinary one-head-per-tape, nonsensing work tapes. It does falsify an unqualified transfer to a sensing multihead architecture.

**Repair:** preserve each pair's initial relative displacement if its absolute value is at most `2t`; otherwise preserve its FAR-LEFT/FAR-RIGHT sign. For query budget `t`, those classes determine every possible head collision in at most `t` charged steps.

## 3. SMH21 model and new candidate theorem

Fix **one finite deterministic total uniform machine** `A` over all source lengths. The immutable original binary source `x` occupies cells 1 through `L`; position 0 is the left endmarker, position `L+1` is the right endmarker, and positions outside are fixed blank. It has `r>=1` locally moving original-source heads, possibly sharing source tapes, and `w>=0` locally moving writable heads, possibly sharing writable tapes. Each head moves at most one physical cell per unit-cost transition. Writable alphabet size is at most `g` including blank; `q` is the finite number of states. The control may sense coincidence of heads **on the same physical tape**, but not absolute numerical coordinates, separation magnitudes, or coincidences across physically distinct tapes. Concurrent writing to one cell follows one fixed finite deterministic conflict rule. One-sided work-tape endmarkers can be treated as one extra local symbol.

The machine preprocesses `x` for arbitrary **charged** time with arbitrary finite visited writable space, without learning the later query index. It then receives `p in {1,...,L}` through a separate ordinary read-only query tape whose initial content/head state depends only on `p`, not on `x`. Its physical query computation must output `x[p]` correctly for **every** source and later query and halt. The source and work heads may park at arbitrarily large input-dependent coordinates after preprocessing. Input rereads, all work-head movements, writes, output and query-tape movements count as actual transitions.

Let `h_j` be the number of original-source or writable heads on physical tape `j`, and define the fixed head-pair count

$$
H=\sum_j {h_j\choose 2},\qquad D=r+w\log_2(g+1)>0.
$$

Let `t=t_A(L)` be the **maximum actual charged query transitions** across all `x in {0,1}^L` and `p in [L]` for that same machine. The theorem is

$$
\boxed{2^L\le q\,(L+2t+4)^r\,(4t+3)^H\,2^{r(2t+1)}(g+1)^{w(2t+1)}.}
\tag{SMH21}
$$

For each fixed machine, regardless of its preprocessing work-space magnitude and with `r,w,g,q,H` independent of `L`, this entails

$$
\boxed{t_A(L)\ge \left(\frac{1}{2D}-o_A(1)\right)L.}
$$

This is a **linear** bound in the optional delayed-INDEX service, not a superpolynomial bound for SAT.

## 4. All-transition coupling proof

For any fixed `L,t` and preprocessed source `x`, define the finite fingerprint of its *actual* query-boundary configuration to contain:

1. The entire finite control state.
2. For every source and work head, all `2t+1` physical tape symbols at offsets `-t,...,t` from that head. For work tapes use the actual mutable contents produced during preprocessing, not an abstract source sketch.
3. For every unordered pair of heads on the **same physical tape**, the exact signed initial coordinate difference when its absolute value is at most `2t`, and otherwise `FAR-` or `FAR+`. No position coordinates are given to the machine as free information.

Two boundary states with equal fingerprints, supplied the **same later query tape**, have identical legal query transitions for `t` steps. Proof by induction on transition number `i<=t`: finite states and local scanned symbols agree initially. Every head's displacement from its own boundary coordinate is the same in both runs by the common previous transition instructions. Thus any source cell inspected at step `i` lies in an equal initially recorded radius-`t` source window. For mutable work cells, a current read either sees its equal initial local-window symbol or a preceding write. A write by another head can affect the currently inspected cell only if their *initial* separation was at most `2t`; for these pairs the exact signed separation and both sequences of relative movements agree. If the separation was larger than `2t`, collision is impossible in either execution during the budget. Therefore all previously written values, simultaneous-write conflicts and head-collision sensors agree as well. Same read symbols, sensor predicates and control imply identical writes, movements, halt status and output in the next transition. The induction includes adaptive rereads and every paid query-phase transition. Preprocessing need not have the same trace.

If two different `L`-bit sources `x!=y` yielded the same fingerprint, choose a coordinate `p` where their bits differ. Coupling forces equal output on this identical later query, contrary to exact two-label INDEX correctness. Hence the fingerprint map from all `2^L` sources is injective.

Count at most `q` control states and at most `(4t+3)^H` pairwise relative-geometry records: exact differences `-2t,...,2t` plus two far classes. A source head has at most `L+2t+4` physical positional types (all near coordinates and two far-end classes), and at most `2t+1` freely varying binary source symbols in its local view. Each work-head neighborhood has at most `(g+1)^{2t+1}` possibilities including any one-sided boundary symbol. This proves SMH21. Overlapping windows and mutually inconsistent geometry records are harmless **overcounts**.

For `t<L`, logarithms yield the explicit same-machine inequality

$$
t\ge \frac{L-\log_2q-r\log_2(3L+4)-H\log_2(4L+3)-D}{2D}.
$$

If `t>=L`, the asymptotic claim is immediate. No pre-query `S=o(L)` premise is used, and no time from another machine or input is borrowed.

**Model boundary:** This proof does not include numeric head-position sensors, free distance comparisons, a late query that itself carries source-dependent advice, free random access, infinitely many heads, or cross-tape head-collision predicates. Those would require new fingerprints and, in some cases, invalidate the bound.

## 5. Independent execution and hostile controls

The exact **published CommonJS source** was executed as original JavaScript functions in hosted V8, not under native Node, with direct physical current-cell reads/writes of one **shared writable tape**, two read-only source heads sharing one source tape, and same-tape collision sensing. For reproducibility, its function bodies are the exact functions used in the executed V8 test; it requires no packages and can be run with `node experiments/tmr/tmr1_shared_multihead_locality021.cjs`.

- `L=5..9`, six deterministic preprocessing layouts, `t=0..3`: **120** parameter cases.
- **1,649** equal corrected-fingerprint opposite-source collision pairs.
- **5,380** paired post-query simulations, checking **10,459** physical transitions, zero failed assertions.
- **650** colliding-work-head controls and **40** far-source-parked controls, plus **650** overlapping-head layouts.
- One explicit naive-fingerprint falsifier: work heads (0,0) versus (0,1) on an all-blank two-way tape.
- Nonrandom exhaustive source enumeration within every tested length/mode. The simulated phase-2 controller has a fixed finite observation-based transition rule. This does **not** execute a universal TM compiler or charge host-language preprocessing and is **COMPUTATIONAL** only.

The direct original peer source `experiments/tmr/tmr3_local_fingerprint019.cjs` and raw file `results/raw/tmr/2026-11-14_0634_TMR3_LOCAL_FINGERPRINT019_RAW.json` were inspected. Its theorem for **nonsensing ordinary heads on separate tapes** is mathematically supported by the same coupling induction, but no claim is made that the peer's executable was rerun natively in this run. A separately written native CPython implementation of the present sensing-head control was also executed locally (120 cases, 1,649 collisions, 5,380 paired queries, 10,459 transitions, zero failures), **LOCAL ONLY**, not presented as the published GitHub runnable. Neither finite program establishes an arbitrary-machine runtime lower bound.

**Published executable:** `experiments/tmr/tmr1_shared_multihead_locality021.cjs`, Git blob `98a5f320278ff23a42b3cee0ff72981e0bc9b654`.

**Published immutable raw:** `results/raw/tmr/2026-11-14_0707_TMR1_SHARED_MULTIHEAD021_RAW.json`, Git blob `376c3608b247a69e208a29436b01b00540a2470f`.

## 6. Relation to the unrestricted target

The team's actual separation target, for **each one fixed total correct deterministic standard-encoding 3-SAT decider A**, is

$$
\forall k\ge1\ \forall C>0\ \forall L_0\ \exists F\in\mathrm{3CNF}_{valid}:
\quad |F|\ge L_0\ \wedge\ T_A(F)>C(|F|+1)^k.
$$

SMH21 proves only that a **different two-phase INDEX service** with all-input, all-late-index correctness has a query requiring `Omega(L)` operations. It does not imply that a 3-SAT solver must implement that service; even a full `Theta(L)` cached source is allowed, and SAT may use Horn, 2-SAT, XOR Gaussian elimination, bounded-treewidth DP, products, reencodings, shared circuits, rereads, auxiliary variables or any polynomial work space. `S_A(F)<=O(T_A(F))` on the same locally moving machine does not amplify a linear query lower bound into an all-exponent separation.

**Dependency DAG:** Correct finite local model -> (new pairwise-geometry certificate) -> every query-phase transition coupled -> injective source fingerprint -> linear delayed-INDEX query lower bound. The arrow from delayed INDEX to a compulsory SAT/UNSAT *semantic-processing* charge is **OPEN**; an additional superpolynomial lower bound for that charge is **OPEN**. There is no proof of P=NP or P!=NP here.

## 7. Primary sources and corpus audit

[1] Fischer, P. C., Meyer, A. R., and Rosenberg, A. L. (1972), *Real-Time Simulation of Multihead Tape Units*, Journal of the ACM. Primary abstract: https://research.ibm.com/publications/real-time-simulation-of-multihead-tape-units . It treats multihead-tape models and real-time simulations; SMH21 is proved directly and does **not** borrow an uncharged simulation theorem.

[2] Fortnow, L., Lipton, R., van Melkebeek, D., and Viglas, A. (2005), *Time-Space Lower Bounds for Satisfiability*, JACM 52(6):835-865, https://doi.org/10.1145/1101821.1101822 . Its SAT theorem restricts simultaneous low time and small space in a random-access model, **not** arbitrary polynomial workspace or unrestricted all-exponent SAT time.

[3] Van Melkebeek, D., and Raz, R. (2005), *A Time Lower Bound for Satisfiability*, Theoretical Computer Science 348(2-3):311-320, https://doi.org/10.1016/j.tcs.2005.09.020 . The one-dimensional/d-dimensional work-tape hypotheses do not establish an all-machine SAT separation.

**Repository primary artifacts reviewed:** replacement directive on main (first and rechecked), full `proof1.txt` (28,714 chars, SHA `06f7ebc8c2283304a0f5200b518c6e48fa41e343`), full `proof2.txt` using authentic Git blob (1,051,196 chars, SHA `930c5eeddafce656717f28055a7a9a755f44737c`, file-content endpoint blank), full canonical root `main.tex` using authentic Git blob (2,536,131 chars, SHA `f0054c990e11602b4b60ead3bccffa73f11d0d7b`, file endpoint blank), `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, issue #3 through TMR-4/021, latest five TMR handoffs, and original reports/source/raw TMR-1/020, TMR-3/019, TMR-4/021 and TMR-5/017; relevant historical counterexample and FLMV/ARC limitations retained in root trackers. Obsolete LSPV allocations have no role authority.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Neither tracker was written. Canonical `main.tex` is reserved for TMR-5 synthesis; no TMR-1 edit was necessary and no historical section was changed. Full local checkout, project preflight executable and LaTeX build were **not run**, because the repository was not available to the local runtime and direct Git network access failed; connector reads and exact repository write/readbacks were successful. No tasks/schedules modified.

**ONE NEXT TARGET:** TMR-5/TMR-3 independent review of the shared-tape sensing-pair locality induction, especially cross-head writes and noncolliding far pairs. TMR-2 still needs an all-correct-SAT-decider semantic transfer without externally delayed INDEX requests. Keep SMH21 CANDIDATE/RESTRICTED and the unrestricted arrow OPEN.

END_OF_REPORT::TMR-1::021::2026-11-14_0709_PST
