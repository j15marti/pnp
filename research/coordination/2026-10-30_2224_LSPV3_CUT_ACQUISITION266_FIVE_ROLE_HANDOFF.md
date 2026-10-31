# LSPV-3 CUT-ACQUISITION266, five-role handoff

2026-10-30 22:24 America/Los_Angeles (PDT). **P versus NP OPEN.** No agent identity, enabled/paused state, task, or schedule was changed. Existing issue #3 remains the coordination venue.

## Restricted exact theorem (independent mathematical referee pending)
For the canonical cubic-prism vertex parity proper-3CNF source family F_{k,b}, every deterministic correct terminal label/constant-child selector that reads source vertex blocks must read **all q=2k original four-clause blocks on every input**. Proof: toggling one unread charge toggles SAT/UNSAT while changing only that block. For a randomized pointwise-error-epsilon selector, under uniform charges Pr[reads all q] >= 1-2 epsilon and E[# distinct blocks] >= (1-2 epsilon)q. This is a classical parity-query lower bound in a **restricted source-block** model, not an arbitrary SAT time or space lower bound. Source length N=Theta(q log q), so this is Omega(N/log N) distinct block touches, compatible with O(N) source recognition.

Source authentication also yields an exact cut certificate: for any vertex subset S, XOR of the cut-edge variables equals XOR of S's charges. The top k prism vertices yield a parity constraint on exactly k rung variables and 2^{k-1} provably forbidden partial cubes, without mistaking them for a complete UNSAT certificate.

## Measured adverse controls
16 original formulas, 8 SAT and 8 UNSAT, independently checked in 643,952 assertions plus 3 deliberate corruptions rejected. q=6/8/10/12 SAT models 16/32/64/128, corresponding UNSAT models zero; both global endpoints fail for all controls. Rung-first UNSAT DPLL nodes fall 47->39,95->79,191->159,383->319 with authenticated cut; selected event work falls 7698->6946,20855->18818,52564->47422,126705->114282. On SAT the cut checks add work and prune zero nodes. W1 UNSAT and SWAP6 SAT (54 models) require full-size fallback, with 24,823 vs 24,203 and 13,130 vs 12,510 selected events. Signed-renamed prism sources need a more expensive generic group/XOR recognizer; Horn and Krom both labels are controls. Counted proxies are NOT native simultaneous FLMV instruction/space bounds and industrial CDCL benchmarking is pending.

Full raw includes exact original occurrence S/U targets and inversions, 4-bit SS/SU/US/UU indexed clause-pair compatibility, coherent 0^n/1^n, Gray full traversal and flip trails, adaptive strict-descent trails, proof-relevant cut rows/cubes, deterministic policy attempts/failures/guest work, and Python peak bytes.

## Roles
LSPV-1: use the all-block acquisition necessity as a falsifier of free terminal policy choice; do not elevate this restricted query bound to arbitrary-A hardness.
LSPV-2: test source-derived cut/cached RUP certificates inside transactional elimination and power-short child generation, charging source grammar and proof export.
LSPV-3: next test signed-renaming-invariant cheap recognition and actual **source-accessed** policy acquisition on mixed high-width residuals; maintain SAT/UNSAT separation, full fallback and rank/width easy countercontrols.
LSPV-4: map the q distinct block queries, physical N bits, child 8/13 bits, retained group arrays, and full-parent fallback to the exact FLMV same-machine ledger. No native TM certification is claimed.
LSPV-5: referee randomized query bound's quantifiers and the conditional vs actual ARC arrow; ensure root MAIN contains only restricted conclusions.

**Single open bridge:** construct a uniform all-input, hereditary, both-label exact ordinary-SAT A -> Phi(A) with genuinely short ordinary children on every unavoidable guest query, fully charged discovery, strategy switches, source reads, output, replay, retained/ancestor workspace, and arbitrary DELAY/COPY guests. P vs NP remains OPEN.