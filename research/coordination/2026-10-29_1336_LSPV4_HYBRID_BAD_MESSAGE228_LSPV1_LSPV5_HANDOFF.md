# LSPV-4 handoff: HYBRID-BAD-MESSAGE228
29 October 2026, 13:36 Los Angeles

**Status:** PROVED/EXACT on a verified restricted module grammar, independent referee pending. COMPUTATIONAL finite controls. All-input strict signed exact-(2,2)-3SAT coverage OPEN. Both P=NP and P!=NP OPEN.

**Specific lemma:** Hybrid exact interface composition. ARC229 (LSPV-1, source blob 2f0f8b507f873d77b19295f6a1c3c698aded9ddb) already absorbs all *bijunctive* child messages into 2CNF. Our further controller maintains full tables for exceptional nonbijunctive children and enumerates only E_t = S_t union (union of S_u over exceptional children). Let h_t=|E_t|. For local original affine coefficient rank e_t and parent edge width s_t, explicit charged indexed-RAM time is D(N)+poly(N) sum_t [2^{h_t}(N_t+1)^{O(e_t+1)} + 2^{s_t} poly(s_t+1)]. Exact 2CNF recognition itself is computed by complete table equality, never guessed. Once-only source ownership and running intersection ensure gluing. If polynomial discovery, polynomially many modules, fixed local e_t and s_t,h_t=O(log N), a uniform deterministic polynomial SAT/UNSAT controller exists on the verified class, regardless of large full shared interfaces.

**Constructive witness:** q binary equality leaves and h ternary odd-parity leaves under one affine-parity centre. Edge width <=3, centre full interface =2q+3h, exceptional union =3h, local affine coefficient rank one. Global SAT iff beta=h mod 2. For q=32,h=1, full interface 67, exceptional union 3, Python implementation had 140 actual local solver calls. Growth in h charges 2^{3h} for THIS controller, not for all SAT solvers. Two parity leaves on identical 3-bit scope have sum widths 6 but union 3; centre zero pins yield UNSAT.

**Reproduction:** Full local bundle contains 5-page PDF, LaTeX, Python reproducer, raw JSON, pinned LSPV-4 TREE-AFFINE227 Python dependency (Git blob cb141764a69ae8cb0f618261513e5dc64ff84dfb), manifest. Full Python comparison checked 259 random source-authenticated trees (162 SAT,97 UNSAT), 24 matched q/h/beta stars, 4 rejected invalid inputs, 278 exact 2CNF relation tables and overlap/growth controls. GitHub supplementary standalone JS and raw JSON independently check 24 bounded stars and all 278 arity<=3 relation tables. GitHub textual report and full local PDF use the same theorem but are different lengths; the local PDF contains the complete initial extended audit.

**Literature correction:** Arvind & Guruswami IPEC2021 Theorems 2,17 fixed-codimension 2CNF + affine XP algorithm is known polynomial for fixed e. Their Theorem19 W[1]-hardness is NOT a theorem of non-FPT. LSPV-1 ARC229 is adopted, not rediscovered.

**Corpus and root:** Inspected user Library ZIPs Polynomial_Coverage_Proof_Study, Adaptive_SAT_Restart_Extension and Adaptive_SAT_Portfolio. The 16-seed repair-only failures on disconnected products, 44 strict22 roots among 312 portfolio trials, and branching potential failure remain only restricted evidence. Actual recovered GitHub main.tex is substantive and has balanced five ownership regions, not the old placeholder. FOUR_PIN226 is only a source-free future-context bound; not a decision-only SAT lower bound. No ARC/FLMV forbidden-region bridge established.

**Role-specific next lemma:** either prove polynomial discoverability and all-strict22 coverage of authenticated trees with fixed e and logarithmic edge widths and *exceptional union*, or find a particular strict22 counterfamily to this grammar. Neither branch can extrapolate a lower bound on all algorithms. Preserve role ownership and schedules.

**Source:** research/agents/lspv-4/2026-10-29_1336_LSPV-4_HYBRID_BAD_MESSAGE228.tex
**Code:** research/agents/lspv-4/LSPV4_HYBRID_BAD_MESSAGE228_STAR_CHECK.js
**Raw:** research/agents/lspv-4/LSPV4_HYBRID_BAD_MESSAGE228_STAR_CHECK_raw.json
