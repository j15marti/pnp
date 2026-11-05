# LSPV-1/414: canonical implicit refutations are not fixed-R proof certificates

**November 5, 2026, 02:00 PST.** IDEA → SEARCH → ITERATE complete. All rules, unit weights, five roles, schedules and enabled states of fixed `R_mix341` unchanged. **PROVED/EXACT** for a separately defined implicit Resolution-plus-Weakening format (specialist review pending), **KNOWN** Haken and implicit-proof literature, **COMPUTATIONAL** finite controls, and **OPEN** same-fixed-R B1/B2/B3, native grammar, superpolynomial mixed minimum, P versus NP. This is an elementary explicit instantiation of known implicit-proof ideas, not a new complexity separation.

## IDEA and falsifiers before searching

Test whether a polynomial-bit program describing a valid exponentially long refutation, with every interior Resolution step legal, could be treated as a polynomial native R proof or yield B3 under SAT in P. Predictions: a canonical implicit tree exists for every UNSAT CNF; its all-leaf validity check is coNP-complete; unfolding to ordinary Resolution is exponentially costly on Haken PHP. Falsifiers F1: a SAT source passes the global checker; F2: malformed/different source passes authentication; F3: internal nodes are not exact binary resolvents; F4: polynomial unfolding into ordinary Resolution on PHP. Mandatory countercontrol: Cook ER PHP and native AND3/GF(2) Tseitin, which permit shortcuts in stronger calculi.

## Search and duplication audit

Read original fixed calculus `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (blob c87acd11), the governing Nov-2 12:04 handoff, current issue #3 through REFEREE358, AGENTS.md, CODEX.md and research skill, LSPV-1/357/408/412/413, LSPV-2/412, LSPV-3/417, LSPV-4/408 and LSPV-5/REFEREE358. Actual Grok `GROKPROOF/2026-11-05_1218_PROGRESS.md` blob d3183283 and Claude `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob 9a5b05d6 were read and do not establish B3. Authenticated github.com/openai code search `ExecCNFNodeSearchCosts` located, and full `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` blob 1ced21f4 was read: it charges an actual program run, but does not supply the mixed proof translation. Other code queries: project `DEF-facet`, `Grok`, `Claude`.

General-web searches included Cook–Reckhow 1979, Haken 1985, bounded-arithmetic reflection, implicit Resolution proofs, Krajíček implicit proofs, and Zi Chao Wang implicit Resolution. Wang 2013 constructs **a circuit plus an explicit correctness proof** and shows equivalence to EF; our bare canonical circuit has *no* such extra proof and is not an unconditionally polynomial-time Cook–Reckhow proof system. Direct Google-branded UI unavailable; web-engine and authenticated GitHub searches used instead.

## Exact model and theorem

Let F be a valid original-signed CNF over x_1,...,x_n, with complete original clause list and IDs. For each binary prefix p of length d define the blocking clause

$$
B_p=\bigvee_{i=1}^d\begin{cases}x_i,&p_i=0,\\\neg x_i,&p_i=1.\end{cases}
$$

At every internal node, the two children are $B_p\vee x_{d+1}$ and $B_p\vee\neg x_{d+1}$, whose exact binary resolvent is $B_p$. The root is the empty clause $B_\epsilon=\bot$.

The leaf program scans the original source and outputs the **first original clause falsified** by complete assignment a, or MISSING. When a clause C_j is returned, every literal of C_j is false under a, so C_j is a subclause of B_a. A separately declared **Weakening** step derives B_a from this original clause. Hence:

$$
\operatorname{Valid}_{\mathrm{implicit\ W+Res}}(F,G_F)
\iff
\forall a\in\{0,1\}^n\ \exists j:\ C_j(a)=0
\iff F\in\mathrm{UNSAT}.
$$

One constant node-label program plus a source-scanning first-false selector has a Boolean circuit of size poly(N), and the full original source is included for **exact syntactic** checking. The JSON SHA-256 is only an integrity diagnostic, not a cryptographic soundness assumption. The descriptor constructor runs in poly(N) time for **SAT and UNSAT** alike. It neither decides satisfiability nor supplies a native mixed proof.

**PROVED/EXACT:** CANON-TEMPLATE-VALID is coNP-complete. Its complement has a polynomial witness (an assignment with no falsified clause), and the map $F\mapsto(F,G_F)$ reduces UNSAT to this validity problem. Conditional on SAT in P, validity can be tested in P, thus providing a *different* polynomially bounded P-verifiable proof format. This only recovers Cook–Reckhow existence under P=NP, not the fixed-R B3 implication.

## Weakening elimination and explicit unfolding obstruction

For any explicit Res+Weakening refutation maintain a strict-Resolution-derived *subclause* of each node's clause. A source retains itself; Weakening reuses its parent. At a Resolution step, if both subclauses retain the complementary pivot, resolve; if one loses its pivot, reuse it because it is already a subclause of the intended resolvent. By induction the root subclause is empty. At most one strict resolvent is added per Resolution inference. Therefore Haken's ordinary shared-DAG Resolution lower bound applies unchanged to explicit Res+Weakening after this length-preserving conversion.

For the **standard unary pigeonhole** $P_h$ (h+1 pigeons, h holes, signed variables x_ij, pigeon at-least-one and pairwise hole-collision clauses), original encoded length $N_h=\operatorname{poly}(h)$, canonical implicit template length poly(N_h), but Haken proves every ordinary DAG Resolution refutation has $2^{\Omega(h)}$ lines. A polynomial-output all-input translation from these implicit circuits to *source-only explicit Res+Weakening* is therefore mathematically impossible, regardless of translation search time. **This counterexample is restricted to that weaker output calculus.** Cook's polynomial Extended Resolution PHP construction and native R_mix341's GF(2) odd-Tseitin shortcut prevent importing it as full-mixed hardness or as a native B3 refutation.

## Computation and physical costs

Python producer locally exhaustively tested all 256 subsets of eight signed 2-variable clauses: 95 SAT, 161 UNSAT; six PHP h=1..3 SAT/UNSAT; K4 odd/even Tseitin; empty CNF, empty clause, positive unit and opposing units. Eight malformed source inputs and four changed/mismatched descriptors rejected. Independent Node.js verifier passed **24,653 assertion groups** over 268 distinct fixtures, 5,585 internal checks and 5,189 leaf visits. PHP h=3 UNSAT has n=12 source variables, 189 compact source-JSON bytes, **604 exact-source descriptor bytes**, and **8,191 derived nodes in this particular explicit canonical tree**, NOT its optimum; the matched SAT source is rejected. K4 odd/even controls passed. Full local raw SHA-256: `539b275b292378e98eac2cdff647c7732cb17fbda972f911a968311c2ead01da`.

The implicit constructor uses poly(N) bit time and storage; actual full certificate verification by scanning leaves takes $O(2^n\operatorname{poly}(N))$ bit time and can stream with poly(N) scratch. The separate hypothetical SAT-in-P verifier is polynomial but uses **its own decider**, not a native paid R inference. Explicit canonical unfolding has $2^n-1$ binary resolutions plus at most $2^n$ Weakening nodes and incurs corresponding output and proof-check costs. No machine-time lower bound, FLMV transport, or claim that every proof has $2^n$ nodes is made.

## Transfer status

**FALSIFIED/RETIRED:** a short, source-bound implicit circuit with locally sound internal steps by itself is a polynomial native R refutation; or a generic polynomial-cost source-only Resolution unfolding. **OPEN:** (i) literal original R_mix341 DEF-facet/exported-wire/AND3/GF(2)/LOCAL-CONVERT selectors, all-consumer-preserving polynomial bit normalization, (ii) noncircular B3 for the **same fixed calculus**, (iii) superpolynomial mixed worst-case minimum and P versus NP. One still needs an independent, honest native proof of the universal leaf-consistency condition or a valid same-R reflection compiler, without smuggling a coNP check into a unit-cost inference. This is a representation/verification barrier, not a separation.

Full runnable producer, independent checker and full raw are attached as conversation artifacts. This GitHub report plus the five-role handoff are the append-only archival summaries. If canonical main.tex cannot be safely read in full and reconciled within LSPV-1 markers, leave it unchanged rather than replace it with a partial body.

### Primary references

[1] Haken A. *The Intractability of Resolution*. Theoretical Computer Science 39 (1985):297–308.

[2] Cook SA, Reckhow RA. *The Relative Efficiency of Propositional Proof Systems*. Journal of Symbolic Logic 44 (1979):36–50. https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf

[3] Krajíček J. *Implicit Proofs*. Journal of Symbolic Logic 69(2) (2004):387–397.

[4] Wang ZC. *Implicit Resolution*. Logical Methods in Computer Science 9(4):7 (2013). https://doi.org/10.2168/LMCS-9(4:7)2013

[5] Cook SA. *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*. SIGACT News 8(4) (1976):28–32.
