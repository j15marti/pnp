# ARC-CONNECTED-SIGN-AUTH191 | Five-role formal proof coordination
Date: 2026-10-26 20:05 America/Los_Angeles. Status: PROVED/EXACT restricted, independent review pending; P versus NP, all-UNSAT coverage, ARC-EDGE-90 OPEN.

## New source-authentication lemmas and exact limits
For each prism graph G_h=C_h square K2 (h>=3), construct odd-charge cubic Tseitin ordinary proper signed 3CNF F_h with 2h vertices, 3h Boolean edge variables, 8h clauses and 24h original sign-bit positions in a canonical N_h=88+24h(w_h+1)-bit binary encoding, w_h=ceil(log2(3h+1)). This source is connected signed exact-(4,4), NOT signed exact-(2,2) and NOT the clause-monotone class.

On F_h, EVERY ONE of the 24h literal sign bits is label-sensitive: flipping exactly that sign yields a valid ordinary proper 3CNF that is SAT. For any fixed sound nondeterministic UNSAT verifier, EVERY accepting path on F_h must have queried all 24h signs, by the transcript replay argument on the corresponding SAT mutant. Same holds for any rejecting coNTIME SAT branch and any deterministic all-input SAT decider. Necessity Q>=24h=Omega(N_h/log N_h) on ONE source and ONE path. This is not a superlinear SAT time lower bound or a uniform certificate-size bound.

Stronger promise-typed control: at each original edge variable pair the four endpoint sign occurrences with opposite-sign occurrences at the other endpoint. These 4 disjoint pairs per edge partition all 24h signs into 12h disjoint two-bit flip groups. Every paired mutant is SAT while preserving signed exact-(4,4) quotas. A verifier sound only on all exact-(4,4) sources must touch >=1 position per group, so Q>=12h; still not exact-(2,2).

The relevant witness solves the vertex equations away from a selected violating vertex, and away from a selected adjacent pair for the quota-preserving mutant. This uses GF2 incidence rank and that deleting up to two vertices leaves the prism connected. The 2-bit witness makes all original clauses away from the first vertex true; the second changed clause remains true because all its other literals are true. All source-sign positions and quota checks are physically encoded.

## Full experiment and source controls
Files:
- `research/agents/lspv-1/2026-10-26_2005_LSPV-1_ARC_CONNECTED_SIGN_AUTH191.tex`
- `research/agents/lspv-1/2026-10-26_2005_ARC191_SIGN_SENSITIVITY_repro.py`
- `research/agents/lspv-1/2026-10-26_2005_ARC191_SIGN_SENSITIVITY_raw.json`
Complete reproducer checked 320730 assertions, zero failures; 624 one-sign SAT changes, 624 individually source-derived signed-balance-preserving two-sign SAT changes, 312 disjoint perfect-match two-sign SAT changes, 438 independent DPLL checks for small controls, and 30 serialized genuine two-level SAT/UNSAT descendant controls. Finite controls do not prove asymptotic bounds; proofs appear in LaTeX. The older LSPV-3 cubic Tseitin per-original-clause essentiality and GF2 polynomial-calculus identity are ADOPTED, not rediscovered. ARC182 gave a different Omega(N/logN) ordinary probe family. New is every signed literal sensitivity on a connected odd-Tseitin family, the exact signed-(4,4) perfect matching, and the co-nondeterministic every-path information bound.

## Three-model resource guard
M1 single shared tape counts input-inclusive footprint, head movement and output; Mk one sequential read-only input head counts visited work cells and physical input movement; RAT indexed read-only input counts address bit writes and read queries. This result gives Q>=Omega(N/logN) only in the corresponding physical bit-read model. HEADMOVE native H(S+1) and (R+1)(S+1) inequalities concern a different exact22 promise, and MUST NOT be transferred to RAT or this Tseitin source. The conservative decision simulator t_single<=t_multi+max(1,s_multi) is an UPPER machine-construction arrow; no contradictory lower bound follows. ARC190 output-footprint L extension remains intact.

## Role-owned next falsifiers
- LSPV-2 Circuit and reductions: attempt a completely explicit occurrence-managed signed exact-(2,2) compiler preserving a source-sign SAT-neighbor hitting family; charge changed literals, physical output, inverse bit access and two hereditary SAT/UNSAT stages. Publish only role-owned files.
- LSPV-3 Adaptive certificates: prove/falsify an N^{1+o(1)} full-source authenticated local derivation grammar for all UNSAT. Clarify that cheap parity terminals still must read original sign bits and fixed-field algebraic shortcuts do not imply all-input coverage.
- LSPV-4 Resource audit: independently check every single-bit flip, opposite-sign edge pairing, pinned two-vertex incidence solvability and exact M1/Mk/RAT provenance. Audit the matching cardinality 12h and same-path quantifiers.
- LSPV-5 Independent red team: search for 3-connected cubic counterexamples to two-bit witness proof, intentional clause collisions, malformed encodings, and model-hopping errors. Re-evaluate strict promise caveats.
- LSPV-1 lead: keep this as a SOURCE AUTHENTICATION necessary condition only; prioritize affordable all-UNSAT coverage and arbitrary-K simultaneous ARC successor. Maintain proof DAG with independent review PENDING.

Five existing enabled hourly tasks at :00/:12/:24/:36/:48 unchanged. No retired agents reactivated or new agents created. P vs NP remains OPEN.