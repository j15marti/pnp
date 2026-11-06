# LSPV-1/441 | Paid GATE-LOCAL boundary refutation composition
**2026-11-06 01:57 PST | Route B | PROVED/RESTRICTED conditional typed simulation + COMPUTATIONAL finite replay. Historical R_mix341 acceptance, B1/B2/B3 and P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE; exact falsifiers
Hypothesis: LSPV-5/REFEREE381's polynomial guarded odd-Tseitin derivation can eliminate *unpaid owner-facet references* by composing the existing LSPV-3/441 paid GATE-LOCAL compiler, preserving original-source proof ancestry and with fully charged facet-emission work. Falsifiers: F1 an indexed facet is not an 8-row implication of its paid DEF relation; F2 a RES step or GF(2)/AND3 row breaks after the replacement; F3 extra paid facets are duplicated or dead, or corrupt sources accepted; F4 the historical /341 rule does NOT accept DEF objects as LOCAL antecedents. F1-F3 were tested within a **separately declared GATE-LOCAL completion**; F4 remains **OPEN**.

Sources actually reviewed: governing five-role handoff c3889a3e; live issue #3; historical /341 c87acd11; /439, /440; LSPV-3/436 and /441; LSPV-5/REFEREE381 and its **actual 221,850-byte raw proof fixture** (blob d8ef987a201904a7f828c94e9bb195cee66a6a41); AGENTS.md, CODEX.md, repository skill; GROKPROOF/2026-11-06_0515_PROGRESS.md and Claude world-ledger. Both required outside repositories were inspected at scripts/proof_status.json (konard, blob 93b77ed3), METHOD_INDEX.md (blkph0x, blob 18d693ea), with explicit proof limitations; checked FRAT-XOR format (986a21aa), CakeML/LPR README (e94f45e9), short-proof README (93d2090d), and openai/math README (cc5b0a03). Web indexed primary research included Urquhart 1987, Ben-Sasson/Wigderson 2001, Cook/Reckhow 1979 and Pich/Santhanam JACM 2026. No Google-branded search or historical native checker was available.

## Exact established family and applicable lower bound
Let $G_h$ be a connected simple cubic graph with $h$ even vertices and one charge-one vertex $v_*$. The standard odd Tseitin formula has one edge bit per edge, $3h/2$ bits, and four signed distinct-variable three-clauses for each vertex, encoding $\bigoplus_{e\ni v}x_e=\chi_v$; altogether $4h$ clauses. Sum of all vertex rows gives $0=1$. For constant-degree expander sequences, Urquhart (1987) and Ben-Sasson/Wigderson (2001) imply $\exp(\Omega(h))$ ordinary unrestricted *DAG Resolution* refutations, **not** R_mix341 or all-machine hardness.

The established positive-guard strict-3 construction /435-/436 replaces every $C=(a\vee b\vee c)$ by $(g\vee a\vee y_C)\wedge(\neg y_C\vee b\vee c)$ and adds four proper-three clauses $(\neg g\vee p^s\vee q^t)$ over all polarities of fresh $p,q$. This yields $8h+4$ source clauses and $11h/2+3$ source variables; when $g=0$ its existential projection is the original Tseitin formula. The earlier /435 lower-bound-preserving substitution/restriction (not equisatisfiability alone) applies to ordinary Resolution. Known paid GF(2), ER and branch/shared-DAG shortcuts remain upper controls.

## Theorem 441.1: paid-facet composition (defined completion, not historical certification)
Specify **GATE-LOCAL** as a sound extension reading a paid two-input DEF relation itself as an antecedent to a unit-paid LOCAL-CONVERT implication over its three wires. For each globally shared edge owner $w_e=(\neg g)\wedge x_e$, independently derive these **three unit-paid LOCAL nodes**:

$$
(\neg w_e\vee\neg g),\qquad
(\neg w_e\vee x_e),\qquad
(w_e\vee g\vee\neg x_e).
$$

Each implication is verified by all eight assignments on $(g,x_e,w_e)$. The original REFEREE381 used references N#f0/1/2 attributed to the paid owner but did not pay for their separate LOCAL export. Replace every such reference with the unique added LOCAL node, **one per owner and facet**, preserving every original RES pivot, AND3 factor, XOR row, original-source byte identity, shared-DAG reconvergence, and final empty clause. No split/discharge/weakening or semantic oracle is introduced. All original and new nodes remain live ancestors. This is composition of *previous* /381 and /3/441 lemmas, not claimed as an independently new proof-system theorem.

For $h$ vertices, $D=3h/2$ shared DEF owners and exactly $3D=9h/2$ facet LOCALs. The exhibited cost is

$$
W_{\mathrm{GATELOCAL}}(K(F_h))
\le \left(\frac{51h}{2}+6\right)+\frac{9h}{2}
=\boxed{30h+6}.
$$

The bound is **CONDITIONAL** on that exact GATE-LOCAL grammar, **not** a proven historical R_mix341 upper bound or an exact minimum. A serialized left-fold row sum in the available traces has span $h+11$, and a balanced schedule gives an *exhibited possible* span at most $13+\lceil\log_2(h-1)\rceil$ under unit-latency unlimited processors. The abstract $h$-family proof remains conditional until an authoritative historical checker accepts the exact translated proof syntax.

## Actual original-source and adverse finite verification
Read the full REFEREE381 source-authenticated K4/K3,3/cube raw instances by connected GitHub at blob d8ef987a. The independent fresh JS/V8 transformation generated **all 3 facets per DEF** and substituted every owner reference in the original complete proof. A rule-by-rule validator checked full original DIMACS source multiset, all source leaves in the root ancestry, every newly paid gate facet's 8-row implication, correctly oriented RES, each at-most-three-variable AND3 factor and affine annotation, XOR additions, parity LOCAL implications and an empty root. 18 deliberately corrupted originals or translated certificates were rejected (6 per graph). The checker was an independent implementation of the **declared** grammar, not the historical parser.

| Control | $h$ | Source clauses | /381 nodes | Added paid LOCAL | GATE-LOCAL paid nodes | Serial span | Rule checks |
|---|---:|---:|---:|---:|---:|---:|---:|
| $K_4$ | 4 | 36 | 108 | 18 | **126** | 15 | 838 |
| $K_{3,3}$ | 6 | 52 | 159 | 27 | **186** | 17 | 1,229 |
| Cube | 8 | 68 | 210 | 36 | **246** | 19 | 1,620 |

All 36/52/68 original source clauses were live. Exact rule-check count groups are from independently executed JS/V8, not a formal checker proof. The upstream independent verification retained odd-charge UNSAT, even-charge SAT witnesses, malformed controls and structural corruptions; this run independently rejected source-clause corruption as well.

## Work, span, evidence, resources and safety
Node weights remain one for every DEF, LOCAL, RES, AND3, XOR. Each edge DEF and each distinct facet is paid **once**, shared across both incident vertices and every downstream branch. Total distinct proof nodes $30h+6$ are NOT computational time; proof selection is free only for the minimum, not for producing this certificate. Added facet emission requires $O(h)$ constant-size truth tables and source/head reads. Explicit boundary proof evidence is $O(h\log(h+2))$ bits for bounded-degree indexed families. The original three traces serialized to 13,997/20,937/27,918 JSON characters; expanded traces approximately 15,383/23,034/30,738 (serialization format dependent). Source reads, JSON parsing, transfer, failed policies, emitted bytes, cross-references, checking, caches, retained DAGs and all-phase peak must be charged for any actual machine upper bound. The connected V8 service did not expose process RSS, transfer cache size or same-machine Turing-machine cost; these are **unmeasured**, not inferred. Retaining all $O(h)$ nodes implies $O(h\log h)$ abstract reference bits in a standard explicit representation, but no experimentally verified FLMV space exponent.

## Exact remaining transfer and B3
The historical /341 document fixes a semantic LOCAL rule from already-derived **local factor/equation**, and a paid conservative DEF whose relations are owned at the definition node; it **does not unambiguously specify** whether a DEF owner itself is an admissible LOCAL antecedent, how ports are typed/exported, or exact byte serialization. FACET-A versus GATE-B acceptance fork (/3/436) remains unresolved. The composition removes the need for *unpaid indexed facet references*, not the need to authenticate **DEF→LOCAL as native**. No historical execution or unauthorized rule/weight revision is claimed.

B1, B2 and the weakest sufficient noncircular B3 remain

$$
\mathrm{SAT}\in P
\ \Longrightarrow\
\overline W_{R_{\mathrm{mix341}}}(N)=N^{O(1)}.
$$

Even if the GATE-LOCAL completion is native, one linear easy family does not establish B3. A genuinely superpolynomial worst-case minimum over **all** legal rules of the same historical R is also OPEN. P versus NP OPEN.

References: Urquhart 1987 DOI 10.1145/7531.8928; Ben-Sasson/Wigderson 2001 DOI 10.1145/375827.375835; Cook/Reckhow 1979 DOI 10.2307/2273702; Pich/Santhanam JACM 2026 DOI 10.1145/3801091.
