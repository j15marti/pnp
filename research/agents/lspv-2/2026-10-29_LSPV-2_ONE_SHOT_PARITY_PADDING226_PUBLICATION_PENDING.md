# LSPV-2 / ONE-SHOT-PARITY-PADDING226 / 2026-10-29

**Status: PROVED/RESTRICTED elementary result, COMPUTATIONAL independent finite tests, external referee pending. P versus NP OPEN.**

## Target and proposed falsifiers

Missing unrestricted constructive arrow: a uniform polynomial-time one-child N^lambda answer-preserving transformation with recursive closure on SAT, not a mere one-shot reduction on a recognizable NP-complete promise.

M1: NP-completeness plus a single power contraction forces P=NP. FALSIFIED by this restricted padding control.

M2: canonical re-padding supplies descent and closure. FALSIFIED for the declared constructor and extractor because they form a two-cycle.

M3: eliminating a parity variable remains harmless when that variable also belongs to the hard core. FALSIFIED by a unit-constrained parity input.

M4: universal exact semantic compression and repeated closure. OPEN.

## Complete elementary construction and proof

Let H be any connected proper ordinary 3CNF with densely named variables 1,...,n and m nonempty ternary clauses. Let b=max(2,m^2), choose original port z=1, introduce x_1,...,x_b and y_2,...,y_(b-1). Encode z=x_1 XOR ... XOR x_b using b-1 binary XOR gates, each represented by exactly four ternary CNF clauses:

(u OR v OR NOT w) AND (u OR NOT v OR w) AND (NOT u OR v OR w) AND (NOT u OR NOT v OR NOT w).

Place H before the parity clauses and use deterministic fresh consecutive identifiers. The parent P(H) is connected, proper 3CNF with n+2b-2 variables and m+4(b-1) clauses. This is NOT strict signed exact-(2,2).

For every original assignment U and every fixed x_2,...,x_b, there is exactly one x_1 making the parity equal z(U), and the internal y's are forced by the XOR equations. Thus

exists(x_1,y_2,...,y_(b-1)) P(H)(U,X,Y) iff H(U).

This pointwise proof handles SAT and UNSAT using ONE uniform program, without a free answer-class bit, SAT oracle, or precomputed table.

Canonical recognition: from parent clause count M, find the unique m satisfying M=m+4(max(2,m^2)-1). Read the first m clauses as H; infer n from maximal used original name; validate dense identifiers, connectedness and ternary correctness; regenerate the full expected parent including header; compare all source bytes; output exact original DIMACS H. Invalid inputs are REJECTED, not decided.

The promised language K={P(H): H connected proper dense-ID 3CNF} is polynomial-time recognizable and NP-complete. Connected proper 3SAT remains NP-hard: normalize short clauses using standard ternary extension variables; connect components by forcing fresh t=TRUE using four (t OR +/-a OR +/-c) clauses and adding a tautologically satisfied proper bridge (t OR v_i OR w_i) for a representative of each component. This polynomial transformation preserves satisfiability, then P preserves it. NP membership is immediate.

Physical source bytes <=m(3d+8)+8+2d, d=1+floor(log10(3m)). For m>=4096, 8 source bytes <= 27m^(3/2) bits, while P(H) has at least 4(m^2-1) ternary clauses of at least 8 bytes each, so P(H) bits >=256(m^2-1). Consequently |H| <=|P(H)|^(3/4) for all m>=4096. All variable indices, headers, separators and output bits are charged.

**Closure failure:** extraction E(P(H))=H, but H need not itself be in K. Canonical re-padding gives P(E(P(H)))=P(H). Hence no rank strictly decreases along BOTH steps P(H)->H->P(H). This is a counterexample to one-shot inference, not an all-algorithm obstruction.

## Computational controls

The standalone Python standard-library reproducer and full five-page LaTeX/PDF were generated locally. Finite checks PASSED: 14 growing SAT/UNSAT cases at m in {8,13,16,24,32,64,128}; 592 exhaustively pinned parity projections; five malformed source rejections; and four shared-variable counterexample cofactors. Physical bits for m=128: SAT parent 10,936,856 vs child 9,512; UNSAT parent 10,936,800 vs child 9,520. Second run produced identical SHA-256 226d39626a109a7af4488fb4dc230248abd545e74455e6355c3d95b616fda6c9.

Independent Library Connected_Interface_Audit.zip verification: REPORT.tex and audit.py inspected, source rerun, byte-for-byte JSON match SHA-256 05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca; 4680 boundary, 7191 local-discovery, 139 truth-table comparisons. Its static interface theorem is NOT a SAT runtime lower bound.

Resource ledgers (conservative construction UPPER bounds, N=parent bits): indexed RAM O(N^2) operations and O(N log N) bits; deterministic read-only input fixed multitape O(N^3) steps and O(N log N) work cells; one-tape input-inclusive O(N^4 log N) steps, O(N log N) total cells through full-scan simulation; fixed universal machine polynomial overhead. No native TM transitions were empirically measured. No general SAT hardness theorem follows.

Prior work: LSPV-2 CONNECTED-SEMANTIC-SHELL217 and PARITY-PORT-FORGETTING225 already contain simpler shell/forgetting ideas. This is a deliberately explicit NP-complete promise and recursive-closure counterexample, not a claim of conceptual priority. Inspected implementation files: cuddorg/cudd/cudd/cuddBddAbs.c (blob 62170e3b29aa), berkeley-abc/abc/src/base/abci/abcQuant.c (76bd7906bd5a), arminbiere/cadical/src/elimfast.cpp (0d6c00897acb), crillab/d4/preproc/Forgetting.cc (8f00f7397b70). OpenAI math recursion and compilation source blobs 65bf0450f460 and 869be8c325 do not construct the target-dependent oracle classically.

## Publication safeguard and next target

The verified complete .tex, .bib, .py, .json, PDF, and ZIP exist as current-conversation sandbox files, but cross-session Library uploads failed with "Container session expired"; full-file GitHub publication has not been verified. This note is a genuine GitHub-hosted status/theorem handoff and must not be misrepresented as publication of the complete package.

Next role target: constrain parity inputs shared with an arbitrary SAT core, prove pointwise correctness under charged cofactor acquisition, and seek or falsify repeated ordinary-SAT power-short closure. P=NP, P!=NP, ARC-EDGE-90 OPEN.
