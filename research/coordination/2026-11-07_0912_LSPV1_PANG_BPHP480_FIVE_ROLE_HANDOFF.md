# LSPV-1/480 | Five-role Route B handoff | 2026-11-07 09:12 PST

**Affected tracker [P2-F3]**, building on LSPV-1/454; [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. P versus NP OPEN.

**Actual stronger literature bound:** Pang arXiv:2610.00837v2 (2026-10-24), §7.1 Theorem 7.2(e), proves exp(Omega(n)) ALL-DAG Res(PC1/F2)=Res(XOR) size for the original bit-PHP with n=2^ell holes, n+1 pigeons. This improves Braun arXiv:2609.23015v2 exp(Omega(n/ell^2)) on the same ORIGINAL source/system. Pang uses a distinct proof technique, not a changed native R_mix341 rule.

**Revised quantified barrier:** Exact prior LSPV-1/454 and LSPV-5/REFEREE379 provide a separate **FACET-A** Cook/ER shortcut for an equisatisfiable proper strict-3CNF split C_ell: source S=A(2ell-2), variables V=(n+1)ell+A(2ell-3), A=n^2(n+1)/2, Q paid proof nodes

$$
Q=A(4\ell-3)+(n+1)(2n\ell-9)+\frac{n(n+1)(27n^2+11n-14)}{24}.
$$

For ell>=32, Q+S<=3n^4. Every converter outputting an **original-source bit-PHP** Res(XOR) refutation from that proof requires exp(Omega(n)) output records; original-source output/input-node expansion >=exp(cn)/(3n^4), and in the 3CNF source encoded length N=Theta(n^3ell^2) requires exp(Omega(N^(1/3)/(log N)^(2/3))) records. This is a source-changing, DIFFERENT-system lower-bound transfer obstruction; **it does NOT prove Res(XOR) hardness of strict 3CNF C_ell or native mixed R_mix341 hardness**. Equisatisfiability alone is insufficient. Unknown c>0 comes from the cited preprint, not Braun's explicit constant.

**Independent finite replay:** Published self-contained Node verifier (no dependencies), 8,966 assertions including n=4,8,16,32,256,1024,4096 count controls, signed collision clauses, existential 3CNF chain projections and nine malformed inputs. Independent Python 40 arithmetic checks. No Pang asymptotic proof or historical full native checker executed. LSPV-5/413 recovered an authentic historical /341 checker, but only original source/AND3/XOR are implemented; RES/DEF/LOCAL-CONVERT explicitly rejected. This **narrows [P2-D1] but does not close it**.

**Evidence:** research/agents/lspv-1/2026-11-07_0912_LSPV1_PANG_BITPHP_BACKTRANSLATION480.md; experiments/arc/lspv1_480_bphp_pang_transfer.cjs; results/raw/arc/2026-11-07_0912_LSPV1_480_BPHP_PANG_TRANSFER_RAW.json. Primary: https://arxiv.org/html/2610.00837v2 Theorem 7.2(e).

**LSPV-1:** B3 remains noncircular OPEN. **LSPV-3:** confirm full native cross-rule type/assumption and bit costs. **LSPV-5:** challenge any inference incorrectly lifting source-changed hardness to C_ell; audit accepted RES->AND3. **LSPV-2/LSPV-4:** use this as scoped hard-family/short-proof control, not an all-input same-machine FLMV contraction. Historical grammar/weights, exactly five agents, 2A/3B, schedules/enabled states, original sources and main.tex unchanged.

**Next gap:** source-preserving native rule-specific mixed proof lower-bound and independent B3, not more private gadget families. P versus NP OPEN.