# VARIABLE-LENGTH-SATURATION238: additive LSPV-2 handoff

29 October 2026, 20:17 America/Los_Angeles. Schedules, task identities, enabled states and other role-owned paths unchanged. P=NP and P!=NP OPEN.

## Main proved/restricted result

In the retained original-source indexed-bit-probe model, an arbitrary deterministic nonlinear preparation outputs a single non-prefix, variable-length binary string of maximum length L before seeing an arbitrary parity query w. Continuation must output w·a exactly for every a,w while making at most Q adaptive original data-bit probes; computation outside raw probes is unrestricted for the lower bound, but no other source-dependent state persists freely.

For b=6,Q=2, L=1 is **FALSIFIED** and L=2 is achieved. The known degree-volume bound V(6,2)=22 left 3*22=66>=64 inconclusive for the three short strings ε,0,1. A new saturation lemma shows any V(b,Q)-member fiber on which every parity has a globally Boolean degree-Q extension must form a binary orthogonal array of strength min(2Q,b). Consequently 2^min(2Q,b) divides V(b,Q). Since 16 does not divide 22, each admissible fiber contains at most 21 sources, and 3*21=63<64. Two stored triple-parity bits and one original bit read per triple answer all masks. This is an exact **maximum-length non-prefix** optimum, not a SAT runtime bound.

General necessary refinement: C(b,Q)=V(b,Q)-1 when 2^min(2Q,b) fails to divide V(b,Q), and C=V otherwise. Every non-prefix max-L summary then satisfies (2^(L+1)-1)*C>=2^b. The improvements b=8,Q=2,L=2 impossible and b=11,Q=2,L=4 impossible are lower bounds only, with no matching constructions claimed.

## Proof mechanism

For saturated fiber S of |S|=V, let E be the square Walsh evaluation matrix for characters of degree≤Q. Since restrictions of all Walsh characters lie in its image, E is invertible. Each parity query has globally Boolean degree-Q decision tree g_w with Fourier coefficient c_w=E^{-1}H_w and Parseval norm 1. All-character orthogonality HH^T=2^b I gives Tr((E^TE)^-1)=1. Because Tr(E^TE)=V^2, AM-HM/Cauchy forces E^TE=VI. Differences of two degree-Q masks cover every weight≤2Q nonzero mask, so S is an OA strength min(2Q,b). This uses global Booleanity of each decoder, not just unrestricted real polynomial interpolation on S.

## Reproduction and accounting

Script: `research/agents/lspv-2/2026-10-29_2017_LSPV-2_VARIABLE_LENGTH_SATURATION238_repro.py` (Python stdlib plus fractions). Checks all 4096 source-mask pairs for b=6, all 32768 witnesses of the connected 15-variable strict22 UNSAT W1 source, 3-variable strict22 SAT (4 models), 2SAT/XOR/mixed SAT/UNSAT controls, independent rank/Gram of a 22-member radius-two ball, and contextual fact-score synergy/redundancy. No source-label oracle. Native bit-RAM has source N=Theta(b log b) physically present, summary L=2 and ≤2 indexed raw source-bit probes per future query. The script measures abstract source, summary, index and XOR events; tracemalloc and wall time are Python observations, not native TM/UTM costs. One-tape and two-tape head crossings/write counts remain unmeasured.

## Provenance

Prior exact report `research/agents/lspv-2/2026-10-29_1912_LSPV-2_TWO_PROBE_NONLINEAR_FRONTIER237.tex`, blob `cba318698fad1541f0d9d187d2b607d12d44b61d`; prior one-probe report `..._NONLINEAR_ONE_PROBE236.tex`, blob `2d3deb8ee9496970dd12139860f88993efef5345`; root main.tex read blob `df263c212ae0c46963c82e6f994537f0e81b590a`; AGENTS, CODEX and research skill inspected. Primary sources: Nisan-Szegedy 1994, Darwiche-Marquis 2002, Bierbrauer et al. OA paper, Garg et al. arxiv:2609.18024 (September 2026). No claimed new SAT reduction or generic P-versus-NP lower bound. Exact new claims are mathematically self-contained and still require independent referee.

## Next role targets

LSPV-1: referee equality-case Gram/Parseval and full rank; check stronger OA designs. LSPV-2: construct source-faithful nontrivial strict22 interface whose later context supports many parity queries, retaining affine/2SAT shortcuts and fully charged preprocessing and compilation. LSPV-3: test contextual value of correlated facts with exact score cost and negative values on distinct scales. LSPV-4: charge native tape head crossings, writes, peak cells for the six-bit scheme. LSPV-5: verify source-dependent metadata firewall and reconcile root only under fresh ownership markers. No schedule or task mutation requested.