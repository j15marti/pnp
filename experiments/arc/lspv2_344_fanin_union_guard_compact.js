'use strict';
// LSPV-2 344, standalone fixed-calculus rule-union and selector-guard controls.
// Unit PARITY4 has arity four; weighted PARITY4 costs arity minus one.
const assert=require('assert').strict;
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
const models=(cs,n)=>{let count=0;for(let a=0;a<2**n;a++)
  if(cs.every(c=>c.some(l=>(l>0)===!!(a&(1<<(Math.abs(l)-1))))))count++;
  return count;};
function tseitin(charges){const cs=[],groups=[];
  for(let v=0;v<4;v++){const xs=edges.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean),ids=[];
    for(let a=0;a<8;a++){const b=[(a>>2)&1,(a>>1)&1,a&1];
      if((b[0]^b[1]^b[2])!==charges[v]){
        ids.push(cs.length);cs.push(xs.map((x,j)=>b[j]?-x:x));
      }}
    groups.push({xs,ids,rhs:charges[v]});
  }
  return {cs,groups};
}
const odd=tseitin([1,0,0,0]),even=tseitin([0,0,0,0]);
assert.equal(models(odd.cs,6),0);assert.equal(models(even.cs,6),8);
const deletions=odd.cs.map((_,i)=>models(odd.cs.filter((_,j)=>i!==j),6));
assert(deletions.every(x=>x===2));
const proof=[];
for(const g of odd.groups){
  for(let a=0;a<8;a++){
    const b=[(a>>2)&1,(a>>1)&1,a&1],assignment={};
    g.xs.forEach((v,j)=>assignment[v]=b[j]);
    const truth=g.ids.every(i=>odd.cs[i].some(l=>(l>0)===(assignment[Math.abs(l)]===1)));
    assert.equal(truth,(b[0]^b[1]^b[2])===g.rhs);
  }
  proof.push({id:'d'+proof.length,rule:'PARITY4',parents:g.ids.map(i=>'s'+i),xs:g.xs,rhs:g.rhs});
}
let acc=proof[0];
for(let i=1;i<4;i++){
  const b=proof[i],xs=[...new Set([...acc.xs,...b.xs])]
    .filter(x=>acc.xs.includes(x)!==b.xs.includes(x)).sort((a,b)=>a-b);
  const nxt={id:'d'+proof.length,rule:'XOR',parents:[acc.id,b.id],xs,rhs:acc.rhs^b.rhs};
  proof.push(nxt);acc=nxt;
}
assert.deepEqual(acc.xs,[]);assert.equal(acc.rhs,1);
const unitNodes=proof.length;
const weightedCost=proof.reduce((sum,p)=>sum+Math.max(1,p.parents.length-1),0);
assert.equal(unitNodes,7);assert.equal(weightedCost,15);
function blockers(n){return Array.from({length:2**n},(_,a)=>
 Array.from({length:n},(_,i)=>(a&(1<<(n-i-1)))?-(i+1):i+1));}
function guard(cs,n){return cs.map(c=>[...c,n+1]).concat(cs.map(c=>[...c,-n-1]));}
const selector=[];
for(let n=1;n<=5;n++){
  const F=blockers(n),G=guard(F,n),m=F.length;
  assert.equal(models(F,n),0);assert.equal(models(G,n+1),0);
  assert(F.every((_,i)=>models(F.filter((_,j)=>j!==i),n)===1));
  assert(G.every((_,i)=>models(G.filter((_,j)=>j!==i),n+1)===1));
  selector.push({n,source_clauses:m,guard_clauses:2*m,weighted_exact_source:m-1,weighted_exact_guard:2*m-1});
}
const output={status:'PASS',K4:{odd_models:0,even_models:8,all_source_deletions_models:deletions,unit_4premise_upper:unitNodes,unit_4premise_source_lower:5,weighted_exact:weightedCost,locally_checked_parity_rows:32},selector,rule_union_status:'candidate, lead ratification pending',P_vs_NP:'OPEN'};
console.log(JSON.stringify(output,null,2));
