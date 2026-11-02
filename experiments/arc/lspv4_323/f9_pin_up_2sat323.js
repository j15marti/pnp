"use strict";
// Standalone exhaustive F9 original-source 3^9 ternary-pin classifier and 2SAT certificate.
function run(){
const F=[[1,5,6],[2,3,8],[1,3,5],[4,6,9],[2,4,7],[7,8,9],
[-4,-6,-8],[-1,-6,-7],[-2,-3,-4],[-3,-5,-8],[-1,-2,-9],[-5,-7,-9]];
function check(p,msg){if(!p)throw Error(msg)}
function sat(a){return F.every(c=>c.some(z=>a[Math.abs(z)]===+(z>0)))}
const witnesses=[];
for(let z=0;z<512;z++){const a=Array(10).fill(0);for(let i=1;i<=9;i++)a[i]=(z>>(i-1))&1;if(sat(a))witnesses.push(a)}
check(witnesses.length===70,"models !=70");
function up(p){
const a=p.slice(),trail=[];
while(true){let change=false;
for(let j=0;j<F.length;j++){
const C=F[j];if(C.some(z=>a[Math.abs(z)]===+(z>0)))continue;
const U=C.filter(z=>a[Math.abs(z)]===-1);
if(!U.length)return {conflict:j+1,trail};
if(U.length===1){const z=U[0];a[Math.abs(z)]=+(z>0);trail.push([j+1,Math.abs(z),+(z>0)]);change=true;break;}
}
if(!change)break;
}
return {conflict:null,trail,residual:F.map((C,j)=>{
if(C.some(z=>a[Math.abs(z)]===+(z>0)))return null;
return [j+1,C.filter(z=>a[Math.abs(z)]===-1)]}).filter(Boolean)};
}
const out={all_cubes:0,sat_cubes:0,unsat_cubes:0,direct_empty:0,no_initial_empty:0,
up_refuted_no_initial_empty:0,not_UP:0,not_UP_is_2SAT:0,min_no_empty_pins:10},exc=[];
for(let code=0;code<19683;code++){let tmp=code,p=Array(10).fill(-1),fixed=0;
for(let i=1;i<=9;i++){const d=tmp%3;tmp=(tmp-d)/3;if(d){p[i]=d-1;fixed++;}}
out.all_cubes++;
const yes=witnesses.some(a=>p.every((v,i)=>i===0||v<0||v===a[i]));
if(yes){out.sat_cubes++;continue;}
out.unsat_cubes++;
const direct=F.some(c=>c.every(z=>p[Math.abs(z)]!==-1&&p[Math.abs(z)]!==+(z>0)));
if(direct){out.direct_empty++;continue;}
out.no_initial_empty++;out.min_no_empty_pins=Math.min(out.min_no_empty_pins,fixed);
const r=up(p);
if(r.conflict){out.up_refuted_no_initial_empty++;continue;}
out.not_UP++;check(r.residual.every(e=>e[1].length===2),"nonbinary UP stall");
out.not_UP_is_2SAT++;
exc.push({pins:p.flatMap((v,i)=>i&&v>=0?["x"+i+"="+v]:[]),trace:r.trail,residual:r.residual});
}
check(out.no_initial_empty===2175,"no-empty mismatch");
check(out.not_UP===3,"UP exception mismatch");
check(out.min_no_empty_pins===4,"pin minimum mismatch");
const pin=Array(10).fill(-1);pin[1]=1;pin[4]=0;pin[5]=1;pin[8]=0;
const core=up(pin).residual.filter(c=>[4,5,6,8,11,12].includes(c[0]));
check(core.length===6&&core.every(x=>x[1].length===2),"source core wrong");
const certificate={source_pin_assignments:{"x1":1,"x4":0,"x5":1,"x8":0},
source_clause_ids:[4,5,6,8,11,12],binary_residual:core,
x9_to_notx9:[[11,"x9","not_x2"],[5,"not_x2","x7"],[12,"x7","not_x9"]],
notx9_to_x9:[[4,"not_x9","x6"],[8,"x6","not_x7"],[6,"not_x7","x9"]]};
return{experiment:"LSPV4-F9-PIN-UP-2SAT323",proof_status:"COMPUTATIONAL 3^9, source-indexed explicit 2SAT cycle",f9_models:70,statistics:out,nonUP_cubes:exc,certificate,universal_status:"OPEN"};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
