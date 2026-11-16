# TMR-4/062: live shared-component interfaces and an end-to-end polynomial compiler

Date: November 15, 2026, 21:28 PST. Owner: TMR-4 / PNP Cost-Sound Abstraction. Direct follow-up to the user's “Try that” on D4-SHARED-CORE-EXTENSION. Status: PROVED/EXACT in the declared construction model; independent mathematical peer review OPEN. Executed tests are COMPUTATIONAL. P versus NP remains OPEN.

## Connected result

The earlier /061 compiler retained all k original shared values permanently. This run replaces that bound with the number q of shared target values which still have an unfinished component consumer. It closes D4-SHARED-CORE-EXTENSION for a recognizable binary in-tree shared-core class, and supplies a correct parameterized fallback for arbitrary authenticated DAGs. It does not claim that all circuits have small q.

The pipeline is original bytes -> authentication -> original-vertex ownership and shared-reference component decomposition -> paid core recognition and schedule discovery -> actual READ/GATE/REF/STORE/DROP/OUTPUT program -> BFS on genuine stage transitions -> complete labelled OBDD -> exact evaluation/count and prefix-rank statement. There is no source-answer oracle, prescribed expensive proof obligation, or uncharged gate unrolling.

## Candidate and falsifiers

The initial candidate was to replace total sharing by simultaneously live shared dependencies while preserving every original operation and exact path count. Falsifiers fixed before research were premature eviction, omitted recomputation/access costs, and loss of terminal or counting semantics. DISJ's legal small circuit remained a standing control. The full current directive, own manuscript, relevant peer sections, five main handoffs, recent issue #3, pending PR metadata and original /061 report/code/raw were consulted. Main3's stale handoff is not treated as its latest merged research; its newer /060 work remains a draft. The old TMR-4 PR158 studies a fixed-partition signal cut, not this temporal interface.

## Exact model and theorem

Retain /061's canonical ASCII JSON version-one grammar: n original input identities, g binary truth-table gates, arbitrary record order, sparse canonical gate IDs, repeated operands, arbitrary fan-out, one gate root, an acyclic graph with every input/gate root-reachable. Reject malformed inputs as malformed. Check n<=2g before input-indexed allocation. Let L be complete source bits and M=n+g.

A shared original vertex occurs in at least two operand positions, including repeated operands; there are k such identities. Targets are those k vertices and the root. Local component T_t expands original predecessors only until another shared vertex, which becomes a REF leaf. Every original vertex is evaluated once at its owner; every REF occurrence remains charged. Distinct dependency s->t means T_t references s. Let H be this shared-component graph, R the number of actual REF occurrences, and r the maximum local Sethi-Ullman label.

For a completed topological component prefix I, let F(I) be completed targets with at least one unfinished component consumer, retaining the root through OUTPUT. Put q=max|F(I)|. After a component finishes, decrement each distinct predecessor's consumer count, DROP only at zero, then STORE the new result. The actual emitted instruction count is exactly

    I = n + g + R + 2k + 2,     R <= 2g.

There are n READs, g original GATEs, R REFs, k+1 STOREs, k DROPs and one OUTPUT. The local scratch bound is r<=1+floor(log2(n+2g)). Conservative live Boolean width W=q+r+1 yields

    V <= n*2^W;     B(x)=C(x);     #B=#C.

For every field, every prefix of the actual discovered input order has assignment-matrix rank at most 2^W. This says nothing about arbitrary nonprefix cuts or necessary resources of all equivalent algorithms.

### Complete proof mechanism

A nonshared vertex has at most one operand-use consumer, so following its unique forward path assigns it to exactly one first shared target or root. Shared vertices are computed at their own target, not duplicated. Each REF leaf maps to a source operand occurrence, proving R<=2g and at most n+2g local leaves. Larger-local-label-first evaluation uses at most r scratch values; original argument order is restored for noncommutative gates.

At a component's start every referenced predecessor has an unfinished consumer, namely the current component, so it is cached. All references finish before DROP. No future component can need a dropped value. Induction over every original READ/GATE and every actual cache instruction proves intermediate-value agreement, empty initial-state correspondence and both terminal labels. The cache has at most q values before a component and the stack at most r; the staging slack adds one. REF copies occupy actual separately charged stack cells.

The program counter, cache identity set and stack depth are public at each fixed READ stage. The target state stores exactly the live value tuple, not expired slots. Real instruction execution constructs both successor tuples. Complete labelled paths correspond bijectively to the n original input bits, even when successor nodes merge. Thus integer path propagation through BOTH arc labels preserves exact counts. Rows at a prefix factor through reachable live tuples, proving the all-field rank statement. No state is merged merely because two residual counts happen to agree.

### Recognizable many-share class

Check that H has at most two distinct predecessors per target and exactly one distinct consumer per shared target. Acyclicity/root reachability then make it a rooted binary in-tree. A second larger-label-first schedule, now on H, gives

    q <= 1+floor(log2(k+1)),
    W <= 3+floor(log2(k+1))+floor(log2(n+2g)),
    V <= 8*n*(k+1)*(n+2g).

Proof: a finished child result is retained only for its unique parent. With child labels a>=b the peak is max(a,1+b); unary nodes retain the same label. A label-h tree has at least 2^(h-1) leaves. All labels and the decomposition are discovered from source records, with no layout advice. These are established tree-scheduling ingredients integrated into an authentic shared-circuit compiler, not a claim of a new general DAG register-allocation theorem.

The recognized class can have k=Theta(M), unlike /061's sufficient small-k condition. Combining the new certificate with the general fallback also retains all earlier k=O(log L) cases. Arbitrary reconvergent cores may still have large q.

## Same-realization resource ledger

Let A=n*2^W and

    D = 1+L+O(M^2 log(M+2)+A*(W+n+log(A+2))).
    T_total = O(D^5+n^2),     S_peak = O(D).

One ordinary deterministic locally headed multitape realization performs parsing, graph authentication, decomposition/label discovery, reference counting, fallback checks, original/cache instruction recording, exact BFS, comparison and storage of state tuples, both arcs, exact n+1-bit counters, source/head addressing and output. At most 2A arcs execute at most I=O(M) instructions, with at most A candidate-state comparisons; a deliberately conservative O(D^2) bit scan cost per primitive gives the displayed bound. Logical W excludes source/control/address tables, which are included in D. No original gate is recomputed in this implementation, and no alternative algorithm's recomputation is declared free. The output variables remain exactly the n originals; no CNF auxiliary growth is used. The OBDD output contains two labelled arcs per node. This is a simultaneous constructive upper budget, not a measured physical TM trace or a forbidden DTISP pair. For the certified tree-core class it is polynomial in L.

## Falsifiers and controls actually executed

A four-gate source has g0=x0 AND x1, g1=g0 XOR x2, g2=g1 AND g1, and output g3=g0 OR g2. The core value g0 has two different consumer components. The certificate correctly fails; the general fallback returns the exact count five. A mutant DROP after finishing g1 fails at the later actual REF g0. Genuine cross-component reuse cannot be erased by a tree-only eviction rule.

A constant-one gate with repeated input x0 accepts two assignments. Its two labelled arcs may share a destination but cannot be counted once. All sixteen binary opcodes were tested, including noncommutative operand-order controls. Named controls cover DISJ, equality, independent products, Horn/2-SAT cycles, affine parity, unique-solution conjunction, and a selector with canceled padding. General Gaussian/autarky/auxiliary/semantic rewriting algorithms remain legal but are not claimed exhaustively implemented.

## Concrete extension witness

Replace every binary-tree node with p=a AND b, z=a XOR b, t=p OR z. Then g=3(n-1), k=2n-2, and the shared core is the original binary tree. At n=128:

| Shape | Shared vertices k | q | Local r | Actual Boolean width | Constructed OBDD nodes |
|---|---:|---:|---:|---:|---:|
| Balanced | 254 | 8 | 3 | 11 | 2187 |
| Comb | 254 | 2 | 3 | 5 | 255 |

Both exact counts equal 2^128-1. These are unreduced constructed node counts, not minimum-size lower bounds. The modules compute OR, so an even cheaper direct OR algorithm is legal. Random opcode modules independently test the broader structural result.

## Actual execution and provenance

Local CPython 3.13.5, seed 202611152112, revision tmr4-live-core062.v1: 251 canonical sources, 6968 exhaustive assignments, 11386 constructed arcs, 1294 finite-field ranks, 730 independently enumerated small-core topological orders, 13 malformed rejections, 631130 instrumented checks, zero unexpected failures. Two completed audits were byte-identical. The initial pre-audit harness had a wrong root-name literal and was fixed; no failing mathematical test was suppressed.

Independent serialized checker: 28 actual CLI compilations, 2032 assignments, 572 serialized arcs, 2472 checks, zero failures. It does not import compiler semantics; original evaluation uses separate readiness scans. This is independent implementation checking within this run, not external peer review.

Executed compiler blob cccf879676960f57de141e74816ad77b75946349; verifier 984ca0cb76233351b606c69e25e81ea3b405ca0d; primary raw c455c4e1796f743fbbcaaef410a64ee29a51e511; independent raw e2f858566e766ee534fa4190dad51a41917059a9. Code/raw filenames appear in the maintained main4 manuscript and handoff. Primary reads pinned at 82dcb3fb232297f9eaed04b29dbd5a365de9cdcb; publication branch starts from 78cc3151bb97e0be3d5f9eab226c0922d93e9bc6. The owned manuscript's prior blob was unchanged when the branch was created and is archived byte-identically, along with the full prior handoff.

Two local pdfLaTeX draft-mode builds succeeded. Repository checkout/preflight was unavailable due local GitHub DNS failure. No native TM microtransition trace, proof-kernel build, or external mathematical peer review was performed. The prototype's explicit million-node cap and Python numeric limits are not theorem-domain restrictions and never denote UNSAT.

## Four gates

| Gate | Verdict | Reason |
|---|---|---|
| DISJ | PASS restricted | Actual-order rank only; no static-rank-to-general-hardness transfer. |
| Relativization | PASS intermediate; unrestricted OPEN | No nonrelativizing NP step or algebrization/Natural Proofs escape. |
| Simultaneous DTISP | PASS upper-bound construction; lower bridge OPEN | One jointly charged T/S realization; no forbidden pair. |
| Deterministic configurations | PASS upper-bound guard only | T<=2^O(S+log L) is not a necessary-work lower bound and is not applied to quantum/randomized machines. |

/341 remains FAIL as full UNSAT authority; /386 RESTRICTED. Unique-solution rank one, local-basis field restrictions, charged isolation, legal compact representations and alternate recomputation remain intact.

## ONE next dependency

D4-RECONVERGENT-CORE-DISCOVERY: find a paid, source-authenticated low-width decomposition when shared results have multiple distinct later component consumers. Correct fallback exists, but a generally small interface bound does not. Arbitrary-circuit necessity and P versus NP remain OPEN.

## Primary references

1. Sethi and Ullman, JACM 17(4), 1970, DOI 10.1145/321607.321620. Known tree scheduling.
2. Appel and Supowit, Software: Practice and Experience 17(6), 1987, DOI 10.1002/spe.4380170607. Author manuscript revised September 24, 1986, https://www.cs.princeton.edu/~appel/papers/sun.pdf; recurrence/tree assumptions consulted directly, including PDF screenshot.
3. Bryant, IEEE Transactions on Computers 35(8), 1986, DOI 10.1109/TC.1986.1676819. OBDD background.
4. Sethi, SIAM J. Comput. 4(3), 1975, DOI 10.1137/0204020. General DAG allocation is a different problem; no unproved optimal-layout algorithm imported.
