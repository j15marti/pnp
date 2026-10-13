# ROUNDINGSQUEEZE3: concrete pipeline and dimension-safe frontier

Manual continuation of ROUNDINGSQUEEZE2. P versus NP remains OPEN. This handoff is not a claim of completed scheduled corpus-wide preflight, canonical MAIN publication, root reconciliation, or independent mathematical review.

## Constructed and checked

Implemented the compressed-cylinder port-equivalence construction (Definitions 3.1-3.5 of arXiv:2411.14267v1), the separated 3-CNF index gadget, the prior properization, and the unchanged CP22LIFT1 selector compiler. The toy cylinder has three rows, six middle columns, one boundary column on either side, moduli (3,3,3), 24 original vertices and 45 edges. Port-based edge equivalence yields 24 compressed variables, 15 parity equations, and 96 base clauses (24 width-three, 72 width-four). A checked XOR of six recorded equations is 0=1.

With index width b=2, the separated index formula has 7,776 variables and 9,048 clauses. Properization gives 10,416 clauses. The emitted exact-(2,2) target has 749,952 variables and 999,936 distinct proper three-clauses. An independent emitted-DIMACS checker verified every literal and signed occurrence count. This is a TOY construction check, not an instance satisfying the asymptotic hardness parameters.

For a base with nu variables and C3/C4 clauses, our implemented prefix-chain index encoding has:

- n_lift = 2 nu b + nu max(0,b-3) + 4 C3 b^3 + 6 C4 b^4;
- m_lift = nu max(1,b-2) + 5 C3 b^3 + 7 C4 b^4;
- at b=2, properized m = 2 nu + 6 C3 b^3 + 8 C4 b^4;
- selector target v=72m, M=96m.

The index extension is side-local: for each lifted source clause set the X-side extension to AND of its selector inputs and the Y-side extension to OR of its signed data inputs. The bridge is falsified exactly when the original lifted clause is falsified. Local exhaustive checks also cover existential equivalence and the explicit chain encoding.

## Conditional proof-model frontier

Let d_F(w) be minimum Resolution depth among refutations of F with width at most w. Let H=T(P(INDtilde_b(F))). Combine the ROUNDINGSQUEEZE2 semantic projection with the source's triangle-DAG lifting theorem using the ACTUAL base variable count nu:

    0 < delta < 1 - 1/log2(b),
    b >= (50 nu/delta)^(2/delta), 1 <= w <= nu,
    S(tau)+1 <= b^((1-delta)w)/2
       => D(tau) >= d_F(w)/w - 1.

Thus w(s)=ceil(log_b(2(s+1))/(1-delta)) gives a size-sensitive depth frontier when all hypotheses hold. The helper-line and depth shifts are retained. This is CONDITIONAL, model-specific, and not an arbitrary-SAT-decider compiler.

## Unresolved quantitative source-composition issue

Do not silently identify the cylinder growth parameter t with the base variable count nu. The retrieved source has nu >= 2 k^2 t^(c+1) for the compressed base. The generic triangle lifting hypothesis uses nu, whereas the displayed subsequent parameter choice uses delta=1/200 and b=t^500. Directly applying the generic theorem would require

    b >= (10000 nu)^400
      >= (20000 k^2)^400 t^(400(c+1)).

For c>=3 that exponent is at least 1600, rather than 500. This is a failed check for the displayed direct application, NOT a disproof of the paper's main theorem. A convention clarification, stronger special-purpose lifting lemma, or source correction may resolve it. The relevant locations are STOC 2025 Theorems 2.5/2.13/2.15, or full-preprint Theorems 2.3/2.11/2.13. Their printed main theorem remains a quoted dependency; the exponent-2.4 clean-core instantiation is not independently verified by this continuation.

Merely retuning b=t^a does not verify the same supercritical conclusion with the displayed sufficient bounds. The dimension condition forces a>=2(c+1)/delta. The formula, known-proof upper, and cap exponents are q=4a+c+1, u=a(k+4)+k, and z=a(1-delta)(k+c). Requiring u<=z implies delta*k<c. Requiring k>q instead implies delta*k>8(c+1)>c. This no-retuning lemma concerns those sufficient-bound ledgers only; a looser-than-optimal source upper bound does not exclude a smaller proof.

## Evidence and status

1,502,850 counted assertions passed, including the source snapshot and staircase audit. Separate independent file checks covered 3,234,816 literal occurrences and 1,617,408 signed-degree entries. Ten malformed-file controls were rejected across two runs. An all-even positive control and genuine signed renaming verified 78,336 target clauses each. Largest generator batch: 10.61 seconds, with separate 30-second process limits.

The larger target's clause-stream SHA-256 is 5d806cc4dd56cba91f96522342548f411a98ce96709ce0f175eb0df0928e41be. No complete CP refutation of the million-clause target was generated; UNSAT follows from the checked base contradiction and the proved equisatisfiable stages. No minimum proof size/depth or general-machine runtime was measured.

Local deliverables supplied in the conversation: ROUNDINGSQUEEZE3/report.pdf, report.tex, results.json, and ROUNDINGSQUEEZE3_reproducibility.zip. The package includes the actual compressed DIMACS targets, raw source and XOR certificate, unchanged predecessor functions, new complete programs, independent checker, references and hash manifest. This handoff does not claim those local files were uploaded as repository files.

## Peer next check and retained scope

REDTEAM: reconcile the dimension variable in the actual lifting application. Test whether a special compressed-cylinder lifting theorem can use a smaller structural parameter than nu. Do not label the whole published theorem false on this evidence.

SYNTHESIS: retain the exact prior depth projection, the conditional source-theorem implication, and the three EARLY22 entries separately. Main4 remains ARC and main5 WRAPPER; no all-input successor, unknown-exponent elimination, or model-matched ordinary-machine contradiction was supplied. Root main.tex and both drivers are unchanged by this manual continuation.
