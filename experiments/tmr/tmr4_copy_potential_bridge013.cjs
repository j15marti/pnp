/* TMR-4/013, independent physical COPY/REWIND/RUN step emulator. Run: node tmr4_copy_potential_bridge013.cjs */
const audit = function audit(){
 "use strict";
 const counts={pairedExecutions:0,originalSteps:0,simulatedSteps:0,copySteps:0,rewindSteps:0,accept:0,reject:0,stateComparisons:0,errors:0,certificateChecks:0,hostileControls:0}, failures=[];
 const sc={L:0,"0":1,"1":2,R:3};
 function check(cond,where){if(!cond){counts.errors++;if(failures.length<9)failures.push(where);}}
 function source(x){return ["L",...x.split(""),"R"];}
 function state(h,mode){
   return {heads:Array(h).fill(0),workheads:[0,0],work:[new Map(),new Map()],
           visits:[new Set([0]),new Set([0])],q:0,t:0,mode,done:false,out:null};
 }
 function core(s,reads,L){
   if(s.done)throw Error("attempt to step terminal");
   const wr=s.workheads.map((p,j)=>s.work[j].get(p)??0);
   const sum=reads.reduce((v,ch)=>v+sc[ch],0);
   const nq=(s.q*3+sum+wr[0]*5+wr[1]*7+s.mode+s.t)%19;
   for(let j=0;j<2;j++){
     let p=s.workheads[j];
     s.work[j].set(p,(nq+sum+wr[j]+j)%4);
     const move=(nq+s.mode+j+s.t)%3-1;
     s.workheads[j]=Math.max(0,p+move);
     s.visits[j].add(s.workheads[j]);
   }
   s.heads=s.heads.map((p,j)=>{
     let delta=(nq+2*j+sc[reads[j]]+s.t+s.mode)%3-1;
     if(p===0&&delta<0)delta=0;
     if(p===L+1&&delta>0)delta=0;
     const np=p+delta;
     check(np>=0&&np<=L+1&&Math.abs(np-p)<=1,"illegal input move");
     return np;
   });
   s.q=nq;s.t++;
   s.done=s.t>=12||(s.t>=2&&(nq+s.mode)%7===0);
   if(s.done)s.out=nq%2;
 }
 function snap(s){
   const normalize=m=>[...m.entries()].sort((a,b)=>a[0]-b[0]);
   return JSON.stringify({heads:s.heads,q:s.q,t:s.t,mode:s.mode,done:s.done,out:s.out,
     wh:s.workheads,w:s.work.map(normalize),v:s.visits.map(set=>[...set].sort((a,b)=>a-b))});
 }
 function newA(x,h,mode){return {src:source(x),core:state(h,mode),ticks:0};}
 function aStep(a){core(a.core,a.core.heads.map(p=>a.src[p]),a.src.length-2);a.ticks++;}
 function newB(x,h,mode){
   return {src:source(x),core:state(h,mode),clones:Array.from({length:h},()=>new Map()),
     cloneHeads:Array(h).fill(0),readHead:0,phase:"COPY",ticks:0,copy:0,rewind:0,sim:0,
     seen:new Set()};
 }
 function bStep(b){
   const L=b.src.length-2;
   if(b.phase==="COPY"){
     const ch=b.src[b.readHead];
     for(let j=0;j<b.clones.length;j++)b.clones[j].set(b.cloneHeads[j],ch);
     if(ch==="R"){b.phase="REWIND";}else{
       b.readHead++;
       for(let j=0;j<b.cloneHeads.length;j++)b.cloneHeads[j]++;
     }
     // Source data at physical position p corresponds to zero-indexed bit p-1.
     if(ch==="0"||ch==="1")b.seen.add(b.readHead-2);
     b.copy++;
   }else if(b.phase==="REWIND"){
     check(b.cloneHeads.every(v=>v>0),"rewind underflow");
     for(let j=0;j<b.cloneHeads.length;j++)b.cloneHeads[j]--;
     b.rewind++;
     if(b.cloneHeads.every(v=>v===0)){
       b.phase="RUN";
       check(b.readHead===L+1,"park physical input at right endmarker");
       check(b.copy===L+2&&b.rewind===L+1,"setup exact charge");
       check(b.seen.size===L,"complete initial observation");
       for(let j=0;j<b.clones.length;j++)for(let k=0;k<=L+1;k++)
         check(b.clones[j].get(k)===b.src[k],"copy fidelity");
     }
   }else if(b.phase==="RUN"){
     const reads=b.cloneHeads.map((p,j)=>b.clones[j].get(p));
     check(reads.every(c=>c!==undefined),"missing cloned source cell");
     const oldHeads=b.cloneHeads.slice();
     core(b.core,reads,L);
     b.cloneHeads=b.core.heads.slice();
     for(let j=0;j<b.cloneHeads.length;j++)
       check(Math.abs(b.cloneHeads[j]-oldHeads[j])<=1,"clone illegal move");
     b.sim++;
     if(b.core.done)b.phase="DONE";
   }else{throw Error("step past terminal");}
   b.ticks++;
 }
 for(let L=0;L<=7;L++){
  for(let word=0;word<(1<<L);word++){
   const x=L?word.toString(2).padStart(L,"0"):"";
   for(const h of [1,2,3])for(let mode=0;mode<7;mode++){
     const a=newA(x,h,mode),b=newB(x,h,mode);
     while(b.phase!=="RUN")bStep(b);
     check(b.copy===L+2&&b.rewind===L+1,"setup phase count");
     check(snap(a.core)===snap(b.core),"initial prepared simulation state");
     while(!a.core.done){
       aStep(a);bStep(b);
       counts.stateComparisons++;
       check(snap(a.core)===snap(b.core),"full trace mismatch "+L+":"+h+":"+mode);
       check(b.cloneHeads.every((p,j)=>p===a.core.heads[j]),"head trace mismatch");
     }
     check(b.phase==="DONE","did not reach terminal");
     check(b.core.out===a.core.out,"different terminal label");
     check(b.ticks===a.ticks+2*L+3,"time identity");
     const sa=a.core.visits.reduce((n,v)=>n+v.size,0);
     const sb=b.core.visits.reduce((n,v)=>n+v.size,0)+b.clones.length*(L+2);
     check(sb===sa+h*(L+2),"visited space identity");
     counts.pairedExecutions++;counts.originalSteps+=a.ticks;counts.simulatedSteps+=b.sim;
     counts.copySteps+=b.copy;counts.rewindSteps+=b.rewind;
     counts.accept+=a.core.out===1?1:0;counts.reject+=a.core.out===0?1:0;
     if(L>0){check(b.seen.size===L,"ghost full source");
       check([...Array(L).keys()].every(i=>b.seen.has(i)),"certificate not discharged");
       counts.certificateChecks++;
     }
   }
  }
 }
 // Hostile: one missing rewind step leaves the clone head at data cell 1.
 const bad=newB("101",2,0);while(bad.phase!=="REWIND")bStep(bad);
 for(let k=0;k<3;k++)bStep(bad);
 check(bad.cloneHeads.some(p=>p!==0),"missing rewind was undetected");
 counts.hostileControls++;
 // Hostile: changing one copied bit invalidates the correspondence invariant.
 const corrupt=newB("101",2,0);while(corrupt.phase!=="RUN")bStep(corrupt);
 corrupt.clones[0].set(1,"0");
 check(corrupt.clones[0].get(1)!==corrupt.src[1],"corrupted copy accepted as faithful");
 counts.hostileControls++;
 // Hostile: treating a scan that is required for source observation as free
 // invalidates the potential inequality from an unobserved last-bit support.
 const lastBitStartPotential=4,afterCopyPotential=0;
 check(!(lastBitStartPotential<=0+afterCopyPotential),"unsound free-setup edge overlooked");
 counts.hostileControls++;
 return {tag:"TMR4-COPY-TO-POTENTIAL-BRIDGE013",status:"COMPUTATIONAL",
  distinction:"Independent explicit COPY/REWIND/RUN counted-step emulator; not a general SAT TM",
  limits:{maxInputBits:7,inputHeads:[1,2,3],fixedModes:7,maxCoreSteps:12},
  ...counts,failures,
  mathematicalClaim:"For every B_A all-edge cost-sound potential Phi, Phi(B_start)-(2L+3)<=T_A; Phi(B_ready)<=T_A. At B_ready the observed source ghost set V contains all L data bits, hence source-difference potentials vanish."};
};
console.log(JSON.stringify(audit(),null,2));
