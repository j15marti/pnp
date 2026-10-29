# ARC207: One-child bit descent and pivot-projection handoff

**LSPV-1, 2026-10-29 00:05 UTC.** Independent cross-role review pending. P versus NP OPEN. All original five task identities, enabled states, ownership and staggered schedules preserved.

## One exact missing arrow

Construct ONE uniform deterministic unconditional polynomial-time map C on every valid instance x of a closed NP-complete SAT encoding, preserving SAT and UNSAT, closure, and directly decidable finite bases, satisfying

\[
 |C(x)|\le |x|-1,\qquad
 \mathrm{SAT}(C(x))\iff\mathrm{SAT}(x).
\]

All parsing, failed choices, source access, output, temporary caches, and recursive restarts must be counted in one declared machine. The one-bit target is weaker than a power-shrink child of size N^lambda, but it is sufficient for P=NP: at most N successive calls, with aggregate time O(N^(c+1)). A power shrink needs O(log log N) levels. The bare *existence* of an efficient shrinker is equivalent to P=NP, because a preexisting decider could print a fixed YES/NO instance. That reverse direction is CONDITIONAL, and not an acceptable noncircular construction.

## New representation-restricted theorem

For F_t(z,x)=AND_i(z OR (a_i OR b_i)) AND_j(NOT z OR (c_j OR d_j)), using pairwise distinct variables, existential elimination has both the t²-clause four-literal CNF and the compact (4t-1)-gate shared circuit

\[
G_t=(\bigwedge_i(a_i\vee b_i))\vee(\bigwedge_j(c_j\vee d_j)).
\]

**PROVED/EXACT restricted, independent referee pending:** any equivalent CNF over the same 4t original variables without auxiliaries has at least t² clauses, permitting negation, arbitrary widths and repeated literals. There are t² distinct minimal falsifying assignments x_ij. Any clause falsified at x_ij and made true by each single zero-to-one flip must include all four positive coordinates a_i,b_i,c_j,d_j, and cannot also be falsified by a different x_pq. The standard resolvents meet the bound. Auxiliary variables, shared DAGs and decision-only equivalent formulas are not covered. Standalone F_t is always SAT, so this is no SAT-decision lower bound.

**COMPUTATIONAL:** independent Python and Node.js versions verified 69,904 assignments t=1..4. The canonical JS audit also exercised 559,232 disjoint-core truth settings and 354 resolvent separation pairs, all zero failures.

## OpenAI source and scoped search

Actual source in openai/math main commit 7ef5c0cc5ca4b0e072b7a050fca09ab24bc6fa3a, directory preprints/Polynomial-Time-Unitary-Synthesis-from-a-Boolean-Oracle-October-5-2026/build/sections: 01-introduction.tex states exists A_n forall U exists f with no efficient target-oracle construction. 03-contraction.tex gives M=4096(n+1)^2, s=max(1,floor(q/M)), k=d-s. For d=2^n and n>=2, k>2^(n-1), so the first dimension reduction retains the full n-bit index width. 06-recursion.tex uses the smaller quantum circuit exactly once. 07-compilation.tex stores slot contents in the oracle. This is only an architectural analogy to the desired classical SAT contraction.

GitHub searches specifically targeted SAT kernelization, one-child self-reduction, clause elimination, compression, shared circuits and bounded-treewidth methods. Actual arminbiere/cadical/src/elim.cpp skips pivots with excessive resolvent growth; dbueno/funsat/src/Funsat/Circuit.hs explicitly uses DAG sharing. Neither gives universal bit descent. Fortnow--Santhanam 2008, Dell--van Melkebeek 2014 and Fernau et al. 2016 were inspected for the precise conditional kernelization context. No found source solves the missing arrow; absence from search is not a theorem.

## Native ledgers and complementary roles

Single-tape RW: count original input in footprint, physical head moves, writes, output and restarts. One-read-only-input multitape: charge all work cells, traffic and generated-child access. Two fully writable tapes: count symbol changes on both tapes, no illicit work-only D2 bound. Indexed RAM: charge full materialization and simultaneous time/workspace before any FLMV comparison. Fixed UTM: one program across SAT and UNSAT; no free oracle truth table or answer-class advice.

LSPV-1: own closure, base cases and quantified one-bit descent theorem. LSPV-2: implement a bit-serialized CNF, DAG and Tseitin successor on connected exact22 hostiles; report true output lengths. LSPV-3: attempt effective adaptive one-child selection and source authentication on BOTH answer classes, including failed choices and proof discovery. LSPV-4: independently transport a concrete SAME solver, and check only native strict FLMV hypotheses. LSPV-5: red-team the t² lower bound with unusual clauses, auxiliary variables, semantic-only compression, and padding; reconcile main.tex markers.

## Artifacts and root publication safeguard

Role-owned report: research/agents/lspv-1/2026-10-29_0005_LSPV-1_ARC_SINGLE_CHILD_DESCENT_PIVOT207.tex

Canonical executable and data: research/agents/lspv-1/2026-10-29_0005_ARC207_pivot_repro.js ; research/agents/lspv-1/2026-10-29_0005_ARC207_pivot_raw.json

Independent replica: research/agents/lspv-1/2026-10-29_0005_ARC207_independent_python_check.py

Root main.tex at last audit lacks the ownership markers prescribed by AGENTS.md, so LSPV-1 is not authorized to edit or restructure it. Root synchronization remains PENDING LSPV-5 structural initialization. Earlier restricted findings stay valid in their original models. P versus NP remains OPEN.
