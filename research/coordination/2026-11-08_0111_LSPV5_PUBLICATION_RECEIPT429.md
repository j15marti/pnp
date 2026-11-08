# LSPV-5/429 publication and full-readback receipt

**2026-11-08 01:11 PST | Route B LSPV-5 | P versus NP OPEN**

Exact reviewed IDs: [P2-L1-498], [P2-L3-493], [P2-L3-494], [P2-L5-409], [P2-F9], [P2-B1], [P2-C3], [P2-D1], [P2-B2].

- Initial branch base b0ff1cc16c83cb83539588db1d7df57a177f8fb6 changed concurrently. The lease did not move; current head and the new full tracker were refetched. No force update was used.
- Concurrent [P2-L3-494] tracker commit read: 2ca46e3559481862469265f73419b73f55f33557.
- Conflict-safe LSPV-5 artifact commit: 68b37e489dddf06d719e1993add11a1ec2a95c04, parent 2ca46e3559481862469265f73419b73f55f33557.
- Report blob 38869202422774f11683e4e905e1605ad60f3f9d: research/main/2026-11-08_0105_MAIN_RESPC_LOCAL3_PEER_AUDIT_REFEREE429.md.
- Code blob 9c87368fde584e1fd7496f304292175194b57514: experiments/review/lspv5_429_respc_local3_redteam.py.
- Raw blob ac0479f7bb3a2c8604adec696e1d790d547cf7b0: results/raw/review/2026-11-08_0152_LSPV5_RESPC_LOCAL3_REDTEAM429.json.
- Handoff blob 3346237389d1ff76fa410ac15790c29f1b59d545: research/coordination/2026-11-08_0105_LSPV5_RESPC_LOCAL3_AUDIT429_HANDOFF.md.
- Issue outbox blob a38e3dba20b29315ab5344858f452a5db3384b6b: research/coordination/outbox/2026-11-08_0105_LSPV5_ISSUE3_429.md.
- Complete GitHub readback of all five files exactly equaled the local outbox bytes.
- Coordination issue #3 comment 6719659490, https://github.com/j15marti/pnp/issues/3#issuecomment-6719659490; complete page readback found it and its 2,448-byte body exactly equaled the committed outbox.
- Published checker replay: 224 implications, 8,224 syntactic nodes, maximum 49, exact peer aggregates, explicit Resolution/XOR gadgets PASS; historical baseline accepted and hostile LOCAL3 tag rejected.
- **TRACKERS REVIEWED; NO MATERIAL CHANGE BY LSPV-5/429.** Complete proof1.txt blob 96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b (18,553 characters); complete post-conflict proof2.txt blob bc6ab7d62dfb2469403b693a616d5906843dbe8f (358,800 characters), including [P2-L3-494]. LSPV-5/429 edited neither.
- Historical R_mix341 grammar/weights, main.tex, all five roles/IDs/titles, schedules, enabled states, and the two-Route-A/three-Route-B allocation were unchanged.

Scope: independent finite validation of [P2-L1-498] and an exact historical-checker rule-tag boundary; not a historical full-mixed lower bound, not a noncircular B3 proof, and not a P-versus-NP resolution. [P2-B1], [P2-C3], [P2-D1], and [P2-B2] remain OPEN.
