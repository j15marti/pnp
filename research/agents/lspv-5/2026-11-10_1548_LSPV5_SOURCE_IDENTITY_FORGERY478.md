+# LSPV-5/478: Original-source identity is not authenticated by the recovered /341 fixture verifier
+
+**2026-11-10 15:48 PST | Independent Proof Red Team, historical Route B | COMPUTATIONAL + PROVED/RESTRICTED | P versus NP OPEN**
+
+**Affected tracker nodes:** material new evidence for still-OPEN [P2-D1], with a necessary repair condition for still-OPEN [P2-C3]. [P2-B1] remains OPEN. [P2-B2]/B3 remain separate and OPEN.
+
+## IDEA -> SEARCH -> ITERATE
+
+**Target claim.** The pinned recovered LSPV-2/341 verifier binds every accepted SOURCE record to an independently authenticated original source and therefore can serve as the concrete source layer for a cost-sound abstraction.
+
+**Falsifiers stated before search.**
+
+1. Change the purported original-source identity/coordinates without a trusted digest and retain acceptance.
+2. Supply source rows only through the self-declared certificate object, with no separately authenticated source argument.
+3. Cross an AND3 or XOR parent-kind boundary and retain acceptance.
+4. Forge source identifiers or coordinates while leaving the accepted paid DAG and check count unchanged.
+
+The first, second and fourth falsifiers occurred. The third did not: this restricted checker does enforce the displayed factor/affine kinds for its AND3/XOR subset.
+
+## Governing reads and scope
+
+Read complete current root [proof1.txt](../../proof1.txt), [proof2.txt](../../proof2.txt), issue #3, AGENTS.md, CODEX.md, .codex/skills/pnp-research/SKILL.md, the 2026-11-09 16:24 FLMV handoff, LSPV-2/539-542, LSPV-3/549 and 551-554, LSPV-1/556 and LSPV-4/526 materials. In particular, [P2-L3-552] was independently rerun below rather than accepted from its report.
+
+The executable under attack is exactly the recovered SOURCE/AND3/XOR **fixture verifier**, Git blob `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`. It is not established to be the complete historical R_mix341 parser or checker. Nothing here authenticates or changes the historical grammar or weights.
+
+## Accepted hostile certificate
+
+Starting from the exact 197,515-byte seven-fixture baseline, the audit changed the first fixture as follows:
+
+- graph name `K4` -> `FORGED-K4-EXTERNAL-SOURCE`;
+- all 16 SOURCE identifiers were replaced by `forged-source-0`, ..., `forged-source-15`, with proof parents and deletion references changed consistently;
+- all 16 `pattern` coordinates were replaced by unrelated strings;
+- every three-literal array was cyclically reordered, changing source bytes while preserving its clause;
+- a top-level `claimedOriginalSourceDigest` equal to 64 zeroes was inserted.
+
+The unchanged original verifier accepted the 198,537-byte hostile packet with all **30,714** checks. Its SHA-256 is `1ca3baf09e7d673e20533e36e9218bdeadbdbc02c4965399b98a857e8dc8227c`.
+
+Two controls delimit the finding:
+
+- an unbound SOURCE parent was rejected;
+- a literal-sign mutation changing source semantics was rejected.
+
+Thus this is not a claim that the checker performs no semantic checking. It checks a self-contained parsed fixture, but does not bind that fixture to independent original-source bytes, a trusted hash, or authenticated external coordinates.
+
+## Static source-binding lemma
+
+Let the concrete acceptance relation implemented by the pinned verifier be
+
+$$
+A(B)=1
+$$
+
+for one supplied JSON byte string $B$. Static inspection and execution agree that:
+
+1. the command line accepts only the certificate/results JSON path;
+2. no independent CNF/source path or trusted source digest is supplied;
+3. SOURCE semantics are reconstructed from the certificate's own `clauses[*].literals`;
+4. `pattern`, graph name and the added digest field do not participate in source authentication.
+
+Therefore acceptance proves at most a predicate of the self-declared parsed object:
+
+$$
+A(B)=1 \Rightarrow \operatorname{InternalConsistent}(\operatorname{parse}(B)),
+$$
+
+not the required two-input statement
+
+$$
+A(F,B)=1 \Rightarrow \operatorname{Refutes}(F),
+$$
+
+for separately authenticated original source $F$. A coordinated alpha-renaming of identifiers and clause-literal permutation remains internally consistent, so it cannot establish byte identity or provenance of $F$.
+
+The inserted all-zero digest is not claimed to be historical syntax. It is a hostile demonstration that unknown JSON fields are ignored; the stronger absence result comes from the one-input interface and lack of any trusted digest comparison.
+
+## Abstract-interpretation consequence
+
+A source-authenticated concrete state needs at least
+
+$$
+c=(F_{\rm raw},h_F,P_{\rm raw},\pi,\Gamma,D,w),
+$$
+
+where $F_{\rm raw}$ is external source bytes, $h_F$ is a trusted binding or an equivalent exact occurrence relation, $P_{\rm raw}$ is certificate bytes, $\pi$ maps SOURCE leaves to authenticated occurrences of $F$, $Gamma$ records contexts, $D$ is the full shared DAG and $w$ carries fixed native charges.
+
+Any abstraction $alpha$ that retains only the self-declared parsed fixture erases $h_F$ and $pi$. Its concretization $gamma$ then contains states over multiple external sources, including sources not named by the intended theorem. It cannot satisfy both completed-refutation preservation and source authentication merely because the recovered checker accepts.
+
+The minimal repaired condition is:
+
+$$
+\forall c\;(\operatorname{Accept}_{\rm native}(c) \Rightarrow
+\operatorname{SourceBind}(F_{\rm raw},h_F,\pi,c)).
+$$
+
+For cost-sound negative-proof transfer, one must additionally prove every legal native concrete step is included and
+
+$$
+\operatorname{cost}^{\#}(\alpha(P))\leq \operatorname{cost}_R(P).
+$$
+
+This audit proves the pinned subset verifier does not supply the SourceBind premise. It does not prove that no different authenticated full historical checker can do so.
+
+## Correct CEGAR treatment
+
+The hostile path was concretely replayed in the unchanged verifier. It is therefore genuine in that verifier's observed accepted language and cannot be removed as a spurious abstract path. A CEGAR refinement may separate:
+
+- `OPERATIONAL_ACCEPT_RECOVERED_FIXTURE`; and
+- `SOURCE_BOUND_CERTIFIED_UNSAT`.
+
+It may not silently replace the observed parser with a duplicate-key rejecting, canonical-ID, external-source-bound or typed reference checker. Those are explicit repairs or proposed calculi until historical authority and a cost-preserving simulation are proved.
+
+## Independent review of LSPV-3/552
+
+The exact published producer, checker and base packet were refetched and their Git blobs checked:
+
+- producer `4081022e8a3841d79f751a3d3a7a10decbb026da`;
+- checker `fcb7d4ced8f922de14c0bda16263a8cc7853e8e0`;
+- base packet `706947c767361e7c979b8208677eb983d33838f4`.
+
+The original Node/V8 runner independently reproduced six accepted SAT-source packets at $t=0,\ldots,5$ with check totals
+
+$$
+2272,2416,2560,2704,2848,2992,
+$$
+
+and all 30 typed-support/charge/source/table/sink controls rejected. The separately implemented Python graph/SAT audit passed all six witnesses and reproduced the first possible restricted cubic size $V=12,E=18,m=48,q=47$. Rerun SHA-256 values were `beb2c7bf...76feba` for the native ledger and `6fc3923e...bd1a4` for the independent Python ledger.
+
+This confirms [P2-L3-552] at its stated restricted scope. It is stronger semantic-unsoundness evidence for the recovered fixture checker, but the malformed string charge/support path is not thereby a legal intended R_mix341 inference.
+
+## Literature and repository search
+
+- Cook and Reckhow (JSL 44, 1979, DOI 10.2307/2273702) give the proof-system/verifiability framework; they do not authenticate this project parser or transfer a lower bound to the full mixed calculus.
+- Cousot and Cousot (POPL 1977, DOI 10.1145/512950.512973) provide the abstraction/fixpoint framework; soundness still requires the concrete relation and abstraction polarity to be proved.
+- `cake_lpr` explicitly takes a DIMACS formula file and a separate proof file, a relevant source-binding interface control, but it recognizes LPR rather than R_mix341.
+- FRAT-XOR/XLRUP has a separately specified CNF/XOR/BNN input grammar and a different checker. It is not evidence for the missing historical parser.
+- Change-aware reads were unchanged for `konard/p-vs-np` README blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95`, proof-status blob `93b77ed3d8fe456f81c690035f45f07910a247f2`, `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`, `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`, and `tanyongkiam/cake_lpr/README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`. None supplies the full historical R_mix341 accepted-byte language.
+
+## Resource ledger
+
+| Phase | Evidence/work | Time/space statement |
+|---|---|---|
+| governing reads | full trackers, policies, handoffs, peer reports and issue | network/read cost charged to this research run; not proof cost |
+| parse/baseline | 197,515-byte baseline, 9,360-byte verifier | ordinary host parse; no FLMV-machine claim |
+| mutation | 16 source IDs, 16 parent/deletion updates, 16 literal rotations, 16 pattern replacements | linear in this finite packet |
+| verification | baseline, hostile packet, two controls | 0.55 s illustrative host wall time for one rerun; 30,714 accepted checks |
+| stored evidence | 3,167-byte script, 1,415-byte raw ledger, 198,537-byte accepted packet | explicit bytes; Node peak RSS was not measured |
+| peer replay | six positives, 30 negatives plus independent Python witnesses | separate execution; not charged to $W_R$ |
+| publication | report, code, raw, packet, handoff, tracker and issue readback | repository I/O charged to research workflow |
+
+No inference from certificate cardinality, assertion count, proof-DAG work or host RSS to algorithmic live work space is made.
+
+## Status and precise gap
+
+**Actual advance:** an independently reproduced, checker-accepted source-identity/provenance forgery shows that the recovered /341 fixture verifier cannot by itself instantiate the original-source-authenticated concrete semantics required by [P2-D1] or the SourceBind premise required by [P2-C3].
+
+**Remaining gap:** locate and authenticate the complete historical R_mix341 byte grammar and checker covering SOURCE, Resolution, AND3, GF(2), LOCAL-CONVERT, paid DEF/facets, freshness, exported/private wires, contexts, branching/discharge, joins, weakening and deletions; then prove whole-DAG concrete-step inclusion, completed-refutation preservation and cost nonincrease. Only after those can [P2-B1] be attacked over every legal rule. [P2-B2]/B3 remain separate. P versus NP remains OPEN.
+
