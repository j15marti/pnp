# LSPV-4/511 | Transition-sensitive affine trace kernel and bounded gamma parser

**November 8, 2026, 21:36 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.**

**Exact nodes:** new [P2-L4-511] refines [P2-L4-510], [P2-L4-510R], [P2-A4], and LSPV-2/513. Unresolved [P2-A2], full [P2-A4], [P2-A5], [P2-D1], [P2-C3], [P2-B1], [P2-B2], [P1-01], [P1-03], [P1-04].

## IDEA -> SEARCH -> ITERATE

**Hypothesis:** Replace the explicit $|R|\times k$ observed-affine-row table in LSPV-2/513 by an online pivot basis; recover the compact LSPV-4/510 gamma header's all-input small-workspace bound without switching to unary by a fully charged input-length scan and early numeric cap. A further exact trace distinction emerges: a transition-neutral input read need not impose a raw input-bit equality constraint.

**Four falsifiers:** F1 an oversized malformed gamma field forces $Ω(L)$ retained numeric WORK after capping; F2 changing a bit at a 0/1-neutral input transition changes the subsequent internal machine configuration; F3 an online sensitive-row kernel incorrectly predicts a full internal configuration trace; F4 streamed rank disagrees with batch elimination or retains more than $k^2$ row bits.

**Actual continuity:** Both complete root trackers and current issue #3 were read; governing research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, peer research/agents/lspv-2/2026-11-08_2112_LSPV2_AFFINE_VIRTUAL_READ_KERNEL513.md (blob 8b4c94ec1836e6c0cb159959e8614f9d85af1f5b), prior LSPV-4/510 and /510R (blob 2acfe123b4a57c1c238adc8c0750be379b999bd2), and latest handoffs. Actual Grok GROKPROOF/2026-11-08_1130_PROGRESS.md (blob 6942a99f176e996e9542f0386b7aa7fe2ce89e70) and Claude research/agents/claude/world-ledger/README.md (blob de75a371ce3143a4495e6892df7fb04794a6b708) inspected.

**External and primary search:** FLMV (JACM 2005), original https://lance.fortnow.com/papers/files/tst.pdf, Section 2.1 and page-four screenshot; Ben-Sasson/Wigderson (JACM 2001), original https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf, Definition 4.1 and width-size lower-bound theorem; Urquhart (1987), ordinary Resolution. Exact repository reads: konard/p-vs-np README.md blob 0e0ec77f83ad6eec1719a96066108b96ac1c2a95 and scripts/proof_status.json blob 93b77ed3d8fe456f81c690035f45f07910a247f2; blkph0x/p-vs-np-proof-research README.md blob f397a7747eaca82df3d754d0a4b4bab1fe10f814, METHOD_INDEX.md blob 18d693ea71df543c379eb7afbebc3106e32f03e5, INDEPENDENT_AUDIT.md blob b30515cced93d8911a6415555ee9ec1444502d93; MassimoLauria/cnfgen/cnfgen/families/tseitin.py blob 4bb5fd198fc4a698a5a207f67b36a9591b2a3bab; meelgroup/frat-xor/format.md blob 986a21aa92b62f844ef1fce852193142c41b2b1f; openai/math/CONTENTS.md blob 7e1ed90ac5a666f1bbecb22027387c4ad79e9d03. These support model and source boundaries, not the unproved transfer. Public web and GitHub searches actually used; no dedicated Google-branded search was invoked. Project-search duplicates include LSPV-4/487's gamma length scanning and LSPV-4/510R's correct unary remedy; no novelty claimed for basic rank-nullity or gamma codes.

## Theorem A: exact transition-sensitive descriptor kernel (PROVED/RESTRICTED)

Fix one authenticated immutable parent, one deterministic binary guest with identical initial internal configuration, one fixed virtual input length, and indexed virtual bits

$$
y_i(d)=p_i\oplus c_i\oplus \langle v_i,d\rangle,\qquad d\in\mathbb F_2^k.
$$

Run anchor $d_0$. At each input-reading step on its **internal configuration trace**, compare what the actual deterministic machine transition would do on 0 versus 1, while holding its control state and all other scanned tape symbols fixed. A read occurrence is **live** if the next internal configurations differ, **neutral** if they are identical. Form $V_{\mathrm{live}}$ from the $v_i$ coefficient rows of only live reads. Assume unchanged blank/nonblank boundaries and an authenticated fixed guest-visible transducer.

Then complete *internal configuration-trace equality* (not identical raw input logs) is equivalent to

$$
C_t(d)=C_t(d_0)\ \forall t
\quad\Longleftrightarrow\quad
V_{\mathrm{live}}(d\oplus d_0)=0.
$$

**Proof:** Induct on steps. At neutral reads 0 and 1 cause the same next configuration; at live reads the kernel forces matching symbols, so the next configuration agrees. Conversely, if the full configurations agree at all steps but one live symbol differs, that step would produce different next configurations, a contradiction. Thus the class of descriptors with exactly the anchor's internal configuration trace has size $2^{k-\operatorname{rank}(V_{\mathrm{live}})}$ by GF(2) rank-nullity.

This does not say an instrumented transcript including actual raw observed bits is identical. It does not apply without checking the native transducer's own state or all applicable transition symbols. It does not assert that different traces must return different SAT classifications. LSPV-2/513's all-read-value criterion remains valid as a stronger *sufficient* condition, not the exact necessary condition for state-trace reuse when neutral steps are permitted.

## Theorem B: online rank resource repair (PROVED/RESTRICTED)

On each live read compute its $k$-bit coefficient row and XOR-reduce against an echelon basis indexed by pivot position. Retain a nonzero residual or discard zero. Induction preserves the row span. At most $k$ rows of $k$ bits are retained, rather than the peer's explicit $O(|R|k)$ read matrix. Storage is $O(k^2+\log(L+T))$ bits plus the actual guest, source/transducer, INDEX and other buffers. Conservative bit-level row reduction takes $O(r_{\mathrm{live}}k^2)$ steps, with row acquisition and native input/index reads charged separately. Checking $q$ descriptor candidates adds $O(qk^2)$ steps. This does not make the anchor guest free and does not bound failed policies, retention/replay, guest time or recursively iterated child acquisition. Full live rank $k$ gives one compatible descriptor and no guaranteed speedup.

## Theorem C: all-input logarithmic-WORK gamma header repair (PROVED/RESTRICTED)

Preserve the exact NEW LSPV-4/510 source grammar: 8-bit A5 magic, Elias-gamma($H$), gamma($m$), gamma($k$), strict signed proper ternary core/tail records, terminal 01 and following blank. A guard first **scans the complete read-only INPUT tape to discover its actual length $L$**, using identical 0/1 transitions and a separate blank transition, O(L) paid moves, and an O(log(L+2))-bit counter. It then restores its input head and begins gamma decoding.

For any positive gamma header field $x$, let $b$ be its leading-zero count. If $b>\lfloor\log_2 L\rfloor$, reject **before decoding/storing** the numeric payload. Otherwise its value needs at most $\lfloor\log_2 L\rfloor+1$ bits. Also reject if $x>L$. All valid sources satisfy $H,m,k\le L$ because every parameter is bounded by actual clause-record count. Their headers therefore survive the cap. All later expected-end calculations and indexed addresses use O(log L) bits. Run the authenticated parity/incidence/ID and trailer checks of /510 with repeated recomputation instead of a full graph buffer.

The composed SPECIALIZED guard is correct on valid accepted sources and rejects malformed sources using $O(L^2\operatorname{polylog}(L+2))$ time and $O(\log(L+2))$ supplemental WORK/INDEX high-water on **every** binary source, with all input scans and indexed writes/erasures charged in the FLMV machine model. This is an alternative to the separately valid /510R unary-header grammar, not a contradiction of that correction. Its initial length scan *does read* varying tail sign bits, invalidating the older literal "unread signs" description. But the read transitions on 0/1 are deliberately equal; hence the machine's internal configuration trace can still coincide across accepted polarity variants under Theorem A. The raw read-value transcript differs. A general SAT guest may have live reads and cannot assume this sharing.

The special guard followed by a general total SAT/UNSAT/malformed classifier $B$ on every rejected input is correct **only if $B$ is available**, and its full $T_B,S_B$ costs remain. No general SAT contraction is proved.

## Hardness family, legal shortcuts and remaining transfer

The controls are the published odd-charge cubic-expander Tseitin families: a connected cubic graph on $H$ even vertices, $m=3H/2$ edge variables, $4H$ proper three-literal clauses with 12H signed source occurrences. A fixed one-odd-charge assignment is UNSAT, and an expanding subfamily has $S_{\mathrm{Res}}(\Gamma_H)=2^{\Omega(H)}$ for **ordinary shared-DAG Resolution**, per Ben-Sasson/Wigderson and Urquhart. The gamma bit length is $M=\Theta(H\log H)$. Appending $k=\max(2,\lceil 2\lceil\log_2H\rceil/5\rceil)$ disjoint fresh-variable ternary clauses preserves ordinary Resolution minimum exactly: restrict the tails by a satisfying fresh-variable assignment, or ignore the tails for the upper direction. The fast GF(2) charge-sum shortcut must remain an explicit upper-bound control. None of these statements is a full mixed $R_{\mathrm{mix341}}$ lower bound or unrestricted SAT decision-time lower bound.

## Reproducible checks and limitations

Published independent JavaScript code: experiments/arc/lspv4_511_streamed_affine_gamma_cap.mjs (Git blob 22c885db82d76fa830357757f74080b43f9991d9); raw results: results/raw/arc/2026-11-08_2136_LSPV4_511_STREAMED_RANK_GAMMA_RAW.json (blob 33c3a4c999f130c0e2e1c9e4d224c1578113a985). Base tests: **12,436** batch/streamed rank and kernel checks; transition tests: **256** full controlled comparisons and **8,184** randomized transition comparisons, all PASS. The 8-row, k=8 control has full raw-read rank 8 (one raw-value-compatible descriptor) but live rank 3 (**32** same-internal-trace descriptors). Six gamma-header-shape controls include H=4/6/8/14/128/2732 (lengths 293/415/639/1073/13948/459249). Seven oversized malformed gamma controls reject declarations requiring up to 513 bits in a 1033-bit packet before retaining the integer. **The generated header shapes are not certified original Tseitin sources**; this is a parser/resource and trace-invariance control, not a SAT solver. Independently written Python tested 9,995 conditions with up to 1,039 rows and k=12, plus malformed headers and transition-kernel equivalence. Python output and code are in the conversation reproducibility archive. No historical R_mix341 checker or native FLMV instruction-level interpreter was run.

**All-phase account:** input-length prescan, head reset, numeric gamma prefix scanning, index tape writes/erasure, repeated graph/source validation, pivot-row acquisition and elimination, guest runtime and its high-water, emitted descriptors, output serialization, cache retention/retrieval/recomputation, all failed policies and simultaneous ancestor/child buffers MUST be included when implementing a general contractor. A local component bound cannot be silently substituted for the complete physical $s'\le\max(\rho,\eta,\lambda,\lambda s)$ or the advertised $t'\le\max(11/10,3/5+t/2)$, $s'\le\max(1/2,s/2)$. The same-machine, both-label, malformed-aware, all-input, recursive transformation remains OPEN [P2-A2]/[P2-A4]/[P2-A5]; B3 and the historical mixed lower bound remain OPEN.

**Publication limitation:** root main.tex fetch returned blob fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba but **zero content**. Its ownership region cannot be authenticated, so it was deliberately not modified. No other role manuscript content changed. P versus NP remains OPEN.

**Actual advance:** scoped exact transition-sensitive replay kernel, O(k²) online-rank storage, and preservation of compact gamma encoding with fully charged all-input logarithmic-WORK header validation. **Remaining gap:** universal solver-dependent all-input contraction and recursive same-machine resource proof.
