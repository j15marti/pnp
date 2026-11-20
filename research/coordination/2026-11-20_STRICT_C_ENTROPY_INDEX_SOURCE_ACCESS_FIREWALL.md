# Strict-C entropy / adaptive-compatibility source-access audit (2026-11-20)

**PROVED (restricted one-pass theorem); COMPUTATIONALLY VERIFIED finite strict-C gadget checks; OPEN unrestricted T5/SAT lower bounds.**

Strict C: R(a,b) iff (b-a)%5 in {1,3}; C is a directed 3-cycle, 30/125 ordered value triples. Construct 5-clause palette C(p_i,p_{i+1},p_{i+2}), which admits exactly 10 dihedral palette frames, and original C relative pin PIN_c(x)=C(x,p_{c-1},p_{c+1}) iff x=p_c. Encoding arbitrary n source bits as pins to p0/p2 and appending a late test pin to p0 at variable i realizes one-way INDEX: complete formula SAT iff bit b_i is zero. All source clauses use three distinct variable names. With one nonrewindable pass over prefix before learning i and error epsilon on uniform b,i, a retained S-bit state requires S >= n*(1-H_2(epsilon)). For accuracies 75,90,99,99.9,100% this is respectively 0.18872n,0.53100n,0.91921n,0.98859n,n bits. **This does not transfer to random-access source-visible T5.** A rescanning solver locates the late-selected pin in O(n) time, O(log n) space.

Independent exhaustive verification: all 125 C value triples, exactly 10 palette frames, 250 relative pin tests, 1,538 source/index cases over prefix lengths 1..7, and 112,600 original C evaluations passed.

Second test: private-head strict-C K6 uses 15 physical clauses and 15,625 shared 5-color assignments. First-refutable-edge output has empirical exact Shannon entropy 3.400815275446587 bits and min-entropy 2.321928094887362 bits. Among 1,800 unique-blocker shared assignments, each of the 15 edge blocks is uniquely refutable in exactly 120 rows; output label entropy equals log2(15)=3.906890595608519 bits. Essential block count and obstruction rank do not themselves yield high entropy per label.

For original architecture with R <= N^0.195 explicit rows and B <= N^0.65 blocks, the complete selector-label table uses at most R*ceil(log2 B)=O(N^0.195 log N)=o(N^0.5) bits. This **does not mean** selecting labels is necessarily easy; it means output-label entropy cannot independently establish the square-root space lower bound. To charge changing parameters across levels use conditional information increments, not the sum of marginal entropies, and account for rereads, recomputation, learning, both child polarities, proof replay, and physical source verification.

Relevant published work: Göös & Pitassi, Communication Lower Bounds via Critical Block Sensitivity, SIAM J. Comput., doi:10.1137/16M1082007; Göös, Pitassi & Watson, Query-to-Communication Lifting for BPP, SIAM J. Comput. 2020, doi:10.1137/17M115339X; Huang et al., A Min-Entropy Approach to Multi-Party Communication Lower Bounds, CCC 2025, doi:10.4230/LIPIcs.CCC.2025.33. These are restricted communication results, not unrestricted SAT lower bounds.

Independent reproduction package is attached to conversation: `T5C_Entropy_Index_Compatibility_Audit_20261120.zip`, SHA-256 `52b5290ddb297572809543b0a0f45ab401ed4750289857c79d7bff64bfb74eb9`. Includes full Python standard-library verifier, results.json, detailed report, SHA256SUMS. The package was verified by re-hashing its contents. **Not uploaded to GitHub.**

P versus NP remains open.
