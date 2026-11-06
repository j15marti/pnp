# LSPV-1/438 | Edge-shared guarded parity product port (Route B)
**November 6, 2026, 00:18 PST.** PROVED/EXACT elementary Boolean/GF(2) identity; COMPUTATIONAL original-source controls; CONDITIONAL historical mixed upper bound; B1/B2/B3, historical grammar, full mixed superpolynomial lower bound and P versus NP OPEN.

## IDEA -> SEARCH -> ITERATE
Hypothesis: the existing /436 proper-three guarded odd-Tseitin family has a uniformly edge-shared affine port, so one missing *local* source-to-row native certificate suffices for a linear global refutation. Falsifiers: F1 port fails at g=1 or g=0; F2 shared w_e used across two vertices is inconsistent; F3 row XOR fails to cancel an edge or sign; F4 actual historical R_mix341 parser cannot compile each row from its real source clauses and paid owner references. F1–F3 were disproved by proof and independent finite checks. **F4 remains OPEN.**

**Duplication correction:** LSPV-1/436, blob `2c72bdf3934f91188e330fa628207ac1a02c5d68`, already proved this exact guarded + four-pad CNF minimally UNSAT with 2m+4 indispensable clauses and a 2m+3 all-binary paid-node source floor. The current finite K4 source SHA256 `bc669b8665a3ab0dcb132fbae71fdf5396b9dd3522cb616f0f669f1982ec2755` matches /436 exactly; neither its source witnesses nor its 51-node RES certificate is claimed new. The new focus is the conditional affine product port using a single shared conservative gate per edge.

## Established 3-CNF family ledger
Let G_h be connected simple **bridgeless cubic**, h even vertices, n=3h/2 edges, with odd charges chi_v. F_h contains exactly four signed proper 3-clauses for each local equation XOR_{e incident v} x_e = chi_v; m=4h original sources. XOR of all local equations proves UNSAT. Clause indispensability holds on bridgeless cubic graphs; /341 gives a 4h-1 semantic mixed AND3/GF(2) proof. On suitable *expanding* cubic sequences, ordinary unrestricted shared-DAG Resolution needs 2^{Omega(h)} lines (Urquhart 1987; Ben-Sasson–Wigderson 2001). This is not unrestricted algorithmic or mixed-calculus hardness. Indexed encoding length Theta(h log h).

Use /436's already authenticated exact proper-three encoding:
$$
K(F_h)=\bigwedge_{i=1}^{4h}[(g\lor a_i\lor y_i)\land(\neg y_i\lor b_i\lor c_i)]\land\bigwedge_{s,t\in\{0,1\}}(\neg g\lor p^s\lor q^t).
$$
It has 8h+4 original proper three-clauses and 11h/2+3 variables. Every clause is indispensable, hence **W_R(K(F_h)) >= 8h+3** for any sound source-authenticated, conservative, at-most-two-antecedent unit-paid calculus. /435–/436 prove ordinary Resolution hardness preservation by whole-DAG signed substitution/restriction, not equisatisfiability.

## Theorem 438.1, exact semantic product identity
Define exactly **one** conservative signed two-input AND output for every original edge:
$$w_e=(\neg g)\land x_e.$$
For each cubic vertex v the four signed guarded parity clauses (after existentially eliminating their four private y variables) are exactly equivalent, under the three incident gate definitions, to
$$\boxed{\bigoplus_{e\ni v}w_e\oplus\chi_v g=\chi_v.}$$
Proof: at g=0, each w_e=x_e and the row is the original vertex parity; at g=1, all w_e=0 and the row reduces to chi_v=chi_v. The port is unconditional and has no assumption leakage. Summing h such rows with h-1 binary GF(2) steps cancels every edge wire twice, leaving g=1 for odd total charge. The four original negative-guard pad clauses yield not-g by three ordinary Resolution nodes.

This is **not** a historical native refutation: obtaining a row via a semantic equivalence test is not a free LOCAL-CONVERT or AND3. In particular an AND3 over g and three original edge variables has four-variable support and is impermissible as one native step; original /341 does not uniquely specify DEF facets, exported/private wires and exact LOCAL parser.

## Proposition 438.2, falsifiable conditional native upper
**IF** the unchanged historical R_mix341 accepts a uniform at-most-c *paid*, at-most-two-parent micro-certificate at each vertex deriving its exact row from the actual eight original indexed split clauses plus its three referenced shared DEF owners, with source ancestry, facet selectors and bounded-support LOCAL checks actually verified; **AND IF** its one-variable GF(2) row g=1 can be made the unit clause g by one paid LOCAL, then the complete original-source-refutation has
$$
\boxed{W_{R_{\mathrm{mix341}}}(K(F_h))\le (c+5/2)h+4.}
$$
Count: 3h/2 shared paid DEF owners + ch local-paid macro nodes + (h-1) GF(2) joins + 1 LOCAL + 3 RES for pad + 1 RES for empty. Reference costs are paid as historically defined; no alternative unit rule or new split/discharge is added. The existing 8h+3 source floor forces c >= 11/2 asymptotically if this unit-cost macro exists. This is a **consistency check**, not a constructed native macro. An accepted instance would show this published-family candidate has linear full-mixed work, and should be retained as an upper-bound control.

## Executed falsification
Independent Python truth checked all g and original x assignments: 72,192 local port comparisons for K4, K3,3 and cube, all passed. Independently authored JS replay passed 72,199 assertions and rejected the invalid naive w_e=x_e substitution at g=1. The symbolic sum in each graph ended exactly at row g=1. K4/K3,3/cube old /436 source-deletion regression used 36/52/68 indispensable source witnesses and an independent JS RES verifier with 13,650 checks, six corruptions rejected; native historical Rmix checker was **not** executed. Ordinary RES certificates: 51/103/219 paid nodes, ideal depths 8/11/14, source ASCII lengths 384/580/776 bytes. See the role-owned reproducibility archive in this run for full Python producer, independent JS verifier, original DIMACS, proofs, raw witness assignments and SHA256SUMS.

## Corpus, literature, and provenance
Read governing 2026-11-02 five-role handoff `c3889a3e`, current issue #3, historical /341 `c87acd11`, /434–/437, peer LSPV-3/441 `437bf093` and /436 `4d3cfc1`, LSPV-5/379, actual GROKPROOF/2026-11-06_0515_PROGRESS.md `93f9202`, Claude ONETAPE `9a5b05d6`, AGENTS.md `19656af1`, CODEX.md `754999f5`, research skill `b8df83a7`. External source files actually read: konard/p-vs-np/README.md `0e0ec77f` and scripts/proof_status.json `93b77ed3`; blkph0x/p-vs-np-proof-research/README.md `f397a774`, METHOD_INDEX.md `18d693ea`; meelgroup/frat-xor/format.md `986a21aa`. Indexed literature included Cook–Reckhow 1979, Urquhart 1987, Ben-Sasson–Wigderson 2001, and Pich–Santhanam JACM 2026. No direct Google-branded interface or Lean replay was available. External project repositories are hypotheses/controls, not P-vs-NP authorities.

Host runs observed Python 0.0602 seconds / 97,040 KiB peak RSS for original-source proofs; Python 0.0594 seconds / 95,708 KiB for new port truth controls; independent Node replay 32,751,616 RSS bytes. No same-machine TM exponent claim. Actual implementations still charge original parsing, source/index/head reads, all gate bits and references, search/construction, failed branches, proof output, validation, retention/recomputation and all-phase simultaneous peak space.

**Next exact gap:** authenticate a bounded native vertex-row certificate or disprove such a micro-certificate under the true unmodified /341 grammar. A linear mixed proof on this family would invalidate it as a full-mixed hardness witness, not prove B3. Noncircular SAT-in-P => polynomial Wbar of the SAME R, superpolynomial all-mixed Wbar, B1/B2/B3, and P versus NP remain OPEN.