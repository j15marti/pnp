# LSPV-4 single-child oracle/resource ledger 208
Date: 2026-10-28 17:36 America/Los_Angeles. Status: P versus NP OPEN. Independent mathematical referee pending.

## Concrete results and statuses
**PROVED/EXACT, restricted:** One closed unconditional SAT- and UNSAT-preserving single-child map with actual child bit length at most N^lambda for fixed lambda<1 yields a polynomial SAT decider, provided every recursive generation is polynomial and bases are directly decidable. As LSPV-1 and LSPV-2 already noted, existence of such a map in unrestricted form is equivalent to SAT in P, because a hypothetical polynomial SAT decider can print a constant YES or NO instance. It is NOT a new noncircular construction.

**RESTRICTED physical-length firewall:** The canonical expansion P_t=AND_{ij}(a_i OR b_i OR c_j OR d_j) shrinks to the selector F_t=AND_i(z OR a_i OR b_i) AND AND_j(NOT z OR c_j OR d_j) without losing pointwise existential equivalence. The source is Theta(t^2 log t) and child Theta(t log t) under actual DIMACS serialization; this restricted source grammar is not closed under repetition. For fixed t with arbitrary unchanged context R_k of k clauses, the source and child sizes have ratio tending to 1, falsifying a universal fixed-power shrink for the context-pass-through interface. This does not lower-bound all SAT algorithms.

**RESTRICTED NP-hardness transport firewall:** Embedding m-clause arbitrary G into a materialized quadratic canonical expansion E_m then shrinking once requires Omega(m^2 log m) output work and leaves a Theta(m log m) child. A hypothetical SAT solver with time L^K therefore gives the specific materialize-then-shrink pipeline exponent max(2,K), no improvement for K>=2. Fusing the two transformations can avoid that cost, but then the allegedly compressed expanded source was not actually generated.

**PROVED/EXACT interface accounting:** A virtual child-bit decoder with q_i parent queries per bit and a_i local operations obeys G_i<=a_i+q_i G_{i-1}. One semantic recursive call does not mean one source bit probe: a parity-chain 64->8->3->2 requires 3072 un-memoized bottom-source bit requests versus 542 bit reads across explicit levels (512 at original source). Caching is an alternative but must be fully charged. Finite computational checks passed: 139,866 assertions, zero failures; 69,904 exhaustive assignments t=1..4. Full local PDF, LaTeX, Python and raw JSON were generated; exact local SHA256 recorded in PDF. Publication of exact local files via GitHub connector is PENDING unless independently read back.

## Real machine ledgers
For a closed fully charged physical child map of generation time n^c and output size n^lambda on fixed-k read-only-input tape machine, recursive one-child total time is N^{c+o(1)} and work-space upper bound N^{max(lambda,sigma)+o(1)} (sigma = local generation-work exponent, disjoint held child buffers accounted). At one step followed by a hypothetical solver with time M^K and space M^s: t_k<=max(c,lambda K), s_k<=max(sigma,lambda,lambda s), conditional on a real same-model guest invocation. One-tape simulation: T1=O(Tk(N+Sk+log(Tk+2))), P1=O(N+Sk+log(Tk+2)); t1<=t_k+max(1,s_k), p1<=max(1,s_k). Physical one-tape input footprint >=N. No illicit reverse transfer, and no tape-only lower bound applies to indexed RAM. For two fully writable tapes count D1,D2 separately. Program interpretation, virtual source addresses and every failed choice must be included.

## Actual sources inspected (GitHub paths and source hashes)
* openai/math/preprints/Polynomial-Time-Unitary-Synthesis-from-a-Boolean-Oracle-October-5-2026/build/sections/01-introduction.tex, blob 5ad06c26238e: theorem has polynomial uniform quantum skeleton A_n, forall U exists target-dependent Boolean f, with no bound on computing/evaluating f classically.
* Same /06-recursion.tex, blob 65bf0450f460: one smaller controlled *quantum* circuit per level, t+O(n^10) qubits, O(n^13) slots.
* Same /07-compilation.tex, blob 869be8c325: oracle stores table entries at structured addresses.
* uds-psl/coq-library-complexity/theories/NP/TM/M_multi2mono.v, branch coq-8.16, blob 1231857819c4: source-inspected formal simulation and termination theorem explicitly retaining encoding length and simulated loop cost, not independently kernel compiled.
* uds-psl/coq-library-complexity/theories/TM/Single/DecodeTapes.v, blob 2bdc1cbf1f2a: formal tape encoding injectivity and time-indexed termination.
* j15marti/pnp/research/agents/lspv-2/2026-10-28_1722_LSPV-2_SINGLE_CHILD_PROJECTION_CLOSURE.tex, blob 70be73dec2a5: prior restricted contraction and NP-hard embedding, no closure.
* j15marti/pnp/research/coordination/2026-10-29_0005_ARC207_SINGLE_CHILD_DESCENT_FIVE_ROLE_HANDOFF.md, blob a1727350291e: prior 69,904 assignments and one-bit shrink target.

## Role-safe next targets
LSPV-1: test a genuinely recursively closed, unconditional SAT/UNSAT exact child map; distinguish a construction from a hypothetical decider hiding in the mapping.
LSPV-2: report true serialized output size and cache/guest-bit access for every alternative representation, including the next child of compact F_t AND R.
LSPV-5: independently falsify cost recurrences, audit native FLMV strict time/space assumptions, and initialize root main.tex specialist markers if authorized. Root main.tex as inspected (blob 959f12e5c91a) had *no* specialist OWNED markers; LSPV-4 must not edit the document absent markers under AGENTS.md. Root reconciliation is PENDING LSPV-5.

No agent count, ownership, schedule, or enabled state changed. Neither P=NP nor P!=NP proved.
