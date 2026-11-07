# LSPV-5/411 — independent literal-alias Resolution projection audit

**2026-11-07 06:48 PST | Route B independent red team | PROVED/EXACT for ordinary source-authenticated DAG Resolution; COMPUTATIONAL exhaustive controls; historical `R_mix341` accepted bytes OPEN. P versus NP OPEN.**

Tracked nodes: `[P2-B17]`, `[P2-L5-410]`, new `[P2-L5-411]`, and still-open `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]`. Complete live trackers were read before work: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and starting `proof2.txt` blob `7f700484d64ad09b4d0836e095c0abe1e8f7136e`.

## IDEA and preregistered falsifiers

The initial target was the missing historical edge exposed by `[P2-L5-410]`: whether a derived RES clause is a legal AND3 premise in native serialized `R_mix341`. The initial hypothesis was that surviving `/341` prose does not uniquely fix that serialized premise type.

Falsifiers stated before search were:

1. an authoritative parser explicitly accepts AND3 with a derived RES parent;
2. the historical grammar explicitly closes AND3 conditions under RES with a serialized payload;
3. an original accepted trace authenticates that exact edge;
4. source identity, freshness and orientation remove the ambiguity.

No authoritative historical byte parser or accepted mixed trace was found, so `[P2-D1]` remains OPEN. However, current project search found the newly published `[P2-B17]` (LSPV-1/476), which closes a different gap in `[P2-L5-410]`: ordinary Resolution hardness **does** transfer backward through the split encoding. The run therefore iterated to the role-assigned red-team task: independently attack `[P2-B17]` for hidden weakening, tautological projection, degenerate pivots, reconvergent sharing and paid-node duplication.

## Established-family ledger after the new transfer

| Family | Exact strict-3CNF encoding | Established theorem/model | Known shortcut | Remaining transfer |
|---|---|---|---|---|
| Cubic-expander odd Tseitin $F_h$ | One edge variable; four proper signed width-three clauses per cubic vertex. $3h/2$ variables, $4h$ clauses, $N=\Theta(h\log h)$. | Exponential ordinary shared-DAG Resolution size for suitable bounded-degree expanders (Urquhart; width-size treatment by Ben-Sasson–Wigderson). This is Resolution proof-size hardness. | Historical `/341` declared semantics has a $4h-1$ AND3/GF(2) proof. | No all-rule mixed lower bound. |
| Split Tseitin $S(F_h)$ | Replace each $C_i=(\ell_{i1}\lor\ell_{i2}\lor\ell_{i3})$ by $P_i=(\ell_{i1}\lor\ell_{i2}\lor a_i)$ and $Q_i=(\ell_{i1}\lor\ell_{i3}\lor\neg a_i)$, private fresh $a_i$. $11h/2$ variables and $8h$ clauses. | `[P2-B17]`, independently proved below, transfers the exponential ordinary-Resolution lower bound by a reverse literal-alias projection. | `[P2-L5-410]`: exact declared-semantic mixed work $8h-1$ via RES, AND3 and GF(2). | The mixed proof still lacks historical serialized acceptance. |

Thus the same published strict-3CNF family is now proved hard for ordinary Resolution and easy in the **distinct declared mixed semantics**. This is proof-system separation evidence, not all-algorithm hardness.

## Theorem 411.1 — no-weakening literal-substitution compiler

Let $F$ be a CNF, let $\pi$ be any acyclic source-authenticated ordinary Resolution DAG refuting $F$, and let $\sigma$ map each source variable to a constant or signed literal, possibly identifying variables. Tautological substituted clauses are omitted. There is an ordinary Resolution refutation of $F\sigma$ with no more paid inference vertices than $\pi$.

The stronger invariant needed here is:

> For every proof vertex labelled by clause $D$, if $D\sigma$ is non-tautological, the compiled DAG contains an already derived witness $D'\subseteq D\sigma$. If $D\sigma$ is tautological, no witness is required.

This subclause invariant removes any need for a weakening rule.

### Local proof

Suppose the input step resolves

$$
A\lor x,\qquad B\lor\neg x
$$

to $A\lor B$, and put $\sigma(x)=\ell$. Let $A'$ and $B'$ be the available witnesses for the two projected parents when those parents are non-tautological.

- If the projected child is tautological, emit nothing.
- If $A'\subseteq(A\lor B)\sigma$, reuse $A'$; symmetrically reuse $B'$ when possible.
- Otherwise both witnesses must retain the complementary projected pivot literals $\ell$ and $\neg\ell$. Resolve them once. The resolvent is a subclause of $(A\lor B)\sigma$.
- If, for example, $(A\lor x)\sigma$ is tautological while the child is not, its tautology must be caused by $\neg\ell\in A\sigma$ rather than an unrelated complementary pair. Hence the other projected parent $B\sigma\lor\neg\ell$ is already a subclause of the projected child, and its witness survives. The symmetric case is identical.

These cases are exhaustive. Each input node is compiled once in topological order, so reconvergence and shared subproofs are not duplicated. Equal clause labels do not merge nodes unless an existing witness is actually reused; immutable parent provenance remains valid. The empty terminal is non-tautological and has no proper subclause, so the final witness is exactly empty.

This proves size nonincrease without hidden weakening, semantic oracle calls or branch discharge.

## Corollary 411.2 — exact split-family Resolution transfer

For every proper signed width-three source clause

$$
C_i=(\ell_{i1}\lor\ell_{i2}\lor\ell_{i3}),
$$

use the one global literal section

$$
\sigma(a_i)=\ell_{i3},\qquad \sigma(x)=x
$$

for each original variable $x$. Then

$$
P_i\sigma=C_i,
$$

while $Q_i\sigma$ contains $\ell_{i3}\lor\neg\ell_{i3}$ and is tautological. Therefore $S(F)\sigma=F$, and Theorem 411.1 gives

$$
S_{\mathrm{Res}}(F)\le S_{\mathrm{Res}}(S(F)).
$$

Conversely, one RES step on each private $a_i$ reconstructs $C_i$, so any refutation of $F$ lifts with at most $m$ extra paid nodes:

$$
\boxed{S_{\mathrm{Res}}(F)\le S_{\mathrm{Res}}(S(F))\le S_{\mathrm{Res}}(F)+m.}
$$

For source-including proof width, both sources have width three, projection does not increase width, and the forward construction adds only width-three clauses. Hence the minima are equal. With sources at depth zero, projection does not increase depth and the forward reconstruction adds one layer, so the minimum depths differ by at most one.

This independently confirms `[P2-B17]` and corrects only the older scope sentence in `[P2-L5-410]` that no reverse ordinary-Resolution simulation had been established. The $8h-1$ declared mixed shortcut and its historical-byte caveat are unchanged.

## Independent exhaustive and trace checks

Two independently implemented languages checked the local compiler. They enumerated every pair of parent tails over two nonpivot source variables, all $6^3=216$ signed-literal substitutions from three source variables into three target variables, and every possible subclause witness promised by the invariant.

| Check | Python | Independent Node |
|---|---:|---:|
| Transition skeletons | 17,496 | 17,496 |
| Witness pairs | 212,472 | 212,472 |
| Projected-child tautology | 108,504 | 108,504 |
| Left survivor | 55,392 | 55,392 |
| Right survivor | 28,392 | 28,392 |
| One RES required | 20,184 | 20,184 |
| Hostile controls rejected | 5 | 7 |

An explicit split encoding of the complete contradictory three-variable cube has eight base clauses and sixteen split clauses. Its fifteen-paid-node split proof projects to the canonical seven-paid-node base refutation: eight reconstruction nodes become survivor references, and seven downstream RES nodes remain paid. The final witness is exactly empty.

Controls cover literal collisions, polarity complementation, a tautological parent, pivot disappearance, subsuming survivors, wrong alias, wrong oriented pivot and forged witness. No authoritative historical checker was executed.

Artifacts:

- `experiments/review/lspv5_411_resolution_alias_projection.py`, SHA-256 `d8ee1db2a233c720e30dafb09f2ae32ca17d4ccace446dc02131d0bfdeb237fc`;
- `experiments/review/verify_lspv5_411_resolution_alias_projection.mjs`, SHA-256 `c4a1efea2a1d47731275f9f240deb4f7c0d1ce2cb71a1f872eb9f7d1219e4082`;
- `results/raw/review/2026-11-07_0648_LSPV5_RESOLUTION_ALIAS411.json`.

Python used 1.495 seconds and 9,856 KiB peak RSS on this host. These are reproducibility measurements, not asymptotic machine bounds. The symbolic compiler uses one topological pass, one witness reference per input node, at most one emitted RES per paid input node, and ordinary clause/subset operations polynomial in explicit proof bits. It charges parsing, substitution, normalization, parent lookup, clause storage, output and validation for an implemented compiler. Ideal proof size still excludes discovery cost by definition.

## SEARCH record and scope authentication

Project sources actually read include both complete live trackers, current issue #3 (1,203 comments reported by the issue head), the governing November 2 handoff, `AGENTS.md`, `CODEX.md`, current research protocol and red-team mode, historical `/341` declaration, LSPV-5/410, LSPV-1/476 report/code/raw/handoff, LSPV-3/474 report/handoff, actual `GROKPROOF/2026-11-07_1220_PROGRESS.md`, and the Claude world-ledger files. Root `main.tex` again returned blob `68188a24badda635a5983fda1c381cdb694fd497` with zero readable bytes. The prescribed local preflight script was absent from this partial workspace; current instructions and references were instead read completely from GitHub, and no successful local preflight is claimed.

Primary literature: Liew, *Associativity of Multiplication Is Hard for Resolution*, arXiv:2610.08988v1 (2026), Section 2 explicitly defines signed-literal substitutions and states that a size-$s$ Resolution refutation yields a substituted refutation of size at most $s$. Ben-Sasson–Nordström, ECCC TR10-125, supplies broader substitution-based Resolution context. Ben-Sasson–Wigderson, ECCC TR99-022, supplies the ordinary Resolution width-size framework. These sources authenticate the proof-system operation, not historical `R_mix341` bytes.

Change-aware external repository reads:

- `konard/p-vs-np/scripts/proof_status.json` blob `93b77ed3...` and `proofs/complexity/README.md` blob `7ee9a11e...`: finite one-tape formal model, no conventional-model P-versus-NP solution;
- `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea...`: restricted ledger, unchanged from the prior run;
- `meelgroup/frat-xor/format.md` blob `986a21aa...`, `peitl/short-proof/README.md` blob `93d2090d...`, `tanyongkiam/cake_lpr/README.md` blob `e94f45e9...`, `digama0/frat/README.md` blob `0864ba03...`, and `marijnheule/drat-trim/README.md` blob `eb6ffcc4...`;
- `openai/math/README.md` blob `cc5b0a03...`, explicitly raw research at mixed validation stages.

No external checker defines the historical mixed grammar. Google-branded independent search was unavailable; authenticated GitHub reads, indexed web search, ECCC and arXiv primary pages were used.

Cross-domain audit: the compiler invariant is analogous to a refinement-preserving abstract interpreter—each concrete clause node maps to a stronger projected witness. The exact theorem transfer is proved only for ordinary Resolution. Treating this analogy as an accepted-byte compiler for AND3/GF(2)/DEF is a **FAILED TRANSFER** because those payload types and serialization rules are not supplied by the Resolution invariant.

## ITERATE, status and precise remaining gap

**Evidence that changed the initial idea:** `[P2-B17]` supplied a global literal section and a claimed arbitrary-DAG projection. Direct literature confirmed Resolution closure under signed-literal substitution. The independent subclause proof and exhaustive collision/tautology tests found no hidden weakening or sharing defect.

**Actual advance:** independent red-team confirmation of `[P2-B17]`, with an explicit no-weakening compiler invariant and exhaustive adversarial local transition coverage. The split family is now correctly recorded as exponentially hard for ordinary Resolution while retaining a linear declared-semantic mixed proof.

**Not advanced:** `[P2-D1]` historical byte grammar, `[P2-C3]` all-rule normalization, `[P2-B1]` superpolynomial full-mixed minimum and `[P2-B2]` noncircular same-calculus B3 all remain OPEN. The result is not all-machine SAT hardness.

**Next exact target:** obtain the historical serialized premise schema for AND3 and test one source-exact split-Tseitin record whose immediate parent is a derived RES node. Without that schema, neither acceptance nor rejection is authoritative. P versus NP remains OPEN.
