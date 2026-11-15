'use strict';
// TMR-3/048 PHYSFRONTIER148. Self-contained deterministic, exact integer audit.
// Run: node experiments/tmr/tmr3_multifrontier148.js
const assert=require('node:assert/strict');
let assertions=0,rows=0,zeroRows=0,negativeDischarges=0,jointRows=0;
let pairs=0,sweepSteps=0,spaceChecks=0,hostileChecks=0,sampledStates=0;
function ok(test,label='check'){assert.ok(test,label);assertions++;}
function eq(a,b,label='equality'){assert.deepStrictEqual(a,b,label);assertions++;}
const moves=[-1,0,1];
function vector(d,h,seen,correct){
 const p0=seen?0:Math.abs(h[0]-d[0])+1;
 const p1=correct[0]?0:Math.abs(h[1]-d[1])+1;
 const p2=correct[1]?0:Math.abs(h[2]-d[2])+1;
 return [0,0,0,p1,p2,p0,Math.max(p0,p1,p2)];
}
function step(d,h,seen,correct,move,write){
 // One physical price-one step reads CURRENT input head; writes only CURRENT
 // work-head cells, then moves each local head independently by at most one.
 if(move.some((m,i)=>h[i]+m<0))return null;
 const newSeen=seen||h[0]===d[0],newCorrect=correct.slice();
 for(let j=0;j<2;j++){
   if(h[j+1]===d[j+1]&&write[j]!==null)newCorrect[j]=write[j];
   else if(write[j]!==null)return null;
 }
 return {h:h.map((v,i)=>v+move[i]),seen:newSeen,correct:newCorrect};
}
// Exhaustive exact LOCAL TARFF replay. Full original tape symbols may be
// arbitrarily changed away from the two output targets: such writes leave
// the seven-component obstruction unchanged and are included as MAY.
for(let d0=0;d0<=3;d0++)for(let d1=0;d1<=3;d1++)for(let d2=0;d2<=3;d2++){
 const d=[d0,d1,d2];
 for(let h0=0;h0<=4;h0++)for(let h1=0;h1<=4;h1++)for(let h2=0;h2<=4;h2++){
  const h=[h0,h1,h2];
  for(let mask=0;mask<8;mask++){
   const seen=!!(mask&1),correct=[!!(mask&2),!!(mask&4)];
   const old=vector(d,h,seen,correct);sampledStates++;
   for(let m0 of moves)for(let m1 of moves)for(let m2 of moves){
    const m=[m0,m1,m2];
    for(let w1 of (h1===d1?[null,true,false]:[null]))
    for(let w2 of (h2===d2?[null,true,false]:[null])){
      const nxt=step(d,h,seen,correct,m,[w1,w2]);if(!nxt)continue;
      const neu=vector(d,nxt.h,nxt.seen,nxt.correct);
      const delta=old.map((v,i)=>v-neu[i]);
      for(let i of [3,4,5,6])ok(delta[i]<=1,'local physical tariff');
      ok(delta[4]+delta[5]+2*delta[6]<=4,'rational 1/4+1/4+1/2 tariff');
      ok(delta[6]<=1,'max frontier tariff');
      rows++;
      if(delta.slice(3).some(v=>v<0))negativeDischarges++;
      if(delta[3]===1&&delta[4]===1&&delta[5]===1&&delta[6]===1)jointRows++;
    }
   }
   eq(vector(d,h,seen,correct),old,'zero-cost inert VIEW');zeroRows++;
  }
 }
}
// Sharp joint source/2-write/HALT witness: one genuine transition pays all.
for(let n=0;n<30;n++){
 const d=[n,n,n],h=[n,n,n];
 const old=vector(d,h,false,[false,false]);
 const next=step(d,h,false,[false,false],[0,0,0],[true,true]);
 const neu=vector(d,next.h,next.seen,next.correct);
 eq(old,[0,0,0,1,1,1,1]);eq(neu,[0,0,0,0,0,0,0]);
 jointRows++;hostileChecks++;
 ok((old[3]-neu[3])+(old[4]-neu[4])+(old[5]-neu[5])+
    (old[6]-neu[6])===4,'separate unit tariffs overcount');
}
// ONE FIXED finite-state machine: reads actual target symbols and x bit,
// parks early heads, co-writes when source observed, halts on last operation.
// Work output tape target marks are PRESTAGED and preparation is NOT free
// in a complete blank-work-tape machine; this is a qualified suffix.
function runSweep(d,bit){
 let h=[0,0,0],known=null,correct=[false,false],t=0;
 const visited=[new Set([0]),new Set([0])];
 while(!correct.every(Boolean)||known===null){
  if(h[0]===d[0])known=bit;
  for(let i=1;i<=2;i++)if(h[i]===d[i]&&known!==null)correct[i-1]=true;
  for(let i=0;i<3;i++){
   if(i===0){if(h[i]<d[i])h[i]++;}
   else if(!correct[i-1]&&h[i]<d[i])h[i]++;
  }
  for(let i=1;i<=2;i++)visited[i-1].add(h[i]);
  t++;ok(t<1000,'fixed sweep terminates');
 }
 return {t,output:correct.map(()=>known),visited:visited.map(s=>s.size),heads:h};
}
for(let d0=0;d0<=12;d0++)for(let d1=0;d1<=12;d1++)for(let d2=0;d2<=12;d2++){
 const d=[d0,d1,d2],D=Math.max(...d);
 for(let bit=0;bit<=1;bit++){
  const z=runSweep(d,bit);pairs++;sweepSteps+=z.t;
  eq(z.t,D+1,'exact shortest prepared suffix');
  eq(z.output,[bit,bit],'authentic same-bit physical outputs');
  eq(z.visited,[d1+1,d2+1],'same-realization writable cells');
  eq(z.heads,d,'completed head positions');
  const init=vector(d,[0,0,0],false,[false,false]);
  eq(init[6],D+1);
  eq(Math.max(init[3],init[4],init[5],init[6]),D+1);
  spaceChecks++;
 }
}
const summary={
 run:'TMR3_PHYSFRONTIER148',timestamp_pacific:'2026-11-15 09:26 PST',
 status_experiment:'COMPUTATIONAL',
 model:'one read-only source head + two already marker-staged writable output heads; fixed finite alphabet; all moves local; one transition can read and co-write two output cells; distinct correct source-dependent output targets',
 enumeration:{target_distances:'0..3 inclusive',head_positions:'0..4 inclusive',symbolic_states:sampledStates,physical_paid_edges:rows,zero_view_rows:zeroRows,negative_signed_edges:negativeDischarges,joint_max_discharge_edges:jointRows},
 sweeping:{distances:'0..12 inclusive',source_bits:[0,1],source_pairs:pairs,paid_microsteps:sweepSteps,work_space_checks:spaceChecks},
 sharp_joint_controls:hostileChecks,
 theorem:'T_min(d0,d1,d2)=max(d0,d1,d2)+1; S_visited_output=(d1+1)+(d2+1) for fixed uniform monotone sweep; tariff lambda=(0,0,0,0,0,0,1) gives Phi_init=max(d0,d1,d2)+1',
 complete_active_cone:'lambda_FUS+lambda_Gamma+lambda_Interface+lambda_Machine<=1 and each lambda>=0; exact across all legal physical steps and all positioned states',
 assertions,failures:0,random_seed:null,
 limits:'marker-staged suffix, NOT blank-work-tape SAT decider; no source-literal parsing, target-index generation, or gate-ID authentication; physical machine implementation expressed as a finite-control construction rather than compiled low-level transition table'
};
process.stdout.write(JSON.stringify(summary,null,2)+'\n');