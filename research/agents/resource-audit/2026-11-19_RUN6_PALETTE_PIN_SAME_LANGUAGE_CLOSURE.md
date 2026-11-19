# Resource audit RUN6: one-clause relative pins, original-C same-language closure
2026-11-19 Pacific. P vs NP is **OPEN**. New theorem **PROVED**; exhaustive checks **COMPUTATIONALLY VERIFIED**; full uniform resource transfer **OPEN**.

## Theorem
Canonical strict C has colors Z5, R(a,b) iff (b-a) mod5 in {1,3}, and C is the directed 3-cycle in either orientation (30/125). All physical C clauses have three distinct variable names. Historical Q/P/S are different.

Introduce fresh palette variables p_0,...,p_4 and five original-C clauses
P(p)=AND_(i in Z5) C(p_i,p_(i+1),p_(i+2)).
There are exactly ten palette satisfying assignments, p_i=s*i+t mod5 for s in {1,-1} and t in Z5. This is verified by exhaustive enumeration of all 5^5 cases using the exact original C and independently by unordered cyclic consecutive triples.

For any c in Z5, the **single** original-C clause PIN_c(v;p)=C(v,p_(c-1),p_(c+1)) holds under a valid palette frame iff v=p_c. The palette positions c-1,c+1 are pentagon-distance two and have exactly one color completing a consecutive strict-C triple.

Let F be any nonempty m-clause strict-C block, Z its shared variable names and eta:Z->Z5 **any** fixed color assignment. Retain all m original clauses, add P(p), and add PIN_(eta(v))(v;p) for **each occurrence** of a shared variable v in every original clause, including duplicates. Call the result H(F,eta).

**For every F, Z, eta:**
  SAT(H(F,eta)) iff EXISTS x F(eta,x).
If F has no isolated names, exactly #SAT(H)=10 * #private extensions of F(eta,.) (the inverse palette frame projects the private variables). The physical expanded source has at most **4m+5 C clauses** and only five fresh names. All triples have distinct variable names. Duplicated pins avoid a dedup dictionary. One output record is computable from O(1) indexed source clauses plus eta read(s), in O(log N) auxiliary index bits and polylog bit operations **conditional on authenticated random access to source records and eta**.

**Necessary distinction:** an *absolute* unary pin v=0 cannot be pp-defined by unpinned C alone, since pp-definitions are D5 invariant. The palette reduction does not break D5: it rehomogenizes the absolute assignment as a 10-orbit frame. It also destroys physical clause criticality (duplicate pins) and growing incidence girth (palette incidence 4-cycles), so it does not transfer restricted-family lower bounds.

## Fully reproducible independent checks
Pure Python, no seed, two independently coded C predicates:
- 125/125 original-C tuples matched; exactly 30 true.
- Exactly 10/3125 palette frames, all dihedral.
- 250/250 uniqueness tests for PIN_c.
- All 6^3=216 pin patterns of C(a,b,c): 106 SAT, 110 UNSAT, exact 10-to-1 model count (sum 240 pinned, 2400 expanded).
- Six additional pin patterns of C(a,b,c) AND C(a,b,d) passed 10-to-1 count.
- 19,525 numerical controls of the aggregate child-cost inequality.
Script SHA256 be3ff8f0fae216d232389b0327b58081e84e1e4ff9ac48f6772e5e69981e9a9d; independent replay SHA256 1bdb85593175df58f5e2ba2e47a5787e715408bed01017bcdd26c147652d69c7; results JSON SHA256 629dee8abc7f0112616c81cd589d13a80cdee9a2deeb7ecf0bf20148456155dc. Full scripts, JSON, REPORT, HANDOFF and SHA256SUMS in user-facing archive T5C_Resource_PinnedClosure_Run6_20261119.zip, archive SHA256 3e17e35757ae940e9600d5f61b679c25c3e6daa1d814aa471bc133db473f73ea.

## Resource frontier (arithmetic proved, algorithm conditional)
N is bit-encoded source size; R<=N^.195 rows, B<=N^.65 blocks, p_j<=N^.35 private variable names. Let m_j be original physical clauses in block j. The translated source length is <=4m_j+5 clause records, sum_j <=4M+5B. **A private variable cap does not imply** each child has <=N^.35 encoded bits.

If actual complete child bit lengths L_j obey sum_j L_j<=N^(1+o(1)), max_j L_j<=N^(gamma+o(1)), with complete child runtime L_j^(a+o(1)) for a>=1, then
sum_j L_j^a <= (max_j L_j)^(a-1) sum_j L_j.
Thus R full scans cost N^(1.195+gamma(a-1)+o(1)) **plus** row generation, source access, BOTH polarities, failed trials, certificate materialization/replay, output. At gamma=.35 this equals N^(.845+.35a), so target N^1.33 requires a<=97/70. At gamma=.4 need a<=1.2125; at gamma=.45 need a<=1.07777... . Child peak space L_j^s requires gamma*s<=.5, and every parent buffer, read-only-source abstraction, row value access, and stack must be charged.

Correctness UNSAT: FORALL z EXISTS j FORALL x_j NOT F_j(z,x_j). SAT: EXISTS z FORALL j EXISTS x_j F_j(z,x_j). The theorem only converts the **local pinned decision**. It does not discover an all-z symbolic cover, generate a source-authenticated row or certify even one negative block. An index j(z) is not its UNSAT proof. A deterministic one-sided specialist that is sound on all instances and complete by a known time on *every target-polarity* instance becomes a full decider by timeout. Supplied k-bit nondeterministic paths may require 2^k checked attempts; universal alternating branches must not disappear.

## Exact published comparison, no overreach
Buss & Williams, Computational Complexity 24 (2015) Figs 8.2-8.3: deterministic SAT not in the paper's DTISP(n^1.34070,n^.5) at this certified point, 44 search rounds and 406 retained triples. Their DTISP convention includes n^(c+o(1)) time and n^(epsilon+o(1)) space. Williams 2006 Cor. 2.3 requires each bit of the reduction to be locally computed in n^o(1) time in the target machine model. Repo candidate fixed-width 3-CNF->C compiler is research/agents/proof/2026-11-19_LOCAL3COL_C_SOURCE_ACCESS_RESOURCE_FIREWALL.md. Exact SAT source encoding and machine-model adapter remain unresolved. Restriction-promised high-girth C does NOT inherit a general SAT lower bound, nor does a simultaneous bound prove P != NP.

**Next blocker:** independently demonstrate source-indexed access to eta and scattered blocks *on each child polarity* with complete verified output in N^.5 peak writable space, then build the missing uniform all-z selector. Test native 25-clause critical and 149-variable incidence-girth-10 sources. Do not claim a proof of P vs NP.

References: (1) Buss-Williams 2015 https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf ; (2) Williams 2006 https://people.csail.mit.edu/rrw/sat-journal-final.pdf ; (3) repository resource-audit RUN5 and proof-lead LOCAL3COL-C1.