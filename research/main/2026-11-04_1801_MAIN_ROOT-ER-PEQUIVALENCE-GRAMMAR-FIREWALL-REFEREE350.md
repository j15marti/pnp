# REFEREE350 — root/ER p-equivalence and native-grammar firewall

**PNP Independent Proof Red Team | November 4, 2026, 18:01 PST**  
**Status:** PROVED/EXACT conditional p-equivalence for the explicitly completed root-only grammar `R_root341`; PROVED that the original `/341` prose does not uniquely determine root-only versus exported-wire payload semantics; PROVED conditional equivalence of B3 for `R_root341` with `SAT in P => Extended Resolution is p-bounded`; COMPUTATIONAL finite controls. No rule or weight of fixed `R_mix341` was changed. Full unconditional native normalization, B1/B2/B3, superpolynomial `Wbar`, unrestricted SAT hardness and P versus NP remain OPEN.

## IDEA before search

Test whether the strict root-only completion of `R_mix341` is polynomially equivalent, at fully encoded exact-source certificate level, to fan-in-two Extended Resolution (ER).

Assumptions registered before searching:

1. `LOCAL-CONVERT` has a fixed constant-size support list and exports one root condition only;
2. GF(2) rows explicitly encode their coefficient masks and right-hand sides;
3. every reusable auxiliary wire is a separately paid, globally fresh, conservative two-input `DEF`;
4. every derived record has at most two parent identifiers and unit logical weight.

Falsifiable prediction: every native rule has a uniform polynomial ER macro and every fan-in-two ER proof maps back by `DEF+RES`. A rule requiring an unbounded semantic implication, a public uncharged internal wire, or an implicit exponential row would falsify the theorem. If the theorem survived, B3 would become the still-missing question whether `SAT in P` makes this same ER-equivalent system p-bounded; machine runtime alone would not answer it.

## SEARCH

### Governing project, issue and peers

Read the governing `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`, current issue #3 through comments LSPV-4/399 and REFEREE349, and the authoritative original

`research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`

(blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`). The original says that a `LOCAL-CONVERT` node derives “a clause or bounded-support Boolean circuit condition” after a constant-support truth-table check. It does not give a parser for the circuit payload, say whether internal gate identifiers are public, or state whether internal gates are separately paid. By contrast, `DEF` explicitly introduces one fresh reusable gate and charges its node.

Relevant peer evidence:

- `research/agents/lspv-3/2026-11-04_1724_LSPV-3_PORT_COHERENCE_GRAMMAR406.md` (blob read from main): fresh definitions are model-bijective, but the native exported-port syntax is incomplete.
- Issue #3 comment `6647421855`, LSPV-4/399: under a separately declared permissive `R_chain`, arbitrarily long circuit payloads can live in one paid node, separating logical-node count from validation work. The linked role file was not present at the guessed default-branch path during this run, so only the actual issue comment was used; no inaccessible report was claimed read.
- `research/main/2026-11-04_1748_MAIN_NATIVE-ROOT-NORMALIZATION-TRACE-B3-FIREWALL-REFEREE349.md`: the root-only reading yields polynomial typed serialization, but does not prove evaluator-to-source retraction or B3.
- REFEREE342/343: one transparent indexed evaluator has polynomial source retraction; short same-system reflection remains equivalent to the target worst-case bound.

Actual Grok and Claude files read:

- `GROKPROOF/2026-11-04_2315_PROGRESS.md` (white-box residual extraction remains open);
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`;
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`.

None proves native grammar completion, ER reflection shortness or B3.

### Primary literature and general web

Actual queries:

1. `Extended Resolution polynomially equivalent Extended Frege proof systems primary source PDF`;
2. `Soltys Extended Frege Gaussian elimination polynomial proofs PDF`;
3. `SAT in P implies Extended Frege polynomially bounded reflection proof complexity open problem primary`;
4. `Res XOR Tseitin polynomial refutation Gaussian elimination proof complexity primary paper`.

Read rather than relying on snippets:

- J. Krajíček, *Propositional Proof Complexity I*, lines 1340–1403: extension atoms, ER/EF p-equivalence, and polynomial EF proofs of PHP. <https://www.karlin.mff.cuni.cz/~krajicek/ds1.pdf>
- E. Hirsch, *Boolean Satisfiability, Lecture 9*, Theorem 4: ER polynomially simulates EF through Tseitin variables and Resolution macros. <https://edwardahirsch.github.io/edwardahirsch/archive/students/sat/lecture9.pdf>
- M. Soltys, *Extended Frege and Gaussian Elimination* (2002): uniform polynomial EF proofs of Gaussian-elimination correctness. <https://www.researchgate.net/publication/246150913_Extended_Frege_and_Gaussian_elimination>
- E. Khaniki, ECCC TR20-034: lower bounds for `Res(PC)`/`Res(oplus)` are explicitly proof-system and field/model restricted. <https://eccc.weizmann.ac.il/report/2020/034/>

Direct Google-branded UI was unavailable. The available general-web search was used and this limitation is recorded; no direct Google session is claimed.

### GitHub, including OpenAI

Actual authenticated queries included:

- project: `MIXED_TSEITIN_MIN_DAG341`, `R_chain LOCAL-CONVERT 399`, `Extended Resolution Gaussian elimination XOR`, `R_mix341 Extended Resolution p-simulation`;
- OpenAI: `ImplementationCertificates`, `Gaussian elimination proof certificate`.

The only directly relevant OpenAI result was `openai/math/lean/OAI/Algorithms/SubexponentialSAT/RuntimeAssembly.lean`, which explicitly labels `ImplementationCertificates` as open obligations, not a theorem. No OpenAI repository supplied the required proof compiler or reflection theorem.

## ITERATE I: the search forces a grammar correction

REFEREE349's strict root-only reading is a coherent completion, but the original prose does not force it. Two parsers satisfy all words actually present:

- **Root parser `R_root341`:** a record has one public root relation on at most the fixed `c_R` support; a supplied circuit is private checking evidence and can be replaced by its constant truth table. Internal gates have no public identifiers.
- **Export parser `R_export341`:** a record carries a gate list and makes some internal identifiers available to later nodes, while the record still has unit logical cost.

The original file neither authorizes nor forbids the latter exports. These are not the same proof system. With three original inputs, the root parser has only 256 possible root relations and a constant canonical record. In the export parser, one paid record can contain `m` distinct gate records and therefore at least `Omega(m)` encoded bits and verification reads. If public wires are reusable without paid `DEF`, translating that single logical node into ordinary ER requires `Omega(m)` extension evidence. Thus a polynomial bound in `N+q` fails as `m` grows while `q=1`.

This is an explicit grammar countermodel, not an `R_mix341` refutation and not a P-versus-NP result. It proves that a full unconditional theorem cannot be attributed to the original natural-language rule list until the parser/export/pay boundary is fixed. No rule was amended here.

The smallest semantic safety witness remains source `(x)` with private circuit

`g0=x; g1=NOT g0; g2=NOT g1`.

The public root `g2=x` is implied by the source. Private `g1=NOT x` is not. Consuming `g1` as an asserted true condition would create the false contradiction `x, NOT x`. A separately paid conservative definition of `g1` is safe because it asserts only the relation `g1 <-> NOT x`, not the unit `g1`.

## ITERATE II: exact theorem for the root-only completion

### Theorem 1 — exact-source p-equivalence

Let `R_root341` be the root parser above, with explicit coefficient masks and fan-in-two paid `DEF`. Let `ER_2` be Extended Resolution whose extension axioms are normalized to fresh fan-in-two Boolean gates. Then `R_root341` and `ER_2` mutually p-simulate one another while preserving the exact original CNF source.

#### `R_root341 -> ER_2`

Process a topologically ordered mixed DAG.

1. Source clauses and RES records are copied.
2. A paid `DEF` becomes the corresponding ER extension axiom; its constant number of defining clauses has constant overhead.
3. An AND3/root-local condition is replaced by its canonical truth table on at most `c_R` inputs. A constant-size fan-in-two circuit and Tseitin clauses define a root variable; the parents' asserted roots derive its unit by a constant ER macro.
4. A GF(2) row on `V` available variables is represented by a balanced or prefix XOR circuit of `O(V)` fresh gates and a unit asserting the requested parity. For a native XOR inference, the two parent equations logically imply their row sum. Soltys supplies uniform polynomial EF proofs of Gaussian-elimination row operations; ER p-simulates those EF proofs. Hence each row-addition macro has `poly(V)` encoded size and is uniformly constructible.
5. `LOCAL-CONVERT` is a fixed-support truth-table implication. Replace its payload by the canonical root table and use the constant ER implication macro. No internal payload identifier survives.

After `q` paid nodes there are at most `V <= n_0+q` named variables. The complete ER output has `(N+q)^{O(1)}` bits and is constructed, serialized and checked in polynomial time and peak space. Every proof/source bit read and every output bit written is charged.

#### `ER_2 -> R_root341`

Normalize each ER extension to a fresh fan-in-two gate. Emit one paid native `DEF` for it. Every ER Resolution step is one native RES step. The defining views of an extension are the relations already attributed to its paid DEF. Thus an encoded ER proof of length `s` gives a same-source native proof with `O(s)` paid nodes and polynomial construction/checking/output work.

This proves mutual p-simulation. It does not translate an arbitrary semantically correct evaluator's axioms back to the original CNF; REFEREE340's poisoned evaluator remains a counterexample. It translates proofs that already have the same authentic source.

### Corollary 2 — B3 is the ER/EF short-reflection question

Under `R_root341`, node-to-bit normalization and the p-equivalence above give

`Wbar_Rroot341 is polynomial  <=>  ER is polynomially bounded`

up to polynomial source-length rescaling. Consequently

`SAT in P => Wbar_Rroot341 polynomial`

is equivalent to

`SAT in P => ER (equivalently EF) is polynomially bounded`.

`SAT in P` implies `NP=coNP`, so Cook–Reckhow yields existence of some polynomially bounded proof system. It does not say that the preselected ER-equivalent system p-simulates that system. Supplying that p-simulation or polynomial ER reflection proofs for the chosen decider is exactly the missing step. Assuming it would presuppose the polynomial certificates B3 is meant to derive.

Thus this run neither proves nor refutes B3. It proves that the strict grammar does not offer a shortcut around the recognized ER/EF reflection obstacle. A non-reflection proof of the implication could still exist.

## Established-hard-family controls

Haken's theorem remains exact and restricted: for sufficiently large `h`, every ordinary shared-DAG Resolution refutation of the explicit unary `PHP_(h+1)^h` CNF has `2^{Omega(h)}` lines. It excludes extensions, GF(2), AND3 and LOCAL-CONVERT. Krajíček records polynomial EF/ER PHP proofs, so PHP cannot lower-bound `R_root341` through the p-equivalence above.

Odd Tseitin is likewise a mandatory escape: native AND3 extraction plus GF(2) row addition gives the already certified linear mixed refutation, while ordinary Resolution can be exponential. Khaniki's `Res(oplus)` lower bounds use their exact algebraic proof model and do not become arbitrary-machine bounds.

## Computational controls and physical costs

Producer:

`experiments/arc/lspv5_350/root_er_equivalence_referee350.py`

Independent verifier:

`experiments/arc/lspv5_350/verify_root_er_equivalence_referee350.js`

Raw:

`results/raw/arc/2026-11-04_1801_LSPV5_350_ROOT_ER_EQUIVALENCE.json`

The producer passed **1,789,628** assertions: all 16 two-input Boolean definitions; all truth-table pairs on supports 0–3; every affine equation pair and assignment through six variables; root/export parser separation through 1,024 internal gates; the private-wire witness; and eight malformed controls. The independently written JavaScript verifier passed **5,605** checks. Raw SHA-256:

`b35fb39d8e25cd3f0afcfa264ec6e532ecd5d71e49a45bdfbfbd04f776dd4c1d`.

Finite enumeration corroborates the displayed local semantics, not the asymptotic p-simulation or any lower bound.

Physical accounting is separate from unit logical nodes. For the root grammar, the normalized proof has polynomial intermediate length, construction, bit access, checking, output and peak space. For a permissive payload, reading and validating `m` gates costs `Omega(m)` regardless of the one-node logical charge. Exponential payloads are allowed but charged at their real encoded length; compact root truth tables are checked as the alternative. No logical-node count is reported as machine runtime.

## Precise status

- **PROVED/EXACT, conditional grammar:** `R_root341` and fan-in-two ER are exact-source p-equivalent with fully polynomial encoded translation.
- **PROVED grammar firewall:** the original `/341` prose does not uniquely choose root-only versus exported-wire syntax; therefore the conditional theorem cannot yet be promoted to the unqualified native calculus.
- **PROVED minimal semantic counterexample:** an implied circuit root does not make a private internal wire an asserted consequence.
- **PROVED characterization:** B3 for `R_root341` is the conditional ER/EF polynomial-boundedness problem.
- **COMPUTATIONAL:** 1,789,628 producer and 5,605 independent checks.
- **OPEN:** authoritative parser/export/pay grammar; unconditional full native translation; short ER/`R_mix341` reflection from `SAT in P`; B1/B2/B3; superpolynomial mixed minimum; unrestricted SAT hardness; P versus NP.

## Next unresolved step

Without changing weights, freeze one machine-readable native record grammar. If root-only is confirmed, formalize the GF(2)-to-ER compiler and its inverse at byte level, then attack short reflection for the fixed transparent family. If public internal exports are confirmed, charge each exported gate or prove a polynomial bound on exports per paid node; otherwise `N+q` node-to-bit normalization is false.
