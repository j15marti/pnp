# LSPV-2/412: Shared-variable existential projection destroys DEF/GF(2) port coherence

**November 5, 2026, 01:12 PST | PNP SAT-Circuit Reduction Builder | R_mix341 unchanged**

**Status:** **PROVED/EXACT** in the explicitly stated conservative-definition semantic model, with proof below; **COMPUTATIONAL** finite independent verification; **OPEN** original native DEF-row export/LOCAL public-wire grammar, all-proof polynomial translation, same-calculus B3, superpolynomial mixed minimum, and P versus NP. This is a restricted falsifier of *independent existential port projection*, **not** a legal-native counterexample to all polynomial normalizations.

## IDEA (stated before SEARCH)

**Hypothesis:** With the fixed calculus's paid, fresh, total two-input DEF gates, eliminating the same hidden original variable separately in each gate relation may lose a correlation needed by GF(2) consumers. **Falsifiable prediction:** A two-gate XOR chain on two original variables has a forced equality between original and public output after joint elimination, whereas the conjunction of separately projected gate relations permits both output values. The discrepancy multiplies as $2^k$ over $k$ independent chains. A compact shared-wire certificate should still exist, so this is not a hard-family claim.

Falsifiers: (F1) one of the proposed gates violates freshness/totality or the three-original-support bound; (F2) the joint and separate projections coincide; (F3) parity cancellation gives a false equation when operands repeat; (F4) the apparent obstruction disappears once the identical hidden-variable occurrence is retained; (F5) a supposed native GF(2) row was obtained from DEF without an authorized export. F1/F2/F3 were refuted by exact proof and tests; F4 **does** repair the obstruction; F5 remains a native serialization limitation.

## SEARCH: primary sources, corpus and access limits

Read the governing 2026-11-02 12:04 five-role directive at `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` (current blob c3889a3e); live issue #3 including LSPV-1/413, LSPV-3/416 and REFEREE357; `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`; original fixed rules `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob c87acd11; grammar addendum `research/coordination/2026-11-04_0108_LSPV1_384_ORIGINAL_LOCAL_CONVERT_GRAMMAR_ADDENDUM.md` blob bbcdad9a. Materially relevant: LSPV-2/407 and /411; LSPV-3/410 (already establishes five-gate public-wire functional normalization) and /414 (already falsifies source-model-only affine annotation copying); LSPV-3/415 (root-only local circuit normal form); REFEREE357 (B3/byte firewall); LSPV-1/413 (RUP/PHP output lower bound). No claim of general novelty for existential projection or XOR cancellation.

Actual independent review files read: `GROKPROOF/2026-11-04_1518_PROGRESS.md` blob 4e2bb9d9 (fully charged FLMV contraction still OPEN), and `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob 9a5b05d6 (one-tape crossing-sequence lower bound does not transfer to unrestricted/random-access machines). No independent assessment supplies the missing B3 implication.

General-web queries actually run: `Haken 1985 the intractability of resolution pigeonhole principle exponential lower bound pdf`; `Cook 1976 feasible proof systems extended resolution pigeonhole principle polynomial proof`; `Cook Reckhow 1979 relative efficiency propositional proof systems polynomial bounded iff NP coNP`; `Raz Tzameret 2008 resolution over linear equations odd Tseitin polynomial proofs`; and `definitional extension Tseitin variables projection existential quantification composition shared variables Boolean circuits certificate checking`. Read Cook--Reckhow's original author-hosted PDF (including page screenshot), Haken's publication record, Cook's original ER bibliographic record and the Raz--Tzameret author/publisher abstracts. The primary full Haken paper and publisher full Raz--Tzameret text were not available in this session; no contrary full-text claim. Direct Google-branded UI was unavailable; **general web search** substituted.

Authenticated `github.com/openai` searches: `ExecCNFNodeSearchCosts`, `CookLevin`, `LRAT checker`, `extended resolution proof`, `definitional gate`. Full sources read: `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean`, blob 1ced21f4 (node and stack-bit accounting), and `openai/math/lean/OAI/Combinatorics/KMedian/CookLevin/CookLevin.lean`, blob 1e23a159 (machine-to-constraint correctness), neither a native mixed proof compiler or B3 proof.

## ITERATE: exact all-k counterexample to independently forgotten ports

For any integer $k\ge1$, take original Boolean variables $x_i,y_i$ and **two separately paid conservative DEF gates per index**, with unique acyclic extensions:

$$
D_i^{(1)}:\quad a_i=x_i\oplus y_i,\qquad
D_i^{(2)}:\quad b_i=a_i\oplus y_i.
$$

Each definition uses exactly two input occurrences, has at most two original-variable dependencies, is total and conservative, and costs one **logical** paid DEF node. Thus $q_{\rm DEF}=2k$. These gates are legal as definitions under the original /341 rule; no defining clause, affine equation or public wire is presumed independently exported.

Let $J_i(x_i,a_i,b_i)=\exists y_i[D_i^{(1)}\land D_i^{(2)}]$ with ONE shared $y_i$. Then

$$
D_i^{(1)}\Rightarrow y_i=a_i\oplus x_i
\quad\Rightarrow\quad
b_i=a_i\oplus(a_i\oplus x_i)=x_i.
$$

Conversely if $b_i=x_i$, choosing $y_i=a_i\oplus x_i$ satisfies both gates. Therefore

$$
\boxed{J_i(x_i,a_i,b_i)\iff b_i=x_i.}
$$

But independently projecting the identical hidden variable in each gate uses distinct existential witnesses:

$$
\bigl(\exists y_i D_i^{(1)}\bigr)\land\bigl(\exists y_i D_i^{(2)}\bigr)
=\top\land\top=\top.
$$

For $k$ independent copies, the exact joint projection has $2^{2k}$ models over the public triple $(x,a,b)$, whereas the incorrectly separately projected conjunction has $2^{3k}$, a factor of **$2^k$ spurious valuations**, including assignments $b_i\ne x_i$. This is an exact all-size, constant-local-original-support failure of the *specific* compiler operation $\exists y(A\land B)\leadsto(\exists y A)\land(\exists y B)$; it is NOT a lower bound on the optimal original proof DAG or an arbitrary SAT algorithm.

**Source controls:** choose genuine signed original CNFs
$$
F_k^+=\bigwedge_i(x_i)\land(x_i\lor y_i),\quad
F_k^-=\bigwedge_i(\neg x_i)\land(x_i\lor y_i),\quad
F_k^\bot=F_k^+\land(\neg x_1).
$$
Both $F_k^+$ and $F_k^-$ are SAT (respectively $2^k$ and 1 source models); $F_k^\bot$ is UNSAT. Under the *consistent* conservative definitions, every model of $F_k^+$ has all $b_i=1$ and every model of $F_k^-$ has all $b_i=0$. No empty-model implication is used to invent a proof.

**Repair / compact alternative:** jointly retain the shared $y_i$, or eliminate it ONCE from the combined relation. The latter yields the $O(k)$-length exact equality certificate
$$
\bigwedge_i [ (\neg b_i\lor x_i)\land(b_i\lor\neg x_i) ].
$$
At the affine level, the two *semantic defining identities*
$a_i\oplus x_i\oplus y_i=0$ and $b_i\oplus a_i\oplus y_i=0$ cancel to $b_i\oplus x_i=0$. If, **and only if**, the original native byte checker authorizes both DEF-to-GF(2) row exports, a paid XOR node would authenticate this step and two paid LOCAL-CONVERT clauses could publish the equality when auxiliary outputs are legal. Under that explicit `Splus` interpretation the illustrative charge is $2k$ paid DEF + $k$ XOR + $2k$ LOCAL = $5k$ derived nodes. This is a conditional completion, **not a certified original R_mix341 inference DAG**. Sminus and SrowOnly remain legitimate distinct completions of the inherited prose (LSPV-2/407; REFEREE357).

## Verification and physical resources

**COMPUTATIONAL:** a deterministic Python producer exhaustively enumerated all $2^{3k}$ public triples for $k=1,\dots,6$, checks each pair of defining functions and the corrected two-clause equality, evaluates SAT+/SAT-/UNSAT source controls, and rejects six malformed/forged gate-record fixtures. The independent Node.js program uses a different shared-witness bit-mask calculation, independently checks source assignments and all 2k formal GF(2) cancellation identities. **316,163 assertions passed**. For $k=6$: exact public models 4,096; independently projected public models 262,144; spurious multiplier 64; $q_{\rm DEF}=12$; exact equality uses 12 uncharged-as-proof representation clauses. These numbers are not optimal proof sizes and no random seed was used.

The logical DEF count $2k$ and conditional Splus $5k$ must NOT be substituted for physical runtime. Explicit gate serialization uses $O(k\log k)$ identifier bits; the literal equality CNF uses $O(k\log k)$ bits. A fully materialized naive joint truth table uses $\Theta(2^{3k})$ bits, while the exact compact row representation uses $O(k\log k)$. Parsing all supplied original/evidence bytes, repeated indexed reads, construction, source checks, proof serialization, verification and peak writable memory remain separately charged. The exhaustive finite **search/check** work $\Theta(2^{3k}k)$ is distinct from the **chosen logical derivation** and from optimal computation. Flat truth-table expense is not an intrinsic machine lower bound. No FLMV contraction is inferred; all-phase memory must obey $s'\le\max\{\rho,\eta,\lambda,\lambda s\}$ if that transfer is attempted.

## Relation to established hardness and exact open arrows

**KNOWN, model-restricted:** Haken (1985) proves $2^{\Omega(h)}$ **ordinary shared-DAG Resolution line** lower bounds on explicit unary PHP with $h+1$ pigeons, $h$ holes and $N_h=\Theta(h^3\log(h+2))$ binary/ASCII source length. The theorem quantifies over all Resolution derivations of those formulas, NOT all uniform deciders or the mixed system. Cook (1976) supplies polynomial Extended Resolution proofs of PHP. Raz--Tzameret (2008) construct stronger algebraic proof systems with polynomial PHP/Tseitin proofs. Existing source-authenticated native AND3/GF(2) gives linear odd-Tseitin proofs (LSPV-2/341). These are mandatory controls against an invalid proof-hardness-to-machine-hardness transfer.

**OPEN, same fixed calculus:** a complete explicit native LOCAL/DEF-facet/GF(2)/AND3/exported-wire grammar; consumer-aware and original-source-authenticated polynomial proof-byte normalization *or a certified legal obstruction*; a noncircular $\mathrm{SAT}\in\mathrm P\Rightarrow\overline W_{R_{\rm mix341}}(N)=N^{O(1)}$; any superpolynomial $\overline W_{R_{\rm mix341}}$ lower bound. B1/B2/B3 remain OPEN. No outcome of this test refutes them. This project remains short of P versus NP.

## Next test

Implement exact **stable slot selectors** for the two ordered DEF input occurrences in an explicit versioned checker, then (i) attempt a conservative consumer-preserving compiler for whole mixed proofs including auxiliary row/circuit ports; (ii) separately prove a genuine noncircular B3 for the preselected calculator or exhibit a valid conditional countermodel. Until the authentic native serialization is fixed by authority, do not treat Splus's $5k$ trace as native, and do not silently change R_mix341.

**Publication artifacts:** role report (this file); `experiments/arc/lspv2_412_joint_projection_producer.py`; `experiments/arc/lspv2_412_joint_projection_independent.js`; `results/raw/arc/2026-11-05_0112_LSPV2_JOINT_DEF_PROJECTION412_summary.json`; and `research/coordination/2026-11-05_0112_LSPV2_JOINT_DEF_PROJECTION412_FIVE_ROLE_HANDOFF.md`. External mathematical review pending.