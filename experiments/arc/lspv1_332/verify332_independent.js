'use strict';
// Independent no-producer-import finite referee for LSPV-1 332.
const assert=require('assert').strict,crypto=require('crypto');
const clauses=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],
[-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]];
function sat(a,cs=clauses){
 for(const c of cs){let hit=false;for(const l of c){const b=(a>>(Math.abs(l)-1))&1;if(b===(l>0?1:0))hit=true;}if(!hit)return false;}
 return true;
}
function valid(cs,n){
 if(!Number.isSafeInteger(n)||n<3||3*cs.length!==4*n)return false;
 const ct=new Array(n*2).fill(0),seen=new Set();
 for(const c of cs){
  if(!Array.isArray(c)||c.length!==3||!c.every(v=>Number.isSafeInteger(v)&&v!==0&&Math.abs(v)<=n))return false;
  if(new Set(c.map(Math.abs)).size!==3)return false;
  if(!c.every(v=>v>0)&&!c.every(v=>v<0))return false;
  const key=[...c].sort((a,b)=>a-b).join(',');if(seen.has(key))return false;seen.add(key);
  for(const l of c)ct[2*(Math.abs(l)-1)+(l<0?1:0)]++;
 }
 return ct.every(v=>v===2);
}
let checks=0;function ok(x,msg){assert.ok(x,msg);checks++;}
ok(valid(clauses,9),'canonical F9');
function f(mode,x){return sat(mode===0?x:(mode===1?x&~1:x|1));}
const funcs=[0,1,2].map(mode=>Uint8Array.from({length:512},(_,x)=>f(mode,x)?1:0));
const weights=funcs.map(z=>z.reduce((a,b)=>a+b,0));
ok(JSON.stringify(weights)===JSON.stringify([70,80,60]),'lifted cofactor supports');
for(let x=0;x<512;x++){
 ok(funcs[0][x]===(sat(x)?1:0),'source truth');
 for(const c of clauses){
  let v=0,w=0;
  for(const l of c){
   v+=((x>>(Math.abs(l)-1))&1)===(l>0?1:0)?1:0;
   w+=(((x^511)>>(Math.abs(l)-1))&1)===(l>0?1:0)?1:0;
  }
  ok(v+w===3,'complement identity');
 }
}
let hashes=new Set(),supports=[];
for(let a=0;a<3;a++)for(let b=0;b<3;b++){
 const mask=Buffer.alloc(262144);let k=0;
 for(let y=0;y<512;y++)for(let x=0;x<512;x++)mask[k++]=funcs[a][x]&funcs[b][y];
 hashes.add(crypto.createHash('sha256').update(mask).digest('hex'));
 supports.push(mask.reduce((sum,v)=>sum+v,0));
}
ok(hashes.size===9,'nine distinct exact cofactor functions');
supports.sort((a,b)=>a-b);
ok(JSON.stringify(supports)===JSON.stringify([3600,4200,4200,4800,4800,4900,5600,5600,6400]),'supports');
let satLeaves=0,unsatLeaves=0,cover=[];
for(let pivot=0;pivot<=1;pivot++)for(let x2=0;x2<=1;x2++)for(let x4=0;x4<=1;x4++)for(let x9=0;x9<=1;x9++){
 const x=(pivot<<0)|(x2<<1)|(x4<<3)|(1<<4)|(x9<<8);
 if(sat(x)){ok(pivot===0,'wrong label');satLeaves++;}
 else if(pivot===1){
  unsatLeaves++;
  cover.push(clauses.findIndex(c=>!c.some(l=>((x>>(Math.abs(l)-1))&1)===(l>0?1:0)))+1);
 }
}
ok(satLeaves===2&&unsatLeaves===8,'same original SAT2 UNSAT0');
ok(cover.every(x=>x>=1&&x<=12),'original source clause cover');
let pairs=0,infeasible=0;
for(let j=0;j<12;j++)for(let k=j+1;k<12;k++)for(let a=0;a<2;a++)for(let b=0;b<2;b++){
 const assigned=new Map();let feasible=true;
 for(const [idx,mode] of [[j,a],[k,b]])for(const l of clauses[idx]){
  const need=mode===1?(l>0?1:0):(l>0?0:1),id=Math.abs(l);
  if(assigned.has(id)&&assigned.get(id)!==need)feasible=false;
  assigned.set(id,need);
 }
 let same=false,opp=false;
 for(const l of clauses[j])for(const r of clauses[k])if(Math.abs(l)===Math.abs(r)){
  if((l>0)===(r>0))same=true;else opp=true;
 }
 ok(feasible===(a===b?!opp:!same),'SS/SU/US/UU rule');
 pairs++;if(!feasible)infeasible++;
}
ok(pairs===264,'pair modes');
const bad=[[...clauses,clauses[0]],clauses.slice(0,-1),
clauses.map((c,j)=>j===0?[1,1,6]:c),
clauses.map((c,j)=>j===0?[1,-5,6]:c),
clauses.map((c,j)=>j===0?[1,5,10]:c),
clauses.map((c,j)=>j===0?[1,5,7]:c),
clauses.map((c,j)=>j===0?[true,5,6]:c)];
for(const x of bad)ok(!valid(x,9),'malformed rejected');
process.stdout.write(JSON.stringify({independent_assertions:checks,
  canonical_models:weights[0],cofactor_supports:weights,
  exact_two_block_classes:hashes.size,exact_two_block_supports:supports,
  same_original_sat:2,same_original_unsat:0,unsat_source_cover:cover,
  pair_modes:pairs,infeasible_pair_modes:infeasible,malformed_rejected:bad.length,
  status:'COMPUTATIONAL only; P versus NP OPEN'},null,2)+'\n');
