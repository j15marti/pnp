# POINTWISE-GUEST-CEILING1 | technical handoff | 2026-11-18 12:55 PST

**Status:** Restricted pointwise circuit-size ceiling proved by Shannon counting; 223,551 finite Python audit assertions passed, zero errors. No SAT decision lower bound. General A -> Phi(A) hereditary contraction and P vs NP remain OPEN.

1. On the indexed-source family G(i,y,c,u)=NOT F(y), with private post-y u and shared post-y c, the exact bad guest satisfies D_F(y,j)=F(y) AND all_valid(j). Fix all selector words j_d=0, and D_F becomes F(y) pointwise.
2. For each k>=8 there is k-input F requiring Omega(2^k/k) two-input Boolean gates by the elementary 2^(2^k) function-counting argument, while a full Shannon-ROM encoding of F has n=Theta(k*2^k) physical bits. Consequently ANY pointwise implementation of D_F has m>=n^(1-o(1)) guest bits, even with optimization and shared subexpressions.
3. If a compiler insists on guest m<=sqrt(N) for its tagged-source input N, this forces N>=n^(2-o(1)). Literal q-copy indexing satisfies the promise only by q>=n^(1-o(1)) for this family. This is an obstruction solely to **pointwise index-guest representation**, not to equisatisfiable compilation.
4. In the actually executed finite bit-normalized test, n=3456 bits, q=8192, N=29613616 bits, m=4384 bits, sqrt(N)=5441.84 bits. Thus m<sqrt(N), yet m>n and N/n=8568.755. Easy ROM function only, no time lower bound.
5. If a particular architecture reaches a padded correct A_D call on m>=n^(1-o(1)), the Omega(n^(D-o(1))) reached cost violates n^(max(11/10,3/5+D/2)+o(1)) for D>6/5. Source-aware algorithms that skip this call are NOT excluded.
6. Next target: a genuinely satisfiability-only (not pointwise function-preserving), near-linear, same-machine, source-checkable compiler to n^(1/2+o(1))-bit ordinary SAT guests, with hereditary closure and all access/encoding/calls/strategy certification charged. Retest source replay, q<2^h, early existential hoists, reconvergence and shared witnesses.

Full proof: research/agents/sigma-primary/2026-11-18_1255PST_POINTWISE_GUEST_CEILING1.md
Auditor + raw results + SHA-256 manifest in local reproducibility bundle POINTWISE_GUEST_CEILING1_20261118_1255PST_bundle.zip.

VERIFICATION_SENTINEL_POINTWISE_GUEST_CEILING1_HANDOFF_20261118_1255PST