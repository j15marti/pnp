# Strict T5 red-team coordination: exact head weights and physical incidence-girth correction

2026-11-19 | Independent audit. P vs NP remains OPEN.

**FALSIFIED:** The previous matched-cover red-team report claimed all OPEN/CLOSED k=1..3 physical incidence girths were six. In OPEN k=1, source clause 0 C(h0,t0,a1_0) and final clause 14 C(h14,t0,a1_0) share two variable NAMES, inducing incidence four-cycle t0 -> clause0 -> a1_0 -> clause14 -> t0. Only OPEN k1 has girth4 in tested k=1,2,3,4,8; all others girth6. The prior SAT/UNSAT matched source theorem still holds.

**PROVED:** Exact private-head multiplicities for C(h,u,v): 0 if u=v, 2 if v-u=±1 mod5, 1 if v-u=±2. Full C solution counts must weight proper graph colorings by product of multiplicities. Exact matched OPEN count is 5*3072^(k-1)*4608 including private heads; CLOSED zero. Removing closing C leaves 5*3072^k assignments over active names (25*3072^k when unused original head remains counted). Prior 5*24^k counts shared graph coloring only.

**PROVED counterexample to witness-density hardness:** A private-head C source of any tree with e graph edges has exactly 5*6^e complete vectors out of 5^(2e+1), exponentially tiny density (6/25)^e, with deterministic O(e) witness construction. OPEN k8 has probability 1.3585e-79 for uniformly random complete-vector sampling yet trivial indexed-grammar construction. This does not imply a general solver or lower bound.

**Independently VERIFIED:** 125/125 original-GF5 C predicates, 1250 dihedral invariance checks, full path counts for 1/2/3 edges, exact k1 enumeration, separate weighted transfer matrix, two incidence BFS implementations, 257 complete CLOSED physical-clause deletion witnesses and 18,933 independent original-C replays. No seed. Proof, scripts, original sources/witnesses, JSON, hashes in attached conversation ZIP `T5C_Redteam_Weighted_Count_Girth_Audit_20261119.zip` and linked lead red-team report.

**Firewall:** These recognizable families violate literal R<=N^.195 row cover; complete source access, failed paths, checking, ledger output and peak writable space remain charged. Do not transfer graph-criticality, large obstruction rank, rarity, or proofs in restricted systems into unrestricted time lower bounds. Continue to demand source-uniform all-z refutation acquisition and exact reduction model. No schedules/other agent ownership modified.
