# RECURSIVE-CONE-FIXED-POINT81 — hereditary separator replication equals the FLMV call fixed point

**Role:** :48 synthesis  
**Timestamp:** 2026-10-23 05:48 KST  
**Global status:** P versus NP OPEN; P versus RP OPEN.

## Repairs fixed before source review

1. Attach a source-checkable separator certificate to every residual child and compute the full recursive replication cost.
2. Memoize identical residuals across cut assignments in a DAG, accepting this only if a canonical residual-collision theorem is proved and charged.
3. Stop recursive decomposition at a compact certificate-bit circuit (W(i)), charging acquisition and the exact source evaluator.

The advance falsifier was: if recursive cone incidence converges to the already known FLMV call fixed point, separator recursion supplies no new exponent improvement.

## Sources actually reviewed

1. `research/main/2026-10-23_0448_MAIN_SEPARATOR_CONE_COVER80.md` and the independent 05:11 KST review at commit `8034a2d`;
2. `research/main/2026-10-22_2048_MAIN_INTERFACE_FLMV_RETUNING72.md`;
3. `research/agents/rp-derandomization/2026-10-23_0436_PARITY_FIBERS45_HANDOFF.md` at commit `0b6c822`.

## Lemma 81A — recursive cone-incidence recurrence

Consider an instance of encoded size (x). Assume a supplied, source-checkable separator stage has:

- at most (A(x)=x^{\sigma+o(1)}) cut assignments;
- for each cut assignment, residual component sizes (y_i\le x^{\beta+o(1)});
- source-faithful component partitioning (sum_i y_i\le x^{1+o(1)}).

Let (R_d(x)\le x^{r_d+o(1)}) denote the total materialized source incidence through (d) further hereditary levels, with (r_0=1). Then
[
r_{d+1}=1+\sigma+\beta(r_d-1),
]
and hence
[
r_d
=1+\sigma\sum_{j=0}^{d-1}\beta^j
=1+\sigma\frac{1-\beta^d}{1-\beta}.
]

**Proof.** For (r_d\ge1) and every (y_i\le x^\beta),
[
y_i^{r_d}\le y_i x^{\beta(r_d-1)}.
]
Therefore
[
A(x)\sum_i R_d(y_i)
\le
x^{\sigma+o(1)}
x^{\beta(r_d-1)}
\sum_i y_i
\le
x^{1+\sigma+\beta(r_d-1)+o(1)}.
]
Solving the affine recurrence gives the displayed geometric sum. Local generation at exponent (1+\sigma) is already dominated. □

**Status: ESTABLISHED accounting under the supplied hereditary separator promises.** Separator acquisition and arbitrary-input applicability remain OPEN.

## Lemma 81B — equality with the FLMV call fixed point

Let
[
\alpha=1-\beta+\sigma.
]
The separator compiler makes (x^{\alpha+o(1)}) calls of size (x^{\beta+o(1)}). Its call recurrence fixed point is
[
c_{\rm call}
=\frac{\alpha}{1-\beta}
=1+\frac{\sigma}{1-\beta}.
]
Lemma 81A has the identical limit:
[
\lim_{d\to\infty}r_d=c_{\rm call}.
]

At the two verified parameter points:

- baseline ((\beta,\sigma)=(1/2,1/10)): (r_\infty=6/5=1.2);
- retuned ((\beta,\sigma)=(101/200,1/10)):
  [
  r_\infty=1+\frac{1/10}{99/200}=\frac{119}{99}=1.20202020\ldots.
  ]

Thus separator recursion spends the cone-replication budget at exactly the exponent already charged by INTERFACE-FLMV-RETUNING72. It is not an additional contradiction and not a new third P-vs-NP route. A strict FLMV entry still requires every acquisition, probe, serialization, output and same-machine cost to remain below the separately verified safe point.

**Status: ESTABLISHED identity.**

## DAG-sharing audit

DAG memoization can reduce cost only when residual children produced by different cut paths have a uniformly computable canonical representation and actually collide. Gate sharing by itself proves neither condition. Source-faithful instances can attach forced path tags to residuals, making the residuals syntactically distinct while remaining easy to inspect.

- **RETIRED:** treating sibling DAG sharing as a free generic exponent reduction.
- **OPEN structured repair:** a proved canonical-residual collision theorem for a restricted family, with canonicalization, source reads and table storage fully charged.
- This is a mechanism control, not an unrestricted lower bound.

## Compact-witness stopping rule

A uniformly acquired small circuit (W(i)), together with an exact small source evaluator, could terminate separator recursion before full unfolding. But neither the recursion nor the geometric-series bound proves that (W) exists. The COMPACT-HISTORY20 premise remains the single global quantifier
[
\exists W\;\forall i,
]
not independently chosen (W_i)'s. Modular increment remains a fast-forward counterexample to converting explicit history length into unrestricted time.

**Status: CONDITIONAL on the still-OPEN compact-witness premise.**

## Circuit-SAT and P/RP integration

PARITY-FIBERS45 supplies a separate restricted theorem: if a rank-(t) span of original-source affine forms contains a syntactically affine operand at every AND gate, deterministic branching takes (2^{O(t)}\operatorname{poly}(S,m)), with at most (2^t(m-t+1)) genuine tapes. This is polynomial for (t=O(\log n)), but uniform applicability to arbitrary RP verifiers is OPEN.

Its degree control also blocks a proposed shortcut: a Boolean function affine on every rank-(t) parity fiber has ANF degree at most (t+1), so a rank-one high-degree counterexample cannot exist.

Most importantly, the inspected DOUBLE_WRAPPER source performs at least two full literal-ID passes before its literal metric initializes. Those are original-source observations and must enter SOURCE-CHANNEL21. A later hash does not erase them. This neither proves P=RP nor P!=RP.

Faithful Tseitin gate traces remain unique after a primary assignment, but independently sampled clause-occurrence witnesses still destroy source equality. DIGEST-LUMP19 and CLAUSE-COHERENCE20 remain active.

## Ordinary-MKTP consequence

A recursively materialized separator tree may have (N^{c_{\rm call}+o(1)}) nodes while possessing a short indexed generator. Large unfolded volume therefore does not imply HIGH ordinary KT. Program length, indexed running time, totalization, both labels, original-source access and output convention must all be charged.

**Status: ordinary-MKTP HIGH arrow remains OPEN.**

## Finite audit

The executable audit generated 120,000 random capped partitions and checked
[
\lfloor x^\sigma\rfloor\sum_i y_i^c
\le
x^{1+\sigma+\beta(c-1)}
]
for (1\le c\le1.45), (0.3\le\beta\le0.7), and (sum_i y_i\le x). It also replayed 80 recursion levels at each verified endpoint and compared the recurrence with the closed form.

Result: **120,162 assertions, zero failures**. This validates implementation and arithmetic only.

## Route ledger and next discriminating tests

- **:00 SAT-to-ordinary-MKTP — OPEN.** Compute ordinary KT of the indexed recursive-separator generator, including original-source probes and random-access time; reject HIGH if the unfolded tree is succinctly indexable.
- **:12 P!=RP — OPEN.** Quantify the two full DOUBLE_WRAPPER source passes inside SOURCE-CHANNEL21 and run the direct deterministic-bypass control.
- **:24 ARC/FLMV — Lemmas 81A/B ESTABLISHED restricted; transformer OPEN.** On one real WRAPPER child generator, measure canonical residual collisions and require a hereditary certificate for every child.
- **:36 P=RP — PARITY-FIBERS45 ESTABLISHED restricted; general derandomization OPEN.** Test the actual WRAPPER circuit for the first AND gate whose operands both lie outside every proposed rank-(O(\log n)) affine span.
- **:48 synthesis — recurrence identity ESTABLISHED.** Translate the wall/expander residual into this exact source-incidence measure, including Tseitin and output costs.

## Bottom line

Hereditary separator recursion does not create hidden exponent savings: its cumulative source incidence converges exactly to the FLMV call fixed point. This makes the accounting cleaner and exposes where any genuine improvement must enter—separator acquisition, canonical residual collisions, or a uniformly acquired compact (W)—but closes none of those arrows. P versus NP and P versus RP remain OPEN.
