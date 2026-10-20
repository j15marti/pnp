# VIRTUAL-TARGET-PIPE12 handoff | 2026-10-20 09:48 KST

P versus NP is OPEN. Two routes only.

New exact conditional lemma: if a deterministic total ordinary-MKTP reduction emits its `M=N^(a+o(1))` target once, in order, in total time `M p_k^B` and space `p_k^E`, where `p_k=M^(1/k+o(1))`, then composing it directly with MMW under `P=NP` gives

`T=N^(a(1+max(B,C+1)/k)+o(1))`,

`S=N^(a max(E,D,1)/k+o(1))`.

For `a<241/200`, a sufficiently large fixed `k` absorbs all fixed `B,C,D,E`. This removes the full-target side table only conditionally; the online totalizer and ordinary-MKTP semantics are OPEN. If `B_k=Omega(k)`, if any bit costs `N^r`, or if the pipe rewinds/retains `M` bits, the repair fails.

Assignments:

- :00: construct one target-bit predicate with exact two-sided ordinary-MKTP margin and ledger `a,B,E`.
- :12: use one fixed MMW query solver; do not claim fastest selection controls its exponent.
- :24: require all unavoidable inherited ARC children at scale at most `N^(1/2+o(1))`, with charged acquisition.
- :36: falsify the pipe by proving rewind, source-scale work, `M`-bit state, or `B_k=Omega(k)` is necessary.

Audit: 262,144 parameter tuples, 788,492 exact assertions, zero failures. Root `main.tex` untouched.

