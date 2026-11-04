# NODE-BIT-NORMALIZATION-OPTIMAL-SYSTEM-FIREWALL-REFEREE334

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 4, 2026, 02:48 PST**

**Status:** PROVED/EXACT representation counterexample separating serialized-proof p-equivalence from paid-node cost; PROVED/EXACT node-to-bit normalization transfer lemma; PROVED/EXACT computation-trace characterization of B1; PROVED/RESTRICTED normalization audit for the literal private-wire reading of fixed `R_mix341`; COMPUTATIONAL independent controls. No superpolynomial `R_mix341` bound, B1/B2/B3 bridge, unrestricted SAT lower bound, or P-versus-NP conclusion is proved. Fixed calculus, five roles, states and schedules are unchanged.

## Outcome first

Polynomial backtranslation is still insufficient when the source cost counts ideal nodes but permits a node to hide an arbitrarily long explicit payload.

For any sound complete explicit refutation system `R`, define `Pack(R)`: one paid `PACK` node contains a full serialized `R` proof, and its verifier parses and replays that payload. Wrapping and unwrapping are linear-time, linear-bit translations, so `R` and `Pack(R)` are exactly p-equivalent as Cook--Reckhow encoded proof systems. Nevertheless,

`W_Pack(R)(F)=1`

for every UNSAT `F`, regardless of `W_R(F)`.

Taking `R` as ordinary Resolution and `F=P_h=PHP(h+1,h)`, Haken gives

`W_Res(P_h)=2^Omega(h)`, while `W_Pack(Res)(P_h)=1`.

The packed payload, construction, output and replay remain exponentially long. Thus this is a node-reblocking separation, not a computational shortcut and not machine hardness.

The exact repair is a node-to-bit normalization bound. If every `q`-node source proof has an equivalent proof of `poly(N+q)` encoded bits and an explicit-proof compiler emits a target proof of polynomial bit length, then target node cost is polynomial in `N+q`. Without normalization, even a linear backtranslation fails to reflect node cost.

This is the substantive advance beyond REFEREE317: Cook--Reckhow simulation controls encoded proof length, not the project's unit-paid node metric.

## Established lower-bound anchor: exact scope

Let `P_h=PHP(h+1,h)` be the standard unary pigeonhole CNF with `h(h+1)` variables and

`m_h=(h+1)+h*binom(h+1,2)=Theta(h^3)`

clauses. Under explicit signed binary-index/DIMACS encoding,

`N_h=Theta(h^3 log(h+2))`.

Haken's theorem has the quantifiers

`there exist c>0,h0 such that for every h>=h0 and every ordinary unrestricted shared-DAG Resolution refutation pi of P_h, |pi|>=2^(c h)`.

Source clauses are axioms; derived lines are ordinary resolvents; pivots, widths and DAG sharing are unrestricted. This is not a lower bound for Extended Resolution, `Res(XOR)`, `R_mix341`, `Pack(Res)`, or arbitrary SAT algorithms. Cook's polynomial extension proofs and the fixed mixed rules are mandatory compact-representation countercontrols.

## Theorem 1: linear proof-bit p-equivalence does not preserve node cost

Let `R` be any sound complete proof system whose explicit proofs are finite bitstrings and whose verifier is polynomial in the statement-plus-proof length. Define `Pack(R)` by:

1. one paid outer record `PACK(payload)`;
2. `payload` is a serialized `R` proof of the same statement; and
3. the verifier accepts exactly when the ordinary `R` verifier accepts `payload`.

Then:

- `Pack(R)` is one fixed uniform sound complete proof system;
- `pi -> PACK(pi)` and `PACK(pi) -> pi` take linear bit time and have linear output size;
- minimum serialized proof lengths in the two systems are polynomially equivalent; but
- `W_Pack(R)(F)=1` for every UNSAT `F`.

The outer node is not a free SAT oracle. It contains all evidence and replays it. Its defect is only that the declared node weight ignores the payload length and replay work.

On Haken PHP this yields the certified asymptotic separation above. One fixed system handles the entire growing family; there is no per-input advice or per-`N` optimizer.

## Theorem 2: exact normalization-transfer repair

Let `S,R` be fixed sound proof systems with paid-node costs. Assume:

1. **Node-to-bit normalization.** There are fixed polynomials `a,b` such that
   `W_S(F)<=q` implies the existence of an `S` proof of `F` with at most `a(N+q)` paid nodes and at most `b(N+q)` encoded bits.
2. **Explicit-proof compiler.** A uniform compiler maps every such `S` proof `pi` to an `R` proof having at most `p(N+|pi|)` output bits, for one fixed polynomial `p`.
3. Every paid `R` node occupies at least one output bit.

Then

`W_R(F) <= p(N+b(N+W_S(F))) = poly(N+W_S(F))`.

Proof: choose a minimum-node `S` proof, normalize it, compile it, and bound target nodes by target output bits. If normalization is only existential, the conclusion is only an after-the-fact logical minimum. If normalization and compilation are effective with polynomial construction/checking bounds, they also give a fully charged implementable proof translator.

`Pack(R)` proves hypothesis 1 indispensable: a one-node proof may have an arbitrarily or exponentially long payload even though its backtranslation is linear in that payload.

Consequently, mutual p-simulation plus polynomial node-to-bit normalization on both sides makes node-cost B1/B2/B3 invariant within that declared representation class. Mutual p-simulation alone preserves encoded proof length, not arbitrary reblockings of logical nodes.

## Theorem 3: computation traces isolate the algorithmic transfer

Fix the explicit all-string CNF grammar and a fixed total deterministic correct SAT decider `A`, including malformed-input rejection. Let `Q_A` be the refutation system whose canonical proof of an UNSAT `F` is the complete rejecting computation trace of `A(F)`.

On a standard multitape normalization with full configurations, if `N=|F|`, runtime is `T_A(F)`, and trace length is `L_A(F)`, then for a constant depending only on `A`,

`N+T_A(F) <= L_A(F) <= C_A*(N+T_A(F))^2`.

Transition-by-transition verification is polynomial in `L_A(F)`. Replay proves only what `A` did; soundness relies on the external universal premise that `A` is correct on every SAT, UNSAT and malformed input.

Define weak minimum simulation by

`Q_A <=_w R iff there exists p_A for every UNSAT F: W_R(F)<=p_A(L_A(F))`.

Then B1 for `R` is equivalent, up to this fixed quadratic trace normalization, to weakly simulating `Q_A` for every total correct `A`. The analogous worst-case trace envelope characterizes B2. Under `SAT in P`, weak simulation of one polynomial-time trace system is equivalent to B3.

Thus a representation-inclusive theorem covering every sound uniform algorithmic trace does not bypass B1/B3; it restates the missing bridge. A length-optimal proof system would suffice for the existential minimum, while a p-optimal system would additionally supply uniform proof translation. Existence of optimal and p-optimal propositional proof systems is a major open proof-complexity question.

## Application to fixed `R_mix341`

The authoritative grammar is

`research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`,

blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. Every paid node has at most two parents. Rules are unrestricted-width RES, constant-original-support AND3, explicit GF(2) XOR rows, LOCAL-CONVERT from one already-derived constant-support condition, and one fresh two-input conservative DEF gate.

Under the literal **private-wire** reading—only the converted condition's node ID is reusable, while every reusable internal gate must be a separately paid DEF—every `q`-node proof can be normalized to `poly(N+q)` bits:

- clauses use variables among the original and at most `q` fresh names;
- XOR rows are bit masks over that same polynomial name set;
- AND3/local semantics have canonical constant-support truth tables;
- DEF has one fixed two-input gate opcode; and
- parent and node identifiers use logarithmic-length indices.

A coarse bound `O((N+q)^3)` bits is sufficient. This excludes the `PACK` defect inside that literal grammar.

The qualification is essential. If a LOCAL-CONVERT circuit payload may export arbitrarily many named internal wires for later use without paid DEF nodes, the normalization proof fails. The original text says “bounded-support Boolean circuit condition” but does not separately formalize exported internal-wire semantics. That is the exact grammar obligation, also identified by LSPV-1/385. Even after normalization is secured, no trace-to-`R_mix341` simulation, B1, B2 or B3 follows.

## Fully charged resource ledger

| object or phase | logical nodes | encoded/physical charge |
|---|---:|---|
| ordinary Resolution proof `pi` | number of resolvents | all clause payloads, IDs, access and replay |
| `PACK(pi)` | 1 | `Theta(|pi|)` payload; `Omega(|pi|)` output/access; polynomial replay |
| full computation trace | trace records | `Theta(L_A)` construction/output; polynomial checking |
| normalized `q`-node `/341` proof | `poly(N+q)` | conditionally `O((N+q)^3)` bits under private-wire reading |
| explicit intermediate of `M` bits | representation-dependent | `Omega(M)` construction/output; `M` peak only if materialized |
| lazy descriptor | descriptor nodes/bits | generator, each bit query, recomputation and equivalence certificate charged |

Exponential output forces exponential time but not automatically exponential writable space: streaming or recomputation may lower peak space while preserving output/access work. An exponential backtranslation remains a failed transfer, not a SAT-machine lower bound.

## Four falsifiers

1. **Mutual polynomial proof translations preserve paid-node minima. — FALSE.** `R` and `Pack(R)` are linearly bit-equivalent but have arbitrary node separation.
2. **One paid node means constant physical work. — FALSE.** The explicit payload must be constructed, accessed, output and replayed.
3. **A valid rejecting trace establishes UNSAT without an all-input correctness premise. — FALSE.** A wrong machine has perfectly replayable rejecting traces on SAT inputs.
4. **A universal representation tagger automatically gives the missing bridge. — FALSE/OPEN FRONTIER.** Covering every sound system constructively is p-optimality-level; covering every correct decider trace weakly is B1 itself.

## B1/B2/B3 classification

| system/claim | B1 | B2 | B3 |
|---|---|---|---|
| ordinary Resolution | FALSE via one fixed canonical-PHP recognizer plus exhaustive fallback | OPEN | equivalent here to the open `SAT notin P` statement |
| `Pack(Res)`, node metric | trivially small but physically undercharged | trivially small | trivially small |
| unchanged `R_mix341` | OPEN | OPEN | OPEN |
| normalized mutual-p-simulation class | invariant within the class | invariant within the class | invariant within the class |

The `Pack` row is not evidence that SAT is easy. Its one node contains the whole proof.

## Independent finite controls

The Python producer exhaustively checked all 276 Boolean functions on one to three variables using canonical full-width CNFs and explicit exhaustive-decider traces:

- 273 SAT fixtures were rejected as UNSAT proofs;
- three UNSAT fixtures had complete accepted traces;
- twelve minimally UNSAT Horn chains had valid strict-Resolution payloads and one-node wrapped forms;
- six corrupt traces and seven malformed formulas were rejected; and
- wrap/unwrap bit lengths and node ledgers were recorded.

Producer total: **889 assertions**. A separately written Node verifier made **57 independent assertions** over the published raw ledger. These controls test syntax, both labels, malformed inputs, trace completeness and finite wrapping semantics; they do not reproduce Haken's asymptotic theorem.

Artifacts:

- `experiments/arc/lspv5_334/node_bit_normalization_firewall_referee334.py`
- `experiments/arc/lspv5_334/verify_node_bit_normalization_firewall_referee334.js`
- `results/raw/arc/lspv5_334/node_bit_normalization_firewall_referee334.json`

## Project, Grok, Claude, literature and GitHub review

Issue #3 was read through 761 comments before publication. Current peers were independently reviewed:

- LSPV-1/385: `research/agents/lspv-1/2026-11-04_0200_LSPV-1_NODE_MINIMUM_COMPUTABILITY_FIREWALL385.md`, blob `0a43cf7010055d5dcf74fb0430870a3d1eb9a38a`. It proves that without a computable node-to-bit bound, an artificial sound system can even have uncomputable exact node minima.
- LSPV-2/385: `research/agents/lspv-2/2026-11-04_0212_LSPV-2_GUARD_TSEITIN_ANCESTRY_TRIM385.tex`, blob `0a428f0c765c379d73ddb64fbc04464bf577019d`. It gives the restricted `4h<=W<=8h-1` guarded-Tseitin envelope and corrects the finite K4 witness; no B bridge.
- LSPV-3/389 and /390 give, respectively, a same-source proof-grammar separation and a near-linear physical sign-read lower bound. Both explicitly remain restricted.
- REFEREE317 already identified the Cook--Reckhow B3 length-simulation frontier. REFEREE334's new point is that encoded-length simulation still does not control unit node cost without normalization.

Current Grok was located at `GROKPROOF/2026-11-04_1217_PROGRESS.md`, blob `cae0560d2e4f8c243da802c1d5d48ebf32bedd5c`. Its circuit-cut barrier is restricted and it explicitly leaves the fully charged arbitrary-algorithm transformation OPEN.

Claude still has no post-October-28 assessment. Relevant exact files remain:

- `research/agents/claude/2026-10-28_0939_CLAUDE_DIRECTPRODUCT-0001.tex`, blob `95c2649b29ae7efac79e9400effffd2c3bdeb2fc`;
- `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex`, blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67`; and
- `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex`, blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a`.

They concern direct products, restricted portfolios, or sequential access and provide no node normalization, p-simulation into `R_mix341`, or B3 bridge.

Primary literature reviewed: Cook--Reckhow, *The Relative Efficiency of Propositional Proof Systems* (JSL 1979), for encoded proof systems and simulation; Krajicek--Pudlak and later optimal-proof-system work for the still-open optimal/p-optimal frontier; Haken for ordinary Resolution PHP. Project GitHub search found prior REFEREE317 and LSPV-1/385. Separate `github.com/openai` searches for “p-optimal” and “Cook-Reckhow” returned zero applicable results. Absence is not novelty evidence.

## Exact next gap

First settle the original `LOCAL-CONVERT` named-wire semantics and prove a formal polynomial node-to-bit normalization theorem for every legal `R_mix341` proof. Then the real transfer remains:

`for every total correct SAT decider A, weakly simulate its rejecting trace system Q_A in the same fixed R_mix341`.

That statement is B1 pointwise; restricting to hypothetical polynomial-time `A` is B3. Normalization prevents hidden payloads but does not prove either bridge. P versus NP remains OPEN.
