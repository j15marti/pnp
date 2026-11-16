# TMR-4/066: authenticated HWB-to-adaptive-FBDD end-to-end transfer

**Date:** November 16, 2026 PST. **Owner:** TMR-4 / PNP Cost-Sound Abstraction, Tracks A/C. **Named dependency:** D4-ADAPTIVE-FBDD-ESCAPE, **CLOSED FOR THE EXACT AUTHENTICATED HWB SOURCE FAMILY**, not for arbitrary circuits. **Status:** KNOWN THEOREM on quadratic HWB FBDD size (Sieling–Wegener 1995; Bollig et al. 1999 Theorem 3.2), together with an explicit restricted source compiler and symbolic proof. PROVED/EXACT restricted; external independent mathematical review OPEN. Executed evidence COMPUTATIONAL. P versus NP OPEN.

## Candidate fixed before primary-source search, and falsifiers

For every n>=1, take an authentic, fully encoded shared fan-in-two Boolean gate DAG C_n computing the hidden weighted bit function HWB_n(x)=x_(sum_i x_i), with sentinel x_0=0. Construct **one fixed uniformly generated, complete, deterministic adaptive read-once FBDD** with no supplied variable order, <=n²-n+1 internal vertices, original pointwise decision and original-input exact count, while charging all source/target costs.

Four falsifiers: (1) repeated queried variable on any legal path or an implicitly preloaded input; (2) falsely applying the all-order OBDD lower bound to an adaptive program; (3) free original-source certification or incorrect gate/auxiliary counting; (4) loss of either distinct labelled arc or costly full serialized output.

The 1999 paper by Bollig, Löbbing, Sauerhoff and Wegener, Theorem 3.2, explicitly attributes an O(n²) FBDD for HWB to Sieling–Wegener. Drechsler–Sieling (2001), Figure 13, supplies an actual adaptive graph ordering. Therefore **the asymptotic FBDD escape is prior art**; the present contribution is an authenticated, tested, fully costed integration, not a newly discovered separation.

## Full source semantics, target model and construction

The source is canonical printable ASCII JSON with exact keys `version,n,gates,root`, version one, each gate with authentic `id,a,b,op` and one of sixteen two-input truth tables. A fixed generator uses a binary ripple counter with r=ceil(log2(n+1)) bits, increments it by each original x_i using source XOR/AND gates, compares the resulting counter with each k=1,...,n via source NOT/AND, gates that equality with the actual x_k and ORs the terms. Gate records are reversed, so no convenient input topological layout is advice. The complete parser checks exact bytes, IDs, opcodes, all reachable original inputs/gates, cycles and n<=2g **before allocating n-sized arrays**. The family recognizer regenerates and byte-compares the entire source. It **rejects valid generic circuits outside the declared family as out of scope**, not UNSAT. There is no implicit all-circuit equivalence test.

Induction over every original increment operation proves the counter equals the number of true original inputs consumed so far; it never overflows r bits. Induction over every comparator and original OR operation proves f_Cn(x)=HWB_n(x), for both outputs. An optional source evaluator actually executes each original gate once for a specified assignment. The target semantically compiles the authentic source; it **does not** assert that it replays every original gate on each target branch.

The FBDD root queries x_n. After t>=1 actual queries store a=#ones read, b=#zeros read, z=last bit; thus t=a+b. If t<n, the **next genuine input query** is x_a when z=1 and x_(n-b) when z=0. At t=n, halt with terminal output z. The index is computed from prior branch values, not from the unread bit. Every internal vertex has exactly one variable label and both 0/1 successor arcs. The target must be distinguished from a two-pass OBDD that rechecks x_(sum): the target never rereads a variable.

### Complete read-once and semantic invariant

At every t>=1 state (a,b,z), all x_1,...,x_(a-1) and x_(n-b+1),...,x_n have been read. If z=1, then x_(n-b)=1 was read and every index in [a,n-b) remains unread. If z=0 and a>0, then x_a=0 was read and every index in (a,n-b] remains unread; when a=0 use the nonqueried constant sentinel x_0=0. This is true for both outcomes of the initial x_n test. When z=1, reading fresh x_a either advances a (result 1, preserving the high pivot) or advances b (result 0, making the low pivot 0). When z=0, reading fresh x_(n-b) either advances b (result 0, preserving the low pivot) or advances a (result 1, making the high pivot 1). These four cases preserve the invariant. Therefore every full path reads each original input **exactly once**, and when a+b=n the two boundaries meet at x_a=z, including the all-zero sentinel case. Hence the FBDD computes exactly HWB_n, both terminal labels and every assignment agree.

At depth t=1,...,n-1 there are at most t states with z=1 and t states with z=0, because a+b=t and z=1 requires a>=1, z=0 requires b>=1. Including the root gives V<=1+sum_(t=1)^(n-1)2t=n²-n+1. These are explicit graph vertices, not implicit symbolic oracle states. No global variable order exists, so Bryant's Omega(1.14^n) all-order **OBDD** lower bound remains entirely valid.

Every original assignment induces a unique complete length-n labelled root-to-terminal path, and conversely the queried labels uniquely specify an original assignment. A source-to-target exact-count DP propagates an integer separately through *both* labelled arcs, even when their destinations merge. The accept terminal count is #HWB_n=sum_(k=1)^n binom(n-1,k-1)=2^(n-1); total paths 2^n. Each integer count requires <=n+1 bits. A cheap structural direct counter remains lawful, and neither the FBDD size nor the source-authenticated exact count implies an arbitrary SAT algorithm lower bound.

## Simultaneous physical resource ledger

Let L be the complete source bit count, including the optional n input bits. A deterministic conventional locally headed multitape machine charges complete parse and failed-source authentication, actual source graph records and fan-out identities, deterministic family regeneration, original source gate checks, graph-node/arc construction and any failed candidates, adaptive selection and arithmetic, head/address registers and seeks, all cached counters and path multiplicities, both outputs, full serialization and final integer emission. The target has V<=n²-n+1 internal vertices and 2V distinct labelled arcs. Each carries O(log(n+2)) bits of label/address overhead and one at-most-(n+1)-bit path count when materialized. With a conservative **single-run** writable-bit budget D=1+L+O(n²(n+log(n+2))), all such physical objects and buffers fit simultaneously; no source gate is double-counted simply because it has multiple fan-out references.

One fixed TM performs source authentication, explicit target construction and serialization, exact count and optional actual-source/target pointwise evaluation with simultaneous T_total=O(D^5+n²) bit steps and S_peak=O(D) writable bits. It is a coarse polynomial upper bound, not measured Python microsteps, and the logical FBDD branch-state count is not the total physical machine space. Network span/per-worker memory, preloaded advice, a SAT oracle, probabilistic error and free random isolation are not used.

## Executed evidence and reproduction

ACTUALLY EXECUTED CPython standard-library exact source revision `tmr4-hwb-fbdd066.v1` (SHA-256 `b8637e823a65fa5772ef2f8d1f6e928c0f1f9c3e52750722a84a6ec23b0f8d1f`), deterministic seed 20261116: **17 canonical source circuits**, n=1..12 plus 16,32,64,128,256; 8,240 original assignments (exhaustive at n<=12, ten seeded assignments per larger n); **16,555 instrumented checks, 0 unexpected failures**, seven malformed/source/certificate corruptions rejected. An independent source-gate interpreter, actual adaptive path executor and graph-shape validator were used. At n=256 the original source has 6,921 gates and the actual graph has 65,281 nonterminal vertices. Two executed paths, the direct script and authenticated compressed-source loader, produced the same complete JSON bytes. Raw SHA-256 `7462ba9cd9b3f0479f6b37c9ee2f54148d8da566442ef1036460e1683ed6059b`.

Files: `experiments/tmr/tmr4_hwb_adaptive_fbdd066.py.zlib.b64`, `experiments/tmr/tmr4_hwb_adaptive_fbdd066_loader.py`, `results/raw/tmr/2026-11-16_TMR4_HWB_ADAPTIVE_FBDD066_RAW.json`. The compressed source is digest checked before execution. A standalone subsection compiled using pdfLaTeX twice. No local Git checkout/preflight (github.com DNS resolution failed), no native physical TM microstep trace, no full repository LaTeX compilation, no independent formal-kernel/external mathematical review. This finite evidence is COMPUTATIONAL, not a substitute for the all-n symbolic invariant.

## Mandatory verification gates and controls

| Gate | Verdict and scope |
|---|---|
| DISJ sanity | PASS restricted. Exponential grouped X:Y rank coexists with cheap DISJ circuits/FBDDs. Static rank cannot imply general circuit hardness. |
| Relativization | PASS for this elementary intermediate. No nonrelativizing NP step; algebrization and Natural Proofs barriers remain OPEN for any separation. |
| Simultaneous DTISP | PASS for one constructed source-to-count/evaluate upper pair. A strict hierarchy forbidden-region or arbitrary-machine lower-bound transfer is OPEN. |
| Deterministic configuration counting | PASS solely as the deterministic upper bound T<=2^O(S+log L); no necessary-work or probabilistic/quantum inference. |

Horn, 2-SAT, affine/Gaussian, equality, bounded treewidth, autarky, products, padding, auxiliary/selector inputs, unique-solution rank-one tensors, local-basis/field restrictions, legal compact algorithms and recomputation remain available. No majority-tie, coherent quantum amplitude or randomized isolation step is imported. /341 FAIL full logical UNSAT authority; /386 RESTRICTED. A fixed-order prefix-rank bound cannot simply be transported to this **adaptive** order. A partition X:Y may instead use charged switch transcripts, generally with many switches. Unrestricted SAT lower bounds and P versus NP remain OPEN.

## Pinned primary references

1. Sieling D, Wegener I. Graph Driven BDDs: A New Data Structure for Boolean Functions. *Theoretical Computer Science* 141 (1995):283-310. Published 1995.
2. Bollig B, Löbbing M, Sauerhoff M, Wegener I. On the Complexity of the Hidden Weighted Bit Function for Various BDD Models. *RAIRO Theoretical Informatics and Applications* 33 (1999):103-115, Theorem 3.2, https://doi.org/10.1051/ita:1999108 (explicit O(n²) FBDD and OBDD contrast).
3. Drechsler R, Sieling D. Binary Decision Diagrams in Theory and Practice. *International Journal on Software Tools for Technology Transfer* 3 (2001):112-136, Figure 13, https://doi.org/10.1007/s100090100056 (actual adaptive graph-order drawing checked).
4. Bryant RE. On the Complexity of VLSI Implementations and Graph Representations of Boolean Functions with Application to Integer Multiplication. *IEEE Trans. Computers* 40 (1991):205-213, Theorem 2, https://doi.org/10.1109/12.73590.

## ONE next load-bearing lemma

**D4-FBDD-SOURCE-CLASS-EXTENSION (OPEN):** identify an efficiently authenticatable structural family beyond the exact HWB gate grammar for which a source-derived adaptive-variable policy has provably polynomial state count, and contrast it with an explicit **exponential-FBDD** source family using the same parser/charging discipline. This is not a universal all-circuit compiler or a P-versus-NP proof.
