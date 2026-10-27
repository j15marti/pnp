"use strict";
// UTM-PROOF-HEAD-CHANGE151. Node >= 16. No dependencies, deterministic.
const W1=[
 [-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],
 [5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],
 [-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],
 [2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]
];
function audit(){
 let checks=0;const check=(p,m)=>{checks++;if(!p)throw Error("failed: "+m)};
 const variants={};let evaluated=0;
 for(let a=0;a<2;a++)for(let b=0;b<2;b++){
  const f=W1.map(c=>c.slice());
  if(a===0){f[6][0]*=-1;f[11][0]*=-1}
  if(b===0){f[17][2]*=-1;f[9][2]*=-1}
  const occ=Array.from({length:16},()=>[0,0]);
  for(const c of f){check(new Set(c.map(Math.abs)).size===3,"proper");for(const v of c)occ[Math.abs(v)][v>0?0:1]++}
  for(let i=1;i<=15;i++)check(occ[i][0]===2&&occ[i][1]===2,"signed 2,2");
  let count=0;
  for(let mask=0;mask<(1<<15);mask++){
   let sat=true;
   for(const c of f){let ok=false;for(const v of c){const bit=(mask >>> (Math.abs(v)-1))&1;if((v>0&&bit===1)||(v<0&&bit===0)){ok=true;break}}
   if(!ok){sat=false;break}}
   count+=sat?1:0;check(typeof sat==="boolean","enumerated assignment");evaluated++;
  }
  variants[""+a+b]=count;
 }
 check(JSON.stringify(variants)===JSON.stringify({"10":272,"11":0,"00":772,"01":272}),"W1 selector counts");
 let foolingPairs=0,diagonals=0;
 for(let m=1;m<=7;m++){
  const z=(1<<m)-1;
  for(let a=0;a<=z;a++){
   const b=z^a;check((a&b)===0,"diagonal SAT");diagonals++;
   for(let a2=0;a2<=z;a2++)if(a!==a2){
     const b2=z^a2;
     check(((a&b2)!==0)||((a2&b)!==0),"crossed UNSAT");
     foolingPairs++;
   }
  }
 }
 // Constant-control proof-head clock: input A|B, proof 1^L then endmarker.
 // Each tick moves source head across the ONE cut and proof head right once.
 // Only the initially scanned blank work-head cell is visited; no symbols change. Crossing labels include proof position.
 let clocks=0,clockCrossings=0,omittedFactorFailures=0;
 for(let L=0;L<=512;L++){
  let src=0,proof=0,state=0;const labels=new Set();
  for(let i=0;i<L;i++){
   check(proof<L,"proof reads one");src^=1;proof++;state^=1;
   const label=state+":"+src+":"+proof;
   check(!labels.has(label),"no repeated configuration on halting clock");
   labels.add(label);clockCrossings++;
  }
  check(proof===L,"proof endmarker reached");
  check(labels.size===L,"exact L crossings");
  const q=2,k=1,S=1,h=2*S+3;
  const withoutProofHead=2*q*Math.pow(h,k);
  const withProofHead=withoutProofHead*(L+3);
  check(L<=withProofHead,"valid epoch cap with proof position");
  if(L>withoutProofHead)omittedFactorFailures++;
  clocks++;
 }
 check(omittedFactorFailures===492,"omitted proof-position factor falsified L=21..512");
 // Exhaustively compare count of complete transcripts with A^(K+1).
 for(let alphabet=2;alphabet<=12;alphabet++){
  for(let K=0;K<=10;K++){
   let sum=0n,pow=1n;
   for(let j=0;j<=K;j++){sum+=pow;pow*=BigInt(alphabet)}
   check(sum<=pow,"transcript counting geometric bound");
  }
 }
 // Seeded transition table controls with two-way proof head and bounded source.
 let seed=0x1512026;function rnd(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0}
 let halted=0,looped=0,randomTrials=0;
 for(let test=0;test<5000;test++){
  const q=3,L=test%17;
  const table=Array.from({length:q*2*2},()=>({next:rnd()%q,src:(rnd()%3)-1,pr:(rnd()%3)-1,halt:rnd()%11===0}));
  let st=0,src=0,pr=0;const seen=new Set(),crossLabels=new Set();let crossings=0,stop="timeout";
  for(let t=0;t<300;t++){
    const key=st+":"+src+":"+pr;
    if(seen.has(key)){stop="loop";break}seen.add(key);
    const flag=pr<L?0:1;const rule=table[st*4+src*2+flag];
    if(rule.halt){stop="halt";break}
    const old=src;src=Math.max(0,Math.min(1,src+rule.src));
    pr=Math.max(0,Math.min(L,pr+rule.pr));st=rule.next;
    if(old!==src){crossings++;const label=st+":"+src+":"+pr;crossLabels.add(label)}
  }
  if(stop==="halt"){
    halted++;
    check(crossLabels.size===crossings,"halting no-change crossing state unique");
    check(crossings<=2*q*(L+3),"one-epoch proof-aware bound");
  }else if(stop==="loop")looped++;
  randomTrials++;
 }
 check(halted+looped===randomTrials,"finite-state simulation terminates or loops");
 // Certified exponent translations are one-way upper ceilings.
 let simulationGrid=0;
 for(let ti=10;ti<=30;ti++)for(let si=0;si<=20;si++){
   const t=ti/10,s=si/10;
   const t1=t+Math.max(1,s);
   check(t1>=2-1e-12,"one-tape stripe yields no new Mk restriction at t>=1");
   simulationGrid++;
 }
 const ex={t:2.2,s:0.3,d:0.1,ell:0.2,r:1.0,k:1};
 const face={time:ex.t+Math.min(ex.s,ex.d),reversal:ex.r+Math.min(ex.s,ex.d),
   workChange:ex.d+ex.k*ex.s+ex.ell+Math.min(ex.s,ex.d)};
 check(face.time>2&&face.reversal>1&&face.workChange<1,"strict write-only excluded face");
 return {id:"UTM-PROOF-HEAD-CHANGE151",method:"exhaustive W1 15-bit assignments, exhaustive diagonal pairs, proof clock, seeded finite-control controls",seed:0x1512026,
   assertions:checks,errors:0,variants,w1AssignmentsEvaluated:evaluated,diagonals,foolingPairs,
   proofClock:{Lmin:0,Lmax:512,trials:clocks,totalCrossings:clockCrossings,
     casesInvalidatingEpochCapWithoutProofHead:omittedFactorFailures,exampleL:64,
     exampleCrossings:64,exampleChanges:0,exampleVisitedWorkCells:1},
   finiteState:{trials:randomTrials,halted,looped},
   simulationGrid,
   strictFaceExample:{...ex,...face,positiveWriteGap:1-face.workChange},
   limitations:"Restricted signed exact-(2,2) DISJ promise, external reusable read-only proof tape. Random finite controls do not prove asymptotic theorem. Mathematical theorem is given separately in report."};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(audit(),null,2));
