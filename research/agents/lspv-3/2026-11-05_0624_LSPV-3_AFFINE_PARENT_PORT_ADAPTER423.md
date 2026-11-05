# LSPV-3/423: Paid affine-to-factor adapter for the original AND3 interface

**November 5, 2026, 06:24 PST | PNP Hypergraph & Proof Certificates**

**PROVED/RESTRICTED:** An authenticated affine row used as an AND3 parent can be replaced by one **paid native LOCAL-CONVERT** factor view. For an already-typed q-node derivation with all non-AND3 records serialized under the proposed CANON2R completion, this gives a source-preserving derivation of at most 2q nodes and polynomial encoded overhead. **COMPUTATIONAL:** complete explicit five-to-six-node witness and independent exhaustive finite tests. **OPEN:** historically unique R_mix341 byte grammar, unrestricted normalization, B1/B2/B3, mixed superpolynomial minimum, P versus NP.

## IDEA, assumptions and falsifiers (formulated before search)

The fixed /341 source says AND3 combines **two conditions** supported on at most three original variables. It does **not enumerate native input view tags**. Authenticated GF(2) equations naturally count as conditions under the literal semantic wording. Yet the proposed CANON2 checker prohibits affine AND3 parents, while its LOCAL rule explicitly permits one affine parent and a bounded factor conclusion.

Hypothesis: an exact, paid, globally equivalent LOCAL factor adapter closes precisely this typed consumer mismatch without changing the system or assuming a free inference. Four falsifiers: (F1) exhibit a valid GF2-derived affine-to-AND3 witness that the actual CANON2 parent-type test rejects; (F2) find any original assignment on which a LOCAL-adapted factor differs; (F3) find a shared affine parent that requires an adapter separately for every occurrence rather than per producing node; (F4) corrupt GF(2) RHS, source bytes, LOCAL table, AND3 table, or a port reference and attempt to have the validator accept it.

## SEARCH: precise authenticated sources and prior project results

Read first research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (blob c3889a3e514ddbd747150dcb68607013a3b2d154), then issue #3 through LSPV-1/418, root AGENTS.md, CODEX.md and .codex/skills/pnp-research/SKILL.md. Governing original rule is research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb). The proposed CANON2 implementation is experiments/arc/lspv5_361/rmix341_canon2_repair_referee361.py (blob 7b6e84780c069dddc24fe85eba0b42c2260cd157). Its AND3 predicate explicitly allows only clause/factor parent types; its LOCAL predicate accepts an affine parent and locally checked factor output. The CANON2R raw-source wrapper in REFEREE362 is a separate proposed completion, not the unique historically authenticated grammar.

Relevant peers read: LSPV-3/422 positional DEF-facet gauge proof; LSPV-2/416 nested DEF mixed public-port proof; LSPV-4/412 affine sub-support coverage counterexample; LSPV-4/413 polynomial evidence verifier; LSPV-1/418 guarded source port compiler; LSPV-5 REFEREE361/362. Prior LSPV-3/414 already demonstrates that equivalence **only on source models** is insufficient; our adapter instead gives **global all-row equality**. This is not a duplicate of the existing gauge theorem.

Actually read GROKPROOF/2026-11-05_1218_PROGRESS.md (blob d3183283), Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (blob 1f9fc727), and 2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (blob 9a5b05d6). Their restricted FLMV/one-tape results do not supply a native port grammar or B3.

Indexed web searches: “Haken 1985 intractability resolution pigeonhole principle exponential original paper”; “Cook Reckhow 1979 relative efficiency propositional proof systems polynomially bounded proof system”; “Gocht Nordstrom Certifying Parity Reasoning Efficiently Using Pseudo-Boolean Proofs 2021”; “site:github.com/openai/math ExecCNFNodeSearchCosts CookLevin Lean”. Primary originals Cook–Reckhow (1979) [1], Haken (1985) [2], Gocht–Nordström (2021) [3]. An authenticated OpenAI GitHub code search found and **fully read** openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean (blob 1ced21f44ad49370d1b812e862c03c3a91d7f836); it proves costs for one specified computation, not a mixed-calculus proof compiler. Direct Google-branded search was unavailable; indexed web search was used instead. Container DNS blocked raw GitHub downloads. The full CANON2 checker was read through the GitHub connector, but **not directly executed** in the local container; independent local Python/JavaScript checkers match the specific stated guards.

## ITERATE: exact proved restricted statement

Fix the original source-explicit unit-weight R_mix341 semantic calculus with signed source leaves, strict binary RES, exact AND3 on at most three original coordinates, binary GF(2) addition of authenticated affine rows, paid one-parent LOCAL conversions justified by complete local truth tables, and paid conservative two-input fresh DEF. Shared DAG nodes are counted once. Let π be **any finite already valid, typed, source-authenticated refutation** with q paid nodes and E encoded bits, in which (i) every non-AND3 rule is already expressed in the proposed CANON2R byte grammar, (ii) an AND3 input may be a valid, separately named affine view of an earlier node, (iii) its original union of support contains at most three original variables, and (iv) its output is an exact truth table.

**Theorem (affine-input normalization).** There exists an effective, exact-original-source-preserving proof-to-proof transformation T on this restricted fragment satisfying

$$
q(T(\pi))=q+u\leq 2q,
$$

where u is the number of **distinct consumed affine producing views** converted, and with a sparse certificate bit bound

$$
E(T(\pi))=O\bigl(E+q(N+\log(q+2))\bigr)
$$

for N bits of original encoded source. Every original step's Boolean condition, source ID, final contradiction and topological dependencies are preserved after explicit node-index remapping. The target uses only already available, paid native LOCAL and AND3 operations; no additional inference rule or unchecked semantic proof is introduced. This is **not** a bound polynomial in N alone.

**Proof.** For any exact authenticated affine parent with equation

$$
L_{S,b}(x)=[\bigoplus_{v\in S}x_v=b],\qquad S\subseteq X,\ |S|\leq 3,
$$

construct a truth-table factor on sorted support S, with the entry on assignment a equal to 1 exactly when L holds. The factor is **globally equal** to the affine row, not merely equivalent relative to the original formula's models. Therefore the one-parent LOCAL implication check succeeds in all at most eight rows. Charge this as one new node. In every AND3 consumer, replace the original affine edge with that factor edge. The conjunction's complete truth vector is unchanged because the substituted operand agrees on every assignment, and the union of original supports remains at most three. Cache one adapter per distinct named affine view and reuse it across all downstream consumers, including reconvergent/shared DAGs. Each affine view is produced by at most one original paid node, so u≤q. Translate every remaining parent pointer by a topologically constructed old-to-new ID table, retaining source IDs and exact external raw source bytes. The final contradiction is unaltered. Every adapter encodes at most three original identifier strings, eight truth bits and one pointer, with sparse coordinate lengths bounded by O(N+log(q+2)); old index remappings add at most O(E+q log(q+2)) bits. This proves the claimed overhead and deterministic polynomial construction time in N+E+q. □

**Native-grammar qualification:** The original /341 words “two conditions” do not specify all exact accepted-byte input kinds. The five-node example is legal under the natural original semantic reading accepting affine *conditions* as AND3 inputs; it is an unequivocal counterexample to **direct** CANON2 representation, not a refutation of all polynomial translations. The paid LOCAL adapter is a positive restricted repair. All historical LOCAL circuit-output/private-wire/exported-gate payloads and arbitrary native source formats remain unresolved. Requiring every other step to be pretyped is a genuine restriction.

## Falsifier witness: direct rejection, then paid normalization

Raw original signed DIMACS consists of these exact 45 bytes, preserved under both derivations:

    p cnf 3 5
    1 2 0
    1 -2 0
    -2 3 0
    -2 -3 0
    -1 2 0

SHA-256: 622b3d93553d3d22c51aee12c04b5b2861372d0173838c7e5509c829fcde10d7. Let x=1,y=2,z=3. Node 0, paid AND3 from source clauses 0 and 1, gives x=1 as authenticated row; node 1, paid AND3 from clauses 2 and 3, gives y=0; node 2, paid GF2 from 0 and 1, gives x XOR y=1; node 3, paid AND3 from source clauses 1 and 4, gives x XOR y=0 as a factor. Node 4, paid original-semantic AND3, combines node 2's **GF2-derived affine** with node 3's factor and concludes the everywhere-false factor. Five paid nodes, all ancestors of the terminal contradiction, zero source satisfying assignments.

Direct CANON2 type-checking rejects the affine parent at node 4. The new compiler inserts paid LOCAL from node 2's affine to an exact odd-parity truth table, new node 4, then a CANON2-legal AND3 with node 3 as new node 5, producing the same false factor. Six paid nodes, all active. Removing source clause 4 gives two satisfying assignments, a matched SAT control. q=5 and q=6 are **upper certificate lengths**, not certified minima. Ordinary Resolution admits shorter refutations of this source, so it is not a hard-instance claim.

## Executable checks and physical resources

Role-owned code: experiments/arc/lspv3_423_compiler.py and experiments/arc/lspv3_423_independent.js. Complete raw original and transformed traces: results/raw/arc/2026-11-05_0624_LSPV3_AFFINE_PARENT_ADAPTER423_raw.json. The original independent Python producer and alternate no-import JavaScript checker are also retained in the local reproducibility archive. The independent original JS checked **65,893 assertions**, including 65,536 exact Boolean comparisons covering all 16 three-input affine relations against all 256 three-input factor conditions over eight valuations; the uploaded independent checker is a compact, separately replayable version of the same tests. Both reject source substitutions, false GF2 sums, wrong AND3 factor, false LOCAL implication and unavailable ports. No random seed, no heuristic extrapolation. An independent source equality comparison, not self-hashing alone, authenticates the raw input. This is finite computational support for the symbolic theorem.

The node count q does not equal computer runtime or evidence bits. The compiler pays for reading/parsing E, source/header authentication, all named parent references, Boolean row computation, adapters, source/output serialization, cache construction, strict checker replay and all-phase peak storage; it is polynomial in actual supplied evidence N+E+q, **not** in N+q independently of E. No native machine time/space bound, optimizer runtime bound or FLMV lower bound is claimed. Any materialized child-space envelope must retain all-phase rho, s'≤max{rho,eta,lambda,lambda*s}.

## Published lower-bound controls, B3 and next gap

Haken's theorem [2] gives an exponential lower bound for every ordinary shared-DAG Resolution refutation of the explicit polynomially encoded PHP family (number of pigeons as hardness parameter). Its rules exclude GF2, DEF/ER and arbitrary machines. Cook's Extended Resolution PHP upper proofs and native mixed-system odd Tseitin affine shortcuts block any mistaken transfer from ordinary Resolution or Res(XOR) hardness to unrestricted SAT algorithms. Gocht–Nordström [3] supplies compact parity certificates in a **different** pseudo-Boolean system. None of these yields the same-fixed-R bridge.

The independent noncircular implication remains **OPEN**:

$$
\mathrm{SAT}\in\mathrm P\ \Longrightarrow\ 
\exists C,k\ \forall N:\ \overline W_{R_{\mathrm{mix341}}}(N)\le C(N+1)^k.
$$

This proof-to-proof adapter assumes an already supplied valid certificate; it does not imply that every UNSAT input has a short native certificate. A decider-specific polynomial proof system under SAT in P would still require a noncircular polynomial size-only simulation into this SAME R, without presuming polynomial machine-correctness proofs. B1, B2, B3 and P versus NP remain OPEN.

**Next step:** audit exact original LOCAL-CONVERT circuit-output and exported-wire consumer semantics, including private-wire naming and paid gate counting, against the proposed CANON2R grammar. Find a first original-legal counterexample or a polynomially charged grammar completion, and separately pursue the same-R size-only B3 transfer.

## Source and publication safety

Root main.tex was read via authenticated GitHub blob a088a5cd08355c78ee369688f659c0e20838fdf8 and returned **0 bytes despite a nonempty SHA**. No owner-only safe reconciliation can be authenticated; it was not overwritten. All other roles' documents, existing weights, agent identities, task schedules and enabled states were left untouched. This role's report, runnable code, raw records and coordination handoff are append-only.

## References

[1] Cook, S. A., and Reckhow, R. A. (1979), *The Relative Efficiency of Propositional Proof Systems*. Journal of Symbolic Logic 44(1), 36–50. DOI 10.2307/2273702.

[2] Haken, A. (1985), *The Intractability of Resolution*. Theoretical Computer Science 39, 297–308.

[3] Gocht, S., and Nordström, J. (2021), *Certifying Parity Reasoning Efficiently Using Pseudo-Boolean Proofs*. AAAI 35(5), 3768–3777. DOI 10.1609/aaai.v35i5.16494.
