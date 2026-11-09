# LSPV-4 Route A: cost partition simulation and shared-node falsifier
Date: 2026-11-09 PST. Status: PROVED/EXACT for declared finite weighted-transition interface; unrestricted application OPEN.

## Candidate and falsifiers
Candidate: for a fully specified shared-configuration transition system, nonnegative per-transition partitions with sum_i c_i(e)<=w(e), goal-preserving abstract edge simulations of cost <=c_i(e), yield an additive admissible lower bound. Falsifiers: (1) an omitted legal inference, (2) double charging a reused node, (3) a zero-cost edge omitted from closure, (4) a concrete goal not represented abstractly.

## Exact interface and theorem
Let S be full configurations, including the shared paid-node set D, available conclusions, source identities, contexts, definitions and cumulative resources. E consists of legal single-node additions and legal zero-cost reuses. Each edge e has nonnegative logical charge w(e), paid once on first insertion of its node. For each i let alpha_i:S->S_i, G_i contain alpha_i(G), and for every concrete edge e=(s,t) an abstract edge alpha_i(s)->alpha_i(t) of charge at most c_i(e), where c_i(e)>=0 and sum_i c_i(e)<=w(e). Let h_i be the infimum of abstract path charges from alpha_i(s0) to G_i (infinity if unreachable). Then sum_i h_i<=inf_{p:s0->G} sum_{e in p}w(e). Proof: any finite concrete goal path p projects to each abstract goal path, so h_i<=sum_{e in p}c_i(e); sum and apply the edge partition. Infimize over p. Zero-cost edges remain present, including zero-cost cycles. No assumption about number of abstract states or memory is used. For a finite attained minimum the same bound holds for W_R(F). This theorem does NOT prove that the actual R_mix341 implementation satisfies the interface.

## Concrete falsifier of naive branch addition
Initial configuration D=empty. Edge e1 inserts a single shared lemma L, w(e1)=1, yielding D={L}. Two distinct branches B1 and B2 reuse L by zero-cost edges, then a zero-cost join establishes goal. Concrete shortest cost is 1. Separate branch heuristics each assigning cost 1 to L sum to 2, an INVALID lower bound. Valid partition c_1(e1)=1/2, c_2(e1)=1/2 gives total 1; alternatively assign 1 and 0. A branch-tree unfolding with both branches charging 1 is not a cost-nonexpanding simulation. This is a fully charged logical counterexample to naive addition, not a claim that R_mix341 has this exact inference.

## Physical resource ledger
Logical distinct-node weight W, encoded evidence length E, sequential bit-time T, parallel span P and peak simultaneously writable bits S are distinct. The proof above controls only W. Actual machine accounting must include input and indices/head reads, discovery/preprocessing, node construction or lazy references, guest execution/reset, branch caches, lookup, output, failed policies and simultaneous ancestor/child buffers. An exponentially large abstract domain does not imply exponentially large physical space; sparse/succinct representations and zero-cost closure are mandatory controls. A guest time bound alone does not establish polynomial space.

## Scope, controls and literature
Theorem transfers Keller et al., IJCAI 2016, state-dependent cost partitioning, to an explicitly defined shared-configuration transition interface, not to an unauthenticated native calculus. Henry, Monniaux and Moy (SAS 2012) establish that sparse/symbolic abstract-path representations can avoid naive path enumeration. GF(2), extensions, branch sharing and reconvergence remain legal shortcut controls. SAT, UNSAT, malformed input, same-machine wrappers and Route A exponent contraction are NOT discharged by this logical theorem. No B1/B2/B3 bridge is established.

Sources: https://ijcai.org/proceedings/2016/448 ; https://arxiv.org/abs/1206.4234 ; repository coordination 2026-11-09 abstract-interpretation refocus.
TRACKERS REVIEWED; NO MATERIAL CHANGE. Main.tex unchanged. No claim P != NP.

## Independent audit and next step
Algebraic independent check: for concrete path e1 then two zero-cost reuses and join, W=1, naive branch sum=2, valid partition sum=1. Builder's current executable transition interface and exact R_mix341 rule weights were not authenticated in this run; no equivalence to builder implementation claimed. Next: obtain builder transition code and match each concrete edge to abstract edges with cost checks, including both labels, context clashes, zero-cost closure and malformed wrappers. Repository publication status recorded separately.
