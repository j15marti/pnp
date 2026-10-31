"use strict";
function produce(){
 const out={run:"ARC_HORN_INTERFACE_HELLY275",timestamp:"2026-10-31T09:00:00-07:00",status:"PROVED/EXACT restricted; COMPUTATIONAL finite controls; OPEN universal ARC and P versus NP",sources:[],theorem:{horn_module_helly:"k+1 sharp",arbitrary_module_helly:"2^k sharp"},totals:{assertions:0,endpointChecks:0,pairModes:0,proofSteps:0,bruteAssignments:0,guestChildren:0}};
 function ck(x,s){out.totals.assertions++;if(!x)throw Error(s)}
 function litval(l,a){return a[Math.abs(l)-1]===(l>0?1:0)}
 function truecount(c,a){return c.reduce((s,l)=>s+(litval(l,a)?1:0),0)}
 function model(C,a){return C.every(c=>c.some(l=>litval(l,a)))}
 function counts(C,a){const t=C.map(c=>truecount(c,a)),N=[0,0,0,0];for(const x of t)N[x]++;return {t,N,SAT:N[0]===0}}
 function assign(n,mask){return Array.from({length:n},(_,j)=>(mask>>j)&1)}
 function brutes(C,n){let count=0,w=null;for(let m=0;m<(1<<n);m++){out.totals.bruteAssignments++;const a=assign(n,m);if(model(C,a)){count++;if(!w)w=a}}return {count,w}}
 function dpll(C,n){
  const v={nodes:0,clauses:0,literals:0,unit:0,branches:0};
  function go(a){v.nodes++;while(true){let changed=false;
   for(const c of C){v.clauses++;let open=[],sat=false;for(const l of c){v.literals++;let x=a[Math.abs(l)-1];if(x<0)open.push(l);else if(x===(l>0?1:0)){sat=true;break}}
    if(sat)continue;if(open.length===0)return null;if(open.length===1){const l=open[0],i=Math.abs(l)-1,b=l>0?1:0;if(a[i]>=0&&a[i]!==b)return null;if(a[i]!==b){a[i]=b;v.unit++;changed=true;break}}}
   if(!changed)break;
  }
  let every=true;for(const c of C){if(!c.some(l=>a[Math.abs(l)-1]>=0&&litval(l,a))){every=false;break}}
  if(every)return a.map(x=>x<0?0:x);
  let i=a.findIndex(x=>x<0);if(i<0)return null;
  for(const b of [0,1]){v.branches++;const copy=a.slice();copy[i]=b;const w=go(copy);if(w)return w}return null;
  }
  const w=go(Array(n).fill(-1));return {...v,label:w?"SAT":"UNSAT",w};
 }
 function makeMods(k){let next=k+1,mods=[];
  function pin(lit){const p=next++,q=next++;return {clauses:[[lit,p,q],[lit,p,-q],[lit,-p,q],[lit,-p,-q]],private:[p,q],kind:"pin",lit,p,q}}
  for(let i=1;i<=k;i++)mods.push({name:"positive_"+i,...pin(i)});
  let neg;
  if(k===1)neg=pin(-1);
  if(k===2){const z=next++;neg={clauses:[[-1,-2,z],[-1,-2,-z]],private:[z],kind:"binary",z}}
  if(k===3)neg={clauses:[[-1,-2,-3]],private:[],kind:"ternary"};
  if(k>=4){let x=next++,cl=[[-1,-2,x]],ids=[x];for(let i=3;i<=k-2;i++){let y=next++;cl.push([-x,-i,y]);ids.push(y);x=y}cl.push([-x,-(k-1),-k]);neg={clauses:cl,private:ids,kind:"chain"}}
  mods.push({name:"negative_all",...neg});
  return {mods,n:next-1};
 }
 function flatten(mods,drop){let clauses=[],groups=[];mods.forEach((m,j)=>{if(j===drop)return;const ids=[];for(const c of m.clauses){ids.push(clauses.length);clauses.push(c.slice())}groups.push({id:j,name:m.name,kind:m.kind,sourceIds:ids,private:m.private,lit:m.lit,p:m.p,q:m.q,z:m.z})});return {clauses,groups}}
 function support(C,g,k){let mask=0,probes=0;for(let b=0;b<(1<<k);b++){let ok=false;for(let a=0;a<(1<<g.private.length);a++){let vals=Array(Math.max(k,...g.private)).fill(0);for(let j=0;j<k;j++)vals[j]=(b>>j)&1;for(let j=0;j<g.private.length;j++)vals[g.private[j]-1]=(a>>j)&1;probes+=g.sourceIds.reduce((z,idx)=>z+C[idx].length,0);if(g.sourceIds.every(idx=>model([C[idx]],vals))){ok=true;break}}if(ok)mask|=1<<b}return {mask,probes}}
 function meetclosed(mask,k){for(let a=0;a<(1<<k);a++)if((mask>>a)&1)for(let b=0;b<(1<<k);b++)if((mask>>b)&1)if(!((mask>>(a&b))&1))return false;return true}
 function extremes(c){return c.map(l=>({variable:Math.abs(l),literal:l,S:l>0?1:0,S_inverted:l>0?0:1,U:l>0?0:1,U_inverted:l>0?1:0}))}
 function pair(c,d){const m={SS:true,SU:true,US:true,UU:true},same=[],opposite=[];for(const l of c){for(const v of d)if(Math.abs(l)===Math.abs(v)){(Math.sign(l)===Math.sign(v)?same:opposite).push(Math.abs(l));for(const mode of Object.keys(m)){let a=mode[0]==="S"?(l>0?1:0):(l>0?0:1),b=mode[1]==="S"?(v>0?1:0):(v>0?0:1);if(a!==b)m[mode]=false}}}ck(m.SS===(opposite.length===0)&&m.UU===(opposite.length===0)&&m.SU===(same.length===0)&&m.US===(same.length===0),"pair theorem");return {same:[...new Set(same)],opposite:[...new Set(opposite)],m}}
 function res(c,d,p){let c1=c.includes(p)?c:d,c2=c1===c?d:c;if(!c1.includes(p)||!c2.includes(-p))return null;const r=[...new Set([...c1.filter(l=>l!==p),...c2.filter(l=>l!==-p)])].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);if(r.some(l=>r.includes(-l)))return null;return r}
 function genproof(C,groups,k){const pool=C.map(c=>c.slice()),steps=[];function step(i,j,p){const r=res(pool[i],pool[j],p);ck(r!==null,"invalid resolution");const id=pool.length;pool.push(r);steps.push({parents:[i,j],pivot:p,clause:r});return id}
  const u=[];for(let i=1;i<=k;i++){const g=groups.find(z=>z.name==="positive_"+i),ids=g.sourceIds;const a=step(ids[0],ids[1],g.q);const b=step(ids[2],ids[3],g.q);const id=step(a,b,g.p);ck(JSON.stringify(pool[id])===JSON.stringify([i]),"pin resolution");u.push(id)}
  const g=groups.find(z=>z.name==="negative_all");let v;
  if(k===1){const ids=g.sourceIds;const a=step(ids[0],ids[1],g.q),b=step(ids[2],ids[3],g.q);v=step(a,b,g.p)}
  else if(k===2)v=step(g.sourceIds[0],g.sourceIds[1],g.z);
  else if(k===3)v=g.sourceIds[0];
  else {v=step(g.sourceIds[0],g.sourceIds[1],g.private[0])}
  for(let i=1;i<=k;i++)v=step(u[i-1],v,i);
  ck(pool[v].length===0,"refutation not empty");return {steps,terminal:v};
 }
 function child(C,n,i,b){const outC=[];for(const c of C){if(c.some(l=>Math.abs(l)===i&&((l>0?1:0)===b)))continue;outC.push(c.filter(l=>Math.abs(l)!==i))}return {clauses:outC,text:"p cnf "+n+" "+outC.length+"\n"+outC.map(c=>c.join(" ")+" 0").join("\n")+"\n"}}
 function analyze(k,drop,mods,n,label){
  const {clauses:C,groups}=flatten(mods,drop);for(const c of C)ck(c.length===3&&new Set(c.map(Math.abs)).size===3,"source proper");
  const oracle=brutes(C,n),baseline=dpll(C,n);ck((oracle.count>0)=== (label==="SAT"),"source polarity");ck(baseline.label===label,"UP-DPLL label");if(baseline.w)ck(model(C,baseline.w),"DPLL witness");
  const supports=groups.map(g=>({...g,...support(C,g,k)}));const fullmask=(1<<(1<<k))-1;let joint=fullmask;for(const g of supports){ck(meetclosed(g.mask,k),"Horn projection not meet closed");joint&=g.mask}
  ck((joint!==0)===(label==="SAT"),"join polarity");
  if(drop===-1){ck(joint===0,"Horn core should UNSAT");for(const g of supports){let j=fullmask;for(const h of supports)if(h!==g)j&=h.mask;ck(j!==0,"sharp Horn core")}}
  const e=C.map((c,j)=>({clauseIndex:j,literals:c,occurrences:extremes(c)})),pairs=[];for(let j=0;j<C.length;j++)for(let h=j+1;h<C.length;h++){pairs.push({j,h,...pair(C[j],C[h])});out.totals.pairModes+=4}
  const zero=Array(n).fill(0),one=Array(n).fill(1),base=counts(C,zero),opp=counts(C,one);for(let j=0;j<C.length;j++)ck(base.t[j]+opp.t[j]===3,"complement");out.totals.endpointChecks+=C.length;
  const flips=[];let a=zero.slice(),prev=base;for(let i=0;i<Math.min(n,6);i++){a[i]^=1;const nextStatus=counts(C,a);for(let j=0;j<C.length;j++){const c=C[j];let delta=0;for(const l of c)if(Math.abs(l)===i+1)delta+=litval(l,a)?1:-1;ck(prev.t[j]+delta===nextStatus.t[j],"flip");}flips.push({variable:i+1,status:nextStatus});prev=nextStatus}
  const derived=[];for(let j=0;j<C.length;j++)for(let h=j+1;h<C.length;h++)for(const l of C[j])if(C[h].includes(-l)){const r=res(C[j],C[h],l);if(r){ck(!oracle.w||r.some(x=>litval(x,oracle.w)),"source resolvent");if(derived.length<12)derived.push({parents:[j,h],pivot:Math.abs(l),clause:r,forbiddenCube:r.map(t=>[Math.abs(t),t<0?1:0])})}}
  const ch=[];for(const b of [0,1]){const c=child(C,n,1,b),solver=dpll(c.clauses,n),truth=brutes(c.clauses,n);ck((truth.count>0)===(solver.label==="SAT"),"child label");ch.push({pin:[1,b],bytes:c.text.length,dimacs:c.text,label:solver.label,guestNodes:solver.nodes,guestLiteralReads:solver.literals});out.totals.guestChildren++}
  ck(label===(ch.some(c=>c.label==="SAT")?"SAT":"UNSAT"),"Shannon OR");
  const cert=label==="UNSAT"&&drop===-1?genproof(C,groups,k):null;
  if(cert)out.totals.proofSteps+=cert.steps.length;
  return {name:"horn_k"+k+"_"+(drop===-1?"UNSAT":"drop"+drop+"_SAT"),k,drop,label,n,clauses:C,groups:supports.map(g=>({id:g.id,name:g.name,kind:g.kind,sourceIds:g.sourceIds,private:g.private,supportMask:g.mask})),models:oracle.count,witness:oracle.w,baseline:{nodes:baseline.nodes,clauses:baseline.clauses,literals:baseline.literals,unit:baseline.unit,branches:baseline.branches},costLedger:{sourceLiteralScan:3*C.length,projectionLiteralProbes:supports.reduce((s,g)=>s+g.probes,0),policySwitches:1,failedPairwiseShortcut:label==="UNSAT"&&k>=2,proofCheckSteps:cert?cert.steps.length:0,guestChildLiteralReads:ch.reduce((s,g)=>s+g.guestLiteralReads,0),childSerializedBytes:ch.reduce((s,g)=>s+g.bytes,0)},extremes:e,compatibility:pairs,endpoints:{zero:base,one:opp},flipTrail:flips,resolutionBlockers:derived,shannonChildren:ch,sourceResolutionRefutation:cert}
 }
 for(let k=1;k<=4;k++){const {mods,n}=makeMods(k);out.sources.push(analyze(k,-1,mods,n,"UNSAT"));out.sources.push(analyze(k,k,mods,n,"SAT"))}
 // Arbitrary interface modules: complete signed 3CNF, every 7 of 8 SAT, but all 8 UNSAT.
 const B=[];for(let m=0;m<8;m++)B.push([1,2,3].map((i,j)=>((m>>j)&1)?-i:i));
 const full=brutes(B,3);ck(full.count===0,"8-sign control");for(let d=0;d<8;d++)ck(brutes(B.filter((_,i)=>i!==d),3).count>0,"7-sign control");
 out.nonHorn={name:"8-signed-clause-coverage",k:3,moduleCount:8,everySevenSAT:true,allEightUNSAT:true,meetClosedEach:B.map(c=>{let mask=0;for(let a=0;a<8;a++)if(model([c],assign(3,a)))mask|=1<<a;return meetclosed(mask,3)}),clauses:B};
 return out;
}
if(typeof module!=="undefined"&&require.main===module)process.stdout.write(JSON.stringify(produce(),null,2)+"\n");