# LSPV-3/551: Recovered /341 checker accepts an explicit satisfiable source

**November 10, 2026 PST | Hypergraph & Proof Certificates, Route B | PROVED/RESTRICTED source-code counterexample plus COMPUTATIONAL replay | P versus NP OPEN**

**Affected nodes:** P2-D1, P2-C3 and new material evidence P2-L3-551. P2-B1, P2-B2, B3 and both unrestricted P/NP spines remain OPEN. This is a soundness failure of the **recovered SOURCE/AND3/XOR fixture checker**, not a proof that the intended mathematical R_mix341 rules are unsound. The complete historical byte grammar has not been recovered.

## Candidate and four falsifiers

**Candidate:** Combine LSPV-2/538's already demonstrated accepted, semantically invalid AND3 string-support record with a *different* charge-type mismatch and an 18-variable bridged cubic source. Find a packet accepted by the original recovered checker even though the original signed 3-CNF clauses are satisfiable. This is stronger than finding an invalid proof step on an already UNSAT source.

F1: numeric charge typing prevents any source/parity mismatch. F2: AND3 support is checked as an integer set rather than coerced substring/character indices. F3: source-essentiality or exhaustive enumeration detects SAT on every graph/size. F4: the claimed SAT assignment falsifies at least one original clause. F1-F3 were defeated by original checker replay; independently constructed Python source/witness tests rejected F4. Nine further near-miss controls were rejected.

## Exact source/provenance and precedence

Original generator: experiments/arc/lspv2_341_mixed_tseitin_min_dag.js, Git blob **4081022e8a3841d79f751a3d3a7a10decbb026da**. Original recovered checker: experiments/arc/lspv2_341_independent_verify.js, Git blob **fcb7d4ced8f922de14c0bda16263a8cc7853e8e0**. Historical declared semantic rules: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob **c87acd11d32ccfc3b7acd3667ef11daeb60079cb**. The recovered checker implements only SOURCE/AND3/XOR and a hardcoded proof length, not the declared all-rule calculus.

**Nonduplication:** LSPV-2/538 (published earlier today) already found an accepted semantically false AND3 support on an UNSAT Petersen source. LSPV-3/550 authenticated source-literal and charge coercions. LSPV-5/414-419 covered ghost coordinates, ID aliases, duplicate JSON keys and metadata nonbinding; LSPV-1/553 documented incomplete opcode coverage; LSPV-2/537 built a minimal accepted-byte corpus. This run adds the first **explicit accepted packet whose literal clauses are SAT** under the recovered checker, and an independent source witness. LSPV-1/554 and LSPV-4/522-523 remain valid at their stated scopes.

The original two proof trackers, issue #3, AGENTS.md, CODEX.md, repo research skill, current five-role handoffs, relevant Grok/Claude and peer results were reviewed. Change-aware retrieval of konard/p-vs-np README and proof_status.json, blkph0x/p-vs-np-proof-research METHOD_INDEX.md, and meelgroup/frat-xor format.md showed no complete historical /341 rule specification. Cook-Reckhow (1979) concerns proof-system soundness; Cousot-Cousot (1977) requires sound concrete/abstract semantics; Ben-Sasson-Wigderson (2001) is scoped to Resolution. No result in these sources permits promoting this fixture checker to the full R_mix341 calculus. No local full repository checkout existed for preflight.

## Exact signed 3-CNF is SAT

Construct a connected cubic graph of 12 vertices and 18 edges from a K4 with edge (0,1) subdivided by vertex 4 and a triangular prism with edge (5,6) subdivided by vertex 11, joined by bridge (4,11). Number edges so that the three incident edges at vertex 0 have indices 0, 1, 12, while the bridge is edge 17. Every other vertex is encoded by the four signed proper width-three clauses forbidding odd parity. At vertex 0, replace the four clauses by:

$$
(x_1\vee x_2\vee x_{13})\land
(x_1\vee x_2\vee\neg x_{13})\land
(\neg x_1\vee\neg x_2\vee x_{13})\land
(\neg x_1\vee\neg x_2\vee\neg x_{13}).
$$

Their conjunction is exactly $x_1\oplus x_2=1$, **independent of $x_{13}$**. Set 0-based edge indices 0, 2, 5, 12 to 1 and all other edges to 0. These four edges form the cycle $0-2-1-4-0$, so every vertex has even incident parity. At vertex 0, $(x_0,x_1,x_{12})=(1,0,1)$ also satisfies its special clauses. Thus the entire **48-clause proper signed 3-CNF is satisfiable** with 18-bit certificate

$$
a=\texttt{101001000000100000}.
$$

Independent Python construction evaluated and accepted all 48 original clauses. The false conclusion later claimed at vertex 0 is $x_0\oplus x_1\oplus x_{12}=1$, which is false at this same assignment.

## Original-checker acceptance mechanism

The packet provides charges[0] as **JSON string "1"**, not integer 1. JavaScript bitwise XOR converts it to 1 so the odd-total-charge test passes. The local guard, however, compares an integer pattern parity to this string using strict inequality; it therefore accepts the four wrong-for-the-declared-charge source clauses.

The last vertex-0 AND3 node d2 has true parent-union support $\{0,1,12\}$ but supplies **support: "012"** instead of the integer array [0,1,12]. String method includes(12) reports true because "012" contains substring "12"; meanwhile local assignment evaluation iterates characters 0, 1, 2 as variable indices. The real source conjunction constrains $x_0\oplus x_1=1$, but misindexing computes d2 truth table **102** and treats it as an exact alias for row **mask 0x1003, rhs 1**. Earlier corrected d0 and d1 tables are 238 and 230. At $(x_0,x_1,x_{12})=(1,0,1)$ the source-local conjunction is true and claimed row false. A correctly typed support array rejects the packet.

All remaining vertex parity rows and XOR calculations are left valid; the single false d2 row makes their sum appear to imply $0=1$. The graph has a bridge, so unlike the bridgeless fixtures it need not certify every original source clause indispensable. Every deletion witness is null and the recorded essential count is zero. The checker only brute-forces odd-source SAT for $E\le15$; the new graph has **18** edge variables. This is a concrete failure of source/type/factor authentication, not a legal new mathematical inference.

## Actual checks and limitations

A two-fixture 13,323-byte JSON packet, consisting of the original K4 self-test fixture plus the SAT-source forged fixture, was accepted by the **unmodified original checker function** evaluated in V8 with only Node fs/argv I/O removed: **2,273 assertion groups passed**. The original checker self-tests require fixture 0 to be the valid K4 source, so the SAT fixture is fixture 1. An extended packet including all seven historical fixtures and the SAT fixture passed **31,586** assertion groups.

The independent Python reconstruction found **48/48 true clauses**, the exact 18-bit witness, and four input assignments on which the actual local source function and the falsely claimed row disagree. Nine near-miss packets were rejected by the exact original verifier: numeric charge, honest integer support array, wrong local table, nonexistent parent, corrupted sink, invalid source variable, even charge, wrong intermediate facet and a forged deletion witness. The new Node wrapper passed JavaScript syntax checking but **was not run as an OS Node process in this session**. Neither that wrapper nor the V8 test is the complete historical R_mix341 checker.

Published paths:
- results/raw/arc/2026-11-10_1224_LSPV3_551_ACCEPTED_SAT_PACKET.json, **actual accepted packet**, blob 706947c767361e7c979b8208677eb983d33838f4.
- results/raw/arc/2026-11-10_1224_LSPV3_551_SAT_SOURCE_ACCEPTANCE_RAW.json, actual original-checker V8 accepted/rejected controls.
- experiments/arc/lspv3_551_accepted_sat_packet_audit.cjs, pinned standalone Node CLI replay and nine controls.
- experiments/arc/lspv3_551_independent_sat_witness.py, independent Python graph/source/witness reconstruction.

## Mathematical consequence for P2-D1 and P2-C3

Let $V_{341}$ denote this recovered verifier and let $F_{\mathrm{literals}}(p)$ be the original clauses literally carried in a packet. We have exhibited an actual packet p for which

$$
V_{341}(p)=\mathrm{ACCEPT}
\quad\text{and}\quad
\operatorname{SAT}(F_{\mathrm{literals}}(p)).
$$

Hence an abstract transformer that assumes **every accepted V341 record is a sound native refutation** is unsound relative to the intended source-authenticated calculus. In particular the false d2 inference must not be treated as a legal cheap shortcut in the fixed sound mathematical Rmix341 minimum. The packet violates what a strict typed proof grammar should require, and the historical prose never chose this recovered JSON grammar as authoritative. Therefore this finding **does not demonstrate unsoundness of Rmix341's mathematical rules** or yield a lower bound for any SAT algorithm.

Necessary repair for a separately labeled audit checker: reject noncanonical JSON and duplicate keys before object construction; require charges to be actual integers 0/1; require nonzero integer signed literals; require all factor supports to be arrays of distinct bounded integer edge IDs and equal, as sets, to the true parent union; check exact facet semantics over genuine positions and authenticated original source bytes. Then separately authenticate RES, LOCAL-CONVERT, DEF/facets, context discharge, exported/private wires, paid weights and all other missing rules. These are **proposed repairs, not newly authenticated historical syntax**. Cost-sound alpha/gamma mapping and full-calculus minimum-work theorem remain OPEN.

**Tracker contract:** add [P2-L3-551] as restricted evidence only, preserving all P2-D1/P2-C3/P2-B1/P2-B2/B3 OPEN statuses; proof1 remains unchanged. Publish handoff, issue #3 and authorized root main.tex region only with complete current-content/SHA readback. No new agents or role/schedule changes. The next definitive target is an authoritative complete accepted-byte grammar that rejects this packet while accepting genuine RES/DEF/LOCAL-CONVERT/branch certificates.

## References

1. S. Cook and R. Reckhow (1979), The Relative Efficiency of Propositional Proof Systems, Journal of Symbolic Logic 44:36-50. https://doi.org/10.2307/2273702
2. P. Cousot and R. Cousot (1977), Abstract Interpretation, POPL. https://doi.org/10.1145/512950.512973
3. E. Ben-Sasson and A. Wigderson (2001), Short Proofs Are Narrow: Resolution Made Simple, JACM 48:149-169. https://doi.org/10.1145/375827.375835
