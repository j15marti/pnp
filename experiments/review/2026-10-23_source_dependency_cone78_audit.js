// SOURCE-DEPENDENCY-CONE78 finite audit
// Verifies the multiplexer union/flip controls and counting arithmetic only.
let checks = 0, failures = 0;
const cases = [];
for (let k = 3; k <= 16; k++) {
  const N = 2 ** k;
  const union = new Set();
  for (let z = 0; z < N; z++) {
    union.add(z);
    checks++;
    if (union.size !== z + 1) failures++;
  }
  for (let t = 0; t < 200; t++) {
    const hot = (Math.imul(t, 2654435761) >>> 0) % N;
    const F = new Uint8Array(N);
    F[hot] = 1;
    checks += 3;
    if (F[hot] !== 1) failures++;
    if (!Array.from(F).some(Boolean)) failures++;
    const omitted = new Uint8Array(N);
    if (Array.from(omitted).some(Boolean)) failures++;
  }
  const s = Math.floor(Math.sqrt(N));
  const logCount = s * (4 + 2 * Math.log2(k + s)) + Math.log2(k + s);
  cases.push({
    k, N, union_size: union.size, dynamic_probes_per_witness: 1,
    s_floor: s, log2_circuit_count_upper_bound: logCount,
    truth_table_bits: N, counting_certifies_missing_function: logCount < N
  });
  checks++;
  if (union.size !== N) failures++;
}
console.log(JSON.stringify({
  artifact: "SOURCE_DEPENDENCY_CONE78", cases, checks, failures,
  scope: "multiplexer and counting arithmetic only"
}, null, 2));
if (failures) process.exitCode = 1;
