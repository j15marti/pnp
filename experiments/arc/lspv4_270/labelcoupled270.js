"use strict";
// ARC-LABELCOUPLED-ONEHOT270, Node.js 18+, no dependencies.
function source(m,h){
 const F=[];for(let j=1;j<=m;j++)F.push(j===h?[-1,j%2?2:-2,3]:[1,2,3]);
 for(const [v,a,b] of [[2,4,5],[3,6,7]])for(const s of [-1,1])for(const t of [-1,1])F.push([-v,s*a,t*b]);
 return F;
}
function truth(l,a){return ((a>>(Math.abs(l)-1))&1)===(l>0?1:0)}
function counts(F,a){return F.map(C=>C.reduce((s,l)=>s+Number(truth(l,a)),0))}
function sat(F,a){return counts(F,a).every(t=>t>0)}
function ser(F){
 const n=Math.max(...F.flat().map(Math.abs));
 return "N"+String(n).padStart(2,"0")+"M"+String(F.length).padStart(4,"0")+"|"+
 F.map(C=>C.map(l=>(l>0?"+":"-")+String(Math.abs(l)).padStart(2,"0")).join("")).join("|")+"|";
}
function child(F,m){const i=F.slice(0,m).findIndex(C=>C[0]<0);if(i<0)throw Error("not promise");
 const s=F[i][1];return [[s,3,8],[s,3,-8],...F.slice(m)]}
function dpll(F,n){
 let nodes=0,tests=0,scans=0,branches=0;
 function recur(a){
  nodes++;
  while(true){
   let change=false,allsat=true;
   for(const C of F){
    scans++;let yes=false,u=0,last=0;
    for(const l of C){tests++;const bit=a[Math.abs(l)];
     if(bit===-1){u++;last=l}else if(bit===(l>0?1:0)){yes=true;break}}
    if(yes)continue;allsat=false;if(u===0)return false;
    if(u===1){const k=Math.abs(last),b=last>0?1:0;
     if(a[k]!==-1&&a[k]!==b)return false;
     if(a[k]===-1){a[k]=b;change=true;break}}
   }
   if(change)continue;
   if(allsat)return true;
   let i=0;for(const C of F){for(const l of C)if(a[Math.abs(l)]===-1){i=Math.abs(l);break}if(i)break}
   if(!i)return false;branches++;
   for(const b of [0,1]){const copy=a.slice();copy[i]=b;if(recur(copy))return true}
   return false;
  }
 }
 const answer=recur(Array(n+1).fill(-1));
 return {answer,nodes,tests,scans,branches,selectedEvents:nodes+tests+scans+branches};
}
function details(F){
 const local=F.map((C,j)=>({originalClause:j+1,occurrences:C.map(l=>({
  variable:Math.abs(l),literal:l,S:l>0?1:0,notS:l>0?0:1,U:l>0?0:1,notU:l>0?1:0}))}));
 let pairs=[],checks=0,impossible=0;
 for(let j=0;j<F.length;j++)for(let k=j+1;k<F.length;k++){
  let row={j:j+1,k:k+1};
  for(const A of ["S","U"])for(const B of ["S","U"]){
   const a=new Map();let feasible=true;
   for(const [C,mode] of [[F[j],A],[F[k],B]])for(const l of C){
    const id=Math.abs(l),value=((l>0)===(mode==="S"))?1:0;
    if(a.has(id)&&a.get(id)!==value)feasible=false;
    a.set(id,value);
   }
   let brute=false;
   for(let mask=0;mask<128;mask++){const t=counts([F[j],F[k]],mask);
    if(t[0]===(A==="S"?3:0)&&t[1]===(B==="S"?3:0)){brute=true;break}}
   if(brute!==feasible)throw Error("pair");
   checks++;if(!feasible)impossible++;row[A+B]=feasible;
  }
  pairs.push(row);
 }
 const trail=[];for(const mask of [0,127,1,3,7,126]){
  const t=counts(F,mask),complement=counts(F,mask^127);
  if(t.some((x,j)=>x+complement[j]!==3))throw Error("complement");
  const buckets=[0,1,2,3].map(r=>t.filter(x=>x===r).length);
  trail.push({mask,complementMask:mask^127,assignment:Array.from({length:7},(_,j)=>(mask>>j)&1).join(""),
   buckets,sourceClauseTrueCounts:t,SAT:buckets[0]===0});
 }
 return {local,pairs,trail,checks,impossible};
}
function frac(n,d=1n){n=BigInt(n);d=BigInt(d);let a=n<0n?-n:n,b=d<0n?-d:d;
 while(b){[a,b]=[b,a%b]}if(d<0n){n=-n;d=-d}return [n/a,d/a]}
function add(a,b){return frac(a[0]*b[1]+b[0]*a[1],a[1]*b[1])}
function sub(a,b){return add(a,[-b[0],b[1]])}
function mul(a,b){return frac(a[0]*b[0],a[1]*b[1])}
function div(a,b){return frac(a[0]*b[1],a[1]*b[0])}
function less(a,b){return a[0]*b[1]<b[0]*a[1]}
function fmt(a){return a[0]+"/"+a[1]}
function FLMV(u,v){
 const c=frac(u,v);let f=frac(1),p=frac(1),best=frac(-1),win=0,rows=[];
 for(let k=1;k<40;k++){
  f=div(mul(c,f),add(frac(1),f));p=div(p,c);if(k<2){const a=div(sub(div(frac(1),f),c),frac(k)),d=less(a,p)?a:p;rows.push({k,d:fmt(d)});if(less(best,d)){best=d;win=k}continue;}
  const x=div(sub(div(frac(1),f),c),frac(k)),d=less(x,p)?x:p;
  rows.push({k,d:fmt(d)});if(less(best,d)){best=d;win=k}
  const tail=div(p,c);
  if(k>=3&&less(tail,best))return {c:fmt(c),best:fmt(best),winner:win,rows,tailFrom:k+1,tailCeiling:fmt(tail)};
 }
 throw Error("tail");
}
function run(){
 const rows=[],fullControls=[];let assertions=0;
 for(const m of [8,16,32,64])for(const h of [m-1,m]){
  const F=source(m,h),G=child(F,m),expected=h%2===0;
  const models=Array.from({length:128},(_,i)=>sat(F,i)).filter(Boolean).length;
  const childModels=Array.from({length:256},(_,i)=>sat(G,i)).filter(Boolean).length;
  assertions+=384;if((models>0)!==expected||(childModels>0)!==expected)throw Error("label");
  const direct=dpll(F,7),guest=dpll(G,8);if(direct.answer!==expected||guest.answer!==expected)throw Error("DPLL");
  const D=details(F);assertions+=D.checks+6*F.length;
  let unmarked=h===1?2:1;
  const res=h%2?[2,3]:null;
  const proof={sourceClausePair:[unmarked,h],pivotVariable:1,resolvent:res,
   tautologyDiscarded:!res,forcedBySourceGadgets:[-2,-3],
   forbiddenCube:res?{"2":0,"3":0}:null,
   gadgetOriginalClauseIndices:Array.from({length:8},(_,j)=>m+j+1)};
  const nbits=ser(F).length*8,cbits=ser(G).length*8,q=Math.ceil(Math.pow(nbits,0.6));
  if(nbits!==ser(source(m,h===m?m-1:m)).length*8)throw Error("length channel");
  rows.push({m,h,label:expected?"SAT":"UNSAT",originalPhysicalBits:nbits,childPhysicalBits:cbits,
   models,childModels,baselineDPLL:direct,childDPLL:guest,
   exactMinimaxBitProbes:m/2,naiveSourceProbes:h,
   dummyGuestReads:q,coldStatelessSourceProbes:q*m/2,cachedOnceSourceProbes:m/2,
   recognizableGrammarScanClauses:m+8,materializedChildClauseWrites:G.length,
   retentions:{coldIndexBits:Math.ceil(Math.log2(m+1)),cachedLabelBits:1,physicalChildBits:cbits},
   proof,extremePairAssertions:D.checks});
  if(m<=16)fullControls.push({m,h,originalClauses:F,ordinaryChildClauses:G,
   originalClauseIndexedLocalSandU:D.local,originalClausePairExtremes:D.pairs,
   coherentGlobalEndpointsAndFlips:D.trail,sourceResolutionProof:proof});
 }
 const flmv=[FLMV(6,5),FLMV(241,200)];
 if(flmv[0].best!=="23/45"||flmv[1].best!=="11642479/23232400")throw Error("FLMV exact");
 return {id:"ARC-LABELCOUPLED-ONEHOT270",localTime:"2026-10-31 04:31 PDT",
  proofStatus:"PROVED/EXACT restricted, independent review pending; ARC OPEN",
  encoding:"fixed-width signed literal fields; original proper 3CNF; proper-3CNF child via fresh padding variable",
  rows,fullControls,flmv,finiteAssertions:assertions,
  limitations:["restricted one-hot promise, not arbitrary 3CNF","source bit-probe counts not native FLMV transitions",
   "repeated original clauses and fixed 7 variables, not strict-(2,2)","cached one-bit summary defeats repeated cold query tariff",
   "no universal hereditary arbitrary-A compiler"]};
}
if(typeof module!=="undefined")module.exports={source,child,sat,counts,ser,dpll,run};
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run(),null,2));