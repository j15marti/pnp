# FACTOR-JOIN56 handoff (LSPV-2, 2026-10-23 18:18 KST)

**Status:** P versus NP OPEN. Restricted source-exact upper bounds and counterexamples only.

**Files verified:** `research/agents/lspv-2/2026-10-23_1818_LSPV-2_FACTOR_JOIN56.tex`, adjacent `_minirepro.py` and `_raw_summary.json`. Root `main.tex` reconciled inside its LSPV-2 ownership region.

**Exact paired sources.** With original triples (a_i,b_i,c_i) and genuine source z,w, set G_y=(a|b|c)&(!a|y)&(!b|y)&(!c|y). Let p blocks use y=z, q blocks y=w, k=p+q. The SAT core has (!z|w)&(z|!w), while the UNSAT core has (z|w)&(!z|!w). Each input has n=3k+2 original variables, k ternaries and m=4k+2 clauses, and no units, pure literals, duplicates or disconnected source components. Labels are 7^k vs 0 models. Minimum syntactic strong 2CNF backdoor is k. Original primal tw=3. Role-1 PAIRHELLY67 choice graph on UNSAT is K_(3p,3q), with 9pq edges and tw=3 min(p,q), despite a linear source-aware resolution shortcut. Three resolution steps project each G_y to unit (y), and a final 2-variable SCC check decides the core. An eight-step refutation needs one left and one right block.

**Certified arbitrary 2CNF + ternary pipeline.** Given a true source separator Y of size b, delete Y and compute disconnected residual incidence components F_i containing k_i ternaries each. Every source clause belongs to exactly one block or to the Y-only core B0. For each alpha in 2^Y, branch locally on at most k_i variables and run SCC with signed-source paths. Exact parent label is OR_alpha B0(alpha) AND_i Exists_local F_i(alpha). Time is O(n+m+2^b m0+2^b sum_i 2^k_i (n_i+b+m_i+1)) word operations inclusive of full proof/witness replay. Profile/branch proof storage can be streamed. A good separator is **not** assumed freely discoverable: an arbitrary search may require binomial(n,b) candidates.

**Finite audit:** 5,218 assertion groups, 0 failures; 16 paired cases up to p=q=64; 240 random sources compared to brute force (183 SAT, 57 UNSAT); independent local profile-proof checks on small pairs; changed core sign hostile control. At p=q=64, n=386, k=128, m=514, N=28,812 encoded bits, 36,864 optional compiled choice edges, 768 SCC calls for complete factor profiles versus 384 resolution events plus one final SCC in certified special grammar.

**Roles 1 and 3:** Test the source-coherent factor profile against PAIRHELLY67 and existing all-algorithm transport claims. Do not transfer the optional 9pq edge-output bound to unrestricted decision; don't count a replicated shared source as independent local coins or witnesses.

**Role 4:** Compare QUADRATIC-SOURCE-LADDER55's d^2 *actual input fields*, tight O(N/logN) word reads, against our k linear source clauses whose optional quadratic *derived* graph can be entirely avoided. These are categorically different models.

**Role 5:** Incorporate only restricted exact upper bounds, source compatibility, the matched hostile pair and explicit OPEN obligations. General component-backdoor depth is KNOWN, not new.

**Next missing lemma:** Under fully charged, uniform, all-input separator acquisition, prove that *every* polynomial-time SAT decider must incur a superpolynomial cost or give a counterexample. Existing pair fails this task because a source-readable linear shortcut solves it.

**Source review limit:** Original MAIN64, STAR-CHOICE53, AFFINE-INTERFACE54 were directly read; full latest Role-4/Role-1 originals were not, beyond indexed handoffs and root summary. Literature: APT 1979 and Dreier-Ordyniak-Szeider 2024.
