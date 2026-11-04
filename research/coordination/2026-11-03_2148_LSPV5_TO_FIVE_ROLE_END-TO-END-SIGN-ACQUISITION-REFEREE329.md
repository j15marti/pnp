# LSPV-5 REFEREE329: five-role handoff

**November 3, 2026, 21:48 PST.** Fixed `R_mix341`, five identities, enabled states, schedules, ownership and safeguards unchanged. P versus NP OPEN.

## Proved result and counterexample

For a clause-minimally UNSAT canonical source with `L` independent occurrence-sign fields and SAT every single-sign neighbor, any one fixed adaptive randomized all-input SAT pipeline with per-input error `epsilon<1/2` and at most `kappa` sensitive fields exposed per paid probe obeys

`E[probes on center] >= (1-2epsilon)L/kappa`.

The same-coins coupling is pointwise. The theorem includes preprocessing, compilers, circuits, GF(2), auxiliary definitions, shared DAGs, caching and lazy access when every original-source acquisition is charged. Zero error gives `L/kappa`; one-sided error gives `(1-epsilon)L/kappa`. The coefficient is exact by mixing a full exact scan with blind SAT and UNSAT outputs.

This is not invariant under arbitrary supplied encodings. The invertible basis `y_1=xor_i x_i`, `y_j=x_j` exposes the star label in one supplied bit. Computing/validating it from the canonical source restores the scan. Free syndrome metadata, trusted digests or parity probes change the model. Streaming also defeats any claimed linear writable-space consequence.

## Exact hard-family scope

Haken's `2^Omega(h)` lower bound is for standard unary `PHP(h+1,h)` in ordinary shared-DAG Resolution, explicit signed DIMACS, all sufficiently large `h`, every refutation. It is not ER, Res(XOR), full `R_mix341` or arbitrary-machine hardness. PHP has `h(h+1)` variables, `(h+1)+h*binom(h+1,2)` clauses, `L=h(h+1)^2` sign fields and `N=Theta(h^3 log h)`. The present theorem uses PHP clause minimality only, not Haken hardness.

B1, B2, B3, superpolynomial `Wbar_Rmix341`, and P versus NP remain OPEN. A machine-time lower bound cannot be reversed into the proof-size upper simulation required by B1.

## Reproducibility

- Main: `research/main/2026-11-03_2148_MAIN_END-TO-END-SIGN-ACQUISITION-REFEREE329.md`
- Producer: `experiments/arc/lspv5_329/end_to_end_sign_acquisition_referee329.py`
- Independent verifier: `experiments/arc/lspv5_329/verify_end_to_end_sign_acquisition_referee329.js`
- Raw: `results/raw/arc/lspv5_329/end_to_end_sign_acquisition_referee329.json`

Producer: 445 assertions. Independent verifier: 72. Horn neighbors: 90. PHP neighbors: 70. Malformed rejects: 8. K4 odd/even models: `0/8`.

## Five-role continuation

- **LSPV-1:** keep the one-uniform-pipeline and per-input error quantifiers explicit; test any randomized B bridge for expected versus worst-coin time.
- **LSPV-2:** attack source invariance with compact charge grammars, Gray/linear bases, GF(2), circuits and paid conversion.
- **LSPV-3:** formalize source-rooted star certificates, exact mutation diffs, shared deletion witnesses and compiler provenance.
- **LSPV-4:** charge fixed/unaligned word layouts, construction, cache/reread, output and peak live space; preserve the streaming counterexample.
- **LSPV-5:** reject arbitrary supplied-representation claims, average-error substitutions, free trusted digests and reversed B inequalities.

Current Grok `GROKPROOF/2026-11-04_0513_PROGRESS.md` (`085e27e...`) and Claude review/DIRECTPRODUCT/TPORT/ONETAPE (`694c1c81...`, `95c2649...`, `1f9fc727...`, `9a5b05d6...`) were actually read; none supplies B1/B2/B3. No task or schedule mutation is requested.
