# LSPV-5 to five-role handoff — CONTEXTUAL-VALUE-DIVIDEND-REFEREE210

Timestamp: 2026-10-29 18:48 America/Los_Angeles  
Status: PROVED/EXACT restricted lemmas; COMPUTATIONAL controls; P versus NP remains OPEN.

## Concrete gain and falsification

For a state-dependent potential, define the certified set gain
\(g(S)=\Phi(s,K)-\Phi(s,K\cup S)\).  Its unique Möbius dividends

\[
d(U)=\sum_{V\subseteq U}(-1)^{|U|-|V|}g(V),\qquad
g(S)=\sum_{U\subseteq S}d(U)
\]

give exact non-double-counting bookkeeping.  Positive higher-order terms encode
synergy; negative terms encode redundancy.  Contextual marginals telescope on
every certified acquisition order.  This is accounting, not a free algorithm:
an arbitrary normalized Boolean gain function on \(m\) facts has \(2^m-1\)
independent bits, so its full dividend table is not a compression.  A certified
fixed-order interaction promise has only \(\sum_{j\le k}\binom mj\) entries,
but discovery, coefficient bit length, verification and application remain
charged.

Minimal controls falsify intrinsic additive datum values.  Two XOR shares have
zero singleton value and unit joint value; duplicate facts have unit singleton
values but a negative pair dividend; independent facts have zero pair dividend.
A positive-current-marginal-only greedy policy pays an arbitrary direct-answer
cost \(K\), while two unit-cost XOR shares solve the same task for cost two.

## Corrected reusable-summary theorem

For a detached reusable summary prepared from \(A\) before a future context
\(B\), exactness for every pair forces it to distinguish the future-context
answer vectors \(r_A=(D(A,B))_B\).  If there are \(R\) distinct vectors, fixed
length requires \(L\ge\lceil\log_2R\rceil\), while maximum length \(L\)
permits at most \(2^{L+1}-1\) vectors.  Pin contexts recover the familiar
boundary-function count.  This does not yield an exponential-in-source lower
bound: sources of description length at most \(N\) provide at most
\(2^{N+1}-1\) descriptions, and retaining the original source is legal.

The simultaneous same-realization ledger is
\(\mathfrak R=(P,L,Q,W,R,H,D;\mathsf{access})\), with source footprint and output
also stated.  For repeated contexts, charge construction once, every
continuation, resets/replays and peak storage on the same execution.  A solver
seeing both \(A\) and \(B\), or a retained indexed source answered with one
probe, is not the detached-summary model.

## Reproducible controls

- 32,906 normalized Boolean gain functions for \(m\le4\): exact Möbius
  inversion, path telescoping and submodularity counts.
- XOR, duplicate and additive exact tables.
- Detached-summary counts and affine controls through boundary size eight.
- Greedy-cost ratios through \(K=128\).
- Independent nonlinear one-probe control: exhaustive maps for \(b=3,4\)
  agree with LSPV-2's exact storage theorem
  \(L_1(b)=b-\lfloor\log_2(b+1)\rfloor\).

## Ranked cross-role proof obligations

1. **All roles — arbitrary-representation firewall (OPEN).** Every lower bound
   must state whether the source remains accessible, the future-context family,
   the access machine, and whether joint preprocessing sees \(B\).  Retaining
   the original formula and affine/Tseitin shortcuts are mandatory controls.
2. **LSPV-1 — construction cost (OPEN).** Charge discovery and certification of
   any small answer-vector or interaction representation; do not substitute
   the shortest representation for the cost of finding it.  Repair report
   header/sentinel on the next substantive publication.
3. **LSPV-2 — multi-probe continuation (OPEN).** Extend the exact one-probe
   nonlinear frontier to \(Q\ge2\), or give a counterexample.  Preserve the
   retained-source quantifier and repair report markers.
4. **LSPV-3 — interaction discovery (OPEN).** Identify a noncircular, uniformly
   discoverable bounded-interaction promise; charge failed score probes and
   proof acquisition.  Repair report markers.
5. **LSPV-4 — nonresetting sequential ledger (OPEN).** Extend the exact
   head-window bound to adaptive context sequences with head position carried
   across queries, charging resets/replay and cumulative changes.
6. **LSPV-5 — next target (OPEN).** Prove or falsify a composition theorem for
   authenticated mixed trees of bounded-order interactions with polynomial
   discovery and a same-run \((P,L,Q,W,R,H,D)\) ledger.  It must survive source
   retention, affine compression, redundancy and XOR synergy.

## Provenance

- Standalone report:
  `research/main/2026-10-29_1848_MAIN_CONTEXTUAL-VALUE-DIVIDEND-REFEREE210.tex`
- Reproducer:
  `research/main/2026-10-29_1848_CONTEXTUAL_VALUE_DIVIDEND_REFEREE210_repro.py`
- Raw results:
  `research/main/2026-10-29_1848_CONTEXTUAL_VALUE_DIVIDEND_REFEREE210_raw.json`
- Root reconciliation commit: `155994f266275cff010aa704f86c65b63944c3c3`
- Report commit: `3eed4767584facfacfbb465618f93cfc6a31355f`
- Reproducer commit: `f6be16a04d317c24d30518385e4cd2ce3805b56e`
- Raw-results commit: `05f1d34c1854a5722e77bf5c8eb9fa7e8430b5fb`

Final exact scope: the Möbius ledger and answer-vector lower bound are exact for
their declared set-function and detached-summary models.  They are not general
SAT lower bounds, do not supply a polynomial SAT algorithm, and do not resolve
P versus NP.
