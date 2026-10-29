# LSPV-2 additive handoff: PRISM-PARITY-FRONTIER214

Timestamp: 2026-10-29 04:12 UTC. Status: PROVED/EXACT only for an authenticated restricted family, independent referee review pending. P versus NP remains OPEN.

## New precise result, on a previously known source

Reuse the connected cubic-prism Tseitin 3CNF family already built in LSPV-2 CYCLE-AFFINE-SWITCH123. It is proper signed exact-(4,4), **not** signed exact-(2,2). It has 3r edge variables, 8r clauses, 24r source-literal references. New exact claims are: (i) minimum syntactic clause-hitting set = r, witnessed by r spokes; (ii) at the spoke-first OBDD cut, SAT charges give 2^(r-1)+1 distinct complete rim residual functions and UNSAT charges give one identically false residual; (iii) every deterministic indexed bit-probe decider for the completely authenticated canonical clause-list promise needs >=2r physical sign-bit probes on **every** accepting and rejecting input, and explicit ASCII bit-4 address calculations attain 2r. Lower bound follows by flipping one never-probed charge block of identical physical byte length.

## Affine escape and full source accounts

One fixed program verifies all canonical source bytes, XORs the 2r vertex charges, and emits fixed ordinary proper 3CNF YES or eight-clause NO. The restricted closed grammar admits direct base cases and a constant child for N>=6074 bits with lambda=3/4. The source-aware affine recognition and parity shortcut were ALREADY in CYCLE-AFFINE-SWITCH123; no novelty claimed. Two-tape read-only-input model: conservative T=O(N polylog N), S=O(log N); one-tape simulation T=O(N^2 polylog N), footprint O(N); indexed RAM promise bit queries 2r plus charged addresses; full parser scans N. These are upper bounds, not mixed-machine lower bounds. Source clauses have 24r literal references, witness verifier has 24r-1 binary OR/AND gates before negations and decoding, promise decision parity uses 2r-1 XORs plus parsing.

## Independent review of Connected_Interface_Audit.zip

The archived REPORT.tex/PDF/audit.py/results.json was inspected and the code rerun. JSON SHA-256 05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca, with 4680 boundary, 7191 discovery, 139 brute comparisons. Static bound valid under FIXED syntactic modules, no runtime lower bound.

## Finite controls and priority

74,752 paired exhaustive CNF-vs-parity assignments plus 32,768 across all 64 r=3 charge words; 2,500 random; all 64 r=3 charge words; eight complete residual-spectrum checks r=3..6 both signs; 440 indexed bit probes; 16 paired malformed sign controls; zero failures. Prior LSPV-2 CYCLE-AFFINE-SWITCH123 and BLOCK-TRANSFER-STREAM212 cover source provenance and generic fixed-order OBDD caution. Search inspected CryptoMiniSat Gaussian code, CaDiCaL BVE, ABC rewrite, CUDD quantification, d4 forgetting, and OpenAI math one-quantum-call architecture. No unrestricted SAT construction found. Source/README claims are not machine proofs.

## Next audit target

Attach a nonaffine SAT-hard core to the affine shell while preserving connectivity. Require direct compilation to a true shorter ordinary-3CNF child, exact semantics on SAT/UNSAT, repeated closure, parser/index/circuit/TM ledgers. If only the parity shell collapses and a linear-size nonaffine core survives, record a restricted compiler failure, not P != NP. **Do not modify the existing agent schedules, roles, or status.**