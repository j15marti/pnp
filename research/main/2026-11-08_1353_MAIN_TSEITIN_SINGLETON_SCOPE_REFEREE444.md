# LSPV-5/444 independent red-team report: singleton scope repair for [P2-L3-510]

**Timestamp:** 2026-11-08 13:53 PST, America/Los_Angeles  
**Role:** LSPV-5 Independent Proof Red Team, Route B primary  
**Status:** PROVED/RESTRICTED scope counterexample and repair; COMPUTATIONAL exhaustive controls; historical mixed transfer, B1/B2/B3 and P versus NP OPEN.

## Actual advance

The universal wording of [P2-L3-510] needs one boundary repair. For the connected loopless graph \(G=(\{v\},\varnothing)\) with odd charge \(\chi_v=1\),

- \(d_v=0\);
- \(G-v\) has \(c_v=0\) components;
- the natural CNF for the false equation \(0=1\) is the single empty clause;
- deleting that clause leaves the empty, satisfiable CNF.

Consequently the report's intermediate assertions \(1\le c_v\le d_v\) and “the local parity equation has \(2^{d_v-1}\) clauses” are false/undefined as integer clause counts at this boundary. The final count nevertheless extends correctly under the natural convention:

\[
M_v=2^{d_v-c_v}=2^0=1.
\]

**Repair.** State the generic encoding/count proof for connected loopless graphs with at least two vertices (equivalently here, every vertex has positive degree), or separately define the degree-zero parity CNF. For \(|V|\ge2\), connectedness gives \(d_v\ge1\); \(G-v\) is nonempty so \(c_v\ge1\), and every component contains a neighbor of \(v\), giving \(c_v\le d_v\). The published cubic corollary and the source-ancestry corollary remain unchanged.

This is a scope repair, not a refutation of the articulation formula, not a lower bound for the full historical \(R_{mix341}\), and not progress on B3.

## IDEA -> SEARCH -> ITERATE

### Initial idea and falsifiers

Initial hypothesis: any claimed historical normalization using a Resolution-derived clause as an AND3/LOCAL-CONVERT input still lacks a native byte-level port; semantic equivalence alone cannot authorize the cross-type edge.

Predeclared falsifiers:

1. the original historical production explicitly defines the coercion;
2. an authoritative accepted trace exercises it;
3. a rule-by-rule simulation avoids the disputed edge;
4. the newest peer explicitly confines its result to a distinct calculus.

Falsifier 4 succeeded. [P2-L3-510] expressly limits its lower bound to a sound, conservative, source-explicit, at-most-binary-premise, positive-unit-weight calculus and says it is not a complete historical \(R_{mix341}\) minimum. It therefore does not use or authenticate the disputed historical port. The revised audit tested the strongest remaining universal phrase, “any finite connected loopless graph,” and found the degree-zero singleton boundary above.

### Continuity actually read

- complete current `proof1.txt`, initially blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`;
- complete current `proof2.txt`, after the concurrent LSPV-4/502 publication blob `ec1bcf4ee51581801841ac44a08fd6701a91dd2f`;
- issue #3 current last page through LSPV-4/502 comment `6727635172`;
- governing historical handoff at commit `4e29ed7646f484707767acb6e63ec5f38afd98a8`, file blob `033b54b87b7cbe94912af5cf67daa52859143a07`;
- `AGENTS.md` blob `19656af102604d5f0a721d548cf2e4e72a063561`, `CODEX.md` blob `754999f50de93cdb693ed37bc8110d31e9e698ef`, and `.codex/skills/pnp-research/SKILL.md` blob `b8df83a7b0b1428f349b0e02ce1387d979e8db7f`;
- historical native declaration `research/agents/lspv-2/2026-11-02_1216_LSPV-2_MIXED_TSEITIN_MIN_DAG341.tex` blob `c87acd11d32ccfc3b7acd3667ef11daeb60079cb` and LOCAL-CONVERT addendum blob `bbcdad9a487203f160d1009235de6bec7322a2a2`;
- peer [P2-L3-510] report blob `cc0cbad880424170a2355eab98730d1cee18e6a7`, published replay blob `467ff11e94247d9162043ae7e11208c732a42517`, raw blob `b589ed6817e91b617f5b8db1a63e87cdfcb2be1a`, and handoff blob `828149b6f841f03eb34cb9caddcec39e224cb730`;
- LSPV-1/514 report blob `3d8d60a31d9e98c061bf3212cb03c0b84ade2265`, LSPV-4/502 report blob `acac437441905dad52761631d979e8ba18f8781e`, and prior LSPV-5/443;
- actual Grok file `GROKPROOF/2026-11-08_1130_PROGRESS.md` blob `6942a99f176e996e9542f0386b7aa7fe2ce89e70` and Claude `research/agents/claude/world-ledger/README.md` blob `de75a371ce3143a4495e6892df7fb04794a6b708`.

The repository preflight script was run in the transient workspace. Its local-checkout omissions were expected because this environment uses the GitHub connector rather than a full checkout; every governing file above was read from its actual repository object. No access failure was disguised as review.

### Research and repository search

Primary sources actually opened:

- Urquhart, “Hard examples for resolution,” JACM 34(1), 1987, DOI `10.1145/7531.8928`: exponential ordinary Resolution lower bounds for Tseitin formulas from expanders, while the formulas have polynomial proofs in a stronger standard axiomatic system.
- Ben-Sasson and Wigderson, “Short Proofs Are Narrow—Resolution Made Simple,” JACM 48(2), 2001, DOI `10.1145/375827.375835`: Definition 4.1, Lemma 4.2, Theorem 4.4 and Corollary 4.5 were read from the paper. Theorem 4.4 gives width at least graph expansion; Corollary 4.5 gives exponential ordinary Resolution size for connected 3-regular expanders.
- Haken, “The intractability of resolution,” TCS 39, 1985, DOI `10.1016/0304-3975(85)90144-6`: exponential ordinary Resolution hardness for pigeonhole formulas; its abstract explicitly contrasts polynomial Extended Resolution proofs.
- Cook, “A short proof of the pigeon hole principle using extended resolution,” SIGACT News 8(4), 1976, pp. 28–32: mandatory stronger-system shortcut control.

The exact articulation count in [P2-L3-510] was not located as a peer-reviewed theorem in this search. Its cited 2-connected predecessor is an informal 2024 CS Stack Exchange argument by Emil Jeřábek; the project proof and independent replay carry the present restricted result. No novelty priority is inferred.

Google-branded search was not separately available. Public scholarly web search and direct paper/PDF access were available and used.

Required change-aware repository review:

- `konard/p-vs-np` at `ecedd2b45f1c524d85c00b2da27a9c140025550c`, `scripts/proof_status.json` blob `93b77ed3d8fe456f81c690035f45f07910a247f2`: formal slices and explicit residual-key counterexamples, not the missing mixed-calculus transfer.
- `blkph0x/p-vs-np-proof-research` at `7dedc73f758dfbdc072e7aa29dfc08505761ebd5`, `METHOD_INDEX.md` blob `18d693ea71dfa433370eb7afbebc3106e32f03e5`: scoped method ledger, no P-versus-NP resolution.
- `meelgroup/frat-xor/format.md` blob `986a21aa92b62f844ef1fce852193142c41b2b1f`: a distinct FRAT/XLRUP XOR format and checker trust boundary, not historical \(R_{mix341}\).
- `tanyongkiam/cake_lpr/README.md` blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`: verified LPR checker artifact, not a minimum-proof or B3 theorem.
- `peitl/short-proof/README.md` blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab`: bounded exact Resolution optimizer, not a full mixed-calculus optimum.
- `openai/math/README.md` blob `cc5b0a03bca6c742f045d683b6647a6f44ef2cae`: explicitly research artifacts at different verification stages, not automatic theorem authority.

### Iteration and independent challenge

The peer's published `lspv3_510_articulation_source_replay.py` was fetched from blob `467ff11e94247d9162043ae7e11208c732a42517` and replayed successfully: 12 cases, 448 clause deletions, 422 satisfying witnesses, and zero assertion failures.

The new independent program enumerates every labeled connected simple graph on 1–5 vertices, every odd charge vector, and every local wrong-parity pattern. It compares:

1. the component balance criterion;
2. an independent GF(2) elimination solver;
3. for \(n\le4\), exhaustive edge-assignment search.

After correcting a discovered back-substitution-order bug in the new audit code, all comparisons passed:

- 772 connected graphs;
- 11,971 graph/odd-charge cases;
- 173,517 deleted-clause checks;
- 146,225 satisfiable deletions;
- 2,637 independent brute-force cross-checks.

For every tested vertex the satisfiable deletion count equalled \(2^{d_v-c_v}\). The singleton alone triggers the universal proof-text boundary. The finite experiment does not prove the all-graph theorem; the symbolic singleton argument and the positive-degree repair are the rigorous parts.

## Established-family ledger

| Family | Exact encoding and size | Published theorem/model | Known legal shortcuts/controls | Remaining transfer |
| --- | --- | --- | --- | --- |
| Odd-charge cubic Tseitin on connected 3-regular \(G=(V,E)\), \(|V|=h\) | Variable \(x_e\) per edge, so \(n=3h/2\). At each \(v\), include one strict 3-clause \(C(v,z)=\bigvee_{e\ni v}x_e^{1-z_e}\) for each of the four local assignments \(z\) with \(\oplus z_e\ne\chi_v\). Total \(4h\) clauses; encoded bit length depends on the fixed binary/DIMACS convention, typically \(O(h\log h)\), and is not silently identified with \(h\). | KNOWN/PROVED-RESTRICTED: Ben-Sasson–Wigderson Theorem 4.4 gives ordinary Resolution width at least expansion; Corollary 4.5/Urquhart gives \(2^{\Omega(h)}\) size for 3-regular connected expanders. This is general shared-DAG ordinary Resolution with its stated rules, not all algorithms or full \(R_{mix341}\). | Polynomial Gaussian elimination over GF(2); source-explicit SOURCE/AND3/XOR constructions; extension-variable/stronger-system proofs; branching/search methods must be charged and scope-correct. These are upper-bound controls, not excluded shortcuts. | Authenticate every historical mixed rule and port, then prove a lower-bound-preserving transfer against all legal Resolution/AND3/GF(2)/LOCAL-CONVERT/DEF/shared-DAG derivations. Still OPEN. |
| Articulation generalization [P2-L3-510] | General parity CNF has \(2^{d_v-1}\) local clauses only for \(d_v\ge1\); degree zero needs the explicit empty-clause convention. | PROVED/RESTRICTED project theorem: \(M_v=2^{d_v-c_v}\) after the boundary repair; source-ancestry \(q\ge M-1\) only in the stated conservative binary-premise source-explicit calculus. | Sharing/reconvergence already allowed and distinct nodes counted once; GF(2) is an explicit shortcut control. | Same historical-calculus transfer and B3 gaps remain OPEN. |

Certified UNSAT, proof-size hardness, and empirical solver difficulty remain distinct. Odd total charge certifies UNSAT. Urquhart/Ben-Sasson–Wigderson prove proof-size hardness only for ordinary Resolution. This run makes no empirical general-solver hardness claim.

## Branching/shared-DAG audit

The [P2-L3-510] ancestry proof is compatible with shared DAGs: a contradiction node depending on \(M\) indispensable source leaves in an acyclic at-most-binary-premise graph has at least \(M-1\) paid internal nodes, and shared nodes are counted once. This is an AND-dependency lower bound, not an OR search cost. It does not add case-split, discharge, or weakening rules to historical \(R_{mix341}\); nor does it authorize branch-local conclusions outside their assumptions.

For the singleton, \(M=1\) makes \(q\ge0\) vacuous. That is consistent, not a counterexample to the ancestry lemma. No branching certificate or historical checker trace was needed for this boundary correction.

## Resource ledger

- **Logical nodes:** no new historical proof node rule; the finite audit enumerates deletion instances only.
- **Evidence bits/output:** published Python source blob `be6b2c84b9ef45b4849cf9afd5a1e902bcf87a5c`; raw JSON blob `28fda4b99c1c983fc81a39c20332254e0f99e747`.
- **Construction/search:** exhaustive generation of all labeled simple graphs through five vertices and all odd charges/local wrong patterns.
- **Verification:** GF(2) elimination on every deletion, plus brute-force assignments through four vertices; peer script replayed separately.
- **Measured run:** 173,517 deletion checks in about 1.5 seconds with approximately 8 MiB reported peak RSS in the transient Python process. These hosted measurements are not FLMV transition or space bounds.
- **Reads/parsing:** complete tracker reads, cited GitHub blobs, issue last page, primary paper/PDF reads and repository source reads were charged as research work.
- **Publication:** code/raw artifact commit is `c6a274e4a0ae0ef0f2b0bbf224bcb49afad76172`; report/handoff/tracker/manuscript commits and complete readbacks are recorded in the finalization receipt.
- **Caches/retrieval/recomputation/failed policy:** one failed first GF(2) back-substitution run was retained in the ledger and repaired; one concurrent branch-head lease conflict was detected and safely rebased before artifact publication.

No claim is made that the finite audit satisfies the Route A same-machine exponent contract.

## Tracker decision and remaining gap

Material update: add `[P2-L5-444]` to `proof2.txt`, refining `[P2-L3-510]`, `[P2-D3]`, and the evidence boundary under `[P2-D1]`. `proof1.txt` has no material change. The status of `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, `[P2-B2]`, `[P2-A2]`, and `[P2-A5]` remains OPEN.

**Precise remaining gap:** authenticate the exact historical \(R_{mix341}\) byte grammar and every cross-type port, then either prove a lower-bound-preserving transfer from an established hard 3-CNF family against every legal mixed branching/shared derivation or exhibit the strongest legal shortcut. Separately, prove a noncircular same-calculus B3 implication. P versus NP remains OPEN.

## Publication/readback receipt

- Code/raw artifact commit: `c6a274e4a0ae0ef0f2b0bbf224bcb49afad76172`.
- Initial report/handoff commit: `639b8ef15afa86b9145a2f529a54bcfe5b679186`.
- Exact prewrite outbox commit: `b303ccbacacb42a0199f13e2387995fe11fb1f52`.
- Material tracker/manuscript commit: `11ef952a61ae977fc1d7df98839ad20e2e65d52b`.
- `proof1.txt` complete readback: unchanged blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 characters.
- `proof2.txt` complete readback: prewrite blob `ec1bcf4ee51581801841ac44a08fd6701a91dd2f`, final blob `cc44d51199d43ab6acd51df0b15fb58d184aea7e`, 512,830 characters, exactly one `[P2-L5-444]` occurrence.
- `main.tex` complete blob readback: prewrite blob `3af7fe65a235acccf2ccd7e0389282bead1f105b`, final blob `ab8d1e3e13b8cceac8d0277fdded3cc90b08e5c4`, 1,779,162 characters, one REFEREE444 occurrence, and exact prefix/suffix equality outside the pre-existing LSPV-5 ownership markers.
- Artifact readback: code blob `be6b2c84b9ef45b4849cf9afd5a1e902bcf87a5c`, raw blob `28fda4b99c1c983fc81a39c20332254e0f99e747`, handoff blob `c30f639c3b2aed739c72b3ad5c990b8445f6572f`.
- Issue #3 comment `6727725843` was posted and read back with affected ID `[P2-L5-444]` and material commit `11ef952a61ae977fc1d7df98839ad20e2e65d52b` present.

Historical \(R_{mix341}\) grammar/weights, all roles, IDs, titles, schedules, enabled states and the two-Route-A/three-Route-B allocation were not changed. P versus NP remains OPEN.
