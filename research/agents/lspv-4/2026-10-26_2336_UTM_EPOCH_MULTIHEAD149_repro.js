"use strict";
// LSPV-4 UTM-EPOCH-MULTIHEAD-FIREWALL149
// node 2026-10-26_2336_UTM_EPOCH_MULTIHEAD149_repro.js
// Exact finite controls only. The report separately proves the scoped lemmas.
function run(){
 let checks=0;const ok=(v,s)=>{checks++;if(!v)throw Error("FAIL "+checks+" "+s)};
 const C=(n,r)=>{r=Math.min(r,n-r);let x=1;for(let j=1;j<=r;j++)x=x*(n-j+1)/j;return Math.round(x)};
 let sparse=0,maxratio=0;
 for(let k=1;k<=2;k++)for(let S=0;S<=12;S++)for(let D=0;D<=10;D++){
   const h=2*S+3;let count=0;
   for(let j=0;j<=Math.min(D,k*h);j++)count+=C(k*h,j);
   const A=6*Math.pow(h,k)*count;
   ok(count>=1&&count<=Math.pow(2,k*h),"sparse count");
   if(D===0)ok(count===1,"zero changes allow position labels");
   ok(A>=6*Math.pow(h,k),"label floor");
   maxratio=Math.max(maxratio,Math.log2(A)/Math.min(S+1,(D+1)*Math.log2(S+2)));
   sparse++;
 }
 // Two read-only heads, initially at the left; second advances to Bob,
 // first stays at Alice; both then advance synchronously. D=S=R=0.
 let two=0,diag=0,maxTperN=0;
 for(let m=1;m<=7;m++)for(let a=0;a<(1<<m);a++)for(let b=0;b<(1<<m);b++){
   const aa=Array.from({length:m},(_,i)=>(a>>>i)&1);
   const bb=Array.from({length:m},(_,i)=>(b>>>i)&1);
   const x=aa.join("")+"#"+"X".repeat(4*m)+"#"+bb.join("");
   let p=0,q=0,seps=0,T=0,accept=true;
   while(q<x.length&&seps<2){if(x[q]==="#")seps++;q++;T++}
   for(let i=0;i<m;i++){if(x[p]==="1"&&x[q]==="1")accept=false;p++;q++;T++}
   const intended=!aa.some((v,i)=>v&&bb[i]);
   ok(seps===2&&p===m&&q===x.length,"synchronized heads");
   ok(accept===intended,"two-head DISJ correctness");
   ok(T===x.length,"native input-head transition cost");
   if(b===(((1<<m)-1)^a)){ok(accept,"all diagonal fooling inputs");diag++}
   maxTperN=Math.max(maxTperN,T/x.length);two++;
 }
 // Zero changes still allow an initially blank work-head to act as
 // a zero-tested unary counter; all visited cells count as S.
 let unary=0;
 for(let a=0;a<=40;a++)for(let b=0;b<=40;b++){
   let counter=0,S=1,bad=false;
   for(let t=0;t<a;t++){counter++;S=Math.max(S,counter+1)}
   for(let t=0;t<b;t++){if(counter===0)bad=true;else counter--}
   ok((!bad&&counter===0)===(a===b),"unary counter semantics");
   ok(S===a+1,"count blank visited work cells");
   unary++;
 }
 // Deterministic seeded, finite-config read-only-head/work-head control.
 // Halt/loop outcomes detected; epoch bounds checked for every halted run.
 const nStates=3,workLen=5,stepLimit=600;
 const hsh=(seed,state,cs,w,wp)=>{
   let z=(seed^Math.imul(state+1,0x9e3779b1)^Math.imul(cs+7,0x85ebca6b)^Math.imul(w+1,0xc2b2ae35)^Math.imul(wp+3,0x27d4eb2f))>>>0;
   z^=z>>>16;z=Math.imul(z,0x7feb352d);z^=z>>>15;
   z=Math.imul(z,0x846ca68b);z^=z>>>16;return z>>>0
 };
 let halting=0,looping=0,timedOut=0,events=0,maxEpochs=0;
 function simulate(seed){
   const inp="^"+((seed&1)?"010101":"111000")+"$",I=inp.length;
   let state=0,i=0,wpos=0,w=Array(workLen).fill(0),D=0,R=0,T=0,prevMove=0,epoch=0;
   const visited=new Set([0]),configs=new Set(),byCut={},epochCut={};
   while(T<stepLimit){
     const current=[state,i,wpos,w.join("")].join(":");
     if(configs.has(current))return "loop";
     configs.add(current);
     const cs=inp[i]==="^"?0:inp[i]==="$"?3:inp[i]==="1"?2:1;
     const h=hsh(seed,state,cs,w[wpos],wpos),next=(h%11===0)?nStates:h%nStates;
     const newW=((h>>>8)%7===0)?1-w[wpos]:w[wpos];
     const moveInput=((h>>>12)%3)-1,moveWork=((h>>>17)%3)-1;
     if(newW!==w[wpos]){w[wpos]=newW;D++;epoch++}
     const old=i;
     i=Math.max(0,Math.min(I-1,i+moveInput));
     wpos=Math.max(0,Math.min(workLen-1,wpos+moveWork));
     visited.add(wpos);T++;
     const dir=Math.sign(i-old);
     if(dir){if(prevMove&&prevMove!==dir)R++;prevMove=dir;
       const cut=Math.min(old,i),ek=epoch+":"+cut;
       const label=next+":"+wpos+":"+dir;
       if(!epochCut[ek])epochCut[ek]=new Set();
       if(epochCut[ek].has(label))return "loop";
       epochCut[ek].add(label);byCut[cut]=(byCut[cut]||0)+1;
     }
     state=next;
     if(state===nStates){
       const S=visited.size,V=2*nStates*(2*S+3);
       ok(T<=(D+1)*nStates*I*(2*S+3)+D,"halting epoch time bound");
       for(const key of Object.keys(epochCut))ok(epochCut[key].size<=V,"fixed-cut epoch cap");
       for(const key of Object.keys(byCut)){
         ok(byCut[key]<=R+1,"same-cut reversal cap");
         ok(byCut[key]<=(D+1)*V,"same-cut no-change epoch cap");
         events+=byCut[key];
       }
       maxEpochs=Math.max(maxEpochs,D+1);return "halt";
     }
   }
   return "timeout";
 }
 for(let seed=1;seed<=3600;seed++){
   const tag=simulate(seed);
   if(tag==="halt")halting++;else if(tag==="loop")looping++;else timedOut++;
 }
 const regions={};
 for(let k=1;k<=2;k++){
   let excluded=0,equality=0,allowed=0;
   for(let si=0;si<=20;si++)for(let di=0;di<=20;di++){
     const numer=di+k*si+Math.min(si,di);
     if(numer<20)excluded++;else if(numer===20)equality++;else allowed++;
     ok(numer>=0&&numer<=80,"integer exponent geometry");
   }
   regions["k"+k]={strictly_excluded:excluded,equality_not_excluded:equality,above_boundary:allowed};
 }
 ok(1/5+1/2+1/5<1,"strict counterexample (s=1/2,d=1/5)");
 ok(1/4+1/2+1/4===1,"equality not a contradiction");
 ok(1/6+2*(1/4)+1/6<1,"k=2 strict control");
 return {id:"UTM-EPOCH-MULTIHEAD-FIREWALL149",date:"2026-10-26 23:36 America/Los_Angeles",
  method:"exhaustive combinatorics; exhaustive two-head promise; fixed-seed TM samples",
  parameters:{k:[1,2],sparse_S:"0..12",sparse_D:"0..10",work_alphabet:2,
    two_head_m:"1..7",unary_lengths:"0..40",tm_seed:"1..3600",tm_states:nStates,
    tm_work_cells:workLen,tm_step_limit:stepLimit},
  assertions:checks,sparse_cases:sparse,max_sparse_log2A_over_M:maxratio,
  two_head_input_pairs:two,accepted_diagonal:diag,max_two_head_T_over_N:maxTperN,
  unary_cases:unary,tm_halted:halting,tm_looped:looping,tm_timed_out:timedOut,
  counted_boundary_crossings:events,max_epochs:maxEpochs,
  exponent_grid:regions,
  limitations:["Finite tests do not prove an asymptotic lower bound.",
    "Two-head control is a separated DISJ promise, not all-input SAT.",
    "One-input-head theorem needs initially blank work, bounded input endmarkers, fixed interpreter, global soundness."]};
}
const result=run();
if(typeof process!=="undefined")process.stdout.write(JSON.stringify(result,null,2)+"\n");
result;
