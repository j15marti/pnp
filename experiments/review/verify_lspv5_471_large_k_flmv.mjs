import assert from "node:assert/strict";

const beta = x => (((x + 2) / (x * x)) - x) / 2;
const step = ([t, s]) => [Math.max(1.1, 0.6 + t / 2), Math.max(0.5, s / 2)];
const iter = (t, s, r) => {
  let z = [t, s];
  for (let i = 0; i < r; i++) z = step(z);
  return z;
};

let checks = 0;
assert.ok(Math.abs(beta(1.2) - 23 / 45) < 1e-14); checks++;
for (const k of [2, 10, 100, 1000, 1e6]) {
  let first = null;
  for (let r = 0; r < 100; r++) {
    const [t, s] = iter(k, k, r);
    if (s <= 0.5 && beta(t) > 0.5) { first = r; break; }
  }
  assert.notEqual(first, null); checks++;
  const [t, s] = iter(k, k, first);
  assert.ok(s <= 0.5 && beta(t) > 0.5); checks++;
  if (first > 0) {
    const [pt, ps] = iter(k, k, first - 1);
    assert.ok(ps > 0.5 || beta(pt) <= 0.5); checks++;
  }
}

for (let r = 0; r <= 40; r++) {
  const t0 = 1.2 + (2 ** r) * 0.01;
  const [t] = iter(t0, 0.5, r);
  assert.ok(Math.abs(t - 1.21) < 2e-8); checks++;
  assert.ok(beta(t) < 0.5); checks++;
}

console.log(JSON.stringify({status: "PASS", checks, scope: "independent floating-point recurrence control"}, null, 2));
