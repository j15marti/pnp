# ARC-ONEHOT-CHILD-SELECT253: five-role handoff
Date 2026-10-30 13:31 America/Los_Angeles. LSPV-1 formal proof lead.
Scientific control: UNIVERSAL-PARAMETERIZED-FLMV-REDIRECT1 and CONTRACT1. All five existing roles, schedules, and enabled/paused status are unchanged. P vs NP OPEN.

## One proved restricted no-go, independently review pending

Take even m>=4 and the original proper 3-CNF family
F_{m,h,b}=G_b AND [AND_{i=0}^{m-1} (ell_i OR a_i OR z)]
with exactly one positive x-occurrence ell_h=x and all ell_i=NOT x otherwise.
G_YES is empty, and G_NO consists of all eight signed clauses on three
independent variables. The source is SAT exactly when b=YES and is
uniformly easy. Original N=Theta(m log m) indexed fixed-width bits.

Pin x=0. The direct syntactically restricted ordinary SAT child is
G_b AND (a_h OR z), only O(log m) bits. Pin x=1. The other child retains
m-1 clauses of Theta(N) total bits. Any exact OR-join uses BOTH children
for source NO, while source YES may terminate after a YES answer.

Let P source sign probes be performed before the requested physical child
bit is specified, Q afterwards, with arbitrary adaptive deterministic
source reads, arbitrary nonlinear summary of acquired bits, and no free
source-dependent side channel. The same fixed physical bit, the LSB of
the retained variable ID, equals (h+3) mod 2. On an all-zero probe path
fewer than m/2 distinct source-sign probes leave a possible mark in
each parity class, so transcript indistinguishability gives

    P+Q >= m/2.

For output of the entire child, all m possible source positions must
be distinguishable, so aggregate P+Q >= m-1. Both are tight in the
declared bit-probe model. This generalizes the selected single-level
directory firewall of earlier ARC-SELECT-INDEX252 to arbitrary
adaptive source-sign-probe scheduling on this ONE-HOT family. It is
NOT a SAT lower bound, NOT a general data-structure lower bound, and
NOT an obstruction to global source-aware recognition, streaming,
compression, or source caching. A paid O(m)-probe pass storing h in
O(log m) bits supplies polylogarithmic future bit access.

## Reproducible both-label controls and measured work

Thirty parent cases: m in {4,6,8,10,12}, h in {0,m/2,m-1},
both SAT and UNSAT controls. Exact DP verified m/2 parity probes
and m-1 full-location probes, including 4095 subset states at m=12.
Source and both original cofactors were fully decided by a complete
UP-DPLL guest and checked by an independent parent decision. All
original signed clause occurrences received S/U and inversions;
pairwise SS,SU,US,UU were checked against exact variable-consistent
enumeration; global 0^n,1^n, complements, flips and explicit
source resolution chains were checked. The source-indexed compact
bit accessor reproduced every bit of the materialized short child.

For m=8,h=7, selected charged logical events:
SAT: baseline 227, cached two-child 255, stateless 407.
UNSAT: baseline 3147, cached two-child 4028, stateless 4180.
These are declared Python event-proxy counts, NOT FLMV TM steps or
writable-space bounds. The controller did not win on either control.
No industrial CDCL or native indexed-TM simulator was executed.

## Provenance

GitHub mathematical LaTeX:
research/agents/lspv-1/2026-10-30_1331_LSPV-1_ARC_ONEHOT_CHILD_SELECT253.tex
verified blob 8a129ba300a37393838d311dea2a469f4b305794.

GitHub Python:
research/agents/lspv-1/2026-10-30_1331_LSPV-1_ARC_ONEHOT_CHILD_SELECT253.py
verified blob cdcdb6c2d8a8280165369042489d8492e3eafcc4.

GitHub entire raw JSON:
research/agents/lspv-1/2026-10-30_1331_LSPV-1_ARC_ONEHOT_CHILD_SELECT253_raw.json
verified blob dc1aab66a060b31ea00db17794745f5363b451bf;
original local raw SHA-256 3f6a7a6045808e46b9269bba3a59ac92384704f53c9f8ddb0ebe0ceae37b2097.
The runnable PDF and complete ZIP are persisted separately under
/PNP Formal Proof Lead/ARC_ONEHOT_CHILD_SELECT253 in the Library
(the Library upload covered report source, code, raw JSON and ZIP).
Full GitHub readbacks were exact after normalizing source trailing newlines.
No claim of whole-repository CI or native machine execution.

## Role-addressed next steps

LSPV-1: independently audit the bit-probe quantifiers, especially allowing paid
preprocessing; prioritize the all-input both-label child correctness theorem.
LSPV-2: attempt genuine arbitrary-bit emitted strict22 final output
after intermediate sorting, with complete source-index rank/select and
a power-short child test, not just N^{1+o(1)} normalizing output.
LSPV-3: construct adversarial renaming/padding/COPY/DELAY and SAT/UNSAT
controllers that escape direct one-hot select; bill the escapes.
LSPV-4: audit exact FLMV indexed read-only input blank/out-of-range handling,
serial child buffering, far work address, source reads and retained peak space.
LSPV-5: referee no-source-dependent-advice premise, check all-input/compiler
quantifier remains OPEN and integrate only independently verified scope.

## Corpus reconciliation
Reviewed current root/AGENTS/CODEX/skill, 09:48 governance,
CONTRACT1, AFFINE-SMALLBIAS-DESCENT-GATE2 (restricted MCSP),
CONSTRUCTION-STRENGTHEN17, ARC-LINEAR22-SATURATION1,
ARC-SELECT-INDEX252, ARC-MATERIALIZE-GUARD253,
ARC-EXPONENT-DISCOVERY-FIREWALL224, LSPV-1 ARC-KRAFT252,
LSPV-2 VIRTUAL-SORT-ACCESS254 and LSPV-3 SAT-ONLY-SELECTOR256.
Original clause S/U remains an adversarial control, not the active route.
The root integration must preserve ownership regions. No universal ARC
compiler has been constructed. P=NP and P!=NP OPEN.

Primary literature: Fortnow-Lipton-van Melkebeek-Viglas,
Time-Space Lower Bounds for Satisfiability, JACM 2005,
https://lance.fortnow.com/papers/files/tst.pdf ;
Kurpicz, Engineering Compact Data Structures for Rank and Select Queries
on Bit Vectors, SPIRE 2022, https://doi.org/10.1007/978-3-031-20643-6_19.

END_OF_VERIFIED_HANDOFF::ARC_ONEHOT_CHILD_SELECT253::P_VS_NP_OPEN
