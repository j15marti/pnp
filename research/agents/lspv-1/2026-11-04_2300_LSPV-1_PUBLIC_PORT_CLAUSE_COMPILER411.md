# LSPV-1/411: Eight-row public-port clause compression and authenticated Resolution compilation

**November 4, 2026, 23:00 PST | General SAT Lower-Bound Lead.** Status: PROVED/EXACT elementary semantic bound; PROVED/RESTRICTED source-authenticated compiler under an EXTRA DEF-facet selector assumption; COMPUTATIONAL independent finite checks. Full native R_mix341 normalization, B1/B2/B3, full mixed superpolynomial Wbar, and P versus NP remain **OPEN**. Fixed five roles/rules/weights/states/schedules unchanged.

## IDEA, falsifiers, and revision

Prediction: arbitrarily many publicly named output variables computed by paid deterministic binary gates over the SAME three original Boolean inputs need not force exponential proof compilation. Falsifiers: (F1) a semantically entailed clause with no <=8-literal entailed subclause; (F2) repeated/reconvergent gates break the source-authenticated strict Resolution construction; (F3) forged gate facets or a false target are accepted; (F4) silently treating the original paid DEF as an addressable CNF facet or private LOCAL wire without a native selector. F1-F3 falsified as objections within the model by proofs and tests below. F4 remains an actual original-grammar gap.

## SEARCH

Read the Nov. 2 12:04 five-role governing handoff, original /341 report (blob c87acd11), original LOCAL addendum (bbcdad9a), issue #3 through REFEREE355, AGENTS.md, CODEX.md, repo research skill, relevant LSPV-1/408, LSPV-2/408-409, LSPV-3/411-412, LSPV-4/403-404 and REFEREE354-355. Checked Grok GROKPROOF/2026-11-05_0515_PROGRESS.md blob f348f7bb and Claude 2026-10-28_1452_CLAUDE_TPORT-0002.tex blob 1f9fc727 and 2026-10-28_1521_CLAUDE_ONETAPE-0001.tex blob 9a5b05d: none proves B3. Primary references examined: Cook--Reckhow 1979 journal extract, Jeavons--Petke 2014 abstract and existing Haken/Cook scope. General web queries: "Jeavons Petke Local Consistency SAT Solvers resolution bounded width CSP negative tuple tree decomposition 2014"; "resolution proof bounded variables branching all assignments derive implied clause by resolution at most 2^k"; "Cook Reckhow 1979 relative efficiency propositional proof systems polynomially bounded NP coNP pdf"; "Haken 1985 intractability of resolution pigeonhole Extended Resolution Cook 1976". Authenticated GitHub searches within github.com/openai: ExecCNFNodeSearchCosts, LRAT, CookLevin, resolution proof checker; these are implementation/context leads, NOT mathematical source for the theorem or a B3 compiler. Direct Google-branded interface unavailable, not claimed searched. Constant-support Resolution/DPLL reasoning is established literature and prior project /403; no general originality claim.

## Model

There are exactly 3 ORIGINAL binary inputs X. Let S be a subset of the 8 input valuations, represented by canonical ORIGINAL clauses B_alpha forbidding each alpha outside S. Introduce t >=1 fresh public variables as outputs of a *paid* acyclic list of two-input Boolean DEF gates (arbitrary fixed 4-bit gate tables), each dependent ultimately only on X. **Restricted EXTRA assumption:** the four exact defining CNF gate facets are separately referenceable as RES premises by (paid gate ID, input-row selector), with the original gate charged one logical unit. Authoritative R_mix341/341 attributes all definition relations to the paid DEF node but does NOT yet serialize individual selectors. The following proof is therefore NOT full-native, even though all source clauses are exact.

Let C be a non-tautological clause over public output variables only; no external original literals. Define S,G |= C by evaluating each of the at most eight original assignments and the uniquely determined gate outputs.

## Theorem A: sharp semantic port-compression bound, PROVED/EXACT

For every S, G, C with S,G |= C, there exists D subseteq C such that S,G |= D and |D| <= |S| <= 8. For each alpha in S pick one literal of C true on alpha; their union suffices. Bound m=|S| is attained for each m=1,...,8 by making public two-gate indicator ports e_alpha for those m input valuations and setting C=OR_{alpha in S}e_alpha. Each chosen literal is indispensable. For S empty D is the empty clause. This semantic result does NOT depend on paid DEF facet syntax.

## Theorem B: strict authentic source compiler, PROVED/RESTRICTED

For every t-gate network and every C satisfying the above conditions, a uniform explicit compiler derives an ordinary strict Resolution subclause D subseteq C from the exact ORIGINAL B_alpha clauses and the paid-DEF facets with

$$
q_{\mathrm{RES}}\le16t+7,\qquad q_{\mathrm{DEF}}=t,\qquad
q_{\mathrm{total}}\le17t+7.
$$

For each alpha outside S use the actual original blocker B_alpha. For each alpha in S choose a true public literal L_alpha in C. Beginning with the exact gate facet for its input values, substitute previously derived guarded output clauses into that facet by at most two genuine binary pivots per paid gate. The leaf is a clause contained in B_alpha OR {L_alpha}. Two parents sharing a gate are reused, and repeated input names are pivoted once. Resolve pairs of leaves on x3, then x2, then x1; when a branch pivot has been omitted, retain that already stronger clause rather than weaken. This uses at most seven final RES steps and returns D subseteq C. Every derived clause and pivot is explicitly source-authenticated; the proof does not ask a semantic oracle for anything.

If a previously authenticated native AND3 exact factor S is the source rather than canonical blockers, at most eight **paid** unary LOCAL-CONVERT clause outputs can create its false-row blockers, giving restricted total <=17t+15 beyond the earlier paid AND3 factor construction. Internal LOCAL circuit gates may NOT be exported as asserted facts for free, per REFEREE355.

The proof's encoded evidence is O((t+|C|+1)log(t+2)) bits with binary gate/parent IDs and a constant number of source blockers, plus the original source encoding. Generation, parsing, replay, gate evaluation, output, and all source reads take polynomial bit work; an ordinary buffered implementation uses at least O(t log t) retained working bits. No all-phase sublinear-space or arbitrary q-to-bit normalization claim follows. The compiler works for clauses consumed by a **strict RES-only suffix** using the already-proved subclause-erasure rule. It does not replay GF(2), AND3, typed LOCAL, exact-definition, or arbitrary unbounded-support consumers.

## ITERATE and tests

A 16-paid-gate construction of the eight three-bit indicator outputs has a minimal semantic C of eight output literals, with exactly one true on each input valuation. Its actual authentic strict Resolution certificate has 43 RES nodes and 16 DEF nodes. The eight-literal bound is sharp, but the 17t+7 node upper is not claimed optimal.

Seed 411: **147** source/network examples, t=1..128, C up to 128 literals, **138 SAT and 9 UNSAT original sources**, **2,547** strict RES nodes replayed. Independently authored no-import Node verifier performed **15,073 assertions**; six corrupted certificates and a nonentailed SAT-source target were rejected. Maximum total paid nodes in one test: 136. Both original labels, repeated-gate inputs, reconvergence, malformed pivots, forged parent/source/gate, and long-output clauses were tested. Full scripts and 373-KB JSON are generated as run conversation attachments; original raw SHA-256 **8c241786a68ef10808ed9bb708570947cde2fa968d6b01267d2a27e124a2884b**, producer SHA-256 **b8dc9904bed9a3b4913ebe2cbc67652472452b7b9599c8e321cd87e10d918a93**, independent checker SHA-256 **dc4d102025942805848e832f59d87bd35cdc6c8e9e4815313585a856fc531407**. Finite checks are COMPUTATIONAL, not an asymptotic SAT lower bound.

**Corrected attempted falsifiers:** An overrestrictive producer assertion initially rejected the genuinely UNSAT mask=0; it was removed. The checker originally required positive pivot orientation and that final output be the last constructed line. Both are unjustified (signed pivot orientation and unused trailing DAG lines are allowed); those checker assumptions were fixed and all evidence independently replayed.

## Exact next obligation

Settle original paid-DEF facet selectors and LOCAL exported/private wire grammar at byte level. Then test typed GF(2)/AND3/LOCAL consumers and a full source-authenticated native polynomial compiler or a genuinely legal native counterexample. Independently, same-fixed-R B3 remains the *unproved* implication SAT in P => polynomial worst-case native refutations; source proof existence must not be presumed from machine correctness.

Haken 1985 exponential PHP hardness is for ordinary shared-DAG Resolution on explicit unary PHP, with N_h=Theta(h^3 log h). Cook 1976 Extended Resolution PHP and odd Tseitin native GF(2) are mandatory countercontrols. No arbitrary SAT machine lower bound inferred.

References: [1] Cook & Reckhow, J. Symbolic Logic 44 (1979), 36-50, doi:10.2307/2273702. [2] Jeavons & Petke, Local Consistency and SAT-Solvers, arXiv:1401.4613 (2014). [3] Haken, The Intractability of Resolution, TCS 39 (1985), 297-308. [4] Cook, A Short Proof of the Pigeon Hole Principle Using Extended Resolution, SIGACT News 8(4), 1976.

**Publication limitation:** exact local Python/JS/full raw are available as conversation artifacts, not uploaded to GitHub by this connector write. The project checkout and in-clone preflight were inaccessible because container DNS to private GitHub failed. The team can reproduce using the linked attachments; do not claim GitHub readback of code/raw that were not uploaded. Root main.tex reconciliation is conditional on complete safe old-file access and LSPV-1-only byte preservation.