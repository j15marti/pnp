# LSPV-4/431: Untagged namespace authentication and physical resource firewall

**2026-11-05 22:00 PST, Route A PRIMARY. PROVED/RESTRICTED + COMPUTATIONAL. Universal FLMV contraction OPEN. P versus NP OPEN.**

## IDEA -> SEARCH -> ITERATE

**Initial hypothesis:** the LSPV-4/429 one-pass low-space autarky verifier cannot verify all core/tail shared variable names under arbitrary unsigned numerical identifiers. Four falsifiers: F1 the original grammar already syntactically separates core and tail names, F2 its implementation actually checks arbitrary set intersection in one pass with logarithmic workspace, F3 a verified namespace certificate is provided, F4 its claim is only for syntactically restricted inputs. **F1 holds.** Read the actual /429 report (blob `4b369eecc9983cadf961eeb124ff0c23a0768555`): core IDs have bit-length <= b and private tail IDs have length > b. This is a valid cheap authenticated namespace certificate. The original claim is **retained unchanged at its restricted scope**. Our revised target is the strictly harder task of *untagged* arbitrary core/tail ID intersection detection.

## Exact 3-CNF family (a syntactic validator control, NOT a hard SAT family)

Let n>=1, i in [0,n-1], w=ceil(log2(7n+5)). Use distinct positive variables x_i=1+i, p_i=1+n+i, q_i=1+2n+i, r_i=1+3n+i, s_i=1+4n+i, d_i=1+5n+i. For S,T subsets of [n], form the n-clause **core** with clause (x_i OR p_i OR q_i) when i in S and (d_i OR p_i OR q_i) otherwise, followed by a tail clause (x_j OR r_j OR s_j) for each j in T. Every clause is proper positive width three; source encoding: eight-bit magic 01101011, unary n, two-bit core/tail clause tags, one sign and w binary identifier bits per literal, terminating 00.

The source has N=Theta(n log n) bits for |T|<=n, core prefix length independent of S. Its **syntactic variable-name intersection** is nonempty iff S intersection T is nonempty. All formulas are trivially SAT by the all-TRUE assignment. Hence the reduction is deliberately **NOT** a hardness-preserving reduction of SAT and yields no computational SAT lower bound.

## Theorem 431.1: exact one-pass lower bound (PROVED/RESTRICTED)

Consider any fixed deterministic verifier that reads this source only once left to right and decides for *every* S and singleton tail T={j} whether the core and tail variable ID sets are disjoint. Let c(S) be the complete machine configuration at the boundary between the equal-length core prefix and tail suffix. If c(S)=c(S') for two different subsets S,S', choose j in their symmetric difference. The **identical** remaining tail suffix T={j} then requires different answers, impossible for deterministic continuation. Thus c is injective, there are at least 2^n distinct configurations, and the retained complete configuration contains >=n bits of information.

Under a standard fixed finite-alphabet sequential-input Turing machine, polynomial time, fixed tape count and usual head charging, this implies Omega(n)=Omega(N/log N) writable physical extent up to lower-order head/index fields. This is a *one-pass streaming* theorem and does not apply to FLMV's indexed input model, because it allows revisiting the original read-only source. It also does not contradict /429's bit-length-tagged grammar. The exact underlying communication principle is deterministic one-way INDEX / set disjointness (Kushilevitz and Nisan, *Communication Complexity*, 1997).

## Theorem 431.2: charged indexed repair (PROVED/RESTRICTED)

On the FLMV 2005 Section 2.1 indexed-input machine, verify arbitrary fixed-width input syntax, then store only clause/ID offsets, index positions, slot counters and bit counters on **densely addressed** work and index tapes. For n core clauses and m tail clauses, compare <=9nm ID pairs bitwise via original-source indexed rereads. With identifier width w=O(log n), cost is O(N+nmw) *input-bit probes*, O((N+nmw) polylog N) **native time** including every index write, indexed read, erasure, return-position reconstruction and output, and O(log N) highest-position physical work/index workspace. The proof is the direct nested-loop implementation, with at most six O(log N)-bit counters and fresh indexed address construction for each requested bit.

For singleton m=1, this is N^(1+o(1)) time; for dense m=Theta(n), it can be N^(2+o(1)). For general self-delimiting arbitrary-length identifiers, an intentionally loose pairwise rescan gives O(N^3 polylog N) time and O(log N) physical space. These are concrete **upper bounds**, not optimal lower bounds. No uniform N^(11/10) all-CNF validation guarantee follows from this method. For q independent untrusted children, independently validate q originals, in agreement with LSPV-4/430's O(qM) pivotal-input objection. A *shared authenticated generator* could avoid this cost, but needs a separately proved acquisition and native simulation theorem.

## Established hard-family and legal shortcut ledger

The actual published *hard* family retained as a transfer control is cubic growing edge-expander odd-charge Tseitin: H even vertices, 3H/2 edge variables, 4H proper signed width-3 parity clauses, binary encoding Theta(H log H) with polynomial numbering; odd total charge gives certified UNSAT. Ordinary shared-DAG Resolution has size 2^Omega(H) under suitable graph/expander hypotheses (Urquhart 1987 and Ben-Sasson/Wigderson 2001). This restriction does NOT transfer to mixed R_mix341 or arbitrary SAT algorithms. The project's 4H-1 mixed AND3/GF(2) short refutations are mandatory upper-bound controls. CNFgen actual native code: `MassimoLauria/cnfgen/cnfgen/families/tseitin.py`, blob `4bb5fd198fc4a698a5a207f67b36a9591b2a3bab`.

K4 and cube odd/even-charge instances were independently reproduced for SAT/UNSAT and private-tail controls. Alias corruption rejects the *namespace certificate* but need not change the underlying SAT label. This is why certificate-invalid and UNSAT must remain separate.

## Computational audit (host-level, not native FLMV execution)

The Python producer exhaustively covered every S subset [n] and singleton T={j}, n=1,...,8; included two dense-tail controls per n, unique 2^n core-prefix checks, four malformed-source rejections and n=128 indexed-read stress. **14,899 assertion groups.** The independent Node.js implementation ran **10,804 checks** and recomputed 15 sample SHA-256 source hashes. Independent exhaustive Boolean evaluation of four even/odd K4 and cube Tseitin originals with private tail controls passed **12 assertions**. For n=128: 4,654 encoded source bits, 4,589 instrumented source-bit probes, a deliberately conservative 78-bit bound for six dense address registers. The measurement is a host-language simulator, not a native FLMV machine benchmark. Source/proof/verification costs do not arise from logical DAG node counts.

## Actual research and source continuity

Read governing five-role handoff `research/coordination/2026-11-02_1204_WORST_CASE_MINIMUM_DERIVATION_FIVE_ROLE_REFOCUS.md` blob `c3889a3e`, current issue #3, `AGENTS.md`, `CODEX.md`, `.codex/skills/pnp-research/SKILL.md`. Read LSPV-4/429 blob `4b369eec`, LSPV-4/430 blob `8b2b5d09`, LSPV-2/434 blob `cb86930e`, actual `GROKPROOF/2026-11-06_0515_PROGRESS.md` blob `93f9202d` and `research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex` blob `1f9fc727`. Both requested third-party repos were read: `konard/p-vs-np/proofs/complexity/README.md` blob `7ee9a11` and `scripts/proof_status.json` blob `93b77ed` (distinct finite one-tape framework); `blkph0x/p-vs-np-proof-research/METHOD_INDEX.md` blob `18d693e` and `PROOF_PORTFOLIO_BRIDGE_REPORT.md` blob `22215ce` (bounded proof fragment projectors). `openai/math/lean/OAI/Algorithms/SubexponentialSAT/ExecCNFNodeSearchCosts.lean` blob `1ced21f` describes specific costed programs, not arbitrary SAT machines.

The FLMV author PDF `https://lance.fortnow.com/papers/files/tst.pdf`, §2.1 page 4 was text-read and visually checked, including erased indexed-tape contents and highest-position space. Primary and related communication sources: Kushilevitz/Nisan *Communication Complexity* (1997), Roughgarden *Communication Complexity (for Algorithm Designers)*, Proposition 1.8. Actual indexed-web search: deterministic one-way DISJ/INDEX; SAT time-space lower bounds; Tseitin ordinary Resolution. Direct Google-branded interactive search unavailable. No new universal proof claim, no native R_mix341 checker run.

## OPEN transfer and role-owned boundary

A valid O(log N)-space tagged parser does NOT imply an equally cheap one-pass parser for arbitrary untagged variable intersections. Conversely a streaming lower bound does NOT imply indexed-time SAT hardness. All-input recursively iterable same-machine contraction for every fixed uniform SAT decider, both labels, malformed sources and full work/space including local search, guest, ancestor, replay, references and caches remains OPEN:
$$
t'\le\max\{11/10,3/5+t/2\},\qquad
s'\le\max\{1/2,s/2\}.
$$
Route B fixed R_mix341 B1/B2/B3 remains separate and OPEN. P versus NP OPEN.

**References:** [1] Fortnow, Lipton, van Melkebeek, Viglas, JACM 52 (2005), DOI 10.1145/1101821.1101822. [2] Kushilevitz and Nisan, *Communication Complexity*, Cambridge UP (1997). [3] Urquhart, JACM 34 (1987), 209-219. [4] Ben-Sasson and Wigderson, JACM 48 (2001), 149-169.
