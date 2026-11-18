# CROSS-TRACK T5-ROOTGAUGE-PC51 | 2026-11-17 19:25 PST

**Status:** New restricted all-field Polynomial Calculus (PC) proof-transport theorem for arbitrary satisfiable single-root T5 attachments. Independent finite audit completed. P versus NP is **OPEN**.

## Four candidates proposed BEFORE search
1. Resource Contraction + Proof Transport: extend RESRETRACT50's four-path Resolution retraction to arbitrary rooted satisfiable gadgets, and test monomial-only PC retraction without free semantic summaries.
2. Nonrelativizing Simulation: delayed attachment or delayed gadget parameters might be a WRAPPER challenge; test whether SAT status actually changes and whether a direct source check defeats the challenge.
3. Universal Obstruction: use one identical final SAT input and common clock; include explicit gauge-shift witness recovery rather than changing the input per program.
4. Proof Transport size firewall: test variable-to-variable substitution separately from ALLFIELD-SHIELD-RETRACTION1's complemented-product substitutions, which can exponentially increase expanded PC size.

## Sources actually reviewed
- Freshest Resource/Information Necessity: [TMR-2/073, 2026-11-17 18:50 PST](https://github.com/j15marti/pnp/blob/main/research/agents/tmr-2/2026-11-17_1850_TMR2_T5_TWO_TERMINAL_ORBIT073.md): authenticated K3,3 two-terminal T5 family, cofactor F=(10,0,2,2,0), exact counting, paid source recognition. Resource TMR-4/062 shared-core compiler, TMR-4/069 encoding-neutral MDD and prior RESRETRACT50 also reviewed.
- Nonrelativizing Simulation: [TRACEAUDIT23](https://github.com/j15marti/pnp/blob/main/research/agents/nonrelativizing-simulation/2026-10-16_2223Z_TRACEAUDIT23_minimal.txt) and the [new CLOCKRMFIBER25 handoff](https://github.com/j15marti/pnp/blob/main/research/agents/clock-gate/handoff.md). Neither yields a correctness-forced nonrelativizing SAT operation.
- Universal Obstruction: [DIAGONALLIST34](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-3/2026-10-17_0545_DIAGONALLIST34_NOTE.md) and ORACLELEAK35 historical project-chat critique. No later standalone UWI proof was retrieved; same-final-input quantifier remains open.
- Proof Transport: [PC22-ORCLOSURE38](https://github.com/j15marti/pnp/blob/main/research/agents/cross-track/2026-10-17_0900_CROSS-TRACK_PC22_ORCLOSURE38_SHORT.md), [ALLFIELD-SHIELD-RETRACTION1](https://github.com/j15marti/pnp/blob/main/research/agents/proof/2026-10-16_2137_PROOF-TRANSPORT_ALLFIELD_SHIELD_RETRACTION1.md), and [RESRETRACT50](https://github.com/j15marti/pnp/blob/main/research/agents/cross-track/2026-11-17_1834_T5_RESRETRACT50_STATUS.md).
- Google Drive [KRYLOVGUARD41](https://docs.google.com/document/d/1sOFo42CQyQpvE20g3l0z2AJtCBaAZwtIhmfLgHNmrno/edit), project chats, Library TMR-4/069-070, latest GitHub commits. Primary literature: Bang-Jensen/Hell/MacGillivray [DOI:10.1137/0401029](https://doi.org/10.1137/0401029); Miksa/Nordstrom [DOI:10.1145/3675668](https://doi.org/10.1145/3675668); Cook/Reckhow [DOI:10.2307/2273702](https://doi.org/10.2307/2273702).

## Theorem: rooted gauge PC retraction

Let T5 be the five-symbol regular tournament R(a,b)=1 iff (b-a) mod 5 is in {1,3}. Let G be any original-arc T5 CSP with designated vertex r, and let Q be any satisfiable original-arc T5 CSP with designated vertex s, otherwise disjoint from G. Form H by identifying only r and s.

Use the direct five-rail one-hot polynomial encoding F_X over any field K. Its axioms are: sum_j X_vj - 1 = 0; each X_vi X_vj = 0 for i!=j; each X_vi^2-X_vi=0; and each forbidden arc-pair monomial X_ui X_vj=0 whenever u->v and NOT R(i,j).

Choose a satisfying Q labeling c rotated to c(s)=0. Define a literal-to-literal polynomial map rho(X_vj)=X_r,(j-c(v)) mod5 on Q vertices, identity on original G rails. Each Q one-hot, exclusivity and Boolean axiom maps to the corresponding original root axiom. Any forbidden-pair monomial on a Q arc u->v maps to X_r,a X_r,b for DIFFERENT a,b: equality would imply j-i=c(v)-c(u), contradicting the pair being forbidden because R(c(u),c(v))=1. Thus EVERY target axiom maps to an existing G axiom, with no complements or polynomial expansion.

Polynomial Calculus inference rules (K-linear combination and multiplication by a variable) project linewise to those same rules under rho. Degree, line count and total sparse monomial count do not increase. Conversely any G refutation is also an H refutation because G axioms are included. For every UNSAT G and every field K, the **minimum PC degree, minimum number of derivation lines, and minimum total sparse monomial count are each exactly equal** between F_G and F_H, under the explicit sparse-PC convention excluding physical source size and proof verification time. For SAT G, both systems are satisfiable, so neither has a refutation.

This is restricted to **one-vertex gluing and a satisfiable Q**. Existence of c is nonuniform if Q is merely promised SAT. A uniform projector must generate or verify c and pay that cost. No arbitrary-decider-to-PC proof transport follows.

Exact counting: global Z5 translation is a free action on Q's colorings. For every fixed root color Q has Z(Q)/5 extensions. Thus Z(H)=(Z(Q)/5)*Z(G). Every G satisfying assignment extends by the shifted c, and every H assignment restricts to G.

## Concrete new integration with TMR-2/073

Let Q_b (b>=2) be b oriented K3,3 blocks sharing internal terminals s,t. Each block has private source c_i, three private sinks w_i1,w_i2,w_i3 and 9 arcs from each of {s,t,c_i} to all 3 sinks. Explicit valid coloring: c(s)=c(t)=c(c_i)=0 and c(w_ij)=1. Attach Q_b to arbitrary G only at s=r; t remains private.

Exact K3,3 cofactor F=(10,0,2,2,0) by independent original-five-color enumeration. Its circulant matrix determinant 80864 is full-rank over Q. Q_b is bipartite, triangle-free, has minimum undirected degree 3, no articulation and undirected cycle excess 5b-1, minimum vertex cover b+2 and treewidth 3 (as in TMR-2/073). The glued H itself has a one-vertex articulation; this is intentional and not an irreducible 3-connected family.

Z(Q_b)=5*(10^b+2*2^b), hence **Z(H_b)=(10^b+2*2^b)*Z(G)** and **D_PC,K(F_H_b)=D_PC,K(F_G)** for all K on UNSAT G, with separately identical minimal sparse PC proof sizes under the specified convention. High two-terminal rank and large cycle/cover parameters of the attachment contribute no necessary PC-refutation cost. This is a counterexample to the unqualified rank-to-proof-work inference, not an arbitrary SAT runtime lower bound.

## Hostile independent audit
Executed local CPython 3 standard-library script t5_rootgauge_pc51_audit.py, SHA256 3dc0d430994270a97207684346f0c18fe5ddfb49bb7b37c263a0a769a8daf820; JSON 2026-11-17_T5_ROOTGAUGE_PC51_results.json SHA256 eecd5f65195b2d1c88270c0496e4747c95fbb90f1508d155dce4a609b8e17945.

**69,478 assertions, 0 failures.** Direct K3,3 cofactor 5^4 enumeration; independent entire original-graph backtracking for b=1,2,3 giving Z=70,540,5080; six rooted-G contexts including UNSAT two-opposite-arc graph, all glued original counts match factor 108 for b=2; 43,875 forbidden-arc monomial retraction checks over b=1..25; separate coefficient-by-coefficient 63-line PC refutation checked over F2,F3,F5,F7,F11,F101. No independent peer review, native Turing-machine microtrace, general arbitrary proof search or asymptotic machine lower bound.

The authenticated restricted family admits polynomial source recognition, original graph parsing, big-int cofactor counting, witness extension, and proof projection with explicit charges as TMR-2/073. No source decomposition, SAT witness or proof-system certificate is free. For nonmembers the relevant general algorithm may take exponential time.

## Proof DAG
- ESTABLISHED: fixed T5 tournament CSP NP-complete (Bang-Jensen et al.).
- PROVED RESTRICTED: single-root exact count identity; all-field one-hot PC monomial retraction; degree/line/sparse-size equality; K3,3 gluing multiplier; witnessed and finite-audited.
- FALSIFIED: high-rank cyclic attachment necessarily increases PC refutation degree or sparse PC size.
- OPEN: a uniform polynomial-time constructor of arbitrary satisfiable Q witness; full-cost universal contraction for arbitrary 3-connected mixed-status T5 cores; a SAT-correctness-forced nonrelativizing WRAPPER; same final SAT input and common clock defeating every eligible witness program; arbitrary-decider-to-PC transport; P != NP.

## Next four specialist assignments
1. Resource Contraction: original-source one-articulation recognizer/producer with complete scanning, rejected candidates, exact counting, witnesses, proof output and workspace, then attack 3-connected mixed-status cores where root gluing fails.
2. Nonrelativizing Simulation: delayed status-changing edit crossing the separator; test direct source checks, replay, oracle and P=NP conditional shortcuts. Changing Q_b size is SAT-neutral and not a mandatory-work hinge.
3. Universal Obstruction: identical final H, common clock, program class, and source-aware G-witness gauge-lifting challenger; do not swap exists-one-input/forall-program quantifiers.
4. Proof Transport: independently certify all-characteristic PC and PCR extension; audit proof-size convention and compare real source/certificate costs; no transfer to arbitrary SAT deciders without actual compiler theorem.

**Single next load-bearing arrow:** an affordable, authenticated, fully charged reduction/obstruction for genuinely 3-connected mixed YES/NO T5 cores that survives alternative semantic algorithms, not a rank or proof-width surrogate.

READBACK_SENTINEL: T5_ROOTGAUGE_PC51_P_VERSUS_NP_OPEN
