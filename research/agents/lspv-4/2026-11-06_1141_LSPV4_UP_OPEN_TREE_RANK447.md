# LSPV-4/447 | Exact UP-open branch count on cubic Tseitin original 3-CNF
**2026-11-06 11:41 PST | Route A primary | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE
Hypothesis: the prior /446 existence of one original-clause-unit-propagation (UP) open branch after logarithmic branching can be amplified to exponentially many open branches. Prespecified falsifiers: (F1) tree-component boundary equations can be dependent with a residual cyclic component; (F2) more than 2k/3 tree components remain after deleting k edges from a cubic graph; (F3) CNF UP differs from graph leaf-elimination on a signed 3-CNF; (F4) surviving children lose nearly all unchanged original clauses. Structural proof rejects F1/F2, independently implemented finite checks reject F3, and /446's previous incidence theorem addresses F4. Degree-two graphs are an explicit hostile control.

## Established family and theorem ledger
Let G=(V,E) be **any connected simple cubic graph**, H=|V|, M=3H/2. For every v with incident ordered edges a<b<c, original charge χ_v, and p,q in {0,1}, use the four **original proper signed three-literal clauses**
$$
C_{v,p,q}=\ell_p(x_a)\vee\ell_q(x_b)\vee\ell_{p\oplus q\oplus1\oplus\chi_v}(x_c),
\quad \ell_0(x)=x,\quad\ell_1(x)=\neg x.
$$
These exactly encode x_a⊕x_b⊕x_c=χ_v. There are 4H clauses, 12H literal occurrences; with fixed-width IDs of w=ceil(log₂(M+1)) bits, literal body is 12H(w+1) bits and N=Θ(H log H) with bounded headers. Connected-source SAT iff XOR_v χ_v=0.

**KNOWN MODEL-QUALIFIED HARDNESS:** odd-charge cubic *growing constant-expander* instances have exponential size against ordinary unrestricted shared-DAG **Resolution**, by Urquhart (JACM 1987, DOI 10.1145/7531.8928) and the Ben-Sasson–Wigderson width machinery (JACM 2001, DOI 10.1145/375827.375835). This is **not** a lower bound for mixed R_mix341, ER, Res(XOR), or arbitrary SAT algorithms. The authenticated GF(2) total-charge shortcut decides this entire source family efficiently. Finite graphs used below certify only semantics, not asymptotic Resolution hardness. No non-3-CNF reduction is needed.

## Theorem 447.1: EXACT open-branch count (PROVED/RESTRICTED)
Fix any S⊆E, |S|=k≤H/2, and branch over all 2^k assignments to S. Let r be the number of connected **tree** components (including isolated vertices) of G-S. Then exactly
$$
\boxed{B_{\mathrm{open}}=2^{k-r},\qquad 3r\le 2k,\qquad B_{\mathrm{open}}\ge 2^{\lceil k/3\rceil}}
$$
assignments are **UP-open**, meaning ordinary source-clause unit propagation halts without conflict. OPEN does **not** mean SAT. The result holds for every charge vector and every edge selection, with no expansion or edge-connectivity assumption beyond connected cubic G.

**Proof.** G-S has 3H/2-k≥H edges on H vertices, so has at least one cyclic component. For any tree component C, sum its original XOR equations. Every unassigned tree edge and each selected edge internal to C cancels. The necessary-and-sufficient consistency equation for a full assignment α to S is
$$
\bigoplus_{e\in\delta_G(C)}\alpha_e=\bigoplus_{v\in C}\chi_v. \tag{447A}
$$
The unassigned edges of a tree can be removed by leaf forcing; original signed 3-CNF unit clauses implement the same unique parity assignment. The last vertex conflicts iff (447A) fails. In a cyclic component, leaf removal stops at a nonempty 2-core, so no source parity clause becomes empty or unit there. Thus UP-open iff all r tree equations hold.

Contract the connected components of G-S to vertices, keeping crossing selected edges, and omit internal selected loops. The contracted multigraph is connected. Its GF(2) incidence rows have the sole dependency that their full sum is zero. Because at least one contracted vertex represents a **cyclic** component, deleting that cyclic row leaves all others independent. In particular the r tree rows are independent, so the r equations (447A) have exactly 2^(k-r) solutions, for *every* charge vector.

For each unassigned tree component C of v_C vertices, its unassigned edges use 2(v_C-1) of its 3v_C incident edge ends. Therefore v_C+2≥3 ends belong to **selected** edges. The disjoint tree components contribute at least 3r fixed incidences, while k selected edges supply at most 2k ends. Hence 3r≤2k. This incidence count **includes selected edges internal to a tree component**, even though they cancel from (447A). The result follows. QED.

## Corollary 447.2: restricted serial-output obstruction
Let k=ceil((3/5)log₂N). For sufficiently large H, k≤H/2 and H-6k>0. LSPV-4/446 established that any UP schedule after k initial edge decisions forces at most 2k additional distinct edges. Consequently every UP-open residual retains at least 4(H-6k) literally unchanged original ternary clauses, with **ordinary fixed-width explicit child encoding length Ω(N)**.

A compiler that enumerates all branches and separately **serializes every UP-open ordinary child in full**, even to a write-only output stream, has
$$
T_{\mathrm{emit}}\ge \Omega(N\,2^{k/3})=\boxed{\Omega(N^{6/5})}.
$$
This is strictly greater than the desired local-work N^(11/10+o(1)) for **that** exhaustive explicit-output architecture. If the compiler writes an ordinary child on a work tape it also incurs Ω(N) physical peak for that architecture; a write-only output cost does not automatically imply Ω(N) work-tape space. Shared templates, compact descriptors, native algebra, virtual ports, GF(2) joins, recomputation, and other legal methods **are not excluded**. The theorem does not restrict R_mix341's legal optimal shared-DAG derivations, does not prove any arbitrary-machine SAT lower bound, and does not establish the Route A contraction.

## Independent computational tests
Python built the exact source signed clauses and ran actual repeated original-CNF UP on every assignment to every subset of k≤2 (K4, Heawood) or k≤3 (Cube, Petersen, 10-vertex bridged cubic graph), with four charge patterns (both SAT and UNSAT). Results: **44,748** branch cases, **44,300 open**, **448 closed**, **41,248** forced assignments tracked under t≤2k, **1,472** exhaustive local signed parity checks. Independent JavaScript reconstructed all clauses by forbidden valuations rather than the p,q formula, checked each original-clause UP result, calculated exact GF(2) row ranks, detected corrupted signed clauses, and passed **125,145** assertions. A degree-two odd-charge 8-cycle had zero open branches and seven propagated variables from one fixed edge: the cubic restriction is essential. These are host-language finite controls, not native FLMV resource traces or asymptotic proof-size certifications.

## Resource and transfer ledger
**Logical proof DAG:** no new R_mix341 nodes or inference weights; shared node union and contexts Γ⊢C remain historical. **Inputs:** tested authenticated/generator-created original signed clauses; arbitrary unannotated CNF parsing and source acquisition remain OPEN. **Branch policy:** selected S supplied; failed policy search not executed. **UP:** actual host-language work, not zero-cost or native machine verification. **Explicit output:** Ω(N^(6/5)) bits in the declared exhaustive architecture. **Materialized guest:** Ω(N) peak if stored; no guest ran in controls. **Other costs:** indexing, source/head reads and erasure, output, caches, replays, ancestor/child buffers, references, search and all-phase peak must be charged by a real SAT compiler. Retain s'≤max(ρ,η,λ,λs). No claim on parallel critical span or shared-port work. Both SAT and UNSAT charge patterns tested; malformed sign corruptions rejected.

## Continuity and source authentication
Read governing Nov-2 five-role handoff, issue #3, AGENTS.md SHA 19656af1, CODEX.md SHA 754999f5, pnp-research skill SHA b8df83a7; LSPV-4/444-446, LSPV-2/449-450; Grok GROKPROOF/2026-11-06_1617_PROGRESS.md SHA b931933c; Claude ONETAPE-0001 SHA 9a5b05d6. Mandatory external sources actually read: konard/p-vs-np scripts/proof_status.json SHA 93b77ed3 and SOLUTION_STRATEGIES.md SHA 62f59558; blkph0x/p-vs-np-proof-research METHOD_INDEX.md SHA 18d693ea and INDEPENDENT_AUDIT.md SHA b30515cc and AFFINE_BOUNDARY_DESIGN.md SHA ed4f4a99; CNFgen tseitin.py SHA 4bb5fd19; FRAT-XOR README SHA 38a137bc; openai/math README SHA cc5b0a03. Primary research search included Urquhart, Ben-Sasson/Wigderson, FLMV (JACM 2005, DOI 10.1145/1101821.1101822), and Beame's 1991 unique-elements TS theorem; the latter applies to a **different computation/output model** and was not transferred. No separate Google-branded search, native FLMV run, third-party write, or proof-assistant execution. Root main.tex fetch returned a SHA but **zero readable characters**, so no edit was attempted.

**Actual advance:** exact 2^(k-r) UP-open enumeration formula and a restricted Ω(N^(6/5)) serial-output work floor. **Verification:** complete restricted mathematical proof; independently reconstructed 44,748 finite branch cases. **OPEN:** all-input, malformed-aware, recursively iterable, same-FLMV-machine contraction for every uniform total correct polynomial SAT decider, with t'≤max(11/10,3/5+t/2), s'≤max(1/2,s/2), and all phases charged. Route B's full mixed lower bound and noncircular B3 remain OPEN. **P versus NP OPEN.**
