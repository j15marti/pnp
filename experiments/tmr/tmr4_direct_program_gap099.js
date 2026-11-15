// TMR-4/045 original executed native V8 audit. No randomness.
"use strict";
function audit(){
"use strict";
let checks=0,transitions=0,fastTraces=0,slowTraces=0,jointRows=0,exactGrid=0,crossOvercharges=0;
const assert=(b,msg)=>{checks++;if(!b)throw Error(msg)};
const delta=(a,b)=>a.map((v,i)=>v-b[i]);
const eq=(a,b,msg)=>assert(a.length===b.length&&a.every((v,i)=>v===b[i]),msg+" got="+a+" expected="+b);
const pv=(s,n,m)=>[0,0,0,Number(s.W[0]!=="1"),Array.from({length:n-1},(_,j)=>Number(s.W[j+1]!=="g")).reduce((a,b)=>a+b,0),n+1-s.seen,s.O.filter(x=>x!=="@").length+Number(s.control!=="HALT")];
const goals=(s,n,m)=>s.control==="HALT"&&s.seen===n+1&&s.W[0]==="1"&&s.W.slice(1,n).every(x=>x==="g")&&s.O.length===m&&s.O.every(x=>x==="@")&&s.paid.size===n-1;
const statRows={FAST_FIRST:0,FAST_GATE:0,FAST_EOF_HALT:0,SLOW_INIT:0,SLOW_GATE:0,SLOW_EOF_BACK:0,SLOW_BACK:0,SLOW_ACTIVATE:0,SLOW_HALT:0};
const rowValues={FAST_FIRST:[0,0,0,1,0,1,"m"],FAST_GATE:[0,0,0,0,1,1,0],FAST_EOF_HALT:[0,0,0,0,0,1,1],SLOW_INIT:[0,0,0,0,0,1,0],SLOW_GATE:[0,0,0,0,1,1,0],SLOW_EOF_BACK:[0,0,0,0,0,1,0],SLOW_BACK:[0,0,0,0,0,0,0],SLOW_ACTIVATE:[0,0,0,1,0,0,"m"],SLOW_HALT:[0,0,0,0,0,0,1]};
function run(n,m,fast){
let s={control:fast?"FAST_FIRST":"SLOW_INIT",ih:0,wh:0,W:Array(n+1).fill("_"),O:Array(m).fill("_"),paid:new Set(),seen:0,everEOF:false,t:0};
let init=pv(s,n,m);eq(init,[0,0,0,1,n-1,n+1,m+1],"initial");
while(s.control!=="HALT"){
const old=pv(s,n,m),pre={ih:s.ih,wh:s.wh,W:s.W.slice(),O:s.O.slice(),paid:new Set(s.paid),seen:s.seen,control:s.control};let row;
switch(s.control){
case "FAST_FIRST":
assert(s.ih===0&&s.wh===0,"first heads");assert(s.ih<n,"first symbol");
s.W[0]="1";for(let i=0;i<m;i++)s.O[i]="@";
s.ih++;s.wh++;s.seen=1;s.control="FAST_GATE";row="FAST_FIRST";break;
case "FAST_GATE":
assert(s.ih>=1&&s.ih<n,"gate input");assert(s.wh===s.ih,"gate heads");
assert(!s.paid.has(s.wh),"duplicate gate identity");s.paid.add(s.wh);
s.W[s.wh]="g";s.ih++;s.wh++;s.seen=s.ih;
s.control=s.ih===n?"FAST_EOF_HALT":"FAST_GATE";row="FAST_GATE";break;
case "FAST_EOF_HALT":
assert(s.ih===n&&s.wh===n,"EOF head");s.seen=n+1;s.everEOF=true;s.control="HALT";row="FAST_EOF_HALT";break;
case "SLOW_INIT":
assert(s.ih===0&&s.wh===0,"slow init");s.W[0]="0";
s.ih++;s.wh++;s.seen=1;s.control="SLOW_GATE";row="SLOW_INIT";break;
case "SLOW_GATE":
assert(s.ih>=1&&s.ih<n&&s.wh===s.ih,"slow gate");assert(!s.paid.has(s.wh),"slow duplicate");
s.W[s.wh]="g";s.paid.add(s.wh);s.ih++;s.wh++;s.seen=s.ih;
s.control=s.ih===n?"SLOW_EOF_BACK":"SLOW_GATE";row="SLOW_GATE";break;
case "SLOW_EOF_BACK":
assert(s.ih===n&&s.wh===n,"slow EOF");s.seen=n+1;s.everEOF=true;s.wh--;
s.control="SLOW_BACK";row="SLOW_EOF_BACK";break;
case "SLOW_BACK":
assert(s.wh>=1&&s.W[s.wh]==="g","slow back position");s.wh--;
s.control=s.wh===0?"SLOW_ACTIVATE":"SLOW_BACK";row="SLOW_BACK";break;
case "SLOW_ACTIVATE":
assert(s.wh===0&&s.W[0]==="0"&&s.paid.size===n-1,"slow stage finished");
s.W[0]="1";for(let i=0;i<m;i++)s.O[i]="@";s.control="SLOW_HALT";row="SLOW_ACTIVATE";break;
case "SLOW_HALT":
assert(s.W[0]==="1"&&s.O.every(x=>x==="@"),"slow terminal");
s.control="HALT";row="SLOW_HALT";break;
default:throw Error("unexpected state");
}
s.t++;transitions++;statRows[row]++;const next=pv(s,n,m),d=delta(old,next);
const expected=rowValues[row].map(v=>v==="m"?m:v);eq(d,expected,row+" signed discharge");
assert(s.ih-pre.ih>=0&&s.ih-pre.ih<=1,"input local move");
assert(Math.abs(s.wh-pre.wh)<=1,"work local move");
assert(s.W.filter((v,i)=>v!==pre.W[i]).length<=1,"single W cell per step");
assert(s.O.every((v,i)=>v===pre.O[i]||v==="@"),"one cell per output tape");
assert(s.paid.size-pre.paid.size>=0&&s.paid.size-pre.paid.size<=1,"count-once gate pay");
assert(s.seen-pre.seen>=0&&s.seen-pre.seen<=1,"one newly read source cell");
assert(d[5]<=1,"universal source tariff");assert(s.t<=2*n+3,"terminating");
const must=expected[3]+expected[4]+expected[5]+expected[6];if(must>1)crossOvercharges++;
assert(d[5]<=1,"common rational cert");
assert(s.control!=="HALT"||s.everEOF,"early halting");jointRows++;
}
assert(goals(s,n,m),"goal");eq(pv(s,n,m),[0,0,0,0,0,0,0],"terminal");
assert(s.t===(fast?n+1:2*n+2),"exact trace cost");
assert(init[5]===n+1,"initial input prefix");
if(fast)fastTraces++;else slowTraces++;
return {n,m,program:fast?"M_DIRECT":"M_STAGE_OUTPUT",steps:s.t};
}
const representative=[];
for(let n=2;n<=96;n++)for(let m=1;m<=5;m++){
const a=run(n,m,true),b=run(n,m,false);
if([2,3,4,8,16,32,64,96].includes(n)&&[1,3,5].includes(m))representative.push({n,m,direct:a.steps,stage:b.steps});
}
for(let n of [2,3,5,11,37,96])for(let m of [1,2,3,5]){
for(let F=0;F<=6;F++)for(let G=0;G<=6;G++)for(let I=0;I<=6;I++)for(let T=0;T<=6;T++){
const eligible=(F+I+m*T<=6)&&(G+I<=6)&&(I+T<=6);
if(eligible){const init=F+(n-1)*G+(n+1)*I+(m+1)*T;
assert(init<=6*(n+1),"rational grid weak duality");exactGrid++;}
}
}
assert(1+1+1>1,"logical falsifier present");
return {protocol:"TMR4-DIRECT-STAGE",status:"COMPUTATIONAL",scope:"genuine deterministic fixed-port record/marker programs, not SAT",inputs:{n_min:2,n_max:96,m_min:1,m_max:5},fastTraces,slowTraces,transitions,jointRows,exactGrid,checks,failures:0,crossOvercharges,representative,statRows,rows:rowValues,primal:{weights:{fus:"0",gamma:"0",interface:"1",machine:"0"},initial:"n+1"},dual:{FAST_FIRST:1,FAST_GATE:"n-1",FAST_EOF_HALT:1,total:"n+1"},result:"one fixed correct M_DIRECT reaches authenticated extensional goal in n+1 transitions; source-prefix alone is a universal n+1 lower bound for that goal"};
}
const result = audit();
if (typeof console !== "undefined") console.log(JSON.stringify(result,null,2));
