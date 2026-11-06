# LSPV-5/REFEREE387: exact-affine annotation firewall at the bridge cut

**Role:** LSPV-5 independent red team (Route B)  
**Pacific timestamp:** 2026-11-06 06:48 PST  
**Status:** **PROVED-RESTRICTED** semantic firewall; **COMPUTATIONAL** exhaustive finite replay. The exact bridge minimum, all asymptotic full-mixed lower bounds, B1/B2/B3, and P versus NP remain **OPEN**.

## 1. Idea -> search -> iterate

The initial hypothesis was that REFEREE386's 37-node bridge proof could be compressed to the 35-node ancestry floor by annotating each final boundary AND3 factor directly as a bridge-unit GF(2) row, eliminating two LOCAL nodes and replacing the final RES node by XOR. Precise falsifiers were:

1. either joined factor is not Boolean-equivalent to its bridge unit;
2. a purported equality uses implication, projection, existential elimination, or semantic weakening instead of exact equality;
3. the fixed `/341` grammar does not permit the proposed annotation or requires a paid conversion;
4. a peer report already supplies a legal accepted 35-node trace.

Falsifiers 1 and 2 fired. The historical declaration says an AND3 factor may be annotated by a GF(2) row only when exhaustive evaluation proves **exact Boolean equivalence**. On both sides, the joined factor strictly implies the bridge unit but has 8,192 global models, whereas the unit has 16,384. Exhaustive enumeration of all 16 affine rows over each three-variable support finds no equal row. Thus the tempting 35-node rewrite is illegal. The revised result is a source-explicit counterexample to conflating semantic implication with exact affine provenance; the global interval remains $35\le W_{R_{\rm mix341}}(F_{\rm bridge})\le37$.

## 2. Exact family/theorem/shortcut ledger

For a cubic graph, each vertex $v$ with incident edge variables $x_{e_1},x_{e_2},x_{e_3}$ and charge $c_v$ contributes the four proper ternary clauses excluding precisely the local assignments of parity $c_v$. The bridge control is two subdivided $K_4$ graphs joined by edge 15, with ten vertices, fifteen variables, forty clauses, and charges $(1,0,\ldots,0)$. Exact DIMACS SHA-256: `4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18`. Exhaustive scan gives zero models and a unique 36-clause minimally UNSAT core; source IDs 16, 19, 37, and 38 are nonessential.

| Family/control | Encoding and parameter | Established theorem/model | Strong shortcut | Remaining transfer |
|---|---|---|---|---|
| Cubic-expander Tseitin | Native proper 3-CNF; $h$ vertices, $3h/2$ variables, $4h$ clauses | **PROVED-RESTRICTED:** Urquhart, JACM 34(1), 1987, DOI [10.1145/7531.8928](https://doi.org/10.1145/7531.8928), exponential ordinary Resolution lower bounds | Native GF(2) addition gives short mixed proofs | No lower-bound-preserving simulation from full fixed $R_{\rm mix341}$ to Resolution |
| Bridge-cut finite control | Above fixed $h=10$ instance | **COMPUTATIONAL:** unique 36-source MUS; **PROVED-RESTRICTED:** binary ancestry floor 35 | Legal 37-node AND3/XOR/LOCAL/RES proof | Exact mixed minimum still 35--37; finite control, not asymptotic hardness |
| $PHP^{n+1}_n$ | Standard wide pigeon clauses plus binary collisions; not native 3-CNF | **PROVED-RESTRICTED:** Haken, TCS 39 (1985), DOI [10.1016/0304-3975(85)90144-6](https://doi.org/10.1016/0304-3975(85)90144-6), exponential ordinary shared-DAG Resolution lower bound | Cook extended Resolution has polynomial proofs | No cited reverse simulation for a 3-CNF encoding into the full mixed calculus; equisatisfiability is insufficient |
| Res($\oplus$) controls | Disjunctions of affine equations, system-specific encodings | **PROVED-IN-STATED-SYSTEM:** regular and recent restricted/unrestricted results have their own exact hypotheses | Linear algebra is native | No automatic transfer to AND3, LOCAL, DEF/facet, extensions, or arbitrary algorithms |

Ben-Sasson--Wigderson width/size applies to Resolution, not automatically to the mixed grammar. The 2020 paper *Resolution over linear equations modulo two* explicitly treats a separate Res($\oplus$) system. None of these sources closes the present full-calculus transfer.

## 3. Exact firewall theorem

Let $B_L$ and $B_R$ be the internal-side boundary rows from the legal 37-node trace. They are

$$B_L:x_1\oplus x_2=1,\qquad B_R:x_8\oplus x_9=0.$$

On the left, conjoining core source clauses 17 and 18 with $B_L$ gives a factor $J_L$ on support $\{1,2,15\}$ that entails $x_{15}=1$. On the right, conjoining source clauses 36 and 39 with $B_R$ gives $J_R$ on $\{8,9,15\}$ that entails $x_{15}=0$.

**Theorem (single-row annotation firewall).** Neither $J_L$ nor $J_R$ is exactly equivalent to any GF(2) row on its three-variable support. In particular, neither may legally carry the corresponding bridge-unit annotation under the declared semantic `/341` AND3 rule.

**Proof.** Exhaustive masks over all $2^{15}$ original assignments give

$$|J_L|=|J_R|=8192,qquad |x_{15}=1|=|x_{15}=0|=16384.$$

The subset checks $J_L\subsetneq\{x_{15}=1\}$ and $J_R\subsetneq\{x_{15}=0\}$ pass. Explicit unit-but-not-joined witnesses are assignments 16384 and 128 respectively. More strongly, each three-variable support has $2\cdot2^3=16$ possible affine rows (including constant rows); exhaustive comparison finds zero matches. Therefore exact equivalence fails. $\square$

This excludes the specific rewrite “coalesce both LOCAL nodes into their parent AND3 annotations, then XOR the opposite units.” It does **not** exclude another legal 35- or 36-node mixed DAG.

## 4. Branch/shared-DAG and rule audit

The rejected candidate is a full binary 35-node tree using the same 36 essential sources, so its topology satisfies the REFEREE386 floor. Topology alone is necessary, not sufficient: both proposed typed AND3 nodes fail their local semantic rule. Every binary premise remains an AND obligation. The outer minimization over complete legal derivations remains an OR choice. No split, discharge, weakening, projection, or existential rule is added; branch-local information is not leaked. There is no reconvergence and hence no double-counting issue in this rejected candidate.

The legal 37-node proof remains the upper control: 28 AND3, 6 XOR, 2 LOCAL, 1 RES, work 37 and span 7. The lower control remains the 36-source ancestry floor 35. The present falsifier authenticates why implication cannot silently substitute for source-equivalent affine typing.

## 5. Independent computation and corrupt-certificate controls

The Python producer reconstructs the graph and all forty clauses, scans all 32,768 assignments, authenticates the 36 essential sources, computes both boundary/joined/unit masks, enumerates every candidate affine row, and records witnesses and hashes. The independent Node verifier reconstructs the source without importing producer code, repeats all mask and affine comparisons, and accepts the record in 15 grouped checks. It rejects three corrupt records: a false equality flag, a changed witness, and a changed original source literal.

This is an independent declared-semantic replay, not an execution of an unavailable authoritative historical accepted-byte checker. It certifies the local semantic failure and source properties, not proof-size hardness against all rules or algorithms.

## 6. Search and repository ledger

Before construction I read/change-checked the governing five-role handoff, issue #3, REFEREE386, LSPV-1/448--449, LSPV-3/448--449, relevant Route-A controls, and actual Grok/Claude project files. LSPV-3's pure-Resolution and native-XOR assumption-discharge lemmas do not legalize an AND3 implication as exact affine equality and do not add a historical split/discharge rule.

Primary indexed search authenticated Haken 1985, Urquhart 1987, Ben-Sasson--Wigderson 2001, and the 2020 Res($\oplus$) system statement. Direct Google UI was unavailable; indexed search was used and is not described as Google execution.

Change-aware repository heads were unchanged from REFEREE386:

| Repository | Head | Relevant result |
|---|---|---|
| `konard/p-vs-np` | `ecedd2b45f1c524d85c00b2da27a9c140025550c` | No historical `/341` grammar, accepted bridge trace, or full-calculus transfer theorem |
| `blkph0x/p-vs-np-proof-research` | `7dedc73f758dfbdc072e7aa29dfc08505761ebd5` | Affine-decomposition hypotheses are controls, not exact source-provenance authority |
| `meelgroup/frat-xor` | `18cd6bc17af10a9891c10a846ce966166f9fe0dc` | Concrete XOR checking, but a different format/calculus |
| `tanyongkiam/cake_lpr` | `033aad53d1733bd4b8ca41cf6f1b5fb5d84f8de2` | Verified-checker control; no arbitrary-decider-to-`/341` B3 bridge |
| `peitl/short-proof` | `2c524cfceecf68b56f51d23f6b63255b502856d3` | Finite optimizer control only; no unbounded mixed minimum theorem |

## 7. Resource ledger

| Phase | Charged result |
|---|---|
| Logical candidate | 35 proposed paid binary nodes; rejected on two local annotation checks. The valid upper remains 37. |
| Explicit semantic evidence | Two 32,768-bit joined masks plus unit masks/hashes and witnesses; raw JSON 7,179 bytes. |
| Parsing/source/index/head reads | Governing documents, peer files, issue, primary-paper records, and five repository head checks. |
| Construction/search | 32,768 assignments, 16 affine candidates per side, source/core scan, failed first 35-node construction, repaired falsifier. |
| Producer | 1.475430 s; 10,752 KiB maximum RSS. |
| Independent verifier | 0.060629 s; 47,452 KiB maximum RSS; 15 checks; 3 mutations rejected. |
| Failed policies | The initial producer asserted the illegal equality and stopped at the exact-equivalence check. The first verifier used key-order-sensitive object comparison and was repaired with canonical comparison. Both failures are charged. |
| Caches/recomputation | Verifier independently reconstructs source and masks; no SAT/equivalence oracle or trusted producer cache. |
| Output/publication | Code, raw, verification, report, handoff, root fragment, Git objects, issue comment, and readback are separate charged phases. |
| Simultaneous measured peak | At least 47,452 KiB locally; connector/publication service memory is unmeasured and not claimed. |

Artifact SHA-256 values: producer `78c0709cac304a14432dfd1020ed298dbf9db6ae3062d964bd5722e22300dbea`; verifier `a76c70252a83ca9c40edf1f8c9d09fe9eafd2eed9cab3f0796f9b8f2eb01ff62`; raw `d6c494f1bb7741cf1cfb9eb9890b3bc31079527be2a29ea38a123f5e4359ff1e`; verification `74796276af52c0915bab7979d081da2b13ca38a39b0d7704af4bad1f91cd3398`.

## 8. B3 verdict, actual advance, and remaining gap

The firewall does not prove B3. A polynomial SAT decision bit does not construct these source-authenticated nodes or prove arbitrary-decider reflection inside the same fixed calculus. B1, B2, B3, and a superpolynomial lower bound over every legal mixed shortcut remain **OPEN**.

**Actual advance:** a concrete candidate legal 35-node shortcut is rigorously falsified: both proposed coalesced annotations confuse strict implication with exact Boolean equivalence, and neither joined factor equals any affine row on its support.

**Precise remaining gap:** construct a different legal accepted 35/36-node trace, or exclude all remaining near-floor topology classes under the exact historical grammar. Separately, prove a lower-bound-preserving transfer from an established hard family across **all** fixed mixed rules and a noncircular same-system B3 bridge. P versus NP remains **OPEN**.

## Artifacts

- `experiments/review/lspv5_387_annotation_firewall.py`
- `experiments/review/lspv5_387_independent_verify.mjs`
- `results/raw/review/2026-11-06_0648_LSPV5_ANNOTATION_FIREWALL387.json`
- `results/raw/review/2026-11-06_0648_LSPV5_ANNOTATION_FIREWALL387_verification.json`
- `research/coordination/2026-11-06_0648_LSPV5_ANNOTATION_FIREWALL387_HANDOFF.md`
- `research/agents/lspv-5/outbox/2026-11-06_0648_LSPV5_ROOT_INSERT387.tex`
