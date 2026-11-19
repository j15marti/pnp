# Resource audit: dihedral-orbit blocker-capacity theorem and source-scan firewall

**2026-11-19. PROVED a new structural theorem, COMPUTATIONALLY VERIFIED exact finite controls. P vs NP remains OPEN.**

## Theorem (PROVED)
Let F(z,x_1,...,x_B)=AND_j F_j(z,x_j) be physically clause-minimal UNSAT over strict C, with pairwise disjoint private variables and every block containing a physical clause. Define D(z,j)=1 iff F_j(z,.) is unsatisfiable. Every physical clause deletion witness for block j provides a row z_j for which D(z_j,j)=1 and D(z_j,i)=0 for all i!=j. Because strict C is invariant under the ten maps a -> +/-a+t in Z5, the full D5 orbit of z_j consists of unique-blocker rows for j. These orbits must be distinct between block indices. By Burnside's lemma, for q=|z|>=1,

B <= number of D5 orbits on (Z5)^q = (5^q+5)/10,

and q >= ceil(log_5(10B-5)). For q=0, B<=1. This strengthens the previous B<=5^q result even for dynamic blocker selection, but establishes NO time-space lower bound.

**Exactly D5:** The unordered accepted C triples are five cyclic consecutive triples. Their complement pairs form the edges of C5; thus every automorphism of C preserves this 5-cycle, and all 10 dihedral symmetries preserve C. Independent brute force found exactly 10 of the 120 permutations.

**Special graph-encoding strengthening:** For distinct private-head clauses C(h_e,z_u,z_v), existential projection is z_u != z_v, with full S5 relabeling invariance. Thus for graph-only blocks, B <= sum_{i=1}^{min(q,5)} Stirling2(q,i), the number of partitions of q shared vertices into at most five color classes. Do NOT transfer S5 to unrestricted strict C.

## Executed deterministic verification
Canonical relation R(a,b) iff (b-a) mod5 in {1,3}; C is the directed triangle in either orientation. C true on 30/125 triples; independently checked GF(5) quadratic predicate on all 125; head projection checked all 25 endpoint pairs. For q=1...6, full shared rows 5,25,125,625,3125,15625 collapse under D5 to 1,3,13,63,313,1563, and under S5 to 1,2,5,15,52,202.

K6 source: six shared vertices, 15 distinct private heads, 15 physical strict-C clauses. All 15 clause deletion witnesses checked against original C and independent quadratic predicate, 225 evaluations; each retained clause true and each deleted clause false. All 15625 shared assignments have a blocker. Exactly 1800 unique-blocker rows, 120 per edge, constituting one S5 orbit or 12 D5 orbits per edge. Lexicographic first-hit scan used 70785 comparisons. No random seed.

Independent reproduction scripts and complete witnesses are in archive T5C_Resource_Symmetry_Orbit_Audit_20261119.zip, delivered in this conversation. Script SHA256: cd98b9f62517d644eccf3cec49657ee93550a7c779648a624a71bde09e0200b3; independent replay SHA256: 7483718476758f29e87838404b5193628d0e56a053b962978ecbe91dc2da434d.

## Exact time-space firewall
Let L be bit-encoded input length, R<=L^.195, B<=L^.65, m<=L^.35. A full sequential row/block scan using a complete local child solver in m^a time and m^s writable space has CONDITIONAL exponent max(1.195,.845+.35a), provided all source and certificate costs fit. To reach T<=L^1.33, a<=97/70=1.385714... is required; local space requires s<=10/7 for S<=L^.5, excluding other live storage.

**New source-order firewall (CONDITIONAL, for a particular algorithm):** If an implementation rereads the entire unsorted flat source of L bits to recover every (row,block) child, its source work alone is Theta(RBL)=L^1.845 at saturation. The earlier L^1.195 source-read budget presupposes indexed reconstruction or an actual single pass per row. Materializing a directory of B general block offsets costs Theta(L^.65 log L) writable bits, exceeding L^.5. These are NOT general algorithmic lower bounds; source-aware or streamed alternatives may avoid them.

Clocking a globally sound deterministic one-sided specialist that succeeds on every target-polarity input by a uniform known T,S yields a total decider by answering the opposite polarity at timeout. A supplied k-bit nondeterministic correct path is not deterministic discovery; wrong paths, potentially 2^k enumerated trials, and verification must be charged. Universal branches in an alternating UNSAT cover cannot be omitted. UNSAT quantifiers: FORALL z EXISTS j FORALL x_j NOT F_j(z,x_j). SAT quantifiers: EXISTS z FORALL j EXISTS x_j F_j(z,x_j). Original-C verification is mandatory.

Buss-Williams (Computational Complexity, 2015), Figures 8.2-8.3, establish SAT not in DTISP(n^1.34070,n^.5) in their deterministic random-access model (44 search rounds, 406 triples). A uniform fully correct unrestricted SAT algorithm at (1.33,.5) in this model is excluded. Restricted promise strict-C specialists need a separately proved locally indexed resource-preserving SAT reduction, per Williams (2006), Corollary 2.3. Do not transfer resolution or nondeterministic lower bounds to general machines.

## Prior evidence and open obligation
Read: research/agents/resource-audit/2026-11-19_UNIQUE_BLOCK_ROW_COVER_BARRIER.md, research/agents/proof/2026-11-19_LEAD_RANK_ROW_VOLUME_FIREWALL_RUN2.md; user t5_strict_research.pdf pp1-4. Strict research ZIP could not be recovered from Library search. OPEN: source-uniform sound dynamic symbolic global-cover acquisition on nonrecognizable critical high-incidence-girth strict-C sources with full access/preprocessing/both polarities/certificate replay/peak writable-space charged. P vs NP OPEN.

References: Buss & Williams 2015 https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimits/paper-journal.pdf ; Williams 2006 https://www.cs.cmu.edu/~ryanw/sat-journal-final.pdf ; Fortnow et al. 2005 https://doi.org/10.1145/1101821.1101822 .
