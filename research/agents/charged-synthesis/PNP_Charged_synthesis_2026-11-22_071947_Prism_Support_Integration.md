# Compiled prism supports and the remaining compulsory-work gap

22 November 2026, 07:19:47 PST. PNP Charged Proof Synthesis.
DYNAMIC-COMPILED-PRISM-SUPPORT1 within DYNAMIC-COMPATIBILITY-OBLIGATION1.

**PROVED/EXACT** restricted symbolic support transfer and composition with Redteam's pivotal-read lemma. **COMPUTATIONAL** for 588 source-flip comparisons and symbolic offset checks. Independent adversarial review requested. This continues the same conversation's compiler audit and does not claim a separate independent researcher. P versus NP remains **OPEN**.

## Integration at one revision

All peer sources were recovered at 6fecbf3b15a85e2739d48230d13c8849330c2653. Governance, continuation, transport and applicable T5 definitions retain the same content hashes as the preceding runs. The latest owned report and all five peer handoffs were recovered before this composition.

| Peer | Statement incorporated |
|---|---|
| [Bounds](https://github.com/j15marti/pnp/blob/6fecbf3b15a85e2739d48230d13c8849330c2653/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-22_060516_First_Read_Debit.md) | Universal first acquisition and observable-history decoder on the parity family. |
| [Construction](https://github.com/j15marti/pnp/blob/6fecbf3b15a85e2739d48230d13c8849330c2653/research/agents/charged-construction/PNP_Charged_construction_2026-11-22_063248_Twice_Occurring_Ports.md) | Twice-occurring positive exact-one rows reduce to perfect matching. Prism pair has both labels. |
| [Discovery](https://github.com/j15marti/pnp/blob/6fecbf3b15a85e2739d48230d13c8849330c2653/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-22_065545_Online_Matching_Transcript.md) | After matching and erasure, the one-bit suffix cannot reconstruct the component transcript without extra information. |
| [Accounting](https://github.com/j15marti/pnp/blob/6fecbf3b15a85e2739d48230d13c8849330c2653/research/agents/charged-accounting/PNP_Charged_accounting_2026-11-22_065000_Matching_Cache_Reachability.md) | Fixed cached scan has conditional actual records and mean 2−2^(1−k) under independent fair labels. |
| [Redteam](https://github.com/j15marti/pnp/blob/6fecbf3b15a85e2739d48230d13c8849330c2653/research/agents/charged-redteam/PNP_Charged_redteam_2026-11-22_070724_Pivotal_Read_Audit.md) | Pivotal-read theorem on packed prism rows. Compiled support transfer was open. |

Construction's matching branch is the strongest current concrete bypass relevant to the new compulsory-read claim. We close the pending physical-support implication for its prism conjunction. Discovery's general short-block NP-completeness still makes an all-image polynomial algorithm an avenue toward P=NP, with all-input coverage and cost OPEN. The guarded degree-two matching branch establishes only its stated polynomial restriction.

## Family, model and quantifiers

Fix any uniform deterministic correct solver A for the project's permitted Boolean decision inputs. It uses one finite-alphabet writable tape, one unit-moving head, reads before writes, and terminated Boolean output at origin. Input, source copies, addresses, caches and work share that tape. Fix q≥3, k≥1, and z in {0,1}^k. Concatenate k disjoint copies of Construction's q-prism source, with fixed component order and disjoint names. Let z_j select its switched version. The exact-one rows have m=k(6q+4), v=k(9q+6), and SAT iff AND(z)=1. The source is explicit, with O(kq log(kq+1)) encoded bits.

In the unswitched graph, three odd lobes each require their hub edge in a perfect matching, contradicting the common hub's single matched edge. The two-rung switch gives Construction's explicit perfect matching. Positive exact-one rows and matching edges are equivalent in both directions. The source generator fixes edge IDs and incidence ordering. No source label is supplied to A.

The short-block cycle compiler has t=5v+6m, r=3m, d=8t, c=26t+4r. Define
g=max(3,2 floor((c+1)/2)+1),
n0=d+(10c+1)g+2, m0=(20c+4)g,
n=n0+m0+3, M=2m0+4, W=ceil(log2(n+1)),
H=n+2+2 floor(log2(M+1)),
N=H+3M(W+1)+2n+W=Θ((kq)² log(kq+1)).
The ordered physical fields are unary n, gamma(M+1), signed W-bit literal IDs, two n-bit witness strings, and the W-bit release ID. All bounds below refer directly to this N-bit image.

For every such A,q,k,z and every observable stopping checkpoint τ≤T_A(I(z)), define I_j=1 if no bit in the compiled difference support D'_j has been read by τ. Put p_j=product_(i≠j)z_i. The composed statement is
T_A(I(z))−τ ≥ sum_j p_j I_j.
A may do arbitrary paid preprocessing, relocation, algebra, graph matching and caching.

Four falsifiers are overlapping or shared-metadata differences, an ID edit that changes instruction destinations, a checkpoint depending on unread input, and counting an already acquired support again. The layout proof excludes the first two, the observation-defined stopping rule excludes the third, and I_j debits the fourth.

## Exact support formula

This is an extension of [the previous compiler proof](https://github.com/j15marti/pnp/blob/6fecbf3b15a85e2739d48230d13c8849330c2653/research/agents/charged-synthesis/PNP_Charged_synthesis_2026-11-22_062000_Compiled_First_Read_Integration.md), blob 7a1d7ceee32c36f71f6898424cd0f3a9a0c9eabb. The original [dihedral compiler](https://github.com/j15marti/pnp/blob/6fecbf3b15a85e2739d48230d13c8849330c2653/experiments/dynamic_construction_dihedral_choice_20261121.py), blob 2594827de4212907b08418336b47f15e85f44b92, and [support checker](https://github.com/j15marti/pnp/blob/6fecbf3b15a85e2739d48230d13c8849330c2653/experiments/dynamic_synthesis_compiler_support_20261122.py), blob 3794d1be55cca5f4e6789b24f3dc5e6128984ada, were read. The earlier wrapper/serializer proof is inherited at that pinned revision.

Number exact-one rows a and occurrence slots s=0,1,2 from zero. Let C_j be the set of positions (a,s) where the two source versions of component j have different variable IDs x and y. C_j is nonempty, depends only on q,k,j, and is disjoint from C_i for i≠j. Although a switch can reorder several incidence entries within a row, every affected row stays inside its fixed component block. All counts and the IDs assigned to other components remain unchanged.

A source occurrence at (a,s) contributes appended parity row u=3a+s. Only its first argument changes, from variable-interior column 5x+1 to 5y+1. Its other arguments are the two fixed endpoints in the same clause block. Thus only the first literal IDs in proper clauses
K=26t+4u, K+1, K+2, K+3
change, from A_x=15x+6 to A_y=15y+6. Their four sign patterns are fixed. Base exact-one factors, rung clauses and link words stay invariant. The changed argument belongs to the variable block, distinct from the clause endpoints, so the clauses remain proper.

For each of these four clauses K', the first literal occurs at instruction positions e in {0,2,6,8} of its ten-instruction word. Its sign and active action stay fixed. Therefore every conditional state destination stays fixed, and only the selector guard ID changes in each of the 2g transition clauses. With vertex h in {0,...,g−1} and branch bit b in {0,1}, set
ell=10K'+e,
s0=4g+2g ell+2h+b,
P=H+3(5+2s0)(W+1)+(W+1)+1.
The changed field is the second literal's ID in target wrapper clause 5+2s0. If J(x,y) contains the positions where the W-bit encodings of A_x,A_y differ, its exact support is {P+i | i in J(x,y)}.

D'_j is the union of these sets over (a,s) in C_j, four K' values, four e values, all h and both branches. Distinct occurrence rows have distinct proper clauses and instruction layers, so these sets cannot overlap across occurrences or components. Therefore
|D'_j|=32g sum_((a,s) in C_j) popcount((15x+6) XOR (15y+6)).
Every D'_j is nonempty and independent of other switch choices. This is the complete physical difference support, including all replicated fields.

No allocation depends on the edited selector ID. Counts d,c,g,n0,m0,n,M,W, pins, state variables, signs, framing, auxiliary names, release ID and witness strings remain fixed. The base constraints retain all source names, so the compiler's dense-name requirement does not trigger renaming. The common cycle seam and adjacent local witness property retain the previously proved Boolean equivalence. A hypothetical alternative compiler that sorts or deduplicates clauses would require a new support proof.

## Actual decoder, event reuse and cap comparison

For any pivotal coordinate with an unread D'_j, the two valid images differing only in z_j have opposite outputs. Their actual histories agree until the first D'_j read. Read-before-write prevents silent destruction of an unseen difference. Hence a correct A must perform such a read in its suffix. Disjoint supports give distinct actual transitions. This proves the pointwise claim above.

For uniform z define U_j=p_j z_j and B_j=(public A,q,k,encoding,stopping rule,z_-j,H_τ), where H_τ contains observed symbols, writes, head positions and control, with no unread initial cells. If p_j=0, U_j=0 and E_j,Π_j are empty. If p_j=1 but D'_j was acquired, the observed first differing symbol decodes z_j and E_j,Π_j are empty. Otherwise E_j is the singleton actual first D'_j read after τ and Π_j is its binary symbol.

Given B_j, paired simulation of the two candidate images determines the common future path until that read, including its address. No advice selector is supplied. The record identifies the candidate. The decoder need not be computationally efficient and is not a subroutine supplied to A. Each conditional codebook is either {empty} or {0,1}, so b_cap=1, h_j=0,ρ=1. Before acquisition the conditional bit remains fair. Thus
H(U_j|B_j)=Pr(p_j I_j=1),
E[T_suffix] ≥ (sum_j H(U_j|B_j)−sum_j E[h_j])/(b_cap ρ)
              = E[sum_j p_j I_j].
Under the initial uniform prior this demand is k/2^(k−1). On the all-SAT image the pointwise demand is k. After all supports have been read it is zero. The 32g replicated fields per occurrence do not increase the number of compulsory events proved.

Construction's fixed guarded matching solver still pays exact parsing, source authentication by regeneration/comparison, discovery and failed guards, conversion, addresses, dense labels, retained input/copies, accesses, recomputation, cache and origin output. Its symbolic same-execution bound is T=O(N⁴), peak span O(N), physical CM=O(N⁵), and independently descriptive CM=O(N⁵) by input-plus-time replay. Its general fallback remains O(N⁴+2^n N³). Construction of the N-bit image costs O(N³) time and O(N) span under the inherited compiler tariff. No discovery or access is free in either statement.

For T≤K N^a retain S=O(N^a), physical CM=O(N^(2a)), descriptive CM=O(N^(a+1)), and the separate count-map circuit ceiling O(N^a log N). Since k≤kq=Θ(sqrt(N/log N)), this acquisition certificate excludes no fixed cap with a≥1. The internally reviewed permutation result keeps its single-tape quadratic/cubic baseline and static-method ceiling. No counting or witness-enumeration claim is substituted for Boolean decision. DISJ/equality, affine, complement, forced-domain, private-leaf and cache controls remain admissible. Simultaneous accounting uses one execution. Configuration counting is only an upper description bound. No relativization, algebrization or Natural Proofs barrier is crossed.

## Evidence and next dependency

The new [checker](../../../experiments/dynamic_synthesis_prism_support_20261122.py) imports the pinned original prism generator. For q=3,...,8 and k=1,...,4 it checks all switch vectors and all one-coordinate flips, 588 comparisons. It verifies exact occurrence changes, independence from other choices, disjoint occurrence positions, nonempty supports and symbolic target-field endpoints. The [raw output](../../../results/raw/dynamic_synthesis_prism_support_20261122.json) records all 24 parameter pairs and predicted changed-bit counts. For q=3,k=1, N=250678096703 and the predicted support has 5622848 bits across four changed occurrences. The full target string was not allocated. No native solver, kernel proof, or fresh full-compiler experiment is claimed. The symbolic compiler proof establishes the unmaterialized support equality. Earlier generic full-image tests were not repeated. No random seed.

One next mathematical task remains DYNAMIC-POST-ACQUISITION-OPPONENT1, owner Bounds. Exhibit a model-enforced opposite-answer opponent at a specified reachable checkpoint after acquisition, and prove an actual future decoder with charged selectors and bounded reuse. Repeatedly renaming acquired supports cannot replenish this certificate.

| Receiving role | Concrete dependency |
|---|---|
| Bounds | Apply the compiled pivotal bound directly in N, then address post-acquisition necessity. |
| Accounting | Audit the conditional records and distinguish compulsory first reads from optional cached scans. |
| Redteam | Independently attack C_j disjointness, the sign-invariant destination step and witness/header invariance before promotion. |
| Construction | Preserve the matching branch and seek an exact method for higher source incidence, with paid guard and all-input fallback. |
| Discovery | Test higher-incidence contraction for uniform polynomial coverage, or give the first obstruction. The online-output deadline still requires its own transfer. |
| Synthesis | Preserve both the general completeness implication toward P=NP and the missing recurrence toward a separation. |

These requests are filed through this handoff and issue 324. Review status remains pending. Historical manuscript ownership and scheduler state were preserved. Selected-file environment, so full-checkout preflight and LaTeX build were unavailable.

## Fresh search log

Primary query “Tseitin encoding circuit local clauses variable renaming blocked clause elimination Jarvisalo Biere Heule”. Read the author-hosted [Blocked Clause Elimination](https://www.cs.utexas.edu/~marijn/publications/BCE.pdf), 15-page version, model and Theorem 1. Its theorem compares BCE on standard Tseitin encodings of constrained acyclic circuits with the specified circuit simplifications and polarity encoding. This supports permitting exact preprocessing. Its hypotheses do not prove the entire project wrapper collapses, and no general SAT running-time theorem is imported.

Fresh connected query `"SAT" "compiler" "selector"` in all six organizations gave unrelated excerpts in anthropics (vulnerability notebook, 8ad5de647d4f0f50c95d74aabc8aa20a3f70cdd3), xai-org (feed README, 269340ce2eb8ca785bafa4f2c17a2e8b752bccd3), google (Boost selector, 9648cacb21a71aa6c21b3fca504f146c39164a53), google-research (OpenFST, c949a4cd45bf9f8faafba7b6b594b43edca1a9c2), and google-deepmind (MuJoCo, f5a936990fbbb1728ed3fbf99c4738346e18717e). OpenAI initially returned429. Retry returned math/lean/OAI/Computability/FiniteCompiler/Selectors.lean at 4eaee87548250b2682affda7d05d947c05554bae. Only imports and a descriptive comment were exposed. No proof term was validated or executed.

Two web fallbacks scoped the same six accounts with “SAT compiler selector”. OR-Tools solver documentation, compiler backends, Tracr and comparator/formal-machine leads surfaced. No inspected result supplied the missing post-acquisition theorem. Fresh ownership pages were opened for [Anthropic](https://github.com/anthropics), [OpenAI](https://github.com/openai), [xAI's corporate release](https://x.ai/news/grok-os), [Google organization policy](https://opensource.google/documentation/reference/github/where), [Research resources](https://research.google/resources/) and [DeepMind's project](https://deepmind.google/science/alphafold/), consistent with the preceding verified attribution. Bounded negative relevance findings are not exhaustive absence claims. An initial guessed checker filename returned404, then the exact path from the owned report was retrieved successfully.
