// ARC204: finite hostile controls for fixed sequential-work-head rejecting histories.
// Deterministic, exhaustive, zero external dependencies.
// This is a toy guest, not an unrestricted SAT solver.
"use strict";
const assert = require("assert");
function step(i, r) {
  if (i === 0 && r === 0) return {write:1,next:"s1",move:1};
  if (i === 1 && r === 0) return {write:0,next:"s2",move:-1};
  if (i === 2 && r === 0) return {write:0,next:"REJECT",move:0};
  if (i === 2 && r === 1) return {write:1,next:"ACCEPT",move:0};
  return null;
}
function inspect(trace, wantReject=true) {
  if (!Array.isArray(trace) || trace.length !== 3) return {local:false,valid:false,bad:"length"};
  let state="s0", head=0, memory=new Map(), firstBad=null;
  for (let i=0;i<3;i++) {
    const rec=trace[i];
    if (rec.state!==state || rec.head!==head) return {local:false,valid:false,bad:"state/head"};
    const transition=step(i,rec.read);
    if (!transition || rec.write!==transition.write || rec.next!==transition.next)
      return {local:false,valid:false,bad:"local transition"};
    const real=memory.get(head)??0;
    if (firstBad===null && rec.read!==real) firstBad={step:i,head,expected:real,claimed:rec.read};
    memory.set(head,rec.write);
    state=transition.next; head+=transition.move;
  }
  if (wantReject && state!=="REJECT") return {local:false,valid:false,bad:"wrong polarity"};
  if (!wantReject && state!=="ACCEPT") return {local:false,valid:false,bad:"wrong polarity"};
  return {local:true,valid:firstBad===null,bad:firstBad};
}
function record(r0,w0,r1,w1,r2,w2) {
  const values=[[r0,w0],[r1,w1],[r2,w2]];
  const states=["s0","s1","s2"], positions=[0,1,0];
  return values.map(([read,write],i)=>{
    const t=step(i,read);
    return {state:states[i],head:positions[i],read,write,next:t?t.next:"BAD"};
  });
}
let tests=0, localReject=0, authenticReject=0, forged=0, localAccept=0, authenticAccept=0;
for(let mask=0;mask<64;mask++){
  const bits=Array.from({length:6},(_,i)=>(mask>>i)&1);
  const tr=record(...bits);
  for(const wantReject of [true,false]){
    const r=inspect(tr,wantReject);
    if(r.local && wantReject)localReject++;
    if(r.valid && wantReject)authenticReject++;
    if(r.local && !wantReject)localAccept++;
    if(r.valid && !wantReject)authenticAccept++;
    // Every invalid record has an explicit finite local or last-write violation.
    assert.strictEqual(r.valid,r.local && r.bad===null);
    if(r.local && !r.valid){ assert.strictEqual(typeof r.bad.step,"number"); if(wantReject)forged++; }
    tests+=2;
  }
}
assert.strictEqual(localReject,1);
assert.strictEqual(authenticReject,0);
assert.strictEqual(forged,1);
assert.strictEqual(localAccept,1);
assert.strictEqual(authenticAccept,1);
const forgedTrace=record(0,1,0,0,0,0);
assert.deepStrictEqual(inspect(forgedTrace,true).bad,{step:2,head:0,expected:1,claimed:0});
tests++;
// General chronological last-write invariant, including writes of zero and aliasing.
let lastWriteChecks=0;
for(let code=0;code<6**5;code++){
  let n=code, writes=[], memory=new Map();
  for(let j=0;j<5;j++){const d=n%6;n=Math.floor(n/6);const addr=Math.floor(d/2),val=d%2;writes.push({addr,val});memory.set(addr,val);}
  for(let addr=0;addr<3;addr++){
    let last=0; for(const w of writes)if(w.addr===addr)last=w.val;
    assert.strictEqual(last,memory.get(addr)??0);
    lastWriteChecks++;
  }
}
const raw={run:"ARC204_TRACE_BAD_WITNESS_POLARITY",status:"COMPUTATIONAL",date:"2026-10-27",toyGuestCorrectSAT:false,exhaustiveTraces:64,polarityChecks:128,localReject,authenticReject,forged,localAccept,authenticAccept,lastWriteChecks,assertions:tests+lastWriteChecks,failures:0,notes:["A locally legal forged rejecting trace skips a previously written value.","Nondeterministic bad-witness detection accepts invalid transcripts, not valid UNSAT certificates.","The symbolic theorem applies to any fixed sequential-head deterministic guest and does not use the toy's SAT semantics."]};
console.log(JSON.stringify(raw,null,2));
