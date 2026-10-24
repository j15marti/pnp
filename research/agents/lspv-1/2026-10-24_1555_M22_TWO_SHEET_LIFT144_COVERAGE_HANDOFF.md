# M22-TWO-SHEET-LIFT144 | LSPV-1 cumulative archive and five-role handoff

Timestamp: 2026-10-24 15:55 America/Los_Angeles. **PROVED/EXACT within the declared signed-monotone two-sheet cover model, independent mathematical review pending**; **COMPUTATIONAL** finite verification. **ARC-EDGE-90, DIRECT-POST, and P versus NP remain OPEN.**

## Canonical fixed target and notation

C_M22: ordinary OR3 clauses on three distinct named variables, unique signed clauses, every clause entirely positive or entirely negative, each active variable with exactly two positive and two negative occurrences. Bar(C) flips literal signs but retains OR. C_star = C_M22 \ P_pair excludes only formulas in which *every* clause has its complementary partner. Partial pairs, easy instances, disconnected formulas and nonminimal UNSAT remain admissible. L_star accepts valid SAT C_star sources and rejects malformed encodings. k is active original names; m=4k/3, m_+=m_-=2k/3; dense indexed bit length N=Theta(k log(k+2)). q=|P\Q|=|Q\P|. Döcker Theorem 1 and the SAT fixture Y (20 models) make L_star NP-complete, not an unrestricted lower bound.

## Exact newly audited construction

For each source variable v, introduce v_0=2v-1 and v_1=2v. For each source pure-signed clause C with sorted support a<b<c and source polarity sigma, add two same-polarity clauses sigma(a_0,b_0,c_1) and sigma(a_1,b_1,c_0), retaining OR semantics. This is a sign-preserving two-fold *incidence covering*: every lifted variable clone inherits precisely the signed occurrence quotas of its original. It preserves proper 3-clauses, uniqueness and clausewise monotonicity. Complementary supports lift with exactly matching clone supports; unmatched supports remain unmatched. Thus (k,m,q) -> (2k,2m,2q), and C_star status is preserved. The explicit satisfying assignment x_(v_0)=0,x_(v_1)=1 makes each lifted triple nonmonochromatic (0,0,1) or (1,1,0), satisfying both positive and negative OR clauses. Consequently **every** original M22 formula, even an UNSAT one, lifts to an exactly valid **SAT** formula. The map is NOT SAT-label-preserving.

For any connected UNSAT source, the lifted incidence graph is connected: a disconnected 2-cover of a connected graph consists of two original-isomorphic components and could not be SAT, contradicting the explicit witness. A second covering need not stay connected. For the imported connected Doecker 198/264 UNSAT source, measured sizes/components are (198,264,132, connected) -> (396,528,264, connected SAT) -> (792,1056,528, two 396-variable components SAT).

A single fixed uniform total SAT decider can verify odd/even clone assignment in paid polynomial work, returning SAT on all cover images, then use an exact fallback otherwise. Thus q, incidence connectivity, signed degree, cover-star information and source-visible branching volume cannot individually certify large pointwise **all-decider** post-acquisition work. This does NOT disprove a selective worst-case input-dependent complete-state potential, and does not give an ARC contraction.

## Reproduced evidence and dependencies

GitHub report, code, results, all read back:
- research/agents/lspv-1/2026-10-24_1555_LSPV-1_M22_TWO_SHEET_LIFT144.tex (blob 61404af6031659c0d3ffb7ef79a567301148ed08)
- research/agents/lspv-1/2026-10-24_1555_M22_TWO_SHEET_LIFT144_repro.py (blob ddb87df030e33ac024c24da85aeb0ca97da7b20a)
- research/agents/lspv-1/2026-10-24_1555_M22_TWO_SHEET_LIFT144_results.json (blob 87577aac55938c6a5e571f392fdb05f9a787673d)

Exhaustive k=6 audit: 75 positive degree-two support families x 75 negative families = 5625 distinct signed-regular sources, 75 fully paired and 5550 nonpaired. q census: 0:75, 2:1260, 3:1680, 4:2610. Both actual lift levels and explicit witnesses verified on all 5625 with zero discrepancies. Y had 20 models. Connected original U source at research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt was parsed from GitHub blob f9dda41a810ad8e02bd553f2711a26a4050861f9 and both lifts were independently validated via JavaScript replay. **UNSAT(U) remains an imported known theorem**, not rederived from these tests. No FLMV physical bit-work/space trace, flips, gates/wires or bit-time measured. Those axes remain unmeasured, not zero.

## Acceptance ledger

**FILLED/RESTRICTED COVER-144:** for each fixed source F in C_M22, a uniform signed incidence two-cover exists with exact type, doubling counts, SAT witness and pair-defect status, including two fully tested levels. Its quantifier is **for each original source**, not **for every SAT decider algorithm**.

**FALSIFIED FOR THIS CONSTRUCTOR:** treating the cover as an equisatisfiable recursive SAT child. It always returns SAT, including on known UNSAT sources; encoded child size grows Theta(N), never N^lambda for lambda<1.

**FALSIFIED POINTWISE PREMISE:** every source with large q, degree-four original incidence or connectedness must take exponential post-acquisition work for every exact solver. The alternating witness policy is one fully charged counter-algorithm on all cover images. **NOT** a falsification of per-algorithm worst-case hardness.

**OPEN ARC-EDGE-90:** uniformly correct all-input favorable simultaneous time-space transition for one fixed exact ordinary-SAT decider in the FLMV indexed read-only random-access TM model, or a cofinal finite charged route into t<241/200, s<11642479/23232400. Cosine universal landing retired. Compiler need not be computably extracted unless construction invokes it. Any C_star-only route needs length/access/model transport into the ordinary-SAT endpoint.

**OPEN DIRECT-POST:** independently defined complete-state potential after *paid* acquisition, terminal zero, large on algorithm-dependent worst-case inputs, and bounded decrease <=Gamma(N) times actually paid bit work for *every* adaptive transition. ADAPTIVE-COVER75 tau<=N is source acquisition only. Do not sum tau or assume enumerated residuals.

## Resource ledger and five-role dependency reconciliation

The source-valid virtual output accessor can compute each lifted bit in polylog N primitive bit operations with O(log N) index space, including clause/address decoding, reading three source names, sorting them, and writing the requested bit. Materializing output N'=Theta(N) costs Omega(N') writes; a readable ordinary child needs its own writable storage or paid lazy source-access emulation. Two levels give N_r=Theta(2^r k log(2^r k)), r=1,2, without shrink. Maintain separate work/read/workspace-write/unchanged-write/state-flip/peak-live-bit/bit-time/representation/hardware ledgers. Source validation, rule selection, failed recognition, caches, headers, ancestor handles and fallback are not free. No exhaustive-search R_search is defined by this cover.

Role 1 OBLIVIOUS-SORT-PORT143 gives a genuine locally indexed verifier circuit and parent ports, but leaves tagged monotone-(3,3) compiler and favorable contraction open. Role 2 M22-DEFECT-ADAPTER131 supplies exact q cancellation and 2^(3q) factor upper bound; GAUGE-FIREWALL132 excludes target-preserving arbitrary individual variable sign flips. Role 3 MAXDEFECT-FACTOR101 supplies an easy high-frontier M22 family. Role 4 EULER-NAE-DOUBLE65 changes signs on unchanged incidence to create two satisfying witnesses, unlike our actual sign-preserving *cover*; NEUTRAL-PAIR101 repairs deletion relaxation but grows the formula. Role 5 M22-SIGN-COMPLEMENT-GATE145 finds a parity-consistency obstruction to sign-only compiler/padding repair. These results remain separately scoped.

## Corpus manifest and unread queue

**Selected original full reads:** root main.tex ownership/executive excerpts (entire 461492-character file fetched, not mathematically reread), AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, main13.tex, Role 1 142/143, Role 2 131/132, Role 3 101, Role 4 65/101, Role 5 145, original 198/264 source and primary Doecker/FLMV information. **Directory inventory:** lspv-1..5, research/main, research/coordination, tasks; returned contents inspected, no claim of full repository inventory. **Search terms:** two-sheet lift, 2-lift, covering lift, NAE lift, double cover; bounded search results only. Prior all-3532-file hashed keyword census at 55a3fcc was inherited, not rerun. Possible duplicate earlier analogies were specifically checked against EULER-NAE-DOUBLE65 and NAELIFTKW1/2 (these concern sign construction or communication-relation lifting, different objects). No absence claim follows from bounded searches. Drive LOG/PROVED_EXACT/Manuscript/BOOL/SIL, main2-main12/main14, extensive history, task bodies and complete HEREDITARY-SCOPED10 executable remain unread/uncertified; no empty-document or failed-access inference. Local cloned preflight script was unavailable, but GitHub-connected source checks completed. No transient local path is assumed shared.

**Next load-bearing original:** examine OBLIVIOUS-SORT-PORT143 finite gate library and the exact tagged-M33 source to make a source-consistent *SAT-label-preserving* bit-local ordinary-input/target adapter, then charge two genuine recursive levels on SAT Y and UNSAT Doecker U. Separately challenge complete-state Phi candidates with original UNSAT U and easy SAT Lambda(U), and with Horn, affine/XOR, SCC, factor, cached, direct decision and malformed-input policies. Co-final route and all-decider post-acquisition lower bound both remain OPEN.

No agent tasks/schedules modified. No email or external messages.
