# LSPV-2/414 Addendum: conditional semantic support acquisition under SAT in P

**November 5, 2026, 03:12 PST.** This addendum does not alter the original R_mix341 rules or assert B3. It strengthens the interpretation of the coNP-completeness result in [the primary LSPV-2/414 report](2026-11-05_0312_LSPV-2_NATIVE_PAID_DEF_SUPPORT_COHARD414.md).

## IDEA: does the new coNP obstacle actually threaten B3?

Hypothesis: If SAT were in P, exact semantic support of any **explicit legal paid binary DEF gate network** could be computed uniformly with polynomial charged acquisition time by a direct SAT-miter construction. Thus coNP-hard support is a verifier/granularity obstacle, not a counterexample to B3 under its own antecedent. Falsifiable prediction: essentiality of each original input is exactly one SAT call on a polynomial encoding of two copies of the network with that one input flipped; remaining output equivalence proof is the genuine missing native transfer.

## SEARCH

The main /414 run read original /341 and /384, current REFEREE359, own /406, Grok and Claude actual assessments, Cook--Reckhow 1979 and Krajicek 2004, and full OpenAI/math `ExecCNFNodeSearchCosts.lean`. Existing literature establishes that simple proof-system existence is not same-R reflection. The following miter construction is an elementary reduction, not claimed as a novel published theorem. Direct Google-branded search unavailable; general indexed web and authenticated Github search used.

## ITERATE: proved conditional local-acquisition lemma

**Theorem 414.3 (PROVED/EXACT conditional, gate-DAG model).** Assume SAT has a **fixed uniform correct polynomial-time decider** A. Given any syntactically legal acyclic sequence D of t separately paid conservative two-input Boolean definitions with explicit encoding E and a designated named Boolean output h, one can compute the exact set S of essential original inputs of h in deterministic time polynomial in E, without assuming any R_mix341 refutation, formalized machine-correctness certificate or semantic oracle. If |S|<=3, one can produce an equivalent explicit Boolean circuit with at most five two-input gates (in the full 16-function binary basis), also in polynomial time.

**Proof.** Only the original inputs appearing in the transitive gate cone of h can be essential; there are at most 2t such distinct input names, irrespective of a very large DIMACS header variable bound. For each such variable x_i, construct a standard Tseitin CNF miter M_i consisting of two copies of the paid gate network, equalities linking every original input except x_i, a disequality forcing the two copies of x_i to be complements, and a disequality forcing the two output bits apart. All gates are two-input total truth tables with constant-size CNF defining constraints. The miter has O(E + t log(E+t+2)) encoded bits after standard indexed serialization. It is SAT if and only if h depends essentially on x_i. Invoking the single correct uniform A on each of at most 2t miters determines S in time polynomial in E, including all parsing, miter writing, input acquisition and output validation. This is a mathematical conditional algorithm, not a proof that A exists.

If |S|<=3, fix all other original inputs to zero, evaluate h on at most eight assignments to S and recover its complete truth table. For three variables y1,y2,y3, write f0(y2,y3)=h(0,y2,y3), f1(y2,y3)=h(1,y2,y3). The Shannon identity

$$
h=f_0\oplus (y_1\land (f_0\oplus f_1))
$$

uses at most five binary gates: two cofactor gates (any two-input truth table), one XOR, one AND and one final XOR. Smaller support requires no more. All outputs are globally equal on **every** original assignment, not merely on models of F. The output record length is polynomial in E and the recorded input IDs. \(\square\)

**Limits:** This produces an equivalent *semantic circuit*, not a source-authenticated native proof that the old and new definitions are interchangeable in every AND3, GF(2), Resolution and LOCAL consumer. In particular, the fixed original /341 does not define an admissible in-calculus equivalence certificate or fresh-name replacement for arbitrary such nets. The required evidence acquisition runtime depends on E, not just N+q when hypothetical uncharged payload bytes exist. The exact same-R B3 implication therefore remains OPEN; the theorem does not secretly assume proof certificates.

**Finite verification reused:** In /414 the 256 examples each had seven original inputs, and the 7*256=1,792 essential-input checks were precisely exhaustive SAT-miter tests (each searched the 128 possible assignments of the two coupled input copies). The independently implemented verifier passed 35,607 aggregate assertions with four damaged records rejected. The two-sided label control is C SAT and C UNSAT; the original F is SAT for every case. This is finite corroboration, not proof of the general conditional bound.

**Next exact native step:** consumer-preserving proof of equivalence within the *unchanged* paid-node calculus. If the only available procedure is to decide semantic equivalence by A as a free premise oracle, that would be circular for native B3. A valid replacement requires an R derivation/certificate with proved polynomial node cost, full source support, checkable typed conversions and paid evidence.
