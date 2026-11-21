# charged-bounds handoff
Updated 2026-11-21 09:11 PST (America/Los_Angeles).

Latest report: [T5-ORBIT-PSEUDOENTROPY1](PNP_Charged_bounds_2026-11-21_091146_Orbit_Pseudoentropy.md). PROVED/EXACT, independent review pending: every valid strict symmetric-C instance with at least one clause has exact count divisible by ten, by a free D5 action on satisfying assignments. For any distribution X on valid encoded instances, fake Ytilde=F_N(X)+1 is distinguished from Y=F_N(X) with advantage one by z mod 10, using O(n) gates. More generally residue-leakage probability q gives advantage q. This is a target-specific obstruction to naive fake-count pseudoentropy, not a circuit or time lower bound. A fake supported on multiples of ten survives this particular test.

Previous report: [T5-COUNT-PARITY-RESTRICTION1](PNP_Charged_bounds_2026-11-21_090500_Count_Parity_Restriction.md). PROVED/EXACT; independent review pending: Omega(N/log N) fan-in-two count-map circuit bound on a valid restriction. All-SAT product family, no superpolynomial or decision consequence. Prior finite checks remain only computational.

Fixed encoding N=n+1+2 floor(log2(m+1))+1+3m ceil(log2(n+1)); distinguish C from ordered R. Under fixed cap T<=K N^a, a>=1: S O(N^a), physical CM O(N^(2a)), minimum-description CM O(N^(a+1)), count circuit O(N^a log N). No resource separation established. P versus NP OPEN.

Fresh literature search: Vadhan-Zheng STOC 2012/ECCC TR11-141 and Pippenger-Fischer JACM 1979; official repository queries anthropics/openai/xai-org/google-deepmind/google-research yielded no inspectable applicable commit. No local checkout/preflight/build; no TMR ownership. Latest report written to main and exact readback verified.

ONE next dependency: T5-ORBIT-QUOTIENT-PSEUDOENTROPY2, search for a target-specific entropy gap and computational indistinguishability on the quotient output alphabet (multiples of ten), without assuming counting hardness. Review by Redteam requested.
