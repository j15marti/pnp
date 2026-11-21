# PNP Independent Counterexamples: T5-COUNT-PARITY-AUDIT1

Pacific timestamp: 2026-11-21 09:14 PST. Role: charged-redteam.

## Target and disposition

Independent reconstruction of Bounds' T5-COUNT-PARITY-RESTRICTION1 at commit **81c887aac5366bab0bec755617b21fe03ce6ee4b**, report [1], code and raw evidence [2]. The selected bridge is from literal restrictions of the actual strict-C encoded count map to unrestricted bounded-fanin circuit demand. This is the newest count-map bridge recovered from issue #324, not a witness-representation surrogate.

**PROVED/EXACT, independently reconstructed within the stated scope:** the source-bit restriction, exact multiplicities, parity output coordinate, and k-1 gate/ceil(log2 k) depth lower bounds survive. No legal counterexample to the published lemma was found. This audit does not certify the entire baseline or an unrestricted separation. Its new independent checks and scope control have not themselves had a further external review.

**FALSIFIED/RETIRED only as an unclaimed extension:** arbitrary semantic variable renaming need not preserve the one-free-source-bit-per-switch property. A two-block example below changes that distance to two. The original construction intentionally fixes identifiers and does not make that stronger claim.

**COMPUTATIONAL:** independent local overlap enumeration, direct two-block counts, header/identifier-boundary checks, and exhaustive small shared-circuit semantics pass. Finite evidence does not prove the asymptotic statement.

Next dependency: **T5-COUNT-OVERLAP-DEMAND1**, Bounds owner, Synthesis tracking. Prove a demand beyond input support for a shared-variable encoded count map that exceeds the chosen cap's N^a log N ceiling. Repeating product/parity constructions or refining a constant does not meet it.

## Quantifiers, model and falsifiers

For every integer k>=2 set n=8k, m=2k, w=ceil(log2(8k+1)) and
N_k=8k+2+2 floor(log2(2k+1))+6kw.
For every fan-in-at-most-two AND/OR/NOT circuit computing the exact count on ALL valid length-N_k encodings, with constants, arbitrary sharing/fanout, arbitrary depth, and 3N_k zero-padded binary output bits, its gate count is at least k-1 and depth at least ceil(log2 k). Invalid inputs are don't-cares, but every restricted input below is valid. No uniform circuit-discovery hypothesis is imposed by gate count.

For cap comparison separately fix ONE deterministic correct halting sole-tape counter A, K>0 and a>=1, all independent of input; suppose T_A(N)<=KN^a. The tape, alphabet and control are fixed; input, output, head positions, stored addresses and all continuation-relevant state are charged. A different solver, input representation, CM definition or execution cannot supply a missing factor.

Four falsifiers used:
1. The switch changes more than one source coordinate, changes the header, or makes an identifier/clause invalid.
2. Direct local counts disagree with 93750 and 31250, including declared unused variables.
3. Carries or 2-adic factors break bit k+1 = parity(b) XOR (k mod 2).
4. A shared bounded-fanin circuit has one output essentially depending on k inputs with fewer than k-1 gates.

C consists of permutations of 012,123,234,340,401 on Z_5. Clauses have distinct variable names; duplicate clauses and declared unused variables are allowed. No constants/domain restrictions are primitive. R has 40 tuples and is different; neither R nor historical S/Q is substituted here. Our independent predicate tests directed tournament cycles with i beating i+1 and i+3, which yields exactly C.

The original encoding is 1^n0 gamma(m+1) followed by m triples of one-based w-bit names. Thus N=n+2+2 floor(log2(m+1))+3mw. Padding the output to 3N bits changes neither its least-significant coordinates nor the exact integer. This is a counting claim; all constructed inputs are SAT.

## Reconstruction from source bits to a circuit cone

In block j=0,...,k-1 write C(8j+1,8j+2,8j+3) and C(8j+1,8j+2,8j+3+4b_j), interpreting numbers as variable names. Since 8j+3 has low three bits 011, adding four changes only bit 2 to give 111, with no carry. Headers, other names and all other bits stay fixed. Each switch occurs once at its own source position. All IDs are <=8k and each clause is strict. Hence the entire Boolean cube is inside the valid domain, even though circuit behavior outside that domain is arbitrary.

Fix an ordered color pair (u,v). There are ten pairs with two allowable third colors and ten with one, while equal colors have none. With a duplicate clause the used-variable count is 30 and five declared variables are unused: 30*5^5=93750. With distinct private third names the used-variable count is 10*2^2+10*1^2=50 and four names are unused: 50*5^4=31250. This derivation uses identity of names, not syntactic clause multiplicity as independent constraints.

For r=sum b_j, disjoint scopes give
Z=31250^k 3^(k-r)=2^k 15625^k 3^(k-r).
The second factor is odd and 15625=1 mod 4. Thus the count modulo 2^(k+2), shifted by k, is 1 if k-r is even and 3 if it is odd. Lower bits vanish, bit k is one, and bit k+1 is the claimed parity. Higher carries cannot affect this modular identity. Flipping any b_j changes that output bit.

Restrict the original circuit and retain the ancestor cone of that output. Let g count noninput gates and l count source vertices, including constants. Connectivity gives at least g+l-1 distinct undirected edges; bounded gate indegree gives at most 2g. Essential support gives l>=k. Therefore g>=k-1, even with repeated inputs and shared subcircuits. Distinct-edge count only becomes smaller when operands repeat, so it cannot defeat the inequality. A depth-d cone reaches at most 2^d sources, giving the depth bound. No theorem about restricted witness circuits is imported.

N_k=Theta(k log(k+2)), so C_Nk=Omega(N_k/log N_k) along this sequence. No interpolation to every exact length is claimed. This lower bound lies below O(N^a log N) for every fixed a>=1. The baseline simulation transfer therefore excludes no exponent. The gap is quantitative as well as conceptual: essential support by itself is bounded by the number N of source bits.

## Small legal scope control and narrowest supported statement

Use k=2, n=16,m=4,N=82, and b=(0,0) versus (1,0). Apply the fixed variable-name permutation exchanging 3 and 4 to both inputs. The varying name is now 4 versus 7, whose binary forms 00100 and 00111 differ in TWO coordinates. Every clause remains strict, lengths match and counts are unchanged by the bijection. The test records the exact changed source positions.

This falsifies only “the same literal restriction works after every semantic renaming.” It does not refute existence of the original restriction. In the renamed pair one can still describe a diagonal identification of two source bits, but that is not literally leaving one coordinate free and fixing all others. This distinction matters when transferring the restriction through a preprocessing or canonicalization map.

Smallest safe statement: use the explicitly numbered raw encoding, duplicates and unused variables as declared, and the fixed least-significant output coordinate. The existential restricted cube and gate-cone consequence need no correction. Do not silently assert that they survive every equivalent encoding at no cost. This is a clarification to Bounds/Synthesis, not a request to retract the published lemma.

## Independent evidence and controls

New runner: experiments/t5_redteam_parity_audit1_20261121.py.
Raw: results/raw/t5_redteam_parity_audit1_20261121.json.
Run in a temporary directory with Python 3 and assertions enabled; the script writes raw.json there. No peer module is imported.

The independent counter enumerates assignments only to names actually used and multiplies by 5 per unused name. It directly checks all 55 unordered pairs with repetition among the ten strict triples on five names, not only the proposer’s overlap pattern. Counts by overlap 1,2,3 are 180,250,750. Four k=2 counts are obtained by assignment enumeration over all used variables, with unused factors, independently of the product formula. This catches shared-variable/product mistakes.

The parser decodes actual unary/gamma/fixed-width bits. Thirteen k values through 128 straddle identifier/header growth boundaries; 510 Hamming-weight representatives check exact encoding and low count bits, and every single-switch coordinate is independently located. Larger counts in this portion use the proved product identity, not full assignments. No random seed or heuristic sampling is used.

All three-input straight-line AND/OR/NOT semantic sequences through two gates are enumerated with constants, repeated operands, sharing and unused gates: 1,14,226 distinct semantic sequences at budgets 0,1,2. Their maximum supports are 1,2,3. This finite test supplements the general connectivity proof; it is not a circuit lower bound inferred from enumeration. Original peer raw evidence was also parsed: all 2046 rows match its exact product formula. That consistency check is not independent counting.

Affine/Tseitin and private-leaf-tree controls: cheap scalar algorithms remain legal; the audited claim is not about their witness representation size. Our arbitrary-overlap enumeration tests the relevant local count mechanism beyond the selected product family. No expensive duplicate affine/tree experiment was rerun.
Complement: complementing parity preserves essential support; no DNNF complement transfer is used.
Sharing: covered in both cone proof and circuit enumerator.
Renaming: the explicit counterexample distinguishes semantic invariance from source-bit geometry.
Relocation: no old-cut traffic claim; moving input does not force a new circuit lower demand.
Forced domains: not silently added; adding constraints changes the count function. Easy forced counts cannot amplify this support argument.
Decision-witness: every product instance is SAT. Positivity on this cube is constant, so the parity lower bound cannot be recycled as a decision lower bound.
Full-state entropy: H(Z|C_t)=0 for a correct deterministic full state remains compatible; entropy is not our progress measure.

## Complete same-execution ledger

| Item | Charge or limitation |
|---|---|
| Source parsing/authentication | Scan actual unary/gamma headers, all names, clauses and trailing length. Exact comparisons, not hash equality. A conservative sole-tape family recognizer uses O(N^2) time. |
| Discovery/failures/switching | All actual attempts, rejected recognizers and representation changes stay in t_A. No compulsory recognition of this family is assumed. |
| Restriction construction | O(N) emitted bits; counters/IDs O(log N); conservative sole-tape O(N^2). In the circuit proof fixing bits does not require an executing reduction circuit. |
| Algebra and caches | A legal fixed shortcut multiplies k fixed-size factors; O(k^2) elementary bit arithmetic and O(k) arithmetic storage suffice. A conservative whole sole-tape envelope is O(N^3) time, O(N) simultaneous storage. Faster algorithms allowed. |
| Queries/accesses/addresses | No oracle or residual queries. Actual reads, head movement, address bits, cache lookup and buffer transport charged. Circuit wire existence is not a RAM runtime assertion. |
| Sharing/recomputation | Shared gates/cells count once. Discarded data must be reread or recomputed. No uncached recursion tree charged to a cached solver. |
| Output | Exact O(k)-bit count here, O(N) padded output; emission and retained output charged. Recognition failure is UNKNOWN for a paid complete fallback, never UNSAT. |
| General fixed cap | Same A,N: S=O(N^a), physical CM=O(N^(2a)), description CM=O(N^(a+1)), count gates O(N^a log N). No demands multiplied across different runs. |
| Shortcut CM | Its own conservative time/space give physical CM O(N^4), an upper envelope only. Minimum-description CM is not physical storage. |
| Nonuniformity | Circuit size does not charge discovering the circuit. A uniform compiler/evaluator would pay description, wire addresses and evaluation. |

DISJ: PASS as a scope check, no communication theorem imported. Relativization: NOT APPLICABLE to separation; oracle gates are outside this basis. Simultaneous DTISP: PASS for ledger compatibility, OPEN for any cap-defeating demand. Deterministic configurations: PASS for consistency, not used as a lower-demand shortcut. Natural Proofs/algebrization: no barrier evasion or superpolynomial theorem asserted.

## Fresh literature and official-repository search log

Search date 2026-11-21 PST. Queries: “Boolean circuit parity AND OR NOT fanin two gate elimination lower bound Schnorr”; “site:github.com/anthropics SAT counting formal verification”; “site:github.com/openai circuit theorem proving counting”; “site:github.com/xai-org SAT counting verification”; “site:github.com/google-research SAT circuit complexity counting”; “site:github.com/google-deepmind theorem proving SAT”.

Primary paper inspected: Carmosino, Dang, Jackman, *Simple Circuit Extensions for XOR in PTIME*, STACS 2026, article 23, publisher HTML [3], definitions and circuit-model discussion, including its use of the classical 3(n-1) parity bound. Full proofs are explicitly deferred there to its full version. We do not import the stronger bound: the self-contained k-1 cone proof suffices for this audit and a constant-factor improvement would not close the cap gap. ETH/MCSP hardness statements in that paper concern different functions and assumptions, not the encoded T5 count map.

Official owner checks: GitHub organization pages for anthropics and openai display verified corporate domains; xai-org links x.ai; google-research links research.google. google-deepmind's organization page was read, but a search for deepmind.google there returned no match, so affiliation verification through that particular signal is incomplete. No theorem is accepted merely from organization name.

Pinned repository reads:
- anthropics/formal-math, 16a5ce41304fcdaea4e0be7c132e1c361dc26da5, eth/README.md: counting/formalization lead. README claims subexponential SAT/counting and explicitly distinguishes statement accuracy from kernel checking. Neither proof nor build audited here; UNVERIFIED external theorem, not imported.
- openai/math, 4eaee87548250b2682affda7d05d947c05554bae, README.md: research-artifact catalogue with varying verification status. Search found a quantitative circuit source lead, but no target-specific T5 restriction theorem was checked. No theorem imported.
- google-research/circuit_training, c417a3a13f40867b649c719c03daaf1b39a909bc, README introduction: AlphaChip floorplanning, not Boolean gate-count lower bounds. Rejected for this dependency.
- google-deepmind/formal-conjectures, d8d031d4998c78575159ccab9a7a9e95ce043883, README: formalized conjecture statements, not a proof of this target lemma. No kernel build; no imported theorem.
- xai-org: bounded search and organization page exposed model/API tools, no applicable parity/counting lower-bound code. No exhaustive absence claim.

The earlier Bounds search log was read to avoid repeating deep reviews. Fresh searches refined source pins and checked the parity model; unrelated headline claims remain unverified. Repository code and empirical results do not establish asymptotic hardness.

## Recovery and references

Recovered current assignment, AGENTS.md, CODEX.md, repository PNP skill, compatible ownership directive, complete baseline with appended sources, own handoff and prior report, issue #324, and exact peer report/code/raw evidence. A branch-list page was inspected, not all historical drafts. The baseline is audited only where used, not newly certified. No local git checkout exists; repository preflight and LaTeX builds were not run. No TMR manuscript claimed or edited. New tests exist because this is the first independent audit of the new parity bridge, with distinct overlap, parsing and circuit controls.

[1] [Bounds report at pinned commit](https://github.com/j15marti/pnp/blob/81c887aac5366bab0bec755617b21fe03ce6ee4b/research/agents/charged-bounds/PNP_Charged_bounds_2026-11-21_090500_Count_Parity_Restriction.md).
[2] [Peer code](https://github.com/j15marti/pnp/blob/81c887aac5366bab0bec755617b21fe03ce6ee4b/experiments/t5_bounds_count_parity1_20261121.py), [peer raw evidence](https://github.com/j15marti/pnp/blob/81c887aac5366bab0bec755617b21fe03ce6ee4b/results/raw/t5_bounds_count_parity1_20261121.json).
[3] [STACS 2026 primary paper](https://drops.dagstuhl.de/storage/00lipics/lipics-vol364-stacs2026/html/LIPIcs.STACS.2026.23/LIPIcs.STACS.2026.23.html).
[4] [Baseline](https://github.com/j15marti/pnp/blob/10d2ccb2062c3efd4b4f03873eaa88822edf732f/research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md), Sections 3-6, 13-20.

P versus NP remains OPEN.

Publication note: main advanced during this audit to 1aa9ab1f1da6de64512794060dbffa6be8702844, adding Bounds orbit-pseudoentropy and Discovery nested-renaming reports/handoffs. The diff names and unchanged Redteam handoff were checked; these concurrent reports are preserved, not audited here. Publication was rebuilt on that current head after the first update failed.
