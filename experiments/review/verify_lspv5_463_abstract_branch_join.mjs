#!/usr/bin/env node
// Independent finite replay. This is not an R_mix341 checker.

import assert from "node:assert/strict";

const vals = [
  {x: 0, y: 0}, {x: 0, y: 1}, {x: 1, y: 0}, {x: 1, y: 1},
];
const vars = ["x", "y"];
const vk = v => `${v.x}${v.y}`;
const lits = v => new Set(vars.map(x => `${v[x] ? "" : "!"}${x}`));
const intersection = sets => {
  if (!sets.length) return new Set(["x", "!x", "y", "!y"]);
  return new Set([...sets[0]].filter(z => sets.slice(1).every(s => s.has(z))));
};
const alpha = states => intersection(states.map(lits));
const gamma = facts => new Set(vals.filter(v => [...facts].every(z => {
  const neg = z.startsWith("!");
  const x = neg ? z.slice(1) : z;
  return Boolean(v[x]) === !neg;
})).map(vk));
const union = (a,b) => new Set([...a,...b]);
const subset = (a,b) => [...a].every(x => b.has(x));
const subsets = [];
for (let mask=1; mask<16; mask++) subsets.push(vals.filter((_,i) => mask & (1<<i)));

let checks = 0, unsound = 0;
for (const s0 of subsets) for (const s1 of subsets) {
  const a0 = alpha(s0), a1 = alpha(s1);
  const concrete = new Set([...s0,...s1].map(vk));
  const join = intersection([a0,a1]);
  const joinedStates = vals.filter(v => concrete.has(vk(v)));
  assert.deepEqual([...alpha(joinedStates)].sort(), [...join].sort()); checks++;
  assert.ok(subset(concrete, gamma(join))); checks++;
  const pooled = union(a0,a1);
  if (!subset(concrete, gamma(pooled))) unsound++;
}

const fmodels = new Set(["00", "11"]);
const l0 = new Set(["!y"]), l1 = new Set(["y"]);
assert.ok(subset(fmodels, gamma(intersection([l0,l1])))); checks++;
assert.equal(gamma(union(l0,l1)).size, 0); checks++;

console.log(JSON.stringify({
  status: "PASS",
  ordered_nonempty_subset_pairs: 225,
  checks,
  bad_pool_unsound_pairs: unsound,
  example_correct_join_gamma: [...gamma(intersection([l0,l1]))].sort(),
  example_bad_pool_gamma: [...gamma(union(l0,l1))].sort(),
  limitations: "semantic finite replay only; not historical R_mix341",
}, null, 2));
