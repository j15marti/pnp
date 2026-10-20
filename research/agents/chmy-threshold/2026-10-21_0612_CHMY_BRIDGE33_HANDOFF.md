# CHMY Bridge 33

Status: P vs NP OPEN.

Verified result: The CHMY 2021 local generator/counting proof also yields the two-sided-error one-work-tape lower bound for the OPS-shaped GapMCSP promise with large threshold exponent beta>1/2, not just exact MCSP. This does not match OPS's nonuniform circuits or its all-small-beta hypothesis.

Constructed E(f)(x,y)=f(x) XOR (y0 AND (x0 XOR y1)); CC(f)<=CC(E(f))<=CC(f)+9. On x-major truth-table order the extension is one-pass with N source reads and N^2 target writes. Same-c OPS gap thresholds do not preserve source YES, but the stronger source threshold S/(4c log N) correctly maps to target S/(2c log N) for sufficiently large N, while NO threshold S is preserved. Exposing the full target already costs N^2, more than CHMY's N^(2nu) lower bound (nu<beta<1), so this provides no positive hardness-margin transfer.

Tested 753 finite assertions, zero failures. The actual CHMY pseudorandom generator was used through the published theorem, not numerically instantiated. One-work-tape decoder composition was not established. Full report and Python audit are local, external sharing status independent.

Next: A length-preserving, witness-correct small-beta transfer with fully charged one-tape simulation.
