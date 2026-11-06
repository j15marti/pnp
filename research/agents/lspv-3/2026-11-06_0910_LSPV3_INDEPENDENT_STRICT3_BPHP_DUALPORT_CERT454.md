# LSPV-3/454: Independent strict-3 bit-PHP full certificate and typed facet audit

**2026-11-06 09:10 PST. Route B. PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.** This report records an independently produced full finite original-source certificate, a differential typed-port check, and a repaired soundness bug. It is *not* a new asymptotic hardness or shortcut theorem.

## Idea -> falsify -> revise

Target: reconstruct the established bit-PHP-to-unary-PHP proof compiler with explicit paid nodes; go beyond a premise-only derivation to the empty clause on an original strict-3-CNF instance. Falsifiers: (F1) a DEF variable overlaps the original source variable range; (F2) a width-$2\ell$ clause is not honestly reconstructed from its private strict-three chain; (F3) wrong RES pivot or DEF facet survives independent replay; (F4) a purported refutation lacks all source ancestors; (F5) the construction already exists in project work.

**F1 and F5 fired.** An initial prototype allocated DEF outputs before all original source-private chain variables, so the outputs were not genuinely fresh relative to the source DIMACS bound. We fixed this before publication by reserving the entire source variable range and emitting every DEF output strictly above it. Independent checker now checks source headers, freshness, gate semantics and all resolution steps. Prior LSPV-1/341 and LSPV-3/346, /439, /440 and /445 already prove and implement the relevant bit-PHP/ER shortcut within declared FACET-A or GATE-LOCAL completions. This report's deliverable is an **independent finite strict-3 full refutation** and differential check of those two *proposed* port models. The general compiler is not claimed novel.

## Established family, source and lower-bound firewall

For $n=2^\ell$ holes and $m=n+1$ pigeons, a pigeon $i$ has address bits $b_{i,t}$. For each $i<j$ and address $a$ the original bit-PHP clause forbids both pigeons choosing $a$:

$$
C_{ij,a}=\bigvee_{t=1}^{\ell}[b_{i,t}\ne a_t]\vee
\bigvee_{t=1}^{\ell}[b_{j,t}\ne a_t].
$$

There are $M=n\binom{m}{2}$ clauses, each width $2\ell$. Braun [1], arXiv:2609.23015v2 (updated 3 November 2026, while the article header retains 22 October), claims every unrestricted DAG-like **Res($\oplus$)** proof requires more than $\exp(n/(32768\ell^2))$ lines for $\ell\ge32$. It **excludes conservative defining extension axioms**. This lower bound is not an ER or R_mix341 lower bound; this run did not replay the linked Lean development.

Split each original width-$k=2\ell$ clause into $k-2$ signed proper 3-clauses with $k-3$ private source-chain variables. Each original clause is reconstructed in $k-3$ native paid RES operations. The strict original source has:

$$
S=(2\ell-2)M,\qquad V=m\ell+(2\ell-3)M.
$$

The strict-3-CNF transformation provides an upper-bound compiler, **not** a lower-bound-preserving simulation from a hard source proof system.

## Exactly what was independently checked

**FACET-A proposed grammar:** one paid conservative two-input signed-AND DEF owner makes its three explicitly indexed defining clauses available to later RES as owner-qualified facets. The facets are not independent free source axioms. Each RES has two earlier premises and a correctly oriented pivot. Every definition output is greater than all $V$ original source variables.

**OWNER-LOCAL proposed grammar:** all direct DEF-facet RES parent references are forbidden. Instead, each facet is reintroduced by one *paid* LOCAL inference from its DEF owner's exact factor. It requires $3D$ extra nodes if every gate's three facets are exported; the checker enforces the alternate parent type. Historical R_mix341 [2] names charged DEF and LOCAL but lacks a fully authenticated native facet or DEF-owner-to-LOCAL accepted-byte contract. Neither proposed grammar should be passed off as authenticated historical syntax.

Shared prefix predicates for addresses introduce $D=m(2n-4)$ paid binary DEF gates. Paid RES steps derive all unary-PHP at-least-one rows and each pair/address collision clause. This deterministic frontend uses exactly

$$
Q_{\rm pre}=(4\ell-3)M+m(2n\ell+n-13)
$$

distinct paid FACET-A nodes for all unary-PHP premises. This agrees with the polynomial bounds previously published in project work, although its row-expansion schedule is not globally optimal. The established Cook extended-resolution unary-PHP proof [3] provides a polynomial suffix under suitable gate-facet semantics. No new general mixed lower-bound transfer is asserted.

**Complete finite strict-3 certificate:** with $\ell=2$ (four holes, five pigeons), the DIMACS original is **80** proper strict-three source clauses in **50** source variables, SHA-256 **13361aa6164d76373ac8d4b4b6935f05257bb99266441f3405cfeecb653da6a6**. The frontend has 20 paid DEF plus 215 paid RES (235). A conventional shared ordinary Resolution unary-PHP tail adds 260 RES nodes. The final proof therefore has **495 paid nodes** and an actual final empty clause. Independent reverse traversal finds **all 80 sources and all 495 paid nodes** in the root ancestry; ideal span is **19**. The explicit OWNER-LOCAL conversion adds 60 charged LOCAL nodes: **555 paid**, **span 20**, same source and empty root. This is an exhibited upper bound in each proposed system, not a certified optimum.

For $\ell=3$ the source has 1,152 clauses/891 variables, with 108 DEF and 2,871 RES, **2,979 FACET-A paid frontend nodes**, **3,303 OWNER-LOCAL paid**. For $\ell=4$ the source has 13,056 clauses/10,948 variables, with 476 DEF and 30,039 RES, **30,515 FACET-A paid frontend nodes**. Those two tests derive **unary PHP premises only** and are *not* full refutations.

A separate Node.js checker, written without producer imports, independently reconstructs every original source clause and signed gate relation; replays every oriented inference and root ancestor, validates all unary rows and collisions; checks that the complete five-pigeon/four-hole bit assignment space is UNSAT; exhausts small chain-clause semantics; rejects five corrupt traces and five malformed DIMACS variants for the $\ell=2,3$ tests. The $\ell=4$ large case was checked without hostile mutations. Full producer, local-port converter, independent checker, exact source DIMACS, complete typed raw traces, timed resource logs and SHA-256 manifest are in the dated run reproducibility archive, rather than claimed as GitHub-hosted full raw evidence.

**Measured Linux-host resource controls**, producer wall/max RSS: $\ell=2$ 0.80 sec / 97,164 KiB, $\ell=3$ 0.99 sec / 100,000 KiB, $\ell=4$ 1.56 sec / 133,780 KiB. Separate checker wall/max RSS: 0.05 sec / 36,596 KiB, 0.14 sec / 47,384 KiB, 0.40 sec / 106,464 KiB. Raw FACET-A JSON trace sizes: 51,804; 364,964; 4,096,647 bytes. These are separate observed process runs, not a measured combined peak, proof-search cost, or a same-machine FLMV bound. All-phase source read, parsing, output, references, storage, cache and recomputation remain separate from ideal charged work.

## Exact status and corpus reconciliation

Original /341 specification blob c87acd11, /452 semantic universal projection blob adaa0d3 and the earlier /453 induced-width note; LSPV-1/341, /449, /451; LSPV-3/346, /439, /440, /445; LSPV-5 REFEREE386; original five-role handoff; current issue #3; AGENTS.md and CODEX.md and research skill; GROKPROOF/2026-11-06_1220_PROGRESS.md SHA 5c4fbf8; Claude TPORT-0002 SHA 1f9fc72 and current user-approved working MathJax/GitHub Markdown format. Prior work establishes the asymptotic ER shortcut already. All claims here remain within explicitly *proposed* FACET-A/OWNER-LOCAL systems.

External checked corpus: konard/p-vs-np/scripts/proof_status.json SHA 93b77ed; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md SHA 18d693e and resolution_width_lab/PHP_WIDTH_REPORT.md SHA f650bfe; meelgroup/frat-xor/format.md SHA 986a21aa and cake_xlrup/README.md SHA c71de80. Those are other proof grammars, not authority for historical native R_mix341 port syntax. Indexed primary literature and authenticated GitHub searches were used; Google-branded standalone search and original historical accepted-byte checker were unavailable. Root main.tex remained unedited because no complete safe-content retrieval was available. Five task IDs, schedules, weights, 2 Route A / 3 Route B and permissions unchanged.

**Open:** historical accepted-byte owner/facet and DEF-to-LOCAL interface, polynomial full all-rule source-normalization/backtranslation, superpolynomial worst-case $\overline W_{R_{\rm mix341}}$, noncircular same-calculus B3 and P versus NP.

**References:** [1] Braun, arXiv:2609.23015v2, 2026; [2] LSPV-2/341, 2026-11-02; [3] Cook, *A Short Proof of the Pigeon Hole Principle Using Extended Resolution*, SIGACT News 8(4), 1976; [4] Grosof–Zhang–Heule, *Towards the Shortest DRAT Proof of the Pigeonhole Principle*, arXiv:2207.11284, 2022.
