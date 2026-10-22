# EQUALITY-LOCALIZATION-MINOR-BARRIER65

Timestamp: 2026-10-22 13:48 KST

**Global status: P versus NP OPEN; P versus RP OPEN.**

Scope: the two existing P-vs-NP routes and the independent P-vs-RP question. Circuit-SAT remains a representation and hostile-control tool.

## Repairs proposed before source review

1. **Occurrence localization:** duplicate every cross-block variable occurrence and connect its copies by equality trees, hoping to replace a large shared interface by small local interfaces.
2. **Certified elimination order:** supply a recursive separator or tree-decomposition certificate and charge both discovery and verification.
3. **Semantic compiler under \(P=NP\):** abandon syntax-preserving partitions and construct equivalent small-interface children, but require an explicit uniform transformation and same-machine resource bound.

The first repair is falsified below as a universal compiler. The second works exactly when the source already has low treewidth or a valid separator tree. The third is the remaining nonlocal possibility and is OPEN.

## Reports reviewed after recording the repairs

1. [UNIVERSAL-SHIFT29](https://github.com/j15marti/pnp/blob/main/research/agents/rp-separation/2026-10-22_RP_UNIVERSAL_SHIFT29_HANDOFF.md): a uniform hitting list for promised RP verifiers with an unknown logarithmic coin backdoor and constant residual ANF degree; exact acceptance counting is unnecessary once the RP promise is fixed.
2. [SMALL-INTERFACE-EXACT-JOIN64](https://github.com/j15marti/pnp/blob/main/research/main/2026-10-22_1248_MAIN_SMALL_INTERFACE_EXACT_JOIN64.md): exact SAT reconstruction and the target ARC recurrence for a source-checkable logarithmic-interface recursive class.
3. [ARC-DISJ37](https://github.com/j15marti/pnp/blob/main/research/agents/arc/2026-10-22_ARC_DISJ37.md): detached answer-only joins fail on shared witnesses, while explicit source-aware joining can succeed.

## Correction incorporated

For a **promised valid RP verifier**, deterministic simulation needs to hit one accepting original random tape on YES inputs; it does not need to estimate or compare the acceptance probability with \(1/2\). NO inputs have no accepting tape. Certifying that an arbitrary circuit satisfies the RP promise is separate.

The SMALL-INTERFACE64 main report and coordination handoff were corrected on GitHub before this synthesis.

## Model — occurrence localization

Let \(H(F)\) be the clause-variable incidence graph of a CNF \(F\). A syntax-preserving occurrence localization replaces each incidence edge \((C,x)\) by a fresh occurrence variable \(x_C\) used in clause \(C\), and connects all copies of the same original variable \(x\) by a connected equality network. Equality constraints may use fresh auxiliary variables and constant-size CNF or Circuit-SAT gadgets.

The transformation is exact only if the equality network forces all copies to agree.

## Lemma 65A — incidence-minor preservation

For every exact connected occurrence-localization \(F'\) of \(F\),

$$
H(F)\preceq H(F'),
$$

where \(\preceq\) denotes the graph-minor relation, up to the constant-size equality-gadget expansion.

**Proof.**

For each original variable \(x\), contract the connected equality network joining all occurrence copies \(x_C\) and its auxiliaries to one vertex. Delete gadget vertices and edges not needed for connectivity. Every original clause vertex remains, and every original incidence \((C,x)\) is restored by the edge from \(C\) to its contracted occurrence copy. Thus the quotient contains \(H(F)\). \(\square\)

Treewidth is minor-monotone, so

$$
\operatorname{tw}(H(F'))\ge\operatorname{tw}(H(F)).
$$

**Status: ESTABLISHED.**

The claim is purely structural. It is not a SAT runtime lower bound.

## Lemma 65B — recursive SMALL-INTERFACE implies logarithmic treewidth

Suppose a graph of encoded size \(N\) has a recursive decomposition in which every node of size \(m\):

- removes a separator of size at most \(c\log_2m\);
- leaves components of size at most \(m^{1/2}\);
- recurses until constant size.

Along a root-to-leaf path, separator sizes sum to

$$
c\log N+c\log N^{1/2}+c\log N^{1/4}+\cdots
\le 2c\log N.
$$

Combining every component decomposition with the accumulated ancestor separators gives a tree decomposition of width

$$
\operatorname{tw}(G)\le2c\log_2N+O(1).
$$

For SMALL-INTERFACE64, \(c=0.1+o(1)\).

**Status: ESTABLISHED.**

This is a sufficient structural consequence, not a converse characterization.

## Corollary 65C — equality localization cannot be a universal separator compiler

Bounded-degree wall graphs \(W_r\) are bipartite, have \(\Theta(r^2)\) vertices, maximum degree three, and treewidth \(\Theta(r)\). Treat one bipartition as clauses and the other as variables; boundary degree-two clauses can be padded by constant-size local gadgets.

Their ordinary encodings have length

$$
N=\Theta(r^2\log r).
$$

Any exact occurrence-localized encoding contains \(W_r\) as a minor by Lemma 65A, hence has treewidth

$$
\Omega(r)=\Omega\!\left(\sqrt{N/\log N}\right),
$$

which eventually exceeds every \(O(\log N)\) bound from Lemma 65B.

Therefore duplicating occurrences and adding equality trees cannot transform every explicit CNF into the recursive logarithmic-interface class required by SMALL-INTERFACE64.

**Status: ESTABLISHED for syntax-preserving occurrence localization.**

**RETIRED:** occurrence splitting plus equality gadgets as a universal SMALL-INTERFACE64 compiler.

This does not rule out a nonlocal semantic reduction that fails to preserve the source incidence graph as a minor.

## Why equality removal is not a repair

For the two blocks

$$
F_1=(z),\qquad F_2=(\neg z),
$$

deleting or failing to expose the equality/shared-source relation makes both blocks individually SAT, while the conjunction is UNSAT. Short hashes cannot replace equality unless exact congruence is proved; DIGEST-LUMP19 shows that general nonlinear congruence certification can itself be coNP-complete.

Thus the minor barrier cannot be escaped by simply omitting the join edges.

## Certified elimination orders

If a source already has treewidth \(O(\log N)\), a supplied tree decomposition or recursive separator certificate can support exact dynamic programming. Verification must check:

- every clause/gate appears;
- every source variable's bags form a connected subtree;
- every incidence edge is covered;
- bag size, child size and source-access bounds;
- all tables, arithmetic, output and replay costs.

Under \(P=NP\), searching for an existing polynomial-size certificate may become polynomial, but high-treewidth wall inputs have no such certificate. The assumption does not create nonexistent separators.

**Status: ESTABLISHED verification target; OPEN as an arbitrary-input ARC compiler.**

## Consequences for the ARC/FLMV route

SMALL-INTERFACE64 remains a valid restricted contractor. The new barrier identifies precisely why the most obvious universalization fails:

- localizing occurrences preserves exact semantics;
- connected equality networks preserve the source graph as a minor;
- high-treewidth inputs therefore retain superlogarithmic separators;
- the \(N^{0.6}\)-call ledger cannot enumerate those interfaces.

The remaining constructive target is a **nonlocal, solver-dependent semantic contraction** whose children do not preserve the incidence graph as a minor, while still providing exact joint labels, source-checkable completeness, virtual bit access, hereditary recursion and the matched FLMV machine ledger.

**Arbitrary-input ARC/FLMV status: OPEN.**

## MKTP route audit

Occurrence localization and equality gadgets are uniform, locally indexable transformations. Their outputs have short reconstruction programs relative to the source and therefore tend toward ordinary-KT LOW, not the missing UNSAT-HIGH target.

ORBIT39's robust HIGH mask construction remains label-insensitive. The SAT-to-ordinary-MKTP both-label arrow is unchanged.

**SAT-to-ordinary-MKTP status: OPEN.**

## RP synthesis

UNIVERSAL-SHIFT29 establishes a polynomial uniform hitting set for the promised class where an unknown \(k=O(\log n)\) set of original coin coordinates reduces every slice to constant ANF degree. No backdoor discovery is needed. Certification of a specified backdoor remains coNP-complete and is not language hardness.

For promised RP verifiers carrying a valid recursive small-interface certificate, acceptance existence can be decided by the restricted contractor; exact acceptance counts are unnecessary. The minor barrier says equality localization cannot put every verifier into that class.

**P versus RP status: OPEN.**

## Finite structural audit

The stdlib-only audit constructed 28 bounded-degree brick-wall incidence graphs for \(2\le r\le128\), localized every variable occurrence, connected copies by equality paths, and mechanically contracted the equality components.

It verified:

- bipartiteness and maximum degree three;
- exact recovery of every original incidence edge after contraction;
- up to 66,049 localized vertices and 49,472 source edges;
- growing disjoint horizontal linkage;
- the \((z)\wedge(\neg z)\) hidden-equality hostile control.

Result: **85 structural checks, zero failures.**

The finite audit verifies the encoding/minor implementation. The asymptotic conclusion uses Lemmas 65A and 65B plus the standard wall-treewidth property.

## Five-role ledger

| Role | Status | Single next discriminating test |
|---|---|---|
| :00 SAT-to-ordinary-MKTP | **OPEN** | Test whether any SAT-sensitive target transformation avoids both ORBIT39 label-insensitivity and a short source-reconstruction program. |
| :12 P!=RP | **OPEN**; UNIVERSAL-SHIFT29 **ESTABLISHED restricted** | Apply the hitting list to three growing WRAPPER sizes using original coin coordinates and complete source/gate charges. |
| :24 ARC/FLMV | SMALL-INTERFACE64 **ESTABLISHED restricted**; equality compiler **RETIRED**; arbitrary contractor **OPEN** | Attempt a non-minor-preserving semantic child compiler under \(P=NP\), and expose the exact joint-label certificate. |
| :36 P=RP | **OPEN** | Cross-check UNIVERSAL-SHIFT29 on dummy-padded and verifier-replaced circuits; the same language must remain decidable. |
| :48 synthesis | Minor barrier **ESTABLISHED** | Use wall/expander incidence inputs as mandatory controls for every proposed separator compiler. |

## Route conclusion

- **MKTP magnification:** unchanged OPEN both-label ordinary-KT arrow.
- **ARC/FLMV:** a restricted exact contractor exists, but variable splitting and equality gadgets cannot extend it to all inputs. A nonlocal semantic contraction is now the highest-value constructive interface.
- **P versus RP:** restricted derandomization improved; equality and separation remain OPEN.

No root manuscript, automation, or role assignment was modified.
