# LSPV-4 MIXED-131-BITLOCAL-COMPLETION316
**November 1, 2026, 15:36 PST. Circuit Resource Auditor. PROVED/EXACT finite 512-case mixed tile; PROVED/EXACT promised signed-(2,2) to canonical Döcker fixed-slot bit-local reduction; independent computational checks; external review pending. P vs NP OPEN.**

## Universal obstruction and four falsifiers
Earlier FIXED-TILE-PORT-CONGRUENCE314 proved the pure 131-record tile but left the mixed clause tile unauthenticated. This run independently reconstructed the 42-clause signed gadget in Döcker (2019), its three-copy 131-clause composition and checked its *entire* port truth table using independently replayable original-clause evidence. (F1) Mixed tile violates 2P2N monotone quotas: FALSIFIED by exact incidence check. (F2) All 512 port cases implement three original mixed clauses: VERIFIED via 343 checked SAT witnesses and one universally replayable 45-leaf UNSAT subtree for each of 169 bad cases. (F3) Fixed-slot output bits require sorting/materializing output: FALSIFIED on VALID signed 2P2N sources by an explicit per-record virtual output-bit accessor. (F4) A locally accessible signed-to-monotone compiler alone transfers numerical FLMV: INVALID, missing ordinary-SAT first leg and same-machine compiler.

## Authenticated finite gadget theorem
Define the 42 original signed clauses M on 32 internal names x1..x8,y1..y9,z1..z15 and signed ports (+u1,-u2,-u3), transcribed from Döcker (2019) Section 4 and listed in the executable producer in the full reproducibility archive. It begins +(x1,x2,u1), -(x2,x3,u2), -(x2,x4,u3). Take three independently renamed M copies, and add five all-positive bridge clauses:
```
(x1@0,x5@0,x6@0)
(y6@0,z15@0,x1@1)
(x5@1,x6@1,y6@1)
(z15@1,x1@2,x5@2)
(x6@2,y6@2,z15@2)
```
The resulting 131 original-clause-ID records use 96 distinct internal names and 9 signed single-use source ports. There are exactly 65 positive and 66 negative proper monotone clauses. Internal names each have two positive and two negative occurrences. Its existential port truth function is exactly
```
AND for b=0,1,2 of (u[3b+1] OR NOT u[3b+2] OR NOT u[3b+3]).
```
Of 512 possible port valuations, 343 pass and 169 fail. For all 343 passing cases, independent verifier checked the complete 105-bit source-port/internal witness against every one of the 131 gadget clauses. Every failing case falsifies one incoming 1P2N clause; the associated 42-clause M component is UNSAT, verified by the independently replayed 89-node, 45-falsified-original-clause-leaf, maximum-depth-8 exhaustive UP-DPLL tree on 32 original internal names. Since all three M blocks are name-disjoint, the same proof transports by explicit renaming. Complementing all gadget literals yields the 2P1N case, with 66 positive and 65 negative target clauses. SciPy/HiGHS was used only to FIND positive-case certificates, not to verify either label.

## Exact uniform promised-language reduction
For every VALID duplicate-free proper signed exact-(2 positive,2 negative)-occurrence 3-CNF F, including mixed source clauses, let n be its original variable count and m=4n/3 its clause count. Make three independent renamed copies of every source variable; for every original clause j reserve precisely 131 output clause-record slots and 96 fresh internal names. When j is pure positive or pure negative, emit its three copies plus 16 variable-disjoint Y6 blocks, each a valid six-name eight-clause source with 18 satisfying assignments. When j is 1P2N emit the verified 131 mixed tile on three copied source clauses; when 2P1N emit its all-literal-complement. Each original signed source variable has two incidences of each polarity *in each copy*, each internal name is 2P2N, no output clauses duplicate, and all output clauses are monotone proper three-variable clauses. Thus output F' is canonical Döcker Monotone 3-SAT-(2,2), with
```
n' = 3n+96m = 131n,     m' = 131m,
SAT(F') iff SAT(F).
```
If F' has a model, its three original-variable projections satisfy F by the exact port theorem; if F has a model, three copies of it extend independently across mixed gadgets via the 343-case table and pure paddings via Y6. This is Döcker's underlying gadget reduction adapted to uniform fixed-width source-clause slots, not a claim that the general complexity reduction is novel.

An arbitrary target bit at index b lies in the target header or in a record j=floor(targetClauseIndex/131) and a local slot s<131. Read *only* source record j at its indexed read-only input position, compute locally the fixed template clause, namespace, polarity, and output field. Source grammar uses Elias-gamma n,m and signed 3(w+1)-bit clause records; target uses 1+3w' bits/monotone clause, w'=ceil(log2(131n+1)). No prefix sums, sorting or full output copy. Under the declared VALID signed-source promise, bit addressing is polylogarithmic time and O(log N) additional work/index cells on a deterministic indexed-read-only-input TM; the Python functional verifier is **not** a native FLMV full-machine execution. The output length M=Theta(N) for valid source inputs. The full arbitrary malformed-input, near-linear-time low-space grammar validator is **not** certified.

## Independent SAT/UNSAT and extreme controls
The canonical F9 source has exactly 70 SAT assignments. A new signed proper 2P2N source S9 is formed by changing the polarity of x1 in F9's positive clause 0 and negative clause 7, yielding 69 total SAT assignments. On the SAME S9 source, original pins (x1,x2,x3,x4)=(0,0,0,1) have 3 SAT completions, while (0,0,0,0) have 0, with no initially empty original clause; a 32-leaf complete source-clause-false cover verifies UNSAT. All 264 clause-pair extreme SS/SU/US/UU modes, 512 complete assignment-complement identities and six malformed source controls passed. F9 and S9 compile into independent valid canonical outputs of n'=1179,m'=1572 and each complete 1179-bit SAT witness was checked against all 1572 original target clauses. Each output binary string has 53,490 bits. The independent random-output-bit verifier matched EVERY bit on BOTH sources, 106,980 exact comparisons. A deliberately repeated non-cached protocol used 801,720 source-bit reads on 53,448 output-clause field bits; this is **an implementation-specific upper cost**, not a machine-independent lower bound. Separate no-producer-import verifiers passed **45,908** and **20,064** checks respectively. Full 512-port raw data SHA256: `b323cd8d0b22fdb4ca9541aff0a09cffec70456ab02cc74a4a21197b85bca480`. Certified U198 UNSAT/V198 SAT are inherited project controls, NOT replayed this run.

## Complete charging and numerical FLMV firewall
Per executed adaptive state z, actual controller work must include grammar, original source reads and bit-address preparation, source/index-head motion and atomic index erasure, all attempted policy discovery/selection/switch/failure, triangle/K4/matroid/GE proof and verification, memoization, replay and ancestor retention, child translation/output-bit access, guest DELAY/COPY/RECOMP, and outputs:
```
W(z) <= C_grammar,source,index,head(z)
      + SUM_ATTEMPTED_POLICY C_acquire,select,switch,fail(z,policy)
      + C_GE,matroid,proof,cache(z)
      + SUM_EXECUTED_CHILD(C_encode,child,bit,guest(z,y)+W(y)).
```
Peak space is the maximum *simultaneous* writable/index/ancestor/guest/cache/matrix/proof/child state. Read-only input and write-only output are space-exempt only under the exact FLMV model; output WRITES cost time and a write-only output is not later readable as guest memory. Full child materialization on a writable tape is counted. Logical XOR is offline diagnostic, not a universal hardness measure.

At hypothetical canonical solver exponents (K,L)=(6/5,1/2), FLMV Theorem 5.7 reference (c,d)=(241/200,11642479/23232400) has strict margins 1/200 and 26279/23232400. A FULL ordinary-SAT-to-canonical bit-local compiler with combined length exponent a and multiplicative access exponent rho still needs (6/5)a+rho <241/200 and a/2 <11642479/23232400, plus setup, grammar, extra peak space and guest simulation conditions. This verified SECOND LEG has b=1 and polylog virtual bit addressing on valid signed quota sources; the needed first ordinary-SAT-to-signed proper exact-(2,2) leg, unknown-exponent arbitrary A->Phi(A), and uniform all-input polynomial total-work controller remain OPEN. NP-completeness alone does NOT transfer the numerical FLMV region.

## Source literature / corpus audit
Read first integrated 01:48 handoff and 01:44 saturated-cycle theorem, newest LSPV-1..5 reports and coordination issue #3, AGENTS.md, CODEX.md, pnp-research skill and root metadata. Required project search and independent GitHub openai searches performed. Primary literature DOI FLMV 2005 10.1145/1101821.1101822 and Döcker 2019 arXiv:1912.08032 reviewed visually at PDF pp. 5,6,10 (gadget) and FLMV paper model page 4. Further sources Berman/Karpinski/Scott ECCC TR03-049 and McKay/Manlove 2024. Prior LSPV-4 FIXED-TILE-PORT-CONGRUENCE314 already constructed pure slots, prior project OUTPUT-USE-TRILEMMA170 warns write-only output cannot be free guest work. The new result closes **that specific finite mixed-gadget verification gap**, not the all-input proof barrier. Full executable producer, two independent no-import verifiers, complete 512-case raw JSON, source/compiled originals and SAT/UNSAT proof certificates are in the conversation reproducibility ZIP. GitHub readback and issue #3 documented independently. Root `main.tex` not overwritten through empty Contents response.

**Status: PROVED restricted signed exact-(2,2) promised-input compiler; independently COMPUTATIONAL full gadget certificate; P versus NP OPEN.**
