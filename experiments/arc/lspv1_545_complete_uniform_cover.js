'use strict';
// LSPV-1/545: exact finite controls for a DISTINCT complete k-uniform AND/OR cover calculus.
// This is NOT a native R_mix341 checker and not a proof of P != NP.
const assert = require('node:assert/strict');
function choose(n,k){let z=1;for(let i=1;i<=k;i++)z=z*(n-i+1)/i;return Math.round(z)}
function popcount(n){let c=0;while(n){n &= n-1;c++}return c}
function full(n,k) {
  if(!Number.isInteger(n)||!Number.isInteger(k)||k<2||n<k||n>20)throw Error('bad dimensions');
  const universe=Array.from({length:2**n},(_,i)=>i).filter(mask=>popcount(mask)===k);
  const min=n-k+1, states=2**n;
  assert.equal(universe.length,choose(n,k));
  let accepting=0, transitionChecks=0;
  for(let mask=0;mask<states;mask++){
    const goal=universe.every(e=>(e&mask)!==0);
    assert.equal(goal,popcount(mask)>=min);
    if(goal)accepting++;
    const v=Math.min(popcount(mask),min);
    for(let i=0;i<n;i++){
      const next=mask|(1<<i), v2=Math.min(popcount(next),min);
      assert.ok(v2>=v&&v2-v<=((mask>>i&1)?0:1));
      transitionChecks++;
    }
  }
  assert.equal(accepting,Array.from({length:k},(_,i)=>choose(n,n-i)).reduce((a,b)=>a+b,0));
  const base=choose(n-1,k-1);
  assert.equal(universe.length/base,n/k);
  return {n,k,obligations:universe.length,states,transitionChecks,
    optimum:min,additiveDualNumerator:n,additiveDualDenominator:k,
    ratioNumerator:k*min,ratioDenominator:n};
}
function k4Control(){
 const edges=[];for(let a=0;a<4;a++)for(let b=a+1;b<4;b++)edges.push([a,b]);
 function F(charge){
   const clauses=[];
   for(let v=0;v<4;v++){
     const incident=edges.map((e,i)=>e.includes(v)?i:-1).filter(i=>i>=0);
     assert.equal(incident.length,3);
     for(let bits=0;bits<8;bits++){
       if(popcount(bits)%2===charge[v])continue;
       clauses.push(incident.map((id,j)=>(bits>>j&1)?-(id+1):(id+1)));
     }
   }
   return clauses;
 }
 function count(C){
   let models=0;
   for(let mask=0;mask<64;mask++){
     if(C.every(cl=>cl.some(l=>Boolean(mask>>(Math.abs(l)-1)&1)===(l>0))))models++;
   }
   return models;
 }
 const odd=F([1,0,0,0]),even=F([0,0,0,0]);
 assert.equal(odd.length,16);assert.equal(even.length,16);
 assert.equal(count(odd),0);assert.equal(count(even),8);
 for(let i=0;i<16;i++)assert.ok(count(odd.filter((_,j)=>j!==i))>0);
 return {variables:6,clauses:16,oddModels:0,evenModels:8,deletedClauseSATControls:16};
}
function main(){
 const records=[];for(let n=3;n<=11;n++)for(let k=2;k<=n;k++)records.push(full(n,k));
 for(const [n,k] of [[2,3],[3,1],[0,0],[-1,2]]){
   assert.throws(()=>full(n,k),/bad dimensions/);
 }
 const k4=k4Control();
 const out={schema:'LSPV1_545_HYPERGRAPH_COST_PARTITION/v1',
  status:'PROVED/RESTRICTED symbolic + COMPUTATIONAL finite; separate cover model; R_mix341 OPEN',
  configurations:records.length,
  exhaustiveSponsorStates:records.reduce((a,x)=>a+x.states,0),
  transitionChecks:records.reduce((a,x)=>a+x.transitionChecks,0),
  malformedRejections:4,k4Control:k4,records};
 assert.equal(out.configurations,54);assert.equal(out.exhaustiveSponsorStates,36864);
 return out;
}
if (require.main===module) process.stdout.write(JSON.stringify(main(),null,2)+'\n');
module.exports={full,k4Control,main};
