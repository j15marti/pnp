# ACCESS-MODEL-COMPOSITION17 handoff

Timestamp: 2026-10-20 14:48 KST. **P versus NP remains OPEN.**

New proved interface: nested deterministic local generators on random-access sources compose geometrically. If each stage shrinks length by exponent `v` and costs exponent `g` relative to its parent, then a depth-`r` bit costs base exponent `g(1-v^r)/(1-v)`. For ARC `v=1/2`, the cumulative limit is `2g`, exactly matching the prior recurrence; the strict conditional window remains `g<1/400`, `h<=1/2`, `e<241/200`.

New model firewall: after a one-way pass, exact arbitrary-coordinate replay requires an `N`-bit synopsis. Random access avoids that storage by rereading source bits, but many constant-size ordinary queries can still transmit all `N` bits and incur `N` reads. Therefore lazy virtual input is a candidate for FLMV random-access ARC, not an automatic CHMY one-way repair. Hutter input caching restores replay but charges the cached stream in space.

Role targets:

- :00: an order-compatible one-way totalizer or a necessary out-of-order request counterexample.
- :12: exact selective Hutter scheduler ledger; do not claim it bounds unknown exponent `C`.
- :24: uniform all-input ARC bit predicate within `g<1/400`, `h<=1/2`, `e<241/200`.
- :36: force forbidden reread, `N`-bit synopsis, or generator threshold failure.
- :48: flatten every nested generator to the named base-source model.

Audit: 103,298 assertions, including 65,536 exhaustive short-synopsis encoders, zero failures. Root `main.tex` remains placeholder-bearing and was not modified.
