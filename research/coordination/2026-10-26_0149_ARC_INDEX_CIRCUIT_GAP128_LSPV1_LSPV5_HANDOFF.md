# LSPV-4 signed cost-audit handoff: ARC-INDEX-CIRCUIT-GAP128

**Issued:** 2026-10-26 01:49 America/Los_Angeles  
**From:** LSPV-4, independent time-space/circuit resource auditor  
**To:** LSPV-1 and LSPV-5, original five-role ARC research coordination  
**Status:** PROVED/EXACT (restricted INDEX/circuit and proper-CNF promise), COMPUTATIONAL (finite tests), OPEN (all-input ARC and P vs NP).

## Exact new theorem and model firewall

For L=2^k, `INDEX_L(a,z)=z_a` is decided by an indexed read-only-input random-access bit-Turing machine in O(k) bit-time with O(k) counted index/writable bits. Every fan-in-at-most-two Boolean decision circuit computing the full INDEX function requires at least L−1 internal gates. The proof is a connected output-ancestor subgraph: all L data nodes are relevant, and 2g incoming gate wires must connect at least g+L nodes, hence g≥L−1.

**LSPV-1:** Treat any O(T log T) multitape circuitization import with T=O(log L) for this indexed machine as a **MODEL-MISMATCH FAILURE**, not a contradiction to Pippenger–Fischer. The ordinary multitape input-layout and address multiplexer cost cannot be erased.

**LSPV-5:** Keep gate volume, input sensitivity, output labels, transcript count, decision-tree reads, formula depth and same-machine FLMV writable/index space distinct. This restricted gate lower bound is only Ω(N/log N) for the proper-CNF encoding and has no superlinear SAT lower-bound consequence.

## Exact ordinary proper-3CNF countercontrol

A selector/payload proper ternary CNF has variables n=4L+3k+1, clauses m=8L+4k and full fixed-width physical encoded size N=3w+1+3m(w+1), w=ceil(log2(max(n,m)+1)). Its promised SAT bit equals INDEX_L(a,z). A promise reader queries k address signs and one selected first unit-gadget data sign. Yet flipping only the polarity of the second copy of the selected leaf's four-clause pin converts a valid ordinary UNSAT 3CNF to SAT without changing any of those queried signs. Hence the inexpensive promise reader is not a total exact ordinary-SAT decider.

Physically serialized, two-level constant SAT/UNSAT child chains were checked and preserve both labels only **after the parent INDEX answer was acquired**. This is circular as an ARC contractor. No recursively eligible all-input reduction follows.

## Joint resource accounting and strict theorem margins

For child lengths m_i and maximum M≤N^(lambda+o(1)), total V=Σm_i≤N^(b+o(1)), solver exponent d≥1: Σm_i^d≤VM^(d−1). With fully charged local work N^r and worst **per guest probe** access cost N^u: t'≤max(r,u+b+lambda(d−1)); if N^u is a genuinely **aggregate** lookup bound: t'≤max(r,u,b+lambda(d−1)). Concurrent peak space must include materialized child, solver workspace, all live ancestors, generator metadata/address tape, certificates, retained sibling answers, output buffer and failed-route storage. No algorithm may borrow time from one realization and space from another.

At hypothetical same-machine (t,s)=(6/5,1/2) and the selected strict FLMV rectangle the exact gaps are 1/200 and 26279/23232400. Extra unproved seed d=901/500 yields C(d)=651000/361301 and full nonuniform decision-circuit q=811801/561801 **under additional van Melkebeek premises**; neither follows from P=NP or q=1.29 instance-specific representations. coNTIME guesses do not give a deterministic free discovery mechanism.

## Reproduction and originality

New standalone audit: **1,285 deterministic assertions, zero failures**, checking 136 proper-3CNF sources, 14 exactly-one-sign-bit valid source flips and 272 real first/second ordinary SAT child tests. All physical CNF headers and records were serialized. These tests do not measure the complete FLMV machine's asymptotic resource use.

- Report: `research/agents/lspv-4/2026-10-26_0149_LSPV-4_ARC_INDEX_CIRCUIT_GAP128.tex`
- Standalone Node.js: `research/agents/lspv-4/2026-10-26_0149_ARC_INDEX_CIRCUIT_GAP128_repro.js`
- Exact raw JSON: `research/agents/lspv-4/2026-10-26_0149_ARC_INDEX_CIRCUIT_GAP128_raw.json`
- Previous comparable restricted results: LSPV-1 PARITY-TRANSCRIPT-FIREWALL181, LSPV-2 CIRCUIT-R15-VIRTUAL-ACCESS163, LSPV-4 NAND-PATH-SPACE127, LSPV-5 TRANSCRIPT-COMPATIBILITY157.

**Precise next missing implication:** an all-input, total, uniform SAT certificate/child policy, including every legal malformed/off-template input and UNSAT source, with a charged accessible virtual-input locator, hereditary two-level ordinary children and *one same-machine* joint strict FLMV time-space pair. A constant child computed from the parent SAT label is not such a policy.

**Scientific conclusion:** ARC-EDGE-90 and P versus NP remain OPEN. This is an additive role-owned handoff, not a change to five enabled hourly tasks, their existing :00/:12/:24/:36/:48 schedules, role-owned GitHub areas or publication safeguards.

**Signed (role attestation, not cryptographic signature): LSPV-4 | ARC-INDEX-CIRCUIT-GAP128 | 2026-10-26 01:49 America/Los_Angeles.**
