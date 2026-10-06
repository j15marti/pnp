# PROOF-0001

Status: PROVED/EXACT in the stated deterministic compiler model. Global problem remains open.

## RESTRICTED-ACCESS-ELIMINATION1

Let H be a family of SAT instances. Let C be a deterministic polynomial-time compiler that sees a candidate exact SAT procedure only through returned decision bits. Assume every adaptive query C issues lies in H, and a fixed ordinary polynomial-time algorithm B gives the correct SAT decision on every q in H. Then an ordinary polynomial-time simulation can reproduce C's complete transcript and output by answering each query with B.

Proof: induct on adaptive query number. Equal states issue the same next query q. Since q is in H, B returns the same bit as the exact procedure. Hence next states agree. Polynomial overhead follows from polynomially many polynomial-length queries and polynomial B.

Therefore a compiler with only this restricted extensional access cannot be the source of a forbidden small representation when the target already has an unconditional lower bound in that representation class. A surviving route must use correctness outside H, implementation/source information not determined by the answer transcript, or abandon the claimed landing/size/correctness guarantee.

This is a necessity theorem, not arbitrary-algorithm extraction. The theorem itself relativizes and also survives giving both simulations the same algebraic-oracle resources. It is therefore not the nonrelativizing or nonalgebrizing hinge. ASCS remains qualitatively different because its absolute ordinary-source premise can fail under oracle replacement; FSC remains open.

Handoffs: LEAD should use this exact necessity statement. WRITE should integrate it into main2/main3. RED should test whether proposed intensional data reduce to advice/preprocessing/extensional functionals. RESEARCH should seek formal analogues without treating them as SAT extraction theorems.
