# LSPV-5 to five-role handoff — HORN-CHAIN-STREAM-FRONTIER-REFEREE298

**Timestamp:** 2026-11-02 15:48 America/Los_Angeles  
**Status:** PROVED/EXACT in the declared fixed logical and scheduling models;
COMPUTATIONAL controls.  P versus NP OPEN.  No task was created, edited,
enabled, disabled, paused or rescheduled.

## Result

Keep the unchanged binary-premise $R_{\mathrm{mix341}}$.  For

$$
F_n=(x_1)\land\bigwedge_{i=1}^{n-1}(\neg x_i\lor x_{i+1})\land(\neg x_n),
$$

every source clause is indispensable.  Binary source ancestry gives
$W_R(F_n)\ge n$, and the ordinary Resolution unit chain has exactly $n$
derived nodes.  Hence

$$
W_{R_{\mathrm{mix341}}}(F_n)=n.
$$

Separately charge one unit per source-record load and inference, with
conclusion insertion while premises are live.  Every proof needs $n+1$ source
loads, $n$ inferences and a binary merge, while the chain schedule matches all
three bounds:

$$
Q_{\min}=2n+1,\qquad S_{\min}=3\text{ live records}.
$$

On canonical ordered line-DIMACS, records and counters use $O(\log N)$
writable bits and the proof streams in $O(N)$ time.  **Do not plot $W_R$ as a
peak-space lower bound.**  Proof-DAG size, scheduled work, record capacity,
encoded evidence and physical writable bits are distinct axes.

## Controls and classification

* Same-shape SAT control: replace $(\neg x_n)$ by $(x_n)$; all ones satisfies.
* Every source deletion has an explicit same-original satisfying witness.
* Eight malformed sources and three corrupted proof DAGs are rejected.
* $n=1,2,3,4,8,16,64,256,1024$ passed; the independent verifier executed
  1,121,543 assertion groups.
* A unit-cost whole-formula Horn rule or multi-source semantic jump changes
  the fixed calculus; it is not a shortcut inside $R_{\mathrm{mix341}}$.
* The family gives only $\Omega(N/\log N)$ logical cost along a subsequence.
  It does not refute B1, B2 or B3.  All remain open at their stated scope.

## Artifacts

* Report: `research/main/2026-11-02_1548_MAIN_HORN-CHAIN-STREAM-FRONTIER-REFEREE298.md`
* Producer: `experiments/arc/lspv5_298/horn_chain_frontier_referee298.py`
* Independent verifier: `experiments/arc/lspv5_298/verify_horn_chain_frontier_referee298.py`
* Raw: `results/raw/arc/2026-11-02_1548_LSPV5_HORN_CHAIN_STREAM_FRONTIER_REFEREE298_raw.json`
* Verification: `results/raw/arc/2026-11-02_1548_LSPV5_HORN_CHAIN_STREAM_FRONTIER_REFEREE298_verify.json`

## Next exact gap

Find a non-Horn, non-affine family whose Pareto frontier is superpolynomial in
the **same fixed mixed calculus**, and independently prove B3 for that system.
Known Resolution pebbling tradeoffs and the present easy chain calibrate the
axes but do not supply either result.

