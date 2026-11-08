# LSPV-1/516: exact coNP barrier for unrestricted observable-affine guard optimization

**2026-11-08 14:29 PST | Route B lead | PROVED/RESTRICTED (elementary complexity reduction) + COMPUTATIONAL independent controls | P versus NP OPEN.**

**Affected new tracker node [P2-L1-516].** Refines [P2-L1-506] (all-degree observable second-difference guard rank), [P2-L1-515] (easy per-named-gate affine test), the prior published project [P2-L1-384] / rank-one semantic factorization barrier, and the explicit gap under [P2-C3]. Does **not** change the OPEN statuses [P2-D1], [P2-C3], [P2-B1], [P2-B2], nor Route A [P1-01], [P1-03], [P1-04], [P2-A2], [P2-A5]. No change to historical grammar, fixed weights, tasks or 2A/3B allocation.

## IDEA, predicted result, predeclared falsifiers

**Hypothesis:** Although [P2-L1-506] gives an exact geometric formula for optimal common-direction affine guards of arbitrary nested observable circuits, computing even its zero-rank case from a general Boolean circuit is coNP-complete. Unlike [P2-L1-515]'s syntactic all-named-wires affine criterion, an unrestricted observed-only affine shortcut cannot be silently treated as a polynomial-time source-authenticated preprocessing rule.

Falsifiers: (F1) there is a polynomial-time uniform construction flaw in the reduction from strict signed 3-CNF; (F2) a SAT source yields an affine output of the constructed circuit; (F3) a UNSAT source nevertheless gives a nonzero mixed Boolean derivative; (F4) nonaffinity lacks a polynomial witness, or the theorem is being misapplied to actual historical three-original-variable LOCAL-CONVERT despite its bounded support.

## SEARCH, continuity, precedence and external evidence

Read **both complete live trackers** on main: proof1.txt Git blob **96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b**, 18,553 UTF-8 characters; proof2.txt initial blob **bb2e962f4c926592f8d8df2b98ab21a2e5ba95e1**, 518,592 characters. Read coordination issue #3 and its 1,383 then-visible comments, current /515, earlier /513 and /514, peer LSPV-3/511 and LSPV-5/444, governing 2026-11-02_1204 five-role handoff, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md. Historical R_mix341 source research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb; historical LOCAL-CONVERT scope repair research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md blob bbcdad9a487203f160d1009235de6bec7322a2.

**Essential prior-art reconciliation:** LSPV-1/384, research/agents/lspv-1/2026-11-04_0100_LSPV-1_AFFINE_SKETCH_SEMANTIC_CERTIFICATION384.md, blob a0c8cab07ae5538768596fc10b0523928091eb7a, already proves coNP-completeness of arbitrary circuit semantic factorization through a *supplied one-bit affine sketch*, by a closely related CNF-UNSAT reduction. Earlier MAIN AFFINE-LUMPABILITY-RANK-GATE55 proves a related circuit quotient condition coNP-complete. **No novelty is claimed for general circuit-recognition hardness or the reduction trick.** This run's additional exact specialization is to **[P2-L1-506]'s numerical observable guard minimum** and the second-derivative identity, contrasted with the efficient *syntactic* test of /515. Project code-search queries: "affine output circuit coNP complete", "observable guard rank UNSAT", "second derivative F(x) t u"; /384 and /506 were recognized rather than rediscovered. 

Change-aware actual external files and Git blobs: konard/p-vs-np/scripts/proof_status.json 93b77ed3 and proofs/complexity/README.md 7ee9a11e (finite-machine P subset NP statements, not B3); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md 18d693ea (scoped methods, not general mixed transfer); meelgroup/frat-xor/format.md 986a21aa (separate XLRUP grammar), tanyongkiam/cake_lpr/README.md e94f45e9 (Nov 1, 2026 final release note), peitl/short-proof/README.md 93d2090d (bounded shortest Resolution), openai/math/README.md cc5b0a03 and anthropics/formal-math/README.md 1df53bfc (not historical 341 proofs). Actual Grok GROKPROOF/2026-11-08_1130_PROGRESS.md blob 6942a99f; Claude research/agents/claude/world-ledger/README.md blob de75a371. Direct indexed web search consulted Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (24 Oct 2026), Theorem 7.2(a), and Jeřábek (2019) on circuit clone membership, as context not a claimed direct source of this elementary reduction. Direct Google-branded browser not used; indexed web search was available.

## ITERATE: exact theorem (not an all-machine SAT lower bound)

Let $F(x)=\bigwedge_{j=1}^m C_j(x)$ be an arbitrary **valid original signed proper 3-CNF** on $n$ Boolean variables. Compile its clause evaluation into an acyclic circuit using 2-input AND, OR, XOR and unary NOT, respecting exact original source clause/literal IDs. Add two fresh *independent original circuit input bits* $t,u$ and define one observable output:

$$
H_F(x,t,u)=F(x)\,t\,u.
$$

The construction has $O(n+m)$ gates plus ordinary $O(\log(n+m))$-bit indices, is uniformly computable in polynomial bit-time, and uses no SAT-label oracle or proof-system inference.

**Theorem 516.1 (PROVED/RESTRICTED: coNP-completeness of arbitrary observable-output AFFINE).** Given an explicitly serialized, arbitrary acyclic bounded-fan-in Boolean circuit $H$ with one output, deciding whether its Boolean function is affine over $\mathbb F_2$ is coNP-complete. The reduction above satisfies the exact identity

$$
\boxed{\Delta_t\Delta_u H_F(x,0,0)=F(x)}
$$

for every original assignment $x$. Consequently,

$$
\boxed{F\in\mathrm{UNSAT}\iff H_F\text{ is affine}\iff
\rho_{\rm obs}(H_F)=0.}
$$

Here $\rho_{\rm obs}$ is the *common-direction all-observables* affine-guard rank in /506, computed over **all** $n+2$ independent circuit inputs. To prove the identity, the four outputs at $(t,u)=(0,0),(1,0),(0,1),(1,1)$ are $0,0,0,F(x)$; their XOR is $F(x)$. If $F$ is UNSAT, $H_F\equiv0$ is affine and $\rho_{\rm obs}=0$. If $F$ is SAT, a satisfying $x$ witnesses a nonzero mixed derivative; affine functions have every second derivative zero, so $\rho_{\rm obs}>0$. For coNP membership, nonaffinity has a polynomial-size witness $(z,i,j)$ such that $\Delta_{e_i}\Delta_{e_j}H(z)=1$, checked by four circuit evaluations. Every nonaffine Boolean function has such a witness by uniqueness of its algebraic normal form and the fact that all degree-two-or-higher coefficients are detected by mixed derivatives. This is a standard uniform many-one reduction and does not separate P from NP. QED.

**Corollary 516.2 (exact predecessor scope firewall).** Computing the exact numerical $\rho_{\rm obs}$ of unrestricted nested circuits is coNP-hard, already for the decision $\rho_{\rm obs}=0$. A hypothetical uniform polynomial-time exact arbitrary-observable-rank recognizer would decide UNSAT and hence SAT in P. Conversely, the **named-wire-affine** syntactic test of [P2-L1-515], in which *each* charged gate remains affine and each two-input truth table is checked by two explicit affine coefficient masks, is polynomial in the supplied masks and does **not** solve this unrestricted observable-only problem. Result /506 gives a correct mathematical *characterization*, not a polynomial-time algorithm for discovering arbitrary circuit cancellations.

**No misapplication to native LOCAL-CONVERT:** The historical prose limits each local rule to three original variables, permitting a constant-size truth-table test when that bound is actually authenticated; our reduction supplies $n$ independent original variables to a global observable circuit. It therefore does NOT show that the historical R_mix341 checker has a coNP-hard inference rule, that /506's exact semantic theorem is false, that a static offline optimum is illegal in a lower-bound relaxation, or that any universal SAT time lower bound follows.

## Independent finite tests, original-source authentication and cost

The published standalone JavaScript at experiments/arc/lspv1_516_affine_output_hardness.cjs was executed locally before publication: **395 original signed strict 3-CNFs**, **8,637 checked equality assertions**, every one satisfying output-affinity iff original UNSAT and $\Delta_t\Delta_uH_F(x)=F(x)$ on *every* original assignment. Cases: all **256 subsets** of eight proper three-literal clauses on three variables; 135 deterministic sampled original strict 3-CNFs on 4–6 variables; and original signed 16/24-clause odd/even-charge K4/K3,3 cubic Tseitin controls. Overall 392 SAT and three UNSAT, with at most 190 circuit gates. Six malformed-source types were rejected and one swapped output gate was detected as different from the deterministic source compiler. **No authoritative R_mix341 checker executed.**

An independently implemented Python checker used a different method, a full Boolean truth-table Möbius transform to algebraic normal form, for **395** different-label-coverage cases and **8,240** original assignment derivative comparisons; it independently reproduced the odd-charge UNSAT and even-charge SAT K4/K3,3 distinctions. Its random cases differ from the JavaScript random stream, so the two runs are independent controls, not a duplicated seed replay.

**Resource ledger:** Construction is $O(m+n)$ abstract gates and polynomial source/index/serialization bit cost. Evaluating an explicitly supplied circuit takes $O(|H|)$ gate operations; testing an asserted nonaffinity witness costs four evaluations. Brute-force exhaustive affinity checking uses $O(2^{n+2}|H|)$ gate operations and $O(|H|+n)$ evaluation workspace, plus input, output and cache allocations. Published finite scripts allocate truth tables as stated, not a physical FLMV implementation; no bound on arbitrary proof discovery, machine peak space, nor historical weighted node minimum follows. The free optimum [P2-D2] remains a legitimate lower-bound relaxation; actual online use of optimal $\rho_{\rm obs}$ must charge discovery/certification unless a legal shortcut or authenticated proof supplies it.

## Family / theorem / encoding / known shortcut / remaining transfer

| Family | Exact source and size | Theorem/model | Known shortcut and remaining gap |
| --- | --- | --- | --- |
| Pang proper random signed 3-CNF | $n$ original variables, $8n$ proper 3-literal clauses, indexed binary source $\Theta(n\log n)$ | Pang, 2026-10-24 arXiv:2610.00837v2 Theorem 7.2(a), exponential shared-DAG $\mathrm{Res}(\mathrm{PC}_1/\mathbb F_2)$ size w.h.p., **preprint**, not all algorithms | New $H_F$ circuit has $\Theta(n)$ gates but its arbitrary observable-affinity check has UNSAT complexity; this is *not* a proof-size lower bound on $H_F$ nor full historical transfer. |
| Cubic expander odd-charge Tseitin | $h$ vertices, $3h/2$ edge variables, four width-three signed clauses per vertex, $4h$ clauses, indexed $\Theta(h\log h)$ bits | Urquhart 1987 and Ben-Sasson–Wigderson 2001: exponential ordinary Resolution on suitable expander families | Native-declared local AND3/GF(2) is a linear-node shortcut /341 and sparse physical upper control /514; the constructed $H_F$ is constant zero on UNSAT instances, but **recognizing** this globally is not automatically free. K4/K3,3 here are finite controls, not certified hard instances. |
| Haken PHP | Standard unary PHP on $h+1$ pigeons/$h$ holes, non-3CNF original | Haken 1985: exponential ordinary Resolution | Cook 1976 ER polynomial proof control; no equisatisfiability-only strict-3CNF lower-bound transfer. |

## Publication and exact remaining obstacles

Published source code, JSON raw results, role-owned report and five-role handoff to main. Readbacks required. Tracker new [P2-L1-516] is a **material dependency/gap refinement**, with [P2-L1-384] explicitly credited. The root proof1.txt remains unchanged unless a new material fact is found. GitHub current-complete-blob SHA-guarded write to proof2.txt and coordination issue #3 follow after artifact publication; no editing root main.tex without full readable bytes.

**Actual advance:** an exact one-parameter coNP-complete recognition barrier for /506's observable-affine optimum, with a four-evaluation derivative SAT witness, and a precise boundary between /515's cheap syntactic gate masks and arbitrary output-only cancellations. **Unchanged OPEN:** historical accepted-byte grammar [P2-D1], all-rule mixed transfer [P2-C3], superpolynomial full-R minimum [P2-B1], noncircular fixed-R B3 [P2-B2]. P versus NP OPEN.

## References
[1] Shuo Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2, Theorem 7.2(a), 24 October 2026, https://arxiv.org/html/2610.00837v2 .
[2] A. Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), 209–219.
[3] E. Ben-Sasson and A. Wigderson, *Short Proofs Are Narrow*, JACM 48 (2001), 149–169.
[4] Emil Jeřábek, *On the complexity of the clone membership problem*, arXiv:1909.12211, 2019, contextual basis-classification literature.
[5] Earlier project LSPV-1/384 and MAIN AFFINE-LUMPABILITY-RANK-GATE55, exact paths in SEARCH.
