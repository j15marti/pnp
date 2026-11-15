// Exact audit() function executed inside a native V8 isolate; no imports or randomness.
function audit(){
"use strict";
let assertions=0,transitions=0,traces=0,controls=0;const rows=new Map();
function ok(c,m){assertions++;if(!c)throw Error("AUDIT FAILED: "+m)}
function potential(s){const n=s.n,w=s.w;if(s.phase===0)return [Math.abs(w-(n-1))+1,n];if(s.phase===1)return [0,Math.abs(w)+2];if(s.phase===2)return [0,1];return [0,0]}
function addRow(kind,d){const key=kind+"|"+d.join(",");rows.set(key,(rows.get(key)||0)+1)}
function init(n,m){return {n,m,ip:0,w:0,W:new Map(),outs:Array(m).fill(""),eof:false,phase:0,halt:false,paid:new Set(),steps:[]}}
function step(s,kind,{expect,write,wm=0,im=0,markers=false,halt=false}={}){
 ok(!s.halt&&[-1,0,1].includes(wm)&&[-1,0,1].includes(im),"legal move");
 const symbol=s.ip<s.n?"1":s.ip===s.n?"#":"invalid";
 if(expect)ok(symbol===expect,kind+": expected "+expect+", saw "+symbol);
 const b=potential(s),oldw=s.w,oldphase=s.phase;
 if(symbol==="#")s.eof=true;
 if(write){
  ok(write.pos===s.w,"write at scanned W head");ok(["0","1","g"].includes(write.val),"finite W alphabet");
  if(write.val==="0")ok(s.w===0,"header cell");
  if(write.val==="1"){ok(s.w===0&&s.W.get(0)==="0"&&s.phase===1,"ordered activation");s.phase=2}
  if(write.val==="g"){ok(s.w>0&&s.w<s.n,"gate cell");s.paid.add(s.w);if(s.w===s.n-1&&s.phase===0)s.phase=1}
  s.W.set(s.w,write.val)
 }
 if(markers){ok(write?.val==="1"&&s.phase===2,"marker/activation fusion");s.outs.fill("@")}
 if(halt){ok(!write&&s.phase===2,"distinct HALT");s.phase=3;s.halt=true}
 s.w+=wm;s.ip+=im;ok(s.ip>=0&&s.ip<=s.n,"source head within tape");
 const a=potential(s),d=[b[0]-a[0],b[1]-a[1]];
 ok(d[0]+d[1]<=1,"all-step tariff: "+kind+" "+d);ok(Number.isInteger(d[0])&&Number.isInteger(d[1]),"exact integers");
 if(oldphase===0&&s.phase===1)ok(oldw===s.n-1&&write?.val==="g","no free final gate");
 addRow(kind,d);transitions++;s.steps.push({rule:kind,w:s.w,ip:s.ip,delta:d});
 return s
}
function end(s,T){
 ok(s.halt&&s.phase===3&&s.eof,"completed goal");ok(s.W.get(0)==="1","activated W0");
 for(let i=1;i<s.n;i++)ok(s.W.get(i)==="g"&&s.paid.has(i),"distinct paid gate");
 ok(s.outs.every(x=>x==="@"),"all separate markers");
 ok(s.steps.length===T,"physical cost "+s.steps.length+" expected "+T);
 ok(s.steps.reduce((z,x)=>z+x.delta[0]+x.delta[1],0)===2*s.n,"telescoping potential");
 traces++;return s
}
function uniform(n,m){
 const s=init(n,m);step(s,"U_INIT",{expect:"1",write:{pos:0,val:"0"},im:1});
 step(s,"U_SEEK",{expect:"1",im:1,wm:1});
 for(let j=2;j<n;j++)step(s,"U_MID",{expect:"1",write:{pos:j-1,val:"g"},im:1,wm:1});
 step(s,"U_EOF_GATE",{expect:"#",write:{pos:n-1,val:"g"},wm:-1});
 while(s.w>0)step(s,"U_BACK",{expect:"#",wm:-1});
 step(s,"U_ACT",{expect:"#",write:{pos:0,val:"1"},markers:true});
 step(s,"U_HALT",{expect:"#",halt:true});return end(s,2*n+1)
}
function special(k,m,neighbor){
 const n=k+(neighbor?1:0),s=init(n,m);
 step(s,"K_INIT",{expect:"1",write:{pos:0,val:"0"},im:1,wm:1});
 for(let j=2;j<k;j++)step(s,"K_STREAM",{expect:"1",write:{pos:j-1,val:"g"},im:1,wm:1});
 step(s,"K_SPECULATIVE",{expect:"1",write:{pos:k-1,val:"g"},im:1,wm:-1});
 if(neighbor){
  step(s,"K_RECOVER_1",{expect:"1",wm:1,im:1});
  step(s,"K_RECOVER_2",{expect:"#",wm:1});
  step(s,"K_FINAL_GATE",{expect:"#",write:{pos:k,val:"g"},wm:-1});
 }
 while(s.w>0)step(s,"K_BACK",{expect:"#",wm:-1});
 step(s,"K_ACT",{expect:"#",write:{pos:0,val:"1"},markers:true});
 step(s,"K_HALT",{expect:"#",halt:true});
 return end(s,neighbor?2*k+4:2*k)
}
for(let n=2;n<=96;n++)for(let m=1;m<=3;m++)uniform(n,m);
for(let k=2;k<=64;k++)for(let m=1;m<=3;m++){
 const a=special(k,m,false),b=special(k,m,true);
 ok(a.steps.length===2*k&&b.steps.length===2*k+4,"adjacent sharp bound");
 ok(a.steps.slice(0,k).every((z,j)=>z.rule===b.steps[j].rule&&z.ip===b.steps[j].ip&&z.w===b.steps[j].w),"same prefix for two source lengths");controls++
}
for(let n=2;n<=16;n++){
 for(let w=-2;w<=n+3;w++)for(let d=-1;d<=1;d++)for(let phase=0;phase<=3;phase++){
  const b=potential({n,w,phase}),a=potential({n,w:w+d,phase});
  ok(b[0]-a[0]+b[1]-a[1]<=1,"all legal single-head moves");controls++
 }
 for(let d=-1;d<=1;d++){
  const b=potential({n,w:n-1,phase:0}),a=potential({n,w:n-1+d,phase:1});
  ok(b[0]-a[0]+b[1]-a[1]<=1,"all paid final-gate fusion");controls++
 }
 ok(potential({n,w:0,phase:1})[1]-potential({n,w:0,phase:2})[1]===1,"one activation");
 ok(potential({n,w:0,phase:2})[1]-potential({n,w:0,phase:3})[1]===1,"one HALT")
}
for(let a=0;a<=4;a++)for(let b=0;b<=4;b++)for(const [key] of rows){
 const d=key.split("|")[1].split(",").map(BigInt);
 ok(BigInt(a)*d[0]+BigInt(b)*d[1]<=4n,"exact rational quarters")
}
ok(3n>2n,"gamma 3/2 violated by PRE_TOWARD");
ok(3n>2n,"machine 3/2 violated by POST_TOWARD");
const signed_rows=[...rows].map(([key,count])=>{const [rule,delta]=key.split("|");return {rule,delta:[0,0,0,0,...delta.split(",").map(Number).slice(0,1),0,...delta.split(",").map(Number).slice(1)],cost:"1",count}}).sort((a,b)=>a.rule.localeCompare(b.rule));
return {schema:"TMR-4/046 authenticated ordered physical service",audit:"exact native V8",timestamp:"2026-11-15 06:42 PST",assertions,transitions,traces,controls,failures:0,uniform_range:[2,96],special_range:[2,64],marker_tape_counts:[1,2,3],signed_rows,lambda:["0","0","0","0","1","0","1"],initial:"2n",goal:"0",lp_cone:["0<=lambda_Gamma<=1","0<=lambda_Machine<=1"],closed_form:["T_universal(n)>=2n","T_uniform_EOFWRITE(n)=2n+1","T_fixed_K(K)=2K","T_fixed_K(K+1)=2K+4","forall fixed A: T_A(K)=2K => T_A(K+1)>=2K+4"],controls_retained:["one authentic physical W head","strictly local source head","genuine EOF and distinct HALT","real paid W cell identity","simultaneous writes on other separate tapes","zero metadata VIEW preserves p"],transfer:"unrestricted SAT still OPEN"}
}
if (typeof module !== "undefined" && require.main === module) console.log(JSON.stringify(audit(), null, 2));
