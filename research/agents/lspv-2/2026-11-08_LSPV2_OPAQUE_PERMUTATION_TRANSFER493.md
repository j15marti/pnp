# LSPV-2/493: Original-source permutation embedding and comparison-model transfer firewall
**November 8, 2026 PST | Route A primary | PROVED/RESTRICTED + KNOWN THEOREM (Yao 1994) + COMPUTATIONAL | P versus NP OPEN.**

**Exact nodes:** [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN. Cross-route [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. This does not modify the historical R_mix341 grammar, weights or the five-role allocation.

## IDEA -> SEARCH -> ITERATE
**Initial idea:** Transfer an independently established worst-case time-space lower bound into an *original strict-3CNF SAT/UNSAT decision problem*, by using known clause-essential odd-charge cubic Tseitin formulas rather than inventing a hard family. **Falsifiers defined before search:** (F1) a connected bridgeless cubic odd-charge source has a redundant clause, invalidating permutation equivalence; (F2) a repeated label and one missing original clause remain UNSAT; (F3) comparison-based lower bounds automatically transfer to arbitrary native SAT machines reading literal bits; (F4) a one-replacement-only promise is mistaken for the all-input element-distinctness problem.

**Search:** Reused LSPV-4/488's original-source clause-essentiality and multi-pass communication proof, LSPV-2/490-/492, LSPV-4/493-/494 and the November 2 five-role governing handoff. Read current complete proof1.txt and proof2.txt, issue #3, AGENTS.md, CODEX.md, the PNP skill, actual GROKPROOF/2026-11-08_1130_PROGRESS.md and Claude TPORT-0002. The primary mathematical source is A. C.-C. Yao, *Near-Optimal Time-Space Tradeoff for Element Distinctness*, SIAM J. Comput. 23(5):966-975, 1994, DOI 10.1137/S0097539788148959: time-space product Omega(m^(2-epsilon(m))) for comparison branching programs, epsilon(m)=O(1/sqrt(log m)). Its accessible publisher abstract was checked; complete publisher proof was not independently reconstructed. Also inspected Borodin et al., SIAM J. Comput. 16 (1987), DOI 10.1137/0216007, and Boppana's finite-domain comparison-tree theorem. Public web search was used; a Google-branded engine was not separately available.

**External actual pinned files:** konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2 (P subset NP only in its declared finite model); blkph0x/p-vs-np-proof-research METHOD_INDEX.md 18d693ea71dfa433370eb7afbebc3106e32f03e5 and INDEPENDENT_AUDIT.md b30515cced93d8911a6415555ee9ec1444502d93 (restricted plans/obstructions only); MassimoLauria/cnfgen cnfgen/families/tseitin.py 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab (actual clause generator); meelgroup/frat-xor format.md 986a21aa92b62f844ef1fce852193142c41b2b1f (external proof format only); openai/math lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean 1ced21f44ad49370d1b812e862c03c3a91d7f836 (actual costed SAT node-search fragment). None supplies a universal SAT compiler.

## Source and EXACT decision equivalence: proved restricted
Fix a connected bridgeless simple cubic graph G=(V,E), H=|V|, m=4H, with one edge variable x_e per edge and charge vector chi of odd total parity. For each vertex v with incident edges e1,e2,e3, include four distinct ORIGINAL proper ternary clauses, one for each locally forbidden edge-bit pattern z, namely

$$
C_{v,z}=\bigvee_{j=1}^3\ell_{e_j,z_j},\qquad
\ell_{e,0}=x_e,\ \ell_{e,1}=\neg x_e,\qquad
z_1\oplus z_2\oplus z_3\ne\chi_v.
$$

The full source F_G is UNSAT by summing its vertex equations over GF(2). Crucially, every one of the m clauses is indispensable. Since G is bridgeless cubic and connected, G-v is connected: any two components of G-v would each need at least two distinct edges to v, impossible at degree three. Fix the three incident edges to the forbidden local pattern z and solve the remaining G-v parity equations. Their total residual charge is even because the global charge is odd and v is violated, so they have a solution. This assignment falsifies exactly C_(v,z). Thus F_G minus any single original clause is SAT.

Order the *actual original source clause IDs* from 0 to m-1, and for any valid word a=(a1,...,am) in [m]^m define

$$
D_G(a)=\bigwedge_{i=1}^m C_{a_i}.
$$

**Theorem 493.1 (exact):**

$$
\boxed{\operatorname{UNSAT}(D_G(a))\iff\operatorname{PERM}_m(a)
\iff\bigl|\{a_i:1\le i\le m\}\bigr|=m.}
$$

**Proof:** If a is a permutation, D_G(a) is exactly F_G up to clause order and UNSAT. Otherwise, at most m-1 distinct source clauses occur, so at least one indispensable C_j is absent; the witness for F_G\setminus{C_j} satisfies D_G(a). This uses ordinary CNF semantics with duplicates allowed, not a restricted proof checker. Every a yields a well-formed proper width-three CNF with identical clause count and variable universe. Out-of-range labels are **malformed label-list encodings** in the auxiliary comparison language; arbitrary malformed CNF encodings still require a separate all-input decider.

For a published bounded-degree cubic-expander family G_H, full F_(G_H) has an exponential lower bound in ordinary shared-DAG Resolution by Urquhart (1987) and Ben-Sasson--Wigderson (2001) width-size methods, under their graph-expansion assumptions. The source already IS strict 3-CNF, so no reduction to 3-CNF is claimed. The theorem above needs only connected bridgeless cubic G, including nonexpanding prisms. Algebraic GF(2), ER, CDCL and source-packet recognition are legal shortcuts in stronger calculi and are NOT excluded.

## Model-specific Yao transfer: proved restricted, NOT a native SAT lower bound
Consider a deterministic comparison branching program whose **only information about its source is the result of pairwise comparisons** between the opaque input labels a_i and a_j, with no label arithmetic, literal inspection, indexed-by-label bucket access, precomputed answers or free external oracle. It correctly decides SAT(D_G(a)) for ALL a in [m]^m. Theorem 493.1 forces it to decide element distinctness (possibly with the output bit reversed).

Every order/equality pattern on any totally ordered domain D of size at least m is realized by an input in [m]^m: replace its distinct values by their ranks 0,...,r-1. A pairwise comparison program has the **same transcript** on both, so its correctness for [m]^m implies correctness for ordinary comparison-model element distinctness. Applying Yao's published comparison-branching-program theorem yields

$$
\boxed{T_{cmp}(m) S_{cmp}(m)=\Omega(m^{2-o(1)})}.
$$

Here T_cmp is the number of comparison steps and S_cmp is the branch-program space in BITS (logarithm of width). With S_cmp<=m^(1/2+o(1)), T_cmp>=m^(3/2-o(1)). Original explicit 3-CNF size N=Theta(m log m), so exponent notation is also T_cmp>=N^(3/2-o(1)), exceeding the hoped-for N^(11/10+o(1)) **within this comparison-only restriction**. This is a sharpened model boundary compared with the fixed sequential-pass restriction in LSPV-4/488; neither contains the other.

**Nontransfer:** A genuine SAT algorithm sees the full signed literal data, may do arithmetic on clause IDs, parse parity packets, use GF(2), learn clauses, share DAG nodes, use indexed access and materialize or virtually generate arbitrary encodings. Nothing shows that any such computation can be simulated as a pairwise-comparison program at polynomial overhead. Yao's theorem alone does not imply an unrestricted FLMV lower bound, SAT hardness, a source-authenticated R_mix341 derivation lower bound, or the B3 bridge. This model gap is precisely [P2-A2]/[P2-A4]/[P2-A5].

## Hostile shortcut and upper control
On the *narrow promise* that a is either a permutation or differs by exactly one replacement, a constant-word arithmetic sum distinguishes cases: a replacement miss->dup changes the sum by dup-miss. Thus it would be invalid to use the Yao bound on that promise. On the full [m]^m domain, balanced replacements 1->0 and 2->3 keep the sum unchanged, so this single fingerprint is not sound.

A fully exact **noncomparison** bucket algorithm uses B bits to mark occurrences in each interval of B labels, rescanning the entire length-m source for each interval. It decides the promised label language with O(m ceil(m/B)) label inspections, O(B+log m) writable bits plus usual head bookkeeping, and authenticates every label. This is an actual legal shortcut/upper control in a model permitting label arithmetic and indexing; its all-phase TIME/SPACE must include input-head and bit parsing on the chosen physical model. It does NOT give a general 3-SAT decider.

## Finite evidence and resource ledger
Independent Python reference (downloadable archive) performed **16,484 assertions**, using original signed K4 (16 clauses), triangular prism (24), cube (32), and Petersen (40). It checked 3,344 one-original-clause-replacement SAT cases, all 112 individual deletion witnesses, parity-even SAT controls with 8/16/32/64 models, random complete source-multisets, all bucket sizes and corrupt labels. Independently written JS passed **8,460 assertions** on the same four graph families. The standalone small GitHub verifier is a THIRD implementation/control; its exact numbers are in the published raw ledger and require readback/execution. None is an official historical R_mix341 check or native FLMV run.

- **Work (theorem):** one symbol comparison per branch-program step, T_cmp; no unrestricted inference-node claim.
- **Space (theorem):** log(width) program state bits, S_cmp. A fully physical SAT guest can require more and is not charged by this theorem.
- **Evidence bits:** full original CNF N=Theta(m log m); opaque label sequence m ceil(log2 m) bits; SAT witness for a missing clause uses O(m) edge bits; UNSAT full permutation accepted only with authenticated original source and parity argument. No R_mix341 certificate bytes produced.
- **Actual finite construction/search/verification:** original signed clauses and all 2^|E| assignments enumerated; both-label and malformed controls, source scans, output JSON, caches and validator costs are paid in host code, but no native time bound is inferred. A materialized child has Theta(N) bits and violates the half-exponent guest bound; virtual access needs an explicit native guest interpreter.
- **Work/span/space separation:** The theorem measures sequential comparison work, not shared-DAG inference work or critical-path depth. Complete subset checking and Boolean model enumeration in the test are host-side finite controls only.

**ITERATE conclusion:** (F1/F2) falsified by exact algebraic minimal-UNSAT proof and finite witnesses; (F3) is the genuine nontransfer to unrestricted SAT; (F4) is a genuine shortcut on the restricted one-replacement promise. The main scientific advance is an explicit family-preserving Boolean decision embedding with a sourced *asymptotic time-space theorem in a specified comparison model*, not a new native all-machine lower bound.

**Remaining open:** No solver-dependent, exponent-oblivious, recursively iterable, both-label/malformed-aware ALL-INPUT A->Phi(A) transformation, with native local q<=N^(3/5+o(1)), B<=N^(1/2+o(1)), time<=N^(11/10+o(1)), writable peak<=N^(1/2+o(1)), has been constructed. [P2-A2], [P2-A4], [P2-A5] remain OPEN. [P2-D1], [P2-C3], [P2-B1], [P2-B2] also OPEN. **P versus NP OPEN.**

## Publication and tracker reconciliation (2026-11-08 06 PST)

Research report, standalone verifier, raw-results ledger and five-role handoff were created on `main` through the UTF-8 GitHub contents interface and independently compared against the COMPLETE returned file bytes. The published verifier blob is `6dd4b62ec7405231fa85e8c189bb5c38f47bd8ed`; independently executing the exact fetched source in a separate V8 isolate passed **4,201** assertions on original signed K4, Prism3 and cube (not misrepresented as native FLMV or historical R_mix341). The final corrected raw ledger blob is `1358d14d2de44d6dae7333efd5cc534ecff30ea4` and passed full readback; local independently executed Python and JS references have 16,484 and 8,460 assertions respectively (their code is preserved in the downloadable reproducibility archive, not falsely described as committed GitHub code).

**Material root proof-chain update:** [P2-A4] gained only the explicit restricted comparison-BP transfer; no universal status was promoted. Complete old `proof2.txt` blob `ae29ed2b792fb2f5c8a88d4c247727a65ee15eba` was preserved byte-for-byte in `research/agents/lspv-2/outbox/2026-11-08_LSPV2_493_PROOF2_PREWRITE_EXACT.txt` and authenticated by matching old SHA and complete content readback. A current-head SHA-guarded replacement inserted exactly one scoped evidence paragraph, and `proof2.txt` read back exactly with new blob `45fac3657435945ef35a8968c6d1c35fb7e9d107`, with removal of the added paragraph reproducing ALL prior bytes. `proof1.txt` retained blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`. Coordination issue #3 comment **6722760143** contains affected IDs [P2-A4], [P2-A2], [P2-A5] and remained byte-identical on independent comment readback: https://github.com/j15marti/pnp/issues/3#issuecomment-6722760143 . Neither root `main.tex` nor task settings, role ownership or historical R_mix341 grammar/weights were modified. General SAT contraction and B3 remain OPEN. P versus NP remains OPEN.
