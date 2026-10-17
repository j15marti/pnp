# SIGMA3-SWITCHGUARD52: SAT-guarded one-step quotient
Timestamp: 2026-10-17 15:34 UTC. Status: exact **restricted** lemmas; computational checks; full P != NP proof OPEN.

## Proposal/search/build
Four candidates: switched linear SAT guard, GF(2) certificate, genuine Sigma3 polarity, fully charged fractional-query accounting. Reviewed project REACHCERT51/HORIZON50 and LEAD-0020 exact continuation quotient; primary anchors: Zhang/Zhang/Su (SIAM JCO 2016); Balabanov et al. (AAAI 2015); Akshay et al. (SAT 2026); Fortnow/Lipton/van Melkebeek/Viglas (JACM 2005), DIMACS 2000-06.

## Theorem A: exact continuation classes (restricted)
Let state s=(s0,...,s_(w-1)), w>=2. O(s)=s0. For universal control u, let T_F(s,u) be the left-shift (s1,...,s_(w-1),0) if F(u)=1 and identity otherwise, for a CNF F. Full-future behavioral equivalence is equality of output traces for all finite control sequences. The minimum exact **stationary** fingerprint width is **1 if F is UNSAT, w if F is SAT**. Proof: under UNSAT every transition is identity and only s0 matters. Under SAT repeat a satisfying u*; outputs reveal all w state bits. This uses only one conditional shift gate on top of the source CNF and has unique local gate traces. Exponentially many distinguishable states alone imply no time lower bound.

## Theorem B: one-step quotient certification
For proposed h(s)=s0, the statement "there exists U such that for all s,u, h(T_F(s,u))=U(h(s),u)" holds iff F is UNSAT. With F SAT, s=(0,0,...) and s'=(0,1,...) have identical tag but different successor tags under u*. Thus certification is coNP-complete on these guarded-shift circuits even for w=2. This is a one-transition analogue of project SAT-activation, not a claim of novelty over the general problem.

The size-near-linear, logspace reduction and the published same-machine deterministic random-access SAT time-space tradeoff exclude a universal exact validator with time N^(6/5+o(1)) **and** space N^(1/2+o(1)); the permitted space exponent upper threshold at c=6/5 is 23/45 > 1/2. This does **not** exclude other polynomial validators or conservative full-state tags.

## Theorem C: exact Sigma3 counterstrategy
Xi_F = exists t forall(u,b) exists z: (z=(b AND F(u))) AND (t=z). This is TRUE iff F is UNSAT. If F is SAT then every Herbrand counterstrategy against t=0 must output (u,1) with F(u)=1. Against t=1, b=0 refutes cheaply. A fixed satisfying u* yields a counterstrategy circuit of O(n) bits but uniform synthesis must find u*; negative witnesses are not free. Moving t behind forall(u,b) makes the formula trivially TRUE, an invalid quantifier-prefix rewrite.

Under a single P=NP hypothetical SAT solver A of time m^(K+o(1)), space m^(L+o(1)), direct Xi_F decision costs N^(K+o(1)) and N^(max(1,L)+o(1)) with materialized child. Standard n-step Herbrand witness self-reduction costs N^(K+1+o(1)) time, N^(max(1,L)+o(1)) space; these are exhibited upper bounds, not lower bounds.

## Resource contraction
If q<=N^theta, child <=N^lambda, acquisition costs (N^a,N^b), parent/copy costs N^rho, live buffers N^sigma, serial ledger is:
 K'<=max{a,rho,theta+lambda*max(K,1)}+o(1);
 L'<=max{b,lambda*max(L,1),sigma}+o(1).
Earlier certified blocks permit lambda=1/2, theta=11/20 and guest exponent 0.55+K/2. Generic certification of the SAT guard by a parent-size SAT call reinstates coefficient 1. No hereditary all-input lambda<1 theorem established.

## BUILD/TEST
Standard-library Python auditor: 500 CNF guarded shift models (223 SAT,277 UNSAT); 347,360 direct next-step evaluations; 400 direct QBF matrices (236 TRUE,164 FALSE); 420 affine-guard Gaussian primal/dual certificates; 350 non-affine postprocessed low-rank models; 650 signed integer and 600 GF(2) complete bipartite flows; gate traces checked. 35,386 recorded assertions; ZERO discrepancies. Exact proofs do not depend on finite tests.

## NEXT
Study a real solver's delayed indirect-address branch. Compare conservative branch closure, source-visible UNSAT proof, and reachable-only inductive invariants. Charge acquisition and verification, source rereads, child size, YES/NO service, canonical witnesses, same-machine joint time/space, and hereditary eligibility.

SENTINEL_SWITCHGUARD52_20261017_1534Z
