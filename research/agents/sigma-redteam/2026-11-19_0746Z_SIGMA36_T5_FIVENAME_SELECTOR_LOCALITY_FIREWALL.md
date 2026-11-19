# SIGMA REDTEAM36 | Five-name T5 locality and no-oracle selector

**UTC:** 2026-11-19 07:46. **PST:** 2026-11-18 23:46.  
**STATUS:** Restricted finite classification and source-certified selector PROVED/EXACT; independent experiments PASS; unrestricted arbitrary-CNF specialist, hereditary contraction and P vs NP OPEN.  
**Sentinel:** SIGMA36_T5_FIVE_NAME_TWO_ORBITS_SOURCE_SELECTOR_20261119_0746Z

## Input audit and primary literature
Retrieved exact user Library archive `T5_Exact_One_Experiments_2026-11-18.zip` (id `libfile_00b4599c2cfc8191a859b757dad101a0`, SHA256 `d811f0ea0b00fc88ebecf2349585386a2f0079508139aa638a8635e765e8a30a`). Independent `verify_bundle.py` PASS, including 236 pre-existing Mycielski deletion witnesses and 55,696 source Q checks; these are inherited controls, not newly claimed findings. Reviewed SIGMA35, LSPV-5 quotient/girth handoff and original Buss-Williams/FLMV sources. No existing project prompts, schedules or manuscripts modified.

## New theorem 36-A: two orbits of five-name local/global obstruction
Use precisely A->{B,D}, B->{C,E}, C->{A,D}, D->{B,E}, E->{A,C}; ties are nonwins and all clause *names* are distinct. For Q(h,u,v)=R(h,u) XOR R(h,v), old P=AND, Q accepts 60/125, P 20/125, disjoint. On 5 names there are 30 canonical Q clauses. Both independent standard-library auditors exhaustively checked every set of 1..5 clauses (174,436 instances) against 3,125 T5 assignments. **Exactly 180 five-clause systems**, and none smaller, are T5 UNSAT while (i) every per-head parity graph is bipartite and (ii) every induced four-name subsystem is SAT. All 180 are clause-minimal UNSAT and form exactly **two S5 name-renaming orbits**: 120 are SAT in some loopless quotient tournament but not in T5, and 60 are UNSAT in every quotient tournament. The quotient referee enumerated 52 equality partitions and 1,378 distinct abstract clause patterns. P on exactly the same five scopes is UNSAT for all 180, so no general Q>P hardness claim follows.

Representatives, with a,b,c,d,e as five *variable names*:
* `F_cap=Q(a,b,c)&Q(a,b,d)&Q(b,c,d)&Q(c,b,e)&Q(c,d,e)`. Deletion solution counts [50,110,110,125,125].
* `F_cmp=Q(a,b,c)&Q(a,b,d)&Q(c,a,d)&Q(d,a,c)&Q(e,c,d)`. Deletion counts [250,250,50,50,100].

An abstract witness for F_cap exists on equality quotient a=e=0,b=1,c=2,d=3, with tournament outgoing-adjacency rows `0100,0010,1000,1110`. Its last class has three outneighbors, forbidden in degree-two T5. The other orbit has no loopless-tournament realization whatsoever.

## New theorem 36-B: source-authenticated adaptive block selector
Partition F_cap using shared z=(b,c,d) and two genuinely disjoint private variable sets:
`B0(a;z)=Q(a,b,c)&Q(a,b,d)`, `B1(z)=Q(b,c,d)`, `B2(e;z)=Q(c,b,e)&Q(c,d,e)`.
A correct source-derived selector depending only on z is:
```
if not Q(b,c,d): j=1
elif R(c,b)!=R(c,d): j=2
else: j=0
```
In the final branch, the premises force c != d and either b=d (then Q(a,b,b)=false) or a transitive triple `high > b > low` among distinct b,c,d. A fourth a meeting both B0 clauses would force high to beat three opponents or low to lose to three; ties a in {b,c,d} also fail. Either possibility contradicts T5 in/out-degree two. Thus this selector does NOT use a BAD/UNSAT oracle. Every one of 125 shared z rows was checked: selected-block histogram (j0,j1,j2)=(20,65,40), **365 private trials and 510 Q evaluations** to verify selected refutations, versus 963 trials and 1,359 Q evaluations for the full-fiber audit. Rotational invariance leaves 25 normalized selector table entries, but does NOT imply general strategy compression.

## New theorem 36-C: strict prefixes give false NO on all SAT siblings
For M(z,j,a,e)=NOT B_j(z,private_j), strict Sigma1=EXISTS z,j,a,e M, Sigma2=EXISTS z,j FORALL a,e M, and Sigma3=EXISTS z FORALL a,e EXISTS j M are each TRUE both for F_cap and for **all five SAT deletion siblings**. Genuine UNSAT is FORALL z EXISTS j FORALL a,e M. The fixed-j formula EXISTS j FORALL z,a,e M is false on F_cap, so adaptive selection is necessary. The five SAT siblings have respectively 10,20,20,30,30 globally good shared rows. Omitting exactly those rows from a purported universal-row covering check gives a **false UNSAT result**. The supplied row limit n^.195 cannot replace ALL shared assignments without a proved covering theorem. Each sibling has an independently checked full satisfying witness.

## Resource, polarity and model firewall
If n^.195 rows and n^.65 blocks **per row** are physically present and child length is n^.35, a literal total SAT seed with time L^p needs guest time n^(.845+.35p); target n^1.33 requires p<=97/70~=1.385714 plus ALL source/verification/replay/negative and positive child costs. Peak space n^.5 requires s<=10/7 plus source offset/materialization. Distinct full child materialization costs n^1.195 bits, inconsistent with an n-bit physical source unless the virtual access cost is charged. Wrong advice paths must return UNKNOWN, and a k-bit correct path is not the same as an all-z Skolem strategy. Deterministic removal of trusted advice, when both verified polarities exist, costs up to 2^k verifier runs. R<=T for touched addresses does not by itself establish matching work-space or input-access bounds.

**Published exclusion:** Buss-Williams' alternation-trading deterministic all-SAT theorem at work-space exponent .5 attains c=1.34070 (rounded), in a multitape indexed random-access TM model. A genuine all-input SAT algorithm at actual length N with T=N^1.33,S=N^.5 in that *same model* would contradict the known bound. The present restricted Q specialist does not imply such an algorithm. FLMV co-nondeterministic (UNSAT-witness) exclusions at c<sqrt2 use sufficiently smaller space, not a blanket .5 bound; nondeterministic SAT witnesses, deterministic decision and proof-system-specific refutation cannot be interchanged. Source: https://mathweb.ucsd.edu/~sbuss/ResearchWeb/npProofLimitsMFCS/MFCS2013_Buss_revised.pdf ; https://doi.org/10.1007/s00037-015-0104-9 ; https://doi.org/10.1145/1101821.1101822 .

## Reproducibility and handoff
Primary code `audit36.py` and independently coded `independent36.py` checked all 174,436 systems, both 120/60 orbit classes, and the strict 125 x 25 QBF matrix. Zero failed assertions; result JSON reran byte-identically. Primary raw SHA256 `59703c754df35e2929bf60d1b6ad6d10ff142f121588444724d3fa5a365a1b66`; independent raw SHA256 `e71255082035b7c8baa40c3f3437ac4bdc076737a3e1ee952998680f6fc00475`. Full report, both complete Python scripts, all 180 sources, all strict prefixes, sibling witnesses and operation counts, runtime/RSS observations and SHA256 manifest are in the separately produced `SIGMA_REDTEAM36_PACKAGE.zip`.

Next adversary: find six-name or increasing-girth critical Q examples with *all five-name induced restrictions SAT*, extract a genuine shared/private cutset, and demand a source-checkable all-z selector that survives omission of SAT-sibling rows. Then require uniform arbitrary-CNF transport, full input encoding, hereditary closure and same-machine all-input resources. P vs NP OPEN.
