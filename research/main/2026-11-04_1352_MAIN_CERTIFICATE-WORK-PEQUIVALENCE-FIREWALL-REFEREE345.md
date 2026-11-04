# REFEREE345: certificate-work p-equivalence and the node-invariance firewall

**November 4, 2026, 13:52 PST — PNP Independent Proof Red Team.**

**Status.** **PROVED/EXACT:** the minimum fully encoded certificate-and-checking envelope is polynomially invariant under mutual uniform exact-target p-simulation. **PROVED/EXACT:** raw paid-node minima are not invariant, even under linear-bit mutual translations; this is the already-known REF334 `Pack` obstruction, independently rechecked rather than claimed as new. **PROVED/CONDITIONAL:** under `SAT in P`, polynomial worst-case encoded certificate work, p-boundedness, uniform exact shortest-bit search, and p-optimality coincide without a separate node-to-bit balance premise. **FALSIFIED:** semantic equivalence, equisatisfiability, or a compact XOR descriptor alone supplies this transfer. Application to fixed `R_mix341`, B1, B2, B3, unrestricted SAT hardness, and P versus NP remain **OPEN**. No rule, weight, task, schedule, state, identity, or ownership boundary changed.

## 1. IDEA before search

Replace raw paid-node count with a fully encoded certificate-work envelope and test whether it survives all polynomially intertranslatable proof representations.

Initial proposed lemma: if two fixed explicit proof systems uniformly p-simulate one another, preserving the exact authenticated source and paying construction, output and verification, then their minimum certificate work should be polynomially equivalent even though their minimum node counts may differ exponentially by batching.

Falsifiable attacks fixed before search:

1. one paid macro node hides an exponential proof payload;
2. compact GF(2) or circuit syntax is semantically equal to a dense table but expansion is exponential;
3. translators preserve only SAT/UNSAT, not the exact source formula;
4. a correct uniform decider emits only a label, not a proof;
5. a per-input or per-`N` translator is substituted for one fixed uniform translator.

## 2. SEARCH and revision

### Primary literature

Actual queries:

- `Cook Reckhow p-equivalence proof systems polynomial simulation encoded proof length primary paper`;
- `propositional proof systems p-equivalent reblocking proof length invariance p-simulation`;
- `proof complexity dense parity representation XOR succinct proof system simulation`;
- `Krajicek implicit proofs circuits exponentially long proof`;
- `Atserias Muller Automating Resolution shortest proof size`.

Sources read:

- Cook--Reckhow, *The Relative Efficiency of Propositional Proof Systems* (JSL 1979): proof strings are fully encoded bitstrings; p-simulation is a uniform polynomial-time same-conclusion translator; mutual p-simulation compares minimum proof length up to polynomial distortion.
- J. Krajicek, *The Cook--Reckhow Definition*, arXiv:1909.03691, and *Information in Propositional Proofs and Algorithmic Proof Search*, arXiv:2104.04711: short proof existence and proof search are distinct absent stronger assumptions.
- Atserias--Muller, *Automating Resolution is NP-Hard*, arXiv:1904.02991.
- Gocht--Nordstrom, *Certifying Parity Reasoning Efficiently Using Pseudo-Boolean Proofs* (AAAI 2021): compact extension/PB reasoning can certify XOR reasoning far more efficiently than standard proof logging, reinforcing the representation control.
- Haken, *The Intractability of Resolution* (TCS 39, 1985), DOI `10.1016/0304-3975(85)90144-6`.

Direct branded Google UI was unavailable. General web search was used; no Google-specific run is claimed.

### Project duplication and correction

Search found that `research/main/2026-11-04_0248_MAIN_NODE-BIT-NORMALIZATION-OPTIMAL-SYSTEM-FIREWALL-REFEREE334.md`, blob `1750c42dabcd72a7fef379a9f9fba001eceaea77`, already proves the `Pack(R)` counterexample and the node-to-bit normalization repair. Therefore raw node reblocking is not the new result here.

The increment is the explicit fully charged envelope theorem below, its source-recoding conditions, and its combination with REF344 to remove the balance premise when the target metric itself is encoded work.

Relevant current project work read:

- REF334 above;
- `research/main/2026-11-04_1251_MAIN_BALANCED-PMIN-POPTIMAL-COLLAPSE-REFEREE344.md`, blob `3b374229d39897941eb822aaf58d186a11888b80`;
- `research/agents/lspv-3/2026-11-04_1327_LSPV-3_ORIGINAL_SUPPORT_TRANSPORT_FIREWALL402.tex`, blob `4b301395...`: after source retraction, a copied AND3 step can become type-illegal because its retyped condition depends essentially on four original variables;
- current issue #3 through LSPV-1/399 and LSPV-4/395.

### OpenAI GitHub, Grok, Claude

OpenAI GitHub queries `proof certificate verifier CNF resolution`, `Cook Reckhow p-simulation proof system`, `proof certificate DAG verifier`, and `XOR SAT proof checker certificate` returned no applicable compiler. The relevant file actually read was `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean`, blob `1ced21f44ad49370d1b812e862c03c3a91d7f836`: it correctly ties a concrete execution trace to instruction and stack-bit upper bounds, but is not a Cook--Reckhow translator into `R_mix341`.

Current Grok was located rather than guessed: `GROKPROOF/2026-11-04_2113_PROGRESS.md`, blob `a5bba58dc9607a7bbe0e6a1509e87852ce97e45a`. It leaves the universal fully charged all-input transformation OPEN. Its statement that `Omega(N^1.1)` “already exceeds” an `N^(1.1+o(1))` budget is not a strict exponent contradiction; LSPV-1/399 correctly records equality at the boundary and distinguishes explicit from virtual query construction. This material objection does not affect the theorem below.

Claude has no later assessment than October 28. Exact files read/rechecked were:

- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`;
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`.

They concern restricted alternation-trading portfolios and sequential-access lower bounds, not certificate p-equivalence or B3.

## 3. Established hard-family anchor: exact scope

Let `PHP_(h+1)^h` be the explicit unary pigeonhole CNF with variables `x_(i,j)`, pigeon clauses `OR_j x_(i,j)`, and collision clauses `(not x_(i,j) OR not x_(k,j))`. It has `h(h+1)` variables and `(h+1)+h*binom(h+1,2)` clauses. Explicit signed binary-index DIMACS length is `N_h=Theta(h^3 log h)`.

Haken's theorem used here is:

> There are constants `c>0,h0` such that for every `h>=h0` and every ordinary unrestricted shared-DAG Resolution refutation of the explicit unary `PHP_(h+1)^h`, the refutation has at least `2^(c h)` lines.

The proof quantifier permits arbitrary legal Resolution pivots, widths and DAG sharing. It excludes extension variables, Extended Resolution, GF(2), `Res(oplus)`, circuits, semantic inference, `R_mix341`, and arbitrary SAT algorithms. The input-length form is `2^Omega((N_h/log N_h)^(1/3))` for this family and proof system.

Cook's polynomial Extended-Resolution PHP proofs are the mandatory compact-representation escape. Haken is therefore a proof-system anchor, not unrestricted machine hardness.

## 4. ITERATE: exact certificate-work invariant

Fix one canonical explicit CNF encoding. A target-exposing proof relation `P(F,pi)` has one total deterministic verifier `V_P` running in time polynomial in `|F|+|pi|` and rejecting malformed sources and certificates.

Define

`CE_P(F) = min_pi [ |F| + |pi| + T_VP(F,pi) + S_VP(F,pi) ]`

over accepted proofs, and infinity on SAT or malformed inputs. `S_VP` is peak writable verification space in a fixed standard model. Because `S<=T` and `V_P` is polynomial-time,

`|F|+L_P(F) <= CE_P(F) <= poly(|F|+L_P(F))`,

where `L_P(F)` is the minimum encoded proof length.

### Theorem 1: one-way exact-source domination

Suppose one fixed total uniform translator `tau_(P->Q)` satisfies, for every accepted `P(F,pi)`:

1. `Q(F,tau(F,pi))` accepts the **same explicit F**;
2. translator runtime and output length are at most `p(|F|+|pi|)` for one fixed polynomial `p`;
3. all source parsing, auxiliary renaming, payload construction, output and checking are ordinary machine operations.

Then one fixed polynomial `r` satisfies

`CE_Q(F) <= r(CE_P(F))`

for every valid UNSAT `F`.

Proof: choose a `CE_P`-minimizing proof. Its source-plus-proof length is at most `CE_P(F)`. Translation time/output are polynomial in that quantity, and the fixed `Q` verifier is polynomial in its explicit input. Add the charged terms.

For cutoff envelopes,

`CEbar_Q(N) <= r(CEbar_P(N))`.

Mutual exact-source p-simulation gives polynomial domination both ways. Thus polynomial versus superpolynomial worst-case encoded certificate work is invariant inside a declared p-equivalence class.

The quantifier order is

`exists fixed translator, exists fixed polynomial, for every F, for every valid supplied proof`.

It is not `for every F exists a tailored translator`, per-`N` advice, or a free optimal representation selector.

### Source recoding

For a syntactic representation map `e:F->G`, the theorem initially gives only

`CE_Q(e(F)) <= poly(CE_P(F))`.

Full cutoff equivalence requires polynomial length bounds in both directions, exact authenticated image membership, and a polynomial byte-exact retraction `d(e(F))=F` (or an equivalent proof wrapper). Equisatisfiability, the same projected boundary relation, or a semantic existential projection is not p-simulation.

Auxiliary variables must be fresh and injectively renamed, definitions conservative and paid, source leaves authenticated byte-for-byte, and shared DAG structure either preserved or every duplicated byte/work charged.

## 5. Raw paid nodes fail; encoded work survives

REF334's generic construction remains decisive. Given any explicit system `P`, `Pack(P)` uses one paid outer record containing a complete serialized `P` proof and replays it. Wrap/unwrap are linear-time, linear-output same-source translators. Hence `P` and `Pack(P)` are p-equivalent in encoded proof work, but

`W_Pack(P)(F)=1`

for every UNSAT `F`.

With `P=Resolution` and Haken's family, raw nodes change from `2^Omega(h)` to one. No evidence disappears: certificate bytes, construction, access, output and replay remain exponential. Therefore an ideal signed-hypergraph/DAG paid-node count is not representation-independent if arbitrary payload-bearing batching is allowed.

The exact restricted repair is also REF334's: require a global polynomial minimum-node-to-bit normal form, a uniform polynomial-output exact-source compiler, and at least one serialized bit per target paid node. Then node minima transfer polynomially. Without those hypotheses, an exponential backtranslation proves nothing about machine hardness.

## 6. Conditional collapse for the encoded invariant

Let

`Lbar_P(N)=max_{valid UNSAT |F|<=N} L_P(F)`.

Under `SAT in P` and one fixed polynomial-time verifier, no separate node-to-bit balance is needed for the encoded metric:

`Lbar_P polynomial`

iff `P` is p-bounded in standard encoded length

iff one uniform polynomial-time total algorithm returns an exact shortest-bit `P` proof on UNSAT inputs, a checked model on SAT inputs, and rejects malformed strings

iff `P` is p-optimal among target-exposing explicit-CNF proof systems.

The exact-search implication asks the NP predicate “there exists an accepted proof of at most `q` bits extending prefix `u`,” binary-searches the least feasible length, and self-reduces a canonical padded encoding. Conversely, polynomial-time output is polynomial length. Exact search p-simulates every source system by authenticating its conclusion and generating a fresh target proof. The p-optimal converse uses the decider-induced target-exposing proof system.

Since `CE` and `|F|+L` are polynomially equivalent, the same polynomial-envelope collapse holds for `CE`.

This is a representation-robust **certificate** invariant. It still does not charge discovery of a proof from `F` unless the conditional search theorem is invoked, and it does not cover a correct algorithm that outputs only SAT/UNSAT. Converting a rejecting trace into sound UNSAT evidence requires an all-input correctness premise and a uniform exact-source compiler—B1/B3's missing transfer.

## 7. Compact alternatives and physical costs

### XOR versus dense tables

The parity relation on `k` bits has an `O(k)` GF(2) row but a `2^k`-bit characteristic table. The two representations are semantically identical. Dense-to-XOR recognition may be polynomial in the already dense input; XOR-to-dense materialization needs `Omega(2^k)` output. Therefore they are not mutually polynomially intertranslatable in the compact input length. Dense-table contraction hardness cannot cross this firewall.

### Fully charged supplied-proof translation

For valid `(F,pi)`, let `m=|pi|` and target output length `ell`. A conservative pipeline is

`T_full <= T_parse + V_P(N+m) + T_tau(N+m) + V_Q(N+ell)`,

with `ell<=T_tau` and output time `Omega(ell)`. Materialized peak space includes the translator state, target bytes and verifier state. Streaming may avoid retaining all `ell` bits only with an actual compatible one-pass consumer; otherwise bytes must be stored, reread or recomputed, each with paid access/update work.

Generic p-simulation preserves only a polynomial total-work class. It does not preserve exact exponents, a low-space schedule, an FLMV profile, proof discovery, or arbitrary-decider runtime.

## 8. Exact finite controls

Producer:
`experiments/arc/lspv5_345/certificate_work_invariance_referee345.py`

Independent verifier:
`experiments/arc/lspv5_345/verify_certificate_work_invariance_referee345.js`

Raw:
`results/raw/arc/2026-11-04_1352_LSPV5_345_CERTIFICATE_WORK_INVARIANCE.json`

For `n=1..16`, the source is declared-`n` CNF `(x1) AND (not x1)`, with a SAT sibling `(x1) AND (x1)`. The two proof encodings contain the same explicit truth-table rows:

- UNPACKED charges one paid row per assignment: `2^n` nodes;
- PACKED charges one outer node;
- tag-only translation is linear time and identical output length;
- encoded certificate work is exactly equal;
- all 32 SAT sibling proofs and 64 malformed/corrupt proofs were rejected;
- at `n=16`, nodes are `65,536` versus `1`, while each explicit proof is `9,961,512` bits;
- the parity control records `18` compact descriptor bits versus `65,536` dense bits at `n=16`.

The independent Node verifier passed 133 checks.

SHA-256:

- Python: `b0058a6483e4991b55229b081cb0649a75f161badcd62a88e80225cae649a36c`;
- Node: `e53cbdae69f1780f9f9aacc3db885004b20f736ee5e0136d719fbded5498b554`;
- raw JSON: `bf620b1dfe468467c20cf33b83e12934269eda981ce1b74fcd154f33a0ddacc5`.

These finite controls test encoding, translation, both labels, malformed rejection and physical ledgers; they do not prove asymptotic Resolution hardness.

## 9. `R_mix341` and B ledger

| Claim | Status |
|---|---|
| Haken explicit unary PHP lower bound | KNOWN; ordinary shared-DAG Resolution only |
| Raw paid-node invariance under p-equivalence | FALSIFIED; REF334 `Pack` |
| Encoded certificate-work invariance under mutual exact-source p-simulation | PROVED/EXACT |
| Semantic relation equality implies certificate invariance | FALSIFIED |
| SAT-in-P encoded-work/p-optimal collapse | PROVED/CONDITIONAL |
| Full `R_mix341` polynomial verifier and node/bit balance | OPEN, especially `LOCAL-CONVERT` exports |
| Full evaluator-source replay of every mixed rule | OPEN; LSPV-3/402 gives an AND3 typing obstruction |
| B1, B2, B3 for fixed `R_mix341` | OPEN |
| Superpolynomial `Wbar_Rmix341` | OPEN |
| Unrestricted SAT hardness / P versus NP | OPEN |

The surviving invariant is meaningful but deliberately narrower than the original ambition: it is independent of all **polynomially intertranslatable exact-source certificate representations**, not of arbitrary sound representations or arbitrary correct algorithms. Extending it to those algorithms requires precisely the uniform trace-to-proof/source-authenticated bridge that remains B1/B3.

The next decisive obligation is to settle the complete `R_mix341` grammar and node-to-bit normalization, repair the typed AND3/LOCAL-CONVERT source replay for every legal rule, and then attempt a uniform polynomial exact-source compiler from the decider-induced proof system. No new hard formula is required.
