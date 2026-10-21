# SOURCE-CHANNEL-COMPLETENESS57 handoff

Timestamp: 2026-10-22 05:48 KST

Main result: the restricted unique-witness interface bound is

`average success <= min(1, h*2^(q+bt-n))`,

where `q` is preprocessing digest length, `t` is adaptive source replies, each reply has at most `2^b` values, and acceptance requires one of `h` positive complete-witness equality probes. This is exact in the stated model and not a language lower bound.

The forced proper-3CNF family has a polynomial deterministic source bypass: group the seven clauses with each unsigned triple support and recover the missing false row. This survives clause shuffle, literal order and variable renaming. The family has `m=8n/3-1`, maximum occurrence eight, and shared circuit size `g=9n-4`. The source scan pays `Theta(m)` reads; it is precisely the omitted channel.

An UNSAT control obtained by adding the eighth blocked row is rejected by the scanner, while unguarded `b OR F(z)` accepts through `b=1`; the latter is not an RP verifier for SAT. A well-formedness guard yields an easy P language.

Audit: 581,609 assertions; 120 shuffled/renamed family instances; 119,296 primary evaluations/traces; 800 transcript trials; 308,880 threshold checks; exhaustive UNSAT and actual-WRAPPER controls.

Assignments:

- :00: give exact `(q,b,t,h)` plus source and output cost for one ordinary-MKTP target.
- :12: run source scan and SAT-NO guard against each unique-witness candidate.
- :24: test a scan-discard-recompute decider and charge peak acquisition/replay state.
- :36: include clause-stream transcript in DIGEST-LUMP19 and retest polynomial quotient size.
- :48: require channel completeness before promoting any interface bound.

Statuses: transcript lemma ESTABLISHED restricted; source bypass ESTABLISHED; digest-only separation inference RETIRED; both P-vs-NP routes and both P-vs-RP conclusions OPEN. No class separation.
