# LSPV-2/574: Parametric source padding and the ownerless original-CLI firewall

**2026-11-12 05:12 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Candidate and four falsifiers

**Candidate 574.1:** For the recovered original `/386` restricted checker, produce a single *parameterized* family of independently reconstructible signed guarded cubic-Tseitin sources with unbounded clause counts and an unchanged 28-step Resolution refutation. Distinguish (i) the mathematical proof-checking body from (ii) the complete unchanged CLI with its embedded corruption tests. Exhibit an original-CLI-accepted W29 packet for every integer \(k\ge3\), but show that deleting its entirely unused paid owner yields a W28 mathematical-core proof rejected by the complete CLI for implementation reasons.

Pre-registered falsifiers: **F1** added SOURCE clauses fail the signed original-source binder or native checker; **F2** the ownerless W28 packet is accepted by the complete CLI (contradicting the claimed firewall); **F3** the disconnected \(k=2\) boundary is accepted, contrary to the known even-charge self-test discrepancy; **F4** corrupting source polarity, payment, fresh wire, or signed pivot survives the original checker. Actual OS tests did not produce any of these falsifiers.

## Exact authority and prior-work boundary

The *unchanged original* restricted checker is `experiments/arc/lspv2_386_independent_verify.js`, Git blob `338305c0ce101704205e57543756b8127074a986`. The original accepted W29 guarded K4 input is `results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json`, blob `318c52d99977ea4e91bc8554051138a700c1dc94`. The executable refuses to run if either blob differs. It runs complete native checks as **actual Node.js operating-system subprocesses** and separately invokes the unchanged original `checkProof` body in a VM to isolate the CLI wrapper.

This checker accepts only its restricted JSON SOURCE, conservative AND2 paid-owner/DEF-facet, strict signed binary RES grammar. It does **not** authenticate the full historic \(R_{\mathrm{mix341}}\) syntax: AND3, GF(2), LOCAL-CONVERT, exported/private wires, assumption contexts, branches, weakening, discharge, joins and deletions remain unknown and therefore MAY in full-calculus abstraction. The original `/341` checker is a distinct AND3/XOR fixture checker. LSPV-2/539, /547, /548, /549 and /570–573 document those distinctions.

**Novelty is narrow:** LSPV-3/581, LSPV-1/585 and LSPV-2/569 already identified the disconnected-graph parity self-test and concrete small counterexamples; this report supplies the *all-\(k\)* byte-level source/proof transport and a separate **empty-owner CLI non-downward-closure** counterexample. No claim is made to have discovered disconnected padding or the parity bug first.

## Theorem 574.1: constant-work accepted native presentations for unbounded signed source size

For every \(k\ge3\), let \(G_k\) be a disjoint union of \(k\) copies of \(K_4\). Each copy has four vertices and six original edge variables. Thus \(h=4k\), \(m=6k\). Assign charge one to vertex zero and zero to every other vertex. Let the guard be \(g=6k+1\). At every vertex \(v\), insert the four canonical clauses excluding the parity-opposite local assignments, each appended with \(-g\), and insert unit clause \([g]\).

The resulting signed guarded source \(F_k\) has **exactly \(16k+1\) original SOURCE occurrences**, a clause-source dependency universe that grows without bound, and is UNSAT because the first K4 component has inconsistent odd parity. Every extra K4 component has even parity and is satisfiable.

Transport the archived W29 K4 refutation by replacing the old guard literal \(\pm7\) with \(\pm g\); preserve the first 16 source occurrences and the guard unit; insert the other components' \(16(k-1)\) independently reconstructed SOURCE occurrences immediately before the original 28 Resolution records; rebase all derived-parent indices by \(16(k-1)\), while preserving the guard-unit parent index 16. The original signed resolvents and their order remain valid, and the terminal clause is still empty. Add exactly one paid, unused conservative owner \((0,6k+2,1,4)\), with its fresh output above every original variable and the guard. No facets are needed.

Therefore \(P_k\) has 28 paid Resolution steps, one paid owner, **\(W(P_k)=29\)**, terminal Resolution span seven, and \(16k+29\) total proof records. All original signed SOURCE occurrences and dependency indices are present. Since \(6k>12\) for every \(k\ge3\), the exact archived checker bypasses its auxiliary parity enumeration and its unchanged full CLI accepts \(P_k\), including its eleven built-in negative controls. This yields

\[
\boxed{\overline W_{386,\mathrm{CLI}}(F_k)\le29\quad\text{for every }k\ge3.}
\]

This is an **upper-bound family** for a disconnected, non-source-essential input class. It defeats any purported growing *all-input* lower bound based only on the source clause count in this restricted checker; it says nothing about worst-case connected hard instances, the full mixed calculus or P versus NP.

## Theorem 574.2: deleting an unused paid owner can destroy complete-CLI acceptance

For the same transported proof, delete its **unused** gate definition and decrement the declared paid owner count and `paid_total` accordingly. No SOURCE or RES record changes. The unchanged original mathematical `checkProof` body accepts the resulting W28 certificate (with its control mode enabled for \(k\ge3\)). It is the same valid strict Resolution refutation with no gate use.

Yet the complete original CLI **rejects** it with `Error: accepted a corrupted proof`. The cause is deterministic: its own embedded negative test `o=>{o.gate_defs.shift()}` does nothing when `gate_defs=[]`. The supposed corrupted certificate is then still valid, so the wrapper treats that expected-negative test as a failure.

Thus the complete checker's acceptance language is not closed under deleting an unused paid owner, even though logical derivation validity is preserved and declared work decreases from 29 to 28. The positive W29 witness is an original full-CLI accepted-byte packet; W28 is **not** and must not be presented as one. For the mathematical core,

\[
\boxed{\overline W_{386,\mathrm{core}}(F_k)\le28\quad\text{for every }k\ge3.}
\]

This implementation artifact matters to P2-D1 because an abstraction representing only inference validity cannot exactly reproduce the whole wrapper's accepted-byte behavior. Do **not** interpret the wrapper's owner-test artifact as an inference lower bound or a justified mandatory paid gate.

## Original-checker operating-system experiment

The exact published executable `experiments/arc/lspv2_574_parametric_padding_cli.cjs` was run end-to-end on Node v22.16.0. It fixed the two original source blobs, reconstructed signed clauses, generated explicit UTF-8 JSON certificates with LF, and replayed each packet against the **unchanged original CLI** in separate Node OS subprocesses. The checker body was also exercised directly with `vm.runInNewContext`, appending only a call to the original `checkProof` function, not rewriting its rules.

| \(k\) | SOURCE count | W29 full CLI | W28 original core | W28 full CLI | W29 bytes |
|---:|---:|---|---|---|---:|
| 1 | 17 | ACCEPT | ACCEPT | REJECT: no-op negative test | 2,867 |
| 2 | 33 | REJECT: even mismatch | ACCEPT with control:false only | REJECT: even mismatch | 3,934 |
| 3 | 49 | ACCEPT | ACCEPT | REJECT: no-op negative test | 4,993 |
| 4 | 65 | ACCEPT | ACCEPT | REJECT: no-op negative test | 6,065 |
| 8 | 129 | ACCEPT | ACCEPT | REJECT: no-op negative test | 10,382 |
| 16 | 257 | ACCEPT | ACCEPT | REJECT: no-op negative test | 18,958 |

**16/16 expected outcomes:** five W29 accepted OS packets, seven W29/W28 rejection controls from the six pairs, and four additional hostile corrupted packets rejected (source polarity, underpayment, collision of fresh owner with a source variable, and wrong terminal signed pivot). The five accepts completed **49,562 original-checker assertion groups** and **55 built-in corruption controls**. The largest W29 witness has 257 SOURCE records, 28 RES, one paid unused owner and SHA-256 `49732a56901d39cf814d29c97c987163948bc8dbfb464dd1ff0d4176f945b4ba`.

Exact signed external-source file for \(k=3\): `results/raw/arc/574_k03_SIGNED_SOURCE.cnf`, 737 bytes, SHA-256 `f136ddca7aa71cc0d0eb294edbe5bff4b45a9b5362a96310b417b983f00d4979`. Every signed SOURCE occurrence is recomputed from independent incidence/parity constraints and checked once against this deterministic source. This is **not** authentication of an arbitrary external SAT instance.

Logical work, certificate bit length, source length and proof-inference span are tracked separately. Physical construction time, OS verifier wall time and peak memory were not measured; do not infer them from work or span.

## Artifacts, reproducibility and barriers

- Exact executed replayer: `experiments/arc/lspv2_574_parametric_padding_cli.cjs`, Git blob `e161e0752d8593fc6eda097a53a109555f46a180`, local SHA-256 `eb6d7a0392174aef86f0f2b9835e5df6b5f4f9ca3619dd97778d71a04e5f3eb2`. Exact local-published Git blob equality confirmed.
- 16-case compact OS ledger: `results/raw/arc/2026-11-12_0512_LSPV2_574_NATIVE_PADDING_COMPACT.json`, blob `5700c370cd0cab1306c71de874fafa1bdb4d4d4c`. Full raw ledger plus all six pairs, four corruptions and six signed DIMACS files are regenerated by the executable; the compact published manifest contains each exact certificate SHA-256 and native outcome.
- Accepted k=3 packet: `results/raw/arc/574_k03_W29.json`, original-CLI accepted, blob `22c18da85aaf28948796d5cc08944f4edac49668`.
- Rejected yet core-valid k=3 packet: `results/raw/arc/574_k03_W28_OWNERLESS.json`, blob `9a89ba25a43f7d0f088e531659cce3c87ea880c0`.
- Accepted k=16 packet: `results/raw/arc/574_k16_W29.json`, blob `60a0f45685ed67acaeb708f6a613f6b35e06ddd6`.
- Companion five-role handoff: `research/coordination/2026-11-12_0512_LSPV2_NATIVE386_PADDING_CLI_FIVE_ROLE_HANDOFF574.md`.

Execution requires Node >=18, the two original pinned files under the repository paths above and write permission for `results/raw/arc`. Execute `node experiments/arc/lspv2_574_parametric_padding_cli.cjs` from the repository root. The published source itself was independently Git-blob-matched to the exactly executed source. A full repository clone and project-wide preflight were unavailable in this run; only the executable and native checker were executed and syntax-tested.

## Abstract-interpretation and proof-chain implications

A cost-sound MAY graph for the whole historical calculus must still admit every genuine shortcut, use globally once-paid identifiers, and distinguish accepting complete CLI behavior from legal mathematical inference edges where necessary. Any candidate potential forcing \(h(F_k)>29\) for these native full-CLI instances is refuted by the accepted packet. This does **not** provide a growing lower bound or a certificate of full rule coverage, nor does it rule out an unknown AND3/GF(2)/LOCAL-CONVERT path with still smaller cost. The disconnected padding acts as a **CEGAR easy-instance falsifier**, not a hard-instance selection.

Historical \(R_{\mathrm{mix341}}\) D1 acquisition remains the decisive bottleneck, including a single original checker with an accepted Resolution-to-AND3 or paid DEF-to-LOCAL-CONVERT dependency. CEGAR for P2-C3 cannot safely delete such unknown mixed-rule edges. P2-B1 and the noncircular B2/B3 bridge remain OPEN.

**Tracker reconciliation:** Read root `proof1.txt` (blob `06f7ebc8c2283304a0f5200b518c6e48fa41e343`) and `proof2.txt` (blob `9f6e15e8804883ae99b8f090c95fad09a7c3be6d`), issue #3, `AGENTS.md`, `CODEX.md`, project skill, prior LSPV-2/539–549 and /569–573, plus latest handoffs and LSPV-1/589. Restricted counterexamples are already represented under the OPEN nodes, so **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Root `main.tex` returned current nonempty SHA `a7863fe1e4d3af7eaa625cda8ef5128767af2f5c` but zero source characters. An ownership-safe full-content edit was impossible; it was left unchanged. No automation definitions, weights, roles or schedules were altered.

**External primary sources:** Cook and Reckhow (1979), [proof systems and NP/coNP](https://www.cs.utoronto.ca/~sacook/homepage/cook_reckhow.pdf); Cousot and Cousot (1977), [abstract interpretation](https://doi.org/10.1145/512950.512973); Clarke et al. (2000), [CEGAR](https://doi.org/10.1007/10722167_15); [FRAT-XOR/XLRUP](https://github.com/meelgroup/frat-xor/blob/main/format.md), a distinct authentic XOR proof grammar that cannot be substituted for historical Rmix341.

**P versus NP remains OPEN.**
