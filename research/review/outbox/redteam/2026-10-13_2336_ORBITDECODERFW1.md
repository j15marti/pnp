# ORBITDECODERFW1 publication ledger

- Role: UNIVERSAL_CORE_REDTEAM / LSPV-3
- Scientific status: CANDIDATE orbit-obstruction theorem with complete proof, independent review pending; COMPUTATIONAL finite audit; universal untagged source orientation and decoder-ambiguity-as-hardness FALSIFIED/RETIRED; unrestricted lower bound OPEN.
- Report: `research/agents/lspv-3/2026-10-13_2336_LSPV-3_ORBITDECODERFW1.tex`
  - commit `ad4996cb3910b2ef0ee6f59725f3dc5ab0c3f633`
  - blob `e0c47e00fed733e5e01a49f86c0f9fbee1a83299`
- Code: `experiments/review/decoder_orbit_symmetry_firewall.py`
  - commit `bc94aeb86f399b566150f15b5cc1775e28cb956e`
  - blob `e22150754dcdc05c64dda2f493a668132eef5887`
  - SHA-256 `3be2d56eca1079e484caac4761750c7b355ee6d0cda686508997d501473bc106`
- Raw result: `results/raw/review/2026-10-13_2336_decoder_orbit_symmetry_firewall.json`
  - commit `380dea9434b505a4a02957bd744f747ff7721d70`
  - blob `dfcaef8e2bd64bed8c36a9e20a312f598f7eff11`
  - SHA-256 `59ea6b1fe17c7b353cb3a51c1c14f54d26a6c4fa61f52b4dd2e22d4cdeda1790`
- Root reconciliation: commit `96d64137ed5a2b8cb0cfdb546d3a916ce5e88f22`, blob `9a205c3b4f4af0177489ac243561363839f39506`.
- Readback: report, code, and raw result exactly matched the local canonical files; the report header and sentinel verified; root ownership markers balanced, strict status labels present, and OPEN status preserved.

## Exact result

For the quadratic involution `S(a,b,c)=(a,b,c xor ab)`, the graph relation `y=S(x)` is invariant under swapping its source and target blocks. A variable-renaming-covariant target-only decoder cannot recover one originally designated block, because covariance under the block-swap automorphism forces the output block to be invariant. Yet `S^{-1}=S`, so either orientation has an explicit one-AND/one-XOR witness map. Decoder ambiguity is therefore not a lower bound.

## Audit totals

- 1,156 assertions.
- All 64 six-variable assignments and all `6! = 720` variable permutations exhausted.
- Eight models, 56 distinct proper forbidden-assignment clauses, 16 automorphisms, and an eight-element source-block orbit.
- All 512 signed-renaming and clause-shuffle witnesses recovered from charged metadata; the naive positional block was correct only 35 times.
- Equality paths of lengths 2 through 8, YES/NO, Horn, Krom, affine, bounded-path, product, planted, and six malformed-metadata controls checked.

## Scope and handoff

The explicit tagged HIERLIFT decoder and structured PERMEXT Gold lift remain exact. The counterexample rules out a universal source-orientation decoder for arbitrary untagged presentations; it does not establish hardness for any residual. Next work should use a tagged, polynomially recognizable residual whose satisfiable image is guaranteed but whose source-witness extension is not already uniform polynomial time.
