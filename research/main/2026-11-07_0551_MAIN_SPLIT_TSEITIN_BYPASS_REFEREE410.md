# LSPV-5/410 — support-unique split-Tseitin bypass

**2026-11-07 05:51 PST | Route B independent red team | PROVED/EXACT in the declared-semantic `R_mix341`; COMPUTATIONAL finite controls; historical accepted-byte grammar OPEN. P versus NP OPEN.**

Relevant live nodes: `[P2-D1]`, `[P2-D2]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]`, `[P2-B13]`, `[P2-B14]`, `[P2-B15]`, `[P2-B16]`, `[P2-L3-473]`, and new `[P2-L5-410]`. Both `proof1.txt` and `proof2.txt` were read at the start of the run. `proof1.txt` remained blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; the starting `proof2.txt` blob was `a0e3abde262ac494b8994bb193291147c43e7b46`.

## Claim card and preregistered falsifiers

- **Target:** falsify any transfer from absence of source-local repeated ternary supports/direct affine packets to hardness in the full declared mixed calculus.
- **Quantifiers:** for every connected simple bridgeless cubic graph $G=(V,E)$ and every odd charge $\chi$, construct one strict proper 3-CNF $S(F_{G,\chi})$ and prove its exact declared-semantic mixed minimum.
- **Model:** original source clauses are free; each distinct RES, AND3, binary GF(2), LOCAL-CONVERT or conservative two-input DEF inference has the unchanged `/341` unit weight and at most two proof antecedents. The construction below uses only RES, AND3 and GF(2).
- **Resource:** union of distinct paid inference vertices; free optimal legal derivation choice. Separately report span, evidence bits and physical construction/checking.
- **SAME_REALIZATION:** the transformed source, deletion witnesses, reconstructed target clauses and mixed proof all use the same signed variable IDs and source clause records.
- **Weakest material result:** a support-unique strict-3CNF source with a proved linear all-rule mixed refutation is enough to defeat the proposed source-local extrapolation; no P-versus-NP consequence is needed.

Falsifiers stated before search:

1. the two-clause gadget is not projection-equivalent to its target clause;
2. oriented Resolution does not reconstruct the target clause exactly;
3. the transformed odd-charge instance is satisfiable, malformed, or not strict proper 3-CNF;
4. the shortcut requires a conversion on derived clauses forbidden by historical `/341`, in which case it is only conditional.

Falsifiers 1–3 are rejected symbolically and computationally. Search of the actual `/341` report rejects falsifier 4 at the declared-semantic level: AND3 directly accepts two derived conditions on combined support at most three, so LOCAL-CONVERT is unnecessary. Historical serialized accepted bytes remain `[P2-D1]` OPEN.

## Exact family/theorem/encoding/known-method ledger

| Family | Exact encoding and size | Established theorem/model | Strongest applicable method | Remaining transfer |
|---|---|---|---|---|
| Original cubic-expander odd Tseitin $F_{G,\chi}$ | One variable per edge. At every cubic vertex, four proper signed 3-clauses exclude the wrong-parity triples. For $h=|V|$: $3h/2$ variables, $4h$ clauses, $N=\Theta(h\log h)$ indexed bits. | Urquhart (1987) and Ben-Sasson–Wigderson (2001) give exponential ordinary shared-DAG Resolution size on suitable expander sequences. This is proof-size hardness in Resolution, not mixed-calculus or machine hardness. | Historical `/341`: three AND3 nodes per vertex and $h-1$ GF(2) joins, exact declared minimum $4h-1$ on connected simple bridgeless cubic graphs. | None of the Resolution lower bound transfers through the GF(2) shortcut. |
| Split family $S(F_{G,\chi})$ from this run | Replace each target clause $C$ by two strict ternaries with one fresh **source** variable $a_C$. Exactly $11h/2$ source variables, $8h$ clauses and $N'=\Theta(h\log h)$ bits. Every unsigned source support occurs once. | UNSAT and exact declared mixed minimum $8h-1$ are proved below. Finite K4, K3,3, cube and Petersen controls are certificate checks, not asymptotic hardness certificates. | $4h$ oriented RES reconstructions, $3h$ AND3 packet nodes and $h-1$ GF(2) joins. Balanced logical span $3+\lceil\log_2 h\rceil$. | No ordinary-Resolution lower-bound preservation from $F$ to $S(F)$ is proved. Equisatisfiability alone is insufficient. Historical byte acceptance is unauthenticated. |
| Chvátal–Szemerédi random proper 3-CNF | $m=cn$ signed proper width-three clauses, $N=\Theta(n\log n)$. | Exponential ordinary Resolution size with high probability in the published model. `[P2-B13]`–`[P2-B16]` add source-local affine/low-degree restrictions. | Arbitrary RES, later AND3, GF(2), definitions, branches and sharing remain legal. | The split construction is a focused adversarial control, not a statement that random formulas contain these gadgets. Full `[P2-B1]` remains OPEN. |

Certified UNSAT, proof-size hardness and empirical difficulty are distinct throughout. The transformed family is certified UNSAT and has an exact declared mixed minimum. It is **not** certified ordinary-Resolution hard.

## The gadget and exact projection

For a proper target clause on distinct variables

$$
C=(\ell_1\lor\ell_2\lor\ell_3),
$$

introduce a fresh source variable $a_C$ and replace it by

$$
S(C,a_C)=
(\ell_1\lor\ell_2\lor a_C)\land
(\ell_1\lor\ell_3\lor\neg a_C).
$$

Both clauses are strict and proper. Resolving them on $a_C$ yields exactly $C$, without weakening:

$$
\frac{\ell_1\lor\ell_2\lor a_C\qquad
      \ell_1\lor\ell_3\lor\neg a_C}
     {\ell_1\lor\ell_2\lor\ell_3}.
$$

Also $\exists a_C\,S(C,a_C)\equiv C$. If $\ell_1$ is true, either value works. If $\ell_1$ is false, the two residual clauses are $(\ell_2\lor a_C)$ and $(\ell_3\lor\neg a_C)$, which have a common solution exactly unless both $\ell_2$ and $\ell_3$ are false. This proves projection equivalence for every polarity pattern.

Use a different $a_C$ for every target clause. The two supports belonging to $C$ are

$$
\{\operatorname{var}(\ell_1),\operatorname{var}(\ell_2),a_C\},\qquad
\{\operatorname{var}(\ell_1),\operatorname{var}(\ell_3),a_C\}.
$$

They are distinct because $C$ is proper. Supports from different gadgets contain different fresh source variables. Therefore **all $8h$ source supports are pairwise distinct**, even though the $4h$ one-step RES conclusions reconstruct the four-clause affine packet at every vertex.

## Theorem 410.1 — exact declared mixed minimum

Let $G$ be connected, simple, bridgeless and cubic, and let $\chi$ have odd total charge. Then

$$
\boxed{W_{R_{\mathrm{mix341}},\mathrm{declared}}(S(F_{G,\chi}))=8h-1.}
$$

### Upper bound

Resolve each of the $4h$ source pairs once to reconstruct the original Tseitin clauses. At each vertex, use the exact `/341` construction: three binary AND3 nodes conjoin the four reconstructed clauses into the local eight-entry factor and certify its GF(2) row. This costs $3h$. Join the $h$ rows with $h-1$ binary GF(2) additions. Odd total charge produces $0=1$. Thus

$$
W\le4h+3h+(h-1)=8h-1.
$$

The proof dependency graph is acyclic. No branching or assumption discharge occurs, so there is no cross-context leakage. The four source-pair reconstructions and vertex factors are distinct; shared rows are referenced once. A balanced schedule has RES depth 1, AND3 depth 2, and GF(2) depth $\lceil\log_2 h\rceil$.

### Lower bound

Historical `/341` proves every original clause $C$ of $F_{G,\chi}$ indispensable. Fix its deletion witness $x$, which satisfies every other original clause and falsifies $C$.

- If the positive-$a_C$ parent of $S(C,a_C)$ is deleted, extend $x$ with $a_C=0$; the surviving negative-$a_C$ parent is true.
- If the negative-$a_C$ parent is deleted, extend $x$ with $a_C=1$; the surviving positive-$a_C$ parent is true.
- Every other target clause is true under $x$, so projection equivalence supplies a satisfying value for its private source variable.

Hence every one of the $8h$ split source clauses is indispensable. In any sound source-explicit ancestry with unit-positive, at-most-binary-premise derived vertices, all indispensable sources must reach contradiction. The connected-ancestry/source-capacity argument gives at least $8h-1$ paid vertices, including every permitted conservative binary mixed rule and shared/reconvergent DAG. The upper and lower bounds match.

This is an exact theorem in the declared semantic calculus, not a bounded optimizer result. It does not authenticate a missing historical byte parser.

## What the result falsifies—and what it does not

**FALSIFIED/RETIRED as a general lower-bound step:**

> pairwise-distinct unsigned source supports, absence of a direct four-source affine row, or absence of an initial two-source AND3 merge implies hardness in the full declared mixed calculus.

One legal RES layer can materialize all missing affine packets at linear cost. This is the precise indirect `RES -> AND3 -> GF(2)` bypass requested in the LSPV-1/472 and LSPV-3/460 handoffs.

The result does **not** falsify their actual restricted theorems. `[P2-B13]`–`[P2-B16]` concern source-local consequences or peelable random-source subsets; they already excluded later arbitrary RES and algebraic shortcuts. The present family is structured, not a random sample from that distribution.

The implication direction for ordinary Resolution is also deliberately limited. Since every original clause is derivable from its split pair, an original Resolution refutation gives a split-source refutation with $4h$ extra steps. That is an **upper** simulation. No reverse simulation from arbitrary split-source Resolution proofs to original proofs is shown. Therefore Urquhart/Ben-Sasson–Wigderson hardness of $F_{G,\chi}$ is not claimed for $S(F_{G,\chi})$.

## Search, precedence and source authentication

Project files read with exact paths/blobs included:

- `proof1.txt` (`96aefb3d...`) and complete `proof2.txt` starting blob (`a0e3abde...`);
- original `/341`, `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` (`c87acd11...`);
- LSPV-3/460 (`bfd30948...`), LSPV-1/472 report (`8170381e...`) and handoff (`14d76aa...`), LSPV-3/473 report (`f819b5af...`) and handoff (`355c3bfc...`), LSPV-1/475 handoff (`db663b25...`), and LSPV-5/409;
- governing November 2 five-role handoff, `AGENTS.md`, `CODEX.md`, and the research protocol; root `main.tex` again returned blob `68188a24...` with zero readable bytes;
- actual Grok `GROKPROOF/2026-11-07_1220_PROGRESS.md` (`2c450bb3...`) and Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` (`79e4d4e7...`).

Current external repository reads:

- `konard/p-vs-np/proofs/complexity/README.md` (`7ee9a11e...`): a different finite one-tape model, explicitly not a conventional-model equivalence or P-vs-NP solution;
- `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` (`18d693ea...`): restricted method/status ledger; its hidden-XOR entry is evidence about bounded motif discovery, not native `/341`;
- `meelgroup/frat-xor/format.md` (`986a21aa...`): in the distinct XLRUP grammar, `i x` explicitly rejects an XOR that needs resolution between hints until the missing clause is first derived by RUP. This independently authenticates the **sequence shape** RES-then-XOR-conversion in that different checker, not historical `/341` bytes;
- `MassimoLauria/cnfgen/cnfgen/families/tseitin.py` (`4bb5fd19...`), exact public generator implementing graph-edge variables and vertex parity clauses;
- `peitl/short-proof/README.md` (`93d2090d...`), `tanyongkiam/cake_lpr/README.md` (`e94f45e...`), and `openai/math/README.md` (`cc5b0a03...`). None proves the target mixed transfer; build/checker availability is not theorem authority.

Primary literature search checked Urquhart, *Hard examples for resolution*, JACM 34(1), DOI [10.1145/7531.8928](https://doi.org/10.1145/7531.8928), and Ben-Sasson–Wigderson, *Short Proofs Are Narrow*, ECCC TR99-022 / JACM 48(2), DOI [10.1145/375827.375835](https://doi.org/10.1145/375827.375835). Their model is ordinary Resolution. Chvátal–Szemerédi, DOI [10.1145/48014.48016](https://doi.org/10.1145/48014.48016), remains the established random-family source for `[P2-B13]`–`[P2-B16]`. No separate Google-branded search service was available; authenticated GitHub reads and indexed web/primary pages were used. Full issue #3 comment enumeration failed with `Transport closed`; the issue head and cited role files were read directly.

Cross-domain audit: Tseitin rows are parity checks of a binary linear code. The split gadget is an exact existential CNF factorization of one forbidden word, but coding-theoretic expansion or LDPC distance does not survive as proof hardness without a proof-system simulation. Status: **FAILED TRANSFER** for any direct code-distance-to-`R_mix341` work lower bound; the algebraic parity-check interpretation instead predicts the observed GF(2) shortcut.

## Reproducibility, hostile controls and resources

Artifacts:

- producer/checker: `experiments/review/lspv5_410_split_tseitin_bypass.py`;
- independent replay: `experiments/review/verify_lspv5_410_split_tseitin_bypass.mjs`;
- raw ledger: `results/raw/review/2026-11-07_0551_LSPV5_SPLIT_TSEITIN410.json`, SHA-256 `5759846fc91f1b26a8691a551203c92d257e3bb79e729e9c521939dc214a09c6`.

Python: 752 explicit check groups plus exhaustive finite model/deletion loops. Independent Node: **7,297 checks PASS**. Controls reject reversed orientation, wrong pivot, same-polarity pivot, tautological resolvent, repeated literal, false-target extension, reused auxiliary freshness, and all scope promotions. The historical checker was not run.

| graph | $h$ | total variables | source clauses | even-base models | source bytes | exact mixed work | balanced span |
|---|---:|---:|---:|---:|---:|---:|---:|
| K4 | 4 | 22 | 32 | 8 | 342 | 31 | 5 |
| K3,3 | 6 | 33 | 48 | 16 | 516 | 47 | 6 |
| cube | 8 | 44 | 64 | 32 | 708 | 63 | 6 |
| Petersen | 10 | 55 | 80 | 64 | 904 | 79 | 7 |

The Python run recorded 0.634 seconds and 10,368 KiB peak RSS on this host; these are reproducibility measurements, not machine-independent bounds. Logical work is exactly $8h-1$. With dense explicit affine masks, a conservative certificate/output upper bound is $O(h^2\log h)$ bits. Construction, parsing, source/support indexing, all RES checks, eight-row AND3 checks, GF(2) bit operations, output, retrieval, serialization and validation are charged for realizable execution. Search/discovery cost is excluded only from ideal $W_R$ by definition.

## Status and next exact gap

**Actual advance:** an infinite, exact strict-3CNF countercontrol with pairwise-distinct source supports and exact linear declared mixed minimum $8h-1$. This closes the requested indirect-RES bypass test and materially narrows source-local lower-bound proposals.

**Still OPEN:** historical accepted bytes and full `[P2-D1]`; any lower bound that survives all legal rules `[P2-B1]`; all-rule source-preserving normalization `[P2-C3]`; noncircular same-calculus B3 `[P2-B2]`; and P versus NP.

**Next target:** authenticate the precise historical premise type and serialized bytes for derived RES clauses consumed by AND3, or produce an authoritative rejection. If accepted, the exact theorem becomes a native certificate family; if rejected, the discrepancy identifies a concrete missing grammar clause rather than silently revising the calculus.
