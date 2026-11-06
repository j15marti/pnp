# LSPV-5/REFEREE390: every remaining 35-node bridge proof needs a cross-cut affine block

**November 6, 2026, 09:48 PST | Route B independent red team | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

This report keeps the historical $R_{\mathrm{mix341}}$ grammar and weights fixed. It adds no split, discharge, weakening, export, or case rule. The actual advance is a necessary-condition theorem for the remaining 35-node bridge class: pure Resolution and every side-local affine-block construction are excluded. A legal 35-node proof, if one exists, must mix sources from both halves inside an affine/factor-producing subtree before the contradiction is reached.

The full interval remains

$$
35\le W_{R_{\mathrm{mix341}}}(F_{\mathrm{bridge}})\le37.
$$

## 1. IDEA -> SEARCH -> ITERATE

**Initial hypothesis.** At the 35-node ancestry floor, historical typing would force each half to export its bridge unit or affine equivalent before the halves could interact.

Falsifiers were:

1. an authenticated 35-node mixed trace;
2. a cross-half AND3 whose combined support is historically legal;
3. an XOR subtree exporting the bridge literal without LOCAL;
4. a source-once mixed tree avoiding any side-local affine partition.

**Search outcome.** The fourth falsifier survives as the exact remaining possibility. The historical /341 source says that only RES outputs clauses, AND3 forms an exact factor on combined support at most three and may annotate it by one exactly equivalent GF(2) row, and XOR consumes two rows. REFEREE389 excludes the all-RES class, but it does not imply that a mixed proof must first finish the two halves.

Primary literature and current project work reinforce the scope firewall. Braun's current DAG-like $\operatorname{Res}(\oplus)$ bit-PHP theorem is exponential in that specific proof system, not in historical $R_{\mathrm{mix341}}$: <https://arxiv.org/abs/2609.23015>. Earlier regular and bounded-depth $\operatorname{Res}(\oplus)$ results are likewise restricted. LSPV-1/452 supplies a legal proper-3-CNF affine upper compiler for complete four-clause row bundles; it does not absorb the bridge core's two incomplete boundary bundles.

**Revised claim.** Exclude every 35-node proof whose primitive affine blocks are side-local, then state exactly what a surviving proof must do. This is proved below and independently reproduced.

## 2. Fixed source and historical rules

The source is REFEREE386's 15-variable, 40-clause strict-3-CNF bridged cubic odd-Tseitin instance, DIMACS SHA-256

4f8a7e613ace4f67cd0b62204cdda2a4d8072047bd55a70da23da282e3537b18.

Its unique essential 36-clause MUS core is

0..15,17,18,20..36,39.

The left and right 18-source halves share only $x_{15}$. Each half has four complete internal parity bundles of four clauses and one incomplete boundary bundle of two clauses. The left half forces $x_{15}$; the right forces $\neg x_{15}$.

The authenticated historical rule source is

research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex,

Git blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. In the 35-node class REFEREE386 already proves that all 36 sources occur once in a full binary tree. Thus unary LOCAL and unary/definition steps, nullary steps, reconvergence, and source duplication are absent. The only relevant native rules are strict RES, binary support-at-most-three AND3, and binary XOR.

## 3. Exact mixed side closure

For every nonempty subset of each 18-source half, the producer enumerates every source-once binary tree outcome under:

- strict oriented RES on clause records;
- exact AND3 truth-table conjunction when combined support has at most three original variables;
- affine annotation only when the resulting truth table is exactly one GF(2) equation, including possible constants;
- XOR of two affine equations.

The closure is representation-aware: a clause remains available to RES; a local factor remains available to AND3; an exact affine alias is available to XOR and, when its support is at most three, to AND3. No implication-to-clause conversion is free.

For **each** side, the full 18-source closure contains:

| Outcome type | Count |
|---|---:|
| Clauses | 1,888 |
| Local factors | 5 |
| Affine equations | 0 |

The forced bridge unit is absent both as a clause and as an affine equation. No false factor or false equation occurs.

Across all proper subsets, exactly 15 source sets derive any affine equation. They are exactly the nonempty unions of the four complete internal four-clause parity bundles, and each derives exactly the XOR sum of the corresponding vertex rows. Neither boundary source belongs to any side-local affine-producing subset. Consequently, no partition of all 18 side sources into affine-producing blocks exists.

The primary enumeration performed, per side:

$$
1{,}126{,}097{,}195
$$

strict-RES pair tests,

$$
55{,}144
$$

AND3 pair tests, and 25 XOR pair tests. Wall time was 32.783 seconds with 440,548 KiB peak RSS.

A separately implemented base-3 clause engine with separately reconstructed local truth vectors reproduced all counts and the exact 15-subset classification. It used 46.863 seconds and 508,444 KiB peak RSS and rejected six hostile count/classification mutations.

## 4. Cross-cut affine-block necessity

### Theorem 390.1 (PROVED/RESTRICTED for the authenticated finite bridge core)

Every legal 35-node historical $R_{\mathrm{mix341}}$ refutation of the authenticated bridge core, if one exists, contains an AND3-produced factor or affine equation whose source ancestry includes at least one left source and at least one right source. Equivalently, no 35-node refutation can be assembled solely from side-local affine blocks followed by XOR.

### Proof

REFEREE386 gives a 36-source full binary source-once tree.

If the root contradiction is the empty clause, every ancestor is a clause: without unary LOCAL, the only rule producing a clause is RES. The whole proof is therefore pure Resolution, excluded by Theorem 389.1 and REFEREE388's exact closures.

Otherwise the contradiction is a false factor or the affine constant $0=1$. If it is produced directly by AND3, that root has ancestry from both halves because all 36 essential sources occur, so it is already the required cross-cut block.

If the root is XOR, expand its XOR-only skeleton until reaching primitive equation-producing subtrees whose roots are not XOR. Their disjoint source ancestries partition all 36 sources. Suppose every primitive block were side-local. Then the blocks on each side would partition that side's 18 sources into affine-producing subsets. The exact mixed side closure proves that no such partition exists: all affine-producing subsets omit the two boundary sources. Contradiction. Hence at least one primitive affine block crosses the cut. $\square$

This theorem counts the union of distinct nodes once. At the 35-node floor there is no reconvergence, so work, tree-node count, and the source partition coincide; no claim about minimum span or scheduled peak space follows.

## 5. Row-respecting quotient control

A stronger finite control first replaces each of the eight complete internal four-clause bundles by its authenticated vertex equation. This spends 24 AND3 nodes and leaves a 12-item quotient: eight rows plus the four boundary clauses, with exactly 11 binary nodes available.

An exhaustive strict RES+AND3+XOR closure of those 12 items finds no full-source outcome of any type:

- 5,725 AND3 pair tests;
- 16 RES pair tests;
- 3,025 XOR pair tests;
- zero clauses, factors, equations, or contradictions at the full source set.

The still smaller six-item quotient, after XOR-summing the four rows on each side, also has no full-source outcome. Thus the natural plan “derive all internal rows, remove both LOCALs, and finish algebraically” is impossible.

This quotient result is not the global 35-node theorem. A surviving proof may split at least one complete internal parity bundle, derive a cross-cut clause by RES, and feed it into AND3. That class is not enumerated globally here.

## 6. Established-family and shortcut ledger

| Family | Exact encoding / theorem | Mandatory shortcut | Status for the fixed mixed calculus |
|---|---|---|---|
| Cubic odd Tseitin | Four proper width-three clauses per cubic vertex; exponential ordinary shared-DAG Resolution on expanders | Historical AND3/XOR gives $4h-1$ nodes | Family failure for mixed hardness |
| Haken PHP | Standard unary PHP; exponential ordinary Resolution | Cook Extended Resolution polynomial proofs | No lower-bound-preserving strict-3-CNF/all-rule transfer |
| Braun bit-PHP | $n=2^\ell$ holes; exponential DAG-like $\operatorname{Res}(\oplus)$, $\ell\ge32$ | Historical DEF/AND3/LOCAL may be stronger or differently typed | Transfer remains OPEN |
| Bridge control | 15 variables, 40 strict 3-clauses, 36-clause MUS | Known 37-node proof uses 28 AND3, 6 XOR, 2 LOCAL, 1 RES | Pure RES and side-local affine 35-node classes excluded; cross-cut block class OPEN |

Certified UNSAT, restricted proof-size hardness, and empirical solver difficulty remain distinct.

## 7. Resource, provenance, and hostile-control ledger

| Phase | Charged result |
|---|---|
| Historical/project reads | Current head and issue #3; governing handoff; original /341; REFEREE386--389; LSPV-1/452; LSPV-3/455; LSPV-4/444; actual Grok and Claude files |
| Primary side closure | 32.783 s; 440,548 KiB peak RSS |
| Independent side closure | 46.863 s; 508,444 KiB peak RSS |
| Row quotient closure | 0.076 s; 10,112 KiB peak RSS |
| Logical work | Exact pair-test counts above; discovery time is not included in $W_R$ |
| Evidence | Two C++ implementations, one Python quotient checker, three JSON records, report, handoff, root fragment, exact issue outbox |
| Verification | Independent base-3 encoding; exact count/classification equality; six hostile mutations rejected |
| Simultaneous peak | 508,444 KiB for executed local verification; connector memory unmeasured |

The computation materializes all subset closures, so its memory is an implementation cost, not a lower bound on proof space. It makes no FLMV claim.

Required repository heads were change-checked: konard/p-vs-np ecedd2b45..., blkph0x/p-vs-np-proof-research 7dedc73f..., FRAT-XOR 18cd6bc1..., CakeLPR 033aad53..., and short-proof 2c524cfc.... None supplies the missing cross-cut theorem, accepted historical byte checker, or B3. FRAT-XOR and CakeLPR authenticate different proof formats.

Primary indexed search covered current DAG-like and restricted $\operatorname{Res}(\oplus)$ lower bounds. Direct Google-branded search remained unavailable. The project scratch checkout remained partial; complete governing/current files were read from GitHub. No authoritative historical accepted-byte checker was located or executed.

Pre-publication SHA-256 values are recorded in the raw manifest and handoff.

## 8. B3 verdict and precise remaining gap

This run is a finite structural narrowing. It does not compile arbitrary polynomial SAT decider traces into this fixed calculus and does not supply correctness/reflection. B1, B2, B3, full mixed superpolynomial growth, and P versus NP remain **OPEN**.

**Actual advance:** pure RES and every side-local affine-block route to 35 are excluded. Any surviving 35-node proof must create a cross-cut factor/equation before the contradiction.

**Precise remaining gap:** construct or exclude a cross-cut affine-producing subtree that splits an internal four-clause parity bundle or uses a cross-cut RES clause before AND3. Then address the three 36-node topology classes. Separately, transfer an established asymptotic lower bound through every historical mixed shortcut and prove a noncircular same-system B3 bridge.

## Artifacts

- experiments/review/lspv5_390_mixed_side_closure.cpp
- experiments/review/lspv5_390_independent_verify.cpp
- experiments/review/lspv5_390_boundary_gadget_closure.py
- results/raw/review/2026-11-06_0948_LSPV5_MIXED_SIDE_CLOSURE390.json
- results/raw/review/2026-11-06_0948_LSPV5_MIXED_SIDE_CLOSURE390_verification.json
- results/raw/review/2026-11-06_0948_LSPV5_BOUNDARY_GADGET390.json
- research/coordination/2026-11-06_0948_LSPV5_CROSS_CUT_AFFINE390_HANDOFF.md
