# LSPV-3/531: Topological mod-2 linking rank does not lower-bound all-rule minimum refutation work

**2026-11-09 03:35 PST | Route B (hypergraph / certificates) | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

Node **[P2-L3-531]**. Relevant obligations **[P2-D1]**, **[P2-C3]**, **[P2-B1]**, **[P2-B2]**. Both proof trackers read before this run: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, `proof2.txt` blob `fba76512d502cdf2f405a336a7fc43068f40ea50`. Tracker changes, if made, require new exact HEAD SHA and complete readback, not these initial SHAs.

## IDEA and prespecified falsifiers

**Hypothesis:** A valid source-authenticated refutation can be constant-size while a genuine ambient-isotopy invariant of the corresponding published 3SAT-to-link reduction grows arbitrarily large. Hence global link rank cannot be used directly as a universally increasing lower bound on the *minimum over all legal proof DAGs*.

The falsifiers were: (F1) the published link reduction does not preserve the original disjoint variable Hopf pairs, destroying the mod-2 rank bound; (F2) the seven-node refutation contains an illegal pivot, missing source, free premise, or omitted AND branch; (F3) any deletion of a core clause remains UNSAT after padding, destroying indispensability and the claimed exact minimum; (F4) number of variable Hopf pairs is not unbounded. A fifth qualification is explicit: if historical accepted-byte `R_mix341` does not accept an ordinary Resolution certificate, no historical byte-language statement follows.

## SEARCH, primary sources and controls

Koenig and Tsvietkova, **“NP-hard problems naturally arising in knot theory,”** *Transactions of the AMS Series B* 8 (2021), 420-441, Theorem 1, DOI https://doi.org/10.1090/btran/71. Full paper inspected at https://www.researchgate.net/publication/351932865_NP-hard_problems_naturally_arising_in_knot_theory , Section 2, pp. 421-424. Their reduction for strict signed 3-SAT on `n` variables and `m` clauses first creates `n` **disjoint Hopf links**, then adds `m` iterated-commutator clause components. Its target is an `(n+m)`-component unlink inside an `(2n+m)`-component link. The crossing upper bound is `2n+m(64n+10)`. This is a polynomial **decision reduction**, not a proof-size-preserving reduction.

Cheng, Chlopecki, Nazar, and Samperton (2025), https://arxiv.org/abs/2509.13120, prove Trivial Sublink NP-hardness from Independent Set using *only mod-2 pairwise linking*, so Brunnian/Milnor structure is not essential to that NP-hardness result. It supplies no superpolynomial proof-work lower bound.

External hard-family controls: Haken (1985), *The Intractability of Resolution*, exponential pigeonhole **ordinary Resolution** lower bounds; Urquhart (1987), *Hard examples for resolution*, JACM 34:209-219, exponential expander-Tseitin **ordinary Resolution** bounds. Neither is a bound for every historical mixed rule; algebraic, extension and shared shortcuts remain admissible. The present family is a deliberately **easy counterexample**, not an invented alleged hard family.

Repository continuity checked: `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, November 2 five-role refocus, current issue #3 comments, `proof1.txt`, `proof2.txt`, the new `research/coordination/2026-11-09_KNOT_LINK_TOPOLOGY_SAT_FIVE_ROLE_HANDOFF.md`, and historical `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`. Peer LSPV-1/531 crown-graph result, LSPV-5/456 proposed ER2 checker malformed-input defect and LSPV-5/457 affine auxiliary obstruction examined. Grok `GROKPROOF/2026-11-08_0930_PROGRESS.md` and Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` read; neither claimed the missing transfer.

Required external repositories read at pinned Git blobs: `konard/p-vs-np/README.md` `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`, `scripts/proof_status.json` `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` `18d693ea71dfa433370eb7afbebc3106e32f03e5` and `RESOLUTION_STANDARD.md` `729a9164d6aad2dc7ae49fb24127759859a60f11`. `meelgroup/frat-xor/format.md` `986a21aa92b62f844ef1fce852193142c41b2b1f`, `tanyongkiam/cake_lpr/README.md` `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`, `peitl/short-proof/README.md` `93d2090dba9739bc4983c65ea639a24e1f5e0fab`, and `openai/math/README.md` `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` also read. Project GitHub code search found the new topology handoff; lack of more hits is NOT a novelty proof. Separate Google-branded search was unavailable; general public web search was used.

## ITERATE: two exact restricted theorems

Define `H` as the **eight original proper three-literal clauses** over `x_1,x_2,x_3` with every possible choice of signs. Under any assignment exactly one is false. Define `G_k` as `k` positive proper strict 3-CNF clauses on pairwise disjoint **fresh** triples, and take `F_k=H AND G_k`, with the original eight clauses first.

Thus `n=3+3k`, `m=8+k`, and there are `24+3k` original literal occurrences.

**Theorem 531.1 (PROVED/RESTRICTED).** In every fixed sound source-authenticated conservative unit-weight refutational calculus with at most two antecedents per paid node and unit-cost ordinary Resolution,

$$
\boxed{W_R(F_k)=7\quad (k\ge 0).}
$$

*Proof of upper bound:* Resolve four pairs of original `H` clauses on `x_3`, then their four resulting clauses in two pairs on `x_2`, and the final pair on `x_1`. Seven unit-cost ordinary Resolution nodes derive the empty clause, with exactly eight original source ancestors, no free assumptions, and shared sources charged once.

*Proof of lower bound:* Removing any `H` clause leaves the unique assignment that falsifies that clause satisfying all other `H` clauses. All fresh padding variables can be TRUE, satisfying `G_k`. Thus all eight `H` source clauses are indispensable to *any* sound refutation, including those using conservative extensions. A connected acyclic ancestry DAG with eight indispensable leaves, `r` paid internal nodes and indegree at most two has at least `8+r-1` dependency edges but at most `2r`. Hence `r>=7`. The seven-node construction attains equality. This is a theorem about the declared **semantic** /341 rule-cost conditions, not authentication of its unknown full accepted-byte grammar.

**Theorem 531.2 (PROVED/RESTRICTED, link-rank barrier).** Let `L(F_k)` be the *actual Koenig-Tsvietkova Theorem 1 reduction output*. The link has

$$
\#\operatorname{components} L(F_k)=2n+m=14+7k.
$$

Its mod-2 linking matrix has a principal `2n`-by-`2n` submatrix indexed by the **variable components**, exactly the block diagonal direct sum of `n` Hopf linking matrices

$$
\begin{pmatrix}0&1\\1&0\end{pmatrix}.
$$

Adding clause components cannot change old variable-variable linking. Therefore the rank of the *whole* linking matrix satisfies

$$
\boxed{\operatorname{rank}_{\mathbb F_2}\operatorname{Lk}(L(F_k))\ge 2n=6+6k,\qquad W_R(F_k)=7.}
$$

This needs **no assumption whatsoever about clause-to-clause linking**. Pairwise linking numbers are ambient-isotopy invariants. Nevertheless, for any nondecreasing unbounded `g`, the universal claim `W_R(F)>=g(rank_F2 Lk(L(F)))` for every UNSAT proper strict 3-CNF is false: take `k` sufficiently large. This is a legitimate falsifier of one proposed topological invariant transfer, **not** a falsifier of core-minimized, instance-restricted, or all-rule-progress potentials that make additional assumptions.

**Necessary core-robustness test.** Any proposed universally valid lower-bound potential must remain bounded by `W_R(H)` under arbitrary satisfiable source padding of the fixed contradictory core `H`. Taking a minimum of a candidate quantity over UNSAT subformulas is a possible *necessary screening repair*, but is not a proved invariant or a polynomial algorithm; identifying the optimal core can itself be hard.

## Typed rule / certificate interpretation

The `3SAT -> link diagram` map is a polynomial **reduction**, not a native proof inference. Sublink selection is a **SAT-witness correspondence**, not an UNSAT refutation. Reidemeister isotopies preserve linking invariants but are **not** automatically RES, AND3, GF(2), LOCAL-CONVERT, DEF, branch discharge or cross-branch lemma application. The first unsupported arrow in an attempted all-rule lower bound is the assertion that some bound on topological invariants of the output diagram induces a **bounded change per native paid inference**. Here no topological move or oracle is inserted into the proof; the seven explicit steps are ordinary correctly oriented Resolution. Sources remain authenticated, all AND premises present, proof DAG acyclic. This rejects invalid derivation/reference interpretations without changing historical R_mix341 grammar.

## Computer controls and resource ledger

Published Node verifier `experiments/arc/lspv3_531_knot_link_rank_audit.cjs`, raw `results/raw/arc/2026-11-09_0335_LSPV3_531_KT_LINK_RANK_PADDING_RAW.json`; separately authored Python certificate constructor/checker and full SHA-bearing packets in the independently downloadable reproduction archive. Both checked `k=0,1,2,4,8,16,32,64`: Node **152** assertion checks; Python **138** plus **six rejected malicious proof mutations** (wrong oriented pivot, foreign source, missing AND premise, forward reference, duplicate line ID, zero pivot). Original H clause deletion has an explicit SAT extension for each of eight choices. The Python checker also exhaustively verified each of the eight three-variable assignments falsifies exactly one H clause. Independently replayed algebraic GF(2) ranks use **only the exact Hopf principal matrix** specified by the published construction. They do **not** constitute an actual link diagram generator or verifier, an official CakeML run, or a historical native R_mix341 checker execution.

At `k=64`, the original strict 3-CNF has `195` variables and `72` clauses; its published link has `462` components and full mod-2 linking rank at least `390`, while the minimum logical proof cost is `7`. The explicit proof has 7 derived nodes, 14 antecedent references, 8 source ancestors, and ideal unlimited-parallel critical-path span 3. The source requires `Theta(k log(k+2))` ordinary indexed encoding bits. Proof ID references are `O(log(k+2))` bits each. The actual input parsing and source-authentication verifier must pay its own complete parsing/read costs, potential malformed-input rejection, materialization, references, storage, verification and output; optimal logical work is NOT constant physical SAT time. The topological diagram has the published **upper** bound `2n+m(64n+10)=O(k^2)` crossings; it is not a runtime lower bound. The Python host run took ~0.002s with ~93.8 MiB process RSS including interpreter. No SAT search/solver discovery time was hidden in the ideal logical minimum: this construction is explicit by definition.

**Established-hard-family/transfer ledger:** Haken PHP and Urquhart expander Tseitin (ordinary Resolution exponentially hard, other mixed shortcuts may be short); prior project modulo-3 one-hot Tseitin (separately sourced fixed-degree lower bounds and flat-CNF representation barriers). The chosen `F_k` is not hard and is used **only** as a tight negative control. No 3-CNF reduction is asserted to preserve any published proof-size lower bound, and NP-hardness of link selection supplies no arbitrary-machine SAT hardness.

## Status / handoff

Material evidence **[P2-L3-531]** negates an unqualified universal raw topological-rank lower-bound candidate. Native historical byte grammar **[P2-D1]**, mixed proof normalization **[P2-C3]**, all-rule superpolynomial worst-case minimum **[P2-B1]**, and noncircular same-R B3 **[P2-B2]** remain **OPEN**. Lead and red team should test any core-aware repair against algebraic/extension reconvergence; Route A should not infer same-machine all-input contraction. Root `main.tex` not edited. No historical weights/rules, other agents' regions, titles, schedules, enabled states or 2A/3B allocation changed. **P versus NP OPEN.**
