# LSPV-3/408 | Paid local port-alias RES macro
**November 4, 2026, 19:27 PST. Role: PNP Hypergraph & Proof Certificates.**
**Status:** PROVED/EXACT under the explicitly stated, still unratified addressable-DEF-clause interface; independent red-team review pending. Finite controls are COMPUTATIONAL. The full fixed R_mix341 grammar, original-source-retracting all-rule translation, B1/B2/B3, superpolynomial mixed hardness and P versus NP remain OPEN.

## IDEA, before searching
**Falsifiable hypothesis:** The coNP-complete global semantic port equality problem (LSPV-3/407) has useful *strict RES proof-carrying* subcases. With paid functional fresh gates, a bounded local Boolean identity can yield an exact, source-independent equality certificate by Resolution, without assuming a free semantic alias oracle.
Falsifiers: (1) XOR cancellation or distributivity fails as a genuine tautological alias; (2) an invalid RES pivot passes checking; (3) an inequivalent port pair passes as equal; (4) the construction is incorrectly advertised as polynomial for unbounded gate count. The positive first three tests passed or rejected the hostile example; the fourth demands a bounded-size restriction.

## SEARCH and duplication audit
Read, first, the governing handoff at research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (blob 033b54b87b7cbe94912af5cf67daa52859143a07). The **authoritative native** R_mix341 rule source is research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. It charges one node for each fresh functional binary DEF with its defining relations attributed to that node. It DOES NOT fully serialize how an individual DEF defining clause is selected as a subsequent RES antecedent. Nor does it settle LOCAL-CONVERT private/public internal wire exports or GF(2) row exports. The theorem below is explicitly conditional on a readable-DEF-clause syntax; it does not change native R.

Reviewed current issue #3, REFEREE350/351, LSPV-1/406, LSPV-2/406, LSPV-4/400, LSPV-3/407, the original local grammar addendum, AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md. LSPV-3/407 already proved global semantic alias coNP-complete and structural gate signature merging; LSPV-4/400 already showed implication-changing rewrites can invalidate consumers. The new contribution here is a narrow nonstructural paid local RES alias certificate.

Actual Grok and Claude directories were listed. Read newest Grok GROKPROOF/2026-11-05_0315_PROGRESS.md (blob 2c21a1eb) and Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727) and ..._1521_CLAUDE_ONETAPE-0001.tex (blob 9a5b05d6). None supplies B3.
Web queries: "Cook Reckhow 1979 relative efficiency propositional proof systems polynomial bounded iff NP coNP pdf"; "Krajicek p bounded extended Frege whether NP equals coNP implies EF polynomial size proofs"; "Haken 1985 intractability of resolution pigeonhole principle ordinary resolution full paper"; "extended resolution proof checking DRAT LRAT circuit extension definitions proof verification local rules"; "Jan Krajicek Extended Frege proofs circuits and rewriting 2026 pdf seven gates approximate relation". Read original Cook publications index, Cook-Reckhow publisher paper, Buss 1987, and full June 2026 v1 of Krajicek's circuit-rewriting paper. **Important version correction:** arXiv:2606.13367v2 of October 15, 2026 describes an $O(k\log k)$ circuit rewrite chain conditioned on an existing EF/CF equivalence proof; the complete revised v2 text was not retrieved, so its v1 seven-gate assertion is not promoted as a v2 theorem.
Authenticated OpenAI GitHub searches: "proof certificate SAT resolution", "CookLevin", "ExecCNF", "ImplementationCertificates". Read full openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNF.lean (SHA e60f4d98) and RuntimeAssembly.lean (SHA 41df76f4). They are not an Rmix341 proof compiler. Direct Google-branded search unavailable; general web and authenticated GitHub search used instead.

## ITERATE: exact restricted theorem
**Readable-DEF-clause assumption (unsettled native field):** every globally fresh paid binary DEF's exact 3-variable gate CNF has at most four defining clauses. Each clause is referenceable as an existing charged DEF node's clause premise by RES, with a separately encoded selector and proper charged bit access. This is an interface assumption, not an introduced free inference.

Let $r\le3$ independent already available boundary bits feed an acyclic network of $b$ separately paid fresh binary Boolean gates. Two **distinct** designated output references $p,q$ compute the same **nonconstant** Boolean function of these $r$ boundary bits under every valuation.

**Theorem (strict RES local alias):** Under the readable-DEF-clause assumption, there is a shared strict-Resolution derivation from the gate defining clauses of BOTH clauses
$$
(\neg p\lor q),\qquad (p\lor\neg q).
$$
At most $3^{r+b}$ distinct non-tautological clauses occur, including defining clauses. Each individual RES step has two authenticated parents and an explicit complementary pivot. Paid gate count is $b$; no equality oracle or instance-specific SAT-label axiom is used. For a fixed gate bound $b\le b_0$, logical node and evidence-bit overhead of this local proof are polynomial in source and existing wire-ID lengths. No polynomial bound in *unbounded* $b$ follows.

**Proof.** Every valuation of the $r$ boundary bits extends uniquely through the acyclic fresh binary definitions. Let $f$ be their common output function. Existential projection of the exact defining CNF onto $(p,q)$ therefore has exactly the satisfying pairs $(0,0)$ and $(1,1)$: both occur by nonconstancy; neither unequal pair can occur. Davis-Putnam elimination of all other wires yields by strict binary Resolution an exact CNF of the projected relation. Any non-tautological clause on $p,q$ that excludes $(1,0)$ while allowing both equal pairs must be $\neg p\lor q$; likewise excluding $(0,1)$ forces $p\lor\neg q$. Thus the projection contains both clauses, and each is a strict RES consequence of the paid definitions. A clause over $r+b$ Boolean wires has three choices per variable (absent, positive or negative); there are at most $3^{r+b}$ non-tautological clauses, each introduced once. QED.

**Necessary caveat:** for constant outputs the strict RES closure may provide two *unit* clauses but not the desired binary equality clauses, because weakening is NOT an Rmix341 rule. Source restrictions forcing local constants cannot be used as free unconditional aliases. For arbitrary long or high-width reconvergent circuits the exponent $3^{r+b}$ is not polynomial. The theorem certifies a bounded local rewrite only, and does not establish consumer-safe AND3, GF(2) or LOCAL-CONVERT transport.

## Computation and independent verification
A strict Davis-Putnam RES producer and separately authored verifier ran on all original input valuations and on every emitted inference. Cases:
| Boolean identity | Original inputs | Paid DEF gates | Defining clauses | Generated RES nodes | Result |
| --- | ---: | ---: | ---: | ---: | --- |
| $(x\oplus y)\oplus y=x$ | 2 | 2 | 8 | 6 | Both equality clauses |
| $(x\wedge y)\lor(x\wedge z)=x\wedge(y\lor z)$ | 3 | 5 | 20 | 44 | Both equality clauses |
| $x\oplus y$ vs $x\wedge y$ | 2 | 2 | 8 | 6 | Correct rejection |
| $(x\wedge y)\lor(x\wedge\neg y)=x$ | 2 | 3 | 12 | 15 | Both equality clauses |

Producer: 550 checks; independent verifier: 863 checks on 119 explicitly labelled proof clauses. Malformed inputs and corrupted pivots rejected. An initial all-pairs saturation timed out for distributivity and was replaced by DP elimination. A negative-control assertion was corrected from "unequal on all valuations" to "unequal on at least one". Full machine-readable traces, producer and verifier are in the local reproducibility archive, not falsely claimed as GitHub-committed source. SHA256 producer e1d1458e6fadd8a86fd7d50f055bad730d3ba8885e8dea39ad0f88338dcf6eb1; verifier 6aad407955f2bca5019419b9740a979018f3fe93a72c01cfd55614efdfa19793; trace 24d6d1a9cd28ab5afbf566a1611a53f6d257b1bd0cbf333ecca78156df8a7e83.

**Physical costs:** The derived clauses require $O(v3^v\log(n+b+3^v))$ explicit bits for $v=r+b$, plus $O(b\log(n+b))$ gate-definition bits. Actual parsing, selection, failed attempts, proof checking, memory and output are separate and were not converted to unrestricted machine lower bounds. No all-phase peak memory or FLMV resource bound is claimed.

## Hardness and B3 safeguard
Haken's 1985 theorem: ordinary shared-DAG Resolution requires $2^{\Omega(h)}$ lines on the standard explicit signed PHP with $h+1$ pigeons and $h$ holes, encoded $N_h=\Theta(h^3\log(h+2))$ bits. It does not bind Rmix341 or general algorithms. Cook's polynomial Extended Resolution proofs and odd-Tseitin GF(2) shortcuts are required negative controls. The weakest B3 is still OPEN:
$$
\mathrm{SAT}\in P\ \Longrightarrow\ \exists C,k\ \forall N:\quad \overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^k.
$$
Krajicek's conditional chain begins with a supplied feasible EF/CF proof, not a correctness proof for any hypothetical SAT decider. B1/B2/B3, superpolynomial mixed lower bound and P versus NP remain OPEN.

## Next precise gap
Resolve the authoritative native DEF clause selector grammar and LOCAL public-root/exported-wire serialization. Then extend the local proof-carrying alias repair to constants and every downstream RES pivot, AND3 original support, GF(2) equation and LOCAL-CONVERT consumer, with encoded lengths and physical checking. The result cannot currently be promoted to an unqualified all-rule native normalization.

## References
[1] S. Cook and R. Reckhow, "The relative efficiency of propositional proof systems", Journal of Symbolic Logic 44 (1979), 36-50, https://doi.org/10.2307/2273702.
[2] S. Buss, "Polynomial Size Proofs of the Propositional Pigeonhole Principle", JSL 52 (1987), https://www.cambridge.org/core/journals/journal-of-symbolic-logic/article/abs/polynomial-size-proofs-of-the-propositional-pigeonhole-principle/B864DC6741A4A220B14625CE1A6082C9.
[3] J. Krajicek, "Extended Frege proofs, circuits and rewriting", arXiv:2606.13367v2 (2026-10-15), https://arxiv.org/abs/2606.13367.
[4] A. Haken, "The intractability of resolution", Theoretical Computer Science 39 (1985), 297-308.
[5] S. Cook, "A Short Proof of the Pigeon Hole Principle Using Extended Resolution", SIGACT News 8(4) (1976), 28-32.
