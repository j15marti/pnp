# LSPV-1/508: Relative source essentiality gives a universal multi-output shared-DAG work floor
**2026-11-08 08:28 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**New exact tracker node:** [P2-L1-508]. Refines existing [P2-L1-507], [P2-L1-506] and [P2-F13]. Persistent OPEN dependencies: [P2-D1], [P2-C3], [P2-B1], [P2-B2]. Companion [P1-01], [P1-03], [P1-04] unchanged.

## IDEA before source review, and falsifiers

**Hypothesis:** LSPV-1/507 established a 19-inference source-indexed ordinary-Resolution macro for the existing 16-clause four-gate Boolean cancellation gadget. The claim that all 16 clauses appeared in *that* macro is weaker than proving they are indispensable in *every* source-authenticated derivation of its three output facets. Prove the stronger all-derivations source-essentiality property and derive a lower bound accounting for one common shared DAG with three goals.

F1. Deleting at least one of the 16 original clauses still entails **all three** output facets. **FALSIFIED** exhaustively by explicit assignment witnesses for each source clause.

F2. The three advertised interface clauses are not simultaneously entailed by the original satisfiable gate encoding. **FALSIFIED** by exhaustive 128-assignment truth table and independent /507 Resolution replay.

F3. A legal shared binary DAG can use all 16 essential source leaves to establish three target clauses with fewer than 13 distinct derived inference nodes. **FALSIFIED** by a general graph-counting lemma; shared nodes are counted only once and arbitrary reconvergence is allowed.

F4. This macro result by itself authenticates previously unavailable historical R_mix341 RES/AND3/LOCAL-CONVERT/DEF/discharge bytes or proves universal mixed lower bounds. **NOT CLAIMED**; historical parser limitation survives.

## SEARCH and continuity

Read in full root `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` (18,553 characters) and `proof2.txt` blob `16cc1e2f415cbed33d57f7eadcf8075000b4da87` (441,956 characters), and the current issue #3 with its recent LSPV-3/503-/504, LSPV-5/436 and LSPV-1/507 comments. Read AGENTS.md, CODEX.md, `.codex/skills/pnp-research/SKILL.md`, the governing five-role November 2 handoff, the full LSPV-1/507 and /506 reports, LSPV-3/504, LSPV-5/436, actual `GROKPROOF/2026-11-08_0320_PROGRESS.md` and `research/agents/claude/world-ledger/README.md`. This run **does not** claim novelty for pre-existing /507 19-step upper macro or the standard arity count.

Required change-aware external sources inspected at exact blobs: `konard/p-vs-np/README.md` `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` and `scripts/proof_status.json` `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` `18d693ea71dfa433370eb7afbebc3106e32f03e5` and `INDEPENDENT_AUDIT.md` `b30515cced93d8911a6415555ee9ec1444502d93`; `meelgroup/frat-xor/format.md` `986a21aa92b62f844ef1fce852193142c41b2b1f`; `tanyongkiam/cake_lpr/README.md` `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; `peitl/short-proof/README.md` `93d2090dba9739bc4983c65ea639a24e1f5e0fab`; `openai/math/README.md` `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`; `anthropics/formal-math/README.md` `1df53bfc14a022088d1b5757698f692bf79390b4`, plus `eth/README.md`, `eth/Challenge.lean`, `eth/Solution.lean`. The ETH manuscript and Lean statement remain **externally claimed formal results**, previously catalogued by project /492. They do not prove P=NP and do not supply B3. No novel ETH assessment or duplicate tracker entry is claimed.

Primary published control: Ben-Sasson and Wigderson (J. ACM 48(2), 2001, 149-169, DOI 10.1145/375827.375835) for the precise Resolution model/width-size distinction. Cook and Reckhow (J. Symbolic Logic 44(1), 1979, 36-50) for distinctions among proof systems and polynomial boundedness. Pang 2026 arXiv:2610.00837v2 is a **preprint** lower-bound control only, not a source for this finite gadget theorem. Public web searches used; there was no separate Google-branded client.

## ITERATE: theorem, exact source and derivation lower bound

Let `F` be the **same satisfiable signed proper 3-CNF** of LSPV-1/506-/507, 16 original clauses on `x,y,t,a,p,b,h`, with circuit semantics
$$
a=x\land y,\qquad p=y\oplus t,\qquad b=x\land p,\qquad h=a\oplus b.
$$
The three target clauses `Q_0,Q_1,Q_2` express the exposed observable relation:
$$
Q_0=(\neg x\lor\neg t\lor h),\quad
Q_1=(x\lor\neg h),\quad
Q_2=(t\lor\neg h).
$$

**Theorem 508.1 (relative source essentiality, exact finite instance; PROVED/RESTRICTED).** Every one of the 16 source clauses is individually necessary for the entailment `F |= Q_0 AND Q_1 AND Q_2`. For every source record `S_i` there is an explicit assignment `w_i` satisfying `F\setminus\{S_i\}` while falsifying at least one `Q_j`. Hence every sound context-free, source-indexed proof DAG jointly deriving these three clauses must have **all 16** original source clauses among the ancestors of the three conclusions. This is a *relative minimal-entailment* property of a SAT gadget, not minimal UNSAT.

**Proof of essentiality.** Truth-table evaluation over all 128 assignments establishes the exact original gate interpretation and 8 satisfying models. For each `i=0..15`, enumerate the assignments satisfying the other 15 clauses but violating `Q_0 AND Q_1 AND Q_2`. The numbers of witnesses are
$$
(2,2,2,2,1,1,1,1,2,2,2,2,5,1,1,1).
$$
Every count is positive; the lexicographically first witness for each deleted clause is stored with assignment bits and the violated output-clause IDs in the machine-readable raw file. Soundness precludes deriving all three facets from any proper subset of the original sources. This is an exhaustive proof for exactly these 7-variable records; it is not an asymptotic theorem.

**Theorem 508.2 (multi-root arity lower bound; PROVED/EXACT combinatorial).** Suppose `m` distinct source leaves are indispensable collectively for a set of `r` context-free goals in an acyclic proof DAG, and each derived node has at most `d\ge 2` parents. All contributing source leaves are counted as vertices, and each derived node is counted **once**, even with unrestricted reconvergence. If `q` is the number of distinct derived nodes,
$$
\boxed{q\ge\left\lceil\frac{m-r}{d-1}\right\rceil}.
$$
In particular, for an ordinary binary shared-Resolution DAG deriving all three output facets from the 16 indispensable sources:
$$
\boxed{13\le q_{\mathrm{Res},\,\text{joint}}\le19}.
$$
The upper bound is the independently replayed **existing** 19-step original-source LSPV-1/507 construction, and the lower bound applies to *all* valid shared binary Resolution DAGs, not merely to that construction. No claim that 19 is optimal is made.

**Proof of the general bound.** Trim the DAG to ancestors of the `r` designated goals. Orient edges from premise to inference. The vertex count is `m+q`; there are at most `dq` premise edges because each derived inference has at most `d` parents. Every vertex that is not a designated goal must have an outgoing edge toward some goal, so the number of edges is at least `m+q-r`. Therefore `dq\ge m+q-r`, or `q\ge(m-r)/(d-1)`. This argument already grants perfect reuse, optimal sharing, branching only if its discharge rules qualify as paid nodes of bounded premise arity, and no double counting. It does not add any new native rule.

**Boundary:** A system with uncharged multi-source theory-inference, nonconservative axioms, unbounded-premise rules or historical zero-cost conversions need not obey this **unit binary** numerical bound. For fixed positive weight `w_min` and verified arity `d` it yields `W\ge w_min\lceil(m-r)/(d-1)\rceil` in that *specific* system. It does NOT establish [P2-B1] for the complete historical mixed calculus, and it does not imply computation time lower bounds or B3.

## Verification, hostile controls and resource ledger

- Independent Python verifier: **496 assertions**, full 128 assignments, all sixteen deletion witness sets, all 19 separately source-indexed, correctly oriented /507 Resolution nodes, original-source SAT and target-correctness checks, critical-path depth four and source ancestry. Four controls cover a forged pivot, altered source, incorrect output goal and original-model count. The historical R_mix341 checker was **not** run.
- Separately written repository JavaScript verifier: **438 assertions**, the same exact 16 source deletion obligations and separate SAT/UNSAT, malformed-source and hostile-source tests. It was read back from main and **executed again** against its published raw file; exact JSON agreement PASS. Unlike the Python verifier it does not independently reconstruct the 19-node resolution trace, which is instead fully specified by /507 and checked by Python.
- Logical ideal upper `q=19`, lower `q\ge13`, three simultaneous roots, one shared DAG; no discovery time charged in ideal bound. Evidence includes 16 original 3-CNF clauses, 16 explicit deletion witnesses and the 19-node proof trace already in /507. Python local raw file is 3,480 bytes; published JS file 2,648 bytes, published raw JSON 2,320 bytes. Python wall clock 0.59 s, user 0.90 s, measured maximum RSS 96,148 KiB (runtime overhead included). This is **experimental** machine usage, not FLMV time/space bound. Enumeration has at most 16×128 deletion checks each scanning at most 15 three-literal clauses, besides 128 base checks; finite verification and evidence sizes are explicit. No all-input resource claim.

## Family / theorem / encoding / known-shortcut / transfer ledger

| Family | Original encoding and size | Established lower bound, model and assumptions | Legal shortcut control | Remaining transfer |
| --- | --- | --- | --- | --- |
| Cubic-expander odd Tseitin, LSPV-3/504 | 3h/2 edge variables, 4h proper signed 3-CNF; expanded replacements produce 4h+2k clauses, encoded Theta(h log h) | exp(Omega(h)) ordinary shared-DAG Resolution (Urquhart 1987; Ben-Sasson–Wigderson 2001), under expansion; substitution backtranslation verified in /504 and /436 | 4h+2k−1 legal **declared distinct** R_bridge503 paid mixed nodes, with GF(2) | Historical RES-to-AND3 acceptance and general mixed lower bound OPEN |
| Pang random proper signed 3-CNF | n variables, 8n with-replacement signed 3-clauses, encoding O(n log n) | exp(Omega(n)) syntactic Res(PC1/F2) w.h.p., Pang arXiv:2610.00837v2 preprint | /498–/502 restricted simulations; extension algebra, branching and nonlocal gates may shorten | Fixed full R_mix341 transfer OPEN |
| LSPV-1/506–/508 SAT cancellation gadget | 7 variables, 16 signed proper 3-CNF clauses; g copies plus shared t | **new relative source essentiality 16/16**, joint binary inference lower 13; **no asymptotic hardness** | /507 source-exact 19-step shared Resolution macro (upper) | The stronger mixed grammar, other cuts and native weights not authenticated |

## Synthesis and next hard arrow

**Advance:** /507's fact that its *chosen* 19-node DAG happens to use all 16 original sources is upgraded to an **all-valid-proofs indispensability theorem** for deriving the three exposed facets, yielding a formal multi-goal **13-node** floor even when optimal derivation, reconvergence and global sharing are free. This is useful for calibrating minimum-DAG computations and prevents claiming linear independence merely from a selected proof's ancestry. Unlike /507, it proves a nontrivial **lower** bound on the minimum joint macro cost.

**Unresolved:** [P2-D1] historical grammar; [P2-C3] all-legal-rule transfer; [P2-B1] genuinely superpolynomial worst-case full mixed refutation minimum; [P2-B2] noncircular same-calculus SAT-in-P implies polynomial minimum. The main technical target remains testing historically legal native RES/AND3/LOCAL-CONVERT/DEF/join shortcuts against the relative-source invariant, rather than extrapolating this seven-variable result. No changes to R_mix341 rules/weights, all five roles, schedules or 2A/3B allocation. Root main.tex was read only by safe range; connector returned SHA `68188a24badda635a5983fda1c381cdb694fd497` but **zero content bytes**; authorized marked-region reconciliation was unsafe, so it was not modified.

**P versus NP remains OPEN.**
