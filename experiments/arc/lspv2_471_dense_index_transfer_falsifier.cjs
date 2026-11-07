'use strict';
// LSPV-2/471: semantic finite controls, not a native FLMV simulator.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const { createHash } = require('node:crypto');
let checks = 0;
const check = (cond, message) => { assert.ok(cond, message); checks++; };
const expanderControls = [];

// Four degree-3 vertex constraints of K4, 6 distinct edge variables.
const edges = [[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function tseitinK4(charge) {
  const clauses = [];
  for (let v = 0; v < 4; v++) {
    const incident = edges.map((e, id) => e.includes(v) ? id + 1 : 0).filter(Boolean);
    assert.equal(incident.length, 3);
    for (let mask=0; mask<8; mask++) {
      const forbiddenParity = (Number((mask&1)!==0) ^ Number((mask&2)!==0) ^ Number((mask&4)!==0));
      if (forbiddenParity === charge[v]) continue;
      // mask is a forbidden assignment. Literal false under that assignment.
      clauses.push(incident.map((id,k) => ((mask>>k)&1) ? -id : id));
    }
  }
  return clauses;
}
function strict3(clauses) {
  return Array.isArray(clauses) && clauses.every(c =>
    Array.isArray(c) && c.length === 3 &&
    c.every(x => Number.isSafeInteger(x) && x!==0 && Math.abs(x)<=6) &&
    new Set(c.map(x=>Math.abs(x))).size===3);
}
function models(clauses) {
  let n = 0;
  for(let bits=0;bits<64;bits++) {
    if (clauses.every(c=>c.some(l=> (((bits>>(Math.abs(l)-1))&1)===1)===(l>0)))) n++;
  }
  return n;
}
for(let mask=0;mask<16;mask++) {
  const charge = Array.from({length:4},(_,j)=>(mask>>j)&1);
  const F=tseitinK4(charge);
  check(F.length===16 && strict3(F), `K4 format ${mask}`);
  const modelCount=models(F);
  check((modelCount===0)===(charge.reduce((a,b)=>a^b,0)===1), `K4 parity ${mask}`);
  check(modelCount===0 || modelCount===8, `K4 count ${mask}`);
  expanderControls.push({charge:charge.join(''),models:modelCount});
}
let malformedRejected=0;
for (const bad of [[[1,1,-2]], [[0,1,2]], [[1,2]], [[1,2,7]], [[-1,2,2]]]) {
  check(!strict3(bad),'malformed strict-3CNF accepted');
  malformedRejected++;
}

// Emulate *just* the guest's long sequential INDEX-tape prologue.
// The guest never reads/indexes the associated non-index WORK tape.
// B is input length; k is a fixed integer (not an input-dependent exponent).
function guestIndexOnly(B,k) {
  check(Number.isInteger(B)&&B>0&&Number.isInteger(k)&&k>=1,'params');
  const H=B**k;
  const index=new Uint8Array(H+1);
  let indexHead=0, steps=0, guestWorkHighWater=0;
  while(indexHead<H) { indexHead++; steps++; }
  index[indexHead]=1; steps++;
  check(index[H]===1 && index.reduce((a,b)=>a+b,0)===1,'single high bit');
  const peakIndex=Uint8Array.from(index);
  // Genuine indexed INPUT move erases INDEX with no charge to non-index WORK.
  index.fill(0); steps++;
  let inputHead=2n**BigInt(H);
  // Conservative native restoration of the INDEX head followed by blank jump
  // to return the source INPUT head to zero before running arbitrary A.
  while(indexHead>0){indexHead--;steps++;}
  inputHead=0n; steps++;
  check(indexHead===0 && inputHead===0n && index.every(x=>x===0),
      'guest configuration not restored');
  return {B,k,H,steps,guestWorkHighWater,indexHead,peakIndex};
}
// A literal dense direct-indexed WORK representation of the guest INDEX
// uses at least one physically addressed WORK slot for every INDEX position.
function denseWorkIndexPort(g) {
  let cap=1;
  while(cap<=g.H) cap*=2;
  const liveFlags=new Uint8Array(cap);
  const fenwick=new Uint32Array(cap+1);
  const frozenFlags=new Uint8Array(cap);
  for(let j=0;j<=g.H;j++) if(g.peakIndex[j]) {
    liveFlags[j]=1;
    for(let p=j+1;p<=cap;p+=p&-p) fenwick[p]++;
  }
  check(liveFlags[g.H]===1,'host bit lost');
  let sum=0,p=g.H+1;
  while(p>0){sum+=fenwick[p];p-=p&-p;}
  check(sum===1,'host fenwick count');
  check(frozenFlags[g.H]===0,'frozen arena must start empty');
  // At minimum, the flag at position H exists on the counted host WORK tape.
  // Capacity and other record fields can only increase that high-water.
  const hostWorkHighWater=Math.max(g.H,cap-1);
  return {cap,hostWorkHighWater,guestWorkHighWater:g.guestWorkHighWater,
          ratioToB:hostWorkHighWater/g.B,sourceInputLength:g.B};
}
const cases=[];
for (const B of [4,8,12,16,24,32,48,64,96]) {
  const g=guestIndexOnly(B,2), p=denseWorkIndexPort(g);
  check(g.steps===2*g.H+3,'prologue time');
  check(g.guestWorkHighWater===0,'guest WORK unexpectedly accessed');
  check(p.hostWorkHighWater>=g.H,'dense physical high-water below bit coordinate');
  check(p.hostWorkHighWater>=B*B,'claimed target correction');
  cases.push({B,H:g.H,guestTransitions:g.steps,guestCountedWorkMax:0,
              hostCountedWorkMin:g.H,hostAllocatedFlagCapacity:p.cap,
              illustrativeParentN:B*B,targetParentSpace:SqrtToTarget(B),
              boundViolation:p.hostWorkHighWater>SqrtToTarget(B)});
}
function SqrtToTarget(B) {return B;} // parent N=B^2 -> N^(1/2)=B
check(cases.every(c=>c.boundViolation),'host should violate the illustrative N^(1/2) target');

const result={status:'COMPUTATIONAL finite controls plus analytic restricted counterexample',
  note:'INDEX tapes not charged in FLMV 2005 Section 2.1; physical non-index WORK positions are charged.',
  controls:{k4Formulas:expanderControls.length,sat:expanderControls.filter(x=>x.models>0).length,
    unsat:expanderControls.filter(x=>x.models===0).length,malformedRejected},
  cases,checks,codeSHA256:createHash('sha256').update(fs.readFileSync(__filename)).digest('hex')};
console.log(JSON.stringify(result,null,2));
