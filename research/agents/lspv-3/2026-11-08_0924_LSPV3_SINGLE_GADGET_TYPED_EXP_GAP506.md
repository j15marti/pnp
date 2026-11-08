# LSPV-3/506: a one-clause gadget separates two source-authenticated mixed proof grammars exponentially

**2026-11-08 09:24 PST | Route B | PROVED/RESTRICTED model-comparison theorem + COMPUTATIONAL finite evidence | P versus NP OPEN.**

**Affected tracker IDs:** new [P2-L3-506], refining [P2-D1], [P2-C3], [P2-D3], [P2-F13], with prerequisites [P2-L3-503], [P2-L3-504], [P2-L3-505] and cross-check [P2-L5-436]. Historical [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. Companion [P1-01], [P1-03], [P1-04] unchanged.

## IDEA and four falsifiers

Hypothesis: replacing only ONE clause of an existing ordinary-Resolution-hard odd-charge cubic-expander Tseitin strict-3CNF family reveals an exponential difference between two sound, complete, unit-weight binary-premise *distinct* grammars that both agree with the old recovered SOURCE/AND3/XOR certificates. The decisive difference is whether a RES-derived clause may serve as an AND3 factor parent.

Falsifiers fixed before searches: (1) a legal RES-to-AND3 edge in the tagged grammar; (2) an independent factor/XOR refutation after the gadget replacement; (3) loss of the ordinary-Resolution lower bound under the gadget substitution; (4) accidental identification of a proposed grammar with the complete historical accepted bytes, DEF or LOCAL-CONVERT. Falsifier (1) is ruled out by the explicit tagged definition, NOT historical authentication; (2) is the independently scoped previous LSPV-3/505 core obstruction; (3) follows from /504 and independent LSPV-5/436 source retraction; (4) remains a historical OPEN obligation.

## SEARCH: actual sources, continuity, assumptions

Read both complete initial main trackers: proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b (18,553 chars) and proof2.txt blob 8f16ca0b2fda81b05ff4ca3d82c68dcb1e801183 (457,804 chars); current coordination issue #3 including peer LSPV-1/509 and LSPV-5/437; governing historical five-role handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md at 4e29ed7646f484707767acb6e63ec5f38afd98a8; AGENTS.md; CODEX.md; .codex/skills/pnp-research/SKILL.md; original 341 grammar declaration research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex (blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb). Compared actual LSPV-3/505 report (blob 04a339fa37479131da2e18ebc13000bb29427d7c), original /505 closure executable (blob 3af7b71fbe78b6a9f7b579928dbe9d20bd55fa14), LSPV-1/509 report (blob 53a6a24625d2a2163e7493136399e2e0319558ee), LSPV-5/437 report (blob 2a40ba660c1bf7bef26b628fa8c6f74932815873), actual GROKPROOF/2026-11-08_1130_PROGRESS.md (blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70) and research/agents/claude/world-ledger/README.md (blob de75a371ce3143a4495e6892df7fb04794a6b708). Grok/Claude are assessments, not historical-rule authorities.

Primary hardness references: Urquhart, Hard Examples for Resolution, JACM 34(1) (1987), DOI 10.1145/7531.8928; Ben-Sasson and Wigderson, Short Proofs Are Narrow, JACM 48(2) (2001), DOI 10.1145/375827.375835, original preprint https://eccc.weizmann.ac.il/eccc-reports/1999/TR99-022/index.html. Their expander lower bounds concern ORDINARY shared-DAG Resolution, not mixed-calculus or all-machine SAT hardness. Haken ordinary-DAG PHP, Cook ER, and Tseitin GF(2) shortcuts remain mandatory adverse controls. Peitl and Szeider (2021) shortest Resolution proofs: https://doi.org/10.24963/ijcai.2021/657.

Change-aware external-file review: konard/p-vs-np/README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research/README.md blob f397a7747eaca82df3d754d0a4b4bab1fe10f814 and METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5. Also inspected meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f; tanyongkiam/cake_lpr/README.md blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c (November 1, 2026 planned final release); peitl/short-proof/README.md blob 93d2090dba9739bc4983c65ea639a24e1f5e0fab; berkeley-abc/abc/README.md blob 88a9d1a316dd9751acade746de315fd1e6e6c362; lsils/mockturtle/README.md blob c1d2b0c4728d923dc7f4ac2b6759994dbaba4c1b; openai/math/README.md blob cc5b0a03bca6c742f045d683b6647a6f44ef2cae. None supplies native 341 RES-to-AND3 bytes. A separate Google-branded client, formal checker compilation and source-independent native 341 replay were unavailable/not performed.

## ITERATE: theorem with exact separate systems

Let G_h be a family of connected simple bridgeless cubic edge expanders and let b have odd charge. Original T_h has 3h/2 edge variables and 4h proper width-three clauses. Select one clause C=(a OR b OR c), where the three are signed original literals, and replace it by fresh-u,v clauses:

$$
A=(a\lor b\lor u),\qquad
B=(\neg u\lor c\lor v),\qquad
D=(\neg u\lor c\lor\neg v).
$$

The resulting source H_h has 4h+2 strict-3CNF clauses and 3h/2+2 variables, with N=Theta(h log h) DIMACS bits. Equisatisfiability follows from existentially eliminating u,v. STRONGER: the literal substitution sigma(u)=c, sigma(v)=0 maps A to C and B,D to tautologies, and earlier [P2-L3-504]/[P2-L5-436] proved the nonexpansive original-source shared Resolution proof backtranslation:

$$
S_{\mathrm{Res}}(T_h)\le S_{\mathrm{Res}}(H_h).
$$

Consequently S_Res(H_h) >= 2^{Omega(h)} on the established expander family.

Define two DIFFERENT sound, complete, effective, source-indexed, unit-weight proof calculi, with at most two inference premises, legal global sharing, source checks and RES completeness:

1. **R_TAG506.** SOURCE clauses are both clauses and local factors. RES takes only SOURCE/RES clause parents, yielding clauses. AND3 takes only SOURCE/AND3 factor parents, retains declared union support of size at most three, and computes exact conjunction. An exact-affine AND3 factor can carry a GF(2) row, and XOR combines two earlier rows. No RES-derived clause is a factor parent; no GF(2)-to-clause conversion, DEF, LOCAL-CONVERT, weakening, splitting or discharge is included.
2. **R_EXT506.** Identical rules, but RES outputs may ALSO serve as AND3 factor parents at no separate node cost. This is an *explicit alternative grammar policy*, not an attribution to the historical system.

Both systems accept the same SOURCE/AND3/XOR-only original cubic-Tseitin witness, and both have exact minimum 4h-1 on the **unexpanded** T_h by the essential-source binary-fan-in lower bound and matching 3h AND3 + (h-1) XOR proof.

**Theorem 506.1 (PROVED/RESTRICTED, system comparison):**

$$
\boxed{W_{R_{\mathrm{TAG506}}}(H_h)=S_{\mathrm{Res}}(H_h)\ge 2^{\Omega(h)},}
$$

$$
\boxed{W_{R_{\mathrm{EXT506}}}(H_h)=4h+1.}
$$

*Proof.* The /505 exact-support factor closure with at least one gadget has no false factor and no XOR contradiction: A and the B/D pair cannot cross their >=4-variable declared support union, B/D yield no exact nontrivial affine row, and the surviving untouched vertex-parity equations are linearly independent. Thus every TAG506 refutation ends in a SOURCE/RES-only ordinary Resolution derivation, and its minimum equals ordinary Resolution size. For EXT506 use two paid RES inferences, first B with D on pivot v to yield (not u OR c), then with A on pivot u to recover C. Reconstruct the full four-clause parity relation at each vertex with 3h paid AND3 and sum h equations with h-1 paid XOR. The total is 2+3h+(h-1)=4h+1. All 4h+2 original expanded sources are individually indispensable by prior /504 clause-deletion witness lifting. Any sound binary-premise shared refutation charging one per derived node requires at least (4h+2)-1 nodes; equality follows. End proof.

**CRITICAL MODEL BOUNDARY:** These are TWO SEPARATE sound complete audit calculi, not verified completions of full historical R_mix341. Their proof-cost gap cannot be asserted for historical RES/DEF/LOCAL-CONVERT, exported/private wires, or branch discharge. It illustrates why [P2-D1] must authenticate cross-type native accepted bytes. No unrestricted lower bound on SAT algorithms or B3 is obtained.

## Exact experimental evidence and limitations

The committed JavaScript constructor at experiments/arc/lspv3_506_tagged_vs_extensional_gap.cjs (blob 94f5ced735eb80a698b72b7f6ca8456dcf655660) was executed in a V8 isolate, yielding **1,599 passing assertions** over nine actual original-source cases on K4, K3,3, and cube with k=0/1/2 replacement clauses. Each local RES pivot, 8-row factor truth table, affine annotation, global XOR contradiction, unique source ID and source mutation control was checked. The paid totals are K4 (15,17,19), K3,3 (23,25,27), cube (31,33,35) for k=0/1/2. Odd-UNSAT claims were checked by complete finite assignments for these cases. For k>0, the constructed proof crosses a RES-to-AND3 typed edge that TAG506 rejects.

Raw typed proofs and data: results/raw/arc/2026-11-08_0924_LSPV3_506_TAGGED_EXTENSION_GAP_RAW.json (blob e89406b0b37f185b25ca79f4f9ccd4a0638851b0). A **separately authored** verification routine refetched the published K4 k=1 packet and recomputed all 17 inferences, source-model count zero and illegal TAG crossing; 168 assertions passed. Raw: results/raw/arc/2026-11-08_0924_LSPV3_506_INDEPENDENT_K4_REPLAY_RAW.json (blob c503da7853beec31acd46c9cbb954522efc17625). The published standalone Node CLI was NOT independently run; the historical 341 verifier was NOT run on new RES certificates. These experiments are finite controls, not an asymptotic hardness proof.

## Resource and sharing ledger

For k=1 the EXT506 certificate uses 2 RES, 3h AND3 and h-1 XOR distinct paid nodes, with global DAG sharing allowed and any distinct inference charged once. Critical-path weighted binary depth is O(log h) under unlimited parallelism. A compact source and proof-ID representation takes O(h log h) bits; materializing O(h) dense XOR masks of length O(h) may raise the full evidence payload and simultaneous peak storage to O(h^2) bits. Construction, parsing, source/index reads, output, verification, references, storage, failed search, and conversions are distinct machine operations with polynomial upper bounds for this explicit generator, not free because logical nodes are unit-paid. No time-space FLMV claim is made. On TAG506 the *proof* has exponential minimal Resolution nodes, but a separate SAT decider may exploit parity or structure in polynomial time.

## Publication/handoff and remaining obligations

Added experimental code, raw packets, independent-replay result and a five-role handoff. The complete previous proof trackers must be reviewed before any write; only the material evidence [P2-L3-506] should be appended to proof2, preserving proof1 and older text. No historical grammar, weight, agent, title, schedule, enabled state, or allocation changes are authorized. The decisive next experiment is an **actual authenticated historical** RES-derived parent accepted by AND3 (or proof of no such rule), plus any mandatory paid conversion, with original source binding and certified checker acceptance.

[P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. **P versus NP remains OPEN.**
