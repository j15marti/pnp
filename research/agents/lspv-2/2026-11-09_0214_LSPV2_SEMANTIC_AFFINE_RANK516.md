# LSPV-2/516 | Semantic affine-read-rank obstruction on guarded Tseitin SAT children

**2026-11-09 02:14 PST | Route A | PROVED/RESTRICTED + COMPUTATIONAL | P versus NP OPEN**

**Proof-chain nodes:** New restricted evidence [P2-L2-516] qualifies the optimization [P2-L2-515] and peer rank noninvariance [P2-L4-515]. Still OPEN: [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04], and cross-route [P2-D1], [P2-C3], [P2-B1], [P2-B2]. No historical R_mix341 rule or weight is changed.

## IDEA -> SEARCH -> ITERATE

Hypothesis before search: the read rank required on some affine SAT children is **semantically forced**, not merely caused by gratuitous reads in a particular solver presentation. An affine family with exactly one UNSAT descriptor forces full input-read rank at that UNSAT descriptor for *every* total correct deterministic SAT decider, regardless of its internal branching algorithm. This obstructs inferring universal low-rank cache gains from [P2-L2-515] while leaving the conditional trie bound correct.

Predeclared falsifiers:
1. The source K4 odd-charge signed Tseitin core is SAT or contains nonproper ternary clauses.
2. Any nonzero guard descriptor still produces UNSAT, or the zero descriptor produces SAT, when the full proper-3CNF gadget is independently solved.
3. The fixed-length sign-position encoding is not affine in the descriptor, or its independently verified positional rank is below k.
4. A correct deterministic guest continuation can distinguish a kernel-equivalent descriptor using no different observed INPUT values (contradicting deterministic transition induction).

**Research and continuity:** Complete proof1.txt and proof2.txt were read at blobs 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b and b3637881aa461b3a0607cc5b02df1b0d12db988d at the research stage. Read issue #3 recent comments, the 2026-11-02_1204 five-role handoff, AGENTS.md, CODEX.md, pnp-research skill, LSPV-2/515, LSPV-4/515 and its five-role handoff, LSPV-3/529, actual GROKPROOF/2026-11-08_1130_PROGRESS.md and research/agents/claude/world-ledger/README.md. [P2-L4-515] already showed presentation-dependent trace ranks using two equivalent deciders and independent UNSAT tag signs. The present experiment instead proves a **solver-independent, semantic** rank obstruction for a one-exception SAT/UNSAT family. The scope is deliberately distinct.

Public-source checks: Fortnow-Lipton-van Melkebeek-Viglas, *Time-Space Lower Bounds for Satisfiability*, JACM 52(6), 2005, DOI 10.1145/1101821.1101822 (native random-access indexed-tape machine); Urquhart, *Hard Examples for Resolution*, JACM 34(1), 1987, DOI 10.1145/7531.8928 (ordinary Resolution on expander Tseitin sources); 2025/2026 literature on parity-query decision trees and monochromatic affine subspaces (known prior decision-tree technique, no originality assertion). Examined actual github.com/konard/p-vs-np README.md and scripts/proof_status.json, github.com/blkph0x/p-vs-np-proof-research README.md, METHOD_INDEX.md and INDEPENDENT_AUDIT.md; cnfgen/families/tseitin.py at MassimoLauria/cnfgen; meelgroup/frat-xor README.md; berkeley-abc/abc README.md; openai/math CONTENTS.md. These provide model, proof-status, certificate and circuit controls, not a universal transformation. Public web search was used, but no separately authenticated Google-branded search, native FLMV emulator or authoritative historical R_mix341 checker was executed.

## Formal restricted theorem (all k, not finite-test extrapolation)

Let y(d) in {0,1}^M be an authenticated fixed-length affine input family y_i(d)=p_i XOR <v_i,d> for d in F_2^k. Let A be any **fixed deterministic total correct SAT decider** on ordinary binary-encoded CNFs, and R(d) the set of actual INPUT positions read by its **complete** execution on y(d). Let V_R be the matrix consisting of their descriptor-direction rows. Exact deterministic trace replay on all descriptors in d+ker(V_R) is valid if the program and all non-input entry state agree: each predicted input bit agrees, so all subsequent transitions, output and input queries agree inductively.

Define h_f(d)=max dimension of a linear subspace U<=F_2^k on whose affine coset d+U the Boolean SAT-label function f remains constant. Then

$$
\operatorname{rank}(V_{R(d)})\ \ge\ k-h_f(d).
$$

Proof: ker(V_R) is a subspace of dimension k-rank(V_R), and the entire coset d+ker(V_R) has the anchor's output. Thus its dimension is at most h_f(d).

If f(d_0)=UNSAT for exactly one descriptor d_0, then h_f(d_0)=0, hence

$$
\boxed{\operatorname{rank}(V_{R(d_0)})=k.}
$$

This theorem holds for ANY correct deterministic SAT decider, **including hypothetical polynomial-time ones**, but it is ONLY a lower bound on the rank of input observations on that affine family, NOT on running time, space or overall SAT complexity. A solver may cache SAT children, use a compact formula recognizing the family, or employ a different compiler; the theorem does not claim that every child needs a fresh full SAT execution.

## Exact original strict-three CNF encoding

Start with the canonical K4 cubic graph with six distinct edge variables x_e. For vertices v=0,1,2,3, choose charge 1 at v=0 and 0 elsewhere. For each of the four wrong-parity assignments to the three incident edge variables, include its one falsifying signed **proper ternary** clause. There are exactly 16 such source clauses; XOR of vertex equations is 0=1, hence UNSAT. This is an instantiation of the standard Tseitin *construction*, **not** a certified asymptotic hard K4 instance.

For each j=1,...,k, introduce a control variable g_j, two distinct pin dummy variables a_j,b_j, and four clauses

$$
(\ell_j\vee a_j\vee b_j),\
(\ell_j\vee a_j\vee\neg b_j),\
(\ell_j\vee\neg a_j\vee b_j),\
(\ell_j\vee\neg a_j\vee\neg b_j),
$$

where ell_j=g_j when descriptor bit d_j=1 and ell_j=not g_j when d_j=0. Their conjunction forces g_j=d_j. Build g=OR_j g_j with a chain of 2-input OR gates: for output z=x OR y, introduce fresh u,v, use both clauses (not x OR z OR +/-u), both (not y OR z OR +/-v), and (x OR y OR not z). This is five proper ternary clauses per gate and exactly expresses the OR relation. For each original signed core clause (a OR b OR c), replace it by two proper ternaries (g OR a OR h) and (not h OR b OR c) using a fresh h. Existentially eliminating h yields (g OR a OR b OR c).

Therefore F_0 is UNSAT (every g_j=0, g=0, so all original odd Tseitin constraints remain); EVERY F_d with d!=0 is SAT (g=1, choose each h=0, pin dummy variables arbitrarily, satisfy OR definitions). For every k>=1 the original formula has **27+9k proper ternary clauses** and **19+6k variables**. Its input packet is 8-bit magic 10110110, unary 1^(19+6k)0, all ordered literals in width w=ceil(log2(20+6k)) unsigned ID bits plus one sign bit each, and the terminal 01. Exact bit length is

$$
M(k)=8+(19+6k)+1+3(27+9k)(w+1)+2.
$$

Exactly four input sign positions per descriptor coordinate toggle, all other positions stay fixed. These four-position sets are disjoint. Hence y(d) is an injective affine binary family and its global descriptor matrix has rank k. This is a **proper strict-three** source, not 4-CNF or a gratuitous unit-clause promise.

**Family/theorem/encoding/shortcut/transfer ledger:** K4 is a finite control using standard signed cubic Tseitin encoding and symbolic XOR UNSAT argument, not an asymptotic lower-bound source. The general expander-Tseitin construction has published exponential **ordinary shared-DAG Resolution** lower bounds on appropriate graphs (Urquhart 1987), but the pin/OR/guard extension used here is only established as an exact satisfiability-preserving *selector family*. We do NOT assert lower-bound preservation through its existential extensions, nor a mixed-rule lower bound. Algebraic XOR proofs, extension variables, normal Boolean propagation, known source recognition, and branch shared-DAGs remain legal upper-bound controls. Remaining transfer: none of the rank lemma proves [P2-A2], [P2-A4], [P2-A5], any same-machine SAT time/space contraction, source-independent decomposition, recursive applicability, B3, or unrestricted complexity lower bound.

## Independent finite tests and full accounting

Python source experiments/arc/lspv2_516_semantic_affine_rank.py (local reproducibility archive) independently generated and DPLL-solved every child for k=1..7: 254 original proper-3CNF sources, 7 UNSAT and 247 SAT. Python: **1,389 checks**, including exact source re-decoding, per-bit affine validation, rank checks, forged-read omissions and malformed header/trailer rejections. Independent Node.js generated, DPLL-solved, and bit-checked the same 254 sources: **1,058 assertion groups**. Both implementations agreed on all seven original-source SHA-256 hashes and packet lengths 684, 852, 1182, 1377, 1572, 1767, 1962 bits. For k=7 the original source has 90 clauses and 61 variables; its zero-descriptor original source is UNSAT and exactly 127 other sources are SAT. Independent DPLL search-node counts differ by implementation, as expected.

These are finite deterministic DPLL experiments and a separate algebraic proof, not native indexed-tape tests. Search/construction includes both enumerative generation and full independent DPLL. Input bits scale M(k)=Theta(k log k), descriptors count q=2^k, so exhaustive testing has explicitly exponential **aggregate** work and output bytes. Reference implementation traverses every encoded bit per source; its high-water is at least M(k) physical materialized bits plus DPLL state. A theoretical compiler using these tests on arbitrary SAT sources would additionally have to pay grammar recognition, preprocessing, any guest executions, trace capture, proof construction, cache storage, retrieval and failed searches. No upper bound of n^(1/2) peak or n^(11/10) local work is claimed.

## ITERATE / red-team conclusion

The initial hypothesis survives the strict-source and independent DPLL falsifiers. The broad interpretation, 'all rank-k children force q=2^k separate executions', is **false and explicitly rejected**: on the one-exception family, a deterministic OR-of-selector-bits strategy can accept most SAT children after one decisive positive read and reject d=0 after k independent reads. The exact claim is **full rank on the isolated UNSAT branch only**. This provides a semantic counterpart to [P2-L4-515] presentation noninvariance, not an all-input machine lower bound or refutation of valid affine-trie caching.

TRACKERS: Review proof1.txt and proof2.txt complete in this run; after the report and code are published, append only new scoped [P2-L2-516] if the current proof2.txt head still matches a full refetch and optimistic blob SHA. Otherwise write TRACKERS REVIEWED; NO MATERIAL CHANGE with explicit blocker and preserve all prior bytes. Keep [P2-A2], [P2-A4], [P2-A5], [P1-01], [P1-03], [P1-04], [P2-D1], [P2-C3], [P2-B1], [P2-B2] OPEN.

No root main.tex edit, no five-agent identity/role/schedule/enabled-state change, and no historical R_mix341 grammar or inference-weight edit. P versus NP remains OPEN.
