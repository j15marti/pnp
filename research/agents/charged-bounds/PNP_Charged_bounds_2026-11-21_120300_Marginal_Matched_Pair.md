# Bounds: marginal-matched positive counts still expose input correlation
2026-11-21 12:03 PST, America/Los_Angeles.

**T5-MARGINAL-MATCHING-PAIR1: PROVED/EXACT distributional falsifier on the published positive-offset image; external independent review pending.** For every p>=2 the explicit pair below has one conditional Shannon AND average-min entropy bit, the same output marginal as the true count, and only positive counts above the shifted baseline, all divisible by the full multiplier. Nevertheless an input-aware circuit of at most12N+3 gates distinguishes with advantage exactly1/2. The T5 embedding uses Construction's pinned reduction theorem, not a newly independent certification of its gadgets.

**FALSIFIED/RETIRED:** this particular marginal-resampling candidate as a cap-sized indistinguishable pair. No general impossibility of T5 pseudoentropy is proved. This is a new correlation test after the zero/baseline/residue controls, not a repeat of those tests. **COMPUTATIONAL:** seven generated pairs p2..8, 28 joint circuit evaluations, and all four predicates on each two-value output support checked exactly.

ONE next dependency: **T5-SAT-SLICE-JOINT1**, Bounds owner, Redteam review/Synthesis tracking. Supply a specified SAT-supported source/fake pair with one conditional bit and an independent argument against input-aware count prediction at the claimed budget, or a new small correlation falsifier. Matching any number of output-only statistics is insufficient.

## Exact model, quantifiers and falsifiers

Fix a total correct deterministic strict-C counter A and constants K>0,a>=1 independent of its input. The proposed cap is T_A(N)<=K N^a on the handoff's fixed-alphabet sole-tape model, with input/work/output, head/control, retained addresses and physical travel charged. This run refutes a pseudoentropy premise, not A or its cap.

F_N maps valid N-bit strict-C instances to their exact integer counts, padded to ell=3N bits. Circuits use fan-in-two AND/OR, unary NOT, constants and unrestricted sharing/fanout; noninput gates are counted. Behavior outside the promised input distribution is arbitrary. For each p>=2 define N=N_p and the joint pair explicitly below. The claimed indistinguishability fails for EVERY B>=12N+3 and epsilon<1/2. Other input lengths can be left outside this ensemble; no padding argument is used.

C consists of all permutations of012,123,234,340,401 over Z5,30 tuples. Every clause has distinct variable names and full initial domains. R is the separate40-tuple ordered tournament relation, whose first argument wins once and loses once with i beating i+1,i+3. No C/R conversion or historical S/Q substitution occurs.
Use exactly
N=n+2+2 floor(log2(m+1))+3m ceil(log2(n+1)),
for unary n, gamma(m+1) and one-based fixed-width triple IDs. Do not replace N by p.

Four falsifiers:
1. The two generated target encodings differ in n,m,N or multiplier, are invalid, or have equal counts.
2. The fake does not have the true output marginal or one bit of BOTH stated conditional entropies.
3. The actual Boolean circuit uses hidden source answers, more than12N+3 gates, or fails on one of the four supported joint pairs.
4. Its distributional success is extended to arbitrary T5 inputs, or its sampler/generator is treated as free physical work for A.

## Authentic positive source and exact count pair

Use the compiler and occurrence splitter from Construction [1], commit16db13effd093c0df7ce104b3c117ec570be7c7c:
Z(B^+_H)=M(2^p+#CircuitSAT(H)),
M=10*2^E,
E=54+14b+13o+3t,
n=285+74b+67o+15t,
m=347+90b+83o+19t.
This source theorem includes unit-fiber Boolean domains, full strict-C clauses, known twofold equality-link multiplicities and occurrence<=5. Its proof and original generator/raw were recovered. The source theorem's review status is preserved.

Define H_0 on p inputs as the one gate OR(x_0,x_0), and H_1 as OR(x_0,x_1), with that gate as output. Unused inputs remain declared. Both source circuits are SAT, share p,o=1,t=0,b=p+1, and have
z_0=2^(p-1), z_1=3*2^(p-2).
For H_0 exactly half the assignments accept; for H_1 exactly three of the four assignments to its two used inputs accept. Free inputs multiply these counts. The generator permits repeated OR inputs, occurring in separate strict clauses.

Let x_j be the actual encoded B^+_(H_j). Then
E=81+14p, n=426+74p, m=520+90p,
y_0=F_N(x_0)=6M*2^(p-2),
y_1=F_N(x_1)=7M*2^(p-2).
These are unequal, so x_0!=x_1. They are both greater than the shifted baseline M2^p and divisible by the full M. Their bit lengths are at most E+p+5<n, so they lie in0..5^n without truncation or wrapping. In fact each fake value is realized by another input of the very same family and same N.

Sample J and L independently as fair bits. Set
X=x_J, Y=y_J, Ytilde=y_L.
This is an explicit sampler, not conditioning an unspecified distribution on SAT. Both target inputs are SAT, and even the underlying source circuits are SAT.

For each x_j, Ytilde is uniform over two distinct integers. Thus H(Ytilde|X)=1 and Hbar_inf(Ytilde|X)=1, with average conditional guessing probability1/2. Y is deterministic given X and has both conditional entropies zero. Unconditionally Y and Ytilde have the EXACT same law: uniform on{y_0,y_1}. Consequently every output-only test, even unbounded or randomized, has zero advantage. This includes equality to zero, the shifted baseline or either actual output; multiplier/residue/range tests; and all combinations of output statistics.

## Explicit joint distinguisher and budget proof

Generate the two encodings and let i be their first differing bit. Set s(x)=x_i if (x_0[i],x_1[i])=(0,1), otherwise s(x)=NOT x_i. Then s(x_j)=j. This uses at most one NOT gate and no count oracle.

For ell-bit z, let E_j(z)=[z=y_j]. Negate at most ell positions then AND the ell literals, using at most2ell-1 gates. Define
D(x,z)=(NOT s(x) AND E_0(z)) OR (s(x) AND E_1(z)).
The selector, its negation, two ANDs and one OR add at most five gates, for total
2(2ell-1)+5=4ell+3=12N+3.

On the true pair D accepts always. On the fake pair it accepts exactly when J=L, probability1/2. Hence Adv_B>=1/2. The total variation distance of these two joint laws is also1/2 (diagonal masses1/2 versus four masses1/4), so this advantage is optimal even for unbounded tests. This is a direct calculation, not an inferred counting lower bound.

The hardwired constants are generated by the displayed closed formulas, and the selector position by generating/comparing two explicit encodings. There is no nonuniform oracle for hard counts. A polynomial-time circuit generator indexed by p suffices; indexed by N it may search p<=N and compare the monotone length formula, with arbitrary output on other lengths. This is polynomial uniformity, not a DLOGTIME-uniformity claim. Circuit wires charge size in the declared standard model; physical discovery and access are accounted separately below.

At p2: n574,m700,E109,N21594, y_0=60*2^109, y_1=70*2^109. First differing bit is14937 using zero-based indexing. The emitted circuit has259124 gates, below259131. Both supported targets have SAT label; this yields no decision separation.

The familiar exact-solver comparator implication remains CONDITIONAL: an independently proved (B,epsilon) pair with average-min entropy>=1 and epsilon<1/2 would exclude exact count circuits fitting B minus comparator overhead. This explicit candidate cannot supply that premise, already failing at linear B. No fixed polynomial exponent is defeated.

## Reproducible evidence and distinction from prior tests

Run Python3 with assertions enabled:
```
python experiments/t5_bounds_marginal_pair1_20261121.py > results/raw/t5_bounds_marginal_pair1_20261121.json
```
Code SHA256 eb01ccb667fa7d7d75ef26a466794772cd58001728b5509bb5910ff49d974ee3.
Dependency experiments/t5_construction_positive_offset1_20261121.py at [1], SHA2566cd122e55ab7150dff6c8a1a22099ec5b44b195395c9f83670965773417accdb; the runner verifies bytes before import. This is integrity checking, never a semantic merge proof.

For p2..8 the runner counts the small source truth tables, generates both complete split clause lists and bit encodings, roundtrips them, finds an actual differing bit, emits AND/OR/NOT gates and evaluates all four supported pairs. It checks full multiplier/alphabet/baseline conditions and all four Boolean output-only predicates. Raw contains exact integers, encoding digests, selectors, gate counts and acceptance matrices. No randomness, external packages or floating entropy estimates.

Expanded split T5 counts use the published equality/gate theorem; the exponentially many orientation assignments are NOT enumerated anew. The prior294 generic T5 counts and8160 fake-value experiment are recovered evidence, not rerun. The new test verifies the previously untested joint-correlation circuit against actual encoded sources. Dependency reuse and same-session authorship are not external independent review.

## Complete charged resource ledger

Let U=N+p+2. A repeated-scan implementation can generate the two source circuits, strict-C clauses, split images, count constants, and differing position in conservative O(U^4) sole-tape time and O(U) span, as in the source compiler. This includes parsing, validation, ID maps, actual accesses, addresses, output and all carries. No discovery lower bound is claimed. A serialized O(N)-gate circuit additionally uses O(N log N) bits for wire IDs; it is not an O(N)-bit physical object.

The source/fake sampler chooses two fair bits and emits an N-bit source and3N-bit padded answer after paid construction. A source bit read at a fixed circuit input is a wire; a tape evaluator pays travel to it. Once constants/position are prepared, comparing the padded answer needs a sequential scan; retaining input, constants, counters and output requires O(N) span. A conservative O(U^2) comparison implementation suffices, separately from generation. These are executions of the generator/test, never a time-space bound for A.

All actual failed candidate searches, source authentication, representation changes, adaptive switches, queries, rereads, retained caches, recomputation and answer emission belong to the deployed algorithm's actual work. Shared computations count once. A solver recognizing this two-input promise on arbitrary data must verify the promise or use a correct fallback. D need not recognize it: a distinguisher is defined on all bitstrings but only its distributional acceptance matters. No virtual residual service, forced original-cut revisit, or trusted hash merge is introduced.

For the SAME A,N,K,a under its hypothetical cap:
S=O(N^a); physical CM=O(N^(2a)); minimum-description CM=O(N^(a+1)); count-map circuits O_A(N^a log N).
These bounds are not summed, multiplied or replaced by the test's costs. Neither padding across p nor large output integers exclude all polynomial exponents.

Controls: affine/Tseitin, private-leaf trees and matching retain legal scalar algorithms; no witness-representation theorem is used. Forced domains and Boolean auxiliaries are covered only by the pinned reduction correspondence. Renaming changes the selector's physical position but a known renamed pair can be regenerated; no universal cheap isomorphism recognition is presumed. Complement changes counts and requires a new pair calculation. Relocation changes tape access costs but not the joint law. Full-state H(Y|C_t)=0 is retained. SAT/UNSAT/UNKNOWN remain distinct; decision-witness packing is not inferred from the count. This easy family is retained as a control, never labeled hard.

DISJ: NOT APPLICABLE, no communication demand. Relativization: no nonrelativizing step, unrestricted route OPEN. Simultaneous DTISP: PASS for separate executions, compulsory violation OPEN. Deterministic configurations: PASS for scope, no state-count lower bound. Natural Proofs/algebrization: no unrestricted circuit lower bound or claimed barrier bypass.

## Recovery and fresh source searches

Base899d207c4f94559db08d730d588de99bce3b055b. Required current sources fetched: baselinea886f3387a8676b9cc86afbf3bebf22630109d49 (141084 bytes, SHA256c9a3a0f362c72dfad7548b0cd44723853f105dcdc6a4f9ea5fef4559d3bb2a33), assignment776c2622d69dbcbb1c7c0d1361f299970fb7f1cc, AGENTS01f05d238736da1a3a2a10c9586be3d882751212, CODEX15639f62a254aa9cd36a949b9f9d81985e5ed538, research instructions6f37fc1a1713b01abd91794d5523fb05a57efa2f. Complete source content recovered, including appended programs; unchanged portions retain the prior continuous-session reading. Retrieval is not independent certification. Own latest report [2], full handoff82d7e405b71c561827bd4d60c3bee9327fc86585, Construction proof/code/raw and issue324 through7068375874 recovered. Discovery's extremal-closure result is not a premise.

Fresh literature query “Vadhan Zheng conditional pseudoentropy joint distribution marginal indistinguishability.” The STOC PDF endpoint timed out; alternate author-hosted March8,2013 full version succeeded [3]. Read Definition1.2 and Theorem1.3 qualifications: indistinguishability is of JOINT pairs with the same X, and the stated sampling characterization assumes polynomial alphabet. The general T5 count range is exponentially large. No sampling-hardness equivalence is imported. The finite joint-law and gate arguments above are direct proofs.

Fresh connected GitHub query “pseudoentropy marginal joint distribution” under anthropics,openai,xai-org,google,google-research,google-deepmind: five returned no matches; Google initially429; one retry returned no matches. Web fallback was also performed. Fresh web queries were site:github.com/anthropics pseudoentropy; site:github.com/openai conditional entropy; site:github.com/xai-org entropy; and each of google,google-research,google-deepmind with “pseudoentropy conditional distribution.” Results included OpenAI math Gaussian-information snippets and RL entropy code, Google Research mixture/DP-sampling snippets, and DeepMind policy entropy/diffusion code. None supplied a T5 joint-indistinguishability theorem. No external repository code was imported or built; no inspected commit is claimed for snippet-only screens. No applicable Anthropic/xAI theorem surfaced. These are bounded relevance searches, not exhaustive absence claims.

Official ownership is based on corporate domain/cross-link verification recovered from earlier continuous-session checks: github.com/anthropics, github.com/openai, x.ai/open-source, developers.google.com/optimization, research.google and deepmind.google corporate repository links. Search results using similar product names are not accepted as official. Prior logs avoided repeating unrelated deep reviews.

Repository query “marginal matching pseudoentropy” found [2] and the baseline, not this completed specific pair. No exhaustive draft-branch novelty claim. No checkout exists; preflight, LaTeX compilation and formal kernel builds were not run. Only Bounds report/handoff and new code/raw are published. No peer/TMR/schedule changes.

[1] [Construction positive-offset pair,16db13e](https://github.com/j15marti/pnp/blob/16db13effd093c0df7ce104b3c117ec570be7c7c/research/agents/charged-construction/PNP_Charged_construction_2026-11-21_113200_Positive_Offset_Pair.md).
[2] [Bounds zero-atom report,15d61b2](https://github.com/j15marti/pnp/blob/15d61b216e5741297b178ddaba6904be14c55806/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-21_105900_Zero_Atom_Minentropy.md).
[3] [Vadhan–Zheng, Characterizing Pseudoentropy, March8,2013, ECCC revision3](https://salil.seas.harvard.edu/sites/g/files/omnuum4266/files/salil/files/eccc2013.pdf).

Redteam/Synthesis: independently check source-count fibers, one actual encoded selector bit, joint versus marginal laws, and gate accounting. The smallest supported correction is that exact marginal matching eliminates output-only distinguishers but says nothing about input-aware indistinguishability. Same-session implementation is not independent external review. Next dependency is T5-SAT-SLICE-JOINT1 above. **P versus NP remains OPEN.**
