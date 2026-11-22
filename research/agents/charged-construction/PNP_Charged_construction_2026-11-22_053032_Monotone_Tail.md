# A monotone tail collapses two large complexity parameters

22 November 2026, 05:30:32 PST. PNP Charged Construction.
**DYNAMIC-MONOTONE-TAIL-COLLAPSE1**, within DYNAMIC-COMPATIBILITY-OBLIGATION1.
**PROVED/EXACT** restricted decision equivalence and scalar algorithm, with inherited symbolic compiler/authentication tariffs. **COMPUTATIONAL** finite source audit. Independent adversarial review, native tape implementation and kernel verification remain pending. P versus NP is **OPEN**.

## Exact target and result

Fix one uniform deterministic SAT decider A before selecting parameters. There is an explicitly generated family F(q,p), q≥1 and 0≤p<6q, such that A authenticates and decides every member in O(N³) time and O(N) span under the pinned one-tape tariff, where N is the entire encoded input length. F(q,p) is SAT exactly when p is odd. The projected cycle has 2q AA columns and maximum shared syndrome rank q, yet its local constraints admit at most two candidate paths. Thus both of these large parameters can coexist with polynomial decision work.

This extends Redteam's no-AA control [1]: the new sources have a long AA tail, so that guard returns UNKNOWN. The first new load-bearing implication tested is that making both the number of potential branching columns and the shared syndrome rank large might force many decision alternatives. The explicit compulsory-work hypothesis
“for every correct A, some c_A>0 and q_A satisfy max_p T_A(F(q,p))≥c_A 2^q for all q≥q_A”
is **FALSIFIED/RETIRED** by this algorithm. This is a stress-test hypothesis, not a theorem attributed to a peer. Failure of this hypothesis resolves neither P=NP nor P!=NP.

Four concrete falsifiers are: a nonconstant monotone tail with equal endpoint bits; a mixed AC/CA column permitting 0→1; an omitted seam condition allowing an extra path; and an encoding or authentication cost hidden outside N. The proof and ledger below address these. No truth table is supplied as a compact parameter.

## Explicit source and both labels

Use the synchronized-cycle source [2]. At each of t columns in each of two rows place a disjoint exact-one triple (a,b,z), for 2t triples. Number their ports consecutively, top row first. A letter A at column i imposes a_i XOR b_i XOR a_(i+1)=0; a letter C replaces the last port by z_(i+1). Successors are cyclic within that row. At each column add two equations z_top XOR h_i XOR r_i=0 and z_bottom XOR h_i XOR r_i=0, with a private helper pair. Append an explicit list of homogeneous ternary equations on distinct top z columns.

Emit the five forbidden exact-one rows per factor, then the four odd rows per parity relation, lexicographically within each block. Order factors, row-longitudinal equations, rung pairs, and appended rows in that order. Each forbidden bit tuple gives the clause falsified precisely by that tuple. Every clause has three distinct names. The source has d=8t names and c=26t+4m′ clauses for m′ appended equations. It is connected through the two cycles and rungs.

Set
t=8q,
top=C^(6q) A^(2q),
bottom=C^p A C^(6q-p-1) A^(2q),
and append the q rows
(2j, 2q+2j, 4q+2j), 0≤j<q.
All indices are zero-based column indices. These rows have three distinct indices. The only mixed column is p; the last 2q columns are AA. Both words are nonuniform. Parameters and source records are explicit, and emission costs O(q log(q+1)) bits and polynomial work. A binary description of q is not substituted for the explicit final input.

Here is the complete projection argument. The two rung equations force equality of the top and bottom z values; equal values extend by h=0,r=z. Exact-one implies a XOR b=1−z. Consequently an A link permits exactly 00,10,11 on consecutive z values, and a C link permits exactly 01,10. Intersect the two row relations. A CC column forces a flip; an AC or CA column forces 1→0; an AA column imposes z_i≥z_(i+1).

Conversely, every closed z path obeying these intersections extends to all ports. In each row choose destination a_i=1−z_(i−1) when its incoming link is A, or a_i=0 when the incoming link is C. Set b_i=1−a_i−z_i. The permitted-edge inequalities make these values Boolean and exact-one. All longitudinal and rung equations hold. An appended parity equation holds exactly when its three z values have even sum. This proves existential equivalence in both directions; helper extension multiplicities are irrelevant to decision and are not asserted to preserve model counts.

In F(q,p), the first 6q links force flips, so for an initial s,
z_i=s XOR (i mod 2) for 0≤i≤6q.
In particular z_(6q)=z_0=s. The AA tail imposes
s=z_(6q)≥z_(6q+1)≥...≥z_(8q)=z_0=s.
Every tail value is therefore s. This is a genuine closing constraint on a chain, not an assumption that the written stages are machine execution stages. There are at most two local candidates, one for each s, independently of tail length.

Each appended row contains three even columns, so its XOR equals s. Since q≥1, the rows force s=0. The mixed column requires z_p=1, which now holds exactly when p is odd. Thus every odd p yields SAT and every even p yields UNSAT. They have identical d,c,n,m,N and parity matrix H. Moving the mixed column changes the label without introducing an all-UNSAT promise.

## Why both large scores collapse

Let k_AA denote the number of AA columns. Here k_AA=2q. The q appended rows have disjoint supports, so rank(H)=q. At the cut after column 2q−1, the prefix contains one unit-vector column for each row and the suffix contains two. Thus
rank(H_prefix)+rank(H_suffix)−rank(H)=q.
This expression is at most rank(H), so its maximum λ is exactly q. The AA tail contributes only zero columns to H.

Hence min(k_AA,λ)=q, while N=Θ(q² log(q+1)); this minimum grows faster than log N. Large sufficient search budgets based on these parameters do not imply necessary search. Discovery's exact suffix-pruned solver [3] remains correct; its 4·2^λ bound is an upper bound, not a required number of states. The new source also bypasses the older all-A/all-C recognizers and the no-AA guard. No claim is made that it is hard for the exact peer solver: the finite growing controls below actually keep its peak list at two.

The scalar proof extends to any admitted cycle whose first L columns are CC/AC/CA with even L≥2, followed by one nonempty AA block, with any explicit list of ternary parity checks. Scan to discover the first AA column, verify the remaining block, and test the two candidates that alternate on the prefix and are constant on the tail. Check every mixed orientation and every parity row. Return SAT if either passes, UNSAT if neither passes. On failure of the structural guard return internal UNKNOWN. Odd L is deliberately outside this particular branch; it is not called UNSAT merely because the guard fails.

This is a uniform restricted algorithm with paid discovery. The known-set conditioning perspective [4] motivates it, but the proof above does not assume free acquisition of a hidden backdoor or import a theorem about arbitrary SAT inputs.

## Physical encoding and complete cost ledger

The machine has one writable finite-alphabet tape and one head with unit motion; input, copies, addresses, source records, retained caches, counters and terminated output share this tape. Span includes origin, head and all nonblank support. End-to-end bounds concern one execution.

For the explicit family d=64q and c=212q. The established proper-3-CNF compiler [2,5] gives
g=max(3,2 floor((c+1)/2)+1),
n0=d+(10c+1)g+2, m0=(20c+4)g,
n=n0+m0+3, m=2m0+4,
w=ceil(log2(n+1)).
The physical fields are unary n with delimiter (n+1 bits), gamma(m+1) (1+2 floor(log2(m+1)) bits), m ordered literal triples (3m(w+1) bits), two supplied n-bit local witnesses, and a w-bit release ID. Therefore
N=3n+2+2 floor(log2(m+1))+3m(w+1)+w=Θ(q² log(q+1)).
The supplied local Horn/dual-Horn witnesses and their adjacency are inherited compiler guarantees. Physical source-column adjacency is neither preserved nor needed. Clause order is an encoding choice, not a mandatory processing order.

At q=1, arithmetic gives n=1,355,814, m=1,807,948 and N=123,392,073 bits. At q=8, n=86,352,362, m=115,138,060 and N=9,930,654,207 bits. These are exact count calculations, not claims that those compiled strings were materialized in this run.

| Step on admitted inputs | Same-run charge |
|---|---|
| Parse, retain input, reject oversized candidate fields before loops | Included in O(N³) time, O(N) span |
| Recover source and exactly regenerate canonical compiled image | Inherited O(N³), O(N); compare signs, identifiers, every clause, both witness fields, release ID and end of input |
| Discover even flip prefix and AA tail, inspect all constraints | O((t+m′) log(c+2)) indexed bit operations, including failed structural tests |
| Test both scalar candidates | Same logical order, including all row indices, parity evaluation and rejected candidates |
| Address manipulation, source access, copies and relocation | Conservatively O(N²) transitions per indexed bit operation over O(N) span |
| Initialization, flags, counters, retained source, branch selection, cache and output | Included above, plus O(N) return-to-origin/cleanup |
| Fallback after any valid nonmatch | Paid admission first, then exhaustive SAT on retained encoded formula |

Since (t+m′) log(c+2)=O(N), the admitted path has T=O(N³), S=O(N). Source construction and canonical compilation also fit the inherited polynomial O(N³) tariff; output length is charged. Physical cumulative cost is Σ_i span_i=O(N⁴). Separately, input plus transition index describes each deterministic configuration in O(N+log(T+2)) bits, so minimum-description cumulative cost is O(N⁴). This description is not free on-machine decoding.

Use exact exhaustive fallback with conservative T=O(N³+2^n N³), S=O(N) for any valid nonimage. Malformed inputs follow the encoding convention. Thus a fixed globally correct solver exists, with a proved polynomial guarantee only on the admitted structural class. General mixed-source feasibility is NP-complete [5]; no polynomial all-input coverage or bound on fallback is established. Symbolic compiler tariffs have not been replaced by a native tape benchmark.

## Actual events, cap comparison and remaining premise

For a fixed q use the equal-probability pair p=0 and p=1. Fix the above decider A, including a READY transition that reads its computed decision bit at origin before terminating. Set U=D and B=(public q,H,pair,prior,A,READY convention), excluding the sampled source, clock and answer. Let E contain precisely that actual read and Π be its one-bit payload. The identity decoder recovers U. The conditional code is fixed length one, hence prefix-free, with b=1,h=0,ρ=1. The shared inequality yields E[T]≥1. The complete prefix, cache construction, framing and input retention are still paid in the preceding ledger.

There is no decoder obligation to expose 2q independent AA choices: on these instances all tail bits are already forced by one boundary value, and on UNSAT roots no satisfying-path choices exist. Repeating the READY event raises ρ. Giving the sampled retained source freely in B erases the conditional entropy. Bounds' joint-prepayment theorem [6] remains applicable only with its actual decoder and event premises; it does not force fresh marginal entropy for repeated descriptions.

Under any hypothetical fixed cap T≤K N^a, preserve S=O(N^a), CM_phys=O(N^(2a)), CM_min=O(N^(a+1)), and the separate count-map circuit ceiling O(N^a log N). Neither this one-bit ledger nor a large syntactic score defeats those ceilings. The internally reviewed single-tape permutation family remains the quadratic-time/cubic-cumulative calibration, with static demand ceilings Δh≤N²/8 and Δh²≤N³/27. Counting, strict T5, symmetric C and ordered R consequences are not imported.

## Reproducible evidence and scientific gates

The new checker exhausts all CC/AC/CA prefixes of lengths 2 and 4, AA tails of lengths 1 and 2, and either no row or one of all ternary rows. All 2,655 cases agree between the new two-candidate procedure, the pinned peer trellis solver and direct enumeration of all cyclic z assignments: 329 SAT, 2,326 UNSAT. Separately all 90 controls q∈{1,2,4,8}, 0≤p<6q agree with p mod 2; they verify k_AA=2q, λ=q and peak peer list two. Direct z enumeration was additionally used for all 18 controls at q≤2. Every control's explicit source CNF was generated, clause counts/distinctness checked, and each SAT control's full source extension evaluated against every clause. No random seed.

[Generator/checker](../../../experiments/dynamic_construction_monotone_tail_20261122.py) imports unchanged [Discovery code at 8a911c17](https://github.com/j15marti/pnp/blob/8a911c17dbb97d350c997cfbb90c5cf818a67ed3/experiments/dynamic_discovery_syndrome_trellis_20261122.py). [Raw evidence](../../../results/raw/dynamic_construction_monotone_tail_20261122.json). Run with Python3 from the repository. These are new tests of the AA-tail extension, not repeated no-AA experiments. The direct oracle is the peer's separately defined enumeration routine, not a newly independent implementation. The symbolic proof supplies asymptotics. Full compiled-image generation, whole-machine execution, kernel proof and full-checkout preflight were not run in this selected-file environment.

DISJ/equality sanity: PASS as a polynomial control. Simultaneous DTISP: PASS for the stated symbolic same-run upper bounds. Deterministic configurations: PASS for description upper bounds only. Relativization: NOT APPLICABLE to this restricted constructive proof; no nonrelativizing separation step is asserted. Algebrization and Natural Proofs provide no promotion. Relocation, affine/Tseitin, complement, private-leaf, forced-domain and cached-decision controls remain permitted. Unrestricted compulsory decoding and all-input polynomial coverage are OPEN.

## Sources and bounded fresh searches

1. [Redteam forced alternation, c3bb6759](https://github.com/j15marti/pnp/blob/c3bb67594ba372f195ffeca8b3bd1403c91710b3/research/agents/charged-redteam/PNP_Charged_redteam_2026-11-22_051542_Forced_Alternation.md). Reconstructed its projection, opposite-label control, code and raw evidence. New feature here is a linearly long AA tail and closure-driven contraction.
2. [Construction marked columns, 009932eb](https://github.com/j15marti/pnp/blob/009932ebaf093a18c19378261d0123f0c0c3297e/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_043212_Three_Marked_Columns.md). Supplies source ordering and compiler parameter definitions; single-check eight-state algorithm remains valid.
3. [Discovery syndrome trellis, 8a911c17](https://github.com/j15marti/pnp/blob/8a911c17dbb97d350c997cfbb90c5cf818a67ed3/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-22_045216_Syndrome_Trellis.md). Exact full-syndrome keys and future-span tests preserved. Its upper bound is not reinterpreted as necessity.
4. R. Williams, C. Gomes and B. Selman, *Backdoors to Typical Case Complexity*, IJCAI 2003, author-hosted six-page [PDF](https://www.cs.cornell.edu/selman/papers/pdf/03.ijcai.backdoors.pdf), Definitions2.2 and2.4 and ensuing known-set enumeration discussion. A strong backdoor is relative to a polynomial subsolver and every setting must be decided; the paper separates given-set search from discovering the set. Our algorithm proves a particular two-candidate reduction directly. No general small-backdoor theorem, heuristic acquisition guarantee, or formal subsolver closure property is assumed. Fresh queries: “Williams Gomes Selman 2003 Backdoors to Typical Case Complexity pdf” and “Dechter Pearl constraint networks cycle cutset conditioning monotone path constraints”. The latter recovered the [Dechter/Pearl author paper](https://ics.uci.edu/~dechter/publications/r3.pdf) as a lead; its theorems were not imported.
5. [Mixed parity ports, pinned recovery](https://github.com/j15marti/pnp/blob/c3bb67594ba372f195ffeca8b3bd1403c91710b3/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_012755_Mixed_Parity_Ports.md), including compiler links and independent source helper extension argument. General mixture completeness is preserved, not claimed for this easy subfamily.
6. [Bounds joint prepayment, c73587c1](https://github.com/j15marti/pnp/blob/c73587c109f5c043e49cc8dfd5512920f4cb5d56/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-22_050620_Joint_Prepayment_Decoder.md). Its conditional decoder scope remains unchanged.

Fresh GitHub searches for `"monotone" "constraint propagation"` scoped separately to anthropics, openai, xai-org, google, google-research and google-deepmind returned no relevant SAT result. DeepMind had HTTP429, followed by one successful empty retry. OpenAI returned a relativity/PDE section, [openai/math at 4eaee87548250b2682affda7d05d947c05554bae](https://github.com/openai/math/blob/4eaee87548250b2682affda7d05d947c05554bae/preprints/Quantitative-Near-Kerr-Evolution-and-Generic-C2-Future-Inextendibility-September-23-2026/build/sections/06-far.tex); only the search excerpt was inspected, and it was rejected as unrelated.

Web fallback used “constraint propagation SAT” with the first three official organization paths and “SAT constraint propagation parity” with google/google-research/google-deepmind paths. It returned [Google OR-Tools SAT sources](https://github.com/google/or-tools/blob/stable/ortools/sat/sat_solver.cc) as a relevant engineering lead, not a theorem. No external code implementation was imported or benchmarked, and no OR-Tools commit was inspected. Earlier bounded searches during this work for `"backdoor" "constraint" "solver"` likewise yielded no applicable algorithm: Google causal-governance changelog d05c7b95 and DeepMind OPRO security data a76bdce2 were unrelated search excerpts.

Official ownership was checked through the domain-verified [Anthropic](https://github.com/anthropics) and [OpenAI](https://github.com/openai) profiles, [xAI's corporate repository link](https://x.ai/news/grok-os), [Google organization policy](https://opensource.google/documentation/reference/github/where), [Research resource links](https://research.google/resources/) and [DeepMind project code links](https://deepmind.google/science/alphafold/). Internal duplicate query `"monotone" "tail" "cycle"` surfaced older unrelated tradeoff material, not this construction; “charged” branch search returned none. Search coverage is bounded, not a novelty proof.

Required governance, continuation, transport and T5 definitions, current handoffs and original peer evidence were recovered at c3bb67594ba372f195ffeca8b3bd1403c91710b3; issue324 was read. No historical manuscript ownership or schedules changed.

**One next dependency, Discovery:** construct a paid contraction procedure for multiple separated AA blocks, retaining all parity equations on their possible switch positions, and prove its exact decision semantics and total acquisition cost. A polynomial generalization is welcome; an exponential residual domain must be measured rather than declared compulsory. Bounds receives this explicit both-label falsifier to independent-AA-choice obligations. Accounting receives the O(N³)/O(N)/O(N⁴) same-run ledger. Redteam receives the seam and mixed-orientation proof for independent adversarial review. Synthesis receives the failure of simultaneous large k_AA and λ as a hardness certificate.
