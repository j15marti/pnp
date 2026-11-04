# LSPV-5 to five-role handoff: LEFT-INVERSE-IMAGE-AUTHENTICATION-FIREWALL-REFEREE338

**November 4, 2026, 06:48 PST. Fixed `R_mix341`, five roles, enabled states, hourly schedules and safeguards unchanged.**

## Exact result

The recognizer-conditioned active-source recoding route is valid but duplicates LSPV-1/373, REFEREE323/325, LSPV-2/375 and LSPV-3/394. Do not claim a new representation-independent theorem from it.

The new exact counterexample is about authentication. For the satisfiable source

`s = p cnf 1 1; (1)`,

the honest lossless encoder keeps active `(2)` and stores every raw bit twice in a disjoint signed-unit tag namespace. Replace only `(2)` by an empty clause, keeping every tag. The tag decoder still returns `s`, but the forged target is UNSAT. Therefore

`D(E(s))=s` does not imply that D authenticates arbitrary G, and `D(G)=s` does not imply `G=E(s)` or semantic projection equivalence.

Full image equality `G=E(D(G))` rejects the forgery. It does not solve proof transport: an honest image may still contain a recognizer-added contradiction. Every used target axiom/inference must also carry a polynomial source-rooted macro.

## Fixed-system limits

- Haken: canonical unary PHP requires `2^Omega(h)` ordinary shared-DAG Resolution lines under explicit `Theta(h^3 log h)` signed encoding. Not ER, `Res(XOR)`, `R_mix341`, or machine hardness.
- LSPV-2/341: canonical connected bridgeless cubic odd-Tseitin has exact `W_Rmix341=4h-1`.
- Honest recognizable-family recoding can make encoded cost zero, but the odd-Tseitin gap is only linear-to-zero. It does not refute a polynomial envelope or B1/B2/B3.
- Haken forces exponential ordinary-Resolution proof backtranslation output, not exponential SAT runtime.

## Role actions

- **LSPV-1:** distinguish left inverse, image membership, semantic projection, proof ancestry, and arbitrary-decider simulation in every quantified invariant.
- **LSPV-2:** use compact GF(2) and unit-tag encodings as mandatory controls; do not promote the `4h-1 -> 0` changed-source calibration to polynomial bridge failure.
- **LSPV-3:** require full image authentication or equivalent certificate semantics; a payload decoder that ignores active clauses is not a verifier.
- **LSPV-4:** charge parse, recognition, `Theta(N log N)` explicit output, decoder reads, re-encoding comparison, random access/indexing and all-phase peak. Lazy output does not authenticate omitted bits for free.
- **LSPV-5:** reject any invariant surviving only because off-image forgeries or recognizer-added contradictions were silently excluded; audit source-rooted macros separately from model equivalence.

## Artifacts

- `research/main/2026-11-04_0648_MAIN_LEFT-INVERSE-IMAGE-AUTHENTICATION-FIREWALL-REFEREE338.md`
- `experiments/arc/lspv5_338/recognizer_conditioned_recoding_referee338.py`
- `experiments/arc/lspv5_338/verify_recognizer_conditioned_recoding_referee338.js`
- `results/raw/arc/lspv5_338/recognizer_conditioned_recoding_referee338.json`

Python: **1,929 assertions PASS** over 273 records (265 valid, eight malformed). Independent Node: **415 assertions PASS**, including an independent reconstruction of the forged target.

Current Grok `GROKPROOF/2026-11-04_1322_PROGRESS.md` and the actual Claude DIRECTPRODUCT/TPORT/ONETAPE reports were read; none supplies B3 or a full-mixed source compiler.

**B1/B2/B3 for fixed `R_mix341`, superpolynomial `Wbar_Rmix341`, unrestricted SAT hardness, and P versus NP remain OPEN.**
