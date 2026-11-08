# LSPV-4/481 | Explicit finite FLMV entry without computing a decider exponent
**November 7, 2026, 16:36 PST | Route A Resource Auditor | PROVED/RESTRICTED and COMPUTATIONAL | P versus NP OPEN**

**Node map:** [P2-A3] conditional arithmetic retained; [P2-A4] native machine resource ledger OPEN; [P2-A5] quantified finite-iteration requirement refined; [P2-A2] universal, effective contraction OPEN; [P1-01], [P1-03], [P1-04] OPEN. No Route B node is closed.

## IDEA → SEARCH → ITERATE

**Idea / prediction:** LSPV-2/479 shows a partial computable routine cannot reliably extract a polynomial running-time exponent from every correct polynomial SAT decider, even under SAT-in-P. A contradiction via the proposed recursion may nevertheless use *some finite iteration depth chosen existentially*, without an effective degree extractor. **Predeclared falsifiers:** (F1) no finite depth achieves strict entry for large finite initial exponents; (F2) a claimed beta tangent bound is false; (F3) choosing the depth existentially makes the final machine nonuniform in input length; (F4) unspecified physical simulator costs defeat the resource recurrence. F1-F3 fail under the precise hypotheses. F4 remains OPEN and load-bearing.

**Project SEARCH (actual files):** both full trackers; current issue #3 and last comments; research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md; AGENTS.md; CODEX.md; .codex/skills/pnp-research/SKILL.md; LSPV-2/478 and /479 (notably research/agents/lspv-2/2026-11-07_1618_LSPV2_EXPONENT_PROMISE_FIREWALL479.md, blob 8b4c8b549ae7445aecb21f2afd7a21cbac4f799a); previous LSPV-4/480 (research/agents/lspv-4/2026-11-07_1540_LSPV4_FLMV_EXPONENT_SLACK_BUDGET480.md, blob fda77cf7d35dbc6f392715a7c38604af1592252e); GROKPROOF/2026-11-07_1920_PROGRESS.md (231561ce216699f286b705a0056584789ba9ee99); Claude research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex (9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a). Root main.tex yielded SHA 68188a24badda635a5983fda1c381cdb694fd497 but zero readable bytes. It was NOT edited.

**Primary literature:** Fortnow, Lipton, van Melkebeek and Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52 (2005), author PDF https://lance.fortnow.com/papers/files/tst.pdf, Section 2.1 and Corollary 5.8 inspected in page screenshots. The stated bounds are on the paper's indexed random-access machine. Ben-Sasson and Wigderson, *Short Proofs Are Narrow*, JACM 48 (2001), supplies only an ordinary shared-DAG Resolution hard-family control, not arbitrary-machine hardness.

**Repository/path/ref audit:** konard/p-vs-np/proofs/complexity/README.md (blob 7ee9a11e, finite one-tape model, not indexed-FLMV equivalence); blkph0x/p-vs-np-proof-research/METHOD_INDEX.md (18d693ea) and affine_projection_recognition_lab/fixed_width_hierarchy/THEOREM.md (4aba9d94, a bounded-representation Boolean-hierarchy result); MassimoLauria/cnfgen/cnfgen/families/tseitin.py (4bb5fd19, source construction); meelgroup/frat-xor/README.md (38a137bc, a distinct proof checker); openai/math/README.md (cc5b0a03, varying proof status); berkeley-abc/abc/README.md (88a9d1a3, DAG-aware circuit rewriting, no all-input machine transfer). No separate Google-branded search available; web search and GitHub source retrieval actually used. No direct native FLMV execution.

**ITERATE:** Previous LSPV-4/480 already derived the limiting resource envelope. The new increment is an explicit *finite* depth bound with reserved safety margin and the precise quantifier distinction between selecting a fixed program in an existence proof and computing an exponent from arbitrary code. This is elementary mathematics; no novelty claim.

## Theorem 481.1 (PROVED/RESTRICTED, CONDITIONAL as applied to SAT)

Assume a single effective, recursively iterable, all-input, both-label/malformed-correct transformation on the **same FLMV machine**, with all physical phases included, really satisfies the exponent recurrence

$$
t_{j+1}\le\max\left(\frac{11}{10},\frac35+\frac{t_j}{2}\right),
\qquad
s_{j+1}\le\max\left(\frac12,\frac{s_j}{2}\right).
$$

For any finite starting exponents $t_0\ge1,s_0\ge0$, put

$$
D_t=(t_0-6/5)_+,\qquad D_s=(s_0-1/2)_+,\qquad
A=\frac{433}{216}D_t+D_s.
$$

Then for every nonnegative integer $j$,

$$
\boxed{\ \beta(t_j)-s_j \ge \frac1{90}-2^{-j}A\ },
\qquad
\beta(c)=\frac12\left(\frac{c+2}{c^2}-c\right).
$$

In particular, every **finite** $j$ with $2^{-j}A\le1/180$ yields the strict certified margin

$$
\boxed{\ \beta(t_j)-s_j\ge\frac1{180}>0\ }.
$$

**Proof:** $g(t)=\max(11/10,3/5+t/2)$ is $1/2$-Lipschitz and fixes $6/5$, hence $t_j\le6/5+2^{-j}D_t$. The same argument for $h(s)=\max(1/2,s/2)$ gives $s_j\le1/2+2^{-j}D_s$. On $c\ge6/5$,
$$
-\beta'(c)=\frac12\left(1+\frac1{c^2}+\frac4{c^3}\right)\le\frac{433}{216}.
$$
As $\beta(6/5)=23/45$, monotonicity and the mean-value inequality yield
$\beta(t_j)\ge23/45-(433/216)2^{-j}D_t$ even if $t_j\le6/5$ (then the bound is weaker). Subtract $s_j$ and use $23/45-1/2=1/90$. QED.

**Quantifier point:** Under the hypothetical SAT-in-P premise, the initial fixed correct uniform decider has some finite exponents $t_0,s_0$. The existence proof may select a finite integer $j$ depending on *those mathematical witnesses* without requiring an algorithm to discover them from arbitrary source code. If $\Phi$ itself is effective and its outputs remain valid inputs to $\Phi$, the fixed composition $\Phi^j(A_0)$ is one finite **uniform** program for all input lengths. This does not circumvent LSPV-2/479's no-extractor theorem, and cannot replace an actual $\Phi$.

**Subpolynomial slack:** For fixed $j$, $n^{o(1)}$ costs at each level can be absorbed into any constant positive additional exponent for sufficiently large $n$. With time and space exponent error each $\epsilon=1/1000$, the gap loses at most $(1+433/216)\epsilon<1/180$, so the final inequality remains strict. The argument does NOT justify growing $j=j(n)$ or hide unknown intermediate native costs.

## Established hard-family and shortcut control

For a connected cubic $H$-vertex graph, write each vertex equation $x_{e_1}\oplus x_{e_2}\oplus x_{e_3}=b_v$ as the four proper width-three signed clauses excluding the wrong-parity assignments. Direct exact 3-CNF encoding: $3H/2$ variables, $4H$ clauses, $N=\Theta(H\log H)$ bits. Odd total charge certifies UNSAT; for suitable expanding cubic families, established size lower bounds hold for **ordinary shared-DAG Resolution** only (Ben-Sasson-Wigderson, 2001, Theorem 4.4/Corollary 4.5). Linear-time charge summation/GF(2) elimination is the relevant easy-computation control. No proof-system lower bound is transferred to all SAT algorithms or full R_mix341. No external 3-CNF reduction is used.

## COMPUTATIONAL controls and full resource qualification

Standalone exact-rational Python script tests 3,008 seeded initial pairs (including $t_0=s_0=10^6$) and checks envelope inequalities, tangent bounds, reserved gap and minimal chosen depth; **15,040 exact assertions pass**, maximum selected depth 30, minimum tested gap 0.00560485372653849 > 1/180. An initial invalid $t_0=0$ control was removed because $\beta(0)$ is undefined; final tests enforce $t_0\ge1$. This does not execute a SAT algorithm, certificate checker or a native FLMV machine.

**Resource ledger:** source parsing, original-bit/index/head reads, malformed checks, local failed policies, q child generations/materializations/lazy ports, outputs and conversion must *actually* fit $N^{11/10+o(1)}$ local time; q must fit $N^{3/5+o(1)}$ and each guest length $N^{1/2+o(1)}$. All-phase simultaneously retained ancestor frames, guest WORK/INDEX tapes, address/caches, replay/recomputation, retrieval, clearing and outputs must *actually* fit the claimed peak recurrence. None is established here. Abstract recurrence arithmetic does NOT pay these costs by itself.

**Actual advance:** explicitly certified finite entry, quantifier reconciliation with LSPV-2/479, 15,040 exact numerical/rational checks. **Remaining gap:** [P2-A2] effective universal contraction; [P2-A4] native full cost; [P2-A5] all-input closure. Fixed historical R_mix341, five-agent allocation, role ownership and schedules unchanged. P versus NP OPEN.
