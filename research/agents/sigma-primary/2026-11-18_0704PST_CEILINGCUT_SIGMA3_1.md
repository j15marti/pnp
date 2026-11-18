# CEILINGCUT-SIGMA3-1 | 2026-11-18 07:04 PST

**STATUS: PROVED/EXACT restricted source-certified shared-cutset QBF identity and charged restricted time/space upper bound. Computational: 27,140 checks / 0 failures. Unrestricted hereditary Circuit-SAT contraction OPEN. P versus NP OPEN. Independent review pending.**

## PROPOSE / SEARCH

1. Certify a universally nonempty, `(x,y)`-dependent **box** for shared post-universal cutset `c`, and choose a factorwise dominating extremal point without searching over `c`.
2. Extend to mixed-coordinate **globally consistent signed polarity**: choose the high endpoint for positive coordinates and the low endpoint for negative coordinates. Permit genuine adaptivity and nonunique cutset witnesses.
3. Construct physical local negative Circuit-SAT guests after extremal substitution, charging all source scans, actual inputs, guest calls, copying, and workspace.
4. Falsify unverified polarity, impossible boxes, private-witness-dependent endpoints, moving global x or unique z traces across universal y, source replay, padding, and the dense q² pair-selector firewall.

Directly read `LOCALDUAL-SIGMA3-1`, `SIGMA PATHCUT-1`, `SIGMA29` and `SIGMA30` in this repository. Primary literature: Fortnow et al., JACM 2005, https://doi.org/10.1145/1101821.1101822 ; Bubeck and Kleine Büning, SAT 2007, https://doi.org/10.1007/978-3-540-72788-0_24 ; Kattermann, Hofstadler and Seidl, SAT 2026, https://doi.org/10.4230/LIPIcs.SAT.2026.22 . Monotone-variable elimination itself is elementary and is not presented as a newly discovered general theorem.

## Theorem: dependent extremal cutset for SIGMA3

Suppose an explicitly tagged N-bit source describes

```
Phi = EXISTS x FORALL y EXISTS c,z_1,...,z_q
      [G(x,y,c) AND AND_i C_i(x,y,c,z_i)].
```

Private `z_i` appears only in its own factor; all factors share the exact same `c`. For each cutset coordinate j, source circuits `g_j(x,y)`, `t_j(x,y)` define `lo_j=g_j AND t_j`, `hi_j=g_j OR t_j`. Guard G asserts `lo_j<=c_j<=hi_j`; it is always feasible because `lo<=hi` by syntax. Assign a **single global polarity** `s_j` to each c_j. Every factor is source-certified nondecreasing in `d_j=c_j` if `s_j=+`, or `d_j=NOT c_j` if `s_j=-`. The sign cannot change between factors.

Set `c*_j(x,y)=hi_j` for + and `c*_j(x,y)=lo_j` for -. Then for every x,y,

```
EXISTS c,z_1,...,z_q [G AND AND_i C_i]
    IFF
AND_i EXISTS z_i C_i(x,y,c*(x,y),z_i).
```

**Proof:** A feasible c lies between lo and hi. Changing each positive coordinate toward hi and each negative coordinate toward lo monotonically preserves every factor's truth for the same z witnesses, and yields c*. Conversely, c* satisfies G and its per-factor private z_i witnesses combine into a common global tuple. Apply pointwise in (x,y), without ever moving outer x or post-y cutset c before y. QED.

**Certified source grammar:** A conservative polarity type system checks DAG gates with source-indexed fixed-width records; AND/OR preserve monotonicity, NOT is allowed only for c-independent subcircuits, and globally signed literals encode negative orientations. Source bounds g,t depend only on x,y, not c or private z. Arbitrary factor reconvergence is allowed. Semantic recognition on arbitrary untagged Circuit-SAT is not assumed.

For fixed x, materialize the *ordinary Circuit-SAT* counterexample circuit

```
D_i[x](y) = AND_{a in {0,1}^{|z_i|}}
                 NOT C_i(x,y,c*(x,y),a).
```

Then `Phi TRUE iff EXISTS x such that ALL i have A(D_i[x])=UNSAT`, for any correct fixed deterministic ordinary Circuit-SAT decider A. Each negative answer incurs one real guest call. The bound circuits are physically included in every guest (shared inside that guest only). Neither universal y nor shared c is enumerated.

## Charged restricted resource bound

Assume A has arbitrary unknown fixed time exponent K>=1 and space exponent L>=0; source length N; at most N^beta outer x choices, N^theta factors, and N^delta private z choices per factor. All *serialized* guest circuits, including extremal definitions, copied gates, renaming, wire indices and output, have physical length <=N^(lambda+o(1)). Keep no q-entry writable source-offset table. Scan/validate the N-bit read-only source for each x, and build/execute guests one at a time with space accounting for the physical guest buffer and A workspace.

```
K' <= max(1+beta, beta+theta+lambda, beta+theta+lambda*K)
L' <= max(lambda,lambda*L)
```

With beta=1/50=.02, theta=11/20=.55, delta=1/20=.05, lambda=1/2=.5, and per-factor source bound N^(.45+o(1)), obtain **K'<=.57+K/2** and **L'<=max(.5,L/2)** for K>=1. This is a 0.03 time-exponent margin relative to max(1.1,.6+K/2) **only on the restricted source language**. Dense unpadded factor geometry is consistent: theta+.45=1. A source-checkable cap on actual resulting guest length is mandatory. Parent-sized SAT calls, a free oracle splitter and any semantic certificate discovery are not assumed.

## Falsification and computational audit

- **Adaptive nonunique shared c:** Guard c<=NOT y and factor (c OR y) makes FORALL y EXISTS c true but EXISTS c FORALL y false. An additional unused bounded c bit makes the response nonunique, preserving truth.
- **Mixed-sign conflict:** C1=c, C2=NOT c; individual local witnesses exist but no common shared cutset witness. Without a global polarity certificate, the extension is UNSOUND.
- **Negative occurrence:** With hi=1, C=NOT c, the original has c=0 while blindly substituting hi=1 makes it false.
- **Invalid/private guard:** lo>hi can empty the feasible box; lo,hi depending on a private z_i can silently introduce forbidden inter-factor dependence.
- **Outer existential:** EXISTS x FORALL y (x=y) is false, but FORALL y EXISTS x (x=y) is true.
- **Unique traces:** FORALL y EXISTS z (z=y) is true, EXISTS z FORALL y (z=y) false.
- **Source/guest costs:** Actual guest serialization/replay is tested; all signs, references, negative results and source scans are charged in the conditional ledger. Delayed A_D of large exponent D contributes D/2 at half-size guests; any reached full-parent N^D call would defeat this implementation. Exact native FLMV random-access-machine transfer and work-head addressing remain unverified.
- **Hereditary firewall:** Generated D_i are unrestricted ordinary Circuit-SAT, not necessarily eligible signed-box factor sources. This is NOT an all-input or recursive contraction, and provides NO P!=NP proof.

Independent standard-library Python finite audit: **27,140 check assertions, 0 failures**, 850 randomized serialized c-positive gate DAG sources, 3,172 physically serialized/parsed ordinary SAT guests, 9,534 guest evaluations, and 6,400 signed two-coordinate interval contexts; exact rational exponent controls for K=1,...,20. These are finite correctness and syntax checks, not measurements on the FLMV machine.

## NEXT

Explore *bounded conflicting sign sets*: if r shared coordinates violate global polarity, determine whether branching or an exact low-width separator can preserve the time envelope without q^(2^r) pair-selector expansion. Seek an all-input near-linear source-to-certificate compiler, with full charged discovery and hereditary closure. The unrestricted target remains OPEN.

VERIFICATION_SENTINEL_CEILINGCUT_SIGMA3_20261118_0704PST
