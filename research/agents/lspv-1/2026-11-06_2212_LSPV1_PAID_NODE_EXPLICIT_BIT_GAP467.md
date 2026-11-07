# LSPV-1/467: paid logical nodes versus explicit proof bits

**2026-11-06 22:12 PST | Route B | PROVED/RESTRICTED in a distinct artificial calculus, COMPUTATIONAL finite controls; P versus NP OPEN.**

## Hypothesis, falsifiers, idea -> search -> iterate
LSPV-1/466 [P2-B10] assumes a compact-witness condition CW before deriving polynomial construction from a polynomial paid-node bound under SAT in P. Test whether that condition follows from soundness, completeness and polynomial checking of EXPLICIT certificate bits alone. Falsifiers: (1) ordinary Resolution admits short bit certificates on the established expander Tseitin family; (2) assignment-enumeration certificates can be compressed under our defined byte grammar; (3) checker silently invokes a semantic oracle; (4) hybrid proofs evade the two specified proof types.

Read BOTH root trackers at main: proof1.txt blob 9273776e5ac0c9a4940b8c3e404d98ed5b205202 (17,530 characters), proof2.txt blob 67fc915249a6f2667b7d85feaedc7853b884ec86 (62,778 characters). Relevant [P1-01], [P1-03], [P1-X3], [P2-B10], [P2-B1], [P2-B2], [P2-D1], [P2-F2], [P2-L3-466], [P2-L5-403]. Read governing 2026-11-02 handoff, issue #3 and comments, AGENTS.md, CODEX.md, .codex skill, LSPV-1/466, LSPV-3/466, LSPV-5/403, GROKPROOF/2026-11-07_0620_PROGRESS.md, and research/agents/claude/world-ledger/README.md. The guessed LSPV-2/341 source path gave 404; no claim to have inspected that file.

Literature queries: Cook Reckhow 1979 polynomial bounded propositional proof systems, Urquhart 1987 Tseitin expander resolution lower bounds, Ben-Sasson Wigderson 1999/2001 width-size theorem, number of lines versus certificate bits. Primary references: Urquhart JACM 34 (1987) 209-219 DOI 10.1145/7531.8928; Ben-Sasson and Wigderson JACM 48 (2001) 149-169 DOI 10.1145/375827.375835; Cook and Reckhow JSL 44 (1979) 36-50 DOI 10.2307/2273702. Scoped project/published result, not new hardness. Actual external files read: konard/p-vs-np README SHA 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json SHA 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research README SHA f397a7747eaca82df3d754d0a4b4bab1fe10f814, METHOD_INDEX.md SHA 18d693ea71dfa433370eb7afbebc3106e32f03e5, REVIEW_ADDENDUM SHA 6a7cc2f8962d3fcfc1778b1d3d8f5dc8d56d70; meelgroup/frat-xor/format.md SHA 986a21aa92b62f844ef1fce852193142c41b2b1f; openai/math README SHA cc5b0a03bca6c742f045d683b6647a6f44ef2cae and CONTENTS.md SHA 7e1ed90ac5a666f1bbecb22027387c4ad79e9d03. No GitHub repository claimed to establish P vs NP. Public web search used, not a Google-specific interface.

## Fixed DISTINCT artificial rule system, NOT R_mix341
Define R_enum_or_res for each binary-encoded CNF F with n original variables. Accepted refutations have exactly ONE mutually exclusive proof tag.

RES: original-source authenticated ordinary Resolution DAG, each inference charged 1 and a mandatory final paid seal charged 1. Clauses, pivots, source IDs and references are explicit.

ENUM: exactly ONE paid terminal inference with 2^n lexicographically sorted, UNCOMPRESSED records. Each row explicitly writes all n assignment bits and the index of an ORIGINAL source clause falsified by that assignment. The checker confirms every row, original clause and order; malformed input/references are rejected. Work cost is 1, regardless of the full written payload. Neither tag can mix inferences from the other.

This is a deliberate **foreign** proof calculus with a globally powerful ENUM rule. It violates the desired native/local rule restriction of R_mix341 and must NEVER be silently inserted into it. It is a falsifier of an unrestricted node->bit inference, not a candidate proof of all-algorithm hardness.

Soundness: RES is sound; ENUM lists every assignment, and each falsifies an original clause. Completeness: UNSAT F admits an ENUM list, and ordinary Resolution is complete. Explicit checker cost is O(2^n n |F|) for ENUM, polynomial in |F|+|pi| because the certificate has at least n2^n explicit bits. Both tags have a required charged terminal, hence for ALL UNSAT F:
$$
W_{R_{\mathrm{enum\lor res}}}(F)=1.
$$

## Published strict 3-CNF family, theorem and proof
Use an established Urquhart expander-based odd-charge cubic Tseitin family. At h graph vertices there are n=3h/2 edge variables, four original proper signed width-three clauses per vertex, m=4h, encoded N=Theta(h log h) bits for consecutive binary IDs. Each vertex's four clauses exclude its four wrong-parity local assignments. Odd total charge makes the system UNSAT since each edge occurs twice in the parity sum. No non-3CNF encoding or lower-bound-preservation conversion is required. Urquhart and Ben-Sasson/Wigderson establish S_RES(F_h)>=2^{c h} for suitable expander graphs, ordinary shared-DAG Resolution, not mixed rules.

**Theorem 467.1 (PROVED/RESTRICTED in this other calculus):**
$$
W_{R_{\mathrm{enum\lor res}}}(F_h)=1,\qquad
\min_{\pi:\,\pi\text{ refutes }F_h}|\operatorname{encode}(\pi)|
\ge\min(2^{c h},(3h/2)2^{3h/2})
=2^{\Omega(h)}=2^{\Omega(N/\log N)}.
$$
Proof: Every certificate is RES or ENUM, never a hybrid. The published RES bound forces exponentially many explicit lines (even with shared DAGs). The ENUM grammar forces n2^n literal assignment bits. The minimum of these two exponential lower bounds is exponential. An ENUM certificate exists with one charged terminal node. QED. This is a **certificate-bit** bound only in the distinct calculus, NOT a native R_mix341 lower bound, B1/B2/B3 proof, or arbitrary SAT lower bound.

## Finite original-source verification
Odd cubic Tseitin original signed 3CNF K4: 16 clauses/6 variables, 64 ENUM rows, 4,720 certificate bits; K3,3: 24 clauses/9 variables, 512 rows, 50,048 bits; cube: 32 clauses/12 variables, 4,096 rows, 498,688 bits. Every odd formula UNSAT by complete enumeration; corresponding even-charge sources SAT. Removing each original clause produces SAT. Python producer 105 assertions, independent JS 96 assertions, ALL source and certificate SHA256 hashes equal. 18 corrupted rows/certificates rejected across the 3 examples, covering truncation, repeated/misordered row, invalid/falsely-satisfied source pointer. These finite graphs are **not** claimed to have individually published asymptotic hardness. Executed code: experiments/arc/lspv1_467_bitwork_independent.cjs (published) and local full Python producer; raw results results/raw/arc/2026-11-06_2212_LSPV1_467_BITWORK.json. This is not an execution of historical accepted-byte checker.

## Resource accounting / revision
ENUM logical minimum one paid distinct node; explicit evidence Omega(n2^n) bits, materialization/output exponential and checking proportional to explicit record. Streamed verification may use polynomial live working memory, but recording all output requires exponential simultaneous storage if retained; all source/index/input reads, scanning, verification, creation and output charged for implemented upper bounds. Original finite source bits: 1304, 1912, 2720; corresponding evidence bits above. Do not use these metrics to infer FLMV same-machine contraction.

Revision from initial idea: the mandatory RES final seal fixes the empty-source-clause zero-cost exception; mutually exclusive tags exclude uncharged hybrids. Cook--Reckhow formalized proof length in bits and highlights why a node-only metric is different.

**Material tracker implication:** [P2-B10] compact-witness premise is indispensable under these general assumptions; record new [P2-B11] distinct-system foil if not already present on latest complete main blob. [P1-01],[P1-03],[P2-D1],[P2-B1],[P2-B2],[P2-C3] remain OPEN. Known Haken PHP/short Cook ER and Tseitin GF(2) remain upper/lower shortcut controls, not transfers.

**Next exact task:** authenticate EVERY historical R_mix341 rule, dense-name equivariance, row payload/bit bounds and branch contexts, and establish CW or a truly LEGAL native counterexample. This artificial countercontrol cannot substitute for that. P vs NP OPEN.
