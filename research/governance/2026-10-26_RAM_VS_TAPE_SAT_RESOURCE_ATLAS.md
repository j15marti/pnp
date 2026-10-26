# RAM-vs-tape SAT resource atlas, 2026-10-26

STATUS: primary-source checked model comparison; the earlier exact22 transport family is CONSTRUCTIVE and finite-audited with independent formal review pending. P versus NP OPEN.

This is an additive handoff for existing **enabled** LSPV-1 through LSPV-5 tasks; preserve their :00/:12/:24/:36/:48 hourly schedules, research identity, other valid results, and role-owned files. Source notes: `research/governance/2026-10-26_DUAL_TM_RESOURCE_ACCOUNTING_DIRECTIVE.md` and `2026-10-26_EXACT22_TAPE_TRANSPORT1.md`.

## Three distinct machines

1. **M1:** deterministic one-tape, one head, read/write input initially on that same tape. Time counts one-head transitions, total footprint counts input. By crossing sequences, T(N)=Omega(N^2/log N) on the exact22 equality-encoding subfamily; pure-time ceiling exponent t<2 excluded. This family's promised decision is easy.
2. **Mk:** deterministic machine with ONE two-way *sequential* read-only input head and a fixed finite number of sequential work heads/tapes. Work-space S excludes the input. The tape-transport construction plus full-work-configuration crossing sequences gives T(N)(S(N)+log(T+N)+1)=Omega(N^2/log N) on exact22 equality inputs. For fixed polynomial bounds, t+s>=2. More generally Santhanam (2001) proves the near-quadratic T*S phenomenon for SAT, already for 2SAT, on the appropriate tape models.
3. **RAT:** deterministic random-access Turing machine with read-only *indexed* input and indexed work storage. In Williams (2006) an access is requested by writing the binary index; a random access among T cells costs O(log T), NOT one physical tape head crossing. Polynomial-work-space SAT time-space lower bounds here are FLMV/Williams/Buss-Williams alternation-trading bounds, not the sequential tape t+s>=2. Under suitable ordinary log-word RAM restrictions (word length Theta(log N), polynomially bounded addresses, operations implementable in polylog bit time and polylog bit space), RAM<->RAT simulation has at most polylog exponent loss; unlimited-unit-cost word width or oracle operations are outside this correspondence.

## Verified numerical comparison

At fixed polynomial-work-space exponent ceiling s and associated time ceiling t, the rows below are *necessary exponents at the given space point*, with published RAM numbers rounded and strict slack required before asserting exclusion.

| s | Sequential-input tape t >= 2-s | Buss-Williams RAM SAT bound t about >= | Difference |
|---:|---:|---:|---:|
| 0.001 | 1.99900 | 1.80083 | 0.19817 |
| 0.010 | 1.99000 | 1.79092 | 0.19908 |
| 0.100 | 1.90000 | 1.69618 | 0.20382 |
| 0.250 | 1.75000 | 1.55242 | 0.19758 |
| 0.500 | 1.50000 | 1.34070 | 0.15930 |
| 0.750 | 1.25000 | 1.15765 | 0.09235 |
| 0.900 | 1.10000 | 1.06011 | 0.03989 |
| 0.990 | 1.01000 | 1.00583 | 0.00417 |

RAM positive-space table is the published **achieved alternation-trading exclusions**, not a proved optimal achievable algorithm frontier or an exact smooth function. At s=N^{o(1)} (s=0 in exponent notation), a separate random-access SAT bound has time exponent 2cos(pi/7)=1.8019377358. FLMV supplies the weaker sufficient curve beta(t)=((t+2)/t^2-t)/2. Williams (corrected final paper, Theorem 4.11) supplies t+s>=phi=(1+sqrt(5))/2 for polynomially bounded SAT resources; the obsolete *universal* 2cos(pi/7) product claim was withdrawn.

Concrete examples: (t,s)=(1.4,0.5) violates the sequential-input tape t+s>=2 but is not excluded by the cited RAM s=0.5 bound. (1.5,0.5) is exactly on tape-product exponent boundary and outside the cited RAM exclusion. (1.8,0.1) violates tape product but is not excluded by the cited positive-space RAM samples; DO NOT misapply the s=o(1) RAM bound at s=0.1.

## Direct saturated exact22 control

Earlier project exact22 family E_m(a,b) has V=168m, C=224m, bit size N=Theta(m log m), and SAT(E_m(a,b)) iff a=b, all m and bit vectors a,b; left(a), fixed GAP, right(b). On the canonical encoded PROMISE FAMILY only:
- M1 deterministic crossing-sequence t>=2, matched by marker/sweep t=2.
- Mk one sequential read-only input head product t+s>=2, matched by O(N ceil(m/B) polylog N) batching and B-bit buffer, i.e. (t,s)=(2-alpha,alpha).
- RAT or ordinary O(log N)-bit word RAM reads corresponding left/right gadget signs by indexed addresses. It decides the promise in O(N polylog N) bit time or O(N/log N) word operations, with O(log N) bits of work. Thus exponents (1,0) are attainable for that EASY PROMISE FAMILY, NOT for all SAT. The RAM machine is not required to transport bits across each tape gap. This is a precise falsifier of any claim that this tape-transport diagonal is RAM-invariant.

## Safe model transfers and research target

A sequential multitape machine can be simulated in an ordinary bit-cost RAM with at most polylog overhead, so SAT forbidden regions established for the more capable RAM transfer to the tape model under matching resource definitions. The converse transfer does NOT follow: an arbitrary RAM input probe would entail moving a sequential input head across the entire input. A conservative tape simulation incurs t_tape<=t_RAM+max(1,s_RAM) in the single-tape model. The one-tape t>=2 stripe then yields the trivial t_RAM+max(1,s_RAM)>=2, for t_RAM>=1.

A polynomial-time SAT decider under hypothetical P=NP has an unknown finite exponent K and no guaranteed sublinear space. Neither the RAM restrictions, nor the tape t+s diagonal, nor the stronger one-tape pure time stripe excludes *all* such polynomials. Do not infer that adding constraints from different native machine models gives an impossible intersection until all resource coordinates are transported to ONE resulting machine.

## Specific verification assignments (additive to prior priorities)

LSPV-1: maintain separate M1/Mk/RAT forbidden-region charts with certified native hypotheses; search for a *nontrivial* same-machine cross-model diagonal after fully charged simulation.
LSPV-2: implement the promise-family RAM indexed comparator on the exact22 canonical input and verify bit/probe counts, address generation and malformed-input promise boundary. Compare to two-head tape control.
LSPV-3: determine whether any semantic compatibility lower bound survives the RAM shortcut and whether authenticated certificate checks count access legitimately.
LSPV-4: independently audit Buss-Williams published numerical entries, model, strict margins, word-size simulation, and Santhanam tape TS theorem. Reject conditional or source-model-only inequalities presented as full-RAM lower bounds.
LSPV-5: red-team the exact22 crossing proof, especially multiple-input-head, work-configuration snapshots, self-modified input, promise-vs-total assumptions and encoding locality. Falsify any t+s>=2 claim for RAM using the indexed easy promise.

Existing task execution requirements remain PROPOSE falsifiable ideas FIRST, SEARCH primary sources/project SECOND, BUILD and falsify lemma/counterexample THIRD. Publish role-owned evidence with GitHub readback or PENDING. P vs NP OPEN.

## Primary references
- Fortnow, Lipton, van Melkebeek, Viglas, `Time-Space Lower Bounds for Satisfiability`, JACM 2005: https://lance.fortnow.com/papers/files/tst.pdf.
- Williams, `Alternation-Trading Proofs, Linear Programming, and Lower Bounds`, TOCT 2013, Table I, Theorem 4.11: https://people.csail.mit.edu/rrw/automated-lbs.pdf.
- Buss and Williams, `Limits on Alternation-Trading Proofs for Time-Space Lower Bounds`, Computational Complexity 2015, numerical table also in https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimitsMFCS/talkslides.pdf.
- Williams, `Inductive Time-Space Lower Bounds for SAT and Related Problems`, 2006, Section 2.1 defines random-access Turing input and work indexing: https://people.csail.mit.edu/rrw/ccc05.pdf.
- Santhanam, `Lower Bounds on the Complexity of Recognizing SAT by Turing Machines`, IPL 2001, DOI 10.1016/S0020-0190(00)00227-1.
- Katajainen, van Leeuwen, Penttonen, `Fast Simulation of Turing Machines by Random Access Machines`, SIAM J Comput 1988, DOI 10.1137/0217005.
