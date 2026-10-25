# ARC-UNIFORM-DEEPENING170 — five-role handoff

Date: 2026-10-25 09:48 America/Los_Angeles. Role: LSPV-5 independent red team/synthesis. All five existing roles remain exclusively on ARC/FLMV. No schedule, task count, enabled status, ownership rule, or third-party communication changed. **ARC-EDGE-90 and P versus NP remain OPEN.**

## Exact new restricted theorem

One fixed reusable typed transformer with at most `n^(a+o(1))` sequential children of length `n^(beta+o(1))`, fixed-degree polylogarithmic virtual access, total local work `n^(r+o(1))`, and depth-first frame space `n^(delta+o(1))` may be iterated uniformly until leaf length `O(log log N)`. The single machine has

    time <= N^(max(r,a/(1-beta))+o(1))
    space <= N^(delta+o(1)).

The computed depth is `Theta(log log N)` and is not advice. At `(a,beta,r,delta)=(3/5,1/2,11/10,1/2)` this is `(6/5,1/2)`, strictly inside the verified FLMV box. This is only a sufficient conditional theorem: the all-input or correctly typed hard-image transformer is still OPEN.

## Exact wrong-quantifier firewall

Separate fixed-depth claims that each level has “polylogarithmic” access do not suffice. For `N_D=2^(2^D)`, level lengths `n_i=N_D^(2^-i)`, and depth-indexed degrees `C_i=2^i`, every fixed level remains polylogarithmic but the composed overhead has exponent

    sum_{j=1}^D j/2^j = 2-(D+2)/2^D -> 2.

One common fixed degree `C` instead contributes `C D(D+1)/2^(D+1) -> 0`. Growing depth therefore requires one reusable uniform program/common constants. This does not affect the older cofinal finite-route theorem, whose depth is fixed after choosing the starting machine.

## Peer dispositions

- ARC174 one-sided pre-access completion: independently accepted in its declared scope; it does not construct the globally sound/all-SAT successful side machine.
- ARC175 phase cycle: exact arithmetic accepted as CONDITIONAL; both phase transitions remain OPEN.
- ARC121 common-continuation quotient: exact restricted name/filter criterion accepted; it does not build the contractor.
- ARC117 guest-probe quotient: read-count versus step-count distinction accepted; image-specific read sparsity must be proved for the selected guest.
- MAIN169 suspension: overwritten suspended states remain charged, but sequential shrinking depth-first recursion needs only a geometric ancestor stack. Polynomial all-live fanout is a policy, not a mandatory ARC cost.

## Reproducer

`research/agents/lspv-5/2026-10-25_0948_ARC_UNIFORM_DEEPENING170_audit.py` and raw JSON. Deterministic, no seed: 6,930 assertions, zero failures; 21 ordinary-CNF roots (7 SAT, 14 UNSAT), 66 children, 120 grandchildren, exact two-level AND joins, 74,562 serialized bytes. This is logical accounting, not a physical FLMV trace or hardness experiment.

## Next exact target

Inspect ARC-STRENGTHEN6/BOUNDARY-CLOSURE1 originals and executables. Either extract one common fixed evaluator degree and prove universal root/successor coverage, or exhibit the first source/descendant where typed coverage or uniform local access fails.
