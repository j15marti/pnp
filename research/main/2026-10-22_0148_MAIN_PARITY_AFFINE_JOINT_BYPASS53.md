# PARITY-AFFINE-JOINT-BYPASS53

Timestamp: 2026-10-22 01:48 Asia/Seoul

## Outcome

The newest ARC and RP reports combine into a single uniform counterexample to promoting verifier/circuit structure into language hardness. There is a uniform RP verifier for a trivial language whose accepting tapes have no short positive subcube certificates, and on an infinite robust affine subfamily every exact ordered residual diagram has exponential width under every variable order. These two strong structural obstructions coexist, yet the language is decided by inspecting one input bit.

This is a falsifier for a proof interface, not a proof of P=RP, P!=RP, or P!=NP. P versus NP and P versus RP remain OPEN.

## Repairs proposed before source review

1. **Language-bypass test.** Before promoting any verifier, Circuit-SAT, certificate-width, residual-width, ANF-degree, or digest claim, state the underlying language and test an independent deterministic algorithm that ignores the selected verifier.
2. **Sufficient-not-necessary discipline.** Use short positive certificates only as a sufficient derandomization condition. Failure of that condition is not evidence for P!=RP.
3. **Compiler-specific ARC status.** Treat every-order residual width as a no-go for ordered residual enumeration only. An ARC claim must also exclude algebraic elimination and other source-aware representations while preserving all-input heredity and peak-resource charges.

## New role evidence

- `research/agents/arc/2026-10-22_0124_ARC_ROBUSTORDER29.tex`, verified at GitHub commit `1afc2579aba408e9f66db57d88b5318110c3ec26`, proves an existential robust binary matrix family whose affine relation has exponential balanced-cut residual width under every variable order. It explicitly retains Gaussian elimination as an easy bypass and leaves unrestricted ARC/FLMV OPEN.
- `research/agents/rp-separation/2026-10-22_RP_POSITIVE_CERT17_HANDOFF.md`, verified at GitHub commit `091807fbda92d1d66f2439f853d9e1831bd50c87`, proves deterministic simulation for RP verifiers whose every YES accepting set contains an O(log n)-coordinate positive subcube certificate. It also shows high acceptance density does not imply such certificates.
- The shared Google document was readable but contained no later substantive role report.

## Construction

Let H be any n by 2n binary matrix. Let u and v each contain 2n bits, and define

F_H(u,v) = PARITY(u) XOR 1[Hv=0].

The ordinary input is x=(n,H,b), where b is one selector bit. Define the uniform verifier

R(x;u,v) = b AND F_H(u,v).

The recognized language is exactly

L = {(n,H,b): b=1},

which is in deterministic linear-time input inspection and, under a canonical record format, can be decided by reading the selector field.

### Exact RP behavior

For each fixed H and v, exactly half of all u have the required parity. Therefore:

- if b=0, every random tape rejects;
- if b=1, exactly half of all random tapes accept.

Thus R is a uniform RP verifier for L with exact YES acceptance 1/2. H is part of the input, so no nonuniform matrix advice is hidden in the verifier.

## Positive-certificate lower bound

Any positive subcube certificate for F_H must fix all 2n coordinates of u. If one u-coordinate remains free, hold every other free coordinate fixed and flip only that bit. PARITY(u), and hence F_H, toggles. The subcube therefore contains a rejecting point.

Consequently every accepting tape has primary-coordinate positive-certificate width at least 2n, even though L is in P. POSITIVE-CERT17 remains a correct sufficient theorem; its converse is RETIRED.

## Every-order residual width

Use a robust H supplied by ARC-ROBUSTORDER29. Write P for the first n v-coordinates encountered by an arbitrary total ordering and Q for the remaining n. For each right side c in

im(H_P) intersect im(H_Q),

choose a P-assignment producing c and set all previously read u-bits to zero. The remaining residual is

PARITY(u_remaining) XOR 1[H_Q v_Q=c],

up to a fixed constant. Distinct c give distinct residual functions. Therefore the width immediately after the nth v-coordinate is at least

2^lambda, where lambda = rank(H_P)+rank(H_Q)-rank(H).

For the matrices in ARC-ROBUSTORDER29, every balanced submatrix has rank at least n-k+1 with k=ceil(2 sqrt(n)), so

lambda >= n-2k+2

and the ordered residual width is exponential for every variable order. Interleaving u variables cannot remove the bound.

## Why the joint obstruction still does not imply hardness

Given H,u,v, the verifier computes parity and the affine syndrome directly. In a random-access/RAM implementation this takes O(n^2) bit operations. A streaming implementation can evaluate one row at a time; its exact random-tape storage or reread cost must be charged in the chosen machine model, but it remains polynomial. More importantly, the language algorithm ignores the verifier computation and returns b.

Thus all of the following may hold on the same YES instance without language hardness:

- exact RP acceptance 1/2;
- no o(n)-coordinate positive certificate;
- every-order exponential residual width;
- growing ANF degree;
- a polynomial-size fanin-two circuit;
- unique deterministic gate traces after Tseitin conversion.

The residual lower bound blocks a specific compilation strategy. The certificate lower bound blocks a specific universal-set simulation. Neither quantifies over all deterministic language algorithms.

## Circuit-SAT / Tseitin / digest integration

The verifier has a polynomial-size circuit computing row parities, the zero-syndrome indicator, PARITY(u), and the final selector AND. A functional Tseitin or the verified parsimonious proper-3CNF conversion gives one auxiliary trace for every primary random tape and preserves projected acceptance exactly.

- Gate sharing reduces repeated parity computation but does not remove the selector-language bypass.
- Unique trace assignments do not imply a unique or hard primary witness.
- Full Tseitin-assignment density differs from projected random-tape density by the deterministic trace factor.
- Hashes or digest portfolios of the trace remain verifier fingerprints; they do not prevent the deterministic algorithm returning b.
- Canonical gate inspection exposes the final selector. Scrambling may hide that local pattern, but a short-seeded scramble is chargeably invertible and an arbitrary incompressible scramble is not a uniform hardness proof.

## ARC/FLMV consequence

ARC-ROBUSTORDER29 is ESTABLISHED as a no-go for exact ordered residual compilation, even with source-chosen static order. The new joint verifier shows that augmenting this width with large positive-certificate width or high acceptance density still does not create an all-input contractor or a SAT lower bound. The missing ARC arrow remains a solver-dependent, source-aware factorization that handles nonaffine contexts and charges generation, failed calls, source rereads, index tapes, recursion, output, and simultaneous peak space on the FLMV machine.

## Finite audit

`experiments/review/2026-10-22_parity_affine_joint_bypass53_audit.py` passed 449,124 assertions. It checked 17,568 balanced cuts of six explicit finite matrices, 69,632 complete verifier assignments, 274,432 certificate-flip controls, 90 independent residual-count identities, exact half acceptance, selector behavior, and ANF degrees three and four. The asymptotic robust-matrix theorem is inherited from ARC-ROBUSTORDER29; finite search is not a substitute for it.

## Status ledger and next discriminating tests

| Role | Status | Boundary | Single next test |
|---|---|---|---|
| :00 SAT to ordinary MKTP | OPEN | Structural circuit complexity, residual width, and certificate width do not yield the required both-label ordinary-KT gap. | Feed this verifier family through one proposed target and exhibit the direct indexed program using H, u/v indices, and the selector before claiming HIGH. |
| :12 P != RP | POSITIVE-CERT17 ESTABLISHED restricted; separation OPEN | Short certificates suffice for P, but their absence does not imply a language outside P. | Recover one actual WRAPPER DAG, collapse deterministic trace coordinates, and test both certificate width and the independent language bypass. |
| :24 ARC/FLMV | ROBUSTORDER29 ESTABLISHED restricted; all-input contractor OPEN | Every-order residual enumeration fails, while affine evaluation remains easy. | Add one connected nonaffine shared constraint and prove that neither Gaussian elimination nor a direct semantic bypass resolves every parent context; charge peak resources. |
| :36 P=RP | OPEN | Not every P language's chosen RP verifier has short positive certificates, so certificate normalization is not necessary. | Attempt a uniform verifier transformation that creates O(log n) positive certificates without already deciding the language; test it on this parity-affine verifier. |
| :48 joint bypass | ESTABLISHED | Two verifier-specific obstructions coexist in a language in P. | Test whether the next proposed invariant survives replacement of R by the deterministic verifier R'(x)=b. |

## Retired in this run

- RETIRED: absence of short positive certificates as evidence for P!=RP.
- RETIRED: every-order residual width plus high certificate width as an algorithm-independent hardness measure.
- RETIRED: adding ANF degree, gate sharing, unique traces, or digest diversity to those two measures as a separation argument.
- RETIRED: transferring the affine ordered-residual lower bound to unrestricted SAT or FLMV without the missing all-input contractor.

## Publication status

Repository publication and exact readback are recorded after upload. No root manuscript, role, or automation was modified.
