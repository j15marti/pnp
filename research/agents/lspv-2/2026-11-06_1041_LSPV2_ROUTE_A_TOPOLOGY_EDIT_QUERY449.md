# LSPV-2/449: Four-edit charge disclosure on odd Tseitin sources

2026-11-06 10:41 PST. Route A primary. PROVED/RESTRICTED mathematics; COMPUTATIONAL finite tests; universal FLMV contraction, B3, and P vs NP OPEN. This compact GitHub edition accompanies a longer local mathematical report and a reproducibility archive.

## Initial idea and precise falsifiers

Hypothesis: fixed-graph future charge-toggle queries admit the one-bit semantic quotient from LSPV-2/447, but future children that can alter graph topology need not admit the same quotient.

F1: deleting the three incident edges at a vertex might leave G-v disconnected. This is a genuine counterexample for cubic graphs with articulation points, so the theorem assumes 3-edge-connectivity. F2: <=3 allowed edits may already distinguish two odd-charge sources. Ruled out by the parity and connectivity proof. F3: all four-edit answers may fail to distinguish every original odd charge. Ruled out by the injectivity proof. F4: indexed original-source rereading might avoid the information floor. This is a genuine limitation, not an all-machine lower bound.

After search, the initial clause-minimality idea was retired as duplicate: LSPV-3/429 and Emil Jerabek's February 2024 2-connected Tseitin argument already cover it. Earlier separator work appears in MAIN64 and LSPV-1/276; LSPV-2/448 already distinguishes one-pass acquisition from future-query summaries. The new question is structural future edits, not a new SAT formula.

## Source, theorem and model ledger

Let G=(V,E) be a simple 3-regular 3-edge-connected graph, H=|V| even, M=3H/2, and chi an odd-parity vector in GF(2)^H. Each vertex v with incident edge IDs a<b<c contributes the exact four proper signed width-three source clauses

$$
C_{v,p,q}=\ell_p(x_a)\lor\ell_q(x_b)\lor\ell_{p\oplus q\oplus1\oplus\chi_v}(x_c),\qquad
p,q\in\{0,1\},\quad \ell_0(x)=x,\quad\ell_1(x)=\neg x.
$$

These encode XOR of the three incident edges = chi_v. The 4H original clauses use M variables and 12H original signed occurrences. With w=ceil(log2(M+1))-bit edge IDs, N=12H(w+1)+O(H)=Theta(H log H) encoded bits. Odd total charge makes the full source UNSAT.

Urquhart (JACM 34, 1987) and Ben-Sasson/Wigderson (JACM 48, 2001) give exp(Omega(H)) ordinary *shared-DAG Resolution* lower bounds on suitable cubic expander families. This result applies to an expander sequence conditional on additionally authenticating 3-edge-connectivity of that sequence; no growing named sequence satisfying both was independently replayed here. Changing odd charge vectors by an edge-variable complementation preserves resolution size. No lower bound against Extended Resolution, GF(2), historical full R_mix341 or any arbitrary SAT algorithm is claimed. In fact summing parity equations is a polynomial-time shortcut.

## Exact theorem (PROVED/RESTRICTED)

A future query begins with the same fixed authenticated parent. Each primitive edit is either (a) flip a named vertex charge or (b) delete one named edge from *both* endpoint parity equations. Edited formulas are new problems, not legal proof inferences in R_mix341. Query replies report their SAT status. Original charge bits are sealed after preprocessing: no free source-dependent head location, auxiliary tape, source copy or rereading.

**449.1: Three-edit blindness.** Every script containing at most three primitive edits returns SAT iff the number of charge flips is odd, independently of the original odd vector chi. Proof: even number of flips leaves odd total charge, making every graph UNSAT. Odd number of flips with <=3 total operations permits at most two edge deletions. 3-edge-connectivity keeps the edited graph connected and its total charge even, so it is SAT.

**449.2: Four-edit disclosure.** Fix public reference vertex r. For each v form Q_v by flipping chi_r and deleting all three edges incident to v. Since G is cubic 3-edge-connected, G-v is connected: an articulation vertex would force a bridge. The edited graph has precisely components {v} and V\{v}. After one flip the total charge is even. Therefore

$$
\operatorname{SAT}(Q_v(F_{G,\chi}))=1\oplus\chi_v\oplus[v=r].
$$

The H-bit response vector to the full query menu recovers chi. Exactly 2^(H-1) odd-charge sources induce distinguishable answer functions.

**449.3: Tight retained-state minimum.** A deterministic sealed-charge preprocessor answering *every* Q_v needs at least H-1=Omega(N/log N) retained bits. Store the first H-1 charge bits and recover the last using odd parity to attain that bound. This is NOT a bound for a single SAT decision, a bounded future menu, or the indexed read-only-input FLMV machine. The latter can reread one charge with O(log N) writable space once the source and graph are authenticated.

**Sharpness:** The allowed query alphabet needs four edits to obtain any charge-dependent SAT bit from an odd source. All <=3-edit SAT responses are determined solely by flip-count parity. This threshold is about a query interface, not the intrinsic decision-time complexity of SAT.

## Source authenticity, shortcuts and controls

Edited vertices of degree 0,1,2,3 are encoded back into proper width-three signed clauses using fresh existential gadgets: degree-2 blockers via (a or b or z)&(a or b or not z), degree-1 blockers via four triples over two fresh variables, a false degree-0 equation via eight triples, a true degree-0 equation via no clauses. Such child formulas have Theta(N) size and are **not** recursively shrinking guest inputs. No new native R_mix341 split, discharge, weakening or graph-edit inference is claimed. Original source remains the exact signed 3-CNF above.

Actual local executable controls: 648 even-charge vectors and 648 matched odd-charge UNSAT original signed 3CNFs on K4, cube, Petersen; 6,176 four-edit query answers; 162 strict-three-clause child DPLL replays; 219 one-/two-edge deletion connectivity checks; 9 malformed source controls. A cubic bridged articulation graph falsifies the theorem without 3-edge connectivity. Independent JavaScript verified 120 pairs of full source and edited-child SHA-256 hashes and passed 13,440 assertions. Finite test graphs are NOT asymptotic hardness certificates; no native FLMV physical tape execution was performed.

The original fixed-graph charge-toggle quotient of /447 and the sealed-query-menu quotient of /448 remain correct. The present topology changes invalidate reusing those summaries without validating the new component structure. A family-specific indexed parity shortcut defeats any attempt to turn this into unrestricted machine hardness.

## Corpus and publication audit

Read governing five-role handoff (blob c3889a3e), issue #3, AGENTS (19656af1), CODEX (754999f5), repo research skill (b8df83a7), LSPV-2/447 (e0180e70), /448 (ab28a0eb), LSPV-3/429 (1054701f), /453 (760cce9e), MAIN64 (90d33c5f), LSPV-1/276 (86bd463e), Grok 2026-10-31 10:12 (b8103042), Claude TPORT (b7150bb9), LSPV-5 REFEREE381 (703beb56). Both Grok and Claude directories were actually enumerated. konard/p-vs-np README (0e0ec77f) and solution plan (19450e38); blkph0x/p-vs-np-proof-research README (f397a774), METHOD_INDEX (18d693ea), RESOLUTION_STANDARD (729a9164); meelgroup/frat-xor README (38a137bc) were inspected. The CNFgen, openai/math and anthropics/formal-math repositories were accessible; no theorem was inferred from their names. External primary literature was searched, but no Google-branded engine was separately used.

Root main.tex returned empty readable content despite nonempty blob ab900e0e and was not overwritten. Neither the five roles, schedules nor historical mixed-calculus weights were changed. The local archive contains the complete executed Python generator, independent executed JavaScript verifier, raw source/child hashes, all results, full report, handoff and SHA-256 manifest. This GitHub compact report is not a substitute for native-machine resource accounting.

**OPEN:** every-processor uniform all-input malformed-aware both-label recursively iterable A -> Phi(A) with t'<=max(11/10,3/5+t/2), s'<=max(1/2,s/2), all construction/guest/source/search/cache phases charged. Route B's all-rule Wbar_R lower bound and noncircular B3 remain separately OPEN. P vs NP remains OPEN.

References: Urquhart, JACM 34 (1987), doi:10.1145/7531.8928; Ben-Sasson/Wigderson, JACM 48 (2001), doi:10.1145/375827.375835; Fortnow et al., JACM 52 (2005), doi:10.1145/1101821.1101822; Jeřábek, https://cs.stackexchange.com/questions/166831/tseitin-formula-on-2-connected-graph.