'use strict';
// Independent literal R_mix341 AND3 -> GF(2) -> XOR control. Node 18+.
// Every local row is reconstructed from FOUR original 3-literal parity clauses.
// No DEF facet or LOCAL private export is asserted to exist.
const A=require('assert');
let assertions=0;
function ok(c,s){assertions++; A.ok(c,s);}
const K=10n**80n,groups=120;
function localTuple(g){return [K-BigInt(3*g),K-BigInt(3*g+1),K-BigInt(3*g+2)];}
const xorbit=b=>b.reduce((acc,x)=>acc^x,0);
const rowValue=(r,m)=>xorbit(r.vars.map(v=>m.get(v)))===r.rhs;
const evalClause=(c,m)=>c.some(l=>{let x=m.get(l<0n?-l:l);return l>0n?x===1:x===0;});
function verifyGate(ids,cts,rhs){
  let truth=Array.from({length:8},(_,a)=>cts.every(c=>c[a]));
  for(let a=0;a<8;a++)
    ok(Number(truth[a])===Number(xorbit([0,1,2].map(i=>(a>>i)&1))===rhs),'false AND3 affine annotation');
  return {vars:ids,rhs};
}
let source=[],seeds=[],sat=new Map();
for(let g=0;g<groups;g++){
  let ids=localTuple(g),rhs=g%2,ct=[];
  for(let a=0;a<8;a++){
    let bits=[a&1,(a>>1)&1,(a>>2)&1];
    if(xorbit(bits)!==rhs){
      let clause=ids.map((v,i)=>bits[i]?-v:v);
      source.push(clause);
      ct.push(Array.from({length:8},(_,b)=>bits.some((bit,i)=>bit!==((b>>i)&1))));
    }
  }
  ok(ct.length===4,'four parity clauses');
  seeds.push(verifyGate(ids,ct,rhs)); // Three AND3 from four original clause factors.
  ids.forEach((v,i)=>sat.set(v,i===2?rhs:0));
  for(let c of source.slice(-4))ok(evalClause(c,sat),'matched SAT control');
}
let combined={vars:[],rhs:0};
for(let r of seeds){
  let S=new Set(combined.vars);
  for(let x of r.vars){if(S.has(x))S.delete(x);else S.add(x);}
  combined={vars:[...S].sort((a,b)=>a<b?-1:a>b?1:0),rhs:combined.rhs^r.rhs};
  ok(combined.vars.length<=3*seeds.length,'unexpected extra GF2 coordinate');
}
ok(combined.vars.length===360,'missing 360-way XOR support');
ok(rowValue(combined,sat),'derived row rejects SAT source witness');
for(let c of source)ok(evalClause(c,sat),'source clause falsified');
let bad=0;
for(let g=0;g<8;g++){
  let ids=localTuple(g),rhs=g%2,ct=[];
  for(let a=0;a<8;a++){
    let bits=[a&1,(a>>1)&1,(a>>2)&1];
    if(xorbit(bits)!==rhs)
      ct.push(Array.from({length:8},(_,b)=>bits.some((bit,i)=>bit!==((b>>i)&1))));
  }
  try{verifyGate(ids,ct,rhs^1);}catch(_){bad++;}
}
ok(bad===8,'false affine RHS accepted');
let aux=K+1n;
ok(!sat.has(aux),'auxiliary coordinate collision');
ok(![aux].every(x=>sat.has(x)),'unregistered DEF output accepted as original row');
let text='p cnf '+K+' '+source.length+'\n'+source.map(c=>c.join(' ')+' 0\n').join('');
let row=JSON.stringify({vars:combined.vars.map(String),rhs:combined.rhs});
ok(Buffer.byteLength(row)<Buffer.byteLength(text),'sparse encoding bound failed');
console.log(JSON.stringify({status:'COMPUTATIONAL',groups,original_clauses:source.length,
 paid_AND3:3*groups,paid_XOR:groups-1,final_row_support:combined.vars.length,
 source_bytes:Buffer.byteLength(text),sparse_row_bytes:Buffer.byteLength(row),
 rejected_corrupt_rows:bad,assertions,scope:'typed AND3/XOR fragment, not full native grammar or B3'},null,2));
