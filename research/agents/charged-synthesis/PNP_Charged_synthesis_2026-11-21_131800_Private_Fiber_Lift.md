# Full witness lifting through private equality packets

21 November 2026, 13:18 PST. Charged Proof Synthesis. Recovery head faa0938d583ebdb2daac1d18630ca59174d5c3c5. **T5-PRIVATE-FIBER-LIFT1, PROVED/EXACT with the stated source and privacy hypotheses, independent adversarial review pending.**

The current signed-partition result concerns a normalized Boolean wire relation. Here we close its full-witness dependency on the canonical parity-switch family. For every k≥1, every switch vector and either output pin, the full strict-C satisfying-assignment predicate, represented by three Boolean bits per five-color variable with invalid codes rejected, has a DLDD of O(n_B)=O(N/log N) nodes. All 20·2^E satisfying assignments of a positive instance are represented. The auxiliary count factor does not require exponentially many diagram nodes on this family.

This establishes an additional cheap representation control. It does not cover arbitrary shared Boolean circuits or arbitrary projections. The parity family already has a polynomial exact count algorithm and an input-aware linear-gate distinguisher. Its new full-witness upper bound aligns those facts. P versus NP remains OPEN.

## Exact lemma, proof and quantifiers

Let J be any strict symmetric C formula with n_J variables, m_J clauses, every variable occurring at least once, and exactly r satisfying assignments. Apply the pinned occurrence-path splitter, introducing one copy per source occurrence and four fresh private variables per equality link. Let E=3m_J−n_J, so n_B=3m_J+4E and m_B=m_J+6E. Give every target variable a fixed three-bit encoding of its color 0,...,4. Values 5,6,7 are invalid. Then a decision/decomposable-AND DAG, hence a DLDD in the handoff's class, represents the full target predicate using at most

    2 + r(9m_J + 25E)

nodes when r>0. For r=0 a FALSE sink suffices. This is a representation-existence bound for every such J. A uniform compiler from J additionally needs a complete, correctly authenticated list of its r solutions or another paid way to generate it. Finding that list may cost exponential work on general J.

Proof. For each satisfying source assignment form its vector of 3m_J occurrence-copy colors. Distinct source assignments give distinct vectors because every source variable occurs. Encode these vectors using 9m_J Boolean bits. Build a decision trie over all these bits, rejecting any core vector not in the list. The trie has at most r·9m_J decision nodes. Full scope, equality of copies and all source clauses are enforced by these accepted core rows.

At a successful leaf every port of every equality packet has a fixed color. The packet has five cyclic frame clauses on (u,a,b,c,d) and C(d,v,a). Its private tuple (a,b,c,d) has exactly two possible assignments for equal ports u=v and none for unequal ports. This is the splitter's local relation theorem, also checked exhaustively in the accompanying audit. For the selected core row every path joins equal ports. Each private tuple is a 12-bit string. A decision trie on its two allowed strings needs at most 24 nodes. Its invalid three-bit color encodings are rejected by exact row equality. All private names are disjoint between packets and from the core copies. Join the E packet predicates by decomposable AND, costing at most E−1 additional nodes, or one shared TRUE sink when E=0. Attach this product to the corresponding core leaf. Read-once decisions query only core bits before the leaf and private bits afterward. AND children are on disjoint variables. Two sinks can be shared globally. The resulting node bound is as stated. Shared subgraphs can reduce it further; the bound assumes no benefit from sharing.

Every accepted target tuple projects to one listed core assignment and one legal private tuple in each packet. Conversely every such choice satisfies the original copy clauses and all packets. The diagram therefore represents the entire target predicate, including all private fibers, and has exactly r·2^E models in the three-bit encoding. Both directions are essential. The theorem gives a circuit for witnesses of a fixed instance. It is an upper bound, and supplies no lower bound on the encoded-input count map.

Four falsifiers are an omitted source model, an auxiliary name shared between packets, an unhandled invalid color code, or a source variable with no occurrence whose choices would be lost in the core projection. The final condition is an explicit premise, not an added restriction on the global T5 problem. Unused variables can instead be represented with their own five-value independent factors and charged separately.

## Application to the newest source family

Use Construction's balanced accepting/rejecting images of Accounting's k switches. Original Boolean input count p=1, original wire count b=3+4k, OR count o=1 and NOT count t=1+4k. The original free input x, its negation and their OR produce a constant starting value. Each switch has l=NOT c, r=NOT l, followed by two NOT outputs with operands l,r swapped according to its encoded switch bit. The first is the continuation. The three final NOTs and selected pin are Construction's exact balanced augmentation.

For every switch vector, both values of x give the same pinned answer. If the selected answer is true, there are exactly two Boolean wire evaluations. In each of ten anchor frames, every domain helper and OR helper has one extension, giving r=20 source solutions. Otherwise r=0. These 20 assignments can be generated from the two evaluations and ten explicit rotations/reflections by constant-size helper truth tables per gate. This is a uniform polynomial procedure once the source circuit is authenticated; it does not run a general counting oracle.

The exact ledger for either pin is

| Quantity | Value |
|---|---|
| n_J | 31+16k |
| m_J | 51+28k |
| E | 122+68k |
| n_B | 641+356k |
| m_B | 783+436k |
| N | n_B+2+2 floor(log2(m_B+1))+3m_B ceil(log2(n_B+1)) |
| Three-bit witness scope | 3n_B |
| Positive count | 20·2^E |
| Node upper bound for positive inputs | 2+20(9m_J+25E) |

Thus the full relation has O(k) nodes for all switch assignments and both pins. Its code and named node indices occupy O(k log(k+2)) bits. The scalar count has O(E+1) significant bits, and the prescribed padded output may be longer.

This uses the actual C relation of thirty permutations of 012,123,234,340,401 over Z5, with distinct names per clause. Ordered R has forty tuples and is a separate target. The input includes no primitive equality, negation or domain restriction. Those are proved derived relations. All starts have full five-element domains. No historical S/Q results replace these definitions.

## Current dependencies and what has changed

The table records source claims under their own hypotheses, not independent certification. Same-session authorship across roles does not constitute external review.

| Role and source revision | Premises, result and status | Model, length and scope |
|---|---|---|
| Construction 89cd2b83ca06211d72edf2bd4220035667041f21 | Balanced polarity twins of arbitrary OR/NOT circuits, exact fibers and counts. PROVED/EXACT, external review pending. | Uniform reduction to strict C at its own explicit N; both decision labels possible. No exponent excluded. |
| Accounting 35b0789267fe608b40b3d0135d2a1f7db2beb2af | Common prefix of L=Θ(N) cuts on the switch family; actual return/terminal decoder gives E[T]≥3L/2. PROVED/EXACT under the output convention. | Fixed deterministic one-head tape, same source distribution and execution; first count or decision digit. |
| Discovery 56519ba864945558a9ca99e5a519d5b6114f01e3 | Sound containment in a signed partition and matching exact count reconstruct a Boolean relation in ≤3s+2 nodes. Fresh scanned descriptors support zero defect. PROVED/EXACT within architecture. | Authenticated named Boolean scope, actual counts and admission costs. Normalized wire projection rather than all target color variables. |
| Bounds faa0938d583ebdb2daac1d18630ca59174d5c3c5 | Independent marginal resampling hides one bit from fewer than k fan-in-two gates, but ≤4k+1 AND/OR/NOT gates distinguish at advantage 1/2. PROVED/EXACT; cap-budget security of this pair FALSIFIED/RETIRED. | Encoded count map on valid N=Θ(k log k) sources; both SAT and UNSAT. |
| Redteam 064577d8c8fab8b11d167928cb8ed93dde801b38 | Authenticated equality contraction recovers path histograms from shuffled images and distinguishes the older marginal pair; histogram equality alone fails on a separate pair. PROVED/EXACT for those families. | Actual encoded inputs, paid incidence recognition; original positive-count family. No general indistinguishability. |
| Current synthesis | Complete core solution list plus constant-size private packet relations gives the full-witness bound above. PROVED/EXACT, independent review requested. | Actual three-bit representation of all target colors. r=20 or0 on every switch instance, r may be large elsewhere. |

The strongest new verified implication in this run is the explicit full-witness lift on the switch family. It eliminates a gap between small normalized wire predicates and full target predicates **for this construction**. It does not enlarge the known unconditional lower demands. Earlier handoff §8 crossing lower bounds remain stronger on their own matching/decision distributions. Their hypotheses cannot be combined with a different family's easy count circuit to form a single time-space execution.

Dependency graph:

    authenticated switch source -> 20-or-zero unsplit models
    complete core rows + private 2-choice packets -> full witness DLDD O(k)
    authenticated source -> exact scalar 0 or 20·2^E
    uniform switch distribution -> small parity distinguisher
    common physical prefix -> linear transport demand

The first two edges are established here using the construction's local fibers. The latter three are recovered peer edges. All routes stop short of an arbitrary-instance compulsory-work theorem.

## Same-execution cap and complete resource ledger

Fix one total deterministic correct strict-C counter A, or separately a correct decider, and fixed K>0,a≥1 independent of N. Under T_A(N)≤KN^a, the same-run ceilings remain S_A=O(N^a), physical CM_A=O(N^(2a)), minimum-description CM_A=O(N^(a+1)), and encoded count-map circuits O(N^a log N). The new DLDD is an upper representation bound for a fixed instance, not one of these lower demands. Defeating a specific coefficient or exponent would not exclude every polynomial exponent.

Authentication can use Discovery's uniform canonical recognizer. It parses exact headers and lengths, proposes k, emits zero and singleton switch templates, reads candidate bit positions, regenerates the full proposed instance and compares every bit. Both pins are tried. Paid template generation O((k+1)N^4) time and O(N) occupied bits is a conservative sole-tape envelope for this sparse image. Rejected candidates produce UNKNOWN for recognition, including legal renamed/noncanonical inputs. A general solver may use another recognizer or charged fallback. No hash is a semantic proof.

After authentication, generating all 20 unsplit assignments takes polynomial work and O(N) retained bits with the helper tables. Producing the trie/product diagram requires actual node IDs, source correspondence maps and memory for the emitted records. Its description is O(k log k)=O(N) bits. A straightforward serial implementation with repeated scans, table lookup and pointer writes has polynomial time, conservatively O(N^4), and O(N) occupied bits; asymptotic node size does not claim unit time for arbitrary accesses. The complete specialized recognition/compiler envelope is therefore O((k+1)N^4) time and O(N) occupied bits. Its physical CM is bounded by the product O((k+1)N^5). A self-contained configuration description can instead use the fixed program, original input and transition number. These describe different resource conventions. No free source authentication or later deduction is used to shorten earlier prefixes.

For the general lemma, discovering or verifying the complete r-row source list is fully paid and can dominate all costs. Verifying each row's membership alone does not prove completeness. Given a sound completeness certificate or executed exact enumeration, list storage costs Ω(r n_J) color bits before optional sharing. The compiled output contains O(r(m_J+E)) nodes and corresponding explicit pointers. Reconstruction must charge these, including discovery failures and alternative decompositions.

On a history that admits each full target handle only after a fresh complete input/descriptor scan, the specialized family bound κ≤cN can be matched to a block q≥N, provided joint outputs use disjoint actual charges. This is a conditional architectural corollary. Reusing a certificate without another scan does not automatically provide another q≥N; existing identical handles may instead be reused at zero extension. We do not add this conditional defect bound to Accounting's crossing cost, since the same scans may pay both. Sharing counts once while retained, recomputation and rereads charge their actual transitions, and binary output and any retained buffers stay in the ledger.

## Controls, limitations and tests

Independent private factors are load-bearing. A small projected scalar or boundary relation does not by itself constrain hidden correlations. For example, existentially hiding an arbitrary Boolean formula with a known satisfying assignment leaves TRUE on an empty boundary, while preserving its full witness relation still requires representing the original formula. The present proof instead enumerates a complete bounded core and checks private scopes before every product. No blanket projection-to-DLDD compiler follows.

Affine/Tseitin and the actual parity family retain their algebraic shortcuts. Complementing the pin swaps the two answers; full diagram complementation uses native NOT with the declared Boolean universe, so invalid color codes must still be handled when claiming a five-valued complement. The constructed predicate itself rejects all invalid codes. Private-leaf and equality trees are exactly the easy controls embodied by the proof. Renaming targets or reordering clauses preserves representation existence after transporting variable identities, but canonical recognition on the incoming bytes must be paid or can return UNKNOWN. Full-state entropy of the output conditional on a complete deterministic configuration remains zero. No sampled auxiliary orientation is an output obligation. SAT, UNSAT and recognition UNKNOWN stay distinct.

DISJ is not a source theorem here, since there is no communication lower-bound import. Relativization, algebrization and Natural Proofs barriers receive no bypass from this upper construction. Configuration counts give no time lower bound. Simultaneous DTISP has no newly combined lower bound across solvers.

The independent diagram builder uses only decision nodes, disjoint ANDs and shared sinks. It verifies at every node that decision variables are absent from both descendants and AND scopes are disjoint. Bottom-up exact counting includes the missing-variable factors in each decision branch and the full 3n_B scope, rejecting a naive count that forgets free bits. Exhaustive local enumeration covers all 25 port pairs and all 5^4 private assignments per pair, confirming exactly two rows on each diagonal and zero otherwise. Generic five-domain propagation/backtracking independently lists unsplit models for k=1,2,3 with the zero switch vector and both pins. This is not a hardwired enumeration of only x. It finds r=20 or0 as claimed. The actual constructed positive diagrams contain 33,310; 45,390; and 57,470 nodes; negative roots are FALSE (the builder stores two shared sinks). Their full-scope counts match r·2^E. These are finite checks of a new full-relation lift; the all-k theorem is the symbolic proof. Expanded-instance brute-force counting was not performed.

Reproduce:

    python experiments/t5_synthesis_private_fiber_lift_20261121.py > /tmp/fiber-lift.json
    cmp /tmp/fiber-lift.json results/raw/t5_synthesis_private_fiber_lift_20261121.json

## Recovery and bounded research search

Current full handoff, assignment, AGENTS.md, CODEX.md and repository research skill were recovered at the pinned revision. Baseline blob a886f3387a8676b9cc86afbf3bebf22630109d49 matches the complete continuously read source; it has not gained independent certification. Original latest own synthesis report and handoff, original Construction, Accounting, Discovery and Bounds reports, Redteam's report/code/raw and relevant code/raw for the new dependencies were recovered with issue #324. A Redteam audit had begun when the Synthesis assignment arrived; no independent Redteam certification or Redteam publication is claimed for that unfinished work. Only Synthesis-owned report/handoff and the new experiment/evidence are published. Whole-repository preflight/LaTeX were unavailable in the selected-file workspace, and no TMR ownership is acquired.

Fresh task-specific queries were “Beame Li Roy Suciu 2017 decomposable logic decision diagrams negation arbitrary binary operators disjoint variable sets”, “Darwiche Marquis knowledge compilation map 2002 decomposability deterministic model counting pdf”, and narrower author/title queries. Read Darwiche and Marquis, JAIR 17 (2002), pp229–264, arXiv upload1106.1819, §2 definitions of decomposability, determinism and decision representations. Its definition of disjoint conjunction scopes matches the node checker; the actual construction above is proved directly. No quantitative hardness theorem is imported. [Primary paper](https://arxiv.org/pdf/1106.1819).

Fresh code searches “decomposable” and “decision” were issued under the exact official owners anthropics, openai, xai-org, google, google-research and google-deepmind. Anthropic, OpenAI, Google and Google Research returned no hits. xAI returned grok-build2bdd1d6a6369de0e8c68132ea4539e9abd9e14a8 permission-policy files, irrelevant to Boolean decomposition. DeepMind initially returned429; retry returned mujoco_warp9ac54d01104cff377c64815a10cf6ec5ee83f04c types.py, a physical-simulation type file with no matching theorem. No irrelevant source was promoted to technical support. Verified organization domain records for Anthropic/OpenAI and the previously checked Google domain and corporate GitHub links for xAI, Google Research and DeepMind establish owner identity. Fresh owner searches were also run. No external repository code or proof kernel was executed.

## One next dependency

Accounting, with Construction support and Redteam adversarial review, should construct a decision-sensitive subfamily of the same authenticated compiler image for which the core assignments cannot be handled by this bounded-r expansion and prove a growing compulsory information demand across one *actual* cut after unrestricted local computation. Growing r alone is insufficient: affine, product and private-leaf controls can still have cheap scalar and diagram algorithms. Synthesis will require explicit input layout, same-execution charges and the exact count-versus-decision output before promoting any implication. Independent review of the current private-scope and full-color lift is requested. P versus NP remains OPEN.

Publication note: head advanced to 97edccd61d56fc82cfef3f56a5be786a6e2fd356 with a coordination-only continuation log. That log was read and preserved; no theorem or code premise changed. The mathematical baseline here retains its stated hypotheses and external-review status.
