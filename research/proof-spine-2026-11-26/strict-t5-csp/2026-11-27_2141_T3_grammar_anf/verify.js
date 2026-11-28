function verify(d,certs){
 const C=Function(d.compiler.slice(d.compiler.indexOf("function compile("),d.compiler.indexOf("function auditLocal("))+";return compile")(),H=Function(d.hybrid.split('if(typeof require==="function"')[0]+";return {sha,norm}")();
 const A=(v,m)=>{if(!v)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),sort=a=>[...new Set(a)].sort((a,b)=>a-b),key=a=>sort(a).join(","),enc=x=>JSON.stringify(x)+"\n",out=[];
 let B=JSON.parse(d.corpus),R=JSON.parse(d.registry),mm=JSON.parse(d.mm),nativeMany=JSON.parse(d.nativeMany);
 function canonical(F){let m=new Map();for(let c of F){let a=sort(c);if(!a.some(l=>a.includes(-l)))m.set(a.join(","),a)}return [...m.values()]}
 function rank(rows){let b=new Map(),ops=0;for(let a of rows){while(a){let k=a&-a;if(!b.has(k)){b.set(k,a);break}a^=b.get(k);ops++}}return {rank:b.size,basis:b,ops}}
 for(let [id,rawCert] of Object.entries(certs)){
  let P=JSON.parse(rawCert),I,E,peer=null;if(id.startsWith("MIXED")){peer=JSON.parse(id.includes("MANY")?d.many:d.mixed).find(x=>x.cert.alias===id);I={id,dimacs:peer.cert.dimacs,nvars:+peer.cert.dimacs.split(" ")[2]};E=id.includes("MANY")?nativeMany.instances.find(x=>x.short_id.startsWith("EB-"+id+"@")):mm.instances.find(x=>x.alias===id)}else{I=B.instances.find(x=>x.id===id);E=R.instances.find(x=>x.alias==="EB-"+id)}
  let G=C(I),S=H.norm(G.network),raw=enc(G.network),expected=E.native??E;
  A(H.sha(raw)===P.instance_id.split(":").pop()&&raw.length*8===P.original_N_bits&&P.original_N_bits===(expected.N_bits??expected.N)&&H.sha(raw)===(expected.sha256??expected.instance?.split(":").pop()??expected.instance_id.split(":").pop()),"native identity");
  A(H.sha(I.dimacs)===(E.source_cnf?.sha256??(E.cnf_id??E.instance_id).split(":").pop()),"cnf identity");
  A(P.gauge===S.gauge&&P.guard_id==="EMPTY"&&P.residual_id==="ROOT","guard");
  let fs=new Map(S.factors.map(f=>[f.id,f])),index=new Map(),seen=new Set(fs.keys()),checks={scope:0,projection:0,cnf:0,local:0,tree:0,intersections:0};
  const insert=f=>{fs.set(f.id,f);for(let v of f.vs){if(!index.has(v))index.set(v,new Set());index.get(v).add(f.id)}};
  const remove=f=>{fs.delete(f.id);for(let v of f.vs)index.get(v).delete(f.id)};
  for(let f of S.factors)insert(f);
  for(let t of P.projection){let ids=[...index.get(t.pivot)??[]],b=ids.map(x=>fs.get(x)),U=sort(b.flatMap(x=>x.vs)),V=U.filter(x=>x!==t.pivot),ok=[];checks.scope+=ids.length;A(eq(ids,t.in)&&eq(V,t.vs)&&U.length<=7&&!seen.has(t.out),"complete bucket");seen.add(t.out);
   for(let y=0;y<2**V.length;y++){let pass=false;for(let p=0;p<2;p++){checks.projection++;let get=v=>v===t.pivot?p:(y>>V.indexOf(v)&1);if(b.every(f=>f.ok.includes(f.vs.reduce((s,v,i)=>s+(get(v)<<i),0))))pass=true}if(pass)ok.push(y)}A(eq(ok,t.ok),"projection");for(let f of b)remove(f);if(ok.length!==2**V.length)insert({id:t.out,vs:V,ok})}
  let F=[];for(let f of fs.values()){let bad=[];for(let w=0;w<2**f.vs.length;w++)if(!f.ok.includes(w))bad.push(w);if(!bad.length)continue;let fixed=f.vs.map((v,i)=>[v,i,bad[0]>>i&1]).filter(([v,i,b])=>bad.every(w=>(w>>i&1)===b));let q=bad.length===2**(f.vs.length-fixed.length)?[fixed.map(([v,i,b])=>b?-v:v)]:bad.map(w=>f.vs.map((v,i)=>w>>i&1?-v:v));for(let w=0;w<2**f.vs.length;w++){checks.cnf++;A(q.every(c=>c.some(l=>(w>>f.vs.indexOf(Math.abs(l))&1)===Number(l>0)))===f.ok.includes(w),"table to CNF")}F.push(...q)}F=canonical(F);
  function up(guard){let p=new Map();for(let l of guard){let v=Math.abs(l),b=Number(l>0);if(p.has(v)&&p.get(v)!==b)return {conflict:true,p};p.set(v,b)}for(;;){let ch=false;for(let c of F){let u=[],hit=false;for(let l of c){checks.tree++;let v=Math.abs(l);if(!p.has(v))u.push(l);else if(p.get(v)===Number(l>0)){hit=true;break}}if(hit)continue;if(!u.length)return {conflict:true,p};if(u.length===1){p.set(Math.abs(u[0]),Number(u[0]>0));ch=true}}if(!ch)return {conflict:false,p}}}
  let root=up([]);A(eq([...root.p],P.rootPins),"root pins");A(!P.rootPins.length,"nonzero pins not handled by this verifier");
  let covered=new Set(),mon=new Map([["",0]]),rows=[];
  for(let r of P.groupedRows){let v=sort(r.ids.flatMap(i=>F[i].map(Math.abs)));A(eq(v,r.vs),"group scope");for(let i of r.ids){A(!covered.has(i),"owner duplicate");covered.add(i)}for(let w=0;w<2**v.length;w++){checks.local++;let bad=Number(!r.ids.every(i=>F[i].some(l=>(w>>v.indexOf(Math.abs(l))&1)===Number(l>0))));let val=0;for(let t of r.terms)if(t.every(a=>w>>v.indexOf(a)&1))val^=1;A(val===bad,"group indicator")}
   let z=0n;for(let t of r.terms){let k=key(t);if(!mon.has(k))mon.set(k,mon.size);z^=1n<<BigInt(mon.get(k))}rows.push(z)
  }A(covered.size===F.length,"row cover");
  let rr=rank(rows),proof=null,removals=null,peerReplay=null;
  if(P.proof){A(P.proof.reduce((s,i)=>s^rows[i],0n)===1n,"constant proof");A(rr.rank===rows.length-P.kernelBasis.length,"nullity dimension");
   for(let dep of P.kernelBasis)A(dep.reduce((s,i)=>s^rows[i],0n)===0n,"nullspace vector");
   A(rank(P.kernelBasis.map(dep=>dep.reduce((a,i)=>a^(1n<<BigInt(i)),0n))).rank===P.kernelBasis.length,"kernel independence");
   // Independent deletion check using direct membership of constant, not producer's nullspace classification.
   let failures=0,ops=0;for(let i=0;i<rows.length;i++){let b=rank(rows.filter((_,j)=>j!==i).concat(1n));ops+=b.ops;let base=rank(rows.filter((_,j)=>j!==i));ops+=base.ops;if(b.rank>base.rank)failures++}removals={tested:rows.length,constantNoLongerInSpan:failures,rowXors:ops};proof={rows:P.proof.length,rank:rr.rank,nullity:rows.length-rr.rank,constant:true};
  }
  let treeNodes=0;if(P.guardedTrees){for(let g of P.guardedTrees){function walk(t,G){treeNodes++;let u=up(G);if(u.conflict){A(t===0,"tree leaf");return}A(Array.isArray(t)&&t.length===3&&!u.p.has(t[0])&&F.some(c=>c.some(l=>Math.abs(l)===t[0])),"branch");walk(t[1],G.concat(-t[0]));walk(t[2],G.concat(t[0]))}walk(g.tree,g.guard)}
   let v=sort(P.guardedTrees.flatMap(g=>g.guard.map(Math.abs))),count=0;for(let mask=1;mask<1<<P.guardedTrees.length;mask++){checks.intersections++;let p=new Map(),good=true,sign=-1;for(let i=0;i<P.guardedTrees.length;i++)if(mask>>i&1){sign*=-1;for(let l of P.guardedTrees[i].guard){let a=Math.abs(l),b=Number(l>0);if(p.has(a)&&p.get(a)!==b)good=false;p.set(a,b)}}if(good)count+=sign*2**(v.length-p.size)}A(count===2**v.length,"exact guard coverage")
  }
  if(peer){
   // Paid map comparison after native proof discovery. Original physical f determines complement gauge.
   let rep=G.source_map.representative_ports,fp=rep.f;A(S.r[fp[0]]+1===S.gauge,"source anchor map");let fbit=S.p[fp[0]]^fp[1],map=new Map();
   for(let i=1;i<=I.nvars;i++){let [p,s]=rep["x"+i];map.set(i,(S.r[p]+1)*(S.p[p]^s^fbit?-1:1))}
   let original=I.dimacs.trim().split("\n").slice(1).map(l=>l.split(/\s+/).map(Number).slice(0,-1));
   let mapped=canonical(original.map(c=>c.map(l=>Math.sign(l)*map.get(Math.abs(l))))),actual=new Set(F.map(c=>c.join(",")));
   A(mapped.length===F.length&&mapped.every(c=>actual.has(c.join(","))),"exact signed chart adapter");
   let ans={mappedClauses:mapped.length,sourceMapHash:H.sha(enc(G.source_map)),peerCertificateId:peer.certificate_id,verifiedPeerDigest:H.sha(enc(peer.cert))===peer.certificate_id.split(":").pop()};
   // Larger peer cert has exact ANF polynomials. Replay from original CNF, not just assume them.
   if(peer.cert.rows.every(r=>Array.isArray(r.terms))){let total=new Set(),tests=0;for(let r of peer.cert.rows){let V=sort(r.ids.flatMap(i=>original[i].map(Math.abs)));for(let w=0;w<2**V.length;w++){tests++;let a=Number(!r.ids.every(i=>original[i].some(l=>(w>>V.indexOf(Math.abs(l))&1)===Number(l>0)))),b=r.terms.reduce((s,t)=>s^Number(t.every(v=>w>>V.indexOf(v)&1)),0);A(a===b,"peer ANF replay")}for(let t of r.terms){let k=key(t);if(total.has(k))total.delete(k);else total.add(k)}}A(total.size===1&&total.has(""),"peer constant");ans.independentPeerWords=tests;ans.peerConstant=true}
   peerReplay=ans;
  }
  out.push({id,certificateSha:H.sha(rawCert),verified:true,checks,treeNodes,rank:rr.rank,rankXors:rr.ops,proof,removals,peerReplay})
 }return out
}
if(typeof require==='function'){const fs=require('fs'),keys=['compiler','corpus','registry','hybrid','mixed','mm','many','nativeMany'];let d=Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]));let ids=['JOINT-24','RANDOM-3CNF-40','MIXED-3-NO','MIXED-MANY-3-NO'];let certs=Object.fromEntries(ids.map((k,i)=>[k,fs.readFileSync(process.argv[i+2+keys.length],'utf8')]));console.log(JSON.stringify(verify(d,certs),null,2));}
