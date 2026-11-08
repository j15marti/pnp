// Independent BigInt reconstruction of the LSPV-5/423 elementary audit.
// This is not a Lean replay and does not prove Pang's lower-bound theorem.

function gcd(a, b) {
  while (b !== 0n) [a, b] = [b, a % b];
  return a < 0n ? -a : a;
}
function reduce(a, b) {
  const g = gcd(a, b);
  return [a / g, b / g];
}
function choose2(n) { return n * (n - 1n) / 2n; }
function choose3(n) { return n * (n - 1n) * (n - 2n) / 6n; }
function encodeNat(n) { return Array(n).fill(true).concat(false); }
function frame(bits) {
  let out = [false];
  for (let i = bits.length - 1; i >= 0; i--) out = [true, bits[i], ...out];
  return out;
}
function encodeList(enc, xs) {
  if (xs.length === 0) return [false];
  return [true, ...frame(enc(xs[0])), ...encodeList(enc, xs.slice(1))];
}
function literalCode(lit) { return 2 * (Math.abs(lit) - 1) + (lit > 0 ? 1 : 0); }
function canonicalFormula(clauses) {
  const rows = clauses.map(c => [...new Set(c.map(literalCode))].sort((a, b) => a - b));
  const unique = new Map(rows.map(r => [r.join(','), r]));
  return [...unique.values()].sort((a, b) => a.join(',').localeCompare(b.join(',')));
}
function encodeCNF(n, clauses) {
  const cs = canonicalFormula(clauses);
  return [...encodeNat(n), ...encodeList(c => encodeList(encodeNat, c), cs)];
}
function strict3(n, clauses) {
  return Number.isInteger(n) && n >= 0 && clauses.every(c =>
    Array.isArray(c) && c.length === 3 &&
    c.every(x => Number.isInteger(x) && typeof x !== 'boolean' && x !== 0 && Math.abs(x) <= n) &&
    new Set(c.map(Math.abs)).size === 3);
}
function count(n, clauses) {
  let z = 0;
  for (let bits = 0; bits < (1 << n); bits++) {
    if (clauses.every(c => c.some(l => Boolean(bits & (1 << (Math.abs(l) - 1))) === (l > 0)))) z++;
  }
  return z;
}

let checks = 0;
const rows = [];
for (let ni = 3; ni <= 10000; ni++) {
  const n = BigInt(ni), m = 8n * n, M = 8n * choose3(n);
  const u = reduce(choose2(m), M);
  const v = reduce(3n * (8n * n - 1n), (n - 1n) * (n - 2n));
  if (u[0] !== v[0] || u[1] !== v[1]) throw Error('closed form mismatch');
  checks++;
  if (ni >= 6) {
    if (u[0] * n > 48n * u[1]) throw Error('48/n bound mismatch');
    checks++;
  }
  if ([3, 6, 10, 100, 1000, 10000].includes(ni)) rows.push({n:ni, numerator:u[0].toString(), denominator:u[1].toString()});
  const L = BigInt(ni + 2) + m * BigInt(24 * ni + 16);
  if (L !== 192n*n*n + 129n*n + 2n) throw Error('encoding polynomial mismatch');
  checks++;
}

for (let n = 3; n <= 9; n++) {
  const clauses = [];
  outer: for (let a = 1; a <= n; a++) for (let b = a + 1; b <= n; b++) for (let c = b + 1; c <= n; c++) {
    for (let mask = 0; mask < 8; mask++) {
      clauses.push([a,b,c].map((v,i) => (mask & (1 << i)) ? v : -v));
      if (clauses.length === Math.min(8*n, 8*n*(n-1)*(n-2)/6)) break outer;
    }
  }
  if (!strict3(n, clauses)) throw Error('strict3 rejected');
  const L = encodeCNF(n, clauses).length;
  const B = n + 2 + clauses.length * (24*n + 16);
  if (L > B) throw Error('exact encoder exceeded bound');
  if (encodeCNF(n, [...clauses, clauses[0]]).join('') !== encodeCNF(n, clauses).join('')) throw Error('Finset dedup mismatch');
  checks += 3;
}

const cube = Array.from({length:8}, (_,mask) => [1,2,3].map((v,i) => mask & (1<<i) ? v : -v));
if (count(3,cube) !== 0 || count(3,cube.slice(0,7)) !== 1 || count(3,[]) !== 8) throw Error('SAT controls');
checks += 3;
for (const bad of [[[1,1,2]],[[1,2,0]],[[1,2,4]],[[1,2]],[[1,2,3,4]],[[true,2,3]]]) {
  if (strict3(3,bad)) throw Error('malformed accepted');
  checks++;
}

console.log(JSON.stringify({
  status:'INDEPENDENT FINITE REPRESENTATION CONTROLS; no Lean or Pang theorem replay',
  checks,
  collision_bound:'3(8n-1)/((n-1)(n-2)) <= 48/n for n>=6',
  encoding_bound:'L <= 192n^2+129n+2 at m=8n',
  rows,
  malformed_rejections:6
}, null, 2));
