# CM forbidden-region status

> Historical status note. Subsequent results establish scoped compact-target auxiliary-CM exclusions; see [Additional forbidden regions](Additional_T5_Tq_Forbidden_Regions_2026-11-22.md), [the complete T_q CM model](T_q_FLMV_and_CM_Forbidden_Regions_2026-11-22.md), and [entropy bounds](T5_Tq_Entropy_Lower_Bounds_2026-11-22.md). The earlier text below is preserved as a dated record. No superpolynomial separation is claimed.

Date: 2026-11-22, America/Los_Angeles.

Publication purpose: share the current conversation's scoped CM result and its limitations. This is a status note, not a new research run or a resolution of P versus NP. No independent review or new computational tests are claimed.

## Current answer

We have a cumulative-memory forbidden region for the explicit-input physical-memory model: on the quadratic regular-tournament family, worst-case CM cannot be o(N^2), where N is the full explicit encoded input length.

We have not established a CM forbidden region that excludes every polynomial-time algorithm for SAT or the compact circuit-encoded tournament decision problem.

| Setting | Result | Status and scope |
|---|---|---|
| Explicit T_odd quadratic family | CM = Omega(q^4) = Omega(N^2) | PROVED/EXACT in the stated physical input-residence model; project proof, not independently reviewed here |
| Compact circuit-encoded T_odd | No corresponding CM lower bound established | OPEN; explicit-table lower bounds do not transfer automatically |
| Unrestricted SAT decision | No superpolynomial CM lower bound established by this project work | OPEN |
| FLMV SAT lower bound | Excludes specified simultaneous time/workspace bounds | KNOWN THEOREM; not a direct cumulative-memory theorem |

## Definition and model

For a single deterministic execution, define

$$
CM(x)=\sum_{t=0}^{T(x)-1}S_t(x).
$$

Here S_t counts physical live storage, including still-needed input. Worst-case CM is the maximum of this sum over inputs of the specified length. Time and memory charges refer to the same execution.

The explicit family has q alphabet values, Theta(q) residual clauses, one unknown variable, and an explicitly stored regular tournament. Its encoded length is N = Theta(q^2).

The proof assumes:

1. The initial representation consists of fixed-position explicit cells, each depending on at most one independent free input bit. Copies and complements are allowed.
2. Each charged microstep acquires at most a constant c new input-bit dependencies.
3. Preprocessing and storage throughout acquisition are included in the measured interval.
4. Deleting the last representation of a bit removes access to it. There is no uncharged external original-input copy.
5. A weighted atomic operation cannot acquire an entire array instantly, discard it, and then accrue its assigned time charge after the storage has disappeared.

The algorithm may delete irrelevant input and redundant copies. These assumptions do not require keeping the whole tournament resident forever.

## Scoped lower-bound argument

The source construction realizes

$$
f(z)=\bigvee_{i=1}^{r}\bigwedge_{j=1}^{t}z_{ij}
$$

inside a regular tournament, with R = rt = Theta(q^2) independent input bits.

A deterministic adversary answers 1 to the first t-1 distinct queried bits in each row and 0 to the last. Every row must be eliminated to decide the resulting UNSAT input, forcing acquisition of all R bits. Every unread bit in an unresolved row is still essential on a completion consistent with the transcript.

Before acquisition, no newly computed aggregate or control state depends on that bit. Deleting its final passive representation would make two consistent inputs with different answers indistinguishable. Since each cell contains at most one unacquired dependency, after s charged steps,

$$
S_s\ge \max(R-cs,0).
$$

For Omega(R) steps, Omega(R) indispensable bits therefore remain live. Thus

$$
CM=\Omega(R^2)=\Omega(q^4)=\Omega(N^2).
$$

This is a worst-case statement: for every correct deterministic solver in the declared model, there are inputs forcing the bound. It is not a claim that one fixed input defeats every program.

The charged-block algorithm in the source note achieves matching worst-case scales in its specified layout and access model:

$$
T=\Theta(N),\qquad S_{\mathrm{total}}=\Theta(N),\qquad CM_{\mathrm{physical}}=\Theta(N^2).
$$

Only O(log q) auxiliary workspace is required by that algorithm. Ordinary OR on explicitly stored bits has the same quadratic input-residence phenomenon under this accounting. The result is not an auxiliary-workspace hardness theorem or a minimum-description CM theorem.

## What FLMV does and does not supply

Fortnow, Lipton, van Melkebeek, and Viglas prove that for every fixed 1 < a < phi, where phi = (1+sqrt(5))/2, there exists b > 0 such that no deterministic random-access Turing machine decides SAT in simultaneous time O(N^a) and workspace O(N^b). Their workspace excludes the read-only input. [2]

This cannot simply be turned into a CM lower bound by multiplying the two thresholds. For every execution,

$$
CM\le T S_{\max},
$$

not the reverse. A peak-space lower bound alone does not specify how long that storage is occupied. Any useful transfer needs a valid memory-duration argument or another proved simulation.

Applying the SAT forbidden region to the compact tournament problem also requires a reduction preserving the relevant simultaneous resource bounds. Polynomial-time NP-completeness alone does not preserve near-linear time and subpolynomial workspace.

## Polynomial-time ceiling and remaining dependency

In a bounded-allocation physical model with initial input storage O(N),

$$
S_t=O(N+t),\qquad CM=O(NT+T^2).
$$

For a fixed time cap T <= K N^k,

$$
CM=O(N^{k+1}+N^{2k}).
$$

Therefore our quadratic CM lower bound is compatible with linear time.

To use this route to separate P from NP, one sufficient target is an unrestricted decision lower bound for the compact NP-complete problem that defeats this CM ceiling for every fixed k, with a valid model transfer covering ordinary polynomial-time algorithms. That target remains OPEN. It cannot be replaced by a lower bound for exact counting alone.

The compact encoding exposes circuit syntax, and an algorithm may exploit it without expanding the tournament table. For example, the circuit template F_(beta,a)(y) = beta AND [y=a] can require 2^k point queries in the black-box model, yet its explicit template reveals satisfiability by reading beta. Consequently, small circuit representations of adversarial completions do not repair the query-to-syntax transfer gap. [1]

## Validation and publication scope

The source notes were read and the FLMV primary paper was consulted for the preceding conversation. This publication adds no new experiments, formal verification, independent review, agent scheduling, or manuscript reconciliation. Repository preflight and compilation were not run: this is an additive Markdown publication through the connected repository interface, with no local checkout. Publication validation consists of complete content readback.

## References

1. Project note, *T_odd proof continuation: tight explicit bounds, live-input memory, and a compact NP-complete target*, 2026-11-22, especially Theorem B and Sections 5-7. [Source note](https://chatgpt.com/library?file_id=libfile_37b1d853fb7481918dd7186969a79c23&account_id=personal). This ChatGPT link requires access to the source owner's file.
2. Lance Fortnow, Richard Lipton, Dieter van Melkebeek, and Anastasios Viglas. *Time-Space Lower Bounds for Satisfiability*. Journal of the ACM 52(6):835-865, 2005. [Author manuscript, September 7, 2004](https://lance.fortnow.com/papers/files/tst.pdf), Theorem 1.1 and Section 2.1.
