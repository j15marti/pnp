# RP POSITIVE-CERT17 | 2026-10-22 Asia/Seoul
Status: P=RP OPEN; P!=RP OPEN; P vs NP OPEN. Original research this run does NOT prove any class separation.

## Ideas before literature
1. A positive random-tape accepting certificate of width O(log n) might give polynomial universal seeds without locating the certificate.
2. Audit exact functional gate-trace Tseitin conversion for primary-randomness projection.
3. Falsify any inference that high RP acceptance density itself yields short positive certificates.

## Primary and original checks
Naor-Schulman-Srinivasan FOCS 1995 Theorem 6, DOI 10.1109/SFCS.1995.492475, explicit (m,k)-universal sets of size 2^k k^{O(log k)} log m, listable in time linear in output size. Three originals directly fetched this run: research/agents/rp-separation/2026-10-21_RP_DENSE_BYPASS14_HANDOFF.md (blob 7d3cf3147a0c4e0728f4fb6a462a71305fcff1f0); research/main/2026-10-21_2248_MAIN_PROJECTED_DENSITY_GAUGE50.md (blob ed1b22301dcdf3033563e26fbdccffba3e484fa4); research/agents/rp-derandomization/2026-10-21_1836_RP_ANF_GATE11_HANDOFF.md (blob 50aaea218eb8bf84a3ed6d400d4fd0c0fbb88025). Other archives and original WRAPPER DAG unseen.

## ESTABLISHED restricted theorem
If a uniform RP verifier R(x,r) uses m(n)=poly(n) random bits, and for every YES input its accepting set contains a subcube determined by at most k(n)=O(log n) PRIMARY random-tape coordinates, then L(R) belongs to P. Enumerate an explicit (m,k)-universal set H and evaluate R on each h. H hits any accepting subcube, while NO tapes all reject. Total cost C_construct(m,k)+|H|(T_R(n)+m), polynomial; polynomial workspace, no advice, source loophole or uncharged witness discovery. This is an application of NSS1995, not a new universal-set construction.

## ESTABLISHED high-density counterexample
Let H_{m,k} be such a global universal set and F(r)=1 iff r not in H. Every assignment to <=k coordinates is matched by SOME rejecting h in H; hence F has NO positive certificate of width <=k. Yet Pr[F=1]=1-|H|/2^m=1-o(1) when m=n^2 and k=O(log n). R(x;r)=x_1 AND F(r) recognizes x_1=1 in uniform P, is an RP verifier for large n, and uses a poly-size fanin-two circuit to compare r to the explicit list. Thus even near-certain RP acceptance does not imply a short positive certificate or language hardness.

## Reproducible finite control
Standard-library Python finite greedy test (explicitly NOT polynomial asymptotic construction) checked (m,k)=(5,2),(6,3),(8,3),(10,3). Universal seed-set sizes 6,12,16,16. At (10,3), complement accepts 1008/1024 tapes yet has no <=3-literal accepting certificate. Shared-DAG majority-plus-certificate circuits have ANF degrees up to 9 while low-weight seeds of weight<3 all fail and universal sets succeed. Parity has acceptance exactly 1/2 but certificate width m. Two-gate functional Tseitin: five primary accepting tapes, five total correct traces. **11,904 assertion-accounted checks, zero failures**.

## Next and scope
Recover ONE actual executable WRAPPER gate DAG, map primary random wires separately from state/hash/timers and auxiliary traces, then test positive certificate width after collapsing deterministic copies. Uninspected original archive is not presumed covered. This does not establish P=RP, P!=RP, or P!=NP.
