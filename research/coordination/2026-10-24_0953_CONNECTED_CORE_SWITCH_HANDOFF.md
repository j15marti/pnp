# CONNECTED-CORE-SWITCH handoff

Role 2 follow-up to HALL-SWITCH70. Standalone report verified at `research/agents/lspv-2/2026-10-24_0953_LSPV-2_CONNECTED_CORE_SWITCH.tex`, commit `5782603743040277c6f65c9f60b6ef59612c1f86`, blob `8d89353d212591cac45bb34053de860e2370ebc8`.

The supplied original U198/264 and the two-sign neighbor V are both connected strict signed exact-(2,2), with identical unsigned supports, zero complementary pairs and no initial degree-two pivot. Hall clause matching fails by 264>198 for BOTH labels.

New evidence: generated a fresh 537-node UNSAT proof (534 local refutation nodes plus 3 core nodes) and verified it with a separately implemented literal-list checker. This run does not rely on importing U's old truth label. The six-module projection itself is prior DOECKER-CORE-CERT61 work, not a new theorem. All 30 allowed local rows and 6 forbidden rows were checked.

Adaptive policy: parse and charge failed sufficient shortcut tests, try 128 DPLL nodes, switch only upon observed budget exhaustion to verified local boundary learning. U uses 128+1038+3=1169 search nodes; direct baseline is UNKNOWN after its 10000-node cap. V finishes in104 nodes before the switch. Mandatory projection worsens V to963+119=1082 nodes. No label is provided to the policy; failed searches, source acquisition, verification and representation switching count.

Connected growing controls: t blocks with n=198t,m=264t; cyclically move the source-1 occurrence in balancing clause254 to the next block. SAT: all blocks V. UNSAT: block0 U, remaining blocks V. Exact sign quotas and connectedness are preserved; labels differ in only2 sign fields. Tested t=1,2,4,8,16,32. IMPORTANT: UNSAT retains an unchanged254-clause core, so connected growth is NOT hardness amplification.

526 recorded checks pass, including120 independently brute-forced small controls (39 SAT,81 UNSAT) and a deliberately corrupted proof. Full source, generator, separate checker, certificate and raw data are in the conversation package; do not assume another runtime can access its local paths. No automation was created, changed or resumed. Root main.tex was not modified in this follow-up.

Next target: connected exact-(2,2) opposite-label instances without that fixed core and without freely supplied boundary metadata. Allow adaptive propagation/SCC, affine methods, matching/factors, learning, source rereading and alternate representations. A finite policy menu is not all-decider coverage. The measured node counts are algorithm-specific, not runtime lower bounds. P versus NP remains OPEN.