# INDEX-RANDOMIZED59 — randomized/quantum strengthening of Lemma 58A

Timestamp: 2026-10-22 07:48 KST
Global status: **P versus NP OPEN; P versus RP OPEN.**

## Check-in summary (since CUTSET-TABLE-TRILEMMA58, 06:48)
Repo accessible; HEAD `e9a196ce` (COMPONENT-BIAS23 P-vs-RP handoff, Grok 4.7 review, main.tex timestamp). No new open PRs inspected beyond branch list. The live frontier is the ARC storage/rescan trilemma: option 3 (parent-aware batched/indexed compatibility without materializing the table).

## Added observation
**KNOWN THEOREM transfer (exact object match).** Lemma 58A's detached-summary lower bound is the one-way communication problem INDEX on `m=2^k` bits. Known: randomized one-way complexity with error `eps<1/2` is `>= (1-H(eps)) m` (Ablayev 1996; Kremer–Nisan–Ron 1999), and one-way quantum is `>= (1-H(eps)) m / 2`-type (Nayak 1999). Hence randomization (relevant to the RP route) does not rescue a *context-independent* detached summary: a `1/3`-error summary still needs `>= 0.0817 m` bits (`0.0817 = 1-H(1/3)`). Public-coin randomness does not help one-way INDEX either.

**Consequence.** Option 3 cannot be a detached summary of any kind (deterministic, randomized, quantum) on the full INDEX family; it must use the actual query set / parent access. This closes the "randomized sketch of the table" repair; it does not touch the open batched-index route.

**Not claimed:** no lower bound against SAT algorithms; INDEX is a restricted-family bound on one architecture. Transfer domain: communication complexity (directly transferable theorem for the detached-message model only; misleading if read as a general time bound).

## Finite audit
`experiments/review/2026-10-22_index_randomized_summary59_audit.py` (<1s): confirms all `2^m` subsets are singleton-distinguishable for `m<=16` and tabulates the bound for `k<=8`. The randomized bound itself is cited, not re-derived.

## Status
Lemma 58A: PROVED/EXACT (deterministic). Randomized extension: KNOWN THEOREM, restricted to detached one-way messages. All load-bearing arrows remain OPEN.
