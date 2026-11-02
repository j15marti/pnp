# LSPV-3 to five roles: GUARDED-EXPANDER-MIXED-ESCAPE341

**November 2, 2026, 12:24 PST.** Research result only. All task identities, states and schedules unchanged. **P versus NP remains OPEN.**

## Verified scientific result

An infinite family of *clause-minimally UNSAT*, every-sign-sensitive, selector-guarded cubic-expander Tseitin formulas has exponential **dense connected-cluster join/projection table** burden yet only linear **minimum mixed proof-DAG cost** for the declared fixed calculus Rmix-v1.

For t guarded disjoint copies of an h-vertex odd-charge cubic expander, Q has m=1+4ht clauses, L=t+16ht independently sensitive literal signs, and bit length N=O(ht log(ht+2)). The exact fixed-calculus inequality is:

```
ceil(4*h*t/3) <= W_Rmix-v1(Q) <= t*(2*h+1).
```

The lower bound is source-essentiality plus explicit inference fan-in <=4. A legal upper proof extracts h source-verified guarded XOR3 equations, adds h-1 rows, infers one negative selector, and then resolves each negative selector with the master clause. Connected induced clusters have parity boundary relation with 2^(|cut|-1) allowed tuples. Expansion gives 2^(alpha*h/3-1) in *dense* materialized tables only. No inference from these dense tables to general SAT machine work is valid.

**Classification:** PROVED/EXACT under stated Rmix-v1 assumptions, KNOWN THEOREM for existence of three-connected cubic expanders, COMPUTATIONAL for small-graph checks. This is a **FAMILY FAILURE** for the proposed hardness conjunction (sign sensitivity + cut expansion), not a failure of B2/B3 and not a new general-SAT lower bound.

## Artifacts, reproducibility and readback

* [Role-owned LaTeX report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-3/2026-11-02_1224_LSPV-3_GUARDED_EXPANDER_MIXED_ESCAPE341.tex), blob 3255216512c0a09ab5b233726cc4415bf76ded2f.
* [Independent Python producer](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv3_guarded_tseitin_mix341.py), blob 301826318243272f5c5307509a2dceb79912f3bb.
* [No-import JS referee](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv3_341_independent.js), blob 20e562b6a8dbbb609de25a4a58eb73018261c035.
* [Full machine-readable GitHub raw formulas, proof DAGs and sign/deletion witnesses](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-02_1224_LSPV3_GUARDED_TSEITIN_MIX341_public.json), 117012 UTF-8 chars, blob cd7456d1d3142642eb501a14faf47bd71fca1380.
* [GitHub-independent-readback check record](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-02_1224_LSPV3_GUARDED_TSEITIN_MIX341_verify.json).

A separately written original local no-import referee passed 6081 assertions; following GitHub publication, the Github-hosted JS referee was executed against the GitHub-hosted JSON inside a JavaScript runtime with native-module read/assert shims and passed **20843 checks**, including 743 unique literal-sign SAT controls (1486 visits including corrupted replay), 99 original inference nodes, five rejected corrupted certificates and five rejected malformed encodings. Five cases: K4 x1/x2, cube Q3 x1/x2, Petersen x1. Dense minimax cut widths 4,4,4,4,5; proof counts 9,18,17,34,21. The local complete raw payload and a longer five-page PDF/LaTeX version are preserved in a user-linked reproducibility archive.

## Corpus, duplication, access and next target

Read the user-approved 12:04 PST five-role refocus at exact commit/blob, issue #3, AGENTS.md/CODEX.md/pnp-research skill, LSPV-1/335, LSPV-2/339-340, LSPV-3/340, LSPV-5/294 and historical guarded parity and selector interface reports. Primary references: Friedman, Wormald, Urquhart, Ben-Sasson/Wigderson, Cook/Reckhow. Project and github.com/openai code searches found prior source support, sign sensitivity, guarded XOR and Lean SAT components; these are credited as prior art. The new tested combination invalidates a hard-family heuristic, not P versus NP.

Root `main.tex` was read from GitHub at blob a9e513dbb40fd408931e7595616cd7369332b8fe but the fetch returned zero content; no specialist marker was available. Consequently it was NOT overwritten. LSPV-5 should reconcile when the current authorized region can be recovered. Local GitHub clone/preflight could not run due DNS failure; direct GitHub connector reads/writes and complete readbacks worked.

**Coordination:** Rmix-v1 is an explicitly declared *candidate* fixed combination, not yet a ratified same-version five-role shared R. The peer R4 and R2/XOR systems differ in rule signatures; use only model-matched comparisons. B3 remains OPEN:
SAT in P implies polynomial upper bound on worst-case W_R for the **same fixed R**.
Next construct candidate families with no cheap GF(2) parity elimination, no cheap gate identity, and no narrow Resolution refutation; seek an invariant that survives ALL allowed mixed rules and then adversarially search for shortcut proofs.