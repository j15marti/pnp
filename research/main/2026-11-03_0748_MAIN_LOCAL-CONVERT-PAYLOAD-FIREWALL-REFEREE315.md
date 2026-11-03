# LOCAL-CONVERT-PAYLOAD-FIREWALL-REFEREE315

**PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393` · November 3, 2026, 07:48 PST**

**Status:** PROVED/EXACT conditional on the previously declared circuit-valued-output syntax `U`; KNOWN CVP theorem; COMPUTATIONAL independent finite replay; FALSIFIED a concrete node-count domination lemma. The intended `Rmix341` LOCAL-CONVERT payload grammar remains unresolved. B1, B2, B3, a superpolynomial worst-case minimum, and P versus NP remain OPEN. No task identity, title, enabled state, schedule, ownership, rule, encoding, or weight was changed.

## Exact obstruction

The fixed-calculus audit must separate logical inference-node cost from the number of encoded bits hidden inside a node. LSPV-4 LOCAL-CONVERT-CVP-GATE-TRACE363 identified the consequential conditional syntax:

> **U:** one unit-weight LOCAL-CONVERT record may contain an explicitly serialized, arbitrary-length acyclic fan-in-two Boolean circuit, provided the circuit has at most three original-variable inputs.

The concrete lemma refereed here was:

> **Q-DOMINATION:** for every legal `Rmix341` derivation, a fixed polynomial in the paid inference-node count `q` bounds both the encoded evidence length and the deterministic validation work.

Under `U`, Q-DOMINATION is false even on one fixed satisfiable source and one fixed two-node logical skeleton.

## Fixed source and exact reduction

Use the authenticated CNF source

$$
F_+=(x)\wedge(x\vee y).
$$

It is satisfiable and has two models. One paid AND3 inference on the two original clauses gives the local parent factor

$$
S(x,y)=x\wedge(x\vee y)=x.
$$

Let `G` be a topologically ordered constant-fed Boolean circuit with output bit `t_G`. A candidate unit LOCAL-CONVERT output is the explicit circuit

$$
C_G(x,y)=x\wedge t_G.
$$

Its original-variable support is `{x}` regardless of the number of internal gates. Exact truth-table semantics gives

$$
S\models C_G\quad\Longleftrightarrow\quad t_G=1.
$$

The forward implication evaluates the assignment `x=1`; the reverse implication is immediate. Appending the `x` input and one final AND gate is a logspace reduction from constant-fed Circuit Value. Membership in P follows by evaluating the serialized acyclic circuit and then the at-most-four relevant source rows. Thus, under `U`, this LOCAL-CONVERT legality subproblem is P-complete by Ladner's CVP theorem.

For the both-label global control, add `(not x)` to obtain

$$
F_-=F_+\wedge(\neg x).
$$

This source has zero models, while the LOCAL-CONVERT node continues to reference only the original two clauses and its local parent remains `S=x`. Hence local conversion legality still depends on `t_G`; independently, resolving `(x)` with `(not x)` certifies the global UNSAT label in one node. Replacing the local antecedent by the contradictory whole source would make every conversion vacuously legal and is explicitly forbidden in this control.

## Exact payload-sensitivity theorem

For every `k>=1`, let `G_k(b)` compute

$$
t_{G_k}=\bigwedge_{i=1}^{k}b_i
$$

from `k` separately encoded constant bits. The canonical left-associated payload has `k` constant records, `k-1` internal AND records, one `x` record, and one embedding AND record: exactly `2k+1` gate records.

On `b=1^k`, the conversion is legal. Flipping any one constant bit makes the conversion illegal. Therefore every deterministic exact bit-probe validator must read all `k` constant positions on the legal input: if it leaves position `i` unread, its execution is identical on the invalid neighbor with `b_i=0`.

Under `U`, the logical skeleton still has only two paid nodes:

1. one AND3 node deriving `S=x`;
2. one LOCAL-CONVERT node carrying `C_G`.

Consequently there is no polynomial `p` satisfying either

$$
|\operatorname{enc}(\pi)|\le p(q)
$$

or

$$
T_{\rm validate}(\pi)\le p(q)
$$

for all such presentations: set `q=2` and increase `k`. This is an exact representation/validation separation, not a SAT-decision lower bound and not a lower bound on `W_R`.

If each internal payload gate must instead be a separately charged DEF node, then `q` is at least the gate count up to a constant additive term and this constant-`q` counterexample disappears. That is a possible formal repair, not a change made by this report. A different bounded or normalized LOCAL-CONVERT syntax could also remove the gap.

## Four falsifiers and dispositions

1. **At most three original variables imply constant validation work.** **FALSIFIED under U:** the all-one `k`-constant payload forces `k` reads.
2. **Paid inference-node count alone polynomially bounds every encoded DAG presentation.** **FALSIFIED under U:** `q=2` while the payload has `2k+1` gate records for arbitrary `k`.
3. **Global UNSAT makes the CVP control vacuous.** **REJECTED for the typed record:** the conversion references the same satisfiable two-clause local parent; the extra contradictory source clause is checked separately. It would become vacuous only if one silently changed the node's antecedent.
4. **The payload lower bound refutes B3 or proves a SAT lower bound.** **REJECTED:** it concerns checking one supplied presentation. B3 relates bare `SAT in P` to polynomial worst-case minimum logical cost for the same fixed calculus.

## Independent experiment

The Python producer and a no-producer-import Node verifier reconstructed the sources, gate grammar, topological references, original-variable support, circuit truth values, and exact local implication.

Tested chain lengths were

`1,2,3,5,8,16,32,64,128,256,512,1024`.

Across them:

- 12 legal all-one chains;
- 2,051 individually flipped illegal neighbors;
- 4,114 gate records across the legal fixtures;
- largest fixture: `k=1024`, 2,049 gate records, 1,024 forced constant probes;
- 512 seeded arbitrary constant-circuit reductions: 228 true and 284 false outputs, each matching LOCAL-CONVERT legality;
- 524 SAT-source controls and 524 paired global-UNSAT controls;
- 12 malformed records and five proof corruptions rejected by the producer;
- six separately constructed malformed payloads rejected by the independent verifier;
- 7,023,626 independent Node assertions.

Final raw SHA-256:

`ab11c374abcc63db088be0b6ef79051075ce7ff84356f79cf5850b8abb0163d5`

## Correct bridge classification

| Obligation | Status | Reason |
|---|---|---|
| B1 pointwise | OPEN | A supplied LOCAL-CONVERT record does not translate every total SAT decider into a proof. |
| B2 worst-case | OPEN | No maximum fixed-calculus proof cost is bounded by arbitrary-decider worst-case time. |
| B3 weakest conditional bridge | OPEN | Bare `SAT in P` still does not yield polynomial `Wbar_R` for the same fixed calculus. |

The result instead identifies a prerequisite for interpreting node weights computationally: either encoded payload length and its verification must be charged separately, or the fixed rule syntax must enforce a polynomial node-to-evidence bound. Unit logical node count may remain a deliberately relaxed proof-size measure, but it then cannot silently serve as machine work.

## Work and all-phase space ledger

| Phase | Measured record |
|---|---:|
| Python producer wall time | 1.538354080 s |
| Python producer peak host RSS | 11,776 KiB |
| Node verifier wall time | 0.195111953 s |
| Node verifier peak host RSS | 77,024 KiB |
| Producer source bytes | 11,691 |
| Verifier source bytes | 6,305 |
| Raw JSON bytes | 4,375 |

These host measurements are not indexed-machine or FLMV bounds. Parsing, source authentication, every gate bit, topological-reference validation, circuit evaluation, implication checking, evidence generation, serialization, and simultaneous live records are actual machine work. Optimizer discovery remains intentionally absent from `W_R`. The all-phase envelope remains

$$
s'\le\max\{\rho,\eta,\lambda,\lambda s\}.
$$

The XOR state-difference adjunct is inapplicable as an internal free oracle here: the exhaustive bit-flip comparison is an offline falsifier. A real validator must acquire the payload bits it relies upon.

## Literature and repository review

Searches covered `Ladner circuit value problem log space complete for P`, `Cook Reckhow propositional proof systems polynomial time verifier`, `DRAT trim proof checking extended resolution`, project GitHub queries for `LOCAL-CONVERT syntax U circuit payload Rmix341`, and scoped `github.com/openai` searches for circuit/SAT proof checkers.

- Richard Ladner, [The Circuit Value Problem Is Log Space Complete for P](https://doi.org/10.1145/990518.990519), SIGACT News 7(1), 1975, supplies the P-completeness theorem used by the exact reduction.
- Cook and Reckhow, [The Relative Efficiency of Propositional Proof Systems](https://www.cs.toronto.edu/~sacook/homepage/cook_reckhow.pdf), requires an effective polynomial-time proof relation in the standard propositional proof-system framework; it does not make raw payload validation free.
- [DRAT-trim](https://github.com/marijnheule/drat-trim) and [LeanSAT](https://github.com/leanprover/leansat) exemplify explicit supplied-certificate validation, distinct from deciding SAT or discovering a proof.

Project review found that LSPV-4 354 had already left circuit-output normalization open; LSPV-4 363 formulated condition `U` and the CVP reduction; LSPV-1 BUDGETED-PROOF-SEARCH364 explicitly assumes bounded-output normalized evidence. The present report independently reproduces the reduction and isolates the exact false Q-DOMINATION lemma. The OpenAI repository search found no applicable `Rmix341` checker or normalization theorem; absence is not novelty evidence.

## Artifacts and next gap

- Producer: `experiments/arc/lspv5_315/local_convert_payload_firewall_referee315.py`
- Independent verifier: `experiments/arc/lspv5_315/verify_local_convert_payload_firewall_referee315.js`
- Raw ledger: `results/raw/arc/lspv5_315/local_convert_payload_firewall_referee315.json`
- Five-role handoff: `research/coordination/2026-11-03_0748_LSPV5_TO_FIVE_ROLE_LOCAL-CONVERT-PAYLOAD-FIREWALL-REFEREE315.md`

Next: settle the authoritative LOCAL-CONVERT grammar without changing `Rmix341` retrospectively. If `U` is intended, every machine-work comparison must include payload length. If internal gates are charged, prove a downstream-preserving normalization and update only future theorems after authoritative agreement. Separately, the decisive mathematical targets remain a mixed-rule-resistant superpolynomial `Wbar_R` and B3 for the same fixed calculus.

**P versus NP remains OPEN.**
