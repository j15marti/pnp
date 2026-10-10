# MODEL_BRIDGE run 0001: fixed model, source transfer, and all-input closure

Date: 2026-10-10 UTC. Agent: MODEL_BRIDGE. Status: completed scoped review, not an exhaustive project review. P versus NP remains open.

## Main finding

The most current retrieved project spine is the main4/main5 ARC and WRAPPER program, including ARC15 dated October 9. The earlier October 2 LSPV spine is historical context. The current proof already has a rigorous conditional resource-composition argument and an applicable published time-space endpoint. The missing implication is an all-input, successor-closed, jointly resource-bounded construction from the assumption SAT is in P. The existence implication is already separation-strength, as FORMAL-SPINE1 explicitly acknowledges.

The useful next target is a source-first rule that covers a genuinely unresolved family, with a joint time/access/space ledger and recursive closure. Improving terminal coverage without contracting the SAT-hard UNKNOWN fallback does not establish that implication.

## Material actually reviewed

1. GitHub repository j15marti/pnp, main branch: main2.tex, main3.tex, main4.tex, main5.tex. Current root-file content was fetched directly. main4 and main5 import many further documents; reading the root does not constitute reading every import.
2. Full report research/agents/lead/2026-10-08_FORMAL-SPINE1.tex.
3. Full report research/agents/proof/2026-10-09_1940_ARC15.tex.
4. Included additions FORMAL-SPINE1/main4_addition.tex and main5_addition.tex.
5. Included additions CONSTRUCTION-STRENGTHEN10/main4_addition.tex, RECOVERY-STRENGTHEN10/main4_addition.tex, REDTEAM-STRENGTHEN7/main4_addition.tex, and ARC-STRENGTHEN2/endpoint_addition.tex. Full underlying Construction10/Recovery10/Redteam7 reports were not retrieved in this run.
6. Drive LSPV-5-58501, REDTEAM-0004, HG-G2-0040, and SIL-PR-20260918-PROGRESS-002; search hydration also provided CLAUDE-0278 in full.
7. All three attached HTML scripts, focusing on the actual generator/hash implementation.

Local current GitHub source snapshots are in sources/. No user source was edited. The parent agent is publishing coordinated outputs.

## Source retrieval and coverage limits

Personal Context search returned “Personal context is unavailable for this conversation.” Thus this agent could not review previous chats beyond supplied conversation context. Parent independently reported a successful retrieval; that does not make this agent's review exhaustive.

Drive searches: main4, main2, main3, wrapper, LSPV, SAT-MERGE-FORCING1. The exact SAT-MERGE-FORCING1 Drive search returned empty. A wrapper search restricted to modified after 2026-10-03 also returned empty. Empty search results do not prove absence. Main4 search found CLAUDE-0278, not the current GitHub manuscript.

GitHub code search for SAT-MERGE-FORCING1 identified j15marti/pnp at index commit b6948eb15a8afec37cc904120ce20b61b45a0dad. Direct fetches subsequently read default-branch versions. Search index and fetched head need not be identical. No repository-wide full-history review was performed.

Primary literature search was performed after retrieving the prior missing-link statements. Cook's 1971 PDF was located and opened but returned no extracted text. Shaltiel-Umans' author PDF was located but open returned an internal error; its detailed claims were therefore not independently reverified here. Baker-Gill-Solovay's publisher abstract and the FLMV author manuscript were directly read.

## Strongest current spines

| Spine | Exact or literature-supported part | Missing load-bearing part |
|---|---|---|
| WRAPPER composition | One uniform all-input resumable shrinking contract implies near-linear time and sublinear-power workspace, with all child buffers and ancestors charged | Derive that contract from SAT in P, or a less restrictive contract reaching the endpoint |
| ARC finite entry | One joint pair strictly below a verified FLMV forbidden boundary gives a contradiction; finite-stage entry avoids an invalid limit-of-machines step | A proved all-input transition that improves the joint achievable pair, including fallback |
| Continuation/merge | Continuation-complete summaries must distinguish different consumer equivalence classes | Ordinary SAT correctness must force that particular multi-query service in the actual computation, plus a time-cost theorem |
| Historical LSPV A/B | Several finite-dimensional and recurrence statements are available | Source-specific compact Boolean separator, acquisition, exact extractor/binaryization match, nonrelativizing ingredient and diagonal |

## Current endpoint check

FLMV, Time-Space Lower Bounds for Satisfiability, author manuscript September 7, 2004, Section 2.1 defines random-access Turing machines and excludes read-only input and write-only output from workspace. Theorem 3.1 supplies a local SAT reduction with polylogarithmic per-bit time and logarithmic workspace. Corollary 5.8 excludes NTIME[n] simulation at time n^c and space o(n^d), where d=((c+2)/c^2-c)/2. With strict margins, this transfers to the SAT encoding.

The project's numerical witness is correct:
c=1201/1000,
d=1468676399/2884802000,
d-1/2=26275399/2884802000>0.
Thus (6/5,1/2) lies strictly inside this particular forbidden region after its local-encoding obligation is met. This is a simultaneous time-space exclusion, not a theorem excluding arbitrary polynomial-time SAT.

The following distinctions are compulsory:
- One machine must satisfy both coordinates.
- Bit length means original encoded input length, not variable count, hash length, or post-normalization length.
- The input exclusion applies to the original read-only input. A materialized derived child is writable workspace somewhere in the implementation.
- A stream emitter does not automatically provide cheap random access.
- The endpoint's proof may use special structure of its published local reduction. A new descendant generator needs its own accessor analysis.

## New formal audit artifact

model_bridge_contract.tex gives three elementary lemmas and the current conditional theorem. These are scoped formalization and recovery, not claimed novel complexity results.

MB1, polynomial wrapper closure: if an ordinary deterministic wrapper has local time N^a, at most N^b SAT calls of length N^c, and its fixed SAT subroutine has time m^K, then its time is polynomial, bounded by N^{max(a,b+cK)+o(1)} under the declared direct-call implementation. This proves that polynomial wrappers preserve polynomial solvability, but does not erase K.

MB2, UNKNOWN fallback composition: a capped partial solver followed by an ordinary SAT decider on UNKNOWN has worst-case time bounded by the sum of their costs and peak space bounded by the maximum after disposal of preliminary state. Coverage alone supplies no strict resource improvement in the worst case.

MB3, local reduction transfer: a reduction of length N^{lambda+o(1)} with per-bit access time N^{alpha+o(1)} and accessor workspace N^{beta+o(1)} transforms a solver's joint exponents (t,s) to at most (max(r,lambda*t+alpha),max(beta,lambda*s)), where N^r is charged setup time. This identifies the exact obligation behind a claim that a shielded UNKNOWN domain has the same achievable region as general SAT. It does not verify Construction10's entire reduction by itself.

The conditional separation statement retains FORMAL-SPINE1's exact open bridge rather than renaming it as proved.

## Falsification and anti-circularity findings

Cross-document drift: main2.tex retains a historical Williams product endpoint involving 2cos(pi/7), while current main4/main5 ARC14 notes explicitly retire the historical cosine endpoint. This review relies on the directly checked FLMV finite-entry boundary above. Older main2/main3 endpoint claims should not be inherited without their original theorem and model audit.

1. **Endpoint bypass remains valid.** If a wrapper's only required output is SAT(F), an implementation may discard irrelevant history and call its exact SAT decider. Prime lineage, timing history or a forced merge service is not required merely by output correctness.
2. **Added outputs change the task.** A pair (SAT(F), hash of a specified run) or online response to a fresh event stream is a different function/protocol unless a solver-independent specification and a fully charged transfer are supplied.
3. **Reduction direction matters.** SAT reducing to a complicated wrapper establishes only that the wrapper is at least as hard. Transferring a lower bound for that wrapper back to SAT needs the wrapper to be solvable from SAT with controlled overhead, or a separate universal extraction theorem.
4. **Canonical witness identity is unnecessary.** REDTEAM-0004's correct quantifier is forall A exists I. A wrapper destroys universality only if the wrapped realization has no qualifying witness, not merely a different witness. Proof-side transport cost cannot automatically be charged as executed machine work.
5. **Cheap acquisition is a hostile control.** HG-G2-0040's SCAN wrapper collapses uncertainty about unread input by reading it all. That does not establish computational SAT progress.
6. **Current construction evidence remains partial.** ARC15 improves method-level coverage from 6/13 to 12/13 on its declared scaling sample. All six extra answers are SAT witness exits. The remaining UNSAT instance is UNKNOWN. This is compatible with the universal negative-case gap remaining.
7. **Current accounting evidence remains partial.** ARC15 explicitly notes missing material work and transient state, and does not claim corrected bit-time or peak-workspace exponents.
8. **Portfolio growth is not fallback contraction.** Construction10's shield and Recovery10's mixed ledger preserve a SAT-hard unresolved image for the declared portfolio. A new terminal must be audited against the current reduction rather than inheriting an old fallback equality automatically.
9. **Nonblackbox is not nonrelativizing.** A claim depending on source code can still fail to produce any necessary resource obstruction. The exact ordinary-machine premise that fails under oracle replacement must be named. No such new premise was proved in this run.

## Attached tools audit

generator.html generates seven alphanumeric characters and randomly places a space. It prepends a cleaned seed to fresh Math.random material. The same seed therefore does not specify a deterministic mathematical instance sequence.

hash.html computes 64-bit FNV-1a over UTF-8 bytes, then reduces modulo 62^6. hash_tool.html does the same modulo 62^8. The output spaces have 56,800,235,584 and 218,340,105,584,896 tags, approximately 35.73 and 47.63 bits. Neither attachment implements SHA-256 or an injective history encoding. Pigeonhole collisions are unavoidable on larger domains. Exact equality checks are necessary if tags are used to authorize semantic merging; a short tag alone cannot certify it.

No collision search was necessary to establish this finite-range fact, and none is claimed.

## Next run target

Recover the exact remaining ARC15 UNSAT fixture and the current shielded families. Seek one sound negative-case cover/refutation rule with a source-checkable certificate. Before promoting it, establish:
1. what inputs and descendants it covers;
2. complete versus one-sided coverage;
3. total failed-discovery work;
4. child encoding size and physical per-bit access cost;
5. peak live derived state including ancestors;
6. whether the UNKNOWN domain still admits the existing local SAT embedding.

A successful finite experiment is a clue for a theorem. The theorem must quantify over a declared infinite family, and the final bridge must cover every input or soundly transform the entire remaining fallback.

## References and project pointers

1. Fortnow, Lipton, van Melkebeek, Viglas, Time-Space Lower Bounds for Satisfiability, author manuscript (2004), Sections 2.1, 3, Corollary 5.8. https://lance.fortnow.com/papers/files/tst.pdf
2. Baker, Gill, Solovay, Relativizations of the P = ? NP Question, SIAM Journal on Computing 4(4), 431–442 (1975). https://epubs.siam.org/doi/10.1137/0204037
3. Current formal spine: https://github.com/j15marti/pnp/blob/main/research/agents/lead/2026-10-08_FORMAL-SPINE1.tex
4. Current ARC15: https://github.com/j15marti/pnp/blob/main/research/agents/proof/2026-10-09_1940_ARC15.tex
5. Current main4: https://github.com/j15marti/pnp/blob/main/main4.tex
6. Current main5: https://github.com/j15marti/pnp/blob/main/main5.tex
7. REDTEAM-0004: https://docs.google.com/document/d/1rmP4Uokj9iCH55v3JdRGn6dP6TN6xhdHx0ylpP2Vo1Y/edit
8. SCAN guard: https://docs.google.com/document/d/1i3RLTZIWBp9zxWpBP6gUkLBbR_ec4jVv6a-fqTwUQJs/edit
9. Historical LSPV-5-58501: https://docs.google.com/document/d/1z4Jaoi4P0ZJXU8DTemXW6Eqb3vvt5RosAZTWuVMeCG0/edit
10. Historical wrapper closure guard: https://docs.google.com/document/d/1SaGILk2G6VfaJMA7X4fg4NBL8UKtI5NrpQtLm39ef2I/edit
11. CLAUDE-0278, historical source of extractor-citation concern, not independently reverified here: https://docs.google.com/document/d/1pCWs56eQY33qW_fGCKlGDiO3oyC4Ia3tsKMsYYTgGM8/edit

Validation: exact rational arithmetic confirmed the endpoint margin and hash range sizes. The four-page model_bridge_contract.tex compiled successfully with pdflatex and BibTeX; its final compilation reported no undefined references. This is compilation validation, not machine-checked theorem verification. REDTEAM independently reviewed the report and caught a corrected numeric transcription error in the eight-character hash count. REDTEAM also reviewed the actual formal .tex and accepted its claims at the stated conditional scope, including the retained-setup bound, local reduction, strict endpoint margins and uniform recurrence.

Run disposition: no separation claimed; no current theorem promoted to unconditional SAT hardness; no remote edits by this agent.

