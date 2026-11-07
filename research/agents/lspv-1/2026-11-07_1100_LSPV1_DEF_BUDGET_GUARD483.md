# LSPV-1/483 | Parameterized paid-definition budget barrier for established random hard 3-CNF

**2026-11-07 11:00 PST | Route B lead | PROVED/RESTRICTED (declared local mixed completion and LSPV-1/481 compilation assumed), CONDITIONAL on Pang's 2026 preprint for the asymptotic lower bound; COMPUTATIONAL finite guard controls. P versus NP OPEN.**

**Tracker IDs:** new evidence for [P2-F9] and [P2-C3]; [P2-D1], [P2-B1], [P2-B2] remain OPEN. Related [P2-L3-479], [P2-L5-414], [P2-B3], [P1-01], [P1-03], [P1-04].

## IDEA and falsifiers

**Hypothesis:** Limit the number of paid, globally fresh two-input conservative DEF gates in the previously studied *definition-free, 3-local* mixed DAG fragment. Assign the original variables on which all gate definitions ultimately depend, evaluate every DEF, syntactically compile each restricted proof into Res(XOR), and resolve all assumption branches. This could prove a quantitative lower-bound tradeoff without pretending that unrestricted DEF elimination is cheap.

Predeclared falsifiers:
1. A gate depends on an original input not counted in the paid DEF input-edge support set, or on an opaque/free internal wire.
2. A specialized AND3/LOCAL/RES/GF(2) inference does not admit the constant-local syntactic Res(XOR) translation from /481 after all DEF outputs become constants.
3. Prefixing every translated line with a branch guard fails to preserve a syntactic Res(XOR) inference, or requires silently adding native split/discharge to historical R_mix341.
4. A branch of the original assignments is omitted, cross-branch evidence is reused without discharging its assumptions, or the original CNF is replaced by a different source.

Result: (1)-(3) are excluded *only* by the exact restricted grammar and target-system rule hypotheses below. (4) is handled formally and by finite certificates. Opaque ports, nonconstant-support conversions, and the historical byte grammar remain open controls, not silently forbidden alternative shortcuts in the full calculus.

## SEARCH and provenance

Read **both complete root trackers** at the start: proof1 blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, proof2 blob `daf0b1977dbfa833e3dec5bfbb024caa0c6cf308`; current issue #3 and last comments; governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` (current blob `c3889a3e514ddbd747150dcb68607013a3b2d154`; historically commit 4e29ed7); `AGENTS.md`, `CODEX.md`, and `.codex/skills/pnp-research/SKILL.md`. Actual prior /481 report `research/agents/lspv-1/2026-11-07_0956_LSPV1_DIRECT_SYNTACTIC_LOCAL_BACKSIM481.md` blob `cd2ec52e7c0fe352a44d55b8b6dab71637ff08c7`; /482; LSPV-3/479 `research/agents/lspv-3/2026-11-07_1024_LSPV3_DEF_OR_RES_CERTIFIED_GATE_PORT479.md` blob `6b3bed216a84331263a6dfd1006b36b0a9c4f982`; LSPV-3/477; original /341 `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`; recent Grok `GROKPROOF/2026-11-07_1815_PROGRESS.md` blob `0532370c9bf99b1204be4e0efd9ef96290454ec7`, Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` blob `79e4d4e7e0e3edff3aba8610852c45534bdde128`. The historical recovered checker /341 accepts only SOURCE/AND3/XOR; it does NOT authenticate the full R_mix341 grammar.

External change-aware reads: `konard/p-vs-np/scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` and `REVIEW_ADDENDUM.md` blob `6a7cc2f8962d3fcfcfc1778b1d3d8f5dc8d56d70`; `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; `tanyongkiam/cake_lpr/README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`. These do not establish historical rules. Search queries included Pang degree-size theorem, uniform reflection/proof systems, and SAT-decider correctness. Primary theorem text actually read: Pang arXiv:2610.00837v2 (2026-10-24), §1 and §7, especially **Theorem 1.1**, **Fact 7.1**, and **Theorem 7.2(a)**: https://arxiv.org/html/2610.00837v2 . Separate Google-branded search not available; indexed web search used. No PDF analyzed. Earlier project /481 already supplied the zero-DEF syntactic local simulation; no claim that this work originally discovered it.

## Exact bounded-DEF model

Let F be an original-source-authenticated CNF, with m clauses on n original Boolean variables. Define **R_loc3+DEF(d)** only as the explicitly stated extension of LSPV-1/481's DEF-free local mixed fragment: ordinary oriented RES on any width; GF(2) binary row addition on arbitrary rows; sound AND3 and single-parent LOCAL-CONVERT when all their *nontrivial local conditions* use at most three named variables of the original-plus-DEF universe, and a RES/LOCAL wide-clause weakening view only as in /481. Add at most d **paid**, acyclic, globally fresh, conservative two-input Boolean gate definitions; each gate input is an original variable or a previously defined gate output, with no free exported or private semantic wire. All source/branch contexts are explicit; no native split/discharge, semantic SAT oracle, or unrestricted gate equivalence. Costs are unit weights on distinct paid nodes. The rule set is a DISTINCT DECLARED completion because historical accepted-byte DEF/facet and LOCAL source semantics [P2-D1] are not authenticated. This does not revise the historical calculus or weights.

Let S(pi) be the set of original variables appearing as direct inputs to the d definitions in a candidate q-node DAG pi; let s=|S(pi)|. Since there are only 2d input slots, **s<=2d** (often much smaller). Every gate becomes a Boolean constant under a complete assignment alpha to S(pi), by acyclic evaluation. All original other variables remain symbolic. We allow free optimal after-the-fact choice of the full legal DAG; this is a restriction on its paid DEF count, NOT a free decomposition algorithm.

## Theorem 483.1 (restricted syntactic DEF budget transfer)

**Assume the /481 DEF-free 3-local syntactic simulation** has absolute constant K_3, and assume substitution of Boolean constants into each permitted local step above preserves its explicitly tested three-variable truth-table semantics, with original-source provenance and rule typing. Then there exists an absolute K such that **every** q-paid-node refutation pi of F in R_loc3+DEF(d) yields a **same-original-source** syntactic Res(PC_1/F_2) (Res(XOR)) refutation with

$$
S_{\mathrm{Res}(\oplus)}(F)
\le K\,2^{s}(m+q+1)\le K\,4^{d}(m+q+1).
$$

**Proof:** First fix any assignment alpha to the s original variables in S(pi). In topological order, evaluate all d gates; every gate output is now constant (no extra original source axiom). Specialize each previously legal source, RES, GF(2), AND3 and LOCAL step. Assigned-pivot RES either remains RES or becomes a weakening of its surviving parent; a GF(2) row remains affine on the unassigned original coordinates; any AND3/LOCAL conclusion is still a bounded-support truth-table consequence on at most three free original coordinates. By the /481 local syntactic compiler (Pang Fact 7.1 for bounded-width truth tables), this restricted proof compiles to Res(XOR) from F|alpha in <=K_3(m+q+1) nodes; tautologies are deleted or treated as target-system tautology axioms. It produces empty. This does **not** pretend that the historical source grammar natively accepts a case split.

Let the branch guard be

$$
G_{\alpha}=\bigvee_{x\in S(\pi)}
\begin{cases}
x &\alpha(x)=0,\\
\neg x &\alpha(x)=1.
\end{cases}
$$

Every restricted source clause C|alpha lifts from the ORIGINAL C by syntactic weakening to (C|alpha) OR G_alpha. Guard every line of the Res(XOR) branch certificate by the same G_alpha. Every syntactic rule is stable under a common disjunctive context: weakening, contraction, deletion, linear combination and multiplication at degree one (Pang §1). The branch empty line therefore becomes G_alpha. These 2^s clauses are all AND obligations, not OR choices. Resolve them in a binary decision tree in reverse assignment order to derive the empty clause, using 2^s-1 additional ordinary Resolution steps, a native special case of Res(XOR). Charge each distinct node once; sharing may only reduce the bound. With K increased to cover source lifts and joins the displayed inequality follows. Source clauses never change and branch-local assumptions do not leak: they are discharged by the explicit guards. QED under the declared-model hypotheses.

**Restriction/falsifier:** The argument FAILS to cover a gate whose inputs include an unauthenticated, free, semantically chosen port; a wide-to-local inference not satisfying /481; additional native inference tags not stable under specialization; or an assumed external SAT/equivalence oracle. If any is historically legal, this proof has not bounded it. This is NOT a full R_mix341 lower bound.

## Corollary 483.2 (published random 3-CNF and paid-DEF threshold)

Choose the established strict signed proper random 3-CNF F~F(n,3,8n): m=8n clauses drawn independently with replacement uniformly from all 8*C(n,3) signed proper width-3 clauses; indexed source bit length N=Theta(n log n). Pang v2 Theorems 1.1 and 7.2(a), using published linear GF(2) PC-degree hardness of this family, give w.h.p. a constant kappa>0 (not numerically identified here) with

$$
S_{\mathrm{Res}(\oplus)}(F)\ge e^{\kappa n}.
$$

Thus **every** legal restricted proof with d paid definitions and q total paid nodes satisfies, w.h.p.,

$$
\boxed{\ln K+\ln(m+q+1)+s\ln2\ge\kappa n,\quad s\le2d.}
$$

In particular,

$$
\boxed{\ln K+\ln(m+q+1)+d\ln4\ge\kappa n.}
$$

Therefore for d=o(n), q=exp(Omega(n))=exp(Omega(N/log N)); conversely **any polynomial-work q=n^{O(1)} proof in this restricted calculus requires** d>=kappa*n/ln4-O(log n), and its gate definitions must touch s>=kappa*n/ln2-O(log n) original-variable inputs. This is a linear gate-budget necessity, NOT a superpolynomial minimum across unrestricted R_mix341 (which allows arbitrary paid d and unresolved export/LOCAL conventions).

## Independent finite controls and limitations

Independent Python exact symbolic-guard generator `/mnt/data/lspv1_483_guarded_branch_control.py` and raw `/mnt/data/lspv1_483_raw.json` constructed literal original-source Resolution+weakening DAGs on odd-charge K4 Tseitin (16 proper 3-CNF clauses, 6 variables). Cases s=0,1,2,3 required all 1,2,4,8 branches and produced 47,63,79,91 total nodes (all original-source checked), final empty, with 11 corruption/omitted-AND/false-source mutations rejected. Odd-charge has 0 models, even-charge has 8. Peak Python tracemalloc measured 79,743 bytes, 0.0241 s host runtime on that test only.

A separately written GitHub JavaScript verifier `experiments/arc/lspv1_483_def_budget_guard_control.cjs` reproduced all four node counts and 11 rejections, and evaluates a two-gate example g1=x1 XOR x2, g2=g1 AND x3 with original dependency support 3<=2d=4. This is a **guard-lift control**, NOT a historical accepted-byte R_mix341 check, not a complete compiler for arbitrary mixed proofs, and not a reproduction of Pang's asymptotic theorem. It does independently validate exact source/resolution/weakening/guard mechanics; no false branch-local lemma may be used without its guard.

**Resource ledger:** Given a valid q-node mixed certificate and its complete input, symbolic translation has O(2^s(m+q+1)) target nodes, explicit bit cost O(2^s(m+q+1) poly(n+d+log(q+m))), and realizable construction, references, source/index reads, gate evaluation, branch-join, output, verification and simultaneous peak storage polynomial in that explicit output bound. The proof's free minimization excludes discovery; an implementation must charge actual proof search and failed candidates separately. Host-level tests are not FLMV native-machine measurements. No hidden free gate, splitter, optimizer or unit-cost large-inference convention was added.

## Status and next transfer

**Actual mathematical advance:** a definition-input-support-sensitive **parameterized** restriction, narrowing the known bounded-local hard family to proofs with o(n) paid fresh gates and showing any polynomial-work candidate in this declared grammar must use Omega(n) paid gates. This is an assembly of /481 and Pang plus a proved guard-lifting argument, novelty relative to external literature unclaimed.

**Open:** [P2-D1] full historical grammar, [P2-C3] simulation under unbounded recursive definitions/private ports, [P2-B1] unrestricted superpolynomial mixed minimum, [P2-B2] noncircular B3. Root main.tex was not rewritten because large-file complete readback cannot be safely authenticated. No schedules, roles, weights or Route A/B allocation were changed. P versus NP OPEN.
