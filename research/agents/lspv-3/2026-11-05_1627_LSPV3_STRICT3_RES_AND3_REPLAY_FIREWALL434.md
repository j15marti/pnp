# LSPV-3/434 | Strict-3-CNF RES-to-AND3 exact-replay firewall
**2026-11-05 16:27 PST. Route B. PROVED/RESTRICTED semantic rule-level counterexample; COMPUTATIONAL verification; historic byte-checker acceptance, full mixed transfer, B3, P versus NP OPEN.**

## IDEA and four falsifiers
Try extending previously PROVED LSPV-3/433 complete signed-padding ordinary-Resolution lower-bound transfer into a zero-extra-node mixed compiler: restrict all dummy inputs, replace disappearing Resolution lines with stronger surviving clauses, and replay downstream AND3 exact GF(2) annotations without changing them. Falsifiers: (1) invalid proper-three source; (2) illegal historical semantic rule step; (3) changed truth-table equivalence after RES strengthening; (4) independent short legal proof showing failure is compiler-specific, not general hardness. Exhaustive checks exclude (1),(2) and establish (3),(4).

## Established family and source model
de Rezende, Nordström, Risse, Sokolov, CCC 2020 DOI 10.4230/LIPIcs.CCC.2020.28: exponential shared DAG **Resolution** length for specified sparse graph-PHP expanders. Graph PHP uses variables x_pj for permitted pigeon-to-hole edges, one positive pigeon disjunction per pigeon and negative binary collision clauses per shared hole. Only published members with suitably verified degree <=3 fit /433's direct width<=3 padding theorem. Their hardness is not proved for full Rmix341, where Cook ER/Buss Frege and paid-definition shortcuts are explicit controls. Cubic odd Tseitin similarly has historical Rmix341 linear GF(2) proofs. The following small minimally UNSAT control is solely a targeted compiler falsifier, NOT an invented claimed hard family.

Prior LSPV-3/433 proved ordinary Resolution
$$
L_{\mathrm{Res}}(F)\le L_{\mathrm{Res}}(\operatorname{Pad}_3(F))
\le L_{\mathrm{Res}}(F)+m_2+3m_1+7m_0.
$$
No reverse inequality was proved for arbitrary mixed proofs.

## Strict source and exact 13-node semantic refutation
Start with $F=(u)\land(\neg u\vee v)\land(\neg u\vee\neg v)$. Apply /433's **fresh-per-clause** complete signed dummy padding: original variables u=1,v=2 and fresh z=3,w=4,t=5,s=6. The exact strict source header is p cnf 6 8. Its eight free source clauses:
S0=(u,z,w); S1=(u,z,-w); S2=(u,-z,w); S3=(u,-z,-w); S4=(-u,v,t); S5=(-u,v,-t); S6=(-u,-v,s); S7=(-u,-v,-s).
All eight source clauses have three distinct variables and are individually essential (deletion SAT witnesses); the strict source agrees pointwise with F for all 64 full assignments.

The following paid nodes each have <=2 explicit parents, under the **printed semantic** RES/AND3/XOR rules in historical LSPV-2/341, unit weight per distinct DAG node:
1. R1 RES(S0,S1,w) = u OR z;
2. R2 RES(S2,S3,w) = u OR NOT z;
3. R3 RES(S4,S5,t) = NOT u OR v;
4. R4 RES(S6,S7,s) = NOT u OR NOT v;
5. R5 RES(R2,R3,u) = NOT z OR v;
6. R6 RES(R1,R5,z) = u OR v;
7. A7 AND3(R6,R4) EXACT factor equivalent to u XOR v =1;
8. R8 RES(R1,R2,z) = u;
9. R9 RES(R8,R3,u) = v;
10. A10 AND3(R8,S0) EXACT factor u AND (u OR z OR w) = u, annotated u=1;
11. A11 AND3(R9,R3) EXACT factor v AND (NOT u OR v) = v, annotated v=1;
12. X12 XOR(A10,A11) = (u XOR v)=0;
13. X13 XOR(X12,A7) = 0=1.

AND3 combined original-variable supports are {u,v} for A7,A11 and {u,z,w} for A10, satisfying the original <=3 bound. Every annotation was independently exhaustively checked for exact Boolean equivalence on the full support, not merely source models. Shared inference DAG critical-path span is 6. No DEF or LOCAL rule was assumed. **The historical /341 byte grammar for ports/facets remains incomplete; this is NOT an authoritative parser-accepted certificate.**

## Exact failure of verbatim replay under a signed padding restriction
Set z=w=t=s=0. Only S0, S4, S6 survive, giving the exact unpadded F; the remaining source rows become TRUE. Restricted R1 is u; restricted R5 is TRUE; the nominal restricted R6 clause is u OR v. Standard Resolution restriction can only carry inherited *stronger* u at that position: the old z pivot is gone. If one replays A7 with this stronger parent and unchanged R4, one obtains
$$
u\land(\neg u\vee\neg v)=u\land\neg v
$$
whose truth vector on (u,v)=(00,01,10,11) is (0,0,1,0), while the exact old A7 GF(2) row u XOR v=1 has (0,1,1,0). The assignment (u,v)=(0,1) is a discriminator. Semantic equivalence merely on UNSAT original models is vacuous and is not sufficient to preserve exact derived-factor provenance. Hence **verbatim unchanged AND3 annotation following ordinary RES subclause-strengthening is unsound**. This neither refutes alternative retyped compilers nor establishes mixed-proof lower bounds.

A fully legal alternative has two original-source Resolution inferences: RES((NOT u OR v),(NOT u OR NOT v),v) yields NOT u; RES(u,NOT u,u) yields empty. Because all 3 unpadded source clauses are individually essential and paid inferences have at most two premises, the ancestry lower bound gives >=2 nodes. Therefore **W_Rmix341(F)=2** exactly. The 13-node construction itself is only an upper-bound witness for padded F.

## Verification and resource accounting
Python producer 1,289 assertions plus all 8 deletion witnesses; independently implemented JS 156 checks and four hostile rejects; standalone dependency-free JS 152 checks, 4 deliberately broken proof conditions and 5 malformed strict DIMACS inputs rejected. All 64 complete assignments, exact source and row semantics checked. Measured Python peak RSS 96,544 kB and independent JS 29,812 kB are host-program measurements, not certified asymptotic TM bounds. Distinct proof nodes=13, ideal parallel span=6, exact original minimum=2. Explicit bits, source/index reads, pivot and truth-vector checks, GF(2) mask operations, output and cache/recomputation need physical charges for algorithmic time/space; no such runtime lower bound follows.

Read original /341 blob c87acd11, prior /433 blob 561c4da2, REFEREE360 blob 8719eba6, issue #3 through LSPV-2/429 and LSPV-5/372, AGENTS/CODEX/repo skill, Grok 2026-11-05 03:15 report, actual Claude TPORT-0002. Required new repo checks: konard/p-vs-np proofs/experiments/README.md blob 4c8752aa states admitted/sorry gaps; blkph0x/p-vs-np-proof-research METHOD_INDEX.md blob 18d693ea maps scoped results only. FRAT-XOR format.md blob 986a21aa describes explicit XOR proof IDs/checker trust boundary; cake_lpr README blob e94f45e9 identifies formally verified LPR checker. Primary CCC2020, Ben-Sasson/Wigderson, Cook ER, Buss Frege references reviewed. Indexed web used; direct Google-branded interface unavailable. Duplicate search found no identical private-padding RES-to-AND3 case, not a novelty claim. Root main.tex complete content unavailable from connector; not edited.

**NEXT:** Prove a polynomial, source-authenticated TYPED repair of arbitrary mixed RES-strengthening -> AND3/GF(2) consumers (including shared DAG and nonzero context), or exhibit a precisely stronger legal failure; then settle historical LOCAL/DEF/export facets. Full mixed lower bound, B3 and P versus NP remain OPEN.

## Addendum 434A: Exact paid-node minimum for the same source

**PROVED/EXACT finite result, all permitted rules:** All eight strict source clauses S0..S7 are individually essential, as independently enumerated, and every paid inference has at most two dependencies. The connected source-ancestry counting lemma therefore forces **at least 8−1=7 paid derived nodes** in *any* sound conservative original-source-authenticated historical Rmix341 proof, even with sharing, GF(2), paid definitions and arbitrary legal branching. A matching **seven-node original-source Resolution refutation** exists:

1. R1: S0,S1 resolved on w yields (u OR z).
2. R2: S2,S3 resolved on w yields (u OR NOT z).
3. R3: S4,S5 resolved on t yields (NOT u OR v).
4. R4: S6,S7 resolved on s yields (NOT u OR NOT v).
5. R5': R1,R2 resolved on z yields (u).
6. R6': R3,R4 resolved on v yields (NOT u).
7. R7': R5',R6' resolved on u yields empty.

The unpadded three original clauses all are individually essential, yielding the lower bound two, matched by two Resolution steps. Therefore

$$
\boxed{W_{R_{\mathrm{mix341}}}(\operatorname{Pad}_3(F))=7,\qquad W_{R_{\mathrm{mix341}}}(F)=2.}
$$

The exhibited 13-node mixed proof is **not shortest**, yet its exact-annotation replay obstruction remains valid and testable. This is not a growing superpolynomial family or a B3 theorem. Updated standalone code checks the seven-node matching proof; producer Python 1,292 checks, separate JS 157 and standalone published JS 153.
