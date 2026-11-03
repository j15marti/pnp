# LSPV-5 handoff: EXTENSION-SIMULATION-BARRIER-REFEREE299

**November 2, 2026, 16:48 PST. Status: PROVED/EXACT syntactic theorem; COMPUTATIONAL finite controls; B1/B2/B3 and P versus NP OPEN.**

For the unchanged binary-premise unit-weight Rmix341, define \(ER_2\) over exactly the same finite two-input gate basis as charged DEF. Every \(ER_2\) extension instruction maps to one charged DEF node with the identical fresh output, inputs, gate tag, and authenticated defining slots; every resolution maps to the identical RES node. The topological translation preserves sharing and contradiction. Hence

$$
W_{Rmix341}(F)\leq W_{ER_2}(F)
$$

for every UNSAT \(F\), and the same inequality holds for worst-case maxima by encoded length. Therefore a superpolynomial mixed lower bound would also be a superpolynomial Extended-Resolution lower bound.

**Family dispositions.** BPHP is retired as a mixed-hard candidate: Cook has polynomial ER proofs, and LSPV-3 now supplies a full polynomial Rmix341 compiler/replay. Braun's claimed DAG Res(XOR) BPHP lower bound does not survive the added DEF rule. Peitl–Szeider finite Resolution extrema and random-3-CNF Resolution hardness do not transfer without an invariant against every mixed rule. Odd Tseitin remains the XOR-easy negative control.

**Finite audit.** A strict producer and independent no-import verifier checked a three-source UNSAT formula with one paid AND DEF plus five RES nodes; its SAT sign-neighbor, all source deletions, BPHP(3,2) and all 12 single-sign flips, odd/even \(K_4\), eight malformed inputs, and four corrupted certificates. All passed. The six-node certificate is an upper example, not a minimum (direct Resolution uses two nodes).

**Bridge classification.** No arbitrary decider trace was translated, no worst-case runtime domination was proved, and SAT in P was not shown to yield polynomial Rmix341 proofs. B1, B2, and B3 remain OPEN. The new result is a proof-system lower-bound barrier, not a P-versus-NP result.

**Artifacts:**

- research/main/2026-11-02_1648_MAIN_EXTENSION-SIMULATION-BARRIER-REFEREE299.md
- experiments/arc/lspv5_299/extension_simulation_barrier_referee299.py
- experiments/arc/lspv5_299/verify_extension_simulation_barrier_referee299.py
- results/raw/arc/2026-11-02_1648_LSPV5_EXTENSION_SIMULATION_BARRIER_REFEREE299_raw.json

**Next exact gap:** choose a growing nonaffine signed family and either prove an invariant surviving RES/AND3/XOR/CONVERT/DEF or exhibit the shorter mixed proof; independently attack B3 for this same preselected calculus.
