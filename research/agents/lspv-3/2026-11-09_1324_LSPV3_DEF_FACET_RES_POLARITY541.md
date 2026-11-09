# LSPV-3/541: DEF-facet polarity is invisible to exact original-assignment masks

**2026-11-09 13:24 PST | Route B | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Proof-chain IDs:** proposed new [P2-L3-541], refining [P2-L3-540], [P2-L5-466], and the open interface obligation [P2-C3]. Historical accepted-byte grammar [P2-D1], superpolynomial mixed minimum [P2-B1], and same-calculus B3 [P2-B2] remain OPEN. Route A and `proof1.txt` unchanged.

## IDEA: candidate and four advance falsifiers (before literature search)

Candidate (falsifiable): exact truth masks over all assignments of the *original* variables, accompanied by the paid DEF owner, determine whether a Boolean-clause Resolution inference involving a fresh gate output is syntactically legal.

F1. Every defining facet for one gate with the same extensional original-assignment mask has the same oriented Resolution pivots. **FALSE.** F2. The source-derived unit `(x)` cannot distinguish those facets through RES. **FALSE.** F3. Retaining clause literal syntax and the unique paid DEF origin still permits a forged resolvent / undercharges the shared definition. **Not found in the declared typed audit; tested corrupted records rejected.** F4. A real authoritative historical parser accepts all the proposed facet-reference and context syntax. **OPEN; not assumed.**

The revised claim is **negative**: mask+DEF-owner is NOT an exact RES eligibility domain. Refinement to (mask, syntactic literal set, paid DEF owner and facet index, DAG contexts and identifiers) repairs this specifically exhibited loss of information. It does **not** prove a superlinear lower bound.

## SOURCE SEARCH and overlap audit

- Governing refocus: `research/coordination/2026-11-09_ABSTRACT_INTERPRETATION_NEGATIVE_FIVE_ROLE_REFOCUS.md`, blob `8a6fd9f5dc73a2ed943e8630cad63bdd768b0b1b`.
- Startup complete root `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; complete `proof2.txt` blob `3298a3fcc7fd5383a371a671e21cada58c99e556` (~811 KB). Issue #3, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md` and historical 2026-11-02 five-role handoff read.
- Original /341 declaration: `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex`, blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`. Specifies one paid conservative two-input DEF with all defining relations attributed to that node, paid oriented binary RES, unit logical weight, and a local truth-table AND3. DOES NOT specify byte-level facet references and exported/private tags.
- Red team: `research/main/2026-11-07_0748_MAIN_AND3_PARENT_GRAMMAR_REFEREE412.md` blob `b99084b9e1534654207042d00d6645361dfc5863` proves surviving prose underdetermines AND3 parent grammar; `research/main/2026-11-03_0748_MAIN_LOCAL-CONVERT-PAYLOAD-FIREWALL-REFEREE315.md` blob `66a184474eb04f07b130af031e3cae500c38bf44` shows arbitrary circuit payload can defeat bit-cost domination at fixed logical node count; `research/agents/lspv-3/2026-11-07_1724_LSPV3_PAID_ABSORPTION_PRIVATE_PORT486.md` blob `dd81cfdc362cc637748398c9c5236b1519899cef` analyzes paid private-port copying.
- Latest LSPV-3/540: `research/agents/lspv-3/2026-11-09_1226_LSPV3_LOCAL_FACTOR_DOMAIN_OPTIMALITY540.md` blob `fe1456d56f790b951dafed231c1c4064d86bf016`. Its 8-bit exactness theorem is for binary AND3 on <=3 original inputs, **not** for syntax-sensitive Resolution through conservative fresh definitions. LSPV-5/466 `research/agents/lspv-5/2026-11-09_1149_LSPV5_PROVENANCE_ALPHA_JOIN466.md` blob `6377759d8746728eed3c738274afad28de1a9890` proves a distinct paid-origin reconvergence repair.
- Actual independent Grok `GROKPROOF/2026-11-09_2015_PROGRESS.md` blob `5610d47e2a78ded4e4e57bc24fca3266e03f42ac`, and Claude `research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex` blob `79e4d4e7e0e3edff3aba8610852c45534bdde128`: no native parser resolution.
- Change-aware required repositories: `konard/p-vs-np:scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2` (scoped theorem targets); `blkph0x/p-vs-np-proof-research:METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` (method/status ledger); `meelgroup/frat-xor:format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f` (EXTERNAL clause/XOR IDs and separate checker boundaries); `tanyongkiam/cake_lpr:README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`; `openai/math:README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`. None supplies the historical /341 accepted-byte productions.
- Primary literature checked: Cousot & Cousot POPL 1977 DOI 10.1145/512950.512973 (sound may-overapproximations); D'Silva-Haller-Kroening, *Abstract Satisfaction*, POPL 2014 DOI 10.1145/2535838.2535868 (abstract deductions, NOT proof-work lower bounds); Giacobazzi-Ranzato-Scozzari JACM 2000 DOI 10.1145/333979.333989 (completeness refinements); Chew-de Colnet-Slivovsky-Szeider AAAI 2024 DOI 10.1609/aaai.v38i8.28635 (random reordered parity 3-CNF exponential ordinary-DAG-Resolution lower bounds, short DRAT as a stronger system control). The external tools were web search and the authenticated GitHub connector; no Google-branded interface or authoritative native checker was executed.

**Established-family control:** Odd-charge cubic expander Tseitin has 3h/2 edge variables, 4h original proper 3-clauses, O(h log h) encoded length and exponential Resolution complexity for qualifying published expander families; the /341 declared AND3/GF(2) construction uses 4h-1 paid nodes. Separately, published reordered-parity rPar(n,sigma) uses 3n-6 variables and 8(n-2) proper 3-clauses, exponential ordinary Resolution with high probability, and short DRAT (not a universal mixed lower bound). The witness below is a **focused syntax-validation control**, not an invented hard SAT family.

## ITERATE: parameterized facet-polarity indistinguishability theorem

Let original distinct Boolean coordinates x,y belong to a larger original set of any size k>=2. Introduce one globally fresh paid DEF output z with unique conservative extension

$$
z \leftrightarrow (x \land y).
$$

The three defining-clause facets (charged to this ONE DEF origin, not separate axioms) are

$$
C_0=(\neg z\lor x),\quad C_1=(\neg z\lor y),\quad
C_2=(z\lor\neg x\lor\neg y).
$$

Under **each** original assignment uniquely extended by z=x AND y, ALL three facets are true. Thus their original-assignment extensional masks are identical to TOP, for every k>=2. In particular, (mask, DEF owner) gives identical abstract summaries for C_0 and C_2.

Yet the oriented RES step from `(x)` on pivot x with C_2 is legal and has the exact resolvent `(z OR not y)`, whereas the same step with C_0 is illegal: C_0 does not contain the complementary literal `not x`.

Therefore no **deterministic exact** RES-eligibility checker taking only parent extensional masks and the DEF-owner identifier can distinguish these two parent edges. This is a formal information-loss/precision obstruction. It does NOT invalidate sound MAY overapproximation, which may retain both possibilities; the spurious edge must be handled by CEGAR before claiming nonreachability.

**Cost-sound syntactic repair in declared typed fragment E541 (not native historical bytes):** preserve a facet's complete signed-literal set and immutable paid DEF origin in addition to its original-input mask; require oriented pivot, correct exact resolvent, topological ancestry and one charge per DEF/RES node. Then every accepted RES step is an ordinary valid Resolution inference from already available clauses; every DEF is a conservative extension with all facets available only after the paid owner. This is a direct induction over the typed DAG, including reconvergence through common earlier owners. The step witness incurs one paid DEF and eight paid RES nodes, with no charge for individually reusing facets but no free independent creation of gate semantics.

**Strict 3-CNF original-source witness:** variables (x,y,a,b,c,d)=(1,2,3,4,5,6). Use eight original strict proper clauses:
- `(x or a or b)`, `(x or a or not b)`, `(x or not a or b)`, `(x or not a or not b)`;
- the same four clauses with `x,a,b` replaced by `y,c,d`.

Three RES nodes from the first four clauses derive `(x)`, and three from the second group derive `(y)`. After the paid DEF `z=x AND y`, resolve `(x)` with C_2 to derive `(z OR not y)`, then resolve `(y)` to derive `(z)`. All original clauses are authenticated, the original formula is SAT (16 assignments), and the proof proves `z` under that source plus the charged definition; it is NOT an UNSAT refutation. The same gate facets have TOP masks over all 64 original assignments. An attempted one-step derivation of `(z)` from `(x)` and C_2 is a **corrupt certificate**, even though global source plus definitions entails z; it is not the literal RES resolvent and is rejected. This separates source-global entailment from correct local inference provenance.

A context-control with incompatible assumptions `Gamma={x}` and `Delta={not x}` leaves a nonempty, inconsistent assumption label on their joined descendant. It does not give a global refutation absent an authenticated native discharge. This is a representation test, not a new case-split rule.

## Finite verification, resource account and errors

Independent Python and independently authored Node.js implementations both PASS the 8 original clauses, six RES steps yielding the units, the single DEF with three attributed facets, and two final RES steps. Python checks all 64 original assignments, rejects malformed clause, uncharged DEF, nonfresh output and incorrect pivot, and checks 6,132 facet evaluations for k=2..10. Python: 0.05146 seconds, 48,612 bytes peak traced Python allocations in one recorded execution (NOT actual peak RSS). Node.js retrieved **back from GitHub** and independently replayed in V8: 223 explicit assertions, 192 gate-facet checks, 2 rejected corrupt RES orientations. Python performs 5 explicit additional logical controls. JavaScript tests a >2^53 integer as BigInt and uses a small semantic surrogate for clause manipulation; Python actually uses the complete 28-digit fresh semantic identifier in the refutation. No historical checker run is claimed.

Logical work: 9 distinct paid nodes (1 DEF, 8 RES). Premise node references: 16 for RES, 2 earlier wire inputs for DEF, and three generated DEF facets bound to its paid owner. Ideal paid critical-path depth: 4 (three-step unit derivations finish by depth 2, DEF at depth 1, two subsequent pivots at depths 3 and 4). Python compact UTF-8 serialization of the displayed source and paid trace subset: 7,208 bits; this is **not** a complete historical proof-file size. Construction, parsing, source reading, lookup, serialized identifiers, facets, validator time and peak memory are separate real implementation costs and do not inherit unit weight.

The exact upper bound exhibited here is only on a SAT formula in a proposed typed audit fragment. No negative budget-exclusion invariant is claimed. This run supplies an adversarial refinement obligation on such an invariant: keep literal polarity and DEF facet origin, not just extensional mask.

## Status, publication and next OPEN implication

**PROVED/RESTRICTED:** original-input mask + paid-DEF-owner is not sufficient for exact oriented Resolution when facets of a conservative gate are available. Signed syntactic clause views, owner identity and reference scope repair that exhibited failure. **COMPUTATIONAL:** strict original 3-CNF trace and independent tests. This does not authenticate native bytes, generalize to every historical mixed rule, or imply all-algorithm hardness.

**OPEN:** [P2-D1] historical grammar, [P2-C3] complete source-authenticated all-rule abstract transformers, [P2-B1] superpolynomial minimum work for same full calculus, [P2-B2] noncircular same-calculus B3. Need accepted historical FACET/LOCAL-CONVERT/DEF grammar and a native executable accepted proof to advance beyond this typed obstruction. Unrestricted SAT and P vs NP remain OPEN.

Files: `experiments/arc/lspv3_541_def_facet_resolution_independent.cjs`; `results/raw/arc/2026-11-09_1324_LSPV3_541_DEF_FACET_RES_RAW.json`; `research/coordination/2026-11-09_1324_LSPV3_DEF_FACET_RES541_FIVE_ROLE_HANDOFF.md`. Independent Python package also attached as a durable local fallback.
