# BALANCED-OCCURRENCE-FIREWALL243 (LSPV-1), 2026-10-30 01:00 PDT

PROVED/EXACT under proper original signed exact-(2+,2-)-3CNF. Original source occurrences share global variables; four local extreme modes are NOT independent global assignments. P vs NP OPEN.

## Corpus and duplication
Read active #3, AGENTS.md blob 19656af1, CODEX.md 754999f5, research skill b8df83a7, root main.tex d495942a (substantive with balanced ownership), LSPV-1 ARC240/241/242, LSPV-3 paired matching source blob 7326505b, LSPV-4 tree overlap and extreme Helly, W1 and S original source template blob f4a467c9, task hostile controls and primitive-trace tasks. The S/U four-way compatibility matrix, resolution, UP and 2SAT SCC are preexisting. New proven content here is a strict22 arithmetic/UP dominance firewall plus a precise equality-to-2SAT sufficient test. No first-to-discover claim.

## Proof obligations and scoped conclusions
Let m=4n/3. Every original variable has exactly two TRUE literal occurrences under every complete assignment, so sum_j t_j=2n. Every SAT witness obeys N1=m/2+N3. Given original-variable partial pin rho fixing k variables, let c_j be #fixed-TRUE source occurrences; Z=#c_j=0; H2=#c_j>=2, H3=#c_j=3. Identity H2+H3=2k-m+Z. Absence of an original uncovered empty/unit clause means uncovered clauses each contain >=2 free occurrences, giving 2Z<=4(n-k), therefore H2+H3<=m/2. The tempting count-based rule H2+H3>m/2 can NEVER discover an original cube beyond source UP, no matter whether SAT or UNSAT. If equality holds and no unit/empty, uncovered clauses each have exactly two free literals and every free occurrence is uncovered; residual is genuine 2CNF and SCC witnesses decide the cube exactly. Converse equality iff 2CNF is FALSE: K4 paired NAE pinned x3=x5=0,x6=1 has residual 2CNF but H2+H3=1 <m/2.

Source-authenticated CUBE9 original n=9,m=12 after pin (4,5,6)=000,(7,8,9)=111 has Z=6,H2=4,H3=2, no UP units. The residual is six 2CNF clauses C0..C5: (1,2),(2,3),(3,1),(-1,-2),(-2,-3),(-3,-1). Opposing implication paths 1 -> -2 -> 3 -> -1 and -1 -> 2 -> -3 -> 1 certify the ENTIRE pinned partial cube UNSAT. Original full formula is SAT. This is a known SCC consequence, newly connected to this equality ledger.

Further PROVED: two proper ternary clauses cannot both have exactly one true literal iff they have identical support and opposite sign-pattern parity. Hence pairwise exactly-one conflict graph is disjoint union of complete bipartite graphs and alpha>=ceil(m/2). Counting N1>=m/2 plus merely pairwise exactly-one conflicts cannot certify original root UNSAT. Triple clause counterexample (-1,-2,-3),(-1,-2,-4),(-1,3,4) is pairwise exactly-one feasible but globally exactly-one infeasible; ordinary CNF SAT.

## Computation
stdlib full reproducible Python seed 202610300100. 3,764 source indexed SS/SU/US/UU compatibility checks, 1,184 multi-clause checks, 120,756 strict22 coherent partial cubes checked, 496 ternary signed clause pairs (64 singleton-incompatible), all pass. W1 UNSAT baseline UP+DPLL vs enhanced count: 151 vs 151 recursion nodes, charged selected ops 21,739 vs 27,814. S SAT 12 vs 12 nodes, 1,078 vs 2,050 ops. K4 SAT 7 vs 7, 286 vs 484. CUBE9 SAT 4 vs 4, 452 vs 648. Includes source scanning, failed prefilter, UP, DPLL, witnesses, conflict leaves. Peak traced Python bytes and measured walls in full local raw. These are selected heterogeneous operation counts, not native TM steps, and no industrial CDCL claim.

## Provenance and known blockers
Published and readback verified complete public LaTeX:
https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-10-30_0100_LSPV-1_BALANCED_OCCURRENCE_FIREWALL243_PUBLIC.tex
blob 9992e1ddc53a8584cdc2317ef85cb1dbb29fe24a.
Compact checker:
https://github.com/j15marti/pnp/blob/main/research/agents/lspv-1/2026-10-30_0100_LSPV-1_BALANCED_OCCURRENCE_FIREWALL243_compact.py
blob 1817421ced797ccc79275275559caa9f1e315aee.
Full raw JSON SHA256 7bc1e04ab1c7f28b6b4ee80900e510a8ad8a398f91e7bce941e684d7b341cf95; full local bundle SHA256 ee99ee28c0dc9e00e050b13335776be56b811cbfb6164665a9d47fd44cff4020. Expanded PDF and source are attached to the conversation as sandbox downloads, NOT uploaded to GitHub. Persistent Library folder /PNP Formal Proof Lead/EXTREME243 exists, but PDF/ZIP upload attempts failed container_session_unavailable, so Library archival is PENDING. Local-only files are not cross-run shared.

## Five-role handoff
LSPV-1: next seek a source-authenticated triple-wise exactly-one obstruction eliminating full non-2CNF cube AFTER saturated UP, and charge acquisition.
LSPV-2: seek structural source family exposing triple-wise obstruction but evading obvious SCC/Horn/affine routes, supply source-index RUP paths.
LSPV-3: compare paired matching-cut cube restrictions against equality-to-2SAT on the SAME pinned SAT/UNSAT source instances.
LSPV-4: independently referee strict22 unit-dominance proof, especially equality and the triple counterexample; benchmark total work.
LSPV-5: reconcile only verified results into living main; preserve status OPEN on arbitrary-SAT and P-vs-NP. Do not modify task schedules or ownership.

Next load-bearing lemma: find a polynomially discoverable and checkable nonbinary (width >=3) UP-saturated cube contradiction from original triple-wise S/U or exact-one compatibility, with a net-work advantage on an infinite family. Neither P=NP nor P!=NP has been proved.
