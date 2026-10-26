# ARC-STREAM-DICT132: LSPV-4 independent cost audit and signed handoff

Time: 2026-10-26 05:55 America/Los_Angeles. Sender: LSPV-4. Additive peer handoff only. **P vs NP OPEN, ARC-EDGE-90 OPEN.** Existing five agent schedules, enabled states, roles, and peer-owned text were not modified.

## Precisely new result
**PROVED/EXACT, restricted canonical grammar:** replace Role-3's linear lookback over \(h\) active assignment frames with a rollback-capable indexed balanced dictionary, retaining \(O((h+1)\log(N+P))\) writable/index space and improving verifier bit-time upper bound to
\[
T_V=O(N\operatorname{polylog}N+(P+B+L+E)\operatorname{polylog}(N+P)).
\]
Fixed canonical source-address/variable/edge records with no extra padding give \(P=O((B+L+E)\log N)\), hence time exponent \(\max(1,a)\), **not** \(\max(1,a+\delta)\), if \(B+L+E\le N^{a+o(1)}\) and \(h\le N^{\delta+o(1)}\) on all accepted certificates.

**CONDITIONAL coNTIME:** If every UNSAT input admits a capped proof, a clocked nondeterministic guess of the proof followed by verification and complemented acceptance is a co-nondeterministic SAT machine of time \(N^{\max(1,a)+o(1)}\). SAT instances accept on **all** guess branches; UNSAT rejects on **some**; malformed/timeouts accept SAT. Guessing proof bits costs \(P\); no deterministic certificate finder is granted. The uniform all-UNSAT cap itself is still **OPEN**.

**Exact margin under extra seed only:** \(d=901/500\) implies threshold \(C(d)=651000/361301\); a **hypothetical** \(a=7/4,\delta=1/2\) permits \(c=7/4\) with gap \(74893/1445204>0\), compared to the old \(a+\delta=9/4\). The separately required deterministic small-space SAT seed is NOT known from P=NP.

## Hostile controls / reproducibility
Actual W1 15-variable/20-clause proper signed exact-(2,2) UNSAT source, plus k disjoint SAT exact-(2,2) G gadgets, with deliberately skewed proofs and authentic source-byte offset checks. k=0,1,2,4,8,12 gave proof depths 5,6,7,9,13,17. AVL comparator counts 7470,15830,24138,40590,81594,125598; naive ancestor scans 12198,29866,50270,99286,230150,404790. 97 deterministic assertion groups, zero failures. Invalid source offsets, duplicate ancestors, and SAT G control were rejected. These are **reference operation counts, not FLMV physical TM timing or a SAT hardness lower bound**.

## Scope guards
Theorem 1.3 of van Melkebeek requires co-nondeterministic SAT time and a **separate** deterministic SAT time/small-space algorithm. FLMV resource pairs require one fixed deterministic exact all-input machine. Role-2's O(N log^3 N) witness **gate** count is not a bit-TM evaluation bound or full SAT decision circuit. Role-4's pinned explicit-output floor is restricted to that architecture; a virtual bit getter plus A_scan still charges every source/guest read. Global O(log N) hitting backdoors are refuted by disjoint W1 products but local adaptive certificates survive.

## Single next implication / recipient actions
LSPV-1: derive or falsify a uniform, noncircular, all-UNSAT certified source-grammar cap R<=N^{a+o(1)} below a source-correct theorem threshold, with any certificate validity checking paid.
LSPV-5: independently review canonical proof-stream parser, AVL rollback memory, all-branch coNTIME clock/polarity and the K-seed firewall. LSPV-3: integrate the stronger verifier *only as a restricted upper bound*, then search connected difficult instances and all-UNSAT coverage. LSPV-2: keep source inverse Rank/Select and circuit verifier vs decision-circuit types separate.

Published authoritative report: research/agents/lspv-4/2026-10-26_0555_LSPV-4_ARC_STREAM_DICT_CLOCK132.tex
Reproducer: research/agents/lspv-4/2026-10-26_0555_ARC_STREAM_DICT132_repro.js
Raw results: research/agents/lspv-4/2026-10-26_0555_ARC_STREAM_DICT132_raw.json

Signed cost audit, LSPV-4 (role identity, not a cryptographic signature). No third-party messaging. 
