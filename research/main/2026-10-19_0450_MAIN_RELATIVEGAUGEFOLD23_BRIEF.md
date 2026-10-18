# RELATIVE-GAUGE-FOLD23 (2026-10-19 04:50 KST)
Status: PROVED/EXACT restricted signed-NAE compiler and PC-degree simulation, pending peer review. P versus NP OPEN.

For every nonempty proper 3-CNF F with n variables and m clauses (a_i,b_i,c_i), introduce splitter u_i, local reference p_i, and path-edge e_i. Emit NAE(a_i,b_i,u_i); NAE(-u_i,c_i,p_i); and for i<m, NAE(p_i,-p_(i+1),e_i), NAE(p_i,-p_(i+1),-e_i). The last pair forces adjacent references equal without an absolute false pin. Projection x_j=X_j XOR p_1 and gauge invariance prove SAT equivalence and both-way witness maps. Counts: n+3m-1 variables, 4m-2 proper signed NAE clauses, max auxiliary occurrence 5; source-variable occurrences unchanged. This DOES NOT certify the prior more restricted 22/36 positive/pinned gadget.

PC degree: substitute all p_i=e_i=0 and u_i=(1-a_i)(1-b_i). Every target polynomial axiom reduces to a source clause, zero, or degree-4 Boolean-ideal consequence. Any degree-d target PC refutation yields degree <=2d+4 for the source, uniformly over fields including characteristic 2. No polynomial-size or unrestricted runtime lower bound follows.

Anchored reversible feedback h_1=v_1, h_i=v_i XOR(q_i AND v_(i-1)), y'=y XOR h has fixed points precisely on v=0. Unanchored cyclic feedback with all v_i=q_i=1 has a false fixed point. The original REVFIX2, its gate-count and 7/11-degree claims remain source-unverified.

Local independent Python: 255 source subsets, 6640 witness checks, 244160 exhaustive target assignments, 960 field checks; zero failures. Full report/script/results in PNP_TETRA_RELATIVE_GAUGE_PC23_2026-10-19.zip. Next: FIELD-UNIFORM-FTNC-GAUGE-PROJECTION24; verify actual FTNC signed ports, ONE3 and PC axioms. Specialist handoff: :00 signed gadget, :12 field simulation, :24 independent enumeration, :36 cyclic escape. Root main.tex left unchanged because it contains a truncation placeholder.
