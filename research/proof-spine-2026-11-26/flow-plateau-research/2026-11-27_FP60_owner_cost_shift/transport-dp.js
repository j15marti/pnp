function transportDP(G,n,map,cnf){
 const reps=new Map(Object.entries(map.representative_ports).map(([key,[p,s]])=>[key,[n.roots[p],n.sg[p]^s]]));if(reps.get("f")[0]!==n.gauge||reps.get("f")[1]!==0||new Set([...reps.values()].map(x=>x[0])).size!==reps.size)throw Error("representative mismatch");
 const owners=new Map(),priv=new Map(),factors=new Map(n.factors.map(f=>[f.ids[0],f]));let portChecks=0,rowReads=0,rows=0,elims=0,maxWidth=0,scans=0;
 for(const v of n.B){let [tag,id,i,j,k]=map.vertex_provenance[v];if(tag!=="clause")throw Error("tag");let [a,b,c]=map.ternary_clauses[i],lit=x=>["x"+Math.abs(x),Number(x<0)],z="z"+i,T=j===0?[lit(a),lit(b),[z,0]]:[[z,1],lit(c),["f",0]];T.push(["w"+i+"_"+j,0]);for(let h=0;h<4;h++){let [key,s]=T[h],[r,t]=reps.get(key),p=4*v+h;portChecks++;if(n.roots[p]!==r||n.sg[p]!== (t^s))throw Error("port");if(key!=="f"&&(!key.startsWith("x")||Number(key.slice(1))>map.original_n)){if(priv.has(r)&&priv.get(r)!==id)throw Error("owner overlap");priv.set(r,id)}}if(!owners.has(id))owners.set(id,[]);owners.get(id).push(factors.get(v))}
 const union=F=>[...new Set(F.flatMap(f=>f.vs))].sort((a,b)=>a-b),idx=(S,U,w)=>S.reduce((s,v,j)=>s|(((w>>U.indexOf(v))&1)<<j),0);
 const details=[];
 for(let id=1;id<=cnf.length;id++){let C=cnf[id-1],src=[...new Set(C.map(l=>Math.abs(l)))],X=src.map(v=>reps.get("x"+v)[0]),F=owners.get(id).map(x=>({...x})),all=union(F),aux=all.filter(v=>!X.includes(v)),trace=[];
 if(aux.some(r=>priv.get(r)!==id)||X.some(r=>!all.includes(r)))throw Error("scope");
 while(aux.length){let opts=aux.map(v=>{let fs=F.filter(f=>{scans++;return f.vs.includes(v)}),S=union(fs).filter(x=>x!==v);return {v,fs,S}}).sort((a,b)=>a.S.length-b.S.length||a.v-b.v),{v,fs,S}=opts[0],U=[...S,v];maxWidth=Math.max(maxWidth,S.length);if(S.length>14)throw Error("width");
 let cost=[];for(let w=0;w<2**S.length;w++){let vals=[0,1].map(b=>fs.reduce((s,f)=>{rowReads++;return s+f.cost[idx(f.vs,U,w|(b<<S.length))]},0));cost.push(Math.min(...vals))}
 trace.push({v,S,cost,ids:fs.flatMap(f=>f.ids)});F=F.filter(f=>!fs.includes(f));F.push({vs:S,cost,ids:fs.flatMap(f=>f.ids)});aux=aux.filter(x=>x!==v);elims++}
 let final=[];for(let w=0;w<2**src.length;w++){let A=new Map(X.map((r,j)=>[r,((w>>j)&1)^reps.get("x"+src[j])[1]])),got=F.reduce((s,f)=>{rowReads++;return s+f.cost[f.vs.reduce((a,v,j)=>a|(A.get(v)<<j),0)]},0),want=2*Number(!C.some(l=>((w>>src.indexOf(Math.abs(l)))&1)===Number(l>0)));if(got!==want)throw Error("energy");rows++;final.push(got)}
 details.push({id,sourceVars:src,owners:owners.get(id).flatMap(f=>f.ids),trace,final})}
 return {portChecks,rowReads,rows,elims,maxWidth,scans,details};
}
function checkTransportDP(n,map,cnf,d){
 let checks=0;const reps=new Map(Object.entries(map.representative_ports).map(([key,[p,s]])=>[key,[n.roots[p],n.sg[p]^s]])),by=new Map(n.factors.map(f=>[f.ids[0],f]));
 let seen=new Set();for(const a of d.details){let F=a.owners.map(v=>{if(seen.has(v))throw Error("owner repeated");seen.add(v);return by.get(v)});
 for(const t of a.trace){let fs=F.filter(f=>f.vs.includes(t.v)),vars=[...new Set(fs.flatMap(f=>f.vs))],S=vars.filter(v=>v!==t.v).sort((a,b)=>a-b);if(JSON.stringify(S)!==JSON.stringify(t.S)||JSON.stringify(fs.flatMap(f=>f.ids))!==JSON.stringify(t.ids))throw Error("trace");let m=Array(t.cost.length).fill(Infinity);for(let w=0;w<2**vars.length;w++){let A=new Map(vars.map((v,i)=>[v,(w>>i)&1])),z=0;for(let f of fs){checks++;z+=f.cost[f.vs.reduce((s,v,j)=>s|(A.get(v)<<j),0)]}let j=S.reduce((s,v,i)=>s|(A.get(v)<<i),0);m[j]=Math.min(m[j],z)}if(m.some((x,i)=>x!==t.cost[i]))throw Error("trace row");F=F.filter(f=>!fs.includes(f));F.push({vs:S,cost:m,ids:t.ids})}
 const X=a.sourceVars,C=cnf[a.id-1];for(let w=0;w<a.final.length;w++){let A=new Map(X.map((v,j)=>[reps.get("x"+v)[0],((w>>j)&1)^reps.get("x"+v)[1]]));let z=F.reduce((s,f)=>{checks++;return s+f.cost[f.vs.reduce((s,v,j)=>s|(A.get(v)<<j),0)]},0);if(z!==a.final[w]||z!==2*Number(!C.some(l=>((w>>X.indexOf(Math.abs(l)))&1)===Number(l>0))))throw Error("final")}}
 if(seen.size!==n.B.length)throw Error("missing owner");return {checks,owners:seen.size};
}
function shiftOnly(F,pins,cap=250000){
 const A=new Map(pins),Q=F.map(f=>{let vs=f.vs.filter(v=>!A.has(v));return {vs,ids:f.ids,cost:Array.from({length:2**vs.length},(_,w)=>f.cost[f.vs.reduce((s,v,j)=>s|((A.has(v)?A.get(v):(w>>vs.indexOf(v))&1)<<j),0)])}});
 let work=0,steps=[],bounds=[],status="COMPLETE";const idx=(S,U,w)=>S.reduce((s,v,j)=>s|(((w>>U.indexOf(v))&1)<<j),0),bound=()=>Q.reduce((s,f)=>s+Math.min(...f.cost),0),inc=new Map();
 for(let i=0;i<Q.length;i++)for(let v of Q[i].vs){if(!inc.has(v))inc.set(v,[]);inc.get(v).push(i)}
 const adj=Q.map((f,i)=>[...new Set(f.vs.flatMap(v=>inc.get(v)))].filter(j=>j!==i).sort((a,b)=>a-b));
 const tick=(k=1)=>{if(work+k>cap)throw Error("cap");work+=k};
 bounds.push(bound());try{for(let sweep=0;sweep<4;sweep++){for(let i=0;i<Q.length;i++)for(let j of adj[i]){tick();let a=Q[i],b=Q[j],I=a.vs.filter(v=>b.vs.includes(v)),p=Array(2**I.length).fill(Infinity);for(let w=0;w<a.cost.length;w++){tick();let z=idx(I,a.vs,w);p[z]=Math.min(p[z],a.cost[w])}if(p.every(x=>!x))continue;let ac=a.cost.map((z,w)=>{tick();return z-p[idx(I,a.vs,w)]}),bc=b.cost.map((z,w)=>{tick();return z+p[idx(I,b.vs,w)]});for(let w=0;w<ac.length;w++){tick();if(ac[w]<0||a.cost[w]-ac[w]!==p[idx(I,a.vs,w)])throw Error("a")}for(let w=0;w<bc.length;w++){tick();if(bc[w]-b.cost[w]!==p[idx(I,b.vs,w)])throw Error("b")}if(Math.min(...ac)+Math.min(...bc)<Math.min(...a.cost)+Math.min(...b.cost))throw Error("decrease");steps.push({i,j,I,p});a.cost=ac;b.cost=bc}
 bounds.push(bound());}}catch(e){if(String(e)!=="Error: cap")throw e;status="CAPPED"}
 return {status,work,bounds,final:bound(),steps,adjEdges:adj.reduce((s,a)=>s+a.length,0)};
}
function replayShifts(F,pins,s){
 let A=new Map(pins),Q=F.map(f=>{let vs=f.vs.filter(v=>!A.has(v));return {vs,cost:Array.from({length:2**vs.length},(_,w)=>{let M=new Map(A);vs.forEach((v,j)=>M.set(v,(w>>j)&1));return f.cost[f.vs.reduce((s,v,j)=>s|(M.get(v)<<j),0)]})}}),checks=0;
 for(const t of s.steps){let a=Q[t.i],b=Q[t.j],I=t.I;if(!I.every(v=>a.vs.includes(v)&&b.vs.includes(v)))throw Error("interface");const fn=(f,sign)=>f.cost.map((x,w)=>{checks++;let A=new Map(f.vs.map((v,j)=>[v,(w>>j)&1])),z=I.reduce((s,v,j)=>s|(A.get(v)<<j),0),q=x+sign*t.p[z];if(q<0)throw Error("negative");return q});a.cost=fn(a,-1);b.cost=fn(b,1)}
 let bound=Q.reduce((s,f)=>s+Math.min(...f.cost),0);if(bound!==s.final)throw Error("bound");return {checks,bound};
}
module.exports={transportDP,checkTransportDP,shiftOnly,replayShifts};
