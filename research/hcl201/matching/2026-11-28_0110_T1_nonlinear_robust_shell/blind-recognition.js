
function recognize(C){
 let events=0,D=[],cons=[],neg2=[],neg3=[],iv=new Map(),x=new Set(),owners=Array(C.length);
 function ok(a,b){if(!a)throw Error(b)}
 try{
 for(let [i,r] of C.entries()){events+=r.length+1;let pos=r.every(v=>v>0),neg=r.every(v=>v<0);if(pos&&r.length===3){ok(new Set(r).size===3,"repeated demand literal");let d=D.length;for(let v of r){ok(!iv.has(v),"overlapping positive demands");iv.set(v,d)}D.push(r);owners[i]=["D",d]}else if(pos&&r.length===2){ok(r[0]!==r[1],"consumer loop");cons.push([i,r]);r.forEach(v=>x.add(v))}else if(neg&&r.length===2)neg2.push([i,r.map(Math.abs)]);else if(neg&&r.length===3)neg3.push([i,r.map(Math.abs)]);else throw Error("non-shell clause grammar")}
 ok(D.length>0&&[...x].every(v=>!iv.has(v)),"interior boundary overlap");
 let adj=new Map([...iv.keys()].map(v=>[v,new Set()]));for(let [i,[a,b]] of neg2){events++;ok(iv.has(a)&&iv.has(b)&&a!==b,"non-bin exclusion");adj.get(a).add(b);adj.get(b).add(a)}
 let bins=[],seen=new Set();for(let v of sort([...iv.keys()]))if(!seen.has(v)){let Q=[v];seen.add(v);for(let i=0;i<Q.length;i++)for(let w of adj.get(Q[i])){events++;if(!seen.has(w)){seen.add(w);Q.push(w)}}for(let a of Q)for(let b of Q)if(a!==b){events++;ok(adj.get(a).has(b),"nonclique bin")}bins.push(sort(Q))}
 bins.sort((a,b)=>a[0]-b[0]);let d=D.length,q=bins.length,binOf=new Map();bins.forEach((B,j)=>B.forEach(v=>binOf.set(v,j)));
 let N=D.map(r=>sort(r.map(v=>binOf.get(v))));ok(q===d+2&&N.every((r,i)=>r.join(",")===[i,i+1,i+2].join(",")),"interval shell not recognized");
 let xs=sort([...x]),xi=new Map(xs.map((v,i)=>[v,i])),blockByVar=new Map();for(let [i,r] of neg3){events+=3;let a=r.filter(v=>iv.has(v)),B=r.filter(v=>x.has(v));ok(a.length===1&&B.length===2&&B[0]!==B[1]&&!blockByVar.has(a[0]),"not one AND per occurrence");blockByVar.set(a[0],sort(B));owners[i]=["AND-BLOCK",binOf.get(a[0])]}
 let edgeVars=[];for(let [j,B] of bins.entries()){let b=blockByVar.get(B[0]);if(j<d){ok(b&&B.every(v=>J(blockByVar.get(v))===J(b)),"different blocker in bin");edgeVars.push(b.map(v=>xi.get(v)))}else ok(B.every(v=>!blockByVar.has(v)),"unexpected blocker")}
 let byPair=new Map();edgeVars.forEach((r,i)=>{let k=r.slice().sort((a,b)=>a-b).join(",");ok(!byPair.has(k),"repeated blocker pair");byPair.set(k,i)});ok(cons.length===d,"consumer count");let covered=new Set();for(let [i,r] of cons){let k=r.map(v=>xi.get(v)).sort((a,b)=>a-b).join(","),e=byPair.get(k);ok(e!==undefined&&!covered.has(e),"consumer/blocker mismatch");covered.add(e);owners[i]=["CONSUMER",e]}
 for(let [i,[a,b]] of neg2)owners[i]=["EX",binOf.get(a)];
 let links=Array.from({length:xs.length},()=>[]);edgeVars.forEach(([a,b],i)=>{links[a].push([b,i]);links[b].push([a,i])});let centers=links.map((r,i)=>r.length===6?i:-1).filter(i=>i>=0);ok(centers.length===1&&links.every((r,i)=>r.length===(i===centers[0]?6:2)),"noncactus degrees");
 let center=centers[0],ordered=[center,...Array.from({length:xs.length},(_,i)=>i).filter(i=>i!==center)],relabel=new Map(ordered.map((v,i)=>[v,i])),visited=new Set(),cycles=[],used=new Set();
 for(let [v,e] of links[center])if(!used.has(e)){let cur=v,prev=e,vs=[center],es=[e];used.add(e);while(cur!==center){events++;ok(!visited.has(cur),"cycle overlap");visited.add(cur);vs.push(cur);let next=links[cur].find(z=>z[1]!==prev);ok(next&&!used.has(next[1]),"cycle edge reuse");es.push(next[1]);used.add(next[1]);cur=next[0];prev=next[1]}cycles.push({v:vs.map(v=>relabel.get(v)),edges:es})}
 ok(cycles.length===3&&used.size===d&&visited.size===xs.length-1,"incomplete cactus");
 let X=ordered.map(i=>xs[i]),E=edgeVars.map(r=>r.map(v=>relabel.get(v))),edges=D.flatMap((r,i)=>r.map(v=>[i,binOf.get(v),v]));return {status:"RECOGNIZED",events,G:{b:d,nv:X.length,d,q,N,bins,C,owners,x:X,edges,edgeVars:E,cycles}}
 }catch(e){return {status:"REFUSED",reason:String(e.message),events}}
}
function blindRun(raw,common,corpus){
 let result=[];for(let r of raw){let C=r.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1)),a=recognize(C);assert(a.status==="RECOGNIZED","blind acquisition "+a.reason);let G=a.G;
 // Normalize edge orientation in independent cycle traversal; only undirected AND/OR semantics.
 let R=cactusDP(G),checks=verifyCactusDP(G,R),ans=R.best<=2?"SAT":"UNSAT";assert(ans===r.answer&&R.best===r.dp.best,"blind agreement");let w=ans==="SAT"?cactusWitness(G,R.z):null;
 result.push({instance:r.instance_id,N:r.N,sourceHash:sha(r.dimacs),events:a.events,cycles:G.cycles.map(x=>x.v.length),center:G.x[0],boundary:G.x,binCount:G.q,dp:R,checks,answer:ans,witness:w})
 }
 let refusals=[];for(let x of common){let src=corpus.instances.find(z=>z.id===x.name),C=src.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));refusals.push({instance:x.cnf.summary.instance_id,root:"ROOT",...recognize(C)});let F=x.native.artifact.residual.map(([s,h,o])=>({s,m:BigInt("0x"+h),o})),v=reindex(F);refusals.push({instance:x.native.summary.instance_id,residual:x.native.summary.residualId,...recognize(clauses(v.F))})}
 // Two direct refusal controls for an unqualified scalar quotient.
 let H=[[0],[1,2]];let a=matching(H,new Set([0])),b=matching(H,new Set([1]));assert(!a.ok&&b.ok,"robust slack counterexample");let shared={adj:[[0,1],[1,2]],blocked:new Set([0,1])},m=matching(shared.adj,shared.blocked);assert(!m.ok,"selector multiplicity counterexample");
 return {result,refusals,counterexamples:{sameBlockedCount:{adj:H,blocked0:a,blocked1:b},oneSelectorTwoBins:{adj:shared.adj,blockerSets:[[0,1]],matching:m}}}
}

// Load pinned check.js, nonlinear-shell.js, cactus-shell.js; call blindRun(cactusData,commonData,corpus).
