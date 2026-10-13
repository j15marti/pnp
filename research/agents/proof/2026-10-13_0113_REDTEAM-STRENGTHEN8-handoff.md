# REDTEAM-STRENGTHEN8 handoff

Scientific status: P versus NP remains OPEN.

Substantive result:
- ALLFIELD22's neutral-slot arithmetic, 610-clause local support, complementation range, coefficient cancellation, and orbit-wide LP refuter survive independent review in their declared models.
- ALLFIELD22-TO-PREA1 is FALSIFIED/RETIRED. The compiler expands the source; the refuter is a one-sided zero-child terminal. It returns UNKNOWN on every satisfiable input, so any exact fallback is executed once on the current-size parent. It is not an essential smaller child and supplies no all-input PRE-A transition.
- Conditional K elimination is preserved but not instantiated.

Validation:
- bounded script completed in 0.005321 seconds under a 25-second timeout;
- 2,560 complemented threshold cases, 174 PC/PCR identities, 168 deficit pairs, five graph cancellations, and exact 484/610 support arithmetic passed;
- no full 610-clause enumeration, full LP, asymptotic expander test, or proof-degree computation was performed.

Primary model checks:
- FLMV Corollary 5.8 and Theorem 3.1 were checked in the 7 September 2004 author manuscript; the deterministic random-access input/index/work-tape model is the endpoint used.
- Mikša--Nordström Definition 4.6 and Theorem 4.8 were checked in the retrieved 24-page primary source; the theorem is PC/PCR proof complexity over a fixed arbitrary field, not arbitrary machine time.
- The retired unrestricted cosine endpoint is not used.

Artifact SHA-256:
- report: c4409e72ec83a54ff61d767006613705d6c34d95d8001009dbfa951e1dd38467
- code: 414838ef239afbafb1075a7e056c9fa7c015cfb9d33b385f48db93ccd204eb16
- results file: 39c70fe583159931a3c5a01b44afb6afbbbc1ad0a7f11c6ecdbcbf6b586b6712
- main4 addition: d52b6637165f0016c81d8b7feee17624559e8805a21320fb6a98bfa96b4e7088
- main5 addition: d52b6637165f0016c81d8b7feee17624559e8805a21320fb6a98bfa96b4e7088
- exact desired main4 body: 3c2f5d24f283a0662ee6a54621fb0bd55cf0dfd239f2173b5f0ee8d9f86171bf
- exact desired main5 body: 17153899de32ccf4f155e7eb559484faabbfa1a2899d5b13ba4fbbe7f11b2d8d

Root main.tex ownership was preserved. Its current synthesis predates ALLFIELD22; the next authorized LSPV-4/LSPV-5 reconciliation should replace the canonical-layout-only escape with the orbit-wide escape while keeping the solver-independent transition OPEN.

Next target: construct or falsify a source-checkable all-input rule that terminates or emits essential strict children before any parent-size SAT decision, with aggregate volume, access, replay, buffers, state, and recursive closure charged on one matched machine.
