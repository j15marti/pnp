# LSPV-3/446: complete four-facet shared proof-DAG normalization

**2026-11-06 04:38 PST. Route B. PROVED/RESTRICTED, COMPUTATIONAL.** Historical R_mix341 and B3 OPEN.

## Hypothesis, falsifiers, revision
Hypothesis: the two-paid-Resolution reconstruction of conventional binary-AND facets proved in /445 can translate every *given* nested signed-AND2 plus Resolution shared refutation, through the final empty clause, with overhead 2 paid RES per gate. Falsifiers: wrong signed facet or pivot; broken shared-DAG source ancestry; degenerate or unowned gate in the complete Cook peer trace; historical prohibition of facet selectors. A complete independent proof-DAG replay rules out the first three **within explicitly declared FACET4**. The fourth, historical exact accepted-byte grammar, remains OPEN. A local control corrected an initially too-strong statement that all emitted nodes must be final ancestors: the upper bound need not be exact for every certificate.

## Exact theorem
FACET-A has D paid globally fresh, distinct-underlying-input signed-AND2 owners z=a AND b with three conventional selectable defining clauses, followed by R paid ordinary oriented RES nodes. FACET4 instead exposes the four truth-table forbidden-row owner facets T00=(a OR b OR NOT z), T01=(a OR NOT b OR NOT z), T10=(NOT a OR b OR NOT z), T11=(NOT a OR NOT b OR z). A **paid RES on b** between T00,T01 derives (NOT z OR a); a **paid RES on a** between T00,T10 derives (NOT z OR b); T11 is the third conventional facet. Inductively replay every original RES with identical clauses, source IDs, owner scope, recombination and final contradiction. Both normalized outputs are globally exact (not merely source-model equivalent), each has a paid provenance path, and shared nodes are counted once.

$$
W_{\mathrm{FACET4}}(C(\pi))\le 3D+R.
$$

This is a *given-proof* syntactic simulation and a polynomial evidence-bit bound when original bytes are charged. No SAT decision-to-proof existence is proved, no arbitrary mixed AND3/GF(2)/LOCAL/branching simulation is asserted, and FACET4 has **not been authenticated as historical R_mix341**.

## Established-family ledger
Cubic odd Tseitin has 3h/2 edge bits and four proper ternary clauses per vertex. Urquhart 1987 shows exp(Omega(h)) ordinary shared-DAG Resolution hardness on appropriate cubic expanders; /341 has a 4h-1 AND3/GF(2) mixed shortcut, so no full mixed lower bound. Chvatal-Szemeredi 1988 random signed 8n-clause proper 3-CNF has exponential ordinary Resolution hardness with high probability; Pang arXiv:2610.00837v2 reports further restricted Res(PC) bounds in a recent preprint, not ER. Braun bit-PHP has n=2^ell holes, n+1 pigeons and M=n*binom(n+1,2) width-2ell collision clauses; arXiv:2609.23015v2 proves exp(n/(32768ell^2)) DAG Res(XOR) hardness for ell>=32 without extension variables. Its standard private-chain strict-3 encoding has S=M(2ell-2) clauses and (n+1)ell+M(2ell-3) variables. Equisatisfiability alone does **not** transfer that lower bound. Cook extended Resolution remains a required shortcut control.

## Independent complete proof replay
Peer full source: results/raw/review/2026-11-05_2253_LSPV5_FULL_COOK_FACETA379.json, Git blob cbf6b243d3697cc775801ac26a052b0622d3e9ef, 741690 UTF8 bytes. Fresh independent V8 replay read the entire GitHub content, reconstructed each source clause, each owner, each signed facet, all oriented pivots and the final empty-clause ancestor union. For ell=2, 80 strict-3 clauses, D=60, R=560, original 620 paid, extra 120 RES, new **740 paid**, ideal span 20. For ell=3, 1152 clauses, D=444, R=7905, original 8349 paid, extra 888, new **9237 paid**, ideal span 54. All original sources and both normalized nodes of every owner are final ancestors in these two instances. Original strict-3 source SHA256s independently recomputed from the prior local /440 archive match: 13361aa6164d76373ac8d4b4b6935f05257bb99266441f3405cfeecb653da6a6 (ell2) and 27f97b3a3c906b2858769ad9e9d691dfd95002852c5f99febf01e21f11c3bd9d (ell3). These are finite valid conditional upper witnesses, not global minima or a direct test of Braun's ell>=32 statement.

A separate comprehensive local Node verifier, preserved in LSPV3_446_FACET4_FULL_DAG_NORMALIZATION_REPRO.zip, verified a tiny original-source UNSAT proof and rejected 9 of 9 corruptions, including pivot, spoofed source hash and changed genuine SAT source. Emitted work=7 but only 6 final paid ancestors on this control. Its observed 0.06 s and 26992 KiB peak RSS cover only the tiny local control; full peer network transfer into the local runtime failed, so full-peer physical runtimes/peak space are **not claimed**. The GitHub compact script runs independently on the existing peer JSON in a clone; no historical native checker was executed.

For B original explicit proof bits, reindexing finite owner/reference IDs and producing two RES records per DEF adds O(D log(B+D+2)) bits, with charged parsing, source hashing, construction, output and verification. Depth 20 and 54 assumes unlimited ideal processors; actual retention, references, recomputation, schedules and all-phase peak memory are separate physical costs.

## Project, literature and repository checks
Read original 2026-11-02 /341 grammar blob c87acd11d32ccfc3b7acd3667ef11daeb60079cb, governance handoff, issue #3, peer REFEREE379/382/383/384, actual Grok REWIRE and Claude TPORT files. Both mandatory external repositories were inspected: konard/p-vs-np finite-machine model in README and proofs/complexity; blkph0x/p-vs-np-proof-research bounded projection and affine recognition reviews. FRAT-XOR format and CakeML XLRUP checker, cake_lpr November 1 transition, short-proof, ABC, openai/math ExecCNFNodeSearchCosts.lean were inspected. No external source supplies the original mixed owner-facet accepted-byte syntax. General web literature was searched; Google-branded access unavailable.

Root main.tex returned SHA3392567ec9141e247b541e46462efd536fb0b1c6 but zero readable bytes and was NOT edited. Five existing task identities and 2 Route A/3 Route B allocations, schedules and historical weights preserved.

**Actual advance:** restricted complete 3D+R shared signed-gate proofwise simulation with full source and empty-clause replay; **OPEN:** exact historical rule interface, all-rule mixed lower bound, noncircular same-R B3, P versus NP.
