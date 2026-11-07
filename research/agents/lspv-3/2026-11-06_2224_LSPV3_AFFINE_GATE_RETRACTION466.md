# LSPV-3/466 | Affine gate elimination in shared XOR proof DAGs

**2026-11-06 22:24 PST | Route B | PROVED/RESTRICTED mathematical lemma, COMPUTATIONAL finite replay. Historical R_mix341 native-byte acceptance, B3 and P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE, falsifiers fixed before investigation
**Hypothesis.** The exponential leaf cost in LSPV-3/465 and [P2-B9] is a property of the constant-auxiliary-section *Resolution* translation. For an all-affine, authenticated GF(2) proof DAG, topological functional substitution of conservative XOR2 definitions commutes with every binary XOR inference. It should permit nonexpansive proof-to-proof elimination even under reconvergence.

Falsifiers: (F1) some acyclic XOR2 definition retains a nonzero projected row; (F2) a projected paid line fails to follow from exactly its projected two parent rows; (F3) a shared ancestor must be rederived after substitution, so distinct paid XOR nodes increase; (F4) the construction silently treats a branch on an auxiliary z as a branch on one original literal, or treats a source clause as an unlicensed free affine row.

**Search and prior work.** Inspected current `proof1.txt` [P1-03] and `proof2.txt` [P2-D1],[P2-B1],[P2-B2],[P2-B9],[P2-C3],[P2-L3-465], issue #3, governing five-role handoff, LSPV-2/341 original calculus, LSPV-3/436/462/464/465, LSPV-1/465/466, Grok `GROKPROOF/2026-11-06_2316_PROGRESS.md`, Claude `research/agents/claude/world-ledger/README.md`, `AGENTS.md`, `CODEX.md` and pnp-research skill. Source corpus reads: `konard/p-vs-np/scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` and `REVIEW_ADDENDUM.md` blob `6a7cc2f8962d3fcfc1778b1d3d8f5dc8d56d70`; `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`. GitHub/OpenAI code search returned an ETH preprint, not a native proof checker; no evidence from it was imported. Public web search (not a Google-specific interface) located Urquhart 1987, Emdin et al. MFCS 2022 and the FRAT-XOR CAV24 format. Existing ideas are cited as prior work, no novelty priority claim.

## Theorem 466.1: source-preserving affine retraction (PROVED/RESTRICTED)
Fix original Boolean variables X and acyclic globally fresh gates `z_j = u_j XOR v_j XOR c_j`, where both inputs of gate j are originals or previously defined outputs. Consider a source-authenticated GF(2) proof DAG whose free source rows are *already legally established affine consequences of original F(X)*, whose additional axiom rows are exactly the paid gate definitions, and whose only derived steps are binary row additions. There are NO other derived rules and NO auxiliary-variable case-assumptions. Each source-row conversion has its own explicit proof/provenance cost, unchanged by this theorem.

Recursively write each gate as a linear/affine function `z_j = s_j(X) XOR d_j`. Define the substitution `pi` on affine rows by replacing each auxiliary with that function and collecting coefficients over GF(2). Then (i) every original source row is fixed; (ii) every gate-definition row maps to `0=0`; (iii) `pi(A XOR B)=pi(A) XOR pi(B)`. Process the input DAG in topological order, memoizing one image per node. Delete `0=0` images, redirect additions with a deleted neutral parent, and retain one paid binary XOR node when both parent images are nonzero. Therefore an augmented refutation ending at `0=1` maps to an **original-source-only GF(2) refutation**, with

$$
q_{\mathrm{XOR}}^{\mathrm{projected}}\le q_{\mathrm{XOR}}^{\mathrm{augmented}}.
$$

The construction preserves DAG reconvergence (not just proof trees) and never pays a shared inference twice. With n active original variables, g affine two-input gates and q proof nodes, dense bitvector implementation takes O((q+g)gn) bit operations as a conservative upper bound and O((q+g)n+q log(q+1)) output bits, plus source IDs and parsing, caching, verification and peak storage. These are physical *upper* bounds, separate from unit logical weights. This is an elementary linear-substitution lemma and is not asserted to be new.

**Important typing.** The claim assumes already authenticated original affine rows and paid affine DEF rows. It does NOT claim the historical accepted-byte R_mix341 parser exposes those gate equations or that its LOCAL-CONVERT and clause-facet interface is settled. In particular it is NOT a complete simulation of RES/AND3/LOCAL-CONVERT/AND-gate steps and not a normalization of arbitrary mixed branch DAGs. `P2-C3` and `P2-D1` remain OPEN.

## Exact branch-boundary obstruction
For `z=x_1 XOR x_2`, the auxiliary branch assumption `z=0` retracts to `x_1 XOR x_2=0`, which is **not** a single original-variable literal: its models are 00 and 11, unlike any literal's two models. A purported literal-preserving branch normalizer must add a legal affine-context handling rule or expand justified cases; it cannot silently relabel this branch. This finite four-row obstruction is exact, but does not prove exponential general mixed transfer cost.

## Established 3-CNF family, legal shortcuts and controls
Use the standard odd-charge Tseitin encoding on a connected cubic graph G: n=3h/2 edge variables and m=4h proper width-three original clauses, four clauses per vertex excluding the four forbidden local assignments for its incident-edge XOR equation. Odd total charge makes it UNSAT by XOR summation. Urquhart 1987 proves exponential ordinary Resolution lower bounds on suitable expander-graph Tseitin families, not on every finite graph and not in the stronger mixed calculus. Existing known shortcut: four source clauses per vertex combine to one parity row via three paid AND3 in the *declared semantic* R_mix341 calculus, then h-1 binary XOR additions reach false. The declared optimum is 4h-1 for bridgeless simple cubic graphs (LSPV-2/341); independently verify the old scope before reusing it. Conservative linear DEF may generate more derivations but cannot be excluded.

Finite published-construction controls: K4 (h=4), K3,3 (h=6), cube (h=8), each odd-charge UNSAT and even-charge SAT. Two genuinely nested shared gates `z1=x1 XOR x2`, `z2=z1 XOR x3` were used twice each in a reconvergent augmented row DAG; retraction removes their zero images. Independently reconstructed original DIMACS sources, each 4-clause parity conversion and its exact source identifiers, every XOR line, every projected parent, full SAT/UNSAT counts and original-source hash. Node counts:

| graph | clauses | odd augmented XOR / projected XOR | odd conditional charged work AND3+DEF+XOR | even SAT models |
|---|---:|---:|---:|---:|
| K4 | 16 | 7 / 3 | 21 / 15 | 8 |
| K3,3 | 24 | 9 / 5 | 29 / 23 | 16 |
| Cube | 32 | 11 / 7 | 37 / 31 | 32 |

The conditional work columns assume two paid gate definitions with affine row exports; this is not a claim of authoritative byte acceptance. Even-charge fixtures reduce to `0=0`, **not** an UNSAT certificate. A Node.js producer rejected 24 corrupted controls; independent Python replay reconstructed six original sources, checked all 2^n assignments (up to 4096), every clause row, every proof parent, checked 30 further independent corruptions, and rejected the auxiliary-branch literal substitution. Source/checker evidence in reproducibility archive; compact result ledger `results/raw/arc/2026-11-06_2224_LSPV3_466_AFFINE_PROJECTION_SUMMARY.json`.

## Resource, provenance and publication constraints
Distinct logical work: above. Complete raw JSON: 94,255 bytes; original DIMACS sources 163/239/340 bytes per corresponding graph. Reconstructed proof evidence is explicit and retains original clause IDs, not a SAT oracle. Production included source construction, 8-row local checks, affine transformation, output and corruption testing; independent verification included full exhaustive SAT/UNSAT checking and projected proof replay. Memory/runtimes measured only in the finite host environment, not FLMV. All native bit parsing, source reads, head updates, cache storage, references, recomputation and all-phase simultaneous peak must be charged in a machine-time claim. Neither proof minimum nor span is equated with execution time.

## Status and remaining gap
**Material restricted evidence under [P2-C3], new [P2-L3-466]; all load-bearing [P2-B1], [P2-B2], [P2-D1] OPEN.** Affine functional projection repairs one GF(2)-only subproblem left by LSPV-3/465, but native authenticated definition export, nonlinear gates, resolution, LOCAL-CONVERT, case-context retraction and B3 remain unproved. No branch/discharge/weakening rule was introduced. No task, schedule, role, historical weight or root manuscript changed. P versus NP OPEN.

Primary references: Urquhart, *Hard examples for resolution*, JACM 34(1), 1987, DOI 10.1145/7531.8928; Emdin, Kulikov, Mihajlin & Slezkin, *CNF Encodings of Parity*, MFCS 2022, DOI 10.4230/LIPIcs.MFCS.2022.47; `meelgroup/frat-xor/format.md` (distinct XLRUP format; not historical native R).
