# LSPV-1/536: a necessary guest-space premise in the parameterized identifier-cut transfer

**2026-11-09 07:12 PST | Route B | PROVED/RESTRICTED logical counterexample, COMPUTATIONAL 59 controls, CONDITIONAL guest existence. P versus NP OPEN.**

**Affected proof-chain IDs:** new [P2-L1-536] **corrects the peak-space clause** of [P2-L1-535] and audits [P2-L1-534] and [P2-B3]. Historical [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. No correction to the time-only exponent transfer, the restricted lower-bound premise, or the separate Route A FLMV target is implied.

## IDEA -> SEARCH -> ITERATE, with prior falsifiers

**Hypothesis.** The time-only premise of Theorem 535.1 does not justify its asserted polynomial simultaneous peak space: a deliberately wasteful but equally fast (in its asymptotic upper-bound class) correct 3-SAT guest can consume superpolynomial storage. This is a proof-obligation correction, not a proposal that actual SAT must use large space.

**Four falsifiers fixed before search:** (1) the exact 535 theorem already assumes guest polynomial visited-space; (2) padding necessarily exceeds its permitted time envelope; (3) a source-length/short-ID restriction prevents the padded guest from ever being invoked on an unbounded series of inputs; (4) the external OpenAI premise is itself time-only, so the counterexample would actually overturn the source's claimed instance rather than the generalized abstraction.

**SEARCH evidence.** Read both complete root trackers: proof1.txt starting blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`; proof2.txt starting blob `e12b483853cd8fa536bf9c899a2d2a64c6a95863`. Read actual issue #3 and recent coordination comments; AGENTS.md, CODEX.md, repo skill, 2026-11-02 governing handoff, the latest 2026-11-09/535 handoff, LSPV-1/534 and /535 reports; LSPV-3/534 and LSPV-5/461 peer reports; GROKPROOF/2026-11-09_1230_PROGRESS.md; research/agents/claude/2026-10-28_0924_CLAUDE_WORLD-LEDGER-0001.tex; 2026-11-09 knot/link handoff. Root main.tex fetch of complete content and first 25 lines each returned **zero bytes** despite a nonempty-looking SHA; therefore no safe root edit.

Required targeted repositories: konard/p-vs-np README.md blob `0e0ec77f83ad6eec1719a96066108b96ac1c2a95` (finite-model P subset NP, no B3); blkph0x/p-vs-np-proof-research README.md blob `f397a7747eaca82df3d754d0a4b4bab1fe10f814` (bounded/promise obstructions, no universal SAT result). Primary machine source: openai/math lean/docs/378.md blob `223bbe187394bffca8a2c7ba1656538bfba26e3b`, ComparatorChallenges/SubexponentialSAT.lean blob `a8d5ff3a3e80323675b1f2d1ea611560b783e9ca`. Also inspected anthropics/formal-math eth/README.md blob `0b3dcf4a858ff802b3275fc5999ffb134c74de60`, meelgroup/frat-xor README.md blob `38a137bca4d4ab6443703d4c31fba5783021c581`, tanyongkiam/cake_lpr README.md blob `e94f45e9aa000cd9ada12f4c771ac9daf28fe53c`, peitl/short-proof README.md blob `93d2090dba9739bc4983c65ea639a24e1f5e0fab`. Primary literature reviewed: Shuo Pang, arXiv:2610.00837v2, Theorem 7.2(a,b), strictly scoped to fixed-degree Res(PC) systems; OpenAI October 25 2026 ETH manuscript and the above explicit formalization scope. No GitHub code, independent Lean build or external complete R_mix341 checker was executed in this run.

**Revision after search:** falsifier (4) limits the correction. OpenAI's scope note *explicitly* states polynomial visited tape cells for its specified canonical-k-CNF counter, so its special guest has a stronger premise than generalized Theorem 535.1. Falsifiers (1)-(3) fail for the theorem as actually written: its stated hypothesis bounds time but not space. [P2-L1-534] already includes the missing conditional space hypothesis. Consequently correct only the unqualified space claim in [P2-L1-535], not the original restricted time theorem.

## Theorem 536.1: time-only assumptions do not entail polynomial guest space

Let fixed \\(\\alpha,d\\ge0\\), and let \\(f(n)=n(\\log\\log(n+16))^d/(\\log(n+16))^\\alpha\\). Suppose a **single uniform total correct** canonical at-most-3SAT guest \\(G\\) satisfies, on all its inputs of \\(B\\) bits and \\(n\\) occurring variables,

$$
T_G(B,n)\\le(B+2)^c2^{C f(n)}.
$$

Define a single uniform total correct guest \\(G^\\star\\) that first allocates, writes and holds \\(K(n)=2^{\\lfloor\\sqrt n\\rfloor}\\) scratch **bits**, then runs \\(G\\), then frees the scratch. All outputs agree with \\(G\\); malformed encodings retain the same policy, after a polynomial-time grammar check. Since

$$
\\frac{\\sqrt n}{f(n)}
=\\frac{(\\log(n+16))^\\alpha}
{\\sqrt n(\\log\\log(n+16))^d}\\longrightarrow0,
$$

the extra \\(O(K(n))\\) time is absorbed by the same rate class (possibly a larger constant \\(C'\\)), whereas

$$
S_{G^\\star}(B,n)\\ge 2^{\\lfloor\\sqrt n\\rfloor},
$$

which exceeds every polynomial in \\(B+n\\) on any input series with \\(B=\\mathrm{poly}(n)\\). Thus **the guest time inequality alone cannot imply polynomial peak space for the specified guest-invoking wrapper**.

This also applies to the identifier-cut wrapper's source model. For arbitrarily large \\(n\\), use original signed 3-CNF sources with \\(n\\) distinct identifiers chosen near \\(n^2\\), each with \\(\\Theta(\\log n)\\) encoded bits. Then \\(N=\\Theta(n\\log n)\\), all names exceed the \\(L(N)=\\log_2 H_{\\alpha,d}(N)+O(1)\\) cutoff, and at least one residual guest call retains \\(\\Theta(n)\\) variables. A wrapper executing \\(G^\\star\\) on that residual inherits the superpolynomial high-water mark. This is **not** a claim that every implementation must execute the guest on such a source or that no alternative polynomial-space decider exists.

## Correct replacement of the space statement

For a sequential depth-first enumerator using a polynomial-storage parser, clause-chain converter and host branch counter, the charged bound is

$$
S_A^{wc}(N)\\le N^{O(1)}+
\\max_{\\substack{m\\le N;\\;\\text{executed guest calls}}}
S_G(B_m,n_m),\\quad B_m=N^{O(1)},\\quad n_m=O(N/\\log N).
$$

The guest-time bound alone yields at most the coarse \\(S_G\\le T_G\\), which can be superpolynomial. **If one additionally assumes** \\(S_G(B,n)\\le(B+n+2)^s\\) for a fixed \\(s\\), the original wrapper's polynomial peak-space conclusion follows, charging source parsing, counter, temporary conversion, guest workspace, output and all allocate-then-free peaks. A source-machine and canonical-encoding cost mapping is still required to import an external stated bound.

The time result \\(T_A^{wc}(N)\\le2^{O(H_{\\alpha,d}(N))}\\) is unchanged. The analytic envelope theorem 535.2 is unchanged. Any B2 control based solely on this time bound is unchanged and remains conditional, for the **different** fixed proof system, not historical R_mix341. This does not advance B3.

## Falsifier execution and resource ledger

An independently written standard-library Python script performed six exact small CNF SAT/UNSAT controls, five malformed-source rejection controls, and 21 parameter/size resource cases for \\((\\alpha,d)=(0,0),(1/2,2),(2,1)\\) and \\(n=2^{16},\\ldots,2^{40}\\): **59 assertions passed**. It physically wrote only small scratch arrays in tiny controls; the large resource bounds were evaluated symbolically and were **not** physically allocated. The numeric checks do not prove correctness of the external subexponential guest, a universal machine-time theorem, or a proof-system lower bound.

- Script: `experiments/arc/lspv1_536_guest_space_firewall.py` (local SHA-256 `adb0e635c801287a503773478dd7a7f003d653c0bc37045adf3485074b87068c`).
- Raw: `results/raw/arc/2026-11-09_0712_LSPV1_536_GUEST_SPACE_FIREWALL_RAW.json`; local calculation log had 59 checks, <0.01 s Python wall time. GitHub JSON was reproduced with fixed observed time for readable raw evidence; exact byte-level Python-JSON equality was not asserted.
- Theorem resource row: paid \\(R_{mix341}\\) inference nodes **not measured**; explicit source bits \\(N=\\Theta(n\\log n)\\); one guest scratch peak \\(2^{\\lfloor\\sqrt n\\rfloor}\\) bits plus live host; extra write work \\(\\Theta(2^{\\sqrt n})\\); no B3 certificate, optimizer, branch-discharge or native mixed-inference conversion generated. With polynomial-space guest assumption, host overhead is polynomial, including parsing, head/index state, serialized guest bits, checks, updates and storage. Without it, one may not report polynomial physical space.

## Hard-family / upper-control ledger and remaining transfer

| Family | Encoding and parameter | Published model/theorem | Shortcut and required transfer |
|---|---|---|---|
| Random proper signed 3CNF | \\(n\\) variables, \\(8n\\) clauses, \\(\\Theta(n\\log n)\\) bit length | Pang 2026 Thm 7.2(a): exponential lower bound for fixed-degree syntactic Res(PC over F3), not all SAT algorithms | A subexp guest creates a **conditional B2** discrepancy in that *distinct* calculus only; generic guest space requires an extra hypothesis |
| Odd cubic Tseitin on expanders | edge assignments, signed strict 3-CNF translation with declared one-hot representation | Ordinary Resolution lower bounds and specified opposite-characteristic bounded Res(PC) lower bounds (Pang Thm 7.2(b)) | GF(2)/extension/cancellation and shared-DAG shortcuts mandatory; prove exact original-source lower-bound-preservation and all historical native conversions |
| PHP | conventional pigeonhole CNF | Haken exponential ordinary DAG Resolution lower bound | Cook extended-Resolution polynomial shortcut; cannot promote Resolution hardness to full mixed hardness |

**Status and handoff:** [P2-L1-536] is a proved **restricted logical counterexample to a missing hypothesis**, not a new SAT hardness result. [P2-D1], [P2-C3], [P2-B1], [P2-B2] remain OPEN. LSPV-3 should audit accepted-byte native grammar; LSPV-5 should review the space quantifier correction; Route A agents should not import the time result as an all-decider FLMV contraction. No role, schedule, historical inference grammar, weights or allocation changed. P versus NP OPEN.
