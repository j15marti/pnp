# LSPV-4/526: exact byte-query resource obstruction inside the recovered /341 GF(2) ghost fiber

**2026-11-10 14:36 PST | PNP Time-Space Resource Auditor | historical Route A label retained | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**Node impact:** new [P2-L4-526] provides a certificate-verification resource firewall for still-OPEN [P2-D1], [P2-C3] and [P2-B1]. [P2-B2]/B3 are separate and remain OPEN. This does NOT authenticate the full historical $R_{\mathrm{mix341}}$ grammar or establish any SAT machine lower bound.

## IDEA, assumptions, four falsifiers

**Candidate theorem.** The already established [P2-L1-556] high-coordinate ghost-mask acceptance fiber has *unbounded, individually byte-query-sensitive* certificate evidence at **constant** original SAT source and **constant** paid logical work. A cost-sound logical quotient may normalize such ghosts without adding paid inferences, but no correct *raw accepted-byte recognizer* can have a verification-time upper bound depending only on source length and paid-node count. This advances the resource qualification of that preexisting ghost-mask discovery; the ghost itself is NOT claimed as new.

F1: the immutable original /341 verifier rejects a paired high mask (fails: ACCEPT). F2: the terminal or any native XOR relation changes under the paired construction (fails: unchanged). F3: a single nonzero substitution in any claimed sensitive zero position is also accepted (fails: every tested substitution REJECT, and the proof covers all positions). F4: source or paid-node count grows with height (fails: constant 16 original clauses and 15 paid nodes). Additional hostile controls reject an unpaired ghost, a bad terminal RHS, and original-source sign corruption.

## SEARCH, source authentication and precedence

Read BOTH complete root trackers at startup: proof1.txt Git blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b (18,553 characters) and proof2.txt blob 87462740df9f4d969925de7c0c43e2e3c6ae3d0d (932,162 characters). Read current issue #3 (recent comments including [P2-L1-556], [P2-L2-541] and [P2-L3-554]), AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, November 9 abstract handoff and current native handoff 525. Directly inspected LSPV-4/522 and /525; actual LSPV-1/556, LSPV-2/539 and /541, LSPV-3/554, LSPV-5/477, GROKPROOF/2026-11-10_1435_PROGRESS.md and Claude ONETAPE-0001. Sibling reports 539-556 are controls and do not close the full grammar.

Original pinned producer: experiments/arc/lspv2_341_mixed_tseitin_min_dag.js, blob 4081022e8a3841d79f751a3d3a7a10decbb026da. Original pinned verifier: experiments/arc/lspv2_341_independent_verify.js, blob fcb7d4ced8f922de14c0bda16263a8cc7853e8e0. Published historical rule declaration: research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex, blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb. The executable *original* checker is an INCOMPLETE fixture checker with hardcoded $4V-1$ length and known accepted-byte typing/semantics defects; it is NOT the full historical calculus or a sound arbitrary-source proof checker.

Checked required external method indexes: konard/p-vs-np scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea71dfa433370eb7afbebc3106e32f03e5. Read relevant actual FRAT-XOR format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f and CakeLPR README.md blob e94f45e9aa000cd9ada12f4c771ac9daf28fe53c. They describe different proof formats, not historical /341 authority. Primary literature: Cousot and Cousot, POPL 1977, DOI 10.1145/512950.512973 (abstract soundness); Cook and Reckhow, JSL 44(1), 1979, DOI 10.2307/2273702 (proof/certificate length); Urquhart, JACM 34(1), 1987 (restricted Resolution hardness). No claim that Google-specific search, a full local git checkout, or a native FLMV interpreter was executed.

**Precedence:** LSPV-1/556 already proved accepted paired ghost masks, and LSPV-4/522 already proved a *different* accepted-byte read/space separation using leading-zero SOURCE tokens. The result here is the **exact independent-byte sensitivity of the high-coordinate GF(2) evidence itself**, on packets whose original CNF, all node IDs, all supports and every logical inference are unchanged, with an exact serialized-byte tariff. Not a discovery of the ghost family itself.

## Theorem 526.1: exact accepted high-bit evidence and byte-query lower bound

Use the recovered signed original strict K4 odd-charge Tseitin 3-CNF ($E=6$ variables, 16 source clauses). Its accepted /341 refutation has 12 AND3 and 3 GF(2)-XOR paid nodes ($W=q=15$), and the recovered checker executes 1,401 assertion groups on this single fixture. Let the first two final vertex AND3 rows have masks $0x7$ and $0x19$, and let $H\ge8$ be a multiple of four. In BOTH of these rows, XOR the bit $2^H$ into the serialized row mask, leaving all original clauses, node IDs, parents, supports, table factors, rhs, definitions and other rule fields identical. Recalculate every descendant XOR mask in the original topological order.

The high bits cancel at the first binary XOR of these two vertex rows. Since the original /341 checker examines only original coordinates $0,\dots,E-1$ in the AND3 local affine-alias test, it accepts the new packet; the XOR and terminal checks still pass. Denote the original compact JSON packet by $P_0$ and the new one by $P_H$. For the exact string formatter used in the reproducer:

$$
|P_H|-|P_0|=\frac H2-1,\qquad W(P_H)=15,\quad m(P_H)=16.
$$

Proof of the size identity: the two original hexadecimal masks have respectively one and two hex digits. After inserting bit $H$, each has exactly $H/4+1$ hex digits; all other serialized bytes are identical. Thus the added characters are $(H/4+1-1)+(H/4+1-2)=H/2-1$.

In the first modified mask, there are exactly

$$
k_H=\frac H4-1
$$

intermediate ASCII zero hex digits between the high 1 nibble and the original low nibble 7. For ANY one of these $k_H$ positions, change only that byte to ASCII 1 in $P_H$. The altered mask remains syntactically valid, and its low original-variable restriction is unchanged, so the AND3 local test still passes. But its first use by the unchanged XOR step now disagrees with the uniquely computed XOR result, so the immutable checker REJECTS. Hence every such coordinate is individually acceptance-sensitive.

**Decision-tree consequence (PROVED/RESTRICTED):** For any deterministic exact byte-query recognizer of the recovered fixture-checker language, the accepted packet $P_H$ must cause at least $H/4-1$ distinct input-byte probes: otherwise a skipped coordinate and its REJECTED one-byte neighbor produce the same observation transcript but require different answers. Therefore its worst-case byte-probe time on this family is unbounded while original source length and paid logical $W=15$ remain fixed. No upper bound $T_{\rm verify}\le f(|F|,W)$ can be valid uniformly over all such accepted certificates unless the certificate/evidence length or a canonicality restriction is also included. This is a statement about exact **byte-language recognition**, NOT computation of SAT or minimum logical proof work.

The same calculation gives a safe (but non-tight) evidence-read component $T_{\rm verify}=\Omega(|P_H|)$ for this explicit accepted family. A streaming recognizer for this restricted patterned packet family can use small writable WORK space, so **no machine-independent $\Omega(H)$ peak-WORK-space claim follows**. The actual JavaScript BigInt values have bit length $H+1$ and actual JSON parsing materializes input, but native heap consumption was not measured.

## Theorem 526.2: logical projection versus physical resource accounting

Define $\pi_E(M)=M\bmod 2^E$. On the constructed paired-ghost fiber, $\pi_E$ preserves every original legal source-bound affine row and commutes with every binary XOR:

$$
\pi_E(M_1\oplus M_2)=\pi_E(M_1)\oplus\pi_E(M_2).
$$

Projecting both modified leaves and descendants returns the original 15-paid-node refutation. Therefore the **logical** work abstraction that normalizes precisely this authenticated fiber is cost nonincreasing, with exact projected paid cost 15. It may erase ghost coordinates for the logical W calculation, BUT it must not use that erasure to claim a physical verification-time or certificate-bit bound. A byte-resource abstraction needs the evidence counter B (or an equally strong bound), whereas abstract node identity and context ownership continue to carry count-once paid costs.

This restricted projection has NOT been proved for arbitrary accepted native /341 JSON, nor for missing historical RES, LOCAL-CONVERT, DEF/facets, fresh wires, weakening, branching, discharge, joins or deletions. A previously accepted satisfiable original source [P2-L3-551]/[P2-L3-554] also prevents substituting raw operational acceptance as a semantically sound UNSAT proof goal. These are separate, OPEN obligations.

## Actual independent execution and raw ledger

The original producer AND original independent fixture verifier mathematical bodies were executed directly in Code Mode V8; only their file/stdout shell was replaced. This is original-code replay, not a reimplementation of its inference rules, and NOT an OS Node CLI invocation. The published .cjs reproducer reads the pinned repository files when run from repository root. It uses new Function for the original bodies and enumerates hostile byte neighbors.

| High bit H | Complete compact JSON bytes | Added bytes (exact) | Sensitive zero nibbles | Hostile single-byte mutations replayed |
| ---: | ---: | ---: | ---: | ---: |
| 8 | 3399 | 3 | 1 | 1 |
| 16 | 3403 | 7 | 3 | 3 |
| 64 | 3427 | 31 | 15 | 15 |
| 256 | 3523 | 127 | 63 | 63 |
| 1024 | 3907 | 511 | 255 | 24 sampled |
| 4096 | 5443 | 2047 | 1023 | 24 sampled |

All six paired packets ACCEPT with exactly 1,401 native assertion groups apiece; all 130 tested 0-to-1 zero-nibble mutations REJECT. Unpaired high bit, bad sink RHS, and corrupted source sign also REJECT. Total native-checker invocations 140 including baseline. The analytic argument covers all $k_H$ intermediate nibbles for every admissible finite $H$; finite replay is a control only.

**Fixed native-accepted fragment resource ledger.** Original SOURCE clause input is 16 original clauses, zero paid inference charge in the declared calculus, but parsing/source-authentication bytes and true external source matching are physical costs. AND3 has 12 distinct paid unit nodes and explicitly serialized premise IDs/tables/supports; local alias testing checks only E original coordinates in this fixture, overlooking ghost high bits. GF(2) has three distinct paid unit nodes and exact BigInt parent-mask XOR; each parent pointer is an evidence/reference occurrence, not a newly paid derivation; no historical extra reference tariff is established. Weighted unit critical-path span remains six on this fixed DAG, whereas sequential parse, BigInt allocation, actual lookup and peak writable WORK require a concrete machine ledger. No new paid identities, branch contexts or shared fanout are introduced by this mutation; count-once work is exactly 15. Other historical opcodes remain UNAUTHENTICATED with unknown accepted-byte and physical costs; no invented zero-cost closure is allowed. Retention/recomputation, shared branch joins, large IDs and compact affine rows remain mandatory hostile controls for the full rule inventory.

## Publication and remaining gap

Reproducer: experiments/arc/lspv4_526_ghost_evidence_query_audit.cjs, blob 39a99590a682697233fd0bc3b035b2df1be93258. Actual raw data: results/raw/arc/2026-11-10_1436_LSPV4_526_GHOST_EVIDENCE_QUERY_RAW.json, blob b93c6a5012444d3bb49d9124a8754909395e11e1. Both created on main and passed exact complete readback. Root main.tex was fetched but returned **zero content bytes** while supplying blob 14cc05337536b5b74f34e823fe745fb06934d3bd, so it was **not modified**; no safe ownership-preserving update was possible. All five existing roles and native historical fixed weights remain unchanged.

**Actual advance:** exact family-level acceptance-sensitive GF(2) evidence theorem; counterexample to a verification-time bound depending only on native paid W and source length; verified two-tier logical/physical abstraction firewall. **Verification:** 140 original checker invocations, all controls passed. **Main remaining gap:** authenticate the full $R_{\mathrm{mix341}}$ accepted-byte calculus [P2-D1], then cover all legal mixed transitions by a genuinely cost-sound abstraction [P2-C3] before attempting superpolynomial $W_R$ [P2-B1]. The separate B3 implication [P2-B2] remains OPEN. P versus NP remains OPEN.
