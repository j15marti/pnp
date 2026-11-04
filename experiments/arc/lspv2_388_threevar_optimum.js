/* LSPV-2/388, exact <=3-original-variable R_mix341 proof compiler.
   No dependencies. node: node lspv2_388_threevar_optimum.js > result.json
   The producer computes covers, not general unbounded-SAT hardness. */
"use strict";
function allClauses(n) {
  const clauses=[];
  for(let i=0;i<3**n;i++) {
    let x=i,c=[];
    for(let j=0;j<n;j++){const a=x%3;x=Math.floor(x/3);if(a)c.push((a===1?1:-1)*(j+1));}
    clauses.push(c);
  }
  return clauses;
}
function badMask(n,c) {
  let bits=0;
  for(let a=0;a<(1<<n);a++) {
    let sat=false;
    for(const l of c)if(!!(a&(1<<(Math.abs(l)-1)))===(l>0)){sat=true;break;}
    if(!sat)bits|=1<<a;
  }
  return bits;
}
function solve(n,ids) {
  const cs=allClauses(n), ms=ids.map(i=>badMask(n,cs[i]));
  const full=(1<<(1<<n))-1, cover=ms.reduce((a,b)=>a|b,0);
  if(cover!==full) {
    const witness=Array.from({length:1<<n},(_,i)=>i).find(i=>!(cover&(1<<i)));
    return {label:"SAT",witness};
  }
  const D=Array(full+1).fill(999),prev=Array(full+1);D[0]=0;
  for(let s=0;s<=full;s++) {
    if(D[s]===999)continue;
    ms.forEach((c,j)=>{
      const z=s|c;
      if(D[s]+1<D[z]){D[z]=D[s]+1;prev[z]=[s,j];}
    });
  }
  let s=full,core=[];
  while(s){const [before,j]=prev[s];core.push(j);s=before;}
  core.reverse();
  const nodes=[];
  let truth=full;
  core.forEach((j,k)=>{
    truth &= (full^ms[j]);
    if(k)nodes.push({rule:"AND3",left:k===1?core[0]:"d"+(k-1),right:j,truth});
  });
  if(truth!==0||core.length!==D[full])throw Error("producer invariant");
  return {label:"UNSAT",mu:core.length,paid:nodes.length,core,nodes};
}
function run() {
  const fixtures=[],counts={};
  function add(n,kind,ids){
    const r={n,kind,clause_indices:ids,...solve(n,ids)};
    fixtures.push(r);
    const key=n+":"+r.label+":"+(r.paid??-1);
    counts[key]=(counts[key]||0)+1;
  }
  for(const n of [1,2]){
    for(let bits=0;bits<(1<<(3**n));bits++){
      const ids=[];for(let i=0;i<3**n;i++)if(bits&(1<<i))ids.push(i);
      add(n,"exhaustive",ids);
    }
  }
  const n=3,U=allClauses(3);
  for(let t=0;t<512;t++){
    let ids=[];
    if(t===0)ids=U.map((c,i)=>c.length===3?i:-1).filter(i=>i>=0);
    else if(t===1)ids=[];
    else if(t===2)ids=[0];
    else if(t===3)ids=U.map((_,i)=>i);
    else {
      // Exclude the empty clause in general fixtures; retain explicit t=2 negative control.
      const m=((Math.imul(t,2654435761)^Math.imul(t*t,2246822519)^0x9e3779b9)>>>0)&((1<<26)-1);
      ids=U.map((_,i)=>i>0&&(m&(1<<(i-1)))?i:-1).filter(i=>i>=0);
    }
    add(n,"deterministic",ids);
  }
  return {schema:"LSPV2-388-three-variable-optimum-v1",
    model:"fixed R_mix341, free clauses; AND3 local factors; every paid inference <=2 premises",
    fixtures,counts};
}
if(typeof module!=="undefined" && require.main===module)process.stdout.write(JSON.stringify(run())+"\n");
