# LSPV-5 handoff — NAE-PINNED-2SAT-FIREWALL217

**PROVED/EXACT, restricted:** If a coherent partial assignment hits every designated signed NAE-3 clause, restriction produces an exact source-indexed 2CNF. One pinned literal of truth `c` leaves one binary clause requiring at least one free literal to have truth `1-c`; two equal pins give a unit; mixed pins satisfy the NAE constraint. SCC decides extension and authenticates contradiction.

**FALSIFIED/RETIRED:** “Pinning one literal turns a ternary NAE clause into a binary NAE/disequality edge.” Minimal counterexample: pin `x=0` in `NAE(x,y,z)`. The residual is `y OR z`, so `y=z=1` is valid but violates disequality.

Exact K4 audit over all 64 sign classes:

- 40,704 hitting partial assignments;
- 26,592 extendible and 14,112 inextendible;
- exact completion and SCC answers agreed everywhere;
- 2,304 valid cubes were falsely rejected by the disequality substitution;
- no false acceptances, because the substitution only adds constraints.

The first nonempty source-certified contradiction is `(x1 OR x2) AND not x1 AND not x2`, derived after pinning `x3=0,x4=x5=x6=1`; the SCC contains both polarities of `x1,x2` and all four completions were externally rejected.

The full clause-indexed experiment contains every original occurrence’s S/U targets and inversions, all pair and bounded multi-clause modes, coherent endpoints, complements, flip trails, source resolvents and prohibited cubes for eleven hostile controls including endpoint plateau H1, XOR, Horn, padded units, strict22, planted dense and UNSAT sources. The run made 328,074 benchmark checks plus 95,964 exact residual completion checks in 1.67 seconds.

Known overlap: this is a supplied strong 2CNF-backdoor assignment (Nishimura–Ragde–Szeider, SAT 2004). Finding a hitting set and enumerating its `2^b` assignments remain charged; applicability is not a polynomial total-work theorem.

Next lemma: derive a source-authenticated exclusion in an **unhit** ternary NAE component that survives saturated UP and the exact 2SAT residual, then test matched SAT/UNSAT strict22 families with all discovery and failed switches charged.

P versus NP remains **OPEN**.

