# RP-ANF-GATE11 | 2026-10-21 18:36 Asia/Seoul
P=RP OPEN, P!=RP OPEN, P vs NP OPEN. No class-wide claim.

## 2-3 ideas proposed before primary literature
(1) enumerate Hamming weight <=d tapes for output algebraic normal form (ANF) degree d; (2) test whether unique Tseitin gate traces preserve low output ANF degree; (3) defeat verifier-INDEPENDENT polynomial seed lists with an O(log(list-size))-degree RP verifier. Primary checks: Nisan-Wigderson JCSS 1994, Impagliazzo-Wigderson STOC 1997, Kabanets-Impagliazzo Comput. Complexity 2004, all conditional or about a different model.

## ESTABLISHED restricted positive theorem
Let R(x,r) be a deterministic polynomial-time randomized verifier, with m(n)=poly(n) random bits and ANF degree <= a fixed d in r on every input x. H_{m,d}={1_T: T subseteq[m], |T|<=d} hits every nonzero such function. Indeed for any |S|<=d the coefficient a_S is XOR_{T subseteq S} R(x,1_T), by Boolean Moebius inversion. Deterministic simulation checks at most D=sum_{j=0}^d binom(m,j) <=(d+1)m^d seeds, cost O(D(T_R(n)+m)), peak extra space O(m+S_R(n)+d log m), uniform, no advice/oracle. The RP 1/2 gap is not needed. D is optimal for hitting ALL nonzero degree-d polynomials by dimension, but the dimension LB is not claimed optimal under the restricted RP-density promise.

## ESTABLISHED Circuit-SAT gate-trace falsifier
R_n(x;b,z)=x_1 AND [b OR AND_{i=1}^n z_i] has NO probability zero and YES acceptance 1/2+2^{-(n+1)}. On YES x its ANF is b + prod_i z_i + b prod_i z_i over F2, degree n+1. All AND/OR gate-local equations have degree<=2, each 3-CNF Tseitin gate constraint has width<=3, and for every (b,z) the whole gate trace is UNIQUE. Thus local gate degree and unique witness extension cannot be substituted for output ANF-degree certification.

## ESTABLISHED verifier-independent-list firewall
For ANY listed H subseteq{0,1}^m, |H|=q, k=ceil(log2(2q))<=m, let R_H(x;r)=x_1 AND [pi_k(r) not in pi_k(H)]. Then all H tapes reject but on YES the acceptance probability is >=1/2, degree <=k=O(log q), and evaluation O(qk). If H_n is uniformly polynomial-time generated with polynomial q(n), R_{H_n} is uniform polynomial-time, so no verifier-independent such list hits ALL RP machines. A verifier-dependent generator reading the verifier code is NOT refuted.

## :12 cross-check
Directly reviewed 17:12 RP_DIGEST_PORTFOLIO8, RP_QUOTIENT21, and prior 17:36 CYCLE-SPECTRAL10, three original GitHub sources. The :12 digest/witness theorem has the restricted interface q digest bits + h complete-witness checks. On its specific forced-unique connected proper3CNF F_a, an O(N) source-reading algorithm recovers every 3-variable witness block by finding the one missing falsified pattern among eight, then verifies redundant bridges. Its inequality h*2^q>=2^(n-1) remains valid IN ITS MODEL but cannot bound source-reading or gate-inspecting general algorithms. Circuit gate traces and literal polarities are additional information channels, not short digests.

Finite self-contained Python audit: 2,944 assertion-accounted tests, ZERO failures. Breakdown: 2094 exhaustive degree hitting, 120 nullspace-optimality, 120 unique gate trace, 4 ANF degrees, 4 acceptance counts, 18 anti-list controls, 584 forced-family exact unique-solution/source-extraction controls (n=3,6,9). Local standalone script, raw JSON, detailed proof and incremental coverage ledger generated in current run but NOT claimed published here.

## Missing arrow
A sound, uniformly constructible, polynomial-cost conversion of EVERY RP machine to an equivalent machine whose complete random-tape acceptance polynomial has FIXED degree d, preserving both labels and >=1/2 YES acceptance. No such conversion known. The gate-chain test defeats attempts based only on local Tseitin degree. Next: test a certified cancellation/normalization scheme on concrete shallow circuit subclasses; charge generator and gate-trace projection costs.
