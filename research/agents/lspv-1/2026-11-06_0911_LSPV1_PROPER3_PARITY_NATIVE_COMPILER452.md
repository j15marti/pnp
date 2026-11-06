# LSPV-1/452: Proper-3-CNF original-source parity compiler, 4k-1 paid native semantic nodes

**2026-11-06 09:11 PST | Route B lead | PROVED/RESTRICTED for the declared R_mix341 semantic AND3/GF(2) subcalculus; COMPUTATIONAL finite replay.** Accepted-byte historical checker, B1, B2, B3, full mixed superpolynomial minimum and P versus NP remain OPEN.

## IDEA -> SEARCH -> ITERATE

**Hypothesis:** A 1-, 2-, or 3-local GF(2) row can be encoded in four *proper signed width-three original CNF clauses* by padding missing coordinates with fresh original input variables. The four source clauses can then be combined with three paid two-parent, at-most-three-original-coordinate AND3 nodes into a factor exactly equivalent to the row, and a legal paid XOR tree can reach 0=1.

**Four falsifiers:** (F1) padding or factor conjunction exceeds original-coordinate support three; (F2) eight-bit complete table does not equal the claimed row; (F3) a forged source clause/AND parent/equation alias/XOR step is accepted; (F4) a minimum-proof optimizer or free XOR-from-CNF axiom is silently assumed. F1-F3 rejected by exact proof and finite hostile controls. F4 avoided by an explicit uniform nonminimum fallback.

Read governing five-role handoff, issue #3 including latest comments, AGENTS.md, CODEX.md, repo skill and LSPV-2/341 grammar (blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb`); actual LSPV-1/451, LSPV-3/452-453, Grok `GROKPROOF/2026-11-06_1220_PROGRESS.md` (blob `5c4fbf8f`), and Claude `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` (blob `1f9fc727`). External change-aware review: konard/p-vs-np `proofs/complexity/README.md` and `scripts/proof_status.json`; blkph0x/p-vs-np-proof-research `METHOD_INDEX.md`; meelgroup/frat-xor `format.md` (distinguishes original XOR sources from XOR derived from clauses); peitl/short-proof `README.md`; openai/math `lean/OAI/Algorithms/SubexponentialSAT/ExecCNF.lean`. Indexed web searches reviewed Cook-Reckhow, Urquhart, Ben-Sasson/Wigderson, Braun arXiv:2609.23015v2 and bounded arithmetic. No separate Google-branded engine or historical production checker was used. Neither repository code nor Lean axioms prove the target transfer.

## Source encoding and theorem

Let $E=\{(S_i,b_i):1\le i\le M\}$ be GF(2) equations $\bigoplus_{x\in S_i}x=b_i$, with $1\le|S_i|\le3$, no variable repeated within a row, and $n$ distinct equation variables. Pad each row with $3-|S_i|$ globally fresh variables to form a three-variable original input scope $T_i$. For each of the **four** three-bit assignments $a$ violating row $i$, put into the original signed CNF the clause

$$
C_{i,a}=\bigvee_{z\in T_i}\begin{cases}z,&a(z)=0,\\\neg z,&a(z)=1.\end{cases}
$$

It blocks exactly the violating assignment $a$. Thus the group of four proper width-three clauses is exactly equivalent to row $i$ for every one of its eight assignments. All padding variables are **original coordinates of the newly constructed CNF**, not paid DEF wires. The new source $\Phi(E)$ has exactly $4M$ proper width-three signed clauses, $n+\sum_i(3-|S_i|)\le n+2M$ original variables and indexed size $O(M\log(n+M+2))$ bits after compact naming. This changes the CNF encoding used in LSPV-1/451 (which used width at most three); no hardness-preserving reduction from that earlier CNF is asserted.

**Theorem 452.1 (PROVED/RESTRICTED).** If $I\subseteq[M]$ is a set of $k$ source rows whose XOR equals $0=1$, then the *declared semantic* R_mix341 has a valid source-labelled refutation of $\Phi(E)$ with

$$
\boxed{q=3k+(k-1)=4k-1\text{ paid nodes},\quad D\le2+\lceil\log_2 k\rceil.}
$$

**Proof.** For each chosen row, two AND3 nodes conjoin disjoint pairs of its four original clauses, followed by one AND3 node joining those local factors. All support sets have three original variables; the output is the exactly eight-row-verified GF(2) equation. The final annotation is the same node's permitted normal form, not an extra free axiom. These $3k$ inference nodes have two-layer parallel span. A balanced $k$-leaf tree of $k-1$ paid two-parent XOR inferences cancels the row masks and produces $0=1$. The entire DAG has original-source indices, acyclic legal dependencies and exact unchanged unit weights. No SPLIT, DISCHARGE, LOCAL, paid DEF, weakening or source oracle occurs. QED.

**Corollary 452.2.** Every inconsistent affine system E admits an inconsistent row subset of size $k\le\min(M,n+1)$ by linear-algebra basis selection. Therefore

$$
\boxed{W_{R_{\rm mix341}}(\Phi(E))\le4\min(M,n+1)-1.}
$$

This is a valid **upper** bound even when W minimizes over *all* mixed shared/reconvergent proof DAGs, because it explicitly supplies one legal proof. Gaussian elimination constructs some supporting subset in polynomial time, with full bit and storage charges. Finding the smallest support can be NP-complete (LSPV-1/451), but free optimal proof choice does not charge the optimizer; a uniform nonminimal fallback suffices for this upper bound. This does NOT provide any lower-bound preservation for R_mix341.

## LSPV-1/451 application, existing family controls

For X3C universe $r=3q$, chain length $L=q+1$, and $m$ triple rows, existing LSPV-1/451 equations have

$$
M=rL+2r+m+2,\qquad M_1=r+2,\ M_2=rL,\ M_3=r+m.
$$

The new proper width-three CNF has $4M$ source clauses and $V'=4r+5+2rL$ original coordinates. The known contradiction using **only the global chain and all fallback chains**, with no input X3C triples, has $K=rL+2r+2$ rows. Thus a uniformly constructible no-oracle native-semantic proof has

$$
\boxed{W_R(\Phi(E_S))\le4K-1=4(rL+2r+2)-1=O(rq).}
$$

If a shortest XOR support of cardinality $\kappa(E_S)$ is supplied, the compiler yields $W_R\le4\kappa(E_S)-1$, **not** equality for the full mixed calculus. The X3C NP-completeness result is about *discovering the exact optimum*, not the existence of short proofs.

| Original source / control | Rows M | Proper 3-CNF clauses | Chosen rows | Paid proof nodes | Span |
| --- | ---: | ---: | ---: | ---: | ---: |
| X3C q=1 exact cover | 15 | 60 | 6 | 23 | 5 |
| X3C q=1 no triple | 14 | 56 | 14 | 55 | 6 |
| X3C q=2 exact cover | 34 | 136 | 10 | 39 | 6 |
| X3C q=2 no exact cover | 34 | 136 | 18 | 71 | 7 |
| X3C q=2 uniform fallback | 34 | 136 | 32 | 127 | 7 |
| Existing odd K4 Tseitin finite instance | 4 | 16 | 4 | 15 | 4 |

**Known hard-family ledger:** For suitable cubic expander odd-Tseitin graphs with h vertices, source has $3h/2$ edge variables and four proper width-three clauses per vertex, $4h$ clauses, $N=\Theta(h\log h)$ bits. Urquhart (1987) and Ben-Sasson–Wigderson (2001) establish $2^{\Omega(h)}$ ordinary unrestricted shared-DAG **Resolution** lower bounds, but the project's declared semantic mixed AND3/GF(2) proof uses $4h-1$ nodes on bridgeless cubic graphs. This defeats a hard-family transfer to the full mixed calculus. Haken PHP is likewise Resolution hard but has Cook/Buss extension/Frege shortcuts. Braun (arXiv:2609.23015v2, Nov 3 2026) proves $\exp(n/(32768\ell^2))$ on bit-PHP in unrestricted DAG Res($\oplus$) for $n=2^\ell$, $\ell\ge32$; this is not an all-mixed or arbitrary machine lower bound, and a hardness-preserving 3-CNF reduction is still required to import that family.

## Verification and charge ledger

Standalone standard-library Python producer replays all eight-bit original-clause groups, two-parent AND3 and GF(2), original source references, explicit contradiction, SAT terminal-toggle controls and six malformed DIMACS inputs. Independent Node.js verifier tested five original certificates and 20 corruptions, **72,766 assertions passed**. Python reported **2,241** explicit and per-node/source checks. Odd original K4 has zero models, every one of its 16 single-clause deletions has a SAT witness, and even K4 has eight models. Python generator measured about 0.082 seconds and 97,420 KiB maxRSS including interpreter allocations, not external research or GitHub publication. No historical accepted-byte engine execution was claimed.

Selected proof nodes $4k-1$ and ideal critical path $2+\lceil\log_2k\rceil$ are *not* actual time/space. Dense explicit equation payloads may require $O(kn\log(n+M)+k\log(M+k))$ bits; building them takes $O(kn)$ elementary bit operations after row selection, with input/header/source-reference parsing, serialization, proof verification, search and failed policies, cache retention, recomputation, output and all-phase peak additionally charged. Gaussian elimination uses polynomial time and up to $O(Mn)$ bits in its explicit matrix phase, including allocate-then-free peaks. Choosing the minimum support by exhaustive enumeration is NOT a polynomial-time construction and is not charged inside the ideal W minimum. No same-machine FLMV contraction is inferred.

**OPEN:** R_mix341 historical **accepted-byte** grammar, soundness of any further claimed private/LOCAL/DEF interfaces, genuinely superpolynomial $\overline W_R$ across every legal mixed rule, and noncircular **same-calculus B3** $\mathrm{SAT}\in P\Rightarrow \overline W_R(N)=N^{O(1)}$. Cook-Reckhow's p-bounded *some-system* result does not supply this fixed calculus. The present result is a **polynomial upper-bound shortcut** invalidating one class as a candidate for full mixed hardness. Historical source, rules, weights, role ownership, task identities, enabled states and schedules unchanged. P versus NP **OPEN**.

## References

1. Urquhart, A. Hard Examples for Resolution. J ACM 34 (1987), 209-219.
2. Ben-Sasson, E., Wigderson, A. Short Proofs Are Narrow. J ACM 48 (2001), 149-169.
3. Haken, A. The Intractability of Resolution. Theor Comput Sci 39 (1985), 297-308.
4. Cook, S. A., Reckhow, R. A. Relative Efficiency of Propositional Proof Systems. J Symbolic Logic 44 (1979), 36-50.
5. Buss, S. R. Polynomial Size Proofs of the Propositional Pigeonhole Principle. J Symbolic Logic 52 (1987), 916-927.
6. Braun, K. An exponential lower bound for bit-PHP in resolution over parities. arXiv:2609.23015v2 (2026-11-03).
