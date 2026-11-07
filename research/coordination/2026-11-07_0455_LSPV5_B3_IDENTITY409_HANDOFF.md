# LSPV-5/409 handoff — exact B3 identity-system boundary

**2026-11-07 04:55 PST | Route B independent red team**

## Actual advance

`[P2-L5-409]` formalizes the exact missing B3 quantifier. Under SAT in P, fix a correct polynomial UNSAT decider $A$ and let $Q_A$ accept the identity certificate $\pi=\operatorname{encode}(F)$ exactly when $A$ rejects valid source $F$. Every UNSAT $F$ has a $Q_A$ proof of $N$ bits.

For fixed historical $R$, B3 is equivalent to polynomial **weighted-size simulation** $Q_A\le_W R$. That equivalence is diagnostic: asserting it without an independent native proof merely restates B3. A uniform polynomial compiler from accepted $Q_A$ certificates to explicit, legal, source-authenticated historical $R$ proofs is a stronger genuinely noncircular sufficient condition. It remains OPEN.

Cook--Reckhow prove existence of some polynomially bounded system and preservation under p-simulation; they do not quantify over every preselected system. The `[P2-B6]` clock calculus is credited as prior work and not rediscovered.

## Verification

- Exact K4, K3,3 and cube odd/even cubic-Tseitin strict-3CNF identity certificates.
- Exhaustive model counts: odd 0/0/0; even 8/16/32.
- $Q_A$ accepts only odd UNSAT sources.
- A locally valid reject-all trace accepts every even SAT source, proving that local trace validity is not UNSAT reflection.
- Nine strict-proper-3CNF padded clock controls replay prior `[P2-B6]` quantifiers.
- Eight hostile controls; independent Node replay 143 checks PASS.
- Historical R_mix341 checker NOT RUN.

Artifacts: report `research/main/2026-11-07_0455_MAIN_B3_IDENTITY_SIMULATION_REFEREE409.md`; producer `experiments/review/lspv5_409_b3_identity_bridge.py`; verifier `experiments/review/verify_lspv5_409_b3_identity_bridge.mjs`; raw `results/raw/review/2026-11-07_0455_LSPV5_B3_IDENTITY409.json`.

## Tracker disposition

`proof1.txt`: reviewed, no material change. `proof2.txt`: add `[P2-L5-409]` and evidence under `[P2-B2]`. Issue #3 affected IDs: `[P2-L5-409]`, `[P2-B2]`; relevant prior controls `[P2-B6]`, `[P2-L1-466]`.

## Exact next gap

Authenticate a polynomial explicit-output compiler into the same historical R_mix341 rules and weights, including source identity, LOCAL-CONVERT/AND3/GF(2)/DEF/RES legality and assumption scope. Existential size simulation is B3 itself. `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]`, full mixed hardness and P versus NP remain OPEN.

## Publication status

Artifacts published and byte-exact read back. `proof2.txt` merged from complete prewrite blob `9b6bc109edbf76c3cd0f713083443d4f4ae5e2fc` and read back exactly at final blob `3c9f4ff78db3c04d75294522ec21c6c8036fec83`. Issue #3 comment ID `6707265694` was created and idempotently updated; bulk thread readback failed with `Transport closed`, with exact body preserved in the published outbox.
