# LSPV-4 AFFINE-MATCHING59 handoff, 2026-10-23 20:45 KST

**P versus NP OPEN.** Source-aware restricted theorem, no superpolynomial SAT lower bound.

## Literal-splitting endpoint
For arbitrary proper 3SAT input Phi over n0 variables with k ternaries, introduce paired variables p_i,m_i with (p_i OR m_i) AND (not p_i OR not m_i). Map each positive source x_i to positive p_i and each negative source not-x_i to positive m_i. Every source ternary is now all-positive. Output n=2n0, m2=2n0, k=m3; N=(8n0+4k+2)ceil(log2(64(4n0+k+1))). Matching-pair constraints are independent 2-variable XOR equations. The map is parsimonious, linear-record, answer-blind and invertible on valid grammar. The unrestricted language is NP-complete via known proper 3SAT; the two constituent constraint types are separately easy.

## Source-preserving 2SAT-chain lift
For q>=1 add three underlying variables t,a,b and their complement pairs. Add four all-positive ternary guards (m_t OR signed-a OR signed-b), one per sign combination; they force t=0 while leaving a,b free. Replace each source binary (l1 OR l2) by positive ternary (Y(l1) OR Y(l2) OR p_t). Output n=2q+12, m2=2q+12, k=q+8, m=3q+20, N=(12q+82)ceil(log2(64(5q+33))). SAT iff some chain orientation b_i=0. There are four extensions per source witness. On the all-ones UNSAT input, changing any b_i flips label and alters ONE distinct ternary literal-identifier word; hence every total deterministic exact full-language decider reads at least q cells in the declared word-RAM model. A source-aware O(q) scan matches this. No superlinear or superpolynomial post-acquisition lower bound.

## Source-visible pure-polarity bypass
Mark pair i bipolar if both p_i and m_i occur in ternaries; let p be the count. Assign every other appearing pair's unique cited literal true and delete satisfied clauses. The exact remainder uses at most p underlying Boolean variables; decision O(2^p poly N), paid parse O(n0+k), witness lift O(n0+k). All Boolean output variables nevertheless have both signs in the binary matching scaffold. A syntax-only pure-literal test is blind. p=Theta(n0) is at best a necessary condition to defeat this one bypass, not a hardness guarantee.

## Independent checks, status and delivery
Full local audit: 6,953 assertions, 0 failures, seed 2026102359. Repository mini reproducer gives a smaller exact test subset. Both labels checked: q=1 chain; odd/even XOR cycles; eight-cube full UNSAT versus same-count single-sign-flip SAT. Other controls: 2SAT, padding (free y), affine, Horn, independent components, source-readable witness and strong backdoor. Full report contains the resource ledger and proof.

**Role 5:** independently verify paired grammar, 4-clause guard, q disjoint modified words, and bipolar-kernel source correctness.
**Roles 1-3:** use q=3,8,64 lifted chains and eight-cube matched controls; test any claimed charged universal compression or continuation lemma against the O(q) source scan.
**First candidate amplification:** increase bipolar interaction while charging parsing, affine propagation, compatibility, caching, all failures and witness replay. No mandatory 2^p or 2^k inference.

Status: PROVED/EXACT restricted theorems; KNOWN THEOREM NP-complete endpoint; COMPUTATIONAL finite audit; FALSIFIED/RETIRED mandatory enumeration; OPEN universal worst-case superpolynomial time and P versus NP. Five existing schedules unchanged.