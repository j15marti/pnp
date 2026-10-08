# RECOVERY-STRENGTHEN6 handoff

Status: P versus NP remains OPEN.

Recovered correction:

- `COMBINED-REPLAY1` is an exact terminating source-backed solver for every finite CNF. General implementation/termination was built.
- `RECURCLOSE1` gives conditional recursive `K` elimination.
- `MARKED-CUTSET-BLOCK1` meets the favorable one-level ledger only on supplied marked inputs.
- No one implementation is proved to have all-input exactness, recursive successor closure, and the favorable joint resources.

New exact result:

- A successor-closed hereditary marked domain would compose to time `N^(6/5+o(1))` and space `N^(1/2+o(1))`.
- The current flat marked domain is not successor-closed. An unbounded accepted-parent family emits an unmarked child and the next invocation returns `UNKNOWN`.
- Trivial padding gives an ordinary-to-marked expansion `N = Omega(m^2/log^2 m)`; followed by square-root emission it gives no strict typed-cycle contraction.

Validation:

- `experiments/proof_spines/hereditary_marker_closure_test.py`
- SHA-256 `e893ff9b0c584525d8f3c42a0fb1e2b692f04c2131babd16edd2aea1b5527934`
- Six exact CNF1 nonclosure families and exact recurrence/FLMV fractions passed in 0.13 seconds under a 25-second alarm.

Next target: implement and charge a genuinely hereditary nested grammar plus an all-input causal acquisition rule, or prove favorable completed-phase bounds directly for `COMBINED-REPLAY1`. Test the flat-child family and expander-guarded general core first.
