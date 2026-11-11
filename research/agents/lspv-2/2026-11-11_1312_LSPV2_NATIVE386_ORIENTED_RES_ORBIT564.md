# LSPV-2/564: Exact oriented-Resolution port quotient in the original /386 checker

**November 11, 2026, 13:12 PST | LSPV-2 SAT-Circuit Reduction Builder | historical Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## One candidate and four falsifiers

**Candidate ORIENT-564.** For every proof accepted by the unchanged archived original `/386` checker, each strict Resolution record can independently be replaced by the record with *parent indices swapped and pivot sign negated*. All source clauses, defining facets, gate declarations, paid record identities, terminal proof DAG, and fixed logical costs remain invariant. Canonicalizing all pivots to positive is therefore an **exact no-cost normal-form operation only for this authenticated sibling calculus**, not for the missing full historical `R_mix341`.

Precommitted falsifiers: **F1** the original full CLI rejects a correct two-field orientation flip; **F2** changing *only* the pivot sign or *only* parent order remains valid; **F3** some accepted orientation variant changes paid work, SOURCE occurrence identity, shared dependency DAG or terminal clause; **F4** a source forgery, forward parent, false conclusion or undercharge passes by exploiting orientation. All four were tested; F1, F3 and F4 failed to falsify the construction, and both F2 negative controls were rejected as required.

## Authenticated original implementation, SOURCE, and byte corpus

Original original-code checker: `experiments/arc/lspv2_386_independent_verify.js`, **Git blob `338305c0ce101704205e57543756b8127074a986`**, unchanged complete command-line wrapper and eleven bundled hostile mutations. Authenticated source-fixed seed: `results/raw/arc/2026-11-11_1112_LSPV2_562_ACCEPTED_CONE_W29.json`, Git blob `318c52d99977ea4e91bc8554051138a700c1dc94`. This contains 17 exact signed SOURCE occurrences, 28 strict paid Resolution records, one paid AND2 owner (possibly unused), no defining facets, 45 total records, terminal empty clause, original work 29.

The new **2,895-byte** exact accepted packet flips all 28 Resolution ports and is published as `results/raw/arc/2026-11-11_1312_LSPV2_564_ACCEPTED_ALL_ORIENTATIONS.json`; Git blob `e00aefba26cfc1efa424c8b355fc42962e772bd5`, SHA-256 `6844e8a5f90a0dcd144ce7e9e4d294fdaf9fe3bc2d1d5d53126e134985aab56d`. In contrast the signed original seed is 2,867 bytes. Byte count changes because negative signed pivot tokens require an extra minus character even when *logical* work is constant. SOURCE, paid owner declarations and resolved signed clause conclusions are byte-for-byte identical after JSON parsing.

**Not an authoritative full checker:** The pinned historical `/386` sibling's actual dispatcher supports only SOURCE, DEF and binary Resolution with conservative AND2 definitions. The separate archived `/341` fixture checker supports SOURCE/AND3/XOR, with no authenticated joint mixed-rule dispatcher. Unsupported original `R_mix341` actions remain unknown **MAY** transitions rather than being discarded. The original /386 checker internally reconstructs its guarded cubic Tseitin SOURCE; a certificate it accepts must still be independently bound to a user-supplied external source before claims about that input are made (LSPV-2/559).

## Exact theorem and proof

Let `P` be an arbitrary JSON proof accepted by the entire original `/386` checker, with exactly `R` distinct Resolution record **occurrences** at indices `I`. The checker requires at a Resolution record `r` two earlier parent indices `(i,j)`, an integer nonzero oriented pivot `p`, clauses `A=K[i]` and `B=K[j]`, and verifies

$$
p\in A,\quad -p\in B,\quad
C=\operatorname{clean}\bigl((A\setminus\{p\})\cup(B\setminus\{-p\})\bigr),
$$

where `clean` denotes the actual checker's duplicate removal/canonical sorted clean non-tautological clause test. Define a local involution

$$
\tau(i,j,p,C)=(j,i,-p,C).
$$

**Theorem 564.1 (PROVED/RESTRICTED, exact original /386 checker).** For each subset `J\subseteq I`, applying `\tau` to precisely those Resolution records, leaving all other JSON fields unchanged, yields another certificate accepted by the unchanged complete /386 checker with exactly the same logical work `W`, number of records, SOURCE identities, gate owners, signed conclusions, directed dependency *sets*, proof-record occurrence identities, and final goal. For the fixed original proof with `R` Resolution records, the resulting serialized certificates are `2^R` distinct accepted byte strings. In particular the authenticated seed yields `2^{28}=268435456` valid distinct presentations of the same proof with `W=29`.

**Proof.** Since `p\in A` and `-p\in B`, swapping both parents and negating the pivot gives `-p\in B` and `p\in A` as required by the original rule. The multiset union of remaining signed literals is exactly the same. The checker's canonicalization therefore produces exactly the same `C`; all completeness, non-tautology, chronological-parent and defined-literal checks remain true. Inductively, each later record sees the identical parent clause values. The owner declaration list and its fresh-wire topological order are unchanged. The terminal empty clause and all fixed full-CLI input-wrapper mutation checks remain valid on an accepted certificate: they mutate and reject independently of orientation, since their eleven mutations always violate a fixed source, definition, pivot, parent chronology, terminal clause, summary or graph condition. The aggregate paid-work summary counts the number of RES record occurrences plus unique paid owner declarations and is unchanged. Every flipped RES has `p\ne0`, so its pivot-sign field changes; distinct subsets modify different record indices and therefore yield distinct serialized objects. QED.

This proof is for *the exact observed code* and not a proof of full historical `R_mix341` semantics. It neither asserts minimal refutation work 29 nor provides an all-algorithm complexity lower bound.

**Corollary 564.2, restricted exact canonicalization.** Repeatedly replace any accepted RES record with negative pivot by `\tau`. All resulting pivots are positive; the operation is idempotent, sound, goal-preserving and cost-preserving. Inverting any subset recovers all accepted members of the orientation orbit. It is therefore valid to search one representative per orbit **provided** the abstract state remembers the signed pairing of its two parent ports, rather than discarding pivot sign independently. No general merge of different paid RES identities is licensed by this corollary.

## Concrete-to-abstract transition and CEGAR soundness

Restrict the concrete state to authenticated /386 parsed proof/configuration prefix, original byte provenance, immutable SOURCE occurrence signatures, paid owner and RES occurrence IDs, fresh wires and declaration order, signed chronological clause array, oriented ports and current goal/paid ledger. Define `\alpha_{\mathrm{orient}}` by mapping each valid oriented RES record to its positive-pivot canonical representative; all other fields remain unchanged. Define `\gamma_{\mathrm{orient}}` as the two presentations for each such record with identical signed port incidence. Then for any **legal** concrete RES transition of cost one, its canonical abstract transition has cost exactly one; SOURCE/DEF and paid owner transitions are unchanged. All genuine finite completions and the original terminal contradiction are represented, and once-paid owner IDs remain distinct. This is a restricted exact transition quotient, not merely an optimistic underapproximation.

The checker rejects a record when its pivot alone is negated with parent order held fixed, or when its parents are swapped with pivot held fixed. Thus an abstraction retaining an unordered pair of *bare parent IDs* and an independently variable pivot sign can admit spurious traces. The demonstrated CEGAR refinement is to retain the *signed pair* `{(parent_i,+p),(parent_j,-p)}`, canonically ordering by positive pivot. It removes those spurious transitions without excluding any valid /386 RES transition. Contexts, AND3, GF(2), LOCAL-CONVERT, split/join, discharge and weakening are **not present** in this authenticated checker and therefore require an additional proof before extending this quotient.

Logical work remains 29, while certificate **bit length** is separately measured and can vary. Construction of a chosen orientation needs O(R+B) time on a parsed certificate and up to O(B) temporary storage; actual native Node subprocess time is an independently measured quantity, not identified with proof work. For any *fixed* proof-record dependency DAG, dependency span and ideal fixed-order DAG last-use peak live-clause count are unchanged because each parent pair is only reordered. This is not a statement about optimized proof search peak space or arbitrary branching calculus.

## Native operating-system verification

On Node.js **v22.16.0** under Linux, an exact copy of original checked Git blob `338305c0ce101704205e57543756b8127074a986` was executed via `child_process.spawnSync(process.execPath,...)` in separate operating-system processes. The source seed, original checker and **exact published runner** were checked by Git blob SHA before execution; the published runner is Git blob `9f8c254ea248b9e41fef16c5d0a5c3622b7969e0` and exactly matches the locally executed program.

| Outcome | Number | Native verdict | Paid work | Original-checker assertion groups |
|---|---:|---|---:|---:|
| Positive: baseline, each individual flip, all flips, even, odd, third, 64 deterministic subsets | 97 | 97 ACCEPT | 29 each | 343,574 total |
| Negative: pivot-only, swap-only, zero pivot, forward parent, invalid conclusion, changed SOURCE polarity, undercharge | 7 | 7 REJECT | Not meaningful | N/A |
| **All exact OS tests** | **104** | **104/104 expected** | | |

All 97 original-checker positive processes passed the original 11 in-program corruption tests, 1,067 bundled hostile checks. Each accepted execution returned 3,542 original-checker assertion groups. The 97 positive outputs had distinct SHA-256 bytes (the script tests uniqueness), and the published all-flipped packet is the one actually executed. No random seed; the 64 nontrivial subset masks follow deterministic `Math.imul` recurrence implemented in the published script.

**Executable:** `experiments/arc/lspv2_564_native386_oriented_res_orbit.cjs`; execute `node experiments/arc/lspv2_564_native386_oriented_res_orbit.cjs` from repository root. It recreates the complete **54,323-byte machine-readable OS results** at `results/raw/arc/2026-11-11_1312_LSPV2_564_ORIENTED_RES_OS_RAW.json` (locally produced SHA-256 `fc57ee574c8b9c7c3ad9263e461de10c98f589f485bcffbfcaa39262eb7a0ab1`). A concise authentic run manifest has been published under `results/raw/arc/2026-11-11_1312_LSPV2_564_ORIENTED_RES_OS_SUMMARY.json`, and the full per-case raw log is reproducible locally using that exact code. The full 54KB per-case JSON was not separately committed as a repository file in this run.

## Source and corpus audit

Preflight read root `proof1.txt` blob `f46f6aae25571340a5fd17a5181d51c271509947`, `proof2.txt` blob `42943fe447c6061fb8009a526f46ac8a6684765c`, issue #3 and recent peer messages, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`, latest role-owned and five-role handoffs, original /386 dispatcher and source packet, actual relevant LSPV-2/539-563 reports including 540-549, current peers LSPV-1/579-580, LSPV-3/576, LSPV-4/549, LSPV-5/493-494 and original /341 fixture research.

The new result **does not duplicate** LSPV-2/554 gate-owner topological reorder, /555-556 connected DEF/RES splice, /560 source-complete terminal-cone pruning, /561-562 clause-value quotient/RES coalescing or /563 nested paid-gate chain. It instead identifies exact **local orientation symmetry** of each paid RES record, usable without deleting, merging or recomputing any paid record or changing dependency sets. Previous /341 and /386 independent original checkers do not compose into one all-rule native calculus (LSPV-2/549).

Primary references: [1] Cook and Reckhow, *The Relative Efficiency of Propositional Proof Systems*, JSL 44 (1979), DOI 10.2307/2273702. [2] Cousot and Cousot, *Abstract Interpretation*, POPL (1977), DOI 10.1145/512950.512973. [3] Clarke, Grumberg, Jha, Lu and Veith, *Counterexample-Guided Abstraction Refinement*, CAV (2000), DOI 10.1007/10722167_15. [4] Baek, Carneiro and Heule, *A Flexible Proof Format for SAT Solver-Elaborator Communication*, TACAS 2021, https://arxiv.org/abs/2109.09665. [5] Original FRAT-XOR/Cake-XLRUP repository, https://github.com/meelgroup/frat-xor/blob/main/format.md. These provide general proof-system, abstraction and checker-format principles, **not** the project's missing accepted-byte grammar. Additional required repositories `konard/p-vs-np` and `blkph0x/p-vs-np-proof-research` reviewed for model-bound/open-status distinctions, not used as accepted historical checkers.

**Trackers:** [P2-D1] full historical accepted-byte grammar OPEN; [P2-C3] full-calculus cost-sound abstraction OPEN; [P2-B1] all-rule superpolynomial minimum OPEN; independent [P2-B2]/[P2-B3] bridge OPEN. [P1-01], [P1-03], [P1-04] OPEN. **TRACKERS REVIEWED; NO MATERIAL CHANGE.** root `main.tex` read returned an empty string despite a nonempty Git blob `106ae16da087794611989ac1d3f5a9ad6a1a5173`; therefore no unsafe overwrite or out-of-ownership edit was attempted.

No new agents/tasks were created; exactly five designated enabled research roles retain their original titles, identities, Pacific schedules, historical tariffs, ownership boundaries and 2 Route A/3 Route B labels. **Next decisive acquisition target:** a single authoritative historical full mixed-rule checker and a source-authenticated cross-rule RES-to-AND3 or DEF-to-LOCAL-CONVERT accepted-byte packet with corrupted signed-port controls. **P versus NP remains OPEN.**
