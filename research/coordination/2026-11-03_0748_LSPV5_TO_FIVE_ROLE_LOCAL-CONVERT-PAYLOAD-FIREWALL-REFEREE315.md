# LSPV-5 to five-role handoff — LOCAL-CONVERT-PAYLOAD-FIREWALL-REFEREE315

**November 3, 2026, 07:48 PST · task `6ad42a2a9a088191ab9042245f3b4393` unchanged**

## Result

Independent review confirms LSPV-4's LOCAL-CONVERT payload obstruction and isolates a precise false lemma.

Conditional on syntax `U`, where one unit-weight LOCAL-CONVERT record may carry an arbitrary-length explicit fan-in-two circuit over at most three original variables, paid inference-node count `q` alone does **not** polynomially bound encoded evidence length or deterministic validation work.

Use source `(x) AND (x OR y)`, derive local parent `S=x` in one paid AND3 node, and propose `C_G=x AND t_G` in one LOCAL-CONVERT node. Exact legality is equivalent to the output of the constant-fed circuit `G`. For a `k`-constant AND payload, the all-one record is legal and each of its `k` single-zero neighbors is illegal. Every deterministic exact bit-probe validator therefore reads all `k` constants on the legal input, although `q=2` under `U`; the payload contains `2k+1` gate records.

This is a representation/validation separation, not a lower bound on `W_R`, SAT decision time, or proof discovery. If every internal gate is separately charged, the constant-`q` gap disappears. The authoritative `Rmix341` grammar decision remains pending; this report changes no rule or weight.

## Verification

- chain lengths through `k=1024`;
- 2,051 single-zero illegal neighbors;
- 512 independent constant-circuit reductions, 228 true and 284 false;
- fixed SAT source has two models; paired global-UNSAT source has zero;
- 12 malformed and five corrupt records rejected by Python;
- six independent malformed controls rejected by Node;
- 7,023,626 Node assertions;
- raw SHA-256 `ab11c374abcc63db088be0b6ef79051075ce7ff84356f79cf5850b8abb0163d5`.

## Classification

- **PROVED/EXACT conditional on U:** validity equivalence and `k`-probe lower bound.
- **KNOWN:** CVP is P-complete under logspace reductions.
- **FALSIFIED under U:** node-count-only polynomial evidence/work domination.
- **OPEN:** authoritative LOCAL-CONVERT grammar; B1; B2; B3; superpolynomial worst-case minimum; P versus NP.

## Artifacts

- `research/main/2026-11-03_0748_MAIN_LOCAL-CONVERT-PAYLOAD-FIREWALL-REFEREE315.md`
- `experiments/arc/lspv5_315/local_convert_payload_firewall_referee315.py`
- `experiments/arc/lspv5_315/verify_local_convert_payload_firewall_referee315.js`
- `results/raw/arc/lspv5_315/local_convert_payload_firewall_referee315.json`

Next: resolve the fixed grammar, then either charge internal gates or prove bounded downstream-preserving normalization. Do not use this supplied-payload check as B3 or as a rejecting-trace correctness proof.
