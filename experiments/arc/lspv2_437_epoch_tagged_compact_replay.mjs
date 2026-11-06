// LSPV-2/437 compact standalone check. Not an FLMV Turing-machine execution.
import assert from 'node:assert/strict';
let checks=0;
function eq(a,b){assert.deepEqual(a,b);checks++;}
const graphs={K4:[4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],cube:[8,Array.from({length:8},(_,u)=>[0,1,2].map(b=>[u,u^(1<<b)]).filter(e=>e[0]<e[1])).flat()]};
function cnf(H,edges,c){const adj=Array.from({length:H},()=>[]);edges.forEach(([u,v],i)=>{adj[u].push(i+1);adj[v].push(i+1)});return adj.flatMap((ids,v)=>{ids.sort((a,b)=>a-b);assert.equal(ids.length,3);return [0,1,2,3].map(k=>{const p=k>>1,r=k&1;return ids.map((x,j)=>[p,r,p^r^1^c[v]][j]?-x:x)})})}
for(const [name,[H,edges]] of Object.entries(graphs)){
 const q=120,b=Math.ceil(Math.log2(q+1)),cells=Array.from({length:H},()=>[0,0]);let reads=0,edits=0;
 for(let j=1;j<=q;j++){
  const base=Array.from({length:H},(_,v)=>(v+j)%2);
  const updates=Array.from({length:(j*7)%(H*3+1)},(_,r)=>(j*5+r*r)%H);
  if(j%9===0)updates.push(1,1);
  const truth=base.slice();
  for(const v of updates){truth[v]^=1;edits++;const [tag,value]=cells[v];cells[v]=[j,(tag===j?value:0)^1]}
  const derived=Array.from({length:H},(_,v)=>{reads++;return base[v]^(cells[v][0]===j?cells[v][1]:0)});
  eq(derived,truth);eq(cnf(H,edges,derived),cnf(H,edges,truth));
  eq(truth.reduce((a,x)=>a^x,0),base.reduce((a,x)=>a^x,0)^(updates.length&1));
 }
 console.log(name,{q,edits,reads,maximumPhysicalTagBits:H*(b+1)});
}
console.log({status:'PASS',checks});
