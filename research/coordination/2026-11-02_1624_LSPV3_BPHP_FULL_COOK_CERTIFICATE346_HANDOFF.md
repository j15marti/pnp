# LSPV-3 346: Full Cook RES/DEF signed-BPHP certificate handoff (November 2, 2026, 4:24 PM PST)

**Role:** PNP Hypergraph & Proof Certificates. **Scientific directive:** 12:04 PST worst-case minimum derivation/B3 with 16:00 PST hardest signed-instance atlas. **Original fixed calculus:** Rmix341, each derived node has at most two paid parent references and unit cost, with conservative two-input DEF (definitional clauses available by charged slots), binary RES, AND3, XOR, LOCAL-CONVERT. No modification to rule weights, tasks or schedules.

**PROVED/EXACT symbolic family escape:** For the width-2log(h) signed bit-pigeonhole formula B_h with h=2^ell holes, h+1 pigeons, m=h*binom(h+1,2) individually indispensable source clauses and N(h)=Theta(h^3 ell^2) encoded ASCII DIMACS bits,

    m-1 <= W_Rmix341(B_h) <= O(h^4+h^3 ell^2).

An explicit, uniformly constructible conservative RES/DEF proof first derives unary PHP using binary AND prefix gates, then performs Cook's pigeonhole-downshift with exactly two paid DEF gates per new hole indicator and an exact nine-variable local binary-resolution collision projector. The projector is a fixed complete local Davis--Putnam elimination, at most 3^9 distinct clauses, and is not a hidden SAT/equivalence oracle. Thus the lower-bound direction fails for BPHP in this unchanged mixed calculus even if Braun's recent unrestricted DAG Res(XOR) preprint claim is accepted. This is a **FAMILY FAILURE**, not a refutation of global worst-case hardness or B3.

**COMPUTATIONAL full proof DAGs and independent replay:** h=4,8,16 respectively: original clauses 40,288,2176; derived (DEF,RES) pairs (60,530), (444,7629), (3196,109599); total logical nodes 590,8073,112795. Actual proof bits 344824,5206552,78921616. An independently written Python checker (no producer imports) verified 117,758 RES nodes, 3,700 DEF nodes, all 2,504 original-source ancestors, 24,992 signed/source/SAT controls; rejected 21 deliberately corrupted certificates and 24 malformed fixture encodings. Same-source deletion witnesses and every signed occurrence flip are SAT; h=4 exhaustive UNSAT (1024 assignments) and even/injective SAT labels passed. Horn, 2SAT, odd/even K4, guard and compact equality were also checked. The full 9.5 MB h16 JSON certificate, producer, checker and source/complete certificate SHA256 manifest are in the user-facing reproducibility archive. The public lightweight Node program checks source sensitivity and the local projector but does NOT replay full proof DAGs.

**Verified published GitHub files:**
- Formal report: research/agents/lspv-3/2026-11-02_1624_LSPV-3_BPHP_FULL_COOK_CERTIFICATE346.tex
- Standalone compact finite signed-control code: experiments/arc/lspv3_346_bphp_compact.js
- Raw counts, evidence checksums and scope: results/raw/arc/2026-11-02_1624_LSPV3_BPHP_FULL_COOK_CERTIFICATE346_public.json

**Bridge and next implication:** no certified global optimum beyond source floor, no superpolynomial Wbar_Rmix341, and no B1/B2/B3. Need a new growing nonaffine family whose EVERY legal combined RES/AND3/XOR/CONVERT/DEF derivation has a superpolynomial minimum, *plus* independent B3 for precisely Rmix341. No search cost is improperly added to W_R. Peak all-phase physical storage and proof evidence are kept separate. The external Braun arXiv:2609.23015 theorem was not independently kernel-replayed. The 16:12 LSPV2 weighted local macro theorem is compatible, not a changed calculus.

Search provenance: current issue #3, the 12:04 and 16:00 handoffs, AGENTS/CODEX/pnp-research, preceding LSPV-2 341/345 and LSPV-3 343/345, relevant Cook 1976, Haken 1985, Peitl--Szeider 2021, Braun 2026, Buss 2021; repository search BPHP, Extended Resolution, Rmix341 and separate github.com/openai resolution proof (only unrelated sheaf results). Project web 404, authenticated GitHub connector succeeded. Root main.tex must be reconciled only within LSPV-3 ownership on the current head, with complete-blob readback.

**P versus NP remains OPEN.**
