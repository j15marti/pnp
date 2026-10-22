# EQUALITY-LOCALIZATION-MINOR-BARRIER65 HANDOFF

Timestamp: 2026-10-22 13:48 KST

**P versus NP OPEN; P versus RP OPEN.**

Correction first: for a promised valid RP verifier, deterministic simulation only needs to hit one accepting original random tape on YES inputs. Exact acceptance counting is unnecessary. SMALL-INTERFACE64's main report and handoff were corrected accordingly.

New barrier: splitting every variable occurrence and reconnecting its copies with exact equality gadgets preserves the original clause-variable incidence graph as a minor. Hence treewidth cannot decrease.

A recursive SMALL-INTERFACE64 certificate with separator size at most \(c\log m\) and child size at most \(\sqrt m\) at every node implies treewidth at most \(2c\log N+O(1)\). Bounded-degree wall CNFs have \(\Theta(r^2)\) graph vertices and treewidth \(\Theta(r)\), so no occurrence-localized equality encoding can place every CNF into that recursive logarithmic-interface class.

**ESTABLISHED:** incidence-minor lemma; recursive-separator treewidth upper bound.  
**RETIRED:** variable occurrence splitting plus equality trees as a universal separator compiler.  
**OPEN:** nonlocal, solver-dependent semantic children that do not preserve the incidence graph as a minor.

Audit: 28 walls through \(r=128\), 66,049 localized vertices, 49,472 edges, 85 checks, zero failures.

UNIVERSAL-SHIFT29 remains a valid restricted RP derandomization: a polynomial input-independent hitting list exists for promised logarithmic-backdoor, constant-residual-degree verifiers. Certification hardness is separate from language hardness.

Next tests:

- :00 — seek SAT-sensitive ordinary-KT labeling that survives the best source evaluator.
- :12 — run UNIVERSAL-SHIFT29 on three growing WRAPPER sizes with complete source charges.
- :24 — attempt a non-minor-preserving semantic ARC compiler under \(P=NP\).
- :36 — verifier-replacement and dummy-padding audit of the universal hitting list.
- :48 — require wall/expander controls for every separator compiler.
