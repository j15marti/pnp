# LSPV-5/453 publication receipt

**Pacific run time:** 2026-11-08 22:50 PST  
**Tracker commit:** `4ae91d88d825be26d61eed2e001ce28ccdff32f7`  
**Pre-tracker-write main head:** `afdf8887fca222bbb5af48dc70374bedce8b4026`  
**Conflict control:** the complete current tracker was fetched and replacement used its exact current blob SHA. The write succeeded; later peer commits preserved `[P2-L5-453]` exactly once.

Tracker inputs immediately before the tracker write:

* `proof1.txt`: complete blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, 18,553 UTF-8 characters; unchanged.
* `proof2.txt`: complete blob `f4085484ae51028d22b6b81a9168b8b9d597cd89`, 645,070 UTF-8 characters; current peer `[P2-L4-513]` preserved.

Immediate tracker result at commit `4ae91d...`:

* `proof2.txt`: complete blob `1ae4bd7d53cf61fc5d807f5f2fddfc4b737bafae`, 647,502 UTF-8 characters, `[P2-L5-453]` present.

Full later-current readback after peer commit `d32affece08379ee698d75d8b50ef5c64f6bc560`:

* `proof1.txt`: blob `96aefb3dce074afa81d0ca9b5bcd726b2ca7e76b`, unchanged.
* `proof2.txt`: blob `9ab6e9155c495b5aa405d7d9715eef63efe08267`, 647,803 UTF-8 characters; `[P2-L5-453]` occurs exactly once and the peer update is preserved.

Published files and complete readback blob SHAs:

* report `d592af5dad8c92027427f232d315f536f90aac33`
* producer `782be47f6f46c9c67a851f6019835793c1617d55`
* independent verifier `d6add62a57dea997ff50e49a8c16f11234493589`
* raw JSON `b36c1fe7482084bbdc7b422a32b05238d8fea994`
* verification transcript `9922ccdbf88253a6784ed1326387e15006202ae0`
* fallback manuscript insertion `8042b7ebc6244685568b9a7d59e1e35fec2fb1b5`
* five-role handoff `a4d343b2707aed1c63cb812313be10ca6cf214cd`
* issue outbox `a23430108c3af1823c1169e7a368a973b9ed8dc7`

Every listed file was refetched from `main`; its content exactly matched the local outbox. Issue #3 comment `6734200968` was refetched from the GitHub API in full and contains `[P2-L5-453]`, `[P2-L5-452]`, `[P2-D1]`, `[P2-C3]`, `[P2-B1]`, and `[P2-B2]`.

Root `main.tex` blob `fcb1ed08ec2e55bcbcf37f1dbfef2ea2bbe418ba` still returned zero readable bytes and was not edited. No task, role, title, schedule, timezone, enabled state, five-agent allocation, historical grammar, or historical weight changed. P versus NP remains OPEN.
