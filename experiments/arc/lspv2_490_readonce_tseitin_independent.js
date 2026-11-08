/* LSPV-2/490. Independent finite verifier; not historical R_mix341 or native FLMV. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),assert=require('node:assert/strict');
const graphs={
 K4:[4,[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]]],
 prism3:[6,[[0,1],[1,2],[2,0],[3,4],[4,5],[5,3],[0,3],[1,4],[2,5]]],
 cube:[8,Array.from({length:8},(_,v)=>[0,1,2].map(b=>[v,v^(1<<b)]).filter(pair=>pair[0]<pair[1])).flat()],
 petersen:[10,[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[5+i,5+((i+2)%5)]),...Array.from({length:5},(_,i)=>[i,5+i])]]
};
let assertions=0,rows=[];
function enc(n,edges,b){
 const incident=Array.from({length:n},()=>[]);
 edges.forEach(([a,c],i)=>{incident[a].push(i);incident[c].push(i)});
 const clauses=[];
 for(let v=0;v<n;v++){
  assert.equal(incident[v].length,3);assertions++;
  for(let p=0;p<8;p++){
   const val=[p&1,(p>>1)&1,(p>>2)&1];
   if((val[0]^val[1]^val[2])===b[v])continue;
   clauses.push(incident[v].map((e,j)=>(val[j]?-1:1)*(e+1)));
  }
 }
 return {clauses,incident};
}
function sourceSat(cs,x){
 for(const clause of cs){
  let ok=false;
  for(const lit of clause){
   let val=(x>>(Math.abs(lit)-1))&1;
   if(val===(lit>0?1:0)){ok=true;break}
  }
  if(!ok)return false;
 }
 return true;
}
function directBP(inc,charge,x){
 let depth=0;
 for(let v=0;v<inc.length;v++){
  let parity=0;
  for(const e of inc[v]){parity^=(x>>e)&1;depth++}
  if(parity!==charge[v])return [false,depth];
 }
 return [true,depth];
}
function correctSource(cs,b,n,edges){
 if(b.length!==n||b.some(t=>t!==0&&t!==1))return false;
 return JSON.stringify(cs)===JSON.stringify(enc(n,edges,b).clauses);
}
for(const [label,[n,edges]] of Object.entries(graphs)){
 const inc=enc(n,edges,Array(n).fill(0)).incident;
 let seed=0;for(let i=0;i<edges.length;i++)if(i%3===1)seed|=1<<i;
 const even=inc.map(es=>es.reduce((p,e)=>p^((seed>>e)&1),0));
 for(let odd=0;odd<=1;odd++){
  const b=even.slice();if(odd)b[0]^=1;
  const {clauses,incident}=enc(n,edges,b);
  assert.equal(clauses.length,4*n);assertions++;
  assert.equal(correctSource(clauses,b,n,edges),true);assertions++;
  for(const bad of [
   clauses.slice(1),
   clauses.concat([clauses[0]]),
   [clauses[0],clauses[0],...clauses.slice(2)],
   [clauses[0],[-clauses[1][0],clauses[1][1],clauses[1][2]],...clauses.slice(2)]
  ]){assert.equal(correctSource(bad,b,n,edges),false);assertions++}
  assert.equal(correctSource(clauses,[...b.slice(0,n-1),2],n,edges),false);assertions++;
  let sat=0,terms=[],maxDepth=0;
  for(let x=0;x<(1<<edges.length);x++){
   const fromCNF=sourceSat(clauses,x);
   const [fromBP,depth]=directBP(incident,b,x);
   assert.equal(fromCNF,fromBP);assertions++;
   assert.ok(depth<=2*edges.length);assertions++;
   maxDepth=Math.max(maxDepth,depth);
   if(fromCNF){
    sat++;terms.push(x);
    for(let e=0;e<edges.length;e++){
     assert.equal(sourceSat(clauses,x^(1<<e)),false);assertions++;
    }
   }
  }
  assert.equal(sat,odd?0:(1<<(edges.length-n+1)));assertions++;
  if(edges.length<=9){
   for(let x=0;x<(1<<edges.length);x++){
    const mintermOR=terms.some(t=>Array.from({length:edges.length},(_,i)=>((t>>i)&1)===((x>>i)&1)).every(Boolean));
    assert.equal(mintermOR,sourceSat(clauses,x));assertions++;
   }
  }
  rows.push({graph:label,vertices:n,edges:edges.length,odd,sat,maxDepth,read2Nodes:5*n+2});
 }
}
const result={run:'LSPV-2/490',independent:true,assertions,rows,note:'Finite exhaustive source/BP checks only; theorem transfer symbolic and sourced.'};
fs.writeFileSync(path.join(__dirname,'lspv2_490_js_raw.json'),JSON.stringify(result,null,2)+'\n');
console.log(JSON.stringify({assertions,rows:rows.length,SAT:4,UNSAT:4}));
