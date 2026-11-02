#!/usr/bin/env node
// Independent referee for LSPV-3 SOURCE-SUPPORT-BOUNDARY340, Node builtins only.
// node experiments/arc/lspv3_340_independent.js results/raw/arc/2026-11-02_1124_LSPV3_SOURCE_SUPPORT_BOUNDARY340.json
const fs=require('fs'),assert=require('assert');
const raw=JSON.parse(fs.readFileSync(process.argv[2]||'results/raw/arc/2026-11-02_1124_LSPV3_SOURCE_SUPPORT_BOUNDARY340.json','utf8'));
function build(t,k){
  const z=Array.from({length:t},(_,i)=>i+2);
  const x=z.map((_,j)=>Array.from({length:k},(_,i)=>2+t+j*k+i));
  const C=[[-1,...z]],ids=[];
  for(let j=0;j<t;j++){
    const from=C.length,Z=z[j],X=x[j];
    C.push([-1,-Z,X[0]]);
    for(let i=0;i<k-1;i++) C.push([-1,-Z,-X[i],X[i+1]]);
    C.push([-1,-Z,-X[k-1]]);
    ids.push(Array.from({length:k+1},(_,i)=>from+i));
  }
  return {n:1+t+t*k,C,z,x,ids};
}
function firstModel(n,C,bit){
  for(let a=0;a<2**n;a++){
    if(bit!==undefined && (a&1)!==bit)continue;
    if(C.every(c=>c.some(v=>Boolean(a&(2**(Math.abs(v)-1)))===(v>0))))return a;
  }
  return null;
}
function proof(o){
  const db=o.C.map(c=>new Set(c));
  let steps=0;
  function res(a,b,p){
    assert(db[a].has(p)&&db[b].has(-p));
    const r=new Set([...db[a],...db[b]]);r.delete(p);r.delete(-p);
    for(const v of r)assert(!r.has(-v));
    db.push(r);steps++;
    return db.length-1;
  }
  const ends=[];
  for(let j=0;j<o.z.length;j++){
    let r=o.ids[j][0];
    for(let i=0;i<o.x[j].length;i++)r=res(r,o.ids[j][i+1],o.x[j][i]);
    assert.deepStrictEqual([...db[r]].sort((a,b)=>a-b),[-o.z[j],-1].sort((a,b)=>a-b));
    ends.push(r);
  }
  let root=0;
  for(let i=0;i<o.z.length;i++)root=res(root,ends[i],o.z[i]);
  assert.deepStrictEqual([...db[root]],[-1]);
  return steps;
}
let flips=0, deletions=0, nodes=0;
for(const row of raw.cases){
  const o=build(row.t,row.k);
  assert.strictEqual(o.n,row.variables);
  assert.strictEqual(o.C.length,row.clauses);
  assert.strictEqual(o.C.reduce((s,c)=>s+c.length,0),row.sign_occurrences);
  assert(firstModel(o.n,o.C,0)!==null);
  assert.strictEqual(firstModel(o.n,o.C,1),null);
  const core=o.C.map(c=>c.filter(v=>v!==-1));
  assert.strictEqual(firstModel(o.n,core),null);
  const q=proof(o);
  assert.strictEqual(q,row.resolution_inferences);
  assert.strictEqual(q,o.C.length-1);
  nodes+=q;
  for(let j=0;j<o.C.length;j++){
    assert(firstModel(o.n,o.C.filter((_,i)=>i!==j),1)!==null);
    deletions++;
    for(let i=0;i<o.C[j].length;i++){
      const mod=o.C.map(c=>c.slice());mod[j][i]*=-1;
      assert(firstModel(o.n,mod,1)!==null);
      assert(firstModel(o.n,mod,0)!==null);
      flips++;
    }
  }
}
assert.strictEqual(raw.malformed_rejected,5);
assert.strictEqual(flips,raw.totals.sign_flips);
assert.strictEqual(deletions,raw.totals.deleted_clause_witnesses);
assert.strictEqual(nodes,raw.totals.certified_inferences);
console.log(JSON.stringify({independent_referee:'PASS',families:raw.cases.length,flips,deletions,nodes}));
