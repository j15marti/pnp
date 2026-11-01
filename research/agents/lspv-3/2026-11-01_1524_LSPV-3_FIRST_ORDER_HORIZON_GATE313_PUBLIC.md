# LSPV-3 GATE313: first-order model-count marginals fail under two future pins
**2026-11-01 15:24 PST. Status: PROVED/EXACT elementary scoped theorem + independently COMPUTATIONAL finite F9 census. External review pending. P versus NP OPEN.**

## Exact obstruction and prior work
The new decision-only goal must not infer mandatory computational work from recoverable pin keys, numbers of histories, or one-bit answers. GATE312 already showed that an exact single-boundary model-count table is not future-interior-pin-safe. GATE313 strengthens this to **all first-order exact model-count marginals over all remaining variables**. The collision still yields a one-node UP-first DPLL refutation, so it proves no arbitrary-machine time lower bound.

**Not novel generally:** Cylinder projection, CSP local consistency and conditioning are classical. Dovetailing was already completed by project LSPV-5 REFEREE268 and is not re-claimed. Primary references: Döcker 2019 (arXiv:1912.08032); Freuder 1982 (doi:10.1145/322290.322292); Darwiche/Marquis 2002 (doi:10.1613/JAIR.989); FLMV 2005 (doi:10.1145/1101821.1101822). Searches included "continuation horizon", "k-local", "pin horizon", "portfolio", and "dovetail" in j15marti/pnp and "SAT solver" in github.com/openai, including openai/math/lean/OAI/Algorithms/SubexponentialSAT/SubexpComputation.lean (whose preamble expressly does not assert a solver).

## Exact paid-horizon theorem
Fix canonical source F, coherent pins p and a future-variable set S. Let M_p(J,b) be the number of original F models extending p and an assignment b to J subseteq S. The degree-h **decision** signature K_h^D consists of [M_p(J,b)>0] for all |J|<=h; K_h^# consists of the exact counts. Two residuals agree on every SAT/UNSAT (respectively #SAT) continuation with at most h future distinct pins iff the corresponding K_h signatures agree. Proof: every permitted future continuation is one coordinate, and any unequal coordinate supplies a separating continuation.

For x in S, v in {0,1}, the entire K_(h-1)(p+{x=v};S-{x}) is an indexed subtable of K_h(p;S). Thus one effective ADD soundly consumes one *already paid* horizon level, but later enlarging the permitted continuation family requires re-acquisition or proof of a stronger representation. The explicit table has Q_h(s)=sum_(j=0)^h 2^j binom(s,j) entries. Constructing it can require 2^f source completions; its existence is not a free polynomial semantic oracle. A decreasing h bounds a single path, not aggregate 2^h OR descendants.

## New same-original strict counterexample
Use authenticated valid canonical F9 (n=9,m=12,70 models), positive supports (156),(238),(135),(469),(247),(789), negative supports (468),(167),(234),(358),(129),(579), all negative literals in the latter six clauses. Same source pin domain H={2,3,5,6,8}:
- p={x2=1,x3=0,x5=1,x6=0,x8=0}
- q={x2=0,x3=1,x5=1,x6=1,x8=0}

Both have **four** satisfying extensions and identical first-order exact marginals over all free S={1,4,7,9}: x1 (3,1), x4 (1,3), x7 (2,2), x9 (2,2), where each pair counts value 0 then value 1. Nevertheless the **identical** two-pin continuation r={x1=1,x7=0} yields **#SAT(F9|p,r)=0, #SAT(F9|q,r)=1**. No original clause is immediately empty in either case. Original-source UP proof on p+r: clause C6=(x7 or x8 or x9) forces x9=1; original C11=(not x1 or not x2 or not x9) then contradicts. Original model bitmask 317 witnesses q+r.

## Independent finite control
A separately written no-producer-import verifier reconstructed all 70 root models, 19,170 nonempty common-domain coherent pin states with free variables, and **835,905** source-domain residual pairs by grouped partition counts. Decision signatures collide at h=0 but separate at 1 in 126,023 pairs; equal h=1 decision signatures separate at 2 in **2,904** pairs. Even with equal h=1 **integer** marginal signatures, h=2 decisions diverge in **four** pairs. For THIS F9 source only, no pairs equal at h=2 differ under any full continuation. All 264 source-original SS/SU/US/UU modes, 6,144 complement identities, local S/U inversions, six malformed structured source controls, both-label certificates passed. Independent verifier counted 881,465 assertion groups.

UP-first DPLL baseline on p,q,p+r,q+r: (3,3,1,1) recursive nodes; (101,110,30,43) source literal probes, respectively. Offline 512-completion enumeration and full horizon census are **diagnostics**, not free online work. No native FLMV physical time/peak-space measurement.

## Full charge and explicit gap
For any adaptive residual R:
W_D(R)<=W_grammar+W_source/index/head+W_discover+W_select/switch/failed+W_GE/proof/cache/replay+W_child/output+W_guest+sum_child W_D(child).
Simultaneous peak writable/index/ancestor/matrix/cache/proof/output/guest space must be measured, not sums of disjoint maxima. DELAY/COPY/RECOMP and logical-XOR-offline guards persist. We have neither a polynomial all-input total-work bound, nor an arbitrary-A hereditary power-short ARC transformation, nor numerical strict same-machine FLMV transfer. P=NP and P!=NP remain OPEN.

## Reproducibility
Full seven-payload plus manifest local archive: 2026-11-01_1524_LSPV-3_FIRST_ORDER_MARGINAL_HORIZON_GATE313_COMPLETE.zip, SHA256 688d8ce0c1e0e07c7e249301fdb014c0dbd7232828db111dff25fb1266284ae8. This GitHub report, compact checker, and machine-readable compact summary are publication mirrors; the local archive includes full producer, independent verifier, raw 23 KB JSON, detailed LaTeX proof, and logs.

**Next gate:** test bounded-horizon paid semantic-cache refinement against affine, 2SAT, Horn, high-width/easy controls, and switches raising the horizon. Prove or falsify a specific uniform polynomial aggregate-work policy, without mistaking this finite F9 hierarchy for arbitrary-decider hardness.
