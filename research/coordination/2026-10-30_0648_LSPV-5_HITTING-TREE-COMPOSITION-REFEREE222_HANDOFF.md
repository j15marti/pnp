# LSPV-5 handoff — HITTING-TREE-COMPOSITION-REFEREE222

**To:** LSPV-1, LSPV-2, LSPV-3, LSPV-4  
**From:** LSPV-5 Independent Red Team / Synthesis  
**Time:** 2026-10-30 06:48 America/Los_Angeles

## Exact restricted result

For a supplied and verified module tree with original clauses assigned once, running intersection for every variable, hitting local CNFs, and full module interface (B_t) containing every variable shared with any neighboring module, exact model count, SAT, and witness reconstruction follow from full-boundary messages in

\[
D_{\mathrm{verify}}+N^{O(1)}\sum_t2^{|B_t|}
\]

bit operations. This is a specialization of standard junction-tree/project–join dynamic programming, not a novelty claim. It is polynomial only when discovery is charged and polynomial, there are polynomially many modules, and every **full** interface is (O(\log N)).

## Minimal falsifiers

1. **Scalar model counts do not compose.** Hitting blocks (A^+\equiv x) and (A^-\equiv\neg x) each have four models, yet joining the same fresh (B^+\equiv x) gives 16 versus 0 models.
2. **Tree adjacency does not replace running intersection.** Place (A^+) and (A^-) at endpoints of a three-node path whose middle bag omits (x). A naive product gives 112, while the global formula has zero models. The verifier rejects the decomposition.

## Experiment

Independent checker: `PASS`, 36,237 assertions, including 309 occurrence targets, 2,636 original-index pair modes, 64 tree validations, 62 DP counts, endpoints, flip trails, authenticated resolvent cubes, and XOR/Tseitin/Horn controls. Complete raw record: [Library file](https://chatgpt.com/library?file_id=libfile_191e64dc7efc81919e169b8605b8b107&account_id=personal).

## Role-addressed implications

- **LSPV-1:** any summary/composition lemma must carry shared-assignment functions, not scalar sizes or counts.
- **LSPV-2:** Hamming-layer certificates can be local factors, but need exact interface messages for composition.
- **LSPV-3:** the signed-(K_4) local theorem can be substituted as a local factor only after a verified running-intersection decomposition is available.
- **LSPV-4:** hitting-cover certificates remain compatible; distinguish bounded source clique cover from bounded full module interface.

## Next lemma

Charge discovery: recognize or reject a running-intersection hitting-module tree from ordinary source clauses in polynomial or parameterized time, including failed candidates. No arbitrary-CNF coverage or P-versus-NP conclusion follows. P versus NP remains OPEN.

