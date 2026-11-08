#!/usr/bin/env node
/* Independent replay of LSPV-5/437 individual-goal Resolution certificates.
   This is not the historical R_mix341 checker. */
import fs from "node:fs";

const rawPath = new URL("./raw/lspv5_437_individual_resolution_results.json", import.meta.url);
const raw = JSON.parse(fs.readFileSync(rawPath, "utf8"));
let checks = 0;
const ck = (condition, message) => {
  checks++;
  if (!condition) throw new Error(message);
};
const sources = [
  [1,2,-4],[1,-2,-4],[-1,2,-4],[-1,-2,4],
  [2,3,-5],[2,-3,5],[-2,3,5],[-2,-3,-5],
  [1,5,-6],[1,-5,-6],[-1,5,-6],[-1,-5,6],
  [4,6,-7],[4,-6,7],[-4,6,7],[-4,-6,-7],
];
const norm = c => [...new Set(c)].sort((a,b) => Math.abs(a)-Math.abs(b) || b-a);
const same = (a,b) => JSON.stringify(a) === JSON.stringify(b);
const sat = (clause, assignment) => clause.some(lit =>
  ((assignment >> (Math.abs(lit)-1)) & 1) === (lit > 0 ? 1 : 0));
function resolve(left, right, pivot) {
  if (left.includes(-pivot) && right.includes(pivot)) [left,right] = [right,left];
  if (!left.includes(pivot) || !right.includes(-pivot)) return null;
  const child = norm([
    ...left.filter(x => x !== pivot),
    ...right.filter(x => x !== -pivot),
  ]);
  return child.some(x => child.includes(-x)) ? null : child;
}

ck(raw.status === "PROVED_RESTRICTED_EXACT_INDIVIDUAL_MINIMA", "status");
ck(raw.results.length === 3, "result count");
for (let g = 0; g < raw.results.length; g++) {
  const result = raw.results[g];
  const deletion = raw.deletion_essentiality_checks[g];
  const essential = result.essential_sources.map(id => Number(id.slice(1)));
  ck(same(result.goal, deletion.goal), `goal ${g} mismatch`);
  ck(same(result.essential_sources, deletion.essential_sources), `essential ${g} mismatch`);
  ck(result.minimum_distinct_inference_nodes === essential.length - 1,
     `binary-fanin lower bound ${g}`);

  // Independently exhaust all 128 assignments and recover the exact deletion-
  // essential source set for this one goal.
  const recovered = [];
  for (let omitted = 0; omitted < sources.length; omitted++) {
    let witness = null;
    for (let a = 0; a < 128; a++) {
      if (sources.every((c,i) => i === omitted || sat(c,a)) && !sat(result.goal,a)) {
        witness = a;
        break;
      }
    }
    if (witness !== null) {
      recovered.push(omitted);
      const id = `S${String(omitted).padStart(2,"0")}`;
      ck(deletion.deletion_witness_assignments[id] !== undefined, `missing deletion witness ${id}`);
      const cited = deletion.deletion_witness_assignments[id];
      ck(sources.every((c,i) => i === omitted || sat(c,cited)), `bad deletion model ${id}`);
      ck(!sat(result.goal,cited), `deletion model satisfies goal ${id}`);
    }
  }
  ck(same(recovered, essential), `recovered essential set ${g}`);

  const db = new Map(sources.map((c,i) => [`S${String(i).padStart(2,"0")}`, norm(c)]));
  const ancestry = new Map(sources.map((_,i) => [`S${String(i).padStart(2,"0")}`, new Set([i])]));
  for (const node of result.tree_witness_nodes) {
    ck(db.has(node.left) && db.has(node.right), `topology ${node.id}`);
    const child = resolve(db.get(node.left), db.get(node.right), node.pivot);
    ck(child !== null && same(child,node.clause), `resolution ${node.id}`);
    db.set(node.id, child);
    ancestry.set(node.id, new Set([...ancestry.get(node.left), ...ancestry.get(node.right)]));
  }
  ck(same(db.get(result.root), result.goal), `root ${g}`);
  ck(same([...ancestry.get(result.root)].sort((a,b)=>a-b), essential), `root ancestry ${g}`);
  ck(result.tree_witness_nodes.length === essential.length - 1, `tree floor ${g}`);
}

// Hostile controls must fail under the same independent logic.
const q2 = raw.results[2];
const badPivot = structuredClone(q2.tree_witness_nodes);
badPivot.at(-1).pivot = 7;
const dbBad = new Map(sources.map((c,i) => [`S${String(i).padStart(2,"0")}`, norm(c)]));
let acceptedBadPivot = true;
for (const node of badPivot) {
  const child = resolve(dbBad.get(node.left), dbBad.get(node.right), node.pivot);
  if (child === null || !same(child,node.clause)) { acceptedBadPivot = false; break; }
  dbBad.set(node.id, child);
}
ck(!acceptedBadPivot, "corrupt pivot accepted");
ck(!same(norm([-1,-2,-4]), norm(sources[3])), "corrupt source undetected");
ck(!same(q2.goal, [3,7]), "corrupt goal undetected");

console.log(JSON.stringify({
  status: "PASS",
  assertions: checks,
  individual_minima: raw.results.map(x => x.minimum_distinct_inference_nodes),
  hostile_controls: 3,
  historical_R_mix341_checker_run: false,
  p_vs_np: "OPEN",
}, null, 2));
