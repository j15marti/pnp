# LSPV-3/469 | Direct original-source sparse polynomial calculus over GF(2)

**2026-11-07 01:24 PST | Route B | PROVED/RESTRICTED binary-PC theorem; COMPUTATIONAL independent tests | P versus NP OPEN**

## IDEA, search, precise falsifiers, revision

Hypothesis: the established original strict 3-CNF odd-Tseitin family used in LSPV-2/341 and LSPV-3/468 admits a *direct standard sparse polynomial-calculus over GF(2)* proof, with the same source clauses, exactly 4h-1 binary polynomial additions, no variable-multiplication steps, no Boolean axioms, no definition variables, and no multi-premise theorem jump.

Four falsifiers fixed before research: (1) source clause polynomials add to parity only as Boolean functions, not formal polynomials; (2) a source clause is inessential, invalidating exact optimality; (3) ordinary PC does not permit binary polynomial addition; (4) intermediate sparse representations or depth are exponential. Local multilinear uniqueness resolves (1), the existing bridgeless-cubic source-indispensability theorem LSPV-2/341 resolves (2), ordinary PC linear combination resolves (3), and balanced boundary-edge row accounting resolves (4).

Revised scope: this is a proof of a restricted *family-specific positive simulation* into standard PC_GF2, **not** a translation of arbitrary R_mix341 proofs, and not historical accepted-byte native authentication. LSPV-3/468 already proved the contrasting obstruction into characteristic-mismatched ordinary sparse-PC, so no new broad polynomial simulation is claimed.

## Exact published-family ledger

For connected simple bridgeless cubic G=(V,E) with h even vertices and n=3h/2 edge variables, choose odd vertex charges chi. For each vertex with edges e1,e2,e3 and each a in {0,1}^3 with XOR(a) != chi_v, include the unique original signed proper width-three clause falsified exactly on a. Thus m=4h original clauses, indexed input bits N=Theta(h log(h+2)). Summing all h parity equations gives 0=1, so F is UNSAT. Every individual original clause is indispensable by the prior LSPV-2/341 theorem. For suitable cubic expanders, published exponential lower bounds apply to *ordinary shared Resolution* (Urquhart 1987, Ben-Sasson/Wigderson 2001), and characteristic-mismatched ordinary sparse polynomial calculus has linear-degree lower bounds (Buss et al. 2001, Alekhnovich/Razborov 2003). Neither establishes mixed-system or all-machine hardness. Known shortcuts: AND3+GF(2), Extended Resolution, parity-native proof systems, shared DAGs.

## Theorem 469.1 | PROVED/RESTRICTED, fixed binary standard PC_GF2

Encode source clause C_(v,a) as the standard polynomial axiom

$$
p_{v,a}(x)=\prod_{i=1}^{3}(1+x_{e_i}+a_i)=0\quad\text{over }\mathbb F_2.
$$

Each polynomial is an exact multilinear indicator for the assignment forbidden by its source clause. The *formal polynomial* identity

$$
\sum_{a:\,\oplus_i a_i\neq\chi_v}p_{v,a}(x)
=x_{e_1}+x_{e_2}+x_{e_3}+\chi_v
$$

holds because both sides are multilinear polynomials with identical evaluations on all eight Boolean triples, and multilinear interpolation is unique over GF(2). Combine the four original-source PC axioms using three **binary** PC additions, balanced in depth two, to derive the local affine equation. Sum the h local equations with h-1 further binary PC additions. Every edge cancels twice and odd global charge leaves the polynomial 1, a valid original-source refutation.

For standard ordinary polynomial calculus with binary linear-combination rules and unary variable-multiplication rules, fixing unit cost per derived inference node, each of the 4h indispensable source clause axioms must be in the final proof DAG's ancestry. All universal Boolean axioms are sound independently. The connected directed-acyclic proof's underlying graph and indegree<=2 give q>=4h-1; the number of original leaves at depth d is at most 2^d, so d>=ceil(log2(4h)). The balanced construction attains both:

$$
\boxed{W_{\mathrm{PC}_{\mathbb F_2}}(F)=4h-1,\qquad
D_{\mathrm{PC}_{\mathbb F_2}}(F)=\lceil\log_2(4h)\rceil.}
$$

This exact equality is for **unit-cost binary-inference PC over GF(2) on the original clauses**, including all legal PC DAGs, shared nodes and unary multiplication. It is NOT an equality for general proof formalisms admitting a free arbitrary multi-premise linear-combination step, a statement about minimal certificate bits, or a new historical R_mix341 rule. The known exact mixed AND3/GF(2) work and span were already proved separately (LSPV-2/341, LSPV-1/423); the material addition here is a native **standard PC_GF2** directly and independently replayed proof from the same indexed source clauses.

## Bit bounds, independence, false-label controls

Each clause polynomial has <=8 monomials, local intermediate sums are constant-size, and every global balanced tree layer represents vertex-set boundary-edge parities. Each edge occurs in at most two rows per layer, yielding O(h log h) total sparse monomial occurrences and O(h log^2 h) explicit proof-bit upper bound for monomial IDs, source IDs and references. No extension variables and no exponentially long polynomials are required. This is a proof existence construction on this recognized family, not an all-input efficient acquisition theorem.

The executable Python producer generated eight original-source cases (K4, K3,3, cube, prism6, both odd- and even-charge). The **independently written Node checker** reconstructed clause polarity, exact GF2 clause polynomials, all binary additions, root contradiction or zero, source SHA256, original SAT model counts and, for each odd source, a satisfying assignment upon deletion of each individual source clause. It passed 3,184,909 assertion groups and rejected ten deliberate corruptions (polarity, digest, inference, future ref, omitted premise, incomplete root, changed charge, false label, nonfresh ID, incorrect span).

Odd-charge source/mixed-PC proof controls: K4 16 clauses /15 additions / span4; K3,3 24/23/5; cube 32/31/5; prism6 48/47/6. Even-charge controls have 8,16,32,128 satisfying assignments respectively and end in polynomial 0, not 1. The first three odd source hashes reproduce prior certificates exactly; prism6 odd SHA256 = da4f5b2532ec71717eafff0f93d8df8dfe831d5f8961d77e96282b5f885ad7d8.

Host resource observation for full exhaustive producer: 2.25s, 96,132 KiB peak RSS; independent Node checker: 2.26s, 38,220 KiB peak RSS. These are host measurements with all original-source enumeration, negative controls and serialization; not native FLMV time-space results. The distinct-node ideal proof cost excludes search by design. Full proof DAGs, two independent implementations, raw logs, negative controls and SHA256 manifests were preserved in the LSPV-3/469 run reproducibility archive. Public compact replay: experiments/arc/lspv3_469_pc2_replay.py. Compact raw results: results/raw/arc/2026-11-07_0124_LSPV3_469_PC2_SUMMARY.json. Authoritative historical R_mix341 checker was not run.

## Research corpus and status

Actually read: root proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and proof2.txt initial blob 7ca014e3d0d1ec04a7e6631cbd468b9861f3d76d, issue #3, governing Nov 2 five-role handoff, AGENTS.md, CODEX.md, pnp skill, LSPV-2/341, LSPV-1/423, LSPV-3/429, /449, /468; current Grok progress and actual Claude World Ledger LaTeX. Corpus: konard/p-vs-np README and finite-machine model (blobs 0e0ec77/7ee9a11), blkph0x/p-vs-np-proof-research README and METHOD_INDEX (f397a77/18d693e), FRAT-XOR format (986a21a), cake_lpr README (e94f45e), openai/math README (cc5b0a0). These are not external confirmations of P vs NP. Literature web search consulted published first-party Buss et al. JCSS 62 (2001) and Grigoriev/Hirsch ECCC TR01-011; Google-specific search not independently available.

Relevant source/theorem citations: Buss et al., https://mathweb.ucsd.edu/~sbuss/ResearchWeb/lineargaps/ ; Alekhnovich/Razborov, https://www.mathnet.ru/eng/tm403 ; Grigoriev/Hirsch, https://eccc.weizmann.ac.il/eccc-reports/2001/TR01-011/ ; Urquhart, JACM 34(1) 1987; Ben-Sasson/Wigderson, JACM 48(2) 2001.

Tracker nodes read: [P1-01], [P1-03], [P1-04], [P1-X3], [P2-D1], [P2-D2], [P2-D3], [P2-B1], [P2-B2], [P2-C3], [P2-F2], [P2-F9], [P2-L3-468]. Add evidence node [P2-L3-469] only, without promoting any open bridge.

**Remaining:** Historical exact accepted-byte R_mix341 grammar [P2-D1] OPEN; transfer across all mixed legal rules [P2-C3] OPEN; full R superpolynomial Wbar [P2-B1] OPEN; noncircular B3 [P2-B2] OPEN. Keep all roles/schedules/weights and root manuscript unchanged. P versus NP OPEN.
