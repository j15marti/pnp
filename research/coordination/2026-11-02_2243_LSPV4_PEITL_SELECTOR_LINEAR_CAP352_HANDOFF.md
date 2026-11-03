# LSPV-4 Peitl selector linear-cap and input-cost audit 352
**November 2, 2026, 22:43 PST.** Additive role handoff to the existing worst-case-minimum five-role team. **No task, schedule, state or ownership mutation. P versus NP OPEN.**

## Fixed-calculus result and duplication
Use the unchanged Rmix341, strict source-independent conservative VARDEF; all derived nodes cost one, original source axioms cost zero, explicit proof-premise indegree <=2, optimal derivation chosen freely. LSPV-3 GUARD-SUM-NONHORN349 already proves the universal selector sandwich, so do not claim this as a new mathematical discovery.

For minimally UNSAT pairwise variable-disjoint seeds F_i with m_i source clauses and explicit ordinary Resolution proof of q_i inferences, any full binary selector-guarded composition H_T satisfies

    sum_i m_i - 1 <= W_Rmix341(H_T) <= sum_i q_i +(k-1).

Every original source remains indispensable and its independent sign flip creates a SAT neighbor. Lower bound: connected authenticated binary proof ancestry. Upper bound: lift each leaf's resolution proof through its ancestor guards and resolve sibling guards bottom-up.

## New controlled test on a genuine excess-three mixed-hard seed
Use authentic Peitl-Szeider seven-clause five-variable source (mixed exact minimum nine from LSPV-5 REFEREE304, matching genuine nine-step Resolution proof). Thus seed excess 9-(7-1)=3. For k copied leaves,

    n=6k-1, m=7k,
    7k-1 <= W_Rmix341(H_T) <= 10k-1,
    0<= mixed excess <=3k.

These are **bounds, NOT exact k>1 mixed minima**. This family is not superpolynomial-hard against the fixed mixed calculus regardless of balanced or comb shape.

Independent Python producer and no-import Node referee generated 11 cases (k=1,2,4,8,16,32); Node passed 16,293 checks; SAT deletion and sign-flip neighbor witness checks 10,137; 66 malformed binary encodings rejected; odd/even K4 0/8 models, invalid signed pivot rejected. For k=32 balanced, 17,438 input bits and 4,610 eager parent literal reads; for comb, 40,875 source bits and 11,950 eager reads. Both have q=319 exhibited Resolution nodes, 8,932 pivot-only additional proof bits, and mixed W bounded 223..319. Source sign fields: 1,760 versus 4,329.

All-phase Python host measurement 2.12 s / 97,680 KiB RSS; Node 0.16 s / 33,524 KiB RSS. These **are not FLMV time/writable-space bounds**. In implemented transforms rho covers every phase, including source reading, preprocessing, proof generation/materialization, validation and temporary storage. No polynomial SAT algorithm or arbitrary-decider-to-proof compilation was derived. B1/B2/B3, superpolynomial Wbar and P versus NP remain OPEN.

## Falsifiers and next gap
(1) Selector growth of a hard constant-size core produces superpoly mixed W: **family failure**, explicit linear upper proof.
(2) Selector W must equal sum of leaf mixed minima plus k-1: **OPEN**, no additive lower proof.
(3) Same proof node count forces equal source/verification work: **FALSIFIED**, balanced versus comb.
(4) Short certificates avoid source-bit acquisition: **FALSIFIED only in the independent-sign deterministic query model**, not all Turing machines.

Next construction must force genuinely interacting components, eliminate the easy selector decomposition and certify excess cost under RES/AND3/XOR/CONVERT/VARDEF. Independently pursue the **weakest sufficient B3** with correct worst-case quantifiers.

## Published, readback-verified
- [LSPV-4 research report](../agents/lspv-4/2026-11-02_2243_LSPV-4_PEITL_SELECTOR_LINEAR_CAP352.md)
- [Standalone compact executable](../../experiments/arc/lspv4_352_peitl_selector_compact.js)
- [Machine-readable summary](../../results/raw/arc/2026-11-02_2243_LSPV4_PEITL_SELECTOR_LINEAR_CAP352_summary.json)
- Full producer, independent referee, raw data, logs and checksums in user-facing ZIP `LSPV4_PEITL_SELECTOR_LINEAR_CAP352_repro.zip`.
