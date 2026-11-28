function canon(c){return [...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)}

function dedup(F){let S=new Map();for(let c of F){c=canon(c);if(c.some(l=>c.includes(-l)))continue;S.set(c.join(","),c)}return [...S.values()]}

function vars(F){return [...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b)}

function up(F,g,M){let a=new Map();for(let l of g){let v=Math.abs(l),b=Number(l>0);if(a.has(v)&&a.get(v)!==b)return {a,dead:true};a.set(v,b)}for(;;){let changed=false;for(let c of F){let u=[],yes=false;M.scans++;if(M.scans+M.visits+M.extra>M.cap)throw Error("CAP");for(let l of c){M.visits++;let b=a.get(Math.abs(l));if(b===undefined)u.push(l);else if(b===Number(l>0)){yes=true;break}}if(yes)continue;if(!u.length)return{a,dead:true};if(u.length===1){a.set(Math.abs(u[0]),Number(u[0]>0));changed=true;M.pins++}}if(!changed)return {a,dead:false}}}

function meter(cap=3000000){return{cap,visits:0,scans:0,extra:0,pins:0,nodes:0,probes:0,peakRows:0}}

function search(F,M,seed=[],reverse=false){let V=vars(F);M.peakRows=Math.max(M.peakRows,F.length);function go(g){M.nodes++;let u=up(F,g,M);if(u.dead)return{tree:0};let a=u.a,m=new Map();for(let c of F){M.extra+=c.length;if(!c.some(l=>a.get(Math.abs(l))===Number(l>0)))for(let l of c)if(!a.has(Math.abs(l)))m.set(Math.abs(l),(m.get(Math.abs(l))||0)+1)}if(!m.size)return{model:V.map(v=>[v,a.get(v)??0])};let v=[...m].sort((a,b)=>b[1]-a[1]||(reverse?b[0]-a[0]:a[0]-b[0]))[0][0],q=[...a].map(([v,b])=>b?v:-v),a0=go([...q,-v]);if(a0.model)return a0;let a1=go([...q,v]);if(a1.model)return a1;return{tree:[v,a0.tree,a1.tree]}}return go(seed)}

function replay(F,T,M,g=[]){let u=up(F,g,M);M.nodes++;if(T===0){if(!u.dead)throw Error("false leaf");return}if(u.dead||!Array.isArray(T)||T.length!==3||u.a.has(T[0])||!vars(F).includes(T[0]))throw Error("bad split");let q=[...u.a].map(([v,b])=>b?v:-v);replay(F,T[1],M,[...q,-T[0]]);replay(F,T[2],M,[...q,T[0]])}

function modelOK(F,A){let a=new Map(A);return F.every(c=>c.some(l=>a.get(Math.abs(l))===Number(l>0)))}

function split(F,ix){let S=new Set(ix);if(S.size!==ix.length||ix.some(i=>!Number.isInteger(i)||i<0||i>=F.length))throw Error("split");let L=F.filter((_,i)=>!S.has(i)),R=F.filter((_,i)=>S.has(i)),V=new Set(vars(R)),boundary=vars(L).filter(v=>V.has(v));return {L,R,boundary}}

function blind(F){let ix=F.map((c,i)=>c.length<=2?i:-1).filter(i=>i>=0);if(ix.length)return ix;
 // Deterministic alternative: choose all clauses touching one low-occurrence variable, no peer advice.
 let V=vars(F),cnt=v=>F.reduce((s,c)=>s+Number(c.some(l=>Math.abs(l)===v)),0);
 let v=V.sort((a,b)=>cnt(a)-cnt(b)||a-b)[0];
 return F.map((c,i)=>c.some(l=>Math.abs(l)===v)?i:-1).filter(i=>i>=0)
}

function graphProject(R,B,M){
 // Complete exact width-two projection by Davis-Putnam elimination. Non-2CNF is refused.
 if(R.some(c=>c.length>2))return null;
 let F=dedup(R),steps=[];const Bset=new Set(B);
 for(let v of vars(F).filter(v=>!Bset.has(v))){let pos=F.filter(c=>c.includes(v)),neg=F.filter(c=>c.includes(-v)),others=F.filter(c=>!c.includes(v)&&!c.includes(-v)),add=[];
 for(let p of pos)for(let n of neg){M.extra++;let q=canon([...p.filter(x=>x!==v),...n.filter(x=>x!==-v)]);if(!q.some(l=>q.includes(-l)))add.push(q)}
 steps.push({v,pos:pos.length,neg:neg.length,added:add.length});F=dedup([...others,...add]);M.peakRows=Math.max(M.peakRows,F.length);if(M.extra>M.cap)throw Error("CAP")}
 return {F,steps}
}

function cut(R,B,word,M,maxw=2){let g=B.map(v=>word.get(v)?v:-v);if(!up(R,g,M).dead)return null;
 // Use all assumption subsets of width <=2; each accepted exclusion is checked from R alone.
 if(up(R,[],M).dead)return [];
 for(let i=0;i<g.length;i++){M.probes++;if(up(R,[g[i]],M).dead)return[-g[i]]}
 if(maxw>=2)for(let i=0;i<g.length;i++)for(let j=i+1;j<g.length;j++){M.probes++;if(up(R,[g[i],g[j]],M).dead)return canon([-g[i],-g[j]])}
 return null
}

function lazy(F,ix,cap=3000000,seedCuts=[],maxw=2){
 let {L,R,boundary}=split(F,ix),M=meter(cap),proof=[],cuts=[],seen=new Set(),modelCount=0,fullFallback=0;let root=up(F,[],M);if(root.dead)return{status:"UNSAT",M,cuts,tree:0,root:true};
 let base=[...L,...[...root.a].map(([v,b])=>[b?v:-v])]; // unit pins replayed separately
 for(let c of seedCuts){c=canon(c);if(c.some(l=>!boundary.includes(Math.abs(l)))||!up(R,c.map(l=>-l),M).dead)throw Error("invalid seed");if(!seen.has(c.join(","))){seen.add(c.join(","));cuts.push(c)}}
 let status="UNKNOWN",tree=null,witness=null;
 try{for(;;){let A=[...base,...cuts],q=search(A,M);if(q.tree!==undefined){status="UNSAT";tree=q.tree;break}modelCount++;
 let word=new Map(q.model);for(let v of boundary)if(!word.has(v))word.set(v,0);
 let pins=boundary.map(v=>word.get(v)?v:-v),u=up(R,pins,M),c=null;
 if(u.dead)c=cut(R,boundary,word,M,maxw);
 else{let z=search(R,M,pins);if(z.model){let a=new Map([...q.model,...z.model.filter(([v])=>!word.has(v))]);for(let v of vars(F))if(!a.has(v))a.set(v,0);witness=[...a];if(!modelOK(F,witness))throw Error("lift");status="SAT";break}
 // A wider region refutation isn't admissible as a narrow cut; refuse rather than silently enumerate.
 fullFallback++;break}
 if(c===null)break;if(seen.has(c.join(",")))throw Error("duplicate cut cannot exclude consumer model");seen.add(c.join(","));cuts.push(c);if(cuts.length>2*boundary.length*boundary.length+1)throw Error("credit");up([...base,...cuts],[],M); // restart unconditional closure after each cut
 }}catch(e){if(String(e).includes("CAP"))status="UNKNOWN_CAP";else throw e}
 return {status,M,cuts,tree,witness,rootPins:[...root.a],modelCount,fullFallback,boundary,ix}
}

function verifyLazy(F,q){let {L,R,boundary}=split(F,q.ix),M=meter(10000000);let u=up(F,[],M);if(JSON.stringify([...u.a])!==JSON.stringify(q.rootPins))throw Error("root pins");for(let c of q.cuts){if(c.length>2||c.some(l=>!boundary.includes(Math.abs(l)))||!up(R,c.map(l=>-l),M).dead)throw Error("cut")}
 if(q.status==="UNSAT"){if(q.root){if(!u.dead)throw Error("root");}else replay([...L,...q.rootPins.map(([v,b])=>[b?v:-v]),...q.cuts],q.tree,M)}else if(q.status==="SAT"&&!modelOK(F,q.witness))throw Error("witness");return M}

function eager(F,ix,cap=3000000){let M=meter(cap),{L,R,boundary}=split(F,ix),P=graphProject(R,boundary,M);if(!P)return{status:"REFUSED_NONBIJUNCTIVE",M};let q=search([...L,...P.F],M);if(q.tree!==undefined){let C=meter(10000000);replay([...L,...P.F],q.tree,C);return{status:"UNSAT",M,checker:C,rows:P.F.length,projection:P.steps}}return{status:"SAT_REQUIRES_LIFT",M,rows:P.F.length,projection:P.steps}}

function bruteSupport(F,B,M){let S=new Set(),V=vars(F);function go(g){let u=up(F,g,M);if(u.dead)return;let v=V.find(v=>!u.a.has(v));if(v===undefined){S.add(B.reduce((w,v,i)=>w+((u.a.get(v)??0)<<i),0));return}let q=[...u.a].map(([v,b])=>b?v:-v);go([...q,-v]);go([...q,v])}go([]);return [...S].sort((a,b)=>a-b)}

function baseline(F){let M=meter(),q=search(F,M),C=meter(10000000);if(q.tree!==undefined){replay(F,q.tree,C);return {status:"UNSAT",M,checker:C,tree:q.tree}}if(!modelOK(F,q.model))throw Error("baseline model");return{status:"SAT",M,model:q.model}}

function earlyAffine(F,M){ // Extract all exact local Boolean affine consequences from distinct clause scopes of width <=4.
 let groups=new Map(),eq=[],basis=new Map(),V=vars(F),index=new Map(V.map((v,i)=>[v,i]));
 for(let c of F){let s=vars([c]),k=s.join(",");if(!groups.has(k))groups.set(k,{s,F:[]});groups.get(k).F.push(c)}
 for(let {s,F:G} of groups.values()){if(s.length>4)continue;let rows=[];for(let w=0;w<2**s.length;w++){M.extra+=G.length;let a=new Map(s.map((v,i)=>[v,(w>>i)&1]));if(G.every(c=>c.some(l=>a.get(Math.abs(l))===Number(l>0))))rows.push(w)}if(!rows.length)return{dead:true,rank:basis.size};for(let mask=1;mask<2**s.length;mask++){let val=w=>{let t=0;for(let j=0;j<s.length;j++)t^=((mask>>j)&1)&((w>>j)&1);return t},b=val(rows[0]);M.extra+=rows.length;if(rows.every(w=>val(w)===b)){let z=BigInt(b)<<BigInt(V.length);for(let i=0;i<s.length;i++)if(mask>>i&1)z^=1n<<BigInt(index.get(s[i]));eq.push(z)}}}
 for(let z of eq){for(let i=0;i<V.length;i++)if((z>>BigInt(i))&1n){M.extra++;if(basis.has(i))z^=basis.get(i);else{basis.set(i,z);z=0n;break}}if(z!==0n)return{dead:true,rank:basis.size,equations:eq.length}}return{dead:false,rank:basis.size,equations:eq.length}
}

function miniLanes(F,cap=3000000){let V=vars(F),G=V.slice(0,3),guards=Array.from({length:5},(_,i)=>i<4?[(i&1)?G[0]:-G[0],(i&2)?G[1]:-G[1]]:[G[2]]);let rows=[];
 for(let g of guards){let M=meter(cap),u=up(F,g,M);let A=meter(cap),af=earlyAffine([...F,...g.map(l=>[l])],A),Q=meter(cap),bi=graphProject([...F.filter(c=>c.length<=2),...g.map(l=>[l])],[],Q),Z=meter(cap);
 let res=search(F,Z,g),ck=meter(10000000);if(res.tree!==undefined)replay(F,res.tree,ck,g);else if(!modelOK(F,res.model))throw Error("guard model");
 // Geometry: bounded private-variable elimination on complete incident buckets, width <=4, not arbitrary branching.
 let R=dedup([...F,...g.map(l=>[l])]),E=meter(cap),pivots=0;
 for(let v of vars(R)){let P=R.filter(c=>c.includes(v)),N=R.filter(c=>c.includes(-v)),all=[...P,...N],S=vars(all);if(S.length>4)continue;let out=[];for(let a of P)for(let b of N){E.extra++;let c=canon([...a.filter(l=>l!==v),...b.filter(l=>l!==-v)]);if(!c.some(l=>c.includes(-l)))out.push(c)}R=dedup([...R.filter(c=>!c.includes(v)&&!c.includes(-v)),...out]);pivots++;if(R.some(c=>!c.length))break}
 let geo=up(R,[],E).dead;
 rows.push({g,occupancy:{dead:u.dead,M},affine:{...af,M:A},bijunctive:{dead:bi.F.some(c=>!c.length),M:Q},geometry:{dead:geo,pivots,M:E},dag:{dead:res.tree!==undefined,M:Z,check:ck,tree:res.tree}})
 }let cover=0;for(let w=0;w<8;w++){let a=new Map(G.map((v,i)=>[v,w>>i&1]));if(rows.some(q=>q.dag.dead&&q.g.every(l=>a.get(Math.abs(l))===Number(l>0))))cover++}
 return{rows,coverage:cover,carrier:8}
}

function feedback(F,mode,cap=1000000,width=4,seed=91357){let M=meter(cap),root=up(F,[],M),a=new Map(vars(F).map(v=>[v,root.a.get(v)??((v^seed)&1)])),G=F.map(c=>c.slice()),learn=[],moves=0,ties=0,peak=G.length;let keys=new Set(G.map(c=>canon(c).join(",")));function fields(c,A){let k=0,s=0;for(let l of c){M.extra++;if(A.get(Math.abs(l))===Number(l>0)){k++;s+=l>0?1:-1}}return{k,km:k%3,sm:(s%3+3)%3}}
 function score(A){let f=G.map(c=>fields(c,A));return[f.filter(x=>x.k===0).length,f.filter(x=>x.k>0&&x.sm===0).length]}
 let status="UNKNOWN",tree=null,check=null;
 try{if(mode!=="base"){for(;;){let now=score(a),best=[];let min=now[0];for(let v of vars(G)){if(root.a.has(v))continue;let b=new Map(a);b.set(v,1-b.get(v));let s=score(b);if(s[0]<min){min=s[0];best=[[v,s,b]]}else if(s[0]===min&&min<now[0])best.push([v,s,b]);if(M.extra+M.visits+M.scans>M.cap)throw Error("CAP")}
 if(!best.length)break;best.sort((x,y)=>x[0]-y[0]);let ordinary=best[0][0];if(mode==="residue")best.sort((x,y)=>x[1][1]-y[1][1]||x[0]-y[0]);if(best[0][0]!==ordinary)ties++;a=best[0][2];moves++}
 // At plateau, learn replayable violated resolvents from break partners. Fixed one batch and width cap.
 let old=G.slice(),U=old.filter(c=>fields(c,a).k===0),S=old.filter(c=>fields(c,a).k===1);
 for(let c of U)for(let l of c)for(let d of S){M.extra++;if(!d.includes(-l)||a.get(Math.abs(l))===Number(l>0))continue;let e=canon([...c.filter(x=>x!==l),...d.filter(x=>x!==-l)]);if(e.length>width||e.some(x=>e.includes(-x))||keys.has(e.join(",")))continue;keys.add(e.join(","));G.push(e);learn.push({p:old.indexOf(c),q:old.indexOf(d),pivot:l,e});fields(e,a);peak=Math.max(peak,G.length);if(M.extra+M.visits+M.scans>M.cap)throw Error("CAP")}
 up(G,[],M)}
 let q=search(G,M);if(q.tree!==undefined){tree=q.tree;let C=meter(cap);for(let {p,q,pivot,e} of learn){let c=F[p],d=F[q];if(!c.includes(pivot)||!d.includes(-pivot)||JSON.stringify(canon([...c.filter(x=>x!==pivot),...d.filter(x=>x!==-pivot)]))!==JSON.stringify(e))throw Error("resolution check");C.extra+=c.length+d.length}replay(G,tree,C);check=C;status="UNSAT"}else{if(!modelOK(F,q.model))throw Error("feedback model");status="SAT"}
 }catch(e){if(String(e).includes("CAP"))status="UNKNOWN_CAP";else throw e}
 return{mode,width,status,M,check,moves,ties,learned:learn.length,peak,tree,proof:learn}
}
// Node.js replay: node lazy.js compile.js benchmarks.json registry.json native-chart.js certificate.json
const fs=require("node:fs"),crypto=require("node:crypto"),[cp,bp,rp,hp,qp]=process.argv.slice(2),read=p=>fs.readFileSync(p,"utf8"),cc=read(cp),pp=read(hp),sha=s=>crypto.createHash("sha256").update(s,"utf8").digest("hex"),enc=x=>JSON.stringify(x)+"\n",compile=Function(cc.slice(cc.indexOf("function compile"),cc.indexOf("function auditLocal"))+";return compile")(),H=Function(pp.slice(pp.indexOf("const enc="),pp.indexOf("const [bp,kp"))+";return {project,verifyProjection,adapter}")(),B=JSON.parse(read(bp)),R=JSON.parse(read(rp)),q=JSON.parse(read(qp)),e=R.instances.find(z=>z.instance_id===q.instance_id),x=B.instances.find(z=>"EB-"+z.id===e.alias),G=compile(x),s=enc(G.network);if(sha(s)!==e.sha256||s.length*8!==e.N_bits||sha(x.dimacs)!==e.source_cnf.sha256||sha(enc(G.source_map))!==e.source_map_sha256||q.guard_id!=="EMPTY"||q.residual_id!=="ROOT")throw Error("identity");let P=H.project(G.network),pv=H.verifyProjection(G.network,P),F=P.clauses,CH=sha(enc({anchor:P.anchor,clauses:P.clauses,raw:P.raw,cond:P.cond,steps:P.steps,final:P.final})),MH=sha(enc({root:P.root,phase:P.phase}));if(CH!==q.chartHash||MH!==q.mapHash||!P.raw.every(f=>f.a.every(w=>f.a.includes(w^(2**f.s.length-1)))))throw Error("map/gauge");let C=meter(10000000);replay(F,q.baselineTree,C);let out={projectionReplay:pv,baseline:C};if(q.lazy)out.lazy=verifyLazy(F,q.lazy);if(q.seeded)out.seeded=verifyLazy(F,q.seeded);console.log(JSON.stringify(out));
