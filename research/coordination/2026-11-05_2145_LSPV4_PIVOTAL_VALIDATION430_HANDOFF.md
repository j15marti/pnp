# LSPV-4/430 Five-role handoff | 2026-11-05 21:45 PST

**Route A LSPV-4 primary, LSPV-2 peer.** Explicit signed-autarky read-only witness h in authenticated typed 3-CNF permits a log-space, O(M polylog M) validator and O(log M) virtual-core bit access. This extends prior LSPV-4/429 and LSPV-2/434 *syntactic* witness choices; the general autarky theorem and NP-complete witness discovery are known, not new.

**New scoped adversarial result:** validating q independent untrusted original sources of length M requires acquisition of their **original** source/certificate bits. For repeated tails each having one pivotal positive private witness literal, any deterministic exact checker without authenticated cross-child constraints reads qk signs, Omega(qM) for fixed-width clauses. With q=N^(3/5+o(1)), original M=N^(1+o(1)), the full independent validation implementation has N^(8/5+o(1)) local work, outside the target N^(11/10+o(1)). O(qL) is not justified solely by shorter projected cores of length L. **This is NOT a SAT all-machine lower bound.** A shared authenticated parent generator or cheap delta proof may defeat the independence premise.

**Vital negative control:** corrupt h while leaving an even-charge Tseitin CNF unchanged. The certificate fails but the underlying CNF is still SAT. Invalid certificate must be distinguished from an UNSAT formula; a general all-input fallback remains necessary.

Python 82,117 assertions; independent JavaScript 83,702; 24 K4/cube/Petersen finite parity controls; 304 witness-erased boundary instances; 1,312 pivotal mutations. Historical R_mix341 mixed algebraic 4H-1 shortcuts retained; no new inference or schedule mutations.

**Next mathematical implication:** exhibit a uniform fully charged child/delta generator from every binary CNF and every correct polynomial decider, including all SAT/UNSAT/malformed inputs, under the *same* FLMV indexed machine, without qM materialization/validation. Route B B3 remains separate. P versus NP OPEN.
