# LSPV-4/417 Route A: unchanged-guest fallback defeats universal iterability

**2026-11-05 09:36 PST | PROVED/RESTRICTED under SAT in P | FINITE CONTROLS PASS | P vs NP OPEN**

## IDEA, stated before SEARCH
Hypothesis: LSPV-2/421's correct *tagged* contiguous-separator SAT sieve cannot furnish a universally power-short all-input A -> Phi(A) when its declared nonpromise branch calls the same arbitrary guest A on the unchanged original. Falsifiers: (1) untagged valid CNFs actually trigger certified children; (2) emitted children retain certified tags; (3) the specific wrapper performs more than a direct original-guest fallback; (4) no correct padding decider exists conditional on SAT in P. The checked implementation falsifies (1)-(3); the construction below falsifies (4) conditionally.

## Exact conditional lemma and proof
Fix the template Phi_421 from LSPV-2/421: on checked tagged promised CNF, use streamed boundary-survivor decomposition; on an untagged valid CNF x, *call the passed-in total correct SAT guest on unchanged x*. No promise is assumed on ordinary children.

Assume SAT in P, and fix any total uniform correct polynomial decider D, with time N^(a+o(1)), writable space N^(b+o(1)), malformed encodings rejected. Choose integer p>max(b,1) and k>max(a,p,6/5). Define a *single fixed uniform* total correct polynomial decider A_{D,k,p} as follows. On untagged strings of input bit length N, sequentially write N^p work-tape cells and read from the last cell, execute at least N^k native clock steps using O(log N) counter cells, then execute D(x); on other strings execute D directly. This does not alter correctness for SAT, UNSAT, or malformed encodings. The explicitly accessed farthest work cell and the clock give actual worst-case exponents (t,s)=(k,p), with upper bounds N^(k+o(1)) and N^(p+o(1)); no free oracle or nonuniform hardcoding.

An infinite sequence of canonical untagged valid SAT/UNSAT originals U_N is supplied by repeated (x) clauses, optionally with a final (not x). Under general CNF grammar duplicate clauses are permitted. Every such U_N bypasses the tag sieve and the specified wrapper *executes A(U_N)*. Therefore

$$
T_{\Phi_{421}(A)}(U_N)\ge N^k,\qquad S_{\Phi_{421}(A)}(U_N)\ge N^p.
$$

The proposed universal Route A contract would require instead

$$
t'\le\max\{11/10,\,3/5+k/2\}<k,\qquad
s'\le\max\{1/2,\,p/2\}<p,
$$

a contradiction. For every fixed positive r, Phi_421^r(A) likewise calls Phi_421^(r-1)(A) on the same untagged U_N, ultimately executing the original A; *no finite iteration of this wrapper* improves the worst-case exponents. Tagged-parent cofactor children produced by /421 are untagged ordinary CNF, so the special transformation is not hereditary even on the promised parent.

**Scope firewall:** This falsifies this specific direct-fallback completion as a proof of the universal transformation. It does not refute all possible solver-dependent compilers, the tagged-family separator lemma, the conditional FLMV forbidden region, or P=NP. The base padding objection already appears in historic LSPV-2/118; the new contribution is the exact /421 both-label and recursive-site audit with all-phase FLMV resource lower bounds. No semantic machine analysis or proof-system invariant is claimed.

## Native same-machine ledger
Read FLMV 2005 primary author manuscript, section 2.1 page 4: indexed input is read-only, work/index tapes are charged, input/output tapes exempt; an indexed head move consumes/erases index tape. On the bypass branch no child/mask/cache or policy selection is used; tag scan uses O(N polylog N) time, O(log N) writable space. The guest explicitly touches N^p work cells, so all-phase peak is at least N^p even if later freed; at least N^k charged counter iterations occur; counter maintenance, input indexing, output, guest D and conversion only increase work. If a wrapper materializes the unchanged input on writable tape, this is extra charge, not an escape. This is a specified direct execution, not a claim that *every* SAT solver needs this work.

Illustrative k=4,p=2 gives claimed erroneous envelope (2.6,1) against the bypass's actual (4,2). This example is symbolic; an all-CNF polynomial D is NOT constructed unconditionally. Python checked 100 finite assertion groups, including SAT and UNSAT untagged families of h=2,7,100,700, malformed controls, legal empty clause, and tagged-parent ordinary child outputs. Independently authored Node verified 144 assertions, source hashes and exact BigInt padded counts. Both host tests are finite models, NOT native FLMV TM traces or evidence of general SAT in P.

## SEARCH: provenance, conflicts and sources
Governing project /1204 handoff blob c3889a3e, issue #3 through LSPV-2/421, LSPV-1/422, LSPV-3/426; source LSPV-2/421 report blob 05e39f45, replay bf14a1c6, raw 5179699e, LSPV-4/416, AGENTS/CODEX/repo research skill. Actual Grok assessment GROKPROOF/2026-11-05_1428_PROGRESS.md (a0e35e77) and Claude research/agents/claude/2026-10-28_1452_CLAUDE_TPORT-0002.tex (1f9fc727). New repositories konard/p-vs-np (README 0e0ec77f, proofs/complexity/README 7ee9a11e; finite one-tape only) and blkph0x/p-vs-np-proof-research (METHOD_INDEX 18d693ea, INDEPENDENT_AUDIT b30515cc; uniformity and cost controls) inspected. OpenAI/math ExecCNFNodeSearchCosts.lean 1ced21f4, FRAT-XOR README 38a137bc, CakeML LPR README e94f45e9 read: none supplies generic all-input contraction. FLMV 2005 JACM 52(6):835-865 primary PDF https://lance.fortnow.com/papers/files/tst.pdf; page 4 screenshot inspected. Queries: FLMV indexed random access model, separator SAT boundary join, konard and blkph0x audit models, OpenAI costed SAT. Direct Google-branded search unavailable; general indexed web and authenticated GitHub used. Code/CI is not a theorem.

## Proof status and next gap
**PROVED/RESTRICTED** the unchanged-guest wrapper cannot establish universal strict recurrence for every polynomial A, even assuming SAT in P. **KNOWN/RESTRICTED** LSPV-2/421 tagged separator identity and its finite promise controls unaffected. **OPEN** uniform recursively iterable all-input same-machine Phi with no unchanged-parent fallback and *certified* child hereditary semantics; full native Rmix341 B3 is separate and open; P vs NP open. No R, weight, task, schedule or other manuscript region changed. Root main.tex fetch returned nonempty blob 1b8a7d9a but zero bytes; left unchanged to preserve ownership and full outside-byte equality.

Next: construct and verify a no-tag all-input transformation, including explicit child indexed read/write/erase, selector acquisition, failed policy, materialization versus lazy access, recomputation/caches and simultaneous peak, or certify a further exact obstruction at the real machine level.
