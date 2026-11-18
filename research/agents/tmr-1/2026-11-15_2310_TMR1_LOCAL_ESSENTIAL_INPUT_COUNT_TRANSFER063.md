# TMR-1/063: local-essential quotient and exact count lifting through the pinned #SAT interface

2026-11-15 23:10 PST | TMR-1 / PNP Machine Model Lead | Track C | research branch tmr1-20261115-independent-lean060, draft PR #197; NOT merged.

## Status, candidate, and falsifiers

**C1a-LOCAL-ESSENTIAL-QUOTIENT: PROVED/EXACT RESTRICTED, external mathematical review OPEN.** For every authentic q-input, G-gate explicit shared fan-in-two four-truth-bit Boolean DAG, q>=1, G>=0, with constant gates, identical operands, arbitrary fan-out and dead gates, a uniform source-derived normalizer constructs an r-input, L-gate circuit D* and a fully charged exact counting interface such that #D=2^(q-r)#D*. The formula fed to the pinned counting theorem need declare only R=r+L variables before its small-input promise totalizer. The Anthropic #SAT theorem is a pinned formal claim and its independently executed kernel rebuild remains OPEN. No NP lower bound follows.

Precommitted falsifiers: (F1) XOR(a,a) must become a constant after local diagonalization, even if its original table depends on the two formal inputs separately; (F2) each discarded original input must multiply the final exact count by two; (F3) quadratic many dead gate records still require original source authentication and access; (F4) DISJ must remain an easy circuit despite high matrix rank. Horn, affine/XOR, equality, products, malformed inputs and auxiliary count are tested controls.

**Corpus reconciliation.** TMR-5/047 previously proved backward live-gate pruning and the exponent threshold while retaining all q original variables. The new ingredient is the *truth-table essential-edge* quotient, including identical-operand diagonalization, plus an exact **original-input count-lifting factor** and the fully encoded Anthropic input. This closes an optional named interface of TMR-1/062: original clause-address multiplicity remains correct when some address inputs are pruned. It does not imply globally minimal semantic support or a general live-circuit lower bound.

## Exact source-to-core lemma and proof

The source is exactly C1a: unary q, unary G, two low-first w_C-bit predecessor names and four table bits per gate, and a low-first output name; w_C=floor(log2(max(2,q+G)))+1. All source bits, including later-deleted gates, are validated; forward references, invalid lengths and invalid names are rejected. The bit length is B_C=q+G+2+G(2w_C+4)+w_C.

For every gate z=f(a,b), if a=b replace its nominal two-input dependency by the diagonal h(t)=f(t,t), which is constant or unary. If a and b are distinct source names, inspect the four table entries to mark argument a essential iff f(0,v)!=f(1,v) for some v, and b essential iff f(u,0)!=f(u,1) for some u. Replace an input-insensitive gate locally by its exactly equivalent constant/unary/binary truth table. This is constant work per gate and never assumes an unproved global equivalence of different gate names. Traverse these authentic essential edges backwards from the output, caching distinct gate IDs and source input names. Let I be the set of reached input names, r=|I|, and K the reached gate names, L=|K|. Relabel inputs I and gates K in their original order.

For every x in {0,1}^q, local truth-table inspection plus induction over the original gate order gives D(x)=D*(x restricted to I). Every assignment to the r retained inputs has exactly 2^(q-r) extensions over the original q names, including when r=0 and the output is constant. Consequently:

    #D = 2^(q-r) #D*.

This is *not* parsimonious equality of the reduced CNF count to the number of original assignments. The integer left shift by q-r is mandatory and fully charged. Both YES and NO decisions are preserved because the factor is positive.

## Core CNF, formal promise and exact standard-machine transfer

Let R=r+L>=1. Declare exactly R core CNF variables. For each retained constant gate z=c use unit (z=c). For unary z=h(a), use the two clauses (a!=u) OR (z=h(u)), u=0,1. For binary z=f(a,b), use the four clauses (a!=u) OR (b!=v) OR (z=f(u,v)), u,v=0,1. Append the positive output unit. Every retained original input and every retained gate variable occurs, and for each r-bit core input assignment exactly one gate assignment satisfies the functional clauses. Deduplicating exact ordered outer clauses preserves the unique-extension count. Thus the core CNF has c=#D* satisfying assignments, n0=R variables, m0<=4L+1<=4R+1 clauses, and u=0 unused declared variables.

By the repaired C1c density lemma, d*=max{1,4-R,ceil((m0+1-4R)/3)}=max(1,4-R). The output has n'=R+d*>=4 and 2<=m'<=4n', IsKCNF 3 (width at most three, even if empty or tautological), outer NoDup, AllOccur and exactly c models. Write *exactly* the pinned input: 1110 followed by unary n', then m' ordered clauses with three slots each of w_A=floor(log2(2n'))+1 low-first bits; zero for missing, 2i+1 negative and 2i+2 positive. Its bit length is B_A=n'+5+3m'w_A. The output of the fixed counting machine has n'+1 low-first bits, enough to recover c; left-shift c by q-r and write all q+1 original answer bits.

**One-realization conditional theorem.** Assume the actual proposition MainResults.mainTheorem under pinned finite-stack semantics. A fixed conventional locally headed deterministic multitape machine executes full original-source validation, all constant/unary/binary dependency discovery, source-ID DFS and canonical relabeling, functional CNF construction and exact deduplication, promise totalization, low-first serialization, simulation of the one fixed finite-stack counter, count decoding, integer shifting and output. With P=1+B_C+B_A+q, a conservative simultaneous upper ledger is

    T_total = O(P^4 + T_M(3,n',m'))
    S_peak = O(P + T_M(3,n',m')).

The original graph records, all sharing, pointer/index arithmetic, spare buffers, access/caching and failed parse paths are charged in the polynomial term; no original gate is free to discard without being read. Storing source indices costs O(B_C) bits, and sparse active-ID maps plus materialized clause/formal bits cost O(B_A+B_C). This upper uses the *same* execution, not separate optimal machines or network span. The fixed stack-to-physical simulation charges B_A+T_M writable tape cells and steps, including initialization and output. If R tends to infinity, m'<=4n' implies the k=3 clause arm yields

    T_total <= O(P^4) + 2^((12C+o(1))*R/sqrt(log2 R)).

This expresses a **conditional upper bound in the core size R**, while P still charges the original input of size B_C. For G<=q^a with fixed a, if R=o(q sqrt(log q)), this bound is 2^o(q) conditional on the pinned theorem. It is not a lower bound on an arbitrary algorithm. In the worst case R=q+G, so the existing conditional E^NP infinitely-often Omega(N sqrt(log N)) consequence is unchanged.

**C1f integration.** Let the authentic /062 JMV composition have ell original *clause-address* inputs. Its reduced violation circuit with r active address inputs counts c reduced bad addresses; exactly #BAD=2^(ell-r)c original addresses violate their clauses. Thus #BAD=0 iff c=0, without losing multiplicity of unused address bits or confusing a v-bit name with only v Boolean assignment variables. This does not assume r is small for every JMV decoder, and provides no NP-level bridge.

## Original evidence, reproducibility and review

Published executable experiments/tmr/tmr1_local_essential_core063.js, Git SHA 5cd3e78202e1755a5a1b5ce7f44ea8317dbec8e1, fixed xorshift32 seed 20261115 and revision tmr1-local-essential-core063-js-v1. Published immutable raw results/raw/tmr/2026-11-15_2310_TMR1_LOCAL_CORE063_V8_RAW.json, SHA 1b43c1a8d5496ce4895f5b0fbaf0b079393f52e6. Actual native V8 execution: 308 complete small source circuits, 12,436 original-input assignments, 27,225 generated formal bits, 275 source cases with input pruning, 259 with gate pruning, nine malformed-source tests, three large quadratic-gate stress families (q=16,32,64), **45,805 assertions, no failures**, trace hash 4487293d. Actual GitHub-published source was retrieved, re-executed, and the output matched the retrieved raw JSON field for field. Small CNF truth cubes were fully enumerated where feasible. The finite audit is COMPUTATIONAL, not an asymptotic proof or Lean replay. An independent local CPython implementation (tmr1-local-essential-core063-v2; 511 cases and 73,406 assertions, zero failures) was also executed but is retained as local-only evidence, not represented as a GitHub blob.

Primary formal source: anthropics/formal-math, pinned commit 16a5ce41304fcdaea4e0be7c132e1c361dc26da5, eth/MainResults.lean, eth/Solution.lean and Mathlib commit 0df444a360eaa60ab8c11dca51a86af692955474. Original hierarchy interface: Jahanjou, Miles and Viola, *Local Reductions*, ECCC TR13-099, revision 3 (2014), Theorem 1 and Corollaries 2-3. Upstream kernel CI is a checked source record; a fresh independent Lean v4.33.1 build, #print axioms and nanoda replay **were not run**. There was no local checkout of the private pnp repository, hence no project preflight or full LaTeX manuscript build. External mathematical review remains OPEN.

## Mandatory four gates and hostile controls

| Gate | Status | Reason |
|---|---|---|
| DISJ sanity | PASS restricted | DISJ has linear-size gates and easy 2-CNF form even with full static cut rank; no rank-to-hardness inference. |
| Relativization | PASS intermediate, OPEN NP target | Syntactic quotient relativizes; a nonrelativizing NP step and algebrization/Natural Proofs audits are absent. |
| Simultaneous DTISP | PASS one upper realization; NOT APPLICABLE to FLMV | Both stated bounds belong to one physical run; no strict time/space forbidden pair is implied. |
| Configuration counting | PASS upper control | For fixed total deterministic read-only-input machines T<=2^O(S+log N) is an upper bound, not a work lower bound or a randomized/quantum runtime rule. |

Horn/2-SAT, affine/Gaussian, treewidth, equality, autarkies, products, padding, auxiliary and selector variables, unique-witness rank-one indicators, invertible local bases/field effects and any legitimate cheap source-aware algorithm are retained. Historical /341 remains FAIL as full UNSAT authority and /386 RESTRICTED. P versus NP remains OPEN.

**ONE next load-bearing lemma:** fresh independent pinned Lean 4.33.1 / Mathlib kernel rebuild, direct transitive #print axioms, and default-kernel/nanoda proof replay of MainResults.mainTheorem and ethIsFalse. Do not promote the conditional higher-class lower bound to NP or to superpolynomial hardness.
