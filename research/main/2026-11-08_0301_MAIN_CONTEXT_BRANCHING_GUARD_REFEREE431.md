# LSPV-5/431 | Explicit assumption-scoped branching preserves the restricted guarded transfer

**2026-11-08 03:01 PST | LSPV-5 independent red team | PROVED/RESTRICTED conditional on Pang's cited preprint theorem; COMPUTATIONAL finite controls | P versus NP OPEN.**

Material node **[P2-L5-431]** extends **[P2-L1-500]** to one new, DISTINCT fixed contextual calculus. It gives a rigorous answer to the branching/shared-DAG clarification inside that restricted model: both split branches are conjunctive obligations, branch-local lemmas cannot leak, and reconvergent nodes are charged once. It does not authenticate or change historical `R_mix341`, close **[P2-D1]**, **[P2-C3]**, **[P2-B1]**, same-calculus B3 **[P2-B2]**, or any proof1 node. P versus NP remains OPEN.

## IDEA first and precommitted falsifiers

Initial hypothesis: explicit assumption-scoped binary case splits can be added to the restricted locality calculus without defeating Pang's lower bound. Translate a judgment $\Gamma\vdash L$ to the target line guarded by the clause $G_\Gamma=\bigvee_{a\in\Gamma}\neg a$; discharge of the two conclusions under $x$ and $\neg x$ becomes ordinary Resolution on $x$.

Assumptions: contexts are explicit consistent literal sets; every lift/application is paid; the proof dependency graph is acyclic; the two discharge premises have the same conclusion and contexts exactly $\Gamma\cup\{x\}$ and $\Gamma\cup\{\neg x\}$; no fresh definitions, hidden semantic oracle or unrestricted weakening is added.

Prediction: the guarded compiler has polynomial overhead when the one fixed authenticated LOCAL threshold is $b(n)=\lceil\log_2(n+2)\rceil$, even with arbitrary branching, reconvergence and sharing.

Precommitted falsifiers:

1. Pang's target rules do not preserve a common disjunctive guard.
2. A legal affine/XOR step cannot be simulated under the guard.
3. Reconvergent reuse permits a lemma derived under one branch to leak into an incompatible branch.
4. The discharge rule can accept only one side of an AND split.

The symbolic proof and two independent finite verifiers reject all four for the separately defined calculus below. They do not answer whether historical `R_mix341` contains a native rule with these exact semantics.

## Claim card

- **Exact quantifiers:** fix the single total computable $b(n)=\min(n,\lceil\log_2(n+2)\rceil)$ and the complete contextual grammar below before all sources. For every valid original CNF $F$ and every valid context-labelled shared refutation DAG with $q$ paid nodes, there is an effective same-original-source syntactic $Res(PC_1/\mathbb F_2)$ refutation with at most $c(n+1)(b(n)+1)2^{b(n)}(q+m+n+1)$ nodes, for one absolute $c$.
- **Model:** original Boolean variables only; ordinary Resolution, global $GF(2)$ addition, explicit bounded-support LOCAL steps, explicit context lift, and two-premise binary discharge.
- **AND/OR semantics:** alternative legal proofs are OR choices in the minimum; a selected discharge is an AND hyperedge requiring both branches. Distinct context-labelled nodes are paid once; compatible shared ancestors can reconverge.
- **Resource:** logical work, evidence bits, construction/verification, span and realizable storage are kept separate.
- **Scope:** a restricted proof-system transfer, not arbitrary-machine SAT hardness and not a B3 bridge.

## SEARCH and continuity record

Complete current trackers were read before publication: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 bytes) and `proof2.txt` blob `98a1f9cd17fd62d803ab94ffc4ee5bc8bee9dbc2` (376,201 bytes). Exact nodes reviewed include **[P1-00]**, **[P1-01]**, **[P2-D1]**, **[P2-C3]**, **[P2-B1]**, **[P2-B2]**, **[P2-L1-500]**, **[P2-L3-496]** and **[P2-L5-430]**. Current issue #3, the November 2 five-role handoff, AGENTS.md, CODEX.md, the complete research protocol, LSPV-1/500, LSPV-3/496, LSPV-4/491, latest Grok `GROKPROOF/2026-11-08_0930_PROGRESS.md` blob `e3e8c9657e0f2b2e0751752135cf2558e28183cf`, and Claude's direct-product audit blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc` were read. The user-provided native-core archive and report remain pinned prior inputs; they do not define the new contextual calculus.

Primary searches actually issued:

1. `Pang arXiv 2610.00837 Res(PC_r) inference rules linear combination weakening common guard`;
2. `clause learning branching proofs shared DAG resolution simulation case split discharge theorem`;
3. `DPLL clause learning polynomially simulates general resolution proof system primary paper`.

Beame, Kautz and Sabharwal, *Towards Understanding and Harnessing the Potential of Clause Learning*, JAIR 22 (2004), explicitly model branching/restarts and prove polynomial simulations between their clause-learning proofs and Resolution; their Lemma 1 gives an $n$ factor in one direction. Buss, Hoffmann and Johannsen, *Resolution Trees with Lemmas*, develop WRTL/WRTI and DAG-Resolution simulations. These are controls for branch/lemma accounting, not proofs about `R_mix341`. Pang, *A Degree--Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, supplies the target lower bound as freshly audited in /500. Direct full Pang PDF opening was unavailable in this run, so the exact theorem/rule statement is inherited from that current primary-source audit rather than falsely claimed as a new replay. No separate Google-branded client was available.

Required repository delta review found unchanged heads for `konard/p-vs-np` `ecedd2b45f1c524d85c00b2da27a9c140025550c`, `blkph0x/p-vs-np-proof-research` `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, `meelgroup/frat-xor` `18cd6bc17af10a9891c10a846ce966166f9fe0dc`, `tanyongkiam/cake_lpr` `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2`, `peitl/short-proof` `2c524cfceecf68b56f51d23f6b63255b502856d3`, `MassimoLauria/cnfgen` `24e633bdbed0d0998493bee99c42faf480c7dc96`, `openai/math` `4eaee87548250b2682affda7d05d947c05554bae`, `anthropics/formal-math` `16a5ce41304fcdaea4e0be7c132e1c361dc26da5` and archived `leanprover/leansat` `b83b5d8631ee54bc913b0e6aaf44711c34a50e0d`. `CakeML` is now pinned at `b3e6ea34...` from 2026-11-07. Actual method/status/audit/format files were reread; none supplies the historical grammar, a same-system B3 bridge, or this theorem.

## Established-family ledger

| Item | Exact record |
|---|---|
| Family | $F(n,3,8n)$: exactly $8n$ proper signed width-three clauses sampled uniformly with replacement over $n$ original variables. |
| Encoding | Ordered indexed 3-CNF; each literal has one sign and an $O(\log n)$ identifier; encoded source length $N=\Theta(n\log n)$. |
| Theorem/source | Pang arXiv:2610.00837v2, Theorem 7.2(a), as authenticated in **[P2-L1-499/500]**: with probability $1-o(1)$ every syntactic shared-DAG $Res(PC_1/\mathbb F_2)$ refutation has at least $\exp(\kappa n)$ nodes for some $\kappa>0$. |
| Model/rules | Syntactic Resolution over degree-one polynomials over $\mathbb F_2$, with the source's Boolean axioms, linear combination, weakening and false deletion. |
| Assumptions | Preprint theorem, characteristic two, degree one, same original proper signed random 3-CNF, sampling with replacement. |
| Known shortcuts used as controls | Global XOR, legal bounded semantic steps, ordinary shared Resolution, explicit branching/reconvergence and learned lemmas. Cook/ER fresh definitions and unbounded semantic jumps are absent; Tseitin XOR is expected easy. |
| Remaining transfer | Authenticate and simulate every historical `R_mix341` rule, including any native split/discharge interface, and establish noncircular same-system B3. Both remain OPEN. |

This is certified proof-size hardness in a specified proof system. It is not merely certified UNSAT, empirical solver difficulty, or hardness against all algorithms.

## ITERATE: the distinct contextual calculus

### Definition of $R_{\mathrm{ctxlog}}$

The source parser validates the canonical CNF header and original-variable universe $[n]$, and rejects malformed input. A proof node is a judgment $\Gamma\vdash L$, where $\Gamma$ is an explicit consistent set of original literals and $L$ is a clause, affine unit or explicitly tabulated factor. The proof is an acyclic directed hypergraph. Rules are fixed once for all inputs:

1. source-authenticated ordinary RES under a common context;
2. global affine addition over $\mathbb F_2$ under a common context;
3. `LOCAL_log`, with the /500 complete-table and false-parent witness discipline, when total support is at most $b(n)$;
4. paid context lift only from $\Delta\subseteq\Gamma$;
5. binary `DISCHARGE`: from both $\Gamma\cup\{x\}\vdash L$ and $\Gamma\cup\{\neg x\}\vdash L$, infer $\Gamma\vdash L$.

Both discharge premises must be present and have exactly the claimed contexts and conclusion. A node may be referenced from multiple later nodes only when its context assumptions are justified by subset inclusion or discharged by rule 5. There are no fresh variables/definitions, unbounded LOCAL jumps, free equivalence oracle or tailored answer axioms. RES at empty context makes the calculus complete. All weights are positive integers, so every nonempty set of refutation costs has a minimum rather than only an infimum.

### Theorem 431.1 (PROVED/RESTRICTED)

There is an absolute constant $c$ such that every $q$-node $R_{\mathrm{ctxlog}}$ refutation of an $m$-clause original CNF $F$ on $[n]$ compiles to a same-source syntactic $Res(PC_1/\mathbb F_2)$ refutation of size

$$
S(F)\le c(n+1)(b(n)+1)2^{b(n)}(q+m+n+1).
$$

**Proof.** Define the guard $G_\Gamma=\bigvee_{a\in\Gamma}\neg a$. Translate each clause line $\Gamma\vdash C$ to $G_\Gamma\vee C$. Translate a factor to its canonical bundle of guarded exclusion clauses; translate an affine unit to the corresponding guarded polynomial line/bundle used by /500.

Source and context lift are simulated by syntactic weakening, adding guard literals one at a time; the displayed safe bound pays $O(n)$ even if the target supports a more direct weakening. RES under one context preserves the common guard. Affine linear combination preserves the common guard because the guard disjunct remains an alternative on every assignment. The /500 LOCAL compiler works row by row after adjoining the same guard: an assignment satisfying $\Gamma$ is discharged by the named false parent; an assignment violating $\Gamma$ satisfies the guard. Thus one LOCAL node costs $O((b+1)2^b)$ target nodes, with an additional safe $O(n)$ allowance for explicit guards and bit evidence.

For `DISCHARGE`, each non-tautological translated output clause $D$ has premises

$$
G_\Gamma\vee\neg x\vee D,
\qquad
G_\Gamma\vee x\vee D.
$$

Resolving on $x$ yields $G_\Gamma\vee D$. If $D$ already contains $x$ or $\neg x$, one premise is the target and the other is tautological, so no unsound contraction is needed. This applies independently to every canonical factor clause. Process the acyclic source hypergraph topologically, sharing every translated context-labelled ancestor once. Therefore the total bound follows. QED.

The proof explicitly distinguishes OR alternatives from AND premises: the minimum may choose any one complete legal refutation, but every discharge node inside that refutation contains both incoming branch edges.

### Corollary 431.2 (PROVED/RESTRICTED conditional on Pang)

For $b(n)=\lceil\log_2(n+2)\rceil$, the compiler overhead is polynomial. Pang's $\exp(\Omega(n))$ target lower bound therefore implies $q=\exp(\Omega(n))$ with high probability for $F(n,3,8n)$ and

$$
\overline W_{R_{\mathrm{ctxlog}}}(N)\ge \exp(\Omega(N/\log N))
$$

along an unbounded encoded-length sequence. This minimum ranges over all legal branching structures, reconvergence and compatible shared lemmas in the fixed restricted calculus. It says nothing about a historical rule not authenticated above.

## Independent challenge and accepted finite trace

Independent Python and JavaScript implementations agree on 14,103 guarded output clauses, including 555 native pivot resolutions, 13,548 cases where one branch already equals the target and 16,488 tautological targets omitted. Python exhaustively checks 966,561 contextual factor implications on three variables, including 789,414 implications valid only under their context and 609,368 consistent output-false rows with a false parent. Both check 55,296 guarded affine assignments.

Both independently accept the same exact 594-byte proposed trace for

$$
(x\vee y)\wedge(\neg x\vee y)\wedge(x\vee\neg y)\wedge(\neg x\vee\neg y).
$$

It has seven paid context nodes: three under $x$, three under $\neg x$, then one two-parent discharge. Its guarded target translation has exactly three distinct derived lines $\neg x$, $x$, and the empty clause. Both verifiers reject missing positive/negative branches, mismatched conclusions, cross-branch lift, inconsistent context and cycles. These are independent proposed-grammar verifiers, **not** executions of an authoritative historical `R_mix341` checker.

## Hostile controls

- **Illegitimate reuse:** a node at context $\{x\}$ cannot lift into $\{\neg x\}$; only a common ancestor or discharged result can be shared.
- **Omitted AND case:** either missing branch rejects the trace. A different proof may avoid the split, but a selected split cannot.
- **Double counting:** a context-labelled node is paid once even when several compatible descendants reference it; reference costs remain whatever the fixed calculus specifies.
- **Affine/Tseitin:** guarded affine addition remains legal, so parity instances remain shortcut controls rather than protected hard candidates.
- **Cook ER:** fresh definition variables are absent. If authenticated historical definitions are present, this transfer does not apply until their target simulation is proved.
- **Horn/2SAT/tiny core:** RES may be short. The lower bound is worst-case via one published random family, not pointwise.
- **Clause-learning literature:** known polynomial simulations support the use of branching/learned-lemma controls but do not identify the historical byte grammar or prove B3.

## Resource ledger

- **Logical work:** the source cost is the union of distinct context-labelled inference nodes. Multi-premise rules are AND hyperedges; selected derivations are OR alternatives. The target bound above counts distinct compiled nodes.
- **Evidence bits:** each context costs $O(n\log n)$ bits in the safe explicit representation; each LOCAL table/witness record costs $O(2^b(1+\log(q+2)))$ plus support identifiers. The 594-byte trace is fully explicit.
- **Construction/search:** the ideal minimum omits discovery. The effective compiler and verifiers charge parsing, topological/cycle checks, context comparison, branch matching, table enumeration, reference lookup, output and failed-control checks.
- **Parsing/source/index/head reads:** the original source, declared universe, every node id, parent id, context and output are read and range checked. Repository head and full tracker blobs were refetched before the write.
- **Conversions/output:** guard materialization can cost $O(n)$ per line; factor expansion costs $O(2^b)$. No exponential intermediate is forbidden by fiat; here $2^b=O(n)$.
- **Peak space:** full materialization can use output-size storage. Streaming lowers retention but may add retrieval/recomputation. No FLMV space claim follows.
- **Span:** one discharge contributes $1+\max$ of the two branch spans, while work includes the union of both branches. Guard/table macros add $O(n+b)$ sequential span in the conservative schedule; parallel rows require an explicit processor model and joins.
- **Execution:** Python runtime was 2.777867923 seconds with 9,088 KiB reported maximum RSS; JavaScript independently matched the common fields. Compilation and syntax checks passed.

## Tracker, manuscript and precise boundary

`proof2.txt` requires the material additive node **[P2-L5-431]**; `proof1.txt` has no material change. The tracker addition does not alter historical grammar/weights, five-role allocation, role IDs/titles, schedules or enabled states. Root `main.tex` was not edited because a complete body could not be authenticated through the connector; outside-byte preservation therefore remains intact. A complete local checkout was unavailable, so repository-wide preflight was not claimed.

**Actual advance:** a fully explicit context/AND-discharge/shared-DAG extension of the logarithmic-local restricted calculus still transfers polynomially to Pang's target system. **Verification:** symbolic uniform compiler proof, one exact accepted 594-byte proposed trace, two independent implementations and hostile negative controls. **Precise remaining gap:** authenticate whether historical `R_mix341` has these exact context, lift and discharge semantics and accepted bytes; then simulate all remaining fresh/nonlocal rules and prove noncircular same-system B3. P versus NP remains OPEN.
