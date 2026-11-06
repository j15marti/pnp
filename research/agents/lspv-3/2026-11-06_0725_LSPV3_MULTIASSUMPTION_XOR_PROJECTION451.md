# LSPV-3/451: Source-authenticated multi-assumption affine-context elimination

**2026-11-06 07:25 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.** This extends LSPV-3/449's one-marked-assumption XOR compiler to arbitrary jointly consistent affine assumption families. The result concerns a given binary-XOR proof, not arbitrary mixed inferences or historical accepted-byte syntax.

## Idea, falsifiers, source review, revision

Pre-search hypothesis: eliminate jointly satisfiable marked affine assumptions from a supplied original-source-authenticated shared XOR proof while adding no more XOR inferences than its original number. Falsifiers: (F1) unlicensed free zero-row axiom; (F2) a consistent context projects contradiction to virtual tautology; (F3) double-counted common ancestors or assumption-scope leakage; (F4) an impermissible application to contextual AND3, RES, DEF or LOCAL lines. F1 is repaired by virtual zero markers and reference-copying. F2 is ruled out using joint consistency. F3 is controlled by shared node IDs and one topological pass. F4 is a genuine barrier for an arbitrary mixed compiler.

Prior work: original /341 semantic grammar blob c87acd11, previous LSPV-3/448–450, LSPV-1/449, LSPV-5/REFEREE384 and 387, November 2 governing handoff, current issue #3, AGENTS.md, CODEX.md, research skill, actual Grok 2026-11-06_1220_PROGRESS and Claude TPORT-0002. External required repos: konard/p-vs-np/scripts/proof_status.json SHA 93b77ed3; blkph0x/p-vs-np-proof-research/METHOD_INDEX.md SHA 18d693ea; meelgroup/frat-xor/format.md SHA 986a21aa. These do not establish a native mixed compiler. Literature: Urquhart (1987); Haken (1985); Braun arXiv:2609.23015; Pang arXiv:2610.00837v2; Beame–Sun arXiv:2605.15002. Google-branded direct search unavailable, indexed primary literature and GitHub inspected. The theorem is an elementary linear-algebraic deduction principle with paid DAG/source-provenance accounting, not claimed novel in its algebraic substance.

## Theorem 451.1, PROVED/RESTRICTED

Let E be context-free affine GF(2) rows with previously paid, original-source-authenticated legal derivations. Let A=(a_1,...,a_k) be **jointly satisfiable affine assumption rows**. Suppose a supplied acyclic shared DAG derives 0=1 from E and A using r distinct paid binary XOR inferences. Then there is an unconditional, source-preserving proof DAG over E deriving an affine row P using **at most r additional paid XOR nodes**, such that A entails the negation of P.

For each original line L track a k-bit coefficient vector t(L) and a projected row P(L) with

$$
L=P(L)\oplus\bigoplus_{i:t_i(L)=1}a_i.
$$

For source row e use P(e)=e, t(e)=0 and its authenticated reference. For assumption a_i use t(a_i)=e_i but P(a_i)=0=0 **only as a virtual marker**, not an axiom or proof node. At every paid XOR combine tags. If both projected parents have real references, emit one native XOR; if one vanishes, copy the other reference; if both vanish, keep a virtual zero. This preserves the invariant, ancestor sharing and acyclic dependencies at no more than one new paid XOR per old XOR.

At the contradictory root:

$$
P=(0=1)\oplus\bigoplus_{i:t_i=1}a_i.
$$

If P were 0=0, that combination of jointly satisfiable assumption equations would equal 0=1, impossible. Thus P is a real non-tautological E-consequence, false on all models of A. The theorem establishes a *consequence*, not an unconditional contradiction and not a generic case-discharge inference. No SPLIT, DISCHARGE, weakening, semantic oracle, or new calculus rule is added.

**Necessary counterexample:** E empty and A={x=0,x=1} gives a paid contextual XOR contradiction, but projection is solely virtual 0=0. Joint satisfiability, rather than linear independence of A, is exactly the sufficient hypothesis in this construction.

**Accounting:** With B already-paid source extraction nodes, work of the emitted consequence is at most B+r, sharing once. With n-variable dense row bitmaps and k-bit tags, straightforward serialization is O((B+r)(n+k+log(B+r+k))) bits plus original-source evidence. Ideal work differs from critical-path span and realizable time/peak space. Actual compilers pay all parsing, source/index reads, output, caching, tag retention, recomputation, failed policies and verification.

## Published hard family and finite original-source anchor

Original cubic odd-charge Tseitin formulas on suitable expanders: h cubic vertices, 3h/2 edge variables, 4h original signed proper 3-clauses, Theta(h log h) indexed bits. Urquhart's exponential ordinary shared-DAG Resolution hardness does **not** transfer automatically to the full mixed calculus: its declared AND3+GF(2) rules provide a 4h-1-node shortcut for bridgeless cubic odd-charge sources. Haken PHP versus Cook ER and bit-PHP Res(XOR) versus ER are mandatory legal shortcut controls, not all-machine hardness.

**Finite K4 control (not asymptotically certified proof-hard):** charges (1,1,0,0), edges (01),(02),(03),(12),(13),(23); 16 authenticated original strict-3-CNF clauses, 163 exact ASCII DIMACS bytes, SHA-256 061ee272d1e2e6167ae91c2adf9ab360c7b791e786e274a89a49dcd5164da115; eight original-source satisfying assignments over 64 valuations. Six paid AND3 nodes recover, from the four source clauses at each of vertices 0 and 2, the exact rows

$$
E_0:x_{01}\oplus x_{02}\oplus x_{03}=1,\qquad
E_2:x_{02}\oplus x_{12}\oplus x_{23}=0.
$$

Under four jointly consistent contextual assumptions x_01=x_03=x_12=x_23=0, XOR E0,E2 then the four assumption rows yields 0=1 after **five** paid XORs. The projection emits **one** XOR to derive x_01 XOR x_03 XOR x_12 XOR x_23 = 1 from E alone. Total original-context work is 6+5=11 versus unconditional *consequence* work 6+1=7. The original K4 input is SAT; a complementary context with the last boundary bit 1 has an actual source model. Therefore 7 is explicitly **not** a refutation minimum.

**Independent tests:** Python produced the original DIMACS, paid AND3 two-parent eight-row tables, XOR proof ancestry, tag projection and raw JSON. Independently implemented Node checker rederived all source facets/labels, 64 valuations, local parity aliases and XOR invariants; additionally exhausted **65,536** four-row GF(2) systems on three variables. It found **3,376** contradictory sums with jointly consistent assumption pairs and **720** with inconsistent pairs, with **11,706 total assertions passed**. Corrupted proof XOR and mutated-source-hash controls rejected; inconsistent-assumption counterexample checked. Producer observed 1.0554 CPU seconds and 96,144 KiB peak host RSS (not FLMV). All typed source, code, independent verification, raw results, and SHA-256 manifest are retained in the full reproducibility ZIP. Independently checked finite results are COMPUTATIONAL, symbolic theorem PROVED/RESTRICTED.

## Missing transfer and safeguarding

The exact historical R_mix341 accepted-byte checker for DEF facets, PRIVATE/EXPORTED ports, LOCAL-CONVERT and arbitrary mixed contextual derivations is unauthenticated. This proof establishes no universal all-rule superpolynomial minimum, no noncircular same-R B3, no SAT algorithm contraction, and no P versus NP solution. The original five roles, schedules, weights, and ownership regions remain unchanged. Root main.tex was not edited: authenticated retrieval yielded SHA but zero readable text, so preservation of unowned bytes could not be guaranteed. **P versus NP OPEN.**