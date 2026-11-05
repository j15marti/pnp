# LSPV-4/415 | Sparse-ID False Refutation Under Lossy Parsing
**November 5, 2026, 07:36 PST. PROVED/RESTRICTED parser-level soundness counterexample, COMPUTATIONAL controls; historical native R_mix341, B1/B2/B3, and P versus NP OPEN.**

## IDEA before SEARCH
Falsifiable hypothesis: exact raw-source byte authentication cannot preserve Resolution soundness if the parser quotients distinct original variable IDs via floating-point rounding. Test with a true-SAT source, an exactly hashed but false one-step Resolution certificate, exact BigInt control, legitimate UNSAT control, malformed inputs, and hash mutations. This attacks an *implementation semantics*, not the mathematical fixed R.

## SEARCH
Read first Nov. 2 governing handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`; then issue #3 (through LSPV-2/418), exact /341 original blob `c87acd11`, Nov. 4 grammar addendum, CANON2/CANON2R, peer LSPV-1/418, LSPV-2/418, LSPV-3/423, LSPV-4/414, LSPV-5 REFEREE363, AGENTS/CODEX/skill, actual GROKPROOF/2026-11-05_1218_PROGRESS.md blob `d3183283`, Claude TPORT-0002 and ONETAPE-0001. Haken PHP DAG Resolution 1985, Cook ER PHP, Cook-Reckhow 1979, Braun Res(XOR) arXiv:2609.23015, Gocht-Nordstrom AAAI 2021, Pich-Santhanam ECCC TR23-199, MDN MAX_SAFE_INTEGER reviewed. General web queries included `Cook Reckhow relative efficiency`, `Haken intractability resolution`, `Braun bit pigeonhole Res xor`, `JavaScript Number MAX_SAFE_INTEGER`; direct branded Google unavailable. Authenticated GitHub searched `Rmix341 LOCAL-CONVERT`, `REFEREE361`, `CANON2R`, `GROKPROOF`, `Claude`; also `openai/math ExecCNFNodeSearchCosts`, and read complete 7,306-character `lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` blob `1ced21f4`. This implementation is NOT a SAT-decider-to-mixed-proof compiler.

**Prior-work delta:** REFEREE363 had already documented 2^53 numeric aliasing. This run gives an explicit *SAT* original with an exactly authenticated *false RES* proof, an independently checked opposite-label original, and exact parser safety theorem.

## ITERATE, proved lemma
Let h be a noninjective parser mapping two **legal** distinct positive original variable identifiers a!=b to h(a)=h(b). The two unit clauses F=(x_a) AND (NOT x_b) are satisfiable (x_a=1,x_b=0) but after lossy parsing appear complementary. A verifier using h for RES pivot equality can accept a one-node empty-clause derivation even with an exact-byte authenticated original source. Thus **byte-authentication and typed semantic parsing are separately indispensable**.

Actual legal sparse DIMACS under unbounded integer-token semantics, 97 ASCII bytes:
```dimacs
c legitimate sparse 16-digit IDs
p cnf 9007199254740993 2
9007199254740992 0
-9007199254740993 0
```
At IEEE-754 binary64 precision Number(9007199254740992) equals Number(9007199254740993). The intentionally unsafe checker accepts the fake RES pivot 9007199254740992 despite the source byte hash SHA-256 `65e2540699c8755cc29f9cad8c02c4aff5f7717ceb04ca79d6a2884a98f56ac1` being exact. The BigInt checker rejects. Changing the second unit to `-9007199254740992` creates a genuine UNSAT original and both parsers correctly accept the legal RES step; source hash changes to `6c7bd3e06b7438650478244f77cc9d4dbd5cca77bfca6e41f95955b6dd8b0030`.

**Status scope:** This is **NOT** a legal false inference under fixed semantic R_mix341. A strict parser with only <=32-bit/<=2^53-1 IDs also avoids the example. Source hash equality is necessary but not sufficient for correct interpretation. Use canonical decimal byte-string comparisons or arbitrary-precision integer arithmetic for every source, DEF, LOCAL, AND3, GF(2), and reference identifier.

## Tests, costs, and B3 firewall
Full reproducibility producer (Node.js) passed **118 assertions**, with 97 byte-change hash rejections. Independent Python referee passed **656**, checking 128 SAT and 128 UNSAT large-ID pairs, six malformed sources, and digest verification. Seed 0, no external dependencies. The GitHub compact verifier carries the central test; full source and raw fixtures are in the local reproducibility archive.

Let N be raw input bytes, E supplied proof bytes, q=1. Exact source acquisition and header parsing take O(N) byte work, and raw authenticity forces Ω(N) byte inspections under adversarial perturbations (LSPV-4/414). Digit-string exact identity compares in O(N) time, O(log(N+E)) indexed-read-only scratch by rescans; buffered implementation uses O(N+E) writable space. Materializing E bytes requires S_peak>=E during some phase, even if later released. Count indexing, head motion, comparisons, certificate output, failed checks, caches, guest and simultaneous retained state separately. Neither q=1 nor a cryptographic hash converts logical cost into physical T/S.

Haken's exponential result is for *ordinary DAG Resolution* on explicit unary PHP, not mixed R or arbitrary SAT machines. Cook's ER PHP shortcut and GF(2) Tseitin are countercontrols. Braun's September 2026 exponential DAG-like Res(XOR) result applies to bit PHP with n=2^ell, ell>=32, not full mixed R. **B3 is still OPEN**: SAT in P does not itself supply an original-source R_mix341 proof or formalized decider correctness. Full historical LOCAL/exported-wire/paid-DEF grammar is also OPEN.

**Next:** demand byte-injective integer tokens in proposed CANON2R; independently close historical typed clause-to-LOCAL, affine-to-AND3, DEF/public-wire consumer induction. Preserve original weights, tasks, schedules and OPEN status.
