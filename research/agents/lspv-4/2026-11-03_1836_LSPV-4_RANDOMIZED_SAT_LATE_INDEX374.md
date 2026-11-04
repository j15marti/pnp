# LSPV-4 / 374 | Randomized one-pass SAT decision, one-node proof, and reread escape
**November 3, 2026, 18:36 PST | PNP Time-Space Resource Auditor**

**STATUS:** PROVED/EXACT for the explicitly declared sequential one-pass SAT model, independent referee pending; COMPUTATIONAL for finite controls; KNOWN INDEX/Fano information inequality. General SAT B1/B2/B3, a superpolynomial full-mixed minimum, and P versus NP remain OPEN.

## Published lower bound anchor
Haken (1985) proves: for the standard unary PHP with h+1 pigeons and h holes, there exist c>0 and h0 such that for all h>=h0 **every ordinary shared-DAG Resolution refutation** contains >=2^(ch) lines. The CNF has h(h+1) variables, (h+1)+h*binom(h+1,2) clauses and explicit signed-binary-length N=Theta(h^3 log(h+2)). This is a Resolution proof-system bound, not an all-algorithm SAT time bound. Cook's polynomial Extended Resolution PHP proofs and short GF(2) refutations of odd Tseitin control the forbidden transfer. Nothing about this hard family is regenerated.

## Exact model and result
Keep preselected Rmix341 unchanged: original signed clauses are free source leaves, paid inference nodes include binary RES, local AND3, GF(2) row XOR, checked LOCAL-CONVERT, and conservative AND2 DEF. Define for k>=1, sign vector a in {0,1}^k and late selector j in [k]:

$$
F_{a,j}=\bigwedge_{i=1}^{k}\ell_{a_i}(x_i)\ \wedge\ (\neg x_j),\qquad
\ell_1(x)=x,\quad\ell_0(x)=\neg x.
$$

First emit k ordered unit clauses, then the final negative unit. The selector j is **not known** until the last clause. Use a fixed signed-field canonical DIMACS subgrammar: each positive prefix unit has a leading ASCII space (e.g., " 1 0"), each negative prefix unit has a '-' sign (e.g., "-1 0"); the same identifier digits and terminator follow. Prefix length is therefore exactly independent of a at fixed k. Valid sources have N=Theta(k log(k+2)) bits.

**PROVED/EXACT:** F is SAT iff a_j=0, with one model. If a_j=1, opposite source units give a one-inference strict RES contradiction, so W_Rmix341(F)=1 exactly for **all UNSAT members**.

A deterministic one-pass exact SAT decider needs >=2^k distinguishable post-prefix states, because distinct a,b have a position j at which the same suffix yields opposite labels. A public-coin randomized one-pass decider with at most epsilon<1/2 error on *each* valid source and s bits of retained state (including all nonpublic information/control/address state) satisfies

$$
s\ge k(1-H_2(\epsilon)),\qquad H_2(e)=-e\log_2e-(1-e)\log_2(1-e).
$$

For epsilon=1/3 this is >=0.0817041659455*k bits. Proof: for uniform independent A,J, the suffix must decode A_J from post-prefix state M and public independent coins R. Binary Fano, conditional entropy subadditivity and concavity yield H(A|M,R)<=k H2(epsilon); therefore s>=I(A;M|R)>=k(1-H2(epsilon)). No restriction is placed on the solver's internal algorithms beyond the explicitly sequential one-pass channel.

**FALSIFIER:** a second charged read-only source pass invalidates the retained-space conclusion. Pass 1 validates the source and saves the suffix j; pass 2 rereads the jth prefix sign. This has O(N) bit/head work and O(log N) writable space on the promise family. On indexed read-only input the lookup can also be paid through indices. Neither the streaming lower bound nor constant W_R gives an unrestricted SAT machine lower bound.

## Four adversarial tests
1. One-node UNSAT logical proof implies constant one-pass decision memory: **FALSIFIED**, since all k prefix signs may matter to the late suffix.
2. Public-coin random fingerprints with o(k) retained bits decide every such input at bounded error: **FALSIFIED** in this model by Fano.
3. The same memory bound holds with rereads/random access: **FALSIFIED** by the two-pass algorithm.
4. The result implies B2, B3 or P!=NP: **REJECTED**, since the family is elementary unit-CNF and the lower bound is channel-restricted.

**Actual ledger:** one-pass work O(N) with Theta(k) live sign bits; two charged passes O(N) time, O(log N) writable bits, paying all source/head operations and grammar validation. Outputting/checking an explicit proof and discovering its source references are additional charged activities. An unmaterialized virtual table is not writable memory. The all-phase envelope remains s'<=max{rho,eta,lambda,lambda*s}; allocating the k-bit cache raises rho, even if freed later. No FLMV indexed-machine exponent is inferred.

## Independent finite controls
An executable standalone Node producer enumerated all 3,586 pair sources for k=1..8, 1,793 SAT and 1,793 UNSAT, and checked a two-pass replay for each. It independently brute-forced 642 source assignments for k<=6, found one or zero models respectively, checked 36 distinct low-memory collisions, rejected 11 malformed source records, and verified K4 odd/even parity model counts 0/8. The detailed producer counted 11,457 assertions. A separate Python implementation independently checked 47,029 assertions, including every prefix pair and its distinguishing suffix for k<=8. No random seed or heuristic search was used. Host measurements are not indexed-TM space bounds.

## Corpus / assessment audit
Read verified five-role handoff research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md (blob c3889a3e), issue #3, AGENTS.md (19656af1), CODEX.md (754999f5) and project research skill (b8df83a7). **Duplication credited:** LSPV-1 ONEPASS66 (deterministic SAT one-pass INDEX), PASSMEM84 (multipass); LSPV-4 SOURCE-FIRST355 (deterministic delayed authentication), RANDOMIZED-SOURCE-FIRST356 (Fano for source authentication); LSPV-4/373 (supplied-proof streaming compiler). The increment is a *randomized actual SAT-decision* Fano bound, tight opposite-label unit-CNF proofs, and fixed-length signed grammar. This is an elementary, restricted combination, not a claimed new information-theoretic theorem.

Actual repository files reviewed: GROKPROOF/2026-11-04_0116_PROGRESS.md (blob ca5a8353), research/agents/grok/2026-10-23_1915_GROK_REWIRE.tex (d06a2d56), research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727), and 2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6). Grok still has no charged universal SAT decomposition. Claude's restricted alternation-trading/one-tape results do not give B3. Also inspected latest LSPV-1/376, LSPV-2/376, LSPV-3/380 issue update and LSPV-5/325. The authorized root main.tex fetch returned nonempty SHA b2012505... but zero bytes even for lines 1-100; no ownership-safe root reconciliation was possible.

Project GitHub searches: late-index unit-CNF streaming; randomized one-pass SAT late selector Fano; proof checker indexed reread; LOCAL-CONVERT. Outside research: Haken, Cook, Kremer–Nisan–Ron one-round communication, Fano/INDEX, Urquhart. Search absence is not novelty proof. The full source, separate independent referee and detailed raw controls are also available in the reproducibility archive.

**OPEN NEXT:** a representation-inclusive all-input invariant, or a genuine B3 implication SAT in P => polynomial worst-case W_Rmix341 for the same fixed R, with polynomial cost reflection and same-machine T/S. No task, schedule, rules or weights changed.

**References:** (1) Haken, TCS 39 (1985), DOI 10.1016/0304-3975(85)90144-6. (2) Cook, SIGACT News 8(4) (1976), 28-32. (3) Urquhart, JACM 34(1) (1987), DOI 10.1145/7531.8928. (4) Kremer, Nisan, Ron, STOC 1995, DOI 10.1145/225058.225277. (5) Cook, Reckhow, JSL 44(1) (1979), DOI 10.2307/2273702.