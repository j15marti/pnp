# Recognizable-island and certificate-rooting firewall — REFEREE325

**PNP Independent Proof Red Team, November 3, 2026, 17:48 PST.**  
**Status:** one broad representation-invariance proposal is **FALSIFIED**; a source-rooted certificate lemma is **PROVED/ABSTRACT**; its full-`Rmix341` application, B1/B2/B3 and P versus NP remain **OPEN**. No task, schedule, enabled state, calculus rule, encoding convention or weight was changed.

## 1. Exact obstruction and falsifiers

The obstruction is not lack of a hard source. It is that semantic equivalence, source retention, reversibility and paid construction still allow a compiler to recognize a certified UNSAT island and append an unrelated tiny contradiction.

This run tested four precise claims:

1. **Common-envelope claim:** one polynomial reflects native proof cost through every uniform exact source-prefix compiler. **False.**
2. **Physical-charge repair:** charging parsing, reads, construction, output and peak space blocks the recognizable-island compiler. **False; the compiler is linear-time and logspace-streamable.**
3. **Algorithm-independent family claim:** one explicit polynomial-time recognizable hard family is hard for every fixed correct uniform SAT decider. **False.**
4. **Certificate-rooting repair:** requiring every added leaf and target inference to carry a paid source-derived macro restores representation robustness. **True, but the resulting logical invariant is exactly the native fixed-calculus proof cost and the missing simulation reappears unchanged.**

No new candidate hard formula was generated.

## 2. Published lower-bound anchor: exact scope

For `h` holes and `h+1` pigeons, let `PHP_(h+1)^h` be the standard unary CNF with variables `x_(i,j)`, one pigeon clause `x_(i,1) OR ... OR x_(i,h)` for each pigeon, and each collision clause `NOT x_(i,j) OR NOT x_(k,j)` for distinct pigeons `i,k` and hole `j`. It has `h(h+1)` variables and `(h+1) + h * binom(h+1,2)` clauses. With explicit signed indexed literals its binary/DIMACS-style length is `N_h=Theta(h^3 log h)`.

**Haken's theorem used here:** there exist constants `c>0,h0` such that for every `h>=h0`, every ordinary unrestricted shared-DAG Resolution refutation of this explicit CNF has at least `2^(c h)` lines/nodes. Resolution permits arbitrary legal pivots and DAG reuse; it does not include extension variables, GF(2), circuits, Horn solvers, semantic jumps, or arbitrary algorithms. Haken also notes that Extended Resolution has polynomial proofs of these formulas. The theorem is therefore restricted proof hardness, not an unrestricted SAT time lower bound.

Source: Armin Haken, *The Intractability of Resolution*, Theoretical Computer Science 39 (1985), DOI `10.1016/0304-3975(85)90144-6`.

## 3. One fixed uniform encoder defeats the broad common envelope

Let `P_PHP(F)` be the fixed syntactic parser recognizing whether valid CNF `F` is exactly canonical `PHP_(h+1)^h` for some `h`. The ordered grammar makes this recognizable in time linear in the explicit source length. Define one encoder, fixed before every input and size:

```
E_PHP(F) = F AND (z) AND (NOT z),  if P_PHP(F)=1;
           F AND (z),              otherwise,
```

where `z` is fresh. Malformed encodings are rejected.

### Exactness

For every assignment `a` to the original variables, `F(a) = exists z E_PHP(F)(a,z)`. On the recognized island `F(a)` is always false and the opposite units are false for every `z`. Off the island the fresh positive unit has the unique extension `z=1`. Hence this is stronger than label preservation: it preserves the complete projected original-variable relation. The original clauses are an unchanged prefix, so decoding is source-prefix reversible.

### Fully charged construction

The compiler performs a full grammar scan, reads all source bits, writes `F` plus one or two units, and verifies freshness. It has `O(N)` time/output/access work; canonical ordered comparison is `O(log N)` streaming workspace, or `O(N)` space if the output is materialized. All these costs are polynomial and are included below.

### Contradiction

On every canonical PHP source, the target has a one-step Resolution refutation by resolving `(z)` with `(NOT z)`. Since no empty clause is a source, its minimum target cost is exactly one:

`W_Res(E_PHP(PHP_(h+1)^h))=1`.

Suppose the REFEREE324 common envelope held over this broad encoder class:

`W_Res(F) <= p(|F| + |code(E)| + C_E(F) + W_Res(E(F)))`

for one polynomial `p`, every encoder and every UNSAT `F`. Substituting the single fixed `E_PHP` and the whole PHP family makes the right side polynomial in `N_h`, while Haken makes the left side `2^(Omega(h))`, superpolynomial in `N_h`. Contradiction.

**Conclusion:** REFEREE324's common-envelope implication was correct conditionally, but its premise is false for all uniform polynomial-time semantically exact encoders. The failure uses one encoder for the whole growing family, not per-input advice, a per-length optimizer, or an uncharged exponential conversion.

The weaker family-tail/budget-stratified formulations identified by LSPV-1 also fail on this example: the same encoder has polynomial budget on every sufficiently large family member.

## 4. Algorithm-independence firewall

More generally, let `H` be any fixed polynomial-time recognizable family containing only valid UNSAT formulas, and let `A` be any fixed total correct all-CNF decider. The single fixed decider

```
A_H(F): if F is in H, return UNSAT; otherwise run A(F)
```

is uniform, total and correct, and runs in polynomial time on every member of `H`. Therefore no one explicit P-recognizable certified family can carry a superpolynomial runtime lower bound for **every** correct uniform algorithm.

For `H=PHP` and ordinary Resolution, choose a complete exponential fallback `A`. Then `A_H` is polynomial on the Resolution-hard family, so **B1 fails for ordinary Resolution**. B2 and B3 are not refuted: `A_H` can be exponential elsewhere and their hard input may depend on the solver.

This theorem does not say that unrestricted worst-case SAT is easy. It shows why algorithm-independent hardness cannot be obtained merely by attaching an intrinsic number to one recognizable established family.

## 5. What survives: source-rooted certificate closure

Fix a sound shared-DAG calculus `R`. Permit any exact, lazy, circuit, GF(2), auxiliary-variable or shared representation package `P` for source `F`, but require:

- every non-source leaf actually used has a paid `R`-macro deriving its mapped claim from authenticated source/parent claims;
- every target inference used has a paid `R`-macro under the same mapping;
- the terminal maps to contradiction;
- shared macro nodes are charged once, and payload serialization, construction, access, checking, output and peak space are recorded separately.

Topologically splice the macros. The result is an `R`-refutation of `F`, so `W_R(F) <= Cert_R(P)`.

Taking the infimum over all such packages cannot beat `W_R(F)`. Conversely, the identity package containing a minimum `R` proof attains `W_R(F)` in its logical-node component. Thus the representation-robust rooted logical invariant equals the native model-relative quantity `W_R`; physical evidence/checking costs can only increase it and need not be polynomial in node count when payloads are unbounded.

This repair blocks `E_PHP` only by charging derivations of its opposite units from `F`. Splicing those derivations with the one-step contradiction is already an `R`-refutation of `F`. The repair therefore does not discover a new algorithm-independent invariant; it reinstates the desired backtranslation as a hypothesis.

The newest LSPV-3 result gives a concrete restricted instance. In strict `E = RES + paid conservative AND2-DEF`, for `G=F AND Gamma(D)` with `k` acyclic conservative definitions, `W_E(G) <= W_E(F) <= W_E(G)+k`. That is a valid proof-splicing theorem in its declared grammar. Full opaque `LOCAL-CONVERT` and full `Rmix341` remain open.

## 6. Relation to B1/B2/B3

For any fixed correct decider `A`, define a label-switching source-prefix compiler `E_A`: execute `A`; append opposite fresh units on UNSAT and a benign fresh unit on SAT. Its construction cost is `Theta(N+T_A(F))`, and on UNSAT its target proof costs one. Consequently, polynomial cost reflection for this one compiler is exactly strong enough to imply B1 for `A`. If a polynomial-time `A` exists, the same reflection gives B3.

So an envelope covering every sound exact compiler is not an easier substitute for the computational bridge. It already contains the bridge. Restricting to source-rooted proof-carrying compilers makes the statement true by splicing but model-relative; extending that splicing polynomially to the decider-induced proof system is precisely B3.

## 7. Peer, Grok and Claude audit

- **LSPV-1/375**, `research/agents/lspv-1/2026-11-03_1700_LSPV-1_AFFINE_ROW_ER2_SIMULATION375.md`, blob `92e5a295c53a58c003004ff36a59294546740310`: polynomial simulation only for normalized `X3` into paid `ER2`; arbitrary-width parity has compact prefix gates; full opaque `LOCAL-CONVERT` remains open.
- **LSPV-2/375**, `research/agents/lspv-2/2026-11-03_1712_LSPV-2_UNIFORM_SOURCE_PREFIX_COMPILER375.md`, blob `d33582b746604732575e0ddec48d8bc3aa9a4cb9`: independently exhibits the same one-encoder phenomenon inside fixed `Rmix341`, reducing the known linear odd-Tseitin cost `4h-1` to one while paying linear construction. It is not superpolynomial mixed hardness.
- **LSPV-3/379**, `research/agents/lspv-3/2026-11-03_1724_LSPV-3_SOURCE_GATE_REPAIR379.tex`, blob `f37a00cd05f42e6fb6e2555db84dd95707403ae1`: proves the strict-`E` additive sandwich above; full mixed transport remains open.
- **LSPV-4/372**, `research/agents/lspv-4/2026-11-03_1636_LSPV-4_SHARED_XOR_PATH_MULTIPLICITY372.tex`, blob `43f2d2ed2179ce8dc00c519f2f7ee4193b054d80`: exponential dependency-walk multiplicity can coexist with polynomial shared-DAG evidence and checking.

Every reviewer located and read actual Grok and Claude files. Current Grok `GROKPROOF/2026-11-04_0116_PROGRESS.md`, blob `ca5a835356eb918b8cb4ab94d14de6174edeab03`, leaves the all-input fully charged contraction and certificate coverage open and rejects automatic proof-complexity-to-machine transfer. Claude `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`, supplies a valid hidden-selector/portfolio critique; `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`, remains a restricted alternation-trading result. None supplies rooted full-mixed transport or B3.

## 8. Literature and repository searches

Primary-source queries included:

- `p-optimal propositional proof systems simulation every proof system Cook Reckhow primary paper`;
- `optimal propositional proof systems p-simulation open problem primary source`;
- `Haken intractability resolution pigeonhole principle exact theorem PDF`.

Cook and Reckhow define p-simulation and prove that a system p-simulating a polynomially bounded system is polynomially bounded (*The Relative Efficiency of Propositional Proof Systems*, JSL 1979; preliminary STOC 1974, DOI `10.1145/800119.803893`). The existence of a p-optimal system remains open; it cannot be assumed as the missing common transport. Project GitHub searches found the peer reports above. A separate `github.com/openai` search for a model-matched propositional proof checker/compiler returned no match; this is an access/search result, not an absence theorem.

## 9. Finite controls and accounting

The producer and independently written JavaScript verifier checked:

- canonical PHP with one through three holes: UNSAT counts `0` and exact one-step encoded refutations;
- paired satisfiable PHP controls: model counts `1,2,6`, unique benign-unit extensions;
- ordinary contradictory-unit, Horn and 2-SAT controls;
- exact source-prefix recovery and complete projected-relation preservation;
- mandatory K4 Tseitin control: odd charge `0` models, even charge `8` models;
- ten malformed records rejected before encoding.

Producer: 54 explicit compiler assertions. Independent verifier: 36 assertions. No published asymptotic lower bound was regenerated and no finite proof search was used as asymptotic evidence.

SHA-256:

- producer `ef0bfca49ec2acc6f13b3fee2efb46fd145121124727a6d3d05fcf2849eb0d47`;
- verifier `3d70a7e558f2a24eeeb144faa108c9f43dff0dd86050bbbc9deb6315f495d60d`;
- raw `c1184225f9eb83a25934657ca903d5ef435b1fafbab864727c64d19d130ea933`.

## 10. Classification and next obligation

**PROVED:** one fixed uniform exact source-prefix encoder falsifies the broad common envelope; fully charged construction does not repair it; recognizable-family algorithm-independence fails; source-rooted macro splicing restores only the native model-relative proof measure.

**RESTRICTED:** Haken is ordinary Resolution hardness; LSPV-1/375 and LSPV-3/379 cover declared subgrammars only; LSPV-2/375 is a linear mixed-cost countercontrol.

**OPEN:** a superpolynomial lower bound for fixed full `Rmix341`; polynomial rooted transport for every full mixed rule; B1/B2/B3 for `Rmix341`; any unrestricted SAT time/space lower bound; P versus NP.

The weakest honest next target is now narrower: specify a nontrivial proof-carrying transformation class closed under every allowed `Rmix341` rule and prove polynomial source-rooted splicing there. That is a model-relative transfer theorem. It must not be called representation- or algorithm-independent, and it still does not provide B3 without transporting the decider-induced proof system.
