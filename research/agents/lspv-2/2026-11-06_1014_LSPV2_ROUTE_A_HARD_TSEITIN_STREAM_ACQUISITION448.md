# LSPV-2/448: Streaming acquisition on Resolution-hard Tseitin products

**2026-11-06 10:14 PST.** KNOWN THEOREM, PROVED/RESTRICTED, COMPUTATIONAL. Universal FLMV contraction, B3 and P versus NP OPEN.

## Idea, falsifiers, correction
Hypothesis: A 1-bit *final* SAT-status summary can take Omega(c) *peak* writable bits to acquire on a one-pass source even when every UNSAT member is rigorously exponentially hard in ordinary shared-DAG Resolution. Falsifiers: (1) two distinct first-block charge strings cannot be distinguished by the same suffix; (2) a shorter cross-component Resolution proof evades each hard factor; (3) the source ceases to be genuine signed proper 3-CNF or its SAT label ceases to equal binary equality; (4) the streaming bound survives indexed rereading or implies all-algorithm SAT hardness. F1/F2 are ruled out symbolically; F3 was tested; F4 is FALSE outside the declared model.

Prior related work: LSPV-2/438 source *authentication* equality, /446 charge reconstruction, /447 unrestricted future-toggle syndrome, LSPV-4/444 read-once *permutation-authentication*. The distinction here is the SAT decision **itself** for an already authenticated, proof-size-hard promise family.

## Exact source, family/theorem/model ledger
Fix a growing connected simple cubic expander graph G_h with h vertices satisfying the known Urquhart and Ben-Sasson/Wigderson hypotheses. Use c variable-disjoint copies. Each vertex v has three incident edge variables x_a,x_b,x_d (indices a<b<d). Define l_0(x)=x and l_1(x)=NOT x. For charge chi_v encode four **original proper signed width-three** source clauses:

$$
C_{v,p,q}=l_p(x_a)\vee l_q(x_b)\vee l_{p\oplus q\oplus1\oplus\chi_v}(x_d),\qquad p,q\in\{0,1\}.
$$

Exactly the four violating assignments to x_a XOR x_b XOR x_d = chi_v are forbidden. There are H=ch vertices, 3ch/2 original edge variables, 4ch clauses, and 12ch signed occurrences. With fixed-width identifiers w=ceil(log_2(3ch/2+1)) and signed literal words, N=12ch(w+1)+O(ch)=Theta(ch log(ch)). No equisatisfiability-only reduction is involved. In component j charge v_0 with arbitrary bit a_j, distinct v_1 with b_j, and all other vertices with zero. Stream first all v_0 four-clause bundles for j=1..c, then all v_1 bundles, then zero-charge bundles. The public graph metadata has no copy of a or b.

**Established model-specific theorem:** On connected odd-charge cubic expanders, every ordinary shared-DAG Resolution refutation needs 2^{Omega(h)} size (Urquhart 1987; Ben-Sasson/Wigderson 2001). This is not a general SAT algorithm lower bound and not established for complete R_mix341, Extended Resolution, or paid GF(2). Haken PHP ordinary Resolution hardness and Cook Extended Resolution PHP shortcuts remain mandatory controls.

## Theorem 448.1, product hardness (PROVED/RESTRICTED)

$$SAT(F_{h,c,a,b})\iff a=b.$$

Every UNSAT member has ordinary DAG Resolution refutation size at least 2^{alpha h} for fixed alpha>0 and sufficiently large h (the established expander bound).

Proof: On a connected graph, the vertex-edge GF(2) incidence matrix has image equal to the even-charge vectors, so component j is SAT iff a_j=b_j. Original clauses use variables from only one component. Ordinary binary Resolution needs a common pivot, so clauses from distinct variable-disjoint components cannot resolve. Inductively, every derived nonempty clause is component-pure; the empty root must be refuted entirely within one odd-charge component. Any two odd charges of G_h differ by an even vector in the incidence image, and are equivalent under literal complementations, preserving Resolution size. Thus the existing expander lower bound applies. Shared DAG reuse is permitted and cannot change this pure-component invariant. QED.

For c=h^2, N=Theta(h^3 log h) and Resolution size is exp(Omega((N/log N)^{1/3})), superpolynomial. This bound is specific to **ordinary Resolution**. Algebraic charge parity is a polynomial-time shortcut for this same family.

## Theorem 448.2, one-pass SAT acquisition state (PROVED/RESTRICTED)

Machine: deterministic one-way *read-once* original signed-clause stream; graph and canonical source order are public and correctly authenticated; no input rereads, indexed ports or uncharged source-dependent caches/head locations. At the cut after the first c vertex-bundles, the input head position is independent of a. For every a distinct from a', the identical suffix b=a yields SAT on prefix a and UNSAT on prefix a'. Identical post-prefix machine states would force identical answers, impossible. There are 2^c distinguishable prefixes, so

$$S_{\mathrm{cut}}\ge c.$$

At c=h^2 this is Omega((N/log N)^{2/3}), which exceeds N^{1/2+o(1)} **for this source-order streaming architecture**. A matching upper-bound stream algorithm stores a (c bits) and compares b. Conversely, with indexed read-only source access and publicly authenticated canonical layout, reread each pair of charge bundles by address and use O(log N) writable space and O(c polylog N) time. The indexed upper-bound control defeats any claim of an all-machine lower bound. Malformed/general-CNF authentication and fallback are separately charged and not solved here.

## Theorem 448.3, future query-menu quotient (PROVED/RESTRICTED)

Let sigma(chi) be the c-component parity syndrome. Fix a publicly permitted set of later charge-toggle queries Q, with distinct syndrome image D={sigma(u):u in Q} subset GF(2)^c. A sealed-source preprocessor permanently loses original charge access and must subsequently answer any Q query, possibly adaptively. Each in-menu syndrome has a unique one-hot answer vector; all off-menu syndromes, if any, induce the identical all-zero answer vector. Therefore the **exact** number of distinguishable final states is

$$K(D)=|D|+\mathbf1_{\{D\ne GF(2)^c\}},\qquad S_{\min}=\lceil\log_2K(D)\rceil.$$

Store the matching D index or an off-menu sentinel to attain the count. If D is a proper d-dimensional GF(2) subspace, S_min=d+1 bits, NOT d (the sentinel matters). If d=c, S_min=c. An empty menu requires no retained bits. This is an exact final-summary minimum, not an acquisition-space or full machine-time bound. For Q={0}, the eventual summary is 1 bit but Theorem 448.2 forces c bits of read-once *intermediate* space.

## Tests, resources, controls
The archived executable Python generator passed **350,572** checks on **364** original signed 3-CNF instances: K4 (1-4 components), cube (1-2), Petersen (1), all charge pairs; **21** altered-sign, swapped-clause and foreign-ID source controls rejected, **44** (c,d) menu combinations. An independently implemented Node verifier passed **351,373** checks, independently rederived all 364 signed sources and SHA-256 byte hashes and brute-forced all assignments for 24 sources with at most 12 original edge variables. Finite graphs are semantics controls, not certified asymptotically hard expander instances. Both executed original programs, 364 raw fixtures, expanded 20KB math report, independent checker and SHA-256 manifest are in the complete local reproducibility archive, SHA-256 f5319b0424ebb37225dfe35b3d0fe6b4a21b3d1d01a0f8e9b561388fa3cf4831.

**Accounting:** This run produced no native R_mix341 proof and no SAT guest calls; archival host code materialized source arrays and is NOT an FLMV space upper bound. The one-pass lower bound charges all machine state and source-head positions. An indexed promise algorithm does NOT authenticate arbitrary sources for free. A full contraction must charge parsing, index/graph acquisition, all child construction and actual smaller guest calls, source authentication, failed policies, joins, caches/recomputation, output, and simultaneous physical peak. Preserve s'<=max(rho,eta,lambda,lambda*s), t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2). The required uniform total correct all-input recursively iterable compiler A -> Phi(A) is OPEN.

## Reviewed sources, exact paths and status
Governing Nov. 2 five-role handoff (SHA c3889a3e), issue #3, AGENTS (19656af1), CODEX (754999f5), repo skill (b8df83a7), LSPV-2/447 (e0180e70), LSPV-4/443 (1e000297) and /444 (1b1f477e), LSPV-1/452 (8eb3dfb9), LSPV-3/455 (a12eab9f), Grok research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex (d06a2d56), Claude research/agents/claude/2026-10-28_1326_CLAUDE_TPORT-0001.tex (b7150bb9). Required repositories: konard/p-vs-np README.md (0e0ec77f), scripts/proof_status.json (93b77ed3), DETAILED_SOLUTION_PLAN.md (19450e38); blkph0x/p-vs-np-proof-research index.md (e8f685d0), METHOD_INDEX.md (18d693ea), INDEPENDENT_AUDIT.md (b30515cc), residual_equivalence_barrier.py (1b37efdb), projection_discovery_barrier.py (3ea94ff9). Also MassimoLauria/cnfgen cnfgen/families/tseitin.py (4bb5fd19), meelgroup/frat-xor format.md (986a21aa), openai/math README.md (cc5b0a03). Primary literature abstracts/metadata were searched with the available web index; no separate Google-branded engine, external build, or Lean formalization replay.

References: Urquhart, JACM 34 (1987), 209-219, DOI 10.1145/7531.8928; Ben-Sasson/Wigderson, JACM 48 (2001), 149-169, DOI 10.1145/375827.375835; Haken, TCS 39 (1985), 297-308; Morgenstern, JCTB 62 (1994), 44-62; Fortnow/Lipton/van Melkebeek/Viglas, JACM 52 (2005), 835-865.

Root main.tex (blob ab900e0e...) returned **zero readable bytes**, so no unsafe edit. Exactly two Route A and three Route B agents, current schedules, tasks and fixed proof weights remain unchanged. Universal contraction, full-mixed Wbar hardness, B3, P versus NP **OPEN**.

## Verified compact publication replay addendum

After the initial role report commit, the exact published compact Python replay was saved locally, executed **verbatim** and passed 40 strict-3 source controls, 44 query-menu controls and all nine prefix-inequality ranges. Local git hash-object returned **a51c28d7ddd033b2160990151f00b0e59ffe831f**, identical to the verified GitHub content blob for the compact replay file. This is additional successful standalone replay, separate from the archived full producer's 350,572 assertions and independent Node's 351,373 assertions. The compact script is not a native FLMV-machine implementation and its smaller checks do not replace the full archival fixtures.
