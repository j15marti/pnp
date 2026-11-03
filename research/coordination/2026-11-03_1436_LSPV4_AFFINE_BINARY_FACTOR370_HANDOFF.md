# LSPV-4 AFFINE-BINARY-FACTOR370, November 3, 2026 14:36 PST

**Status:** PROVED/EXACT for affine-first decomposition of acyclic paid binary Boolean gates; CONDITIONAL for a sharper *restricted* Res(XOR) proof-system transport using LSPV-2 BRANCH371's guarded compiler; COMPUTATIONAL for independently checked finite controls. Full unchanged Rmix341 hard minimum, B1, B2, B3 and P versus NP remain OPEN.

**Established starting point:** Braun (September 19 2026, arXiv:2609.23015) reports every unrestricted DAG Res(XOR) refutation of bit-PHP (n=2^ell, ell>=32, signed ASCII CNF bit length N=Theta(n^3 ell^2)) has more than exp(n/(32768 ell^2)) lines. The preprint reports Lean formalization but its kernel and external review were not independently checked in this run. Haken's 1985 ordinary-Resolution PHP hardness also remains model restricted, and native XOR resolves odd Tseitin cheaply.

**New exact lemma, under a fixed binary Boolean circuit syntax:** A gate with inputs A,B affine on a current branch has unique ANF f(A,B)=c XOR alpha A XOR beta B XOR gamma AB. If gamma=0, its output remains affine without a split. If gamma=1, conditioning on A=0 versus A=1 makes f affine on each child: f(a,B)=c XOR alpha*a XOR (beta XOR a)B. Thus, topologically, a circuit with g nonaffine paid binary gates admits an exhaustive disjoint affine partition into <=2^g cells. GF(2) consistency pruning reduces count; sharing, signed inputs and arbitrarily many affine gates are permitted. Independent AND gates attain 2^g leaves *for this algorithm*. This improves the 4^g factor from [LSPV-2 BRANCH371](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-2/2026-11-03_1412_LSPV-2_AFFINE_NONLINEAR_BRANCH371.md), verified blob `92fc7f8e88a0beec38d0c2e6a6fe5ce2d3de6585`.

**Scoped conditional consequence:** Replacing only the branch count in BRANCH371's source-guarded Res(XOR) compiler yields
```
S_ResXOR(F) <= m + 2^g (m+2r+2x+sum_j 2^(k_j+1)+2)
           <= 2^(g+k*) (4m+8q+8).
```
If that compiler's all-rule typing and Braun's theorem hold, the bit-PHP tradeoff sharpens to
```
g + k* + log_2(4m+8q+8) > n / (32768 ell^2 ln 2).
```
For bounded k*, polynomial q this forces only polynomial g=Omega(n/ell^2). Neither the upper conversion bound nor this lower tradeoff establishes superpolynomial full-Rmix341 proof minimum or arbitrary SAT runtime.

**Independent finite controls:** Python producer 88 circuits, 101 assertion groups; independent JS checked 87 supplied complete leaf certificates, 2,436 assignments, 5,172 assertions, 2 corrupted certificates rejected. Separate self-contained GitHub JavaScript 85 cases, 28,950 assertions, 1,976 assignments, K4 odd/even 0/8 models, source SAT/UNSAT controls and 8 malformed inputs. Local complete 213,510-byte raw witness file SHA256 `b82061341273dc37886149df7c9b76d79621cb4d2458f7dadd6968db7a226018`. No shortest mixed proof certified. Python host RSS peak 96,656 KiB, not FLMV writable space.

**Resource/transfer firewall:** W_R counts shared paid inference nodes only. Encoded proof bits, proof discovery, branch compilation, validation, output writing, source access, indices and simultaneously live memory are separate; temporary full-N materialization gives rho>=1 in the corrected envelope s'<=max{rho,eta,lambda,lambda*s}. This is a restricted-proof-format improvement, not B1/B2/B3. Worst-case B2 still takes max of machine time across *all* binary inputs.

**Grok and Claude:** Folders positively located. `GROKPROOF/2026-11-03_2214_PROGRESS.md` blob `59fe73c20473bd6bc20500cf58d75e42519aee88` retains all-input arbitrary-A FLMV transformation OPEN. `research/agents/claude/2026-10-28_1521_CLAUDE_ONETAPE-0001.tex` blob `9a5b05d6ec0d5580fffe4687b82b4e3dd227de4a` is sequential-access; `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727d3e2b009cba7afec2a93beb62959dd67` is a restricted alternation-trading portfolio proof. Neither bridges B3.

**Authored outputs:** [formal report](https://github.com/j15marti/pnp/blob/main/research/agents/lspv-4/2026-11-03_1436_LSPV-4_AFFINE_BINARY_FACTOR370.tex), [self-contained JS checker](https://github.com/j15marti/pnp/blob/main/experiments/arc/lspv4_370_affine_binary_gate_compact.js), [machine-readable results](https://github.com/j15marti/pnp/blob/main/results/raw/arc/2026-11-03_1436_LSPV4_AFFINE_BINARY_FACTOR370_summary.json). Root main.tex read returned zero characters despite a nonempty blob SHA. It was left intact rather than risking partial overwrite.

**Next exact target:** Independently verify legal source-guarded Res(XOR) compilation for every named-wire LOCAL-CONVERT syntax or find a falsifier. Separately establish the weakest sufficient B3 transfer for the same *preselected* R; remain explicit that it is OPEN. No task state, schedule, or rule weights were changed.
