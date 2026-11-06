# LSPV-4/448 five-role handoff | 2026-11-06 12:46 PST

**Allocation unchanged:** LSPV-2 / LSPV-4 Route A, LSPV-1 / LSPV-3 / LSPV-5 Route B. No schedules, identities, historical grammar or weights changed. P versus NP OPEN.

**PROVED/RESTRICTED:** For any connected simple cubic original signed Tseitin 3-CNF, select $k\le H/2$ edges; deleting them leaves $r$ tree and $b\ge1$ cyclic components. EXACT original-CNF UP-open branch count is $2^{k-r}$ (prior /447). Actual SAT-child branch count is $2^{k-r-b+1}$ for even global charge and zero for odd global charge. In even-charge cases, $1-2^{1-b}$ fraction of UP-open branches are still UNSAT.

**Counterexample:** Connected cubic 10-vertex graph formed by joining subdivided K4 copies with a bridge; select bridge ($k=1,r=0,b=2$). Both assignments UP-open; if all charges zero, only one SAT; if odd, neither SAT. Not a growing expander-hard control.

**Verification:** 41,216 Python/independent Node branch classifications, 476 brute-force checks, 32 valid + 48 corrupt-source authentication controls, all PASS. Full mathematics, resource audit and archives in LSPV-4/448 report and user-facing ZIP. This refines KNOWN incidence algebra/LSPV-2/422 and /450, not all-algorithm hardness.

**Route A:** A correct join on multiple residual cyclic components must account for exact boundary syndrome, not just UP-open or local SAT labels. Acquiring the source, computing component relations and executing guests are not free. Universal all-input same-FLMV-machine transformation with both labels, malformed awareness, finite iteration and complete work/space charges remains OPEN.

**Route B:** This graph algebra is a shortcut control only. Do not revise historical R_mix341 or treat Resolution hardness as a mixed rule/all-machine bound. Minimize over all legal shared assumption-scoped AND/OR proof DAGs. B3 OPEN.
