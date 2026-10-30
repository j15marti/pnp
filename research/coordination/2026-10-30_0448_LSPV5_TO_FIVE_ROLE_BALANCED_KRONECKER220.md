# LSPV-5 additive handoff — BALANCED-KRONECKER-REFEREE220

Timestamp: 2026-10-30 04:48 America/Los_Angeles  
Audience: LSPV-1/2/3/4/5 and issue #3  
Status: P versus NP remains **OPEN**.

## Exact referee result

**PROVED/EXACT, restricted.** For a proper sign-balanced ternary source with `m=2h`, every coherent complete-assignment profile satisfies

`N1 = h − 2N0 + N3`, `N2 = h + N0 − 2N3`.

The algebraically permitted `(N0,N3)` pairs number exactly

`floor(h^2/2 + h + 1) = floor(m^2/8 + m/2 + 1)`.

For `m=20`, 61 profiles are permitted; W1 realizes 24 and SWAP6 realizes 30. Permitted is not the same as source-realizable.

## Representation correction

**PROVED/EXACT.** Put `M=h+1`. The scalar exponent `k=N0+M*N3` injectively encodes the entire four-category profile and decodes by radix division. For Laurent differences `(u,v) in [-h,h]^2`, `u+(2h+1)v` is injective. This is bounded Kronecker substitution.

**FALSIFIED/RETIRED.** “Only a two-variable Laurent representation can return the complete histogram.” LSPV-2’s two-generator quotient remains correct and natural, and its observed rank-two witness proves two-dimensional lattice span. It does not prohibit a source-size-dependent one-exponent encoding on a bounded support.

**PROVED/EXACT firewall.** Collision-free packing preserves the number of nonzero coefficients. Direct sparse products still generate the same candidate term pairs when the radix is collision-free for the complete intermediate range. Key representation changes; sparse state count does not. The packed exponent reaches `Theta(m^2)`, so its bit length is asymptotically the same as the combined two-coordinate key.

## Required clause-extreme experiment

The independent checker passed **387,160** claims over nine SAT/UNSAT and hostile controls:

- every original clause/occurrence `S_j`, `U_j`, and both inversions;
- all 5,304 indexed `SS/SU/US/UU` modes by fresh enumeration;
- coherent `0^n`, `1^n`, complement identities and multi-flip trails;
- 379,024 forbidden-resolvent-cube completions;
- 83 balanced identities/decodings and six exact profile-count checks;
- complete model counts and same-answer controller checks.

Complete raw JSON: ChatGPT Library `libfile_19a506929ec0819183ef4cee0f199b67`, SHA-256 `38ae6a5b6b991e29ebe5ed0c34853e36da4f4c6983d7cb3daf527f99e0271894`.

The uniform full-profile prepass followed by the same UP–DPLL did not prune the backend. W1 used 1,975,190 selected events versus 9,110 baseline; SWAP6 used 1,970,693 versus 4,613. This is a representation/firewall result, not an all-algorithm SAT lower bound.

## Next exact target

Test conditioned selected-prefix connected-log updates under a simultaneous bit-cost ledger. Require positive fully charged total-work improvement on one unbounded connected strict22 SAT-and-UNSAT family while permitting Kronecker packing, source retention, Gaussian/Horn/2SAT switches, failed prefixes and explicit reconstruction.

