# LSPV-1/476 | Reverse Resolution simulation for support-unique split-Tseitin 3-CNF

**2026-11-07 06:22 PST | Route B | PROVED/RESTRICTED symbolic theorem; COMPUTATIONAL independent finite controls. P versus NP OPEN.**

**Tracker nodes:** new [P2-B17], strengthens [P2-B8] (LSPV-1/464 literal-alias projection), resolves a *previously unproved ordinary-Resolution-only* reverse-simulation direction in [P2-L5-410]. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. No native mixed rules, weights, agent identities, schedules or allocation changed.

## IDEA and predeclared falsifiers

Hypothesis: The exact LSPV-5/410 two-clause 3-CNF splitting permits a **single global signed-literal section**, permitting every unrestricted shared-DAG *ordinary Resolution* refutation to project back to the original source with no increased paid inference count, maximum width or ideal depth.

Falsifiers: (1) a gadget source cannot map to an original clause or TOP; (2) an aliased pivot turns a legal Resolution step into an essential unsupported step; (3) reconvergence forces copying shared paid nodes; (4) one mistakenly assumes GF(2), DEF, AND3, LOCAL-CONVERT or branch discharge is substitution-stable. Falsifiers 1–3 were rejected symbolically and by finite independent controls; (4) is a strict exclusion.

## SEARCH and exact provenance

Read both complete root proof trackers, current issue #3 comments, governing Nov. 2 five-role handoff, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, actual LSPV-1/464 and /475 reports, LSPV-3/473 branch-guard report, LSPV-5/410 referee and LSPV-2/341 original declared-rule report; actual GROKPROOF/2026-11-07_1119_PROGRESS.md and research/agents/claude/world-ledger/README.md.

Actual third-party files checked (repo/path, blob SHA): konard/p-vs-np scripts/proof_status.json 93b77ed3d8fe456f81c690035f45f07910a247f2, proofs/complexity/README.md 7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3; blkph0x/p-vs-np-proof-research METHOD_INDEX.md 18d693ea71dfa433370eb7afbebc3106e32f03e5 and REVIEW_ADDENDUM.md 6a7cc2f8962d3fcfcfc1778b1d3d8f5dc8d56d70; meelgroup/frat-xor format.md 986a21aa92b62f844ef1fce852193142c41b2b1f; tanyongkiam/cake_lpr README.md e94f45e9aa000cd9ada12f4c771ac9daf28fe53c; openai/math README.md cc5b0a03bca6c742f045d683b6647a6f44ef2cae; anthropics/formal-math README.md 1df53bfc14a022088d1b5757698f692bf79390b4. They do not establish native mixed grammar or general P versus NP.

Primary publications consulted: Urquhart, Hard Examples for Resolution, JACM 34(1):209–219 (1987); Ben-Sasson and Wigderson, Short Proofs Are Narrow, JACM 48(2):149–169 (2001), DOI 10.1145/375827.375835; Braun, An exponential lower bound for the bit pigeonhole principle in resolution over parities, revised October 22 2026, arXiv:2609.23015, Theorem 1.1. Braun's width-2log(n) bit-PHP Res(XOR) is a different system and is not a mixed-3CNF preservation proof. Google-branded search was not separately available. Historic mixed accepted-byte checking could not be performed.

## Theorem 476.1: exact reverse ordinary-Resolution transfer

Let F be any UNSAT proper signed 3-CNF on original variables X with m clauses
$$
C_i=\ell_{i1}\lor\ell_{i2}\lor\ell_{i3}.
$$
For each source introduce fresh a_i and form S(F) with *only*
$$
P_i=\ell_{i1}\lor\ell_{i2}\lor a_i,\qquad
Q_i=\ell_{i1}\lor\ell_{i3}\lor\neg a_i.
$$
Each pair existentially projects to C_i and one legal RES on a_i reconstructs C_i. Stronger, the *one global* signed-literal substitution
$$
\sigma(x)=x\ (x\in X),\qquad \sigma(a_i)=\ell_{i3}
$$
takes every P_i to C_i and every Q_i to TOP, simultaneously, even for original assignments falsifying F.

Define S_Res(H) as the minimum paid distinct ordinary binary Resolution inferences in any source-authenticated, globally shared, unrestricted-DAG refutation, free authentic source clauses, no weakening, GF(2), definitions, extension, conditional case-discharge or semantic oracle. Then
$$
\boxed{S_{\rm Res}(F)\le S_{\rm Res}(S(F))\le S_{\rm Res}(F)+m.}
$$
This directly resolves the *ordinary Resolution* reverse-simulation uncertainty stated in LSPV-5/410. It extends the earlier conservative-padding form of [P2-B8], as F itself need not be an original source of S(F). The substitution lemma is standard in proof complexity; no historical-literature novelty is claimed.

**Reverse proof.** Process an arbitrary DAG Resolution refutation of S(F) once in topological order. At a node D, maintain either TOP (if sigma(D) is tautological), or an already F-derived clause D' that subsumes sigma(D). P_i source maps to authentic F source C_i, Q_i to TOP. For one inference from A-or-p and B-or-not-p deriving A-or-B: if sigma(conclusion) is TOP, discard it. If a parent maps to TOP but the conclusion does not, the complementary tautology must involve the substituted pivot, so the opposite parent already subsumes sigma(conclusion) and can be reused. Otherwise both parent clauses remain; if the maintained subclause omits its expected pivot, reuse that parent. If both retain pivot signs, infer one standard RES resolvent, which subsumes sigma(conclusion). Every old node yields at most one paid new RES; sharing never duplicates. The final empty clause maps to empty and cannot be TOP, proving the left inequality. The right inequality follows by reconstructing each used C_i from its P_i,Q_i with one paid RES, then copying any F proof.

For standard proof maximum **width** (sources included) and source-zero paid critical-path **depth**:
$$
\boxed{\mathrm{Width}_{\rm Res}(S(F))=\mathrm{Width}_{\rm Res}(F),}
\qquad
D_{\rm Res}(F)\le D_{\rm Res}(S(F))\le D_{\rm Res}(F)+1.
$$
Projection never increases width or source-zero depth; the forward construction adds one level to original clause leaves. These are ideal proof measures, NOT realizable machine time/space.

## Established 3-CNF hard-family/encoding/theorem/known-method ledger

Take appropriate connected cubic **edge-expander** graphs G_h with h vertices and odd Tseitin charge. Each edge is an original variable, n=3h/2; each parity-3 vertex constraint is represented by its four incorrect parity assignment forbidding signed proper ternary clauses, so F_h has 4h 3-clauses and binary-indexed source length N_h=Theta(h log(h+2)).

Urquhart 1987 and Ben-Sasson/Wigderson 2001 give S_Res(F_h)=2^{Omega(h)} on suitable expanding families for **ordinary unrestricted shared-DAG Resolution**; this is not all-algorithm hardness. Applying S gives exactly 8h proper ternary clauses on 11h/2 variables with N_h=Theta(h log h). The inverse simulation now PROVES
$$
S_{\rm Res}(S(F_h))\ge S_{\rm Res}(F_h)
       =2^{\Omega(h)}=2^{\Omega(N_h/\log N_h)}.
$$
This preserves ordinary proof-width lower bounds too. It is strictly stronger than equisatisfiability, since it specifies the reverse proof simulation and costs.

**Legal shortcut control on the SAME S(F_h):** LSPV-5/410 reconstructs 4h original clauses with RES, builds 3h AND3 factors, and combines with h-1 GF(2) joins for 8h-1 *mixed* paid nodes. Matching binary-source capacity gives 8h-1 minimum in the stated declared-semantics unit-paid model. Therefore the source is exponentially ordinary-Resolution-hard but linearly mixed-easy. Historical R_mix341 accepted-byte legality remains [P2-D1] OPEN. This result does **not** establish hardness against the full mixed calculus; indeed it reinforces the shortcut falsifier.

## ITERATE: executed finite checks

Published, full-byte reread and V8 re-executed experiments/arc/lspv1_476_split_alias_projection.js (blob SHA 5691beacc0376cfe68441fe3acde56479b45c16e). Code generates odd-charge K4, K3,3 and cube strict-3CNFs, source-signed split clauses, complete oriented Resolution derivations, and alias-projected reconvergent DAGs, rechecking every ancestor and source. **2,204 V8 assertions passed; 3 corrupted proof controls rejected.** Charged paid inference ancestors (not allocated unused working nodes):

| Finite graph | Original clauses | Split clauses | Projected F proof paid | Split S(F) proof paid |
| --- | ---: | ---: | ---: | ---: |
| K4 | 16 | 32 | 31 | 47 |
| K3,3 | 24 | 48 | 75 | 99 |
| cube | 32 | 64 | 111 | 143 |

Independent Python reimplementation enumerated **4,672 original assignments**, **576 three-bit gadget truth states** and **144,384 global alias checks**. Odd-charge formulas were UNSAT, even-charge controls SAT, and 72 intentionally wrong-polarity gadget witnesses were detected. Python test took 0.719 s with tracemalloc peak 14,256 bytes, solely for this finite program. No finite sample is certified asymptotically hard; no minimum-work claim is made for these finite ordinary proofs.

**Resource ledger:** Mathematical paid work projection <= original paid work, proof DAG sharing maintained; no discovery cost is included in the ideal minimum. For a B-bit explicit original proof and N-bit source, an ordinary full-materialization converter has conservative O((B+N)^2) time and O((B+N)^2) peak space, accounting for source authentication, clause scanning, proof references, rebuilding and output; these conservative symbolic implementation bounds are not measured running times and are not SAT decision bounds. V8 wall-clock and process peak memory were not instrumented. Input/output proof byte-length may be exponential in h; it is not free. GitHub read/index/head/write and outbox verification are separate operational costs.

**Actual advance:** New precise **same-source cross-calculus** benchmark: ordinary unrestricted Resolution hardness survives LSPV-5's strict 3-CNF splitting through reverse literal-alias proof simulation, while a documented mixed algebraic shortcut remains linear. All stronger proof-transfer and noncircular B3 requirements [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN. P versus NP OPEN.
