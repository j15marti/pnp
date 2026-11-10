+# LSPV-5/478 five-role handoff: recovered fixture checker does not bind an external source
+
+**2026-11-10 15:48 PST | Independent Proof Red Team, Route B | COMPUTATIONAL + PROVED/RESTRICTED | P versus NP OPEN**
+
+## Material evidence for still-OPEN P2-D1 and P2-C3
+
+The unchanged pinned recovered /341 SOURCE/AND3/XOR fixture verifier (blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`) accepted a coordinated source-identity mutation with all 30,714 checks:
+
+- graph/source name changed;
+- every SOURCE ID changed and every proof/deletion reference updated consistently;
+- every ignored pattern/coordinate replaced;
+- every three-literal array cyclically reordered;
+- a false all-zero `claimedOriginalSourceDigest` added.
+
+Accepted packet SHA-256: `1ca3baf09e7d673e20533e36e9218bdeadbdbc02c4965399b98a857e8dc8227c`. Unbound-parent and semantic-sign-change controls reject.
+
+This proves the recovered checker validates a self-contained semantic fixture, not a certificate bound to separately authenticated original source bytes/hash/coordinates. It is a genuine accepted path, so CEGAR cannot call it spurious. It is not a proof that the full historical R_mix341 calculus is unsound, and it is not a legal shortcut in an intended sound calculus.
+
+## Independent peer reproduction
+
+LSPV-3/552 was independently rerun from the exact published producer/checker/base blobs. Six SAT-source packets accepted with 2272, 2416, 2560, 2704, 2848 and 2992 checks; all 30 negative controls rejected. Independent Python verified all six SAT witnesses and the restricted first size $V=12,E=18,m=48,q=47$. This confirms [P2-L3-552] only at its declared recovered-checker scope.
+
+## Required abstract repair
+
+Keep these goal predicates separate:
+
+- `OPERATIONAL_ACCEPT_RECOVERED_FIXTURE`;
+- `SOURCE_BOUND_CERTIFIED_UNSAT`.
+
+A usable concrete state must carry external source bytes $F$, a trusted binding $h_F$ (or exact authenticated occurrence relation), SOURCE-leaf map $pi$, raw proof bytes, full typed shared DAG, contexts and fixed charges. Prove
+
+$$
+\operatorname{Accept}_{\rm native}(c)\Rightarrow\operatorname{SourceBind}(F,h_F,\pi,c)
+$$
+
+before using acceptance as semantic bottom. Then prove complete native-step inclusion, completed-refutation preservation and
+
+$$
+\operatorname{cost}^{\#}(\alpha(P))\leq\operatorname{cost}_R(P).
+$$
+
+## Role routing
+
+- **LSPV-1:** preserve P2-D1 -> P2-C3 -> P2-B1 quantifiers; keep P2-B2/B3 separate.
+- **LSPV-2:** test source-occurrence bijection /542 against raw-byte aliases, duplicates and independent source hashes; do not call REF-539 historical.
+- **LSPV-3:** locate authoritative full grammar/checker; prove source-binding theorem for every native source form before semantic abstraction.
+- **LSPV-4:** charge raw source/certificate hashing, reads, parsing, storage/recomputation and peak writable space separately from logical $W_R$.
+- **LSPV-5:** continue hostile accepted-byte replay, especially SOURCE aliases, LOCAL-CONVERT ports, DEF facets, contexts/discharge and cross-branch provenance.
+
+No roles, schedules, timezones, Route A/B labels, native rules or historical weights changed.
+
