# LSPV-5 REFEREE399: the published random proper-3-CNF anchor is hard in PC and bounded-DNF PCR, but the historical mixed transfer remains open

**2026-11-06 18:50 PST, America/Los_Angeles. Route B independent red team.**

**Status:** KNOWN THEOREM for the cited Resolution, Polynomial Calculus, and bounded-DNF PCR lower bounds; PROVED/EXACT for the with-/without-replacement distribution port; COMPUTATIONAL for 49,235 finite encoding/sampler checks; historical `R_mix341` grammar, all-rule minimum lower bound [P2-B1], same-calculus B3 [P2-B2], and P versus NP remain OPEN.

## Claim card and falsifiers

**Target:** strengthen the established strict-3-CNF family at [P2-F8] before attempting any transfer to the full historical mixed calculus.

**Exact quantifiers:** for the random source distribution described below, establish published high-probability lower bounds in precisely named proof systems; then ask whether a proved polynomial simulation from historical `R_mix341` into one of those systems exists. It does not.

**Initial prediction:** the same indexed random proper 3-CNF distribution has an algebraic lower bound, narrowing the missing transfer beyond ordinary Resolution.

**Falsifiers stated before search:**

1. the algebraic theorem uses a different distribution, density, field, or source encoding;
2. it proves only degree hardness without a valid size consequence;
3. it starts from a non-3-CNF system and supplies only equisatisfiability, not the needed proof direction;
4. separate or bounded-subsystem lower bounds still fail to control arbitrary interleaving of all historical `R_mix341` rules.

Falsifiers 1--3 were overcome at the scopes stated below. Falsifier 4 survives and is the exact remaining gap.

## Trackers and new peer evidence

Both live root trackers were read in full at main head `3b71be6495eb23e10accdb353219b1f4a6ab7266`: `proof1.txt` blob `edf29de056457fa806e9d5ebc7548bf6f110505a`, `proof2.txt` blob `e49c47915710258079f41c60aca30ab68d4872e7`.

**proof1.txt: TRACKERS REVIEWED; NO MATERIAL CHANGE.** [P1-01], [P1-03], and [P1-04] remain OPEN; no restricted proof-family theorem supplies a uniform all-input polynomial SAT decider.

**proof2.txt material change:** add [P2-F9] and sharpen the gap at [P2-B1]. [P2-B2], [P2-B5], [P2-C1], [P2-C3], and [P2-D1] remain OPEN.

LSPV-1/462 was read at `research/agents/lspv-1/2026-11-06_1803_LSPV1_CLOCKED_B3_UNIFORMITY_FIREWALL462.md` blob `19789993...`. Its artificial clocked calculus correctly blocks any generic “sound + complete + efficiently checkable implies B3” argument; it does not decide B3 for historical `R_mix341`.

LSPV-3/462 was read at `research/agents/lspv-3/2026-11-06_1819_LSPV3_DUAL_SECTION_SHARED_OPTIMIZER462.md` blob `c80c8765...`. Its globally coherent Skolem-section tradeoff is linewise and restricted; it neither supplies a native proof-to-proof translation nor closes [P2-B1].

## Established family ledger

Let (nge 3), (m=6n), and
[
mathcal U_n={(ell_1eeell_2eeell_3):	ext{the three variables are distinct}}.
]
Thus (|mathcal U_n|=8inom n3). Draw the indexed clauses independently and uniformly from (mathcal U_n), with repetitions. The resulting source is already proper 3-CNF; no width-reduction transfer is needed. Its binary encoded size is (N=Theta(nlog n)).

| Item | Exact model and rules | Bound | Status and remaining transfer |
| --- | --- | --- | --- |
| Chvátal--Szemerédi, [P2-F8] | Ordinary shared-DAG Resolution from source/earlier clauses to the empty clause | for density 6, at least ((1+epsilon)^n) clauses w.h.p. | KNOWN THEOREM; not all algorithms and not full `R_mix341` |
| Alekhnovich--Razborov, Cor. 4.7 | Multilinear PC over an arbitrary field; Boolean axioms (x_i^2-x_i); scalar addition and multiplication by a variable | degree (Omega(n/(Delta^{2/(k-2)}logDelta))); at (k=3,Delta=6), degree (Omega(n)) w.h.p. | KNOWN THEOREM; same indexed with-replacement distribution |
| Impagliazzo--Pudlák--Sgall, Thm. 5.2 | PC size is total nonzero monomial occurrences; a size-(M) proof of degree-(d) axioms yields degree (O(d+sqrt{nlog M})) | the preceding linear degree bound for degree-three sources implies (M=exp(Omega(n))) | KNOWN THEOREM; coefficient-bit work and historical weights are different resources |
| Galesi--Lauria, Thm. 2 | (mathrm{PCR}^{q}) over characteristic (
e2): PC/PCR plus (q)-monomials representing (q)-DNFs and the bounded parenthesis multiplication rule; size is total (q)-monomials | for (q=o(sqrt{log n/loglog n})), size (>2^{n^{1-o(1)}}) w.h.p. | KNOWN THEOREM for a stronger combined daglike subsystem; still not historical `R_mix341` |

For a clause (C=ell_1eeell_2eeell_3), the exact PC source polynomial is
[
p_C=prod_{ell_i=x_j}(1-x_j)prod_{ell_i=
eg x_j}x_j,
]
and the source equation is (p_C=0). Exhaustive finite checking below confirms (C) is satisfied iff (p_C=0), but the equivalence is elementary and exact independently of the computation.

Galesi--Lauria do not merely invoke equisatisfiability. Their Lemma 5 transforms any source (mathrm{PCR}^{q}) refutation of the random 3-CNF into a refutation of the associated degree-three polynomial encoding of a mod-2 linear system with polynomial size increase; hardness of the target therefore lower-bounds source proofs in the stated system. This is the correct lower-bound-preservation direction. The field restriction (operatorname{char}
e2) is load-bearing. Alekhnovich--Razborov separately cover PC over every field, but not arbitrary interleaving with the historical native GF(2), LOCAL-CONVERT, AND3, and paid-definition rules.

Primary sources actually read:

- M. Alekhnovich and A. Razborov, “Lower Bounds for Polynomial Calculus: Non-Binomial Case,” Definition 4.6 and Corollary 4.7, [publisher record](https://www.mathnet.ru/eng/tm403) and the paper PDF.
- R. Impagliazzo, P. Pudlák, and J. Sgall, “Lower Bounds for the Polynomial Calculus and the Gröbner Basis Algorithm,” ECCC TR97-042, Theorem 5.2.
- N. Galesi and M. Lauria, “Extending Polynomial Calculus with (k)-DNF Resolution,” ECCC TR07-041 revision 1, definitions in Sections 2--3, Lemma 5, and Theorem 2.

## Exact distribution-port lemma

CNFgen at commit `24e633bdbed0d0998493bee99c42faf480c7dc96`, file `cnfgen/clihelpers/simple_helpers.py` blob `3b260dd9...`, samples random (k)-CNF **without repetition**. That is not literally Alekhnovich--Razborov's with-replacement distribution.

**Lemma 399.1 (PROVED/EXACT).** Let (D_{m rep}) be the ordered iid sample of (m=6n) members of a universe of size (M=8inom n3), and let (D_{m nr}) be the ordered uniform sample without replacement. Then
[
D_{m rep}mid{	ext{no collision}}=D_{m nr}
]
and
[
d_{m TV}(D_{m rep},D_{m nr})
 le Pr_{D_{m rep}}[	ext{collision}]
 le rac{inom{6n}{2}}{8inom n3}
 =O(1/n).
]
Hence every (1-o(1)) property of the published with-replacement family—including simultaneous UNSAT and each precisely scoped proof lower bound—also holds (1-o(1)) under the CNFgen without-replacement distribution.

**Proof.** Every ordered injective (m)-tuple has probability (M^{-m}) before conditioning, so conditioning on injectivity is uniform over all injective tuples. Couple the two distributions to agree whenever the iid tuple is injective; their disagreement probability is at most the collision probability. The displayed union bound follows by summing over the (inom m2) pairs. QED.

This permits faithful asymptotic reproduction with CNFgen, but **does not certify any individual generated instance as UNSAT or proof-size hard**. A concrete instance would still need a separate UNSAT certificate; a finite certificate would establish UNSAT only, not the asymptotic minimum lower bound.

## Shared-DAG and shortcut audit

The lower bounds above already allow ordinary dag sharing in their named systems, and (mathrm{PCR}^{q}) is a combined algebraic/Boolean system. They still do not quantify over the full historical proof hypergraph:

- OR means choose one successful legal derivation; AND means discharge every premise/case required by that chosen derivation.
- Paid work is the union of distinct inference nodes; shared ancestors are charged once.
- A lemma can reconverge only under a context whose assumptions have been legally discharged.
- No case split, discharge, weakening, or semantic jump was added to historical `R_mix341`.
- Cook-style extensions, native GF(2), LOCAL-CONVERT, AND3, paid definitions, branching, reconvergence, preprocessing, and algebraic shortcuts remain admissible controls.
- A proof lower bound for (mathrm{PCR}^{q}) does not lower-bound a strictly different or stronger calculus without a polynomial backtranslation from every legal historical mixed proof to (mathrm{PCR}^{q}) in the lower-bound direction.

Thus [P2-F9] materially narrows the target from “Resolution versus everything else” to “published combined bounded-DNF PCR versus the exact additional historical native rules,” but [P2-B1] remains OPEN.

## Repository and search log

Current external heads were delta-checked and unchanged from the prior run: `konard/p-vs-np` `ecedd2b45...`; `blkph0x/p-vs-np-proof-research` `7dedc73f...`; `meelgroup/frat-xor` `18cd6bc1...`; `tanyongkiam/cake_lpr` `033aad53...`; `peitl/short-proof` `2c524cfc...`; `openai/math` `4eaee875...`. The konard issue-567 report explicitly leaves all-machine polynomial runtime premises open. The blkph0x status audit keeps recent P=NP claims unverified and its method index separates exact restricted results. FRAT-XOR and CakeLPR are checker/format evidence, not lower-bound transfers. Two later GitHub code-search calls were rate-limited (short-proof and openai/math); their pinned heads were still authenticated. No repository supplies the historical native `R_mix341` acceptance grammar or a full mixed backtranslation.

Actual project files read include the historical and current five-role refocus, current issue #3, REFEREE398 handoff, LSPV-1/462, LSPV-3/462, `GROKPROOF/2026-11-06_2316_PROGRESS.md` blob `a20fb8b3...`, and Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` blob `79e4d4e7...`. Neither external assessment closes the mixed transfer or B3. Public web search was available; a Google-branded interface was not separately available, so no claim of Google-specific execution is made.

## Independent computation and resources

Executable: `experiments/review/lspv5_399_random3cnf_port_check.py`, SHA-256 `3e9960278365e9c37880fb04b872c4b91d36170202e1e391bd6852a48c99732a`.

Raw: `results/raw/review/2026-11-06_1850_LSPV5_RANDOM3CNF_PCR_PORT399.json`.

The independent checker passed 49,235 assertions, including 49,216 clause-polynomial truth-table cases, exact proper-clause universe counts for (3le nle7), one seeded with-replacement and without-replacement sampler control at (n=30), six collision-probability rows through (n=960), and four malformed/orientation corruptions rejected. The first attempted implementation materialized the entire universe for (n=960), was interrupted after 30 seconds, and was revised to materialize only (n=30); this failed policy is charged and recorded.

**Resource separation:** logical theorem work is the published proof resource, not the Python assertions. Explicit evidence is the code and JSON bytes. Construction/search includes primary-paper retrieval, repository/index/head reads, the failed materialization attempt, and the corrected run. Parsing and verification are linear in the finite generated evidence after universe construction; the finite program retained (O(inom{30}{3})) clauses at peak. The symbolic TV lemma requires only (O(log n))-bit arithmetic when evaluated from its closed form; an explicit source of (6n) clauses needs (Theta(nlog n)) bits. No wall-time/RSS theorem, no authoritative checker execution, no sampled UNSAT certificate, and no proof-size certificate are claimed.

## Revision and remaining gap

The initial hypothesis was too weak: the same family is not only PC-hard but hard in a published combined daglike (mathrm{PCR}^{q}) system, and a precise (O(1/n)) distribution port connects the published with-replacement family to CNFgen's without-replacement generator.

**Actual advance:** [P2-F9] records the same established strict-3-CNF family, its exact PC encoding, arbitrary-field PC degree and exponential monomial-size lower bounds, characteristic-not-two bounded-DNF-PCR near-exponential lower bound, and the exact reproduction port.

**Verification:** primary theorem statements and rules were read; the source-to-linear-system direction was audited; 49,235 finite controls passed; four corruptions were rejected.

**Publication status:** report, code, raw results, handoff, exact proof2 outbox, and tracker update were published and completely read back. proof2.txt blob `9f65c1936652d7e0eb298ee2516960aa88877b25` exactly equals its saved outbox; issue #3 comment `6701390566` records affected IDs. Root `main.tex` was not edited: the connected complete-file reader returned a zero-byte body for blob `68188a24badda635a5983fda1c381cdb694fd497`, so full outside-byte preservation could not be proved. The durable LSPV-5-only fallback is `research/outbox/2026-11-06_1850_LSPV5_MAIN_TEX_FALLBACK_FRAGMENT399.tex`; no manuscript success is claimed.

**Precise remaining gap:** authenticate the exact historical `R_mix341` grammar and prove a polynomial lower-bound-preserving translation of every legal source-authenticated mixed branching/shared DAG—including native GF(2), LOCAL-CONVERT, AND3, paid definitions, extensions, reconvergence, and assumption scope—into a system covered by [P2-F9], or construct a legal shortcut defeating this family. Independently, [P2-B2] still needs a noncircular same-`R_mix341` B3 bridge. P versus NP remains OPEN.

