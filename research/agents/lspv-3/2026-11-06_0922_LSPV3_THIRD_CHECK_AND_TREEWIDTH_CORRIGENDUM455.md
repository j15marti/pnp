# LSPV-3/455: Third independent strict-3 BPHP audit, previous treewidth bound correction

**2026-11-06 09:22 PST | Route B | KNOWN THEOREM, PROVED/RESTRICTED, COMPUTATIONAL, OPEN.** No P versus NP proof. Fixed historical R_mix341, five roles, 2 Route A/3 Route B allocation, schedules, ownership and weights unchanged.

## IDEA, explicit falsifiers, SEARCH and ITERATE

Hypothesis: independently reconstruct the full strict-three original-source bit-PHP certificate from already produced LSPV-3/454 raw evidence, checking every signed source, globally fresh paid DEF gate, typed owner-qualified facet, correct oriented RES pivot, root, ancestry and adversarial corruption. Cross-check purported newer treewidth work against existing project reports.

Four falsifiers: (F1) paid definition reuses an ORIGINAL source-private wire; (F2) an unjustified defining facet, altered source or false pivot is accepted; (F3) a declared empty-clause root excludes any counted source or paid node, or SAT/UNSAT/malformed controls fail; (F4) the earlier 08:57 /453 result is a duplicate of stronger pre-existing work. F1-F3 passed the independent checker after the previous /454 producer had already repaired a real freshness bug. **F4 fired: /361 already proved a strictly sharper upper bound.** This is a reporting correction, not a new theorem. The original /453 report and five-role handoff have both been updated with visible corrigenda.

## PRIOR established sharper treewidth upper bound, not a new proof

For UNSAT F, let v count actually OCCURRING variables, w_i(sigma) be each elimination frontier size, and tw(F) primal graph treewidth. Previous verified LSPV-3/361 already proved

$$
W_R(F)\le \min_{\sigma}\sum_{i=1}^{v}3^{w_i(\sigma)}
\le v\,3^{\operatorname{tw}(F)}.
$$

A variable's w-neighbor bucket can generate at most 3^w distinct non-tautological conclusion clauses because each remaining variable is positive, negative or absent. The up-to-9^w parent pairs are redundant; one source-labelled native oriented RES inference per distinct conclusion is enough, and sharing is charged once. Therefore /453's n*9^tw result was correct but weaker and duplicative. The stronger /361 source is https://github.com/j15marti/pnp/blob/main/research/coordination/2026-11-03_0324_LSPV3_DP_WIDTH_UPPER361_HANDOFF.md, blob 7ccbdce81cf836ba87988f046fa556375d9d4e04. Low treewidth only gives an upper bound; high treewidth does not imply mixed hardness, as existing linear-time-size mixed odd-expander Tseitin proofs show. This is ideal paid logical work, not physical solver runtime.

## Established family, model qualification and exact strict-three encoding

Braun arXiv:2609.23015v2, metadata last revised **2026-11-03**, proves in the stated formally checked preprint model a lower bound greater than exp(n/(32768 ell^2)) for unrestricted shared-DAG **Res(XOR)** proofs of bit pigeonhole with n=2^ell holes and n+1 pigeons, ell>=32. Its M=n*binom(n+1,2) original clauses have width 2ell, not width three; the lower bound does NOT apply to arbitrary algorithms, R_mix341 or proof systems with charged extension definitions. This run did not replay the Lean formalization or establish peer review. The current ell=2,3,4 test fixtures are **BELOW the published ell>=32 threshold**.

For each original width-k clause, replace it with its standard k-2-clause signed private strict-3 chain using k-3 fresh source wires. This preserves the exact existential projection of the wide clause and permits a k-3-paid-RES recovery, as previously established in LSPV-3/445. Equisatisfiability and upper recovery are NOT a lower-bound-preserving proof transformation.

For the finite upper-bound trace we separately declare proposed **FACET-A** grammar: one paid conservative, globally fresh two-input signed-AND DEF owner makes its exact three signed defining clauses available for RES as typed (owner ID, facet index) references. Prior /454 separately checks a proposed **OWNER-LOCAL** type requiring three separately paid unary LOCAL exports per owner. On ell=2 FACET-A has 495 and OWNER-LOCAL has 555 charged nodes. The original historical /341 text DOES NOT specify a complete independent native accepted-byte DEF-facet/LOCAL port serialization. Neither proposed grammar can be called authenticated native accepted-byte R_mix341. This typed limitation is load-bearing.

## New independently executed third checker and controls

A new standard-library-only Python implementation, with no code imported from the original Python producer or independent Node verifier, reconstructed exact signed original strict-3 bitPHP DIMACS from scratch. It verified the full original source, every globally fresh DEF output above the entire original variable maximum, every three-clause defining facet, all RES parent references and pivots, exact conclusions, declared work and root dependency ancestry.

| ell | original clauses | original variables incl. private | paid DEF | paid RES | paid total | certificate status |
|---:|---:|---:|---:|---:|---:|---|
| 2 | 80 | 50 | 20 | 475 | **495** | Genuine empty root; exactly 575 original/paid nodes in root ancestry |
| 3 | 1152 | 891 | 108 | 2871 | **2979** | All predecessor derivations verified; NO empty root supplied |
| 4 | 13056 | 10948 | 476 | 30039 | **30515** | All predecessor derivations verified; NO empty root supplied |

Exact original source SHA256: ell2 13361aa6164d76373ac8d4b4b6935f05257bb99266441f3405cfeecb653da6a6; ell3 27f97b3a3c906b2858769ad9e9d691dfd95002852c5f99febf01e21f11c3bd9d; ell4 38bb9c946fe622532d5ab2f93136241177b53960e328e63bb98bdcb1f2f2b3be.

Six independently generated malicious ell2 proof mutations REJECTED: definition/source ID collision, wrong defining-clause sign, wrong RES pivot, modified signed source, forged root, and forward parent reference. A separate second standalone source-label test enumerated all 4^4=256 assignments for 4 pigeons/4 holes and checked 24 satisfying projected assignments, and all 4^5=1024 assignments for 5 pigeons/4 holes and checked zero, by existentially validating every private chain. Five malformed-source controls rejected: header count, missing source clause, malformed terminator, out-of-range literal and non-ASCII header.

Logical nodes differ from evidence bits and execution costs. Original ell2 source 868 bytes, full refutation JSON 51,804 bytes; ell3 raw proof 364,964 bytes and ell4 4,096,647 bytes. Actual third-checker time/peak RSS: ell2 including six corruption controls 0.81 s/97,600 KiB, ell3 0.81 s/101,776 KiB, ell4 1.63 s/154,356 KiB; paired source-label/malformed test 0.84 s/96,540 KiB. Producer/search, source authentication, cache/retrieval, serialization, verification, failed policies and all-phase simultaneous space need separate machine charges; previous /454 provides the independently run producer/Node ledger. These are not same-machine FLMV bounds.

## Corpus/source and status audit

Read original LSPV-2/341 SHA c87acd11, governing handoff SHA c3889a3, earlier /361, /389-/390, LSPV3/445, /449, /451-/454, red-team REFEREE299,315,316,358,368, issue #3, AGENTS.md, CODEX.md, skill and formatting handoff. Grok actual GROKPROOF/2026-11-06_1617_PROGRESS.md SHA b931933 and Claude actual research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex SHA 1f9fc72 retain B3 OPEN.

External inspected pinned content: konard/p-vs-np proofs/experiments/issue532/ideas/Idea27.md SHA f61827f, scripts/proof_status.json SHA 93b77ed; blkph0x/p-vs-np-proof-research METHOD_INDEX.md SHA 18d693e and PROOF_PORTFOLIO_BRIDGE_REPORT.md SHA 22215ce; meelgroup/frat-xor format.md SHA 986a21aa and cake_xlrup/README.md SHA c71de80. The FRAT-XOR/CakeML proof formats are not native R_mix341. General indexed primary search reviewed Braun v2, Urquhart 1987 restricted ordinary Resolution-hard expander Tseitin, and Cook 1976 polynomial Extended Resolution PHP proofs. Google-branded direct search, full git local preflight, independent Lean replay and historical accepted-byte checker were unavailable, not claimed. Full executable independent Python checker, paired-label controls, original raw signed CNFs, original proof traces, verification outputs, resource logs, detailed report and digest manifest are in downloadable dated reproducibility archive; GitHub records a compact peer-readable report and handoff.

## Remaining exact obligations

(1) Recover the authentic historical native byte-level grammar for paid DEF facets and LOCAL/export wiring, or present a typed counterexample; acceptance under *proposed* FACET-A does not close that gap. (2) Prove an all-rules superpolynomial worst-case minimum for a certified-hard strict-3 family allowing every legal ER, XOR, AND3, LOCAL, branching and shared subcomputation. A Resolution-only or Res(XOR)-only lower bound does not suffice. (3) Independently prove same-fixed-R noncircular B3, SAT in P implies polynomial mixed minimum worst-case. Both are OPEN. P versus NP OPEN.

Primary references: Braun arXiv:2609.23015v2 (2026-11-03); Urquhart JACM 34(1):209-219 (1987), DOI 10.1145/7531.8928 (Resolution only); Cook, SIGACT News 8(4):28-32 (1976), polynomial ER PHP; original LSPV3/361 and /454.

## ADDENDUM: independent paid OWNER-LOCAL type replay, not native historical acceptance

A distinct third-party Python verifier (no original producer or previous Node checker code) also checked the separate PROPOSED OWNER-LOCAL interface. A paid DEF owner is **not** a RES clause parent in this grammar. Each of its three signed facets must first appear as a distinct, paid unary LOCAL node; RES can cite only SOURCE, LOCAL, or RES clause references. Each signed facet, true owner, reference type, unique gate output, oriented RES pivot and final root is checked.

- ell=2 full strict-three source: 80 original + 20 DEF + 60 paid LOCAL + 475 RES = **635 source/paid ancestry nodes**, of which **555 are paid**. Genuine empty-clause root independently verified. All six additional hostile mutations REJECTED: wrong LOCAL clause, wrong owner, illegal direct DEF-facet RES parent, invalid LOCAL facet index, wrong RES pivot and falsified paid-LOCAL count.
- ell=3, premise derivations only: 1152 original + 108 DEF + 324 LOCAL + 2871 RES = **4455 records / 3303 paid**, and no root. Original source checksums match independent FACET-A.
- Physical checker process ell=2 (including six hostile cases): 0.74 seconds, 97,680 KiB RSS. ell=3: 0.99 seconds, 101,904 KiB RSS. These are validation resources only, not solver construction cost.
- The second checker was independently executed from the conversation's reproducibility ZIP and its corresponding GitHub verifier is under experiments/arc/lspv3_455_third_ownerlocal_checker.py. The raw OWNER-LOCAL proof and original source are in the ZIP.

**Historical-granularity firewall:** The original R_mix341 LOCAL rule limits support to at most **three original variables**; a paid DEF output may depend on many original variables. Therefore a three-*named-wire* LOCAL implication accepted by this proposed OWNER-LOCAL checker is not automatically permitted in historical LOCAL-CONVERT. Proving that implication requires a valid native input-type and support/export derivation, not just matching the three-clause gate truth table. A complete accepted-byte historical checker remains OPEN.
