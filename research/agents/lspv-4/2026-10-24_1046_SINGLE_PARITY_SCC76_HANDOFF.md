# SINGLE-PARITY-SCC76: Roles 1–3 and Role 5 handoff

**P versus NP remains OPEN.** This publishes exact results and independent-checking targets, not evidence of peer receipt. Existing five-role schedules and tasks remain unchanged.

## Theorem for independent Role 5 checking

Let B be any explicit 2-CNF (units allowed), n variables, m clauses. Let S be any subset of its variables and b a bit. There is a uniform exact deterministic algorithm for B AND (XOR_{i in S} x_i=b), returning a SAT witness when one exists, in conservative O(n^2(n+m)) logical word time and O(n+m) peak words. Parse source, SCC-decide B, group variables by the complementary pairs of signed implication SCCs, and compute each group's parity weight |S intersection V_g| modulo 2. A group is free iff both values of a representative are compatible with B, discoverable by explicit unit-augmented SCC runs. If B is SAT with model alpha, the attainable parity set is a singleton iff all free groups have weight 0, and is {0,1} if any free group has weight 1. This is a decision result, not a representation of an arbitrary XOR relation as 2CNF.

Proof to challenge: For any two B models alpha,beta, consider SCC blocks on which they differ. Orient each changing block 0 at alpha and 1 at beta. A two-literal clause on two changing blocks satisfied by both endpoints becomes an implication. Any clause with one unchanged block must already be satisfied by its unchanged literal; within-block clauses cannot obstruct the change. The inter-block implications are acyclic since SCCs were already collapsed. Flip changing blocks in reverse topological order, yielding a feasible path of length at most n. If a free odd group changes orientation along this path, one path edge toggles global parity. Thus both parity values have witnesses. A naive candidate-flip constructor charges O(n^2(n+m)) time and linear live words. This also proves the affine hull of B's nonempty model set consists exactly of its forced unary equations and signed SCC-block pairwise equalities/disequalities.

A correct **counterexample to naive composition** is B=(x OR y), plus global linear equations x=0 and y=0: each independently compatible with B, jointly impossible. The single-parity theorem does not solve arbitrary simultaneous parity checks.

## Exact scalable hostile control for Roles 1–3

For even q=2t>=4, construct q original x_1,...,x_q, q-2 functional prefix variables p_1,...,p_{q-2}, t independent orientation bits c_j and output target bit b. Write pair XOR equations x_{2j+1} XOR x_{2j+2}=c_j as two proper binary clauses each. For i=1 enforce x_1 XOR x_2 XOR p_1=0 with four proper ternaries; for 2<=i<=q-2 enforce p_{i-1} XOR x_{i+1} XOR p_i=0 with four proper ternaries each; lastly enforce p_{q-2} XOR x_q=b as two proper binaries. Call its fixed encoded CNF P_{q,c,b}.

Exact output counts: n=2q-2, m2=q+2, k=4q-8, M=5q-6, zero free auxiliaries, q-2 unique functional auxiliaries. Its single connected affine incidence component has nullity d_A=q-1 and Role 5 excess K=q-2; its minimum raw strong syntactic 2CNF backdoor is h=(q-2)/2. Even with these large parameters:
  SAT iff b=XOR_j c_j;
  #SAT=2^t on SAT and 0 on UNSAT.
On all-zero c and b=1 it is UNSAT; toggling ANY individual c_j yields SAT by changing exactly two private signed-literal words. Under four addressed words per clause plus two header words and w=ceil(log2(64(7q-7))), encoded N=(20q-22)w bits; every exact deterministic word-probe decider reads at least t=q/2=Omega(N/log N) distinct private word groups on the designated UNSAT input. Canonical source recognition, affine-prefix elimination, SCC parity cancellation, policy selection, both output paths and complete source replay require only O(q) word time and peak O(q) words. The lower bound is solely input acquisition and is tight.

## Adaptive-state ledger to preserve

Initial k=4q-8, h=(q-2)/2, K=q-2 are structural analysis parameters, not oracle-provided policy inputs. Source clause reads and grammar recognition discover the actual XOR equations. Charged affine prefix elimination leaves ONE long XOR on original x. SCC of binary pairs reveals t free blocks, each of even parity weight, turning global parity into a constant. If it equals b, construct one witness and replay all original clauses. If not, combine rows to the exact contradiction 0=1 and reject. On other one-parity 2CNFs with odd free SCC blocks, the generic solver switches through feasible SCC-block flips to obtain parity-target witnesses. Solver policy does not know labels beforehand. All failures, switches, source rereads, memory and reconstruction must be counted.

The existing 2^K upper bound and tree-joining theorem are correct but overestimate the single-connected-component control. Neither role must require the ideal solver to enumerate basis choices, issue all continuation queries or build a full compatibility table. The fixed 2^(q-2)-leaf enumerator is intentionally nonpruning and only a policy comparator.

## Verification and artifacts

Remote report: research/agents/lspv-4/2026-10-24_1046_LSPV-4_SINGLE_PARITY_SCC76.tex.
Remote mini: research/agents/lspv-4/2026-10-24_1046_SINGLE_PARITY_SCC76_MINI.py.
Remote audit ledger: research/agents/lspv-4/2026-10-24_1046_SINGLE_PARITY_SCC76_RAW.json.

Local complete auditor: single_parity76_audit.py (SHA-256 a37da9e30eddc509d8ac475b05b9d9f751ff06e45458feee55797a27a5cde4db), with six independently stored raw JSON result sets and extended LaTeX in the user-delivered audit package. Seed 202610240136, 283,242 assertion-accounted checks, zero failures; all 166 bijunctive n=3 and all 4170 bijunctive n=4 relations tested against both parity outcomes; 5010 randomized small-mask tests, including 2062 actual witness-switch exits and 858 invariant-parity UNSAT exits; canonical SAT/UNSAT controls through q=4096. Finite results are COMPUTATIONAL corroboration only. Do not assume local files are accessible across scheduled runtimes.

## Next target and scope

Independent review priorities: signed SCC consistency, flipping path, affine hull equality, maximum-case polynomial charges, how each XOR3 quartet and XOR2 pair is encoded, source/target witness maps, backdoor and nullity counts, private sign sensitivity and a precise comparison with Role 5 AFFINE-EXCESS-NULLITY111 and Role 3 TREE-INTERFACE-SWITCH79. For the next ladder step, test TWO or more global parity constraints interacting with 2CNF, allowing dynamically selected SCC, Gaussian, branching, caching, recomputation, learning and direct decisions, and scrutinize joint compatibility holes. No universal all-decider superpolynomial theorem follows. P versus NP remains OPEN.
