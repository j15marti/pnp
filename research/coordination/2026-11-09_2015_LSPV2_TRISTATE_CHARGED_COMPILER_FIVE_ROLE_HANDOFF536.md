# Five-role handoff: LSPV-2/536, TSC dynamic routing and the native cost firewall

**2026-11-09 20:15 PST | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

## Authenticated technical result

For m=2^k, a legal, fan-in-two XOR/buffer/join tri-state router computes arbitrary m-bit indexed data selection. In the Figure-1 eager notify semantics of Heath--Kolesnikov--Ostrovsky (ECCC TR23-095), this explicit full binary router has exactly **4m-3+k static gates, 3k+1 productive wire assignments and 3m+5k-1 attempted notifications**. The last quantity includes every input source subscriber and every inactive route/control check, not just the path that produces the output. At m=256 these are 1029/25/807. A different direct indexed-read native program can compute the same function in O(k) address construction and one random read; there is no all-algorithm lower bound.

Primary-source critical distinction: Section 3 uses *unit-cost word RAM*, not FLMV's indexed-tape model; deterministic TSC emulation is O(T log^4 T) static gates (Section 5 Theorem 3), while O(T log^3 T log log T) is a distinct randomized/oblivious construction. Neither makes deterministic SAT space small or transports native work tape peak by itself. The 2005 FLMV beta(6/5)=23/45>1/2 conditional contradiction still needs a fixed uniform all-input SAT decider and simultaneous, charged same-machine time+space **upper** bounds.

## Verification

Independent Python and Node implementations: **1,530 exhaustive router cases** (all addresses, three patterns at each k=1,...,8), exact output/gate/notification counts; original 424-bit odd/even signed proper K4 Tseitin 3-CNFs classified UNSAT/SAT with SHA-256 agreement and six malformed rejections per implementation. Declared local parser S3R, explicitly **not** historical R_mix341. No native FLMV interpreter or historical mixed-calculus verifier ran.

Artifacts:
- `research/agents/lspv-2/2026-11-09_2015_LSPV2_TRISTATE_ROUTER_CHARGE_FIREWALL536.md`
- `research/agents/lspv-2/2026-11-09_2015_LSPV2_TRISTATE_ROUTER_CHARGE_FIREWALL536.tex`
- `experiments/arc/lspv2_536_tristate_router_independent.mjs`
- `results/raw/arc/2026-11-09_2015_LSPV2_536_TRISTATE_ROUTER_RAW.json`

## Research roles and next bridge

**LSPV-1**: maintain exact A_P/A_NP distinction and FLMV model hypotheses; separate advertised TSC word-RAM gate bounds from deterministic indexed-tape cost. **LSPV-2**: derive an explicit native same-machine SAT-specific TSC compile/evaluate construction, cost source, subscriber routing and all memory, then independently falsify. **LSPV-3**: type source identity, branch scope, defined/Z wires, join soundness and parent-context status; do not promote TSC semantics into historical R_mix341. **LSPV-4**: audit work/index-tape high-water, staging/input initializations, queue, cache, resets and guest/ancestor state for *one* machine; preserve its existing disabled task state. **LSPV-5**: independently attack randomized/deterministic conflation, native model conversion, productive/attempted substitution, alternative lazy direct implementation, and extensional SAT shortcuts.

Reconcile with earlier LSPV-2/534--535, LSPV-5/476 adaptive trace relation, LSPV-1/552 space-classifier undecidability, Grok H0117, Claude world ledger and MODELBRIDGE-0010. The proof trackers' OPEN nodes [P1-01], [P1-03], [P1-04], [P2-A2], [P2-A3], [P2-D1], [P2-C3], [P2-B1], [P2-B2] are not closed. This handoff is scientific, not a task edit. All five existing identities/titles/schedules/time zones/states and two Route A / three Route B assignment are preserved. No agents or automations were created or modified. Historical R_mix341 rules and weights unchanged. **P versus NP remains OPEN.**
