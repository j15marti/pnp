# LSPV-2/467: failed input-head materialization firewall and model reconciliation

**2026-11-07 PST | Route A LSPV-2 | FALSIFIED/RETIRED initial hypothesis | COMPUTATIONAL corrected controls | P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis (RETIRED):** A guest writes m=n^k bits on its input INDEX tape, jumps its read-only INPUT head to 2^m-1, returns to zero, then invokes a correct SAT decider. A host materializing the guest input-head address on counted WORK requires m cells, apparently exceeding the guest's O(log n) counter memory.

**Four falsifiers, checked:** (F1) Guest writable INDEX tape high-water was not charged: **FALSIFIED** by the original FLMV Sec. 2.1 model and prior LSPV-4/273; (F2) no historical prior analysis: **FALSIFIED** by LSPV-4/256, /273 and /274; (F3) finite far-jump/label arithmetic inconsistent: **NOT OBSERVED** in 352 tests; (F4) naive full-binary guest head register exceeds *total* guest measured space: **FALSIFIED**, because guest INDEX space already exceeds m.

**Corrected restricted observation.** On a FLMV indexed-input machine, a sequential writable associated INPUT INDEX tape that visits m consecutive positions contributes at least m to space high-water, even if the indexed jump later erases it. The read-only INPUT tape itself is space exempt; its writable INDEX tape is distinct. If the guest constructs m=n^k consecutive one bits before jumping to address 2^m-1, then

$$
S_{\mathrm{guest}}(n)\ge m=n^k.
$$

A PARTICULAR host implementation that stores this exact address as an ordinary binary WORK register also needs m cells:

$$
S_{\mathrm{host\ register}}(n)\ge m.
$$

These two lower bounds alone show **no asymptotic extra register-space penalty** beyond this guest's already-charged INDEX extent. The original proposed separating witness fails. Under a child length B=N^{1/2+o(1)}, its apparent N^{k/2} register cost is matched by at least N^{k/2} guest INDEX space; it is impermissible to count only O(log B) ordinary counters when assigning guest exponent s.

This is not a universal guest-transducer theorem: an alternative compressed far-blank guard may avoid materializing a huge address; correctness of source-backed virtual INPUT access remains OPEN.

## Reproducible corrected finite checks

Executed the corrected self-contained V8 program at experiments/arc/lspv2_467_input_head_firewall.cjs, verified content blob SHA 2887764d10b60d12a12f1e4f7e5dc6b603b4e6e4. It tested 24 pairs with n in {2,3,4,6,8,12,16,24} and k in {1,2,3}; the largest case has 13,824 INDEX positions. It checked exact binary address bit lengths, erasure and reset semantics, equal m-sized guest-index and host-binary-register high-water. It independently enumerated the 16 original signed K4 Tseitin charge 3-CNFs: 8 SAT, 8 UNSAT; 64 corrupted/malformed inputs were rejected. **352 assertions PASS.** These are abstract host-language checks, not native FLMV executions or any arbitrary-SAT algorithm.

Original results/raw/arc/2026-11-07_LSPV2_467_INPUT_HEAD_FIREWALL.json incorrectly treated the writable guest INDEX tape as uncharged. This earlier raw artifact is preserved solely as an error record. Corrected results/raw/arc/2026-11-07_LSPV2_467_INPUT_HEAD_CORRECTED.json, Git blob 2236ed5c510cfc49bc2103066804a11f829afb39, SUPERSEDES it. GitHub code bytes were corrected and verified by complete readback. No new asymptotic theorem or native machine bound is claimed.

## Search, prior work, and mandatory controls

Primary FLMV source: Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6) (2005), Sec. 2.1, author PDF https://lance.fortnow.com/papers/files/tst.pdf (page 4 visually inspected). The paper distinguishes the free read-only INPUT tape from associated sequential writable INDEX tapes and states that configurations of space s have O(s) size. Earlier project report research/agents/lspv-4/2026-10-31_0606_LSPV-4_ARC_BOUNDED_GUEST_INPUT273.tex (blob fad21b399e0141dc4d442ff7390e798f10dded50) already explicitly charges M INDEX high-water. See also /256 (blob bc288e342185ab6a2fd3a012ce5193b5e77c4e44), /274 (blob 70a4ac0987fc289b5354a067a10e3e6d1e0a96c8). LSPV-2/466 WORK-index lift and LSPV-4/465 checkpoint tradeoff do not establish complete INPUT port virtualization.

Actually consulted: both complete root proof trackers, issue #3, November 2 five-role governing handoff, AGENTS.md, CODEX.md, repository pnp-research skill, Grok 2026-11-07_1119_PROGRESS.md (blob d87fcb3a12ed115c277f7ffda87ecca0f4072630) and Claude world-ledger README (blob de75a371ce3143a4495e6892df7fb04794a6b708). External repository files: konard/p-vs-np/proofs/complexity/README.md (blob 7ee9a11e434e358d25ca941f7ce5e01efa0b3ce3; different one-tape model), blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (blob 18d693ea71dfa433370eb7afbebc3106e32f03e5; restricted methods), meelgroup/frat-xor/format.md (blob 986a21aa92b62f844ef1fce852193142c41b2b1; distinct certificate grammar), openai/math/README.md (blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae; heterogeneous verification). General web search was used, but no separate Google-branded service was verified.

**Established hard-family ledger:** Odd-charge cubic expander Tseitin 3-CNF has H vertices, 3H/2 edge variables, 4H signed proper ternary clauses, and N=Theta(H log H) binary size. Odd total charge certifies UNSAT; appropriate expander families have 2^{Omega(H)} proof-size lower bounds under ordinary shared-DAG Resolution (Urquhart 1987, Ben-Sasson/Wigderson 2001), but GF(2) elimination decides them efficiently. No lower bound transfers to all SAT algorithms or historical complete R_mix341. K4 provides only finite labels. Haken PHP and Cook ER are distinct mandatory controls.

## Tracker review, actual status and next implication

Read complete proof1.txt (blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b) and proof2.txt (blob d8b1dff97e0b72d38473c550423f4a26a6f51acb). Relevant exact IDs: [P1-01], [P1-03], [P1-04], [P1-S3], [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-B2]. The attempted claim is retired by existing model accounting, with **no material change** to any tracker node or evidence status.

**TRACKERS REVIEWED; NO MATERIAL CHANGE.**

No tracker mutation was made. Root main.tex returned zero readable source bytes (SHA 68188a24badda635a5983fda1c381cdb694fd497); it was not overwritten. No native proof rule, weight, task schedule, identity, or existing 2 Route A / 3 Route B allocation was changed.

**Resource ledger scope:** the finite checks charge abstract guest INDEX positions, host counted binary register, exact address width and erased INDEX contents. There is no claim to all-phase source parsing, failed search, input-bit virtualization, native resets, construction, machine output, certificates, work/span or simultaneous peak on a complete wrapper.

**Next OPEN target:** a fully charged same-machine source-backed virtual INPUT access controller, including arbitrary INDEX-head excursions, read-only original source queries, guest WORK resets, and simultaneous peak space. Independently, source decomposition for ALL inputs and hereditary child applicability remain OPEN. Route B full mixed-calculus lower bound and noncircular B3 remain OPEN. **P versus NP OPEN.**
