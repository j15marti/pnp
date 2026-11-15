# TMR-5/049: exact-count collision defeats a pointwise compression census transfer

**2026-11-15 13:48 PST | TMR-5, PNP Machine Bottleneck Redteam | Tracks A/C.**
**Status:** PROVED/EXACT for the model-scoped symbolic constructions and counts (independent mathematical peer review OPEN); COMPUTATIONAL for finite hosted-V8 tests; no circuit lower bound or P-versus-NP separation. Current governing directive: research/coordination/2026-11-15_SAT_COMPRESSION_CIRCUITS_FIVE_AGENT_REFOCUS.md, main blob 7b8804dc7587abc5134055b5b0d16a143055ca5a.

## Candidate and four precommitted falsifiers

**Candidate audited:** TMR-1/052 obtains at least 2^(g/32) distinct n-input functions from live, shared, g-gate minterm-trie circuits, and shows that some cannot have pointwise existential width-three CNF projections with V=o(g^(1/3)) variables. Can that particular census transfer to a lower bound on *total-count-preserving* width-three compression, or furnish an obstruction to the pinned October 2026 exact-#SAT algorithm?

Falsifiers: (F1) all many pairwise distinct functions might have exactly the same satisfying-assignment count; (F2) a single short count-equivalent CNF might represent them all, even with original input variables and unique auxiliary extensions; (F3) universal short count-equivalent normal forms might exist but require exponentially expensive construction; (F4) counting/formula size must not be converted into same-machine time, general circuit lower bounds or an NP hierarchy contradiction.

**Verdict:** F1, F2 and F3 occur explicitly. TMR-1/052's pointwise existential-projection theorem survives at its exact stated scope. An attempt to transfer its counting-of-*functions* lower bound to the scalar #SAT count **FAILS**.

## Theorem A: one exponentially large function-census fiber has a common tiny exact-count CNF

For k>=2, r=2^k and n>=k, take each S subseteq {0,1}^k with |S|=r/2. The original TMR-1/052 family is

    f_S(x_1,...,x_n)
      = [x_{k+1}=...=x_n=1] AND [(x_1,...,x_k) belongs to S].

There are binom(r,r/2) pairwise different f_S, all computable by the original shared minterm-trie using at most 3r+n genuinely live gates. For r>=8, binom(r,r/2)>=2^r/(r+1)>=2^(r/2). TMR-1 selected g with r>g/16, so its census fiber can have at least 2^(g/32) distinct **input functions**.

But for EVERY S, the exact number of satisfying n-bit inputs is

    #f_S = |S| = r/2 = 2^(k-1),

because the suffix is fixed to all ones and each selected k-bit prefix gives one assignment. Consider a SINGLE CNF, independent of S:

    H_(n,k)(x) = x_k AND x_(k+1) AND ... AND x_n.

Its first k-1 variables are free, so #H_(n,k)=2^(k-1)=#f_S. It is width-at-most-three with n named original inputs and n-k+1 clauses, but intentionally does NOT agree with f_S at each input x.

For a literal **strict proper exactly-three CNF with all original variables occurring and exactly one auxiliary extension for each x satisfying H**, add a copy y_i<->x_i for i<k (two binary functional clauses per i), three pinned zero bits a,b,c forced by the seven three-distinct-variable clauses excluding the seven nonzero assignments, and pad each unit with (a,b), each binary with a. This creates exactly

    V = n+(k-1)+3 = n+k+2,
    m = (n-k+1)+2(k-1)+7 = n+k+6

declared variables and distinct three-literal clauses, and exactly 2^(k-1) satisfying full assignments. The pin and copy records are uniquely determined for every x. For n>=k, both V and m are O(n); for the original g=n^4 regime, k=Theta(log n). Source parsing/grammar authentication can be polynomial in the actual circuit encoding, but the conclusion concerns only this explicitly recognized family, NOT arbitrary circuits.

**Important distinction:** The TMR-1 counting proof remains CORRECT for pointwise existential projection because the f_S are different functions; the same f_S are indistinguishable under **scalar exact counting**. No operation here claims to recover S or the pointwise output from H.

## Theorem B: a universal O(n)-variable exact-count normal form exists, but not a fast compiler

For every integer n>=1 and K with 0<=K<=2^n, there is a duplicate-free proper width-exactly-three CNF C_(n,K) satisfying the Anthropic-formalization-style *syntactic* gates (every declared variable occurs, m>=2, n_CNF>=4), with

    V(C_(n,K)) <= 2n+3,
    m(C_(n,K)) <= 3n+7,
    #C_(n,K) = K.

Construction. Number x as an n-bit unsigned integer, x_1 least significant. For K=0, impose both x_1 and NOT x_1. For K=2^n, impose no condition. Otherwise let j be the least significant position where K has a 1 (0-based). Start L_j = NOT x_(j+1). For i=j+1,...,n-1 define, in order,

    L_i = (NOT x_(i+1)) AND L_(i-1), if K_i=0;
    L_i = (NOT x_(i+1)) OR  L_(i-1), if K_i=1.

This is the exact comparison of the low i+1 bits of x against the low i+1 bits of K, by induction on the most significant processed bit. Demand final L_(n-1)=1. Each new binary AND/OR gate has exactly THREE functional Tseitin clauses, determines its output uniquely and uses one fresh auxiliary variable. Every x with x<K has one satisfying extension; x>=K has none. The resulting count is K.

To satisfy AllOccur without changing the count, attach a unique functional copy y_i<->x_i for every original x_i not mentioned in any previous comparator clause, using two binary clauses and one fresh variable. Add the same three uniquely-zero pins a,b,c, pad all one/two-literal clauses to exact proper ternary width and add seven pin clauses. No source variables are repeated in a clause; the new gate records are unique and each clause is distinct. In the nontrivial K case, writing j for the initial set-bit index, the ledger is

    comparator gates = n-j-1; copy gates = j;
    V = n+(n-j-1)+j+3 = 2n+2;
    m = 3(n-j-1)+1+2j+7 = 3n-j+5.

For K=0, V=2n+2 and m=2n+7; for K=2^n, V=2n+3 and m=2n+7. The asserted uniform bounds follow. Each successful full assignment has the unique auxiliary extension, with all pin values zero.

Now any n-input AND/OR/NOT shared circuit C with g gates has an exact total count K(C) in [0,2^n]. An *unbounded-construction-time* mapping C -> C_(n,K(C)) therefore compresses EVERY scalar count into O(n) variables and O(n) clauses. A **uniform total** implementation can enumerate every one of 2^n assignments, evaluate each actual shared gate once per assignment, accumulate the n+1-bit exact K and write the canonical formula. For encoded input length N, one conservative fixed-multitape implementation has

    T_count = O(2^n (N+n)^3),   S_count = O(N+n),

using sequential rescanning rather than uncharged random-access words, plus O(n log n) output-bit generation. Even if a subsequent trusted fixed-width #SAT solver runs in 2^o(n) on the compressed CNF, the SAME sequential execution has total time O(2^n poly(N+n))+2^o(n), not 2^o(n) or polynomial in the original n. Space for the composed machine must also include the original gate store, counter, output and solver peak; no forbidden DTISP pair is obtained. No exact #SAT algorithm has been assumed for the construction.

**Information ledger:** An n-input function has just one total-count value in a set of size 2^n+1, at most n+1 bits to name. Thus a census of 2^Omega(g) *different functions* by itself cannot imply 2^Omega(g) distinct exact counts when g>>n. Conversely a short scalar description does not make computing that scalar cheap.

## Independent executable verification and scope

Self-contained published ECMAScript source: experiments/tmr/tmr5_scalar_countcollapse049.js (revision tmr5_scalar_countcollapse049_v1, seed NONE). It was executed as a hosted V8 function before publication; standalone Node, Lean rebuild, full repository test suite and physical TM replay were NOT run. Immutable structured output: results/raw/tmr/2026-11-15_1348_TMR5_COUNT_COLLAPSE049_V8_RAW.json.

- 261 complete C_(n,K) instances for n=1,...,7 and ALL 0<=K<=2^n. Checked exact proper ternary width, nonduplication, all variables occurring, V and m budgets, every original-input extension, unique gate/pin flips, and full auxiliary truth-table enumeration at n<=3.
- 6, 70 and 96 distinct S choices for k=2,3,4 respectively, each checked against every original input and the SAME independent shortcut count. These 172 cases are finite checks, not the all-k proof.
- **119,967 assertions**, 3,008 exhaustive full auxiliary assignments, 95,939 uniqueness-bit-flip tests, **zero failures**. Finite status COMPUTATIONAL; the exact symbolic induction and counting arguments are distinct.

The original TMR-1/052 report/source and TMR-2/052 unique-selector construction were compared, not overwritten; TMR-4/052's switch-product OBDD theorem and TMR-5/048's bilinear exact counting remain valid restricted controls. No prior project report was located making the exact TMR-1/052 **count-collision + all-occurrence proper-3CNF normalizer** comparison. Historical /341 remains FAIL as a complete logical UNSAT authority and /386 remains RESTRICTED.

## Mandatory four-gate table

| Gate | Verdict | Exact reason |
| --- | --- | --- |
| DISJ sanity | **PASS (restricted); FAIL for the proposed static-to-general transfer** | DISJ_k has rank 2^k and O(k) circuit/2-CNF, so it is a legal easy control. This report derives no generic circuit hardness and constructs further cheap scalar-count paths. |
| Relativization, algebrization, Natural Proofs | **PASS (restricted); OPEN for any unrestricted separator** | These are elementary syntactic and counting identities and make no P-vs-NP claim. Any future claimed universal lower-bound bridge must locate a nonrelativizing step; Baker-Gill-Solovay prevents full relativization, with other barriers separately audited. |
| Simultaneous DTISP | **PASS for the explicit normalizer resource upper ledger; OPEN for a forbidden-region transfer** | Exactly one deterministic composer performs source evaluation, K arithmetic, formula emission and eventual #SAT call; its time is exponential and its space is charged. No single-machine strict FLMV time-and-space exclusion is achieved. Networks would need sequential total work and aggregate space. |
| Deterministic configuration counting | **PASS as upper-bound guard only** | For total fixed deterministic read-only-input machines T<=2^O(s+log N), or 2^O(s) if s>=log N. The normalizer with Omega(n) stored source/counter is consistent. This is never used as a necessary-work lower bound or extended to random/quantum machines. |

## Ranked dependency map, corpus and next peer repair

1. **PASS, PROVED/RESTRICTED:** TMR-1/052 width-3 pointwise existential projection census and original pairwise-distinct f_S premise, at precisely its fixed-named-input scope.
2. **PASS, PROVED/RESTRICTED (new; review OPEN):** all f_S count to r/2; one O(n)-size strict proper 3CNF with unique auxiliary extensions preserves their common total count. The would-be scalar-count census transfer **FAILS**.
3. **PASS, PROVED/RESTRICTED (new; review OPEN):** universal K-normalizer V<=2n+3, m<=3n+7, but construction time O(2^n poly(N)) means NO general #Circuit-SAT speedup.
4. **PASS, RESTRICTED:** TMR-2/052 high-rank slice cancellation, TMR-4/052 multicut switch product, and TMR-5/048 Gaussian counting counterexample; none implies general circuit or machine time.
5. **OPEN:** uniformly compute the scalar K or find a correct SAT-equivalence/total-count-equivalence encoding in genuinely subexponential ORIGINAL-n time for arbitrary polynomially many genuinely LIVE shared gates, charging all wires, clause indices, arithmetic and peak space.
6. **OPEN:** translate such an algorithm into the EXACT Williams/Bathie-Williams class target and establish a noncircular NP-level bridge. TMR-3's sublinear-height Tree Evaluation target likewise remains OPEN.

**Weakest surviving lemma / one next target:** Replace the expensive exhaustive K(C) stage with a **uniform exact count-preserving compression construction** that runs in 2^o(n) time for every n-input g=n^4 LIVE shared circuit (and pays at least source-reading costs). The short normal form is not the missing algorithm; only computing its scalar index quickly could make it useful. Test hard-to-count circuit controls rather than selecting another many-functions/same-count family.

**Corpus/preflight:** Governing directive read FIRST; root proof1.txt fully available (SHA 06f7ebc8c2283304a0f5200b518c6e48fa41e343), root proof2.txt SHA 930c5eeddafce656717f28055a7a755f44737c and main.tex SHA 6ac34c5dc20a09ba2dc3b8565ed2afac3fb2eb34 had EMPTY GitHub connector text despite valid blob metadata; no complete bodies and therefore no shared writes. Reviewed AGENTS.md, CODEX.md, repository skill, five TMR handoffs, issue #3 current timeline, relevant originals TMR-1/052, TMR-2/052, TMR-4/052, TMR-5/048 and the primary sources below. Full local checkout/preflight and Lean rebuild unavailable in this tool run. This is distinct from any claimed full-corpus machine verification. **TRACKERS REVIEWED AT AVAILABLE CONTENT/METADATA; NO MATERIAL CHANGE.** No agent identity/title/schedule/enabled state was altered.

**Primary sources:** (1) Anthropic, pinned eth/MainResults.lean commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5, https://github.com/anthropics/formal-math/blob/16a5ce41304fcdaea4e0be7c132e1c361dc26da5/eth/MainResults.lean (definition-level syntactic guards; independent Lean build OPEN). (2) OpenAI, Oct. 25, 2026 revised manuscript, https://github.com/openai/math/tree/main/preprints/The-Exponential-Time-Hypothesis-is-False-October-25-2026 (fixed-k subexponential #SAT claim). (3) Williams, *Thinking Algorithmically About Impossibility* (CSL 2015), https://drops.dagstuhl.de/storage/00lipics/lipics-vol041-csl2015/LIPIcs.CSL.2015.14/LIPIcs.CSL.2015.14.pdf (specific NEXP circuit-class consequence, not NP). (4) Bryant (1986), https://doi.org/10.1109/TC.1986.1676819 (shared BDD model context). (5) Baker, Gill, Solovay (1975), https://doi.org/10.1137/0204037 .

**P versus NP remains OPEN.**

END_OF_VERIFIED_REPORT::TMR-5::049
