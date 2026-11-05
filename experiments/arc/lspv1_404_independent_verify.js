#!/usr/bin/env node
// LSPV-1/404 independent JS verifier; no dependency on producer.
// node lspv1_404_independent_verify.js raw.json
'use strict';
const fs=require('fs');
const raw=JSON.parse(fs.readFileSync(process.argv[2]||'lspv1_404_raw.json','utf8'));
let assertions=0;
function check(b,m){if(!b)throw Error(m);assertions++;}
function clauses(n){const out=[];for(let i=0;i<n;i++){const a=3*i+1,b=a+1,c=a+2;
for(const sb of [1,-1])for(const sc of [1,-1])out.push([a,sb*b,sc*c]);}return out;}
const end=[-1,-4,-7];
function holds(C,mask){return C.every(d=>d.some(l=>Boolean(mask[Math.abs(l)])===(l>0)));}
function solveTruth(n){const A=clauses(n),B=A.concat([end]);let cntA=0,cntB=0;
for(let mask=0;mask<Math.pow(2,3*n);mask++){
 const bits=[0,...Array.from({length:3*n},(_,j)=>(mask>>j)&1)];
 cntA+=holds(A,bits);cntB+=holds(B,bits);
}return [cntA,cntB];}
function resol(L,R,v){check(L.includes(v)&&R.includes(-v),'bad pivot');
const C=[...new Set([...L.filter(x=>x!==v),...R.filter(x=>x!==-v)])];
check(C.every(x=>!C.includes(-x)),'tautology');return C.sort((x,y)=>Math.abs(x)-Math.abs(y));}
function proof(n){const arr=clauses(n).concat([end]);let q=0;
for(let i=0;i<3;i++){
 const a=3*i+1,b=a+1,c=a+2,j=4*i;
 const bpos=resol(arr[j],arr[j+1],c),bneg=resol(arr[j+2],arr[j+3],c);
 const unit=resol(bpos,bneg,b);check(unit.length===1&&unit[0]===a,'forced literal');
 arr.push(unit);q+=3;
}
let last=end.slice();for(let i=0;i<3;i++){last=resol(last,arr[4*n+1+i],-(3*i+1));q++;}
check(last.length===0&&q===12,'12 paid steps');
}
function deletedWitness(n,d){const A=clauses(n).concat([end]),x=Array(3*n+1).fill(0);
for(let i=0;i<n;i++)x[3*i+1]=1;
if(d<12){const C=A[d],i=Math.floor(d/4);
 x[3*i+1]=0;x[3*i+2]=C[1]<0?1:0;x[3*i+3]=C[2]<0?1:0;}
const rem=A.filter((_,j)=>j!==(d===12?4*n:d));
check(!holds(A,x)&&holds(rem,x),'source deletion n'+n+' d'+d);
}
function validateRow(row){check(row.n>=3&&row.n<=9,'n');
if(row.kind==='core'){
 const n=row.n;check(row.certified_mixed_paid_nodes===12&&row.indispensable_source_clauses===13,'core');
 check(row.source_clauses===4*n,'source count');
 const [a,b]=n<=5?solveTruth(n):[4**n,0];
 check(row.original_satisfying_assignments===a&&row.triggered_satisfying_assignments===b,'models');
 for(let d=0;d<13;d++)deletedWitness(n,d);proof(n);
}else{
 const n=row.n,trigger=row.halt_threshold!==null&&row.halt_threshold<=row.test_steps;
 check(row.changed===trigger&&row.output_sat===!trigger,'threshold');
 check(row.num_source_clauses===4*n&&row.num_output_clauses===4*n+(trigger?1:0),'count');
 check(row.source_sat===true,'source label');
}}
function malformedFixture(){for(const s of ['', 'p cnf 3 1\n1 2 3','p cnf nope','p cnf 3 2\n1 2 3 0\n','p cnf 3 1\n1 2 0\n']){
 const lines=s.trim().split('\n'),p=lines[0].split(' ');
 const ok=p.length===4&&p[0]==='p'&&p[1]==='cnf'&&+p[3]===lines.length-1&&
 lines.slice(1).every(t=>{const a=t.trim().split(' ');return a.length===4&&a[3]==='0'&&new Set(a.slice(0,3).map(x=>Math.abs(+x))).size===3;});
 check(!ok,'malformed accepted');
}}
function main(){check(raw.theorem==='LSPV1 SINGLE3 SOURCE PRESERVATION404','label');
check(raw.runs.length===77,'row count');
for(const row of raw.runs)validateRow(row);
malformedFixture();
let rejected=false;try{resol([1,2],[-1,-2],3)}catch(_){rejected=true}check(rejected,'bad pivot');
const corrupted={...raw.runs[0],output_sat:!raw.runs[0].output_sat};
rejected=false;try{validateRow(corrupted)}catch(_){rejected=true}check(rejected,'corrupted raw');
console.log(JSON.stringify({status:'PASS',assertions,records:raw.runs.length,independent:'JS recomputation; enumeration n<=5; strict RES; deletion witnesses'}));
}main();
