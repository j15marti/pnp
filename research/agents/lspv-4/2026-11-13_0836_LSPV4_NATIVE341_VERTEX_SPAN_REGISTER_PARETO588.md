# LSPV-4/588: Exact all-fixture typed local-parity span versus retained-register frontier

**November 13, 2026, 08:36 PST | PNP Time-Space Resource Auditor | Historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## Candidate theorem and four falsifiers fixed before the audit

For every original signed cubic-Tseitin fixture with V vertices, within the properly typed numeric-array-support SOURCE/AND3/GF(2) local-parity tree language, with 4V signed SOURCE clauses, original /341-mandated 4V-1 binary paid records, read-only source leaves, no recomputation and atomic paid-result last-use overwrite, the exact (logical span, retained paid registers) Pareto frontier depends only on V and is both calculable by a finite recurrence and attained by concrete original-checker-accepted certificates.

F1: authentic /341 rejects a proposed frontier witness, or signed sources, deletion witnesses, costs or references change. F2: a legal typed tree beats the recurrence. F3: legal GF(2), paid extension, sharing, recomputation or compact representation defeats a universal mixed-calculus extrapolation. F4: a checker-accepted SAT source is wrongly treated as sound UNSAT. F1 was excluded on the tested seven original sources by 22 complete authentic hosted-V8 replays and five hostile controls. F2 is excluded by the recurrence proof and an independent brute enumeration for V=1 through 8. F3 and F4 are preserved as full-calculus scope limitations, NOT ruled out.

## Theorem 588.1 and proof

Let \(P_v\) be the Pareto-minimal pairs \((d,r)\) attainable by joining \(v\) complete local four-clause parity rows, where \(d\) is binary paid inference depth and \(r\) is the minimum number of simultaneously live atomic paid-result registers in a source-read-only, no-recomputation, in-place last-use model. Each local AND3 quartet has two nondominated binary associations, comb \((3,1)\) and balanced \((2,2)\). For any two subexpressions define

$$
J((d_1,r_1),(d_2,r_2)) =
\left(1+\max(d_1,d_2),
\max(r_1,r_2)+{\bf 1}_{r_1=r_2}\right).
$$

Then exactly

$$
P_1=\{(3,1),(2,2)\},\qquad
P_v=\operatorname{ParetoMin}\Bigl\{
J(a,b):1\le k<v,\ a\in P_k,\ b\in P_{v-k}
\Bigr\}.
$$

**Proof.** The original checker forces every one of its 4V original SOURCE leaves to lie in the terminal ancestry with exactly 4V-1 paid binary steps. By previous LSPV-3/598 all-accepted-packet rigidity, that ancestry is a full binary tree, with no shared source or paid result. In the declared typed numeric-support sublanguage, two distinct cubic vertices have distinct incident-edge support triples whose union is at least five, violating AND3 maximum support three. A local partial conjunction of one, two or three of its four forbidden assignments has respectively seven, six or five satisfying assignments on the local three bits and cannot be an affine parity row. A conjunction of all four has four models and produces precisely its local parity row. Therefore all cross-vertex joins are XOR joins of complete local AND3 quartets. Each quartet has either the comb or balanced two-coordinate resource type.

For any paid binary tree node, logical span is \(1+\max(d_1,d_2)\). The optimal in-place last-use slot requirement is the classical register recurrence: \(\max(r_1,r_2)\) when child ranks differ and \(r_1+1\) when equal. The higher-ranked subtree must be computed first when ranks differ. An induction over a split into k and v-k local rows enumerates every binary XOR association; monotonicity of the join permits removal of dominated children. Every surviving pair has an explicit witness association and source-local AND3 trees, all accepted by the original checker on the seven historic sources. This proves exactness within the declared model. The result does not cover noncanonical String supports or historically missing mixed rules.

## Exact attainable frontier

| V | Pareto pairs (logical span, atomic paid registers) |
|---:|---|
| 4 | (6,2), (5,3), (4,4) |
| 6 | (8,2), (6,3), (5,4) |
| 8 | (10,2), (6,3), (5,5) |
| 10 | (12,2), (7,3), (6,4) |
| 12 | (14,2), (7,3), (6,4) |
| 32 | **(34,2), (11,3), (8,4), (7,7)** |

For \(V\ge2\), global minimum inference depth is \(2+\lceil\log_2 V\rceil\). The optimal two-register comb has depth \(V+2\). At the original PRISM16 source (V=32), the original-checker-accepted 7-layer realization and its 34-layer two-register counterpart both have **127 paid deductions** and **254 paid-parent applications**. Thus an abstraction that uniformly charges 34 span layers to this native fixture **overcharges the accepted 7-layer proof**. Both endpoints and intermediate frontier points are realized by actual checker-accepted certificates.

## Audits and same-realization accounting

The unchanged original /341 checker (Git blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0) was executed in hosted V8 using only file/console adapters on rebuilt certificates from the original corpus (Git blob fe27fe1011d0021e721ccaeb747ed58da65d7464). The generator changed only the proof-tree topology; every fixture retained its original signed SOURCE, graph, charges, deletion witnesses and even witness. Results: **22/22 native positives**, **163,012 aggregate native assertion groups**, **5/5 hostile full-packet rejections** (forged parent, bad AND3 table, bad XOR sink, malformed signed SOURCE and invalid deletion witness). Source graphs: K4, K33, CUBE, PETERSEN, PRISM6, PRISM16 and BRIDGE_K4x2. The independently OS-executed Python 3 checker reproduced every DP Pareto point and independently enumerated all binary tree association resource pairs for V=1 through 8.

The published Node runner supports a separate --os replay of all 22 checker cases in original Node subprocesses, but this OS replay **was not executed in this run**. No repository-wide preflight or LaTeX compilation is claimed.

The logical charge is exactly 4V-1 distinct paid **occurrence records** in this restricted original-checker grammar and reference/application count 8V-2. Every computed frontier point is backed by one concrete accepted realization; the raw evidence records its own compact UTF-8 packet bytes, which are NOT constant across frontier variants. The Pareto claim concerns only logical depth and abstract paid-register retention. It is not a joint optimum over bytes, physical RAM or verifier time. Original input parsing, UTF-8, reference-digit length, retrieval, source access, incremental scratch, parallel processor demand, recomputation, genuine shared proofs, branch contexts, exported/private wires, discovery time, and full sequential bit-operation verification costs remain unbounded/unmeasured by this two-coordinate audit.

The original /341 checker has an independently source-bound SAT-source acceptance defect (LSPV-3/615). A native accepted packet is therefore not automatically a sound logical UNSAT refutation. The separately authenticated /386 checker allows genuine shared DEF/RES DAGs and arbitrary free facets; they cannot be excluded from the target full native calculus. No general SAT machine lower bound, full \(W_{R_{\mathrm{mix341}}}\) bound, or P versus NP proof follows.

## Provenance and literature

Read both root trackers (proof1.txt current blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343; full proof2.txt blob 930c5eeddafce656717f28055a7a9a755f44737c), issue #3 and latest comments, AGENTS.md, CODEX.md, the pnp-research skill, current handoffs, role LSPV-4/539, 543, 545, 548, 549 and 579–587, peer LSPV-3/598, 615 and LSPV-2/601, original checker and seven-fixture source. Earlier tree rigidity and K4 Pareto are explicitly credited; the incremental result is the exact all-vertex DP, independently tested and originally checker replayed. Primary scholarship: Sethi and Ullman (1970), https://doi.org/10.1145/321607.321620; Appel and Supowit (1987), https://doi.org/10.1002/spe.4380170607; Cousot and Cousot (1977), https://doi.org/10.1145/512950.512973.

Executable: experiments/arc/lspv4_588_all_vertex_span_register.cjs. Independent Python: experiments/arc/lspv4_588_independent_dp.py. Raw: results/raw/arc/2026-11-13_0836_LSPV4_588_TYPED_VERTEX_SPAN_REGISTER_RAW.json. Five-role handoff: research/coordination/2026-11-13_0836_LSPV4_VERTEX_PARETO_FIVE_ROLE_HANDOFF588.md.

**TRACKERS REVIEWED; NO MATERIAL LOAD-BEARING CHANGE.** P2-D1 -> P2-C3 -> P2-B1 remain OPEN; P2-B2/B3 separately OPEN; P1-01/03/04 and P versus NP OPEN. Exactly five existing roles, original Pacific schedules, two Route A/three Route B labels, ownership and historical rule weights unchanged.

**Next priority:** obtain a truly historical single mixed-rule dispatcher and one source-authenticated RES-to-AND3 or paid DEF-to-LOCAL-CONVERT native transition, then extend cost-sound, concrete-inclusive shared-DAG resources without discarding genuine shortcuts.
