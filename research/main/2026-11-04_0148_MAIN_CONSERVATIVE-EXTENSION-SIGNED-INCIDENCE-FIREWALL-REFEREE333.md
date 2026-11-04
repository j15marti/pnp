# CONSERVATIVE-EXTENSION-SIGNED-INCIDENCE-FIREWALL-REFEREE333

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 4, 2026, 01:48 PST**

**Status:** PROVED/EXACT ordinary-Resolution counterexample to source-retention, selector-profile and unique-fibre invariance under total conservative definitions; PROVED/EXACT necessary cost-reflection direction; PROVED/RESTRICTED linear source-ancestry invariant for fixed `R_mix341`; COMPUTATIONAL independent finite controls. This independently audits and synthesizes project LSPV-2/378, LSPV-1/384 and REFEREE332, not a new published lower bound. Fixed `R_mix341`, its rules and weights, five roles, enabled states and hourly schedules are unchanged. B1/B2/B3 for `R_mix341`, superpolynomial `Wbar_Rmix341`, unrestricted SAT hardness and P versus NP remain OPEN.

## Outcome first

Retaining the complete original signed hypergraph is not enough if sound conservative definitions are permitted.

Let `P_h=PHP(h+1,h)`, the established Haken-hard unary pigeonhole CNF. Cook's polynomial Extended-Resolution proof uses an acyclic family `D_h(X,Y)` of total functional gate definitions. Move those definition clauses into the input source and set

`G_h(X,Y)=P_h(X) AND D_h(X,Y)`.

Then all of the following hold simultaneously:

1. every original PHP clause, sign, variable and source identity occurs unchanged in `G_h`;
2. `exists Y G_h(X,Y)=P_h(X)` exactly;
3. every original assignment has exactly one auxiliary extension satisfying `D_h`;
4. the complete selector SAT function on the original clauses, with `D_h` retained, is unchanged;
5. every original PHP clause remains deletion-essential; and
6. both explicit signed binary-index sources have `Theta(h^3 log h)` bits.

Nevertheless,

`W_Res(P_h)=2^Omega(h)` but `W_Res(G_h)=h^O(1)`.

Thus exact projection, unique fibres, signed-source retention, deletion essentiality and complete original selector semantics still do not preserve proof hardness. Any valid hardness transfer must reflect each short extended proof back to the original system with polynomial overhead. For Cook's family, such an ordinary-Resolution backtranslation provably cannot exist.

This is a proof-system/source-map separation. It is not an arbitrary-machine SAT lower bound and not a lower bound for unchanged `R_mix341`.

## Established anchors: exact models, encodings and strength

### Haken ordinary-Resolution lower bound

`P_h` has `h(h+1)` variables, `m_h=(h+1)+h*binom(h+1,2)=Theta(h^3)` source clauses and explicit signed binary-index/DIMACS length `N_h=Theta(h^3 log(h+2))`.

There exist constants `c>0,h_0` such that

`for every h>=h_0, for every ordinary unrestricted shared-DAG Resolution refutation pi of P_h, |pi|>=2^(c h)`.

Source clauses are axioms; every derived line is an ordinary resolvent; pivots, widths and DAG sharing are unrestricted. With free source leaves and unit-paid derived nodes,

`W_Res(P_h)>=2^(c h)-m_h=2^Omega(h)`.

This is not an ER, `Res(XOR)`, `R_mix341`, or arbitrary-SAT-algorithm theorem. Haken's abstract explicitly contrasts polynomial Extended-Resolution proofs. [Haken 1985](https://doi.org/10.1016/0304-3975(85)90144-6).

### Cook extended-Resolution upper bound

Cook defines fresh variables recursively using gates of the form

`q <-> a OR (b AND c)`.

The exact four defining CNF clauses are

`(q OR not a)`, `(q OR not b OR not c)`, `(not q OR a OR b)`, `(not q OR a OR c)`.

They are acyclic, total and functional: every valuation of earlier variables has one and only one value of `q`. Across the PHP recursion there are `Theta(h^3)` constant-width definition clauses/fresh names, and an ordinary Resolution refutation of the resulting extended source with `O(h^4)` lines. Hence `enc(G_h)=Theta(h^3 log h)` and the proof has polynomial serialized length and check time once all line payloads and identifiers are counted. [Cook 1976](https://doi.org/10.1145/1008335.1008338); the explicit `O(h^4)` account appears in [Grosof--Zhang--Heule 2022](https://www.cs.cmu.edu/~mheule/publications/PoS22-PHP.pdf).

No new hard family or lower-bound replay is used here. The certified Haken/Cook separation is the starting point.

## Lemma 1: total conservative extensions preserve original semantics

Let `F(X)=AND_i C_i` and let `D(X,Y)` use fresh auxiliary variables. Assume totality:

`for every x, there exists y with D(x,y)=1`.

Set `G=F AND D`. Then:

- `exists Y G(X,Y)=F(X)`;
- for every original-clause selector `s`,
  `SAT(D AND AND_{i:s_i=1} C_i) iff SAT(AND_{i:s_i=1} C_i)`; and
- if each `C_i` is copied literally, the original signed incidence hypergraph is a labelled induced source substructure.

If `D` is functional as well as total, each original witness lifts uniquely. Consequently every deletion witness for an original clause lifts uniquely, so original deletion essentiality is preserved.

Totality is load-bearing. A non-total condition can silently constrain `X` and change the projection or selector relation. Uniqueness is not needed for SAT preservation, but it is needed for bijective fibre/model-count claims.

## Theorem 2: retained signed incidence does not preserve Resolution hardness

Use Cook's complete acyclic definition bank `D_h`. The preceding lemma gives exact projection, unique fibres, original selector preservation and deletion-witness lifting. The original PHP signed hypergraph is present unchanged.

Cook's ER derivation becomes an ordinary Resolution derivation of `G_h` simply by treating every extension axiom as an initial source clause. Therefore `W_Res(G_h)=h^O(1)`. Haken gives `W_Res(P_h)=2^Omega(h)`.

This falsifies any candidate invariant that ignores or quotients away total definitions while claiming to polynomially track ordinary Resolution cost. Conversely, if it includes the entire definition syntax, it becomes representation-dependent and must handle alternate gate bases, aliases, circuits, GF(2), sharing and lazy encodings by proved polynomial cost domination.

The full selector profile over *all* clauses of `G_h` is not claimed equal to the PHP selector profile. The exact preserved object is the original-clause selector profile with the authenticated total definition bank retained. This qualification is essential.

## Corollary 3: exact missing transfer direction

For an extension map `E:F -> G`, preserving an `R` lower bound requires cost reflection:

`W_R(F) <= p(|F|+|G|+W_R(G))`

for one fixed polynomial `p`. A uniform compiler that translates every `G` proof into an `F` proof in polynomial time is stronger and sufficient.

The easy inequality

`W_R(G) <= W_R(F)`

when `G` retains all clauses of `F` points the wrong way: an `F` proof may ignore the new clauses, but a `G` proof may exploit them. Exact existential projection also supplies no proof compiler.

For Cook's family, no polynomial ordinary-Resolution backtranslation can exist. Applying it to the polynomial `G_h` proofs would produce polynomial `P_h` proofs, contradicting Haken. Any elimination that unfolds the shared definitions must incur superpolynomial overhead on some such proofs. That overhead is a failed transfer, not evidence of machine hardness.

## Raw-incidence inflation countercontrol

Even invariants that inspect the whole presented incidence graph can be manipulated without changing projected semantics. For any CNF `F(X)`, variable `x`, and connected graph `H`, introduce fresh aliases `y_v` and add

`Eq(y_r,x) AND AND_{uv in E(H)} Eq(y_u,y_v)`,

where `Eq(a,b)=(not a OR b) AND (a OR not b)`.

This extension is total, functional and parsimonious; all `y_v=x`. The new incidence graph contains a subdivision of `H`, so raw treewidth, cycle rank, degree, expansion and diameter can be inflated or altered by choosing `H`. Yet any proof of `F` remains legal and may ignore every alias clause:

`W_R(E_H(F))<=W_R(F)`.

On the established odd cubic Tseitin source, unchanged `/341` has exact cost `4h-1`; arbitrarily large alias networks do not increase this upper bound. This is a direct counterexample to treating raw signed-incidence expansion or size as universal computational work. An invariant may minimize away inessential aliases, but then it must pay for discovering/certifying the quotient and confront the Cook extension above.

## What survives: a restricted linear invariant

Let `mu(F)` be the minimum number of authenticated source clauses in an UNSAT subset. In any source-rooted proof grammar whose paid inference nodes have at most two antecedents, positive weight and sound conservative semantics,

`W_R(F)>=mu(F)-1`.

Indeed, the contradiction ancestry contains an UNSAT set of `s>=mu(F)` source leaves. After irrelevant nodes are pruned, its underlying graph is connected. If there are `q` inference nodes and `E` dependency edges, then `E>=s+q-1` while binary indegree gives `E<=2q`; hence `q>=s-1`.

This lower bound survives paid DEF, GF(2), shared DAGs, temporary growth, lazy storage and adaptive choices **inside fixed `R_mix341`**, because its rules retain authenticated at-most-two-parent ancestry. For connected simple bridgeless cubic odd Tseitin, every one of `4h` clauses is essential and `/341` attains the bound exactly:

`W_Rmix341(F_G,chi)=4h-1`.

This is meaningful representation robustness, but only relative to the fixed grammar and only linear: `mu(F)<=m<=O(N)`. It cannot provide a superpolynomial mixed lower bound. A free unbounded-premise macro or source-changing encoder destroys the argument.

## Semantic-certification support-width firewall

LSPV-1/384's elementary reduction was independently checked. For an explicit circuit `C(u)` and supplied affine sketch `L(u)`, deciding whether `C` factors through `L` is coNP-complete even when `L` is one fresh bit `y` and the proposed replacement bank is constant zero. Given CNF `D(x)`, use

`C_D(x,z,y)=z AND D(x)`, `L=y`.

The factor claim holds exactly when `D` is UNSAT. A polynomially bounded, sound, polynomial-time checkable certificate system for every positive arbitrary-support factor claim would imply `NP=coNP`. This is a certification-complexity barrier, not an unconditional time lower bound. General Boolean-circuit equivalence coNP-completeness is standard; see [Jordan 2013](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=913896).

The fixed `R_mix341` rule is narrower: `LOCAL-CONVERT` has constant original support, and `AND3` has at most three original variables. Exhaustive checking costs `O(8L)` for an explicit deterministic payload of length `L`. Therefore the growing-support coNP theorem does **not** apply to one legal `LOCAL-CONVERT`. If `L` is exponential, reading/checking/outputting it still has its real exponential physical cost; node weight one does not make the payload free.

## Fully charged resource ledger

| phase/representation | encoded work and peak space |
|---|---|
| strict source authentication | `Omega(N)` probes; conservative `O(N polylog N)` bit work; malformed header/index/EOF rejected |
| Cook definition source | `Theta(h^3)` clauses, `Theta(h^3 log h)` serialized bits/writes; polynomial construction |
| Cook proof | `O(h^4)` logical lines; identifiers, clause payloads, access, checking and output all separately polynomial |
| shared definitions | compact DAG names remain compact; tree unfolding may be exponential and cannot serve as a polynomial backtranslation |
| exponential intermediates | allowed; construction/read/write/check and retained peak charged at actual encoded length |
| alias networks | linear in the supplied graph `H`; exact projection does not force a proof to use them |
| arbitrary semantic quotient | compact output may be constant, while acquisition/certification is coNP-complete at growing support |
| legal constant-support conversion | `O(8L)` verification, with `L`-bit access/output and corresponding materialized or streaming costs |

An ideal paid-node count remains distinct from physical runtime. A SAT decider need not construct either the Cook proof or a backtranslation.

## Four falsifiers

1. **Exact projection plus original signed-incidence retention preserves proof hardness. — FALSE.** Cook/Haken gives exponential versus polynomial ordinary Resolution.
2. **Unique fibres and every original deletion witness repair the transfer. — FALSE.** Both survive Cook's total functional definitions.
3. **The forward proof-reuse inequality transfers a lower bound. — FALSE DIRECTION.** Hardness requires polynomial cost reflection from extended proofs back to original proofs.
4. **Arbitrary semantic quotient certification is a free local check. — FALSE generally, but not applicable to fixed three-variable `LOCAL-CONVERT`.** Growing-support factor certification is coNP-complete; constant support is exhaustively checkable.

## B1/B2/B3 classification

| obligation | ordinary Resolution | unchanged `R_mix341` |
|---|---|---|
| B1 | **FALSE** via one fixed canonical-PHP recognizer plus exhaustive fallback | **OPEN** |
| B2 | **OPEN**; family recognition has exponential global fallback | **OPEN** |
| B3 | Haken makes this equivalent to `SAT notin P`; **OPEN** | **OPEN** |

The conservative-extension theorem is not itself a B counterexample. It proves that a candidate representation transfer fails. PHP/Cook is a mandatory mixed-calculus escape, not a mixed-hard witness.

## Independent finite controls

The Python producer independently checked:

- all eight truth rows and both output values for Cook's four-clause gate;
- exact unique extension of every original assignment for PHP `h=1,2,3` under small acyclic total definition banks;
- projection preservation and every original-clause deletion witness after extension;
- all original selector masks for `h=1,2` with definitions retained;
- odd/even `K4` Tseitin labels `0/8` under path, star and complete alias networks;
- 276 rank-one factorization fixtures over full-width CNFs on one to three variables; and
- six malformed gate records.

It passed **9,984 assertions**. A separately written Node verifier passed **59 assertions** over the raw ledger and theorem/scope fields. These controls validate elementary semantics and accounting, not Haken's lower bound or Cook's full `O(h^4)` derivation.

Artifacts:

- `experiments/arc/lspv5_333/conservative_extension_invariant_firewall_referee333.py`
- `experiments/arc/lspv5_333/verify_conservative_extension_invariant_firewall_referee333.js`
- `results/raw/arc/lspv5_333/conservative_extension_invariant_firewall_referee333.json`

Pre-publication SHA-256: producer `3060d1c8...`, verifier `2656cf45...`, raw `a71f8b27...`.

## Project, Grok, Claude, literature and GitHub review

Issue #3 was read through 755 comments at the substantive audit. The direct predecessor is `research/agents/lspv-2/2026-11-03_2009_LSPV-2_TOTAL_EXTENSION_SPEEDUP378.md`, blob `e0d81d9d6f50d30172f056698e9e5260e1041c3b`; its Cook/Haken theorem is correct. REFEREE332 is `research/main/2026-11-04_0048_MAIN_SELECTOR-PROFILE-COST-NONIDENTIFIABILITY-REFEREE332.md`, blob `77dc3205697a7071b2266b3b885667bbea1c5a0c`. The support-width boundary is `research/agents/lspv-1/2026-11-04_0100_LSPV-1_AFFINE_SKETCH_SEMANTIC_CERTIFICATION384.md`, blob `a0c8cab07ae5538768596fc10b0523928091eb7a`, with grammar correction `research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md`, blob `bbcdad9a487203f160d1009235de6bec7322a2a2`. LSPV-2/384 supplies a finite 128-paid-node guarded-K4 definition proof, not an all-size minimum.

The authoritative fixed grammar was read at `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`.

Current Grok was located and read: `GROKPROOF/2026-11-04_1217_PROGRESS.md`, blob `cae0560d2e4f8c243da802c1d5d48ebf32bedd5c`. Its circuit-cut obstruction is restricted; it explicitly leaves the fully charged arbitrary-algorithm transformation OPEN.

The current Claude directory still has no post-October-28 review. Files read were `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` (`9a5b05d6...`), `2026-10-28_1452_CLAUDE_TPORT-0002.tex` (`1f9fc727...`) and `2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex` (`95c2649b...`). They concern restricted sequential, alternation-trading or portfolio settings and provide no proof backtranslation or B3 bridge.

Primary searches covered Haken's exact model, Cook's PHP extension construction and size, circuit equivalence, and cost-reflecting proof translations. Project GitHub search located the November 2 refocus and LSPV-2/378 by exact path; raw-incidence searches found earlier occurrence/select work but no stronger invariant. Separate `github.com/openai` queries for PHP ER proof compilers and conservative-extension backtranslations returned no applicable result. Absence is not novelty evidence.

## Exact next gap

The strongest surviving signed-source invariant is the linear `mu(F)-1` ancestry floor inside the unchanged positive-cost binary-premise grammar. To advance beyond it, one must either:

1. prove a superlinear invariant that survives every legal paid definition, GF(2), circuit, sharing and lazy representation in `R_mix341`; or
2. prove polynomial cost reflection for a declared representation class.

Exact projection, source retention, unique fibres and exponential-overhead backtranslation are now certified insufficient. The weakest sufficient B3 bridge

`SAT in P => Wbar_Rmix341(N)=N^O(1)`

remains OPEN, as does P versus NP.
