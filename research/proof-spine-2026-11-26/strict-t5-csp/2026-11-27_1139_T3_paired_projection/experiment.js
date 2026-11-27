function experiment(compile,B,R,L){
 const {sha,norm,closure,affine,compact,reduce,solve,lift,unique}=L;
 const out=[];
 for(const id of ["JOINT-24","RANDOM-3CNF-40"]){
 const x=B.instances.find(z=>z.id===id), e=R.instances.find(z=>z.alias==="EB-"+id), g=compile(x),raw=JSON.stringify(g.network)+"\n";
 if(sha(raw)!==e.sha256||raw.length*8!==e.N_bits||sha(x.dimacs)!==e.source_cnf.sha256||x.dimacs.length*8!==e.source_cnf.N_bits)throw Error("ID");
 let S=norm(g.network),M={n:0,cap:1e7},pins=new Map(),local=closure(S.factors,pins,M),ge=affine(S),H=compact(S),fs=H.fs.slice(),trace=[],checks=0,scans=0, cap=3000000;
 // Exact two-factor affine/Boolean join, only if result is one clause.
 const project=(w,U,V)=>V.reduce((a,v,i)=>a+(((w>>U.indexOf(v))&1)<<i),0);
 for(;;){
  let occ=new Map();for(const f of fs)for(const v of f.vs){if(++scans+checks>cap)throw Error("cap");if(!occ.has(v))occ.set(v,[]);occ.get(v).push(f);}
  let found=false;
  for(const [v,ff] of occ){if(ff.length!==2)continue;let U=[...new Set(ff.flatMap(f=>f.vs))].sort((a,b)=>a-b),V=U.filter(z=>z!==v);if(U.length>7)continue;
   let ok=new Set();for(let w=0;w<2**U.length;w++){if(++checks+scans>cap)throw Error("cap");if(ff.every(f=>f.ok.includes(project(w,U,f.vs))))ok.add(project(w,U,V));}
   let bad=[];for(let w=0;w<2**V.length;w++)if(!ok.has(w))bad.push(w);
   if(!bad.length)continue;
   const c=V.flatMap((z,i)=>bad.every(w=>((w>>i)&1)===((bad[0]>>i)&1))?[((bad[0]>>i)&1)?-z:z]:[]);
   if(bad.length!==2**(V.length-c.length))continue;
   const a=[...ok].sort((a,b)=>a-b),newId=S.factors.length+trace.length;
   trace.push({v,inputs:ff.map(f=>f.id),V,ok:a,clause:c,newId});
   fs=fs.filter(f=>!ff.includes(f));fs.push({id:newId,vs:V,ok:a});found=true;break;
  }if(!found)break;
 }
 // Alternative independent projection check: enumerate output words and both pivot choices.
 let replay=H.fs.slice(),verify=0;for(const t of trace){let ff=replay.filter(f=>f.vs.includes(t.v));if(JSON.stringify(ff.map(f=>f.id))!==JSON.stringify(t.inputs)||ff.length!==2)throw Error("scope");let V=[...new Set(ff.flatMap(f=>f.vs))].filter(v=>v!==t.v).sort((a,b)=>a-b);if(JSON.stringify(V)!==JSON.stringify(t.V))throw Error("boundary");
 let a=[];for(let w=0;w<2**V.length;w++){let sat=false;for(let b=0;b<2;b++){verify++;const get=v=>v===t.v?b:((w>>V.indexOf(v))&1);if(ff.every(f=>f.ok.includes(f.vs.reduce((s,v,i)=>s+(get(v)<<i),0))))sat=true;}if(sat)a.push(w);if(sat!==t.clause.some(l=>((w>>V.indexOf(Math.abs(l)))&1)===Number(l>0)))throw Error("clause");}if(JSON.stringify(a)!==JSON.stringify(t.ok))throw Error("join");replay=replay.filter(f=>!ff.includes(f));replay.push({id:t.newId,vs:V,ok:a});}
 // Reclose and independently encode exact remaining tables, using all forbidden assignments.
 let Q=[],M2={n:0,cap:1e7},p2=new Map();let cl2=closure(fs,p2,M2);
 for(const f of fs){let t=trace.find(t=>t.newId===f.id);if(t)Q.push(t.clause);else {for(let w=0;w<2**f.vs.length;w++)if(!f.ok.includes(w))Q.push(f.vs.map((v,i)=>((w>>i)&1)?-v:v));}}
 Q=unique(Q);let D=reduce(Q,2e6),T=solve(D.F,2e6),V=solve(D.F,2e6,T.tree),lifted=lift(Q),prior=lift(H.F);
 let cnf=x.dimacs.trim().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1)),C=solve(cnf,2e6);
 out.push({id,instance:e.instance_id,N:e.N_bits,hash:sha(raw),cnfHash:sha(x.dimacs),local:{ok:local,pins:pins.size,checks:M.n},ge,privateRetired:H.trace.length,initialCompact:H.F.length,pairRetired:trace.length,remainingFactors:fs.length,clauses:Q.length,scans,checks,verify,reclosure:{ok:cl2,pins:p2.size,checks:M2.n},resolution:{retired:D.trace.length,clauses:D.F.length,scans:D.scans,pairs:D.ops},tree:{nodes:T.nodes,reads:T.scans,verify:V.scans},directCNF:{nodes:C.nodes,reads:C.scans},priorLift:{n:prior.n,m:prior.m,N:prior.N},newLift:{n:lifted.n,m:lifted.m,N:lifted.N},trace,dpTrace:D.trace,treeProof:T.tree});
 }return out;
}
// Node CLI: node experiment.js compile.js benchmarks.json registry.json hybrid.js
const fs=require('node:fs');const [cp,bp,rp,hp]=process.argv.slice(2);const c=fs.readFileSync(cp,'utf8'),h=fs.readFileSync(hp,'utf8');const compile=Function(c.slice(c.indexOf('function compile('),c.indexOf('function auditLocal('))+';return compile')();const lib=Function(h.slice(0,h.lastIndexOf('if(typeof require'))+';return {sha,norm,closure,affine,compact,reduce,solve,lift,gadgetAudit,unique}')();console.log(JSON.stringify(experiment(compile,JSON.parse(fs.readFileSync(bp)),JSON.parse(fs.readFileSync(rp)),lib),null,2));
