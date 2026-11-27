function verify(s){
 let compile=Function(s.compiler.slice(s.compiler.indexOf("function compile("),s.compiler.indexOf("function auditLocal("))+";return compile")(),H=Function(s.hybrid.split('if(typeof require==="function"')[0]+";return {sha,norm}")(),B=JSON.parse(s.corpus),R=JSON.parse(s.registry);
 const assert=(b,m)=>{if(!b)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),CAP=2000000;let result=[];
 for(let [key,id] of [["joint","JOINT-24"],["random","RANDOM-3CNF-40"]]){
  let P=JSON.parse(s[key]),I=B.instances.find(x=>x.id===id),e=R.instances.find(x=>x.alias==="EB-"+id),G=compile(I),raw=JSON.stringify(G.network)+"\n";assert(H.sha(raw)===e.sha256&&raw.length*8===e.N_bits&&H.sha(I.dimacs)===e.source_cnf.sha256,"source");assert(P.instance_id===e.instance_id&&P.original_N_bits===e.N_bits&&P.guard_id==="EMPTY"&&P.residual_id==="ROOT","identity");
  let S=H.norm(G.network),fs=S.factors.slice(),checks={private:0,batch:0,dp:0,literals:0,scope:0},nodes=0;assert(P.gauge===S.gauge,"gauge");
  function proj(w,U,V){let a=0;V.forEach((v,i)=>{let j=U.indexOf(v);assert(j>=0,"coordinate");a|=((w>>j)&1)<<i});return a}
  function step(fac,v,vs,ok,kind){let U=[...new Set(fac.flatMap(f=>f.vs))].sort((a,b)=>a-b),V=U.filter(x=>x!==v),A=new Set();assert(eq(V,vs)&&U.length<=7,"scope/width");for(let w=0;w<2**U.length;w++){if(++checks[kind]>CAP)throw Error("cap");if(fac.every(f=>f.ok.includes(proj(w,U,f.vs))))A.add(proj(w,U,V))}assert(eq([...A].sort((a,b)=>a-b),ok),"projection");}
  for(let t of P.privateTrace){let fac=fs.filter(f=>{checks.scope++;return f.vs.includes(t.v)});assert(fac.length===1&&fac[0].id===t.factor,"private scope");step(fac,t.v,t.vs,t.ok,"private");let j=fs.indexOf(fac[0]);fs[j]={...fac[0],vs:t.vs,ok:t.ok}}
  let seen=new Set(fs.map(f=>f.id));
  for(let row of P.batches){let piv=new Set(row.map(t=>t.v)),kill=new Set(),add=[];assert(piv.size===row.length,"unique pivot");
   for(let t of row){let fac=fs.filter(f=>{checks.scope++;return f.vs.includes(t.v)});assert(fac.length===2&&eq(fac.map(f=>f.id),t.in),"pair scope");assert(fac.every(f=>!kill.has(f.id)&&f.vs.filter(v=>piv.has(v)).length===1),"simultaneous disjoint");assert(!seen.has(t.out),"fresh factor");seen.add(t.out);step(fac,t.v,t.vs,t.ok,"batch");fac.forEach(f=>kill.add(f.id));if(t.ok.length!==2**t.vs.length)add.push({id:t.out,vs:t.vs,ok:t.ok})}
   fs=fs.filter(f=>!kill.has(f.id)).concat(add)
  }
  function canon(a){let s=[...new Set(a)].sort((a,b)=>a-b);return s.some(l=>s.includes(-l))?null:s}
  function uniq(a){let m=new Map();for(let c of a){let s=canon(c);if(s)m.set(s.join(","),s)}return [...m.values()]}
  let F=[];for(let f of fs){let bad=Array.from({length:2**f.vs.length},(_,i)=>i).filter(w=>!f.ok.includes(w));if(!bad.length)continue;let fixed=f.vs.map((v,i)=>[v,i,bad[0]>>i&1]).filter(([v,i,b])=>bad.every(w=>(w>>i&1)===b));let Q=bad.length===2**(f.vs.length-fixed.length)?[fixed.map(([v,i,b])=>b?-v:v)]:bad.map(w=>f.vs.map((v,i)=>w>>i&1?-v:v));for(let w=0;w<2**f.vs.length;w++)assert(Q.every(c=>c.some(l=>(w>>f.vs.indexOf(Math.abs(l))&1)===Number(l>0)))===f.ok.includes(w),"CNF exact");F.push(...Q)}F=uniq(F);
  for(let t of P.dp){let A=F.filter(c=>c.includes(t.v)),B=F.filter(c=>c.includes(-t.v));assert(eq(A.concat(B),t.removed),"DP scope");let Q=[];for(let a of A)for(let b of B){checks.dp++;Q.push(a.filter(l=>l!==t.v).concat(b.filter(l=>l!==-t.v)))}Q=uniq(Q);assert(eq(Q,t.added),"DP");F=uniq(F.filter(c=>!c.includes(t.v)&&!c.includes(-t.v)).concat(Q))}
  function walk(t,p){nodes++;let changed=true;while(changed){changed=false;for(let c of F){let open=[],hit=false;for(let l of c){if(++checks.literals>CAP)throw Error("cap");let v=Math.abs(l);if(!p.has(v))open.push(l);else if(p.get(v)===Number(l>0)){hit=true;break}}if(hit)continue;if(open.length===0){assert(t===0,"leaf");return}if(open.length===1){p.set(Math.abs(open[0]),Number(open[0]>0));changed=true}}}assert(Array.isArray(t)&&t.length===3&&!p.has(t[0])&&F.some(c=>c.some(l=>Math.abs(l)===t[0])),"branch");for(let b=0;b<2;b++)walk(t[b+1],new Map([...p,[t[0],b]]))}
  walk(P.tree,new Map());result.push({id,verified:true,certSha:H.sha(s[key]),checks,nodes,finalClauses:F.length})
 }return result
}
if(typeof require==='function'){let fs=require('fs');let keys=['compiler','corpus','registry','hybrid','joint','random'];let s=Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]));console.log(JSON.stringify(verify(s),null,2));}
