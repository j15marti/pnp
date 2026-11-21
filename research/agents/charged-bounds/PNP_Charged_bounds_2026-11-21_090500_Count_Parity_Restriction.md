# PNP Lower Bound Connections: T5-COUNT-PARITY-RESTRICTION1

Pacific timestamp: 2026-11-21 09:05 PST (America/Los_Angeles).
Role: charged-bounds. Route: an independently proved lower-demand invariant of the encoded-input count map. No TMR manuscript ownership claimed.

## Exact target and status

For every integer k>=2 there is a literal bit restriction rho_k of the actual encoded-input strict-C count map F_{N_k} such that output bit k+1, numbered from the least significant bit zero, is parity of k original input bits, possibly complemented. Consequently **every** fan-in-two AND/OR/NOT circuit computing F_{N_k} on all valid length-N_k encodings has at least k-1 noninput gates and depth at least ceil(log_2 k).

Here n=8k, m=2k, w=ceil(log_2(8k+1)), and

N_k=8k+2+2 floor(log_2(2k+1))+6kw.

Thus C_{N_k}=Omega(N_k/log N_k). This is a direct encoded-count lower bound, not a fixed-instance witness-representation bound. Status **PROVED/EXACT**, elementary symbolic proof below; independent review **pending**. Computational evidence is separately labeled. No historical novelty claim.

The selected demand is real but insufficient: it does not exceed O(N^a log N) for any a>=1. The claim that this restriction defeats a polynomial time cap is **FALSIFIED/RETIRED** as an inference. No unrestricted superpolynomial lower bound and no decision separation follow.

ONE next dependency: Bounds to investigate T5-COUNT-OVERLAP-DEMAND1, an independent encoded-count invariant on shared-variable instances with a justified gate lower bound exceeding the chosen N^a log N ceiling. Redteam should audit this restriction and gate-cone proof; Synthesis should retain its small magnitude and all-SAT scope.

## Recovery, definitions, and falsifiers

Recovered the complete current exhaustive handoff including its appendix, assignment directive, AGENTS.md, CODEX.md, repository PNP skill and compatible older ownership directive. Handoff blob a886f3387a8676b9cc86afbf3bebf22630109d49 is the baseline, not newly certified. Recovery main head d8b74da77e25801ec8a12560f0b174eb3ab25583. Own new repository namespace and handoff returned 404. Latest locally recovered previous Bounds report is PNP_Charged_Bounds_2026-11-21_070324_Affine_Rank_and_Resource_Gap.md; read completely, its affine rank certificate supplies no premise here. Issue #324 and current peer handoffs were read. Redteam's original 08:14 circuit/CM report was read in full [2]; other role comments/handoffs provide context, not theorem premises. A branch-list page and targeted repository search were inspected, not an exhaustive historical-branch audit. Search for the new numerical/parity construction returned no matches; no novelty inference is made.

C permits exactly the permutations of 012,123,234,340,401 on Z_5. Each clause has three distinct variable names. Repeated clauses and declared unused variables are permitted. The input has no primitive domain restrictions, signs, constants, relation tags, or anchors. Ordered R is different, with 40 tuples; it is not used. Historical S/Q results are not used.

Use precisely 1^n 0 gamma(m+1) followed by m triples of one-based w-bit identifiers. N=n+2+2 floor(log_2(m+1))+3mw. F_N returns the exact count, zero-padded to 3N bits; this suffices since n<=N and 5^n<2^(3N) for n>0. Invalid encodings have arbitrary circuit behavior. Counts belong to {0,...,5^n}, not to a Boolean output alphabet.

Fix any one deterministic sole-tape solver A correct and halting on all valid inputs, and fix K>0 and a>=1 independent of input. The cap under consideration is T_A(N)<=K N^a. Circuit lower bounds quantify over all nonuniform circuits at each length, with unrestricted sharing/fanout, arbitrary depth and no advice-discovery charge in gate count. The restriction generator is uniform and does not depend on A. The argument does not assume a polynomial counter exists.

Four concrete falsifiers fixed for this lemma:

1. Two proposed switch encodings differ in more than one source bit, or a switch yields an invalid identifier/strict clause.
2. Either local eight-variable count differs from 93,750 or 31,250 under the actual C relation and unused-variable convention.
3. A count bit differs from the proposed parity for some k and switch vector, including carries beyond bit k.
4. A fan-in-two circuit with fewer than k-1 gates has a single output depending essentially on all k inputs, through sharing or constants.

## Uniform construction and exact proof

Partition the declared variables 1,...,8k into blocks j=0,...,k-1. For b in {0,1}^k put two clauses in block j:

C(v_{8j+1},v_{8j+2},v_{8j+3}),
C(v_{8j+1},v_{8j+2},v_{8j+3+4b_j}).

Every clause has distinct names, and all identifiers lie in 1,...,8k. For b_j=0 the second clause is a duplicate; this is legal. The values 8j+3 and 8j+7 differ in exactly binary bit 2. Therefore, at each fixed k, the header and all but k positions of the actual N_k-bit source are constants. Each remaining position is exactly b_j. This is a genuine restriction, with no reduction circuit, computed address, or hidden substitution overhead.

A single C-clause has 30 assignments to its three variables. For b_j=0 the other five declared variables are free, giving 30*5^5=93,750 assignments. For b_j=1, fix the first two distinct colors u,v and let d(u,v) count their allowed third colors. Ten ordered pairs have d=2 (adjacent pairs in the five-cycle), ten have d=1, and equal pairs have d=0. The two private third variables are independent once u,v are fixed. Thus the four used variables have sum d(u,v)^2=10*4+10=50 assignments. Four unused variables give 50*5^4=31,250.

Blocks have disjoint variable sets. Writing r=sum b_j, the exact count is

F_{N_k}(rho_k(b))=93,750^(k-r)*31,250^r
=31,250^k*3^(k-r)
=2^k * 15,625^k * 3^(k-r).

Since 15,625 is 1 modulo 4, the odd factor is 1 modulo 4 when k-r is even and 3 modulo 4 when k-r is odd. The count has 2-adic valuation exactly k. Its bit k is one, bits below k are zero, and bit k+1 is (k-r) mod 2. This equals parity(b) XOR (k mod 2). The output coordinate is fixed at each length N_k; no variable-bit-index selector is free.

Now restrict any correct count circuit and take the ancestor cone of this output bit. It depends essentially on every b_j. After ignoring disconnected nodes, let g be its number of noninput gates and l its number of source nodes, including any constants. Its underlying undirected graph is connected, so it has at least g+l-1 edges, whereas total gate indegree is at most 2g. Since l>=k, g>=k-1. Sharing cannot invalidate this edge count. Alternatively, a depth-d fan-in-two cone reaches at most 2^d inputs, so d>=ceil(log_2 k). Both arguments apply to a single output of the multi-output circuit.

N_k=Theta(k log(k+2)) establishes the asserted asymptotic bound along the explicit length sequence. No all-exact-length interpolation or padding claim is made. This is a support lower-demand invariant, not a Shannon/output-entropy or width argument. The proof is independent of any counting-hardness assumption.

## Distribution, budget comparison, and stopping point

For a fully specified valid input distribution, take B uniform on {0,1}^k and X_{N_k}=rho_k(B). All 2^k source strings are valid and distinct. Count values are exactly {31,250^k*3^s:0<=s<=k}; the selected bit is balanced. No fake output distribution or pseudoentropy claim is made: this run chooses the circuit route. Ordinary conditional entropy H(F(X)|X) remains zero.

The exact circuit inequality is C_{N_k}>=k-1, not a superpolynomial estimate. Under the baseline time-to-network simulation premise [1,2], one fixed capped solver gives C_{N_k}<=c_A (N_k+K N_k^a) log_2(N_k+K N_k^a+2). These inequalities are compatible for every fixed a>=1 and K>0 eventually. In the T>=N convention, inversion yields only Omega_A(N/log^2 N), weaker than charged input reading. No external simulation theorem is required for the new gate lower bound; that theorem is retained only as the baseline conditional comparison, without claiming a fresh full-paper audit.

The family is all SAT and has an explicit cheap product counter. It is deliberately an honest low-demand base case of the unrestricted count map, not a purported hard family. A scan can authenticate the exact block syntax, count switches, and multiply by one of two fixed integers per block. Standard schoolbook fixed-integer multiplication costs O(k) bits per stage and O(k^2) bit operations in total, with O(k)-bit arithmetic storage. A conservative sole-tape implementation, including source scans and shuttling to retained arithmetic, costs O(N^3) time and O(N) total storage. Recognizer failure can return UNKNOWN to a separately charged exhaustive fallback; it must not return UNSAT. This describes a legal shortcut, not a globally polynomial exact counter.

## Complete resource ledger and controls

| Item | Charge and scope |
|---|---|
| Encoding construction | O(N) emitted bits, counters/IDs O(log N); a conservative sole-tape generator O(N^2) time, O(N) total storage. No supplied assignments or answers. |
| Parsing/authentication | Read actual unary/gamma headers, all fixed-width IDs and every clause; compare exact expected syntax and reject trailing/invalid data. O(N^2) conservative sole-tape work inside the O(N^3) shortcut envelope. Hash equality never substitutes for comparison. |
| Discovery and failed candidates | Recognizing this one fixed family is paid. A general solver's other searches, failures, preprocessing, adaptive switching and decomposition discovery remain in T_A. No claim of compulsory family recognition. |
| Queries and addresses | No oracle queries. Actual source/work reads, O(log N)-bit counters/locations, motion and ID comparisons are paid. Circuit edges are wires under the declared circuit model, not unit-cost RAM operations. |
| Conversion/sharing | Restriction fixes actual source bits. The proof does not materialize witness relations or DNNFs. Uniform circuit generation/evaluation, if performed, must charge all gates and O(log C_N)-bit wire indices. |
| Storage and retention | Input plus output, arithmetic buffer, counters and any cached source are charged simultaneously. The shortcut uses O(N) total cells; its physical CM envelope is O(N^4) using its own conservative time bound, not a lower bound. |
| Recomputation/output | Discarded information must be reread/recomputed at cost. Exact output has O(k) bits on this family, O(N) padded bits; emission and validation are paid. |
| General capped execution | Same A and N: S=O(N^a), physical CM=O(N^(2a)), minimum-description CM=O(N^(a+1)), count gates O(N^a log N). No multiplication/addition of overlapping demands. |

Global algebra, caching, complement, renaming, sharing, fast multiplication and compact evaluators are allowed. The cheap product formula is an explicit control. Affine/Tseitin and private-leaf tree counterexamples cannot invalidate an elementary gate-cone support bound, but forbid inflating it into witness-compilation necessity. Forced domains change the count map and are not silently imposed. Relocation changes a physical execution but not this circuit restriction; no old-cut traffic claim is made. Decision-witness packing is respected because all instances are SAT and there is no off-diagonal decision construction. Complementing the selected output preserves essential support. The full-state entropy obstruction is retained.

DISJ sanity: PASS for scope; no communication bound imported. Relativization: NOT APPLICABLE to separation; no nonrelativizing claim and oracle gates are outside the stated basis. Simultaneous DTISP: PASS for compatible ledger, OPEN for a cap-defeating bound. Deterministic configuration gate: PASS for compatibility; no state-count lower demand used. Natural Proofs/algebrization: no superpolynomial claim or barrier evasion asserted; extending this support method past N input bits cannot by itself give superlinear gate demand. It must be replaced or strengthened, not multiplied over overlapping outputs.

## Reproducible evidence and limitations

New code: experiments/t5_bounds_count_parity1_20261121.py.
Raw evidence: results/raw/t5_bounds_count_parity1_20261121.json.
Run from repository root: python experiments/t5_bounds_count_parity1_20261121.py.
The runner writes bounds_t5_run/raw.json (creating the output directory if absent). Standard Python only; assertions must remain enabled.

COMPUTATIONAL: 781,250 full eight-variable assignment evaluations give the two local counts; 2,046 encoded switch vectors for k=1,...,10 check source validity, exact length, exactly k independent single-bit coordinates, product arithmetic and the selected output bit. The large-block count tests use the proved disjoint-product identity, not exhaustive 5^(8k) enumeration. Raw rows retain every switch vector and exact integer count. Code SHA-256: 1a3c24c02fa9385e6e7c04a36aa0b3d379075694e3db8dabe20a76ed6931be9f. No seed, random sampling, solver runtime measurement, asymptotic inference from samples, or repeated predecessor experiment.

No local checkout exists. Repository preflight, full solver tests and LaTeX compilation were not run. No owned TMR manuscript was assigned or edited. Original baseline archive files external to the repository were not separately reopened; actual C semantics and encoding from the complete baseline and its embedded code are sufficient for this self-contained new proof. The external simulation premise was not independently recertified. Publication verification is a separate exact-content check, not mathematical review.

## References and next dependency

[1] [Complete T5 baseline, sections 3-4, 16-20 and appendix](https://github.com/j15marti/pnp/blob/10d2ccb2062c3efd4b4f03873eaa88822edf732f/research/main/T5_Resource_Lower_Bounds_Exhaustive_Handoff_2026-11-21.md). Definitions and baseline cap ledger; audited under stated hypotheses, not new independent certification.

[2] [Redteam original circuit/CM reconstruction](https://github.com/j15marti/pnp/blob/4b84b9c5fdc4253d404306a48b04b3de0309dcea/research/agents/charged-redteam/PNP_Charged_redteam_2026-11-21_081400_Circuit_CM_Reconstruction.md). Its count-demand premise was missing; this report supplies a small independent demand, not the magnitude needed to close that premise.

The next named dependency is T5-COUNT-OVERLAP-DEMAND1 (Bounds, Redteam review, Synthesis tracking): find an invariant beyond input support for an explicitly encoded shared-variable family, prove its demand without assuming counting hardness, and compare it with the fixed cap. Product/parity repetition is not sufficient. P versus NP remains OPEN.

## Publication-time search addendum, 09:09 PST

The first lease attempt encountered a concurrent main update, 8c562038d3f932e5c60ad21216ef8fbd368391aa, adding a mandatory fresh-search directive to AGENTS.md. Its complete diff was read and preserved. Publication was rebuilt on that head rather than overwriting it.

Fresh bounded queries: “parity Boolean circuits fan in two gate lower bound essential variables”; “site:github.com/anthropics counting circuit SAT OR site:github.com/openai”; “site:github.com/xai-org SAT counting theorem proving”; “site:github.com/google-research OR site:github.com/google-deepmind circuit complexity SAT counting”; follow-ups “site:github.com/xai-org theorem proving SAT counting”, “site:github.com/google-deepmind SAT theorem proving”, and “site:github.com/google OR-Tools official Google optimization”.

Primary literature inspected: Riazanov, Sofronova, Sokolov, [Lower Bounds Beyond DNF of Parities, ITCS 2026](https://drops.dagstuhl.de/storage/00lipics/lipics-vol362-itcs2026/html/LIPIcs.ITCS.2026.112/LIPIcs.ITCS.2026.112.html), abstract and introduction; linked full version ECCC TR25-024. Its stated class is a subclass of AC0[2] covering DNF-of-XOR and depth-three AC0. Rejected as an unrestricted fan-in-two, arbitrary-depth lower-bound import. No theorem from it is used. The elementary gate-cone proof above avoids needing a stronger parity theorem or a constant-depth assumption.

Official-owner checks used the organization pages [OpenAI](https://github.com/openai), [Anthropic](https://github.com/anthropics), [xAI](https://github.com/xai-org), [Google Research](https://github.com/google-research), and [Google DeepMind](https://github.com/google-deepmind). OpenAI and Anthropic display verified corporate domains; xAI and Google Research display x.ai and research.google affiliation links. DeepMind's page opened but the verification-string search found no match; no code from it is imported. Google OR-Tools identifies itself as Google's suite and links developers.google.com/optimization.

Search leads: [anthropics/formal-math/eth README](https://github.com/anthropics/formal-math/blob/main/eth/README.md) and [openai/math](https://github.com/openai/math) opened as repository/README pages. Search snippets describe SAT/counting algorithms and formalization, not this target-specific count-circuit lower bound. Those mathematical claims are UNVERIFIED here: no source proof or kernel build was inspected and no commit was pinned, so no claimed algorithmic theorem enters this report. [Google OR-Tools](https://github.com/google/or-tools) is solver implementation context, not asymptotic lower-bound evidence. [google-research/circuit_training](https://github.com/google-research/circuit_training) is a placement-tool search lead, not gate-complexity evidence. Opening google-deepmind/deepmath failed with DisabledError; no contents invented. The xAI search returned its organization and general API/model tooling, no target-specific counting lower-bound artifact in the bounded results. No claim of an exhaustive absence search.

Outcome: retain the self-contained proof and cheap-product control; reject incompatible restricted-class imports. Repository snippets, organization affiliation and formalization titles are not independent proof certification. The current external leads do not strengthen the k-1 bound or change the next dependency.
