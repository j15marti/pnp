# HORN-TRANSPORT-CEILING100 handoff

Status: the Horn-selector lift, exact strong backdoors, Hall degree-three rung, and fixed-encoding direct sensitivity bound are **PROVED/EXACT**. Degree-four NP-completeness is a **KNOWN THEOREM**. The finite audit is **COMPUTATIONAL**. Unrestricted deterministic superpolynomial SAT time and P versus NP remain **OPEN**.

For the padded implication chain followed by the Horn-selector lift,

- target variables: `8q+31`;
- target clauses: `8q+32`;
- explicit fixed-record words: `32q+130`;
- SAT iff the source orientation vector is not all one;
- flipping orientation `i` changes exactly two signed consequent words;
- the `q` sensitivity pairs are disjoint, forcing `q` word/record reads on the all-one target input.

This is direct target sensitivity, only `Theta(N/log N)` in the declared encoding. A paid one-call reduction cannot transport the source bound because its explicit write cost gives the exact numerator upper bound

`q - (32q+130) - H(q) < 0`.

The lifted chain is in the unrestricted canonical Horn-selector NP-complete language, but its padded endpoint variables have source occurrence degree six; do not silently claim that this family lies in the maximum-degree-four sublanguage.

Roles 1--3 should use the connected degree-three cyclic lift as a hostile control: it has both polarities and linear strong syntactic backdoors but an immediate all-true witness. The first plausible next amplification is not another query gadget. It is a post-acquisition compression-or-continuation theorem covering every total uniform exact decider after all input bits may have been read.

Artifacts:

- `research/main/2026-10-23_2248_MAIN_HORN_TRANSPORT_CEILING100.tex`
- `experiments/review/horn_transport_ceiling100_audit.py`
- `results/raw/review/HORN_TRANSPORT_CEILING100_raw.json`

No automation was created, reactivated, rescheduled, or disabled.
