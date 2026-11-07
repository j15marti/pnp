# LSPV-5/414 handoff — affine ghost ports

**Time:** 2026-11-07 09:50 PST  
**Affected trackers:** [P2-D1], [P2-D3], [P2-L5-414]  
**Still OPEN:** [P2-C3], [P2-B1], [P2-B2]

The exact recovered /341 verifier accepts equal out-of-range mask bits on K4 nodes d2 and d5 when they cancel at immediate XOR child d12. Bits $H=6,64,1024,8192$ replayed with unchanged 15-node work and identical checker-summary hash. The $H=8192$ packet grew by 4,095 bytes.

This is an evidence/canonicalization defect, not an UNSAT-soundness break. Projection

$$
P_E(m)=m\mathbin{\mathrm{AND}}(2^E-1)
$$

preserves AND3 checks, commutes with XOR, preserves the sink and changes no node. Every mutant projected exactly to the historical packet.

Next actions:

- LSPV-1: keep B3 compiler bit length and verifier runtime separate from paid-node work.
- LSPV-3: require mask shifted right by E to be zero in any proposed accepted-byte grammar; test every affine port.
- LSPV-2: emit canonical projected masks.
- LSPV-4: charge BigInt/JSON parsing, storage and peak space separately.
- LSPV-5: next audit source ID/index identity and numeric freshness while seeking a full historical parser or RES-to-AND3 trace.

No weights, tasks, schedules, roles or agents changed. P versus NP remains OPEN.
