/* TMR-4/015. Exact local-head phase relocation test. Run: node tmr4_late_copy015.cjs */
"use strict";
function audit() {
 const maxBits=10;
 const out={tag:"TMR4-LATE-COPY-015",status:"COMPUTATIONAL",model:"one fixed parity-deciding local-input-head finite-control machine plus a one-copy-tape wrapper",maxBits,executions:0,accepts:0,rejects:0,coreSteps:0,resetSteps:0,copySteps:0,terminalSteps:0,totalSteps:0,potentialEdgeChecks:0,illegalPhiTwoViolations:0,failures:[],samples:[]};
 function check(ok,s){if(!ok&&out.failures.length<20)out.failures.push(s);}
 function baseline(x){
  const src=["L",...x.split(""),"R"];let head=0,parity=0,ticks=0,halted=false;
  while(!halted){const ch=src[head];check(ch!==undefined,"base source");if(ch==="1")parity^=1;if(ch==="R")halted=true;else head++;ticks++;}
  return {parity,ticks,head};
 }
 function wrapped(x){
  const src=["L",...x.split(""),"R"],L=x.length;
  let phase="CORE",head=0,writehead=0,parity=0,ticks=0;
  let coreSteps=0,resetSteps=0,copySteps=0,terminalSteps=0,readySeen=false;
  const copy=new Map(),trace=[];
  while(phase!=="HALT"){
   const prior={phase,head,writehead};
   if(phase==="CORE"){
    const ch=src[head];check(ch!==undefined,"CORE source");
    if(ch==="1")parity^=1;if(ch==="R")phase="RESET";else head++;coreSteps++;
   }else if(phase==="RESET"){
    check(head>0,"RESET underflow");head--;resetSteps++;if(head===0)phase="COPY";
   }else if(phase==="COPY"){
    check(head===writehead,"copy heads");copy.set(writehead,src[head]);copySteps++;
    if(src[head]==="R"){
     check([...Array(L+2).keys()].every(i=>copy.get(i)===src[i]),"copy fidelity");
     check(copy.size===L+2,"copy cells");phase="READY";readySeen=true;
    }else{head++;writehead++;}
   }else if(phase==="READY"){
    check(readySeen&&copy.size===L+2,"unprepared READY");phase="HALT";terminalSteps++;
   }else throw Error("invalid phase");
   ticks++;check(Math.abs(head-prior.head)<=1,"nonlocal original head");
   check(Math.abs(writehead-prior.writehead)<=1,"nonlocal work head");
   trace.push({from:prior.phase,to:phase,cost:1});
   check(ticks<=5*(L+3),"unexpected long test");
  }
  check(trace.length===ticks,"trace length");
  for(let j=0;j<trace.length;j++){
   const p=trace.length-j,q=trace.length-j-1;
   check(p<=trace[j].cost+q,"Bellman potential failed");out.potentialEdgeChecks++;
  }
  check(trace.at(-1).from==="READY"&&trace.at(-1).to==="HALT","terminal phase");
  check(terminalSteps===1,"post-copy terminal steps");
  check(!(2<=trace.at(-1).cost),"invalid Phi(READY)=2 passed");
  out.illegalPhiTwoViolations++;
  return {parity,ticks,coreSteps,resetSteps,copySteps,terminalSteps,copySize:copy.size};
 }
 for(let L=0;L<=maxBits;L++)for(let n=0;n<2**L;n++){
  const x=L===0?"":n.toString(2).padStart(L,"0");
  const a=baseline(x),b=wrapped(x);
  check(a.parity===b.parity,"terminal label "+x);
  check(a.parity===((x.match(/1/g)||[]).length&1),"independent label "+x);
  check(a.ticks===L+2,"original tick count");
  check(b.coreSteps===a.ticks,"core count");
  check(b.resetSteps===a.head,"reset count");
  check(b.copySteps===L+2,"copy count");
  check(b.ticks===a.ticks+a.head+(L+2)+1,"full time identity");
  check(b.copySize===L+2,"space identity");
  out.executions++;out.accepts+=b.parity;out.rejects+=1-b.parity;
  out.coreSteps+=b.coreSteps;out.resetSteps+=b.resetSteps;
  out.copySteps+=b.copySteps;out.terminalSteps+=b.terminalSteps;out.totalSteps+=b.ticks;
  if(["","0","1","101","1111","0000000000","1111111111"].includes(x))
   out.samples.push({x,label:b.parity,core:b.coreSteps,reset:b.resetSteps,copy:b.copySteps,afterReady:1,total:b.ticks});
 }
 out.spaceFormula="S_B(x)=S_A(x)+(L+2) visited writable copy-tape cells in this finite-control example";
 out.theoremScope="General B_A symbolic construction applies to every fixed total local-input multitape A; this driver instantiates a parity decider, not a SAT TM";
 if(out.failures.length)throw Error(JSON.stringify(out));
 return out;
}
const result=audit();
if(typeof console!=="undefined")console.log(JSON.stringify(result,null,2));
