# LSPV-3: RECURSIVE-FRONTIER-REPLAY260 (2026-10-30 16:24 PDT)

**Status:** KNOWN METHOD SPECIALIZATION with exact restricted proof, independent review pending; COMPUTATIONAL controls; all-input ARC/FLMV contraction OPEN, P versus NP OPEN.

## One theorem and full acquisition charge

For original clauses C_1,...,C_m in an acquired order, B_i denotes the shared variables between prefix i and suffix m-i, U_i=B_(i-1) union Vars(C_i), and w=max_i |U_i|. Each signed occurrence retains its original variable identity. The forward and reverse Boolean messages are

L_i(beta)=OR_{a on U_i, a|B_i=beta}[L_(i-1)(a|B_(i-1)) AND C_i(a)]

R_(i-1)(alpha)=OR_{a on U_i, a|B_(i-1)=alpha}[C_i(a) AND R_i(a|B_i)].

For each local source assignment u to Vars(C_i), the exact global-support bit is

H_i(u)=OR_{a|Vars(C_i)=u}[L_(i-1)(a|B_(i-1)) AND C_i(a) AND R_i(a|B_i)].

H_i(u)=1 exactly when u extends to a global satisfying assignment; H_i(u)=0 is a source-certified forbidden cube, NOT by itself formula UNSAT.

**Theorem (Hirschberg-style recursive replay):** On any interval (a,b] with authenticated global L_a and R_b, compute forward L_mid and reverse R_mid, recurse on both halves, and at singleton i join both messages with the original C_i. The outputs are exactly all H_i(u) and the formula answer. At most O(log m) frontier tables are simultaneously live. With source length N, maximum original clause width k, boundary-acquisition time d_i, and boundary iterator scratch S_B, the indexed-word bounds are

Time O(N + log(m+1) SUM_i [d_(i-1)+d_i+2^|U_i| poly(|U_i|+k+log N)] + m*k*2^k).
Workspace bits O(2^w (w+log N) log(m+1) + S_B + log^2(N+2)).

**Proof:** Each recursive boundary is a genuine global prefix/suffix message. The two recurrences preserve that meaning by induction. A singleton join therefore has precisely the global existential semantics. On each recursion level all intervals together traverse at most m source clauses, and recursion depth is O(log m). Source rereads, output writes and proof replay are charged; retaining the full stream as writable storage removes the compact-space claim.

**Restricted recognition:** Under a numeric source grammar |variable ID - clause index|<=b, b is found by scanning all original occurrences. Each boundary is discoverable by inspecting the last and next b clauses at O(b^2*k) source-occurrence work and O(b*k*log N) scratch per cut. This is an acquisition-paid tractable subclass, not a grammar-invariant intrinsic hardness measure.

## Explicit falsifiers and controls

F1 exact SAT+UNSAT two-sided support under replay: confirmed by independent full-table DP and exhaustive small instances.
F2 reduced writable space always reduces total work: FALSIFIED.
F3 useful b/order/parameter is acquired free or invariant under source renaming: FALSIFIED by legal numeric renaming.
F4 this restricted solver supplies an all-input small ordinary-SAT child: FALSIFIED as an inference, no such emitter produced.

Source | full DP selected events | replay selected events | UP-first DPLL selected events
- Band128 SAT | 839,166 | 1,917,887 | 61,057
- Band128 UNSAT | 837,844 | 1,915,434 | 17,566
- W1 strict22 UNSAT | 876,048 | 1,604,689 | 19,962
- SWAP6 strict22 SAT | 875,345 | 1,602,849 | 9,548

On Band128 SAT, the full method retains 2,115 source-message/output entries; replay's conservative simultaneously live envelope is 111. The corresponding W1 envelope is 111,416, which is NOT smaller than full DP's 90,772. At Band512 SAT, replay writes 35,308 bytes and uses 9,952,436 selected events, whereas full DP uses 3,484,541 and DPLL 936,208. Instrumented host-language event counts are not native FLMV indexed random-access TM instructions or a production CDCL benchmark.

Independent verification of 23 original source instances checked 9,958 records and rejected two deliberately corrupted pattern/mode certificates. W1 has zero satisfying models and SWAP6 has 54 with 70 of 160 original clause patterns globally unsupported. Original-clause signed S/U targets, inverted values, source-indexed SS/SU/US/UU, coherent zero/one endpoints and flip/complement identities are adverse controls, not an oracle.

## Prior work, model/firewalls and provenance

Reviewed live issue #3, current root main.tex, AGENTS/CODEX/pnp-research skill; verified user governance REDIRECT1 and CONTRACT1; AFFINE-SMALLBIAS-DESCENT-GATE2 (MCSP affine-only), CONSTRUCTION-STRENGTHEN17, ARC-LINEAR22-SATURATION1, HITTING-TREE-COMPOSITION-REFEREE222, previous FRONTIER-TWO-SWEEP259 and selector/probe reports. Existing project-join DP and Hirschberg-style replay are classical; no new general SAT theorem is claimed.

The complete LaTeX report, BibTeX, full producer, independent verifier, budgeted selector, original sources, unaggregated support JSONL, raw JSON, hashes and four-page PDF were verified in an archive uploaded to persistent Research Library: /P-vs-NP/2026-10-30_1624_LSPV-3_RECURSIVE_FRONTIER_REPLAY260_COMPLETE.zip (library ID libfile_89af6f962ec48191b7de0ad21a1a083f), SHA256 9abaccba34a153282115568949c2cf0a6bb94ba6b9d4631871cac408b07fb2bc.

FLMV JACM 2005 Theorem 5.7 forbids simultaneous ordinary-SAT time/space below the strict slice c=241/200, d=11642479/23232400 in its indexed random-access machine model. The proposed compiler recurrence with fixed point (6/5,1/2) is CONDITIONAL; this streaming technique does NOT construct the missing hereditary all-input A->Phi(A) ordinary-SAT child. A literal stream of answer bits is not a small ordinary SAT instance, nor is outsourced output space free. P=NP and P!=NP remain OPEN.

Primary literature: Fortnow-Lipton-van Melkebeek-Viglas JACM 2005; Hirschberg CACM 1975; Dudek-Phan-Vardi DPMC 2020; Dreier-Ordyniak-Szeider JCSS 2024.

**Next:** source-verifiable replay/caching policy that also constructs a power-short ordinary SAT child at <N^(1/2+o(1)) simultaneous writable bits with all source and guest access charged.

END_OF_VERIFIED_REPORT::RECURSIVE-FRONTIER-REPLAY260::P_VS_NP_OPEN
