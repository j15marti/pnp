# Reachable hybrid conflicts give list decoding of actual crossing records

21 November 2026, 23:07 PST. PNP Lower Bound Connections.
DYNAMIC-HYBRID-CONFLICT-CODE1, within DYNAMIC-COMPATIBILITY-OBLIGATION1.

PROVED/EXACT for the following conditional single-tape lemma. Existence of sufficiently strong postprocessing checkpoint families for every solver is OPEN. Independent adversarial review pending. This is an elementary extension of the crossing argument, with no historical novelty claim.

Source revision fb25e0ddffc036b0355f12afd6983dc0f83d45ae. The new contribution to the current chain is a precise intermediate conclusion between an injective decoder and no decoder: a bounded list, with an explicit entropy debit. It applies to actual reachable configurations after arbitrary paid preprocessing. It does not authorize resetting the initial transport demand.

## Fixed model, encoding and claim

Fix one total deterministic correct Boolean compatibility decider A, before selecting a family or distribution. Use the transport report's one writable finite-alphabet tape, one head, local read/write/move transitions, no external clock, and canonical output/terminator near the origin. Q>=2 is the number of states and ell=ceil(log2 Q). Every original input is a valid N-bit encoding

    1^n 0 gamma(m+1), ordered signed triples, alpha, beta, release ID,
    w=ceil(log2(n+1)),
    N=3n+2+2 floor(log2(m+1))+3m(w+1)+w.

The supplied assignments and original layout remain charged. This is Boolean decision. The strict symmetric C and ordered R counting problems have different semantics and encodings.

Choose a finite index set V and, for each v, an actual checkpoint C_v reached by A on a valid UNSAT input of length N. All checkpoints share the same finite control state and head coordinate h. Choose a physical cut c with h<=c, and put every canonical output cell at coordinates <=c. Checkpoint times may differ. Retained source, relocated copies, addresses, caches and all scratch are included in C_v.

For two indices u,v let M(u,v) be the full configuration with the common state/head, the tape of C_u at coordinates <=c, and the tape of C_v at coordinates >c. Define a simple undirected graph G on V by placing edge {u,v} only if at least one of M(u,v), M(v,u) is actually reachable by A on a valid SAT input. Reachability is a mathematical premise to prove. Arbitrary syntactic mixing does not establish it. Duplicate checkpoints are permitted as indices but cannot have an edge between them.

Let alpha(G) be the largest independent-set size, and let U be any distribution on V. Public B specifies A, the finite checkpoint family, the cut, the index ordering and the distribution, but does not identify the sampled v or supply its selected tape half. Let E(v) be exactly the transitions crossing c after C_v and before halting. Let Z(v) be their chronological sequence of arrival control states.

**Claim.** Every fiber of Z is an independent set of G. In particular

    H(U | B,Z) <= log2 alpha(G).

Define Pi=gamma(|Z|+1) followed by ell-bit state identifiers. This is conditionally prefix-free and has exact length ell |E|+h_rec, where h_rec=2 floor(log2(|E|+1))+1. Then

    ell E|E| >= H(U|B) - log2 alpha(G) - E[h_rec].

For several obligations j, each with these hypotheses, evaluated on the SAME distribution of original inputs and the SAME execution of A, if each transition belongs to at most rho of their crossing event sets, then

    E[T] >= (sum_j H(U_j|B_j)
              - sum_j log2 alpha(G_j)
              - sum_j E[h_rec,j]) / (ell rho).

Use max(0,right side) when reporting a lower bound. A random public context is also allowed by applying the statement conditionally and averaging log alpha. No independence among U_j is required.

Four falsifiers are an unreachable SAT hybrid, an omitted cache or control field, a record truncated before its full halting suffix, and reuse of the same crossing without increasing rho. These are hypotheses of the theorem and explicit bypass targets.

## Proof and actual decoder

Suppose adjacent u,v have equal complete suffix crossing sequences. Start from the mixed configuration M(u,v). Its first left-side excursion follows the continuation from C_u. At the first crossing its arrival state matches that of the C_v continuation. Its right-side excursion therefore follows C_v. Alternate these excursions. Each half has exactly the local contents that its donor run has after the same number of visits. Equal sequence lengths and the common initial head side make the final side agree. The final excursion halts as its donor does. The mixed run writes the same canonical answer as the left donor, namely UNSAT. This also covers halting on the right, since the completed output lies on the left. With zero crossings the whole continuation stays on the left and has the same conclusion. If either orientation of the mixed configuration is reachable from a SAT input, correctness is contradicted. Hence equal records cannot occur across an edge.

The actual list decoder takes B and Pi, parses its self-delimited length and states, simulates A from each supplied C_v to termination, and outputs the indices producing that sequence. It terminates because the listed configurations are reachable on a total machine. Its output is precisely the fiber containing U, whose size is at most alpha(G). This is an external information-theoretic decoder, with no efficient runtime claim and no solver obligation to materialize this list. Its enumeration, source table and simulation are NOT performed for free by A. If alpha=1 it is an exact decoder satisfying H(U|B,Pi)=0. For alpha>1, an exact decoder additionally requires the index within this list. Such extra information is not present in the observed record, so it cannot be charged as another actual machine event.

Conditional support size bounds the remaining entropy by log alpha. Thus I(U;Pi|B)>=H(U|B)-log alpha. Prefix coding gives I(U;Pi|B)<=H(Pi|B)<=E|Pi|. Substitute the exact record length. Finally sum over j and apply sum_j |E_j(x)|<=rho T_A(x) pointwise. This proves the displayed inequality. Record boundaries are paid by h_rec. Directions alternate from a fixed starting side. No individual timestamps or addresses are needed for this decoder because B fixes one cut and the complete suffix; including a clock or a selected checkpoint identity that leaks U would require recomputing the conditional entropy.

A public mathematical checkpoint family is analogous to the public codebook in the static crossing proof. It is not permission to omit retained data when constructing hybrids. If B instead reveals the sampled source or complete C_U, H(U|B) may fall, and the formula must use that smaller entropy. No full-state conditional-entropy work measure is asserted.

## Application to current families and the open step

At the initial checkpoints of the transport permutation family I_(pi,pi), every unequal mixed input I_(pi,sigma) is SAT. G is a clique on r! indices, alpha=1, and the theorem recovers full permutation decoding from the complete crossing record, with explicit length framing. This is a calibration of the lemma, not a new certification of the transport theorem.

After Discovery's 22:53 solver computes its answer on the connected parity-block family, it can erase source and workspace and enter common READY with only the answer bit. For fixed k all its UNSAT checkpoints are identical. For the index set of nonconstant sign strings, |V|=2^k-2, every mixed configuration is that same UNSAT checkpoint. It cannot also be reached on a SAT input by determinism and correctness. Therefore G is edgeless, alpha=|V|, and H(U)-log alpha=0 for the uniform distribution. The same conclusion holds for any distribution because H(U)<=log |V|. The graph calculation explicitly locates the failure of a renewed full-index decoder after preprocessing.

This is a new audit of the reachability premise and list debit, rather than a repeated execution of Discovery's experiment. Its code and raw outputs were recovered at the pinned source revision. Discovery's 124 source cases and two compiled opposite-label controls remain its finite evidence, not new tests in this run.

Construction's 22:32 two-hub family has a correct paid two-variable conditioning algorithm. Its mathematical upper bound O(N^5) time and O(N) span remains a valid bypass to the proposed private-prefix service. Discovery extends admission by acquiring one pivot and local backdoors, with O(3^p N^7) time, O(N) span and separate O(3^p N^8) physical and descriptive cumulative upper bounds. These results remain scoped to their authenticated images and parameters. The new conflict lemma supplies no polynomial bound on p for arbitrary sources.

A proposed dynamic phase ending before halting needs a further splicing/decoding theorem for that endpoint. Two different intermediate configurations may share the same crossing prefix and later distinguish the inputs. Consequently the full-suffix theorem alone cannot be added across disjoint short phases. Keeping full suffixes is valid, but their overlap must enter rho. The first unresolved premise is a large reachable-hybrid conflict graph after paid preprocessing, together with a justified event family whose entropy debit and reuse remain small.

## Same-execution resource ledger

Parsing, authentication, discovery, failed candidates, conversion, switching, source/address reads, retained input, copies, caches, recomputation and output belong to A's complete time T. The theorem charges a subset of those actual transitions, without inventing a new computational graph. Every cut crossing emits at most ell state bits to the external record. Framing h_rec is subtracted, not treated as transferred payload. Physical source access is required by the one-tape model. The graph and the decoder are proof objects, and no efficient construction of them is claimed as an algorithmic result.

Peak span is S=O_A(N+T). Physical CM=sum_t s_t is at most O_A(T(N+T)). Minimum-description CM=sum_t K(C_t|A) is separately at most O_A(T(N+log(T+2))) by replay. The present lemma gives a TIME bound and does not multiply it by unrelated storage maxima or claim a new CM lower bound.

For fixed K,a>=1 and T<=K N^a, the cap comparison required is

    sum_j [H(U_j|B_j)-log2 alpha(G_j)-E h_rec,j] > ell rho K N^a.

The corresponding ceilings are S=O(N^a), physical CM=O(N^(2a)), descriptive CM=O(N^(a+1)). The count-map circuit ceiling O(N^a log N) has no counting-to-decision role here. The initial permutation calibration still has its matching quadratic time and cubic CM algorithm and static demand ceilings N²/8 and N³/27. Excluding one fixed exponent cannot exclude every polynomial exponent.

DISJ/equality sanity PASS for the scoped crossing proof and cached collapse. Simultaneous DTISP PASS because event reuse is pointwise on the same execution. Deterministic configuration consistency PASS because identical complete states cannot require opposite labels. Relativization gate OPEN for any unrestricted promotion: nonlocal oracle access invalidates excursion splicing. Natural Proofs and algebrization are not invoked. Affine/Tseitin, complement, renaming, private-leaf trees, forced domains and decision witnesses remain legitimate shortcuts; none independently guarantees reachable mixed checkpoints. Relocation is included in the snapshot, and sharing is included in rho. P versus NP remains OPEN.

## Sources, searches and reproducibility

Primary search queries were “Witsenhausen zero error side information graph coloring conditional entropy 1976” and “Hartmanis one tape Turing machine crossing sequences 1968 paper”. Hartmanis's original JACM paper was opened and its crossing method inspected. Its single-tape scope applies; its memory/time theorems are not imported here. Witsenhausen's 1976 IEEE entry was found, but the accessible publisher page did not expose its proof text. That paper is bibliographic context only. The coloring and entropy argument above is proved directly.

Fresh GitHub query '"confusability" "graph"' covered anthropics, openai, xai-org, google, google-research and google-deepmind. OpenAI first returned rate limiting and succeeded on retry with no matches. Four other scopes returned no matches. Google returned an unrelated fonts lesson about visual character confusability at 06bfe0d62a98375cb09c942fa18e68bd32cff057, rejected from the search excerpt. No external repository code or theorem imported. Ownership checks used the verified Anthropic/OpenAI GitHub profiles, xAI's official Grok release link and Google's official organization guidance. These bounded searches are not an exhaustive absence claim.

In-repository query '"conflict" "crossing" "independence"' returned earlier affine/interface and snapshot reports, with no exact matching lemma in the limited results. No novelty claim follows. Governance, skill, current directive, transport report, applicable T5 definitions, own previous projected-cut report, Construction/Discovery reports and their original code/raw evidence were recovered at the source revision. Issue 324's latest handoffs were read. The full recursive-tree API request failed, and this workspace is not a full checkout, so repository preflight and manuscript compilation were not run. This role owns no TMR manuscript.

The new standalone audit checks all graphs on 1 through 4 labeled vertices and every proper coloring using at most n colors. It verifies the fiber bound and its uniform entropy consequence by exact integer exponentiation. Result: 75 graphs and 7,238 proper colorings. It does not verify machine reachability or an asymptotic SAT lower bound.

Run python experiments/dynamic_bounds_hybrid_conflict_20261121.py.
[Code](../../../experiments/dynamic_bounds_hybrid_conflict_20261121.py).
[Raw](../../../results/raw/dynamic_bounds_hybrid_conflict_20261121.json).

Primary references:
1. Hartmanis, Computational Complexity of One-Tape Turing Machine Computations, JACM 15(2), 1968, 325–339. https://cse.iitkgp.ac.in/~goutam/toc/readingMaterial/computational-complexity-one-tape-Hart.pdf
2. Witsenhausen, The zero-error side information problem and chromatic numbers, IEEE TIT 22(5), 1976, 592–593. https://doi.org/10.1109/TIT.1976.1055607 (full proof unavailable in this run).
3. Current transport and local-obligation reports under research/main at fb25e0ddffc036b0355f12afd6983dc0f83d45ae.
4. [Construction](../charged-construction/PNP_Charged_construction_2026-11-21_223200_Connected_Two_Hub_Family.md) and [Discovery](../charged-discovery/PNP_Charged_discovery_2026-11-21_225300_Component_Pivot.md), at the same revision.

**One next dependency.** Construction and Bounds must exhibit an actual postpreprocessing family with reachable SAT hybrids and a small independence number. Accounting must bound overlap of its full-suffix events, or prove a new finite-phase decoder before shortening them. Redteam should test mixed-state reachability after the cached answer and relocation. Synthesis receives the list-decoding debit and the still-open recurrence premise. Independent adversarial review is requested before promotion beyond this conditional lemma.
