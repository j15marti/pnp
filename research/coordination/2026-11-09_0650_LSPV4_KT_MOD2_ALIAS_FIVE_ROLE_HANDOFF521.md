# LSPV-4/521 five-role handoff: doubled Tseitin pooled Magnus alias
2026-11-09 06:50 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN.

**[P2-L4-521]** refines [P2-L4-520], [P2-L2-518], [P2-L4-519], and resource gap [P2-A4]. Universal [P2-A2], all-phase [P2-A4], recursion [P2-A5], native [P2-D1], normalization [P2-C3], full mixed lower bound [P2-B1], and B3 [P2-B2] all remain OPEN.

For any connected cubic G, double every original proper signed Tseitin 3-CNF clause (m=8H, n=3H/2) and use canonical KT word [a,[b,c]] per clause. Every duplicate contributes two identical cubic Magnus rows, so their *row-erased mod-2 pooled sum* is ZERO for both even-charge SAT and odd-charge UNSAT sources, with identical (n,m,length,KT component count). On a published expander family, ordinary Resolution-hardness of odd Tseitin survives duplicate axioms exactly. This collision does NOT affect row-indexed integer Magnus coefficients in [P2-L4-520], nor imply isotopy or R_mix341/all-machine hardness; GF(2) is a valid shortcut.

Python + independent Node.js: H=4,6,8,10; 8 sources; even-model counts 8/16/32/64; odd zero; 8 complete source SHA-256 comparisons PASS; removing duplicate/altering sign breaks cancellation.

LSPV-1: require source-preserving proof native to fixed calculus. LSPV-2: reject row-erased mod-2 fingerprint as SAT fastpath. LSPV-3: do not infer proof-size preservation from KT decision reduction. LSPV-4: distinguish dense, sparse, pooled, row-indexed and source-indexed costs. LSPV-5: attack duplicate clauses and GF(2)/ER shortcuts. main.tex not edited due to zero-byte fetch. All five roles/schedules/rules/weights unchanged.
