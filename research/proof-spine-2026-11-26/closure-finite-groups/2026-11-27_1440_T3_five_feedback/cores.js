function coreAudit(L,G,q,g,cert){
 let owners=new Map(),rowTests=0,joinTests=0,reasonVisits=0;
 for(let v=0;v<G.types.length;v++)if(G.types[v]==="B"){
 let p=[0,1,2,3].map(j=>4*v+j),s=[...new Set(p.map(i=>q.R[i]+1))].sort((a,b)=>a-b),a=[];
 for(let t=0;t<2**s.length;t++){rowTests++;if(p.reduce((sum,i)=>sum+(((t>>s.indexOf(q.R[i]+1))&1)^q.Q[i]),0)===2)a.push(t)}
 let key=JSON.stringify([s,a]);if(!owners.has(key))owners.set(key,v)
 }
 let F=q.F.map((f,i)=>({...g.F[i],owners:[owners.get(JSON.stringify([f.s,f.a]))]}));
 if(F.some(f=>f.owners[0]===undefined))throw Error("owner");
 for(let v of cert.chart.projection){
 let idx=F.map((f,i)=>f.s.includes(v)?i:-1).filter(i=>i>=0);
 if(!idx.length)throw Error("missing pivot");
 let s=[...new Set(idx.flatMap(i=>F[i].s))].sort((a,b)=>a-b),b=s.filter(x=>x!==v),a=[];
 for(let t=0;t<2**b.length;t++){let ok=false;for(let z=0;z<2;z++){joinTests++;if(idx.every(i=>{let f=F[i],u=f.s.reduce((m,w,j)=>m|((w===v?z:(t>>b.indexOf(w))&1)<<j),0);return f.a.includes(u)})){ok=true;break}}if(ok)a.push(t)}
 let owner=[...new Set(idx.flatMap(i=>F[i].owners))].sort((a,b)=>a-b),del=new Set(idx);F=F.filter((_,i)=>!del.has(i));if(a.length!==2**b.length)F.push({s:b,a,owners:owner});if(!a.length){F=[{s:b,a,owners:owner}];break}
 }
 let M=new Map();for(let f of F)for(let t=0;t<2**f.s.length;t++)if(!f.a.includes(t)){let c=f.s.map((v,j)=>(t>>j)&1?-v:v);M.set(c.join(","),{c,owners:f.owners})}
 let C=[...M.values()];if(JSON.stringify(C.map(x=>x.c))!==JSON.stringify(cert.chart.clauses))throw Error("chart replay");
 let cores=[];
 for(let guard of cert.guards.filter(x=>x.refuted)){
 let reason=new Map(guard.h.map(l=>[l,[]])),hit=null,change=true,used=[];
 while(change&&!hit){change=false;for(let i=0;i<C.length;i++){let {c,owners}=C[i],sat=false,un=[],deps=[...owners];for(let l of c){reasonVisits++;if(reason.has(l)){sat=true;break}if(reason.has(-l))deps.push(...reason.get(-l));else un.push(l)}if(sat)continue;if(un.length===0){hit=[...new Set(deps)].sort((a,b)=>a-b);used.push(i);break}if(un.length===1){reason.set(un[0],[...new Set(deps)]);used.push(i);change=true}}}
 if(!hit)throw Error("no conflict");let Bset=new Set(hit);
 // Independently check on reduced original factor set. Same gauge, original equality transport, exact projection of reduced factors using greedy order, then scalar UP; failure is disclosed.
 let rawF=q.F.filter(f=>Bset.has(owners.get(JSON.stringify([f.s,f.a])))),pos=q.F.map((f,i)=>Bset.has(owners.get(JSON.stringify([f.s,f.a])))?i:-1).filter(i=>i>=0);
 let Fsub=pos.map(i=>g.F[i]);
 // Only eliminate variables not in guard; use exact projection with pinned guard folded into factors first.
 let A=new Map(guard.h.map(l=>[Math.abs(l),+(l>0)]));
 Fsub=Fsub.map(f=>{let s=f.s.filter(v=>!A.has(v)),a=[];for(let t of f.a)if(f.s.every((v,j)=>!A.has(v)||A.get(v)===(t>>j&1))){let z=s.reduce((m,v,j)=>m|((t>>f.s.indexOf(v)&1)<<j),0);if(!a.includes(z))a.push(z)}return{s,a}});
 let reduced=L.project(Fsub),check={visits:0},replay=reduced.F.some(f=>!f.a.length)||L.up(L.clauses(reduced.F),[],check,1e7).bad;
 cores.push({guard_id:guard.guard_id,residual_id:guard.residual_id,h:guard.h,B:hit,projectionClauseIDs:[...new Set(used)].sort((a,b)=>a-b),subsetReplay:{bad:replay,pivots:reduced.trace.length,scans:reduced.scans,rows:reduced.rows,visits:check.visits}});
 }
 let overlaps=[];for(let i=0;i<cores.length;i++)for(let j=i+1;j<cores.length;j++){let a=cores[i].B,b=new Set(cores[j].B),intersection=a.filter(v=>b.has(v));overlaps.push({i,j,intersection:intersection.length,symmetricDifference:a.length+b.size-2*intersection.length})}
 return{cores,overlaps,rowTests,joinTests,reasonVisits}
}
module.exports=coreAudit;
