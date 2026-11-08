// Independent BigInt reconstruction of the LSPV-5/424 accounting audit.
// This is not a Pang theorem replay or an authoritative R_mix341 checker.

function paidUnion(nodes) {
  const paid = new Map();
  for (const n of nodes) {
    if (n.kind !== 'derived') continue;
    if (paid.has(n.id) && paid.get(n.id) !== n.weight) throw Error('inconsistent duplicate');
    paid.set(n.id, n.weight);
  }
  return [...paid.values()].reduce((a,b) => a+b, 0n);
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
for (let m = 0n; m <= 32n; m++) {
  for (let source = 0n; source <= m; source++) {
    for (let q = 0n; q <= 64n; q++) {
      const S = source + q;
      for (let alpha = 1n; alpha <= 8n; alpha++) {
        const deficit = S > m ? S - m : 0n;
        if (q < deficit || alpha*q < alpha*deficit) throw Error('bridge failed');
        checks += 2;
      }
    }
  }
}

const common = [{id:'g1',kind:'derived',weight:1n},{id:'g2',kind:'derived',weight:1n}];
const left = [...common,{id:'l',kind:'derived',weight:1n}];
const right = [...common,{id:'r',kind:'derived',weight:1n}];
if (paidUnion(left) !== 3n || paidUnion(right) !== 3n || paidUnion([...left,...right]) !== 4n) throw Error('shared DAG');
checks += 4;

const zero = Array.from({length:1000},(_,i)=>({id:`z${i}`,kind:'derived',weight:0n}));
if (paidUnion(zero) !== 0n) throw Error('zero-weight countermodel');
const batch = [{id:'batch',kind:'derived',weight:1n,virtual:1000000n}];
if (paidUnion(batch) !== 1n || batch[0].virtual !== 1000000n) throw Error('batch countermodel');
checks += 2;

const rows = [];
for (let n = 32n; n <= 512n; n += 32n) {
  const S = 1n << (n/8n);
  const q = S > 8n*n ? S - 8n*n : 0n;
  if (n >= 128n && q <= 0n) throw Error('eventual positivity');
  if (n >= 128n) checks++;
  rows.push({n:n.toString(), source:(8n*n).toString(), sampleS:S.toString(), derived:q.toString()});
}

const cube = Array.from({length:8},(_,mask)=>[1,2,3].map((v,i)=>mask&(1<<i)?v:-v));
if (!strict3(3,cube) || count(3,cube)!==0 || !strict3(3,cube.slice(0,7)) || count(3,cube.slice(0,7))!==1 || count(3,[])!==8) throw Error('SAT controls');
checks += 5;
for (const bad of [[[1,1,2]],[[1,2,0]],[[1,2,4]],[[1,2]],[[1,2,3,4]],[[true,2,3]]]) {
  if (strict3(3,bad)) throw Error('malformed accepted');
  checks++;
}

console.log(JSON.stringify({
  status:'INDEPENDENT BIGINT ACCOUNTING CONTROLS; no Pang theorem or authoritative R_mix341 checker replay',
  checks,
  bridge:'W>=alpha*max(0,S-m)',
  branching:{left:3,right:3,andUnion:4,orChoice:3},
  contextLeakRejected:true,
  countermodels:{zeroNodes:1000,zeroCost:0,batchVirtual:1000000,batchCost:1},
  rows,
  malformedRejections:6
}, null, 2));
