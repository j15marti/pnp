# LSPV-5/438: terminal-overlap floor validated; minimum-tree sharing is syntactically incompatible

**2026-11-08 09:31 PST | Route B independent red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Affected tracker IDs:** new `[P2-L5-438]`; independently validates `[P2-L1-509]`, materially supersedes the joint-range sentence in `[P2-L5-437]`, and refines `[P2-L1-508]`, `[P2-L1-507]`, `[P2-F13]`. `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]` remain OPEN. `[P1-01]`, `[P1-03]`, `[P1-04]` were reviewed with no material change.

## IDEA and pre-search falsifiers

Hypothesis: combine the exact individual minima from `[P2-L5-437]` with source-support compatibility to narrow the joint ordinary-Resolution gap. Any hypothetical 18-node joint DAG must reuse substantial cross-goal work; exact clause/support constraints might forbid enough reuse to improve the lower floor.

Four falsifiers were fixed before search:

1. an explicit ordinary-Resolution witness with at most 18 distinct derived nodes;
2. a valid nonminimum goal cone that creates sharing unavailable to individually minimum trees;
3. a shared clause whose exact source support defeats the proposed compatibility bound;
4. failure to exhaust every source subset, exact resolvent and goal-extension case inside the claimed finite scope.

Fresh project search found the concurrent stronger graph theorem `[P2-L1-509]`, raising the generic joint floor from 13 to 15. The revised task was therefore to authenticate that theorem, challenge its abstract tightness control at the clause level, and determine exactly how much sharing individually minimum Resolution trees permit.

## SEARCH: complete current project and external evidence

### Complete project reads

- Current starting main head `c55719cf61d012615d01c82d446538e0e2d4e294`.
- Complete `proof1.txt`: blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 characters, 88 lines.
- Complete `proof2.txt`: blob `8f16ca0b2fda81b05ff4ca3d82c68dcb1e801183`, 457,804 characters, 594 lines.
- Current issue #3 was read completely: 13 full 100-comment pages, page 14 with 53 comments, page 15 empty. Relevant latest comments included `[P2-L1-509]`, `[P2-L5-437]`, `[P2-L3-505]` and current Route-A controls.
- Governing five-role handoff at historical commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, blob `033b54b87b7cbe94912af5cf67daa52859143a07`; `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`; `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`; repository skill blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`.
- Peer target: `research/agents/lspv-1/2026-11-08_0900_LSPV1_TERMINAL_OVERLAP509.md`, blob `53a6a24625d2a2163e7493136399e2e0319558ee`; executable `experiments/arc/lspv1_509_terminal_overlap.cjs`, blob `8092730781f1d0787d509800c8ff7e663bdcb425`.
- Other actual files: `[P2-L3-505]` report blob `04a339fa37479131da2e18ebc13000bb29427d7c`; prior `[P2-L5-437]` report blob `2a40ba660c1bf7bef26b628fa8c6f74932815873`; `GROKPROOF/2026-11-08_1130_PROGRESS.md` blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70`; Claude world-ledger README blob `de75a371ce3143a4495e6892df7fb04794a6b708`.

The `/509` JavaScript was refetched by exact blob SHA and executed locally: 485 checks passed, including 25 per-goal deletion witnesses and its 15-node abstract provenance DAG. No raw `/509` JSON or handoff file was located in the expected current `results/raw/arc` or `research/coordination` directories; the executable itself is available and replayable. This is a publication-completeness limitation, not a theorem failure.

### Literature and actual queries

Queries included `resolution proof minimization DAG shortest proof multi conclusion`, `shortest Resolution proof SAT encoding Peitl Szeider`, `Resolution DAG sharing lower bounds source overlap`, and `proof length minimization branch and bound layer list`.

- Sidorov, van der Linden, Correia, de Weerdt and Demirović, JAIR 86 (2026), introduce an exact branch-and-bound Resolution minimizer using a layer-list representation, clause-subsumption/dominance pruning and lower bounds. Its main warning applies directly: solver-generated proofs need not be minimum, and full permutation symmetry is a central bottleneck.
- Peitl and Szeider's SAT encoding represents clause signs and proof arcs and completely breaks proof-line permutation symmetries in its stated shortest-refutation setting. The actual `short.py` implementation was inspected.
- Haken's PHP theorem and Urquhart/Ben-Sasson--Wigderson Tseitin/width-size results remain ordinary-Resolution lower bounds only. Cook extended Resolution and GF(2) Tseitin elimination remain mandatory shortcut controls.

A separate Google-branded client was unavailable; public web search was used. No code execution or source access is claimed where it was unavailable.

### Change-aware repository review

| Repository/path | Current head/blob | Result |
|---|---|---|
| `konard/p-vs-np/scripts/proof_status.json` | head `ecedd2b45f1c524d85c00b2da27a9c140025550c`; blob `93b77ed3d8fe456f81c690035f45f07910a247f2` | No delta closing historical grammar, mixed transfer or B3. |
| `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` | head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`; blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` | Restricted-method inventory; no accepted P-versus-NP proof. |
| `blkph0x/p-vs-np-proof-research/INDEPENDENT_AUDIT.md` | blob `b30515cced93d8911a6415555ee9ec1444502d93` | Uniform constructive transfer remains open. |
| `peitl/short-proof/short.py` | blob `6508dae79e341d7015949d5919de29a132fbf267` | Exact SAT proof-minimization control; not a multi-root certificate for this gadget. |
| `pysathq/pysat/README.rst` | blob `fefde10b1426a92a21425029892f3f49466bf03c` | Solver API only; timeout is not lower-bound evidence. |
| `meelgroup/frat-xor/format.md` | head `18cd6bc17af10a9891c10a846ce966166f9fe0dc`; blob `986a21aa92b62f844ef1fce852193142c41b2b1f` | Separate provisional XOR proof grammar, not historical authority. |
| `tanyongkiam/cake_lpr/README.md` | blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c` | Verified LPR checker with separate trust boundary. |
| `marijnheule/drat-trim/README.md` | blob `eb6ffcc4a85ff1c74a5995b6caae4372381dcd47` | DRAT checking does not certify shortest ordinary Resolution. |
| `digama0/frat/README.md` | blob `0864ba034d50dbacfb1835c24d108e93d0a8bad9` | FRAT elaboration/checking, separate calculus. |
| `openai/math/README.md` | head `4eaee87548250b2682affda7d05d947c05554bae`; blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` | No relevant transfer theorem. |
| `anthropics/formal-math/README.md` | head `16a5ce41304fcdaea4e0be7c132e1c361dc26da5`; blob `1df53bfc14a022088d1b5757698f692bf79390b4` | No relevant theorem; toolchain evidence is not the target proof. |

## ITERATE I: independent proof of the connected-overlap floor

For the exact existing 16-source signed proper-3CNF gadget, independent exhaustive deletion search recovers

$$
\begin{aligned}
E_0&=\{2,3,5,7,10,11,13,14\},\\
E_1&=\{0,1,8,9,12\},\\
E_2&=\{0,1,2,3,4,6,8,9,10,11,12,15\}.
\end{aligned}
$$

They cover all 16 sources. Moreover,

$$
E_0\cap E_2=\{2,3,10,11\},\qquad
E_1\cap E_2=\{0,1,8,9,12\},\qquad
E_0\cap E_1=\varnothing.
$$

Thus the goal-overlap graph is connected. Identify repeated references to the same context-free source record as one source vertex; this never increases paid inference work. In the pruned union of goal ancestries, every source and every nonterminal derived node has an undirected path to a goal. If there are $m$ source vertices, $q$ derived vertices, at most $c$ weak components and indegree at most $d$, then

$$
m+q-c\le e\le dq,
$$

and hence

$$
q\ge\left\lceil\frac{m-c}{d-1}\right\rceil.
$$

For $m=16$, $c=1$, $d=2$, every context-free source-authenticated binary shared DAG deriving all three goals has at least 15 derived nodes. The current ordinary-Resolution range is therefore

$$
15\le q_{\mathrm{Res,three\ goals}}\le19.
$$

This independently validates `[P2-L1-509]`. It also supersedes only the old `13 <= q` joint-range sentence in `[P2-L5-437]`; the exact individual minima `(7,4,11)` from `/437` remain valid.

## ITERATE II: exact minimum-tree sharing obstruction

The `/509` 15-node construction is explicitly an abstract provenance merge DAG, not a Resolution proof. To test whether its sharing pattern can be realized syntactically, the new Python program exhausts every nonempty subset $U$ of each source intersection, every exact non-tautological clause $C$ derivable by a Resolution tree using exactly $U$, and every exact floor-meeting extension of $C$ to both relevant goals.

The result is stronger than the initial expectation:

| Goal pair | Shared indispensable sources | Candidate exact macro clauses | Maximum derived nodes shareable by two individually minimum trees |
|---|---:|---:|---:|
| $Q_0,Q_2$ | 4 | 4 | **0** |
| $Q_1,Q_2$ | 5 | 31 | **1**, via $(1,-4)$ from $S00,S01$ |

In particular, collapsing the exact four-node $Q_1=(1,-7)$ proof to one macro leaf and adjoining the seven remaining indispensable $Q_2$ sources cannot derive $Q_2=(3,-7)$ in the seven additional inferences required to meet the $Q_2$ floor.

Therefore any union of three **individually minimum Resolution trees** has at least

$$
7+4+11-1=21
$$

distinct derived nodes. The known 19-node `/507` joint DAG escapes this bound precisely by using a nonminimum $Q_2$ cone and reusing more of the $Q_1$ derivation. This is a concrete example of the user's point that the global optimum must range over the entire shared DAG rather than minimize branches separately.

The result does **not** raise the all-DAG lower floor above 15: a hypothetical 15-node DAG may use nonminimum goal cones, source fan-out or a sharing topology outside the individually minimum-tree class. Falsifier 2 remains live for the unrestricted finite joint optimizer.

Independent Node implementation repeated the full subset/clause/extension enumeration and passed 12 aggregate assertions plus three corrupt source/goal/inference controls. Exact recorded Python run: 3.51 seconds, 21,672 KiB maximum RSS, 35 candidate macro clauses and 266,799 aggregate reachable tree states. Node replay: 9.97 seconds.

Six complete goal-order cases of a separate 15-node SAT encoding were launched. Each has 3,675 Boolean variables and 49,449 clauses. All six were interrupted at the scheduled-run host-time budget without SAT/UNSAT status. They are charged failed search policies and supply **no** lower-bound evidence.

## Hard-family and shortcut ledger

| Family/control | Exact encoding/parameter | Established model-qualified result | Known methods/shortcuts | Remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic-expander Tseitin | $h$ degree-3 vertices, $3h/2$ edge variables; each parity equation expanded to four signed proper width-3 clauses, total $4h$ clauses and $\Theta(h\log h)$ binary bits | Exponential ordinary shared-DAG Resolution lower bound on suitable expanders | GF(2) elimination and declared source-local factor proofs are short controls | Every-rule historical `R_mix341` transfer OPEN |
| Haken PHP | Standard PHP CNF; not native 3-CNF without a lower-bound-preserving reduction | Exponential ordinary Resolution; encoding-qualified | Cook extended Resolution polynomial shortcut | 3-CNF preservation and all-mixed transfer OPEN |
| `/507`--`/509` cancellation gadget | 16 exact signed proper 3-clauses, 7 variables, SAT with 8 source models | No hard-family theorem; finite joint ordinary-Resolution range now $15..19$ | Exact individual minima `(7,4,11)`; legal 19-node shared proof | Exact joint optimum, native historical acceptance and asymptotic transfer OPEN |

Certified UNSAT, proof-size hardness and empirical solver difficulty remain distinct. The cancellation gadget is SAT and is only a derivation/interface control.

## Resource, AND/OR and historical-rule accounting

- All three goals are AND obligations. Alternative derivations of one goal are OR choices; free after-the-fact optimal choice is preserved.
- Shared nodes are counted once. The finite enumerator labels exact source subsets and does not leak conclusions between incompatible assumption contexts.
- No split, weakening or discharge rule was added. These certificates are context-free ordinary Resolution only; the historical `/341` checker was not run.
- Charged work includes complete tracker/issue/source reads, repository index reads, public literature searches, exact blob replay, 128-assignment deletion search, 266,799 tree states, Python/Node construction and checking, six failed SAT policies, parsing, raw/report/handoff/output, publication and readback.
- Logical nodes, evidence bits, construction time, peak RSS, proof span and realizable schedules are not conflated. No proof weight is interpreted automatically as FLMV machine time/space.

## Status, artifacts and remaining gap

**Actual advance:** independent proof and executable authentication of the 15-node connected-overlap floor; exact clause-level proof that individually minimum goal trees can share at most one derived node in total, so their union needs at least 21 nodes. This explains why global shared-DAG optimization must admit nonminimum local cones and corrects `/437`'s now-superseded joint lower endpoint.

Artifacts:

- `experiments/review/lspv5_438_terminal_overlap_redteam.py`
- `experiments/review/verify_lspv5_438_terminal_overlap.mjs`
- `experiments/review/raw/lspv5_438_terminal_overlap_redteam_results.json`
- `research/coordination/2026-11-08_0931_LSPV5_TERMINAL_OVERLAP438_HANDOFF.md`

**Precise remaining gap:** decide the finite 15--18-node ordinary-Resolution cases with complete independently checkable evidence; then authenticate native historical RES/LOCAL/DEF/split/discharge bytes and prove or refute transfer across every legal mixed rule. The asymptotic all-rule minimum `[P2-B1]` and noncircular same-calculus B3 `[P2-B2]` remain OPEN. **P versus NP OPEN.**
