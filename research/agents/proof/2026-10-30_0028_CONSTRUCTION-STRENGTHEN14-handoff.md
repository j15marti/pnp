COUNT-REDUCE-RECOUNT14 | 2026-10-29 17:28 PDT
Implemented local exact counts on at most four clauses and six variables; zero counts prove UNSAT, zero conditional counts force bits, equal counts before/after clause deletion certify redundancy. Recompute after every accepted rewrite. Same local variable universe retained for every count comparison.
Positive control: two successive pins, eight original models, 924 trials. Ordinary XOR UNSAT control: three pins, 842 trials. All 48 connected strict22 samples (SAT) remain UNRESOLVED after 422968 trials; only one duplicate deletion. Nine bounded test chunks pass, all under 25 seconds. No claimed total speedup or strict22 UNSAT sample coverage.
Complete elementary correctness and charged termination proofs; independent referee pending. Root main.tex untouched, all-input proof OPEN, conditional K elimination unchanged.
Next: pair-conditioned counts and equivalent shorter relations, with all acquisition and equivalence work charged.

