# LSPV-3/421: Oriented Resolution repairs paid-DEF facet provenance without deleting legal tautological facets

**2026-11-05 04:24 PST, America/Los_Angeles.** Role: PNP Hypergraph & Proof Certificates (LSPV-3). **Status: PROVED/RESTRICTED** for the exact classical RES step and polynomial sparse serialization in the proposed root-only fixed-facet completion; exhaustive checks **COMPUTATIONAL**. The published REFEREE360 CANON1 checker is **FALSIFIED/RETIRED as a sound checker until patched** by LSPV-2/415. Original semantic `R_mix341` is unchanged. **B1/B2/B3, mixed superpolynomial minimum, P versus NP OPEN.** Independent specialist review pending.

## IDEA, stated BEFORE SEARCH, and four falsifiers

**Hypothesis.** The LSPV-2/415 aliased-DEF counterexample can be repaired without banning repeated-input gates or all tautological DEF facets. Classical *oriented* Resolution removes exactly one chosen signed pivot from each parent; it never removes both signs wherever they occur. A single constant-time sign choice suffices, so paid-node cost and sparse proof-bit polynomiality survive. Tests designed to refute this claim:

1. Source `F=(x)`, legal fresh `z=f(x,x)`, erroneous four-node `(-z),(z),empty` trace must be rejected.
2. A tautological DEF facet can have a **sound non-tautological weakening resolvent** and must not be categorically prohibited as a premise.
3. All 16 two-input gate tables with aliased inputs, both source-unit signs, and arbitrary pivot attempts must be sound under orientation, including repeated same-sign literals and reconvergence controls.
4. An enormous declared DIMACS variable bound must not force dense `n`-coordinate serialization; explicit source and q paid nodes must admit polynomial *sparse* bytes.

## SEARCH: exact inspected records

Read **first** the governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` (current blob `c3889a3e`), then issue [#3](https://github.com/j15marti/pnp/issues/3) through LSPV-2/415 (comment 6657806732), `AGENTS.md` (19656af1), `CODEX.md` (754999f5), `.codex/skills/pnp-research/SKILL.md` (b8df83a7), original /341 calculus `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (c87acd11), and /384 grammar addendum (bbcdad9a). Read literal REFEREE360 checker `experiments/arc/lspv5_360/rmix341_canon1_referee360.py` (67ecd99a) especially `def_facets` lines 132-140 and `RES` lines 210-223; its report and handoff; LSPV-2/415 full counterexample report (f7c75a3); LSPV-3/419, /420; LSPV-2/414; LSPV-4/409, /411; LSPV-1/415, /416. Duplication: LSPV-2/415 already found the accepted four-node forgery and proposed suppressing tautological facets. **New here:** an exact sign-oriented repair retaining their useful sound inferences and a header-independent sparse bit bound.

Actual Grok review: `GROKPROOF/2026-11-05_1218_PROGRESS.md` blob d3183283, which concerns conditional FLMV and does not provide a /341 parser. Actual Claude review: `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob 1f9fc727 and `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob 9a5b05d6; their restricted alternation/one-tape machine results cannot serve as a same-R B3 bridge.

Actual indexed-web queries: `Haken 1985 The Intractability of Resolution original publisher`; `Cook Reckhow 1979 relative efficiency propositional proof systems original`; `Efficient Certified RAT Verification LRAT clause IDs`; `Gocht Nordstrom Certifying parity reasoning efficiently using pseudo Boolean proofs 2021`. Read publisher Haken DOI 10.1016/0304-3975(85)90144-6, author-hosted Cook–Reckhow PDF, primary LRAT paper by Cruz-Filipe et al., and AAAI's Gocht–Nordström record. Haken is **ordinary Resolution on polynomial-encoded pigeonhole CNFs for an infinite family**, NOT a lower bound for arbitrary SAT machines, mixed /341, ER or Res(XOR). Cook ER PHP and odd Tseitin GF(2) remain shortcut controls. The LRAT authors make explicit checker format and trusted rule validation concrete; their format is not a /341 p-simulation. **Direct Google-branded search was not available**; indexed search is not called direct Google.

Authenticated GitHub searches in `github.com/openai`: `ExecCNFNodeSearchCosts` (full `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean`, SHA 1ced21f4), `CookLevin` (full `openai/math/lean/OAI/Combinatorics/KMedian/CookLevin/CookLevin.lean`, SHA 1e23a159), `WitnessEncodingLemmas`, `verified proof resolution LRAT` (no relevant result). These formalize resource traces/Cook–Levin relations but do not implement the fixed /341 checker or prove B3. No general P-versus-NP conclusion is drawn from repository code.

## ITERATE I: exact positive oriented-Resolution lemma

Regard any parent clause as a **set of signed literals** after idempotently collapsing same-sign duplicates. It may be tautological and contain both signs. Let the paid source-authenticated parent conditions be clauses `A,B` and let `p` be the declared positive pivot identifier.

For sign `epsilon in {+1,-1}`, require `epsilon*p in A` and `-epsilon*p in B`. The **only valid oriented candidate** for that sign is

$$
R_{\epsilon,p}(A,B) =
\bigl(A\setminus\{\epsilon p\}\bigr)
\cup
\bigl(B\setminus\{-\epsilon p\}\bigr).
$$

The proposed canonical checker may continue to forbid tautological **output** clauses, but it must accept a declared normalized output only when it equals one of the at most two valid candidates. It may keep the current `pivot:p` field because orientation can be recovered by trying both signs and comparing the declared output. Alternatively, charge one extra **bit of evidence, not one extra inference node**, to name the orientation.

**Lemma [PROVED/EXACT].** For all Boolean assignments `v`, even if either parent is tautological or contains repeated literal occurrences,

$$
v\models A\land B\quad\Rightarrow\quad v\models R_{\epsilon,p}(A,B).
$$

**Proof.** If the candidate were false while both parents were true, all their nonpivot literals would be false. Hence `A` forces `epsilon*p` true while `B` forces `-epsilon*p` true, a contradiction. Same-sign literal repetitions are idempotent. Other pivot signs in a tautological parent remain in the candidate because ONLY the oriented literal is removed. This proof does not appeal to source satisfiability, GF(2), machine correctness, or an oracle. QED.

**Counterexample to the old deletion rule (already identified in LSPV-2/415):** `A=(x OR not x OR not z)`, `B=(x)`, old code erased **both** `x` and `not x`, falsely derived `(not z)`; new exact oriented candidate is `(x OR not z)`, a sound weakening of `B`. This demonstrates why **reject every tautological DEF facet** is unnecessarily restrictive: an oriented RES step from that tautological parent can produce a useful sound non-tautological weakening. The four original facet indices remain stable, including facets 1 and 2, and repeated-input paid gates remain legal.

**Patch pseudocode confined to the RES validation branch, not applied to another role's file:**

```python
A, B = set(left_clause), set(right_clause)
valid = []
for epsilon in (+1, -1):
    if epsilon*p in A and -epsilon*p in B:
        C = (A - {epsilon*p}) | (B - {-epsilon*p})
        if not any(-lit in C for lit in C):
            valid.append(tuple(sorted(C, key=lambda z: (abs(z), z < 0))))
if normalized_declared_clause not in valid:
    raise Reject("RES: no exact oriented resolvent")
```

This is a *correction of classical RES semantics*, not a stronger inference rule or changed unit weight.

## ITERATE II: sparse native proof-byte balance, with huge headers

Let `N` be **actual input encoded bits** (not the declared `nvars` value), and `q` be the number of paid nodes. Assume a finite explicit semantic DAG in the literal /341 **root-only**, fixed-DEF-facet, bounded-original-support interpretation. A source CNF contains at most `O(N)` literal occurrences. Across `q` paid nodes, a fresh DEF introduces at most one new auxiliary coordinate and names two earlier inputs, LOCAL emits at most three original coordinates, AND3 adds no support beyond its two inputs, RES adds no new support beyond parents, and GF2 adds no support beyond its two rows. Hence the **total active coordinate set** mentioned anywhere has size `O(N+q)`, *regardless of the numerical header variable bound*. Every coordinate is named by at most `O(N+log(q+2))` bits, since its index is at most the source-declared bound plus q. Each clause and affine row therefore contains at most `O(N+q)` sparse entries, each bounded by that bit cost. Constant-support factors have at most eight truth bits; DEF tables have exactly four; typed references have `O(log(q+2))` bits.

Thus an explicit cost-preserving serialized proof has

$$
\boxed{|\operatorname{cert}(F,\pi)| =
O\!\left(N+q(N+q)(N+\log(q+2))\right)\ \text{bits},}
$$

up to fixed-format encodings and delimiters. This is polynomial in `N+q`. The older asserted `O(N+q(n+q)log(n+q))` may **not be polynomial in N+q** if `n` is the declared numeric DIMACS header (e.g. `10^80` with only 81 decimal digits). The present proof uses actual sparse occurrences and index **digit length** instead of allocating an array of size `n`. Explicit full truth-table exponential payloads or private free LOCAL gate ports are excluded because they are not literal paid-root/fixed-support records.

The bound applies to **semantic proof-to-sparse-evidence existence** and a syntactic topological serializer, not to arbitrary larger proposed grammars or to proof *search*. Its final verification claim is **conditional on correcting the accepted-byte checker** and authenticating the external original source.

## Original-source authentication must mean external equality

The REFEREE360 document embeds a `source` object and `source_sha256` calculated from that same object. This **self-hash alone does not establish that it equals a separately supplied original SAT instance**. For unconditional source authentication, the trusted checker must compare the externally supplied original source's parsed, ordered clause IDs/header to the embedded source **byte-for-byte under one declared canonicalization**, or check an exact source object independently. SHA-256 can be an integrity aid, but hash equality alone is not an unconditional mathematical equality theorem; no collision-resistance assumption is allowed in this proof. This is a provenance contract, **not an exhibited SHA collision or a claim that the embedded-source checker is inherently unsound about its OWN source**.

## Independent experiments and hostile controls

Original Python (standalone local reproducibility): 2,843 checks; independently authored JavaScript **fetched back from GitHub and executed in the V8 sandbox:** 2,935 checks. Both enumerated 16 two-input Boolean gate tables with aliased inputs; 64 fixed facets, exactly **32 tautological off-diagonal facets**, 96 legal oriented RES candidates involving source units, and **64 old-rule invalid branch instances**. Exhaustive three-variable ordinary non-tautological clause pairs and all eight assignments all passed. Both verified the old false `(-z)` unit and corrected sound `(x OR not z)`, allowed a repeated same-sign facet, and rejected missing pivots. The large-header fixture has `nvars=10^80`, compact source/wire JSON length 379 bytes in Python and 81-digit indices in JS, without any length-`10^80` arrays. These checks are **COMPUTATIONAL**; the oriented soundness lemma and asymptotic sparse bound are symbolic proofs.

Precise statuses: This repairs a proposed CANON1 **RES branch**, not the entire 473-line REFEREE360 implementation or the historically undefined byte syntax. Existing native AND3, GF(2), LOCAL and DEF proof interpretations are held fixed, not altered; each needs independent full-checker regression before promoting an all-rule normalization. The patched implementation has **not been installed** in LSPV-5-owned code. Negative SAT controls and K4 odd/even Tseitin must be rerun against that patched **whole checker**. Source source-identity byte comparison is additionally required for external-input claims.

## Physical costs, distinction from minimum DAG work

The repaired RES rule tries at most two orientations and scans the two parent clauses. Given a finite `E`-byte materialized certificate, parsing/exact source comparison, all reference/index reads, clause normalization, explicit output and verification use polynomial bit-time in `E+N`. A buffered implementation may use `O(E+N)` or more host-specific storage; every temporary allocation contributes to all-phase peak, and streaming/recomputation costs must be separately established. Ideal minimum paid nodes `W_R` counts **only** one unit per distinct node, not construction, hash calculation, input/output, search, cache, or physical verification work. No time-space inequality or FLMV improvement is asserted. No exact worst-case `W_R` is computed in this run.

## B3 and lower-bound model discipline

The fixed same-calculus objective is

$$
\mathrm{SAT}\in P\;\Longrightarrow\;
\exists C,k\;\forall N:\quad
\overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^k.
$$

The present repair and normalized evidence **do not prove B3**. A hypothetical polynomial SAT decider, or its rejecting trace, is not automatically an authenticated fixed-/341 refutation, and blanket correctness assumptions would be circular. Haken's polynomial-encoding PHP family has an exponential **ordinary Resolution** minimum over all Resolution proofs, while Extended Resolution and stronger parity systems permit shortcuts on relevant hard controls. Cook–Reckhow's proof-system existence observation under `P=NP` does not automatically give polynomial p-simulation into `R_mix341`. We keep the exact mixed minimum and B3 OPEN; no restricted proof hardness is reinterpreted as unrestricted machine hardness.

## Publication, ownership and next shortest gap

Role-owned code: `experiments/arc/lspv3_421_oriented_res_independent.js`, GitHub blob `0e5f832d64f81a0ff3f7cc18456817d75815e71b`, **readback executed**. Raw JSON: `results/raw/arc/2026-11-05_0424_LSPV3_ORIENTED_RES_FACET421_raw.json`. Local independent Python and its generated JSON are included in this run's reproducibility artifacts. Report + five-role handoff are new non-overwriting files. Latest issue #3 to be updated. Root `main.tex` left unmodified unless complete current blob is retrievable and diff can be confined to LSPV-3 region; no other role's manuscript region or LSPV-5 checker is edited.

**Next step:** have LSPV-5 integrate the exact oriented RES validator into the proposed CANON1 checker; run the exact SAT forgery, all facet controls, K4 and corrupted-local/AND3/GF2 cases, then prove byte-level full-rule soundness with exact external source equality. Independently derive or refute the missing polynomial reflection/p-simulation from a uniform correct SAT P decider into the same unchanged /341 calculus.

### Primary references

[1] A. Haken, *The Intractability of Resolution*, TCS 39 (1985), 297–308, DOI 10.1016/0304-3975(85)90144-6.

[2] S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1) (1979), 36–50, https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf.

[3] L. Cruz-Filipe, M. Heule, W. Hunt, M. Kaufmann, P. Schneider-Kamp, *Efficient Certified RAT Verification*, https://www.cs.cmu.edu/~mheule/publications/lrat.pdf.

[4] S. Gocht and J. Nordström, *Certifying Parity Reasoning Efficiently Using Pseudo-Boolean Proofs*, AAAI (2021), https://ojs.aaai.org/index.php/AAAI/article/view/16494.

<!-- LSPV-3/421 report end, B1/B2/B3/PNP OPEN -->
