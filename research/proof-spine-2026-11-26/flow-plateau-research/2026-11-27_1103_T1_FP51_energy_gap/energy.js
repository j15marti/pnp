
// FP51 native energy threshold, exact min-sum projection and independent verification.
// Inputs: original native strict EB4 graph; no provenance map used by discovery.
function normal(G,independent=false){
 const P=G.types.length*4, roots=new Int32Array(P).fill(-1),sg=new Uint8Array(P);
 let cnt=0;
 if(!independent){
 const adj=Array.from({length:P},()=>[]);
 const edge=(a,b,s)=>{adj[a].push([b,s]);adj[b].push([a,s]);};
 for(const [a,b,s] of G.edges)edge(a,b,s);
 for(let v=0;v<G.types.length;v++)if(G.types[v]==="E")for(let j=1;j<4;j++)edge(4*v,4*v+j,0);
 for(let p=0;p<P;p++)if(roots[p]<0){let stack=[p];roots[p]=p;while(stack.length){let a=stack.pop();for(let [b,s] of adj[a]){cnt++;let z=sg[a]^s;if(roots[b]<0){roots[b]=p;sg[b]=z;stack.push(b)}else if(roots[b]!==p||sg[b]!==z)throw Error("inconsistent transport")}}}
 }else{
 const parent=Int32Array.from({length:P},(_,i)=>i),d=new Uint8Array(P);
 function find(x){let s=0,r=x;while(parent[r]!==r){s^=d[r];r=parent[r];cnt++}return [r,s]}
 function join(a,b,s){let [x,u]=find(a),[y,v]=find(b);if(x===y){if((u^v)!==s)throw Error("contradiction")}else if(x<y){parent[y]=x;d[y]=u^v^s}else{parent[x]=y;d[x]=u^v^s}}
 for(let v=0;v<G.types.length;v++)if(G.types[v]==="E")for(let j=1;j<4;j++)join(4*v,4*v+j,0);
 for(const [a,b,s] of G.edges)join(a,b,s);
 for(let p=0;p<P;p++){let [r,s]=find(p);roots[p]=r;sg[p]=s}
 }
 const counts=new Map(), B=[];
 for(let v=0;v<G.types.length;v++)if(G.types[v]==="B"){B.push(v);for(let j=0;j<4;j++){let r=roots[4*v+j];counts.set(r,(counts.get(r)||0)+1)}}
 const gauge=[...counts].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0]?.[0];
 const factors=[];
 for(let v of B){let ports=Array.from({length:4},(_,j)=>4*v+j),vs=[...new Set(ports.map(p=>roots[p]).filter(r=>r!==gauge))].sort((a,b)=>a-b),cost=[];
 for(let w=0;w<2**vs.length;w++){let sum=0;for(let p of ports){let r=roots[p];sum+=sg[p]^(r===gauge?0:(w>>vs.indexOf(r))&1)}cost.push(Number(sum!==2))}
 factors.push({vs,cost,ids:[v]})}
 return {roots,sg,gauge,factors,cnt,B};
}
const key=f=>f.vs.join(",");
function group(F){const M=new Map();for(let f of F){let k=key(f);if(!M.has(k))M.set(k,{vs:f.vs.slice(),cost:f.cost.slice(),ids:f.ids.slice()});else{let q=M.get(k);q.cost=q.cost.map((x,i)=>x+f.cost[i]);q.ids.push(...f.ids)}}return [...M.values()]}
function union(F){return [...new Set(F.flatMap(f=>f.vs))].sort((a,b)=>a-b)}
function index(vs,U,w){return vs.reduce((z,v,i)=>z|(((w>>U.indexOf(v))&1)<<i),0)}
function reduce(n,cap=2000000){
 let F=group(n.factors),trace=[],scans=0,rows=0,maxWidth=0,peak=F.reduce((s,f)=>s+f.cost.length,0);
 for(;;){let occ=new Map();for(let f of F)for(let v of f.vs){scans++;if(scans>cap)return {F,trace,scans,rows,maxWidth,peak,stopped:true};if(!occ.has(v))occ.set(v,[]);occ.get(v).push(f)}
 let opts=[];for(let [v,fs] of occ)if(fs.length<=2){let S=union(fs).filter(x=>x!==v);if(S.length<=8)opts.push({v,fs,S})}
 if(!opts.length)break;opts.sort((a,b)=>a.S.length-b.S.length||a.v-b.v);let {v,fs,S}=opts[0],U=[...S,v],cost=[],arg=[];
 for(let w=0;w<2**S.length;w++){let c=[0,1].map(b=>fs.reduce((s,f)=>{rows++;return s+f.cost[index(f.vs,U,w|(b<<S.length))]},0));cost.push(Math.min(...c));arg.push(Number(c[1]<c[0]))}
 let ids=fs.flatMap(f=>f.ids).sort((a,b)=>a-b);trace.push({v,S,cost,arg,ids});F=F.filter(f=>!fs.includes(f));F.push({vs:S,cost,ids});F=group(F);maxWidth=Math.max(maxWidth,S.length);peak=Math.max(peak,F.reduce((s,f)=>s+f.cost.length,0));
 }
 return {F,trace,scans,rows,maxWidth,peak,stopped:false}
}
function replay(n,trace){
 let F=group(n.factors),rows=0,scans=0;
 for(let t of trace){scans+=F.length;let fs=F.filter(f=>f.vs.includes(t.v)),U=union(fs),S=U.filter(x=>x!==t.v);
 if(!fs.length||JSON.stringify(S)!==JSON.stringify(t.S)||JSON.stringify(fs.flatMap(f=>f.ids).sort((a,b)=>a-b))!==JSON.stringify(t.ids))throw Error("owner/scope mismatch");
 const c=Array(2**S.length).fill(Infinity),arg=Array(c.length).fill(-1);
 for(let w=0;w<2**U.length;w++){let z=0;for(let f of fs){rows++;z+=f.cost[index(f.vs,U,w)]}let q=index(S,U,w),b=(w>>U.indexOf(t.v))&1;if(z<c[q]||(z===c[q]&&b<arg[q])){c[q]=z;arg[q]=b}}
 if(JSON.stringify(c)!==JSON.stringify(t.cost)||JSON.stringify(arg)!==JSON.stringify(t.arg))throw Error("row mismatch");
 F=group([...F.filter(f=>!fs.includes(f)),{vs:S,cost:c,ids:t.ids}]);
 }
 return {F,rows,scans}
}
function asCNF(F){let clauses=[],owner=[];for(let f of F)for(let w=0;w<f.cost.length;w++)if(f.cost[w]>0){clauses.push(f.vs.map((v,i)=>((w>>i)&1)?-(v+1):v+1));owner.push(f.ids)}return {clauses,owner}}
function proofSearch(C,limit=2000000){
 let scans=0,lits=0,nodes=0;
 function close(A){A=new Map(A);while(true){let change=false,score=new Map();for(let c of C){if(++scans>limit)throw Error("cap");let open=[],sat=false;for(let l of c){lits++;let x=A.get(Math.abs(l));if(x===undefined)open.push(l);else if(x===Number(l>0)){sat=true;break}}if(sat)continue;if(!open.length)return {dead:true};if(open.length===1){A.set(Math.abs(open[0]),Number(open[0]>0));change=true}else for(let l of open)score.set(Math.abs(l),(score.get(Math.abs(l))||0)+1)}if(!change)return {A,score}}}
 function visit(A){nodes++;let x=close(A);if(x.dead)return null;if(!x.score.size)throw Error("zero witness");let v=[...x.score].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];return [v,visit([...x.A,[v,0]]),visit([...x.A,[v,1]])]}
 try{return {status:"UNSAT",tree:visit([]),scans,lits,nodes}}catch(e){return {status:e.message==="cap"?"UNKNOWN":e.message,scans,lits,nodes}}
}
// independent support-row tree replay, not clause unit-propagation code.
function checkTree(F,tree,limit=2500000){let rows=0,nodes=0;
 function close(A){A=new Map(A);for(;;){let change=false;for(let f of F){let good=[];for(let w=0;w<f.cost.length;w++){if(++rows>limit)throw Error("check cap");if(f.cost[w]===0&&f.vs.every((v,i)=>!A.has(v)||A.get(v)===((w>>i)&1)))good.push(w)}if(!good.length)return null;for(let [i,v] of f.vs.entries())if(!A.has(v)&&good.every(w=>((w>>i)&1)===((good[0]>>i)&1))){A.set(v,(good[0]>>i)&1);change=true}}if(!change)return A}}
 function visit(A,t){nodes++;let q=close(A);if(t===null){if(q!==null)throw Error("false leaf");return}if(!q||q.has(t[0]-1))throw Error("bad split");visit([...q,[t[0]-1,0]],t[1]);visit([...q,[t[0]-1,1]],t[2])}
 visit([],tree);return {nodes,rows}
}
// Source-only min-energy witness search. All costs evaluated, deterministic seed and capped work.
function witness(F,limit=2000000,target=2,seed=137){
 let V=union(F),at=new Map(V.map((v,i)=>[v,i])),local=F.map(f=>({cost:f.cost,idx:f.vs.map(v=>at.get(v))})),inc=V.map(()=>[]);
 local.forEach((f,i)=>f.idx.forEach(j=>inc[j].push(i)));
 let R=seed>>>0,rand=n=>{R=(Math.imul(R,1664525)+1013904223)>>>0;return (R>>>8)%n};
 let visits=0,best=Infinity,bestA,steps=0,restarts=0;
 const score=(i,A)=>{visits++;let f=local[i],w=f.idx.reduce((s,j,k)=>s|(A[j]<<k),0);return f.cost[w]};
 outer:while(visits<limit){restarts++;let A=V.map(()=>rand(2)),C=local.map((_,i)=>score(i,A)),e=C.reduce((a,b)=>a+b,0);
 for(let t=0;t<10000&&visits<limit;t++){steps++;if(e<best){best=e;bestA=A.slice()}if(e<=target)break outer;let bad=[];for(let i=0;i<C.length;i++)if(C[i]>0&&local[i].idx.length)bad.push(i);if(!bad.length)break;let f=local[bad[rand(bad.length)]],opts=[];
 for(let j of f.idx){A[j]^=1;let d=inc[j].reduce((s,i)=>s+score(i,A)-C[i],0);A[j]^=1;opts.push([j,d])}
 let j;if(rand(100)<22)j=f.idx[rand(f.idx.length)];else{let d=Math.min(...opts.map(o=>o[1])),q=opts.filter(o=>o[1]===d);j=q[rand(q.length)][0]}
 A[j]^=1;for(let i of inc[j]){let q=score(i,A);e+=q-C[i];C[i]=q}
 }}
 return {best,assignment:V.map((v,i)=>[v,bestA[i]]),visits,steps,restarts,seed}
}
function lift(G,n,trace,W){let A=new Map(W.assignment);A.set(n.gauge,0);for(let t of trace.slice().reverse()){let w=t.S.reduce((s,v,i)=>s|((A.get(v)||0)<<i),0);A.set(t.v,t.arg[w])}
 let bit=p=>(A.get(n.roots[p])||0)^n.sg[p],defects=[];
 for(let [a,b,s] of G.edges)if((bit(a)^bit(b))!==s)throw Error("bad lift edge");
 for(let v=0;v<G.types.length;v++){let a=[0,1,2,3].map(j=>bit(4*v+j));if(G.types[v]==="E"){if(a.some(x=>x!==a[0]))throw Error("bad lift E")}else if(a.reduce((s,x)=>s+x,0)!==2)defects.push(v)}
 if(defects.length!==W.best)throw Error("bad lift cost");
 return {defects,assignment:[...A].sort((a,b)=>a[0]-b[0]),ports:4*G.types.length,edges:G.edges.length}
}
function cnfWitness(instance,limit=1000000){let F=instance.dimacs.trimEnd().split("\n").slice(1).map(line=>{let ls=line.trim().split(/\s+/).map(Number).slice(0,-1),vs=[...new Set(ls.map(l=>Math.abs(l)-1))].sort((a,b)=>a-b),cost=Array.from({length:2**vs.length},(_,w)=>2*Number(!ls.some(l=>((w>>vs.indexOf(Math.abs(l)-1))&1)===Number(l>0))));return {vs,cost,ids:[]}});let s=proofSearch(asCNF(F).clauses,limit);let w=witness(F,limit,2);return {s,w}}
function run(G){let n=normal(G),a=reduce(n),n2=normal(G,true);if(n.gauge!==n2.gauge||n.roots.some((v,i)=>v!==n2.roots[i]||n.sg[i]!==n2.sg[i]))throw Error("normalization mismatch");let q=replay(n2,a.trace);if(JSON.stringify(q.F)!==JSON.stringify(a.F))throw Error("residual mismatch");
 let s=proofSearch(asCNF(a.F).clauses),c=s.status==="UNSAT"?checkTree(q.F,s.tree):null;let w=witness(a.F),L=lift(G,n,a.trace,w);let even=a.F.every(f=>f.cost.every(z=>z%2===0));if(even&&!n.factors.length)throw Error("empty source");
 return {gauge:n.gauge,normalization:{bfs:n.cnt,dsu:n2.cnt,B:n.B.length,roots:new Set(n.roots).size},chart:a,replay:{rows:q.rows,scans:q.scans},zero:s,check:c,even,witness:w,lift:L,remainingVariables:union(a.F).length}
}

if(typeof module!=="undefined")module.exports={run,cnfWitness,normal,reduce,checkTree,replay,proofSearch,asCNF,witness,lift};
