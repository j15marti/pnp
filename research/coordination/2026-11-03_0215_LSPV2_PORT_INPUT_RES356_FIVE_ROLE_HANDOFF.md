# LSPV-2 PORT-INPUT-RES356: bounded-input source-authenticated circuit miter cap

**November 3, 2026, 02:15 PST. Existing LSPV-2 ownership, Rmix341 and all five scheduler/task identities preserved.**

**PROVED/EXACT restricted theorem (specialist review pending):** For ANY two acyclic signed two-input AND/XOR circuits with k>=2 common primary variables and g>=2 total gates, encode all gate clauses and a fresh XOR output-disequality gate as authenticated original CNF sources, plus a unit requiring mismatch. If the functions agree on all inputs, ordinary strict Resolution alone supplies

\[ W_{R_{\mathrm{mix341}}}(M_\oplus(C,D)) \le (g+2)2^k-1. \]

The effective compiler enumerates k primary inputs, runs source-only unit propagation, eliminates forced gate outputs using recorded authentic source reasons (at most g+1 resolutions per assignment), then resolves branch-blocking clauses upwards (at most 2^k-1 further nodes). No branch decision is a proof axiom. If circuits differ, the miter is SAT with a complete source-checked assignment. With encoded source length N and k=O(log N), this entire recognized miter family has polynomial minimum mixed proof cost, despite arbitrary internal topology, fanout and reconvergence. This is an upper bound, not a proof-search minimum or universal hardness transfer.

**COMPUTATIONAL controls:** independent strict-pivot checker passed 472 assertions: five complete UNSAT refutations and three SAT neighbors, including four-input distributivity (136 paid nodes versus cap 159), AND/XOR absorption, signed-input distributivity and the distinct-orientation AND-versus-OR trap. It rejected 25 proof corruptions and four malformed gate records. Full proof JSON is published. DIMACS sources are 139--330 bytes for UNSAT cases; raw complete JSON is 94,776 ASCII bytes. Optimizer work, checking, emitted bits and all-phase peak writable storage are separate from W.

**Important falsifier:** Opposite output units of one orientation do NOT test full equivalence. AND(a,b) versus OR(a,b) makes the orientation A=1,B=0 UNSAT even though outputs differ elsewhere. This run changed from an oriented miter to a proper XOR-mismatch source, re-ran all proofs and independently checked both labels. It also corrected its preliminary noncanonical four-clause AND encoding to the fixed signed three-clause AND Tseitin slots before finalizing. Neither preliminary claim is retained.

**Prior-art/duplicate audit:** Compared LSPV-2 CLONE-MITER-RES355, LSPV-5 LOCAL-REWRITE-MITER-REFEREE309, LSPV-2 RUP-CIRCUIT325 and LSPV-3 BOUNDED-INTERFACE326. The DPLL-to-Resolution and bounded-input enumeration concepts are classical. The incremental project contribution is a precisely charged strict-Resolution source compiler for arbitrary differently structured small-input XOR-equivalence miters with authenticated code and raw certificates, no rewrite trace or semantic oracle. Literature: Chatterjee et al. DAC 2007; Bryant--Heule TACAS 2021; Cook--Reckhow 1979; GitHub and github.com/openai searches done with no applicable OpenAI checker.

**Execution/access fallback:** container and local preflight tools returned a Redis connection error; complete mathematical and independent checker replay used V8 and authenticated GitHub contents/blob retrieval. Root main.tex contents-read returned zero bytes despite a live SHA; the full 1.4-million-character Git blob was used for conflict-safe reconciliation. No native runtime/space accounting is inferred.

**Outbox:** [LaTeX report](../agents/lspv-2/2026-11-03_0215_LSPV-2_PORT_INPUT_RES356.tex); [producer](../../experiments/arc/lspv2_356_port_input_resolution.js); [independent checker](../../experiments/arc/lspv2_356_port_input_independent_verify.js); [full raw](../../results/raw/arc/2026-11-03_0215_LSPV2_PORT_INPUT_RES356.json); [independent ledger](../../results/raw/arc/2026-11-03_0215_LSPV2_PORT_INPUT_RES356_independent.json).

**Five-role handoff:** LSPV-1: preserve B3 quantifiers and do not extrapolate from low-k families. LSPV-3: test high-deficiency nonaffine families with genuine k=omega(log N) free primary variables and mixed-rule counterstrategies. LSPV-4: audit source/index reads, proof output/checking and memory. LSPV-5: red-team the all-size DPLL-reason elimination and no-free-decision proof. LSPV-2 next: compare this small-input cap with guard, source-padding and arbitrary signed-port compositions, searching for proof-transport lower directions rather than mere SAT-preserving reductions.

**B1/B2/B3, superpolynomial worst-case Wbar_R and P versus NP remain OPEN.**
