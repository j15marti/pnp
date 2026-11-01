# ALLINPUT-PIN-CYCLE-TICKET305: all-input signed-incidence resource audit

**2026-11-01 08:36 PST | LSPV-4 Circuit Resource Auditor**

**STATUS:** PROVED/EXACT elementary all-source incidence theorem, external referee pending; COMPUTATIONAL independently verified original-source controls; KNOWN FLMV 5.7; CONDITIONAL ARC; **P versus NP OPEN**.

## Obstruction and four falsifiers

The sole NP-complete target consists of **all valid** duplicate-free proper Döcker monotone 3-SAT-(2,2) originals, rejecting malformed strings. Raw cofactors can be noncanonical. The universal adaptive controller still needs a proven polynomial **aggregate** work bound, or a paid arbitrary-A-to-Phi(A) power-short canonical compiler and separate strict same-machine FLMV transfer.

F1: A single pinned variable might generate arbitrarily many uncovered binary edges. FALSIFIED by the signed-quota injection below.
F2: Delta-zero affine can act at a nonempty valid root. FALSIFIED because root delta=2n/3.
F3: Ticket-product size is an unavoidable lower bound. FALSIFIED by paid component-factor controls, where 3^t naive choices collapse to 3t locally tested tickets.
F4: The incidence lemma implies native FLMV budgets. FALSIFIED as an implication because source reads, index heads, grammar, policy discovery, failed attempts, Gaussian rows, proof memory, child/guest access and retained peak remain charged.

## PROVED/EXACT universal incidence lemma

For every valid original F and coherent p pinning k original variables, let E2(p) be uncovered original clause IDs with exactly two free literals. For ANY original-clause-edge-disjoint family of simple odd binary cycles C_i of lengths ell_i>=3,

    |E2(p)| <= 2k,
    sum_i ell_i <= 2k,
    nu <= floor(2k/3),
    product_i ell_i <= 3^(2k/3).

**Proof.** Every uncovered binary source clause has precisely one pinned literal, necessarily false. Associate its unique pinned false signed occurrence, including original clause ID. This injection uses different source occurrences for different clauses. Every pinned original variable has exactly TWO falsified signed occurrences because it occurs twice positively and twice negatively. Therefore at most 2k uncovered binary source clauses exist. Authenticated edge-disjoint cycles use distinct IDs, and each has at least three edges. For x>=3, log(x)/x is decreasing, hence log(ell_i) <= ell_i log(3)/3; summing gives the product bound. This is uniform over SAT and UNSAT p, delta-zero and positive-delta states, and already-falsified clauses. It is NOT an arbitrary-SAT runtime lower bound.

At the empty root m=4n/3, f=n, u=m, eta=nu=0, so delta=2n/3>0 for EVERY nonempty canonical original. The restricted saturated-cycle affine terminal alone never decides an untouched original.

## Same-original SAT and UNSAT, independent controls

F9 original positive triples: (1,5,6),(2,3,8),(1,3,5),(4,6,9),(2,4,7),(7,8,9). Negative triples are negations of (4,6,8),(1,6,7),(2,3,4),(3,5,8),(1,2,9),(5,7,9). It is valid, duplicate-free and has exactly 70 globally satisfying assignments by exhaustive enumeration.

SAT cube x5=0,x6=1,x7=0,x8=0,x9=1 has **3** completions, delta=0, source-edge cycle (1,2,10), and matched UP-DPLL 3 nodes/132 literal tests.
UNSAT cube x8=x3=x7=x6=0,x1=x5=1 has **0** completions, delta=0, cycle (3,4,10), and UP-DPLL 1 node/57 literal tests.
Y6 has 20 root models and its x2=0,x3=1,x5=0 cube has 3 completions, delta=0 and original clause-ID triangle (1,2,5). These are exact source labels, NOT solver timeouts.

Producer exhaustively inspected all **19,683 F9** and **729 Y6** coherent cubes, testing the universal incidence/cycle inequalities including already-falsified states. The independent NO-IMPORT checker passed **82,044 assertions** covering the same original SAT+UNSAT cubes, original grammar, 36 signed original occurrence S/U targets/inversions, 264 SS/SU/US/UU source-pair modes, 64 Gray checkpoints, malformed-input controls, and independent DPLL. Producer loops visited 242,028 original clause records and 726,084 literal records. These are Python semantic operation proxies, NOT fully charged native FLMV source-bit measurements. The full producer, independent verifier and approximately 40KB original-indexed raw JSON are in the reproducibility archive.

For t disjoint copies of the SAME VALID F9 original with the corresponding SAT/UNSAT cube repeated, both have nu=t certified triangles, 3^t naive global tickets. Paid AND-component factoring requires at most 3t local tickets, plus discovery, proof and source costs. At t=16: **43,046,721** naive combinations versus **48** local tickets; SAT completion count is 3^16, UNSAT is 0. This is an EASY product hostile control and known component-factorization principle, not an all-input SAT lower bound.

## Full-work recurrence and FLMV firewall

For source-indexed state z, charge G(z) for input grammar, source/index/head reads, acquisition/failed rules, selector switches and proof checking. A delta-zero terminal costs G(z) + sum over all authenticated edge-choice vectors e of [row-build(e)+GF2(e)+rank/refutation/witness(e)]. An exhaustive AND/OR rule charges every exact successor's output/reencoding/bit access and total recursive work; Shannon fallback costs W(z|x=0)+W(z|x=1)+Cbranch(z). Decreasing free-variable count proves termination but not polynomial work; the ticket product bound may still be exponential when k=Theta(n), and delta itself can increase. Neither shared computation nor a favorable policy is free.

The original FLMV machine has read-only input with its own writable index tape, indexed work tapes, write-only output, and atomic index erasure on jump. Output tape cannot simply become a guest read-only child input. Dense augmented GF(2) matrix storage takes u(f+1) writable bits before proof provenance, while original cycle IDs take O(sum ell_i log m) bits in an explicit layout. Sparse replay trades space for charged reads and index operations; ancestor+guest+cache+proof **simultaneous peak** controls the actual space exponent. Logical XOR is only an OFFLINE diagnostic.

Primary FLMV Theorem 5.7 exact values remain d*(6/5)=23/45 and d*(241/200)=11642479/23232400, unique k=2 maxima, with the entire k>=4 tail strictly smaller. A hypothetical target solver (6/5,1/2) requires a separately proved near-linear, locally indexed SAT-to-Döcker compiler satisfying, with zero access exponent, b<11642479/11616200 ≈1.00226227 (plus strict setup/source/index/peak bounds). MODELBRIDGE-0012 is only an existing fixed-gadget second leg; the first LOCAL-COOK-MONOTONE22STAR1 is OPEN. NP-completeness does not transfer FLMV's numerical forbidden region.

## Project and primary research checks

Read first the 01:48 five-role handoff, then the 01:44 saturated-cycle theorem; inspected issue #3, root main.tex, AGENTS/CODEX/pnp-research, LSPV-4 GUEST-RECOMP304 and TARGET-STREAM-CUT285, LSPV-2 COMPONENT-SYNDROME-DP295 and LSPV-3 AFFINE-MATROID-COMPONENT-GATE301. Peer work already had matroid factoring and streaming grammar bounds; do not claim those as new.

Web queries included FLMV Theorem 5.7/index tapes, Döcker proper monotone 2,2, component model counting and bounded-degree triangle listing. Primary papers: Fortnow et al. (2005), https://lance.fortnow.com/papers/files/tst.pdf (pages 4 and 17 image-inspected); Döcker (2019), https://arxiv.org/abs/1912.08032; Chiba and Nishizeki (1985), https://doi.org/10.1137/0214017. Separate GitHub searches covered j15marti/pnp for component affine cycle, 3nu 2k, MODELBRIDGE, LOCAL-COOK, streaming grammar and far-index wrappers, and github.com/openai for SAT component and formal algorithms. Full local GitHub checkout preflight and a complete native indexed-TM implementation were unavailable; no novelty inference from missing search matches.

**OPEN next gate:** a fully paid all-input polynomial-total-work controller, OR a power-short both-label-correct hereditary arbitrary-A -> Phi(A) canonical transformation with separate strict same-machine numerical FLMV transfer. All five existing role identities, schedules and enabled states are unchanged. **P versus NP OPEN.**

END_OF_VERIFIED_REPORT::LSPV-4::ALLINPUT-PIN-CYCLE-TICKET305::P_VS_NP_OPEN
