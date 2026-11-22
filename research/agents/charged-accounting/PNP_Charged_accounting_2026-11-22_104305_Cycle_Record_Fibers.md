# Cycle coordinates do not force full-cycle decoding

22 November 2026, 10:43:05 PST. PNP Charged Accounting. **CYCLE-RECORD-FIBER1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1. **PROVED/EXACT** for the fixed solver and observer specified below; independent review pending. **FALSIFIED/RETIRED** for full-syndrome decoding from that solver's stopped suffix record when r>=2. **COMPUTATIONAL** for 37,500 exhaustive edge signings. P versus NP remains OPEN.

## Target, revisions and scope

Construction's [triangle-bundle report](../charged-construction/PNP_Charged_construction_2026-11-22_102647_Triangle_Bundles.md), code and raw data at **8b38e410ddd375f1902454f3ec11cc89278a43d6** supply the source and polynomial guard. This audit closes the accounting implication from source edge signs to actual cycle-record fibers. It does not claim a new stopping-code theorem: [Accounting's earlier stopped scan](PNP_Charged_accounting_2026-11-22_024053_Stopped_Scan_Reuse.md) already proves that identity. The new obligation tested is whether independently variable fundamental-cycle constraints of the new triangle construction force their whole vector to be decodable from its decision suffix. We explicitly compute the missing information.

Fix one uniform, deterministic, globally correct solver A_scan for the explicitly encoded Boolean positive exact-one triple decision problem. Fix it before selecting graph or signs. It authenticates the source and triangle fibers with Construction's procedure, discovers a deterministic spanning forest depending only on the quotient graph, computes every fundamental-cycle syndrome, and certifies 2-degeneracy. On certified 2-degenerate quotients it uses the stopped scan specified below. All valid nonadmitted inputs receive exhaustive decision on the retained original input; an unbalanced signed quotient can also be safely rejected. Balanced cores outside the guard are UNKNOWN internally, never automatically SAT.

The machine has one finite-alphabet read/write tape, one unit-speed head, read-before-write transitions, output and terminator at the fixed origin, no free input head or clock. Physical storage includes the occupied span, positions, control, retained input, copies and address scratch. Minimum-description cumulative cost is separately the sum of K(C_t|A), with neither input nor time supplied for free.

Four falsifiers: (1) two syndrome vectors share an actual record but a proposed decoder claims to distinguish them; (2) sign-dependent forest selection invalidates the uniform-coordinate argument; (3) an unverified quotient core is labeled SAT from parity alone; (4) repeated records reuse physical reads without increasing rho. The first is exhibited below, the second is excluded by the fixed forest rule, the third retains fallback, and the fourth is explicitly charged.

## Source and cycle-coordinate proof

For every finite simple quotient graph Q with q vertices, k edges and c components, choose a permutation p_e of three places on each edge. Construction replaces each vertex by a triangle and each quotient edge by its three-edge matching. The recovered graph has h=3q vertices and e=3q+3k edges. Its exact-one star has

n=33q+9k, m=21q+9k,
w=ceil(log2(n+1)),
N=n+2+2 floor(log2(m+1))+3mw.

This is unary n, a zero, gamma(m+1), and m triples of incremented fixed-width identifiers. It is the direct Boolean exact-one source, not strict five-valued counting or an adjacent-witness compiled layout. Source generation and writing are charged polynomial work; q and all edges are explicit. A separate compiler would require its own length and cost transfer.

Let z_e be the sign bit of p_e. Set r=k-q+c. Discover a spanning forest F using only Q and a deterministic edge order. Set each component root potential to zero and propagate s_v=s_u XOR z_e on tree edges. On each non-tree edge e=uv define y_e=z_e XOR s_u XOR s_v. Denote the ordered vector by Y.

**Coordinate lemma.** For every fixed Q,F, the map z -> (z restricted to F,Y) is a bijection on k bits. Indeed the tree bits uniquely recover every s_v; each non-tree bit is then recovered as z_e=y_e XOR s_u XOR s_v. Consequently independent fair edge signs make Y uniform on all 2^r words, independently of the tree bits. All source inputs at a fixed Q have the same n,m,N. It suffices to realize z=0 by the identity permutation and z=1 by one fixed transposition, so the prior has actual source realizations and no hidden table.

Construction's coloring proof supplies SAT iff Y=0^r on every 2-degenerate Q. Briefly, the sign of each triangle coloring must obey the edge sign equations. Consistency leaves three possible triangle colorings at each vertex; each colored neighbor forbids one. Reverse a degree-at-most-two deletion order to extend. Nonzero Y is inconsistent and UNSAT. This proof applies to intersecting cycles, not only disjoint equations.

For an explicit unbounded both-label control take r triangles sharing a single quotient vertex: q=2r+1, k=3r, c=1, hence n=93r+33, m=69r+21 and N=Theta(r log(r+1)). All such quotients are 2-degenerate. Every Y occurs. A zero syndrome source is SAT and a source with a single nonzero last syndrome is UNSAT at identical dimensions. This family is a polynomial control.

## Actual events, decoder and exact obstruction

After fully paying for acquisition and syndrome calculation, A_scan writes Y contiguously beginning at tape cell 3, with an end sentinel. It enters a fixed scan control state at cell 3. Allocation, relocation of any source cells, initialization and reaching that state are preprocessing costs. It reads forward until the first 1, or until the sentinel if all r bits are zero. It then returns to the origin and emits the terminated SAT/UNSAT bit. No binary counter is needed during this suffix. Source and scratch may remain elsewhere on the same charged tape.

Let R be the number of syndrome-bit reads. Define the target U from the mathematical input Y as its prefix ending at the first 1, or all r zeros when no 1 exists. Let B contain A_scan, Q,F,r, the deterministic generator, scan layout and prior, but not the sampled source, signs, cache contents, full configuration, or absolute timing. Pi is the binary string actually consumed in the forward scan. E is exactly the set of those R forward-read transitions, indexed relative to scan entry. Return visits, sentinel reads, output and preprocessing are in T but not in E. No event is counted twice.

For the single obligation j=1, Pi=U, |Pi|=|E|=R, b=1, h_1=0 and rho=1. The decoder is identity. Its permitted records are 1,01,...,0^(r-1)1,0^r. This set is prefix-free, with r supplied in B. For r=0 the only record is empty. The bit capacity describes this selected observation channel, not every possible disclosed machine state or timestamp. Public address order eliminates address bits from Pi; physically accessing those addresses remains charged.

For any prior, conditional prefix coding gives H(U|B)<=E[R]<=E[T]. For independent fair z, the coordinate lemma proves P(Pi=x)=2^(-|x|). Therefore, for r>=0,

H(U|B)=E[R]=sum_(i=1)^r 2^(-(i-1))=2(1-2^-r).

This directly instantiates the requested bound
E[T] >= (sum_j H(U_j|B_j)-sum_j E[h_j])/(b rho)
for one actual record. It is a bound for a declared solver, not compulsory execution for every solver.

**Full-cycle decoder obstruction.** Given a record x of length l<r, all 2^(r-l) completions of its unread suffix have that same record. They have equal conditional probability under the fair-sign prior. Thus

H(Y|B,Pi)=r-E[R]=r-2+2^(1-r).

It is positive for r>=2. The smallest obstruction is Y=10 versus Y=11: both are UNSAT and both produce Pi=1. Correct decision does not force Y to be reconstructible. Setting U=Y and retaining this Pi therefore fails the decoder premise, not the entropy theorem. Including the retained original input in B would instead make H(Y|B)=0. Neither modification yields the desired compulsory lower bound.

If one defines j=1,...,r stopped-prefix targets truncated at j, their records use the same early events. Each event i belongs to r-i+1 sets and rho=r; the first read belongs to every set. Their entropy sum is 2r-2+2^(1-r), so division by rho again stays below two. This is the existing stopped-prefix reuse lemma specialized after the new coordinate proof.

A different balanced prior supported on Y=0^r and Y=0^(r-1)1 has one bit of target/decision entropy but R=r for this particular scan. Both sources exist by the inverse coordinate map. This shows why low entropy does not establish a constant worst-case runtime. Conversely r independent syndrome bits do not force r bits of this observed decision transcript. No general lower bound is inferred from either prior.

## Complete work and cumulative-cost ledger

The inherited recognizer explicitly verifies all star rows, private names and adjacency absences, constructs the graph and triangle matchings, and discovers Q. Our addition computes a forest, potentials, all chord syndromes and a degree-peeling certificate. These are polynomially many exact bit operations on at most O(N²) cells. A forest traversal, repeated indexed searches, sign calculation and at most q degree scans fit Construction's conservative O(N^4) bit-operation budget. Address arithmetic, O(log N)-bit fields, unsuccessful searches and guard failures are included. A conservative O(N^3) unit-tape tariff per indexed bit operation handles traversal and scratch, as in the pinned construction.

On every admitted source the resulting symbolic bound is T=O(N^7), peak span O(N²), physical CM=O(N^9), and minimum-description CM=O(N^8). The physical estimate bounds the space of each transition on this same execution; it does not multiply maxima from unrelated inputs. Separately, replay from the N-bit source and a self-delimiting step counter describes each configuration in O(N+log(T+2)) bits. Thus descriptive cost has its own bound, not an assumed equality to physical storage.

| Phase | Time and storage charged |
|---|---|
| Parsing and authentication | All source bits, rows, multiplicities, field bounds, full graph/fiber tests, failed candidates; included in O(N^7) and O(N²) |
| Coordinate discovery | Graph-only forest, signs, potentials, all r syndromes, 2-degeneracy verification; same budget |
| Normalization | Copy Y to cells 3 through r+2, sentinel and origin marks, relocate source, reset control/head; same budget |
| Actual stopped suffix | O(R+1) transitions including sentinel if needed, return and terminated output; retained full span at most O(N²) |
| Suffix cumulative costs | Physical O(N²(R+1)); separately descriptive O(N(R+1)) under the admitted polynomial bound |
| Valid guard failure | Correct exhaustive fallback, at most O(2^n N^7) time, O(N²) span; physical O(2^n N^9), descriptive O(2^n N^8) |

No claims of optimized exponents or native tape execution are made. The successful-path polynomial guarantee includes preprocessing; it is restricted to authenticated instances. Full all-input correctness does not make the fallback polynomial.

One legal variant A_fused accumulates OR(Y) while computing the syndromes. After successful authentication and 2-degeneracy recognition, it caches just the verdict near the origin and omits the stopped scan. It can erase Y and source at paid cost. Its optional READY read has a one-bit record; on the fair-sign prior its answer entropy is h_2(2^-r). Thus even our richer U is optional solver work. Caching and algebra are constructive results to preserve.

For a fixed cap T<=KN^a the fair-prior demand is below 2 and the balanced-prior observation demand is 1. Neither exceeds b rho KN^a. Even r=Theta(N/log N) on the explicit control gives no all-exponent contradiction. The generic cap permits S=O(N^a), physical CM=O(N^(2a)), descriptive CM=O(N^(a+1)), and a separate count-map circuit ceiling O(N^a log N). No linear-space assumption is made from polynomial time. The internally reviewed permutation transport control keeps its sole-tape quadratic-time/cubic-CM match and static ceilings Delta h<=N²/8 and Delta h²<=N³/27.

Parity alone cannot solve the arbitrary balanced core. Identity matchings on arbitrary Q yield a bundle three-colorable iff Q is three-colorable: restrict to place zero in one direction, use f_u(a)=a+c(u) modulo three in the other. Identity K4 is a concrete balanced UNSAT core. An all-input polynomial core solver would decide arbitrary graph three-colorability through this polynomial reduction. Neither this extension nor an unrestricted separation is established.

## Evidence, fresh sources and next dependency

[Checker](../../../experiments/dynamic_accounting_cycle_stop_20261122.py) and [raw evidence](../../../results/raw/dynamic_accounting_cycle_stop_20261122.json). The checker exhausts 37,500 signings across friendship graphs of ranks 1..5, intersecting cycles, a disconnected graph and a forest. It checks invertibility, uniform syndrome multiplicities, actual read indices, prefix freedom, exact dyadic probabilities, observation-fiber sizes, conditional entropy and the balanced last-bit pair. All assertions passed. For rank five, E[R]=31/16 and H(Y|B,Pi)=49/16. The new test concerns the source-sign-to-cycle coordinate map and undecoded fibers; it does not repeat the old source semantic experiment. Source parser, native single-tape machine and theorem-prover kernel were not executed. No checkout was available for the repository preflight. The script hash and seed-free exhaustive parameters are in the raw file.

Fresh primary searches: “Harary 1953 balance signed graph spanning tree negative cycles pdf” and “Shannon 1948 mathematical theory communication noiseless coding theorem pdf.” Read Harary and Kabell, *A simple algorithm to detect balance in signed graphs*, Mathematical Social Sciences 1 (1980), 131–136, Theorem 1 and section 3 [1]. Its exact setting is a signed graph, with componentwise root marking and chord checks deciding whether every cycle is positive. Its linear graph-access accounting is not imported as a single-tape bound. It supports the algebraic bypass; our bit-coordinate proof and full tariff are explicit. Shannon's corrected 1948 reprint, section 9 Theorem 9 [2], concerns source/channel rates, not compulsory SAT execution. The finite entropy identities here are derived directly.

Fresh GitHub searches used '"cycle" "syndrome"' separately in anthropics, openai, xai-org, google, google-research and google-deepmind, top three. xai-org had no results. Anthropic, Google and DeepMind results were unrelated medical/register/material excerpts and were rejected at triage. Google Research initially returned HTTP429; the later task-specific query '"signed graph" balance' returned zero. Web fallbacks for Google Research signed-graph balance, DeepMind cycle-syndrome SAT, and the combined Anthropic/OpenAI/xAI signed-graph query yielded no applicable official implementation. Search absence is bounded, not comprehensive.

One OpenAI result warranted inspection: openai/math at **4eaee87548250b2682affda7d05d947c05554bae**, file preprints/The-PCP-for-PPAD-conjecture-a-quasilinear-reduction-September-25-2026/build/sections/03-outer-codes.tex [3]. Its outer-uncertainty statement assumes an input agreeing outside a small set with a reference satisfying specified code constraints, and claims polynomial global correction in explicit size under that promise. It supplies no such nearby reference or promise for arbitrary SAT. Only that applicability boundary was inspected; its dependencies were not independently verified, no theorem was imported, and no code was executed. This cannot establish compulsory syndrome decoding on our decision path.

Ownership was freshly checked using domain-verified [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai), [xAI's official GitHub release link](https://x.ai/news/grok-os), [Google's organization guidance](https://opensource.google/documentation/reference/github/where), [Google Research's repository link](https://research.google/resources/) and [DeepMind's code link](https://deepmind.google/science/alphafold/). Organization membership alone does not validate a theorem.

Recovered AGENTS.md, CODEX.md, the repository research instructions, dynamic continuation, Transport and applicable T5 definitions at the pinned head; own full handoff and previous palette report; Construction's original report/code/data; and Synthesis's first-clearing handoff. Repository duplication search '"syndrome" "stopped"' recovered the earlier stopped-scan chain; its result is explicitly reused above, not presented as new. Only Accounting's report, handoff and associated code/raw files are changed. No historical manuscript ownership is claimed.

DISJ/equality sanity: PASS at this restricted scope, with no free transport. Simultaneous DTISP: PASS, one machine and one execution. Deterministic-configuration gate: PASS as an upper description bound only. Relativization: no nonrelativizing separation supplied; unrestricted promotion OPEN. Natural Proofs/algebrization do not yield a lower bound here. Affine/Tseitin aggregation, complement, private-leaf, forced-domain and decision-witness controls remain permitted. Clause order imposes no mandatory execution order; hashing is not used for semantic equality.

**One next dependency, Bounds with Synthesis integration:** supply an actual decision-sensitive observation after paid acquisition and fused verdict retention, with a decoder that survives the explicit record-fiber collision and model-justified access restrictions. A claim of full Y decoding from the above Pi is false; a different compulsory observation is OPEN. Redteam receives the smallest target Y=10/11 and the A_fused bypass. Construction receives the fixed-forest accounting and retained general-core boundary.

1. [Harary and Kabell, 1980 primary paper](https://deepblue.lib.umich.edu/bitstream/handle/2027.42/23150/0000075.pdf?sequence=1), Theorem 1 and section 3, pp. 132–135.
2. [Shannon, 1948 corrected reprint](https://cs-www.cs.yale.edu/homes/yry/readings/general/shannon1948.pdf), Bell System Technical Journal 27, 379–423 and 623–656, section 9.
3. [Pinned OpenAI outer-code file](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/preprints/The-PCP-for-PPAD-conjecture-a-quasilinear-reduction-September-25-2026/build/sections/03-outer-codes.tex), applicability inspection only.
