# Exact-one cluster augmentation
Same pins and exact instance IDs as report.md. Enumerate bounded local clauses (or extract single excluded row directly), combine a signed at-least-one clause and all complementary pairs into an exact-one table, then acquire its local annihilator basis. Sound because the first clause enforces at least one and pairs enforce at most one. All parents retain their factor IDs. No reference label used during discovery. Exact-one cluster added, not substituted for parents. First attempt stopped on width>7 original CNF; repeated with direct single-excluded-word extraction and skipped unsupported wide tables. Failed attempt charged but not fully metered. All tests executed in JS isolate, sequentially. [
  {
    "id": "EB-JOINT-24",
    "lanes": {
      "native": {
        "groups": 12,
        "partial": 0,
        "wordChecks": 0,
        "pairChecks": 106,
        "directWords": 478,
        "skipped": 0,
        "results": [
          {
            "status": "UNSAT",
            "D": 2,
            "n": 27,
            "rank": 336,
            "monomials": 373,
            "rows": 576,
            "xor": 3221,
            "localChecks": 11010,
            "multiples": 576,
            "certificateTerms": 56
          },
          {
            "status": "UNSAT",
            "D": 3,
            "n": 27,
            "rank": 3261,
            "monomials": 3300,
            "rows": 11350,
            "xor": 81660,
            "localChecks": 17952,
            "multiples": 11350,
            "certificateTerms": 321
          }
        ]
      },
      "cnf": {
        "groups": 15,
        "partial": 0,
        "wordChecks": 0,
        "pairChecks": 155,
        "directWords": 465,
        "skipped": 0,
        "results": [
          {
            "status": "UNSAT",
            "D": 2,
            "n": 24,
            "rank": 300,
            "monomials": 301,
            "rows": 685,
            "xor": 6960,
            "localChecks": 24092,
            "multiples": 685,
            "certificateTerms": 133
          },
          {
            "status": "UNSAT",
            "D": 3,
            "n": 24,
            "rank": 2325,
            "monomials": 2325,
            "rows": 12471,
            "xor": 207663,
            "localChecks": 51288,
            "multiples": 12471,
            "certificateTerms": 461
          }
        ]
      },
      "hybrid": {
        "groups": 12,
        "partial": 0,
        "wordChecks": 0,
        "pairChecks": 89,
        "directWords": 325,
        "skipped": 0,
        "results": [
          {
            "status": "UNSAT",
            "D": 2,
            "n": 24,
            "rank": 270,
            "monomials": 298,
            "rows": 484,
            "xor": 2810,
            "localChecks": 6106,
            "multiples": 484,
            "certificateTerms": 109
          },
          {
            "status": "UNSAT",
            "D": 3,
            "n": 24,
            "rank": 2297,
            "monomials": 2324,
            "rows": 8277,
            "xor": 59369,
            "localChecks": 8577,
            "multiples": 8277,
            "certificateTerms": 258
          }
        ]
      }
    }
  },
  {
    "id": "EB-RANDOM-3CNF-40",
    "lanes": {
      "native": {
        "groups": 0,
        "partial": 0,
        "wordChecks": 0,
        "pairChecks": 184,
        "directWords": 619,
        "skipped": 0,
        "results": [
          {
            "status": "UNKNOWN",
            "D": 2,
            "n": 40,
            "rank": 0,
            "monomials": 1,
            "rows": 0,
            "xor": 0,
            "localChecks": 9016,
            "multiples": 0,
            "dualChecks": 0,
            "dualTerms": 1
          },
          {
            "status": "UNKNOWN",
            "D": 3,
            "n": 40,
            "rank": 184,
            "monomials": 455,
            "rows": 184,
            "xor": 1,
            "localChecks": 10304,
            "multiples": 184,
            "dualChecks": 184,
            "dualTerms": 31
          }
        ]
      },
      "cnf": {
        "groups": 0,
        "partial": 0,
        "wordChecks": 0,
        "pairChecks": 184,
        "directWords": 653,
        "skipped": 0,
        "results": [
          {
            "status": "UNKNOWN",
            "D": 2,
            "n": 40,
            "rank": 0,
            "monomials": 1,
            "rows": 0,
            "xor": 0,
            "localChecks": 9016,
            "multiples": 0,
            "dualChecks": 0,
            "dualTerms": 1
          },
          {
            "status": "UNKNOWN",
            "D": 3,
            "n": 40,
            "rank": 184,
            "monomials": 451,
            "rows": 184,
            "xor": 1,
            "localChecks": 10304,
            "multiples": 184,
            "dualChecks": 184,
            "dualTerms": 24
          }
        ]
      },
      "hybrid": {
        "groups": 0,
        "partial": 0,
        "wordChecks": 0,
        "pairChecks": 184,
        "directWords": 620,
        "skipped": 0,
        "results": [
          {
            "status": "UNKNOWN",
            "D": 2,
            "n": 40,
            "rank": 3,
            "monomials": 8,
            "rows": 3,
            "xor": 0,
            "localChecks": 9052,
            "multiples": 3,
            "dualChecks": 3,
            "dualTerms": 3
          },
          {
            "status": "UNKNOWN",
            "D": 3,
            "n": 40,
            "rank": 295,
            "monomials": 655,
            "rows": 307,
            "xor": 14,
            "localChecks": 10340,
            "multiples": 307,
            "dualChecks": 307,
            "dualTerms": 34
          }
        ]
      }
    }
  }
]
The static row span is not the full degree-bounded PC closure. The dual proves only refusal relative to the specified generating rows. Costs are partial event counts, not aggregate bit-time. Independent review pending. P versus NP OPEN.
