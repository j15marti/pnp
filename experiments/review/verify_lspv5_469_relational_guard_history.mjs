#!/usr/bin/env node
// Independent V8 replay for LSPV-5/469. Not an R_mix341 checker.
import assert from 'node:assert/strict';

const MAX_N = 9;
let checks = 0, relationStates = 0, correlationMasks = 0;

function relationFor(n, active) {
  if (!Number.isInteger(n) || n <= 0 || active < 0 || active >= 2 ** n)
    throw new Error('bad parameters');
  const result = [];
  for (let choice = 0; choice < 2 ** n; choice++) {
    const g = [], h = [];
    for (let i = 0; i < n; i++) {
      const x = (active >> i) & 1;
      const c = (choice >> i) & 1;
      if (x) { g.push(c ? 0 : 1); h.push(c ? 1 : 0); }
      else   { g.push(c ? 0 : 1); h.push(c ? 0 : 1); }
    }
    result.push({g, h});
  }
  return result;
}

const X = [[1, 0], [0, 1]], Y = [[1, 1], [0, 0]];
function projections(r) {
  return [new Set(r.map(p => p[0])).size, new Set(r.map(p => p[1])).size];
}
function cstar(r, w) {
  const a = r.filter(p => p[0] === 1).map(p => p[1] ? 0 : w);
  if (!a.length || !(w > 0)) throw new Error('bad relation or weight');
  return Math.min(...a);
}
assert.deepEqual(projections(X), [2, 2]);
assert.deepEqual(projections(Y), [2, 2]);
assert.equal(cstar(X, 11), 11);
assert.equal(cstar(Y, 11), 0);
checks += 4;

const rows = [];
for (let n = 1; n <= MAX_N; n++) {
  const vectors = new Set();
  for (let active = 0; active < 2 ** n; active++) {
    const r = relationFor(n, active);
    relationStates += r.length; correlationMasks++;
    assert.equal(r.length, 2 ** n); checks++;
    const gs = new Set(r.map(s => s.g.join('')));
    const hs = new Set(r.map(s => s.h.join('')));
    assert.equal(gs.size, 2 ** n); assert.equal(hs.size, 2 ** n); checks += 2;
    const vector = [];
    for (let i = 0; i < n; i++) {
      const weight = i + 3;
      const legal = r.filter(s => s.g[i]).map(s => s.h[i] ? 0 : weight);
      const exact = Math.min(...legal);
      const expected = ((active >> i) & 1) ? weight : 0;
      assert.equal(exact, expected);
      assert.ok(legal.every(v => exact <= v));
      assert.ok(exact >= 0); // marginal product's universally safe value is zero.
      checks += 3; vector.push(exact);
    }
    vectors.add(vector.join(','));
  }
  assert.equal(vectors.size, 2 ** n); checks++;
  rows.push({n, masks: 2 ** n, states_per_relation: 2 ** n,
             distinct_exact_charge_vectors: vectors.size});
}

let malformed = 0;
for (const f of [() => relationFor(0, 0), () => relationFor(2, 4),
                 () => cstar(X, 0), () => cstar([[0, 0]], 1)]) {
  try { f(); } catch { malformed++; }
}
assert.equal(malformed, 4); checks++;

console.log(JSON.stringify({
  run: 'LSPV-5/469 independent V8 replay',
  status: 'PASS / COMPUTATIONAL',
  max_n: MAX_N,
  checks,
  correlation_masks: correlationMasks,
  relational_states_checked: relationStates,
  malformed_rejections: malformed,
  rows,
  firewall: 'Restricted relational model only; no R_mix341, B1/B2/B3, or P-vs-NP claim.'
}, null, 2));
