# LSPV-5/401 — cloning does not repair the corrected PC+Ext transfer

**2026-11-06 20:48 PST, America/Los_Angeles**  
**Role:** Independent red team, Route B primary  
**Status:** PROVED/EXACT clone-disjointization dilemma; COMPUTATIONAL finite controls; KNOWN THEOREM ledger update; historical `R_mix341`, `[P2-D1]`, `[P2-B1]`, `[P2-B2]`, `[P2-B5]`, `[P2-C3]`, and P versus NP OPEN.

## IDEA → SEARCH → ITERATE

Initial repair hypothesis: overlapping local definitions might be normalized into the author-corrected pairwise-disjoint-support PC+Ext model by replacing each shared original variable with fresh clones.

Falsifiers stated before search:

1. omitting clone-equality constraints changes the represented function;
2. treating clone equalities as extension axioms recreates the same support overlap;
3. treating them as source axioms changes the hard source, so the published lower bound no longer applies automatically;
4. even a polynomial algebraic simulation would not authenticate historical `R_mix341` definitions, branch scope, or fixed weights.

All four fired. The revised claim is the exact dilemma below. It narrows one natural attempted repair of `[P2-F10]`; it does not prove the all-rule minimum `[P2-B1]` or B3 `[P2-B2]`.

## Shared trackers and peer reconciliation

Both trackers were read completely before the construction:

- `proof1.txt` starting blob `e417a1a376d3347e6ef8f6915307005f5fa40972`;
- `proof2.txt` starting blob `91f72b6fbff08954a1ae7c85168ca88cbabd377a`.

Relevant exact IDs: `[P1-01]`, `[P1-03]`, `[P1-S3]`, `[P2-D1]`, `[P2-D2]`, `[P2-B1]`, `[P2-B2]`, `[P2-B5]`, `[P2-C1]`, `[P2-C3]`, `[P2-F8]`, `[P2-F9]`, `[P2-F10]`, `[P2-L3-463]`, and `[P2-L3-464]`. New scoped evidence is recorded as `[P2-F11]` and `[P2-L5-401]`.

The newest peer results were independently scoped:

- `[P2-L3-464]` gives an `h+2`-record external XLRUP construction for odd cubic Tseitin and contrasts it with the declared binary-premise `4h-1` optimum. Its report explicitly says neither the official `cake_xlrup` checker nor the historical native checker was run. It is a proof-format arity firewall, not historical grammar authentication.
- `[P2-A4]` LSPV-2/459 is a restricted source-promised balanced-tree OR-folding identity, and LSPV-4/457 gives an established cubic-expander Tseitin witness against automatic packet-preserving recursive closure. Neither closes all-input Route A.
- Grok's current progress file correctly treats FRAT-XOR as a distinct authenticated mixed format and leaves universal transfer open. Claude's current world ledger is an older independent conditional-status resource, not a proof of either route.

The full issue-#3 comment stream could not be fetched in this run: the connector transport closed on the 1,150-comment response. The current issue body and targeted issue searches were read, and the current tracker/peer commits were used as the authoritative coordination state. This limitation is not disguised as a full comment review.

## Established-family and theorem ledger

| Family/system | Exact encoding and size | Published lower bound | Strong legal controls | Remaining transfer |
|---|---|---|---|---|
| Chvátal–Szemerédi random proper 3-CNF `[P2-F8]` | `n` Boolean variables; `6n` indexed iid proper signed width-three clauses; `Theta(n log n)` encoded bits | `exp(Omega(n))` ordinary shared-DAG Resolution clauses with high probability | preprocessing, shared branching, extension and algebraic rules remain allowed | all historical mixed rules |
| Same random strict 3-CNF `[P2-F9]` | clause polynomial `prod_(positive x_j)(1-x_j) prod_(negative x_j)x_j=0` plus Boolean axioms | arbitrary-field PC linear degree and exponential monomial occurrence; bounded-DNF PCR lower bounds in their stated fields/parameters | PC/PCR substitutions and compact circuits are admissible controls | GF(2), LOCAL-CONVERT, AND3, paid recursive definitions, branch scope |
| Impagliazzo–Mouli–Pitassi `F^SEL` `[P2-F10]` | `O(n log n)` Boolean variables, polynomially many width-`O(log n)` constraints | finite-field PC+Ext exponential/subexponential size in published parameter regimes | only original-variable local extensions; official 2026 correction requires disjoint supports | strict-3CNF preservation and full `R_mix341` transfer |
| Alekseev BVP `[P2-F11]` | non-Boolean polynomial equation `1+x_1+2x_2+...+2^(n-1)x_n=0` plus Boolean equations, over `Q` | exponential **bit-size** in dynamic `Ext-PCsqrt` with arbitrary-depth algebraic extension circuits and square-root rule | strong upper-bound control: system p-simulates Extended Frege/Resolution and Res-Lin | source is inherently nonpropositional; no lower-bound-preserving strict-3CNF or historical-node transfer |

These are proof-system lower bounds only. They are not arbitrary-machine SAT lower bounds and do not certify a particular sampled random instance.

## Primary-source audit

Impagliazzo–Mouli–Pitassi, CCC 2023, Definition 4, defines extension axioms

`z_j - Q_j(x_1,...,x_N)`

where every `Q_j` uses original variables only. The paper explicitly excludes dependence on earlier extension variables. The official ECCC TR22-038 author comment accepted 2026-02-25 narrows the usable theorem further: the extension variables must be over disjoint sets of variables. The paper's source `F^SEL` is width `O(log n)`, not strict 3-CNF.

Alekseev's final Theory of Computing 2026 paper proves an exponential bit-size lower bound over `Q` for BVP in the stronger dynamic `Ext-PCsqrt` system. The paper and the CCC 2023 discussion both emphasize why this does not translate into a propositional lower bound: the hard source is non-Boolean as a polynomial system, and its propositional translation is not known to preserve hardness. It is therefore a mandatory strong-system control, not a solution to `[P2-B1]`.

Primary sources:

- Impagliazzo, Mouli, Pitassi, CCC 2023, DOI `10.4230/LIPIcs.CCC.2023.7`, especially Definitions 3–7 and Theorems 1–2.
- ECCC TR22-038, author correction accepted 2026-02-25.
- Alekseev, Theory of Computing 22(4), 2026, DOI `10.4086/toc.2026.v022a004`.

## Exact clone-disjointization dilemma

Take two overlapping local definitions

`z_1 = Q_1(x_0,x_1)` and `z_2 = Q_2(x_0,x_2)`.

The general `M`-arm star has supports `S_i={x_0,x_i}`. Clone `x_0` to fresh symbols `y_i` and use `z_i=Q_i(y_i,x_i)`. The nonlinear gate supports are now pairwise disjoint. Three exhaustive cases remain:

1. **No equalities.** The functions change. For the concrete control `Q_i(a,b)=a AND b`, `x_0=0`, `x_i=1`, `y_i=1` makes the cloned output one while the original output is zero.
2. **Equalities as extensions `y_i=x_0`.** Every equality has defining support `{x_0}`, so the support conflict graph is `K_M` and its maximum disjoint subfamily has size one. Moreover each `z_i` now depends on the earlier extension `y_i`, which Definition 4 forbids. Inlining `y_i=x_0` merely restores the original overlapping supports.
3. **Equalities as source axioms.** Treating each `y_i` as an original variable and adding `y_i-x_0=0` changes the hard source from the published `F^SEL`. Equisatisfiability does not give the lower-bound-preserving direction needed for `[P2-B1]`.

Therefore variable cloning alone does not map overlapping or nested historical definitions into the corrected theorem's model. This is a theorem-hypothesis/source-authentication firewall, not a lower bound against the historical mixed calculus.

## Mandatory algebraic upper-bound control

The repair is not rejected because equality reasoning is expensive. For any commutative ring,

`prod_i y_i - prod_i x_i = sum_i (y_i-x_i)(prod_(j<i)y_j)(prod_(j>i)x_j)`.

Thus, once the equality equations are legal premises, monomial substitution has a linear-in-arity telescoping derivation. A general explicit polynomial is handled monomial by monomial with the corresponding charged expansion. This is a real shortcut and must be allowed when auditing the true minimum. It still does not decide whether the equalities are legal historical source/definition nodes or preserve the published hard family.

## Executable controls

`experiments/review/lspv5_401_clone_disjointization_firewall.py` independently checks `M=2,...,8`:

- the original and equality support graphs are `K_M`;
- the cloned nonlinear gate supports are pairwise disjoint;
- all assignments satisfying `y_i=x_0` reproduce the original gates;
- omitting equalities produces explicit mismatches;
- the product telescoping identity holds symbolically for arities 1–8;
- duplicate/nonfresh outputs, missing equalities, unknown targets are rejected; large numerical IDs are accepted.

Result: **175,809 assertions PASS**, 117,950 semantic mismatches without equalities at `M=8`, Python peak traced allocation 47,373,544 bytes, process peak RSS 112,388 KiB, elapsed about 2.8 seconds. The independently written Node replay performs **85 checks PASS**. These are finite semantic/syntactic controls, not executions of an authoritative PC, XLRUP, or historical `R_mix341` checker.

## Corpus and search log

Change-aware repository review found no head changes since REFEREE400 in `konard/p-vs-np` (`ecedd2b...`), `blkph0x/p-vs-np-proof-research` (`7dedc73...`), `frat-xor` (`18cd6bc...`), `cake_lpr` (`033aad5...`), `short-proof` (`2c524cf...`), CNFgen (`24e633b...`), CryptoMiniSat (`ed61e21...`), or `openai/math` (`4eaee87...`). Actual files re-read included `konard/.../scripts/proof_status.json` blob `93b77ed...`, `blkph0x/.../METHOD_INDEX.md` blob `18d693e...`, `frat-xor/format.md` blob `986a21a...`, `cake_lpr/README.md` blob `e94f45e...`, and `short-proof/README.md` blob `93d2090...`. The external repositories remain sources of formalization, locality, certificate, and optimization controls; none proves the required same-calculus transfer.

Primary web queries covered the corrected PC+Ext theorem, PC substitutions and equality axioms, and Alekseev's final Ext-PC square-root lower bound. Google-branded search UI was not available; primary-source web search was available and used. CNFgen's root `README.md` path returned 404; repository search located its current `docs/cnfgen.rst`, so this is logged as a path failure rather than a source review success.

## Resource ledger

Logical object counts: `M=2,...,8`, 175,809 Python assertions and 85 independent Node checks. Explicit evidence: source script, replay, JSON rows, first counterexample per `M`, hashes. Construction/search: exhaustive Boolean tables through `2^(2M+1)` assignments, bounded at `M<=8`; no asymptotic optimizer claim. Parsing: JSON and fixed typed records only. Source/index/head reads: complete trackers, governing files, peer reports, repository heads and primary papers; issue-comment bulk read failed as stated. Updating/conversion: no CNF or proof-system conversion; planned complete-blob optimistic tracker update only. Verification/output: JSON serialization plus independent Node parse/recomputation. Caches: ordinary process/runtime caches only. Retrieval/recomputation: truth tables recomputed, no persisted semantic oracle. Failed policies: issue-comment bulk retrieval transport closure, CNFgen root README 404, root `main.tex` connector returns zero content. Peak space: measured finite checker values above; no claim that these are FLMV or historical proof-resource measurements.

## Actual advance and remaining gap

**Actual advance:** `[P2-L5-401]` rules out the most direct variable-cloning repair of the official disjoint-support correction and supplies the exact algebraic shortcut that becomes available if equality premises are legal. `[P2-F11]` records a stronger algebraic lower-bound control whose nonpropositional source prevents it from solving the strict-3CNF transfer.

**Precise remaining gap:** authenticate historical `R_mix341` and either prove a lower-bound-preserving simulation/retraction for every legal mixed, shared, branching, recursive-definition proof or find a published theorem that already covers exactly those rules and a preserved strict-3CNF source. Independently prove a noncircular same-`R` B3 bridge. P versus NP remains OPEN.

