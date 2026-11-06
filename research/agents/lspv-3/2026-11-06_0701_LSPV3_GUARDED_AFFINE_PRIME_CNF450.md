# LSPV-3/450: exact guarded-parity prime-CNF cost, compact extension escape, and shared-branch reconvergence

**2026-11-06 07:01 PST | Route B / LSPV-3 | PROVED/RESTRICTED plus COMPUTATIONAL controls.** P versus NP OPEN.

## Initial hypothesis, 4 falsifiers, revision
Attempt to extend the already proved pure-Resolution (/448) and pure-GF(2) (/449) assumption-discharge constructions across native AND3/LOCAL/XOR by exporting a contextual wide parity row as unconditional CNF over original variables. Falsifiers: (F1) exponential original-variable clause output, (F2) legal compact private-DEF/CNF escape, (F3) algebraic reconvergence of both guards without clause expansion, (F4) duplication of earlier projects. The first three all hold. The fourth holds partly: LSPV-3/387 already established guarded affine nonclosure and an AND-gate model, and /414 already furnished a native unchanged-port typing counterexample. Those are not claimed new. The incremental contribution here is the **exact original-variable prime-implicate count**, matching linear private-XOR projection and exact complementary-branch reconvergence.

## Theorem 450.1 (PROVED/RESTRICTED): exact original-variable clause-only size
Let $k\ge1$, let $x,y_1,\ldots,y_k$ be pairwise distinct original variables, and $b,c\in\mathbb F_2$. Put $P(y)=\bigoplus_i y_i$ and $H_{k,b,c}=(x\ne b)\lor(P(y)=c)$. Every non-tautological proper clause implied by $H$ contains **all $k+1$ original variables** and excludes exactly one wrong-parity assignment with $x=b$. There are $2^{k-1}$ such assignments. Thus every CNF using only original coordinates and equivalent to $H$ contains all those full-width clauses. Its unique irredundant proper CNF contains exactly

$$
\boxed{2^{k-1}\text{ clauses, width }k+1,\quad(k+1)2^{k-1}\text{ literal occurrences}.}
$$

For $k\ge3$ no direct proper 3-CNF over these original variables is equivalent to $H$.

**Proof:** Every falsifying point has $x=b,P(y)\ne c$. Flipping $x$ makes the guard true; flipping any single $y_i$ corrects parity. If a proper entailed clause falsified at this point omitted any original coordinate, it would also falsify the satisfying Hamming neighbor, a contradiction. Therefore it includes all $k+1$ coordinates, and excludes a unique falsifying point. Each such point requires its unique clause. Omitting that clause admits the point. QED. Explicit original-variable clause-only bit cost is $\Omega(k2^k\log(k+2))$. This is **NOT** an all-rule mixed refutation lower bound.

## Theorem 450.2 (PROVED/RESTRICTED): polynomial conservative 3-CNF escape
Introduce globally fresh $z_2,\ldots,z_k$ enforcing $z_2=y_1\oplus y_2$ and $z_i=z_{i-1}\oplus y_i$ for $i\ge3$. Encode each XOR2 gate with its four precise three-literal defining clauses. Add the final two-literal guarded clause $(x\ne b)\lor(z_k=c)$; for $k=1$ use the direct two-literal guard. Then the existential projection $\exists z\,G_{k,b,c}(x,y,z)$ equals $H_{k,b,c}$ exactly. The encoding uses **$k-1$ conservative gates, $4(k-1)+1$ clauses, $12(k-1)+2$ literal occurrences and at most $2k$ variable identifiers**, all clauses width at most 3. A unique assignment of private variables satisfies the defining facets for each original valuation; the final clause rejects precisely the forbidden valuations. This follows by induction on the XOR chain.

**Proof-system firewall:** The construction is an encoding/projection, not a certified historical R_mix341 proofwise translation. Although the historical semantic declaration permits unit-paid fresh two-input Boolean DEF, its precise owner-facet and exported/private port byte interface remains unauthenticated; generated clauses cannot be promoted to free axioms. Conversely, this compact candidate is a mandatory shortcut, so the exponential unextended CNF cannot establish full-mixed hardness.

## Theorem 450.3 (PROVED/RESTRICTED): shared two-arm reconvergence
For any $c_0,c_1\in\mathbb F_2$,
$$
\boxed{H_{k,0,c_0}\land H_{k,1,c_1}\equiv
P(y)\oplus(c_0\oplus c_1)x=c_0.}
$$
At $x=0$ the first guard forces $P=c_0$; at $x=1$ the second guard forces $P=c_1$. The displayed single equation matches both cases. This is a **semantic equivalence**, not permission for a free case-split, discharge, or unrestricted conversion. Both contexts are AND obligations; shared legal nodes cost once. It shows that imposing per-branch canonical-CNF output as a necessary intermediate is invalid in a calculus allowing compact reconvergence.

## Established hard family and original-source control
For suitable growing cubic odd-charge expander Tseitin graphs of $h$ vertices and $3h/2$ edge variables, use four wrong-parity signed proper ternary clauses per vertex, $4h$ total, $\Theta(h\log h)$ signed-index bits. Urquhart (1987) and Ben-Sasson–Wigderson (2001) establish exponential **ordinary DAG Resolution** hardness for the appropriate family, NOT full R_mix341 or all SAT algorithms. Known original-source AND3/GF(2) refutations cost $4h-1$ nodes on connected simple bridgeless graphs: a legal shortcut to retain. Haken PHP ordinary Resolution vs Cook ER is a second mandatory shortcut control. Braun bit-PHP begins at width $2\ell$; an equisatisfiable strict-3 encoding alone does not transfer its specified lower bound.

The finite source reproducer instantiates the **published cubic Tseitin encoding on K4**, six edge variables, sixteen actual strict three-literal clauses. Original signed DIMACS SHA-256: ea08104837e167b9ebd06d8f50442d828e3ba4d81f79dff8c14a09ba30050096. Exhaustive source evaluation gives odd charge 0/64 models and even charge 8/64. At its vertex row $x\oplus y_1\oplus y_2=1$, the four actual signed source clauses partition into two guarded clauses for $x=0,P=1$ and two for $x=1,P=0$, reconverging to the original parity. This control certifies SAT/UNSAT and source provenance, not finite proof-size hardness or historical accepted-byte certificates.

## Independent computation and resources
The Python producer and independently written Node replay each checked 28 relations, all $k=1,\ldots,7$ and $(b,c)\in\mathbb F_2^2$, including enumeration of **39,320 candidate nonempty proper clauses**, identification of **508 essential blocker occurrences**, 28 exact compact XOR-chain 3-CNF projections and **2,032** reconvergence assignments. Full independent Node verification passed **7,902 assertions** and rejected **8/8 hostile corruptions**. A separately self-contained compact regression passed **5,223 assertions**, 8/8 negative controls. Python complete host process about 2.2 s and peak RSS 97,180 KiB; full Node verifier about 0.5 s and peak RSS 51,704 KiB. Full producer, independent verifier, source CNF, raw results, host measurements and SHA256 manifest are in the user-accessible conversation ZIP LSPV3_450_GUARDED_PARITY_RECONVERGENCE_REPRO.zip.

No historical native logical-node optimum was computed. The bit sizes above are **representation costs**, not R_mix341 weighted inference costs. A real compiler must additionally charge all source/index/head reads and writes, discovery/failed searches, constructing and checking private definitions, reference retrieval, proof evidence serialization, caches, retention/recomputation, and all-phase simultaneous peak space. No FLMV same-machine contraction is claimed.

## Corpus and exact limits
Reviewed historical rule definition in research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11), governing five-role handoff (c3889a3e), issue #3, AGENTS.md (19656af1), CODEX.md (754999f5), research skill (b8df83a7), project LSPV-3/387, /414, /448–449 and LSPV-1/449, LSPV-2/444, LSPV-4/439, LSPV-5/384. Actual Grok GROKPROOF/2026-11-06_1220_PROGRESS.md (5c4fbf8f) and Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727) were read. Required repositories: konard/p-vs-np/scripts/proof_status.json blob 93b77ed3, blkph0x/p-vs-np-proof-research/METHOD_INDEX.md blob 18d693ea, meelgroup/frat-xor/format.md blob 986a21aa, tanyongkiam/cake_lpr/README.md blob e94f45e9, openai/math/README.md blob cc5b0a03. These are separate proof systems, not authoritative R_mix341 syntax. Primary literature: Urquhart, JACM 1987 DOI 10.1145/7531.8928; Ben-Sasson–Wigderson JACM 2001 DOI 10.1145/375827.375835; Raz–Tzameret APAL 2008 DOI 10.1016/j.apal.2008.04.001. Indexed web searched; no Google-branded direct search available.

Root main.tex blob 6a6a23494708a47ad856865c61131aeccd8e9ea3 returned zero readable bytes: **not edited**. No historical native rule, weight, task, title, schedule, allocation or other agent region changed.

**OPEN:** Authenticate original R_mix341 paid DEF facets/private-export wires and LOCAL byte grammar; give all-rule original-source-authenticated branch normalizer or legal typed obstruction; prove superpolynomial worst-case minimum over ALL mixed legal DAGs and noncircular same-calculus B3. Route A fully charged all-input recursive FLMV transformation remains OPEN. P versus NP OPEN.