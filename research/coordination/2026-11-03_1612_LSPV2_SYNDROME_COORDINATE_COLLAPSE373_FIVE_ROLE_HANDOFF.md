# LSPV-2 / 373: Charge-coordinate basis collapse, exact h-to-1 query gap

**November 3, 2026, 16:12 PST | PNP SAT-Circuit Reduction Builder | No task, schedule, role, rule or weight changes. P versus NP OPEN.**

## Published starting theorem and target
Urquhart (JACM 1987, DOI 10.1145/7531.8928) and Ben-Sasson–Wigderson (JACM 2001, DOI 10.1145/375827.375835): on suitable infinite bounded-degree expander graphs with odd Tseitin charges, every ordinary unrestricted shared-DAG Resolution proof requires 2^{Omega(h)} lines. The project cubic CNF has n=3h/2 edge variables, m=4h width-three signed clauses and explicit encoded length N=Theta(h log h). This is NOT Res(oplus), Extended Resolution, Rmix341 or arbitrary SAT computation hardness. Prior exact LSPV-2/341 gives W_Rmix341(F)=4h−1 for connected simple bridgeless cubic odd charges, using charged AND3 and GF(2).

## Exact scoped theorem (PROVED/EXACT, external specialist review pending)
Fix any connected h-vertex graph G, and provide a promised signed-graph charge vector chi in GF(2)^h in addition to the known fixed G. SAT(B_G x=chi) iff XOR_i chi_i = 0. Every correct deterministic exact charge-bit decision tree must read every raw charge bit, D_raw=h. A single all-size invertible linear map sets

$$
y_1=\bigoplus_{i=1}^{h}\chi_i,\qquad y_i=\chi_i\quad(i\ge2).
$$

Its inverse is chi_1=XOR_i y_i and chi_i=y_i for i>=2. In recoded coordinates SAT iff y_1=0, so D_recoded=1. There are 2^(h−1) charge vectors of each SAT/UNSAT label. The graph, decoded signed CNF and its exact models are unchanged. The recoding introduces no contradictory source clause, label oracle, per-instance advice or new Rmix341 inference rule.

**No-go:** an invariant of the decoded problem, invariant under every uniform polynomial-time invertible linear charge-coordinate representation, cannot both lower-bound charge-bit queries in every already-provided representation and grow unboundedly on this family. This is a restricted representation-independence counterexample, not P!=NP.

**Physical firewall:** This does not contradict LSPV-3 SIGNED-INPUT-QUERY377, which proves a 12h sensitive original-occurrence-sign bit-read floor for every total correct all-CNF decider on the fixed explicit encoding. Computing y_1 from original chi reads h bits; extracting chi from original CNF requires authenticated parsing and reading input source signs. No original input-bit observation is avoided. This run compares charge-coordinate probes only after y has already been supplied.

## Costs and controls
The forward/inverse map is an O(h)-bit-time XOR circuit with h−1 XOR operations plus copies. Actual construction and bit output are charged; full materialization requires Theta(h) output bits and live storage, while streaming can use O(log h) scratch. Decoded CNF output requires Theta(N) bits. An explicit 2^h-row truth table is legal but exponentially expensive to print, and a compact shared XOR circuit is polynomial. Unit logical DAG cost W_R=4h−1 is not physical proof acquisition, checking, machine runtime or simultaneous space. Retain s'<=max{rho,eta,lambda,lambda*s} with all local phases charged.

Four falsifiers tested: (1) wrong connected-graph charge parity label, (2) basis-invariant bit-query depth, (3) bypassing original physical source reads, (4) importing exponential Resolution size to arbitrary SAT machine time. The proposed basis-invariance hypothesis fails; (3) and (4) are unsupported transfers. A uniform recognizer can solve this whole family via GF(2) but may require exponential fallback on other CNF inputs; B2 and B3 remain OPEN.

**Finite verification:** full Python producer 32,358 assertions; independent no-import JavaScript verifier 96,234 positive assertions, six corrupted datasets rejected. All 1,360 charge vectors on K4, K3,3, cube and Petersen checked (680 SAT, 680 UNSAT). Original source 3-CNF model enumeration on every charge vector for K4 and K3,3 (80 cases). Eight malformed charge strings and three invalid graphs rejected. Public compact Python tests 28,280 assertions; public compact independent JavaScript tests 28,200. No random seed, no shortest-proof optimization claim.

## Original project, duplication and other-agent assessments
Read first approved November 2 refocus, issue #3, AGENTS.md, CODEX.md, pnp-research skill, fixed calculus report 341, LSPV-2/371–372, LSPV-1 REVERSIBLE-REPRESENTATION-TRAP373 and CERTIFIED-SOURCE-SPLICE374, LSPV-3 SIGNED-INPUT-QUERY377, LSPV-4 TSEITIN-VIRTUAL-HAMMING371 and LSPV-5 SEMANTIC-QUOTIENT-ALGORITHM-MINIMUM-COLLAPSE-REFEREE323. LSPV-1/373 already refutes broad reversible source-retaining proof-cost transport, LSPV-3/377 already proves source-bit observation, and LSPV-5/323 rejects semantic-only proof costs. The scoped increment is an exact h-to-1 charge-only linear invertible encoding gap without inserted clauses, explicitly reconciled with LSPV-3's original-bit theorem.

The actual Grok folder contains GROKPROOF/2026-11-03_2214_PROGRESS.md, blob 59fe73c20473bd6bc20500cf58d75e42519aee88, which leaves universal charged ARC contraction OPEN. The actual Claude folder contains research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex, blob 1f9fc727d3e2b009cba7afec2a93beb62959dd67, a declared alternation-trading rule-system barrier, not B3. Academic and project searches included Urquhart, Ben-Sasson–Wigderson, earlier parity/source-query and linear-basis reports, and github.com/openai implementations; no applicable code transport was adopted. No claim of complete review of all folder contents or external specialist verification.

## Exact role-owned outbox
research/agents/lspv-2/2026-11-03_1612_LSPV-2_SYNDROME_COORDINATE_COLLAPSE373.tex

experiments/arc/lspv2_373_linear_basis_public.py

experiments/arc/lspv2_373_linear_basis_independent_verify.js

results/raw/arc/2026-11-03_1612_LSPV2_SYNDROME_COORDINATE_COLLAPSE373_public.json

research/coordination/2026-11-03_1612_LSPV2_SYNDROME_COORDINATE_COLLAPSE373_FIVE_ROLE_HANDOFF.md

Full local reproducibility archive: LSPV2_SYNDROME_COORDINATE_COLLAPSE373_2026-11-03.zip, SHA-256 821946fed2e676525a7c5c49a6298edd27053ef0c1082cd0ec793b06ff0e22d9. Public GitHub JSON is a ledger and public code is compact; complete source, source data, independent verifier, expanded LaTeX, and checksums are in the local archive.

**Next gap:** a charged source-authenticated bisimulation or polynomial-cost backwards proof transport for every legal Rmix341 rule, including circuit LOCAL-CONVERT internal wires. B1, B2, B3, superpolynomial Wbar_Rmix341, arbitrary all-algorithm SAT lower bounds and P versus NP remain OPEN.
