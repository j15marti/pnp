# LSPV-3/612: Absent terminal ID is a genuine native /341 accepted-byte form

**2026-11-13 04:20 PST | Hypergraph & Proof Certificates | historical Route B | PROVED/RESTRICTED source theorem plus COMPUTATIONAL hosted original-body replay.** P versus NP remains OPEN.

## One candidate and four advance falsifiers

**Candidate [P2-L3-612]:** In the archived original /341 checker, omission of the JSON `id` property is legal specifically at the terminal paid inference, but not at a SOURCE or nonterminal paid inference. This creates a parsed JavaScript `undefined` key that is distinct from explicit `null`, including packets with an existing null-valued SOURCE ID.

F1: absent terminal ID rejects due to terminal freshness or root ancestry. F2: some nonterminal missing ID accepts because its parent reference can encode undefined in JSON. F3: missing SOURCE ID and deleted-source binding can still reach the terminal ancestor. F4: replacing an absent terminal ID with explicit null is always semantics-preserving, even when a source is already keyed by null.

## Original authority, literature and corpus

Original checker: `experiments/arc/lspv2_341_independent_verify.js`, immutable Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`. Seven-fixture packet: `results/raw/arc/2026-11-02_1216_LSPV2_MIXED_TSEITIN_MIN_DAG341.json`, blob `fe27fe1011d0021e721ccaeb747ed58da65d7464`. Typed-ID seed: `results/raw/arc/2026-11-13_0319_LSPV3_611_TYPED_ID_ACCEPTED.json`, blob `c9722a849f2ca965c94d34b08703a5db9269217f`. All are original/previously published artifacts, not newly invented grammar.

Read complete `proof1.txt` (blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`) and complete `proof2.txt` (blob `930c5eeddafce656717f28055a7a9a755f44737c`) through immutable blob fallback; issue #3 and current peer comments; AGENTS.md, CODEX.md, the pnp-research skill, main.tex, and LSPV-3/539, /544, /549, /590, /606 and /611 including underlying source. Reviewed LSPV-1/616 and LSPV-4/583 issue evidence, current Grok 2026-11-13 07:20 UTC and Claude world-ledger. Current user focus P2-D1 -> P2-C3 -> P2-B1 overrides old priorities; no scheduler changes. Search and source inspection did not locate the missing unified, external-source-bound historical R_mix341 dispatcher.

Relevant primary literature: Cook and Reckhow (1979), *The Relative Efficiency of Propositional Proof Systems*, *Journal of Symbolic Logic* 44, pp. 36-50, https://doi.org/10.2307/2273702. Cousot and Cousot (1977), *Abstract Interpretation*, POPL, https://doi.org/10.1145/512950.512973. ECMAScript Map keys and JSON.parse property semantics are language semantics, not an alternative proof calculus.

## Theorem 612.1, exact omitted-ID placement

Let P be a genuinely accepted byte-serialized JSON packet in the archived /341 accepted language. For each fixture let N=4V signed SOURCE clauses and M=N-1 paid proof records. The checker demands that the terminal ancestor closure contain all N original source IDs, and each paid record has exactly two distinct earlier parents.

**Claim A.** Every SOURCE and every nonterminal paid record in P necessarily has an explicitly present `id` property. Only a terminal paid record can omit its `id` property.

**Claim B.** For any accepted P in which the terminal has an explicit ID, removing exactly that terminal `id` property yields another accepted packet with the identical signed sources, parent DAG, paid record count, terminal rule, inference calculations and original assertion count. Inserting any fresh explicit JSON-primitive ID at the terminal of an accepted absent-ID packet likewise preserves acceptance.

**Proof.** Let k be the number of paid records in the terminal ancestor DAG. Every one of the N sources is an ancestor, so the underlying connected undirected DAG has N+k vertices and at least N+k-1 edges. Since every paid vertex has exactly two parent references, the ancestor DAG has exactly 2k parent edges, hence 2k >= N+k-1 and k >= N-1=M. Thus all M paid records are terminal ancestors. Every nonterminal paid record and every SOURCE must be referenced as a parent of another paid record. A JSON array parent entry cannot parse to the JavaScript primitive `undefined`: missing array elements are not expressible in conforming JSON, and `null` parses to the distinct value null. A record with absent `id` has value undefined, so such a referenced SOURCE or nonterminal record would fail `byId.get` and the checker would reject. The terminal ID is not subsequently referenced; `byId.set(p.id,p)` and `ancestor(last.id)` both operate on the same undefined key. There can be no previously accepted undefined-key SOURCE or earlier paid record by Claim A, so freshness holds and all computations are unchanged. Any genuinely fresh explicit primitive terminal key works analogously. QED.

This proof uses the **actual archived checker** and its mandatory N-1 paid-record count. It is not an assertion about full R_mix341, branch joins, general certificates or external source soundness.

## Original checker replay, packet and hostile controls

41 complete test executions were performed against the unchanged original checker mathematical function within hosted V8 (only Node input/output adapters changed): **6 ACCEPT and 35 REJECT, zero unexpected outcomes, 67,032 original assertion groups on accepted executions**. The original seven-fixture packet and the packet with all seven terminal IDs omitted both ACCEPT with precisely 30,714 assertion groups each, and all 321 paid records across those seven **separate** certificates are preserved (15, 23, 31, 39, 47, 127, 39).

In the complete K4 packet, deleting the terminal ID ACCEPTS; deleting any of the other 14 paid IDs or any of 16 SOURCE IDs REJECTS. Forged parents, false AND3 truth tables, dual missing paid IDs, and missing SOURCE/deletion-reference pairs all REJECT. In the preexisting typed-ID K4 certificate with a null-valued SOURCE, omitting terminal ID ACCEPTS whereas assigning explicit `null` to the terminal REJECTS on `fresh inference ID`; setting a fresh string terminal ID ACCEPTS. This directly refutes the unsafe normalization `missing -> null`.

Canonical accepted-byte witness: `results/raw/arc/2026-11-13_0420_LSPV3_612_K4_MISSING_TERMINAL_ACCEPTED.json`. Raw outcomes: `results/raw/arc/2026-11-13_0420_LSPV3_612_TERMINAL_ID_DOMAIN_HOSTED_RAW.json`. Full OS Node reproduction program: `experiments/arc/lspv3_612_native341_missing_terminal_id.cjs`. The published script runs the **unchanged** pinned original checker as a separate Node process and checks source Git blob SHA hashes; the script was not executed as an OS subprocess in this automation environment. Hosted V8 original-body replay is the execution evidence, not the separate reimplementation of mathematical rules.

## Typed DAG abstraction and CEGAR effect

A concrete terminal owner key has an explicit presence bit `present(id)`; if absent its parsed Map key is undefined. Define alpha on this *verified terminal-only equivalence fiber* by replacing the terminal's ID with a canonical fresh symbolic root, retaining full original SOURCE bytes/IDs, every other owner, every typed parent edge, contexts, all paid identities and fixed weights. Define gamma to include absent terminal encoding and all collision-free explicit root renamings. Native acceptance and the logical goal predicate are separately retained. The commuting transition property follows because the terminal has no outgoing parent reference and the native checker uses the same internal key on insertion and root ancestor lookup. Paid logical work remains exactly M; evidence bytes, parsing, span, time and memory are not equated.

An abstraction that coerces absent terminal ID to JSON null can turn a genuine native accepting path into a falsely rejected path when a null SOURCE exists. Conversely rejecting absent IDs on schema grounds loses accepted checker executions. The CEGAR repair is the presence/type-aware owner identity. This does not prove any unrestricted MAY transformer or source-sound UNSAT certificate.

## Barriers and status

This is a completed restricted **P2-D1 terminal-ID byte-grammar subdependency** and a specified P2-C3 parser abstraction regression, not a complete native calculus. Resolution-to-AND3, DEF-facet-to-LOCAL-CONVERT, globally fresh wires, active/discharged contexts, weakening, branch joins and external-source byte binding remain unauthenticated in one historical implementation. P2-D1, P2-C3 and P2-B1 remain OPEN; P2-B2/B3 separately OPEN. No superpolynomial SAT lower bound, machine-time bound, or P versus NP resolution follows.

TRACKERS REVIEWED; NO MATERIAL CHANGE. No rule, cost, agent, schedule, ownership boundary or two Route A/three Route B allocation was altered. Repo-wide preflight and TeX compilation were not run in this connector-hosted execution.
