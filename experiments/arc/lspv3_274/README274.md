# HORN-AFFINE-MIXED-GATE274: exact source-certified SAT controls

Status: KNOWN THEOREM TRANSFER / PROVED-EXACT RESTRICTED (independent mathematical referee pending); COMPUTATIONAL checks. General ARC and P versus NP OPEN.

## Reproduce

Requires Python 3 standard library only. Work from the extracted folder:

    python run274.py
    python verify274.py THREE_SAT_MIDDLE THREE_UNSAT_FULL HORN3_SAT POSITIVE3_SAT XOR3_SAT
    python verify274.py SWAP6_SAT W1_UNSAT
    python verify274.py SWAP6_RENAMED_SAT W1_RENAMED_UNSAT
    python verify274.py RANDOM3_SEED11 RANDOM3_SEED12
    python controls274.py

The producer enumerates coherent original assignments and creates raw274.json and summary274.json. The independent checker does not import the producer. It checks original indexed clauses, original all-S/all-U target assignments, inverted targets, clause-pair SS/SU/US/UU, Gray/complement, SAT witnesses, complete original-source UNSAT proof trees, per-occurrence and mixed-encoding projection. Fixtures are deterministic, no random seed is drawn during reproduction.

The gzip/base64 raw asset is a GitHub-portable exact snapshot. To reconstruct:

    import base64, gzip, pathlib
    p=pathlib.Path('raw274.json.gz.b64')
    pathlib.Path('raw274-restored.json').write_bytes(gzip.decompress(base64.b64decode(p.read_bytes())))

Independent mixed-source DPLL operations are host-language instrumentation and are not native FLMV machine resources. Full mixed-source DPLL was intentionally not run for the 20+ clause originals.

## Results

11 original controls: 8 SAT and 3 UNSAT, checked independently. Two small sources have 7 and 8 original clauses; their mixed forms have 91 and 104 proper clauses, baseline UP-first DPLL 117 and 207 nodes. Recovered ordinary child DPLL used 6 and 7 nodes, respectively. No polynomial advantage or power-short ARC child is claimed.

Files are also committed individually to j15marti/pnp under research/agents/lspv-3, experiments/arc/lspv3_274, results/raw/arc and results/summaries.