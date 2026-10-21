# RP DENSE-BYPASS14 | 2026-10-21 | ESTABLISHED restricted counterexample

Research run :12 Circuit-SAT. All of P=RP, P!=RP, P vs NP remain OPEN.

## Ideas before literature
(A) Falsify combined ANF-degree + circuit-width + input-relevance hardness using a trivial accepting path; (B) variable-length digest information bound; (C) RP-preserving gate-trace sampling.

## Primary checks and user-source coverage
Directly read live GitHub original project sources: research/agents/rp-separation/2026-10-21_1712_RP_DIGEST_PORTFOLIO8_HANDOFF.md (SHA 9ac1126322833c16c0151b003fe806dd904983d3); research/agents/rp-derandomization/2026-10-21_1836_RP_ANF_GATE11_HANDOFF.md (SHA 50aaea218eb8bf84a3ed6d400d4fd0c0fbb88025); research/agents/mktp/2026-10-21_RP_QUOTIENT21.md. Not a whole-corpus audit. Literature: Lokshtanov-Mikhailin-Paturi-Pudlak SODA 2018 DOI 10.1137/1.9781611975031.18 (circuit treewidth after deleting input gates); Samer-Szeider arXiv:cs/0610174 (#SAT incidence-width FPT); Valiant-Vazirani TCS 1986 (randomized isolation, not unconditional hardness).

## ESTABLISHED restricted counterexample
For n>=3, random bits b,z_1,...,z_n. Define NOT gates u_i=NOT z_i; pair AND gates p_ij=u_i AND u_j for ALL i<j; H=(XOR_{i<j}p_ij) XOR (AND_i u_i); C_n=b OR H. Explicit uniform fanin-2 circuit has 2*binom(n,2)+2n gates, size O(n^2), all random inputs semantically relevant. Its reduced Boolean ANF degree is EXACTLY n+1, since the term b*prod_i u_i survives and u_i=1+z_i. Its gate-only undirected graph AFTER DELETING INPUTS contains a subdivision of K_n with surviving NOT nodes u_i and pair gates p_ij, so treewidth>=n-1 by K_n minor. Yet b=1,z=0^n always accepts, Pr[C_n=1]>=1/2. R(x,r)=x_1 AND C_n(r) is a valid RP verifier for the deterministic P language x_1=1: on NO every tape rejects, on YES at least half accept. No oracle/advice/crypto.
For k=weight(u), pair parity=binom(k,2) mod2, equal to 1 exactly for k mod4 in{2,3}. Exact count: #Acc(C_n)=2^n + sum_{k mod4 in{2,3}}binom(n,k) + (1 if n mod4 in{0,1} else -1). This is polynomial-time evaluable. All input bits are essential. The width claim is for circuit gate graph, NOT only Tseitin primal width.

## Tseitin/falsifiers
Each primary tape has a unique forward trace of deterministic gate outputs. Gate relations admit exact clauses of width<=3; no unproved parsimonious exact-3-literal padding is claimed. Uniform sampling of ALL gate variables dilutes RP mass by 2^{-g}, while sampling only primary random bits then computing gate trace preserves mass with O(g) work. Large width+ANF+relevance cannot force hard deterministic seed search; no unrestricted complexity result.

## Reproducibility
Local self-contained Python script dense_bypass14_audit.py and JSON: n=3..9, 12,752 assertion-accounted checks, ZERO failures; exact Boolean tables, ANF Moebius transform, influence witnesses, complete pair-gate K_n-minor certificate, counting formula, local constraints, Tseitin trace checks.

## Coverage and next work
Only 3 originals above directly checked this run; archival chats, Drive Living Log, original WRAPPER gate netlist, older handoffs remain unseen. NEXT: obtain actual WRAPPER DAG and measure gate-only width, primal width, affine ranks, residual ANF, deterministic bypass, source-access and witness-completion costs. Strict OPEN class labels.