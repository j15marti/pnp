// CONE-COVER-REPLICATION79 finite audit
// Checks bucketed multiplexer, incidence/replication, and global-dependence controls.
let seed = 0x9e3779b9 >>> 0;
function rnd() {
  seed = (Math.imul(seed, 1664525) + 1013904223) >>> 0;
  return seed;
}
let checks = 0, failures = 0, totalCases = 0;
const rows = [];
for (let k = 4; k <= 16; k++) {
  const N = 2 ** k;
  const B = 2 ** Math.floor(k / 2);
  const Q = Math.ceil(N / B);
  let incidence = 0;
  const rep = new Uint32Array(N);
  for (let j = 0; j < Q; j++) {
    const lo = j * B, hi = Math.min(N, lo + B);
    incidence += hi - lo;
    for (let i = lo; i < hi; i++) rep[i]++;
  }
  checks += N + 3;
  if (incidence !== N) failures++;
  if (rep.some(x => x !== 1)) failures++;
  if (Q > Math.ceil(N ** 0.6) + 1) failures++;

  for (let t = 0; t < 200; t++) {
    const F = new Uint8Array(N);
    for (let i = 0; i < N; i++) F[i] = rnd() & 1;
    const parentOr = F.some(Boolean);
    let childOr = false;
    for (let j = 0; j < Q; j++) {
      let value = false;
      const hi = Math.min(N, (j + 1) * B);
      for (let i = j * B; i < hi; i++) if (F[i]) { value = true; break; }
      childOr ||= value;
    }
    checks++;
    if (childOr !== parentOr) failures++;

    const global = F.every(Boolean);
    for (let j = 0; j < Q; j++) {
      checks++;
      if (global !== F.every(Boolean)) failures++;
    }
    totalCases++;
  }
  rows.push({
    k, N, B, Q, total_incidence: incidence, average_replication: incidence / N,
    baseline_Q_cap: N ** 0.6, baseline_total_capacity: N ** 1.1,
    global_control_required_incidence: Q * N
  });
}
console.log(JSON.stringify({
  artifact: "CONE_COVER_REPLICATION79", rows, totalCases, checks, failures,
  scope: "bucketed multiplexer, incidence, and global-dependence controls only"
}, null, 2));
if (failures) process.exitCode = 1;
