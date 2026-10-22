// PADDING-SELF-REDUCTION-FIREWALL77 arithmetic audit
// Node.js; verifies only the stated FLMV/padding identities.
function dF(c) { return ((c + 2) / (c * c) - c) / 2; }
function root(c, s) {
  let lo = 1, hi = 2;
  while (hi * s < dF(hi * c) && hi < 100) hi *= 2;
  for (let i = 0; i < 200; i++) {
    const m = (lo + hi) / 2;
    if (m * s < dF(m * c)) lo = m; else hi = m;
  }
  return lo;
}
const cases = [
  { name: "baseline", c: 1.2, s: 0.5, beta: 0.5 },
  { name: "safe241/200", c: 241 / 200, s: 0.5, beta: 0.5 },
  { name: "retuned", c: 1.2021, s: 0.505, beta: 0.505 }
];
let checks = 0, failures = 0;
const out = [];
for (const x of cases) {
  const p = root(x.c, x.s);
  out.push({ ...x, pmax: p, cprime: p*x.c, sprime: p*x.s,
             dprime: dF(p*x.c), witnessExponentMax: x.beta*p,
             slackAtOne: dF(x.c)-x.s });
  for (let j = 0; j <= 100000; j++) {
    const q = 1 + (p - 1) * j / 100000;
    checks++;
    if (q * x.s > dF(q * x.c) + 1e-12) failures++;
  }
  checks += 2;
  if (!((p - 1e-10) * x.s < dF((p - 1e-10) * x.c) + 1e-12)) failures++;
  if (!((p + 1e-10) * x.s > dF((p + 1e-10) * x.c) - 1e-12)) failures++;
}
console.log(JSON.stringify({ formula: "p*s < dF(p*c)", out, checks, failures }, null, 2));
if (failures) process.exitCode = 1;
