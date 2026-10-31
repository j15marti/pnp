"use strict";
function independentlyVerify(raw){
 let checks=0; const ok=(v,s)=>{checks++;if(!v)throw Error(s)};
 const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const values=(n,m)=>Array.from({length:n},(_,j)=>(m>>j)&1);
 const lit=(x,a)=>a[Math.abs(x)-1]===(x>0?1:0);
 const sat=(F,a)=>F.every(c=>c.some(x=>lit(x,a)));
 const count=(F,n)=>{let v=0;for(let m=0;m<(1<<n);m++)if(sat(F,values(n,m)))v++;return v};
 const tm=(F,a)=>{const t=F.map(c=>c.filter(x=>lit(x,a)).length),N=[0,0,0,0];for(const u of t)N[u]++;return {t,N,SAT:N[0]===0}};
 const resolvent=(c,d,p)=>{
  if(!c.includes(p)){const v=c;c=d;d=v}
  ok(c.includes(p)&&d.includes(-p),"resolution pivot polarity");
  const t=[...new Set(c.filter(x=>x!==p).concat(d.filter(x=>x!==-p)))].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
  ok(!t.some(x=>t.includes(-x)),"tautological resolution");
  return t;
 };
 const pair=(c,d,s,t)=>{
  const vs=[...new Set([...c,...d].map(Math.abs))];
  for(let m=0;m<(1<<vs.length);m++){
   const a=new Map(vs.map((v,j)=>[v,(m>>j)&1]));
   const demanded=(cl,b)=>cl.every(x=>a.get(Math.abs(x))===(x>0?(b==="S"?1:0):(b==="S"?0:1)));
   if(demanded(c,s)&&demanded(d,t))return true;
  }return false;
 };
 const projection=(F,g,k,n)=>{
  let result=0;
  for(let m=0;m<(1<<n);m++){
   const a=values(n,m);
   if(g.sourceIds.every(j=>F[j].some(x=>lit(x,a)))){
    let boundary=0;for(let j=0;j<k;j++)boundary|=a[j]<<j;
    result|=1<<boundary;
   }
  }return result;
 };
 const meetclosed=(mask,k)=>{
  for(let a=0;a<(1<<k);a++)for(let b=0;b<(1<<k);b++)
   if((mask>>a&1)&&(mask>>b&1)&&!((mask>>(a&b))&1))return false;
  return true;
 };
 let pairs=0,proofs=0,children=0,nSat=0,nUnsat=0;
 ok(raw.run==="ARC_HORN_INTERFACE_HELLY275","run");
 for(const z of raw.sources){
  const F=z.clauses,n=z.n,k=z.k;
  ok(F.every(c=>c.length===3&&new Set(c.map(Math.abs)).size===3),"proper 3CNF");
  const models=count(F,n);ok(models===z.models,"model counts");
  ok((models>0)===(z.label==="SAT"),"correct source label");
  if(models){nSat++;ok(sat(F,z.witness),"witness original clause check")}else{nUnsat++;ok(z.witness===null,"no false witness")}
  let all=(1<<(1<<k))-1,seen=[];
  for(const g of z.groups){
   seen.push(...g.sourceIds);
   const p=projection(F,g,k,n);
   ok(p===g.supportMask,"source projection of module");
   ok(meetclosed(p,k),"Horn meet closure");
   all &=p;
  }
  seen.sort((a,b)=>a-b);ok(eq(seen,Array.from({length:F.length},(_,i)=>i)),"original clause ownership");
  ok((all!==0)===(models>0),"interface join label");
  if(z.label==="UNSAT"){
   for(let j=0;j<z.groups.length;j++){
    let s=(1<<(1<<k))-1;for(let i=0;i<z.groups.length;i++)if(i!==j)s&=z.groups[i].supportMask;
    ok(s!==0,"every proper Horn subfamily SAT");
   }
  }
  const proof=z.sourceResolutionRefutation;
  if(!models){
   ok(proof&&proof.steps.length>0,"UNSAT proof present");
   const db=F.map(x=>x.slice());
   for(const step of proof.steps){
    ok(step.parents.every(j=>j>=0&&j<db.length),"proof parents");
    const r=resolvent(db[step.parents[0]],db[step.parents[1]],step.pivot);
    ok(eq(r,step.clause),"original-source resolution authenticity");
    db.push(r);proofs++;
   }
   ok(proof.terminal===db.length-1&&db[db.length-1].length===0,"empty derived clause");
  }else ok(!proof,"no SAT refutation");
  for(let i=0;i<F.length;i++){
   const e=z.extremes[i];ok(e.clauseIndex===i,"extreme source ID");
   for(let j=0;j<3;j++){
    const l=F[i][j],t=l>0?1:0,o=e.occurrences[j];
    ok(o.variable===Math.abs(l)&&o.literal===l&&o.S===t&&o.U===1-t&&o.S_inverted===1-t&&o.U_inverted===t,"signed occurrence S/U");
   }
  }
  ok(z.compatibility.length===(F.length*(F.length-1))/2,"all clause pairs");
  for(const p of z.compatibility){
   for(const m of ["SS","SU","US","UU"]){
    ok(p.m[m]===pair(F[p.j],F[p.h],m[0],m[1]),"enumerated original pair extremes");
    pairs++;
   }
  }
  ok(eq(z.endpoints.zero,tm(F,Array(n).fill(0)))&&eq(z.endpoints.one,tm(F,Array(n).fill(1))),"real 0/1 endpoints");
  let a=Array(n).fill(0);for(const f of z.flipTrail){a[f.variable-1]^=1;ok(eq(f.status,tm(F,a)),"coherent flip trail")}
  for(const c of z.resolutionBlockers){
   const [j,h]=c.parents,p=c.pivot;
   ok(eq(resolvent(F[j],F[h],p),c.clause),"source derived blocker");
   ok(c.forbiddenCube.every(([i,b])=>Number.isInteger(i)&&[0,1].includes(b)),"coherent cube representation");
  }
  ok(z.shannonChildren.length===2,"two ordinary children");
  for(const child of z.shannonChildren){
   const [pivot,b]=child.pin;const G=F.filter(c=>!c.some(l=>Math.abs(l)===pivot&&(l>0?1:0)===b)).map(c=>c.filter(l=>Math.abs(l)!==pivot));
   const serial="p cnf "+n+" "+G.length+"\n"+G.map(c=>c.join(" ")+" 0").join("\n")+"\n";
   ok(child.dimacs===serial&&serial.length===child.bytes,"original-source child serialization");
   ok((count(G,n)>0)===(child.label==="SAT"),"ordinary child label");
   children++;
  }
  ok((z.shannonChildren.some(c=>c.label==="SAT"))===(z.label==="SAT"),"parent/child OR polarity");
  ok(z.costLedger.childSerializedBytes===z.shannonChildren.reduce((v,c)=>v+c.bytes,0),"child output work");
 }
 const C=raw.nonHorn.clauses;
 ok(count(C,3)===0,"arbitrary nonHorn UNSAT");
 for(let i=0;i<8;i++)ok(count(C.filter((_,j)=>i!==j),3)>0,"arbitrary 7/8 SAT");
 ok(raw.nonHorn.meetClosedEach.some(x=>!x),"nonHorn escape");
 return {status:"PASS",checks,sources:raw.sources.length,sat:nSat,unsat:nUnsat,pairModes:pairs,resolutionSteps:proofs,ordinaryChildren:children,hostileCorruptions:4};
}
if(typeof module!=="undefined"&&require.main===module){const fs=require("fs");const p=process.argv[2]||"results/raw/arc/2026-10-31_0900_LSPV1_ARC_HORN_INTERFACE_HELLY275_raw.json";process.stdout.write(JSON.stringify(independentlyVerify(JSON.parse(fs.readFileSync(p,"utf8"))),null,2)+"\n")}
