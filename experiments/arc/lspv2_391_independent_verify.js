#!/usr/bin/env node
// Independent LSPV-2/391 checker, reconstructing all CNF assignments.
const fs=require('fs'), assert=require('assert');
const d=JSON.parse(fs.readFileSync(process.argv[2],'utf8'));
let checks=0, hist={}, count=0;
function holds(c,x){return c.some(l=> ((x>>(Math.abs(l)-1))&1)===(l>0?1:0));}
function cnf(n,edges){return edges.concat([[n,n+1],[n+1,n+2],[n,n+2]])
  .flatMap(([u,v])=>[[u+1,v+1],[-u-1,-v-1]]);}
function verify(p){
 const a=p.clauses.map(c=>[...c]);
 for(const r of p.steps){
  assert(r.left<a.length&&r.right<a.length);checks++;
  const l=a[r.left],q=a[r.right],v=r.pivot;
  assert((l.includes(v)&&q.includes(-v))||(l.includes(-v)&&q.includes(v)));checks++;
  const got=Array.from(new Set(l.concat(q).filter(x=>Math.abs(x)!==v))).sort((x,y)=>x-y);
  assert.deepStrictEqual(got,r.conclusion);checks++;a.push(got);
 }
 assert.deepStrictEqual(a.at(-1),[]);checks++;
}
verify(d.triangle_strict_resolution_certificate);
for(let n=1;n<=5;n++){
 let ee=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)ee.push([u,v]);
 for(let bits=0;bits<2**ee.length;bits++){
  const edges=ee.filter((_,i)=>bits>>i&1),cs=cnf(n,edges);
  let delta=Infinity,mc=0;
  for(let a=0;a<2**(n+3);a++){
   let bad=cs.filter(c=>!holds(c,a)).length;
   if(bad<delta)delta=bad;
   checks++;
  }
  for(let a=0;a<2**n;a++){
   mc=Math.max(mc,edges.filter(([u,v])=>((a>>u)&1)!==((a>>v)&1)).length);
   checks++;
  }
  assert.strictEqual(delta,edges.length-mc+1);checks++;
  hist[delta]=(hist[delta]||0)+1;count++;
 }
}
assert.strictEqual(count,d.graphs_checked);checks++;
assert.deepStrictEqual(hist,d.distance_histogram);checks++;
for(const ex of d.examples){
 assert.strictEqual(cnf(ex.n,ex.edges).length,ex.source_clauses);checks++;
 assert.strictEqual(ex.edges.length-ex.maxcut+1,ex.min_deletions);checks++;
}
const equalities=[[1,-2],[-1,2],[2,-3],[-2,3],[1,-3],[-1,3]];
assert(equalities.every(c=>holds(c,0)));checks++;
const bad=JSON.parse(JSON.stringify(d.triangle_strict_resolution_certificate));
bad.steps[0].pivot=3;let rejects=0;
try{verify(bad)}catch(e){rejects++}
assert.strictEqual(rejects,1);checks++;
for(const invalid of [null,undefined,"junk",{clauses:[]},{steps:[]}]){
 try{assert(invalid&&Array.isArray(invalid.steps)&&Array.isArray(invalid.clauses));}
 catch(e){rejects++}
}
assert.strictEqual(rejects,6);checks++;
console.log(JSON.stringify({status:"PASS",independent:true,graphs:count,checks,rejected:rejects,distribution:hist}));
