# LSPV-4/418: single full-interface CNF child remains linear-size on expander Tseitin

**2026-11-05 10:36 PST. Route A. PROVED/RESTRICTED; P versus NP OPEN.**

## IDEA

Initial falsifiable hypothesis: LSPV-2/422's compact GF(2) boundary messages eliminate the exponential survivor table, but a **single explicit ordinary CNF guest child** representing the *entire* exact boundary relation still needs a linear-size input. Falsifiers: an inessential cut bit; auxiliary CNF omitting an essential variable; injective renaming reducing independent ports; free lazy input shortening the guest's logical source.

## SEARCH (actual inspections)

Read governing November 2 handoff (blob c3889a3e), issue #3 through LSPV-2/422, LSPV-2/422 exact report (blob 67386065), LSPV-4/417, AGENTS.md, CODEX.md and project research skill. Actual Grok report GROKPROOF/2026-11-05_1428_PROGRESS.md (a0e35e77) and Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727) were read; neither supplies the all-input contraction.

Primary research: Urquhart, Hard Examples for Resolution, JACM 34 (1987), DOI 10.1145/7531.8928; Ben-Sasson and Wigderson, Short Proofs Are Narrow, JACM 48 (2001), DOI 10.1145/375827.375835; FLMV, Time-Space Lower Bounds for Satisfiability, JACM 52 (2005), DOI 10.1145/1101821.1101822 (author PDF section 2.1 and screenshot of printed page 4). Fetched actual GitHub files: MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd19), openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (1ced21f4), konard/p-vs-np/proofs/complexity/README.md (7ee9a11e), blkph0x/p-vs-np-proof-research/affine_projection_recognition_lab/AFFINE_HULL_METHOD.md (bb1addfd). External affine hulls are not generally exact projected relations. Searched Urquhart expander resolution, Ben Sasson Wigderson, existential CNF parity ports, indexed FLMV machines and these repositories. Direct Google-branded search was unavailable; used indexed web plus authenticated GitHub.

## THEOREM 418.1, exact scoped statement and proof

Let G_H be a connected cubic edge-expander graph on H vertices, with edge expansion epsilon > 0 and an odd-charge Tseitin source. Its ordinary 3-CNF encoding has 4H width-three clauses and 3H/2 edge variables, hence N_H = Theta(H log H) input bits using consecutive variable IDs. For a balanced vertex cut S, |S|=H/2, the boundary B=delta(S) has b >= epsilon H/2 variables. Let R_S(x_B) be the exact existential projection of the S-vertex source constraints over the internal edges.

The incidence-matrix identity yields

$$
R_S(x_B)=\bigwedge_{C\in \mathrm{Comp}(G_H[S])}
\left[\bigoplus_{e\in\delta(C)}x_e=\bigoplus_{v\in C}\chi_v\right].
$$

Suppose a **single explicit ordinary CNF** Q(x_B,z), with any number of auxiliary variables z and any clause widths, is required to preserve this exact relation for *every* boundary assignment:

$$
\forall x_B\quad ((\exists z\,Q(x_B,z))\iff R_S(x_B)).
$$

Then every one of the b distinct named boundary variables must occur in Q, and under standard direct injective binary literal-ID serialization,

$$
|Q|_{\mathrm{bits}}\ge \sum_{i=1}^{b}(\lfloor\log_2 i\rfloor+1)
=\Omega(b\log b)=\Omega(N_H).
$$

**Proof.** On each connected component, internal-edge existential elimination leaves its single boundary parity equation because the connected incidence matrix has rank |C|-1. Every component has a nonempty outgoing boundary, since G_H is connected and S is proper. A satisfying boundary assignment exists by setting the last edge of each component to meet its charge. Flipping any one boundary edge then falsifies its component equation; hence every boundary variable is essential. If a boundary bit were absent from Q, its existential projection would be invariant when only that bit changed, contradicting exact equivalence. Distinct positive integer IDs have total digit length at least the sum of the b shortest positive-ID digit lengths. Expansion makes b=Omega(H), while source length is Theta(H log H), proving the lower bound.

**Scope:** This defeats the single full-boundary explicit-CNF-child version of the Route A repair, even with Tseitin auxiliaries and internal DAG sharing. It does NOT refute many smaller children plus an independently proved exact join, direct parity reasoning, lazy compressed non-CNF representations, or any arbitrary SAT solver.

## ITERATE, physical cost accounting, and control families

The /422 exponential 2^b mask is replaceable by O(H log H) exact affine rows. This is a genuine shortcut, not a hardness assumption. The new observation is that O(H log H) is still Omega(N_H), not O(sqrt(N_H)), when presented to one ordinary guest as a complete explicit interface CNF.

In the FLMV indexed-input random-access Turing-machine model, the write-only output tape is not a guest-readable input tape. A materialized L-bit child contributes Omega(L) all-phase peak writable space and Omega(L) write operations. A virtual child might use a short descriptor, but the logical ordinary guest input still has length L=Omega(N_H); claiming a T_A(N_H^(1/2)) guest bound requires a different proved simulation. Indexed accesses, index-tape erasure, cache updates, ancestor retention, failed policies, recomputation and output are charged. If a shared M-bit table is retained across K branches, it counts toward simultaneous peak even though its logical DAG computation is counted once. Discarding it can require K repeated reconstructions. Work, span, physical sequential time and peak space are distinct.

The hypothesized transformation needs

$$
t'\le\max\{11/10,3/5+t/2\},\qquad
s'\le\max\{\rho,\eta,\lambda,\lambda s\},
$$

with rho covering **all preprocessing**, eta all retained concurrent state, lambda actual child input exponent. In this single-full-interface compiler lambda >= 1-o(1), not 1/2. The separate FLMV conditional numerical gap beta(6/5)-1/2=1/90 remains correct. No universal transformation is proved.

**Finite tests:** Python producer 267 checks; independently authored Node referee 456; additional independent compact Python audit 213. K4, cube, Petersen and Heawood, eight original-source even/odd charges, malformed/corrupt controls, per-bit essentiality, exactly projected small cuts, fresh XOR-gate 3-CNFs with auxiliary variables. The b=21 Heawood truth table was **sampled**, not exhaustively checked. Source input bits: 1304,2720,3520,5120. Selected boundary widths 4,4,5,21; explicit projected CNF bits 808,928,1312,3664. Heawood has a 79-bit bare binary variable-ID lower bound, exceeding sqrt(5120) as a finite illustration only, not an asymptotic hidden-constant claim. Host-language memory is not physical FLMV workspace.

**Family/theorem ledger:** Suitable odd-charge cubic expander 3-CNFs, H vertices, 4H clauses, N=Theta(H log H) have published exp(Omega(H)) *ordinary shared-DAG Resolution* proof-size hardness (Urquhart; Ben-Sasson/Wigderson); no arbitrary-machine hardness follows. Preexisting authenticated /341 mixed calculus proves full-mixed exact W_Rmix341(F_H)=4H-1 on bridgeless cubic graphs via algebraic reduction. Route A's all-input recursively iterable same-machine A -> Phi(A) remains **OPEN**; Route B B3 independently OPEN. No change to R_mix341, weights, task settings or root manuscript. P versus NP OPEN.
