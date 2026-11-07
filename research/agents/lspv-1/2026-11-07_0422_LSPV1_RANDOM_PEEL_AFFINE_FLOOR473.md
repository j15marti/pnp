# LSPV-1/473 | A linear source-support firewall for affine shortcuts on Resolution-hard random 3-CNF

**2026-11-07 04:22 PST, America/Los_Angeles | Route B | PROVED/RESTRICTED symbolic, COMPUTATIONAL finite controls.** Relevant tracker IDs: [P2-B14] (new evidence), [P2-B1] (OPEN), [P2-B2] (OPEN), [P2-D1] (OPEN), [P2-C3] (OPEN), [P2-D2] (fixed global minimum). P versus NP OPEN.

## IDEA and predeclared falsifiers

**Hypothesis:** A fixed-linear-density, published random 3-CNF family already known exponentially hard for ordinary shared-DAG Resolution has a *linear* floor on the number of original source clauses needed to derive ANY unconditional nontrivial affine equality on original variables, not merely the four-source floor of LSPV-1/472. The mechanism is the absence of small subhypergraphs with all variable degrees at least two. This is a **source-support** statement, not a superpolynomial paid-work theorem.

Precise falsifiers:
1. A peelable signed proper 3-CNF has a satisfiable model set whose affine hull is not the entire cube.
2. With positive limiting probability, a random $m=8n$ proper signed 3-CNF contains a 2-core on $o(n)$ clauses, contradicting the claimed union bound.
3. A source-authenticated, conservative derivation produces a nontrivial *original-variable* affine equality despite a satisfiable full-affine-hull ancestor source subset.
4. The claimed model transfer silently assumes historical LOCAL-CONVERT is unary/binary, auxiliary wires are charged, or branch assumptions are global.

The first three are ruled out within the stated mathematical model. Falsifier 4 remains an OPEN native-grammar question, so no historical mixed minimum bound is asserted.

## SEARCH, original source, and precedence

Read both live complete trackers, governing Nov. 2 five-role handoff, issue #3, AGENTS.md, CODEX.md, repo-scoped pnp-research skill, LSPV-1/472 exact prior four-clause theorem, LSPV-1/471 legal backward shortcut, LSPV-3/471 entire binary mixed Horn control, LSPV-5/408 affine-branch retraction, actual GROKPROOF/2026-11-07_1119_PROGRESS.md and research/agents/claude/world-ledger/README.md. The earlier source-local **four-clause** bound is reused, not claimed as new; the linear source-support improvement and induction are this run's scoped result. Prior project reports on random formulas and affine hulls were searched for duplicate formulations; no exact full-affine-span peeling lemma was located, which does not establish publication novelty.

Primary reference: Chvátal–Szemerédi, *Many Hard Examples for Resolution*, J. ACM 35(4):759-768 (1988), DOI 10.1145/48014.48016. The published random-proper-3CNF model at $m=cn$ with fixed $c/8>0.7$ yields UNSAT and $2^{\Omega(n)}$ ordinary Resolution hardness with high probability. We choose $c=8$. Also reviewed Ben-Sasson–Wigderson, *Short Proofs Are Narrow* (JACM 2001), and 2025 CCC random-CNF proof-complexity article. Exact bound here is derived independently, not attributed to those authors.

Actual third-party pinned file reads: konard/p-vs-np scripts/proof_status.json blob 93b77ed3 and proofs/complexity/README.md blob 7ee9a11e; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea and REVIEW_ADDENDUM.md blob 6a7cc2f8; meelgroup/frat-xor format.md blob 986a21aa; tanyongkiam/cake_lpr README.md blob e94f45e9; openai/math README.md blob cc5b0a03; anthropics/formal-math README.md blob 1df53bfc. They do **not** authenticate historical R_mix341 byte syntax or give its lower bounds. Public internet search was used; Google-branded search was not separately available. The existing historical AN(D3)/GF(2) source shortcut on odd Tseitin remains mandatory as an upper control.

## Family ledger

For $n$ original Boolean variables, sample $m=8n$ signed proper three-literal clauses, each using three distinct uniformly chosen variable names and independently uniform signs. The canonical distinct-clause model samples without replacement from $8\binom n3$ signed clauses. Its binary literal-index source has length $N=\Theta(n\log n)$; an independent-sampling-with-replacement model differs with probability $O(1/n)$ by a collision coupling.

**KNOWN THEOREM:** At this density, with high probability the formula is UNSAT and every ordinary shared-DAG Resolution refutation has $2^{\Omega(n)}$ length (Chvátal–Szemerédi 1988; exact ordinary Resolution model). **New PROVED/RESTRICTED:** with high probability every nonempty subformula of at most $\delta n$ original clauses has a satisfiable model set of *full affine span*. This is a property of its original ternary incidence support hypergraph, independent of literal signs. **Known methods and controls:** Resolution branching and shared proof DAGs, paid extensions, GF(2), and LOCAL-CONVERT remain possible globally, including derived narrow clauses and nonlocal algebra. Odd-Tseitin gives a polynomial mixed-algebraic shortcut on a different family. **Remaining transfer:** no superpolynomial whole-$R_{\mathrm{mix341}}$ invariant, authentic native grammar, or noncircular B3.

## Theorem 473.1: peeling implies full affine hull

Call a proper signed three-CNF $H$ *peelable* if repeatedly deleting a clause containing a variable of occurrence degree exactly one eventually deletes every clause. (Degrees refer to currently remaining clauses, ignoring signs.)

**Claim:** Every peelable $H(X)$ is SAT, and its satisfying assignments have affine hull $\mathbb F_2^{|X|}$. Equivalently, $H$ implies no nonconstant affine GF(2) equation $a\cdot X=b$ with $a\ne0$.

**Proof by induction on clauses.** For $H=\top$, every Boolean assignment is a model, so the affine hull is full. Otherwise select an initial leaf variable $v$, occurring in exactly one clause $C=(\ell_v\vee\ell_u\vee\ell_w)$, and let $H'=H\setminus\{C\}$. Then $v$ occurs nowhere in $H'$, and the remaining hypergraph is peelable. By induction $H'$ is satisfiable and has full affine span. Every $H'$ model extends to an $H$ model by selecting $v$ to satisfy $C$. Thus $H$ is SAT and its projection onto $X\setminus\{v\}$ equals the projection of $H'$.

Suppose an affine equation $a\cdot X=b$ is implied by $H$. If $a_v=0$, it is implied by $H'$ after projection, contradicting the full affine hull of $H'$ (the nonzero coefficient vector remains nonzero). If $a_v=1$, the full affine hull of $H'$ guarantees a model satisfying $\ell_u$ (otherwise $H'$ implies the nontrivial unit affine row fixing $u$). Under that model, BOTH assignments $v=0$ and $v=1$ satisfy $C$ and $H'$. The alleged equation takes opposite values, contradiction. Proper width three supplies $u\ne v$ and $w\ne v$. QED.

## Theorem 473.2: random sources have no small 2-core

For any fixed $c>0$ and $m=\lceil cn\rceil$, consider independent uniform random unsigned triples $T_1,\ldots,T_m$; signed clauses are obtained by independently randomizing their polarities. Let

$$
C_c=e^{5/2}(3/2)^{3/2}(c+1),\qquad
\delta_c=\min\{1/3,(10C_c)^{-2}\}>0.
$$

**Claim:** With probability $1-o(1)$, every set of at most $\lfloor\delta_c n\rfloor$ clauses is peelable.

**Proof.** A nonempty residual 2-core on $s$ clauses and $v$ occurring original variables has each variable of degree at least two, hence $3s\ge2v$, or $v\le3s/2$. For each $s$-element choice among the $m$ sampled clauses and $v$-element variable set, the probability all selected supports lie inside the variable set is exactly $\{\binom v3/\binom n3\}^s\le(v/n)^{3s}$. By union bound the probability of some such residual core with $1\le s\le\delta_cn$ is at most

$$
\sum_{s=1}^{\lfloor\delta_cn\rfloor}
\binom ms\sum_{v=1}^{\lfloor3s/2\rfloor}
\binom nv\left(\frac vn\right)^{3s}.
$$

Use $\binom ms\le(e(c+1)n/s)^s$, $\binom nv\le(en/v)^v$, $e^v\le e^{3s/2}$, and $v/n\le3s/(2n)\le1/2$. Each inner summand is at most

$$
\left[C_c\sqrt{\frac sn}\right]^s.
$$

There are at most $3s/2$ inner summands. Therefore the union bound is at most

$$
\sum_{s=1}^{\lfloor\delta_cn\rfloor}
\frac{3s}{2}\left(C_c\sqrt{\frac sn}\right)^s.
$$

For $s\le\sqrt n$, the base is at most $C_cn^{-1/4}$; its sum is $O_c(n^{-1/4})$. For $\sqrt n<s\le\delta_cn$, the base is at most $1/10$, giving $e^{-\Omega(\sqrt n)}$. Thus the total tends to zero. Sampling **distinct signed clauses without replacement** is coupled to the independent model with error at most $\binom m2/(8\binom n3)=O_c(1/n)$, so the same conclusion holds in the published distinct-source model. QED.

## Corollary 473.3: unconditional source-local affine support floor

Intersect the high-probability events of Theorems 473.1–473.2 and Chvátal–Szemerédi. For a source $F$ in that intersection, **every subset of at most $\delta_8 n$ original clauses is SAT and has full affine hull**, so cannot imply an unconditional nontrivial affine equation on original variables, nor false. If a *sound and original-source-transparent* inference, including a conservative fresh definition and any intermediate legal local clauses, produces such an unconditional original-variable affine row, its provenance must involve **more than $\delta_8 n$ distinct original clauses**.

This counts *support ancestry*, not computational discovery or the number of paid nodes. If, additionally, every paid inference has at most two **explicit** parents, source clauses are distinct free leaves, and there is no hidden multisource primitive, a connected proof ancestry with $s$ original leaves has at least $s-1$ paid binary nodes. Thus within that **separate qualified unit-paid binary model**, any complete refutation has $W_R(F)\ge\lfloor\delta_8n\rfloor$, merely a **linear** lower bound. The fixed historical R_mix341 must NOT be assumed to meet the premises until [P2-D1] is resolved. No lower bound on arbitrary SAT decision time, on the global presence of GF(2) shortcuts, or on B3 is derived. With branch assumptions, an affine row may hold in its context only; cross-branch discharge is not free.

**Key scope firewall:** Affine equations over *fresh* auxiliary wires can follow immediately from paid definitions despite full affine span on original $X$. The theorem only forbids unconditional rows on original variables, or original-variable rows after sound conservative elimination of auxiliaries. Large source provenance can be accumulated in $O(n)$ inferences; this result is not even a superlinear all-mixed work bound.

## ITERATE and independent finite falsifiers

Exact-code V8 controls on signed proper three-CNFs: exhaustive all clause subsets on n=4 with k<=4 (41,449 formulas) and n=5 with k<=3 (85,401 formulas), plus 2,400 reproducible n=6 and 1,800 n=8 deterministic sampled sources and two adversarial controls. Total 131,052 formulas tested, 56,010 peelable, 75,042 not peelable; **every** peelable instance was SAT with full GF(2) affine rank. 112,028 explicit checks passed; one deliberately UNSAT eight-clause triple-packet control and one SAT non-peelable rank-three XOR control; six malformed source controls rejected. The finite checks validate the induction in bounded cases but do not establish the random asymptotic theorem.

Role-owned executable: experiments/arc/lspv1_473_peeling_affine_control.cjs, blob 1478ca396ea439af8fd7b9b34112cfe650ab77ff. It was executed in a V8 isolate after stripping the node shebang and redirecting its final console write; byte-identical source was committed and read back. The authoritative native R_mix341 checker was NOT executed. Raw result: results/raw/arc/2026-11-07_0422_LSPV1_473_PEEL_AFFINE.json.

## Resource ledger and barriers

- **Ideal mathematical work:** Theorem 473.3 counts distinct original-source ancestors. The optional binary-model paid-node implication is $\Omega(n)$, NOT $2^{\Omega(n)}$. The reference ordinary-Resolution hardness bound is a separate published theorem.
- **Evidence bits:** The random original input uses $N=\Theta(n\log n)$ bits. The symbolic union-bound/induction proof is a fixed-size argument; an actual certificate requires its own source IDs, inference records, GF(2) rows, assumptions and explicit serialized bytes.
- **Finite construction, search, checking:** Exhaustive subsets for n=4/5 plus deterministic n=6/8 sampling, complete assignments up to $2^8$, model-span GF(2) elimination and clause-degree peeling. 131,052 test formulas and 112,028 asserted properties; no polynomial-time large-n SAT decision method.
- **Reads/parsing/output/caches:** The tester builds all signed proper clauses and lists of small clause index combinations, scans all finite models and stores a rank basis; source access, temporary combination arrays, cached models, output, and rejected malformed clauses count as implementation work.
- **Physical time/peak space:** No calibrated runtime or simultaneous peak RSS was recorded. This prevents any same-machine FLMV exponent claim. Proof-search, conversion, eventual source-authenticated R_mix341 verification and revision/readback are independent charged phases.
- **Known countercontrols:** Short GF(2) proof of odd Tseitin; non-peelable SAT parity control; early multi-source derived Resolution rows; Extended Resolution may shorten Resolution-hard sources. No argument against any such legal shortcut.

No modification to historical R_mix341 grammar, weights, task roles, titles, enabled states, schedules, route allocation, or main.tex. Complete main.tex was not safely retrieved, so no ownership edit was attempted.

## Status and next load-bearing implication

[P2-B14] is PROVED/RESTRICTED source-support evidence on a **published hard ordinary Resolution family**, supporting but not closing [P2-B1]. [P2-D1] and [P2-C3] must authenticate exact permitted source import, paid local-convert arity, original-variable output typing, auxiliary freshness, branch contexts and reference costs. [P2-B2] remains the noncircular same-fixed-calculus B3 transfer, not supplied here. Known shortcuts must remain available to the ideal global optimizer. **P versus NP OPEN.**

## References

1. Chvátal, V., Szemerédi, E. (1988). Many Hard Examples for Resolution. *J. ACM* 35(4), 759–768. DOI: 10.1145/48014.48016.
2. Ben-Sasson, E., Wigderson, A. (2001). Short Proofs Are Narrow: Resolution Made Simple. *J. ACM* 48(2), 149–169. DOI: 10.1145/375827.375835.
3. Carenini, G. (2026). Random 3-CNF formulas are hard for $k$-DNF resolution up to $k=O(\sqrt{\log n})$. ECCC TR26-158, 30 Aug 2026. Different proof calculus; not a bound for historical mixed R.
