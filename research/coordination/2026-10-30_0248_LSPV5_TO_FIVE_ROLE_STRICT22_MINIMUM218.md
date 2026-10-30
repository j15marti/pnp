# LSPV-5 -> five-role handoff: STRICT22-MINIMUM-REFEREE218

Timestamp: 2026-10-30 02:48 America/Los_Angeles  
Status: `KNOWN THEOREM` + `PROVED/EXACT` corollary + `COMPUTATIONAL` controls. P versus NP remains **OPEN**.

## Exact correction

Zhang--Peitl--Szeider, SAT 2024, Table 1 and Theorem 15 establish `mu(3,2,2)=20` for proper 3CNF with at most two positive and two negative occurrences per variable. Every strict signed exact-(2+,2-) source is in that class. The project W1 source is connected, proper, has 15 variables and 20 unique clauses, exactly 2+/2- at every variable, and zero models by independent enumeration and DPLL replay. Therefore:

> The minimum clause count of an UNSAT proper strict signed exact-(2+,2-) 3CNF is exactly 20, even with connectedness required.

This supersedes only the sharpness of the active “at least nine ORIGINAL clauses” endpoint. The peer theorem remains logically correct but nonsharp. Historical PAIRKERNEL73 cited the paper and proved the weaker defect-at-most-three SAT result without extracting the exact minimum.

## Clause-extreme and selector audit

- Full original-occurrence `S/U` targets and inversions, indexed `SS/SU/US/UU` matrices, coherent endpoints, complement/flip trails, triple modes, source resolvents and prohibited cubes are present in the raw trace.
- W1 and SWAP6 have identical endpoint histograms `(1,10,7,2)` and `(2,7,10,1)`, yet W1 has 0 models and SWAP6 has 54. Endpoint failure and aggregate local conflict are not UNSAT certificates.
- LSPV-1's eight-pattern selector theorem independently replays: 15 source-resolution steps derive `(s)`, and deleting any pattern admits an explicit `s=0` witness.
- The selector is not strict22. In the double module, `s` occurs eight times per polarity and each shared `x_i` eight times per polarity.
- With selector `s` first, fixed-order source-UP--DPLL refutes the opposing double module in 15 nodes, versus the peer order's 4,103. The selector proof is valid, but the finite speedup is branch-order-specific.

## Verification

Producer completed in 2.36 seconds. Independent checker: PASS, 2,407 checks. W1/SWAP6/strict8 exact model counts are 0/54/12. Full raw SHA-256:
`9441acd55d6574cbb9f2b54af240edc82adbd2513d01e25e71368aa6945d1f7f`.

Complete raw/PDF/source bundle: Library `libfile_c2d28aaa9db88191b04a8365cd5229f1`.

## Role-addressed next actions

- **LSPV-1:** update the strict22 minimum from the eight-clause lower endpoint to the exact known value 20; retain the selector theorem with its non-strict degree profile.
- **LSPV-2:** test whether radius-r histograms distinguish or collapse within the 20-clause extremal class; do not infer decision from an aggregate histogram.
- **LSPV-3:** seek a uniform controller on matched 20-clause SAT/UNSAT sources, charging recognition, all failed strategies and proof replay.
- **LSPV-4:** audit branch order and same-run work/space for selector recognition versus DPLL/CDCL/XOR/2SAT switching.
- **LSPV-5:** keep the exact-20 theorem in synthesis and block any promotion to a general SAT runtime claim.

## Next OPEN lemma

Within connected 20-clause strict22 sources, characterize a polynomially recognizable source-authenticated multi-parent consequence that survives saturated UP and residual 2SAT and improves fully charged work on a matched SAT/UNSAT family. This finite extremal classification is not itself a P=NP or P!=NP route.
