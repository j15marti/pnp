# CONTEXTUAL-VALUE-HAMMING235: additive LSPV-2 handoff

Date: 29 October 2026, 18:12 America/Los_Angeles. Role: circuit and reduction builder. Existing five agents and schedules unchanged. No P versus NP result is asserted.

## Exact independently proved restricted result

The reusable summary is prepared from a fixed source `A_a(X)=AND_i(x_i=a_i)` **before** a parity continuation `B_{w,t}(X,Z)=[w dot X=t]` is known. There is a read-only original source, a rank-L linear stored summary `H a`, and a separate charged source-sign bit-probe coordinate. For each query mask `w`, **every** deterministic exact, adaptive and nonlinear continuation using that linear summary needs at least `dist_H(w,rowspace(H))` original source-coordinate probes. The bound is attained by probing a minimum-weight coset leader. Search for the leader, parsing and verification are charged in total time. The proof is an affine-fiber transcript indistinguishability argument, independent of optimal SAT decision time.

At boundary size seven the exact optimal linear-summary frontier is `(L,Q)=(0,7),(1,3),(2,3),(3,2),(4,1),(5,1),(6,1),(7,0)`. Explicit Hamming generator rows `(49,82,100,120)` store 4 bits and guarantee at most one original-coordinate probe across every mask. Literal storage of four source bits instead needs three probes on an adversarial mask. A direct sum of r blocks achieves `(7r,4r,r)` for boundary bits, stored bits and maximum source probes. The sphere-covering inequality `2^L sum_{j<=Q} binom(b,j)>=2^b` applies **only** to this exact fixed-linear-summary probe model. The Hamming point is tight. As source-free preparation, `L>=b` is necessary for exact answers to every later parity mask, but this does not apply to full joint `A,B` SAT decision.

## Contextual information value

Certified datum notation `(I)\mid_v` uses a source-row equality certificate with charged reading; target x and current K determine value `Phi(K)-Phi(K+I)` with `Phi=log2 max(1,#possible target projections)`. Two source-authenticated XOR shares each have marginal v=0 at K empty, while either has v=1 after the other. Repeated facts have v=0. Net value becomes negative after certificate costs; raw value can be negative only for a separately defined nonmonotone potential (an added verification obligation). Scores are not Shannon entropy and are not additive. The small interpreter explicitly charges exponential score-discovery enumeration rather than assuming it free.

## Controls, models and provenance

Exact deterministic runner: 16,384 exhaustive all-source/all-mask Hamming comparisons, Hamming word distance and exact `(L,Q)` witnesses, XOR-gate truth table, 2SAT SAT/UNSAT, mixed 2SAT+XOR SAT/UNSAT, connected signed strict22 six-variable SAT (10 models) and 15-variable W1 UNSAT (`2^15` assignments enumerated). Code and JSON paths in `research/agents/lspv-2/` accompany the report. W1 source: `connector231.py`, blob `ddfea2285320d3143ac653986e708d562ecabde6`. Sage Hamming code source: `src/sage/coding/hamming_code.py`, blob `431e660fae77184147230223f66c76f2d5f04b38`; covering-radius definition: `src/sage/coding/linear_code.py`, blob `0cc870083077303ea087a94bdefb767e18e6ebd6`. Historical same-project online-context lower bound was already in LSPV-5 DECISION-CONTEXT-SEPARATION202. Primary literature: Hamming 1950; Darwiche and Marquis JAIR 2002.

The RAM bit-probe coordinate Q is **not** total time T. Preparsing A and B, decoding the query, candidate comparisons, source index arithmetic, the original read-only source bytes, retained summary, and writable workspace are separately accounted for. Indexed RAM proof is not a one-tape, two-tape or fixed UTM lower bound. Constructed `A_a AND B_{w,t}` is **not** strict22. Strict22 controls are label and grammar checks, not a transfer of the theorem. No fresh claim of polynomial-time general SAT, source-free online compression, or P versus NP separation is made.

## Targets for existing roles

LSPV-1: test whether a non-tautological context-value potential is independent of optimal decision time and certified per primitive transition; audit full joint-solver bypass.

LSPV-2: derive a fully source-authenticated, general connected exact22 boundary-summary family with explicit construction P(N), stored length L(N), retained-source continuation Q(N), and hostile affine/Tseitin controls. Prove or falsify a tight nontrivial frontier beyond the canonical unary source promise.

LSPV-3: use one uniform adaptive controller to test joint preprocessing, caching, changing target masks and duplicate certificates; seek nonlinear-summary counterexamples to linear-only generalization.

LSPV-4: model-match bit-RAM parity probes to indexed bit-time and native one-tape/two-tape head movement; do not propagate restricted Q lower bounds to FLMV SAT time-space claims.

LSPV-5: independently verify affine-fiber lower bound, sphere covering equality, score-discovery charging, and root ownership reconciliation. Keep historical proofs and main OPEN labels unchanged beyond authorized region.

## Status

PROVED/EXACT RESTRICTED: affine-fiber code-distance lower bound; source-free reusable summary injection; explicit seven-coordinate code frontier and direct-sum construction. FALSIFIED/RETIRED: literal storage optimality at fixed L=4; intrinsic or additive contextual fact value. COMPUTATIONAL: finite SAT/UNSAT and Hamming controls. OPEN: arbitrary semantic summaries, general formula families, tight physical-runtime tradeoffs, both P=NP and P!=NP.