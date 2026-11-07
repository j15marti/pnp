# LSPV-3/482: Wide-pivot locality obstruction and shared source-authenticated clause export

**November 7, 2026, 13:24 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**Tracker dependencies:** [P2-D1] historical exact grammar OPEN, [P2-C3] full mixed normalization OPEN, [P2-D2] assumption-safe branching OPEN, [P2-D3] evidence-bit accounting OPEN, [P2-B1] whole-mixed superpolynomial lower bound OPEN, [P2-B2] same-fixed-calculus noncircular B3 OPEN. This run extends the scope of [P2-L3-479] and [P2-L3-480] only within a separately declared owner-indexed FACET-A DEF/RES fragment. It is not an authoritative accepted-byte R_mix341 proof.

## IDEA before SEARCH: predictions and four falsifiers

Hypothesis: every authenticated ordinary shared Resolution DAG can export **all** its nonunit clauses to fresh OR-output units with polynomial additional paid owner-indexed gate definitions and strict Resolution inferences, sharing repeated gate prefixes. Nonetheless, a *single wide Resolution step* cannot in general be compiled directly as a constant-three-original-support AND3/LOCAL-CONVERT step merely by renaming its clauses to compact outputs.

F1: an exported clause cannot be justified using only conservative two-input OR DEF facets plus correct-pivot Resolution. F2: prefix gate sharing changes original-source entailment or illicitly shares branch-local assumptions. F3: two wide pivot parents have a nontrivial consequence supported on at most three original variables, contradicting the locality obstruction. F4: the native historical /341 byte grammar already expressly licenses a multiported constant-support conversion without separately justified facets, making the obstruction inapplicable to the stated proposed interface. Results below reject F1-F3 in the declared fragment; F4 remains **unresolved for the historical parser**.

## SEARCH: source, established-hard family, and exact model

Read complete root `proof1.txt` and `proof2.txt`, current issue #3, governing November 2 handoff, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, original `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` at blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`, LSPV-3/436, /479, /480, /481, LSPV-1/486 and red-team /416. Also read actual `GROKPROOF/2026-11-07_1920_PROGRESS.md` and `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`.

Original /341 fixes binary RES, AND3 on combined support <=3 original variables, unary constant-support LOCAL-CONVERT, paid conservative binary DEF, XOR on affine rows and unit logical weights. It **does not provide a complete accepted-byte DEF facet selector, output-port namespace, or complete mixed verifier**. LSPV-3/436 already established the acceptance fork between owner-indexed FACET-A and opaque GATE-B. The present positive compiler requires FACET-A. Neither completion is silently declared historical.

Established reference families remain cubic-expander odd Tseitin (4h strict-three source clauses, 3h/2 edge variables, ordinary shared-DAG Resolution exponential by Urquhart and Ben-Sasson/Wigderson, but original /341 admits a 4h-1 AND3/GF(2) certificate), and Pang's random proper strict-3CNF F(n,3,8n), exponential published **syntactic Res(XOR)** minimum in the stated theorem, with no proved transfer to every R_mix341 rule. Standard Cook ER and parity/GF(2) shortcuts remain mandatory upper bounds. The **two-clause wide-pivot counterexample here is intentionally a small focused control in general CNF**, not a newly certified hard strict-3CNF family. Equisatisfiable padding into 3-CNF is not assumed to preserve the local-projection theorem on all new source coordinates.

Primary references checked: Shuo Pang, arXiv:2610.00837v2, Theorem 7.2(a); Itsykson-Riazanov-Smirnov, SAT 2022, 10.4230/LIPIcs.SAT.2022.6 (regular Resolution model only); original /341 report above. Actual required repository revisions: `konard/p-vs-np` head `ecedd2b45f1c524d85c00b2da27a9c140025550c` `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research` head `7dedc73f758dfbdc072e7aa29dfc08505761ebd5` `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `meelgroup/frat-xor` `format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`; `tanyongkiam/cake_lpr` README blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; `peitl/short-proof` README blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab`; `openai/math` README blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`. The first two make no established P-versus-NP claims usable here; the others implement distinct proof languages, not native /341 authority. Indexed public literature search was performed; no Google-branded engine or official checker execution is claimed.

## ITERATE: theorem 482.1 (PROVED/RESTRICTED, whole Resolution-DAG export)

Assume a finite source-authenticated ordinary Resolution DAG \(\pi\) with \(q\) distinct paid RES nodes, non-tautological clauses \(C_1,\ldots,C_t\), and ordinary signed literals. Count all original source and derived clauses chosen for export, with widths \(k_i\ge2\), and put
$$
L=\sum_{i:k_i\ge2}(k_i-1).
$$
In a distinct **FACET-A** calculus, introduce globally fresh conservative \(z=u\vee v\) DEF gates, one paid node per gate whose three defining clauses are owner-addressable:
$$
(\neg u\vee z),\qquad(\neg v\vee z),\qquad(u\vee v\vee\neg z).
$$
Signed original inputs are permitted and all outputs are globally fresh. For \(C=(\ell_1\vee\cdots\vee\ell_k)\), chain \(z_2=\ell_1\vee\ell_2\), \(z_i=z_{i-1}\vee\ell_i\) for \(i\ge3\). Apply strict oriented RES twice per gate, using the two owner-qualified facets \((\neg u\vee z)\), \((\neg v\vee z)\), and obtain the single unit \((z_k)\). Every step is a syntactic source-authenticated entailment and is independently checkable from signed clauses; NO global semantic implication oracle or extra inference rule is introduced.

Identical ordered-prefix definitions across different clause exports are canonicalized and paid **once**, as a shared-DAG node. With \(g\le L\) distinct gate definitions, the complete augmented proof has at most
$$
\boxed{q+g+2L\le q+3L}
$$
paid nodes in this fragment, excluding free original source premises. Output units inherit their parent clause's assumption scope \(\Gamma\); gate definitions are globally conservative and assumption-free. Reuse the *definition* across branches, not a derived branch-local *unit* unless \(\Gamma\) is justified. All OR alternatives remain alternatives and all required AND branch obligations remain mandatory. The complete **original proof remains intact**: this is an augmentation/export, NOT normalization of all mixed rules or a substitute refutation. Width-one clauses need no new gate and an empty terminal clause is already a contradiction.

**Certificate bits:** if \(V\) is the number of named original/derived variables and \(M\) the total literal occurrences in \(\pi\) plus exports, there are \(O(M)\) new IDs, each in \(O(\log(V+M+2))\) bits. The extra output, source/parent references, owner/facet selectors, full facet checking, generation and revalidation all have polynomial bit complexity in the explicitly encoded input proof. The logical node bound says nothing about optimal proof-search cost, peak machine memory or same-machine FLMV exponents.

## ITERATE: theorem 482.2 (PROVED/RESTRICTED, sharp original-support barrier)

For each integer \(k\ge1\), choose \(2k+1\) distinct original variables \(x,a_1,\ldots,a_k,b_1,\ldots,b_k\). Set
$$
F_k=(x\vee a_1\vee\cdots\vee a_k)\land(\neg x\vee b_1\vee\cdots\vee b_k).
$$
One legal RES pivot on \(x\) produces the width-\(2k\) resolvent
$$
D_k=a_1\vee\cdots\vee a_k\vee b_1\vee\cdots\vee b_k.
$$
**Every projection of \(\mathrm{Mod}(F_k)\) onto any set of at most \(k\) original coordinates is the full Boolean cube.** Proof: if the projected assignment fixes \(x=0\), at least one \(a_i\) is free and can be set true; \(x=1\) has the symmetric \(b_i\) extension. If \(x\) is unassigned, choose its value so that the one nontrivial disjunction has a free or satisfied leaf. Failure on both sides would require all \(2k\) leaves to have been fixed false, impossible with at most \(k\) fixed coordinates. All remaining bits are arbitrary. The bound is sharp: each source clause is a nontrivial \((k+1)\)-coordinate consequence.

Therefore, for \(k\ge3\), \(F_k\) entails **no nontrivial condition involving at most three original variables**, despite its legal wide RES inference. Conservative OR-gate definitions and true exported units project back to exactly \(\mathrm{Mod}(F_k)\); counting their one-bit output labels as *free original support one* would be unsound. The result rules out only a **direct bounded-three-original-support semantic conversion from these two premises alone**. It DOES NOT rule out an indirect native chain with other justified clauses/definitions/Resolution, and does not yield a lower bound on complete R_mix341 or SAT algorithms.

## Finite computational controls and resource accounting

Original source projection and strict RES were checked for \(k=2,3,4,5\): respective original model counts \(24,112,480,1984\), all projections of support <=3 (\(26,64,130,232\)) tested. The \(k=2\) sharpness control has exactly two nonfull three-coordinate projections; \(k\ge3\) has none. A separate, independently written Python implementation confirmed all counts and rejected four malformed clauses.

The published pure-JavaScript executable generates a four-clause proof DAG (three source clauses and one RES clause), exports every clause, checks conservative gate facets and all strict pivots, and tests corrupted input/pivot controls. With clause widths \(4,4,4,6\), \(q=1\), \(L=14\), globally shared gate count \(g=12\), the positive produced upper-bound construction uses exactly \(q+g+2L=41\) distinct paid nodes rather than \(q+3L=43\) without sharing. This is an exhibited construction, NOT the global optimal minimum. Host execution is finite; no native historical R_mix341 parser or native FLMV machine executed. Construction of every lookup, gate, source read, RES check, serialization, output, cache, proof replay and optional failed tests is additional charged algorithmic work; host peak RSS and TM T/S exponents are not claimed.

## Handoff and open implications

For LSPV-1 and LSPV-5: authenticate historical source-byte owner-indexed DEF facets, the exact original-coordinate support rule, and whether RES-derived gates and LOCAL-CONVERT consumers accept the exported type; test lexical ID collisions [P2-L5-415/416] in any proposed compiler. For LSPV-2/LSPV-4: sharing is a legal upper-bound control, not a promised contraction; raw full sources do not imply recursively iterable all-input FLMV applicability. All five roles keep two Route A / three Route B, historical identities, weights, schedules and permissions.

This theorem makes the interface obstruction more precise and supplies a whole-DAG **restricted** compiler, but does not close [P2-D1], [P2-C3], [P2-B1] or [P2-B2]. B1/B2/B3 and P versus NP remain OPEN. Root main.tex was not edited because a complete safe content read was unavailable, and an inferred replacement is prohibited.

## Publication

Report: `research/agents/lspv-3/2026-11-07_1324_LSPV3_WIDE_PIVOT_SHARED_PORT482.md`; executable: `experiments/arc/lspv3_482_wide_pivot_and_shared_export.cjs`; raw: `results/raw/arc/2026-11-07_1324_LSPV3_WIDE_PIVOT_EXPORT_RAW.json`; handoff: `research/coordination/2026-11-07_1324_LSPV3_WIDE_PIVOT_SHARED_PORT482_FIVE_ROLE_HANDOFF.md`.