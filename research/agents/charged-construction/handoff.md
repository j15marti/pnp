# charged-construction handoff
Updated 2026-11-21 09:32 PST, America/Los_Angeles.

Current report: [T5-FULL-EQUALITY-SPLIT1](PNP_Charged_construction_2026-11-21_093200_Full_Domain_Equality_Split.md).
Recovery head d18f513e02a053db9d30ee7172ee516834c152d3. Supersedes the bounded-occurrence limitation of the [08:39 report](PNP_Charged_construction_2026-11-21_083900_Three_Color_Private_Leaves.md), not its weighted-count warning. Original construction commit 358200a519d8cd27b33a02a12bb1b6b7db24a825 and evidence recovered.

PROVED/EXACT; independent review pending: full-domain equality Q(U,V) uses a five-variable frame with b0=U plus C(b4,V,b1). Four fresh auxiliaries, six C-clauses, exact interface 2*[U=V]. Ports have degrees 3 and 1. No input constants/equality or forced endpoint domain.

For ANY strict symmetric-C input F, n declared variables, m clauses, u used variables, copy each of the 3m occurrences and connect each variable's copies in a path of Q gadgets; retain unused variables. E=3m-u, n'=n+15m-5u, m'=19m-6u, max occurrence5, Z(D(F))=2^E Z(F). Both SAT and UNSAT preserved. Exact original gamma/unary/fixed-ID encoding: generally N'=O(N log(N+2)), not universally O(N). Ordered R transfer by two clauses preserves count but max occurrence becomes TEN.

Apply to prior graph image H_G: E=10+3v+2e, n'=55+18v+11e, m'=65+20v+13e; N'=Theta(N_H). SAT iff G is three-colorable. Count is 2^E times the prior weighted count; not a fixed multiplier of unweighted #3COL. Graph input M_G must also be tracked (isolates can create log growth).

COMPUTATIONAL: all15625 gadget assignments; ten frames;28 compiler cases (all16 four-variable clause subsets; unused, duplicate, zero-variable, attained-degree5, six graph and two rename cases);125 reflection tuples;5 malformed strings rejected. Target counts use exact local interface contraction, NOT full target brute force. Code experiments/t5_construction_occurrence5_20261121.py; raw results/raw/t5_construction_occurrence5_20261121.json. No old1100-graph experiment repeated.

Uniform scanner compiler has conservative sole-tape T=O(U^4), physical S=O(U), physical CM=O(U^5), U=N+N'+2; counters/address motion/parsing/authentication/output paid. Python is the semantic reference, not instrumented physical runtime. Composed solver adds compiler cost; a fixed target cap exponent is not preserved for free.

Legal equality contraction and private-leaf elimination recover the arbitrary graph core. Equality paths themselves are FALSIFIED/RETIRED as a compulsory hardness source. Trees, matching and affine sources retain cheap solvers; bounded occurrence or represented extensions do not prove unrestricted demand.

ONE next dependency to Accounting, Redteam review and Synthesis tracking: T5-BOUNDED-3COL-DYNAMIC1. Fix B_G distribution and solver/cap; identify actual obligations after equality contraction, leaf elimination, global algebra, caching and relocation, and prove demand >brK(N_B)^a or falsify. No such compulsory demand yet. Review requested especially for equality fibers, occurrence/unused-variable ledger and input-regime comparison.

Fresh primary literature: STACS2010 Dyer/Goldberg/Jalsenius/Richerby section4 equality simulation (Boolean, pinned, approximation; not directly imported). Fresh official Anthropic/OpenAI/xAI/Google/Research/DeepMind searches, ownership checks, source scopes and revision pins recorded. No external theorem/kernel build assumed.

No TMR manuscript edits, schedule changes, local checkout/preflight or LaTeX build. P versus NP OPEN.
