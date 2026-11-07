# LSPV-5/407 — adaptive affine branch-rank retraction and reconvergence firewall

**2026-11-07 02:48 PST | Route B red team | PROVED/RESTRICTED abstract binary-GF(2) theorem; COMPUTATIONAL independent controls | historical R_mix341, B1/B2/B3, all-mixed hardness, and P versus NP remain OPEN**

## IDEA -> SEARCH -> ITERATE

### Initial claim card and falsifiers

Target: extend the fixed full-cube control `[P2-L5-406]` to adaptive affine branching without adding a split/discharge rule to historical R_mix341. Exact prefix: for every common affine source $E$, every finite complete adaptive affine decision tree $T$, and every context-typed acyclic union of binary-XOR leaf refutations with $q$ distinct paid inference vertices, if the linear query forms used anywhere in $T$ have rank $r$, then $E$ has a binary-XOR refutation of at most $q+r$ paid vertices.

Predeclared falsifiers were:

1. a discharged adaptive-leaf terminal depends on a direction outside the span of all queried linear forms;
2. both children at every reachable split do not suffice to cover all assignments;
3. affine rows excluding all reachable leaf cells need not span the constant contradiction;
4. reconvergence permits a proof vertex to lose branch assumptions while remaining a legal shared vertex.

Falsifiers 1--3 fail by the proof below. Falsifier 4 **narrows the claim**: arbitrary row-label or search-state reconvergence is not accepted. Sharing is legal only when the complete normalized affine context and immutable proof parents agree; a node with incompatible assumption ancestry remains two paid vertices even if its row label is equal. Different query orders may reconverge only after their affine contexts reduce to the same RREF. This is the weakest repair found.

### Actual search and state recovery

Read the complete root trackers: `proof1.txt` blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b` and `proof2.txt` blob `8600ace1c699eabde707d854246831fed313cf0c`; governing handoff blob `c3889a3e514ddbd747150dcb68607013a3b2d154`; current issue #3; `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`; `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`; the complete project research protocol and red-team mode; actual Grok `GROKPROOF/2026-11-07_0819_PROGRESS.md` blob `c52f2f67956482d1ab10cb751aab1b0217890ba1`; and Claude world-ledger README blob `de75a371ce3143a4495e6892df7fb04794a6b708`.

Peer files read directly, not from chat summaries:

- LSPV-1/470, `research/agents/lspv-1/2026-11-07_LSPV1_SET_COVER_SHARED_RES_OPT470.md`, blob `6b762c700f41b1b2e905c1b08685489b9e1afbb1`: exact NP-completeness only for a uniform layered subset of legal source-authenticated Resolution DAGs; unrestricted minimum and mixed shortcuts remain open.
- LSPV-3/470, `research/agents/lspv-3/2026-11-07_0224_LSPV3_CUT_PARITY_FLAT_CNF_FIREWALL470.md`, blob `02a1bb79e4ddc1e72ccded6553b581b6f8f8916f`, its handoff blob `e3373e524b692de5a514e0df517aaa3aebfcc250`, and compact checker blob `8a2e1a1f0635c941073646c7ad263d2bc8ee8ac2`: a linear declared-semantic GF(2) cut proof can have exponentially large exact flat-CNF intermediates. This is a representation firewall, not a mixed-proof lower bound.

Primary literature read/searched:

- Urquhart, *Hard Examples for Resolution*, JACM 34 (1987), DOI `10.1145/7531.8928`: exponential ordinary Resolution lower bounds for expander Tseitin clauses.
- Ben-Sasson--Wigderson, *Short Proofs Are Narrow—Resolution Made Simple* (JACM 2001): Tseitin definition, width and size transfer for Resolution.
- Haken, *The Intractability of Resolution*, TCS 39 (1985), DOI `10.1016/0304-3975(85)90144-6`: exponential ordinary Resolution lower bound for PHP; the paper itself records polynomial Extended Resolution proofs as a control.
- Itsykson--Sokolov, *Resolution over linear equations modulo two*, APAL 171 (2020), DOI `10.1016/j.apal.2019.102722`: tree-like Res($\oplus$) corresponds to parity decision trees whose nodes query affine/linear forms; this does not authenticate the project calculus.
- Braun, *An exponential lower bound for the bit pigeonhole principle in resolution over parities*, arXiv:2609.23015v2 (2026 preprint): unrestricted DAG-like Res($\oplus$) lower bound in that stated system. It is recent preprint evidence, not an all-mixed or all-algorithm lower bound.

Google-branded search was unavailable; ordinary public web search was used. No source was represented as peer-reviewed when it was a preprint.

Required repository review:

- `konard/p-vs-np` `README.md` blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` and `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`: its certified results have their explicit finite-machine/formal-model scope; NP subset P remains unknown.
- `blkph0x/p-vs-np-proof-research` `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5` and `REVIEW_ADDENDUM.md` blob `6a7cc2f8962d3fcfc1778b1d3d8f5dc8d56d70`: scoped parity/polytope and finite evidence, no P/NP resolution.
- `meelgroup/frat-xor` `format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`: explicit original clause/XOR IDs and `i cx`/`i x` cross-rules are a useful provenance model, but not historical R_mix341 bytes.
- `tanyongkiam/cake_lpr` `README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`: verified LPR checker packaging does not prove a lower bound or B3.
- `peitl/short-proof` `README.md` blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab`: finite shortest Resolution optimization, not full mixed minimum.
- `MassimoLauria/cnfgen` `README.org` blob `9fba4e26f2a4cd10444a7226a7a3a7caa1762721`: reproducible PHP/proof-complexity generators; benchmark difficulty is not proof-size hardness outside a stated calculus.
- `openai/math` `README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae` and `anthropics/formal-math` `README.md` blob `1df53bfc14a022088d1b5757698f692bf79390b4`: both explicitly distinguish raw manuscripts/formalized projects and trust boundaries. Neither supplies the missing R_mix341 transfer.

CryptoMiniSat's guessed `README.markdown` path was unavailable; no review of that nonexistent path is claimed. The local skill preflight could not be executed because this run had a connector snapshot rather than a repository checkout; the complete protocol files were read, and publication/readback was performed through the repository connector.

## Established-family ledger and strongest known shortcuts

| Family | Exact encoding and size | Published theorem/model | Known legal shortcut control | Remaining transfer |
|---|---|---|---|---|
| Odd-charge cubic-expander Tseitin **strict 3-CNF** | For simple cubic $G=(V,E)$, one original variable $x_e$ per edge. At vertex $v$ with incident $e_1,e_2,e_3$ and charge $\chi_v$, for each $a\in\{0,1\}^3$ with $a_1\oplus a_2\oplus a_3\ne\chi_v$, include $\bigvee_i \ell_{e_i,a_i}$, where $\ell_{e,0}=x_e$ and $\ell_{e,1}=\neg x_e$. Exactly $4h$ proper 3-clauses, $3h/2$ variables, indexed size $N=\Theta(h\log h)$. Odd $\sum_v\chi_v$ certifies UNSAT. | Urquhart 1987: $2^{\Omega(h)}$ ordinary DAG Resolution size on appropriate expanders; permitted rule is ordinary syntactic Resolution. This is certified proof-size hardness only in that system. | Four clauses at a vertex yield its parity equation; summing the $h$ equations gives $0=1$. Project declared-semantic AND3/GF(2) controls cost $4h-1$ paid nodes. LSPV-3/470 further shows some flat-CNF presentations blow up, but native algebra avoids them. | This family cannot witness all-mixed R_mix341 hardness while that affine shortcut is legal. Historical accepted-byte authentication and exact weights remain `[P2-D1]`/`[P2-C3]` OPEN. |
| Bit PHP $\mathrm{BPHP}_{n+1}^{n}$, $n=2^\ell$ | Variables $x_{p,j}$ encode the $\ell$ address bits of pigeon $p$. For each $p<q$ and address $a\in\{0,1\}^\ell$, include the width-$2\ell$ clause saying $p$ and $q$ are not both at $a$: $\bigvee_j(x_{p,j}\ne a_j)\vee\bigvee_j(x_{q,j}\ne a_j)$. UNSAT by collision. It is **not 3-CNF**. | Braun 2026 preprint: every unrestricted DAG-like Res($\oplus$) refutation has more than $\exp(n/(32768\ell^2))$ clauses for $\ell\ge32$. | Project declared mixed DEF/RES constructions are mandatory countercontrols; exact legality in historical bytes is separate. | No lower-bound-preserving 3-CNF conversion into the full mixed calculus is established. Equisatisfiable Tseitin conversion is insufficient. No transfer to all R_mix341 rules or algorithms. |
| Unary PHP | Variables $x_{p,h}$; pigeon clauses $\bigvee_h x_{p,h}$ and collision clauses $\neg x_{p,h}\vee\neg x_{q,h}$. Long pigeon clauses mean the standard encoding is not strict 3-CNF. | Haken 1985: exponential ordinary Resolution length. | Cook Extended Resolution has polynomial proofs; this is an explicit upper-bound control. | No precise hardness-preserving strict-3-CNF reduction into full R_mix341 was located. Haken cannot be promoted across ER/DEF/GF(2). |

Certified UNSAT, proof-size hardness, and empirical difficulty are therefore separate columns: odd-charge certifies Tseitin UNSAT; Urquhart certifies Resolution proof-size hardness; solver runtimes were not used as theorem evidence.

## The adaptive affine theorem

Let $E$ be a common set of authenticated affine equations over $\mathbb F_2$ in variables $X$. A finite rooted tree $T$ is **complete** when every internal node $v$ queries an affine form $A_v(X)$ and has both children, adding $A_v=0$ and $A_v=1$ respectively. Empty cells may be discarded; every assignment follows exactly one nonempty leaf cell. Let $r$ be the rank of all linear parts queried anywhere in $T$.

At every nonempty leaf $\lambda$, suppose there is a binary-XOR refutation of $E$ plus the path assumptions. Put all refutations into one acyclic union proof DAG. Every vertex has an immutable ordered parent tuple and a normalized affine context. A vertex can be shared only when these contexts and parents agree. Common vertices have empty assumption ancestry. Let $q$ count the union of distinct paid XOR-inference vertices once.

**Theorem 407.1 (PROVED/RESTRICTED).** Under those hypotheses,

$$
W_{\mathrm{GF}(2)}(E)\le q+r.
$$

**Proof.** Tag each derived row at leaf $\lambda$ by the parity vector of path assumptions used in its derivation. Source rows in $E$ and genuinely common vertices have tag zero; a path assumption has its unit tag; binary XOR adds both the row and its tag. For a false terminal, add back the tagged assumptions. They cancel from the derivation and leave an unconditional $E$-derived affine row

$$
U_\lambda(X)=1+\sum_{e\in P_\lambda}\tau_{\lambda,e}(A_e(X)+b_e).
$$

If $x$ lies in leaf cell $\lambda$, every path equation vanishes at $x$, so $U_\lambda(x)=1$. Completeness of $T$ implies that no assignment zeros all rows $U_\lambda$; the affine system $\{U_\lambda=0\}$ is inconsistent. Consequently the augmented row $(0,1)$ lies in their GF(2) span.

Every linear part of $U_\lambda$ lies in the global query span, of dimension $r$. After adjoining the constant coordinate, all augmented $U_\lambda$ lie in a space of dimension at most $r+1$. Hence at most $r+1$ of them span $(0,1)$, and at most $r$ further binary XOR joins derive false. The tag transformation reuses each valid union inference vertex once; incompatible branch vertices were never identified. Thus the common-source proof has at most $q+r$ paid inferences. $\square$

This is an upper-bound/retraction control. It is not a lower bound, a proof-search algorithm, historical syntax authentication, or B3.

### Reconvergence firewall

The proof extends to an acyclic search DAG only when each reconvergent state carries the full normalized affine context and deterministic assignment routing remains complete. Two syntactic paths that query $x_1,x_2$ in opposite orders may merge because their RREF contexts agree. Opposite contexts $x=0$ and $x=1$ may not merge by dropping the assumption label. Row equality alone is not proof-node identity; if two equal rows have incompatible parents or tags, charging them once silently changes the calculus and can leak branch-local conclusions. General semantic state merging with omitted context therefore remains OPEN, rather than being smuggled into Theorem 407.1.

## Exact computation and independent replay

Artifacts:

- producer: `experiments/review/lspv5_407_adaptive_affine_rank.py`;
- independent no-import Node checker: `experiments/review/verify_lspv5_407_adaptive_affine_rank.mjs`;
- raw: `results/raw/review/2026-11-07_0248_LSPV5_ADAPTIVE_AFFINE_RANK407.json`, SHA-256 `0e8bb52890befdf0c7001b33ec9263ea8886cae18630c55f939fed76bd967455`.

The producer constructed adaptive full-rank trees for $n=1,\ldots,7$; each query is $x_d$ plus a branch-dependent combination of already fixed variables. Each leaf proof uses one actually violated source row of the inconsistent system $x_i=0$ for all $i$ plus $\bigoplus_i x_i=1$, and every leaf uses the same shared non-source inference twice. It checked exact tags, coverage, discharged rows, contradictory basis size, $q+r$, and distinct-node accounting.

It then exhaustively enumerated all 1,024 triangular adaptive query policies on three variables (two base-2 choices at depth one and four base-4 choices at depth two). Every policy covered all eight assignments and had query rank three. Negative controls rejected an omitted reachable leaf, wrong branch constant, incompatible-context merge, dropped-context merge, forged low rank, duplicate node ID, and cyclic predecessor; reordered assumptions with identical RREF context were accepted. Producer: 32,784 counted checks. Independent Node replay: 28,225 checks, PASS. No random seed was used; the campaign was deterministic and exhaustive only for the stated finite scope.

Host producer elapsed time was about 0.022 seconds with peak RSS recorded in the raw file. Construction, parsing, source reads, tag storage, exhaustive-policy enumeration, output, verification and raw serialization were charged in the host run. These host figures are not FLMV machine bounds. The ideal $q+r$ excludes discovery by definition; a realizable constructor still pays tree acquisition, failed policies, context normalization, references, storage, retrieval/recomputation, and verification.

Work and span remain distinct. The theorem bounds total distinct-node work by $q+r$. A balanced final combination of at most $r+1$ discharged rows adds only $\lceil\log_2(r+1)\rceil$ ideal XOR span, but retaining all discharged rows may require more space; recomputation trades space for extra realizable work. No free reference or join rule was added to historical R_mix341.

## Status, tracker effect, and remaining gap

`[P2-L5-407]` materially extends `[P2-L5-406]` from one fixed $k$-query cube to complete adaptive affine decision trees and context-normalized reconvergence. It supports the shortcut/retraction side of `[P2-C1]` but does not close it for nonlinear or historical mixed rules. `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]`, `[P2-B5]`, B3, and all-mixed superpolynomial $\overline W_R$ remain OPEN. `proof1.txt` was reviewed with no material change. P versus NP remains OPEN.

The precise next gap is a rule-by-rule historical-byte simulation: authenticate whether the fixed R_mix341 checker can express the context-typed XOR derivations and assumption discharge natively, with exact weights and source provenance, or give a legal accepted-byte counterexample. Without that, Theorem 407.1 stays an abstract GF(2) upper-bound control.


## Publication/readback status

Published artifacts were read back byte-for-byte at blobs: report pending this addendum update; handoff `9c7a704d44bfcd7c47fb2239c9c72696766efe62`; producer `1093c0cda019f8fe53cb457f93285ea5079933da`; independent checker `65519e71586aa82a4578133bbb301951d67c9dda`; raw `8dcafef38e3c21f858220f652a31592c87bb993b`. The complete pre-write proof2 outbox was read back exactly at blob `71e4a94295cf61baf0ec6b53b15aa97de8815463`; `proof2.txt` was conflict-checked from base blob `31a87b5d2f245300054bc1a5b1fb7eaf3f614b0a` and fully read back exactly at new blob `50ff3c58ab1098266c00df8bc682930fdfaf0af1`. Issue #3 accepted comment ID `6705943800`; fetching the 1,180-comment thread for independent readback failed, so comment readback is explicitly unverified. Root `main.tex` returned an empty payload even for bounded line-range reads at blob `68188a24badda635a5983fda1c381cdb694fd497`; under the no-partial-overwrite safeguard it was not edited. No role, task, title, schedule, enabled state, historical rule, or weight changed.
