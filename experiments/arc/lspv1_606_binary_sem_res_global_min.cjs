#!/usr/bin/env node
"use strict";
// LSPV-1/606. Independent finite control for the binary-semantic / Resolution
// shared-DAG minimum theorem. REFERENCE calculi, NOT historical R_mix341.
// Usage: node experiments/arc/lspv1_606_binary_sem_res_global_min.cjs
function experiment(){
 const n=2,all=[];
 for(let c=0;c<1<<(2*n);c++){let good=true;for(let v=0;v<n;v++)if((c&(3<<(2*v)))===(3<<(2*v)))good=false;if(good)all.push(c);}
 const nonempty=all.filter(x=>x!==0);
 const clauseTrue=(c,a)=>{for(let v=0;v<n;v++){if((c&(1<<(2*v)))&&((a>>v)&1))return true;if((c&(2<<(2*v)))&&!((a>>v)&1))return true;}return false};
 // Truth masks are independent of the syntactic Resolution producer.
 const trueM=all.map(c=>{let z=0;for(let a=0;a<(1<<n);a++)if(clauseTrue(c,a))z|=1<<a;return z});
 const res=all.map(()=>all.map(()=>0)),sem=all.map(()=>all.map(()=>0));
 for(let i=0;i<all.length;i++)for(let j=0;j<all.length;j++){
  let a=all[i],b=all[j];
  for(let k=0;k<all.length;k++)if(((trueM[i]&trueM[j])&(~trueM[k]))===0)sem[i][j]|=(1<<k);
  for(let v=0;v<n;v++){let p=1<<(2*v),q=2<<(2*v);
   for(let [x,y] of [[p,q],[q,p]])if((a&x)&&(b&y)){let r=(a&~x)|(b&~y);if(all.includes(r))res[i][j]|=1<<all.indexOf(r)}
  }
 }
 const shortest=(source,edges)=>{
  let start=0;for(let j=0;j<nonempty.length;j++)if((source>>j)&1)start|=1<<all.indexOf(nonempty[j]);
  if(start&1)return 0;
  let frontier=[start],seen=new Uint8Array(1<<all.length);seen[start]=1;let d=0;
  while(frontier.length){
   let next=[];d++;
   for(let state of frontier){
    let present=[];for(let j=0;j<all.length;j++)if(state&(1<<j))present.push(j);
    let targets=0;for(let j=0;j<present.length;j++)for(let k=j;k<present.length;k++)targets|=edges[present[j]][present[k]];
    targets&=~state;
    for(let j=0;j<all.length;j++)if(targets&(1<<j)){
     let z=state|(1<<j);
     if(z&1)return d;
     if(!seen[z]){seen[z]=1;next.push(z);}
    }
   }frontier=next;
  }return null;
 };
 let counts={sat:0,unsat:0,work:{},counterexamples:[]},tests=0,eq=0;
 for(let s=0;s<(1<<nonempty.length);s++){
  let sat=false;for(let a=0;a<(1<<n);a++)if(nonempty.every((c,i)=>((s>>i)&1)===0||clauseTrue(c,a))){sat=true;break;}
  let r=shortest(s,res),m=shortest(s,sem);tests++;
  if(sat)counts.sat++;else{counts.unsat++;counts.work[r]=(counts.work[r]||0)+1;}
  if(r!==m||((r===null)!==sat))counts.counterexamples.push({s,r,m,sat});else eq++;
 }
 let induct=0,fail=[];
 const isSub=(a,b)=>(a&b)===a;
 for(let i=0;i<all.length;i++)for(let j=0;j<all.length;j++)for(let k=0;k<all.length;k++)if(sem[i][j]&(1<<k))
  for(let u=0;u<all.length;u++)if(isSub(all[u],all[i]))
   for(let v=0;v<all.length;v++)if(isSub(all[v],all[j])){
    induct++;
    const possible=isSub(all[u],all[k])||isSub(all[v],all[k])||all.some((c,x)=>isSub(c,all[k])&&((res[u][v]>>x)&1));
    if(!possible)fail.push([i,j,k,u,v]);
   }
 return {run:"LSPV-1/606",date:"2026-11-12 17:55 PST",
   model:"two-variable non-tautological clauses; canonical signed masks; all original source subsets",
   universe:all.length,nonempty:nonempty.length,source_count:tests,agreement:eq,
   counts,inductive_cases:induct,induction_failures:fail.length,
   induction_examples:fail.slice(0,3),sample_source:nonempty,
   independent_checks:"truth masks for semantic entailment, syntactic resolvents, BFS clause-set minima, direct SAT truth tables",
   historical_calculus_authenticated:false};
}
const out=experiment();
if(out.counts.counterexamples.length||out.induction_failures||out.source_count!==256||out.agreement!==256||out.counts.sat!==95||out.counts.unsat!==161)throw Error("test failure");
console.log(JSON.stringify(out,null,2));
