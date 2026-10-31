# LSPV-4 ARC-TARGET-COFACTOR-TRANSFER279
October 31, 2026, 11:36 a.m. America/Los_Angeles.

**Status:** PROVED/EXACT restricted cofactor theorem and exact rational arithmetic; KNOWN THEOREM NP-completeness and FLMV; COMPUTATIONAL original-source controls; CONDITIONAL reduction theorem; P versus NP OPEN.

## Exact obstruction and updated scientific universe

Scope is every valid, duplicate-free, proper, monotone sign-uniform 3-SAT-(2,2) formula, each variable exactly two positive and two negative occurrences, with malformed encodings rejected. Döcker 2019 proves NP-completeness of this language (arXiv:1912.08032). The broader signed strict-2P2N language is a comparative superset, not the NP-hard target. A polynomial-time solver of this complete language implies P=NP. Proving no polynomial decider exists on this complete language would imply P!=NP. Neither has been accomplished.

**The key missing arrow** is an exact hereditary all-valid-target arbitrary-A -> Phi(A) compiler with genuine power-short target children, with reduction length and per-bit access fully charged on the same indexed-input deterministic Turing model. Mere NP-completeness does not transfer the sharp numerical FLMV SAT forbidden region.

Four falsifiers: (F1) raw connected-target cofactors remain target-valid, FALSIFIED. (F2) mixed same/opposite shared-sign pair extremes occur in monotone clauses, FALSIFIED. (F3) NP-completeness automatically supplies a quantitative FLMV transfer, FALSIFIED as an inference. (F4) virtual bit access makes child materialization and source authentication free, FALSIFIED as an accounting rule.

## PROVED/EXACT theorem: raw cofactor nonclosure

Let F be any nonempty connected valid target formula with n variables and m=4n/3 ternary clauses. Every nonempty proper partial assignment cuts at least one original clause containing both fixed and unfixed variables. The clause is either deleted or shortened, permanently removing a signed occurrence of an unfixed variable, violating its exact two-positive/two-negative quota. A full assignment has only TRUE or an empty clause, also outside the nonempty target class. Thus no nonempty raw cofactor stays target-valid.

For any pivot x, exactly two source clauses contain x and two contain ¬x. Each assignment x=b deletes two clauses and shortens two, yielding exactly m-2 retained clauses, including m-4 ternaries and two binaries, and 3m-8 literal occurrences. Both-label soundness is exact: SAT(F) iff SAT(F|x=0) OR SAT(F|x=1); UNSAT(F) iff both cofactors UNSAT. These are standard identities, not a target-preserving compiler or a hardness proof.

All source clauses are sign-uniform. For any pair with same-polarity sharing the (SS,SU,US,UU) extreme feasibility vector is (1,0,0,1); with opposite sharing (0,1,1,0); with no sharing (1,1,1,1). The previous all-four-extremes-impossible mixed-sign conflict cannot occur within the target. The two coherent allzero/allone original-clause profiles are invariably (m/2,0,0,m/2). This supplies no UNSAT certificate. Complete clause-indexed local S/U targets, inversions, flip trails and original-clause forbidden partial cubes are retained in raw data.

## Matched SAME-SOURCE SAT/UNSAT controls

Read canonical Döcker Appendix C U from research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt (Git blob f9dda41a810ad8e02bd553f2711a26a4050861f9). It has 198 variables, 264 unique proper monotone clauses and is connected. Swapping positive literals in source clauses 2 and 8 produces another valid connected target V with exactly the same source length. Original U is UNSAT; V is SAT. Independently verify both labels, rather than infer either from endpoint failures: a fresh verifier establishes an actual 32-private-variable source-template M UNSAT refutation with 89 nodes, 329 justified UP steps and 45 original-clause conflict leaves. Six disjoint 42-clause blocks of U are exact signed renamings of M and each entails its actual external terminal disjunction. Their eight-clause core over six variables rejects all 64 assignments, proving U UNSAT independently of its last ten original clauses. A complete 198-bit witness independently satisfies every V clause. A small third valid target Y8 has 20 satisfying assignments by exact enumeration.

Y8: (n,m)=(6,8), 688 ASCII DIMACS bits. U and V: (198,264), 29,392 bits each. The U and V indexed clause-pair counts are identically 351 same-sign, 786 opposite-sign and 33,579 disjoint. Their raw one-variable children have 262 clauses, 784 literals, and 29,152 or 29,184 physical DIMACS bits, not power-short or target-valid. Fifteen malformed formula/encoding controls rejected by the finite canonical parser. This demonstrates only the declared dense-identifier encoding: alternate legal variable-identifier syntaxes or labels still need a separately charged total parser/renaming theorem, so all-input target parsing remains OPEN. The 1.5MB complete original-indexed Python raw and 47KB independent certificate are preserved in the downloadable reproducibility archive; a 360KB compact original-indexed JSON is independently published in GitHub.

Instrumented ordinary UP-DPLL Y8 baseline: 4 nodes, 55 literal probes. On U, the baseline ran 8,598 nodes and 17,438,116 literal probes in three seconds, label UNRESOLVED; on V 9,445 nodes and 16,954,613 literal probes, also UNRESOLVED. Both cofactor baselines also hit their three-second limits. No timed-out result is an UNSAT claim. These are logical operation counts, not native FLMV transitions or CDCL.

## CONDITIONAL same-machine FLMV reduction theorem

Suppose a uniform total SAT-to-target transformation on all N-bit source inputs, including explicit malformed-string behavior, creates a valid target string of length M <= N^(a+o(1)). Let charged policy selection, discovery, failed trials, source authentication and output-bit-access preparation cost N^(r+o(1)) time and N^(s+o(1)) simultaneous writable space. Every virtual target input read, including blanks and indexed head semantics, costs N^(beta+o(1)) time within the same writable ledger. Composing with any target decider of simultaneous time M^(K+o(1)) and space M^(L+o(1)) then gives ordinary SAT time exponent at most max(r,aK+beta), space exponent at most max(s,aL). This is conditional on an actual verified same-machine virtual input simulator. NP-completeness by itself supplies no numerical bounds on a,beta,r,s.

Independently exact FLMV Theorem 5.7 has f_0=1, f_k=cf_(k-1)/(1+f_(k-1)), d_k(c)=min((1/f_k-c)/k,c^(-k)). At c=6/5 the full envelope d*=23/45; at c=241/200, d*=11642479/23232400=1/2+26279/23232400. Both have unique k=2 optimum, and the entire k>=4 infinite tail is strictly excluded by d_k<=c^(-k).

At the hypothetical unconstructed target ARC fixed point (K,L)=(6/5,1/2), entering the strict ordinary-SAT FLMV exclusion at c=241/200 requires simultaneously:
r<241/200; s<11642479/23232400; 6a/5+beta<241/200; a/2<11642479/23232400.
Even when beta=0, the reduction's physical length exponent must be a<11642479/11616200=1.0022623... for the space inequality. Materializing the target on writable tape costs exponent at least a>=1, exceeding d=0.501..., so a real virtual-input construction or a direct target lower bound is necessary. The existing strict22 normalizers and CP22LIFT1 are not free, and the affine MCSP theorem is a restricted semantic no-go only.

Original input scans/endpoints may use O(N) time and O(log N) scratch, but storing every ternary truth count uses >=2m bits, retaining a dense four-mode pair matrix uses 4*binom(m,2) bits, and storing even a sparse shared-pair index costs writable memory. Source occurrence index discovery, failed selectors, restarts, per-child guest index tapes, reset/replay, proof checking and ancestor retention remain charged. Degree-quota validation via a naive n-counter pass uses Theta(n log n) writable bits; repeated source rescans can use O(log N) scratch but O(nN) time. These are named-architecture costs, not unrestricted complexity lower bounds.

## Reconciliation, primary literature and searches

Read verified REDIRECT1, CONTRACT1, AFFINE-SMALLBIAS-DESCENT-GATE2, CONSTRUCTION-STRENGTHEN17, ARC-LINEAR22-SATURATION1, root/AGENTS/CODEX/pnp-research skill, issue #3, CP22LIFT1, LSPV2 VIRTUAL-STRICT22-COMPOSE255, historical ARC177, and recent LSPV4 reports. Project ARC177 already had the one-variable m-2 cofactor count and a 32-variable refutation method, so neither is claimed novel.

Web/Google queries: "Doecker monotone 3-SAT-(2,2) duplicate-free NP-complete 198 264"; "FLMV 2005 Theorem 5.7 indexed random-access SAT forbidden region"; "fine-grained bounded-occurrence SAT reductions time-space local". Github project searches: "Monotone 3-SAT-(2,2)", "Döcker", "CP22LIFT1", "hereditary closure balance", "strict22 compiler", "DOECKER-CORE-CERT61". GitHub openai/lean4 "SAT reduction" returned no result; openai/codex "SAT solver" returned unrelated saturation/status material. Historical raw-fixture alias returned 404, canonical source loaded. Failed search is not evidence of novelty.

Sources: Döcker, arXiv:1912.08032 (2019), https://arxiv.org/abs/1912.08032; Darmann and Döcker, Discrete Applied Mathematics 292 (2021), doi:10.1016/j.dam.2020.12.010; Fortnow, Lipton, van Melkebeek, Viglas, JACM 52(6) (2005), https://lance.fortnow.com/papers/files/tst.pdf.

**OPEN:** Every valid target input, malformed-string rejection, certified child hereditary re-encoding, physical/indexed bit access and full same-machine SAT-to-target FLMV transfer remain unproved as one favorable universal arbitrary-A -> Phi(A) transformation. P versus NP OPEN. Five existing research identities, schedules and statuses unchanged.