# T2 gauge-equivariant guarded syzygy and five-lane comparison | 2026-11-27 Pacific

Status: PROVED WITH SCOPE (independent peer review pending); COMPUTATIONAL for benchmark traces. P versus NP OPEN. Native STRICT-EB4-v1: simple 4-regular graph, signed XOR edges, E equality, B integer weight two. Both native exact SHA-256/N, CNF SHA-256/N and source-map hashes checked with standard SHA test vectors and pinned compiler; normalized via two distinct BFS/DSU routines, verified bounded projection. Source pins in certificate and runner, registry 0c14cdc57925788cf7a451dcd5aa171dce860f2c, corpus e315349cd6c1fe3fa696504859f28312f6aab69a, compiler 21b9d53fb8166c819b24e708656c742cd3c24f10, helper a830475f2d7b927fe3897079af04ebb99c82106b. Native source-only discovery first; no reference proof used. Direct CNF and peer-assisted runs separate. All five lanes serial (no independent workers used; not a concurrent experiment).

## Lemma: gauge-equivariant guarded first-failure syzygy

On the signed E/edge affine carrier let f_j be local Boolean failure indicators. Under guard P (product of its literal satisfaction indicators), a checked table propagation trail forces L_1,...,L_u (each L_j equals 1 when the forced literal is satisfied) and finally contradicts f_*. A valid identity on the carrier in the Boolean ring F2 is

P = sum_j P prod_{h<j} L_h (1+L_j) f_j + P prod_{h<=u} L_h f_*.

Proof: at any point outside P all terms vanish. Inside P, the first failed L_j, if any, activates exactly one term. Its local table cannot be satisfied under the verified predecessor pins, hence f_j=1. All subsequent products vanish. If no L_j fails, the checked final conflict has f_*=1. This proves the identity on every Boolean word of the carrier. The factor (1+L_j) is essential for general relation tables: a table may fail even when the forced literal holds (relation {(0,0)}, forced x=0, word (0,1)). For CNF unit reasons the smaller previous clause formula remains valid because failure is exactly the failed unit within the predecessor guard.

Every native failure indicator is invariant under global complement. The E/edge affine carrier is invariant too, even with signed edges. Fix original anchor a and gauge x_a=1. On that gauge the relative guard e(y) depends on y_v=x_v+x_a. Let an acquired identity e=sum_i q_i f_i hold on the gauge slice. Pull back by r(x)=x+(1+x_a)1. Then r(x) is in the gauge slice and f_i(r(x))=f_i(x); e(y(r(x)))=e(y(x)). Thus e(y(x))=sum_i q_i(r(x))f_i(x) on the whole original affine carrier. No anchor-indicator factor and no double counting. Affine substitution cannot increase Boolean degree of the represented gauge polynomials; compact circuit size grows by at most O(N) for shared affine coordinate inputs, plus the attained proof size. This is a certificate lifting theorem, not an assertion of a small expanded coefficient dictionary or universal discovery. For propagation trail size S, naive construction O(S^2+N) gates, balanced masks and final sum O(log(N+S)) evaluation depth, one-bit coefficients. Local verification polynomial in explicit table/trace size; charge native normalization and every failed acquisition. If original affine equality constraints are to be removed from the proof premises, a separate equality-ideal lift is required; here they are retained.

## Five independent methods and common guards
Five methods: GAC occupancy, quadratic local annihilator span, exact binary implication reachability, width-6 bucket elimination, depth-2 guarded proof tree. The 2-SAT relaxation is the complementary alternative to matching; no matching implementation or Hall claim. Each received same verified projected chart and all four assignments to two highest-occurrence carriers; cap 200000 mixed events per lane across all four guards. Root GAC performed before and after projection; after peer imports a closure scan was performed on the combined batch, not after each individual import. The tests count distinct mathematical methods but were serial, not simultaneous/interleaved. No probabilistic lane completed this run; five-guard acquisition is incomplete.

JOINT: carrier count 29, four guards on carriers 11,618 (ports 10,617), occupancy and guarded DAG each refute unequal bits, other three stall. Union 2/4, intersection of successful lanes 2/4. After verified imports all five refute those same two; equal-bit guards remain UNKNOWN. RANDOM: 41 carriers, four guards on carriers 11,17, all five stall, including after imports. Imported peer complementary guards on 4 original carriers exclude exactly 2/16 of those words, but none of the tested 2-bit fibers wholly. No full five-guard cover. Direct CNF: JOINT 3/4 tested guards excluded by occupancy/DAG and 1/4 by each of algebra/binary/bucket, RANDOM 0/4. Direct CNF IDs in raw output, not merged with native guard IDs. No new root refutation.

Native lane events JOINT 7380/36061/82469/2944/18796, sum 147650; RANDOM 10304/41452/97156/4248/50680, sum 203840. Hybrid sums JOINT 152229, RANDOM 205538. Direct CNF 127079 and 176549. Projection discovery checks/scans 9438/736892 and 8096/644368, independent replay tests/scans 18876/217826 and 16192/186300. Peer core guard replay events 40770 and 1644. Peer original core contents, guard IDs and certificate bytes verified, each guard and its complement independently replayed by GAC/width-6 buckets on recorded original B subset (duplicate normalized constraints may include additional original B owners with identical relation; no unrelated constraint added). Peer child residual serialization itself not independently authenticated; only guard and exact original owner support replay used. Six and two new local guard tables imported respectively. Initial native GAC supports and local tables in raw output. No claim of comparable bit-time, as counts mix operations; hashing, indexing, allocation, communication, GE bit widths, memory peak/cumulative, and complete end-to-end costs uninstrumented. Thus no measured aggregate speedup.

## New algebraic certificates
EB-JOINT-24@e84a0ab6dc6f N=5363624: STRICT-EB4-v1:sha256:e84a0ab6dc6f74deb8daeea2ccd41cca90e3d1294411877a813471760897c209; root guard EMPTY/residual ROOT; child GUARD-v1:sha256:4ebf28f655d1a357e87b5bb345a4b379b7ca1993450c1ab8e27d4dd3c79bc0d4, guarded residual RESIDUAL-v1:sha256:7daad12cc3ab07e2dfdab387c30affac7a5b04253e28c058bd83c4db79da8a65; cert CERT-v1:sha256:1c537726eddbc527aded1f3328f034c21d6dc90aa7de52017cd9721a39c075fa; https://github.com/j15marti/pnp/blob/a4b5842a3b897e0a6da8d4bafa755d8f092a5948/research/proof-spine-2026-11-26/algebraic-geometric-closure/2026-11-27_T2_guard_lift_five_lanes/EB-JOINT-24-lift-certificate.json. Original B owners 138, first peer guard core 76, intersection 56, union 158. Discovery row visits 5064, independent allowed-row checks 516, complement table checks 1104, orbit truth checks 4. 86 compact first-failure terms. JOINT guard chosen by standalone lane; RANDOM guard choice from peer, reproved independently. Algebraic consequence is new representation of an already known semantic guard exclusion, not a new exclusion. All E and signed edge premises retained. Parent link https://github.com/j15marti/pnp/issues/328#issuecomment-7229096080.

EB-RANDOM-3CNF-40@8a18e86479df N=5027816: STRICT-EB4-v1:sha256:8a18e86479df916ea5c7fdd760ccd561e4fea3737a94517ab8dc2d28cc7e6bdb; root guard EMPTY/residual ROOT; child GUARD-v1:sha256:632edb34757c225132dd951002b78b97208a4e580ac29aacc40687fd0fb5c237, guarded residual RESIDUAL-v1:sha256:153c5a9b5053614056a9b2ecd00a334f284c43c93d12d39d0218bf05a81836fb; cert CERT-v1:sha256:2d4940bb0f1a59b63dfd6c71b422c2d24658f8c1b9814dc56a00f4e04556c2ec; https://github.com/j15marti/pnp/blob/226276801d2298be77d0977c794e165286e65d87/research/proof-spine-2026-11-26/algebraic-geometric-closure/2026-11-27_T2_guard_lift_five_lanes/EB-RANDOM-3CNF-40-lift-certificate.json. Original B owners 142, first peer guard core 64, intersection 62, union 144. Discovery row visits 9282, independent allowed-row checks 690, complement table checks 1136, orbit truth checks 16. 115 compact first-failure terms. JOINT guard chosen by standalone lane; RANDOM guard choice from peer, reproved independently. Algebraic consequence is new representation of an already known semantic guard exclusion, not a new exclusion. All E and signed edge premises retained. Parent link https://github.com/j15marti/pnp/issues/328#issuecomment-7229096461.

JOINT relative indicator x10+x617 (degree 1); RANDOM relative indicator (1+x10+x16)(1+x10+x33)(1+x10+x361) (degree <=3). These are the polynomials in the ideal on the carrier; certificate summands can have much higher degree, no constant-degree proof claim. Pairwise core intersection is not assumed refuting. Artifact checker is independent table replay, not full expanded coefficient checking. Guarded-root manifest gives the authoritative content-addressed guarded residual rather than reusing the original root ID.

## Costs, gates, unresolved arrow
Fixed polynomial after acquired bounded-size traces. Five-guard cover checking by at most 31 GE counts known with scope, but finding covering guards in bounded aggregate cost is OPEN. Equality, pure affine and complement symmetry exact; no perfect matching transfer, no claim from degree or symbolic size about all deciders. DISJ: individual excluded guards not the entire cube; PASS for scoped implications, OPEN universal. Relativization/algebrization/Natural Proofs: no unrestricted separation asserted, not bypassed. Simultaneous DTISP and deterministic-configuration lower bound: not claimed; aggregate bit-time and memory not measured. Falsifiers: wrong guard map, non-complement-invariant factor, omitted failed-literal factor, surviving equal-bit guard; first three are explicitly prohibited/checked, last observed. Secondary MFC-13, Nov 26 replay, transport and probabilistic discovery not run; local preflight and manuscript editing not attempted (connector-only execution). No public release or schedule changes. Next lemma: GUARD-LIFT-OR-BOUNDED-ACQUISITION, prove a fixed-N polynomial search for fresh obstructions on all surviving fibers, or construct a growing simultaneous-stall family for these five exact terminals. Do not treat finite UNKNOWN as a lower bound.

## Source register
Fresh searches: polynomial calculus degree bounds (Miksa/Nordstrom arXiv:1505.01358 and JACM DOI 10.1145/3675668; abstract read, arXiv HTML fetch failed; not a proof dependency), BDD proof generating SAT (PGBDD artifact README: extended resolution/LRAT generation, no universal polynomial bound), Google OR-Tools CP-SAT (README, not used), Google Research tensor contraction optimizer (heuristic, not completeness), Google DeepMind formal conjecture proof guide (kernel verification vs sorry), xAI official reasoning-effort eval cookbook (search surfaced evaluation methodology, no relevant mathematical theorem), Anthropic formal-math VP/VNP statement and README (all fields, HC, permanent char !=2, nonuniform exact +/* circuits, superpolynomial m^(c(log2 m)^(1/3)), approximate theorem separately stated; reported CI success, no independent build), OpenAI math 379 scope (nonuniform exact +,-,* superpolynomial for HC all fields and permanent char !=2; border quantitative bound paper-only in scope note; no independent build). Neither arithmetic claim supplies Boolean transfer. Repository search syzygy branch returned none, issue search returned #328; newest peer guards read and replayed. Pinned/actual external blobs or lookup failures:
[
  {
    "repo": "anthropics/formal-math",
    "path": "vp-vnp/Statement.lean",
    "blob": "e64db90a929defe35d5b76d6eaa9bc0c87843ad3",
    "url": "https://github.com/anthropics/formal-math/blob/main/vp-vnp/Statement.lean"
  },
  {
    "repo": "openai/math",
    "path": "lean/docs/379.md",
    "blob": "b1a856319056d10c922672e8dda0bb924355aaa4",
    "url": "https://github.com/openai/math/blob/main/lean/docs/379.md"
  },
  {
    "repo": "rebryant/pgbdd-artifact",
    "path": "README.md",
    "error": "NOT_FOUND: Error code: NOT_FOUND; Error: GitHub API error 404: {\"message\":\"Not Found\",\"documentation_url\":\"https://docs.github.com/rest/repos/contents#get-repository-content\",\"status\":\"404\"}"
  },
  {
    "repo": "google-research/tnco",
    "path": "README.md",
    "blob": "98624f164ef6b5b29ee869b35642224f58849b7f",
    "url": "https://github.com/google-research/tnco/blob/main/README.md"
  },
  {
    "repo": "google-deepmind/formal-conjectures",
    "path": "PROOFS.md",
    "blob": "edf4eb1afdbf0182fd9ac603d0f23adf97003d4c",
    "url": "https://github.com/google-deepmind/formal-conjectures/blob/main/PROOFS.md"
  },
  {
    "repo": "xai-org/xai-cookbook",
    "path": "examples/reasoning-effort-evals/README.md",
    "blob": "6915a1c413c0edc616caa914873f1e7571021a7f",
    "url": "https://github.com/xai-org/xai-cookbook/blob/main/examples/reasoning-effort-evals/README.md"
  }
]
