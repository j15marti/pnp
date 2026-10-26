# ARC-DUAL-LOCAL-TRACE187: five-role research handoff

Date: 2026-10-26, Los Angeles. LSPV-1 proof lead.
Scientific status: **PROVED/EXACT restricted local-trace theorem; independent review pending.** The arbitrary-unknown-K ARC/FLMV contraction and P versus NP remain **OPEN**.
This handoff is additive. No new tasks, schedule, enabled-state, agent-count, or peer-owned root changes.

## Mandatory directive and separate ledgers
The original governance file research/governance/2026-10-26_DUAL_TM_RESOURCE_ACCOUNTING_DIRECTIVE.md was retrieved from GitHub. M1 is input-inclusive standard deterministic read/write one-tape TM. Mk has fixed k work tapes and separate sequential read-only input, with distinct visited writable work cells. **Neither is automatically the FLMV indexed-read-only-input random-access model.** With compound input length X (source plus supplied proof), the conservative constructed simulator has T1=O(Tk[X+Sk+log(Tk+2)]), P1=O(X+Sk+log(Tk+2)); consequently t1<=tk+max(1,sk) and p1<=max(1,sk). These are upper construction bounds, not lower bounds on all algorithms; the Hennie-Stearns O(T log T) theorem simulates on two tapes, not one.

## Formal new link
Fix a deterministic total correct SAT decider A in standard sequential Mk. Authenticate a full rejecting computation by source-address reads against immutable source bits, original program's deterministic transition relation, all head movements, initial work blanks, and sorted (tape,address,time) read/write consistency. Then F is UNSAT iff an accepting rejecting-trace proof exists, and every proof fails for SAT F. No parent SAT(A) call is required **by the verifier**. The step-faithful trace has exactly R=T_A(F) transition records, P=O(R log(N+R)) physical bits. A compound-input Mk checker can use T=O((N+R)log^3(N+R)), S=O((N+R)log(N+R)); an explicit bounded-fan-in **witness-verifier**, not SAT-decision, circuit has O((N+R)log^4(N+R)) gates. All source reads, record generation/proof guessing, failed records, unchanged writes, sorting, descendant serialization, and memory storage remain charged.

Actual source variables x,y give four true depth-two residuals F|(x=b,y=c); authenticating rejecting traces for all four is sound and complete for root UNSAT. A SAT parent has a satisfying child and no authenticated rejecting trace there. No special exact-(2,2) residual eligibility is asserted, ordinary SAT is the guest.

## Exact firewall
This **does not improve unknown P=NP exponent K**. The known step-faithful trace ceiling remains N^{K+o(1)} and Mk verification ceiling no better than N^{K+o(1)}. For each fixed r a correct machine can add N^r delayed dummy steps using an O(log N) counter; every one-record-per-transition proof for that machine must account for the extra steps. This falsifies automatic exponent contraction by this restricted transcript grammar, not by other compressed derivations or any arbitrary SAT decider. No d=1.802 small-space seed or FLMV-native contradiction is supplied.

## Reproducible hostile controls
Full standard-library experiment: 32 exhaustive five-bit CNF flag sources (9 SAT, 23 UNSAT); 128 actual depth-two descendants, 32 root joins, 320 corrupted source/head/write/work/clock/output/truncation traces rejected; 1,124 explicit assertions, zero failures. The fixed toy Mk machine used Tk=11, Sk=6 distinct visited work cells excluding 5 source bits, Qk=22 probes, Ck=15 boundary head moves, 11 writes including 6 unchanged, one output bit. An **analytic** conservative M1 sweep upper *budget* is 528 cell visits and 24 cells of footprint, NOT measured one-tape steps or native FLMV exponents. All-input theorem is symbolic for any fixed deterministic Mk A, not a claim that the toy five-bit controls are the full ordinary SAT language. Peer referee review pending.

GitHub artifacts:
research/agents/lspv-1/2026-10-26_1455_LSPV-1_ARC_DUAL_LOCAL_TRACE187.tex
research/agents/lspv-1/2026-10-26_1455_ARC187_trace_audit.py
research/agents/lspv-1/2026-10-26_1455_ARC187_trace_results.json
Seven-page expanded PDF, source .tex, full code, raw JSON and BibTeX are provided in the conversation bundle ARC187_DUAL_LOCAL_TRACE_PROOF_BUNDLE.zip.

## Five roles, unchanged schedules
Role 2: attack low-workspace event authentication or its limits, keeping verifier gate count distinct from deterministic SAT decision circuits.
Role 3: construct sound **non-step-faithful** source-authenticated proof rules, and prove one all-UNSAT cap, including connected hostile cases.
Role 4: independently check compound-input X, input-inclusive one-tape footprint, Mk physical traffic, FLMV-native model/simulation conditions and strict margins.
Role 5: red team the DELAY wrapper and any source/work provenance, model mixing or sign-blind residual DAG merging.
Role 1: update formal proof DAG and seek an actual unknown-K improving, fully charged successor without assuming a small-space seed.

## Reconciliation
ARC184 J_F first-conflict selector remains cheap but parent-UNSAT totality authentication is coNP-complete. ARC186 BRANCH/EMPTY/PATH grammar was already known to be resolution-simulable and exp-hard for connected Tseitin controls; ARC187 does not repeat it. The cited original peers Role 2 INVERSE-SORT166, Role 3 SOURCE-POINTER-STREAM131, Role 4 PINNED-CIRCUIT-OUTPUT-FLOOR131, and Role 5 BACKDOOR-CAP161 were read, together with later reports. No evidence attributes claims to an unread PNP_Circuit_Certificate_Continuation.pdf.
**OPEN:** arbitrary unknown-K coverage/contraction, same-machine native FLMV box, ARC-EDGE-90, P != NP.
END_HANDOFF::ARC-DUAL-LOCAL-TRACE187
