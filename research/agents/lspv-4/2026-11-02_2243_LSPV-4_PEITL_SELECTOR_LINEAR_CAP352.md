# LSPV-4 PEITL SELECTOR LINEAR CAP352
**November 2, 2026, 22:43 PST, America/Los_Angeles.**
**PROVED/EXACT:** source-explicit, binary-premise mixed-system selector sandwich. **COMPUTATIONAL:** two-language Peitl-core stress test. **OPEN:** composite exact mixed optimum, B1/B2/B3, superpolynomial worst-case cost and P versus NP.

## Corpus review and duplication audit
Read the VERIFIED 12:04 five-role handoff FIRST, issue #3 and its latest peer discussion. Reviewed original Rmix341 in LSPV-2 MIXED-TSEITIN341; LSPV-2 LOCAL-RESTRICTION-PIVOT351; LSPV-4 split350 and selector351; LSPV-5 PEITL-EXACT-EIGHT-REFEREE304 and direct-sum305; LSPV-3 GUARD-SUM-NONHORN349 and GUARD-SUM-EXACT350; AGENTS.md, CODEX.md and pnp-research skill. The **general selector sandwich was already proved by LSPV-3 GUARD-SUM349** and is not claimed as new. The new audit here applies it to the authentic Peitl seven-clause *mixed-excess-three* core and independently measures source/evidence/checker work on balanced vs comb selector trees.

Primary literature: Peitl and Szeider, IJCAI 2021, DOI 10.24963/ijcai.2021/657; Cook and Reckhow, JSL 1979; Buss et al., LMCS May 25, 2026, DOI 10.46298/lmcs-22(2:23)2026. GitHub project searches: "selector guard proof DAG", "Peitl exact eight referee"; OpenAI GitHub: "resolution proof checker", no directly relevant fixed-mixed implementation returned. Existing public exact resolution proof optimizer: peitl/short-proof. No novelty claim for selector guarding, proof lifting or proof-system separation.

## Fixed rules and universal theorem
R=unchanged Rmix341 with source-independent conservative VARDEF, binary RES, exact bounded-support AND3, GF(2) XOR, charged local conversion, unit derived-node weights and source-labelled free source clauses. Every node has <=2 named antecedents; conservative definitions do not introduce uncharged source dependencies; shared DAG nodes counted once; best legal derivation chosen free of search/optimizer cost. No SAT oracle, instance-specific axiom or new source-factor DEF.

For pairwise disjoint minimally UNSAT CNFs F_i with m_i clauses and explicit ordinary Resolution proofs of q_i derived nodes, construct H_T on any full binary selector tree T, guarding left and right subtrees by opposite literals of distinct fresh selector variables. If M=sum_i m_i, then:

**M-1 <= W_Rmix341(H_T) <= W_RES(H_T) <= sum_i q_i +(k-1).**

Proof: every selector assignment activates exactly one UNSAT leaf. Removing a source clause allows selecting its leaf and a witness to F_i\{C}, hence H_T is minimally UNSAT; all M sources are indispensable. In any sound contradiction ancestry with q paid binary-premise nodes, E>=M+q-1 and E<=2q, so q>=M-1, regardless of sharing, temporary growth, XOR or paid conservative VARDEF. For the upper bound, append each leaf's complete ancestor guard to all lines of an explicit Resolution proof. Its pivots are leaf variables, hence still legal; the final derived line is that guard. Resolve sibling guard clauses once at each internal node to reach empty, using sum_i q_i+k-1 inferences. Proof cost is independent of construction depth or optimizer effort.

Thus 0<=W_R(H_T)-(M-1)<=sum_i[q_i-(m_i-1)]. With a **fixed constant-size seed** this is O(k), and source binary length N>=Omega(k), so this selector construction cannot yield a superpolynomial W_R(N) lower bound. This is a FAMILY FAILURE, not an upper bound on worst-case Wbar_R(N). A growing hard seed family is not excluded.

## Authentic nonaffine hard seed and exact charged upper bound
Seven original clauses on five variables from the authenticated PEITL-EXACT-EIGHT-REFEREE304:
(-1,2);(-2,3);(-3,4);(-4,5);(1,-5);(1,2,3,4,5);(-1,-2,-3,-4,-5).
The independent prior all-rules finite certificate establishes **W_mix341(seed)=9** versus the source floor 6. This run replays the existing **nine-step genuine Resolution** upper certificate but does not independently rerun the large 105-case lower-bound solver. For k disjoint copies guarded by distinct internal selectors:

**n=6k-1, m=7k, 7k-1 <= W_mix341(H_T) <= 10k-1, 0<=excess<=3k**.

No exact mixed minimum for k>1 is asserted. Balanced k=2^d has L=k(20+7d) independently sensitive original sign fields; a comb has L=20k+(7/2)(k^2+k-2). Each original source deletion and single occurrence-sign flip is SAT, by selecting that leaf and using its omission witness. Ordinary deterministic one-bit source-access deciders must inspect all L independent signs on this UNSAT input, but this is no general writable-space or arbitrary-machine runtime lower bound.

## Executed evidence and adversarial falsifiers
Python standard-library generator and entirely separate no-import Node.js checker: 11 cases k=1,2,4,8,16,32 (balanced and comb for k>1), **16,293 independent Node assertions PASS** and **10,137 SAT deletion/sign-flip neighbor witnesses** checked. Valid source UNSAT follows from selector induction and independently verified full signed Resolution DAGs; n<=11 additionally enumerated. Odd/even K4 parity models 0/8, SAT tautology control, 66 malformed binary encodings rejected by strict Python parser, and forged last pivot rejected. Source bits encoded by gamma(n+1), gamma(m+1), gamma(width+1), then each literal sign and ceil(log2(n+1))-bit id.

| k | shape | N source bits | L sign fields | mixed W range | RES nodes | pivot-only evidence bits | eager parent literal reads |
|--:|:---|--:|--:|:---|--:|--:|--:|
|1|seed|117|20|9 exact|9|117|46|
|4|balanced|990|136|27..39|39|741|338|
|4|comb|1028|143|27..39|39|741|358|
|8|balanced|2630|328|55..79|79|1738|834|
|8|comb|3205|405|55..79|79|1738|1054|
|16|balanced|6794|768|111..159|159|3975|1986|
|16|comb|10954|1265|111..159|159|3975|3406|
|32|balanced|17438|1760|223..319|319|8932|4610|
|32|comb|40875|4329|223..319|319|8932|11950|

Eager reads are **implementation-schedule work only**, not universally unavoidable. Pivot-only evidence excludes source bits and retrieval; fully paid verification includes source grammar/IDs, index/read-head accesses, pivot/tautology checks, materialization, cache/recompute, proof output. Generator all-phase elapsed 2.12s / peak host RSS 97,680 KiB; Node 0.16s / peak host RSS 33,524 KiB. These **are host process measurements**, not matched FLMV indexed-TM steps or sqrt-space proof. The all-phase envelope still requires s'<=max(rho,eta,lambda,lambda*s), with rho covering *every* phase, including allocate-then-free preprocessing.

**F1:** selector nesting of a mixed-hard seed implies superlinear W, FALSIFIED by explicit O(k) proof. **F2:** W must equal k*W(seed)+(k-1), OPEN; no additive lower claim. **F3:** same derived-node count fixes source/checker work, FALSIFIED (balanced/comb). **F4:** short proof eliminates compulsory source reads, FALSIFIED in the explicit independent-sign query model.

## Bridge and status firewall
B1 remains the unproved all-decider pointwise simulation; B2 must involve T_A^wc(N) over **all valid SAT/UNSAT and malformed binary strings**, not the time of this family-specific recognizer; B3 is the weaker unproved implication SAT in P => Wbar_same_fixed_R(N) polynomial. The present family upper does not imply Wbar is polynomial, does not contradict B2, and supplies no computation-to-proof machine-correctness reflection. P versus NP remains OPEN.

Full independent producer/referee/source-by-source witness generator, parsed raw JSON, signed proof replay, logs, exact hash manifest and this expanded report are in **LSPV4_PEITL_SELECTOR_LINEAR_CAP352_repro.zip** in the conversation. Standalone public compact reproducer and public raw summary are separate repo files. Next: use an *interacting* non-selector growth gadget that provably amplifies mixed-system excess; separately establish B3 if possible. No task/state/schedule change. Independent academic review pending.
