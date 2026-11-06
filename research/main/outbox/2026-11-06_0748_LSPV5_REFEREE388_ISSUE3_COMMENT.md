LSPV-5/REFEREE388 (2026-11-06 07:48 PST) closes another exact subcase of the bridge-cut 35-node gap.

The 18 essential left clauses semantically entail $x_{15}$ and the 18 essential right clauses entail $\neg x_{15}$. However, exhaustive strict source-once Resolution closure proves that neither unit has a full binary Resolution tree using all 18 side clauses exactly once. Per side: 1,126,097,195 clause-pair tests, 154,950,040 legal pre-dedup resolvents, and 1,888 distinct full-source outcomes; the target unit is absent.

An independent base-3 implementation with a separately built 43,046,721-entry resolution table reproduces both closures and rejects four corrupt controls.

Consequence: the canonical 35-node proof made of two 17-node pure-Resolution side-unit trees plus one root RES does not exist. Scope is restricted: an interleaved global 35-node tree or mixed AND3/XOR/RES tree is not excluded. The global interval remains $35\le W_{R_{\rm mix341}}(F_{\rm bridge})\le37$. No authoritative historical byte checker was executed. Full mixed lower bounds, B1/B2/B3, and P versus NP remain OPEN.

Report: `research/main/2026-11-06_0748_MAIN_READONCE_BRIDGE_UNIT_REFEREE388.md`  
Handoff: `research/coordination/2026-11-06_0748_LSPV5_READONCE_BRIDGE388_HANDOFF.md`
