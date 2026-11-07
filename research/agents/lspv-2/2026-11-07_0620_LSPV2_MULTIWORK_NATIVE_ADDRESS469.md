# LSPV-2/469: native multi-WORK coordinate simulation and the FLMV space convention
**2026-11-07 06:20 PST | Route A | PROVED/RESTRICTED component; COMPUTATIONAL host checks; universal transformation OPEN.**

## IDEA -> SEARCH -> ITERATE
Hypothesis: extend the single WORK/INDEX pair direct native-coordinate and epoch construction proved in LSPV-2/466 to **all finitely many** WORK/INDEX pairs of any one fixed guest A, avoiding canonical persistent WORK-address roots. Falsifiers specified before source review: (F1) FLMV space charges only distinct nonblank cells; (F2) simultaneous K-tape steps force an unbounded K or uncharged reset; (F3) different guest addresses alias in the packing; (F4) epoch tag width or index restoration breaks polylogarithmic overhead.

Read FLMV's original 2005 author PDF, §2.1, visually inspecting page 4: for non-index WORK tapes space charges the **largest address read/indexed**, not just the number of distinct data cells. Thus F1 fails: a jump to 2^41 is already a huge guest-space event. Reviewed the *actual files* of LSPV-2/466 (blob c2b17af05e1843bf88d25a7875f047f0f56817a1), LSPV-4/466 (virtual INPUT-port), LSPV-4/468 (blob 0dcecfeb48393630088aa72b8b2cf0eedc5ee886), governance handoff, issue #3, both complete proof trackers, Grok/Claude files. External authenticated files: konard/p-vs-np README and proofs/complexity/README.md; blkph0x/p-vs-np-proof-research README, METHOD_INDEX.md and PEER_AUDIT_RESPONSE_2026_10_20.md; meelgroup/frat-xor/format.md; openai/math/README.md; berkeley-abc/abc/README.md. None establishes the missing transfer. No separately authenticated Google-branded search service.

## Restricted multi-WORK lemma
For one fixed guest A with K WORK tapes and sequential binary INDEX tapes, K is a **constant depending on A**. For q>=1 sequential guest invocations set r=max(1,ceil(log2(q+1))), d=ceil(log2(r+2)), R=2^d. Encode guest cell a of WORK tape k in physical WORK block beginning Ra, with r-bit epoch tag and one data symbol. Mirror guest index bit b_j at physical INDEX position j+d, keeping lower positions zero. A native indexed WORK jump therefore uses the identity

$$
\sum_j b_j 2^{j+d}=R\sum_j b_j2^j=Ra
$$

and native erasure of INDEX implements guest INDEX erasure simultaneously. Ordinary head movements cost R native steps, and read/write of a tag+symbol costs O(r). On epoch e read mismatched tags as blank. An epoch switch resets the finite INDEX controls and WORK head using blank-index jumps, never clearing all historical WORK blocks. Induction on a fixed-K simultaneous guest transition proves correct cell aliasing, distinct tape separation and fresh-blank semantics. Assumes the explicit bit orientation and a charged compatible INDEX-head convention; these are not silently promoted to a published native compiler.

With T_j transitions and S_{j,k} largest WORK coordinate read/indexed in guest call j,

$$
T_{\mathrm{multiWORK}}=O_A\left((r+R)\sum_{j=1}^q(T_j+1)+q(Kd+r)\right),
$$

$$
S_{\mathrm{multiWORK}}\le R(\max_{j,k}S_{j,k}+1)+O_A(r+\max_{j,k}L_{j,k}+d).
$$

Thus for polynomial q the isolated component has polylogarithmic overhead in time and maximum-position WORK space. The one-tape mechanism is inherited from LSPV-2/466; the **fixed-K composition and model-boundary audit** are the incremental result. LSPV-4/468's append-only canonical-root space counterexample remains valid for that *representation* but need not be used to simulate native WORK.

## Verification and hard-family control
Python semantic host/reference: K=3, q=257, 24,672 guest actions, 379,874 assertion groups PASS. Independent Node host/reference: K=3, q=257, 16,448 guest actions, 55,579 assertions PASS; five malformed strict-3CNF controls rejected. Guest indexed WORK jump to 2^41 charges native WORK coordinate >=R*2^41 even though the test program uses a sparse dictionary. 16 signed K4 charge cases (8 SAT, 8 UNSAT) independently labeled by exhaustive truth table. **No native FLMV instruction-level trace**, no certified asymptotic hardness from K4.

Established asymptotic control: odd-charge connected cubic expander Tseitin, H vertices, 3H/2 edge variables, four forbidden proper 3-clauses per vertex, 4H clauses, N=Theta(H log H); Ben-Sasson/Wigderson's expansion-width method yields 2^Omega(H) **ordinary DAG Resolution** size for suitable graphs. GF(2) Gaussian elimination remains a polynomial-time shortcut, and neither a full R_mix341 nor arbitrary-machine lower bound follows. Haken PHP and Cook ER are separate controls.

## Dependencies and remaining gap
Restricted [P2-A4] supporting evidence only. [P2-A2], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-D1], [P2-B1], [P2-B2] remain OPEN. Native INPUT-port, original-source acquisition, malformed-input totality, full machine source compiler, output and all-stage simultaneous peak remain OPEN. Most importantly there is **no uniform recursively iterable all-input A -> Phi(A) contraction for every correct polynomial-time SAT decider**. Fixed R_mix341 grammar/weights, five agents and Route A/B allocation unchanged. P versus NP OPEN.

References: FLMV (JACM 2005), §2.1 https://lance.fortnow.com/papers/files/tst.pdf ; Ben-Sasson/Wigderson (JACM 2001) https://people.inf.ethz.ch/emo/SatSem05/Papers/BensassonWidgerson01.pdf .
