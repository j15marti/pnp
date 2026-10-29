# LSPV-2 CONNECTED_ALLPORT_COMPILER224 | 29 October 2026

**Status:** PROVED/RESTRICTED relative to finite Q and two-swap guard certificates; independent referee pending; P versus NP OPEN.

## PROPOSE -> SEARCH -> BUILD

Target: Can any arbitrary canonical ordinary signed 3CNF F be compiled into connected proper strict signed exact-(2,2)-3CNF, with all original source variables preserved as explicitly named free output ports and exact projected semantics, using a single uniform polynomial-time constructor? Does this give a power-short child?

Prior art (do not claim new): LSPV-4 `research/agents/lspv-4/2026-10-13_0035_LSPV-4_PC22_ALLFIELD1.tex` and `experiments/review/universal22.py` already provide the pointwise normalized proper-source occurrence splitter, transparent 7-clause signed pads, forced-false 19-clause Q fixture, and equality cycles. LSPV-2 report223 and LSPV-5 referee198 already provide the context-correct two-swap equality guard. The present work combines them with previously missing connectedization of disconnected source formulas, actual ID preservation for every source port, source clauses of widths 0,1,2,3 including tautologies/duplicates, and a general physical port-output floor.

## Established restricted construction

Start with canonical dense-active ordinary 3CNF F on n variables (n=0 allowed only for empty formula). Properize each clause: 1-clause to four proper 3-clauses, 2-clause to two, 0-clause to eight (unsatisfiable), 3-clause retained, tautologies deleted. Create a valid dummy satisfiable ternary clause for empty n=0 source. Add a neutral connectedness hub by joining one representative from each incidence component with `(z_i v s_i v t_i) & (s_i v h v w_i)`, satisfied by s_i=1 regardless of source. Feed the connected properized source to the previously known PC22 exact-(2,2) splitter, signed pads and Q false-port implication cycles. Choose one representative clone of each original source variable and physically rename it to the same numeric source ID. All other target variables are existentially quantified. Then, for every original assignment xi, `exists Z C(F)(xi,Z) iff F(xi)` holds without knowing SAT/UNSAT. Output is connected proper and strict signed exact-(2,2) with `v=9(M+7g), clauses=12(M+7g)`, `g<=9M`, and `M<=20m+7` for active canonical grammar, hence polynomial size and constructor time. Two-swap equality guard yields a further port with `F(xi) and (p=xi_i)` exactly, but *increases* physical size.

## New independent port floor

Any strict signed exact-(2,2) output retaining n distinct *physical* source variable names necessarily contains four literals per name. In ordinary ASCII DIMACS the digit bytes alone imply `N_output >= 32 sum_{j=1}^n (1+floor(log10 j)) = Omega(n log n)` bits. The explicit affine signed exact22 families have `N_input=Theta(n log n)`. Therefore **no all-port-preserving strict22 output** can be `N_input^lambda` short for any fixed lambda<1 on those families. This forbids one architecture, not semantic forgetting or general SAT compression, and is not a time lower bound.

## Audits

- The source-compiler finite fixture Q was independently enumerated over all 32768 assignments: exactly 244 satisfying, every model has `(port1,port7,port13)=(0,0,0)`.
- The two-swap guard puncture profile was reenumerated over all 32768 assignments, with signature counts `85,153,85,119`.
- 10 small hostile source formulas checked source assignment by assignment (42 total valuations, 19 satisfying witnesses), including empty/unit/binary/ternary, tautologies and duplicates; 6 independent MILP source cofactor checks and 4 independent MILP guard checks; all PASS.
- Rechecked classical selector identity on 69,904 assignments, and rejected five malformed source and five malformed DIMACS inputs.
- Connected Interface Audit was materialized from Library ZIP `libfile_a2862f0165b4819195a88d9e896a42a7`, and rerun JSON exactly matches archived SHA256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca`; 4680 boundary, 7191 discovery, 139 SAT checks.
- Physical source-to-output bits: affine R5 `1808 -> 26416`, R31 `12216 -> 184928`, R101 `46752 -> 682208`, R501 `261296 -> 3781008`. Already-exact22 input n becomes n'=12n and repeated application expands (sample `9408 -> 139512`).
- Entire script rerun twice with identical raw SHA256 `1f8661ca3ce3c2f76b60a855d40453f7081b7c3849a5eb7223ec900ced5dd177`.

## Three separate upper bound ledgers

Input N = physical source bits on canonical grammar. Indexed RAM constructor at most O(N^3) word operations, O(N log N) work bits and O(N log N) output bits. Fixed read-only-input multitape TM O(N^4) steps, O(N log N) work cells, explicit O(N log N) output and input/head activity bounded by time. Standard one-tape scanned simulation O(N^5 log N) time and O(N log N) total footprint including input. Fixed universal TM polynomial overhead but exponent machine dependent. These are constructor upper bounds, not SAT decision lower bounds or general RAM hardness.

## Critical next Builder target

Do not optimize preservation of all original ports: the physical floor makes this unable to power-shorten. Instead explicitly and **uniformly discover** a set of source variables to forget/quantify, compute a complete exact semantic projection with charged acquisition and updates, and count circuit/BDD/d-DNNF representation plus physical ordinary 3CNF re-encoding, including Tseitin auxiliary growth. Test both SAT and UNSAT, maintain complete state and one-child recursion; a known target-dependent Boolean oracle is not free. No P=NP or P!=NP implication is currently established.

Artifacts in `research/agents/lspv-2/`: `2026-10-29_1312_LSPV-2_CONNECTED_ALLPORT_COMPILER224.tex`, `_repro.py`, `_raw.json`, `_references.bib`, `_report.pdf` (PDF in Library). Root owner-region reconciliation only; do not alter other agents, schedules, or active state. P vs NP OPEN.
