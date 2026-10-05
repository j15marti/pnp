# CUT-BOTTLENECK-AUDIT1: restart-charged information transfer

Date: 2026-10-05  
Status: COMPUTATIONAL finite experiment plus CANDIDATE accounting refinement.  
Global status: P versus NP remains OPEN.

## Target

Test whether the recent multilayer accounting separation can replace "information becomes unavailable" by a charged computational cut. The adversary is allowed to retain state, reread the source, or recompute. Restart is not prohibited. The candidate charge is information that must cross the cut by any of those channels.

Exact finite target in the direct-address model:

For K independent continuation bits and S retained coordinate bits, test whether the unresolved K-S bits must cross after the cut through source access/recomputation.

This is not asserted for arbitrary SAT computation.

## Corpus reconciliation

Reviewed repository governance, CODEX protocol and pnp-research skill; root main.tex; TASK-004 Static-to-HEC; HEC-SAT proved core; current multilayer coordinate specification; indexed HEC/VSC-HEC/CCSPC/REREAD1/REACQ1 material. The central idea is not new: TASK-004 already asks for a store-or-recover theorem and explicitly charges reread/recomputation. This run refines the candidate resource by separating raw operation counts from continuation-equivalence information.

Duplication audit: this work should be treated as a refinement of TASK-004/HEC, not a new independent proof spine.

## Literature preflight

KNOWN THEOREM in its own model: Patrascu-Demaine dynamic cell-probe lower bounds charge memory probes and prove amortized tradeoffs for specific dynamic problems.

KNOWN THEOREM in its own model: Alman-Wang-Yu online communication presents future input pieces sequentially and prevents the batching shortcut available in classical communication, yielding cell-probe lower bounds for dynamic problems.

KNOWN THEOREM with limited SAT scope: Fortnow proves model-independent SAT time-space tradeoffs in a restricted near-linear-time/sublinear-space region. This does not rule out arbitrary polynomial-time SAT.

Transfer classification: cell-probe/online communication is ANALOGY/CANDIDATE for unrestricted static SAT until a model-preserving Static-to-HEC compiler is proved. Fortnow is a direct SAT theorem but does not supply the missing arbitrary-polynomial cut theorem.

## Experiment

Runner:
experiments/return_map/cut_bottleneck_audit1.py

Raw result:
results/raw/return_map/2026-10-05_CUT_BOTTLENECK_AUDIT1.json

Seed: 20261005. The enumerations used here are deterministic; the seed is recorded for consistency with the broader experiment protocol.

### Direct independent-payload cut

For K=2,...,10 and every S=0,...,K, retain the first S independent payload coordinates. All K coordinates remain legal future queries. The other K-S coordinates are answered either by post-cut reread or by recomputation that must access the corresponding source coordinate.

63 cases were tested.

Observed violations of

S + postcut_source_crossings >= K

were zero.

This is COMPUTATIONAL for the implemented finite strategy family. The corresponding direct-address information statement is elementary, but this experiment does not promote a theorem about SAT.

### Continuation-equivalence normalization

For a continuation universe U, define the finite behavior signature Phi_U(x). The relevant finite information target is

I_U = ceil(log2 |{Phi_U(x): x in source family}|).

At K=10:

- arbitrary K-bit payload: 1024 behavior classes, I_U=10;
- affine-index stream H_i=a XOR (b AND parity(i)): 4 classes, I_U=2;
- constant stream: 2 classes, I_U=1.

Therefore raw number of future queries is FALSIFIED/RETIRED as a generic cut-information measure.

### Wrapper attack

RECOMP_REPEAT repeated the same K=10 source crossings 1,2,4,8,16,32 times. Raw crossings grew from 10 to 320 while continuation information stayed 10 bits.

Therefore raw reread count and raw recomputation count are wrapper-gameable. They may be execution costs in a fixed model, but they are not invariant information measures.

## Accounting refinement

Add an environment/recovery distinction:

Lambda_state = information retained in machine state.

Lambda_env = information still recoverable from the source/environment.

For a requested object q, use

RECOV(q) = (S_q, D_q, C_q),

where S_q is the recovery authority/source, D_q is an explicit reconstruction procedure when known, and C_q is its model-matched cost.

For a cut with continuation universe U, also record

I_U = log2(number of continuation-equivalence classes)

or the exact finite ceiling when a bit count is required.

A candidate store-or-recover theorem should not use raw event counts. Its schematic form is instead

retained_information + charged_postcut_information_transfer >= I_U,

with a separate theorem required to translate post-cut information transfer into time/space/probe cost for the declared machine model.

## Hostile controls and barrier audit

AFFINE_INDEX and CONSTANT show that many queries need not carry much independent continuation information.

RECOMP_REPEAT shows raw post-cut work can be inflated without increasing information demand.

Static full-input visibility remains the decisive bypass: an arbitrary SAT decider may reread, preprocess, memoize, canonicalize, or rerun. This run charges those actions conceptually but does not prove they cross a superpolynomial bottleneck.

A polynomial number of reruns of a hypothetical polynomial SAT decider remains polynomial.

Semantic-oracle replacement also defeats any claim based only on extensional decision information unless the proposed cut theorem has a model-matched reason to charge that oracle/source access.

Relativization/nonalgebrization remain OPEN. Nothing here supplies the final hinge.

## Status changes

ADOPTED: resource layer should separately track state retention, environment recoverability, explicit decoder/reconstruction, and model-matched reconstruction cost.

ADOPTED: continuation-equivalence information I_U is a better normalization target than raw query count.

FALSIFIED/RETIRED as generic hinges: raw reread count, raw recomputation count, raw number of future queries, and "information left machine state" without environment recovery accounting.

OPEN: prove a Static-to-HEC compiler or another model-preserving theorem forcing an arbitrary static SAT computation through a cut with large I_U while charging reread/recomputation/preprocessing.

## What changed relative to root main

No load-bearing arrow closed. The result sharpens the already-open HEC/Static-to-HEC branch and gives it a normalized candidate resource. Root main remains correct that HEC/CRS-PPC/CCSPC are restricted-model resources and transfer targets, not unrestricted SAT lower bounds.

## Next target

Construct or falsify a static SAT family/compiler where the continuation-equivalence information across a declared cut is large and where every source reread, recomputation, preprocessing shortcut, or semantic-oracle replacement can be mapped to the same charged model without assuming the desired SAT lower bound.

END_OF_VERIFIED_REPORT::CUT-BOTTLENECK-AUDIT1
