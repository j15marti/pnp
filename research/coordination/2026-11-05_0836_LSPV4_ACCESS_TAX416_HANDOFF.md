# LSPV-4/416 Route A handoff: per-child versus per-guest-step input tax
**2026-11-05 08:36 PST.** Correct role split: LSPV-2 and LSPV-4 Route A; LSPV-1, LSPV-3 and LSPV-5 Route B. Identities/schedules/rules/weights unchanged; P versus NP OPEN.

**PROVED/EXACT in specified interpreter architecture (not general machine lower bound).** With $N^a$ sequential children of $N^\lambda$ bits, aggregate local time $N^d$, one-time per-child setup $N^u$, per guest-step address/simulation overhead $N^v$, all-phase parent peak $N^\rho$, retained data $N^\eta$, and guest time-space $(t,s)$:
$$
t'\le\max\{d,a+u,a+v+\lambda t\},\qquad
s'\le\max\{\rho,\eta,\lambda,\lambda s\}.
$$
At $(a,\lambda,d,u,\rho,\eta)=(3/5,1/2,11/10,1/2,1/2,1/2)$, the upper-envelope fixed point is $(6/5+2v,1/2)$. For the strict FLMV k=2 region, $v<(c_\star-6/5)/2\approx0.00278471520029515$ with $c_\star=1.2055694304005903\ldots$. Example $v=0$ enters in 11 iterations and $v=1/400$ in 14 from $(10,6)$, while $v=1/300$ fails to enter via *this upper bound*. Prior LSPV-4/343's much larger one-time per-child threshold does NOT apply to per-guest-step overhead.

**COMPUTATIONAL:** 75 exact Python assertion groups, 12,161 separate JS checks; synthetic input source-index transport 64..4096 bytes, charged index writes/read-only probes/erasures, SAT/UNSAT/malformed/corrupted and source-compatibility controls. For N=4096, 148 children x 64 virtual bits: 9472 direct probes, 113664 index digit writes, 606208 per-child full-source scan probes, 38797312 per-read full-source scan probes. These are *not* physical FLMV machine timings.

**SEARCH:** Governing Nov2 handoff and issue#3; LSPV-2/420 plus ARC prior /119, /154, /118; LSPV-1/272,/399; LSPV-4/343,/375,/387; Grok 2026-11-05_1218, Claude TPORT-0002. Reviewed konard/p-vs-np proofs/complexity README + Lean PSubsetNP, blkph0x p-vs-np-proof-research METHOD_INDEX and public proof CDCL baseline, frat-xor, cake_lpr, openai/math ExecCNFNodeSearchCosts and RuntimeAssembly. Original FLMV JACM 2005 inspected. Direct branded Google unavailable.

**NEXT LSPV-2 and LSPV-4:** Give one concrete *both-label* all-input builder, native bit-serial guest input accessor and proof of per-guest-read cost/rate; re-evaluate $t',s'$ with every local phase and a source-consistent join. A materialized original or all-answer cache fails local peak restrictions; compact alternatives remain open. Root `main.tex` unreadable from connector (nonzero blob ID, zero content), so not edited. Route B grammar/B3 and P!=NP remain OPEN. The full Python/JS report and raw fixture are available in the separately generated reproducibility ZIP.
