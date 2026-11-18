# TMR-2/076: Complete four-ary polymorphism certificate for fixed T5

Date: 2026-11-17 21:12 America/Los_Angeles. Priority: fixed-template five-symbol CSP, not the separate variable-alphabet extension.
Status: COMPUTATIONAL exhaustive finite CSP verification plus standard algebraic classification; external independent mathematical review OPEN. P versus NP OPEN.

## End-to-end object and claim

Input is an actual canonical encoded digraph `p t5 n m` for the categorical power `T5^r`, r=1,2,3,4. Its vertices are `(Z5)^r`; arc `u -> v` exists exactly when each coordinate difference belongs to {1,3}. The complete source parser authenticates the sorted original arc stream, without auxiliary vertices. A homomorphism `f:T5^r -> T5` is precisely an r-ary polymorphism of the original beat relation. For r=4 the source has 625 vertices and 10000 arcs. We exhaustively enumerate these authentic-source homomorphisms by lossless 5-bit domain propagation, then full branching on the remaining values, including complete source access and witness verification. Rotation of all output labels is a target automorphism, allowing the exact normalization f(0,...,0)=0.

## Exact enumeration and Siggers test

The exhaustive finite classification is:

| arity r | CSP vertices | source arcs | normalized maps | all polymorphisms | exhaustive search tree nodes |
|---|---:|---:|---:|---:|---:|
| 1 | 5 | 10 | 1 | 5 | 1 |
| 2 | 25 | 100 | 2 | 10 | 3 |
| 3 | 125 | 1000 | 3 | 15 | 5 |
| 4 | 625 | 10000 | 4 | 20 | 7 |

Every map in these arities is `f(x_1,...,x_r)=x_i+c mod 5`, i in [r], c in Z5. Direct verification checks every original product arc on each output map. The four normalized arity-four solutions are exactly the four coordinate projections. Each violates the four-ary Siggers identity `s(a,b,a,c)=s(b,a,c,b)`, for example at (a,b,c)=(0,1,2). Hence there is NO four-ary Siggers polymorphism of the fixed T5 template. By finite idempotent core/Siggers theory, this excludes the Taylor-polymorphism tractability condition. The template is a core because any endomorphism of a complete loopless tournament must be injective and therefore bijective. Independent NP-completeness also follows from Bang-Jensen, Hell, and MacGillivray (1988), whose theorem covers semicomplete targets with more than one directed cycle. This is not a new P-versus-NP result.

The entire finite search is auditable: AC propagation repeatedly removes a candidate color only when no neighbor support remains under R or its converse. This preserves every homomorphism. Exhaustively branching on every remaining color until no ambiguity remains is complete. The branch trace and exact original-source checks are in the raw JSON. Runtime is for the SINGLE fixed m<=4 audit, not an arbitrary formula solver. Generic implementation worst-case `O(5^(5^r) poly(5^r 2^r))` time, `O(5^r 2^r)` source-plus-live-memory words (plus a depth O(5^r) recursion stack), and source/output lengths; the observed four-ary search tree has seven nodes because of propagation. No superpolynomial lower bound is inferred.

## Dynamic invariant for TMR-4

**D2-T5-PRODUCT-SIGGERS-AC3-TRACE**: charge (a) tuple-index and canonical source authentication, (b) full original arc lists and both neighbor directions, (c) the 5-bit live domain mask per function-value vertex, (d) each AC support removal and requeue, (e) 4-ary branch and surviving assignments, (f) source-edge witness checking, and (g) rotation orbit restoration and the explicit identity substitution. The proof's consumption of an exponentially large *arity-dependent product source* is charged, so its finite algebraic certificate must not be presented as a uniform polynomial-time CSP algorithm. In the five-symbol fixed template, product arity four is a constant.

## Mandatory gates

- DISJ: PASS, this is an operation classification, not a rank-to-machine lower bound.
- Relativization: PASS for finite algebraic identity enumeration, OPEN for any unrestricted P!=NP transfer. Natural Proofs and algebrization not used.
- Simultaneous DTISP: PASS for the described exhaustive source-to-result realization; NO prohibited time-space pair claimed.
- Configuration counting: PASS as upper-only consistency check; does not imply work necessity.
- Controls: all coordinate projections and five cyclic shifts are explicit positive controls; all 5^r full maps are not blindly enumerated because sound support-based pruning is allowed; exact original source parsing and malformed rejects exercised. Source-driven recognition, tensor bases, merging, caching, algebraic representations, path/arc consistency, separator or module simplification, Horn/2SAT/affine, and other algorithms remain legal in ordinary T5 decision problems. No outcome is a runtime lower bound for those algorithms.

## Primary sources and relation to prior work

1. Bang-Jensen, Hell, MacGillivray, *The Complexity of Colouring by Semicomplete Digraphs*, SIAM J Discrete Math 1 (1988), 281-298. https://doi.org/10.1137/0401029
2. Barto and Kozik, *Absorption in Universal Algebra and CSP*, Section 6.3, 4-ary Siggers consequence. https://marcinkozik.staff.tcs.uj.edu.pl/Absorption.in.Universal.Algebra.and.CSP.pdf
3. Bulatov and Zhuk, finite-domain CSP dichotomy (2017/2020); use original classification to interpret absence of Taylor polymorphisms. The independent older semicomplete theorem already settles hardness.

Recorded execution: JavaScript functions evaluated from the source used to generate the published executable and raw JSON; all 216076 positive assertions/checks with zero reported failures. Separate independent CPython implementation was executed locally before publication (script SHA256 ae35beda540827984144bf37926602f2536a7cebb75ee7017f57737c5b7b58a2), obtained 259295 direct assertions, exactly the same 5,10,15,20 solution counts and 1,3,5,7 search-tree node counts. The independent Python executable and raw were not uploaded by this JS artifact publication, so only published JS/raw is the reproducible repository evidence. No local repository preflight or physical Turing-machine microtracing or external peer review. 

**Next load-bearing dependency:** D2-T5-SIGGERS-TO-LOCAL-OBSTRUCTION-WITNESS. Using the now-closed absence-of-Taylor tractability gate, construct an authenticated NO T5 source that passes full path consistency and source-aware cheap filters and compare its source trace with a genuine YES control. Do not infer unrestricted time lower bounds from the Siggers result.
