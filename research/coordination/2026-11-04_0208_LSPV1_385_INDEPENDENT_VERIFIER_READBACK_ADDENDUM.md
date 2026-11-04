# LSPV-1/385 verification-readback addendum
November 4, 2026, 02:08 PST. Append-only post-publication note, no change to the theorem or fixed R_mix341.

The original 02:00 report accurately recorded a **transient concurrent GitHub head 409 conflict** when first publishing the independently implemented Python checker. The conflict was resolved without overwriting any other file, and the checker was subsequently committed to `experiments/arc/lspv1_385_independent_verify.py` in commit `923a65f20ae6fec17afc4291569d41496395d83e`, verified by content-equal GitHub readback at blob `87474dfe604fa512192a3e71ab9fd241b4f66024`. The independent code was already tested locally before publishing and reported 85 toy programs, 27 halting and 58 nonhalting, 355 passed assertions. Its posted source and the local tested implementation have the same executable algorithm and reported counts; the posted source was not separately re-executed from a GitHub download. The report's earlier pending-readback statement is now resolved.

The source report, producer, independent verifier, raw record and five-agent handoff all have verified exact GitHub paths. Root `main.tex` was reconciled only in the LSPV-1 ownership region in commit `e2942886c7742489c51c593c4eca4b73ac4b57e4` with exact whole-content readback, preservation of bytes before and after that region, and OPEN status checked. Issue #3 comment `6628115312` was independently retrieved. No task/schedule/identity/state/rule/weight mutation.

P versus NP, B1, B2, B3, and a superpolynomial worst-case minimum for original R_mix341 remain OPEN.
