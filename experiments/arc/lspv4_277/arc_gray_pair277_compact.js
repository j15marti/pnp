"use strict";
// ARC-GRAY-COMPLEMENT-LEDGER277 compact reproducibility checker.
// Deterministic finite original-source tests. No native FLMV timing.
const W=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],[5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],[-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],[2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]];
const S=[[-1,-3,14],[2,8,-9],[-10,13,14],[3,-7,-13],[-4,9,-11],[-5,-8,-14],[4,-8,11],[1,7,-13],[1,-7,10],[-5,-6,15],[-2,6,-12],[4,9,-10],[-2,5,-12],[3,6,-15],[-6,7,11],[2,-9,-11],[-4,8,10],[-3,12,15],[5,12,-15],[-1,13,-14]];
const H=[];for(const a of [-1,1])for(const b of [-1,1])for(const c of [-1,1])H.push([a,2*b,3*c]);
const X=[[1,2,-3],[1,-2,3],[-1,2,3],[-1,-2,-3]];
const CASES={W1_UNSAT:W,S15_SAT:S,H8_UNSAT:H,H7_SAT:H.filter(c=>c.join(",")!=="-1,2,-3"),
 HORN_SAT:[[-1,-2,3],[-1,2,-3],[-3,-1,-2]],XOR_SAT:X,
 XOR_UNSAT:X.concat([[1,2,3],[1,-2,-3],[-1,2,-3],[-1,-2,3]]),
 W1_RENAMED_UNSAT:W.map(c=>c.map(x=>[1,7,12].includes(Math.abs(x))?-x:x))};
function chk(p,msg){if(!p)throw Error(msg);}
function lit(l,a){return ((a>>(Math.abs(l)-1))&1)===(l>0?1:0);}
function counts(F,a){return F.map(C=>C.reduce((s,l)=>s+(lit(l,a)?1:0),0));}
function verify(F,name){
 const n=Math.max(...F.flat().map(Math.abs)),m=F.length;
 const degree=Array(n).fill(0);for(const C of F)for(const x of C)degree[Math.abs(x)-1]++;
 const order=[...degree.keys()].sort((a,b)=>degree[b]-degree[a]||a-b);
 let models=0,witness=null;
 for(let a=0;a<2**n;a++){const t=counts(F,a);
   if(t.every(x=>x>0)){models++;if(witness===null)witness=a;}
   if(a<((2**n-1)^a))chk(t.every((v,j)=>v+counts(F,(2**n-1)^a)[j]===3),name+" complement");}
 let t=counts(F,0),state=0,updates=0,stopUpdates=null,stopPairs=null;
 for(let k=0;k<2**(n-1);k++){
  if(k){const delta=(k^(k>>1))^((k-1)^((k-1)>>1));const b=31-Math.clz32(delta);const variable=order[n-1-b];state^=1<<variable;
    for(let j=0;j<m;j++)for(const l of F[j])if(Math.abs(l)-1===variable){t[j]+=lit(l,state)?1:-1;updates++;}
    const exact=counts(F,state);chk(t.every((v,j)=>v===exact[j]),name+" flip accounting");}
  if(stopPairs===null&&(t.every(v=>v>0)||t.every(v=>v<3))){stopPairs=k+1;stopUpdates=updates;}
 }
 const optimum=order.slice(1).reduce((sum,v,j)=>sum+degree[v]*2**j,0);
 chk(updates===optimum,name+" optimal update count");
 chk((stopPairs!==null)===(models>0),name+" label");
 let modes=0;
 for(let j=0;j<m;j++)for(let k=j+1;k<m;k++){
   const same=F[j].some(x=>F[k].includes(x)),opp=F[j].some(x=>F[k].includes(-x));
   const expected=[!opp,!same,!same,!opp],seen=[false,false,false,false];
   for(let a=0;a<2**n;a++){const p=counts([F[j],F[k]],a);const x=p[0],y=p[1];
      if(x===3&&y===3)seen[0]=true;if(x===3&&y===0)seen[1]=true;
      if(x===0&&y===3)seen[2]=true;if(x===0&&y===0)seen[3]=true;}
   chk(seen.every((v,i)=>v===expected[i]),name+" four extreme modes");modes+=4;
 }
 return {n,m,models,SAT:models>0,degree,full_pairs:2**(n-1),
    full_updates:updates,early_pairs:stopPairs??2**(n-1),
    early_updates:stopUpdates??updates,first_witness:witness,
    pair_modes_verified:modes,endpoint_N0:[counts(F,0).filter(x=>x===0).length,counts(F,(2**n)-1).filter(x=>x===0).length]};
}
function run(){const cases={};for(const [name,F] of Object.entries(CASES))cases[name]=verify(F,name);
 chk(cases.W1_UNSAT.models===0&&cases.S15_SAT.models===861,"W1/S15");
 chk(cases.W1_UNSAT.full_updates===65532&&cases.H8_UNSAT.full_updates===24,"full updates");
 return {run:"ARC-GRAY-COMPLEMENT-LEDGER277",machine:"abstract host-language events, NOT native FLMV",
  status:"COMPUTATIONAL; exact restricted permutation theorem in formal report; universal ARC OPEN",cases};
}
if(typeof module!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));
