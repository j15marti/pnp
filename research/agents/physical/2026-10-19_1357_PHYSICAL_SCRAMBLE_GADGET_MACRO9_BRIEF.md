# SCRAMBLE-GADGET-MACRO9 | 2026-10-19 13:57 KST

Red-team result. After arbitrary variable-name permutations, consistent per-variable sign flips, and clause/literal shuffles, local 3-CNF patterns still reveal padded AND constraints and XOR3 quartets.

Exact identities: (A∨B∨p)∧(A∨B∨¬p) = A∨B. Combining a ternary (¬a∨¬b∨t) with (a∨¬t),(b∨¬t) enforces t=a∧b. A four-clause parity-class support enforces one XOR3 equation. A complete syntactic partition gives an equivalent Boolean function on the same original variables.

Falsifier: five XOR quartets uniquely require (a,b,t,c,d)=(1,1,0,0,0); a padded AND requires t=a∧b. These 25 distinct proper clauses have 4 XOR-only extensions but ZERO complete models. Gaussian-only decision is unsound for general AND/XOR gadget CNFs.

For the scrambled nonlinear parity family d=7: N=2744,C=6574; raw vs equivalent macro G 22465/5286, E 42187/9882, driven nets 25209/8030, nominal MOS 123814/57108, fanout-2 buffer proxies 12382/893. Same input/output Boolean function, declared CMOS proxy library, not device minima or physical routing. Input 256428 bits, macro 62854 bits, source traversal charged. 303 full-function comparisons, 64 near-image rejections, exhaustive 4096 Q3 primary assignments, all passed. One-tape tape-head cost and physical wiring remain unmeasured. General SAT complexity OPEN.

Full report/code/raw are in the local research bundle. P versus NP OPEN.
<!-- FINAL_VERIFICATION_SENTINEL::SCRAMBLE-GADGET-MACRO9 -->
