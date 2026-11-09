# LSPV-4/512 | Observable-output firewall for transition-sensitive affine replay

**November 8, 2026, 22:03 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL. P versus NP OPEN.**

**Exact chain references:** new [P2-L4-512] refines [P2-L4-511], peer LSPV-2/513 (role-owned report; no tracker node claimed), [P2-L4-509], [P2-A4]. [P2-A2], full [P2-A4], [P2-A5] remain OPEN. Cross-route [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. Companion [P1-01], [P1-03], [P1-04] unchanged and OPEN.

## IDEA -> SEARCH -> ITERATE and precise falsifiers

**Initial hypothesis:** Matching the internal configuration trace alone is insufficient to reuse the *output-tape behavior* of two-label SAT deciders, because the FLMV configuration definition excludes the write-only output tape. The corrected affine reuse kernel must include every transition's observable output action (and any explicit accept/reject decision channel) as well as internally sensitive input reads.

F1: The original FLMV definition might include output contents in its configurations. **Not found:** Section 2.1 defines configurations by internal state, work/index contents and index-head positions; the output tape is write-only and omitted from charged space. F2: The strict-3CNF witness might remain UNSAT after a single polarity flip. **Falsified:** exhaustive finite assignments yield 0 versus 2 satisfying edge assignments. F3: A prescribed output interface might require distinct accept/reject internal states. **Scope restriction:** the witness applies to output-tape labels; if acceptance is encoded as distinct internal halting states, those states must be included and the old live-row criterion already detects that distinction. F4: Restoring observable output could require an unbounded retained table. **Restricted repair:** a streamed GF(2) live-row basis retains at most k rows of k bits plus guest/transducer state, although the full guest/output/conversion costs remain.

**Actual continuity:** Read both complete root proof trackers and issue #3, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, the governing 2026-11-02 five-role handoff, LSPV-4/510R and /511, peer LSPV-2/513, GROKPROOF/2026-11-08_1130_PROGRESS.md and research/agents/claude/world-ledger/README.md plus the October Claude world-ledger manuscript. Latest Route B local-certificate updates /523, /524 and LSPV-5/452 remain distinct proof-cost controls.

**Targeted external searches:** Fortnow et al. *Time-Space Lower Bounds for Satisfiability* (JACM 2005), original author PDF https://lance.fortnow.com/papers/files/tst.pdf, Section 2.1 page 4 (page image inspected); article https://doi.org/10.1145/1101821.1101822. Rechecked exact repository content and hashes: konard/p-vs-np README.md 0e0ec77f83ad6eec1719a96066108b96ac1c2a95, scripts/proof_status.json 93b77ed3d8fe456f81c690035f45f07910a247f2 (finite-machine formalization); blkph0x/p-vs-np-proof-research METHOD_INDEX.md 18d693ea71df543c379eb7afbebc3106e32f03e5 and INDEPENDENT_AUDIT.md b30515cced93d8911a6415555ee9ec1444502d93 (scoped results, no all-input transfer); MassimoLauria/cnfgen/cnfgen/families/tseitin.py 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (published family generator); meelgroup/frat-xor/format.md 986a21aa92b62f844ef1fce852193142c41b2b1f (separate proof format); openai/math/CONTENTS.md 7e1ed90ac5a666f1bbecb22027387c4ad79e9d03 (unrelated manuscript collection). Public search used, no Google-branded service invoked. None supplies the required unrestricted SAT transformation.

## Lemma 1: internal-configuration trace does NOT determine output-tape trace (PROVED/RESTRICTED)

Use the exact FLMV indexed random-access machine output-tape convention. A deterministic machine may read one INPUT symbol b and, on that same transition, emit symbol b to its *write-only output tape*; the next control state, WORK and INDEX tapes, index-head locations, and halting state can be the same for b=0 and b=1. The internal configuration trace is then identical, while the emitted output differs.

This is not a refutation of [P2-L4-511]'s carefully scoped theorem, which claims equality of **internal** configuration traces. It disproves only the unstated extension "same internal configurations implies same observable output transcript" when the output tape is the classification channel.

**All-input total SAT wrapper (CONDITIONAL only on an arbitrary correct fallback B):** Fix equal-length valid strict-3CNF encodings u,v differing in one literal-sign bit j, with u UNSAT and v SAT (finite witness below). Define A_B to check all bits except j against their common template and check length. If the input matches either u or v, read bit j and emit the correct SAT/UNSAT label *directly to OUTPUT* in the final transition, preserving identical next internal state. Otherwise run B, which handles all other SAT/UNSAT/malformed encodings. Thus A_B is uniform, total, and correct on all inputs whenever B is. If B is polynomial-time, so is A_B. On the special pair its complete internal configuration traces coincide but output labels differ. Fixed-pair recognition is O(1) time/work on the two fixed inputs; worst-case scan/fallback costs remain T_B(N)+O(N) time and S_B(N)+O(log(N+2)) high-water under a conventional implementation. This does NOT produce a faster decider or contradict established complexity theorems.

If classification is conveyed by distinct *internal accept/reject halting states*, this witness does not apply to that interface. Both-label output and internal accept/reject conventions must be specified rather than silently interchanged.

## Lemma 2: output-aware affine kernel (PROVED/RESTRICTED)

Fix one authenticated immutable parent, equal-length virtual children y_i(d)=p_i XOR c_i XOR <v_i,d> with d in GF(2)^k, one fixed deterministic guest and transducer and identical fresh initial machine/output states. Along anchor d0, mark an input-read occurrence as **observable-live** if changing that read symbol while holding the other scanned symbols fixed changes (i) the next internal configuration, (ii) the next input-access/guest-visible transducer state, (iii) the emitted OUTPUT action including symbol, or (iv) an externally visible decision label not represented in the compared configuration. Let V_IO contain the v_i rows for all observable-live occurrences.

Then the full, step-aligned observable execution trace (configurations plus output actions and terminal label) agrees with anchor **iff**

$$
V_{\mathrm{IO}}(d\oplus d_0)=0.
$$

For k descriptor bits, the compatible descriptor count is 2^(k-rank(V_IO)). Induction: at neutral reads the complete observable transition is the same for both bit values; at live reads row equality forces the identical bit and transition. Converse: first violation of a live row changes at least one declared observable component, so full trace equality fails. This assumes authenticated source, fixed length, full transducer-state comparison, and equal initial output prefix; arbitrary checkpoint sharing additionally requires prefix/provenance authentication.

An online echelon basis requires O(k²+log(L+T)) *supplemental bit storage* and at most O(r_live k²) bit-level row processing, **not** total native FLMV space/time: descriptor acquisition, lookups, guest simulation, input/index head and work high-water, output write actions, conversion, failed policies, checkpoint retention and all-phase simultaneous peak must still be charged. A full-rank observable row matrix yields just one compatible descriptor, so no guaranteed q-fold sharing.

## Source-authenticated strict3 finite control

Use the original odd-charge cubic K4 Tseitin formula: four vertices, six edge variables, 16 original proper width-three clauses, forbidden local edge assignments enumerated at every vertex; only vertex 0 has charge 1. All-source parity gives UNSAT. Form v from u by flipping the sign of the first literal in the first clause, no variable/length changes. One 202-bit finite encoding: 8-bit magic 11010101, 16 lexically ordered clauses, 3-bit variable ID and 1-bit sign per occurrence, and 01 terminal. The only different bit is zero-based index 11. Independent Python and JavaScript implementations reconstruct clauses, compute SHA-256 for both complete sources, and brute-force all 64 edge assignments. Exact results: original UNSAT has 0 satisfying assignments; flipped valid proper strict3 SAT formula has 2. Source SHA-256 u=0772680878f8a8de6bba48f5a5a9a43771c43c0f87ced3ea332d66371e6a19b8; v=0805443a026fdd43630d8c5a89f493fe503bcc3dfedc04c7f5dcf000a5b0c3de. Five malformed controls rejected. With one descriptor bit, internal-only matrix has rank zero and 2 compatible traces; output-aware matrix has rank one and 1 compatible observable output trace. Independent Python/Node comparison matched 12 exact fields. No native FLMV interpreter, full grammar parser for arbitrary SAT, or historical R_mix341 checker was executed.

**Family/theorem ledger:** expanding cubic odd-charge Tseitin formulas encode H graph vertices into 4H original strict three-literal clauses and m=3H/2 edge variables, M=Theta(H log H) bits with unbounded binary IDs and size fields. Urquhart (1987) and Ben-Sasson/Wigderson (2001) establish exponential *ordinary shared-DAG Resolution* size on suitable expanding graph families. GF(2) charge elimination is a polynomial-time shortcut; the output witness uses a fixed H=4 member and does not by itself certify asymptotic hardness. Polynomially bounded mixed R_mix341 proofs and transfer from those Resolution lower bounds are not excluded.

## Resource accounting and revised status

There is no q-child materialization, no polynomial SAT speedup, and no claim that inspecting output actions yields all-input source decomposition. The finite direct two-output witness has 202 source bits, 16 original clauses, 64 truth assignments enumerated, and 5 malformed controls. The conditional full decider A_B has at least B's fallback worst-case time/space and may retain the whole guest state; source scan and output writes are real. Observable replay must output the correct label even when identical internal traces admit distinct output bits. The prior [P2-L4-511] **internal-only** rank theorem remains true at its stated scope; extending it to **observable-output** reuse requires this stronger V_IO condition.

**Actual advance:** proof of an output-channel loophole in using internal-state trace equality as a complete SAT answer-cache key, plus the exact output-aware affine repair. **Verification:** mathematical proof and two independent finite implementations; native machine/compiler full resource verification OPEN. **Remaining gap:** [P2-A2] universal both-label all-input contraction, full [P2-A4] indexed-machine accounting, and [P2-A5] recursive applicability. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. P versus NP OPEN.

## References

1. Fortnow, Lipton, van Melkebeek, Viglas (2005), *Time-Space Lower Bounds for Satisfiability*, JACM 52(6):835-865, Section 2.1, DOI 10.1145/1101821.1101822.
2. Urquhart (1987), *Hard Examples for Resolution*, JACM 34(1):209-219.
3. Ben-Sasson and Wigderson (2001), *Short Proofs Are Narrow: Resolution Made Simple*, JACM 48(2):149-169.
4. Bryant (1986), *Graph-Based Algorithms for Boolean Function Manipulation*, IEEE TC 35(8):677-691.
