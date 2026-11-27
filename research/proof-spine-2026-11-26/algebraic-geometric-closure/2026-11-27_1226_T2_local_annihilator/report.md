# T2 local annihilator span with dual refusal
2026-11-27 12:26 PT. Scoped proof, finite computational audit; P versus NP OPEN.

Inputs: pinned strict EB4 compiler, corpus, registry, T1 helper and two T1 certificates in this exact argument order: [["21b9d53fb8166c819b24e708656c742cd3c24f10","research/coordination/shared-eb-2026-11-27/compile.js"],["e315349cd6c1fe3fa696504859f28312f6aab69a","research/coordination/shared-unsat-2026-11-27/benchmarks.json"],["0c14cdc57925788cf7a451dcd5aa171dce860f2c","research/coordination/shared-eb-2026-11-27/instance-registry-v1.json"],["a830475f2d7b927fe3897079af04ebb99c82106b","research/hcl201/matching/2026-11-27_T1_hall_clause_feedback/experiment.js"],["0231a616afbf28cf297c6b9c3f7b509b48d2fe04","research/hcl201/matching/2026-11-27_T1_hall_clause_feedback/JOINT-24-certificate.json"],["e4ade84c3056664411885a65e334a550bbc59c93","research/hcl201/matching/2026-11-27_T1_hall_clause_feedback/RANDOM-3CNF-40-certificate.json"]]. Exact SHA256/N of native bytes, DIMACS bytes and map checked. Empty guard and root input, gauge by global complement symmetry, equality and signed edge normalization by BFS and DSU; checked bounded bucket projections. Source-only initial discovery before importing T1. The code uses original carrier IDs (minimum original port plus one), factor IDs and trace; native mapping and residual bytes reproducible from the pinned helper. Initial and post-import support closure. Separate original CNF experiment. All execution sequential in JS isolate, no independent Node process.

## Lemma (local annihilator multiples)
Let F be explicit Boolean relations on named scopes, with every local table exact. In the Boolean ring F2[x]/(x_i^2+x_i), fix D. On each scope form the evaluation map on allowed rows from monomials of degree <=D. Its kernel is exactly the space of degree-bounded polynomials vanishing on the allowed table. Column elimination gives a basis with explicit local polynomial provenance. For each basis polynomial p of degree d, generate p times every squarefree monomial of degree <=D-d, reducing repeated factors by idempotence. The resulting row space V_D consists of sound consequences. If 1 belongs to V_D, the explicit row combination is a refutation; if it does not, triangular elimination produces a dual linear functional L with L(1)=1 and L(r)=0 for every generated row. This certifies refusal of this precise finite terminal, not satisfiability, not the full polynomial calculus degree-D closure, and not arbitrary decision hardness. The local kernel is not restricted to the original single violation indicator; this is a hybrid of exact local table projection and global monomial coefficient elimination. For fixed D, bounded explicit table width O(log N), and polynomially many polynomial-size tables, the row generation, index size, dense GE and proof/dual verification are polynomial in original N; a naive bound poly(N) times N^{O(D)}. Width/coefficients one-bit field elements, index bit cost polynomial. Local truth-table checks can turn each p into a pointwise failure certificate via p=p*f_table. Balanced products/sums then give O(log(N+S)) evaluation depth for attained polynomial-size explicit certificate S, not discovery depth. No complete unrestricted coverage theorem.

Results: [
  {
    "id": "EB-JOINT-24",
    "gauge": 11,
    "projection": {
      "count": 615,
      "checks": 12330,
      "scans": 618966,
      "verifyTests": 12330,
      "verifyScans": 218000
    },
    "closure": {
      "pins": [],
      "scans": 1277
    },
    "peer": {
      "sha": "75fb830677e51f8bd73b3e77510d7a1eae057a269aae4e333f30f654b2ee7c4b",
      "scans": 17967,
      "prefix": [
        {
          "kind": "UP",
          "clause": [
            -618
          ]
        },
        {
          "kind": "UP",
          "clause": [
            -250
          ]
        },
        {
          "kind": "UP",
          "clause": [
            -546
          ]
        }
      ]
    },
    "hybridClosure": {
      "pins": [
        [
          618,
          0,
          -1
        ],
        [
          250,
          0,
          -2
        ],
        [
          546,
          0,
          -3
        ]
      ],
      "scans": 4497
    },
    "lanes": {
      "native": [
        {
          "status": "UNKNOWN",
          "D": 2,
          "n": 27,
          "rank": 129,
          "monomials": 130,
          "rows": 155,
          "xor": 26,
          "localChecks": 10342,
          "multiples": 155,
          "dualChecks": 155,
          "dualTerms": 1
        },
        {
          "status": "UNKNOWN",
          "D": 3,
          "n": 27,
          "rank": 2298,
          "monomials": 2309,
          "rows": 4346,
          "xor": 2100,
          "localChecks": 16904,
          "multiples": 4346,
          "dualChecks": 4346,
          "dualTerms": 4
        }
      ],
      "cnf": [
        {
          "status": "UNKNOWN",
          "D": 2,
          "n": 24,
          "rank": 129,
          "monomials": 130,
          "rows": 155,
          "xor": 26,
          "localChecks": 22722,
          "multiples": 155,
          "dualChecks": 155,
          "dualTerms": 1
        },
        {
          "status": "UNKNOWN",
          "D": 3,
          "n": 24,
          "rank": 1909,
          "monomials": 1916,
          "rows": 3879,
          "xor": 2020,
          "localChecks": 48600,
          "multiples": 3879,
          "dualChecks": 3879,
          "dualTerms": 4
        }
      ],
      "hybrid": [
        {
          "status": "UNKNOWN",
          "D": 2,
          "n": 24,
          "rank": 91,
          "monomials": 94,
          "rows": 108,
          "xor": 17,
          "localChecks": 5526,
          "multiples": 108,
          "dualChecks": 108,
          "dualTerms": 1
        },
        {
          "status": "UNKNOWN",
          "D": 3,
          "n": 24,
          "rank": 1532,
          "monomials": 1566,
          "rows": 2705,
          "xor": 1241,
          "localChecks": 7721,
          "multiples": 2705,
          "dualChecks": 2705,
          "dualTerms": 4
        }
      ]
    }
  },
  {
    "id": "EB-RANDOM-3CNF-40",
    "gauge": 11,
    "projection": {
      "count": 552,
      "checks": 9568,
      "scans": 542616,
      "verifyTests": 9568,
      "verifyScans": 186300
    },
    "closure": {
      "pins": [],
      "scans": 1714
    },
    "peer": {
      "sha": "a1af0f81183d9681db016bbc2381e77273c04da3e16f93e7eb34bbc4de48dda9",
      "scans": 47440,
      "prefix": [
        {
          "kind": "UP",
          "clause": [
            362,
            34
          ]
        },
        {
          "kind": "UP",
          "clause": [
            362,
            -33
          ]
        },
        {
          "kind": "UP",
          "clause": [
            362,
            298
          ]
        }
      ]
    },
    "hybridClosure": {
      "pins": [],
      "scans": 1727
    },
    "lanes": {
      "native": [
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
      ],
      "cnf": [
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
      ],
      "hybrid": [
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
]

Cost: cap 2,000,000 global row XORs per lane; other measured local evaluations, row counts and projection counters above. No full bit-time, peak/cumulative memory or aggregate shared cap measured; bigint width bounded by number of monomials and rows, not unit cost. Failed scans, hash generation, normalization, indexing, local kernel operations, proof replay, serialization and tool transfer additional. Source-only native and CNF lanes separate; imported prefix first independently replayed in full using reverse unit propagation, then reclosed. Parent certificates are not free discovery. Dual checks all generated rows; primal checks exact combination. Controls: consistent and inconsistent two-variable equality systems. No actual full expanded syzygy circuit, separate host or Lean build. No new claim beyond named representation. DISJ: no branch disjunction in row span; gauge symmetry discharged. Relativization/algebrization/Natural Proofs no bypass; DTISP and configuration bounds no unrestricted transfer. Matching existence vs permanent and compact circuit bypass remain valid controls. Falsifiers: a local annihilator nonzero on allowed word; corrupt row combination; dual with nonzero evaluation on any row; universal sufficiency claimed from fixed D. No MFC13/transport rerun. First open arrow: universal acquisition of a productive certificate with polynomial aggregate bit work. Next: adaptive guarded local annihilator generation with global costed coverage. Independent review pending. No public release or scheduler change.
