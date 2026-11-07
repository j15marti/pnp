# LSPV-5 independent red-team report: algebraic branch guards do not authenticate the mixed transfer

**Pacific timestamp:** 2026-11-06 21:48 PST  
**Route:** B (`R_mix341` minimum derivation and noncircular B3)  
**Classification:** one elementary PC/PCR simulation lemma is **PROVED-RESTRICTED**; historical mixed-calculus transfer, superpolynomial `Wbar_R`, B3, and P versus NP remain **OPEN**.

## Initial idea and falsifiers

Hypothesis: Boolean case splits do not add asymptotic power to Polynomial Calculus when both branch refutations are explicitly context-labelled, because branch proofs can be guard-lifted and recombined with polynomial overhead.

Falsifiers tested:

1. a multiplication inference cannot be guard-lifted by native PC rules;
2. a branch assumption cannot be eliminated using only the Boolean axiom;
3. reconvergent sharing requires uncharged reuse or exponentially many context incidences;
4. a valid PC/PCR construction does not simulate authenticated historical `R_mix341` rules, weights, or bytes.

The first two falsifiers fail for one split; the third and fourth remain real boundaries.

## Tracker and continuity read

The complete current trackers were read at blobs `proof1.txt` `006eeeb51fa0440abcdd55ddf86e8059933f8c70` and `proof2.txt` `f430e8d5cd9302fc643308319831b9789d29778b`. Relevant exact IDs were `[P2-F8]`, `[P2-F9]`, `[P2-B9]`, `[P2-L3-465]`, `[P2-C1]`, and `[P2-L5-401]`. The new material affects `[P2-F9]`, `[P2-C1]`, and new node `[P2-L5-402]`; `proof1.txt` has no material change.

Peer evidence changed the target. `[P2-B9]` proves an ordinary-Resolution backtranslation with multiplicative leaf count `L` for a restricted original-variable section tree. `[P2-L3-465]` exhibits a linear-size XOR prefix chain whose exact constant-leaf section tree has `2^k` leaves. This report therefore tests direct algebraic guarding, not truth-table leaf enumeration.

The governing handoff, current issue #3 body, current LSPV-1/2/3/4 reports, actual Grok and Claude ledgers, `AGENTS.md`, `CODEX.md`, and the research instructions were read. The complete issue-comment stream could not be retrieved: the connector closed transport twice. No comment-stream review is claimed.

## Established-family ledger

| ID/family | Exact encoding and parameter | Established theorem/model | Known legal shortcuts/control | Remaining transfer |
|---|---|---|---|---|
| `[P2-F8]` random strict 3-CNF | `m=ceil(Delta n)` distinct-variable width-3 clauses on `n` variables, sampled independently in the cited model | **PROVED-RESTRICTED:** exponential PC/PCR size lower bounds with high probability under the paper's density/degree assumptions; not all algorithms | algebraic PC/PCR derivations, sharing, ideal choice of refutation | authenticate exact distribution/constant hypotheses and transfer across every historical mixed rule |
| `[P2-F9]` random strict 3-CNF | same source family; binary source length `Theta(m log n)` under explicit literal indices | **PROVED-RESTRICTED:** source-family PC/PCR lower bound only | new one-split PC and explicit-tree PCR branch simulations below; direct algebraic guards avoid `[P2-L3-465]` constant-leaf enumeration | shared context-DAG accounting and `R_mix341` rule-by-rule simulation remain open |
| `[P2-B9]` restricted section-tree control | arbitrary UNSAT CNF `F(X)` plus conservative `G(X,Y)` with `L` original-variable decision leaves and fixed auxiliaries making every `G` clause tautological | **PROVED-RESTRICTED:** `S_Res(F) <= L(S_Res(F and G)+1)-1` in ordinary shared-DAG Resolution | legal source restriction and DAG Resolution | `L` can be exponential; no mixed-calculus conclusion |
| `[P2-L3-465]` XOR-prefix barrier | `k` original inputs, `k-1` fresh prefix outputs, four proper 3-clauses per XOR gate | **PROVED-RESTRICTED/COMPUTATIONAL:** linear Skolem circuit but `2^k` exact constant leaves | affine/GF(2), circuit sharing | destroys any claim that functional Skolem size alone bounds section leaves |
| finite 2-SAT control | `(x or y),(x or not y),(not x or y),(not x or not y)` encoded by clause falsifier polynomials | **COMPUTATIONAL:** exact trace only | both branches, legal join, corrupted-certificate tests | not a hard family and supplies no asymptotic lower bound |

Certified UNSAT, proof-size hardness, and solver difficulty are distinct here. The finite control is a checked UNSAT derivation. `[P2-F8]`/`[P2-F9]` are restricted proof-complexity theorems. No empirical solver timing is used as hardness evidence.

## Exact elementary lemma: one Boolean split in PC

Use the standard PC rules over a field: source/Boolean axioms, linear combination, and multiplication by a variable. Include `x^2-x=0`. Let `pi_0` refute `Gamma union {x=0}` and `pi_1` refute `Gamma union {1-x=0}`. Count all source/axiom and inferred lines in `L_i`, all monomial occurrences in `S_i`, and maximum degree `d_i`.

**Lemma (PROVED-RESTRICTED).** `Gamma` has a PC refutation with

$$
L \le 3(L_0+L_1)+1,\qquad
S \le 4(S_0+S_1)+2,\qquad
d \le \max(d_0,d_1)+1.
$$

**Construction.** Guard every line of `pi_0` by `1-x` and every line of `pi_1` by `x`.

- For a source or Boolean line `p`, derive `xp` by one multiplication. The `x`-guarded copy is `xp`; the `(1-x)`-guarded copy is the linear combination `p-xp`.
- A linear-combination step lifts by the same linear combination of guarded parents.
- If `q=yp` is a multiplication step, derive `y(gp)=gq` from the guarded parent, for `g` equal to `x` or `1-x`.
- The `x=0` assumption, guarded by `1-x`, is `x(1-x)=-(x^2-x)`, obtained from the Boolean axiom. The `1-x=0` assumption guarded by `x` is the same polynomial.
- The terminal `1` in `pi_0` becomes `1-x`; the terminal `1` in `pi_1` becomes `x`. Add them to derive `1`.

The length and size constants deliberately charge the extra multiplication and subtraction needed for every source/axiom line. An earlier draft undercounted these source lifts; the executable checker forced the displayed safe constants. The lemma permits arbitrary DAG sharing internal to each branch, but charges the two incompatible branch contexts separately.

## Explicit branching trees in PCR

In PCR use complement variables and axioms `x+bar(x)-1=0` and `x*bar(x)=0`. For an explicit binary decision tree, the path guard of leaf `ell` is one monomial `g_ell`. If a PCR refutation `pi_ell` is supplied under the leaf assumptions, multiply each line along the path to obtain `g_ell p`; complementary assumptions vanish through a multiplied `x*bar(x)` axiom. Each leaf yields `g_ell`. Join sibling guards bottom-up using the corresponding multiplied `x+bar(x)-1` axiom.

For leaf depth `d_ell`, size `S_ell`, and degree `delta_ell`, this gives the explicit bound

$$
O\left(\sum_ell (d_ell+1)S_ell+\sum_{v\text{ internal}}(\operatorname{depth}(v)+1)\right)
$$

and degree at most `max_ell(delta_ell+d_ell)`. This is polynomial in the **context-expanded explicit tree certificate**. It is not polynomial in the union of unlabelled nodes of an arbitrary reconvergent branching DAG. Reusing a node reached under incompatible assumptions is legal only after discharge; otherwise `(context,node)` incidences must be charged separately. Substituting `bar(x)=1-x` into ordinary PC can also expand a depth-`d` guard into `2^d` monomials, so the arbitrary-tree statement is PCR-specific.

No case-split, discharge, or weakening rule was added to historical `R_mix341`. This is a simulation inside the separately specified PC/PCR systems.

## Executable witness and adversarial checks

Artifacts:

- `experiments/review/lspv5_402_pc_case_split_compiler.py`, SHA-256 `37ab7c6bf77ed65bd57717f1fc64e6da13d7d2f2a68358a547dd2ba23e000f64`;
- `experiments/review/verify_lspv5_402_pc_case_split.mjs`, SHA-256 `4c49bcad3f47f2c2b8d71311fd30d7dae5f5738c8a3e924b6de1944df0955420`;
- `results/raw/review/2026-11-06_2148_LSPV5_PC_CASE_SPLIT402.json`, SHA-256 `93876e6c324a490f004ee4d7676d66e923fa3ffb3989f1cb113f8c9c2abb4eb2`.

The exact Python checker compiled two branch refutations into 19 lines, 13 paid inference nodes, 43 monomial occurrences, maximum degree 3, and six source reads. It used IDs above `2^40`. Five corruptions were rejected: omitted AND join, missing parent, reversed linear orientation, branch-assumption leak, and duplicate large ID. The independent Node verifier passed 105 checks. PCR partition controls at depths 1 through 8 performed 87,380 guard evaluations and rejected an omitted leaf witness.

This is an independent checker, not an execution of the authoritative historical checker. The 2-SAT formula is a focused validation control, not a candidate hard family.

## Resource ledger

| Phase | Charged result |
|---|---|
| logical evidence | 19 trace lines; 13 inferred nodes; 43 monomial occurrences; 6 source reads |
| explicit evidence bits | raw JSON 12,717 bytes; Python 13,882 bytes; Node verifier 2,890 bytes |
| construction/search | deterministic compiler; no semantic SAT/equivalence oracle; no failed restarts |
| parsing/index/head reads | complete `proof1.txt` and `proof2.txt`; governing/peer files; repository heads and selected actual files |
| verification | Python exact rational-polynomial checks plus independent Node replay; 5 negative mutations; 87,380 PCR guard evaluations |
| time | Python elapsed about 0.468 s; connector retrieval and publication charged separately in the run log |
| peak space | Python traced peak 79,489 bytes; process maximum RSS 14,080 KiB; publication/connectors not assumed to share this peak |
| caches/retrieval/recomputation | in-memory polynomial maps; stored raw trace; Node independently recomputed polynomials |
| output | report, code, verifier, raw JSON, handoff, tracker update, issue comment |
| failed policies | complete issue comments unavailable; `main.tex` response was content-empty/oversized, so no root edit was attempted |
| simultaneous all-phase peak | not measured across remote connector service and local process; no smaller global peak is claimed |

This ledger concerns a proof-certificate experiment, not Route A's same-machine contraction. It supplies no `s'` exponent bound and no FLMV implication.

## Search and source authentication

Primary-source searches read the formal PC/PCR rule definitions and size/degree measures in the DOI-hosted paper *A Generalized Method for Proving Polynomial Calculus Degree Lower Bounds* and related primary PC literature. No exact published theorem matching the context-labelled guard construction with these constants was found; the construction is reported as an elementary proof, not as a novelty claim.

Change-aware repository review pinned both required repositories and the relevant controls: `konard/p-vs-np` `ecedd2b45...` (`proof_status.md`), `blkph0x/p-vs-np-proof-research` `7dedc73f...` (`METHOD_INDEX.md`), `meelgroup/frat-xor` `18cd6bc...` (format), `tanyongkiam/cake_lpr` `033aad53...`, `peitl/short-proof` `2c524cfc...`, `MassimoLauria/cnfgen` `24e633b...`, `msoos/cryptominisat` `ed61e217...`, `openai/math` `4eaee875...`, and `anthropics/formal-math` `16a5ce413...`. Their repository text/build status was not treated as authority for P versus NP. Google-branded search was unavailable; primary-source web search was available and used.

## Revised claim, status, and precise gap

**Actual advance:** explicit Boolean branching is eliminable with the displayed native overhead for one PC split and for an explicit context-expanded PCR tree. This directly avoids constant-leaf Skolem enumeration in the algebraic model and formalizes where AND obligations and assumption scopes are paid.

**What it does not prove:** no authenticated simulation places PC/PCR guards inside historical `R_mix341`; no theorem bounds context duplication for arbitrary reconvergent shared branching DAGs; no all-mixed-rule lower bound follows from random 3-CNF PC hardness; and no noncircular B3 bridge follows from SAT in P.

The precise remaining gap is a source-authenticated, weight-preserving polynomial simulation or lower-bound transfer covering every legal `R_mix341` rule while charging `(context,node)` sharing correctly, followed independently by a noncircular B3 proof for that same fixed calculus. P versus NP remains **OPEN**.
