'use strict';
// TMR-1/052. Deterministic exact finite audit of a shared minterm-trie circuit
// and width-3 existential-CNF counting envelope. No random seeds.
const assert = require('node:assert/strict');
const checks = { assignments: 0, functionCollisions: 0, gateCaps: 0, budgetRows: 0, failures: 0 };
const examples = [];
const C = (a,b) => (b<0 || b>a) ? 0n : (()=>{let t=1n;for(let j=1;j<=b;j++)t=t*BigInt(a-j+1)/BigInt(j);return t;})();
function clauseCapacity(v) {
  const z=BigInt(v);
  return 1n + 2n*z + 4n*(z*(z-1n)/2n) + 8n*(z*(z-1n)*(z-2n)/6n);
}
function familyCircuit(n,k,subset) {
  const gates=[];const prefixes=new Map();const negs=new Map();
  const add=(op,a,b)=>{ const id=n+gates.length;gates.push({op,a,b});return id; };
  const lit=(j,bit)=>{if(bit==='1')return j;if(!negs.has(j))negs.set(j,add('NOT',j));return negs.get(j);};
  const leaf=[];
  for(const s of subset) {
    const bits=s.toString(2).padStart(k,'0');
    for(let j=0;j<k;j++) {
      const key=bits.slice(0,j+1);
      if(!prefixes.has(key)){
        const id=j===0 ? lit(0,bits[0]) : add('AND',prefixes.get(bits.slice(0,j)),lit(j,bits[j]));
        prefixes.set(key,id);
      }
    }
    leaf.push(prefixes.get(bits));
  }
  let out=leaf[0];
  for(let i=1;i<leaf.length;i++)out=add('OR',out,leaf[i]);
  for(let j=k;j<n;j++)out=add('AND',out,j);
  return {n,k,gates,out};
}
function runCircuit(c,input) {
  const reg=Array.from({length:c.n},(_,j)=>(input>>j)&1);
  for(const g of c.gates){const a=reg[g.a], b=g.b===undefined?null:reg[g.b];reg.push(g.op==='NOT' ? 1-a : g.op==='AND' ? a&b : a|b);}
  return reg[c.out];
}
function* choose(n,k,at=0,acc=[]) {
  if(k===0){yield acc.slice();return;}
  for(let j=at;j<=n-k;j++){acc.push(j);yield* choose(n,k-1,j+1,acc);acc.pop();}
}
const familyRows=[];
for(let k=1;k<=4;k++) {
  const n=k+2, r=2**k, half=r/2, seen=new Set();let families=0,maxGates=0;
  for(const subset of choose(r,half)) {
    if(k===4 && families>=128)break;
    const c=familyCircuit(n,k,subset), accept=new Set(subset);
    assert.ok(c.gates.length<=3*r+n);checks.gateCaps++;
    maxGates=Math.max(maxGates,c.gates.length);
    let signature='';
    for(let a=0;a<2**n;a++) {
      let idx=0;for(let j=0;j<k;j++)idx=idx*2+((a>>j)&1);
      let valid=accept.has(idx);for(let j=k;j<n;j++)valid=valid && !!((a>>j)&1);
      const actual=runCircuit(c,a);assert.equal(actual,Number(valid));checks.assignments++;
      signature+=actual;
    }
    assert.ok(!seen.has(signature));seen.add(signature);checks.functionCollisions++;
    families++;
  }
  assert.equal(families,k===4?128:Number(C(r,half)));
  familyRows.push({k,n,r,halfr:half,families,maxGates,allGatesLiveByConstruction:true});
}
// Theorem requires r<=g/8 and k<=n (which holds at the sampled powers of 2).
const budget=[];
for(let b=8;b<=40;b+=4) {
  const n=1n<<BigInt(b),g=n**4n,r=g/8n,k=4*b-3;
  assert.ok(BigInt(k)<=n);assert.ok(3n*r+n<=g);
  const V=n*BigInt(b*b), logDistinctLower=r-BigInt(k+1);
  const cap=clauseCapacity(V);checks.budgetRows++;
  budget.push({log2_n:b,log2_g:4*b,k,log2_r:k,compressed_V:String(V),Q_width3:String(cap),log2_family_lower:String(logDistinctLower),universal_projection_compression_ruled_out_at_V:cap<logDistinctLower});
}
// The exact formula Q is at most (2V)^3 for small and large V.
for(let v=1;v<=500;v++){assert.ok(clauseCapacity(v)<=8n*BigInt(v)**3n);checks.budgetRows++;}
const result={run:'TMR1_COMPCENSUS052_v1',proofStatus:'PROVED_RESTRICTED_symbolic;COMPUTATIONAL_finite',seed:null,model:'fan-in-2 AND/OR/NOT shared DAG; existential width-at-most-3 CNF with named inputs',checks, familyRows,budget, failures:0};
console.log(JSON.stringify(result,null,2));
