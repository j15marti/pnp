# LSPV-5 NONAFFINE-LIFT-ER2-COLLAPSE-REFEREE308 | November 3, 2026, 00:48 PST

**PROVED/RESTRICTED:** the LSPV-3 nonaffine lifted-Tseitin family has a polynomial refutation in the unchanged fixed `Rmix341`; the fresh-output `AND3` grammar gap is bypassed by the already legal source-independent two-input `AND`/`XOR` `VARDEF` plus strict `RES` fragment. No task or calculus setting changed.

For a connected simple cubic \(h\)-vertex graph, surjective gadget circuit size \(c(k)\), and LSPV-3 local variable counts \(M_v\),

$$
W_{Rmix341}(F_{G,g,\sigma})
\le |E|c(k)+\sum_v3^{M_v}+69(3h)^3+9.
$$

Thus \(c(k)=O(k)\), \(k=O(\log h)\) gives polynomial minimum cost. For the explicit `AND2` lift,

$$
W_{Rmix341}(F_h)\le1863h^3+\frac{163}{2}h+17.
$$

The construction compiles the recovered parity clauses to vertex XOR-output units, XORs the odd charge to one, reassociates and permutes all \(3h\) edge occurrences, copies one occurrence per edge through a paid true rail, cancels each legal distinct-input pair, and derives output zero. Fixed ordinary-Resolution certificates justify commutativity, associativity, congruence, authenticated copy, cancellation, unit propagation, and both parity labels.

Finite independent replay: 11 templates, 81 RES nodes, 155 retained certificate lines, maximum 30 RES in one template; Node verifier PASS. Odd \(K_4\): 0 models. Even neighbor: 8 models. Seven parse controls classified correctly. Raw SHA-256 `b85f616ce678b1bf7653e7bb4bafbf843ba971c9cdb42f7528a24cc8a7453ac9`.

**Classification:** this retires one candidate hard family. It proves neither B1, B2, nor B3. Regular/depth-restricted `Res(⊕)` lower bounds do not transfer through the extension-enabled escape. Superpolynomial worst-case mixed minima, the weakest same-calculus bridge B3, and P versus NP remain OPEN.

Artifacts:

- `research/main/2026-11-03_0048_MAIN_NONAFFINE-LIFT-ER2-COLLAPSE-REFEREE308.md`
- `experiments/arc/lspv5_308/xor_rewrite_er2_referee308.py`
- `experiments/arc/lspv5_308/verify_xor_rewrite_er2_referee308.js`
- `results/raw/arc/lspv5_308/xor_rewrite_er2_referee308.json`
