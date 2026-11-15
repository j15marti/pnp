"use strict";
// TMR-5/041 independent physical delayed EOF write and tariff verifier.
function audit(){
"use strict";
let assertions=0,orderedTraces=0,directTraces=0,physicalTransitions=0,dualChecks=0,lpGridChecks=0;
const check=(ok,msg)=>{assertions++;if(!ok)throw Error(msg)};
const eq=(a,b,msg)=>check(JSON.stringify(a)===JSON.stringify(b),msg+":"+JSON.stringify(a)+" != "+JSON.stringify(b));
const rules={INIT:[0,0,1,0],SEEK:[0,0,1,0],MID:[0,1,1,0],EOF_WRITE:[0,1,1,0],BACK:[0,0,0,1],ACT:[1,0,0,0],HALT:[0,0,0,1]};
function simulate(n,m,ordered){
 const src="1".repeat(n)+"#", W=Array(n+1).fill("_"), O=Array(m).fill("_");
 let ih=0,wh=0,phase=ordered?"INIT":"FIRST",t=0,paid=new Set(),seen=new Set(),everEOF=false,activatedAfterLast=false;
 const initial7=[0,0,0,1,n-1,n+1,n-1];
 function p(){
  const a=Number(W[0]!=="1"),q=W.slice(1,n).filter(z=>z!=="g").length,u=n+1-seen.size;
  const d=["INIT","SEEK","STREAM"].includes(phase)?n-2:(phase==="BACK"?wh:0);
  return [0,0,0,a,q,u,d+Number(phase!=="HALT")];
 }
 if(ordered)eq(p(),initial7,"ordered initial");
 const actualRows={};
 while(phase!=="HALT"){
  check(t<=3*n+3,"loop bound");
  const prevP=ordered?p():null,oldW=W.slice(),oldO=O.slice(),oldIH=ih,oldWH=wh,oldPaid=paid.size;
  let rule;
  if(ordered){
   if(phase==="INIT"){
    check(ih===0&&wh===0&&src[ih]==="1","init");seen.add(ih);W[0]="0";ih++;phase="SEEK";rule="INIT";
   }else if(phase==="SEEK"){
    check(ih===1&&wh===0&&src[ih]==="1","second 1");seen.add(ih);ih++;wh++;phase="STREAM";rule="SEEK";
   }else if(phase==="STREAM"&&src[ih]==="1"){
    check(wh===ih-1&&wh>=1&&W[wh]==="_","mid write place");
    seen.add(ih);W[wh]="g";check(!paid.has(wh),"paid once");paid.add(wh);ih++;wh++;rule="MID";
   }else if(phase==="STREAM"&&src[ih]==="#"){
    check(ih===n&&wh===n-1&&W[wh]==="_","EOF final write");
    seen.add(ih);everEOF=true;W[wh]="g";check(!paid.has(wh),"EOF paid once");paid.add(wh);
    wh--;phase="BACK";rule="EOF_WRITE";
   }else if(phase==="BACK"&&wh>0){
    check(W[wh]==="g","back across paid g");wh--;rule="BACK";
   }else if(phase==="BACK"&&wh===0){
    check(W[0]==="0"&&everEOF&&paid.size===n-1,"legitimate after-last activation");
    W[0]="1";for(let j=0;j<m;j++)O[j]="@";activatedAfterLast=true;phase="READY";rule="ACT";
   }else if(phase==="READY"){
    check(activatedAfterLast&&O.every(x=>x==="@"),"distinct later HALT");
    phase="HALT";rule="HALT";
   }else throw Error("no ordered rule:"+phase);
  }else{
   if(phase==="FIRST"){
    check(ih===0&&wh===0&&src[ih]==="1","direct first");
    seen.add(ih);W[0]="1";for(let j=0;j<m;j++)O[j]="@";ih++;wh++;phase="GATE";rule="D_FIRST";
   }else if(phase==="GATE"&&src[ih]==="1"){
    check(wh===ih&&W[wh]==="_","direct gate");
    seen.add(ih);W[wh]="g";check(!paid.has(wh),"direct paid once");paid.add(wh);ih++;wh++;rule="D_GATE";
   }else if(phase==="GATE"&&src[ih]==="#"){
    check(ih===n,"direct EOF source");seen.add(ih);everEOF=true;phase="HALT";rule="D_EOF_HALT";
   }else throw Error("no direct rule:"+phase);
  }
  t++;physicalTransitions++;
  check(Math.abs(wh-oldWH)<=1&&Math.abs(ih-oldIH)<=1,"head locality");
  check(W.reduce((v,x,j)=>v+Number(x!==oldW[j]),0)<=1,"one W write");
  check(O.every((x,j)=>oldO[j]===x||(oldO[j]==="_"&&x==="@")),"one cell per output tape");
  check(paid.size-oldPaid>=0&&paid.size-oldPaid<=1,"one new gate id");
  check(seen.size<=t,"original read accesses paid");
  actualRows[rule]=(actualRows[rule]||0)+1;
  if(ordered){
   const next=p(),delta=prevP.map((v,j)=>v-next[j]);
   eq(delta,[0,0,0,...rules[rule]],"full signed tariff "+rule);
   check(delta[3]+delta[5]+delta[6]<=1,"selected lambda physical tariff");
   check(next.every(v=>v>=0),"nonnegative components");
  }
 }
 check(everEOF&&seen.size===n+1,"authentic EOF and every source symbol");
 check(paid.size===n-1&&[...paid].every(j=>j>=1&&j<n),"distinct paid gates");
 check(W[0]==="1"&&W.slice(1,n).every(x=>x==="g")&&O.every(x=>x==="@"),"full AND obligations");
 check(t===(ordered?2*n+1:n+1),"exact length");
 if(ordered){
  eq(p(),[0,0,0,0,0,0,0],"zero completion");
  eq(actualRows,{INIT:1,SEEK:1,...(n>2?{MID:n-2}:{}),EOF_WRITE:1,...(n>2?{BACK:n-2}:{}),ACT:1,HALT:1},"row multiplicities");
  orderedTraces++;
 }else directTraces++;
 return {n,m,steps:t,rows:actualRows,output:W.slice(0,n).join("")+"/"+O.join("")};
}
const examples=[];
for(let n=2;n<=128;n++)for(let m=1;m<=5;m++){
 const o=simulate(n,m,true),d=simulate(n,m,false);
 eq(o.output,d.output,"literal physical outputs agree");
 if([2,3,8,32,128].includes(n)&&[1,5].includes(m))examples.push({n,m,ordered_steps:o.steps,direct_steps:d.steps,ordered_rows:o.rows});
 const cover=[1,n-1,n+1,n-1],y={INIT:1,SEEK:1,MID:n-2,EOF_WRITE:1,BACK:n-2,ACT:1,HALT:1};
 const total=Object.entries(y).reduce((s,[key,mul])=>s+mul,0);
 const discharge=[0,0,0,0];
 for(const [rule,mul] of Object.entries(y))for(let j=0;j<4;j++)discharge[j]+=rules[rule][j]*mul;
 eq(discharge,cover,"dual covers exact initial obstruction");
 check(total===2*n+1,"dual cost");
 dualChecks++;
}
for(let f=0;f<=6;f++)for(let g=0;g<=6;g++)for(let i=0;i<=6;i++)for(let t=0;t<=6;t++){
 const feasible=f<=6&&g+i<=6&&t<=6;
 if(feasible)for(const n of [2,3,4,8,16,64,128]){
  check(f+(n-1)*g+(n+1)*i+(n-1)*t<=6*(2*n+1),"exact scaled LP upper");
  lpGridChecks++;
 }
}
return {role:"TMR-5",run:"041",method:"independent V8 emulation; exhaustive parameter range and integer-scaled tariff grid",scope:"ordered unary record service, not SAT",n_min:2,n_max:128,m_min:1,m_max:5,ordered_traces:orderedTraces,direct_traces:directTraces,physical_transitions:physicalTransitions,dual_checks:dualChecks,lp_grid_checks:lpGridChecks,assertions,failures:0,examples,exact_statement:"ordered upper 2n+1, peer prior lower 2n, extensional direct n+1",zero_cost_SCC:"singleton"};
}
if (typeof require !== "undefined" && require.main === module) console.log(JSON.stringify(audit(),null,2));
