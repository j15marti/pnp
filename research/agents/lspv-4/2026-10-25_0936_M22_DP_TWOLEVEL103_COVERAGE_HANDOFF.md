# LSPV-4 M22-DP-TWOLEVEL103: Additive shared gap, evidence and coverage handoff
25 October 2026, 09:36 Asia/Seoul (24 October Los Angeles). No schedules, task counts, or other agents' work are changed.

Status: KNOWN THEOREM for Davis-Putnam existential variable elimination; PROVED/EXACT within the declared ordinary-CNF fixed-two-level model for the M22 specialization, subject to independent mathematical review; COMPUTATIONAL for finite tests. ARC-EDGE-90, DIRECT-POST and P versus NP remain OPEN.

## Canonical target, receiving obligation and exact construction
M22-NONPAIRED1 means distinct proper 3-variable OR clauses, each entirely positive or negative, each original active variable appearing twice per polarity. C_star excludes only fully complementary-clause-paired formulas; partial pairs, disconnected and easy formulas remain allowed; malformed input is NO. With k original active variables, m=4k/3 and N=Theta(k log(k+2)) bits. Y is a 6-variable C_star SAT control (20 satisfying assignments); U198 is a 198-variable C_star UNSAT original source (published/certificate dependency); H is a fully paired SAT control OUTSIDE C_star.

Exact one-variable simplification: for x occurring twice positively and twice negatively, remove its four parent triples and add at most four Davis-Putnam resolvents, each cross of one positive two-literal tail and one negative two-literal tail. Each non-tautological new resolvent is a proper mixed-sign 4-clause. For every assignment to retained names, the new formula is true exactly when the original has an extension on x. With h non-tautological tail-pairs, m'=m-4+h<=m, literal occurrences L'=3m-12+4h. This result is for ORDINARY CNF and does NOT preserve the M22 grammar.

The primal graph of any M22 source has maximum degree 8, giving a greedy independent pivot batch I1 of size q1>=k/9. These pivots have disjoint original clause neighborhoods. First exact existential projection has v1<=8k/9 remaining occurring variables, m1<=m, width <=4, maximum signed degree 4 each. Its primal graph has degree <=24. A second greedy independent pivot batch I2 has q2>=v1/25 and maximum four positive and four negative parents per pivot, so <=16 generated resolvents, clause increase <=8 per pivot and width <=6. The second existential projection has v2<=64k/75, m2<=m1+8q2. Fixed two levels use O(N polylog N) elementary bit work and O(N) writable/index space with explicitly built incidence indices and ordinary child buffers; output encodings remain O(N) bits. The time-space bounds apply to one materializing implementation and cannot meet the FLMV small-space endpoint. A source-queryable lazy address contract was NOT demonstrated.

## Two-label controls and exact computational scope
Independent local Python enumeration verified all 72 complete projection rows on small Y and H, with zero failures. A separately coded JavaScript audit read the complete GitHub U198 original source (blob f9dda41a810ad8e02bd553f2711a26a4050861f9), verified 198 names, 264 distinct proper clausewise-monotone triples, 2+ and 2- occurrence counts, and absence of complementary clause partners, and performed both actual elimination levels. U's UNSAT status was imported from Döcker's original construction and previously certified project source, not newly proven by 2^198 enumeration.

Control Y (C_star SAT): v 6 -> 5 -> 4, m 8 -> 5 -> 4, literal occurrences 24 -> 16 -> 14, pivots 1 then 1.
Control H (paired OUTSIDE C_star SAT): v 6 -> 4 -> 0, m 8 -> 4 -> 0, literal occurrences 24 -> 16 -> 0, pivots 2 then 1.
Control U198 (C_star published UNSAT): v 198 -> 156 -> 132, m 264 -> 264 -> 330, literal occurrences 792 -> 960 -> 1588, pivots 42 then 24. First stage contains 96 width3 and 168 width4 clauses; second has 60 width3, 58 width4, 96 width5, 116 width6. The first 42 U pivots each generated four surviving resolvents with no clause-count improvement. At second level 28 raw resolvents were removed by tautology/duplicate filtering.

Disjoint repeated U and Y provide unbounded opposite-label test families whose outputs under this fixed two-level policy have Theta(N) encoded length. These are easy recognizable controls, NOT evidence of a structurally difficult family or unconditional lower bound. Variable-count contraction by a fixed fraction is not a fractional-power encoded-size contraction.

## Direct post-acquisition potential firewall
For the *particular* complete-state potential required to equal 2^v at committed exact-CNF representation checkpoints, the first charged post-acquisition batch makes Phi drop by at least 2^k - 2^(8k/9) in O(N polylog N) primitive work. A per-transition inequality Phi(C)-Phi(C')<=Gamma(N)*charged_work valid for every state transition would require Gamma(N) at least that exponential drop divided by O(N polylog N). Therefore polynomial-Gamma complete-state extensions of raw candidate volume 2^v are FALSIFIED/RETIRED. Different independently grounded structural potentials remain OPEN. Acquisition is not counted twice; no direct SAT/UNSAT label oracle or mandatory enumeration is assumed.

At the optional U198 two-level enumeration checkpoint with one residual of 132 variables, Psi=2^132 and R_search=198-log2(Psi)=66. This describes an available exhaustive upper budget, not the cost of the actual adaptive decider, and is not mandatory work. No post-acquisition all-algorithm lower bound is established.

## Charged resource, same-realization and endpoint warnings
The one selected policy pays source parsing/access, grammar check when necessary, pivot discovery, neighbor marking, incidence indices, resolvent pairs and tautology checks, duplicate comparison, headers/IDs, source/workspace reads, writes including unchanged writes, arithmetic and address control, failed tests, intermediate representation, caches and peak ancestor buffers. Witness reconstruction is only required if a witness output is demanded; one-bit deciders need not emit it. Actual state flips, primitive work, bit traffic, live memory, cumulative bit-time, and circuit gates/wires/switches are distinct; no physical bit-flip or switching measurement was made.

ARC receiver E consists of simultaneous (t,s) of ONE fixed uniform exact total ordinary-SAT decider correct on ALL ordinary inputs in the matching indexed read-only-input FLMV random-access Turing model. The strict forbidden box is t<241/200 and s<11642479/23232400; beta(c)=((c+2)/c^2-c)/2. Historical universal t+s<2cos(pi/7) endpoint is retired. No all-input favorable successor or finite cofinal route was achieved; target-only solver cannot be applied to mixed ordinary children without an independently proved charged adapter. All proof-system/query/model-counting endpoints retain their separate model boundaries.

## Archive manifest, duplication and remaining queue
Original full GitHub reads: AGENTS.md SHA c5265db, CODEX.md SHA 754999f, PNP skill b8df83a, LSPV-4 QUAD-NEUTRAL102 report 2d874eb and handoff 3724669, LSPV-5 DD-M33-LOCAL146 bfef451, LSPV-1 LAZY-ACCESS-BRIDGE147 8db94e, SIL-RC VE5 catalogue 3f3255d, LOCALSHIELD1 STATIC-INCIDENCE-CLOSURE5 c827e4, U198 raw source f9dda41. Root main.tex blob c120861 was fetched and synthesis excerpts inspected; main13 and FINAL-LINK-ARC relevant excerpts examined. Bounded queries: M22 variable elimination, Davis Putnam exact 2 2, LOCAL-COOK-TAGGED-SIGNED22, signed occurrence rank. These are not exhaustive searches or full mathematics of all roots. Earlier pinned 55a3fcc census of 3532 hash/keyword searched files remains inherited, not reproduced here. The current 483K+ character root main is not entirely re-proved.

Original primary literature: Davis--Putnam, JACM 1960 DOI 10.1145/321033.321034; Eén--Biere SAT 2005 DOI 10.1007/11499107_5; Döcker arxiv:1912.08032; FLMV JACM 2005 DOI 10.1145/1101821.1101822. Davis--Putnam generic VE5 is standard and already in prior SIL catalogue: not newly claimed. QUAD-NEUTRAL102 add-only repair remains correct within its declared universal neutral-port interface. The new quantitative M22 specialization and two-stage potential countercontrol do not contradict it.

FILLED/RESTRICTED: exact charged two-stage ordinary-CNF existential projection.
PARTIAL: useful adaptive solver rule with signed-degree input parameters; no small target child guarantee.
CONDITIONAL: only a future paid representation/accessor or type-restoring machine composition.
FALSIFIED/RETIRED: neutral add-only repair is mandatory for any elimination; linear-variable reduction implies power-bit shrinking; naive 2^v with polynomial-Gamma complete-state transition Lipschitz bound.
OPEN: true N^(lambda+o(1)) ordinary-child compiler with lambda<1, paid parent gluing, source-to-tagged-signed22 LOCAL-COOK first leg, ARC-EDGE-90 all-input charged cofinal route, noncircular direct post-acquisition all-decider Phi.

Unread: most historic main2--main12/main14 mathematical bodies and revisions; unrecovered HEREDITARY-SCOPED10 executable; original Drive LOG/PROVED_EXACT/Manuscript/BOOL/SIL pagination and earlier chats; many CP22LIFT1/PC22_ALLFIELD1 dependencies and full local Cook tagged signed22 original body. Failed/empty sources are not counted exhausted; no transient local path is assumed shared.

Next artifact: recover and inspect complete LOCAL-COOK-TAGGED-SIGNED22-1, or an independently exact parent-compatible typed compiler, and test fully paid two levels on same-name Y and U with source bit addresses, ordinary encoded child sizes, caches and peak memory.

Published files:
research/agents/lspv-4/2026-10-25_0936_LSPV-4_M22_DP_TWOLEVEL103.tex
research/agents/lspv-4/2026-10-25_0936_M22_DP_TWOLEVEL103_AUDIT.py
research/agents/lspv-4/2026-10-25_0936_M22_DP_TWOLEVEL103_RAW.json
research/agents/lspv-4/2026-10-25_0936_M22_DP_TWOLEVEL103_COVERAGE_HANDOFF.md

<!-- END_OF_VERIFIED_HANDOFF::LSPV-4::M22-DP-TWOLEVEL103 -->
