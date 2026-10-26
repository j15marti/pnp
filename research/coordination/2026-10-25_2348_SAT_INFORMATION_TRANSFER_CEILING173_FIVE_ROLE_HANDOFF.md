# SAT-INFORMATION-TRANSFER-CEILING173: independent LSPV-5 archive and proof-DAG handoff

Timestamp: 2026-10-25 23:48 America/Los_Angeles. **P versus NP remains OPEN.** The current coNTIME/circuit/ARC-FLMV proof route has no universal affordable all-UNSAT certificate coverage or general same-machine favorable contraction.

## New restricted exact statements

1. For total f(X,Y) with private p and q bit inputs and both parties knowing the output, the deterministic communication complexity is <=min(p,q)+1. For an arbitrary adaptive transcript Pi, I(X;Pi|Y)+I(Y;Pi|X)<=p+q. A large single raw-input communication matrix cannot alone imply superlinear unrestricted SAT decision time.
2. A deterministic indexed-input machine with at most B counted transferable configuration bits and at most r private-input-owner changes gives a deterministic protocol of cost <=(r+1)(B+O(log(N+T)))+O(1). The owner-change premise is crucial; direct random-address probes and rereading are allowed and charged.
3. The previously known PASSMEM84/CUTFLOW85 proper-3CNF equality construction E_k(u,v) has SAT iff u=v, with n=5k,m=8k and fixed-width N=(32k+2)ceil(log2(64(13k+1))). It has deterministic communication cost k+1 and an ordered one-pass Omega(k)-bit retention requirement, yet a total input-indexed O(N polylog N)-work, O(log N)-space canonical recognizer.
4. New independent negative-certificate observation: every UNSAT E_k(u,v) contains eight input clauses constituting a seven-resolution-inference refutation. An index i with u_i != v_i identifies the refutation in O(log k) bits, and a random-access verifier checks the eight exact signed clauses and resolution steps in polylogarithmic cost on a *valid canonical* source. This is a SHORT UNSAT PROOF ON A FAMILY, NOT coverage for arbitrary UNSAT CNFs. For malformed or other ordinary strings this special recognizer is insufficient without paid fallback.
5. Two genuine Shannon pin/properization levels preserve SAT/UNSAT and ordinary distinct-variable 3CNF syntax on the tested instances, but the children remain parent-scale for fixed pin depth. This is not ARC contraction.

## Reproducibility

Independent standard-library `information_transfer_sat_cut_audit.py`, seed 20261025; `information_transfer_sat_cut_results.json`: 1,604 SAT/UNSAT sources (182/1,422); all 1,422 UNSAT instances accompanied by seven-step resolution refutation; 336 two-level properization controls; 10,378 assertion-accounted checks; zero failures. Full program SHA256 950372c940b6898b6bebac26be4cf4851fc27b99519c9da851ed45591e645662, raw JSON SHA256 d053a34b5084de70e76aa8d2760bbf902fb7032a9e61fb036ae298606f8945c0. Bit-work, peak FLMV bits, actual state flips, and bit-time were not instrumented; no extrapolation to unrestricted algorithms.

## Prior art and nonduplication

- `research/agents/lspv-1/2026-10-23_1555_LSPV-1_CUTFLOW85.tex`: *same exact E_k* grammar, local-input-head k^2/S lower bound and indexed bypass. Its earlier PASSMEM84 is precedent; not newly claimed here.
- `research/review/coordination/model_bridge.md`, MODELBRIDGE-0006: raw-input deterministic communication ceiling plus Horn disjointness, not an all-SAT decision-work lower bound. Preexisting ceiling acknowledged.
- `research/agents/lspv-2/2026-10-13_0224_LSPV-2_INFOFLOWCHAIN1.tex`: Shannon temporal information transport ceiling <=N and copy/parity countercontrol, not independent semantic work.
- `main.tex` / `main13.tex`: current root circuit/coNTIME certificate coverage gap and conditional ARC/FLMV endpoint, no new proof claim.

Primary literature checked: FLMV JACM 2005 Cor 5.8/5.9; Williams small-space SAT; Jain-Neoh-Stephan sparse SAT `O*(1.1199^((d-2)n))` with signed (2,2) d=4 giving `O*(1.25417601^n)`; Jiang-Cai 2026 randomized 3SAT `O*(1.307031578^n)`; Ben-Sasson-Wigderson resolution width/size; Hong-Kung fixed-DAG I/O; Dinur restricted random-query BP; communication-complexity fooling sets. Statements are tied to their original models.

## Rejected transfers and remaining implication

**FALSIFIED/RETIRED AS GENERAL TRANSFERS:** a large fixed raw-input communication matrix forces superlinear SAT work; an ordered one-pass retention lower bound applies to indexed random-access SAT machines; high communication complexity forces long UNSAT refutations; the existence of an exponential SAT upper bound proves any SAT lower bound; a fixed proof-system lower bound binds arbitrary decision algorithms.

**PROVED/EXACT restricted:** communication ceiling, owner-crossing simulation, source-layout equality family, seven-step local negative certificates.

**COMPUTATIONAL:** listed finite tests, not matched physical-machine resource measurements.

**OPEN:** a noncircular all-algorithm resource lower bound or a uniformly affordable, SOUND COMPLETE all-UNSAT adaptive certificate family; an all-input same-machine ARC route reaching strict FLMV endpoint; P versus NP. A tiny certificate for one source family neither proves nor disproves worst-case UNSAT certificate lower bounds.

## Archive coverage and pending files

Full bodies read in this run: current AGENTS.md, CODEX.md, research skill, root main.tex relevant executive, main13.tex, CUTFLOW85 and handoff, INFOFLOWCHAIN1, model_bridge.md, semantic_communication_ceiling_audit.py. GitHub queries: information transfer SAT source cut; COMMUNICATION-CUT; EQUALITY family SAT communication; source-input communication ceiling; cut transcript SAT; CELL-PROBE. These are bounded default-branch search results, not exhaustive mathematical review. Historic 3,532-file pinned survey was not repeated. Unread remain latest peer revisions not targeted, broad Drive and prior chat material, original HEREDITARY-SCOPED10 source and full circuit-certificate continuation bundle not attached here. No absence is inferred.

NEXT: prove a source- and algorithm-independent information-transfer obligation on a defined predecision same-machine state, not just a communication matrix; separately test whether candidate certificate grammar soundly covers every UNSAT input with a polynomially checkable branch partition. Attack the claim with canonical equality UNSAT (short proof), affine Tseitin (Gaussian elimination), Horn, 2SAT, cached/reread direct deciders, invalid certificates, and connected both-label controls. Do not force a prechosen proof system upon a one-bit decider.