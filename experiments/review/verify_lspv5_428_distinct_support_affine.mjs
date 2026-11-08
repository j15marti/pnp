#!/usr/bin/env node
// Independent V8 replay for LSPV-5/428.  No import from the Python checker.

const src = {
  C1:[1,-3,4], C2:[1,-4,5], C3:[1,-5,-3],
  C4:[2,3,6], C5:[2,-6,7], C6:[2,-7,3],
  D1:[-1,-8,9], D2:[-1,-9,10], D3:[-1,-10,-8],
  D4:[-2,8,11], D5:[-2,-11,12], D6:[-2,-12,8],
};
const started = process.hrtime.bigint();

const trace = [
  ['R1','C1','C2',4,[1,-3,5]], ['R2','R1','C3',5,[1,-3]],
  ['R3','C4','C5',6,[2,3,7]], ['R4','R3','C6',7,[2,3]],
  ['R5','R4','R2',3,[1,2]], ['S1','D1','D2',9,[-1,-8,10]],
  ['S2','S1','D3',10,[-1,-8]], ['S3','D4','D5',11,[-2,8,12]],
  ['S4','S3','D6',12,[-2,8]], ['S5','S4','S2',8,[-1,-2]],
];

const canon = c => [...new Set(c)].sort((a,b) => Math.abs(a)-Math.abs(b) || Number(a<0)-Number(b<0));
const same = (a,b) => JSON.stringify(canon(a)) === JSON.stringify(canon(b));
const taut = c => c.some(x => c.includes(-x));
function resolve(l,r,p) {
  if (!l.includes(p) || !r.includes(-p)) throw new Error('oriented pivot absent');
  const out = [...l.filter(x=>x!==p), ...r.filter(x=>x!==-p)];
  if (taut(out)) throw new Error('tautology');
  return canon(out);
}
const satClause = (c,bits) => c.some(l => bits[Math.abs(l)-1] === (l>0));
const allBits = n => Array.from({length:1<<n},(_,mask)=>Array.from({length:n},(_,i)=>Boolean(mask&(1<<i))));

let checks = 0;
for (const c of Object.values(src)) {
  if (c.length!==3 || new Set(c.map(Math.abs)).size!==3 || taut(c)) throw new Error('bad source');
  checks++;
}
const supports = Object.values(src).map(c => c.map(Math.abs).sort((a,b)=>a-b).join(','));
if (new Set(supports).size !== supports.length) throw new Error('repeated support');
checks++;

const db = {...src};
for (const [name,l,r,p,want] of trace) {
  db[name] = resolve(db[l],db[r],p);
  if (!same(db[name],want)) throw new Error(`bad ${name}`);
  checks++;
}

const counts = {'00':0,'01':0,'10':0,'11':0};
for (const bits of allBits(12)) {
  if (Object.values(src).every(c=>satClause(c,bits))) counts[`${+bits[0]}${+bits[1]}`]++;
  checks++;
}
if (counts['00'] || counts['11'] || counts['01']!==144 || counts['10']!==144) throw new Error('projection');

for (const omitted of Object.keys(src)) {
  const kept = Object.entries(src).filter(([k])=>k!==omitted).map(([,c])=>c);
  const witness = allBits(12).some(bits => bits[0]===bits[1] && kept.every(c=>satClause(c,bits)));
  if (!witness) throw new Error(`nonessential ${omitted}`);
  checks++;
}

for (const [l,r,p] of [[src.C1,src.C2,5],[src.C2,src.C1,4],[src.C1,src.C4,4]]) {
  let rejected=false; try { resolve(l,r,p); } catch { rejected=true; }
  if (!rejected) throw new Error('corrupt trace accepted');
  checks++;
}

console.log(JSON.stringify({
  status:'PASS', checks, projection_counts:counts,
  source_supports:12, resolution_nodes:10, deletion_controls:12, corrupt_controls:3,
  scope:'ordinary Resolution only; historical LOCAL-CONVERT remains unauthenticated',
  runtime_seconds:Number(process.hrtime.bigint()-started)/1e9,
  rss_bytes:process.memoryUsage().rss
},null,2));
