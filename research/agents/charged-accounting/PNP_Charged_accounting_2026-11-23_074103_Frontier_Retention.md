# Untouched suffix information under destructive tape reads

23 November 2026, 07:41:03 PST. PNP Charged Accounting.
FRONTIER-RETENTION1 within DYNAMIC-COMPATIBILITY-OBLIGATION1.
PROVED/EXACT restricted sole-tape lemma and matching implementation. Independent review pending. P versus NP OPEN.

Discovery's latest report identifies linear query demands on the sparse accepting prior of the two-terminal family [1]. We now derive matching quadratic expected minimum-description cumulative memory from the untouched suffix, even when visited cells are erased immediately. The physical head-distance argument follows the same geometric principle used in Redteam's earlier output-anchor audit [3]. The new component is the information retained at distinct first-arrival configurations and the contrast with the exact reuse factor in a time ledger.

Fix one deterministic sole-tape continuation M, uniform in m, correct for every 3m-bit cache encoding AND_i OR_(d=0,1,2) x_id. The sole head starts at cell 0 in a fixed state. Cell 0 contains a public marker. Piece i occupies positions 3i−2,3i−1,3i, for i=1,...,m. A public end marker is at 3m+1. Every other initial cell is fixed and public. Bits 0 and 1 are distinct from blank. The machine has fixed finite control and alphabet, unit-speed head movement, reads before writing, and Boolean output with terminator at the origin. It can overwrite, erase, copy, recompute, move left of the origin, and use arbitrary work cells. The initial remainder of its state contains no private summary.

Take W_i independently uniform on {0,1,2}, setting x_id=1 exactly when d=W_i. Expectations below are over these 3^m authentic accepting caches. Correctness is still required on all bit assignments, including neighboring rejecting inputs. For every such M,

    T ≥ 3m−2 on every sampled execution,
    CM_phys = Omega(m²) on every sampled execution,
    E[CM_min] ≥ (m(m+1)/2) log2 3.

Here CM_min sums prefix complexities K(C_t | M) of complete post-transition configurations, with neither the input nor the time supplied freely. The exact coefficient in the last inequality uses that prefix convention. There is one fixed continuation achieving T=O(m), S=O(m), CM_phys=O(m²), and CM_min=O(m²) for every cache. Thus the cumulative orders are tight in the declared setting. The expectation statement implies a hard input for each fixed M and m. It does not say every sparse input is incompressible.

Four falsifiers were arrival times overlapping within an execution, a write changing a supposedly untouched bit before arrival, a shortest-description code failing prefix freedom, and multiplying demands while omitting reuse. Unit head speed, read-before-write semantics, prefix complexity and the explicit overlap ledger below address them.

## Compulsory arrivals and complete-state information

On an accepting sparse input, M must visit the unique one in every piece before halting. Otherwise replacing that unvisited one by zero changes the decision while preserving the entire execution, including any writes at visited locations. This proves necessity from both-label correctness, without prescribing a computation graph.

Let p_i=3i−2 and let tau_i be the first time the head reaches p_i, counted after the move onto that cell and before any transition reads or writes it. These positive times exist on every sampled execution and are strictly increasing. At tau_i, every bit in pieces i through m is still present at its original address. The only head has never reached those cells. In particular erasure of earlier bits, cached partial results, detours and repeated scans cannot erase this suffix sooner.

For fixed i,m, projecting the tape cells from p_i through 3m in C_(tau_i) recovers U_i=(W_i,...,W_m). Therefore H(C_(tau_i))≥H(U_i)=(m−i+1)log2 3. No input prefix or random time is given to that projection. Its addresses are fixed for this distribution.

Choose a shortest prefix program for each complete configuration conditional on fixed M. These programs form a prefix-free set, so their expected lengths are at least the Shannon entropy of the configuration distribution. More explicitly, Kraft gives Z=sum_c 2^(−K(c|M))≤1. Normalizing these weights and applying nonnegativity of relative entropy gives E K(C|M)≥H(C)−log2 Z≥H(C). This does not require the distribution, code choice or stopping times to be computable.

Apply this inequality separately to each distribution of C_(tau_i). In each execution the selected times are distinct, so their description lengths are summands of that execution's CM_min. Summing and then averaging proves the displayed quadratic lower bound. The distributions for the selected states all come from the same source prior and same fixed M. There is no product of independent time and space maxima and no claim that a minimum description can be efficiently constructed.

The sampled accepting trace reaches at least d=3m−2. First arrivals at positions 1,...,d are distinct actual configurations. Each physical span includes its head and origin, so in cell units CM_phys≥sum_(r=1)^d(r+1)=d(d+3)/2. Alphabet conversion changes only a fixed factor. This argument needs no mandatory return-to-origin assertion. In particular speculative early output cannot evade the already necessary outward travel. It is the earlier geometric principle [3] applied to an outward scan.

## Actual event reuse explains the weaker time bound

For each i let B_i consist of M,m,geometry,prior and the prefix witness values W_1,...,W_(i−1). Let E_i be the first transitions scanning initially private bit cells in pieces i through m. Record their original values in chronological order as Pi_i. A replay knows every initial prefix cell from B_i, and every public cell. On a first visit to an unknown suffix cell it consumes the next record bit, then simulates all writes and subsequent reads. The next address follows from the simulation, including detours and reused cells. Halting gives conditional prefix freedom. On the sampled accepting executions the unique ones must be encountered, so replay decodes U_i.

Each selected transition contributes at most one binary symbol, b=1, and no extra length field is needed, h_i=0. A first read in piece r belongs to exactly r sets E_i. Since a first read in the last piece is necessary, maximum reuse is rho=m. Hence the shared compulsory-work inequality gives only

    E[T] ≥ [sum_i H(U_i|B_i)]/m
         = ((m+1)/2) log2 3.

The full vector can instead be one obligation, yielding E[T]≥m log2 3 from first reads once. Discovery's stronger query-search bound is 2m on this prior. All are consistent with linear time. Treating the m suffix obligations as having reuse one would falsely promote their quadratic numerator to a time lower bound.

The quadratic CM_min proof charges descriptions at m different configurations. It does not interpret the resident suffix as m fresh transmissions. Full state is the object being charged there. Supplying it as free side information in the time ledger would destroy the entropy demand.

## Matching destructive implementation and source costs

The companion simulator implements a fixed finite-control machine on this checkpoint. Starting at the origin it moves right, reads and blanks every cache bit, and stores only its position modulo three and the OR of the current triple in finite control. A false triple enters a return state with verdict zero. At the end marker it blanks the marker and returns with verdict one. It travels left until the origin marker, writes the verdict there, moves one cell right and writes the terminator. Returning across a blank cell is a real transition. Each transition has one read, one possible write and at most one move. Neither m nor a numerical address register is used by this continuation.

On sparse inputs the simulated time is exactly 6m+4, and span never exceeds 3m+2. The cumulative bound follows on each execution. A description containing m, the original cache and a transition index reproduces any state using O(m+log m)=O(m) bits. There are O(m) transitions. Thus minimum-description CM has the matching O(m²) upper bound. The simulator verifies physical cells and control. It does not compute Kolmogorov complexity.

This checkpoint can be prepared after paid recognition of the established source family [1,2]. Fix all second masks to full. The graph's q=10m and k=22m−2 produce n=528m−18 Boolean variables and R=408m−18 exact-one rows. With w=ceil(log2(n+1)),

    N=n+2+2 floor(log2(R+1))+3Rw=Theta(m log(m+2)).

The source-to-cache implementation parses the full encoding and authenticates the graph-star rows, triangles, matchings, gain labels, neutral connectors and exact topology. It calculates each three-bit mask, copies it to the prescribed region, removes the source and work, places the markers and resets its head/control. Header decoding, source retention, failed candidates, conversion, all addresses, copies, lookup sweeps, relocation, recomputation and output are charged. A valid guard miss gives internal UNKNOWN followed by exact enumeration. Every permitted source receives a correct Boolean verdict.

The inherited conservative whole-run upper tariff remains O(N^4) indexed-bit work over O(N²) span, with O(N³) sole-tape simulation cost per indexed bit operation. The new linear suffix and cleanup fit this allowance. Thus admitted T=O(N^7), S=O(N²), physical CM=O(N^9), descriptive CM=O(N^8). The valid off-family fallback has time O(2^n N^7), physical CM O(2^n N^9), and descriptive CM O(2^n N^8). The lower bounds apply to continuations that actually start from the declared cache, including their same-execution suffix within this constructed solver. The choice to prepare that cache is an algorithm choice.

The full-input solver may instead compute a running conjunction during mask discovery, erase source/work and retain one verdict at the origin. It then has a constant-size output phase. This legal bypass defeats a proposed universal necessity of the raw checkpoint. The present quadratic cumulative bound does not price the minimum possible production of that verdict.

At N=Theta(m log(m+2)), the suffix cumulative demand is Omega((N/log N)²). This is compatible with a linear time cap's O(N²) physical and descriptive ceilings. More generally fixed T≤KN^a, a≥1 gives S=O(N^a), physical CM O(N^(2a)), descriptive CM O(N^(a+1)), and separate count-map circuit size O(N^a log N). No fixed polynomial exponent is excluded. Boolean decision remains distinct from counting. The internally reviewed proper-3-CNF permutation theorem retains its quadratic-time/cubic-cumulative calibration and Dh≤N²/8, Dh²≤N³/27 static ceilings.

## Evidence, controls and next dependency

The finite test checks every cache at m=1,...,4, totaling 4,680 both-label assignments. It separately checks 3,279 sparse caches at m=1,...,7. Each first-arrival tail is unchanged, and the exact tail fibers have multiplicity 3^(i−1), giving entropy (m−i+1)log2 3. Physical transition counts and cumulative spans are recorded. This experiment tests destructive physical movement and frontier retention, which the earlier logical Bellman checks did not execute. [Code](../../../experiments/dynamic_accounting_frontier_retention_20261123.py) and [raw output](../../../results/raw/dynamic_accounting_frontier_retention_20261123.json). Run python experiments/dynamic_accounting_frontier_retention_20261123.py.

This is an executable finite-state suffix simulation. The full-source bitstream parser, native whole-program tape implementation, proof-assistant kernel and full-checkout preflight were not run. Connected repository reads supplied state. Prefix complexities are bounded symbolically.

DISJ/full-state sanity PASS under the public-remainder checkpoint. Same-execution DTISP accounting PASS. Deterministic-configuration gate PASS for the explicit state replay upper bound. Relativization gate NOT APPLICABLE to separation, since this is a restricted tape lemma and no nonrelativizing step is claimed. Algebrization and Natural Proofs supply no separation mechanism here. The accepting prior is accompanied by required correctness on its rejecting neighbors. Copies, affine shortcuts, forced domains, complement and earlier private-leaf compiler controls retain their scopes.

Next owner Bounds, receiving Synthesis: prove that every candidate all-input solver must incur a comparable charge while creating any sufficient summary, or exhibit another paid bypass. Redteam receives the faulty rho=1 suffix-sum inference as the concrete falsification target. Discovery receives the distinction between linear first-read work and quadratic retained-information accumulation.

## Recovery and bounded searches

Pinned project head 8890a9d90bccf46c5eab09174cdaaed74d3b4a78. Recovered current coordination, transport and T5 definitions, AGENTS/CODEX/research skill, all six handoffs, the latest Accounting and Discovery original reports, and issue 324. Search “first arrival” “retention” found Redteam's output-anchor audit. Its physical geometry argument is credited below. Only Accounting's namespace and its companion evidence are written.

1. [Discovery, adaptive mask probes](../charged-discovery/PNP_Charged_discovery_2026-11-23_064519_Adaptive_Mask_Probes.md), pinned head.
2. [Accounting, mask read ledger](PNP_Charged_accounting_2026-11-23_063714_Mask_Read_Ledger.md), pinned head.
3. [Redteam, selected-anchor output audit](../charged-redteam/PNP_Charged_redteam_2026-11-22_081200_Anchor_Output_Audit.md), pinned head. Its physical return geometry explicitly leaves quadratic minimum-description cost unproved in that different setting.
4. Shannon, A Mathematical Theory of Communication, Bell System Technical Journal 27 (1948), corrected reprint, Theorem 9. Fresh query “prefix Kolmogorov complexity expected length entropy Kraft inequality algorithmic information theorem”. Inspected the noiseless entropy/capacity statement. The needed one-shot prefix-length inequality is proved directly above from Kraft and relative entropy. [Primary paper](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf).
5. Fresh query “cumulative memory complexity sum memory time Alwen Serbinenko 2015 pebbling” found Sustained Space Complexity, ePrint 2018/147. The primary PDF returned 403 and is unavailable for theorem import. No pebbling lower bound is used. [Unavailable primary PDF](https://eprint.iacr.org/2018/147.pdf).

Fresh GitHub queries “cumulative” “pebbling” returned zero results for anthropics, openai, xai-org, google, google-research and google-deepmind. DeepMind succeeded on retry after a rate limit. Ownership was checked through [Anthropic](https://github.com/anthropics), [OpenAI](https://github.com/openai), [xAI release](https://x.ai/news/grok-os), [Google organization guidance](https://opensource.google/documentation/reference/github/where), [Google Research](https://github.com/google-research), and [Google DeepMind](https://github.com/google-deepmind). No external repository implementation or commit was inspected. These bounded searches found no compulsory summary-production theorem.
