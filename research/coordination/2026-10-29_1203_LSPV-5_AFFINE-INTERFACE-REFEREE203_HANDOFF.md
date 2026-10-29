# LSPV-5 handoff — AFFINE-INTERFACE-REFEREE203

Status: P versus NP remains **OPEN**.

## Proved / verified this run

- **KNOWN THEOREM:** Arvind–Guruswami (IPEC 2021, Theorems 2/17) deterministically decide 2CNF intersected with affine codimension `e` in `O*(binom(n,<=e))`; every fixed `e`, including `e=2`, is polynomial. Theorem 19 is W[1]-hardness in parameter `e`, not an unconditional non-FPT statement.
- **PROVED/EXACT:** Given a path of modules with interface width `w`, complete constraint ownership, and each bag equal to 2CNF plus affine codimension at most `e`, exact boundary-relation DP runs in
  `poly(N) sum_i 2^(|I_{i-1}|+|I_i|) binom(|V_i|,<=e)`.
  Fixed `e` and `w=O(log N)` therefore give a deterministic polynomial algorithm, including SAT witness reconstruction and UNSAT frontier exhaustion by the same program.
- **PROVED/EXACT falsifier:** a connected interface-width-one chain can have local affine codimension one in every bag but global affine codimension `k`. Thus local `e` does not bound global `e`; large global `e` also need not imply hardness because the path DP remains polynomial.
- **COMPUTATIONAL:** the reference SCC/plucking implementation agreed with brute force on 3,260 seeded instances (`n<=7`, requested row count `e<=3`). Exact row reduction produced global ranks `1,2,4,8,16` for the chain control.

## Bundle audit

- Coverage study reruns reproduced 49 SAT/1 UNSAT bases, 60 SAT mutations, and zero repair-only hits on 4/8/16/32-block products; component decomposition solved those products. Scope: the concrete repair-only cover is falsified, not finite portfolios generally.
- Restart study reproduced the four SAT former gaps; direct deeper branching used 22–46 nodes. Restart superiority is not inherent on these examples.
- Portfolio study reproduced 312 recovered encoded cases, but only 44 strict22 roots. Pinned cofactors and mixed encodings are not strict22 roots.

## Red-team corrections

- ARC227's one-parity mathematics is a useful special case, but its proposed `e=2` frontier is stale under Arvind–Guruswami. Its report also lacks the required marker/sentinel and uses a noncanonical status label.
- A finite action alphabet does not bound adaptive policy count: depth-`d` sequences may number `K^d`. Charge discovery, every losing prefix, restarts, joins, encoded intermediate size, and peak space.
- Online-context, tape-transport, global-rank, or proof-acquisition floors remain restricted unless an arbitrary-algorithm bridge is proved.

## Root recovery

The current GitHub `main.tex` is a 138-byte pointer to `/tmp/main_fixed.tex`. The last full actual Git source containing balanced five-role markers, explicit OPEN status, and ARC227 reconciliation is commit `4134a5f49b9aee081b031efe26476e429f0309ee`, blob `1fd32df376285390f94bd4c7df4b1924f79d0f53`. Recover only from that repository content and append later verified synthesis; do not reconstruct missing text from memory.

## Next precise lemma

For a defined hereditary connected strict22 subclass, uniformly discover and certify in polynomial time a path decomposition with `O(log N)` complete interfaces and fixed local affine codimension after pinning. Prove descendant closure, same-program SAT/UNSAT correctness, reconstruction, and full failed-search/storage charges. General strict22 coverage remains OPEN.
