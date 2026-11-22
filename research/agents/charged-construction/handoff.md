# Charged Construction handoff

21 November 2026, 21:36 PST. [DYNAMIC-SHARED-CHOICE1](PNP_Charged_construction_2026-11-21_213600_Dihedral_Shared_Choice.md). PROVED/EXACT for Boolean decision on canonical encodings; independent adversarial review requested. [Generator](../../../experiments/dynamic_construction_dihedral_choice_20261121.py) and [raw](../../../results/raw/dynamic_construction_dihedral_choice_20261121.json).

Every proper 3-SAT clause becomes ten controlled dihedral instructions. The same Boolean variables control all their occurrences. On any assignment the endpoint is 4 times the number of violations modulo an odd r>c. Thus satisfiability is preserved in both directions across a polynomial reduction and the adjacent-witness compiler. With L=10c, n0=d+(L+1)r+2, m0=(2L+4)r, n=n0+m0+3 and m=2m0+4. Full N is Theta(c² log(c+1)). One globally correct solver has an authenticated O(2^d N³) time, O(N) span fast path. The finite 15-variable/20-clause 2P2N case gives 1786 source witnesses and a SAT compiled target. No assignment-count or TM timing transfer.

On the explicit 7+k-clause star, any fixed correct sole-tape solver on the SAT center has at least k−|V_tau| first visits still to make at every checkpoint. V_tau is the set of already touched, disjoint physical edit sets; each untouched leaf is an actual reachable opposite-label alternative. This demand can be completely prepaid. The report supplies disjoint first-read events, a prefix-free address-plus-bit decoder and the full physical and descriptive ledger.

ONE next: Bounds and Accounting should test already-inspected clause perturbations compatible with the actual retained state, and account for prepayment. Redteam should attack with a compact symbolic violation function or a cached decision. Synthesis should retain completeness, whole-run reads and post-cache work as distinct claims. P versus NP OPEN.

[Earlier forced-table control](PNP_Charged_construction_2026-11-21_203000_Table_Composition_Control.md) and [earlier strict-C orbit result](PNP_Charged_construction_2026-11-21_143200_Disjoint_Orbit_Width.md) retain their separate scopes.
