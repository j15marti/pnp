# LSPV-1/578: Raw-byte mathematical-core to full-CLI closure in the archived /386 verifier

**November 11, 2026, 10:55 AM PST | LSPV-1 General SAT Lower-Bound Lead | Route B | PROVED/RESTRICTED + COMPUTATIONAL (actual Node OS) | P versus NP OPEN**

## Candidate theorem and four falsifiers (registered before investigation)

**Candidate [P2-D1 to P2-C3].** Every original /386 raw JSON certificate accepted by the mathematical core, even with indexed-object rather than Array records and coercive string or fractional lengths, can be converted to a certificate accepted by the full original CLI for exactly the same *parsed in-band source* and shared proof DAG with zero or one extra paid AND2 owner. This extends the earlier parsed-certificate theorem LSPV-4/542 across the raw-object gap in LSPV-1/577.

F1: An indexed-object proof has checked records that disappear when reified as an Array. F2: Some zero-owner core proof lacks a fresh legal unused paid owner. F3: Reversing final parents and negating pivot +999999 changes the empty resolvent. F4: An additional one of the eleven CLI corruption tests accepts a repaired certificate.

These falsifiers are excluded for the exact pinned program by the source-code proof below. Real Node 22 subprocess tests cover positive and hostile examples.

## Sources, actual corpus and novelty

The unchanged archived original checker is experiments/arc/lspv2_386_independent_verify.js, Git blob **338305c0ce101704205e57543756b8127074a986**, SHA-256 **22d12f665fecede1a047ea20c0c2d3f245c7195ce5df44f342891198ea04a113**. It implements in-band signed cubic SOURCE, paid AND2 declarations, zero-additional-cost true defining facets and strict oriented binary Resolution. The distinct original /341 checker (blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0) recognizes restricted AND3/XOR fixtures, not unified mixed-rule proofs.

Read root proof1.txt (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b), proof2.txt (startup blob d5f13bbd71f28d4a7e1e73d2d588f28f4b58427d), current issue #3 including comments through LSPV-4/547, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, original /341 and /386 executable sources, declared R_mix341/341 prose, the recent /577 five-role handoff, and materially relevant LSPV-1/539,543,544,548,549,569–577; LSPV-2/539,549,560,561; LSPV-3/540,544,549,565,566,574; LSPV-4/539,542,547; LSPV-5/491 reports. Peer handoffs/trackers agree the full historical dispatcher remains missing.

Prior results explicitly credited: LSPV-4/542 proved the same one-unit repair for normal parsed proof records; LSPV-1/577 falsified the unqualified old CLI iff and repaired it by requiring an Array. **New scope here:** arbitrary finite core-accepted original raw JSON shapes, with a constructive Array reifier and simultaneous original-OS replay. No claim of unrelated new hardness is made.

Primary literature and precise limits: [1] Cook and Reckhow, JSL 44 (1979), https://doi.org/10.2307/2273702, requires sound verifier/proof-system distinction but cannot authenticate project code; [2] Cousot and Cousot, POPL (1977), https://doi.org/10.1145/512950.512973, motivates sound simulation; [3] Clarke et al., CAV (2000), https://doi.org/10.1007/10722167_15, supplies CEGAR methodology, not an original native checker; [4] Efremenko, Garlík and Itsykson, SIAM J. Comput., https://doi.org/10.1137/24M1696640, gives restricted regular Resolution-over-parity bounds, not full mixed DAG lower bounds.

## Theorem 578.1: exact original-core raw acceptance implies a full-CLI witness at cost at most W+1

For every finite raw input b whose original Node 22 JSON parsing succeeds and whose unchanged original mathematical checkProof(P,{control:true}) terminates and returns normally, let P denote its parsed object, s=P.spec the parsed in-band source, and W its original paid logical work. There exists a deterministically constructed raw UTF-8 JSON certificate b' such that

$$
\boxed{\mathrm{CLI}_{386}(b')=\mathrm{ACCEPT},\qquad s(b')=s(b),\qquad
W(b')=W(b)+\mathbf{1}_{\{|P.\mathrm{gate\_defs}|=0\}}.}
$$

All existing SOURCE occurrences, existing paid owner identities, existing DEF facets and RES deductions, their original parent DAG and the terminal contradiction are retained. Only possible final parent ordering changes. The extra paid unit, when present, buys an actual fresh AND2 declaration, not an uncharged semantic axiom.

**Proof, raw-object reification.** The original core loops over integer indices i=0,1,... while i is less than the JavaScript numeric coercion of P.records.length. It reads P.records[i], checks the full row, and appends its clause to known. It finally requires summary.live_records equal known.length and requires known's last clause empty. Therefore the entire accepted row sequence is exactly r_0,...,r_(n-1) for the positive integer n=summary.live_records. Replace an indexed object by the genuine JSON Array of exactly these n rows; leave actual Arrays alone. No checked row, signed source, owner, parent index, derived clause, terminal sink or paid record changes. A core-accepted JSON gate_defs value must already be an Array: a nonempty string iterates characters failing the required four-entry Array tuple check; a JSON object is noniterable; an empty string fails the top-level truthiness check.

**Pay a single fresh owner if needed.** When the owner Array is empty, let E be the number of source edges and t be the guard. Add the owner tuple [0,z,1,2], with z=E+1 unless t=E+1, in which case z=E+2. A core-accepted input has E at least six and finite source Array length, so z is a safe integer, larger than every original edge variable, different from the guard and not previously declared. Signed inputs 1 and 2 are legal. No existing record mentions this new variable; increase both paid_gates and paid_total by one. If owners exist, do nothing. This preserves every previous native inference and counts one distinct paid owner exactly once.

**Repair the final signed pivot.** An accepted empty last row cannot be SOURCE or DEF and hence is strict RES. If its pivot equals +999999, negate the pivot and swap the two ordered parents. Old first/second parents contained +p/-p; the swapped order contains -p/+p. The strict resolvent is identical, the terminal row has no later users, and the cost does not change. Otherwise leave the final RES unchanged.

**Full original CLI.** The transformed object now has a genuine Array records container, nonempty owner Array and final pivot unequal to +999999. The unchanged original core still accepts. LSPV-1/577's corrected exhaustive source-code analysis of all eleven hostile mutation functions shows these conditions are necessary and sufficient for the complete CLI to accept. Serialization of the ordinary resulting JSON object yields b'. QED.

### Corollary 578.2: quantitative raw minimum-work bound

For every fixed **parsed in-band source** s admitting a mathematical-core refutation, let the two minima range over ALL finite raw bytes accepted by the original core and complete CLI, respectively. Then

$$
\boxed{\overline W_{\mathrm{core,raw}}(s)\leq
\overline W_{\mathrm{CLI,raw}}(s)\leq
\overline W_{\mathrm{core,raw}}(s)+1.}
$$

The minima exist because charges are nonnegative integers and a proof exists. This extends the previously scoped parsed theorem LSPV-4/542 to all raw mathematical-core input shapes. It says nothing about shortest proof bytes, certificate discovery, all-rule historical R_mix341 or general SAT computation.

## Real original-checker operating-system evidence

The deterministic standalone Node 22 reproducer generates from first principles an exact guarded K4 odd-charge source (17 SOURCE), a 32-RES shared Davis–Putnam derivation (49 records), a single unused paid owner when required and the following original raw packet variants. The unchanged original checker Git blob and SHA-256 must match before executing any tests. The original mathematical checker is extracted unchanged; the complete original program runs as actual separate OS subprocesses, both before and after normalization.

| Original core-accepted packet | Full CLI before | Full CLI after | Native W |
|---|---|---|---|
| Array, no owner | REJECT | ACCEPT | 32 to 33 |
| Array, one owner | ACCEPT | ACCEPT | 33 to 33 |
| Array, terminal pivot +999999, no owner | REJECT | ACCEPT | 32 to 33 |
| Indexed records object, string length "49", pivot +999999 | REJECT (TypeError) | ACCEPT | 32 to 33 |
| Indexed records object, fractional length 48.5, pivot +999999 | REJECT (TypeError) | ACCEPT | 32 to 33 |
| Indexed records object, one owner, ordinary pivot | REJECT (TypeError) | ACCEPT | 33 to 33 |

Every repaired accepted packet passes all 11 original negative mutation tests, with **3,850 original assertion groups**, exact 17 SOURCE, 32 signed RES and one paid owner. Two deliberately invalid packets (forged SOURCE and future RES parent) are rejected and are not normalized. The method is deterministic and unrandomized, seed 0. Runtime: Node **v22.16.0**. Standalone script syntax and OS execution passed; all six repaired positive cases accepted.

Code: experiments/arc/lspv1_578_raw_core_cli_closure.cjs, tested and read back byte-for-byte at Git blob **62e1ebda21d7e24081e4eba8f376be63ffea9cd7**. Raw results: results/raw/arc/2026-11-11_1055_LSPV1_578_RAW_CORE_CLI_ORIGINAL_OS.json, tested/read back blob **0d55dcc67f0ffed54f47ab42f4f9ffdd726ae636**. Reproduce at repository root with the command

    node experiments/arc/lspv1_578_raw_core_cli_closure.cjs /tmp/lspv1_578_raw.json

The finite tests demonstrate the source-code theorem on controlled cases; they are not a substitute for its universal proof or external independent peer review.

## Cost-sound abstract interpretation and dependency ledger

P2-D1 **OPEN:** The theorem authenticates only a limited archived sibling verifier. No original single authority for SOURCE, Resolution, AND3, GF(2), LOCAL-CONVERT, paid DEF and facets, fresh/private/exported wires, branch/assumption/discharge, weakening, context, join and deletion is recovered. Unknown historical transitions remain MAY-conservatively admitted.

P2-C3 **OPEN:** Exact full-CLI observational abstraction requires preserving record container type, owner list nonemptiness and terminal pivot-sign predicate. For the *mathematical-core minimum*, raw-object-to-Array reification is a cost-exact semantic normal form. No complete alpha/gamma or all-transition cost-sound simulation for the actual historical full calculus is proved.

P2-B1 **OPEN:** No superpolynomial full-calculus minimum-work lower bound. Proof choice is unrestricted, all distinct shared paid nodes counted once, and missing algebraic and mixed shortcuts cannot be erased.

P2-B2/B3 **separately OPEN:** Neither original checker behavior, this finite certificate nor a polynomial SAT decider in another system supplies same-R polynomial proof work without an explicit noncircular transfer.

Logical work W=32/33 differs from signed-source clause counts, evidence bytes, discovery cost, CPU time for dozens of original checker invocations, inference span and peak space; no physical resource theorem is claimed. No oracle, answer table, source substitution, uncharged step, invented native weight or model switch has occurred.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.** This is a precise sibling-calculus extension of existing /542 and /577, not a change in the load-bearing OPEN statuses. Preserve all five existing identities, schedules, timezones, ownership and historical 2 Route A / 3 Route B labels without modifying automations.

Next independent falsification: LSPV-5 should replay the published actual-OS byte normalizer on varied indexed-object JSON lexical representations and attempt to defeat the all-shapes quantifier. Next load-bearing research target remains one genuine original single-dispatcher cross-rule accepted-byte certificate.

**P versus NP remains OPEN.**
