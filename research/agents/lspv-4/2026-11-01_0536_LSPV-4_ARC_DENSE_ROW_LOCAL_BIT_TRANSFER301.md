# LSPV-4 ARC-DENSE-ROW-LOCAL-BIT-TRANSFER301
**2026-11-01 05:36 PST.** PROVED/EXACT for the declared dense-row implementation, COMPUTATIONAL SAT/UNSAT controls, CONDITIONAL numerical FLMV transport, universal ARC and P versus NP OPEN.

## Exact obstruction
The canonical target remains **all valid duplicate-free proper Döcker Monotone 3-SAT-(2,2) instances**, and malformed encodings must be rejected. Residuals are not presumed canonical children.

The authenticated same-source valid F9 original has 70 full satisfying assignments. On pS={1:0,2:0,8:1,9:1}, the residual has (f,u,eta,nu,delta)=(5,6,4,0,0), affine rank 4 and exactly 2 satisfying completions. On pU={3:0,6:1,7:1,9:1}, the same state parameters hold, but the GF(2) parity-plus-preference rows are contradictory and there are zero completions. These are **coherent original-variable cubes**, not separate target-language formulas.

For t renamed disconnected F9 originals with these copied cubes, the valid original encoding has
N(t)=2H+36t(B+1), H=ceil(log2(12t+1)), B=ceil(log2(9t+1)).
A fixed-width **rectangular, dense** augmented GF(2) implementation with one full (5t+1)-bit row per active constraint occupies **6t(5t+1)** SAT-case bits or **8t(5t+1)** UNSAT-case bits. This is Omega(N²/log² N) fixed-location *writable work-tape extent* under this representation, and violates an N^(1/2) allocation. At t=128, N=55,318, SAT and UNSAT arrays respectively require 492,288 and 656,384 bits. Even one full row occupies 641 bits, exceeding sqrt(N)≈235.2. This **does not lower-bound another algorithm**: blockwise authenticated independent-component Gaussian elimination reuses constant-size (6×6 or 8×6) matrix payloads, plus paid discovery and indexing. The SAT product has 2^t completions; the UNSAT product has none.

## Matched indexed-input transfer lemma
Suppose a uniform, total and both-label-correct hypothetical SAT→canonical-Döcker reduction produces a **virtual** output of length N^(b+o(1)) with paid setup N^(alpha+o(1)) steps and N^(sigma0+o(1)) workspace, and each virtual output-bit request takes at most N^(rho+o(1)) native FLMV indexed-TM steps and N^(tau+o(1)) simultaneously writable/index-tape space. Fidelity includes source read/address construction, target index-head contents and atomic erasure, guest emulation, cached live state, failed attempts and ancestor retention. For a target decider of joint exponents (K,L), ordinary SAT then has **conditional** exponent upper bounds
T≤N^(max(alpha,bK+rho)+o(1)), S≤N^(max(sigma0,tau,bL)+o(1)).
This is ordinary composition, NOT a constructed reduction.

At the hypothetical target (K,L)=(6/5,1/2), FLMV c=241/200, d=11642479/23232400 requires all strict inequalities alpha<c, (6/5)b+rho<c, sigma0<d, tau<d, b/2<d. The strict length threshold is b<11642479/11616200≈1.00226227. For b=1, rho<0.005; b=1.002, rho<0.0026; b=1.003 already violates the space condition. Mere NP-completeness or a materialized polylog-expanded reduction does not establish the exact arbitrary-output-bit interface.

## Physical XOR and source reads
Declared source-index access protocol: w=ceil(log2(N+2)) index cells, write w index bits, rewind w head steps, perform one indexed jump with atomic index erasure, then read one source symbol. Its counted protocol work is (2w+2)N primitives **before address arithmetic**. The index tape begins/ends blank. Its physical cumulative content-XOR is 2*sum_{i=0}^{N-1}popcount(i), while endpoint XOR is zero. **An FLMV jump may atomically erase multiple bits in one native step**; a one-cell-per-tape-per-step assertion is invalid for those jump steps. Initially blank index contents nonetheless imply the restricted amortized bound D_phys≤2W_nonzero≤2kT for k fixed tapes.

At t=64: source N=25,364, index width w=15, 25,364 source reads, 380,460 index writes (including zero writes), 380,460 index-head moves, 25,364 jumps, total 811,648 counted primitives before address arithmetic. Index content cumulative XOR is 362,736; endpoint XOR=0. The separately specified 9-assignment-bit+24-clause-count-bit OFFLINE logical state trace for 64 six-variable assignments has binary/Gray cumulative XOR 598/449 and assignment-subtape toggles 120/63. No full guest/ancestor physical machine trace is claimed.

## Falsifiers and independent checks
F1 dense delta-zero matrix always fits sqrt(N): **falsified for the stated representation**. F2 this is an arbitrary-SAT-machine lower bound: **falsified by recognized block decomposition**. F3 any near-linear reduction automatically transfers numerical FLMV: **falsified when local bit-query overhead exceeds its exponent margin**. F4 zero endpoint XOR implies zero work: **falsified by charged source access**.

A no-import independent producer verifier tested 6,614 assertions with zero failure, including all 512 original F9 assignments (70 global models), SAT/UNSAT 2/0 cube completions, 264 clause-pair SS/SU/US/UU masks, source endpoints, complements, flips, malformed controls, full GF(2) row-XOR UNSAT provenance, binary/Gray projected XOR, indexed access popcounts, and exact rational FLMV tail. A separately executed independent JavaScript source-authenticated U198/V198 check used the published U198 fixture, 384 six-block boundary queries and 19,488 UP-DPLL nodes. U198 is UNSAT because every boundary assignment is eliminated, and V198's distinct 198-bit witness verifies SAT. Prior ordinary UP-DPLL on the small F9 UNSAT cube required one node, so dense-array cost is not intrinsic decision cost.

Exact FLMV Theorem 5.7: d*(6/5)=23/45 and d*(241/200)=11642479/23232400; k=2 uniquely maximizes each and the entire k≥4 tail is strictly excluded by c^(-4)<d_2(c).

## Prior work and search record
Authenticated 01:48 five-role handoff, 01:44 SATURATED-CYCLE-AFFINE-TERMINAL1, AGENTS/CODEX/pnp-research, root main.tex, 09:48 redirect/contract, AFFINE-SMALLBIAS-DESCENT-GATE2, CONSTRUCTION-STRENGTHEN17, ARC-LINEAR22-SATURATION1, LSPV-2 STREAMED-WALSH-OVERLAP297, LSPV-4 ZERO-CYCLE-CUBIC300 surveyed. Source tests reproduce earlier controls; no novelty is claimed for standard matrix composition or component reuse.

Primary papers: Fortnow, Lipton, van Melkebeek, Viglas (2005), https://lance.fortnow.com/papers/files/tst.pdf, §§2.1,3.1,Thm5.7 (actual PDF screenshots verified); Döcker (2019), https://arxiv.org/abs/1912.08032. Web/Google queries: FLMV Theorem5.7 indexed model; Döcker monotone (2,2) local reduction; space-efficient GF2 rank; locally computable SAT normalizers. GitHub connector searches in j15marti/pnp: "GF(2) elimination source read index tape", "bitonic local output bit target strict22", "ARC-EXPLICIT-BRANCH-CONFIGURATION"; separately in github.com/openai: "SAT XOR elimination", "circuit-sat". OpenAI math returned generic unrelated snippets. Relevant existing XOR engineering: https://github.com/msoos/cryptominisat. No novelty inferred from missing results.

Full source-indexed raw, portable no-import independent verifier, exact rational code and microtrace ledger are in the attached reproducer archive. The repository skill's local preflight script could not run without a full mounted checkout; authenticated connector searches/fetches and guarded root readback were used as fallback.

**OPEN:** a genuinely uniform, malformed-rejecting, full-bit-addressable, near-linear SAT-to-Döcker normalizer and independently a hereditary all-valid-target arbitrary-A→Phi(A) compiler with strict same-realization guest/ancestor/selection space. P versus NP remains OPEN.

END_OF_VERIFIED_REPORT::ARC_DENSE_ROW_LOCAL_BIT_TRANSFER301::P_VS_NP_OPEN
