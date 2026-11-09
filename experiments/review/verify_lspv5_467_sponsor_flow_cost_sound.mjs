#!/usr/bin/env node
// Independent exhaustive Hall/max-flow replay for the sponsor-flow interface.
import fs from "node:fs";

const rawPath = process.argv[2];
if (!rawPath) throw new Error("usage: node verify...mjs RAW.json");
const raw = JSON.parse(fs.readFileSync(rawPath, "utf8"));

function hall(elig, demands, caps) {
  const m = demands.length;
  for (let subset = 1; subset < (1 << m); subset++) {
    let demand = 0;
    const neighbors = new Set();
    for (let u = 0; u < m; u++) if ((subset >> u) & 1) {
      demand += demands[u];
      for (const v of elig[u]) neighbors.add(v);
    }
    let capacity = 0;
    for (const v of neighbors) capacity += caps[v];
    if (demand > capacity) return false;
  }
  return true;
}

function maxflow(elig, demands, caps) {
  const m = demands.length, n = caps.length;
  const source = 0, sink = 1 + m + n, size = sink + 1;
  const cap = Array.from({length: size}, () => Array(size).fill(0));
  const total = demands.reduce((a, b) => a + b, 0);
  demands.forEach((d, u) => {
    cap[source][1 + u] = d;
    for (const v of elig[u]) cap[1 + u][1 + m + v] = total;
  });
  caps.forEach((c, v) => { cap[1 + m + v][sink] = c; });
  let flow = 0;
  while (true) {
    const parent = Array(size).fill(-1); parent[source] = source;
    const queue = [source];
    for (let qi = 0; qi < queue.length && parent[sink] < 0; qi++) {
      const x = queue[qi];
      for (let y = 0; y < size; y++) if (parent[y] < 0 && cap[x][y] > 0) {
        parent[y] = x; queue.push(y);
      }
    }
    if (parent[sink] < 0) break;
    let aug = total;
    for (let y = sink; y !== source; y = parent[y]) aug = Math.min(aug, cap[parent[y]][y]);
    for (let y = sink; y !== source; y = parent[y]) {
      const x = parent[y]; cap[x][y] -= aug; cap[y][x] += aug;
    }
    flow += aug;
  }
  return flow === total;
}

function* tuples(values, length, prefix = []) {
  if (prefix.length === length) { yield prefix; return; }
  for (const v of values) yield* tuples(values, length, [...prefix, v]);
}

let cases = 0, mismatches = 0, localGlobal = 0;
for (let m = 1; m <= raw.max_side; m++) for (let n = 1; n <= raw.max_side; n++) {
  const masks = Array.from({length: (1 << n) - 1}, (_, i) => i + 1);
  for (const ms of tuples(masks, m)) {
    const elig = ms.map(mask => Array.from({length: n}, (_, v) => v).filter(v => (mask >> v) & 1));
    for (const demands of tuples([1, 2, 3], m)) for (const caps of tuples([0, 1, 2, 3], n)) {
      const h = hall(elig, demands, caps), f = maxflow(elig, demands, caps);
      cases++; if (h !== f) mismatches++;
      const local = demands.every((d, u) => elig[u].some(v => caps[v] >= d));
      if (local && !h) localGlobal++;
    }
  }
}

const checks = {
  producer_pass: raw.status === "PASS",
  case_count: cases === raw.counts.cases,
  zero_mismatch: mismatches === 0 && raw.counts.hall_flow_mismatches === 0,
  local_global_count: localGlobal === raw.counts.locally_safe_globally_unsafe,
  shared_duplicate_rejected: !raw.explicit_controls.shared_duplication.hall_feasible,
  scaled_partition_accepted: raw.explicit_controls.scaled_half_partition.hall_feasible,
  context_loss_detected:
    raw.explicit_controls.context_erased.hall_feasible &&
    !raw.explicit_controls.context_exact.hall_feasible,
};
const pass = Object.values(checks).every(Boolean);
console.log(JSON.stringify({pass, checks, cases, localGlobal}));
if (!pass) process.exit(1);
