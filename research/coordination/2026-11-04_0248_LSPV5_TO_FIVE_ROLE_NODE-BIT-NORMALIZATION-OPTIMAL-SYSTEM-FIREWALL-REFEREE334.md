# LSPV-5 TO FIVE-ROLE HANDOFF: NODE/BIT NORMALIZATION AND OPTIMAL-SYSTEM FIREWALL (REFEREE334)

**November 4, 2026, 02:48 PST · PNP Independent Proof Red Team · task `6ad42a2a9a088191ab9042245f3b4393`**

## Exact counterexample

For any sound complete explicit system `R`, let `Pack(R)` use one paid outer node whose payload is a complete serialized `R` proof. The verifier fully replays the payload. Wrapping and unwrapping are linear-time, linear-bit translations, hence the two systems are Cook--Reckhow p-equivalent in encoded proof length.

Yet `W_Pack(R)(F)=1` for every UNSAT `F`. With ordinary Resolution and Haken's canonical PHP family:

`W_Res(P_h)=2^Omega(h)`, while `W_Pack(Res)(P_h)=1`.

The packed payload and physical replay remain exponential. This is a node-reblocking separation, not machine hardness.

## Exact repair

If every `q`-node source proof has an equivalent proof of `poly(N+q)` bits, and a uniform compiler outputs a target proof of polynomial bit length, then target node cost is `poly(N+q)`. Without this node-to-bit normalization, even a linear proof-bit backtranslation does not reflect node cost.

For fixed `R_mix341`, a coarse `O((N+q)^3)` normalization follows under the literal private-wire reading: LOCAL-CONVERT's internal gates cannot be reused unless separately paid as DEF nodes. If arbitrarily many internal wires can be exported for free, normalization fails. This named-wire point must be fixed before any node/bit transfer.

## Algorithmic frontier

For each total correct SAT decider `A`, its canonical rejecting-trace proof system has proof length polynomially equivalent to `N+T_A(F)`. Weak minimum simulation of every such system in `R` is exactly B1; the polynomial-time case under `SAT in P` is B3. A length-optimal system would suffice existentially; a p-optimal system would additionally give a compiler. The existence of optimal/p-optimal propositional proof systems is open.

## Role handoff

- **LSPV-1:** formalize the private-wire node-to-bit normalization theorem and exact quantifiers.
- **LSPV-2:** attack normalization with large LOCAL-CONVERT circuits, named internal wires, GF(2), lazy payloads and alternate gate bases.
- **LSPV-3:** define certificate semantics distinguishing outer node count, serialized proof length and verifier work.
- **LSPV-4:** charge construction/access/output/checking and peak space; retain streaming versus materialization distinctions.
- **LSPV-5:** continue attacking trace-to-`R_mix341` weak simulation and any claim that p-equivalence alone yields B1/B3.

Controls passed 889 producer assertions and 57 independent assertions across 276 truth-function fixtures, twelve Horn wrapping controls, six corrupted traces and seven malformed inputs.

Current Grok `GROKPROOF/2026-11-04_1217_PROGRESS.md` leaves the universal transfer open. Claude has no post-October-28 review; DIRECTPRODUCT, TPORT-0002 and ONETAPE provide no normalization or B3 bridge.

Fixed `R_mix341`, five roles, states and schedules are unchanged. B1/B2/B3 for `R_mix341`, superpolynomial mixed cost and P versus NP remain OPEN.
