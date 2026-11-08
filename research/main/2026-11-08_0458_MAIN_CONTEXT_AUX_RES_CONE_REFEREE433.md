# LSPV-5/433 | Auxiliary Resolution cone transfer survives explicit branching and shared definitions

**2026-11-08 04:58 PST | LSPV-5 independent red team | PROVED/RESTRICTED conditional on Pang arXiv:2610.00837v2; COMPUTATIONAL finite controls | P versus NP OPEN.**

Material node **[P2-L5-433]** composes **[P2-L1-502]** (global auxiliary-bearing Resolution at charged transitive original-variable cone) with **[P2-L5-432]** (explicit original-literal contexts, shared global definitions and two-premise AND discharge). This gives a stronger DISTINCT fixed calculus than either component alone. It does not authenticate or alter historical `R_mix341`; **[P2-D1]**, **[P2-C3]**, full mixed minimum hardness **[P2-B1]**, and noncircular same-calculus B3 **[P2-B2]** remain OPEN.

## IDEA first, duplicate found, and revised falsifiers

Initial hypothesis: the /432 compiler could admit ordinary Resolution on auxiliary gate literals without forcing each step to be relabelled `LOCAL`, provided the cone parameter charges the complete transitive original-variable union of both parents and resolvent.

Pre-search falsifiers:

1. auxiliary-pivot Resolution becomes unsound after gate substitution;
2. canonical parent bundles cannot derive the canonical resolvent bundle within $O((b+1)2^b)$;
3. shared or branch-scoped definitions permit assumption leakage;
4. Cook-style extension reasoning yields a polynomial proof while every measured cone stays sublinear, contradicting the proposed tradeoff.

Search found that the initial rule-level theorem had already been published as **[P2-L1-502]**. It is not restated as new.

**Revised hypothesis:** the /502 auxiliary-Resolution compiler remains valid after adding /432's explicit contexts, globally shared definitions, context lift, branch closure and two-premise discharge. New failure modes are a common context guard corrupting an auxiliary-pivot macro, double-counting a shared definition across branches, or a branch-local definition leaking into its incompatible sibling.

Outcome: the symbolic composition proof and two independent finite verifiers reject these failure modes for the separate calculus below. Historical applicability remains open.

## Claim card

- **Exact quantifiers:** for every authenticated proper signed 3-CNF source $F$, every valid acyclic context-labelled shared refutation $\pi$ in the one fixed calculus below, and every freely selected legal branching structure, there is an effective same-original-source target refutation satisfying the displayed bound.
- **Model:** conservative globally fresh acyclic two-input definitions; ordinary Resolution on original or auxiliary literals under a common context; original-only global $GF(2)$; checked LOCAL; paid lift, closure and binary discharge.
- **Resource:** $q(\pi)$ counts distinct paid definition/inference nodes once. $b(\pi)$ is the maximum complete transitive original-variable ancestor union across any extension-bearing Resolution or LOCAL inference.
- **AND/OR:** the minimum may select any complete legal derivation (OR), but every selected discharge is an AND hyperedge requiring both branch closures. A compatible global definition is charged once even when both branches reference it.
- **Scope:** structural restricted transfer and cone tradeoff, not unrestricted ER size hardness, arbitrary-machine SAT hardness or B3.

## SEARCH and exact continuity

At preflight, main was `faf57f850d44510e9f6ea0dc1879624649cbed38`; complete `proof1.txt` was blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 characters), and complete `proof2.txt` was blob `3603f88acfb4b7631593f19a4fb56ed18ba28ba0` (402,280 characters). Exact nodes reviewed include **[P1-00]**, **[P1-01]**, **[P1-03]**, **[P1-04]**, **[P2-D1]**, **[P2-C3]**, **[P2-B1]**, **[P2-B2]**, **[P2-L1-502]**, **[P2-L3-499]**, **[P2-L4-493]**, and **[P2-L5-432]**. Current issue #3 body and its 1,327-comment count were read; the connector's bulk comment read failed with `Transport closed`, so current peer work was instead read from exact main-branch reports and tracker nodes, not falsely claimed as a complete comment-body replay.

Also read the November 2 governing handoff, AGENTS.md, CODEX.md, the complete repository research protocol and mode references, LSPV-1/502 report blob `340104976b68902064b0a2bdd160378d335a5a68`, LSPV-3/499 source-bound native firewall blob `27e2d66f85e0a7f910ee3f1002be5c2ed49f7d81`, LSPV-4/493 outbound-bit barrier, Grok `GROKPROOF/2026-11-08_1130_PROGRESS.md`, and Claude `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`. None supplies full historical mixed legality or noncircular B3.

Primary searches actually issued:

1. `proof complexity extension variables Resolution substitution projection bounded support`;
2. `extended resolution substitution proof complexity bounded variables`;
3. `Shuo Pang degree size relation Fact 7.1 Theorem 7.2 random 3-CNF`;
4. `Cook short proof pigeon hole principle extended resolution 1976 original`.

Pang's actual theorem text was inspected: target lines are disjunctions of polynomial equations with syntactic weakening, contraction, false-constant deletion, linear combination and multiplication; proofs are finite DAGs counted by nodes. Theorem 7.2(a) applies to random constant-width CNFs, including proper signed width-three with density at least $2^3$. Braun's actual bit-PHP theorem and rules were also inspected as the required current DAG-like `Res(XOR)` control. Grosof--Zhang--Heule give explicit $O(n^3)$ DRAT/PHP shortcut constructions using auxiliary variables, confirming that known shortcut proofs must remain active controls. No separate Google-branded client was available.

### Repository delta review

Required heads were unchanged: `konard/p-vs-np` `ecedd2b45f1c524d85c00b2da27a9c140025550c` and `blkph0x/p-vs-np-proof-research` `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`. Actual files reread: `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `INDEPENDENT_AUDIT.md` blob `b30515cced93d8911a6415555ee9ec1444502d93`. They explicitly contain scoped/model-specific results, not historical authority.

Rotating corpus checks included `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`, `cake_lpr/README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`, `CakeML/cakeml/README.md` blob `8215ddfa23ab8d2254cb475b10689e1d4f92a6ec`, `peitl/short-proof/README.md` blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab`, `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`, `anthropics/formal-math/eth/README.md` blob `0b3dcf4a858ff802b3275fc5999ffb134c74de60`, and deprecated `leanprover/leansat/README.md` blob `afc8a7c67599bd9653c831026571a6b0823ec05f`. The current Anthropic ETH artifact reports only `Challenge.lean` sorries and lists `propext`, `Classical.choice`, and `Quot.sound` for its named theorems, but no independent local build/replay occurred here and it is not load-bearing for this proof-complexity result. `MassimoLauria/cnfgen` README and several default-branch commit lookups were unavailable through the connector in this run; prior pinned head `24e633bdbed0d0998493bee99c42faf480c7dc96` was not promoted to a fresh read.

## Established-family/theorem/encoding ledger

| Family | Exact encoding and size | Theorem/model | Known methods and qualification | Remaining transfer |
|---|---|---|---|---|
| Pang random proper 3-CNF $\mathcal F(n,3,8n)$ | $8n$ independent uniform draws from the $8\binom n3$ signed proper width-three clauses; duplicates allowed; $N=\Theta(n\log n)$ in an explicit indexed encoding | Pang arXiv:2610.00837v2, Theorem 7.2(a): with high probability size $e^{\Omega(n)}$ in syntactic shared-DAG $Res(PC_1/\mathbb F_2)$ | Certified proof-size hardness in the specified target model; ordinary Resolution, sharing, legal algebra and target rules are allowed. Not all-algorithm hardness. | Transfer all historical mixed rules and prove B3. |
| Braun bit-PHP $\mathrm{BPHP}^{n+1}_n$, $n=2^\ell$ | $(n+1)\ell$ bits; $n\binom{n+1}{2}$ collision clauses of width $2\ell$; no range axioms | Braun arXiv:2609.23015v2, Theorem 1.1: DAG-like $Res(\oplus)$ size $>\exp(n/(32768\ell^2))$ for $\ell\ge32$, pivot any affine form, semantic weakening, shared DAG | Precisely sourced `Res(XOR)` lower-bound control. It is not 3-CNF; no equisatisfiability-only 3-CNF transfer is claimed. Fresh extension axioms are outside Braun's system. | Establish a lower-bound-preserving 3-CNF simulation before using it as a 3-SAT family. |
| PHP shortcut control | Standard PHP CNF; historical widths vary and standard encodings are not automatically 3-CNF | Haken: exponential ordinary Resolution; Cook ER and Grosof--Zhang--Heule DRAT: polynomial auxiliary-variable proofs | Demonstrates that a known restricted lower bound can vanish in stronger systems. The current theorem permits the shortcut but charges broad transitive cones where they occur. | No inference from PHP Resolution hardness to historical mixed hardness. |

## ITERATE: distinct contextual auxiliary-Resolution calculus

Fix an authenticated proper CNF source $F$ on original variables $X=[n]$. A proof node is a judgment $\Gamma\vdash C$, where $\Gamma$ is an explicit consistent set of original literals. The proof dependency object is an acyclic directed hypergraph. The fixed calculus $R_{\mathrm{ctx+auxRES}}$ permits:

1. paid globally fresh acyclic conservative two-input Boolean gate definitions over a fixed 16-function basis, with complete defining facets; definitions are global, never branch-scoped;
2. source-authenticated ordinary Resolution on original or auxiliary literals under one common context;
3. original-only global $GF(2)$ addition and the /501 checked LOCAL rule under a common context;
4. paid context lift and `CLOSE` only when a derived clause contradicts an explicit context literal;
5. binary `DISCHARGE` only from both $\Gamma\cup\{x\}\vdash L$ and $\Gamma\cup\{\neg x\}\vdash L$ to $\Gamma\vdash L$.

No extension-bearing global $GF(2)$, semantic oracle, context-scoped definition, tailored answer axiom or unchecked cross-branch lemma is allowed. Ordinary empty-context Resolution makes the system complete. Positive integer weights make the minimum attained.

For a clause $C$, let $U(C)$ be the union of the complete transitive original-variable ancestor sets of its auxiliary literals. For each extension-bearing Resolution inference $P,Q\to C$, charge

$$
|U(P)\cup U(Q)\cup U(C)|.
$$

Together with the analogous /501 LOCAL union, let the maximum be $b(\pi)$; let $q(\pi)$ be distinct paid definition/inference nodes.

### Theorem 433.1 (PROVED/RESTRICTED)

There is an absolute constant $K$ such that every valid shared refutation $\pi$ compiles to a same-original-source syntactic $Res(PC_1/\mathbb F_2)$ refutation of size

$$
S(F)\le K(n+1)(m+n+q(\pi)+1)(b(\pi)+1)2^{b(\pi)}.
$$

**Proof.** Use the /502 translation $\mathcal T(C)$: unfold every global conservative gate, separate original literals outside $U(C)$ as a guard, and represent every falsifying assignment on $U(C)$ by its canonical exclusion clause. For a context-labelled line, append the common disjunct

$$
G_\Gamma=\bigvee_{a\in\Gamma}\neg a
$$

to every clause in $\mathcal T(C)$.

Consider an auxiliary-bearing Resolution inference under one context. On an assignment satisfying $\Gamma$ and falsifying the resolvent, the substituted pivot value selects a false parent exactly as in /502. Weaken that parent's canonical exclusion and eliminate the extra cone variables by the /502 binary assignment tree. On an assignment violating $\Gamma$, the common guard is already true. Thus adjoining $G_\Gamma$ to every intermediate target clause preserves the macro, including an auxiliary pivot that disappears from the resolvent. Pang's syntactic common-disjunct/weakening rules justify this directly. An original pivot, repeated literal or tautological guarded clause is handled by the /502 corner-case construction. The cost remains $O((n+1)(b+1)2^b)$ per paid source node.

Global definitions are compiled once and referenced from both branches. A node derived under $\Gamma$ cannot enter an incompatible context. `CLOSE` contracts a clause containing the complement of a context literal to the already present guard. For `DISCHARGE`, corresponding target clauses have premises

$$
G_\Gamma\vee\neg x\vee D,
\qquad
G_\Gamma\vee x\vee D,
$$

and ordinary Resolution yields $G_\Gamma\vee D$. Process the acyclic hypergraph topologically and retain each compatible target bundle once. Summing the node costs proves the bound. QED.

### Corollary 433.2 (PROVED/RESTRICTED conditional on Pang)

For Pang-hard $F\sim\mathcal F(n,3,8n)$, every legal proof satisfies

$$
\log(m+n+q+1)+b\log2+\log(b+1)+\log(n+1)\ge\kappa n-O(1).
$$

Hence polynomial $q$ forces

$$
b\ge\frac{\kappa}{\log2}n-O(\log n),
$$

while $b=o(n)$ forces $q=e^{\Omega(n)}$. This is a **cone tradeoff**, not an unrestricted ER size lower bound: a polynomial proof may contain a linear-cone inference. Cook/DRAT extension shortcuts remain legal controls rather than excluded derivations.

## Independent exact trace and hostile challenge

The finite source on originals $r,x,y,t$ is

$$
(r\vee x\vee t)\wedge(r\vee\neg x\vee t)\wedge
(\neg r\vee x\vee t)\wedge(\neg r\vee\neg x\vee t)\wedge y\wedge\neg t.
$$

One paid global definition $z\leftrightarrow(x\wedge y)$ is shared by both branches. Under $r$, auxiliary-bearing Resolution derives $\neg r\vee z\vee t$ and $\neg r\vee\neg z\vee t$, resolves on $z$, and closes against $\neg t$. Under $\neg r$, the symmetric derivation closes. Both branch closures are required by discharge.

Independent Python and JavaScript verifiers accept the **same canonical 1,212-byte trace**, SHA-256 `c4cd3fb28f8b0803ed9ffdaa2c0fce8d25aa5c91404812bf7cb8972cd784960b`. They agree exactly on 14 paid nodes, one shared definition referenced four times, eight extension-bearing Resolution nodes, maximum cone two, 160 exhaustive semantic assignment checks, 34 canonical output-false rows, and final target lines $\neg r,r,\bot$. They reject a missing branch, wrong auxiliary pivot, cross-branch reuse, branch-scoped definition, cyclic definition and fan-in/cone aliasing. These are independent proposed-grammar verifiers, not executions of an authoritative historical checker.

## Resource and shortcut ledger

- **Logical work:** union of distinct paid nodes; the shared definition is counted once. Discharge work contains both branches; alternative complete proofs remain OR choices.
- **Evidence bits:** source/facet IDs, gate table, freshness/topology, contexts, pivots, parent IDs and clauses are explicit. The compiler may emit $\Theta(2^b)$ canonical rows per node.
- **Construction/search:** excluded only from the ideal minimum. Actual parsing, source authentication, cone propagation, assignment enumeration, reference lookup, failed candidates, output and verification are charged.
- **Work/span:** discharge span is $1+\max$ branch span, while work is the union of both branches and shared ancestors. Auxiliary elimination has work $O((b+1)2^b)$; parallel depth and processor count require a separate schedule.
- **Peak space:** full materialization has output-scale peak; streaming reduces retention at retrieval/recomputation cost. The final Python replay used 8,448 KiB reported maximum RSS and 938,896 ns elapsed.
- **Cook ER/DRAT:** known polynomial PHP proofs remain active upper-bound controls. The theorem only says a Pang-family polynomial proof in this restricted calculus must expose a broad transitive cone somewhere.
- **Tseitin/parity:** original-only $GF(2)$ remains legal. Braun and Pang show precisely model-qualified parity lower bounds; same-characteristic Tseitin shortcuts remain easy controls.
- **Malformed/corrupt:** duplicate IDs, missing parents, wrong pivot orientation, inconsistent contexts, nonfresh/cyclic definitions, missing discharge side and out-of-range source IDs reject.
- **Machine boundary:** no SAT-time, FLMV same-machine, or arbitrary-algorithm lower bound follows from proof weights.

## Tracker, publication and boundary

`proof2.txt` requires the additive material node **[P2-L5-433]**. `proof1.txt` has no material change. Historical grammar/weights, roles, titles, schedules, enabled states and the two-Route-A/three-Route-B allocation are unchanged. Root `main.tex` was not edited because complete outside-region bytes were not safely available.

**Actual advance:** the /502 global auxiliary-Resolution cone compiler and /432 assumption-scoped branching/shared-definition compiler compose without multiplying shared nodes or leaking contexts. **Verification:** symbolic compiler proof, exact common trace bytes, two independent implementations and six hostile rejects. **Precise remaining gap:** authenticate actual historical `R_mix341` auxiliary RES, definition, LOCAL-CONVERT, $GF(2)$ and split/discharge bytes; then simulate every remaining rule without a broad-cone escape and prove noncircular same-system B3. P versus NP remains OPEN.

## Primary sources

1. Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, Fact 7.1 and Theorem 7.2(a), https://arxiv.org/html/2610.00837v2.
2. Kamil Braun, *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015v2, Theorem 1.1.
3. Stephen Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4), 1976.
4. Isaac Grosof, Naifeng Zhang and Marijn Heule, *Towards the Shortest DRAT Proof of the Pigeonhole Principle*, SAT 2022.
