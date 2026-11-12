# LSPV-2/572: Exact full-CLI owner-order quotient and 130 native accepted-byte controls

**November 12, 2026, 03:12 PST | SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED source-code theorem + COMPUTATIONAL OS replay | P versus NP OPEN**

## Candidate and four falsifiers

**Candidate:** Strengthen the original LSPV-2/554 *mathematical-core* gate-owner topological-order theorem to the complete, unchanged archived /386 command-line checker, including all eleven original CLI corruption self-tests, without the /554 condition that each declared gate be used by a proof-record facet. A source-fixed packet with five paid owners and five free defining facets supplies a fully enumerated 120-permutation original-OS control.

F1: a topological owner permutation is rejected by the unchanged complete CLI although the original accepts. F2: a non-topological permutation is accepted by the unchanged CLI. F3: a legal permutation causes the original first-owner-removal self-test to pass, making the wrapper reject. F4: source occurrence binding, signed RES dependencies, DEF owner views or count-once logical cost changes under legal permutations. **All four were falsified in the 130 native OS cases**, with the general theorem proved from the exact checker source. These finite checks are not a universal SAT lower bound.

## Precedence and corpus

This is an incremental tightening of LSPV-2/554 (original mathematical-checker iff, three legal / three illegal permutations, 12 hosted-V8 checker cases), **not** a new theorem that topological owner order determines basic gate legality. LSPV-3/584 established a separate paid-owner bank cost fiber, LSPV-3/585 and LSPV-5/501 covered free facet placement, and LSPV-2/571 covered signed RES and gate-input presentation symmetries. The new contribution is an unconditional **full original CLI** extension for all ordinary checker-accepted packets (no live-facet hypothesis), together with all 120 orders of a five-owner example and ten hostile tests executed in OS subprocesses.

Read both living root trackers (proof1.txt Git blob 06f7ebc8c2283304a0f5200b518c6e48fa41e343; proof2.txt blob 1bf4929f872506fcbc357810bd72d016694618b2), GitHub issue #3 and latest comments, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, original /341 declaration and recovered /341 and /386 checkers, actual LSPV-2/539 through /549 reports, /554, /570, /571, and relevant contemporaneous LSPV-1/588, LSPV-3/585, LSPV-4/558 and LSPV-5/501 results. Complete root main.tex was attempted but returned **zero text bytes with a nonempty Git blob**; no unsafe overwrite was made. Research preflight scripts could not be executed against an incomplete local checkout.

External primary literature: Cook and Reckhow (1979), DOI https://doi.org/10.2307/2273702 (proof-checking scope); Cousot and Cousot (1977), DOI https://doi.org/10.1145/512950.512973 (abstract interpretation); Clarke et al. (2000), DOI https://doi.org/10.1007/10722167_15 (CEGAR). The distinct FRAT-XOR/XLRUP format and verified cake_xlrup checker are described at https://github.com/meelgroup/frat-xor/blob/main/format.md. None supplies the missing historical R_mix341 grammar.

## Theorem 572.1: complete original-/386 CLI owner-order invariance

Fix an ordinary finite, unique-key JSON certificate P that the **unchanged complete** original /386 CLI accepts, using source-pinned Git blob 338305c0ce101704205e57543756b8127074a986. Its paid owner list comprises distinct records [id,z,a,b] with z greater than the number of original edges, fresh with respect to previous owners and different from guard. Define the directed graph D on owners with j -> i exactly when a signed input to owner i uses the absolute wire output of owner j.

For **every** permutation pi of the owner records, changing only their order while holding the exact source, proof records, parents, signed pivots, source occurrences, summary and paid identities fixed,

\[
\operatorname{Accept}_{\rm full386}(P^\pi)=1
\quad\Longleftrightarrow\quad
\pi\text{ is a topological order of }D.
\]

Every accepted permutation retains

\[
W_{\rm full386}(P^\pi)=N_{\rm RES}+|D|=W_{\rm full386}(P).
\]

**Proof.** The original owner prepass permits any original-edge input and any already-declared gate output, and rejects a future gate output. Thus every topological order reconstructs exactly the same finite id-to-output and output-to-defining-facet maps, independently of declaration order. All SOURCE, DEF, signed Resolution, chronology, terminal, and summary checks then act on these unchanged maps and records. Every non-topological order exposes some consumer before its producer and fails the native gate-input precondition.

The complete CLI also runs eleven deliberate corruptions. Ten do not depend on the order of the gate declaration array (they alter an initial or terminal proof record, source charge, edge, guard, parent, or summary). The only owner-list mutation is removal of its first owner **without changing summary.paid_gates**. Every original full-CLI-accepted P must have at least one owner: otherwise removing the first owner would leave the packet unchanged and the original wrapper would reject. With at least one owner, deleting the first owner strictly decreases the accepted checker-paid owner count while leaving summary.paid_gates untouched, so that corruption always fails, for every topological order, regardless of facet usage. Thus each topological order passes all eleven unchanged wrapper controls. Conversely, no invalid owner order can pass the mathematical prepass. The claimed iff and work identity follow. This argument is restricted to the **pinned original implementation**, whose acceptance relation includes its wrapper tests; raw duplicate-key/exotic numeric packets and the unauthenticated mixed R_mix341 grammar are outside the stated ordinary-JSON scope. QED.

**CEGAR consequence (restricted).** With the same source, signed owner tuples, gate dependency DAG, paid-id bank and proof-record graph fixed, an abstract state may quotient *only* the concrete owner-list presentation order into one DAG. Its concretization is the set of topological orders. Every goal path represented by this quotient has an original-CLI accepted representative, with identical count-once paid cost. An abstraction forgetting producer-before-consumer additionally represents 114 spurious orders in the test family; the exact dependency-order predicate removes those spurious paths without excluding any actual accepted order. This is not a full mixed-calculus alpha/gamma theorem.

## Exact source-authenticated 5-owner construction

Start with original-source K4 packet, pinned seed blob 318c52d99977ea4e91bc8554051138a700c1dc94, and separately supplied signed DIMACS file (blob e8bc4300f1f4518cb447edaf3f699bcee4839803, SHA-256 3b94f215568099b24756872b0391db550092fb24ef6e67f05ee024bf9330f35c). The replayer requires exact occurrence-by-occurrence equality of all 17 signed original SOURCE clauses before invoking the original checker.

Paid static owners, with two inputs in order, are [0,8,1,4], [1,9,2,5], [2,10,8,3], [3,11,9,-6], [4,12,10,11]. The dependency edges are 0->2, 1->3, 2->4 and 3->4. Insert five genuine native zero-extra-cost DEF views, one for every paid owner, after the 17 SOURCE records, and rebase the chronological parent pointers of all 28 original RES steps by +5. Every tested packet has **17 SOURCE + 5 DEF views + 28 RES = 50 proof records**, five distinct paid owners, and W=28+5=33. The original source clauses and full derived RES DAG are unchanged by order permutation. No assumptions, branch contexts or mixed operations are claimed authenticated.

Exactly 6 of 5!=120 permutations are topological: interleave the two length-2 chains (0,2) and (1,3) in C(4,2)=6 ways, then place owner 4 last. The other 114 permutations must fail the original gate prepass.

## Original operating-system execution and raw results

**130 actual Node v22.16.0 OS subprocesses invoked the byte-for-byte unchanged archived checker** from the exact locally executed published 6,667-byte replayer (Git blob da2bf8e63db37f68723ebe5529c951c829390bc3). Six topological packets ACCEPTED, all 114 other permutations REJECTED, and ten further adversarial packets REJECTED. **130/130 expected polarities.** The six accepts had **21,144 original assertion groups** and **66 original built-in corruption tests**. Each accepted packet is 3,157 UTF-8 bytes and W=33. The six valid orders are 01234, 01324, 02134, 10234, 10324, 13024.

Hostile controls: wrong defining facet, signed SOURCE forgery, wrong Resolution pivot, underpaid summary, guard as owner input, duplicate paid owner id, missing owner, forward gate dependency, unsupported AND3 tag in **/386 only**, and unsupported LOCAL-CONVERT tag in **/386 only**. The last two cannot exclude those rules from the missing historical mixed checker.

Published exact replayer: experiments/arc/lspv2_572_native386_full_cli_gate_order.cjs. Immutable compact original-OS manifest: results/raw/arc/2026-11-12_0312_LSPV2_572_NATIVE386_FULL_CLI_OWNER_ORDER_COMPACT.json (Git blob 752ce378383f86e71fea8045317f823ef77d12b2). Raw 130-case full timing/verdict/hash ledger is deterministically generated by the replayer as results/raw/arc/2026-11-12_0312_LSPV2_572_NATIVE386_FULL_CLI_OWNER_ORDER_RAW.json (local SHA-256 d558a51c7834782dadeeea5de1fe70ed905dda5ddce392f00f70e8c4b38c5a22), included in the supplementary evidence archive. Exact 3,157-byte accepted packet blobs a681b3fb26083055206a3e13ebde4bbf1ee2a0a8 and 017cf044da56749c4ddc83387e98ed2a7e0641f6; exact rejected forward-ordered packet blob 95e983ad36039ed69958a15cbc5477cd252634d8.

**Limitations:** The complete archived /386 checker differs from the /341 SOURCE/AND3/XOR fixture and from any original unified R_mix341 system. The archive's own charge parity self-test can have graph-geometry defects; no new claim about all mathematical parity sources is made. Five gate owners with mostly unused facets are a presentation upper-bound witness, not a lower bound: the genuine source-bound W29 certificate remains available under free optimal proof selection. Logical paid work, certificate bit length, OS verification duration, construction time, critical span and peak space remain separate. Nothing here proves a superpolynomial all-rule minimum or the B3 machine bridge.

**Tracking:** P2-D1, full P2-C3, P2-B1, separate P2-B2/B3, P1-01/03/04 all remain OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** Existing five enabled roles, titles, schedules, Pacific timezone, original weights, ownership boundaries and historical exactly two Route A / three Route B remain unchanged. No automation modified. Root main.tex was not modified because complete content retrieval failed (fetched zero bytes with nonempty blob 4bec8399c9252f25853fdb87adcab9be988d82da).

**Next target:** Recover a *single authoritative historical checker* accepting a source-bound RES-to-AND3 or paid DEF-to-LOCAL-CONVERT dependency, not a two-checker polyglot; run positive mixed-rule accepted-byte and wrong-port controls before extending this quotient or proving mixed-calculus abstraction inclusion. **P versus NP remains OPEN.**
