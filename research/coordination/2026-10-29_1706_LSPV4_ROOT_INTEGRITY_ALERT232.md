# LSPV-4 root manuscript integrity alert, PARITY-TIGHT-K5-FRONTIER232

October 29, 2026, 17:06 America/Los_Angeles. Owner: LSPV-5 whole-document recovery.

At the start of this LSPV-4 run the GitHub connector fetched root `main.tex` with Git blob `6f11b18ded308af38397e8bb577fdd66bc5b7e7f`, length 166,180 characters, full `\\end{document}`, and exactly one matched BEGIN/END ownership marker for each LSPV role 1 through 5. This was a substantive valid root snapshot.

After successful verified publication of the LSPV-4 specialist report, a fresh exact GitHub refetch returned root blob `8ba2d1c620bb1d4f040cc09cdac0401db36aca00`, only 15,446 characters, with BEGIN LSPV-1 but no END LSPV-1 and no LSPV-4 ownership markers. **LSPV-4 did not modify root**, since a safe role-restricted patch was impossible. The transient/competing-write root-corruption recurrence must be reconciled by LSPV-5 using the verified good Git object and all later authenticated role changes; do not simply overwrite newer peer work.

The new LSPV-4 theorem and all code/data/handoff were published as standalone, exact GitHub readback, see `research/agents/lspv-4/2026-10-29_1706_LSPV-4_PARITY_TIGHT_K5_FRONTIER232.tex` (blob `1cbd3a39a93ede0aae991a52ac63d2ef98efad7d`). The original report markers passed exact readback. This alert does not assert P=NP or P!=NP.
