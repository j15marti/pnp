# SIGMA3-COMMITHASH46 | 2026-10-17 UTC

Scoped theorem: replacing an exact globally committed w-bit state by an r-bit deterministic hash with r<w is not sound for all Sigma3 quantified circuits. For constants a,b, the game exists x forall y exists z: z=(y?b:a) and z=x is true iff a=b. Replacing x by an r-bit global tag and the equality by hash(z)=tag makes it true iff hash(a)=hash(b). Collision supplies a false positive despite unique local witnesses.

Tests: 65,808 exhaustive small hashes, 4,210,944 ordered-pair checks, 4,352 direct QBF evaluations, 242 independent proper-3CNF checks; no discrepancies. Four distinct salted six-bit SHA-256 outputs collide on 25-bit states 7646 and 7842, giving (9,60,30,22).

Theorem restricted to hash-only joins. The exact streaming equality check is easy; no general SAT lower bound follows. Resource Contraction and P versus NP remain OPEN.

NEXT: certificate for solver-dependent semantic continuation equivalence with two-sided responses, exact witness extraction, and fully charged queries, encoding, memory, and parent reads.
END_SIGMA3_COMMITHASH46_READBACK