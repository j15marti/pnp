# LSPV-5/410 handoff — exact split-Tseitin RES bypass

**2026-11-07 05:51 PST | Route B | PROVED/EXACT in declared-semantic `R_mix341`; historical serialized acceptance OPEN.**

## Result

For each proper target clause $C=(\ell_1\lor\ell_2\lor\ell_3)$, introduce a private source variable $a_C$ and replace $C$ by

$$
(\ell_1\lor\ell_2\lor a_C)\land(\ell_1\lor\ell_3\lor\neg a_C).
$$

The gadget is strict proper 3-CNF, projects exactly to $C$, and one oriented RES step reconstructs $C$. Applied to every clause of a connected simple bridgeless cubic odd-Tseitin instance with $h$ vertices, it gives $11h/2$ variables and $8h$ source clauses with pairwise-distinct unsigned supports. Nevertheless, the declared mixed calculus has the exact minimum

$$
W_{R_{\mathrm{mix341}},\mathrm{declared}}=4h\;\mathrm{RES}+3h\;\mathrm{AND3}+(h-1)\;\mathrm{GF(2)}=8h-1.
$$

All $8h$ split clauses are independently indispensable, so the binary-source-capacity lower bound matches the construction. Balanced logical span is $3+\lceil\log_2 h\rceil$.

## Tracker impact

New node `[P2-L5-410]`. It is a material adversarial control for `[P2-B13]`, `[P2-B14]`, `[P2-B15]`, and `[P2-B16]`: source-support uniqueness and absence of a direct source-local affine packet do not imply hardness after arbitrary RES. The scoped source-local theorems themselves are not contradicted. `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, and `[P2-B2]` remain OPEN.

## Verification

- Python producer/checker: 752 check groups PASS.
- Independent Node replay: 7,297 checks PASS.
- Raw SHA-256: `5759846fc91f1b26a8691a551203c92d257e3bb79e729e9c521939dc214a09c6`.
- Finite controls: K4, K3,3, cube, Petersen; exact work 31, 47, 63, 79.
- Historical `/341` checker was not available and was not claimed to have run.

## Next action

Authenticate the exact historical premise record and serialized bytes for a derived RES clause consumed by AND3. Acceptance upgrades the construction to a native byte-certificate family; rejection identifies the concrete declared/native grammar mismatch.

P versus NP remains OPEN.
