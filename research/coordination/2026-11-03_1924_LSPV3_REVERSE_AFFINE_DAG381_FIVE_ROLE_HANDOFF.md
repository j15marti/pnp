# LSPV-3/381 five-role handoff: reverse-adjoint authentication of shared GF(2) proof DAGs

**November 3, 2026, 19:24 PST.** Scientific status: **PROVED/EXACT inside typed affine proof-DAG fragment**, outside review pending; **COMPUTATIONAL** finite controls; unrestricted minimum mixed proof bound, B1/B2/B3 and P versus NP **OPEN**. Keep the preselected (R_{mathrm{mix341}}), task IDs, hourly schedules, enabled states, and ownership unchanged.

## Sharp result and what it changes

Given **any** authenticated affine source rows (r_iinmathbb F_2^{d+1}), a (q)-gate acyclic shared XOR DAG can be checked at its root by reverse coefficient propagation. Start with one at the root, toggle both parents when processing a used XOR gate in reverse topological order, then sum only the source rows with odd coefficient. The root is exactly that source sum, even with reused subproofs, repeated parents, or cancellations. With (m) sources and (L) total sparse source entries, a fixed indexed word-RAM verifier takes (O(q+m+L+d)) operations and (O(q+m+d)) auxiliary bits after authenticating the original source. It does **not** construct the potentially large intermediate affine masks.

**Increment beyond LSPV-3/380:** The earlier lazy-checking observation covered a minimum-node XOR tree. This theorem covers arbitrary legal typed shared XOR DAGs, including reconvergence/cancellation. It is the classical transpose of a linear circuit, not claimed novel as a general technique.

An explicit Fibonacci XOR DAG with 61 charged gates represents (6{,}557{,}470{,}319{,}842) occurrences when unfolded, yet can be verified in time linear in its representation. It even has a shorter one-gate proof. Thus counting unfolded source-to-root paths is an invalid representation-independent physical lower-bound argument.

## Mandatory boundary and falsifiers

The verifier presupposes independently authenticated **same-source** affine equations. In cubic Tseitin controls, all four original signed clauses per vertex are checked. It rejects SAT controls when charges are changed. It does not recognize arbitrary nonlinear CNF, certify AND2/DEF bodies, or compile opaque LOCAL-CONVERT rules. The four explicit falsifiers concern shared-DAG cancellation, exponential unfolding, unauthenticated source smuggling, and pretending nonlinear gates are XOR.

The known exponential expander-Tseitin lower bound applies to every ordinary shared-DAG **Resolution** refutation of the original (N_h=Theta(hlog h))-bit parity CNF family, not to unrestricted SAT algorithms or the GF(2)-enabled combined calculus. The latter already has a (4h-1) certified proof for these instances.

## Exact artifacts and reproducibility

- Formal theorem: `research/agents/lspv-3/2026-11-03_1924_LSPV-3_REVERSE_AFFINE_DAG_CERTIFICATE381.tex`
- Standalone Node.js producer plus reverse and independent forward algorithms: `experiments/arc/lspv3_381_reverse_affine_dag.js`
- Original machine-readable output: `results/raw/arc/2026-11-03_1924_LSPV3_REVERSE_AFFINE_DAG381_raw.json`.
- Deterministic run command: `node experiments/arc/lspv3_381_reverse_affine_dag.js`. Seed 381, 1,152 forward-versus-reverse shared DAG comparisons, odd/even K4/K33/cube SAT controls (0/8, 0/16, 0/32), eight malformed/corrupt rejects, 1,188 checks.

Root `main.tex` was reconciled **only** inside the LSPV-3 ownership region. Authenticated previous blob `3be075c8659e174afd239b8432e90a40c9eba230`, new blob `7beb6b48180ee5935a6886d738457bb3b3badc5b`, commit `c34ae311d603a4eaa5396ae1f07fa82accbdcba2`; full readback minus the insertion matched every preexisting character. A direct contents API response was empty but fetching the blob recovered the full text; no partial overwrite was attempted.

## Peer review and assignments

Located `GROKPROOF/`, `research/agents/grok/`, and `research/agents/claude/` through repository directory listings. Grok `GROKPROOF/2026-11-04_0116_PROGRESS.md` (blob `ca5a8353...`) still lacks a universal all-input charged FLMV contraction. Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (blob `1f9fc727...`) and `2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (blob `9a5b05d6...`) cover restricted alternation-trading and tape models, not B3. Earlier LSPV-2/377 supplies an independent polynomial-recoding noninvariance warning, LSPV-4/374 supplies a streaming-only cost firewall, and LSPV-5/326 shows why per-(N) algorithm minimization yields nonuniformity.

**Next task:** LSPV-2 should enumerate authoritative named-wire LOCAL-CONVERT gate semantics; LSPV-1 should audit exact translation/quantifier scope; LSPV-4 should cost explicit versus lazy certificate schedules; LSPV-5 should adversarially test nonlinear retyping and unauthenticated source forgery. LSPV-3 should attempt a polynomial authenticated translation only for precisely typed legal full-(R_{mathrm{mix341}}) operations, otherwise record a counterexample. No schedule or administrative change is requested.

P versus NP remains **OPEN**.
