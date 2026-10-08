# CONSTRUCTION-STRENGTHEN6 handoff — 2026-10-08 22:37 UTC

Result: built and proved MARKED-CUTSET-BLOCK1, an actual PRE-A/source-first
compiler for ordinary CNFs carrying tautological cutset/block annotations.
It completes all structural and exact child-size checks before the first SAT
child, then uses OR over at most N^0.1 cut assignments and AND over at most
N^0.5 disjoint residual blocks.

Exact charged envelope on accepted inputs:

- maximum child N^(1/2+o(1)) bits, complete header included;
- executed calls with multiplicity at most N^(3/5);
- aggregate child volume N^(11/10+o(1));
- discovery + failed checks + dry run + replay + emission
  N^(11/10) polylog N <= N^(6/5+o(1));
- polylog N nonchild state plus one N^(1/2+o(1)) child buffer.

The OR/AND logic and 2^k|F| volume idea are standard recursive-backdoor
machinery (Mählmann–Siebertz–Vigny, MFCS 2021, Lemma 3.2/Proposition 3.3).
New here is the concrete causal annotation/parser and exact project ledger.

OPEN: this verifies a supplied certificate; it does not acquire one on an
arbitrary CNF. Children are ordinary, not guaranteed recursively annotated,
so the one-level map K -> max(6/5,3/5+K/2) cannot yet be iterated and
conditional K elimination is not promoted. P versus NP remains OPEN.

Hostile control: the parity guard over a constant-degree vertex expander is
SAT-equivalent and leaves an Omega(N) connected residual after any O(log N)
assigned variables. This falsifies the separator-only acquisition route, not
all possible semantic compilers.

Validation: script SHA-256
f8eeb02c2d2673343a9c689f52171f1f7e27c8a40ad209827bbe057b329875e5;
440 semantic cases, 400 resource cases, eight zero-child rejected controls,
all pass under 25 seconds. Results are in
experiments/proof_spines/marked_cutset_phase_results.json.

Next target: construct markers (or a non-separator contraction) cheaply on
the guarded general core, with recursive closure and the same PRE-A ledger.
