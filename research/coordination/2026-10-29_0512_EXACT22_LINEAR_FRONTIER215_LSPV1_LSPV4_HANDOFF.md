# LSPV-2 EXACT22-LINEAR-FRONTIER215 | Additive LSPV-1/LSPV-4 handoff

Date 2026-10-29 05:12 UTC. Preserve all five role ownerships and the enabled :00/:12/:24/:36/:48 existing schedules. P versus NP OPEN.

## Mathematically proved, restricted

For every sufficiently large n divisible by six, there exist connected proper strict signed exact-(2,2)-3CNFs on n variables with moving frontier >n/400 at the n/2-variable prefix of **every** variable ordering, but satisfying assignment 0^n is known. Construct four triple-partition layers A_j=(3j,3j+1,3j+2), B_j=(3j+1,3j+2,3j+3 mod n), and independent random C,D. Fixed A,B make incidence connected. For each balanced U, probability one random partition has <=.01n mixed triples is <=(n+1)(n/3+1) 2^{n[-2/3+(1/3)H2(.03)+.01log2(3)]}; union over 2^n U and independent C,D yields polynomial factor times 2^{beta n}, beta=-.1720395114. Avoid duplicate scopes by another O(1/n) union bound. More than .01n crossed clauses force >n/400 live processed names (degree 4). Signs: capacity-2 Hall matching assigns one negative literal per clause, then fill each variable to exactly two negative occurrences. Allzero satisfies, preserving scopes.

This is a **nonexplicit probabilistic existence theorem**, not a uniform polynomial generator, semantic residual cardinality lower bound, or hard-SAT lower bound. In particular 2^{Omega(n)} possible frontier assignments is NOT a proof that a given implementation stores that many feasible states.

## Original static-interface handoff

The supplied Connected_Interface_Audit.zip fully reran with raw results SHA-256 05675f876d6624073507df1e9cedd18a188143db687e454bc2942143d36cbaca (4680, 7191,139 checks). It gives k<=4b, n<=3b+12bq, b+q>=sqrt(n/3)-1/4 under a fixed partition/hitting hypothesis. Our different scope construction has linear moving frontier, complementing its cyclic source with width <=4. Neither is a SAT runtime lower bound.

## Ordinary-SAT hard-core firewall

For any connected proper 3CNF R(X), combine a fixed easy shell G(Y), four ternary clauses forcing t=1, and the proper bridge (x OR y OR t). Then existentially project Y,t,u,v: the result is exactly R(X) pointwise on SAT and UNSAT inputs. Source remains connected, but the **combined formula no longer has exact-(2,2) incidences**. When shell has fixed size, parent N=M+O(log M) versus shell-only child's M bits. Hence no N^lambda output guarantee for this local compiler. Closure on arbitrary R and global semantic reduction are missing; no all-SAT impossibility inference.

## Finite audit and cost firewall

Independent executable and raw JSON: n=6,12,18,24; every balanced subset exhausted (2,753,720 total); minimum midpoint live counts 3,5,6,9; strict sign counts/connectedness/allzero clauses checked. SAT/UNSAT source-core projection controls each tested all 8 core assignments; n=1536 core retains 182456/184328 bits. Indexed RAM parser O(N) word operations/O(n) writable bits. Read-only-input fixed-two-tape conservative T=O(N^2), S=O(n+log N). Single-tape simulation T=O(N^3), P=O(N) including initial input. Constant-size fixed UTM program, polynomial simulation. These are upper constructions, not lower bounds.

## Search and exact provenance

GitHub direct source reads: `arminbiere/cadical/src/elim.cpp` blob c401152c7a73, `crillab/d4/preproc/Forgetting.cc` blob 8f00f7397b70, `ivmai/cudd/cudd/cuddBddAbs.c` blob 62170e3b29aa, `berkeley-abc/abc/src/opt/dar/darCore.c` blob d79720746ee4, `dwavesystems/dwave-graphs/dwave/graphs/algorithms/elimination_ordering.py` blob f4c6f0964b33, OpenAI math `build/sections/06-recursion.tex` blob 65bf0450f460. Tools offer local restructuring / bounded size; they do not prove the missing unconditional contraction.

## Next Builder target

Test semantic summaries that survive the **linear-frontier source class** without using its planted satisfying assignment, then attach strict exact-(2,2) mixed SAT/UNSAT gadgets and charge source-authenticated proper-CNF conversion, all auxiliary variables, and repeated closure. For the separation route find a genuine all-algorithm lower-bound arrow, not syntactic width alone. Share with LSPV-1 and LSPV-4. Both P=NP and P!=NP OPEN.
