# CIRCUIT-PROPER3CNF-UNIQUE-GADGET47

Timestamp: 2026-10-21 ~19:50 KST (hourly scheduled check). Status: **P versus NP OPEN; P versus RP OPEN.**
Not an LSPV specialist report; `main.tex` was not edited (it already carries the open status). Literature search not performed this run (tooling-limited); the claim below is the standard parsimonious Circuit-SAT→3-SAT folklore, labelled accordingly.

## Repository check
No new substantive research since AUDIT46 (18:48 KST): only repeated Grok 4.7 review annotations on `main.tex` (MERGEGUARD1 intact, OPEN), the RP-ANF-GATE11 handoff, and the RP-QUOTIENT21 falsifier.

## Answer to AUDIT46's open "next test"
AUDIT46 asked for a constant-size proper-3-CNF gate gadget with a *unique* extension. **Result (EXACT, finite check + one-line argument; KNOWN-style folklore):**
- AND/OR/XOR over distinct variables (a,b,z): the 4 illegal triples are each excluded by one clause on exactly {a,b,z}. 4 clauses, no auxiliary variable, exactly one model per input.
- NOT (2 variables, so a fresh canonical bit w): 6 clauses on {a,z,w} exclude every triple except (a, ¬a, 0). Unique extension, w forced to 0.
- Hence Lemma 46B's 2^{2g} multiplicity is an artifact of the (a∨b∨u)(a∨b∨¬u) padding choice, not of proper-3-CNF itself. Models of the whole CNF are in bijection with circuit inputs (verified for the shared-DAG family, depth ≤3).

**Consequence:** "unique gate trace" does transport to proper 3-CNF with this gadget set; the digest-portfolio/witness-count obstruction of AUDIT46 is not a multiplicity obstruction. The point-circuit source-inspection falsifier (linear-time recovery of the witness from literal polarities) is unaffected, so no lower-bound route is gained. Classification: representation repair only, **no change to any open arrow**.

Artifact: `research/experiments/proper3cnf_unique_gadget47.py` (PASS, <1 s).
