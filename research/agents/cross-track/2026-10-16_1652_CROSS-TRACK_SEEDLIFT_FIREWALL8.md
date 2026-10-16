# CROSS-TRACK SYNTHESIS: SEEDLIFT-FIREWALL8

**Run:** 2026-10-16 16:52 Asia/Seoul  
**Scientific status:** New restricted seed-length obstruction and input-normalization correction. **P versus NP OPEN.**

## 1. Four proposed combinations, fixed before searching

1. **Proof Transport + Resource Contraction:** Re-express GPW-RELATION1's communication bound using the *actual full index-gadget input size*, not the original compiled 3-CNF length. Charge acquisition, output, and workspace for an explicit implementation.
2. **Proof Transport + WRAPPER/Nonrelativizing Simulation:** Restrict Bob's index tables to a public deterministic generator with a short privately held seed. Test whether the communication lower bound survives a seed-transfer protocol. Do not treat a hash as random information.
3. **Universal Obstruction + Resource Contraction:** Compare the same-input witness obstruction to parity-decidable Tseitin families with hard Resolution refutations and large untouched-clause residuals. Test the semantic bypass.
4. **META-LIFT + Proof Transport:** Ask whether a succinct index-gadget instance remains hard after replacing full independent tables with compact descriptors. Demand a separately proved succinct-preservation lemma.

These are separate hypotheses and not presumed correct.

## 2. Source audit

Direct GitHub reads:

- LSPV-1 **BRANCHFRONTIER1** (2026-10-16 06:12 UTC): at most Delta occurrences per variable implies m-Delta k untouched clauses after k restrictions, but semantic termination is expressly excluded. Source: research/agents/lspv-1/2026-10-16_0612_LSPV-1_BRANCHFRONTIER1_HANDOFF.tex.
- LSPV-4 **SPARSECLOCK7** (2026-10-16 06:14 UTC): sparse accessible clock events defeat uniform polynomial padding reachability; hashes do not certify semantic SAT answers. Source: research/agents/nonrelativizing-simulation/2026-10-16_0614Z_SPARSECLOCK7_brief.txt.
- LSPV-3 **SOURCEPROBE19** (2026-10-16 15:35 KST): point-oracle common-input probe obstruction is exact, but compiling the point function into explicit Circuit-SAT exposes the hidden point. Source: research/agents/lspv-3/2026-10-16_1535_SOURCEPROBE19_CONDENSED.md.
- LSPV-2 **GPW-RELATION1** (2026-10-16 15:54 KST): source randomized query hardness to an exact-(2,2) compiled same-realization indexed false-clause search relation; uses an index table with width b=m^256; reports communication Theta(n log n), but does not claim SAT-time hardness. Source: research/agents/proof/2026-10-16_1554_PROOF-TRANSPORT_GPW_RELATION1.md.

Later project-chat summaries mention DUALCOST1 and QUOTEDIAGONAL8; their full bodies were not independently retrievable from GitHub or file search in this run. They are treated as supporting context only, not promoted into verified lemmas.

Google Drive: SIL-PR-20260918-PROOF-007 explicitly marks gadget-lifting/access transport as PROPOSED/NONCANONICAL; SIM-4-0006 and BIG_PICTURE2-0207 preserve the source-acquisition and oracle-scope caveats. Recent project chats include BRIDGE-SWITCH7's satisfiable parent with Resolution-hard restricted branch.

Primary references checked: Göös-Pitassi-Watson (2020), Urquhart (1987), Ben-Sasson-Wigderson (2001), Fortnow-Lipton-van Melkebeek-Viglas (2005).

## 3. Main exact lemma: SHORT-SEED-INDEX-FIREWALL8

Fix a public unsatisfiable CNF H with v variables and M clauses. Let b be an index-gadget width, with Alice holding pointers a_i in [b] and Bob holding b-bit tables y_i, i=1,...,v. The induced assignment is

z_i = y_i[a_i].

Let R_H(z) be the total search relation "output an index of a clause of H falsified by z".

Now restrict Bob's tables to a promise family admitting a *known exact generator*

Gen: {0,1}^s x [v] x [b] -> {0,1},

with one seed sigma of s bits: y_i[j] = Gen(sigma,i,j). Alice may hold arbitrary pointers.

**Theorem.** The deterministic *public-output communication complexity on this promise domain* is at most

D_cc(R_H o IND_b^v | Gen) <= s + ceil(log_2 M) + O(1).

**Proof.** Bob sends sigma (s bits). Alice already has every pointer a_i, so she locally computes z_i=Gen(sigma,i,a_i) for every i. Since H is unsatisfiable, at least one clause is falsified. Alice finds and returns its index, using ceil(log_2 M) bits, so both parties learn a valid answer. No probability, circuit-hardness hypothesis, or random-oracle claim is needed. QED.

**Corollary (necessary seed-length floor).** Any asserted Omega(v log b) communication lower bound *for this seed-restricted promise family* entails

s = Omega(v log b) - O(log M),

provided the formula has at most polynomially many clauses and all parties know the generator. In particular, seeds of O(log v), v^0.9, or any o(v log b) length cannot support a full-domain-scale lower bound on the seed-restricted relation.

**Important boundaries:** (i) The theorem is a promise-domain restriction, so it does not contradict full-domain GPW lifting. (ii) Communication complexity does not charge local generator evaluation. A SAT runtime argument MUST charge Gen evaluation, acquisition, and proof/output costs. (iii) The seed may encode a complex object; only its *bit length*, not its algorithmic acquisition cost, enters the communication bound.

### Application to GPW-RELATION1

For a connected cubic Tseitin source graph with n vertices and m=3n/2 edges, GPW-RELATION1's occurrence-halving compiler reports H with v=24m variables and M=32m clauses. Its canonical extension has four copies per edge and fixed-zero auxiliaries. The source-to-target index embedding duplicates source pointer/table values to the four clones and uses zero auxiliary tables.

A seed-generated source table family maps to an equally seed-generated target table family, because duplication and zero-padding are explicit local operations. The theorem therefore applies to the canonical *seed-restricted target relation*. Bob sends one seed, Alice reconstructs the target assignment, and a false target clause is identified.

Thus the existing full-domain Omega(n log n) GPW result remains valid, while its attempted continuation to a low-seed WRAPPER domain is **falsified** unless an additional hardness-preserving compression theorem is provided.

## 4. Input-length normalization correction

The original compiled 3-CNF has encoded size

L_H = Theta(m log m),

using v=24m variables and M=32m clauses.

The GPW index gadget in GPW-RELATION1 uses width

b=m^256.

The *physical indexed communication input* contains 24m blocks each with b Bob bits and ceil(log_2 b) Alice pointer bits:

G=24m(b+ceil(log_2 b))=Theta(m^257).

Its reported Theta(m log m) communication bound becomes

Theta(G^(1/257) log G)

when expressed as a function of the full gadget-input bit length.

It is therefore arithmetically comparable to L_H, but it is **not a linear lower bound in the actual indexed input length G**, and it is not an unrestricted SAT runtime lower bound. All acquisition and virtual-table read costs require separate accounting.

Any construction which explicitly writes the full index tables spends Omega(G) time and output bits. A virtual on-demand construction may avoid materialization but must prove that its compressed table distribution preserves the GPW relation lower bound. The short-seed theorem above supplies a direct counterexample to such a blanket preservation claim.

## 5. Hostile integration with other tracks

**Resource Contraction:** BRANCHFRONTIER1's inequality m-Delta*k counts clauses syntactically left after restrictions; it does not require a solver to visit any particular branch. The seed bypass incurs explicit s-bit communication and local Gen-query work, which must be included in any charged algorithm ledger. The source, full gadgets, and compact descriptors must not be assigned the same input-length variable.

**Nonrelativizing Simulation / WRAPPER:** A deterministic hash of a small trace/seed is an explicit generator, not a hardness certificate. The send-seed argument does not require any computational assumption. Timing and external bitstreams only change this conclusion if their *uncompressed* semantic information is essential and fully charged. SPARSECLOCK7 additionally rules out generic uniform polynomial pulse-reachability.

**Universal Obstruction:** SOURCEPROBE19 shows an oracle-only point-search obstruction disappears when the point is exposed by explicit source code. The current theorem gives a parallel failure mode in communication: oracle-like tables are hard on the full arbitrary domain but become inexpensive when sourced from an exposed short seed. Neither yields one explicit satisfiable input defeating all eligible UWI witness programs.

**Proof Transport:** The GPW-RELATION1 transport into randomized indexed search is valid within its defined interface. This run does not negate it. The missing arrow is from this communication relation to a mandatory artifact of an arbitrary polynomial-time SAT decider, with actual input size and acquisition work normalized. A restricted proof-system or relation lower bound cannot be silently substituted.

## 6. Computational falsification

Local reproducible Python audit: 2026-10-16_1652_succinct_index_firewall_audit.py. Results: 2026-10-16_1652_succinct_index_firewall_results.json.

For K4, triangular prism and Q3, across b=16,64,256, seed-generated SHA-256-indexed Bob tables were tested against 14,400 arbitrary pointer vectors. For each, the seed-transfer reconstruction found a genuinely false Tseitin clause for the odd-charge source, and an abstract four-clone plus zero-auxiliary embedding preserved every induced bit. 43,215 assertions passed. The finite test uses an abstract canonical extension, NOT a full reimplementation of the exact-(2,2) source compiler; asymptotic results follow from the proof and GPW theorem, not numerical extrapolation.

A separate symbolic check uses b=m^256 without materializing the table, confirming full indexed input Theta(m^257) versus short seed protocol O(log m).

## 7. Explicit proof DAG

| Node / arrow | Status |
|---|---|
| Odd-charge expander Tseitin is Resolution-hard | KNOWN |
| GPW full-domain query-to-communication lifting for index gadget | KNOWN |
| Project's exact-(2,2) source-to-target search relation embedding | SCOPED PROVED in GPW-RELATION1 |
| Short seed Gen, arbitrary Alice pointers => s+O(log m) public-output protocol | PROVED HERE |
| Full index input size Theta(m^257), not Theta(m log m) | PROVED HERE |
| Unrestricted full-domain GPW hardness persists under arbitrary succinct generator | FALSIFIED in general |
| Syntactically large residual => mandatory SAT decision cost | FALSIFIED by parity/bridge controls |
| Hash/timer provenance => required nonrelativizing semantic hardness | OPEN; proposed automatic versions FALSIFIED |
| UWI same-input satisfiable obstruction across entire eligible portfolio | OPEN |
| Every arbitrary polynomial-time SAT decider must emit indexed false-clause/search/proof artifact | OPEN |
| Fully charged universal time-space contractor with model-matched forbidden endpoint | OPEN |
| P != NP | **OPEN** |

## 8. Next specialist assignments

1. **Proof Transport:** Re-state every GPW lower bound with both physical gadget input length G and original CNF length L_H. Attempt a source-dependent mandatory relation extraction theorem, or exhibit a stronger invariant than full-domain communication complexity that survives seed-generated tables.
2. **Resource Contraction:** Audit the two input interfaces under one ledger: explicit y tables cost Omega(G) generation/output; virtual Gen costs per query and seed acquisition. Compute the exponent transformation when all 24m blocks, cache state, clone maps and source accesses are charged.
3. **Universal Obstruction:** Seek source-visible common-input hardness, not hidden-point oracle hardness. Use short-seed exchange and source-polarity decoders as immediate adversarial controls for any candidate formula generator.
4. **Nonrelativizing Simulation:** Specify a genuinely necessary semantic property of ordinary SAT deciders that still survives padding, TQBF-oracle replay and short-seed reconstruction. Do not infer it from deterministic hash outputs or timing records.

**Single highest-value open arrow:** Give a *fully charged, source-dependent, hardness-preserving extraction* from an arbitrary SAT decider to an object whose lower bound applies under the **actual compact encoding and generator domain**. Without that theorem, GPW-RELATION1 is a meaningful restricted transport theorem but not a P versus NP separation route.

## 9. Primary references

1. Mika Göös, Toniann Pitassi, Thomas Watson. Query-to-Communication Lifting for BPP. *SIAM Journal on Computing* 49(4), 2020. doi:10.1137/17M115339X.
2. Alasdair Urquhart. Hard Examples for Resolution. *Journal of the ACM* 34(1), 1987. doi:10.1145/7531.8928.
3. Eli Ben-Sasson, Avi Wigderson. Short Proofs Are Narrow: Resolution Made Simple. *Journal of the ACM* 48(2), 2001.
4. Lance Fortnow, Richard J. Lipton, Dieter van Melkebeek, Anastasios Viglas. Time-Space Lower Bounds for Satisfiability. *Journal of the ACM* 52(6), 2005. doi:10.1145/1101821.1101822.

**FINAL-READBACK-SENTINEL: SEEDLIFT-FIREWALL8-PNP-OPEN**
