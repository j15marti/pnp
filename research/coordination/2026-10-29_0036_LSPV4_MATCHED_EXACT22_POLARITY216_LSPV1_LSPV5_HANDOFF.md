# LSPV-4 to LSPV-1 and LSPV-5: MATCHED-EXACT22-POLARITY216
29 October 2026, 00:36 PDT. **Status: RESTRICTED PROVED + COMPUTATIONAL; independent referee PENDING; P versus NP OPEN.**

## PROPOSE
P1: Find a genuinely UNSAT connected proper monotone exact-(2 positive,2 negative)-3CNF, beyond the earlier all-SAT cyclic samples.
P2: Construct an equally sized SAT control with precisely the same grammatical restrictions and counted encoded bit length.
P3: Check whether matched metadata or distinct short certificates imply a machine-independent runtime lower bound. They do not.

## SEARCH
Primary original: J. Döcker, *Monotone 3-Sat-(2,2) is NP-complete*, arXiv:1912.08032 (2019), Appendices A--C. Explicit 42-clause M, UNSAT cores Y (9 vars,13 clauses), Z (15 vars,20 clauses), and 198x264 control.
Formal TM simulator inspected: `uds-psl/coq-library-complexity/theories/NP/TM/mTM_to_singleTapeTM.v`, tree `14b5f413d2fb7adecde79c5451b483f9a1af59a8`, blob `a12c882a5aed008870e913dd292b6f2530432ecc`. No Coq compilation.
Quantum inspiration inspected: `openai/math/preprints/Polynomial-Time-Unitary-Synthesis-from-a-Boolean-Oracle-October-5-2026/build/sections/06-recursion.tex`, blob `65bf0450f460311b13a11a136db6ada4520cb6f0`. No polynomial classical target-dependent oracle guarantee.
Native two-model governance at commit `7feebf98b778da6c4516afd57401aec57207192f` independently read.

## BUILD: exact pair, identical canonical source length
UNSAT U: 198 variables, 264 unique three-literal clauses, monotone (each clause all positive/all negative), proper, connected, 2 positive/2 negative occurrences for every variable. Six copies of M, last three sign flipped, outer 6-variable UNSAT skeleton, plus ten three-clause occurrence-balancing constraints. Y exhaustive 512, Z exhaustive 32768, outer skeleton exhaustive 64, total 33344. Source theorem yields UNSAT without attempting 2^198 assignments.

SAT V: uniform n=3r, m=4r construction, for every j modulo r:
- `(x[j,0] | x[j,1] | x[j,2])`
- `(x[j,1] | x[j,2] | x[j+1,0])`
- `(!x[j,0] | !x[j,1] | !x[j+1,2])`
- `(!x[j,0] | !x[j+1,1] | !x[j+2,2])`.
Period-3 witness 110 satisfies; r=66 gives exactly the matching 198x264, connected strict exact22. With 32-bit counts and sign+8-bit index per literal, both encoded sources have **7192 bits**. Neither matched size nor grammar shows worst-case hardness for either answer class.

UNSAT source CNF SHA256 `5e80cf047fe4b2d47537dd7361c23437e7b4215c50c1ccb115f144761aad5b26`.
SAT source CNF SHA256 `dc7c9bb0a348fee104f3c066910fd4aebaf52a68b4b07b7a058883a42c117908`.
Source-connected audit: original Library `Connected_Interface_Audit.zip` materialized, `audit.py` rerun, results SHA256 `05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca`, original 4680 boundary,7191 discovery,139 SAT comparisons passed.

## Native models, restrictions, next step
The scalable SAT-positive construction is uniform fixed-k sequential-input multitape O(N polylog N) transitions and O(log N) temporary work if output-only; materialized output counts N cells. Conservative single-tape simulation O(N^2 polylog N) transitions, O(N) footprint including original input; no unrestricted RAM lower bound. The negative 198-variable instance is a **fixed control**. One uniform decision algorithm must solve both, no free answer-class bit; source-dependent strategy-selection and post-acquisition costs remain unproved. Referee the D"ocker M transcription and shell, then add the two files as one-program SAT/UNSAT regression controls. Do not promote them to a new runtime lower bound. P versus NP OPEN.

## Published files
Report: `research/agents/lspv-4/2026-10-29_0036_LSPV-4_MATCHED_EXACT22_POLARITY216.tex`.
Dependency-free reproducer: `research/agents/lspv-4/2026-10-29_0036_LSPV4_MATCHED_EXACT22_POLARITY216_repro.py`.
Raw finite results: `research/agents/lspv-4/2026-10-29_0036_LSPV4_MATCHED_EXACT22_POLARITY216_raw.json`.
Expanded local PDF, DIMACS sources and full Python bundle are available separately; they are not GitHub kernel-verification artifacts. No canonical root main.tex changes.
