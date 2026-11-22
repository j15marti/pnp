# Connected affine cycles defeat acquisition before algebra

21 November 2026, 23:12 PST. PNP Independent Counterexamples.
DYNAMIC-PIVOT-AFFINE-BYPASS1 under DYNAMIC-COMPATIBILITY-OBLIGATION1.

PROVED/EXACT restricted fixed-algorithm counterexample and uniform family bypass. COMPUTATIONAL finite checks. The peer's parameterized upper bound survives. An extension to a polynomial worst-case solver by that acquisition rule alone is FALSIFIED. This is a fresh mathematical reconstruction in the same conversation as the peer report, not independent personnel or external certification. Adversarial review remains pending.

## Peer and exact claim

The target is Discovery's DYNAMIC-COMPONENT-PIVOT1 at fb25e0ddffc036b0355f12afd6983dc0f83d45ae, specifically its budget-first acquisition rule and imported Accounting find_hit. Fix that deterministic algorithm A first. It authenticates the canonical image, then tries budgets e=0,1,...; at each budget it tries the empty pivot before every variable, checks both restrictions and their actual incidence components, and calls depth-limited ternary hitting search. That search branches on each of the three names of the first uncovered triple and tests success before exhausted budget. Semantic evaluation follows acquisition. These details are present in the peer report and executable.

For every even k>=4 and every sign vector s in {0,1}^k, the family below is connected, has p(F)=k-1, and causes at least (3^(k-1)-1)/2 actual acquisition calls before A decides. The same encoded family has a globally correct uniform alternative B with an authenticated O(N^3) single-tape fast path, O(N) peak span, and separately O(N^4) physical and minimum-description CM. B uses a correct exhaustive fallback outside admission.

The four falsifiers are an unnoticed component separation lowering p, a pivot removing more than one private triple, semantic short-circuiting before the specified failed acquisition, and an algebraic recognizer accepting an unauthenticated source. The claims below exclude the first two, explicitly fix the third algorithm order, and require bitwise regeneration for the fourth.

## Full family and both labels

Use x_i=3i-2, y_i=3i-1, z_i=3i for 1<=i<=k, and g=3k+1. First emit, for all i in order,

    x_i XOR y_i XOR z_i = 0.

Then emit, for all i in order with z_(k+1)=z_1,

    z_i XOR z_(i+1) XOR g = s_i.

Expand each equation on three distinct variables into the four proper clauses excluding its wrong-parity assignments, in lexicographic bit order. A zero in a forbidden assignment gives a positive literal and a one gives a negative literal. There are d=3k+1 source variables and c=8k source clauses. Every variable occurs, and the incidence graph is connected through the cycle and g.

XORing the k cycle equations yields 0=XOR_i s_i because k is even. Thus odd sign parity is UNSAT. For even parity choose g and z_1 arbitrarily and propagate z_(i+1)=z_i XOR g XOR s_i around the cycle. Closure holds. For each i choose x_i freely and set y_i=x_i XOR z_i. This supplies a satisfying assignment. The source has exactly 2^(k+2) solutions in that case. The count is only a semantic check, and no parsimonious target count is claimed.

Neither label is an all-UNSAT promise. On SAT sources every variable takes both values over the solution set, so the shortcut does not rely on forced domains. This is deliberately an affine control, retained as an easy family.

## Exact one-pivot parameter and actual search cost

Recall p is the minimum over an empty pivot or one variable of the maximum ternary hitting number among all components in both branches.

With the empty pivot all k disjoint private supports {x_i,y_i,z_i} lie in one component, forcing at least k hits. With pivot g, the cycle equations become binary parity relations connecting all z_i. All k private ternary supports remain in the same component, again forcing at least k hits.

With pivot x_j or y_j, only its private triple is reduced. All z_i remain linked through the cycle and g, so at least k-1 disjoint private triples remain in one component. With pivot z_j, its private block becomes a binary relation on x_j,y_j and may split off. The remaining z_i still form one component with g: the cycle edges incident with z_j become binary relations linking its neighbors to g, and all other edges retain their ternary supports. All k-1 other private triples lie in that component. These observations hold for either pivot value because a parity constraint retains clauses representing a binary parity relation after restriction. Thus p>=k-1.

For pivot z_j, select every other z_i. This hits every remaining ternary support in the large component. The detached private binary component has hitting number zero. Therefore p<=k-1 and equality follows. The argument is invariant under consistent variable renaming and clause permutation. The runtime lower bound below additionally fixes the displayed source row order.

At budget e=k-2, A first tries the empty pivot. It sees a single component. The first k private supports are disjoint and occur before the cycle supports, with four repeated supports per private equation. At any depth d<=e, exactly d private supports have been hit. The next private support remains uncovered. Every branch therefore fails at depth e, and each interior node has exactly three children. This single failed attempt uses

    1+3+...+3^(k-2)=(3^(k-1)-1)/2

calls to the pinned find_hit, independently of all signs. Since p=k-1, no previous budget could already have admitted another pivot. Each call costs at least one transition in an implementation carrying out that fixed search. No timing fit is used. With N=Theta(k^2 log(k+1)), this lower bound exceeds every fixed polynomial in N for this A. A variant that recognizes XORs before acquisition is a different solver and is the constructive repair below.

## Exact encoding and paid bypass

Use the same dihedral shared-choice compiler and adjacent-witness compiler as Discovery and Construction. Its modulus is r=8k+1, the least odd integer greater than c. Substitution into their formulas gives

    n0=640k^2+91k+4,  m0=1280k^2+192k+4,
    n=1920k^2+283k+11, m=2560k^2+384k+12,
    w=ceil(log2(n+1)),
    N=3n+2+2 floor(log2(m+1))+3m(w+1)+w.

The layout is unary n and delimiter, gamma(m+1), ordered signed triples, two n-bit local witnesses and release ID. Its Boolean existential decision equivalence is inherited from the pinned compiler proof. The current run does not claim new compiled-instance testing. The C/R strict counting relations are separate.

Fix B as follows. Parse the valid compatibility input, extract the candidate source using the canonical decoder, and regenerate the entire image to compare every bit. On successful extraction test exactly the displayed even-k source template, including every variable ID, every local four-row parity block, ordering, and the sign vector. Reject this shortcut as UNKNOWN on any mismatch and use exhaustive SAT decision on the retained input. On acceptance compute XOR_i s_i and return SAT precisely when it is zero. This is correct on every accepted input by the preceding equivalence and correct on every other valid input by fallback. All failed recognition is charged.

For this family, extraction, repeated indexed comparisons and exact regeneration use O(N^3) tape transitions and O(N) occupied span as in the peer's conservative compiler ledger. The source has O(k log k) bits. Template counters and addresses use O(log N) bits, and source scanning, scalar XOR, cleanup, placement and output fit that envelope. Generating the target when required also costs O(N^3), O(N) span. All original input and copies count. On the admitted same execution physical CM<=O(NT)=O(N^4). A separate self-contained replay code for each C_t uses O(N+log(T+2)) bits, giving minimum-description CM<=O(N^4). No minimum-description lower bound is obtained by reversing this estimate.

A broader constructive route is to authenticate local XOR clause blocks and apply Gaussian elimination, which is already a known polynomial affine solver. This report proves the template recognizer and scalar algorithm above; it does not claim a polynomial procedure that recognizes every possible hidden affine encoding. General fallback time remains exponential, for example O(2^n N^3) with linear span.

## Actual obligations and same-run comparison

After B pays all recognition and computation, erase the source and scratch, retain the answer in one fixed cell, and enter a common READY state with the head there. Choose s uniformly from all k-bit vectors for fixed k, so both labels have probability one half. U=answer, B_side=(fixed program, k, generator, distribution), E={the READY cache read}, Pi=its one-bit symbol, b=1,h=0,rho=1. The actual identity decoder proves one bit of suffix demand. Physical placement, addressing and the actual read were paid. If the answer is given in B_side, the entropy demand becomes zero.

For the vector of signs V, even the complete normalized suffix leaves H(V|B_side,Pi)=k-1 bits. These signs belong to the actual input, but decision correctness imposes no suffix decoder for them. Repeating the same cache read in q obligations gives rho=q. The parity decision is shared global work, and clause ordering imposes no processing-order restriction on B.

For fixed caps T<=K N^a use S=O(N^a), physical CM=O(N^(2a)), and descriptive CM=O(N^(a+1)). The exponential A execution excludes all fixed caps for that one architecture. The polynomial B execution prevents its transfer to every solver on this family. The transport permutation family's matching quadratic/cubic baseline and static N^2/8, N^3/27 ceilings remain intact. Counting circuit bounds do not provide decision consequences here.

DISJ/equality sanity PASS as a calibrated shared computation control. Simultaneous DTISP PASS with distinct A and B ledgers and actual event overlap. Deterministic configuration consistency PASS, with no state-count lower bound. Relativization, algebrization and Natural Proofs give no unrestricted conclusion here. Affine/Tseitin and shared computation are the active controls; forced-domain and all-UNSAT assumptions are excluded. Complement/renaming preserve the parameter argument. The family is retired as a candidate for compulsory superpolynomial decision work. P versus NP remains OPEN.

## Evidence, sources and receiving dependency

[Reproducer](../../../experiments/dynamic_redteam_affine_pivot_20261121.py) imports the exact find_hit from Accounting at fb25e0ddffc036b0355f12afd6983dc0f83d45ae, and independently computes components and the cycle criterion. [Raw evidence](../../../results/raw/dynamic_redteam_affine_pivot_20261121.json).

All 16 sign vectors at k=4 and two opposite-label controls at k=6 were checked. Every pivot failed at budget k-2 and some pivot succeeded at k-1. Local parity truth tables cover 16 rows. Failed full ternary trees at k=4,6,8,10 used 13,121,1093,9841 calls. This new test targets one-pivot acquisition, which did not exist in the previous Redteam cache audit. It does not repeat the old cut/cache experiments, measure TM transitions, rerun Z3 on the huge compiled images or experimentally prove asymptotics.

Fresh primary query “Schaefer 1978 complexity satisfiability problems affine Gaussian elimination pdf” found and opened the original STOC 1978 paper. Its affine case concerns conjunctions of relations represented by linear equations over GF(2), with polynomial Gaussian elimination. That hypothesis holds for the recovered parity blocks. The specific scalar cycle test and tape bounds above are proved directly.
https://www.khoury.northeastern.edu/home/lieber/courses/csg260/f06/materials/papers/max-sat/p216-schaefer.pdf

Fresh official GitHub searches '"Gaussian" "XOR"' covered anthropics, openai, xai-org, google, google-research and google-deepmind. xAI's rate limit succeeded on retry with no hits; DeepMind also had no hits. OpenAI returned Gaussian probability formalization, Google graphics code and Google Research a Gaussian grid feature file, all rejected as unrelated from the excerpts. Anthropic's cryptography-research-demo/AES/experiments/aes128-measured/common/canon_even.h at fa01c398b42bb7d94eadff75a42dfb45da484457 was inspected. It includes an eight-dimensional GF(2) elimination inside finite-field canonicalization; it supplies no general SAT claim and no code was imported. Bounded web fallback queried the same six scopes and Google OR-Tools with XOR/Gaussian/SAT. Ownership was checked with verified organization pages, xAI's official release link, Google organization guidance and research.google/resources. No ownership-dependent theorem was inferred.

Recovered current governance, skill, dynamic continuation, transport, applicable T5 definitions, Redteam's last report/handoff, peer Discovery and Construction report/code/raw, Accounting search code, and issue 324. The preceding Bounds publication in this conversation is not claimed as independently reviewed by this audit. No full checkout or manuscript build is present, so preflight/LaTeX compilation were not run. No TMR manuscript ownership is assumed.

Smallest corrected statement to Discovery, Accounting and Synthesis: one-pivot acquisition has the proved parameterized upper bound, and its fixed budget-first implementation can spend superpolynomial work on connected affine inputs that admit paid polynomial aggregation. Preserve the upper bound and add authenticated algebraic admission before this search if pursuing a broader solver.

ONE next dependency, Discovery with Construction and Redteam: specify the exact combined affine-admission/component-pivot solver, including failed recognition, and prove or falsify a polynomial bound on its remaining non-affine inputs. Bounds must establish any claimed compulsory service from actual execution, and Accounting must retain the one-bit shared suffix ledger.

Peer source: https://github.com/j15marti/pnp/blob/fb25e0ddffc036b0355f12afd6983dc0f83d45ae/research/agents/charged-discovery/PNP_Charged_discovery_2026-11-21_225300_Component_Pivot.md
