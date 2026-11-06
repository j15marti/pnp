# LSPV-3/447: signed-alias FACET4 normalization and tautology-pruning firewall

**November 6, 2026, 05:37 PST. Route B. Status: PROVED/EXACT in a separately declared grammar, COMPUTATIONAL finite controls, OPEN for historical R_mix341 and B3.**

## Hypothesis and falsifiers

Hypothesis: the prior /446 FACET-A to FACET4 given-proof signed-AND2 translation extends to identical or complementary input literals without additional Resolution inferences, if facets are position-qualified and tautological facets remain addressable. Falsifiers: (1) an alias whose conventional facet has no native counterpart; (2) an incorrectly oriented pivot; (3) removal of a tautological owner facet used downstream; (4) loss of original-source provenance or shared ancestry. We proved the positive statement under its declared grammar, and exhibited a typed obstruction for the *different* tautology-pruning grammar.

## Exact signed-input normalization theorem

Fix one given source-authenticated, acyclic, shared FACET-A proof DAG with $D$ paid conservative globally fresh signed-AND2 definitions $z=a\land b$, $R$ paid oriented binary Resolution nodes, and assumption-respecting references. The conventional facets are

$$
C_a=(\neg z\lor a),\qquad C_b=(\neg z\lor b),\qquad C_{ab}=(z\lor\neg a\lor\neg b).
$$

The FACET4 owner instead has the four *position-qualified* forbidden rows

$$
T_{00}=a\lor b\lor\neg z,\quad
T_{01}=a\lor\neg b\lor\neg z,\quad
T_{10}=\neg a\lor b\lor\neg z,\quad
T_{11}=\neg a\lor\neg b\lor z.
$$

Repeated literals may canonicalize, but syntactically tautological owner facets remain addressable. Let $D_{\ne}$ count definitions whose two signed inputs have *different underlying variables*. For distinct inputs, RES on $b$ between $T_{00},T_{01}$ gives $C_a$, RES on $a$ between $T_{00},T_{10}$ gives $C_b$, and $C_{ab}=T_{11}$. For $a=b$, both $C_a,C_b$ are $T_{00}$, while $C_{ab}=T_{11}$. For $a=\neg b$, $C_a=T_{01}$, $C_b=T_{10}$ and $C_{ab}=T_{11}$ (a tautology). Hence the latter two cases require no extra RES. Replaying original inference nodes in topological order preserves all signed clauses, source references, scopes, reconvergence, and the final empty clause.

With fixed declared owner cost $w_D$ and RES cost $w_R$, the *emitted* proof has cost at most

$$
\boxed{D w_D + (R+2D_{\ne})w_R.}
$$

This is an upper bound; nodes absent from the final dependency union do not count toward the actual minimum. From original evidence length $B$, full compact renumbering uses $O(B+D\log(B+D+2))$ bits under standard constant-arity record encoding. Construction, parsing, checking, physical reference retention/recomputation and peak simultaneous memory remain separate costs. No historical rule weights are changed.

## Exact obstruction for a DIFFERENT tautology-pruning grammar

For the conservative gate $z=x\land\neg x$, $T_{00}$ and $T_{11}=(z\lor x\lor\neg x)$ are tautologies. A parser which *deletes* tautological facets retains only $T_{01}=(x\lor\neg z)$ and $T_{10}=(\neg x\lor\neg z)$. For an original formula not mentioning the globally fresh $z$, neither original clauses nor retained facets have any positive $z$. Oriented Resolution cannot introduce a literal polarity absent from all its premises. Thus a given FACET-A derivation using $C_{ab}=T_{11}$ to derive a positive-$z$ clause cannot be translated *clause by clause with only RES* in this PRUNE4 grammar. A different refutation may of course be shorter. This is a typed given-proof translation obstruction, **not** a separation of proof minima and **not** an authenticated historical R_mix341 counterexample.

## Family / theorem / encoding ledger

| Family | Exact encoding and parameter | Certified restricted theorem | Shortcuts and transfer gap |
| --- | --- | --- | --- |
| Random $F(n,3,8n)$, Chvátal–Szemerédi (1988), Pang arXiv:2610.00837v2 (Oct 24, 2026), Theorems 1.1, 7.2(a) | $n$ variables; $8n$ independent uniformly sampled proper signed ternary clauses **with replacement**, out of $8\binom n3$ possibilities. No 3-CNF conversion. | Exponential ordinary DAG Resolution size (classical), more strongly a.a.s. $\exp(\Omega_{p,r}(n))$ DAG size in $\mathrm{Res}(\mathrm{PC}_r/\mathbb{F}_p)$ for each fixed prime $p$ and degree $r\ge1$ (recent preprint, not independently proved here). | Paid auxiliary definitions, GF(2), AND3 and LOCAL-CONVERT are not all covered by this lower-bound calculus. Individual finite instances have not thereby been proof-size certified. |
| Cubic odd Tseitin, Urquhart 1987 | Cubic expander with $h$ vertices, $3h/2$ edge bits, four ternary parity clauses per vertex, $4h$ source clauses. | $\exp(\Omega(h))$ ordinary Resolution on appropriate expander families. | Previous project /341 has $O(h)$ semantic mixed AND3/GF(2) proof, so no full-mixed lower bound follows. The finite $K_4$ below is only a validity control. |
| Bit-PHP Braun arXiv:2609.23015, Pang arXiv:2610.00837v2 Theorem 7.2(e) | $N=2^\ell$ holes, $N+1$ pigeons, $(N+1)\ell$ bits, $N\binom{N+1}{2}$ clauses width $2\ell$. Standard strict-3 private chains require $N\binom{N+1}{2}(2\ell-2)$ clauses. | Braun: $>\exp(N/(32768\ell^2))$ DAG Res($\oplus_2$) for $\ell\ge32$. Pang: $\exp(\Omega_{p,r}(N))$ DAG Res(PC$_r/\mathbb F_p$), fixed $p,r$, in original wider CNF. | Known Extended Resolution / Cook shortcut; earlier /441,/446 paid-facet full proofs are **conditional** on a separately declared interface. Equisatisfiability alone does not preserve lower bounds in strict-3 form. |

Pang's exact source model and syntactic inference rules were checked in the original 24-page PDF, including the degree-size inequality and its substitution argument for bit-PHP. The resulting fixed-degree proof lower bounds do not cover freely defined Boolean extension variables.

## Reproducible finite test and resource audit

The **original source** is odd-charge $K_4$ Tseitin strict-3 CNF: six edge variables and 16 signed proper ternary clauses generated by forbidding wrong parity assignments at four vertices with charge vector $(1,0,0,0)$. SHA256 of exact ASCII DIMACS: **ea08104837e167b9ebd06d8f50442d828e3ba4d81f79dff8c14a09ba30050096**. All 64 assignments independently fail. A deterministic Resolution saturation produces unit consequences, and twelve complete source-authenticated proof DAGs use one paid signed gate each, with an owner facet in the final contradiction ancestry. Two same-sign aliases, two opposite-sign aliases and eight distinct-variable gates are represented, for twelve complete source-authenticated cases; the compact truth-table regression independently covers all sixteen possible signed-literal pairs. FACET-A paid work is 34, 35 or 38 nodes depending on case. FACET4 requires respectively zero, zero or two *emitted* extra RES nodes. Unused emitted RES nodes are not charged to the final root ancestry.

An independently authored Node checker reconstructed the original K4 source, checked its SHA, exhaustively evaluated its assignments, validated every oriented RES inference, gate truth table and final contradiction, and passed **6,557 assertions**. Seven deliberately corrupted serialized packets were all rejected by seven **fresh full-checker invocations**, including forged source, gate, pivot, root, owner, case dependency and source reference. These are validity checks, not minimum proof-size certifications or a historical native-byte checker test.

Complete producer process: 1.37 s wall time, 97,424 KiB peak RSS; independent check: 0.15 s, 30,648 KiB; hostile test controller: 1.27 s, 99,204 KiB (child processes not included in controller RSS as simultaneous live memory). Raw typed proofs and code are in the separate immutable reproducibility ZIP. No same-machine FLMV implication is claimed.

## Continuity and limitations

Inspected governing November 2 five-role handoff, current issue #3 through LSPV-1/447 and LSPV-5/REFEREE385, AGENTS.md, CODEX.md, repository skill, preceding LSPV-3/445 and /446, actual GROKPROOF/2026-11-06_0515_PROGRESS.md and Claude TPORT source. Both newly requested external repositories were read (konard/p-vs-np README blob 0e0ec77..., blkph0x/p-vs-np-proof-research README blob f397a77...) and relevant FRAT-XOR, CakeML LPR, short-proof and openai/math READMEs were inspected. Original theorem statements in Pang's PDF were verified; Google-branded direct search was unavailable. None provided the accepted-byte historical R_mix341 owner selectors/LOCAL-CONVERT input contract. Root main.tex returned a SHA but zero readable bytes; it was **not** modified. All existing five-role assignments (2 Route A / 3 Route B), schedules, states and historical weights remain unchanged.

**Actual advance:** sharp signed-degenerate gate completion and a typed tautology-pruning translation obstruction, each checked against complete strict-3 source-authenticated refutations. **OPEN:** historical native grammar, all-rule mixed normalization and superpolynomial $\overline W_R$, noncircular B3, and P versus NP.
