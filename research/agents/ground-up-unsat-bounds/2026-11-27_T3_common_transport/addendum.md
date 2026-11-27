# Addendum: exact core count and external source authentication

2026-11-27. The main report at 8ad07652c581e4dd173be947177aaf83e89ceb54 contains one transcription error: the JOINT-24 hybrid source subformula contains **149**, not 146, original clauses, as counted directly from the verified results.json peer.chart.used array. No proof, computation, or measured metric changes. Preserve the original report.

Additional fresh connected reads establish these exact Git blob identities (not independent builds):
- anthropics/formal-math eth/README.md: 0b3dcf4a858ff802b3275fc5999ffb134c74de60.
- openai/math lean/docs/378.md: 223bbe187394bffca8a2c7ba1656538bfba26e3b.
- google/or-tools ortools/sat/sat_parameters.proto: 57202e89a891ca09187cd6672809b5a046941f18 (default branch; web search separately surfaced stable).
- marijnheule/drat-trim README.md: eb6ffcc4a85ff1c74a5995b6caae4372381dcd47.
- msoos/cryptominisat README.md: 7636988713ee16802b84fb1cdf688ea8f87da70e. README.markdown returned 404 before correct path recovered.
- xai-org code search SAT solver: grok-build UI/login/trace files, no applicable mathematical solver. google-deepmind same query: mujoco solver.py, formal-conjectures ErdosProblems/895.lean, torax solver documentation, no applicable transport proof or implementation.
The paper's claims and external implementations are not imported as proof dependencies or executed in this run. No scheduler changes.