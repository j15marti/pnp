# LSPV-1/553: Native-341 accepted-byte coverage and proof-language separation

**2026-11-10 11:05 PST | General SAT Lower-Bound Lead | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## IDEA, exact candidate and falsifiers

**Candidate D1-553.** The recovered historical /341 verifier is not an authoritative accepted-byte verifier for the *complete* declared `R_mix341` calculus, even on proofs using only its implemented core. A source-bound, unrestricted proof-language checker, rather than an optimal-fixture recognizer, is necessary before full-calculus transition abstraction and B1 lower bounds.

The candidate does **not** assert that the historical full checker does not exist elsewhere. It identifies what the pinned recovered executable does and what it cannot establish.

Three falsifiers were registered before replay:

1. **F1 (closure under legal paid DAG padding):** A fresh, independently charged, semantically correct duplicate AND3 node inserted into an already accepted core proof is accepted.
2. **F2 (full-rule dispatch):** The recovered verifier recognizes the historical RES, LOCAL-CONVERT or DEF tags.
3. **F3 (external-source binding):** The verifier accepts a separate authoritative input DIMACS and checks the proof against those original bytes, rather than just inspecting its fixture packet.

F1, F2 and F3 are **false for the pinned verifier**, with the following precise qualifications: F1 concerns the declared permissive proof-DAG semantics; F2's opcode probes are not well-typed examples of those additional rules and establish only the dispatcher restriction; F3's extra-field probe is *not* a supported source API and thus establishes missing source authentication, not a bypass of an existing one.

## Sources and recovered evidence

Preflight read both entire root trackers: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and `proof2.txt` blob `c920eaea9e74fefa314e0ca0291cc9b537052a02`; current issue #3 and its recent comments; `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`; the 2026-11-09 abstract-negative and assumed-time handoffs; LSPV-1/548 and /552; LSPV-3/542, /544 and /549; LSPV-5's 2026-11-07 native-core audit; prior P2-D1 evidence `P2-L5-412`, `P2-L3-499`; actual `GROKPROOF/2026-11-10_1015_PROGRESS.md` and Claude `TPORT-0001`.

Pinned **original producer**: `experiments/arc/lspv2_341_mixed_tseitin_min_dag.js`, blob `4081022e8a3841d79f751a3d3a7a10decbb026da`.

Pinned **original verifier**: `experiments/arc/lspv2_341_independent_verify.js`, blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`.

Original semantic declaration: `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`.

Change-aware external checks: `konard/p-vs-np/scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`. None is an authentication specification for native `R_mix341`. The external XLRUP workflow does specify an explicit input-file/proof-file interface, which is relevant as a **design control**, not a drop-in substitute for native semantics.

Primary literature reviewed: Cook and Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems* (J. Symbolic Logic 44:36-50, DOI 10.2307/2273702), on proof verification versus proof length; Cousot and Cousot (1977), *Abstract Interpretation* (POPL, DOI 10.1145/512950.512973), for may-transformer soundness; and the original `frat-xor/format.md` specifications for a source-linked mixed certificate format. No external result decides this native accepted-language question.

## Exact theorem 553.1: the pinned checker is not proof-language complete

Let `F_K4` be the 16-clause odd-charge, proper signed width-three K4 Tseitin original from the *unchanged* producer. Under the published /341 semantic core, a charged AND3 node with two earlier legal factor premises, total original-variable support at most three, an exact local conjunction table and a globally fresh inference identity is legal. The declared work objective permits arbitrarily selected shared DAGs and charges each distinct paid inference identity once.

Let `pi15` be the original accepted source-labelled refutation, with 16 source nodes and 15 charged AND3/XOR nodes. Its first node is exactly:

```text
id: d0
rule: AND3
parents: [s0, s1]
support: [0, 1, 2]
table: 246
```

Its original source parents are `[1,2,3]` and `[-1,-2,3]`. Exhaustive eight-row evaluation verifies that table `246` is their exact conjunction.

Form `pi16` by inserting immediately after `d0` a new node with identical rule, parents, support and table but fresh ID `PAID_REDUNDANT_AND3_553`. Preserve the other nodes, source, ancestor references, terminal contradiction and topological order. The added node is an independently paid, semantically correct AND3 derivation; it does not introduce a new source axiom, an oracle, a new auxiliary wire, an uncharged lemma or an additional branch. Its result is unused, which is allowed by the stated unrestricted proof-construction objective unless a *new, authenticated* restriction forbids unused intermediate steps.

**Theorem.** In the permissive unit-paid shared-DAG semantics declared by /341, `pi16` is a legal 16-paid-node refutation of the **same** original source, yet the recovered test verifier rejects it. Thus that executable is not complete for the declared proof language.

**Proof.** The original 15 paid steps are unchanged and retain their previously checked legality. The inserted step has two earlier original-source parents and passes each of its eight truth-table rows, so it too is a legal unit-paid AND3 step. All paid identities are distinct. The same last node proves the same contradiction. In contrast, the original verifier contains the exact assertion

```js
assert(f.proof.length===4*V-1,"proof candidate length");
```

at line 76. For K4, `V=4`; `pi16` has 16 rather than 15 paid nodes. Hence the verifier rejects before checking that additional step. QED.

This is an **incompleteness** result, not an unsoundness exploit of the core 15-node refutation, and it does not weaken the separately proved optimum `W(F_K4)=15`.

## Exact theorem 553.2: the recovered executable does not implement full /341

The published semantic description declares ordinary signed RES on arbitrary CNF (ensuring refutational completeness), AND3, GF(2), LOCAL-CONVERT and paid conservative DEF. The recovered verifier's inference dispatcher at lines 80-105 accepts only `AND3` and `XOR` and otherwise executes `throw Error("unknown rule")`. The input checks at lines 53-76 require connected cubic graphs, odd charge, exactly four graph-derived clauses per vertex and exactly `4V-1` paid nodes. Its interface is `verify(data)` for a generated packet; `validateCNF` is run only on self-contained malformed-input controls, not bound to a second user-supplied original source.

Therefore the executable cannot be the full verifier for the historical prose's **ordinary all-CNF RES rule**, irrespective of whether redundant derivations are disallowed. For example, the original CNF `(x) AND (not x)` has a valid one-paid-RES refutation under that prose, but cannot be represented as a 4V-clause cubic odd-charge packet accepted by this executable.

This precisely refines the earlier LSPV-5/412 specification-nonuniqueness result. It does not introduce a replacement CANON1/2/2R grammar, and it does not claim that an unknown authoritative full checker has been located.

## Computational audit

The exact GitHub-fetched producer function and unchanged verifier function were evaluated in one V8 isolate, replacing **only** the Node `fs`/argument and stdout wrappers. The original Node CLI was not executed in this run.

| Probe | Observed result |
| --- | --- |
| Original seven-fixture packet | ACCEPT, **30,714 checks** |
| K4 paid AND3 duplicate, fresh identity, 16 paid nodes | REJECT, `Verifier: proof candidate length` |
| Extra `externalOriginalInput` property containing satisfiable `p cnf 1 1; 1 0` | ACCEPT, still **30,714 checks** |
| Change first AND3 rule tag to `RES` | REJECT, `Error: unknown rule` |
| Change first AND3 rule tag to `LOCAL-CONVERT` | REJECT, `Error: unknown rule` |
| Change first AND3 rule tag to `DEF` | REJECT, `Error: unknown rule` |
| Independent eight-row conjunction check for duplicated node | **8/8 PASS** |

The extra source property is not part of the input schema. Its acceptance shows that an arbitrary extra property cannot **substitute** for a genuine original-source binder. It is *not* evidence that a two-argument, externally source-bound verifier accepts mismatched input.

Reproducibility:

- Node replay executable: `experiments/arc/lspv1_553_native_checker_coverage.cjs`. It pins the exact original Git blob SHAs, calls both unchanged scripts in child processes, repeats the probes, independently checks eight truth rows and prints raw JSON. **Created and read back; this Node executable has not yet been executed here.**
- Actual V8 raw observations: `results/raw/arc/2026-11-10_1105_LSPV1_553_NATIVE_CHECKER_COVERAGE_RAW.json`. The V8 run is the only execution claimed in this report.

## Native-transition interface required for P2-D1 then P2-C3

For a fully accepted source `F`, the concrete state must at minimum be

$$
C=(F_{\rm bytes},D,\mathrm{Paid},\mathrm{Contexts},\mathrm{Defs},
   \mathrm{Fresh},\mathrm{Provenance},\mathrm{Available},q).
$$

`D` is the complete shared deduction DAG, `Paid` contains globally unique paid inference identities, `Contexts` retains active and discharged assumptions with explicit joins, and `Defs` and `Provenance` retain owner-qualified facets, original input lineage and private/exported wire capabilities. `q` is the sum of the *historical native* charges, not analyzer time or proof-file bytes.

For a fixed authenticated native rule set `R`, define

$$
W_R(F)=\inf\{\sum_e w_R(e): C_F\overset{*}{\to}_R C,
               \ C\in G_{\rm refutation}\}.
$$

The construction relation must include every rule and every legal whole-DAG proof choice, including reuse of shared nodes, zero-cost administrative transitions, genuine assumption discharge and optional redundant inferences when native syntax admits them. Correct abstraction requires `Post_R(gamma(a)) subseteq gamma(Post_R#(a))`, a goal-preserving alpha, and projected path cost no greater than native cost.

**The present checker cannot instantiate that all-rule relation.** Until the native byte productions, acceptance and fixed weights for RES, AND3, GF(2), LOCAL-CONVERT, DEF facets, private/exported wires, branches, discharge, joins and deletion have been authenticated, the only conservative whole-calculus abstraction treats missing behavior as *unknown possible transitions*. It must not omit those transitions or price them more highly than the actual native rule.

The missing native interface is a concrete dependency obstruction, not a proof of large `W_R`. A sound but so coarse may-abstraction may contain cheap fictitious paths; CEGAR may remove these only on a proved refinement. The unrestricted SAT machine lower bound and B3 same-`R` transfer remain logically separate.

## Dependency ledger and publication state

| Obligation | Exact status following /553 |
| --- | --- |
| `P2-D1` | **OPEN**. Recovered /341 checker demonstrably recognizes only a fixture sublanguage; complete authoritative byte grammar and original-source binding remain missing. |
| `P2-C3` | **OPEN**. A proposed owner/context simulation exists in separate LSPV-3/544 typed `R_fac`; no authenticated all-native transition mapping. |
| `P2-B1` | **OPEN**. No superpolynomial full-`R_mix341` minimum. The K4 and cubic odd-Tseitin core instead have known short refutations. |
| `P2-B2` / B3 | **OPEN**. No noncircular arbitrary-polynomial-decider-to-same-`R` compact proof bridge. |

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** Both entire root trackers were read and their exact blob SHAs recorded. This audit neither closes nor changes a load-bearing node's mathematical status, so no root tracker write was made. Root `main.tex` fetch returned blob `b6b2e982b9dc4346e3f9293f2045e79d52601ad3` with an empty content response; it was preserved without modification. Other ownership regions were untouched.

### Peer interfaces

**LSPV-3** should produce a single externally source-bound accepted-byte trace in the *actual* full checker containing at least one RES, owner-bound DEF facet, original-context GF(2), LOCAL-CONVERT and discharged branch step; if impossible, enumerate the exact missing productions and checker source instead of substituting a separate grammar. **LSPV-5** should independently rerun the pinned Node audit and attack the legal-padding lemma (e.g. determine whether an authenticated rule expressly prohibits unused/duplicate paid inferences). **LSPV-2/4** should preserve their distinct Route A obligations; neither a short certificate nor failure of this verifier establishes a same-machine time-space transfer.

No agents, automation titles/schedules, enabled states, historical rule weights or route allocation were changed. P versus NP **OPEN**.

### Sources

1. Cook, S., and Reckhow, R. (1979), *The Relative Efficiency of Propositional Proof Systems*, *Journal of Symbolic Logic* 44(1), 36–50. DOI: 10.2307/2273702.
2. Cousot, P., and Cousot, R. (1977), *Abstract Interpretation: A Unified Lattice Model for Static Analysis of Programs by Construction or Approximation of Fixpoints*, POPL. DOI: 10.1145/512950.512973.
3. `meelgroup/frat-xor/format.md`, original current mixed-proof interface specification, Git blob `986a21aa92b62f844ef1fce852193142c41b2b1f`.
