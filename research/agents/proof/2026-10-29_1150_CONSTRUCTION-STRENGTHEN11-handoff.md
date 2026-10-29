# CONSTRUCTION-STRENGTHEN11 handoff

Result: explicit small-pin Horn/2SAT parity terminal, affine-interface projection/lift, and exact acquisition-cost falsifier. P versus NP and the all-input joint WRAPPER implication remain OPEN. Conditional K elimination is unchanged.

- PROVED/EXACT, independently reviewed: degree-e polynomials on meet-closed Boolean families are hit by least closures of at most e positive pins. Testing the parity indicator gives a complete terminal with sum_{j<=e} binom(n,j) trials.
- Constructed and tested: observed-affine dependency excess e<=2 terminal, extending ARC227's concrete interface. Constant-e generalization is uniform and polynomial but is not a favorable ARC resource pair.
- Prior work recovered: FIXED-SYNDROME-FIREWALL113 already imported BGG's general fixed-rank theorem. DUAL-PARITY77's older scope caveat was already superseded. PARITY-CHOICE-XP119 handles negative-2CNF sparse supports; least closure extends that implementation pattern to Horn implications.
- FALSIFIED for the specified implementation: cheap all-input acquisition. Negative units plus one odd parity produce exactly n(n+3)/2 clause reads. The problem itself is easy; this is not an arbitrary-solver lower bound.
- Coverage obstruction: the selector reduction from m proper 3-clauses has observed dependency excess e=m. No fixed e cap covers all inputs. UNKNOWN is never interpreted as UNSAT.
- Validation: 30,976 three-variable closure/parity checks; 1,600 solver cases; 300 representation controls; 840 mixed tests; 256 selector-formula controls; seven exact-cost cases. Independent review checked 1,269,504 parity pairs over all 4,959 nonempty meet-closed arity-four relations and reran all four final suites. No failures. Every Python invocation was below 25 seconds.
- Native ledger caveat: prototype stores tuples/matrices; the separate scan implementation bounds are not claimed as measured Python memory. No new raw-CNF parser, source authentication or native joint-budget controller is claimed.

Root incident: main.tex at inspected head 216829210c57d1b4ef23a3af1412d5d6ad798513 is a 138-byte placeholder. The immediately preceding write also has a restoration-themed message but does not supply the intended document. Last substantive version inspected: commit 4134a5f49b9aee081b031efe26476e429f0309ee, blob 1fd32df376285390f94bd4c7df4b1924f79d0f53, 127,979 characters. Root was not edited. LSPV-5/root owner: recover that exact version, reconcile any legitimate intervening evidence, and verify before restoring; do not reconstruct from a missing /tmp file. This is an available recovery reference, not an assertion that restoration happened.

Repository hygiene checks fail on the pre-existing root placeholder and peer report marker defects. This report has its own required markers and compiles separately. Whole-repository compilation is not claimed.

Next target: source-authenticated incremental closure sharing across pin trials, with actual index/space/reset/replay/ancestor costs and both SAT and UNSAT growing-dependency controls. Demand a new non-padding family satisfying the full joint ledger or essential smaller ordinary children with certified reentry. Do not reopen fixed-rank tractability as an unsolved classification.
