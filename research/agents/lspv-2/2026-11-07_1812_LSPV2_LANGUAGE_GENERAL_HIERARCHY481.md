# LSPV-2/481 | Language-general code-aware contraction firewall
**Date:** November 7, 2026 18:12 PST (America/Los_Angeles). **Role:** LSPV-2, Route A primary. **Status:** PROVED/RESTRICTED as a corollary of the classical deterministic time hierarchy; COMPUTATIONAL finite regression checks. **P versus NP OPEN.**

**Tracker dependencies:** [P2-A2] remains OPEN, with [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04] OPEN. No historical R_mix341 rules, weights or ownership were altered.

## IDEA, falsifiers, and exact model
**Initial idea.** An effective compiler that inspects arbitrary decider **code** and promises the Route A time contraction for *every language in P*, not just SAT, should contradict the deterministic time hierarchy. This strengthens LSPV-2/478's answer-only/extensional firewall in a **different restricted scope**: here the compiler may inspect its input machine's entire code, but is forbidden to use a promise restricted to SAT semantics.

Four falsifiers specified before source inspection:
1. **F1:** The claimed strict $n^2$ versus $n^{3/2}$ deterministic time hierarchy might fail on the declared model. We use the standard deterministic multitape TM, where it is established.
2. **F2:** The compiler might be guaranteed ONLY for SAT deciders, not arbitrary P languages. Then this theorem **does not apply**. This is the crucial scope limitation.
3. **F3:** The compiler's output might not be in the promised total-polynomial language-general decider class, preventing iteration. Recursive closure is an explicit hypothesis.
4. **F4:** The alleged exponent improvement might hide constant-to-exponent or machine-conversion overhead. Both iterations must be on one fixed deterministic multitape model with $n^{o(1)}$-only exponent slack and all costs charged.

## Theorem 481.1 (PROVED/RESTRICTED, classical hierarchy corollary)
Fix the standard deterministic multitape TM complexity measure. There is NO effective transformation $\mathcal C$ defined on the code of **every** total correct polynomial-time binary-language decider $A$ such that all of the following hold:
(i) $\mathcal C(A)$ is a uniform total correct decider for the **same arbitrary language** as $A$, on every binary input;
(ii) it is again in the domain of $\mathcal C$ (unrestricted recursive applicability);
(iii) if $A$ has all-input worst-case time $T_A(n)\le n^{t+o(1)}$ for some finite real $t$, then $\mathcal C(A)$ has a **fully charged same-machine** bound
$$
T_{\mathcal C(A)}(n)\le n^{f(t)+o(1)},\qquad
f(t)=\max\left(\frac{11}{10},\frac35+\frac t2\right).
$$
No restriction on the code inspection, preprocessing, or transformation internals is needed beyond these promises.

**Proof.** The deterministic time hierarchy supplies a language $L\in\mathrm{DTIME}(n^2)\setminus\mathrm{DTIME}(n^{3/2})$ in the standard multitape model. Let $A$ be its uniform total correct $n^2$-time decider. By (i)-(iii) $A_1=\mathcal C(A)$ is a correct all-input $L$ decider with exponent at most
$$ f(2)=\frac85. $$
By recursive applicability, $A_2=\mathcal C(A_1)$ decides the **same** $L$ with exponent
$$ f\!\left(\frac85\right)=\frac75<\frac32. $$
For any sufficiently small fixed $\epsilon>0$ one has $n^{7/5+o(1)}=O(n^{3/2-\epsilon})$, hence $L\in\mathrm{DTIME}(n^{3/2})$, contradiction. QED.

This is an **unconditional** language-general compiler no-go *on the stated standard model*. It is a direct consequence of a known hierarchy theorem, not an original proof of a new time hierarchy. It proves neither SAT hardness nor a no-go for SAT-specific, solver-dependent code-aware contraction. In particular, do NOT silently transfer standard-multitape exponents to the FLMV indexed random-access machine; a separate native-model hierarchy/simulation would be required.

## Theorem 481.2 (stronger one-step firewall; PROVED/RESTRICTED)
**Recursive closure is not needed** for the language-general obstruction. The standard deterministic time hierarchy also provides a language $L\in\mathrm{DTIME}(n^2)\setminus\mathrm{DTIME}(n^{7/4})$. If an effective language-general code-aware compiler preserves every such $L$ and maps a decider of exponent $t=2$ to the fully charged same-standard-multitape bound $f(2)=8/5$, its **first** output would decide $L$ in time $n^{8/5+o(1)}=O(n^{7/4})$, contradiction. Therefore **even a one-shot** all-P-languages time-contraction compiler with that envelope is impossible on the stated model. The two-step $2\to8/5\to7/5$ analysis remains a separate exact recurrence/recursive-closure control, but is not logically necessary for this stronger no-go. No claim about a SAT-only transformer or the native FLMV model follows.

**Independent challenge:** Removing the recursive-closure assumption was a valid strengthening discovered after checking the hierarchy quantifiers. The theorem's *domain-general* assumption cannot be removed by this argument, since time-hierarchy languages need not admit SAT-specific source semantics. A practical candidate $A\mapsto\Phi(A)$ must therefore disclose where it uses SAT semantics, not merely full access to program code.

## SEARCH (primary statements and actual code)
Checked:
- Hennie and Stearns (1966), *Two-Tape Simulation of Multitape Turing Machines*, JACM 13(4):533-546, DOI 10.1145/321356.321362. Together with the deterministic time hierarchy, supports strict separation of $\mathrm{DTIME}(n^{3/2})$ and $\mathrm{DTIME}(n^2)$ for standard multitape machines.
- Hartmanis and Stearns (1965), *On the Computational Complexity of Algorithms*, Transactions AMS 117:285-306, deterministic time hierarchy foundations.
- Fortnow, Lipton, van Melkebeek, Viglas (2005), *Time-Space Lower Bounds for Satisfiability*, JACM 52(6):835-865. **Different** indexed random-access machine and SAT-specific theorem. No model change is asserted.
- Existing project: complete root [P1-01], [P1-03], [P1-04], [P2-A2], [P2-A4], [P2-A5]; LSPV-2/478 answer-only firewall, /479 exponent extractor impossibility, /480 native guest threshold; LSPV-4/481 and /482; current issue #3; November 2 governing five-role handoff; AGENTS.md, CODEX.md, research skill; GROKPROOF/2026-11-06_2316_PROGRESS.md; research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex.
- Required external source review, pinned blob IDs: konard/p-vs-np README.md `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`, TOOLS_AND_METHODOLOGIES.md `b3f5ceb025a75360d1956f4bb0ab6ae702761283`; blkph0x/p-vs-np-proof-research METHOD_INDEX.md `18d693ea71dfa433370eb7afbebc3106e32f03e5`, INDEPENDENT_AUDIT.md `b30515cced93d8911a6415555ee9ec1444502d93`. None proves universal SAT contraction.
- Other pinned controls: meelgroup/frat-xor format.md `986a21aa92b62f844ef1fce852193142c41b2b1f`; MassimoLauria/cnfgen cnfgen/families/tseitin.py `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab`; berkeley-abc/abc README.md `88a9d1a316dd9751acade746de315fd1e6e6c362`; openai/math lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean `1ced21f44ad49370d1b812e862c03c3a91d7f836`. Verified these files' actual contents, not repo names as proof authority. No direct Google-branded access; general web primary-source search was available.

## ITERATE: revision after checking assumptions
Initial tentative formulation could have been overbroad: a time-hierarchy separation for ordinary TMs does **not** establish a hierarchy at the exact FLMV resource exponents. Revised and proved claim is explicitly restricted to a **language-general, same-standard-multitape-model** compiler. It even permits full code inspection, but it does NOT apply if the transformation exploits SAT-specific syntax, correctness, self-reduction, or other domain semantic features. This distinction is the substantive firewall: a proposed code-aware $A\mapsto\Phi(A)$ cannot be justified by a *language-independent* machine rewriting principle alone.

## Established hard-family and shortcut ledger
Tseitin on connected cubic graphs has $H$ parity vertices, $3H/2$ original edge variables, exactly $4H$ strict proper ternary clauses and binary source length $N=\Theta(H\log H)$. Odd total vertex charge certifies UNSAT. For appropriate bounded-degree expander graphs, ordinary shared-DAG Resolution requires $2^{\Omega(H)}$ proof size (precise hypotheses in published Urquhart and Ben-Sasson/Wigderson width literature); this is not a general SAT algorithm lower bound. GF(2) elimination solves this affine family in polynomial time, and can defeat a Resolution-only argument. CNFgen's pinned tseitin.py constructs parity clauses. Test graph K4 is **not** an asymptotic expander-hard witness. Existing OR-folding, tree/path-interface, AND3/GF(2), learned shared-DAG, and ER shortcuts remain legal controls; any native R_mix341 certificate must be separately authenticated.

## Verification, finite controls, resources
Independent Python exact Fraction replay: 90 assertion groups, including all sixteen K4 signed strict-3CNF sources (eight SAT/eight UNSAT, 8 models per SAT source), and the recurrence $2\to8/5\to7/5\to13/10\to5/4\to49/40\to97/80$. Python raw JSON SHA-256: `a8cf4b2d8c3a1ac854d957185f5d91f28e31a540c9e3214b2707f3cce013224d`. Separately written Node.js replay: 25 checks passed and the same recurrence and sixteen source classifications. The published independent verifier and raw summary are finite **COMPUTATIONAL** controls; they do not mechanically prove the hierarchy theorem or execute native FLMV.

Logical proof nodes: none; no R_mix341 proof is generated. Evidence bits: report/code/JSON explicit UTF-8 bytes, not inference weights. Actual host verification performs O(16*2^6*16) small clause evaluations plus fixed rational operations; no asymptotic SAT solver claimed. The hypothetical compiler's time bound must charge parsing, full code/source reads, trace acquisition, failed searches, construction, guests, recursion, caching, output and verification, and any memory allocation. This impossibility uses only its promised time bound; no space bound, FLMV indexing conversion, or actual native execution is inferred. The special-form SAT controls are independently checked, but neither 3-label malformed totality nor arbitrary-input SAT decisions are proved by these finite tests.

## Handoff / exact remaining gap
[P2-A2] is **still OPEN**. A genuinely SAT-specific, solver-intensional, exponent-oblivious, all-input, recursively iterable compiler on the original FLMV machine is required. The impossibility of a language-*general* optimizer is not an impossibility of that target. [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04] remain OPEN. Route B [P2-D1], [P2-C3], [P2-B1], [P2-B2] unchanged. All five agents, two Route A/three Route B, original schedules, historical weights remain unchanged. **P versus NP remains OPEN.**
