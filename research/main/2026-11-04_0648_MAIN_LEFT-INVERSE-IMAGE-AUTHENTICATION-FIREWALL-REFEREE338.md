# LEFT-INVERSE-IMAGE-AUTHENTICATION-FIREWALL-REFEREE338

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 4, 2026, 06:48 PST**

**Status:** **PROVED/EXACT** counterexample separating lossless decoding from image and semantic authentication; **PROVED/RESTRICTED** uniform recognizable-family recoding schema and ordinary-Resolution proof-cost collapse; **PROVED/EXACT but only linear-to-zero** fixed-`R_mix341` prism calibration; **DUPLICATE/SPECIALIZED** recoding mechanism relative to LSPV-1/373, REFEREE323/325, LSPV-2/375 and LSPV-3/394; **OPEN** polynomial source-rooted transport for full `R_mix341`, B1/B2/B3 for that fixed calculus, unrestricted SAT hardness, and P versus NP. No task, schedule, enabled state, ownership, calculus rule, or weight was changed.

## Outcome

The proposed new active-source lossless recoding theorem is valid but is not a new lower-bound mechanism. The project already had a stronger source-prefix compiler and the recognizable-island firewall. The substantive finding of this run is narrower and exact:

> A polynomial-time encoder `E` and decoder `D` with `D(E(s))=s` for every raw source string do not authenticate an arbitrary claimed target `G`. Even if `E` is injective and semantically exact on its image, `D(G)=s` need not imply `G=E(s)`, `G` lies in the image, or `G` projects to the same model relation as `s`.

The current LSPV-3/394 decoder has exactly this risk: it extracts duplicated payload tags and ignores unrelated active clauses. An explicit forged target retains every tag and hence decodes to the same satisfiable source, but its active clause is replaced by a source empty clause, making the target UNSAT. The minimal robust repair is full image authentication, for example `G = E(D(G))`, or an equivalent proof-carrying check of every active clause, tag, branch decision, and header.

This repair blocks forged off-image targets. It does **not** repair proof-cost reflection on honest images. A recognized UNSAT family may still be honestly encoded with a new free contradiction. Transporting that target proof back to the original source remains the missing source-rooted proof compiler.

## Exact obstruction and four falsifiers

1. **Left inversion authenticates the representation. — FALSE.** `D(E(s))=s` constrains `D` only on `im(E)`; it says nothing about arbitrary `G` accepted by a permissive decoder.
2. **Duplicating payload tags authenticates the active formula. — FALSE.** Duplicate agreement detects one-tag corruption, not replacement of active clauses or a coordinated change to both copies.
3. **Retaining every original clause makes the short contradiction source-rooted. — FALSE.** A newly appended empty source clause bypasses every retained clause.
4. **The fixed-mixed `4h-1 -> 0` collapse refutes polynomial domination or B1. — FALSE.** `4h-1=O(N)` is already polynomially dominated by parsing and construction; no superpolynomial fixed-`R_mix341` separation follows.

No new hard formula was generated and no published lower bound was regenerated.

## Published lower-bound anchor: exact model, encoding, quantifiers, strength

For `h` holes and `h+1` pigeons, canonical unary `PHP(h+1,h)` has variables `x_(i,j)`, one positive pigeon clause for each pigeon, and one binary negative collision clause for every pair of pigeons and hole. It has `h(h+1)` variables and

`(h+1) + h * binom(h+1,2) = Theta(h^3)` clauses.

With explicit signed binary indices in an ordered DIMACS-style encoding, its length is `N_h=Theta(h^3 log(h+2))`.

The Haken theorem used by the project is: there are constants `c>0,h0` such that, for every `h>=h0`, every ordinary shared-DAG Resolution refutation of this explicit contradiction has at least `2^(c h)` derived lines. Source clauses are free; every derived line is one clause obtained by binary Resolution on a complementary pivot; arbitrary widths, pivots and DAG reuse are allowed. Extension variables, GF(2) rows, circuit gates, Horn or 2-SAT procedures, semantic jumps, and arbitrary machine computations are not Resolution lines.

Thus the lower bound is `2^Omega((N_h/log N_h)^(1/3))`, not `2^Omega(N_h)`. It is ordinary-Resolution proof hardness, not `Res(XOR)`, Extended Resolution, `R_mix341`, or unrestricted SAT-machine hardness. Haken explicitly records the polynomial Extended Resolution escape.

Primary sources actually checked this run:

- A. Haken, *The Intractability of Resolution*, TCS 39 (1985), DOI `10.1016/0304-3975(85)90144-6`;
- S. Cook and R. Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44(1) (1979), 36–50, primary PDF `https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf`.

Cook–Reckhow polynomial simulation concerns encoded proofs and proof length. It does not supply a simulation of arbitrary SAT deciders by one preselected proof system.

## Fixed `R_mix341`: exact starting theorem and limited corollary

The authoritative fixed calculus is

`research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, current blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. Its rules are free authenticated DIMACS source clauses, unit-paid at-most-binary `RES`, support-three `AND3`, binary GF(2) row addition, unary constant-support `LOCAL-CONVERT`, and paid two-input conservative `DEF`.

For every connected simple bridgeless cubic graph `G` on `h` vertices with odd total charge, its canonical Tseitin CNF satisfies exactly

`W_Rmix341(F_(G,chi)) = 4h-1`.

This is an exact minimum in the declared logical-node measure. It is not a machine-time lower bound; the proof is itself a compact GF(2) shortcut.

Applying the honest recoder below to a fixed polynomial-time recognizable canonical odd-prism subfamily gives an encoded source with a free empty clause, so its encoded minimum is zero. This is a valid same-calculus, changed-source exact-cost collapse. LSPV-2/375 already proved the stronger practical point with a source-prefix compiler and opposite units, giving `4h-1 -> 1`. The present zero-node variant is therefore only a calibration. Since the native cost is linear, it does not refute polynomial cost reflection, B1, B2, or B3.

## Lemma 1: fixed uniform active-source recoder

Let `S` be any fixed language recognized by one deterministic polynomial-time program, with

`S subset ValidCNF intersection UNSAT`.

Then there are fixed uniform polynomial-time programs `E_S,D` such that, for every raw byte string `s`:

1. `E_S(s)` is valid general DIMACS CNF;
2. `D(E_S(s))=s`;
3. `|E_S(s)|=O((|s|+1) log(|s|+2))` bits in the explicit decimal implementation;
4. for every valid CNF `F`, projection of `Mod(E_S(F))` onto the renamed original variables equals `Mod(F)`;
5. if `F in S`, `E_S(F)` contains a source empty clause and hence has zero paid derived nodes in any calculus accepting source contradiction.

**Construction.** Map each original variable `v` to the even identifier `2v` and retain every source clause, sign and clause order. Encode every raw source bit twice using two fresh odd-ID signed unit clauses. The two copies provide corruption detection; the disjoint odd namespace and the ordered contiguous tag grammar give exact byte recovery, including arbitrary malformed bytes. On valid `F`, append one empty clause iff the fixed recognizer accepts `F`. Malformed strings receive tags only.

The signed unit tags are satisfiable and disappear under existential projection. They repair the parser ambiguity in the tautological tags used by LSPV-3/394, because several project grammars reject complementary literals inside one clause. General CNF and `R_mix341` already admit units. If an exact target grammar rejects source empty clauses, append opposite fresh units instead; the target proof cost becomes one, reproducing LSPV-1/373, REFEREE325 and LSPV-2/375.

For `F notin S`, the active renamed source plus disjoint unit tags has exactly the original projected models. For `F in S`, both model sets are empty, so projection equality is true but vacuous. The quantifier order is

`for every fixed S and recognizer, there exist fixed E_S,D, for every s`.

There is no per-input answer, per-`N` optimizer, or advice string. The encoder nevertheless uses family-specific semantic knowledge: recognizing `S` is not a legal `R_mix341` inference.

Taking `S` as the canonical unary-PHP family gives honest encoded Resolution cost zero while the original requires `2^Omega(h)` lines. Therefore no polynomial ordinary-Resolution backtranslator can convert these target proofs to source proofs. Taking `S` as canonical odd prisms gives the exact fixed-mixed `4h-1 -> 0` calibration only.

## Lemma 2: a left inverse is not image or semantic authentication

Let

`s = "p cnf 1 1\n1 0\n"`,

the satisfiable one-variable source `(x_1)`. Its honest encoding contains active clause `(x_2)` followed by the duplicated signed odd-ID unit tags. Let `G` be the same encoded byte string except that the active `(x_2)` clause is replaced by the empty clause.

Then:

- `D(E_S(s))=s`;
- `D(G)=s`, because `D` reads only the tag namespace;
- `s` and `E_S(s)` are SAT;
- `G` is UNSAT because it contains a source empty clause;
- hence `proj Mod(G) != Mod(s)` and `G != E_S(D(G))`.

This is an all-explicit counterexample. It is not a hash collision, malformed-source trick, or nonuniform family. It shows that left inversion plus duplicate payload agreement authenticates the payload, not the active representation or its semantics.

The polynomial full-image verifier

`V(G) := [G = E_S(D(G))]`

rejects the forgery and accepts every honest image. Equivalent implementations may stream a canonical comparison or carry a proof that authenticates the active copy, header, tag order, branch result, and every auxiliary clause. A decoder that merely returns bytes is not such a verifier.

The repair is necessary but not sufficient for representation-independent proof cost. Honest `E_S(PHP_h)` passes `V` and still has a free contradiction. To transport proof hardness one must additionally map every used target axiom and inference to a polynomial-size source-rooted macro. Splicing those macros is exactly the missing proof backtranslation.

## Fully charged time/space and lazy-access ledger

Let `N=|s|` source bits and `L=|E_S(s)|=Theta(N log(N+2))` for the explicit decimal tag encoding.

| phase/object | charged work | output/access | peak writable space |
|---|---:|---:|---:|
| parse and exact family recognition | `Omega(N)` reads; `O(N polylog N)` safe upper bound | every late distinguishing byte may matter | `O(log N)` with rereads; materialized parser uses `Theta(N)` or more |
| active clause copy | `Theta(N)` logical payload plus decimal renaming | every literal emitted | streaming possible |
| duplicated unit tags | `Omega(L)` bit writes | `Theta(L)` explicit bytes | `Theta(L)` if materialized; logarithmic scratch if streamed |
| decoder on honest image | `Omega(L)` reads and `Omega(N)` recovered output | all tags accessed | current Python materializes `Theta(L)`; multipass streaming can reduce scratch |
| full image verifier | decode, re-recognize, re-encode, compare: `O(L polylog L)` safe | every target bit authenticated | `Theta(L)` materialized; lower scratch with paid rereads |
| random-access lazy target | recognition state and tag/index queries still paid | without index, a query may scan; a full index costs `Theta(N log N)` bits | schedule dependent |
| PHP proof backtranslation | must output `2^Omega(h)` Resolution lines | exponential proof output | streaming lowers retained space, not output time |

The current producer constructs lists and strings, so its actual all-phase peak is `Theta(L)` up to interpreter overhead. A two-pass encoder can recognize first and stream second using small auxiliary space, but it still reads the source and writes `L` bits. On a nonrewindable stream, a late mismatch requires spooling the source, patchable output, or a changed wrapper; none is free.

An exponential PHP proof backtranslation is not evidence of exponential SAT runtime. One uniform machine recognizes canonical PHP in polynomial time and outputs `UNSAT` without emitting a Resolution refutation. The backtranslator is slow because its required output is exponentially long.

## B1/B2/B3 classification

| obligation | result |
|---|---|
| ordinary-Resolution B1 | prior **FALSIFIED** by REFEREE325: recognize canonical PHP, otherwise use one fixed complete fallback |
| ordinary-Resolution B2 | **OPEN**; the fallback may be exponential elsewhere |
| ordinary-Resolution B3 | **OPEN** |
| fixed-`R_mix341` B1 | **OPEN**; PHP has stronger-system escapes and the prism native cost is linear |
| fixed-`R_mix341` B2 | **OPEN** |
| fixed-`R_mix341` B3 | **OPEN** |
| superpolynomial `Wbar_Rmix341` | **OPEN** |
| unrestricted SAT time/space lower bound; P versus NP | **OPEN** |

The recoder changes the source and is not an `R_mix341` inference. Nothing here reverses a simulation inequality. No exponential-overhead backtranslation is used as machine-hardness evidence.

## Finite controls and malformed behavior

The Python producer checked 273 records (265 valid CNFs and eight malformed byte strings): all 256 subsets of a fixed eight-clause two-variable universe; canonical PHP with one, two and three holes; and odd and even prism Tseitin controls for `k=3,4,5`. It performed **1,929 assertions PASS** covering exact raw roundtrip, active-clause retention, tag count and grammar, complete-image verification, recognized-family soundness, odd/even prism model counts, tag-pair corruption rejection, and the forged-target semantic failure.

The independently written Node verifier performed **415 assertions PASS**. It independently rebuilt the decisive unit-source encoder, forged target, tag decoder and full-image equality test rather than trusting only the raw status fields.

Artifacts and SHA-256:

- `experiments/arc/lspv5_338/recognizer_conditioned_recoding_referee338.py` — `38f2ebf9b9dc9bc5dd50a7a3008a72a1dc58796e75bea71af20b6867de018458`;
- `experiments/arc/lspv5_338/verify_recognizer_conditioned_recoding_referee338.js` — `6d4d627a4096d6f541236faa796aff69f346e951992588c0b9c7087e21b56f48`;
- `results/raw/arc/lspv5_338/recognizer_conditioned_recoding_referee338.json` — `959872aaca873ba7d464243b97d303e3c486d4f6c04a59408cfcc0394b972150`.

Finite tests support the implementation and counterexample. They do not prove Haken's asymptotic theorem or any machine lower bound.

## Duplication, five-role review, Grok and Claude

Issue #3 was read through **787 comments**. The newest peer reports were LSPV-1/390, LSPV-2/391, LSPV-3/394 and LSPV-4/386. The recoding route was checked against:

- LSPV-1/373 `research/agents/lspv-1/2026-11-03_1500_LSPV-1_REVERSIBLE_REPRESENTATION_TRAP373.tex`, blob `1cf73470332a8d3de56dd5f4d918f5343e96ff97`;
- REFEREE323 `research/main/2026-11-03_1548_MAIN_SEMANTIC-QUOTIENT-ALGORITHM-MINIMUM-COLLAPSE-REFEREE323.md`;
- REFEREE325 `research/main/2026-11-03_1748_MAIN_RECOGNIZABLE-ISLAND-CERTIFICATE-ROOTING-REFEREE325.md`;
- LSPV-2/375 `research/agents/lspv-2/2026-11-03_1712_LSPV-2_UNIFORM_SOURCE_PREFIX_COMPILER375.md`, blob `d33582b746604732575e0ddec48d8bc3aa9a4cb9`;
- LSPV-3/394 `research/agents/lspv-3/2026-11-04_0624_LSPV-3_LOSSLESS_SEMANTIC_RECODING_FIREWALL394.tex`, blob `d79f05a4015da13f44f1e4fcde3604fe2308251c`.

All five specialists agreed that the active-source recoder is a duplicate/specialization, not a new representation-independent theorem. LSPV-1 fixed the uniform quantifiers and B classification; LSPV-2 checked the odd/even affine control; LSPV-3 identified the tag-grammar issue and source-ancestry failure; LSPV-4 supplied the explicit forged-target attack and all-phase ledger; LSPV-5 classified the duplication and polynomial-envelope limit.

The current Grok assessment actually read was `GROKPROOF/2026-11-04_1322_PROGRESS.md`, blob `0850246c1a1ea9a511d12a4de041b8752f69922a`. It leaves the arbitrary-`A`, fully charged all-input transformation open and supplies no proof-cost backtranslation.

Claude has no post-October-28 assessment. The relevant files actually read were:

- `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`;
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`;
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`.

They provide restricted direct-product, alternation-trading, and one-tape evidence, not B3 or a source-rooted full-mixed compiler. Their encoding cautions are consistent with this audit but are not used as authority.

## Search log

Primary-source searches:

- `Haken 1985 intractability of resolution pigeonhole principle shared DAG resolution theorem PDF`;
- `Cook Reckhow 1979 relative efficiency propositional proof systems p simulation PDF`;
- `Tseitin formulas resolution lower bounds expander graph exact proof system primary paper survey PDF`.

Repository/GitHub searches:

- `REVERSIBLE_REPRESENTATION_TRAP373 repo:j15marti/pnp`;
- `UNIFORM_SOURCE_PREFIX_COMPILER375 repo:j15marti/pnp`;
- `left inverse image verification semantic equivalence repo:j15marti/pnp`;
- `decoder image authentication lossless recoding repo:j15marti/pnp`;
- `propositional proof checker resolution certificate compiler org:openai`.

The project search found the prior duplicates and the older IMAGEEQUIV1 image-recognizer theorem. The `github.com/openai` query returned no relevant implementation. This is a search result, not novelty evidence.

## Classification and next exact gap

**PROVED:** left inversion is strictly weaker than image and semantic authentication; the displayed forgery is exact; full-image equality rejects it; the uniform active-source recoder is lossless and semantically exact on its image.

**RESTRICTED/DUPLICATE:** Haken is ordinary Resolution only; the recoding schema and recognizable-island escape predate this run; the fixed-mixed application is merely linear-to-zero on a changed source.

**FAILED CANDIDATE INVARIANT:** signed-hypergraph structure retained as an active subformula does not force proof cost when a new free contradiction is permitted. Lossless payload recovery does not establish proof ancestry.

**OPEN:** define and polynomially verify a nontrivial representation-equivalence relation that authenticates all target semantics **and** carries polynomial source-rooted proof macros for every allowed full-`R_mix341` rule. The first requirement blocks forgeries; the second is the actual proof-cost transfer. Extending it to arbitrary correct uniform SAT deciders is B1/B3, not a routine encoding lemma.

**B1 OPEN; B2 OPEN; B3 OPEN for fixed `R_mix341`; P versus NP OPEN.**
