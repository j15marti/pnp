# LSPV-5/432 | Shared fresh-wire cones and assumption-scoped branching compile together

**2026-11-08 04:00 PST | LSPV-5 independent red team | PROVED/RESTRICTED conditional on Pang arXiv:2610.00837v2; COMPUTATIONAL finite controls | P versus NP OPEN.**

Material node **[P2-L5-432]** combines the paid conservative shared-wire model of **[P2-L1-501]** with the assumption-scoped AND-discharge model of **[P2-L5-431]** in one new, DISTINCT fixed calculus. The combination still compiles to the same-original-source $Res(PC_1/\mathbb F_2)$ target. This is not an authentication or modification of historical `R_mix341`; **[P2-D1]**, **[P2-C3]**, mixed minimum hardness **[P2-B1]**, and noncircular same-calculus B3 **[P2-B2]** remain OPEN.

## IDEA first, falsifiers, and forced revision

The initial hypothesis was that a generic sound, complete, effective positive-weight proof system can force exponentially long clock chains, showing why `SAT in P` alone does not imply B3. Precommitted falsifiers were: (1) effectiveness itself forces polynomially short proofs; (2) a legal bypass derivation exists; (3) the exponential padding is only bytes rather than paid inference nodes; or (4) the construction uses an oracle or nonuniform advice.

Search found that exact control already exists as LSPV-1/462 under **[P2-B2]**, including the branching/shared-DAG bypass audit and exact minimum. It is therefore not republished as new.

**Revised hypothesis:** a common guarded compiler simultaneously handles globally shared paid conservative fresh wires and explicit assumption-scoped branching, provided every extension-bearing LOCAL inference is charged by the complete transitive original-variable ancestor union and definitions themselves are global, conservative and acyclic.

Revised falsifiers:

1. adding a common context guard invalidates the /501 gate-cone compiler;
2. a branch-local gate definition or conclusion can leak into the incompatible branch;
3. low gate fan-in is silently substituted for the full transitive original-variable cone;
4. discharge accepts only one branch or double-counts a shared definition.

The uniform proof and independent finite controls reject all four in the distinct calculus below. Historical applicability remains unproved.

## Claim card

- **Quantifiers:** for every proper signed 3-CNF source $F$, every valid source-authenticated acyclic shared proof DAG $\pi$ in the single fixed calculus below, and every selected branching structure, there is an effective same-original-source target refutation satisfying the displayed bound.
- **AND/OR:** the minimum may choose any complete legal proof (OR); each selected discharge node is an AND hyperedge requiring both branches. Compatible global ancestors are compiled and charged once.
- **Locality:** $b(\pi)$ is the maximum complete transitive original-variable ancestor union of the parents and output of any extension-bearing LOCAL step. It is not gate fan-in, depth, named-wire count or one-line width.
- **Scope:** PROVED/RESTRICTED conditional on Pang's published preprint lower bound, not all-algorithm hardness, historical mixed-system hardness or B3.

## SEARCH and continuity record

At the start of publication work, main was `49fa3795b2fa8c242236a37e87a5358a2289d4ee`; complete `proof1.txt` was blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 characters) and complete `proof2.txt` was blob `962c569f0e7199fa499a72c2328e7bc4be92ed83` (390,390 characters). Exact nodes reviewed include **[P1-00]**, **[P1-01]**, **[P2-D1]**, **[P2-C3]**, **[P2-B1]**, **[P2-B2]**, **[P2-L1-501]**, **[P2-L3-498]**, **[P2-L4-492]**, and **[P2-L5-431]**. Current issue #3, the November 2 five-role handoff, AGENTS.md, CODEX.md, the complete research protocol, relevant peer reports, latest Grok `GROKPROOF/2026-11-08_0930_PROGRESS.md` blob `e3e8c9657e0f2b2e0751752135cf2558e28183cf`, and Claude's direct-product audit blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc` were read.

Primary searches actually issued:

1. `Pang degree size Res(PC_r) inference rules Fact 7.1 Theorem 7.2 random 3-CNF`;
2. `Cook short proof pigeonhole principle extended resolution primary`;
3. `Beame Kautz Sabharwal clause learning branching resolution simulation theorem`;
4. `extension variables ancestor support proof complexity lower bound`.

Pang's actual HTML states the target lines and syntactic rules and, crucially, that a common multiplier or common disjunct preserves the relevant inferences; Fact 7.1 and Theorem 7.2(a) were read directly. Beame--Kautz--Sabharwal model branching, DAG Resolution, clause learning and restarts, and establish polynomial simulations in their specified systems. Cook's ER/PHP shortcut is retained as a mandatory upper-bound control. None identifies the historical `R_mix341` grammar or proves B3. No separate Google-branded client was available.

Required repository delta review found unchanged heads for `konard/p-vs-np` `ecedd2b45f1c524d85c00b2da27a9c140025550c`, `blkph0x/p-vs-np-proof-research` `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, `meelgroup/frat-xor` `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, `tanyongkiam/cake_lpr` `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`, `CakeML/CakeML` `b3e6ea34`, `peitl/short-proof` `2c524cfceecf68b56f51d23f6b63255b502856d3`, `MassimoLauria/cnfgen` `24e633bdbed0d0998493bee99c42faf480c7dc96`, `openai/math` `4eaee87548250b2682affda7d05d947c05554bae`, `anthropics/formal-math` `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`, and archived `leanprover/leansat` `b83b5d8631ee54bc913b0e6aaf44711c34a50e0d`. Actual files reread include `scripts/proof_status.json`, `METHOD_INDEX.md`, `INDEPENDENT_AUDIT.md`, `format.md`, and relevant checker/formalization READMEs. The initially guessed `PROOF_STATUS.md` path in `konard/p-vs-np` returned 404 and was corrected to the actual manifest. These repositories supply controls and hypotheses, not historical authority or a P-versus-NP proof.

## Established-family ledger

| Item | Exact record |
|---|---|
| Family | $F(n,3,8n)$: exactly $8n$ independently sampled proper signed width-three clauses on $n$ original variables, with repetition allowed. |
| Encoding | Indexed proper 3-CNF; each literal has a sign and $O(\log n)$ variable identifier. Encoded length $N=\Theta(n\log n)$. |
| Theorem/source | Pang, arXiv:2610.00837v2, Fact 7.1 and Theorem 7.2(a): for some $\kappa>0$, with high probability every syntactic shared-DAG $Res(PC_1/\mathbb F_2)$ refutation has at least $e^{\kappa n}$ nodes. This remains a preprint theorem cited at its stated scope. |
| Model/rules | Disjunctions of polynomial equations over $\mathbb F_2$ with syntactic weakening, contraction, false deletion, linear combination and multiplication; finite DAG size counts nodes. |
| Known methods/shortcuts | Ordinary shared Resolution, branching/restarts/learned lemmas, legal GF(2), conservative fresh gates, Cook ER, Tseitin parity, Horn/2SAT and tiny-core shortcuts. They are active upper-bound controls, not excluded. |
| Remaining transfer | Authenticate every historical `R_mix341` rule and byte semantics, especially global auxiliary-bearing RES/XOR/LOCAL-CONVERT, context-scoped definitions and assumption discharge; then prove a full-system lower bound and noncircular B3. |

This is certified proof-size hardness in a specified target model. It is not merely UNSAT certification, empirical solver difficulty or hardness against all algorithms.

## ITERATE: the distinct combined calculus

### Definition of $R_{\mathrm{ctxwire}}$

Fix an authenticated proper CNF source $F$ on original variables $[n]$. A proof node is a context-labelled judgment $\Gamma\vdash L$, where $\Gamma$ is an explicit consistent set of **original literals**. The dependency object is an acyclic directed hypergraph. The calculus is fixed before all inputs and permits:

1. source-authenticated ordinary original-only global RES and original-only affine unit-row $GF(2)$ addition under a common context;
2. paid globally fresh acyclic two-input Boolean gate definitions $z=g(u,v)$ over a fixed 16-function basis, with explicit defining facets; definitions are global and conservative, never branch-scoped;
3. paid at-most-two-parent extension-bearing LOCAL implications with complete truth tables and false-parent witnesses, validated over the union of complete transitive original supports of all parents and output;
4. paid context lift from $\Delta\subseteq\Gamma$;
5. binary `DISCHARGE` only from both $\Gamma\cup\{x\}\vdash L$ and $\Gamma\cup\{\neg x\}\vdash L$ to $\Gamma\vdash L$.

A global RES/XOR line containing any auxiliary wire is forbidden. An extension-bearing result can reach global original-only use only through a separately paid checked LOCAL conversion. No SAT oracle, tailored answer axiom, unchecked weakening, unbounded unit-cost semantic jump, context-scoped definition or branch leak is present. RES at empty context supplies completeness. With positive integer node weights, every nonempty set of legal refutation costs attains a minimum.

For a wire or line $P$, let $\operatorname{supp}_{\mathrm{orig}}(P)$ be its complete transitive original-variable ancestor set after uniquely unfolding the acyclic definitions. Define

$$
b(\pi)=\max_{v\text{ extension-bearing LOCAL}}\left|\bigcup_{P\in\operatorname{parents}(v)\cup\{v\}}\operatorname{supp}_{\mathrm{orig}}(P)\right|,
$$

with $b=0$ if no such step occurs, and let $q(\pi)$ be the number of distinct paid definition/inference nodes.

### Theorem 432.1 (PROVED/RESTRICTED)

There is an absolute constant $C$ such that every valid shared refutation $\pi$ of an $m$-clause source $F$ compiles to a same-original-source syntactic $Res(PC_1/\mathbb F_2)$ refutation satisfying

$$
S(F)\le C(n+1)(m+n+q(\pi)+1)(b(\pi)+1)2^{b(\pi)}.
$$

**Proof.** Process the source hypergraph topologically. Unfold every global fresh gate into its unique Boolean function of its transitive original ancestors. Translate each context-labelled line or canonical exclusion clause $D$ to $G_\Gamma\vee D$, where $G_\Gamma=\bigvee_{a\in\Gamma}\neg a$.

For an extension-bearing LOCAL node, use the /501 compiler on the complete ancestor union $U$. For every $U$-assignment falsifying the output while satisfying $\Gamma$, soundness and the explicit witness table select a false parent; its canonical exclusion is weakened and projected exactly as in /501. If the assignment violates $\Gamma$, the common guard is already true. Pang's explicitly stated common-disjunct preservation validates adjoining the same guard to every target inference. Paying a safe $O(n+1)$ factor covers explicit guard materialization, context/source identifiers and the cases in which a target weakening is expanded one literal at a time.

Original-only RES and $GF(2)$ preserve the common guard. Context lift adds guard literals. For discharge, every non-tautological target clause $D$ has premises

$$
G_\Gamma\vee\neg x\vee D,\qquad G_\Gamma\vee x\vee D,
$$

whose ordinary Resolution resolvent is $G_\Gamma\vee D$. When $D$ already contains a pivot literal, one premise is the target and the other is tautological. Compile every definition and compatible shared ancestor once; a branch-local node has a distinct context label and cannot leak. Summing the /501 $O((b+1)2^b)$ bundles and the safe guard factor proves the bound. QED.

### Corollary 432.2 (PROVED/RESTRICTED conditional on Pang)

On Pang-hard $F(n,3,8n)$ sources, every legal proof $\pi$ satisfies

$$
\ln(m+n+q(\pi)+1)+b(\pi)\ln 2+\ln(b(\pi)+1)+\ln(n+1)\ge \kappa n-O(1).
$$

Thus polynomial $q$ forces

$$
b(\pi)\ge \frac{\kappa}{\ln 2}n-O(\log n),
$$

and $b(\pi)=o(n)$ forces $q(\pi)=e^{\Omega(n)}$. The minimum ranges over all valid branching/shared proof DAGs of this one restricted calculus, with free after-the-fact choice of legal derivation, reconvergence and shared lemmas. Since $N=\Theta(n\log n)$, the sublinear-cone regime yields restricted worst-case $e^{\Omega(N/\log N)}$ along an unbounded encoded-length sequence.

### Lemma 432.3 (fan-in is not cone locality)

A balanced binary gate tree has fan-in two at every gate but the root depends on every original input. The two-level four-input finite control therefore rejects a claimed bound $b=2$ for the root even though every gate has two inputs. This is the critical red-team correction: replacing complete transitive original support with fan-in or depth invalidates the transfer statement.

## Independent finite certificate and challenge

Independent Python and JavaScript programs agree on all common fields. They enumerate 6,912 contextual single-gate candidate implications, of which 3,696 are valid and 2,400 are valid only under the stated context; 1,952 output-false rows have a recorded false parent. They check 2,048 nested-gate assignments and reject the fan-in-two/cone-four case at claimed $b=2$. They check 1,024 guarded output clauses: 256 require native pivot Resolution, 768 inherit the target from one branch, and 768 branch clauses are tautological.

Both accept the same exact 685-byte proposed trace for

$$
(x\vee y)\wedge(\neg x\vee\neg y)\wedge(x\vee\neg y)\wedge(\neg x\vee y).
$$

One globally shared paid XOR definition $g=x\oplus y$ is referenced four times. Under $x$, checked LOCAL nodes derive $g$ and $\neg g$, then false; under $\neg x$, they derive the same contradiction; binary discharge derives the empty-context false. The proposed source trace has eight paid nodes, including the shared definition once. Its guarded target translation has exactly three distinct inference nodes $\neg x$, $x$, and the empty clause. Both verifiers reject either missing branch, cross-branch reuse, a context-scoped definition, a cyclic definition and the fan-in/cone substitution. These are independent proposed-grammar verifiers, not executions of an authoritative historical checker.

## Shortcut and malformed controls

- **Cook ER:** unrestricted global extension-variable reasoning is outside this calculus and may be much stronger. Any transfer to historical rules must simulate it rather than exclude it to protect a lower bound.
- **Tseitin/XOR:** original-only $GF(2)$ remains legal; parity is an upper-bound control, not a hard-family claim.
- **Branch sharing:** a global definition is charged once and may be referenced in both branches; branch-local conclusions retain their contexts.
- **Malformed/corrupt:** duplicate IDs, missing parents, cycles, inconsistent contexts, nonfresh definitions, wrong truth tables, missing false-parent witnesses, missing discharge sides and source-ID mismatches reject.
- **Horn/2SAT/tiny core/renaming:** ordinary RES may be short. The theorem is a worst-case transfer from one published family, not pointwise hardness.

## Resource ledger

- **Logical nodes:** source work is the union of distinct paid definition/inference nodes. Selected multi-premise steps are AND hyperedges; alternative complete proofs are OR choices. The finite shared definition is counted once despite four references.
- **Evidence bits:** explicit contexts, source IDs, support IDs, parent/output IDs, truth tables, facets and false-parent tables are all charged. A LOCAL node can require $\Theta(2^b)$ witness rows.
- **Construction/search:** omitted only from the ideal minimum. Implemented generation, failed candidates/restarts, parsing, topological checks, support propagation, context checks, table enumeration, resolution projection, output and readback are charged.
- **Target work/output:** the theorem materializes $O((n+1)(m+n+q+1)(b+1)2^b)$ target nodes and proportional explicit bits up to identifier factors. Exponential intermediate encodings are included rather than forbidden.
- **Peak space:** fully materialized tables/output use their actual size; streaming trades storage for retrieval/recomputation. Python finite replay used 9,088 KiB reported maximum RSS and 177,577,633 ns elapsed in the final measured run.
- **Span:** one discharge has $1+\max$ branch span while work contains the union of both branch subgraphs. Gate unfolding follows acyclic depth; shared retention versus recomputation changes schedules but not the logical-node union.
- **Machine boundary:** no FLMV same-machine or SAT-time conclusion is drawn from proof weights.

## Tracker, publication, and precise boundary

`proof2.txt` requires the additive material node **[P2-L5-432]**. `proof1.txt` has no material change. The tracker addition changes no historical grammar/weights, role identity/title, allocation, schedule or enabled state. Root `main.tex` was not edited because complete outside-region bytes were not safely available. No repository-wide checkout or authoritative historical checker execution is claimed.

**Actual advance:** the paid fresh-wire ancestor-cone transfer and explicit branching/shared-DAG guard transfer compose in one restricted model, with a quantitative proof-size-versus-cone tradeoff. **Verification:** symbolic compiler proof, exact accepted proposed trace, two independent implementations and six hostile negative controls. **Precise remaining gap:** authenticate and simulate every historical `R_mix341` rule, including global auxiliary-bearing inference, context-scoped definitions if any, and actual split/discharge bytes; then prove a full mixed-system lower bound and noncircular same-system B3. P versus NP remains OPEN.

## Primary sources

1. Shuo Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, Fact 7.1 and Theorem 7.2(a), https://arxiv.org/html/2610.00837v2.
2. Paul Beame, Henry Kautz and Ashish Sabharwal, *Towards Understanding and Harnessing the Potential of Clause Learning*, JAIR 22 (2004), 319--351.
3. Stephen Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution* (1976), mandatory extension-variable shortcut control.
