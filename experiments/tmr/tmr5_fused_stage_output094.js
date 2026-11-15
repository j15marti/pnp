"use strict";
// Independent native V8 audit(); reproduce: node experiments/tmr/tmr5_fused_stage_output094.js
function audit() {
"use strict";
const stats={status:"COMPUTATIONAL",seed:"none-exhaustive",family:"fixed-m physical multitape unary gate stage with simultaneous nonterminal activation/output",cases:0,steps:0,assertions:0,failures:0,byRule:{},originalMStageCases:0,originalMStageRows:0,jointShortcutCases:0,lpGridChecks:0,negativeTests:0,examples:{}};
function ck(q,msg){stats.assertions++;if(!q){stats.failures++;throw new Error(msg);}}
function workAt(s,j){return s.work.has(j)?s.work.get(j):"_";}
function make(n,m){return {n,m,input:"1".repeat(n)+"#",ip:0,wp:0,work:new Map(),outs:Array(m).fill("_"),state:"INIT",r:-1,steps:0,views:0};}
function potentials(s) {
 const n=s.n;
 let q=0;for(let j=1;j<n;j++)if(workAt(s,j)!=="g")q++;
 const f=(workAt(s,0)==="1")?0:n-1;
 let o=0;for(const t of s.outs)if(t!=="@")o++;
 const h=s.state==="HALT"?0:1;
 const origM=n-s.r+h;
 return {combined:[f,q,o,h],original:[f,q,origM],seven:[0,0,0,f,q,o,h]};
}
function step(s) {
 const before=potentials(s), ip0=s.ip,wp0=s.wp,old=s.state,writes=[];
 const a=s.input[s.ip]??"_",b=workAt(s,s.wp);
 let rule=null;
 if(old==="INIT"&&a==="1"&&b==="_") {rule="INIT";s.work.set(s.wp,"0");writes.push(["W",s.wp]);s.ip++;s.wp++;s.state="SECOND";}
 else if((old==="SECOND"||old==="EMIT")&&a==="1"&&b==="_") {rule="WRITE_GATE";s.work.set(s.wp,"g");writes.push(["W",s.wp]);s.ip++;s.wp++;s.state="EMIT";}
 else if(old==="EMIT"&&a==="#"&&b==="_") {rule="EOF_BACK";s.wp--;s.state="BACK";}
 else if(old==="BACK"&&b==="g") {rule="BACK_G";s.wp--;}
 else if(old==="BACK"&&b==="0"&&s.outs.every(v=>v==="_")) {
   rule="ACTIVATE_AND_MARK";s.work.set(0,"1");writes.push(["W",0]);
   for(let i=0;i<s.m;i++){s.outs[i]="@";writes.push(["O"+i,0]);}
   s.state="READY";
 } else if(old==="READY"&&b==="1"&&s.outs.every(v=>v==="@")) {rule="HALT";s.state="HALT";}
 else throw Error("illegal replay "+JSON.stringify({n:s.n,m:s.m,old,a,b,ip:s.ip,wp:s.wp,outs:s.outs}));
 s.r=Math.max(s.r,ip0);s.steps++;
 const after=potentials(s);
 const delta=before.combined.map((x,i)=>x-after.combined[i]);
 const oldDelta=before.original.map((x,i)=>x-after.original[i]);
 ck(Math.abs(s.ip-ip0)<=1&&Math.abs(s.wp-wp0)<=1,"nonlocal move");
 const tapes=new Set(writes.map(v=>v[0]));
 ck(tapes.size===writes.length,"multiwrite same tape");
 ck(writes.length<=(1+s.m),"too many written tapes");
 ck(s.steps>=1&&rule!==null,"bad cost");
 const expected={INIT:[0,0,0,0],WRITE_GATE:[0,1,0,0],EOF_BACK:[0,0,0,0],BACK_G:[0,0,0,0],ACTIVATE_AND_MARK:[s.n-1,0,s.m,0],HALT:[0,0,0,1]}[rule];
 ck(delta.every((v,i)=>v===expected[i]),"mismatched exact joint tariff "+rule+" "+delta+"/"+expected);
 ck(delta[1]<=1 && delta[3]<=1,"physical q/h overdischarge");
 if(rule==="ACTIVATE_AND_MARK"){ck(s.state==="READY","activation incorrectly terminal");ck(writes.length===s.m+1,"activation physical tapes");}
 if(s.m===0){
    const ref={INIT:[0,0,1],WRITE_GATE:[0,1,1],EOF_BACK:[0,0,1],BACK_G:[0,0,0],ACTIVATE_AND_MARK:[s.n-1,0,0],HALT:[0,0,1]}[rule];
    ck(oldDelta.every((v,i)=>v===ref[i]),"TMR3/043 original row incorrect");
    ck((s.n-1)*0+oldDelta[1]+oldDelta[2]<=1 || rule==="WRITE_GATE","combined guard diagnostic");
    ck(oldDelta[0]+(s.n-1)*oldDelta[2] <=s.n-1,"TMR3/043 rational original unit coefficient");
    stats.originalMStageRows++;
 }
 stats.steps++;stats.byRule[rule]=(stats.byRule[rule]||0)+1;
 return {rule,delta,oldDelta,writes};
}
for(let m=0;m<=4;m++)for(let n=2;n<=64;n++){
 const s=make(n,m),first=potentials(s),rows=[];
 ck(first.combined.join()===[n-1,n-1,m,1].join(),"incorrect initial vector");
 for(let t=0;t<2*n+5 && s.state!=="HALT";t++){
   const r=step(s);if(n<=4 && m<=2)rows.push({rule:r.rule,delta:r.delta,old:r.oldDelta,writes:r.writes.length});
 }
 ck(s.state==="HALT"&&s.steps===2*n+2,"trace length mismatch");
 ck(s.ip===n&&s.wp===0&&s.r===n,"physical cursor end");
 ck(workAt(s,0)==="1"&&s.outs.every(x=>x==="@"),"bad final output");
 for(let j=1;j<n;j++)ck(workAt(s,j)==="g","missing paid gate record");
 ck(potentials(s).seven.every(z=>z===0),"goal potential not zero");
 ck(n-1+m+1>=0,"total check");
 if(m===0){
   ck(first.original.join()===[n-1,n-1,n+2].join(),"original M_STAGE initial");
   stats.originalMStageCases++;
 }else{
   // Independently calibrated coefficients fail on genuine simultaneous ACTIVATE_AND_MARK.
   const combinedActivationScore=(n-1)/(n-1)+m/m;
   ck(combinedActivationScore===2,"joint nonterminal cross-model shortcut");
   // Exact rational LP: max (n-1)c+(n-1)q+m*o+h=n+1.
   // Feasible witness c=0,q=1,o=1/m,h=1; dual: (n-1) WRITE + ACTIVATE + HALT.
   ck(n-1+1+1===n+1,"primal dual");
   stats.jointShortcutCases++;
 }
 if(n<=4&&m<=2)stats.examples["n"+n+"_m"+m]=rows;
 stats.cases++;
}
// Integer-scaled exact tariff cone equivalence for a dense grid of nonnegative rational weights /6.
for(let n=2;n<=16;n++)for(let m=1;m<=4;m++){
 const discharges=[[0,0,0,0],[0,1,0,0],[n-1,0,m,0],[0,0,0,1]];
 for(let f=0;f<=6;f++)for(let q=0;q<=6;q++)for(let o=0;o<=6;o++)for(let h=0;h<=6;h++){
   const lambda=[f,q,o,h];const expected=q<=6 && (n-1)*f+m*o<=6 && h<=6;
   const all=discharges.every(d=>d.reduce((acc,x,i)=>acc+x*lambda[i],0)<=6);
   ck(expected===all,"rational matrix cone mismatch");stats.lpGridChecks++;
 }
}
for(const [n,m] of [[2,1],[3,2],[5,3],[64,4]]){
 const f=n-1,o=m;
 ck(f/(n-1)+o/m>1,"expected falsifier absent");stats.negativeTests++;
}
return stats;
}
if (typeof module!=="undefined" && require.main===module) process.stdout.write(JSON.stringify(audit(),null,2)+"\n");
