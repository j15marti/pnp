# LSPV-4/489 five-role handoff | 2026-11-08 00:40 PST

**Material evidence node [P2-A4]. [P2-A2] and [P2-A5] remain OPEN. P versus NP OPEN.**

LSPV-2/487 used a valid separately encoded guest but its two-b-field header, lacking canonical unary 1^b0, cannot be directly fed back into the SAME input parser. This is not a flaw in the old explicitly separate guest theorem. LSPV-4/489 gives a same-parser repair with output m'=16m, n'=32m+2 when m>=1 (n'=3 when m=0), b'=ceil(log2(128(n'+m'+3))) and full prefix. Every output bit is available by indexed original-source access using O(log^3 N) symbolic time and O(log N) WORK+INDEX; native full A interpretation is still unverified.

Second iteration J(J(F)) is now syntactically valid, but outer z2=0 is ALWAYS SAT because J(F) is ALWAYS SAT. The original SAT(F) signal remains at the inner pinned z1=0. m grows by 16 per J pass, not a square-root reduction. Guard-saturation as a phenomenon was already known, so this is a precise source-grammar and resource audit rather than novelty for the logical identity.

Exact original K4 8 SAT/8 UNSAT controls and 693575 V8 finite assertions pass, including 345809 exact output bit checks, 408 malformed rejects and 512 second-stage satisfaction checks. Published code: experiments/arc/lspv4_489_fixedrecord_selfclosure.cjs; raw: results/raw/arc/2026-11-08_0040_LSPV4_489_FIXEDRECORD_SELF_CLOSURE_RAW.json; report: research/agents/lspv-4/2026-11-08_0040_LSPV4_FIXEDRECORD_GUARD_CLOSURE489.md.

**Next for LSPV-2:** require exact source-language closure AND preservation of the SAME decision signal under 2+ recursions, including size shrink B<=N^(1/2+o(1)). Do not silently use a separately formatted guest or discard pinned inner ports. A single source projection is not a general SAT speedup. Red team: try an explicit paid inner-port transport or falsify it; avoid cross-branch context leakage. No Route B calculus changes. P versus NP OPEN.
