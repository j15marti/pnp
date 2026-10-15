# LOCALSHIELD1 STATIC-INCIDENCE-CLOSURE5

**Status:** PROVED/EXACT restricted-template theorem and COMPUTATIONAL audit. The arbitrary-input LOCALSHIELD1/FLMV bridge remains OPEN. P versus NP OPEN.

## New closure theorem
For a family of proper ordered 3-CNFs whose *unsigned variable support in each clause slot* is independent of input signs, assume local addressers for (a) source clause positions, (b) degree d(v), (c) degree prefix D(v), and (d) occurrence rank r(v,j), each in polylog time and O(log m) work space. A constant-depth proper-3-CNF OR shield preserves these interfaces. For the original 2026-10-13 00:10 selector+duplication PC22 compiler, the complete exact-(2,2) compiled shield has polylogarithmic per-output-bit access, O(log m) writable scratch, and at most three source-sign-bit probes. No index is materialized.

For source literal ell in shield clause j and U-duplication copy c in {0,1}, its clone label is
sgn(ell) * [1 + 2D(|ell|) + r(|ell|,j) + c*d(|ell|)].
Cycle-edge group boundaries are recovered by binary search over 1+2D(v), without source scanning. The remaining 19-clause Q suffix is an arithmetic local lookup, using **Q = W1 minus (x1 OR x7 OR x13)**, NOT the erroneous version.

Exact output counts for a shield with m clauses:
V22=72m, M22=96m,
L22=|gamma(V22+1)|+|gamma(M22+1)|+3*M22*(1+floor(log2(V22))+1).

## Explicit two-level shield case
Take k>=5 source clauses (x_j,x_{j+1},x_{j+2}) cyclic, allowing independent literal signs, and three fixed UNSAT eight-clause anchors. The two-level OR shield has nW=4k+84, mW=4(k+24); after the original 00:10 compiler V22=288(k+24), M22=384(k+24). Against a fixed-width encoded source of N=Theta(k log k) bits, target length is Theta(N), with polylog per-bit access and at most three direct sign-bit reads. An augmented source adds an independent eight-clause sign-programmed kernel, admitting both SAT and UNSAT inputs with identical unsigned incidence. The selected source families are easy, and cannot themselves instantiate an FLMV hard first leg.

## Independent verification
50 random cyclic sign settings: 7,340 exact shield records; 704,640 exact compiler records; 1,574,162 output bits compared; zero mismatches. All 50 compiled instances were proper, clause-distinct, and exact signed (2,2). Six SAT/UNSAT kernel cases and 3,000 full fixed-width source-sign-address queries passed. An altered unsigned source identifier with identical sign bits produced a differing actual compiled result, proving the method **does not** totalize automatically off the static-template promise. A large virtual instance (k=100,003) exposed 2,996,008,804 output bits, tested by 1,500 random queries without materializing the output.

## Fully charged scope and missing bridge
For a template reduction with output length L=N^{1+o(1)}, any target decider with (T_A(L),S_A(L)) yields source simulation in (T_A(L)*polylog N+polylog N, S_A(L)+O(log N)). This would preserve exponents in an FLMV same-machine transfer **provided** an all-input, SAT-hard, near-linear, locally addressable fixed-incidence sign-template first leg is supplied, with a charged original source-bit adapter. That first leg has NOT been proved. The known raw occurrence-rank Omega(m) obstacle is unaffected for arbitrary unsigned incidence.

References:
- Original PC22_ALLFIELD1 (2026-10-13, 00:10): research/agents/lspv-4/2026-10-13_0010_LSPV-4_PC22_ALLFIELD1.tex
- LOCALSHIELD1_Q_VERSION4; PORTFOLIO22_QUERY_LB1.
- Jahanjou, Miles, Viola, Local Reductions, Information and Computation 261 (2018), https://arxiv.org/abs/1311.3171
- Fortnow, Lipton, van Melkebeek, Viglas, Time-Space Lower Bounds for Satisfiability, JACM 52(6), 2005, https://doi.org/10.1145/1101821.1101822

Reproducibility bundle and full LaTeX report were generated as conversation attachments (not committed with this note).
