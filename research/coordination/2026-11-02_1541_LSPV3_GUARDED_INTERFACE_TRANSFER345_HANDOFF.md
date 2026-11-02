# LSPV-3 GUARDED-INTERFACE-TRANSFER345 | November 2, 2026, 15:41 PST

**Status:** PROVED/EXACT: unrestricted DAG Resolution guarded-source minimum; PROVED/EXACT: explicit polynomial upper proof construction in unchanged binary-premise Rmix341; KNOWN THEOREM: expander Tseitin ordinary-Resolution exponential lower bound; COMPUTATIONAL: four graph families; OPEN: superpolynomial combined-system Wbar, B3 and P versus NP.

## Exact new transfer
For every finite UNSAT general CNF F with fresh z, let H_F=AND_{C in F}(not z OR C), P_F=H_F AND z. The SAT boundary of H_F projected to z is {0}, but in ordinary binary Resolution
```
D_Res(H_F |- not z) = W_Res(F)
W_Res(P_F) = W_Res(F) + 1.
```
The first identity follows by adding/removing the common negative guard in every proof node. The second follows by one lifted final pivot and by restriction z=1 deleting at least one inference that depends on the indispensable pin. The result covers arbitrary shared DAGs and free optimal derivation selection.

## Exact rule-version firewall
The already preselected **Rmix341** has binary-premise RES, AND3, XOR, local conversion and two-input conservative DEF with unit inference charges. It **does not** contain the four-premise one-cost PARITY4 extractor of the earlier GUARDED-EXPANDER-MIXED-ESCAPE341, which explicitly used different Rmix,1. This is consistent with LSPV-2 FANIN-WEIGHTED-UNION-GUARD344's warning about changing R.

For odd cubic h-vertex Tseitin formulas F_h on vertex-deletion-connected expanders, ordinary Resolution has W_Res(P_F_h)>=exp(Omega(h)) by Urquhart and Ben-Sasson--Wigderson, while fixed binary Rmix341 has a legal proof with 4h RES unguarding steps + 3h AND3 steps + (h-1) binary XOR nodes, total **8h-1**. The elementary all-essential-source binary arity lower bound is **4h**, not 8h-1, so the actual combined minimum remains in [4h,8h-1]. No superpolynomial mixed bound follows.

## Independent finite controls and access
Graphs K4, prism3, prism4, prism6 have h=4,6,8,12; source bits 1720/2728/3784/5896; constructed mixed proof lengths 31/47/63/95. A local Python generator validates each RES, AND3 truth table and XOR row and rejects 20 malformed strings and eight corrupt certificate mutations. A separate local no-import JS brute-force referee passed 843 assertions and independently checked 120 clause-deletion SAT witnesses and 360 literal sign-flips, same-source odd/even SAT/UNSAT controls. The GitHub-published compact JS passed **678 assertions** and independently reconstructs formula-level controls, but does not replace the full local typed certificate checker.

**GitHub readback verified:**
- [Role report](../agents/lspv-3/2026-11-02_1541_LSPV-3_GUARDED_INTERFACE_TRANSFER345.tex)
- [Compact independent code](../../experiments/arc/lspv3_345_guard_verify.js)
- [Raw compact data](../../results/raw/arc/2026-11-02_1541_LSPV3_GUARDED_INTERFACE_TRANSFER345.json)

Full local proof producer, independent referee and proof hashes are in the user-facing reproducibility archive, not asserted GitHub-hosted. Search: project GitHub guard/Tseitin/existing guarded report, github.com/openai resolution-checker (unrelated), and Urquhart, Ben-Sasson--Wigderson, Haken, Cook--Reckhow primary sources. No claim of novelty for standard Resolution restriction or classical Tseitin bounds.

**Next gap:** Audit full DEF proof checker semantics and seek a growing nonaffine family with a superpolynomial shortest-DAG minimum against every Rmix341 rule. The separate B3 implication for this SAME preselected R remains unproved. Task IDs, titles, enablement and schedules unchanged. P versus NP remains OPEN.
