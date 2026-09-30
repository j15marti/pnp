# Primitive-trace battery laboratory

The target is an operational rather than semantic resource model.

A shortcut algorithm is never a unit-cost macro. Expand it into its actual primitive execution trace and test candidate potentials step by step.

Core check:

`Phi(C_t) - Phi(C_{t+1}) <= L * cost_t`.

Guards:
- a potential defined as remaining optimal runtime is circular;
- optional failed shortcuts are not unavoidable cost;
- sequential-tape/crossing-sequence lower bounds are restricted-model results unless transferred;
- easy affine/Horn/treewidth computations must not receive false superpolynomial cost;
- oracle replacement and algebraic-oracle access must be tested separately.

See `tasks/TASK-003-primitive-trace-battery.md`.
