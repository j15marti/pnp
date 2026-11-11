#!/usr/bin/env python3
"""Build the P vs NP world ledger (CLAUDE WORLD-LEDGER-0001).

Source of truth for the seeded statements is the ``rows`` list below.
Running this script regenerates, next to itself:

* ``P_vs_NP_World_Ledger.xlsx`` -- the spreadsheet, with live formulas for the
  Category and Consistency columns (recalculate in Excel / LibreOffice /
  Google Sheets after generating);
* ``world_ledger.csv`` -- a plain-text copy with Category and Consistency
  computed in Python by ``classify`` / ``consistency`` (same rules as the
  spreadsheet formulas), so agents can read the ledger without a spreadsheet.

Report with definitions, proofs and category semantics:
research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex

Usage: python research/agents/claude/world-ledger/build_ledger.py
Requires openpyxl. P versus NP remains OPEN; nothing here is a proof of it.
"""

import csv
from pathlib import Path

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.utils import get_column_letter

HERE = Path(__file__).resolve().parent
OUT = str(HERE / "P_vs_NP_World_Ledger.xlsx")
CSV_OUT = HERE / "world_ledger.csv"
REPORT = "research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex"

FONT = "Arial"
f_base = Font(name=FONT, size=10)
f_bold = Font(name=FONT, size=10, bold=True)
f_head = Font(name=FONT, size=10, bold=True, color="FFFFFF")
f_title = Font(name=FONT, size=14, bold=True)
f_small = Font(name=FONT, size=9, italic=True, color="555555")
fill_head = PatternFill("solid", start_color="1F3864")
fill_auto = PatternFill("solid", start_color="EDEDED")
wrap = Alignment(wrap_text=True, vertical="top")
center = Alignment(horizontal="center", vertical="top", wrap_text=True)
thin = Side(style="thin", color="BFBFBF")
border = Border(left=thin, right=thin, top=thin, bottom=thin)

T, F, O = "True", "False", "Open"

# (ID, statement, Algorithmica, Heuristica, Pessiland, Minicrypt, Cryptomania,
#  known, rel, nat, alg, source, notes)
rows = [
    ("L01", "Σ₂P ⊄ SIZE(nᵏ) for every fixed k", T, T, T, T, T, "Theorem",
     "Yes", "No", "Yes", "Kannan 1982; Karp–Lipton 1980",
     "Win-win on whether NP ⊆ P/poly."),
    ("L02", "Either P ≠ NP or E ⊄ SIZE[2ⁿ/n]", T, T, T, T, T, "Theorem",
     "Yes", "No", "Yes",
     "If P = NP then Σ₂E = E by padding; Σ₂E ⊄ SIZE[2ⁿ/n] is Chen–Hirahara–Ren 2023 (arxiv.org/abs/2309.12912)",
     "Hardness conservation: hardness sits in NP (against algorithms) or in E (against circuits)."),
    ("L03", "E ⊄ SIZE[2ⁿ/n] (near-maximum circuit lower bound for E)", T, O, O, O, O, "Open",
     "Yes", "n.a.", "Yes", "Follows from P = NP via L02",
     "Would give BPP = P (Impagliazzo–Wigderson 1997). Technique tags describe the P = NP-side derivation."),
    ("L04", "BPP = P", T, O, O, O, O, "Open",
     "Yes", "n.a.", "Yes", "Sipser–Gács–Lautemann: BPP ⊆ Σ₂P ∩ Π₂P",
     "Conjectured in every world; would follow from L03."),
    ("L05", "P ⊄ SIZE(nᵏ) for every fixed k", T, O, O, O, O, "Open",
     "Yes", "n.a.", "Yes", "L01 plus the collapse PH = P",
     "Best unconditional circuit lower bounds for P are only linear."),
    ("L06", "NP ⊆ P/poly (SAT has polynomial-size circuits)", T, O, O, O, O, "Open",
     "Yes", "n.a.", "Yes", "Immediate under P = NP; Karp–Lipton 1980 for consequences",
     "Refuting it (NP ⊄ P/poly) proves P ≠ NP: the circuit-lower-bound route. Crypto worlds with non-uniform security would set it False."),
    ("L07", "Universal search finds SAT witnesses in polynomial time on satisfiable inputs", T, F, F, F, F, "Open",
     "Yes", "n.a.", "Yes", "Levin 1973 (universal search)",
     "Never halts on unsatisfiable inputs; the equivalence is for the search version."),
    ("L08", "PH = P", T, F, F, F, F, "Open",
     "Yes", "n.a.", "Yes", "Definition of PH", "PH = P iff P = NP."),
    ("L09", "Nested SAT, fixed instances, polynomially many levels, answer bits used as literals (P^NP) is in P",
     T, F, F, F, F, "Open", "Yes", "n.a.", "Yes", "Nested-SAT analysis (chat, 2026-10-28); NP ⊆ P^NP",
     "With negative occurrences allowed this problem is P^NP-complete."),
    ("L10", "Nested SAT where every answer bit occurs only positively stays in NP", T, T, T, T, T, "Theorem",
     "Yes", "n.a.", "Yes", "NP is closed under ∧, ∨ and monotone substitution",
     "B[a] is satisfiable iff B[0] is satisfiable, or A is satisfiable and B[1] is satisfiable."),
    ("L11", "Depth-k nested SAT whose inner formulas depend on outer variables (Σₖ) is in P, for each fixed k",
     T, F, F, F, F, "Open", "Yes", "n.a.", "Yes", "Σₖ ⊇ NP; PH collapses under P = NP",
     "Depth-k parameterized nesting is Σₖ-complete."),
    ("L12", "TQBF ∈ P (polynomial-depth parameterized nesting; PSPACE = P)", O, F, F, F, F, "Open",
     "Yes", "n.a.", "Yes", "TQBF is PSPACE-complete; PSPACE ⊇ NP",
     "Under P = NP the exponent compounds with depth (roughly n^(c^d)), so P = NP does not obviously give P = PSPACE. Mirror of L27."),
    ("L13", "SAT ∈ DTISP(nᶜ, n^o(1)) for some c < 2cos(π/7) ≈ 1.8019", F, F, F, F, F, "Refuted",
     "Unverified", "n.a.", "Unverified",
     "Williams 2008; Buss–Williams 2015 (eccc.weizmann.ac.il/report/2011/031)",
     "Constrains Algorithmica (SAT is not near-linear in tiny space) without contradicting it. 2cos(π/7) is the proven ceiling of alternation-trading proofs."),
    ("L14", "NEXP ⊄ ACC⁰", T, T, T, T, T, "Theorem",
     "Unverified", "Unverified", "Unverified", "Williams 2011 (CCC); JACM 2014",
     "Algorithmic method: circuit-SAT faster than brute force implies lower bounds. Commonly described as avoiding the relativization and natural-proofs barriers; tags not yet checked against the paper."),
    ("L15", "S₂E ⊄ SIZE[2ⁿ/n]", T, T, T, T, T, "Theorem",
     "Yes", "No", "Yes",
     "Chen–Hirahara–Ren 2023 (arxiv.org/abs/2309.12912); Li 2023 (arxiv.org/abs/2310.17762)",
     "Pigeonhole made explicit through range avoidance. The authors state the proofs relativize. S₂E is far above NP."),
    ("L16", "One-way functions exist", F, F, F, T, T, "Open",
     "n.a.", "n.a.", "n.a.", "Impagliazzo 1995; Liu–Pass 2020",
     "Liu–Pass: one-way functions exist iff Kᵗ is mildly hard on average."),
    ("L17", "Public-key encryption exists", F, F, F, F, T, "Open",
     "n.a.", "n.a.", "n.a.", "Impagliazzo 1995", "Defines Cryptomania."),
    ("L18", "Some NP problem is hard on average (distributional NP ⊄ AvgP)", F, F, T, T, T, "Open",
     "n.a.", "n.a.", "n.a.", "Impagliazzo 1995",
     "Heuristica is worst-case hard but average-case easy."),
    ("L19", "MCSP ∈ P (a P-natural property useful against P/poly exists)", T, O, O, F, F, "Open",
     "Unverified", "n.a.", "Unverified", "Razborov–Rudich 1997; Kabanets–Cai 2000",
     "One-way functions give pseudorandom functions, and a fast MCSP algorithm would distinguish them from random."),
    ("L20", "R(Kᵗ) ∈ P for every polynomial t", T, O, O, F, F, "Open",
     "Yes", "n.a.", "Yes", "Evaluation doc, Prop. 3.2; HILL 1999 (one-way functions give PRGs)",
     "A PRG's outputs have low Kᵗ, so deciding R(Kᵗ) breaks every PRG."),
    ("L21", "R(Kᵗ) is P-immune (Lemma B of the evaluated argument)", F, O, O, O, O, "Open",
     "Yes", "n.a.", "Yes", "Evaluation doc, Props. 3.2–3.3",
     "The unproven step of the 'Pseudorandom Trap' argument."),
    ("L22", "R(K) is immune (no infinite c.e. subset)", T, T, T, T, T, "Theorem",
     "Yes", "n.a.", "Yes", "Evaluation doc, Prop. 1.1", "Classical."),
    ("L23", "No Kolmogorov-random finite strings exist", F, F, F, F, F, "Refuted",
     "Yes", "n.a.", "Yes", "Evaluation doc, Fact 1",
     "At least 2ⁿ − 2ⁿ⁻ᶜ + 1 strings of length n are c-incompressible."),
    ("L24", "Chaitin: a consistent Σ₁-complete theory proves 'K(x) > L_T' for no x", T, T, T, T, T, "Theorem",
     "Yes", "n.a.", "n.a.", "Chaitin 1974; evaluation doc §7.4", "Limits proof, not existence."),
    ("L25", "NP-intermediate problems exist", F, T, T, T, T, "Open",
     "Yes", "n.a.", "Yes", "Ladner 1975", "Under P = NP every NP language is in P, so none are intermediate."),
    ("L26", "No sparse set is NP-complete (Karp reductions)", F, T, T, T, T, "Open",
     "Unverified", "n.a.", "Unverified", "Mahaney 1982", "Under P = NP the sparse set {1} is NP-complete."),
    ("L27", "P ≠ PSPACE", O, T, T, T, T, "Open",
     "Yes", "n.a.", "Yes", "PSPACE ⊇ NP", "Mirror of L12."),
    ("L28", "Every satisfiable formula A has a satisfying assignment x with Kt(x | A) = O(log n)", T, F, F, F, F, "Open",
     "Yes", "n.a.", "Yes", "Levin 1973 (universal search); SAT self-reducibility; chat 2026-10-28",
     "If P = NP, a search algorithm running in nᵏ steps outputs a solution, so Kt(x | A) ≤ k·log n + O(1). Conversely, universal search finds such a solution in polynomial time and rejects after the budget, deciding SAT."),
    ("L29", "Direct product for verifiable SAT search: if every randomized short program solves at most 1 − δ₀ of D_m in time m^k', then every short program solves r = C ln m independent blocks with probability ≤ 2e^(−γr)",
     T, T, T, T, T, "Theorem", "Yes", "n.a.", "Yes",
     "Impagliazzo–Jaiswal–Kabanets 2009 (weakly verifiable puzzles); CLAUDE DIRECTPRODUCT-0001, Thm 3R",
     "Randomized black-box reduction. The deterministic uniform version needs L30."),
    ("L30", "Lemma 2 of the direct-product note: a deterministic polynomial-time seed list hits every short program's dense success set for all but 1/m of any samplable distribution",
     T, O, O, O, O, "Open", "Yes", "n.a.", "Yes",
     "CLAUDE DIRECTPRODUCT-0001, Prop. 2 (embedding); Impagliazzo–Wigderson 1998",
     "Implies one-sided heuristic derandomization of RP over samplable distributions; IW98 gets only infinitely-often subexponential simulations from BPP ≠ EXP. If P = NP, approximate counting makes the list constructible. The note's proof is FALSIFIED/RETIRED."),
    ("L31", "Some samplable distribution on satisfiable formulas has SAT search hard on average for every polynomial-time randomized algorithm",
     F, O, O, T, T, "Open", "n.a.", "n.a.", "n.a.",
     "CLAUDE DIRECTPRODUCT-0001, Cor. 5; Impagliazzo 1995",
     "This is the direct-product note's hypothesis at every budget. Minicrypt/Cryptomania: inverting a one-way function as planted SAT. Heuristica is probably False via average-case search-to-decision; left Open until checked."),
    ("L32", "Portfolio collapse: one constant-size algorithm simulates every program of length ≤ b₀ + d·log N with an O(N^d) time factor, so common defeating instances at budget N^k follow from SAT-search lower bounds at time N^(k+d+o(1))",
     T, T, T, T, T, "Theorem", "Yes", "n.a.", "Yes",
     "CLAUDE DIRECTPRODUCT-0001, Prop. 4 and Cor. 5",
     "Shows the direct-product route to the UWI common-input statement is dominated: it needs only worst-case hardness and loses only d in the exponent."),
    ("L33", "T-PORT: SAT ∉ ∃^(log N + b₀) DTISP(N^c, N^o(1)) for some c > 1 (UWI portfolio lower bound in small space, decision form)",
     O, T, T, T, T, "Open", "n.a.", "n.a.", "n.a.",
     "CLAUDE DIRECTPRODUCT-0001 §8; CLAUDE TPORT-0001",
     "Decision form (an N-bit witness does not fit in small space). Alternation trading cannot reach it: see L34 (barrier) and L36. Collapse plus Williams gives only c < 0.80."),
    ("L34", "Barrier: no alternation-trading proof in system S (Williams Speedup Rules 1–2, portfolio slowdown leaving a residual of width d·M, free absorption, brute force) refutes SAT ∈ ∃^(d log N)DTS[N^c] when c ≥ 1 and c + d ≥ 2",
     T, T, T, T, T, "Theorem", "n.a.", "n.a.", "n.a.",
     "CLAUDE TPORT-0001, Thm 6 (potential argument)",
     "At d = 1 (UWI portfolio) nothing beyond the trivial c < 1; at d = 0 it is Williams' quadratic barrier. A statement about proofs, so true in every world."),
    ("L35", "For 0 ≤ d < 1 and c(c+d) < 2: SAT ∉ ∃^(d log N)DTISP(N^c, N^o(1)); computer-found proofs give more, e.g. (d,c) = (9/10, 21/20), (3/4, 57/50), (1/2, 261/200)",
     T, T, T, T, T, "Theorem", "Unverified", "n.a.", "Unverified",
     "CLAUDE TPORT-0001, Thm 4 and exact replay (verify_exact.py)",
     "Sublinear portfolios admit nontrivial bounds; d = 1 is exactly the threshold. Beats the collapse bound 2cos(π/7) − d for d ≥ 1/2."),
    ("L36", "The L34 barrier still holds when Skolemization (∀r∃z ≡ ∃(z_r)∀r, table merged into the previous block) is added to S",
     O, O, O, O, O, "Open", "n.a.", "n.a.", "n.a.",
     "CLAUDE TPORT-0001 §7",
     "COMPUTATIONAL: 0 of 47,938 proofs of length ≤ 18 beat c = 1 at d = 1; Skolemization never improved any exponent. Two natural potentials fail; proof open."),
    ("L37", "Asymptotic threshold: the best exponent c*(d) provable by the S rules satisfies 1 + (1−d)/3 ≤ c*(d) ≤ 1 + (1−d) on [0,1], and c*(1−ε) ≥ 1 + (29/50)ε for all small ε > 0",
     T, T, T, T, T, "Theorem", "n.a.", "n.a.", "n.a.",
     "CLAUDE TPORT-0002 (closed form; barrier; exact ε-polynomial certificate of a length-22 proof)",
     "So the provable gain over linear time is Θ(1 − d) and vanishes linearly at the UWI size. Exact cost match: one speedup round trip changes time by at least c(t−x) + dx − t. The limiting slope lies in [0.58, 1]; its value is open."),
    ("L38", "Every one-tape Turing machine, deterministic or nondeterministic, deciding 3-SAT (clause-list encoding) needs Ω(N²/log N) time on infinitely many lengths",
     T, T, T, T, T, "Theorem", "Unverified", "n.a.", "n.a.",
     "Owner's note (equality family F_{a,b}); CLAUDE ONETAPE-0001 Thm 1; Hennie 1965; Santhanam IPL 2001",
     "Crossing sequences. Tight for nondeterministic one-tape machines up to polylog (NTIME_1(SAT) = O(N² log² N)), so the method cannot separate determinism from nondeterminism."),
    ("L39", "Sequential-access portfolios: SAT needs T·S = Ω(N²/log N) on off-line machines with sequential input, for deterministic portfolios of up to 2^{Ω(N/log N)} programs and for on-the-fly nondeterminism",
     T, T, T, T, T, "Theorem", "Unverified", "n.a.", "n.a.",
     "CLAUDE ONETAPE-0001 Thm 3 and Cor 4",
     "So the UWI small-space portfolio statement (L33) holds with exponent up to 2 when input access is sequential; with random access, alternation trading cannot exceed 1 (L34). The difference is the input-access model."),
    ("L40", "SAT needs one-tape deterministic time N^(2+δ) for some δ > 0",
     O, T, T, T, T, "Open", "n.a.", "n.a.", "n.a.",
     "CLAUDE ONETAPE-0001 Prop 5 (Hartmanis–Stearns translation)",
     "Would imply a superlinear deterministic multitape lower bound for SAT, which is open. Crossing-sequence counting is capped at O(N²)."),
    ("L41", "Bridge(Res): SAT ∈ P ⟹ W̄_Res(N) ≤ poly(N), where W̄_R(N) = max over UNSAT F with |F| ≤ N of the minimum refutation size in R (best sequence free)",
     F, T, T, T, T, "Open", "n.a.", "n.a.", "n.a.",
     "CLAUDE BRIDGE-SQUEEZE-0001 Thm 2; Haken 1985 (W̄_Res superpolynomial unconditionally)",
     "Because W̄_Res is unconditionally superpolynomial, the bridge is false if P = NP and vacuously true otherwise. The same holds for every system with a known superpolynomial lower bound (tree-like and general resolution, cutting planes, polynomial calculus, bounded-depth Frege). A bridge for such a system is P ≠ NP restated."),
    ("L42", "Bridge(EF): SAT ∈ P ⟹ W̄_EF(N) ≤ poly(N) for Extended Frege (also for the project calculus R_mix341, which contains ER_2)",
     O, T, T, T, T, "Open", "n.a.", "n.a.", "n.a.",
     "CLAUDE BRIDGE-SQUEEZE-0001 §4; Cook 1975; LSPV-1 357 (true when some P-time SAT algorithm has a PV-provable rejection-soundness proof)",
     "Vacuous if P ≠ NP. Proving it outright means proving P = NP ⟹ EF p-bounded, which is open. Bridges move up under p-simulation (Lemma 1), so stronger systems have easier bridges."),
    ("L43", "LB(EF): W̄_EF(N) is superpolynomial (no polynomial-size Extended Frege refutations for some UNSAT family)",
     O, O, O, O, O, "Open", "n.a.", "n.a.", "n.a.",
     "Cook–Reckhow 1979; Krajíček 2019 (Proof Complexity, CUP)",
     "Not implied by P ≠ NP and not known to fail if P = NP. Together with L42 it would give P ≠ NP. This is the lower-bound half the boxed program needs for any system strong enough to have a non-trivial bridge."),
    ("L44", "NP ≠ coNP, equivalently W̄_R superpolynomial for every Cook–Reckhow system R",
     F, O, O, O, O, "Open", "n.a.", "n.a.", "n.a.",
     "Cook–Reckhow 1979",
     "This is what a lower bound on minimum derivation cost with free best sequence proves when it holds for all R. Free choice of sequence makes W̄_R a nondeterministic measure, so the all-R version is stronger than P ≠ NP."),
]

headers = ["ID", "Statement", "Algorithmica (P = NP)", "Heuristica", "Pessiland",
           "Minicrypt", "Cryptomania", "Known unconditionally", "Category (auto)",
           "Consistency check (auto)", "Known proof relativizes?", "Naturalizes?",
           "Algebrizes?", "Source / proof", "Notes"]
widths = [6, 46, 13, 11, 11, 11, 12, 13, 26, 24, 13, 12, 12, 40, 52]

wb = Workbook()

# ---------------- Read me ----------------
rm = wb.active
rm.title = "Read me"
rm["A1"] = "P vs NP world ledger"
rm["A1"].font = f_title
lines = [
    ("Purpose", "Each row is a statement S. Its status in each of Impagliazzo's five worlds sorts it into a category automatically."),
    ("Edit these", "Columns B–H and K–O on the Ledger sheet. Add a new statement by filling a new row; copy the two auto formulas (I, J) down from the row above."),
    ("Do not edit", "Columns I and J (grey). They are formulas."),
    ("World values", "True = S holds in that world; False = S fails there; Open = not determined by that world's definition."),
    ("Known unconditionally", "Theorem, Refuted or Open, as currently known in the literature."),
    ("Technique tags", "Yes / No / n.a. / Unverified, describing the known proof in the row. For non-theorems this is the derivation of the known world entries. Unverified means not yet checked against the primary paper."),
    ("Category: Theorem (win-win)", "True in every world."),
    ("Category: Equivalent to P = NP / P ≠ NP", "Decided exactly by P vs NP. A new form of the question, not progress."),
    ("Category: Half-win", "Forced in one camp, open in the other. Proving it in the open camp proves it outright; refuting it settles P vs NP."),
    ("Category: Implies P = NP / P ≠ NP (open)", "Proving S settles P vs NP."),
    ("Category: World separator", "Different values across the four P ≠ NP worlds. Separates worlds rather than deciding P vs NP."),
    ("Consistency check", "Flags CONFLICT when a world contradicts a known theorem. A genuine conflict would eliminate that world; in practice it almost always means an entry is wrong."),
    ("Caveat", "The five worlds are treated as an exhaustive split under fixed definitions (P = NP; else NP easy or hard on average; one-way functions; public-key encryption). Infinitely-often and non-uniform variants can fall between them, so 'True in every world' is a strong signal, not by itself a proof."),
    ("Sources", "Citations are from memory unless a URL is given; check titles and years before reuse. 'Evaluation doc' = Evaluation: the \"Pseudorandom Trap\" argument for P ≠ NP (Claude Doc, 2026-10-28); the propositions it cites are reproduced with proofs in " + REPORT + " (GitHub j15marti/pnp)."),
    ("Source of truth", "Seeded rows live in build_ledger.py next to this file. Prefer adding rows there and regenerating, so the .xlsx and world_ledger.csv stay in sync."),
]
r = 3
for k, v in lines:
    rm.cell(row=r, column=1, value=k).font = f_bold
    c = rm.cell(row=r, column=2, value=v)
    c.font = f_base
    c.alignment = wrap
    rm.cell(row=r, column=1).alignment = wrap
    r += 1
rm.column_dimensions["A"].width = 30
rm.column_dimensions["B"].width = 100

# ---------------- Worlds ----------------
ws_w = wb.create_sheet("Worlds")
wh = ["World", "Definition used here", "P vs NP"]
for j, h in enumerate(wh, 1):
    c = ws_w.cell(row=1, column=j, value=h)
    c.font = f_head
    c.fill = fill_head
    c.alignment = wrap
worlds = [
    ("Algorithmica", "P = NP. Every NP problem is solvable in polynomial time.", "P = NP"),
    ("Heuristica", "P ≠ NP, but every NP problem is easy on average over samplable distributions.", "P ≠ NP"),
    ("Pessiland", "Some NP problem is hard on average, but one-way functions do not exist.", "P ≠ NP"),
    ("Minicrypt", "One-way functions exist (private-key cryptography, PRGs), but public-key encryption does not.", "P ≠ NP"),
    ("Cryptomania", "Public-key encryption exists.", "P ≠ NP"),
]
for i, row in enumerate(worlds, 2):
    for j, v in enumerate(row, 1):
        c = ws_w.cell(row=i, column=j, value=v)
        c.font = f_base
        c.alignment = wrap
        c.border = border
ws_w.cell(row=8, column=1, value="Source: R. Impagliazzo, \"A personal view of average-case complexity,\" Structure in Complexity Theory, 1995.").font = f_small
ws_w.column_dimensions["A"].width = 16
ws_w.column_dimensions["B"].width = 80
ws_w.column_dimensions["C"].width = 10

# ---------------- Ledger ----------------
ws = wb.create_sheet("Ledger")
for j, h in enumerate(headers, 1):
    c = ws.cell(row=1, column=j, value=h)
    c.font = f_head
    c.fill = fill_head
    c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
    c.border = border
    ws.column_dimensions[get_column_letter(j)].width = widths[j - 1]
ws.row_dimensions[1].height = 32

def category_formula(r):
    nT = f'COUNTIF(D{r}:G{r},"True")'
    nF = f'COUNTIF(D{r}:G{r},"False")'
    return (
        f'=IF(COUNTA(C{r}:G{r})<5,"Fill all five worlds",'
        f'IF(C{r}="True",'
        f'IF({nT}=4,"Theorem (win-win)",'
        f'IF({nF}=4,"Equivalent to P = NP",'
        f'IF({nF}=0,"Half-win (true if P = NP)","World separator (true if P = NP)"))),'
        f'IF(C{r}="False",'
        f'IF({nF}=4,"Refuted in every world",'
        f'IF({nT}=4,"Equivalent to P ≠ NP",'
        f'IF(AND({nT}>0,{nF}>0),"World separator (implies P ≠ NP)","Implies P ≠ NP (open)"))),'
        f'IF(C{r}="Open",'
        f'IF({nF}=4,"Implies P = NP (open)",'
        f'IF({nT}=4,"Half-win (true if P ≠ NP)",'
        f'IF(AND({nT}>0,{nF}>0),"World separator (open if P = NP)","Undetermined by P vs NP"))),'
        f'"Check values"))))'
    )

def consistency_formula(r):
    allF = f'COUNTIF(C{r}:G{r},"False")'
    allT = f'COUNTIF(C{r}:G{r},"True")'
    return (
        f'=IF(H{r}="Theorem",IF({allF}>0,"CONFLICT: a world contradicts a theorem","OK"),'
        f'IF(H{r}="Refuted",IF({allT}>0,"CONFLICT: a world contradicts a theorem","OK"),'
        f'IF(AND({allT}=5,H{r}="Open"),"True in every world: check column H",'
        f'IF(AND({allF}=5,H{r}="Open"),"False in every world: check column H","OK"))))'
    )

for i, row in enumerate(rows, 2):
    (rid, stmt, a, h, p, m, cr, known, rel, nat, alg, src, notes) = row
    vals = [rid, stmt, a, h, p, m, cr, known, None, None, rel, nat, alg, src, notes]
    for j, v in enumerate(vals, 1):
        c = ws.cell(row=i, column=j, value=v)
        c.font = f_base
        c.border = border
        c.alignment = center if j in (1, 3, 4, 5, 6, 7, 8, 11, 12, 13) else wrap
    ws.cell(row=i, column=9, value=category_formula(i))
    ws.cell(row=i, column=10, value=consistency_formula(i))
    for j in (9, 10):
        c = ws.cell(row=i, column=j)
        c.font = f_base
        c.fill = fill_auto
        c.border = border
        c.alignment = wrap

last = len(rows) + 1
max_r = 200  # validation and formatting range allows growth

dv_world = DataValidation(type="list", formula1='"True,False,Open"', allow_blank=True)
dv_known = DataValidation(type="list", formula1='"Theorem,Refuted,Open"', allow_blank=True)
dv_tag = DataValidation(type="list", formula1='"Yes,No,n.a.,Unverified"', allow_blank=True)
for dv in (dv_world, dv_known, dv_tag):
    ws.add_data_validation(dv)
dv_world.add(f"C2:G{max_r}")
dv_known.add(f"H2:H{max_r}")
dv_tag.add(f"K2:M{max_r}")

green = PatternFill("solid", start_color="D9EAD3", end_color="D9EAD3")
red = PatternFill("solid", start_color="F4CCCC", end_color="F4CCCC")
grey = PatternFill("solid", start_color="F3F3F3", end_color="F3F3F3")
rng = f"C2:G{max_r}"
ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"True"'], fill=green))
ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"False"'], fill=red))
ws.conditional_formatting.add(rng, CellIsRule(operator="equal", formula=['"Open"'], fill=grey))
ws.conditional_formatting.add(
    f"J2:J{max_r}",
    FormulaRule(formula=[f'LEFT(J2,8)="CONFLICT"'], fill=PatternFill("solid", start_color="E06666", end_color="E06666"),
                font=Font(name=FONT, size=10, bold=True, color="FFFFFF")))

ws.freeze_panes = "C2"
ws.auto_filter.ref = f"A1:O{last}"

# ---------------- Summary ----------------
sm = wb.create_sheet("Summary")
sm["A1"] = "Summary"
sm["A1"].font = f_title
sm["A3"] = "Category"
sm["B3"] = "Rows"
for c in (sm["A3"], sm["B3"]):
    c.font = f_head
    c.fill = fill_head
cats = [
    "Theorem (win-win)",
    "Refuted in every world",
    "Equivalent to P = NP",
    "Equivalent to P ≠ NP",
    "Half-win (true if P = NP)",
    "Half-win (true if P ≠ NP)",
    "Implies P = NP (open)",
    "Implies P ≠ NP (open)",
    "World separator (true if P = NP)",
    "World separator (implies P ≠ NP)",
    "World separator (open if P = NP)",
    "Undetermined by P vs NP",
]
for k, cat in enumerate(cats, 4):
    sm.cell(row=k, column=1, value=cat).font = f_base
    c = sm.cell(row=k, column=2, value=f'=COUNTIF(Ledger!$I$2:$I${max_r},A{k})')
    c.font = f_base
    for col in (1, 2):
        sm.cell(row=k, column=col).border = border
tot = 4 + len(cats)
sm.cell(row=tot, column=1, value="Total statements").font = f_bold
sm.cell(row=tot, column=2, value=f'=COUNTA(Ledger!$A$2:$A${max_r})').font = f_bold
sm.cell(row=tot + 1, column=1, value="Rows flagged CONFLICT").font = f_bold
sm.cell(row=tot + 1, column=2, value=f'=COUNTIF(Ledger!$J$2:$J${max_r},"CONFLICT*")').font = f_bold
sm.cell(row=tot + 3, column=1, value="Best targets: half-wins whose open side would need a non-relativizing proof step.").font = f_small
sm.column_dimensions["A"].width = 38
sm.column_dimensions["B"].width = 10

wb.move_sheet("Ledger", offset=-2)  # Ledger first
wb.active = 0
wb.save(OUT)
print("saved", OUT, "rows", len(rows))


# ---------------- Plain-text copy (same rules as the formulas) ----------------
def classify(algorithmica, others):
    """Python mirror of the Category formula. others = 4 P != NP world values."""
    vals = [algorithmica] + list(others)
    if any(v not in (T, F, O) for v in vals):
        return "Fill all five worlds"
    n_t, n_f = others.count(T), others.count(F)
    if algorithmica == T:
        if n_t == 4:
            return "Theorem (win-win)"
        if n_f == 4:
            return "Equivalent to P = NP"
        return "Half-win (true if P = NP)" if n_f == 0 else "World separator (true if P = NP)"
    if algorithmica == F:
        if n_f == 4:
            return "Refuted in every world"
        if n_t == 4:
            return "Equivalent to P ≠ NP"
        return "World separator (implies P ≠ NP)" if (n_t > 0 and n_f > 0) else "Implies P ≠ NP (open)"
    if n_f == 4:
        return "Implies P = NP (open)"
    if n_t == 4:
        return "Half-win (true if P ≠ NP)"
    return "World separator (open if P = NP)" if (n_t > 0 and n_f > 0) else "Undetermined by P vs NP"


def consistency(known, worlds):
    """Python mirror of the Consistency formula. worlds = all five values."""
    if known == "Theorem" and F in worlds:
        return "CONFLICT: a world contradicts a theorem"
    if known == "Refuted" and T in worlds:
        return "CONFLICT: a world contradicts a theorem"
    if known == "Open" and worlds.count(T) == 5:
        return "True in every world: check column H"
    if known == "Open" and worlds.count(F) == 5:
        return "False in every world: check column H"
    return "OK"


with CSV_OUT.open("w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(headers)
    for row in rows:
        (rid, stmt, a, h, p, m, cr, known, rel, nat, alg, src, notes) = row
        w.writerow([rid, stmt, a, h, p, m, cr, known,
                    classify(a, [h, p, m, cr]), consistency(known, [a, h, p, m, cr]),
                    rel, nat, alg, src, notes])
print("saved", CSV_OUT)
