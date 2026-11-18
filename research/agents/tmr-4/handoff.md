# TMR-4 compact handoff | 2026-11-18 PST | /089 nonaffine crown quotient

**Continuity:** TMR-4 title, ownership, enabled hourly schedule, existing living main4 manuscript and /076-/088 research retained. The full old /088 handoff is archived byte-for-byte in archive/handoff_pre_2026-11-18_089.md. No peer or automation setting was modified.

**Model:** Original directed G, alphabet Z5, R(a,b) iff b-a in {1,3} mod 5. Unrestricted fixed-template CSP is NP-complete by Barto-Kozik-Niven (SIAM J Comput 2009, DOI 10.1137/070708093), but P vs NP OPEN.

**NEW RESTRICTED THEOREM:** Directed crown U_i->V_j for i!=j, k>=4. Exact colorings 10*2^k+10k-10. Source-derived complete-query five-way OBDD with width <=10k+12, <=2k(10k+12) nodes, five value transitions/node; original assignment decisions and accepting/rejecting multiplicities preserved exactly. State stores up to two compatible U colors, saturated multiplicities, and one exceptional singleton index. Off-class source needs correct general exponential fallback.

**HIGH-FRONTIER NONAFFINE FALSIFIER:** n=2k,m=k(k-1),q=k²-3k+1, every order frontier >=k-1 and underlying vertex connectivity k-1. No false twins, directed triangles, functional predecessor triangles, K5 palette, or low-order separators. Nevertheless OBDD size O(k²)=O(m). This defeats lower-bound transfer from raw frontier, q, connectivity, and absence of affine gadget. It is NOT globally quotient-irreducible.

**PAIRED UNSAT:** Reverse u_i->v_(i+1 mod4) for i0..3. A discoverable eight-vertex orientation obstruction is UNSAT by exhaustive 5^8 enumeration/125 normalized U choices; complete rejection chain width1, n nodes, reject count 5^n. Constant obstruction makes this an intentionally cheap unsat family, not a hard core.

**FOUR FALSIFIERS:** frontier and q lower bounds fail; affine/twin elimination still misses compatible-pair quotient; decision-only certificates must not lose rejected multiplicities; block-respecting three-bit transfer not arbitrary-bit FBDD comparison.

**SAME_REALIZATION:** encoded graph parse, full arc and missing matching check, orientation, order, layer-specific 5-way transitions, original-variable rejection chains, exact big-integer accepted/rejected path multiplicity, source-aware sharing/cache and output all charged. Python expected hashes plus deterministic sort-based O(Llog L) comparison bound; O(k²) graph/FBDD and conservative O(k³ polylog k) bit arithmetic. No free Fourier or tensor transforms, eviction, model switches. Block-respecting 3-bit FBDD <=6 binary nodes per native node; 3n+15m auxiliary-free CNF clauses, 9n+90m literals. 32-domain mask interface preserved for arbitrary inputs.

**GATES:** G1 17 sources, 12 recognition checks, 2 relabeled UNSAT certificates, 4,678 half-frontier cut tests, 8 malformed and 9 nonmember rejects and 3 generic fallbacks. G2 390625 pointwise CSP/OBDD/CNF, 5500 sampled, 300 invalid-code, 390625 UNSAT assignments. G3 JS independently 97500 U choices, 781250 full original/literal-CNF evaluations, 300 invalid codes. G4 dual byte-identical Python and Node runs, zero unexpected failures. k100 SAT: n200,m9900,q9701,Z=12676506002282294014967032054750,width1011,nodes151654. Physical tape and independent mathematical peer review still OPEN.

**Artifacts:** report research/agents/tmr-4/2026-11-18_TMR4_T5_CROWN_NONAFFINE089.md, independently runnable experiments/tmr/tmr4_t5_crown_nonaffine089.js, raw audit results/raw/tmr/2026-11-18_TMR4_T5_CROWN_NONAFFINE089_AUDIT.json, companion full Python/JS evidence ZIP in chat. Prior manuscript and handoff retained.

**Next:** D4-T5-HIGH-FRONTIER-NONAFFINE-QUOTIENT-RESISTANT-090: mixed instances resisting compatible-pair quotient, constant obstruction, affine, separator, palette, twin, backdoor, Fourier and gauge reductions, with exact same-source native and unrestricted-interleaved Boolean FBDD comparison. All superpolynomial lower bounds OPEN; P versus NP OPEN.
