/* Load prior pinned checker 2026-11-27_1513_feedback.js; call quadratic(F,guard,true) on its exact projected factors. */
function quadratic(F,guard,multiply=true){
 const V=[...new Set(F.flatMap(f=>f.vs))].sort((a,b)=>a-b), pos=new Map(V.map((v,i)=>[v,i+1])),n=V.length;
 const keys=[[],...V.map(v=>[v])], ix=new Map(keys.map((v,i)=>[v.join(","),i]));
 for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){ix.set([V[i],V[j]].join(","),keys.length);keys.push([V[i],V[j]])}
 const bit=i=>1n<<BigInt(i), high=x=>x.toString(2).length-1;
 const basis=new Map(),orig=[],linear=[],units=[],proofs=[];let rowTests=0,xors=0,peak=0,verification=0;
 const A=new Map(guard);
 function insert(mask,owner,terms,mult=0){
  if(!mask)return null;
  const id=orig.length;orig.push({owner,terms,mult,mask});let proof=bit(id);
  while(mask){let k=high(mask),b=basis.get(k);if(!b){basis.set(k,[mask,proof]);peak=Math.max(peak,basis.size);return null}mask^=b[0];proof^=b[1];xors++}
  return null;
 }
 function toMask(terms,mult=0){let mask=0n;for(const t of terms){let u=[...new Set(mult?[...t,mult]:t)].sort((a,b)=>a-b);mask^=bit(ix.get(u.join(",")))}return mask}
 for(let fi=0;fi<F.length;fi++){
  const f=F[fi], rows=f.rows.filter(w=>f.vs.every((v,i)=>!A.has(v)||A.get(v)===((w>>i)&1)));
  if(!rows.length)return {status:"LOCAL_UNSAT",units:[],rowTests,xors,verification,peak,proofs:[]};
  const terms=[[],...f.vs.map(v=>[v])];for(let i=0;i<f.vs.length;i++)for(let j=i+1;j<f.vs.length;j++)terms.push([f.vs[i],f.vs[j]]);
  const ev=rows.map(w=>terms.reduce((mask,t,i)=>t.every(v=>(w>>f.vs.indexOf(v))&1)?mask|bit(i):mask,0n));
  // enumerate bounded local coefficient vectors; obtain a basis with low degree prioritized
  let local=new Map();
  for(let c=1;c<2**terms.length;c++){
   const b=BigInt(c);let good=true;for(const e of ev){rowTests++;let x=e&b,p=0;while(x){p^=1;x&=x-1n}if(p){good=false;break}}
   if(!good)continue;let z=b;while(z&&local.has(high(z)))z^=local.get(high(z));if(!z)continue;local.set(high(z),z);
   const tt=terms.filter((_,i)=>(b&bit(i))!==0n);
   insert(toMask(tt),fi,tt);
   if(tt.every(t=>t.length<=1))linear.push({fi,tt});
  }
 }
 for(const [v,b] of guard){const tt=b?[[],[v]]:[[v]];insert(toMask(tt),-1,tt);linear.push({fi:-1,tt})}
 if(multiply)for(const {fi,tt} of linear)for(const v of V)insert(toMask(tt,v),fi,tt,v);
 function verify(mask,p){
  let result=0n,used=[];
  for(let j=0;j<orig.length;j++)if(p&bit(j)){
   const {owner,terms,mult}=orig[j];if(owner<0){const u=terms.flat()[0];if(!A.has(u)||Boolean(A.get(u))!==terms.some(t=>t.length===0))throw Error("bad guard")}
   else{const f=F[owner];for(const w of f.rows){let a=new Map(f.vs.map((v,i)=>[v,(w>>i)&1]));if([...A].some(([v,b])=>a.has(v)&&a.get(v)!==b))continue;let parity=0;for(const t of terms){verification++;if(t.every(v=>a.get(v)===1))parity^=1}if(parity)throw Error("bad local polynomial")}}
   // independent monomial conversion: toggle string labels, then map to feature indices
   let set=new Set();for(const t of terms){let u=[...new Set(mult?[mult,...t]:t)].sort((a,b)=>a-b).join(",");if(set.has(u))set.delete(u);else set.add(u)}
   for(const u of set)result^=bit(ix.get(u));used.push({owner,terms,mult});
  }
  if(result!==mask)throw Error("bad combination");return used;
 }
 if(basis.has(0)){let [mask,p]=basis.get(0);proofs.push({claim:"1=0",used:verify(mask,p)});return {status:"UNSAT",units,rowTests,xors,verification,peak,features:keys.length,generators:orig.length,proofs}}
 // linear consequences left after eliminating higher-degree monomials
 const lb=new Map([...basis].filter(([i])=>i<=n));
 for(const j of [...lb.keys()].sort((a,b)=>a-b)){if(j===0)continue;let [m,p]=lb.get(j);for(const k of [...lb.keys()])if(k>j&&(lb.get(k)[0]&bit(j))){let [q,r]=lb.get(k);lb.set(k,[q^m,r^p]);xors++}}
 for(const [j,[mask,p]] of lb)if(j>0&&(mask===bit(j)||mask===(bit(j)|1n))&&!A.has(V[j-1])){let b=Number(mask&1n);units.push([V[j-1],b]);proofs.push({claim:[V[j-1],b],used:verify(mask,p)})}
 return {status:"UNKNOWN",units,rowTests,xors,verification,peak,features:keys.length,generators:orig.length,proofs}
}
function trial(F,guard){
 let s=P.closure(F,guard,"occupancy"),a=P.closure(F,guard,"affine"),b=P.closure(F,guard,"binary");
 const G=F.map(f=>({...f,rows:f.rows.filter(w=>f.vs.every((v,i)=>!new Map(guard).has(v)||new Map(guard).get(v)===((w>>i)&1)))}));
 const sep=P.project(G,8);const ck=P.checkProject(G,sep.trace);
 let q=s.no?{status:"LOCAL_UNSAT",units:[],proofs:[],rowTests:0,xors:0,verification:0}:quadratic(F,guard,true);
 let C=P.cnf(F),d=P.solve(C,guard,[],1500000),check=d.status==="UNSAT"?P.checkTree(C,guard,d.tree):{ok:false,work:0};if(d.status==="UNSAT"&&!check.ok)throw Error("DAG replay");
 let hybrid={status:"not attempted"};if(q.units.length){const extra=q.units.map(([v,b])=>[b?v:-v]);let z=P.solve([...C,...extra],guard,[],1500000),ch=z.status==="UNSAT"?P.checkTree([...C,...extra],guard,z.tree):{ok:false,work:0};hybrid={status:z.status,nodes:z.nodes,work:z.work,check:ch,tree:z.tree}}
 return {guard,occupancy:s,affine:a,binary:b,separator:{status:sep.F.some(f=>!f.rows.length)?"UNSAT":"UNKNOWN",retired:sep.trace.length,work:sep.work,verify:ck.work},quadratic:q,dag:{status:d.status,nodes:d.nodes,work:d.work,check,tree:d.tree},hybrid}
}
module.exports={quadratic,trial};
