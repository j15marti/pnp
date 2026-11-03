"use strict";
// Independent finite MUS stability controls; source model: proper non-taut clauses.
// This is NOT a general mixed-calculus shortest-proof optimizer.
const clauses=[[],[1],[-1],[2],[-2],[1,2],[1,-2],[-1,2],[-1,-2]];
function sat(F) {
 const vs=[...new Set(F.flat().map(x=>Math.abs(x)))].sort((a,b)=>a-b);
 for(let a=0;a<2**vs.length;a++){
  let ok=F.every(c=>c.some(x=>(((a>>vs.indexOf(Math.abs(x)))&1)===1)===(x>0)));
  if(ok)return true;
 }
 return false;
}
function def(F) { return F.length-new Set(F.flat().map(Math.abs)).size; }
function subsets(F){
 const a=[];for(let mask=0;mask<2**F.length;mask++)a.push(F.filter((_,i)=>mask&(1<<i)));return a;
}
function mus(F) {return !sat(F)&&F.every((_,i)=>sat(F.filter((_,j)=>i!==j)));}
let scanned=0, unsat=0, satn=0, musn=0, stable=0, dHist={}, nonminSame=0;
for(let mask=0;mask<512;mask++){
 const F=clauses.filter((_,j)=>mask&(1<<j));scanned++;
 if(sat(F)){satn++;continue;}
 unsat++;
 const all=subsets(F),mx=Math.max(...all.map(def));
 if(mus(F)){
  musn++;
  const d=def(F);dHist[d]=(dHist[d]||0)+1;
  if(mx!==d||all.slice(0,-1).some(H=>def(H)>=d))throw Error("MUS stability failed");
  stable++;
 }else if(mx===def(F)) nonminSame++;
}
if(scanned!==512||unsat!==417||satn!==95||musn!==12||stable!==12||nonminSame!==401)throw Error('two-var mismatch');
function blockers(n) {
 const F=[];for(let a=0;a<2**n;a++)F.push(Array.from({length:n},(_,i)=>((a>>i)&1)?-(i+1):i+1));return F;
}
const Fblock=blockers(3),peitl=[[1,2],[3,4],[-1,-3],[-2,-4],[1,-2,-3,4],[-1,2,3,-4]];
for(const [name,F,d] of [['blocker3',Fblock,5],['peitl_4_6',peitl,2]]){
 if(!mus(F)||def(F)!==d||subsets(F).some(H=>H.length<F.length&&def(H)>=d))throw Error(name);
}
let horn=0;
for(let n=2;n<=8;n++){
 const F=[[1],...Array.from({length:n-1},(_,j)=>[-(j+1),j+2]),[-n]];
 if(!mus(F)||def(F)!==1||subsets(F).some(H=>H.length<F.length&&def(H)>=1))throw Error('horn');
 horn++;
}
const redundant=[[1],[-1],[2]];
if(mus(redundant)||def(redundant)!==1||Math.max(...subsets(redundant).map(def))!==1)throw Error('redundant control');
const result={status:"COMPUTATIONAL",universe_two_vars:{scanned,sat:satn,unsat,mus:musn,stable,d_by_mus:dHist,nonmus_unsat_max_equal_full:nonminSame},controls:{blocker3:true,peitl_4_6:true,horn_n_2_to_8:horn,unsat_nonminimal_redundant:true},limitations:"Finite checks corroborate known MUS deficiency stability, do not establish a mixed-system proof minimum."};
console.log(JSON.stringify(result,null,2));
