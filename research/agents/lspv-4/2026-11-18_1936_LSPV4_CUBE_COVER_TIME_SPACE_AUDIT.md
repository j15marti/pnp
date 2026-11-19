# LSPV-4 Resource Auditor: certified cube-cover specialist and same-machine guard

**Date:** 2026-11-18 19:36 America/Los_Angeles. **Classification:** PROVED/EXACT restricted certificate theorem; COMPUTATIONAL finite audits; CONDITIONAL polynomial child-seed resource bound; OPEN unrestricted SAT or P!=NP. This is supplementary historical LSPV-4 work, not a modification to TMR-4's owned root manuscript.

## Candidate and four falsifiers

Candidate: Given an authenticated source F(z,x) = AND_{j=1}^q B_j(z,x_j), with private sets pairwise disjoint, an UNSAT path can be replaced by a **complete, deterministic, source-bound cube-cover certificate**. A leaf chooses an original block j whose restriction to its *partial* shared assignment is UNSAT over all remaining shared and private variables.

Falsifiers: (1) a block that is UNSAT at one point z but SAT at another completion of the proposed cube; (2) an OR row or aliased private variable breaking the AND/product factorization; (3) one guessed correct branch treated as coverage of all universal z; (4) uncharged source authentication, child inputs, certificate acquisition, output or retained workspace.

## Theorem 1: fully sound, complete restricted UNSAT coverage

Write BAD(j,P) when the source-original conjunction B_j, restricted by shared-variable partial assignment P, is UNSAT under *all* its remaining z and x_j choices. An UNSAT cube-cover certificate is a full binary tree: each internal node splits an unfixed shared bit i and has both children; each leaf (P,j) satisfies BAD(j,P).

A verifier traverses all branches and checks each BAD by a total correct deterministic child SAT solver, or unconditionally by exhaustive local assignments. If accepted, every full z reaches a leaf P, and the selected B_j has no completion. Hence F has no model. Wrong certificates yield REJECT/UNKNOWN, never an unsound UNSAT claim. Conversely, if F is UNSAT and private x_j are disjoint, for each full z some block B_j(z,x_j) is UNSAT; the complete depth-t tree supplies a valid leaf. Thus this certificate *language* is complete, possibly with exponentially many leaves. It does not establish small proofs or cheap discovery.

The SAT counterpart is a complete assignment (z,x_1,...,x_q), verified against **every original source clause**; independent local SAT assignments combine only when the private sets are disjoint. The example (x) AND (NOT x) defeats the combination rule if private variables alias. A single UNSAT block is insufficient for an OR of blocks. For arbitrary CNFs, a source-subformula contradiction at a cube remains *sound*, while the block-completeness and SAT-product theorem do not automatically transfer.

## Theorem 2: exact restricted certificate leaf bound, not an algorithm lower bound

For t shared bits and every u in {0,1}^t, let C_u(z) be a clause false exactly at z=u, introduce private x_u, and set B_u=(C_u OR x_u) AND (C_u OR NOT x_u). Let H_t=AND_u B_u. Each B_u is UNSAT **only** at z=u. Any partial cube P fixing fewer than t bits has a completion z!=u at which B_u is SAT, so cannot be a valid leaf. Thus every complete cube-cover certificate has **at least 2^t leaves**, and the full binary tree achieves exactly 2^t leaves.

Deleting any B_u* makes H_t SAT at z=u*. All local BAD paths at the other 2^t-1 assignments are genuine but not a global UNSAT certificate. **Crucial limit:** H_t itself has 2^t explicit blocks and Omega(t2^t) source bits. The bound is only for this deliberately restricted tree certificate language, and only linear (up to logs) in the explicit input size. It says nothing about arbitrary SAT algorithms, resolution proofs, compact circuit strategies, or P versus NP.

## Time-space ledger: same sequential execution

Let N be actual encoded source bits, t shared bits, q blocks, child length <=L, read-only certificate length K and ell accepted tree leaves. A canonical contiguous-block encoding with private IDs canonically namespaced as (j,i) can be authenticated in O(N) time and logarithmic indexing workspace. Arbitrary scattering/aliased IDs instead demand fully charged owner/disjointness checks and access preprocessing. Under the canonical input layout and a proved deterministic correct child solver A with T_A(L),S_A(L), a read-only prefix certificate can be verified in

    O(N + K + ell * (L + T_A(L)))

time and

    O(t log(t+2) + log(N+K) + L + S_A(L))

**peak writable bits**, sequentially sharing one child buffer, partial assignment and one live call. Source/certificate tapes are read-only, and output must be write-only to exclude its retained bits. Arbitrary block lookup via input rescanning adds up to O(ell N). With no A, exact leaf testing by exhaustive enumeration is unconditionally sound but can use exponential time. Certifier cost does not cover **certificate discovery or production** unless those stages are explicitly included.

The deterministic all-z block specialist scans every attempted block with all failed children included; it returns UNSAT iff every z has a bad block. With T_A(L)=O(L^p), S_A(L)=O(L^s), canonical source and sequential streaming, upper bounds are

    T_dec = O(N + 2^t q (L + L^p)),
    S_peak = O(L + L^s + t + log N).

On a SAT z, complete private witness extraction using a **decision-only** A by naive self-reduction adds O(q L (L+L^p)) time; an actual witness-producing seed might improve it. Storing the entire witness in writable RAM instead costs Omega(sum_j |x_j| +t) bits, while verified write-only streaming avoids that RAM charge. A free selected path, free SAT/UNSAT polarity or untrusted local UNSAT label cannot be substituted for a correct uniform both-polarity algorithm. A K-bit untrusted advice tape saves writable storage, not discovery or verification. Deterministic enumeration of 2^K advice choices incurs that full multiplicative cost; alternating universal branches must all be verified, or replaced by a sound checked shared strategy.

If n^.195 rows contain n^.65 blocks **per row** each of encoded size n^.35, q<=n^.845 and total explicit source size can be Theta(n^1.195), not Theta(n). With p=1, one z costs n^1.195+o(1), giving n^1.33 only if t<=(.135-o(1))log2(n) for the direct all-z scan. Naive decision-to-search adds a n^.35 factor, giving n^1.545+o(1), not 1.33. The claimed n^.5 writable space is feasible only under specified read-only source and streaming output conventions, plus the guest's actually proved S_A. The whole n^1.33 bound for general CNF is OPEN.

## Literature scope and polarity guards

Fortnow, Lipton, van Melkebeek and Viglas (JACM 2005, doi:10.1145/1101821.1101822) analyze random-access Turing machines and exclude simultaneous general-SAT time N^c, space o(N^d) for defined d curves. At c=1.33, the deterministic exclusion d=0.279104226449 and conondeterministic exclusion d=0.089299910571 are attained at k=3 under the cited recurrences. Thus N^.5 polylog N **is not excluded by these particular bounds**. Nondeterministic SAT witness verification already exists; a nondeterministic short accepting UNSAT certificate for arbitrary CNFs is a distinct, unproved coNP-in-NP possibility. An accepted proof-system-specific refutation is not a general time-space lower bound. Williams (2006, doi:10.1007/s00037-007-0221-1) strengthens subpolynomial-space lower bounds, not the claimed square-root-space regime. Buss-Williams (2015, doi:10.1007/s00037-015-0104-9) limits a specified alternation-trading proof paradigm, not all possible algorithms.

## Exact controls and audit status

Independent local Python finite audit: **1175 assertions, zero failures**, t=1..6, checking every omitted-block SAT deletion, every complete certificate, singleton BAD cube and incorrect shortened cube. Independently implemented standalone Node.js audit: **5133 assertions, zero failures**, t=1..8, including all deleted blocks. Full tree leaves: 2,4,8,16,32,64,128,256. The source-authenticated MST T5 witness constructor was independently rerun at deleted edge 0 for the 9-vertex/11-arc and 33-vertex/44-arc source; both full original-color witnesses passed every retained original arc. This does not independently certify UNSAT of the 33-vertex original.

Executable Node: experiments/arc/lspv4_2026-11-18_1936_cube_cover.cjs.
Raw control: results/raw/arc/2026-11-18_1936_LSPV4_CUBE_COVER_RAW.json.
The longer independent Python auditor, raw results and complete same-machine accounting are retained as separately downloadable local artifacts. This report is scoped to explicitly authenticated conjunctive blocks; actual historical row aggregation remains unverified.

**Barriers:** DISJ sanity passed but no new general complexity lower bound; relativization/unrestricted transfer OPEN; simultaneous DTISP numerical guard respected; configuration counting gives upper bounds, not a time lower bound; Natural Proofs/algebrization gates not invoked for this restricted certificate theorem. Full polarity routing, certificate discovery, arbitrary-CNF input/space preservation, and stronger algebraic or compact shared strategies remain OPEN. The five existing research roles and enabled/paused states were not altered. **MANUSCRIPT REVIEWED; NO MATERIAL CHANGE** because this LSPV-4 role does not own the current TMR-4 root manuscript. **P versus NP OPEN**.

References: [1] https://doi.org/10.1145/1101821.1101822; [2] https://doi.org/10.1007/s00037-007-0221-1; [3] https://doi.org/10.1007/s00037-015-0104-9.
