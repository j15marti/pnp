# LSPV-5/426 handoff — externally bound recovered canonical packets

**Affected tracker IDs:** `[P2-D1]`, `[P2-B2]`, `[P2-L3-490]`, `[P2-L5-425]`, new `[P2-L5-426]`. `proof1.txt` unchanged.

**PROVED-RESTRICTED.** Let $B(F,P)$ be the distinct two-input adapter that (i) runs the recovered SOURCE/AND3/XOR checker on packet $P$, (ii) compares the separately parsed external CNF's signed-clause multiset, including duplicate multiplicity, with the packet's internal source clauses, and (iii) checks the declared variable bound. Let $C$ be `[P2-L5-425]`'s canonicalizer. Then

$$B(F,P)\Longrightarrow B(F,C(P)).$$

$C$ preserves graph edges and source signed literals exactly, while its packet length is $O(\sum V(E+W+1))$; the externally bound pair therefore has length $|F|$ plus that polynomial term. No digest, semantic oracle, new inference or equisatisfiable replacement is used.

Node independently reconstructed binder/canonicalizer and executed the exact preserved checker: 1,408 checks, 352 expected rejections, seven fixtures, 63 accepted bindings, and all 324 equal-length satisfiable indispensable-clause substitutions rejected. Independent Python: 1,335 checks, 345 rejections, the same 324 mutants, and exact 71,853-byte/SHA agreement. Duplicate multiplicity, source/literal permutations, malformed header/count/termination, metadata, affine ghosts and ID aliases were controlled.

Scope firewall: this is a distinct adapter around a recovered post-JSON-parse SOURCE/AND3/XOR checker, not the authoritative historical full grammar. `[P2-L5-413]` still shows that recovered bytes reject RES/LOCAL-CONVERT/DEF; no branch/discharge syntax exists. The result neither constructs proofs nor proves full compact witnesses, B1/B2/B3, all-rule hardness or P versus NP.

Next LSPV-1/3: reuse this composition only for the recovered sublanguage. Next LSPV-5: require authenticated native syntax and context identity before extending $C$ to omitted rules. `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]` remain OPEN.
