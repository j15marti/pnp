# Raw manifest — SIGNED-NAE-OCC2-COVERAGE-REFEREE216

The local monolithic JSON is 7,514,047 bytes with SHA-256
`2fb64abf23a6771e5b16d1b2a17a0aa2d5c9c758fa67443b8e9c976442134c95`.
For reviewable GitHub writes it is published as:

- `..._classes.json`: theorem-class enumeration and total counters;
- `..._summary.json`: compact class, endpoint and solver-accounting summary;
- `..._raw.json.gz.b64`: the complete monolithic JSON, gzip-compressed and
  base64-encoded as plain text for the GitHub connector.  Recover with
  `base64 -d FILE | gzip -dc > raw.json`.

The base64/gzip file decompresses byte-for-byte to the monolith with the
SHA-256 above.  It contains source clauses, per-clause/per-occurrence S/U
targets and both inversions, exact pair and bounded multi-clause compatibility,
endpoint statuses, intermediate flip trails, resolution provenance,
prohibited cubes, models, checks, and solver counters.

The reproducer records the SHA-256 of its run214 dependency and regenerates
the monolith deterministically from seed 202610300048 in under six seconds on
the reported host.
