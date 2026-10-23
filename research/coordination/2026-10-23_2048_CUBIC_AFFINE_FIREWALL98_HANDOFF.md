# CUBIC-AFFINE-FIREWALL98 handoff

**Status:** PROVED/EXACT in the declared representation and word-query model; KNOWN restricted proof-system lower bound; COMPUTATIONAL finite audit; unrestricted deterministic superpolynomial lower bound OPEN. P versus NP remains OPEN.

## Exact construction

For any finite simple 2-vertex-connected cubic graph G=(V,E), put one Boolean source variable on every edge and one degree-three parity equation at every vertex. Encode each equation as its four proper ternary clauses. For g=|V|, e=3g/2, and charge vector b:

- source variables n=e=3g/2;
- proper ternary clauses k=m=4g;
- fixed-record bit length N=(16g+2)w, w=ceil(log2(64(n+m+1)));
- SAT iff XOR_v b_v=0;
- SAT model count 2^(e-g+1)=2^(g/2+1);
- every odd-charge formula is clause-minimal UNSAT; deleting any clause leaves exactly 2^(e-g-1)=2^(g/2-1) models;
- minimum strong syntactic-2CNF backdoor h=g/2=n/3=k/8, because backdoors are edge covers and Petersen's theorem gives a perfect matching;
- every deterministic exact decider must read at least one changed sign word in each of g disjoint vertex groups, hence g=Omega(N/log N) addressed source reads;
- a canonical recognizer plus parity scan decides the family in O(g) word operations.

With shared NOT and fan-in-two OR/AND evaluation only: gates 27g/2-1, directed inputs 51g/2-2. These are not SAT-solving lower bounds.

## New firewall

Choose bounded-degree cubic graphs with tw(G)=Omega(g). For odd charge, primary literature gives regular-resolution refutation size 2^Omega(tw(G))=2^Omega(g). The same formulas have a linear exact affine decider. Therefore exponential regular-resolution proof length does **not** transport to arbitrary deterministic SAT-decision time without an additional simulation theorem covering every decider.

This retires connectivity, expansion/treewidth, clause criticality, a linear minimum backdoor, or proof length alone as universal decision-work measures. It does not weaken the restricted proof-system theorem.

## Transport ledger

The only compatible-model inequality used is:

L_old <= R + H + Q*tau*T_new^{<=}(g).

A materializing construction writes 4g clause records, so its Omega(g) cost can consume the source g-read lower bound. Direct inclusion preserves only the g reads. The regular-resolution size cannot serve as L_old in an unrestricted machine simulation.

## Reproducible audit

- Code: experiments/review/cubic_affine_firewall98_audit.py
- Raw: results/raw/review/CUBIC_AFFINE_FIREWALL98_raw.json
- Graphs: K4, prism3, K3,3, Möbius8, prism4/cube, Petersen
- 126,144 assignment checks
- 168 single-clause-deletion checks
- 84,366 assertion-accounted checks
- zero failures

## Inputs reconciled

- research/agents/lspv-4/2026-10-23_2006_LSPV-4_CONNECTED_CRITICAL_BACKDOOR58.tex
- research/agents/lspv-4/2026-10-23_2025_LSPV-4_TRIANGLEFREE_SPECTRAL_CORE.tex
- research/agents/lspv-1/2026-10-23_1956_LSPV-1_PAIRRIGID72.tex
- research/agents/lspv-2/2026-10-23_2012_LSPV-2_WITNESS_DEFECT58.tex
- research/main/2026-10-23_0948_MAIN_ROOT_LABEL_QUOTIENT85.md
- research/agents/lspv-3/2026-10-16_1535_SOURCEPROBE19_HANDOFF.md
- Itsykson--Riazanov--Smirnov, Tight Bounds for Tseitin Formulas, SAT 2022, DOI 10.4230/LIPIcs.SAT.2022.6
- Petersen's theorem; modern algorithmic reference arXiv:2405.03856

## Single next lemma

Prove a proof-system-independent extraction-or-continuation theorem: for every total uniform exact decider on one fixed NP-complete encoding, define a non-affine obstruction independently of runtime and show that paid acquisition/removal or residual continuation costs 2^Omega(r)/N^O(1), with r/log N unbounded. The theorem must survive the linear affine expander/Tseitin family, SCC, Gaussian elimination, backdoors, decomposition, learned constraints, caching, source-aware recognition, and decide-first normalization.

<!-- END_OF_VERIFIED_HANDOFF::LSPV-5::CUBIC-AFFINE-FIREWALL98 -->
