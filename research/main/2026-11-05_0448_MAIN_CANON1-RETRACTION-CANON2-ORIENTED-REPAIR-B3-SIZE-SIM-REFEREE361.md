# REFEREE361 — retire unsound CANON1, oriented CANON2 repair, and weakest B3 size-simulation contract

**LSPV-5 Independent Proof Red Team — November 5, 2026, 04:48 PST**  
**Status:** REFEREE360 checker soundness FALSIFIED/RETIRED; exact four-node SAT exploit reproduced; distinct legal three-node coverage counterexample reproduced; CANON2 repair PROVED for the proposed root-only/fixed-facet completion; historical native byte uniqueness and same-`R_mix341` B3 OPEN. **P versus NP OPEN.**

No semantic rule, paid-node weight, task, role, schedule, or enabled state changed. This report corrects an LSPV-5-owned claim and does not edit another role's manuscript region.

## IDEA before search

Hypothesis: REFEREE360's `CANON1` is unsound at an aliased paid-DEF boundary. A repeated input `a=b=x` makes two of the four positional DEF facets tautological; the old RES implementation deletes every occurrence of both pivot signs. Falsifiable prediction: it accepts a contradiction from a satisfiable one-unit source. The necessary repair must retain positional gate inputs, use oriented one-literal Resolution deletion, accept affine annotations on strict sub-support, compare against an external original source, and use sparse encoded identifier length rather than numeric header value.

B3 hypothesis: after exact balance is repaired, the weakest sufficient bridge is polynomial **size simulation** of the proof system defined by one assumed polynomial SAT decider. Because `W` grants free choice of a shortest proof, polynomial-time proof search/p-simulation is stronger than B3 requires. Prediction: the size-simulation statement is equivalent to B3 for the frozen checker and therefore cannot be obtained merely by choosing minimum proofs.

Registered falsifiers:

1. aliased DEF facet plus old all-occurrence pivot deletion derives false units;
2. legal AND3 factor has affine support strictly smaller than syntactic support;
3. changing both embedded source and self-hash passes without external-source comparison;
4. a huge numeric DIMACS header invalidates a bound using `n <= N`.

## SEARCH

### Governing project record and peers

Read first `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` at blob `c3889a3e`; original `/341` at `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11`; REFEREE356 positional alias audit; REFEREE360 report and checker blob `67ecd99a`; latest issue #3; actual `GROKPROOF/2026-11-05_1218_PROGRESS.md` (`d3183283`); Claude TPORT-0002 (`1f9fc727`) and ONETAPE-0001 (`9a5b05d6`). Grok/Claude do not supply this parser repair or B3.

The initial falsifier was independently found first by LSPV-2/415 while this run was reading the thread. Its exact 615-byte witness and code-branch diagnosis were read and reproduced. LSPV-3/421 supplied the oriented-Resolution repair and sparse-header correction. LSPV-4/412 supplied a separate original-rule-legal affine-sub-support counterexample to CANON1 coverage, strengthened to distinct parents. LSPV-1/416's bad-prefix theorem shows that even detecting a local self-reduction violation can encode SAT; under `SAT in P` it gives another semantic decision procedure, not a native proof.

### Literature and repository search

Actual indexed-web queries:

- `resolution rule tautological clauses oriented pivot proof soundness primary source`;
- `LRAT proof checker duplicate complementary literals tautological clause sorted primary paper`;
- `Cook Reckhow p simulation polynomial bounded proof system original paper PDF`;
- `Haken intractability resolution pigeonhole extended resolution polynomial proof 1985`.

Read the resolution rule in the primary automated-reasoning literature: from `C or x` and `D or not x`, the resolvent is `C or D`; it deletes one oriented complementary pair, not every occurrence of the variable. Read the certified-LRAT paper: exact sorting and duplicate/complement checks are explicit parser restrictions. LRAT often excludes tautological clauses, but that format choice cannot justify silently rejecting original `/341` aliased-DEF facets; CANON2 instead checks sound oriented Resolution on them. Haken's theorem remains an ordinary-Resolution PHP lower bound and expressly notes polynomial Extended Resolution proofs. Cook--Reckhow p-simulation remains a sufficient transfer, not a consequence of `NP=coNP` for every fixed system.

Direct Google-branded search was unavailable; general indexed web search was used and is not reported as Google. Authenticated `github.com/openai` searches were `resolution tautological clause pivot checker`, `LRAT checker duplicate complementary literals`, `ExecCNFNodeSearchCosts`, and `source hash proof certificate commitment`. The first two returned no results; the last returned unrelated build-integrity material. `openai/math/.../ExecCNFNodeSearchCosts.lean` was the only relevant result and charges explicit trace/visit/storage work. No OpenAI repository supplies the grammar repair or B3.

## ITERATE

### 1. Exact falsification of REFEREE360 soundness

Let the original source be the satisfiable unit `F=(x)`, witnessed by `x=1`. Pay one DEF node for fresh `z=f(x,x)` with four positional truth bits `[0,1,0,1]`. Under the CANON1 facet order, the two inconsistent-input facets are

`x or not x or not z`, and `x or not x or z`.

CANON1's old RES code checked that some complementary pivot occurred across the parents, then removed **all** literals of the pivot variable from **both** parents. Resolving each tautological facet against `(x)` therefore produced the false units `(not z)` and `(z)`, and a fourth paid node produced the empty clause. The old checker accepts all four nodes and the 615-byte certificate.

But the unique extension of the real source witness has `x=z=1`, which satisfies the definition and falsifies `(not z)`. Thus the accepted inference is unsound. Independent enumeration finds the same vulnerable opposite-unit pattern for 8 of all 16 two-input truth tables.

This retires REFEREE360's checker-soundness theorem. It is a counterexample to the proposed checker, not a legal inference of sound Resolution and not a defect in the original semantic `R_mix341`.

### 2. CANON2 oriented Resolution repair

For pivot variable `p`, CANON2 tries at most two orientations:

- if `p in A` and `not p in B`, output `(A - {p}) union (B - {not p})`;
- if `not p in A` and `p in B`, output `(A - {not p}) union (B - {p})`.

Literal sets are idempotently normalized, but the other pivot polarity is never erased. On the attack, the two legitimate resolvents are `(x or not z)` and `(x or z)`, not false units. Resolving them on `z` gives `(x)`, not contradiction.

**Soundness proof.** If an assignment falsifies an oriented resolvent, it falsifies `C` and `D`. Satisfying `C or p` forces `p=1`, while satisfying `D or not p` forces `p=0`, impossible. This proof is unchanged when either parent is tautological. DEF facets remain positional and repeated gate inputs remain legal.

The repaired checker rejects the old attack at node 1. An independently written JavaScript audit verifies all sixteen truth tables, all 128 actual aliased-definition model/facet cases, all 32 taut facets, and that oriented resolution retains `x`; 234 total checks pass.

### 3. Legal original-rule coverage counterexample and repair

CANON1 also falsely required the GF(2) mask on an AND3 factor to equal its syntactic support. Consider the original source

`(x or y) & (x or not y) & (not x) & (not x or y)`.

Paid AND3 node 0 conjoins the first two distinct source clauses. Its table on support `[x,y]` is `[0,1,0,1]`, exactly the affine equation `x=1` with strict-sub-support mask `[x]`. Paid AND3 node 1 conjoins the last two distinct clauses, giving `[1,0,1,0]`, exactly `x=0`. Paid GF2 node 2 adds them to `0=1`. This is a legal three-paid-node `/341` proof, independently checked on all four assignments, that CANON1 rejected.

CANON2 requires only `affine mask subset factor support`, then retains exhaustive equality over all at most eight rows. It accepts the legal proof. This repairs the explicit coverage counterexample without granting a semantic oracle.

### 4. External source and sparse balance repairs

A self-hash proves only that a certificate is internally consistent with its own embedded source; without assuming cryptographic injectivity, it does not prove equality to an externally supplied original. CANON2 therefore takes the external source as a separate checker input and compares its canonical bytes exactly. Replacing both the embedded source and hash is rejected before inference checking.

Also, a DIMACS maximum variable identifier can be numerically exponential in its encoded digit length. The earlier `n <= N` sentence was false. Let `A` be the number of active original/DEF coordinates. For a source of `N` bits and a `q`-node proof, `A=O(N+q)` and every original ID has `O(N)` bits while every canonical fresh ID has `O(N+log(q+2))` bits. Thus the repaired coarse bound is

`O(N + q(N+q)(N+log(q+2)))` bits,

polynomial in `N+q` and independent of the numeric header value. CANON2 accepts the contradiction `(x_1)&(not x_1)` under header `10^80` in one paid node; the header has 81 decimal digits but only one active original coordinate.

### 5. Revised normalization theorem and exact scope

**Theorem.** Every valid `q`-node proof in the literal paid-node/root-only/fixed-DEF-facet semantic completion translates rule-for-rule, source-exactly and cost-preservingly into CANON2 with the sparse polynomial bound above, including repeated DEF inputs, tautological fixed facets, affine annotations on strict sub-support, and typed GF(2) rows.

**Proof sketch.** Compare the supplied original source exactly. Topologically alpha-rename only fresh definitions. Serialize every clause as a canonical literal set, each factor as at most three original IDs plus at most eight bits, each affine row as a sparse active-coordinate mask plus RHS, and each positional DEF as two ordered earlier IDs plus four bits. Each semantic rule maps to the corresponding exact checker record. The oriented Resolution lemma, exhaustive AND3/LOCAL checks, GF(2) addition, and unique DEF extension establish acceptance by induction. Summing sparse records gives the bound. ∎

**Scope.** This proves a repaired theorem for a proposed exact completion. The historical `/341` prose still does not choose CANON2's byte syntax or uniquely settle all selector conventions. Therefore “the” pre-existing exact native byte language remains underdetermined; no claim of historical uniqueness is made.

### 6. Weakest B3 contract: size simulation, not necessarily p-simulation

Fix a uniform correct polynomial-time SAT decider `A`. Define a Cook--Reckhow UNSAT proof system `P_A`: the proof of formula `F` is simply canonical `F`; its verifier checks syntax and reruns `A(F)`, accepting iff `A` says UNSAT. External correctness of `A` makes this system sound and complete, and its proofs have `O(|F|)` length.

Because `W_R` grants free after-the-fact proof choice, the following are equivalent for the frozen polynomially balanced CANON2 completion under the assumption that `A` is correct:

1. `Wbar_Rmix341(N)` is polynomial;
2. every `P_A` proof has some polynomial-size CANON2 refutation of the same source;
3. CANON2 polynomially **size-simulates** `P_A`.

The mapping need not be polynomial-time computable for B3: proof discovery is excluded from `W`. Hence earlier wording that B3 *requires p-simulation* was too strong. A p-simulation or polynomial proof generator remains a sufficient stronger theorem.

This correction does not prove B3. Merely mapping each `F` to a minimum CANON2 proof is circular: the unproved statement that those minima have a uniform polynomial bound is exactly item 1. A rejecting trace, BAD-prefix decider, or external correctness axiom still does not provide item 2. Thus the sharp noncircular missing lemma is a system-specific polynomial **size** simulation/reflection theorem, with no presupposed target certificate bound.

## Verification and physical ledger

Producer results:

- old CANON1 accepts the exact four-node 615-byte SAT exploit;
- CANON2 rejects its first false unit as “not an oriented resolvent”;
- legal distinct-parent affine-sub-support proof accepted in three paid nodes;
- odd K4 Tseitin accepted in 15 paid nodes, 2,614 bytes and 128 local rows;
- self-consistent embedded-source replacement rejected against the external original;
- 81-digit header control accepted with one active coordinate and one paid RES node.

Independent JavaScript: PASS, 234 checks; exactly 8/16 aliased truth tables expose the old opposite-unit pattern.

Logical `W` still excludes source acquisition, exact external comparison, JSON parsing, hashing, table enumeration, identifier access, construction, output, writes and peak storage. The implementations buffer source/proof data and establish no FLMV tape bound.

## Status

- **FALSIFIED/RETIRED:** REFEREE360 CANON1 soundness and full-coverage claims as implemented.
- **PROVED counterexample:** exact four-paid-node SAT exploit against CANON1.
- **PROVED legal counterexample:** exact three-paid-node original-rule proof rejected by CANON1's support-equality test.
- **PROVED/REPAIRED:** CANON2 oriented Resolution, affine sub-support, exact external-source comparison and sparse-header balance for the proposed completion.
- **CORRECTED:** size simulation is the weakest exact B3 transfer contract; p-simulation is sufficient but not necessary for minimum proof size.
- **OPEN:** historical native byte-language uniqueness; a noncircular CANON2/`R_mix341` size-simulation theorem; B1/B2/B3; superpolynomial mixed minimum; P versus NP.

## Artifacts

- `experiments/arc/lspv5_361/rmix341_canon2_repair_referee361.py`
- `experiments/arc/lspv5_361/verify_rmix341_canon2_referee361.mjs`
- `results/raw/arc/2026-11-05_0448_LSPV5_REFEREE361_raw.json`
- `research/coordination/2026-11-05_0448_LSPV5_CANON2_ORIENTED_REPAIR_REFEREE361_HANDOFF.md`
