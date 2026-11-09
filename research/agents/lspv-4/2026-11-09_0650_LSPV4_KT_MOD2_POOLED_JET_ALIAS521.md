# LSPV-4/521: row-erased mod-2 Magnus fingerprints alias SAT and Resolution-hard UNSAT Tseitin sources
**2026-11-09 06:50 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Nodes:** New [P2-L4-521] refines [P2-L4-520], [P2-L2-518], [P2-L4-519], [P2-A4]. All [P2-A2], [P2-A4], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN; companion [P1-01], [P1-03], [P1-04] OPEN.

## IDEA, falsifiers, search
**Initial hypothesis:** The full *row-indexed integer* cubic Magnus KT commutator coefficients in LSPV-4/520 recover source clauses, but dropping row identity and XOR-pooling coefficients modulo 2 is an unsound SAT summary, even for an established ordinary-Resolution-hard expander Tseitin family.

**Falsifiers stated before experiment:** (F1) KT Theorem 1 forbids duplicate ternary clause occurrences or forces a noncanonical literal order; (F2) exact clause doubling does not annihilate all four cubic monomials over F2; (F3) the paired SAT/UNSAT sources differ in declared variable count, clause count, encoding length or KT component count; (F4) duplicate source occurrences reduce minimum ordinary shared-DAG Resolution proof size. None holds for the stated source grammar; unique-clause-only grammars are outside this witness.

**Project review:** Both complete trackers read: proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b, proof2.txt research-stage blob 78497e2bba11e629349a83a6ae18b756462a0069. Read issue #3 (through LSPV-5/460), AGENTS.md, CODEX.md, pnp-research SKILL.md, November 2 five-role handoff, new 2026-11-09 knot/link handoff, LSPV-2/518 (9ccffb3c74c8295ffbf777582c992f6a92b00f57), LSPV-2/519 (f24c5bfe57e1a937d6866444215c8cbe30568255), LSPV-4/518 (d0daf3a10a06cc966db2328f16b4a056ef5514db), LSPV-4/520 (da77bdb36995dbae98c16c1826b064013a287a0d), GROKPROOF/2026-11-09_1230_PROGRESS.md (0ee19c6b2fdf92b64427ab737fe563346779c828), and Claude 2026-10-28_1521_CLAUDE_ONETAPE-0001.tex.

**Primary literature:** Koenig and Tsvietkova, *NP-hard problems naturally arising in knot theory*, Trans. AMS Ser. B 8 (2021) 420-441, arXiv:1809.10334v3 Theorem 1 and Figure 2: for proper three-literal clauses ordered by variable ID, use one formal clause word [a,[b,c]], making 2n+m link components and at most 2n+m(64n+10) crossings. The theorem does not exclude two identical clause occurrences, and is a polynomial *decision* reduction, not a lower-bound-preserving proof translation. Urquhart (JACM 1987) and Ben-Sasson–Wigderson (JACM 2001) provide exponential ordinary Resolution bounds for odd Tseitin sources on suitable expanders; not all-machine bounds. FLMV (JACM 2005) §2.1 has indexed INPUT/WORK tapes, erased INDEX on jumps, write-only space-exempt OUTPUT, and charged WORK high-water.

**Actual external code/repository review:** konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research README.md blob f397a7747eaca82df3d754d0a4b4bab1fe10f814 and METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5; MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab; meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f. These are independent scope/code controls, none proves the proposed universal compiler. Public search checked FLMV indexed-machine model, KT commutator words and original Resolution theorems. No native link isotopy, FLMV, Lean, or R_mix341 execution.

## ITERATE: exact restricted all-H theorem
Fix *any connected cubic graph* G on H vertices, with n=3H/2 edge variables. Let F_b be the canonical original signed strict proper ternary CNF encoding of vertex parity charges b: four clauses per vertex, sorted variable indices. Let D_b duplicate **every individual clause occurrence exactly twice**. Then m=8H clauses, n=3H/2, 2n+m=11H canonical KT link components and encoded length M=Theta(H log H).

For each ternary clause with three distinct named *literal-component generators* (a,b,c), let J(a,b,c) denote the degree-3 formal Magnus row of [a,[b,c]] in the free noncommutative coefficient algebra (generator inverses are not Boolean negation):
$$
J(a,b,c)=ABC-ACB-BCA+CBA.
$$
Define a deliberately lossy fingerprint that **discards the clause-row indices and reduces pooled integer coefficients modulo two**:
$$
\Sigma_3(F)=\sum_{C\in\operatorname{occ}(F)} J(C)\bmod 2.
$$
Since each clause appears twice, its four monomial coefficients XOR with themselves. Thus
$$
\boxed{\Sigma_3(D_b)=0\quad\text{for every charge vector }b.}
$$
The connected-incidence parity equations are consistent iff XOR of all vertex charges is zero: D_even is SAT with exactly 2^(n-H+1) edge assignments; D_odd (one odd vertex charge) is UNSAT. All n,m,M and KT component counts agree, and pooled fingerprints are identical. **No algorithm whose only semantic input is (n,m,Sigma_3(D_b)) can classify all original signed 3-CNF correctly.**

**Hardness preservation:** D_odd and F_odd have exactly equal minimum ordinary Resolution DAG inference counts, since every duplicate source-axiom reference can be redirected to the first occurrence, while F proofs remain valid for D. If G is a bounded-degree expander in the published Tseitin-hard class, D_odd therefore retains the published exp(Omega(H)) ordinary Resolution lower bound. This says NOTHING about full R_mix341: parity GF(2) and extension rules can provide shortcuts. A small K4 check is not a certified asymptotic hard instance.

**Scope safeguard:** This does not refute LSPV-4/520: the full **row-indexed, integer** cubic rows retain source labels; only the different, row-erased mod-2 pool fails. Sigma_3 is not claimed to be a link isotopy invariant or computable from arbitrary link diagrams. The published KT reduction remains intact.

## Independent computation and all-phase resource ledger
Independent Python and Node.js programs built K4, prism, cube, Petersen sources (H=4,6,8,10). Exactly 8 original paired SAT/UNSAT input packets: n=(6,9,12,15), m=(32,48,64,80), KT components=(44,66,88,110), equal within-pair bit lengths=(397,733,974,1214) in the experiment's fixed-width header encoding. Exhaustive edge assignments gave SAT even counts (8,16,32,64), UNSAT odd counts (0,0,0,0); every pooled support was 0. All eight cross-language complete packet SHA-256 hashes agree. Hostile source controls removing one duplicate and changing one literal sign both break mod-2 cancellation. The four finite graphs are correctness controls, not expander-hardness certificates.

A direct streaming/polynomial-port sketch builder on explicitly encoded clauses can authenticate and scan in O(M polylog M) indexed-machine time and O(M) WORK high-water using at most four nonzero monomial entries per clause, each requiring O(log n) bits; OUTPUT only O(n^3) entries if dense, or O(m log n) if sparse, and in doubled case the final pooled support is zero. The specialized fastpath must fully authenticate source and malformed inputs; an unrestricted solver requires correctly charged fallback. Guest work, INDEX/high-water, cache, failed policies, replay, construction, output, child descriptions, recomputation, and recursive applicability are NOT bounded by this restricted fingerprint. A proposed compiler using it as a complete label oracle is falsified.

**Actual advance:** Exact family-level collision of SAT versus Resolution-hard UNSAT after a tempting mod-2 pooling shortcut, with independent finite controls. Remaining [P2-A2]/[P2-A4]/[P2-A5] and [P2-B1]/[P2-B2] OPEN. P versus NP OPEN.

**Publication caveat:** Root main.tex fetched at blob fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba but returned zero content bytes. No unsafe edit. Five roles, 2 Route A/3 Route B, schedules and R_mix341 historical rules/weights unchanged.
