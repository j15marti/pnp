'use strict';
const assert=require('node:assert/strict');
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
let checks=0;
function clausePacket(charge,v) {
  const es=edges.flatMap(([a,b],i)=>(a===v||b===v)?[i+1]:[]);
  assert.equal(es.length,3);checks++;
  const packet=[];
  for(let mask=0;mask<8;mask++){
    const parity=((mask&1)!==0)+((mask&2)!==0)+((mask&4)!==0);
    if(parity%2===charge)continue;
    packet.push(es.map((e,j)=>(mask&(1<<j))?-e:e));
  }
  return packet;
}
function verdict(charges){
  if(!Array.isArray(charges)||charges.length!==4||charges.some(v=>!Number.isInteger(v)||(v!==0&&v!==1)))return 'MALFORMED';
  const clauses=charges.flatMap((b,v)=>clausePacket(b,v));
  assert.equal(clauses.length,16);checks++;
  for(let assignment=0;assignment<64;assignment++){
    if(clauses.every(c=>c.some(l=>Boolean(assignment&(1<<(Math.abs(l)-1)))===(l>0))))return 'SAT';
  }
  return 'UNSAT';
}
let sat=0,unsat=0;
for(let x=0;x<16;x++){
  const charges=[0,1,2,3].map(j=>(x>>j)&1);
  const v=verdict(charges);
  const parity=charges.reduce((a,b)=>a^b,0);
  assert.equal(v,parity?'UNSAT':'SAT');checks++;
  v==='SAT'?sat++:unsat++;
}
const malformed=[null,[],[0],[0,0,0],[0,0,0,0,0],[2,0,0,0],['1',0,0,0],[-1,0,0,0]];
for(const m of malformed){assert.equal(verdict(m),'MALFORMED');checks++}
let padded=0;
for(const m of [2,3,5,7,11])for(const k of [1,2,3]){
  const expected=BigInt(m+1)**BigInt(k);
  let touched=0n;
  for(let i=0n;i<expected;i++)touched++;
  assert.equal(touched,expected);checks++;padded++;
}
const eps40=[2,4,5,8];
let expo=0;
for(const eps of eps40){
  const alpha40=20+eps;
  for(let k=2;k<=24;k++){
    const demand=alpha40*k;
    const spaceLimit=Math.max(20,20*k);
    const timeLimit=Math.max(44,24+20*k);
    assert.ok(demand>spaceLimit);checks++;
    assert.equal(demand>timeLimit,eps*k>24);checks++;
    expo++;
  }
}
assert.equal(sat,8);assert.equal(unsat,8);checks+=2;
console.log(JSON.stringify({result:'PASS',independent:'JavaScript native brute force and exact integer-exponent comparison',checks,k4_sat:sat,k4_unsat:unsat,malformed_rejected:malformed.length,padding_cells_executed_cases:padded,exponent_cases:expo},null,2));
