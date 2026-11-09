# LSPV-1/526: exact 148-paid-node original CORE -> zero-plus-port proof splice

**November 8, 2026, 22:22 PST | Route B lead | PROVED/RESTRICTED in signed-AND2 ER2-OWNER/Resolution; COMPUTATIONAL independent full-DAG verifier. Historical R_mix341, B3, unrestricted lower bounds and P versus NP OPEN.**

**Affected chain IDs:** new [P2-L1-526], refining [P2-L1-525], [P2-L3-523], [P2-L3-520], [P2-L1-524], [P2-L1-520], [P2-F6] and a *local upper-control portion* of [P2-C3]. [P2-D1], [P2-C3], [P2-B1], [P2-B2] stay OPEN. [P1-X1] unchanged.

## IDEA before search, prediction, four precise falsifiers

**Hypothesis:** The verified signed ER2/OWNER identity packet [P2-L1-525], which assumed seven padded one-hot source clauses, can be spliced with the independently verified 21-clause original strict-3 CORE-to-inverse packet [P2-L3-523] without importing a single non-CORE source clause, weakening a clause, making a free semantic equivalence, or duplicating the shared original zero proof. Both packet DAGs remain acyclic and owner/type correct, at exactly 34 paid DEF and 114 paid binary RES nodes.

Falsifiers: (F1) old padding-variable $z$ or padded-AMO original clause survives the graft; (F2) a mapping of any added RES pivot or facet owner refers to a nonexistent/forward inference or changes an exact clause; (F3) conservative paid definitions lose global freshness or repeat an absolute input ID; (F4) an original CORE model falsifies an output equality, or the claimed local proof is improperly treated as an accepted historical R_mix341 proof. The first three were rejected by structural validation; (F4) semantic countermodels were excluded in the finite nine-model local test, while the historical translation remains explicitly OPEN.

## SEARCH: sources and precedence

Read both complete root trackers before work: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; `proof2.txt` blob `775dabe9fb69bc9a36b92a564dc3eafd4ed3dde0` (current at initial read). Reviewed current issue #3 (latest LSPV-1/525; LSPV-3/523; LSPV-5/452; LSPV-4/512); governing five-role `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md`; AGENTS.md `19656af102604d5f0a721d548cf2e4e72a063561`; CODEX.md `754999f50de93cdb693ed37bc8110d31e9e698ef`; repo skill `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`; and historical `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`.

Actual direct predecessors (not misrepresented as this run's novelty):
- LSPV-3/520 exact 21-source strict3 CORE inclusion/hardness transfer and 12-RES AMO macro, report `research/agents/lspv-3/2026-11-08_1925_LSPV3_MOD3_21CLAUSE_STRICT3_PORT520.md`.
- LSPV-3/523 CORE-to-inverse source-graft, report `research/agents/lspv-3/2026-11-08_2125_LSPV3_CORE_TO_INVERSE_ER2_PORT523.md`, executable `experiments/arc/lspv3_523_core_inverse_lift.cjs`, blob `c8c62a5eb9a64a6c6949217473ba5075558500c8`.
- LSPV-1/524 signed inverse source proof, `experiments/arc/lspv1_524_strict3_inverse_cancellation.js`, blob `3fa42e25e02d05b9a915458a7f780e59fd828c12`.
- LSPV-1/525 zero-addition identity for independent input bits, `experiments/arc/lspv1_525_zero_sum.cjs`, blob `1d6334fa5712f374bd0455445cd1bb40ac6a2fe0`.
- Actual Grok `GROKPROOF/2026-11-08_0930_PROGRESS.md` blob `e3e8c9657e0f2b2e0751752135cf2558e28183cf`; Claude `research/agents/claude/world-ledger/README.md` blob `de75a371ce3143a4495e6892df7fb04794a6b708`. Neither resolves native Rmix.

Change-aware external repository reads: `konard/p-vs-np/README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` and `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`; `blkph0x/p-vs-np-proof-research/README.md` blob `f397a7747eaca82df3d754d0a4b4bab1fe10f814` and `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`; `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f` and `tanyongkiam/cake_lpr/README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`. None authenticates historical Rmix or proves B3. Google-branded direct search was unavailable; public search and the primary Pang HTML were used.

Primary research: Shuo Pang, *A Degree–Size Relation for Resolution over Polynomials*, arXiv:2610.00837v2 (24 October 2026), Theorem 7.2(b), Corollary 7.3, https://arxiv.org/html/2610.00837v2 . Its fixed-$r$ opposite-characteristic lower bound is restricted and is not contradicted by ER2 certificates with paid gate definitions.

## ITERATE: typed source, splice and exactly charged result

Use one ORIGINAL positive-signed, charge-zero cubic vertex, with independent edge-indicator triples $X=(1,2,3)$, $Y=(4,5,6)$ and $Z=(7,8,9)$, and exactly the 21 clauses

$$
X_0\lor X_1\lor X_2,\quad Y_0\lor Y_1\lor Y_2,\quad Z_0\lor Z_1\lor Z_2
$$

and the 18 forbidden clauses

$$
\neg X_a\lor\neg Y_b\lor\neg Z_c\quad(a+b+c\not\equiv0\pmod 3).
$$

Every original source is proper signed width 3. The 21 clauses imply exact one-hot edge values and enforce the local charge-zero relation. There are exactly nine satisfying assignments to these nine original Boolean atoms. This local source is SAT, not a complete global Tseitin UNSAT refutation.

LSPV-3/523 already reconstructs the three originally absent AMO clauses for $X$ using 12 oriented original-source RES steps each, then proves the zero-sum packet using 19 paid signed two-port definitions. Reuse this *entire* 165-record DAG, with its 87 RES and all shared zero deductions. From /525 append **only** the 15 new definitions and 27 new RES steps needed for $0+Y=Y$, not the padded sources or the preceding /524 proof.

An exact order-preserving source/definition mapping exists. In /525, original IDs $1,2,3$ map identically, original independent port IDs $5,6,7$ map to CORE IDs $4,5,6$, and every paid auxiliary ID $j\ge8$ maps to $j+2$. The old padding $z$ ID 4 is **forbidden**. Old /525 line IDs $i\ge10$ map to $i+47$ in the CORE DAG. All new RES pivots, parent indices, gate ports, owner facet selectors and goal references undergo this mapping. Gate IDs become globally fresh 10..43. No branch-local assumptions or case-split/discharge rules are used.

**Theorem 526.1, PROVED/RESTRICTED.** In the separately declared signed-AND2, owner-qualified-facet extended-Resolution calculus, the exact original 21-clause CORE admits a single acyclic shared-DAG proof of all six Boolean equivalence clauses for the zero-addition identity

$$
0+Y=Y\quad\text{on its three indicator bits}.
$$

The output signed literals are $(-39,-41,-43)$ and the original inputs are $(4,5,6)$. Output goal pairs reference lines $(208,210)$, $(221,223)$ and $(234,236)$. Each equivalence is represented by two *exact* derived clauses, with no free weakening.

Charged distinct-node count:

$$
34\text{ paid DEF}+114\text{ paid RES}=148\text{ total paid nodes}.
$$

There are 21 original source lines, 102 definition-owned facet records and 237 total records. Graph-based paid dependency depth, charging every DEF and RES once on its own path, is at most 18; this is not machine parallel time. The three output identities share all upstream source-to-zero reasoning.

## Actual computation and hostile controls

The new generator `experiments/arc/lspv1_526_core_zero_port.cjs` requires three exact pinned upstream Git blobs, with no additional rules. An independently authored `experiments/arc/verify_lspv1_526_core_zero_port.cjs` checks the 21 exact original source clauses, all 34 globally fresh/distinct-input definitions, 102 owner/facet references, all 114 oriented binary RES edges, DAG acyclicity and all six exact output clauses. In V8 the independent verifier completed **52,645 assertions** and enumerated all **512** original Boolean assignments, including the **nine** valid source models. Every valid model satisfied the seven inherited CORE packet goals and all six new clauses. **Six** corruptions were rejected (pivot, resolvent, source, facet owner, duplicate gate ports, missing equality case). This is an independent checker for the separately declared ER2 syntax, **NOT** execution of an authoritative historical Rmix checker.

The complete materialized packet, including all 237 original/source/owner/pivot records and results, is `results/raw/arc/2026-11-08_2222_LSPV1_526_CORE_ZERO_PORT_RAW.json` (51,356 UTF-8 characters). Generator and checker contain 3,546 and 4,016 characters. The V8 checker was executed against the actual merged packet, not merely its source program. GitHub report/code/raw publication and complete readback were verified. Physical elapsed wall time, RSS peak and full construction/check/output cost exponents were not measured; don't identify 148 paid logical nodes with wall-clock SAT time. Any future scaled algorithm must charge indexing, parsing, proof search, references, caches, repeated failed attempts, I/O, materialization and all-phase simultaneous memory.

## Family/encoding/theorem/known shortcut/remaining transfer ledger

**Published hard-source control:** Pang's fixed-degree regular expander family of mod-3 Tseitin equations with nonzero global charge; the standard one-hot source has $9h/2$ Boolean variables and $24h$ clauses. LSPV-3/520 deletes redundant AMO clauses to get a literal subformula with $9h/2$ variables and $39h/2$ proper signed strict3 clauses, $N=\Theta(h\log h)$, and transfers Pang's $\exp(\Omega_r(h))$ fixed-$r$ Res(PC$_r/\mathbb F_2$) DAG lower bound via source inclusion. This *local* 21-clause proof concerns one charge-zero vertex of that encoding and is an ER2 upper-control. Other valid strategies include the exact LSPV-3/520 AMO reconstruction, the native-resolution LSPV-1/522 vertex interface, Cook ER, shared DAGs, matching-characteristic GF(3) and the balanced cancellation construction. None may be removed from the legal minimum to protect the restricted lower bound.

**Remaining transfer:** compose authenticated vertex and edge packets into a full original-source global contradiction; certify every LCA cancellation/congruence/substitution step; establish exact historical Rmix341 grammar/weights and native simulation [P2-D1]/[P2-C3]. Superpolynomial optimal work under *all* fixed mixed rules [P2-B1] and noncircular same-calculus SAT-in-P => polynomial worst-case minimum B3 [P2-B2] both remain OPEN. No universal SAT time lower bound or P-versus-NP resolution is claimed.

**Root main.tex:** complete content API fetch returned blob `fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba` but zero readable bytes. No unsafe root manuscript edit attempted. Historical Rmix rules, weights, agent identities, enabled states, titles, schedules and 2 Route A / 3 Route B split remain intact. P versus NP OPEN.
