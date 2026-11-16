# TMR-5/055: Genuine nonaffine Williams-image revisits admit a uniform four-state compiler

2026-11-15 18:52 PST, America/Los_Angeles. Track B primary, Track A/C controls. Status: PROVED/EXACT RESTRICTED for the symbolic construction, external mathematical review OPEN; finite tests COMPUTATIONAL. P versus NP OPEN.

## Candidate and falsifiers before primary-source audit

Named TMR-3/057 dependency C3-NONASSOCIATIVE-SHARING: for all b>=3, B>=1 and binary x of length B, construct a total, uniform, blank-work-tape computation with genuine two-time predecessor revisits and a nonaffine transition. Determine whether the combination forces hard evaluation, as opposed to one specified unrolling algorithm.

F1: last-work-cell predecessor is not a genuine physical previous visit.
F2: transition is affine, or either predecessor is phantom.
F3: small compiler uses free source access, hidden advice or preloaded checkpoints.
F4: sharing collapses the wrong count or only a special promise output.

All four are defeated in the present restricted family. No statement about every nonaffine image is implied.

## Authentic source and physical model

For every b>=3, B>=1 and x=(x_1,...,x_B), source word

\[
X_{b,B,x}=1^{b-1}0 \prod_{j=1}^B(x_j1^{b-2}0),\qquad N=b(B+1).
\]

A fixed deterministic locally headed read-only-input parser verifies header, record lengths, fillers and terminal input, rejects all malformed sources and derives b and B through ordinary O(log N)-bit counters. Conservative validation: O(N^2) time, O(log N) writable space. After a paid source rewind, a fixed finite-control processing suffix starts with a blank work tape, moves its head right b-1 genuine cells on the header, and at the first symbol of each b-character record reads and updates one work cell. The filler steps are stationary; the delimiter moves one work cell and reverses direction. The active positions alternate b-1,b,b-1,b,... . Current finite-control bit p is the previous output. Reading the old work-cell value a, update and write

\[
z=(p\land a)\oplus x_j,\qquad p\gets z.
\]

With c_{-1}=c_0=0, the prior same-cell visit is j-2, giving the exact authentic recurrence

\[
\boxed{c_j=(c_{j-1}\land c_{j-2})\oplus x_j.}
\]

Every stage j>=3 has a true state edge from j-1 and last-work-cell revisit edge from j-2. For j>=3 all four parent pairs are attainable on legal prefixes, since each next source bit independently toggles its successor state. The Boolean mixed derivative of (p AND a) XOR x is one, hence the rule is genuinely nonaffine (degree two over GF(2)). The original source-processing suffix spends N+O(1) paid source steps, exactly b-1+B work-head movements and visits b+1 work cells. Authentication is additional paid preprocessing and is not excluded from a total-decider budget.

This is a physical-processing-suffix instance of the Williams Section 3.2 previous-block graph. It is NOT a claim to have compiled native finite transition microcode for the full parser or proved a universal Williams-image simulation theorem.

## Lemma A: exact exponential no-cache expansion

A specified no-cache recursive evaluator that asks for both genuine predecessors at each positive stage, including repeated ones, has Q_{-1}=Q_0=0 and

\[
Q_j=1+Q_{j-1}+Q_{j-2}=F_{j+2}-1.
\]

For b=s,B=s^2,N=s^3+s, Q=2^{Omega(N^{2/3})}. This is a query count of ONE prescribed evaluator, not mandatory machine work or an optimum Tree Evaluation bound. Authentic nonaffine transitions do not remove the Fibonacci graph.

## Lemma B: the legal complete same-source shortcut

A second fixed uniform machine validates the identical binary source, resets its source head if required, and stores two bits (p,a), initialized zero. On real input record x_j it updates

\[
(p,a)\gets ((p\land a)\oplus x_j,\ p).
\]

Inductively this equals (c_j,c_{j-1}) and the machine outputs p=c_B on every authentic word; malformed inputs reject. A single, standard locally headed, deterministic execution has simultaneously

\[
\boxed{T_{\mathrm{direct}}=O(N^2),\qquad S_{\mathrm{direct}}=O(\log(N+2)).}
\]

This includes full parsing, grammar recognition, source scans or rewind, bit-time counters, state updates and output. The simulator need not recreate the physically visited b+1 cells of the original program when only its output is required. Failed recognition attempts and source switching are fixed and charged. It introduces neither random-access queries nor nonuniform advice.

## Lemma C: uniform costed four-state OBDD, ranks and exact count

Given an authenticated declared b,B family, build the natural-order read-once branching program whose stage-j state is (p,a) in {0,1}^2 and whose two labeled successors are ((p AND a) XOR z,p) for z=0 or 1. Output one iff final p=1. By induction it computes the ORIGINAL source-to-output function on all 2^B payloads, not just the observed x. The construction has at most 4B internal nodes and 8B arcs, sharing common states exactly once. It is uniform and authenticated, with a conservative complete locally headed source-to-OBDD compiler ledger T=O(N^3), S_peak=O(N^2), covering parsing, parameter discovery, addresses, node/arc emission, wire-size logs, output validation and representation storage. There is no compulsory complexity lower bound in these numbers.

For any prefix/suffix cut in the original read order, the residual suffix function depends on the prefix solely through the pair (p,a). Hence the fixed-formula assignment-evaluation matrix has rank at most 4 over EVERY field. This is only for these cuts; no arbitrary-cut or SAT-encoding claim follows.

For every prefix of length B-1, exactly one final bit x_B makes c_B=1, because that bit appears as an XOR. Thus

\[
\boxed{\# f_{b,B}=2^{B-1}.}
\]

The four-state weighted DP can compute exact counts with B+1-bit integers and polynomial time and space, but the closed form is itself an even cheaper legal method.

## Full same-realization ledger and independent tests

| Execution and output | Charged time | Peak writable space |
|---|---|---|
| Original authentic machine and work trace | source validation O(N^2) plus suffix N+O(1) | O(log N) parser plus b+1 original work cells |
| Fixed no-cache graph evaluator | Omega(Q), conservatively O(N^2 Q+N^2) including source/node access | O(B log N) recursion/index state |
| Legal direct source-aware decider | O(N^2), including all source validation and output | O(log N) |
| Uniform declared-family OBDD compiler | O(N^3) including all addresses, parsing and emission | O(N^2) |
| Exact weighted four-state count | polynomial in B with B+1-bit counts | O(B), no preloaded count oracle |

Do not combine the expensive evaluator's work with another machine's memory to claim a forbidden simultaneous DTISP pair.

The independently authored hosted V8 verifier was EXECUTED, not merely inspected: revision tmr5-nonlinear-fibonacci055.v2-js, seed none (exhaustive), 78,140 assertions, 0 failures, 4,088 complete authentic source words (b=3..6, B=1..9), 24,608 genuine predecessor checks, 180 malformed-input rejections, 108 GF(2) and GF(101) exact rank controls, all four preceding parent states reachable, half of all payloads accepted, and Q_64=27,777,890,035,287 verified symbolically without executing the exponentially large recursion. Finite tests are COMPUTATIONAL.

Published source: experiments/tmr/tmr5_nonlinear_williams_obbdd055.js (Git blob 1d5755c703821ca60995d001e35ab548f24c996c). Immutable raw: results/raw/tmr/2026-11-15_1852_TMR5_NONLINEAR_OBDD055_V8_RAW.json (blob 17f68641db62e73b5b3eac61d8ad57212fe985d5). Both exact GitHub readbacks passed on branch research/tmr5-nonlinear-williams-branching055-20261115.

No repository checkout preflight, native TM transition-microcode execution, Lean kernel or LaTeX compile took place. External independent mathematical peer review OPEN.

## Four required gates

| Gate | Verdict and scope |
|---|---|
| DISJ sanity | PASS RESTRICTED: this is a cheap representation and not rank-to-work. DISJ retains its compact circuit and interleaved BP. |
| Relativization | NOT APPLICABLE WITH REASON: no P-versus-NP separation is claimed; future NP promotion must satisfy nonrelativization, algebrization and Natural Proofs safeguards. |
| Simultaneous DTISP | PASS within each declared implementation; OPEN for general Tree Evaluation and SAT transfer. Separate executions are not spliced. |
| Deterministic configuration counting | PASS upper bound safeguard only: T<=2^{O(S+log N)} for deterministic total read-only-input machines, neither a lower bound nor a randomized/quantum rule. |

Affine/Gaussian, Horn/2SAT, treewidth, equality, autarkies, product/padding, auxiliary/selectors, unique-witness rank-one, finite-field/local-basis and compact-sharing controls are allowed. The new cheap example is NONaffine, so degree two alone does not rescue a hardness inference. /341 FAIL as unrestricted UNSAT authority; /386 RESTRICTED.

## Ranked dependent pipelines

1. TMR-1 C1, source/compiler/hierarchy: compiler authentic exact counting PASS RESTRICTED; pinned upstream Lean CI was observed. Independent full transitive Lean 4.33.1 kernel/axiom replay, FinTM2-to-physical semantics and independent hierarchy audit OPEN.
2. TMR-3 C3, checkpoint provider plus evaluator: authentic Williams-image nonaffine recurrence and four-state source-aware shortcut PASS RESTRICTED; generic adaptive value provider and improved nonassociative TreeEval evaluator OPEN. Nonaffinity AS A SUFFICIENT HARDNESS PREMISE FAIL.
3. TMR-4 D4, cost-sound transfer: exact four-state ordered read-once BP constructed here and read-once formula/no-advice Ershov compiler PASS RESTRICTED; unrestricted adaptive shared-DAG compiler OPEN.
4. TMR-2 D2, constructive invariant: authenticated twin-cycle quotient exact count PASS RESTRICTED; invariant proving mandatory cost for arbitrary dynamic machines OPEN.

ONE highest-value next lemma: independently rebuild pinned Anthropic MainResults.mainTheorem with Lean 4.33.1 and #print axioms and audit transitive trusted imports and actual FinTM2 stack-to-ordinary-TM per-step costs. This addresses the highest-ranked C1e conditional transfer. C3-NONASSOCIATIVE-SHARING remains OPEN for general Williams images; this example falsifies merely assuming that nonaffinity itself forces hard work.

## Primary sources and scope

[1] Ryan Williams, Simulating Time With Square-Root Space, STOC 2025, Sec. 3.2, https://arxiv.org/html/2502.17779 .
[2] TMR-3/057 original authentic affine Williams-image report, separate unmerged stacked PR #180, https://github.com/j15marti/pnp/pull/180 ; source blob 425cce63870c7236f3321974276580183bfd55fc.
[3] TMR-4/057 source-to-OBDD formula and compact compiler, merged PR #175 and #176, https://github.com/j15marti/pnp/pull/175 .
[4] Anthropic pinned formal-math source revision 16a5ce41304fcdaea4e0be7c132e1c361dc26da5, https://github.com/anthropics/formal-math/tree/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth .

P versus NP remains OPEN; none of the five enabled research schedules, peer manuscripts, retired proof trackers or historical root files were edited.
