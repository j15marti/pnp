'use strict';
// Independently runnable restricted deterministic phase commutation test.
// This is NOT a native FLMV simulator or a general SAT solver.
const assert=require('node:assert/strict'),crypto=require('node:crypto');
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function tseitin(ch){
 let clauses=[];
 for(let v=0;v<4;v++){
  let incident=edges.flatMap(([a,b],i)=>a===v||b===v?[i+1]:[]);
  for(let m=0;m<8;m++){
   let b=[(m>>2)&1,(m>>1)&1,m&1];
   if((b[0]^b[1]^b[2])!==ch[v])clauses.push(incident.map((x,j)=>b[j]?-x:x));
  }
 }
 return {src:'p cnf 6 16\n'+clauses.map(c=>c.join(' ')+' 0\n').join(''),clauses};
}
function sat(clauses){
 for(let mask=0;mask<64;mask++)
  if(clauses.every(c=>c.some(l=>!!(mask&(1<<(Math.abs(l)-1)))===(l>0))))return true;
 return false;
}
function phase(program,initial){
 let memory=new Map(initial),reads=new Set(),writes=new Set(),trace=[],output=[];
 function get(a){return memory.get(a)??0}
 for(let [op,a,val] of program){
  if(op==='READ'){reads.add(a);output.push(get(a));trace.push('R:'+a+':'+get(a))}
  else if(op==='WRITE'){writes.add(a);memory.set(a,val);trace.push('W:'+a+':'+val)}
  else if(op==='COPY'){let v=get(a);reads.add(a);writes.add(val);memory.set(val,v);trace.push('R:'+a+':'+v,'W:'+val+':'+v)}
  else if(op==='INDWRITE'){let v=get(a),dest=v%16;reads.add(a);writes.add(dest);memory.set(dest,val);trace.push('R:'+a+':'+v,'W:'+dest+':'+val)}
  else throw Error('unknown op');
 }
 return {memory,reads,writes,trace,output};
}
function intersect(a,b){for(let v of a)if(b.has(v))return true;return false}
function union(a,b){return new Set([...a,...b])}
function sameMemory(a,b){for(let i=0;i<16;i++)if((a.get(i)??0)!==(b.get(i)??0))return false;return true}
function analyze(p,q,m){
 let P=phase(p,m),Q=phase(q,P.memory),QR=phase(q,m),PR=phase(p,QR.memory);
 let safe=!(intersect(P.writes,union(Q.reads,Q.writes))||intersect(Q.writes,union(P.reads,P.writes)));
 let eq=(sameMemory(Q.memory,PR.memory)&&JSON.stringify(P.trace)===JSON.stringify(PR.trace)&&
          JSON.stringify(Q.trace)===JSON.stringify(QR.trace)&&
          JSON.stringify(P.output)===JSON.stringify(PR.output)&&JSON.stringify(Q.output)===JSON.stringify(QR.output));
 return {safe,eq};
}
let seed=511;
function rand(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
function randomPhase(){let p=[];for(let j=rand(4)+1;j>0;j--){let op=['READ','WRITE','COPY','INDWRITE'][rand(4)];p.push([op,rand(16),op==='COPY'?rand(16):rand(4)])}return p}
let checks=0,safeReorders=0,badGuard=0,different=0;
for(let mask=0;mask<16;mask++){
 let c=[0,1,2,3].map(j=>(mask>>j)&1),f=tseitin(c);
 assert.equal(sat(f.clauses),(c.reduce((a,b)=>a+b,0)%2===0));checks++;
}
for(let i=0;i<4096;i++){
 let m=new Map(Array.from({length:16},(_,j)=>[j,rand(4)])),p=randomPhase(),q=randomPhase();
 let {safe,eq}=analyze(p,q,m);
 if(safe){assert(eq,JSON.stringify({p,q,m:[...m]}));safeReorders++;checks++}else badGuard++;
 if(!eq)different++;
}
assert(safeReorders>1000);checks++;assert(badGuard>1000);checks++;
let hostile=[
 [[['WRITE',1,1]],[['READ',1,0]]],
 [[['WRITE',1,1]],[['WRITE',1,2]]],
 [[['WRITE',1,2]],[['INDWRITE',1,3]]],
 [[['COPY',0,1]],[['WRITE',0,3]]]];
for(let [p,q] of hostile){assert.equal(analyze(p,q,new Map(Array.from({length:16},(_,j)=>[j,0]))).safe,false);checks++}
let valid=new Set(Array.from({length:16},(_,mask)=>tseitin([0,1,2,3].map(v=>(mask>>v)&1)).src));
let base=tseitin([0,0,0,0]).src;
let malformed=['','garbage',base+'\n',base.replace('p cnf 6 16','p cnf 7 16'),
 base.replace(' 0\n',' 1\n'),base.slice(0,-2),base.replace(' 0\n',' 0\n0\n')];
for(let source of malformed){assert.equal(valid.has(source),false);checks++}
let P=[['WRITE',1,1]],Q=[['READ',1,0]];
let first=phase(P,new Map(Array.from({length:16},(_,j)=>[j,0])));
let second=phase(Q,first.memory);
assert.equal(analyze(P,Q,new Map(Array.from({length:16},(_,j)=>[j,0]))).safe,false);checks++;
assert.equal(intersect(first.writes,union(new Set(),second.writes)),false);checks++; // Forged read-set omission wrongly accepts.
console.log(JSON.stringify({status:'PASS',assertions:checks,safe_reorders:safeReorders,failed_guard:badGuard,
 observably_different_orders:different,random_cases:4096,hostile_controls:4,
 malformed_source_controls:malformed.length,forged_footprint_controls:1,
 original_k4_tseitin:16,sat:8,unsat:8,
 first_source_sha256:crypto.createHash('sha256').update(base).digest('hex'),
 scope:'two isolated deterministic memory phases with complete trusted dynamic read/write sets, finite symbolic tests only'},null,2));
