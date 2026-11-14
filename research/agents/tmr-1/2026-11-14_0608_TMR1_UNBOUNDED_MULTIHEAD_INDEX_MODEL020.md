# TMR-1/020: unbounded-coordinate, multihead delayed-INDEX locality

**Date:** November 14, 2026, 06:08 PST (America/Los_Angeles). **Role:** TMR-1 Machine Model Lead. **New claim:** TMR1-UM20 CANDIDATE/RESTRICTED pending TMR-3/TMR-5 peer review. **Finite evidence:** COMPUTATIONAL. **P versus NP:** OPEN.

## 1. Exact machine and quantifiers

Fix ONE finite total deterministic uniform machine A across ALL lengths. It has r >= 1 fixed read-only heads on independent identical copies of the same length-L binary source, w >= 0 fixed locally moving writable work tapes, q fixed control states, and work alphabet size at most g >= 2. On each source tape, bits occupy positions 1,...,L; left/right endmarkers are at 0 and L+1; other positions carry a fixed blank symbol. **Source heads may park at arbitrary integer coordinates outside both endmarkers.** All heads move at most one cell per counted transition. Transitions may inspect scanned symbols but receive no free numerical head coordinates, collisions between source heads, clock, or address oracle. In particular independent read-only copies make head-to-head collision sensing unavailable.

A first preprocesses source x with no query index. Only after this phase an independent, charged read-only query channel supplies p in {1,...,L}; its initial head position and contents are determined by p, not by x except through paid preprocessing state. A must return exactly x_p for EVERY (x,p), and it must halt. No observable preprocessing-clock side channel, uncharged output memory, or advice is allowed. Input rereads, indices, all work buffers, head moves, recomputation, output and other physical transitions are counted. This INDEX query contract is optional and NOT imposed on any 3-SAT decider.

Let s=s_A(L) bound the total **visited writable work cells** at the phase boundary for every source of length L. Let t=t_A(L) bound the total query-phase transitions for every pair (x,p). The complete retained-work configurations number at most

$$
M_A(s)=q(2s+3)^{3w}g^s.
$$

This conservative overcount includes all work-head coordinates, visited intervals, symbols and control. Preprocessing time is unrestricted in this two-phase lemma, but must be paid in any end-to-end algorithm. The separate user-requested SAT target still concerns the actual encoded bit length L, all valid formulas, one fixed A across all lengths, and arbitrary polynomial work space.

## 2. New theorem TMR1-UM20

For the exact locally moving, nonsensing, unbounded-input-coordinate model just specified,

$$
\boxed{2^L\le M_A(s)(L+2t+4)^r 2^{r(2t+1)}.}
\tag{UM20}
$$

For fixed r,w,q,g, if s_A(L)=o(L), then

$$
\boxed{t_A(L)\ge \bigl(1/(2r)-o(1)\bigr)L.}
$$

**Proof.** For each parked source-head position u define its t-local positional type. Positions -t through L+1+t keep their exact coordinates. All positions below -t share one FAR-LEFT type; all positions above L+1+t share one FAR-RIGHT type. There are at most L+2t+4 such types. Two source-head positions sharing a far type have identical read-only blank observations along ANY sequence of at most t unit moves. For equal near types, the endmarkers and outside blanks are at matching coordinates. Source bits physically observable in t transitions from one head occupy at most 2t+1 addresses.

Encode every length-L source x by its complete retained work configuration after preprocessing, all r head local types, and the source-bit values in the union of the radius-t neighborhoods around the parked heads. That union is determined by the head types. The number of possible encodings is no greater than the right side of UM20.

If distinct x and y had identical encodings, take any identical delayed query p. Their work states and query-channel initialization match. By induction over the first t transitions, every near source head reads identical source bits/endmarkers/blanks, and every far source head reads blank symbols only. Thus all scanned-symbol tuples, chosen head moves, writes, finite-control states, outputs and terminal transitions agree on x and y. For p with x_p not equal to y_p, their correct outputs must differ, contradiction. The encoding is injective and UM20 follows. If t>=L the asymptotic claim is immediate; otherwise log(L+2t+4)=O(log L) and log M_A(s)=s log g+O_A(log(s+2))=o(L), so 2rt>=L-o(L). The theorem rests on direct physical current-cell indistinguishability, not an unproved communication-to-SAT reduction. **Proof submitted for independent review.**

## 3. Independent TMR-5/017 audit and repair

Original peer: [TMR-5/017](https://github.com/j15marti/pnp/blob/main/research/agents/tmr-5/2026-11-14_0549_TMR5_UNRESET_INDEX_WINDOW_REDTEAM017.md), which allows ONE input head parked at any **clamped** coordinate u in {0,...,L+1}. Its delayed-INDEX bound is

$$
2^L\le(L+2)M_A(s)2^{2t+1}.
$$

I independently checked the exact all-query injectivity argument and source-locality proof at this restricted model. For an input head permitted to park outside the endmarkers, the raw factor L+2 no longer counts possible exact coordinates, which may be unbounded. UM20 repairs that missing broader-model bridge by quotienting coordinates according to t-step observable type, yielding the factor L+2t+4. This is NOT a refutation of TMR-5/017 as actually stated, only a precisely scoped extension. When r=1 and endmarkers are hard stops, the peer's sharper count remains valid.

For r heads, up to r(2t+1) source bits can lie in their union of reachable windows. Information gained from a position outside those windows would require paid movement or genuine saved writable state. A physically accessible raw head-coordinate oracle or free head-collision sensor changes the model and is NOT silently included.

## 4. Sharpness, falsifiers, and unrestricted SAT gap

A fixed uniform preprocessor can scan length L and park r independently moving source heads near the centers of r equal consecutive blocks, charging all work, with O_r(log(L+2)) retained writable cells. After receiving a delayed p, choose its nearest head and move it to p. Maximum **source-head travel** is L/(2r)+O_r(1), demonstrating the geometric constant is sharp at the movement level. Binary index decoding, counters, initial positioning and output take extra paid transitions; no exact matching total-time leading constant is asserted. A conservative standard-tape upper bound is O_r(L polylog(L+2)) for preprocessing and per query with O_r(log L) workspace. Complete caching of Θ(L) bits escapes the s=o(L) premise. Arbitrary algebraic, Horn, 2-SAT, affine/XOR Gaussian, bounded-treewidth, product, sharing, renaming, padding, auxiliary-variable and recomputation strategies are compatible with the model but are NOT forced to implement delayed INDEX.

No 3-SAT correct uniform decider must accept externally delayed indices or respect sublinear retained workspace. Neither communication lower bounds nor source-input query requirements imply a superpolynomial SAT processing time without an all-machine reduction. The target

$$
\forall A\,\forall k\in\mathbb Z_{\ge1}\,\forall C>0\,\forall L_0\,
\exists F\text{ valid}: |F|\ge L_0,\quad
T_A(F)>C(|F|+1)^k
$$

remains OPEN. On the SAME standard machine S_A(F)<=O_A(T_A(F)+1), but this does not transform a sublinear-space INDEX theorem into an exclusion of all polynomial-space/polynomial-time SAT machines. One fixed general polynomial decider would instead prove P=NP; none is established here.

## 5. Reproducible hostile controls

**Actually executed natively in CPython** in 1.30 seconds (not a wrapper). Published source: [tmr1_unbounded_multihead_probe020.py](https://github.com/j15marti/pnp/blob/main/experiments/tmr/tmr1_unbounded_multihead_probe020.py), exact executed Git blob f62c907f2650b7b8e059d89493ec24fd0803b878. Raw stdout: [TMR1/020 raw JSON](https://github.com/j15marti/pnp/blob/main/results/raw/tmr/2026-11-14_0608_TMR1_UNBOUNDED_MULTIHEAD020_RAW.json), exact Git blob 137d49aae262df7d3dd647d5d30010fb3056c581.

2,880 finite combinations with lengths 1 to 10, r in {1,2,3}, retained synthetic sketches 0/1/2 bits, access radii 0 to 3 and four source-head parking patterns. All 208 mathematically forced collision cases yielded witnesses; 1,904 opposite-bit collisions matched adaptive probe traces using actual current-cell reads, including 660 collisions in deliberately input-encoded far-away source-head positions. Thirty centered-placement geometry checks passed. **Zero assertion failures.** Synthetic preprocessing and Python arithmetic are not a fully charged physical Turing-machine compiler; over-permissive parking policies are explicitly hostile mathematical controls. Finite evidence is COMPUTATIONAL, not an asymptotic proof.

## 6. Corpus, literature and disposition

Authoritative 2026-11-13 12:49 PST five-TMR replacement directive read first and rechecked, unchanged blob 47459817e66dccf1f3079e6c724c0fd2643e7bc4. Complete root proof1.txt read, 28,714 characters, blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343. Complete nonempty proof2.txt recovered via authentic Git blob 930c5eeddafce656717f28055a7a9a755f44737c, 1,051,196 characters. Complete main.tex recovered via Git blob f0054c990e11602b4b60ead3bccffa73f11d0d7b, 2,536,131 characters. Also read AGENTS.md, CODEX.md, repository skill, issue #3 through TMR-5/017, all five latest TMR handoffs, original TMR-5/017 source/raw and TMR-3/018, TMR-1/019, TMR-2/019, TMR-4/020; TMR-3/017, TMR-1/012, TMR-5/014 and original historical LSPV-4/149 model firewall. Superseded LSPV ownership is not reinstated. No original checker path is erased.

Verified primary-scoped references: Miltersen, Nisan, Safra and Wigderson, *On Data Structures and Asymmetric Communication Complexity*, JCSS 57(1) (1998), https://doi.org/10.1006/jcss.1998.1577 (cell-probe/communication scope); Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6) (2005), https://doi.org/10.1145/1101821.1101822 (restricted polynomial exponents and small space, NOT separation); Borodin and Cook, *A Time-Space Tradeoff for Sorting on a General Sequential Model of Computation*, SIAM J. Comput. 11(2) (1982), https://doi.org/10.1137/0211022 (sorting scope). UM20 is independently proved symbolically in this report rather than inherited as one of these sources.

**TRACKERS REVIEWED; NO MATERIAL CHANGE** to proof1.txt/proof2.txt. Root main.tex preserved for TMR-5 whole-document synthesis. No schedules created, revived or modified. **Next:** TMR-3/TMR-5 independently audit t-local equivalence for far source heads, multihead union encoding and exact workspace accounting; TMR-2 attempt a legitimate SAT-semantic bridge; TMR-4 preserve every paid source step in an actual-machine abstraction. No unconditional superpolynomial 3-SAT lower bound is established.

END_OF_REPORT::TMR-1::020::2026-11-14_0608_PST
