# LSPV-1/499 | Constant-support nonlinear feedback survives a random-3CNF proof-size lower bound

**2026-11-08 01:04 PST | Route B lead | PROVED/RESTRICTED conditional on published preprint theorem; COMPUTATIONAL independent finite controls | P versus NP OPEN.**

Material evidence node **[P2-L1-499]**. Refines the gap boundary **[P2-C3]** and restricted-model evidence **[P2-B1]**, building on **[P2-L1-498]**. Historical **[P2-D1]** and same-calculus B3 **[P2-B2]** remain OPEN. Proof1 references **[P1-00]**, **[P1-01]** remain unchanged.

## IDEA first: falsifiable repair

Hypothesis: the restricted random-3CNF lower bound in LSPV-1/498 survives not only RES, global affine XOR and same-support affine extraction, but an entire *fixed-constant-support, bidirectional nonlinear local factor calculus* with arbitrary interleaved factor AND, factor-to-clause, affine-to-factor, factor-to-affine and affine-to-clause feedback, provided no fresh extension variables or unbounded-support semantic jumps are admitted.

Falsifiers stated before searching: (F1) any local Boolean factor needs more than a constant number of original-variable clauses; (F2) a local affine unit equation cannot syntactically yield the full clauses excluding its violating assignments using Pang's actual degree-one rules; (F3) the conversion permits a global high-support equation, hidden auxiliary definition, leaked branch assumption, or free semantic implication; (F4) the target preprint lacks the claimed lower bound for the SAME original proper signed random 3-CNF and fixed characteristic two. F1 and F2 are refuted by the proof below; F3 is explicitly a forbidden extra strength, and F4 was checked in the exact primary theorem. These are restrictions of a distinct fixed calculus, not exclusions from historical R_mix341.

## SEARCH: exact historical corpus and source models

Preflight read both complete current trackers (initial current blobs proof1 `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, proof2 `e0123e4b511deed33fd9551cce34cc34d6ad8b64`; the live proof2 blob subsequently advanced with peer writes). Read current issue #3 (1,306 comments at inspection, latest material LSPV-4/489), November 2 governing handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md. Read LSPV-1/498 `research/agents/lspv-1/2026-11-08_0004_LSPV1_RANDOM3_LOCAL_MIXED_RESPC_TRANSFER498.md` blob `c99ae09691941c5e2b5a5f2d1dee01da8065dfd8` and its five-role handoff, LSPV-3/492 and /493 native one-hot/AND3 controls, LSPV-5/427 and /428 reports, and relevant LSPV-4/489 audit. Read actual Grok `GROKPROOF/2026-11-08_0320_PROGRESS.md` blob `72edb3140d8ed798d0905a827f85d3428728e396` and Claude `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`; neither authorizes a mixed-rule theorem.

Primary paper read: Shuo Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, **published/revised October 24, 2026**, https://arxiv.org/html/2610.00837v2 : exact syntactic Res(PC_r/F_p) rules in §1; Fact 7.1 on O(2^t t) bounded-variable consequences in §7; Theorem 7.2(a) for with-replacement proper random 3-CNF, p=2 and r=1. Pang's preprint is external theorem evidence, not independently formalized/reproved here. Literature additionally located Haken's ordinary Resolution PHP bound, Cook's Extended Resolution PHP shortcuts, and Pich–Santhanam arXiv:2312.08163 on bounded-arithmetic/reflection premises and P-vs-NP lower-bound transfer; the latter does not supply [P2-B2]. Search service used; no Google-branded direct interface or external Lean kernel replay.

Required repository delta/content checks:
- `konard/p-vs-np/README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`; `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`: bounded finite-machine formalization P subset NP only, not P=NP.
- `blkph0x/p-vs-np-proof-research/README.md` blob `f397a7747eaca82df3d754d0a4b4bab1fe10f814`; `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`: promise and finite local results, no unrestricted proof.
- `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`: independently authenticated mixed proof format, NOT historical grammar.
- `peitl/short-proof/README.md` blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab`: ordinary Resolution optimizer only.
- `tanyongkiam/cake_lpr/README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`: distinct verified LPR checker, final planned release 2026-11-01.
- `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`; `anthropics/formal-math/eth/README.md` blob `0b3dcf4a858ff802b3275fc5999ffb134c74de60`: raw research and subexponential 3-SAT claims, respectively, neither B3.

## ITERATE: strengthened fixed proof system

Fix any integer **b >= 3** independent of input size. Define a **DISTINCT** effective source-authenticated proof calculus `R_local-feedback(b)` over original Boolean variables. Original signed proper 3-CNF clauses are leaves. Paid unit rules include:

1. **RES**: arbitrary ordinary shared-DAG clause Resolution with correct pivot orientation and unrestricted derived clause width.
2. **XOR**: binary affine-equation addition over GF(2), retaining arbitrary original-variable support, including contradictory 1=0.
3. **LOCAL_b**: from any finite collection of already-derived constraints (ordinary clause, affine-unit equation, or an explicitly tabulated Boolean factor), derive any constraint of one of these types implied by their conjunction, **only when the union of ALL parent supports and output support consists of at most b ORIGINAL Boolean variables**. For a Boolean factor P supported on I, its complete truth table is the record. Local implication is checked exhaustively on <=2^b inputs. Every occurrence of LOCAL_b is paid. No fresh variables, DEF/ER facets, free semantic oracle, unbounded-support conjunctive operation, branch discharge, or hidden source axioms. Existing global XOR equations may enter LOCAL_b ONLY when their ENTIRE support has size <=b.

LOCAL_b therefore admits RES-derived clause-to-factor input; arbitrary locally shared ANDs of factors; factor-to-affine output; affine-to-factor/clause feedback; and local mixed reconvergence. It is strictly more permissive than LSPV-1/498's source/same-triple affine-only macro. RES alone makes the fixed system complete, and rule checks are finite and uniform for fixed b.

### Theorem 499.1: source-preserving bounded-feedback simulation (PROVED/RESTRICTED)

For each fixed b there is a constant C_b=2^{O(b)} such that for ANY original CNF F with m clauses and n original variables, any q-paid-node shared refutation DAG in `R_local-feedback(b)` yields a same-original-source syntactic `Res(PC_1/F_2)` refutation with at most

$$
S_{\operatorname{Res}(\mathrm{PC}_1/\mathbb F_2)}(F)
\le C_b(q+m+n+1).
$$

**Proof.** Represent a source or RES-derived ordinary clause directly as the disjunction of degree-one literal equations. Represent a global affine E by its one-equation unit line. Represent each b-local factor P on variable support I by the canonical CNF `CNF(P)`: one width-|I| exclusion clause D_alpha for every assignment alpha on I at which P is false. At most 2^b such clauses are needed. Previous factor clauses are shared, not duplicated at every reference. An ordinary RES step is two constant-cost native linear-combination/false-deletion operations; a global XOR step is one native linear combination.

For one LOCAL_b step, let U be the union of supports (|U|<=b). If output Q excludes a full U-assignment alpha, soundness implies that at least one named antecedent is false at alpha. If it is an ordinary clause C, syntactically weaken C to D_alpha; if it is a factor, weaken its previously produced canonical exclusion clause to D_alpha. If it is an affine unit E=(f=0), falsity at alpha gives f(alpha)=1; derive D_alpha from E and the native Boolean axioms as follows. For each variable in f, weaken its Boolean axiom to `D_alpha OR (x_i=alpha_i)`. Combine these chosen equalities to `D_alpha OR (sum_i(x_i-alpha_i)=0)`; combine that equation with f=0 to obtain `D_alpha OR (1=0)`, and syntactically delete the false constant. No semantic rule occurs in the target certificate. All intermediate polynomials have degree one.

The <=2^b full-assignment exclusion clauses give a canonical CNF for output Q. Eliminate variables in U outside Q's support by ordinary resolution, recovering the required <=2^b canonical clauses on the output support. For a clause output, derive the requested clause from these by contraction/tautology axioms. For a new affine-unit output, Pang Fact 7.1 compiles the canonical local CNF into the affine equation using O(2^b b) syntactic steps. Constant true/false cases are covered by Boolean axioms and an exhaustive local resolution contradiction respectively. Every conversion cites preceding native target lines, all assumption contexts are empty, and shared source ancestors are paid at most once. Even if LOCAL_b lists many redundant antecedents, one falsified parent per excluded full assignment suffices, so at most 2^b parent records are used by the target macro. Summing the constant macros over the finite shared proof DAG proves the bound. No extension variable enters either derivation. QED.

**Quantifiers:** for EVERY fixed b, EVERY original CNF F, and EVERY valid (possibly optimal) R_local-feedback(b) DAG, there EXISTS a same-source target DAG with constant C_b independent of F, n and q. The compiler is effective but needs to read the input proof and identify/verify local parent witnesses; its actual time is charged below.

### Corollary 499.2: established hard family still has an exponential minimum

Pang Theorem 7.2(a) states that for F_n uniformly sampled with replacement from proper signed 3-CNFs of n variables and exactly 8n clauses, with probability 1-o(1) every syntactic Res(PC_1/F2) shared refutation has >=exp(kappa n) nodes for some kappa>0. The original indexed literal source length is N=Theta(n log n). Thus Theorem 499.1 implies, in this DISTINCT richer fixed mixed system,

$$
W_{R_{\mathrm{local-feedback}(b)}}(F_n)
\ge \frac{\exp(\kappa n)}{C_b}-9n-1
=\exp(\Omega(n))
$$

with high probability, for every **fixed** b. Hence worst-case minimum is >= exp(Omega(N/log N)) along an unbounded source-length sequence. This is restricted proof-size hardness only; no computational lower bound or all-historical-rule claim.

### Boundary and shortcut controls

This theorem newly covers bounded-support nonlinear factors and bidirectional local clause/GF(2) feedback, but cannot simulate the original historical semantics of an arbitrary paid **fresh extension variable**, unbounded-support AND/LOCAL-CONVERT, unrestricted extension-variable polynomial shortcuts or assumption discharge unless individually authenticated and given polynomial-overhead same-source target simulations. Allowing b to grow with n also destroys the constant C_b claim. Haken PHP ordinary Resolution hardness is no control for Extended Resolution, where Cook gives short proofs. Same-characteristic parity Tseitin is refutable by native affine XOR. These known shortcuts must remain available as upper-bound controls in any full historical minimum.

## Independent finite syntactic verification

Independent Python: `/mnt/data/lspv1_499_local_feedback.py` (conversation artifact, not a GitHub native/historical checker). Independent GitHub JavaScript code: `experiments/arc/lspv1_499_local_factor_feedback.js` blob `b0904366b4af7b2795fd23e066aa8ef1f0f3a159`; raw `results/raw/arc/2026-11-08_0104_LSPV1_499_LOCAL_FEEDBACK_RAW.json` blob `720c5cf4efeb534e519e7a6dff6191d37143c6de`. Both checked all 16 affine equations on three variables, their 64 falsifying full assignments with explicit syntactic Boolean weakening/combination/false deletion, a two-contradictory-row complete AND-case proof ending in the empty clause, factor support expansion, five deliberate malformed rule rejections, and all 65,536 ordered pairs of three-bit Boolean-factor truth sets, of which exactly 6,561 are entailments (3^8). Both produce 342 native syntactic test nodes, partitioned as three Bool, 19 source, 122 weakening, 119 combination and 79 false deletion. Exact published JS and raw were re-fetched, evaluated and matched. These tests verify small syntactic controls only, NOT Pang's asymptotic theorem or accepted native R_mix341 grammar.

## Full cost and proof-system accounting

Ideal R_work counts each DISTINCT, unit-paid inference once, with free after-the-fact optimal derivation and no discovery/search charge. LOCAL_b factors require at most 2^b truth bits; global affine rows require up to n+1 bits; proof references require O(log(q+m+n)) bits. Materializing the translated proof takes O(C_b(q+m+n)) inference records but may require a conservative O(C_b(q+m+n)(q+n+1)(n+log(q+m+n+2))) serialized bits owing to globally wide intermediate lines. The mechanical converter reads original source/indices, source-authenticates every parent, verifies every local b-row table, constructs target lines, verifies and emits all output, with time polynomial in its full input/output bit lengths; simultaneous peak storage is at most polynomial when materialized (not a native FLMV bound). Source/index/head reads, evidence streaming, memory high-water, proof search, failed trials and physical verification are NOT equated with W. Ideal weighted work and parallel critical-path depth are distinct; the syntactic macros add at most C_b factor to DAG span in a unit-cost parallel model, not a bound on realizable space.

## Remaining arrows and publication boundaries

**[P2-D1] OPEN:** historical R_mix341 original-source grammar and allowed DEF/AND3/LOCAL-CONVERT/branch typed interfaces. **[P2-C3] OPEN:** complete polynomial simulation of EVERY historically legal mixed rule, especially nonlocal extensions. **[P2-B1] OPEN:** all-historical-rule superpolynomial minimum. **[P2-B2] OPEN:** weakest noncircular same-calculus B3, SAT in P => polynomial Wbar_Rmix341. The conditional arithmetic remains a conditional target, not a separation. Root main.tex fetch returned content length ZERO with blob SHA only, so it was NOT edited; no other manuscript region was touched. Historical weights, five active roles and two-A/three-B allocation unchanged. P versus NP OPEN.

**Advance:** bounded-support nonlinear factors and full local feedback are not, by themselves, an escape from the Pang characteristic-two random-3CNF lower bound. **Verification:** symbolic source-preserving simulation plus finite independent syntactic controls. **Precise remaining transfer:** paid variable definitions and genuinely nonlocal/branch calculus; and independently B3.
