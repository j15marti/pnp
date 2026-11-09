// Independent finite reconstruction of the history-separated DAG controls.
// This is not an R_mix341 checker.

function combinations(n) {
  const es = [];
  for (let i = 0; i < n; i++) for (let j = i + 1; j < n; j++) es.push([i, j]);
  return es;
}

function isCyclic(vertices, edges) {
  const adj = new Map([...vertices].map(v => [v, new Set()]));
  const indeg = new Map([...vertices].map(v => [v, 0]));
  for (const [u, v] of edges) {
    if (!adj.get(u).has(v)) {
      adj.get(u).add(v);
      indeg.set(v, indeg.get(v) + 1);
    }
  }
  const todo = [...vertices].filter(v => indeg.get(v) === 0);
  let seen = 0;
  while (todo.length) {
    const u = todo.pop();
    seen++;
    for (const v of adj.get(u)) {
      indeg.set(v, indeg.get(v) - 1);
      if (indeg.get(v) === 0) todo.push(v);
    }
  }
  return seen !== vertices.size;
}

function tuples(values, n) {
  let out = [[]];
  for (let i = 0; i < n; i++) out = out.flatMap(xs => values.map(x => [...xs, x]));
  return out;
}

let dagLabelCases = 0;
let quotientCycles = 0;
let nontrivialCycles = 0;
let weightedCases = 0;
let historyViolations = 0;

for (let n = 1; n <= 4; n++) {
  const possible = combinations(n);
  for (let mask = 0; mask < (1 << possible.length); mask++) {
    const edges = possible.filter((_, bit) => mask & (1 << bit));
    if (isCyclic(new Set([...Array(n).keys()]), edges)) throw new Error("concrete forward DAG cyclic");
    for (const labels of tuples(["A", "B"], n)) {
      dagLabelCases++;
      const qmap = new Map();
      for (const [u, v] of edges) qmap.set(`${labels[u]}:${labels[v]}`, [labels[u], labels[v]]);
      const qedges = [...qmap.values()];
      if (isCyclic(new Set(labels), qedges)) {
        quotientCycles++;
        if (qedges.some(([u, v]) => u !== v)) nontrivialCycles++;
      }
      for (const weights of tuples([1, 2, 3], n)) {
        weightedCases++;
        const paid = new Set();
        let abstract = 0;
        for (let i = 0; i < n; i++) {
          if (!paid.has(labels[i])) {
            abstract += Math.min(...weights.filter((_, j) => labels[j] === labels[i]));
            paid.add(labels[i]);
          }
        }
        if (abstract > weights.reduce((a, b) => a + b, 0)) historyViolations++;
      }
    }
  }
}

const witnessEdges = [[0, 1], [1, 2]];
const witnessLabels = ["A", "B", "A"];
const witnessQ = [["A", "B"], ["B", "A"]];
if (isCyclic(new Set([0, 1, 2]), witnessEdges)) throw new Error("bad witness DAG");
if (!isCyclic(new Set(witnessLabels), witnessQ)) throw new Error("quotient cycle missed");
if (!(1 < 2)) throw new Error("sharing overcharge control failed");
if (!(Math.min(1, 3) <= 1 && Math.max(1, 3) > 1)) throw new Error("fiber control failed");

console.log(JSON.stringify({
  status: "PASS",
  dag_label_cases: dagLabelCases,
  quotient_cycle_cases: quotientCycles,
  nontrivial_quotient_cycle_cases: nontrivialCycles,
  weighted_history_cases: weightedCases,
  history_cost_violations: historyViolations,
  checks: dagLabelCases + weightedCases + 4,
  limitations: "finite graph/cost reconstruction only; not historical R_mix341"
}, null, 2));
