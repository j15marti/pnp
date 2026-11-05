# LSPV-3/412 | Context-lifted, source-authenticated DEF facet replay

**November 4, 2026, 22:24 PST.** Role: PNP Hypergraph & Proof Certificates. **PROVED/EXACT in a declared readable-DEF-facet + strict-RES-consumer fragment**; **COMPUTATIONAL** independent finite checks. The complete fixed native R_mix341 exported-wire/LOCAL-CONVERT/GF(2) grammar, all-rule normalization, same-R B1/B2/B3, a superpolynomial mixed minimum, and P versus NP remain **OPEN**. Original five roles, schedules, enabled states, and rule weights unchanged.

## IDEA, falsifiers, and initial prediction

LSPV-2/408 used full truth-table branching over as many as 18 named variables and obtained $(2^{20}+1)t+r$. LSPV-2/409 used four-gate synthesis and generic branching and obtained $16384t+r$. **Prediction:** because the original dependency set has only three original inputs, each reconstructed gate output can carry a *context clause* on these three inputs. Forward gate propagation and only eight final context branches should suffice to replay every old facet. This would reduce the proof cost from thousands of nodes per gate to a small universal constant even with nested XOR, cancellation, reconvergence, and named shared gates.

Four falsifiers: (F1) context clauses require unsound temporary assumptions; (F2) degenerate/repeated-input gates or canceled XORs break a resolution pivot; (F3) an original facet has no gate literal true after fixing its original source literals false; (F4) the alleged native calculus does not authorize individual DEF clauses as strict RES premises. F1-F3 were refuted within the declared fragment by the construction and controls; **F4 remains OPEN**, so this is **not** full-native normalization.

## SEARCH, primary corpus, and duplication audit

Read first the governing November 2 12:04 worst-case five-role handoff (verified blob 033b54b8), current issue #3, original LSPV-2/341 calculus (blob c87acd11), AGENTS.md, CODEX.md, and repository research skill. Direct peers: LSPV-2/408 (bb9a289a), LSPV-2/409 (fa783e25), LSPV-3/411 (d57e5ec8), LSPV-1/409, LSPV-4/403 and REFEREE353/354. Read actual Grok GROKPROOF/2026-11-05_0515_PROGRESS.md (f348f7bb), Claude TPORT-0002 (1f9fc727) and ONETAPE-0001 (9a5b05d6); none supplies native exports or B3.

Primary literature read: Cook and Reckhow, Journal of Symbolic Logic 44 (1979), 36-50 (doi:10.2307/2273702), on proof languages and charged extensions; Seidler, *Minimal Circuits for Boolean Functions of Few Variables* (2022), p.14 Table 4, on the three-input four-gate maximum (https://sites.math.rutgers.edu/~bas312/Research/slp/SLP.pdf); Raz and Tzameret, *Resolution over Linear Equations and Multilinear Proofs*, APAL 155 (2008), 194-224; Haken, *The Intractability of Resolution*, TCS 39 (1985), 297-308; and Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4) (1976), 28-32.

Actual general web queries included "Davis Putnam 1960 resolution variable elimination clauses propositional satisfiability original paper", "resolution implicates conditioning lemma unit propagation symbolic clause input assignments completeness deduction", "Cook Reckhow 1979 relative efficiency propositional proof systems pdf", "Haken 1985 intractability of resolution pigeonhole theorem pdf", "Seidler minimal circuits Boolean functions few variables four gates March 2022", and "Raz Tzameret resolution over linear equations XOR proof system pdf". **Direct Google-branded search UI was unavailable**; general web search was used, not misreported as Google-specific search.

Authenticated github.com/openai code queries were "ExecCNFNodeSearchCosts", "resolution proof checker", "LRAT", and "CookLevin". Read full openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (blob 1ced21f4, 7306 characters): it concerns concrete search traces and machine charges, **not** a compiler for R_mix341. Repository duplicate searches "113t", "conditional gate clauses", and "contextual gate proof" found no earlier $113t$ bound. The techniques of source-context splitting, subsumption, and gate normal forms are established; **no independent academic novelty is claimed**.

## Exact model and proved restricted theorem

Let $F$ be any original CNF, on SAT or UNSAT inputs. Fix a set $S=\{x_1,x_2,x_3\}$ of three original variables (unused variables permitted). Let $D$ consist of $t$ acyclic, source-independent, conservatively paid, arbitrary two-input Boolean DEF gates, whose inputs syntactically descend only from $S$. Each gate has one globally fresh output with a declared truth table. Treat all $t$ output names as public to preserve every old downstream reference, including previously private gates. One paid gate provides its exact non-tautological truth-table CNF clauses, at most four, as individually selectable RES premises. **This selector is an additional assumed interface; original /341 does not completely serialize it.** Let the remainder of a valid old refutation consist of $r$ strict binary Resolution nodes using original source clauses and these facets only. Node weight is 1 per distinct new DEF/RES node; original sources are free; no axiom from a decider's answer is allowed.

**Theorem 412.1 (PROVED/EXACT under the preceding interface):** An exact-source, conservative, consumer-repaired proof exists with

$$
\boxed{q_{\mathrm{new}}\le113t+r.}
$$

The construction uses no SAT oracle, does not expand any named Boolean function beyond its three-input truth table, and tolerates arbitrary reconvergence and sharing inside the original $D$.

**Corollary using the existing /411 four-gate catalog:** Replacing the five-gate normal form by the independently documented at-most-four-gate circuit for every three-input truth table gives

$$
\boxed{q_{\mathrm{new}}\le96t+r.}
$$

The $113t+r$ witness compiler is explicitly implemented and independently checked; $96t+r$ is a symbolic corollary of the previously established four-gate theorem, not a separately executed 4-gate compiler.

## Proof: contextual propagation instead of full-variable branching

For each old output function $f$, use Shannon's identity

$$
f=f_0\oplus\bigl(x_1\wedge(f_0\oplus f_1)\bigr),
\qquad f_b=f(b,x_2,x_3),
$$

with two arbitrary binary cofactor gates, two XOR gates, and one AND gate, all charged. This gives $G=5t$ fresh, legal DEF gates; old output names are retained as the final new gate outputs. Each valuation $a\in\{0,1\}^3$ extends uniquely to the new circuit.

For a gate $v$ with output value $v(a)$, let $L_v(a)$ be its true signed output literal and define the original-input blocker

$$
B_a=\bigvee_{i=1}^3 \neg(x_i=a_i).
$$

**Context lemma.** Using only its own defining CNF facet and previously established gate-context clauses, one can derive a clause

$$
P_{v,a}\subseteq B_a\lor L_v(a)
$$

containing $L_v(a)$, with **at most two strict RES inferences for this gate and this $a$**. Take the defining facet indexed by the actual values of the two input ports. If an input is original, its negated true literal is already in $B_a$ and stays. If an input is an earlier gate, resolve its negative true literal against the previously derived $P_{u,a}$. Duplicate input ports need at most one pivot. By induction the result is a subclause of $B_a\lor L_v(a)$. It cannot omit $L_v(a)$: that would produce a clause contained in $B_a$ entailed by a conservative definition bank, contradicting the uniquely extending valuation $a$. No fabricated assumption unit is ever used as a premise. Across all eight assignments and all $G$ replacement gates this costs at most $16G=80t$ RES nodes, with sharing permitted.

Now take any non-tautological old defining facet $C$, which contains at most three named input/output literals and remains true for every original assignment after rebuilding. Fix every **original-variable** literal of $C$ to false. For each completion $a$ of these fixed values, some *gate-output* literal $L$ in $C$ must be true. Select the already derived $P_{v,a}\subseteq B_a\lor L\subseteq B_a\lor C$. Pair branches on the remaining free original variables, resolving their opposite blocker literals if both survive, or inheriting the stronger clause if one disappears. This costs at most $2^3-1=7$ strict RES inferences and ends at a clause $C'\subseteq C$, because all blocker literals corresponding to fixed original inputs are already literals of $C$. Tautological old facets are dispensable and never asserted as free premises.

There are at most $4t$ non-tautological original facets, so the total facet-recovery overhead is at most $7(4t)=28t$. Replay each old downstream RES step with the stronger clauses; if both pivots survive, resolve, otherwise inherit the parent missing its pivot. This consumes at most $r$ RES nodes and an old empty clause remains empty. Therefore

$$
5t+80t+28t+r=113t+r.
$$

Using the four-gate catalog gives $4t+16(4t)+28t+r=96t+r$. This is an **upper bound** on a restricted witness translator. It is neither a bound on unrestricted R_mix341 proof minima nor a SAT-computation lower bound.

## Verification, failure analysis, physical costs

A deterministic Python producer with seed 412 compiled **63 pseudorandom circuits** at $t=1,2,3,5,8,12,16$ (nine per size), plus one fixed five-gate high-support/XOR-cancellation/reconvergence network. It explicitly stored the entire strict Resolution DAG, checked semantic preservation on all eight source assignments, checked every derived clause and every old facet/subclause, and verified the bound. Producer **385,289 assertions; PASS**. Largest observed total cost **1036** at $t=16$ versus the certified bound $113t=1808$. Structured test: 25 new DEF + 286 RES = **311** against a 565 bound. Independent JavaScript checker reconstructed every paid gate facet, premise/pivot, resolvent, topological order, output value, root subclause and all eight complete assignments: **5,961 assertions; PASS**, plus four malformed source and five corrupted proof rejections. Original source $(x_1)$ had four models over three original variables, and $(x_1)\wedge(\neg x_1)$ had zero.

Complete native source and raw proof-stream hashes are retained in the local reproducibility archive. The 64-fixture machine-readable raw file's SHA-256 is **d401f3f4cfd8dfb365141856a3314cd25828d74b5beb4fce8a85a4d0513646d2**. Measured **container-host**, not abstract TM, producer elapsed 0.96 s and peak RSS 97,560 KiB; independent Node checker elapsed 0.04 s, peak RSS 30,192 KiB. Count reads, parsing, policy selection, all eight truth-table passes, gate/row acquisition, pivot lookup, failed branches, serialization, checking and all-phase memory separately from $q$. Each explicit line has polynomial bounded signed indices and width $\le O(t+N)$ in this *flat readable* model; a fully buffered implementation is polynomial in complete explicit source bits $N$ and old proof bits $E$, with a conservative $O((N+E+2)^4)$ bit-time and $O((N+E+2)^3)$ full-buffer peak-bit allowance, **not** an FLMV exponent. Uncharged arbitrary-length LOCAL circuit payloads are outside this theorem.

## Native grammar, B3, and external hard-family firewall

Original /341 explicitly permits RES, original-support-at-most-three AND3, binary GF(2) row addition, unary locally checked LOCAL-CONVERT, and fresh paid two-input DEF. It does **not** settle standalone DEF-clause selector byte syntax, whether a paid XOR DEF exports a typed GF(2) row, nor whether arbitrary LOCAL circuit interiors expose reusable wires. Our theorem **neither adds nor resolves those rules** and does not assert mixed-rule consumer replay. It supplies a tighter conditional fragment theorem and an executable typed witness.

Haken (1985) gives $2^{\Omega(h)}$ ordinary shared-DAG Resolution refutation size for standard unary $\mathrm{PHP}_{h+1}^{h}$, with $h(h+1)$ variables, $(h+1)+h\binom{h+1}{2}$ source clauses, and $\Theta(h^3\log h)$ signed-index bits. Cook (1976) has polynomial Extended Resolution proofs for the pigeonhole principle. Raz-Tzameret's linear-equation proofs use a different system. The known XOR shortcut on Tseitin persists in R_mix341. None of these results supplies an all-algorithm SAT lower bound.

The **noncircular same-fixed-R B3** implication $\mathrm{SAT}\in P\Rightarrow\overline W_{R_{\mathrm{mix341}}}(N)\in N^{O(1)}$ is **OPEN**. This conditional translation from one *existing old proof* to another proof does **not** construct an old proof from a polynomial-time decider or certify the decider's correctness. No rejecting trace or unbounded circuit semantic-equality oracle was charged as a legal source.

**Next precise gap:** Freeze and verify the native DEF-facet, LOCAL exported-wire, AND3 and XOR typed ports; adapt the context proof to legal mixed-rule consumers without assuming arbitrary external row/facet assertions, or exhibit an exact legal native counterexample. In parallel, address B3 by a new independent argument. P versus NP remains OPEN.