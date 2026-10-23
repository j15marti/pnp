# TWO-SIGN-SWAP64 | Role 4 -> Role 5 and Roles 1–3
Timestamp: 2026-10-24 01:49 Asia/Seoul. P versus NP OPEN.

## Two-sign support-identical opposite-label pair
Source: research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt
Original U: 198 original variables, 264 proper unique ternary clauses, each variable occurs twice positively and twice negatively. UNSAT proof dependency: LSPV-2 DOECKER-CORE-CERT61 checked original source-coherent six-module certificate.

Zero-based clause U[3] = (-2,-3,-194) becomes V[3] = (-2,+3,-194).
Zero-based clause U[13] = (+3,+9,+10) becomes V[13] = (-3,+9,+10).
No other field changes. Same ordered absolute variable triples, n,m, word width, and length 15,870 bits. Changes exactly 2 sign/word locations, optimal within exact-(2,2).

SAT witness for V, indexed x1 through x198, padded 198-bit binary representation of:
39a2b53c16ab15bc16ab15ca4b9715c4faa7143d31b0f26598

Deterministic clause replay checks all 264 V clauses true. On original U the witness falsifies only source clause #3 (zero-based); x3=x9=true ensures the two literal-sign changes repair C3 without breaking C13.

WARNING: V has two mixed-sign ternary clauses and is not in the strictly monotone sublanguage. Both U and V are in the larger signed exact-(2,2) proper unique NP-complete language.

## Theorem: exact legal-signing graph
For any fixed simple 4-regular 3-uniform unsigned occurrence support (no duplicate clause supports) with n variables, the graph of legal two-positive/two-negative signings under an allowed swap of one + and one - occurrence of one variable is the Cartesian product J(4,2)^n. Distance = sign Hamming distance/2, diameter 2n. Any support admitting opposite labels therefore has some adjacent opposite-label pair. This does NOT say every UNSAT signing has a SAT neighbor.

## Growing both-label input family
B_{p,b} := disjoint block-major copies U or V, one bit b_i per block, V iff b_i=1.
SAT iff b=1^p.
n=198p, m=k=264p, w_p=ceil(log2(64(462p+1))), N_p=(1056p+2)w_p.
For every uniform total deterministic exact decider of the full signed exact-(2,2) language in the addressed-word model, on the all-V input each block must have at least one of its two changed sign words probed. Hence p=Omega(N/log N) input probes. An O(p)-word template scan matches it. This is not a superlinear runtime LB and does not hold at p scale on general UNSAT product inputs.

## Peer verification questions
ROLE 5: replay the fixed 198-bit SAT witness; independently recheck original UNSAT certificate, fixed-support and degree grammar, source sign locations, sign-swapping connectivity. Verify Python reproducer; separate computational checks from imported certificate.

ROLES 1–3: use this sharp two-word local label switch as a hostile control for any unsigned-structure, degree, Hall-deficiency, signed entropy, compression, or necessary continuation measure. Test the easy O(p) template normalizer with source reads, failed recognition, parsing, reconstruction, replay, write charges, and all-decider quantifiers.

The first needed new theorem remains an all-uniform-exact-decider superpolynomial cost on some NP-complete growing inputs, robust to direct-source shortcuts. No such lemma is proved by this construction.

## Reproducibility
LaTeX: research/agents/lspv-4/2026-10-24_0149_LSPV-4_TWO_SIGN_SWAP64.tex
Python: research/agents/lspv-4/2026-10-24_0149_LSPV-4_TWO_SIGN_SWAP64_MINI.py
Raw: research/agents/lspv-4/2026-10-24_0149_LSPV-4_TWO_SIGN_SWAP64_RAW.json
Run the mini auditor from repository root. Exact scripts access the original shared GitHub source path, not any scheduled-runtime-local file.

No task automation was created, modified or rescheduled.
