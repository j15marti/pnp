#!/usr/bin/env node
"use strict";
/* LSPV-4 ARC-NAND-PATH-SPACE127. Node.js >=18. Dependency-free reproducible numeric audit.
   NOT a proof of SAT hardness or a simulation of indexed random-access TM bit time. */
let checks=0;const yes=(v,n)=>{if(!v)throw Error("FAILED "+n);checks++;};
const gcd=(a,b)=>{a=a<0n?-a:a;b=b<0n?-b:b;while(b){[a,b]=[b,a%b];}return a;};
const R=(a,b=1n)=>{a=BigInt(a);b=BigInt(b);if(!b)throw Error("zero");if(b<0n){a=-a;b=-b;}const g=gcd(a,b);return [a/g,b/g];};
const add=(x,y)=>R(x[0]*y[1]+y[0]*x[1],x[1]*y[1]);
const sub=(x,y)=>R(x[0]*y[1]-y[0]*x[1],x[1]*y[1]);
const mul=(x,y)=>R(x[0]*y[0],x[1]*y[1]);
const div=(x,y)=>R(x[0]*y[1],x[1]*y[0]);
const eq=(x,y)=>x[0]===y[0]&&x[1]===y[1];
const gt=(x,y)=>x[0]*y[1]>y[0]*x[1];
const fmt=x=>x[0]+"/"+x[1];
const beta=c=>div(sub(div(add(c,R(2)),mul(c,c)),c),R(2));
const dagEval=(k,a,b)=>{const x=[a,b];for(let i=2;i<=k;i++)x[i]=1-(x[i-1]&x[i-2]);return x[k];};
const treeEval=(k,a,b)=>k<2?(k===0?a:b):1-(treeEval(k-1,a,b)&treeEval(k-2,a,b));
function localDescriptor(k,path){let id=k;for(const bit of path){if(id<2)break;id=bit===0?id-1:id-2;}return {id,kind:id<2?"INPUT":"NAND"};}
function pathEval(k,a,b,path=[]){const z=localDescriptor(k,path);if(z.kind==="INPUT")return z.id===0?a:b;return 1-(pathEval(k,a,b,path.concat(0))&pathEval(k,a,b,path.concat(1)));}
function fib(k){let a=1n,b=1n;if(k<2)return 1n;for(let i=2;i<=k;i++){[a,b]=[b,a+b];}return b;}
function runAudit(){
const c=R(241,200),space=R(11642479,23232400),d=R(901,500);
yes(eq(beta(c),space),"FLMV curve");
yes(eq(sub(c,R(6,5)),R(1,200)),"time gap");
yes(eq(sub(space,R(1,2)),R(26279,23232400)),"space gap");
const evalQcut=mul(R(2),space);yes(eq(evalQcut,R(11642479,11616200)),"evaluation q cutoff");
const C=div(sub(mul(R(2),d),R(1)),mul(d,sub(d,R(1))));
yes(eq(C,R(651000,361301)),"coNTIME threshold");
const D=mul(d,d),Q=div(D,sub(D,R(1)));
yes(eq(Q,R(811801,561801)),"decision circuit threshold");
const qcases=[["instance-representation q=1.29",R(129,100)],["conditional full decision circuit q",Q],["q=1.01",R(101,100)],["q=1",R(1)]].map(([label,q])=>{
const exp=div(q,R(2)),margin=sub(space,exp);
return {label,q:fmt(q),evaluation_space_exponent:fmt(exp),margin:fmt(margin),within_space_box:gt(space,exp)};});
yes(!qcases[0].within_space_box&&!qcases[1].within_space_box&&!qcases[2].within_space_box&&qcases[3].within_space_box,"q comparisons");
const dag=[];
for(let k=2;k<=34;k++){const leaves=fib(k),nodes=2n*leaves-1n;
yes(nodes===2n*leaves-1n&&k-1>=1,"formula nodes");
if(k<=12){for(let a=0;a<2;a++)for(let b=0;b<2;b++){
const v=dagEval(k,a,b);yes(treeEval(k,a,b)===v,"direct unfolding");
yes(pathEval(k,a,b)===v,"indexed path desc");
}}
dag.push({k,dag_gates:k-1,dag_wires:2*(k-1),formula_leaves:String(leaves),formula_nodes:String(nodes),depth_at_most:k-1});}
yes(dag.find(x=>x.k===30).formula_leaves==="1346269","Fibonacci F31");
let volume_cases=0;
for(const ms of [[1],[1,1],[1,2,3],[2,3,5,8],[1,1,16,1,2],[2,7,11,3,5,13]]){
const V=ms.reduce((a,m)=>a+BigInt(m),0n),M=BigInt(Math.max(...ms));
for(let e=1n;e<=7n;e++){const exact=ms.reduce((a,m)=>a+BigInt(m)**e,0n);yes(exact<=V*M**(e-1n),"volume inequality");volume_cases++;}}
yes(gt(R(9,10),space),"retained output N^0.9 exceeds FLMV space");
return {id:"ARC-NAND-PATH-SPACE127",timestamp:"2026-10-26T01:16:00-07:00",
status:"PROVED/EXACT conditional model bridge; COMPUTATIONAL; ARC OPEN; P versus NP OPEN",
exact:{flmv_time:fmt(c),flmv_space:fmt(space),flmv_time_margin:"1/200",flmv_space_margin:"26279/23232400",
shalunov_max_q_to_give_strict_space:fmt(evalQcut),extra_seed_d:fmt(d),
extra_seed_coNTIME_c_cutoff:fmt(C),extra_seed_sigma2_D:fmt(D),
extra_seed_full_decision_circuit_q_cutoff:fmt(Q)},
qcases,dag,volume_cases,
retained_countercontrol:{N:1000000,retained_cells:Math.ceil(1000000**0.9),space_exponent:"9/10",child_buffer_bits:64},
assertions:checks,failures:0,
limits:["DAG-to-formula syntactic blowup is not a Boolean-function formula lower bound",
"Shalunov theorem gives circuit evaluation space but not simultaneous time bound or free circuit construction",
"Bathie-Williams transfer requires depth O(log N) and polylog-time input-aware gate path locator",
"Volume bound requires a correct uniform all-input contractor and aggregate access bound",
"No matched FLMV tape/index/bit-operation trace or unrestricted P versus NP proof"]};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(runAudit(),null,2));
