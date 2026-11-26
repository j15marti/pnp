function audit(){
 const ck=(p,m)=>{if(!p)throw Error(m)};
 const ek=(u,v)=>u<v?`${u},${v}`:`${v},${u}`;
 function graph(E){E=E.map(([u,v])=>u<v?[u,v]:[v,u]);E.sort((a,b)=>a[0]-b[0]||a[1]-b[1]);const V=[...new Set(E.flat())].sort((a,b)=>a-b),A=new Map(V.map(v=>[v,[]])),idx=new Map();E.forEach(([u,v],i)=>{ck(u!==v&&!idx.has(ek(u,v)),"simple");idx.set(ek(u,v),i);A.get(u).push([v,i]);A.get(v).push([u,i]);});ck(V.every(v=>A.get(v).length===3),"cubic");return {E,V,A,idx};}
 function matchings(g){const out=[];function rec(V,M){if(!V.size){out.push(new Set(M));return;}const u=V.values().next().value;for(const [v,i] of g.A.get(u))if(V.has(v)){let W=new Set(V);W.delete(u);W.delete(v);rec(W,[...M,i]);}}rec(new Set(g.V),[]);return out;}
 function factor(g,M){const seen=new Set(),C=[];for(const s of g.V)if(!seen.has(s)){const c=[],edges=[];let u=s,p=-1;do{c.push(u);seen.add(u);const [v,i]=g.A.get(u).find(([v,i])=>v!==p&&!M.has(i));edges.push(i);p=u;u=v;}while(u!==s);C.push({v:c,e:edges});}return C;}
 function verifyM(g,M){ck(M.size*2===g.V.length&&g.V.every(v=>g.A.get(v).filter(([u,i])=>M.has(i)).length===1),"matching");}
 const odd=(g,M)=>factor(g,M).filter(c=>c.v.length%2).length;
 const cost=(g,M,x)=>g.E.reduce((a,[u,v],i)=>a+(!M.has(i)&&x.has(u)===x.has(v)?1:0),0);
 function optimalCuts(C){const out=[];function rec(i,x){if(i===C.length){out.push(new Set(x));return;}const c=C[i].v,k=c.length;for(let j=0;j<(k%2?k:1);j++){let S=new Set();for(let t=1;t<k;t+=2)S.add(c[(j+t)%k]);rec(i+1,[...x,...S]);if(i)rec(i+1,[...x,...c.filter(v=>!S.has(v))]);}}rec(0,[]);return out;}
 function evenColor(g,M){verifyM(g,M);const y=Array(g.E.length).fill(0);for(const c of factor(g,M)){ck(c.e.length%2===0,"even");c.e.forEach((e,j)=>y[e]=1+j%2);}ck(g.V.every(v=>new Set(g.A.get(v).map(([u,i])=>y[i])).size===3),"color lift");return y;}
 function parity(g,M,P,A,B){const adj=new Map(g.V.map(v=>[v,[]]));for(let i=0;i<g.E.length;i++){let a=M.has(i)?null:+!A.has(i),b=P.has(i)?null:+!B.has(i);if(a!==null&&b!==null&&a!==b)return false;let c=a??b;if(c!==null){const [u,v]=g.E[i];adj.get(u).push([v,c]);adj.get(v).push([u,c]);}}const x=new Map();for(const s of g.V)if(!x.has(s)){x.set(s,0);const q=[s];for(let k=0;k<q.length;k++){const u=q[k];for(const [v,c] of adj.get(u)){const z=x.get(u)^c;if(x.has(v)){if(x.get(v)!==z)return false;}else{x.set(v,z);q.push(v);}}}}return true;}
 const E="0,5 0,15 0,17 1,2 1,6 1,11 2,4 2,11 3,7 3,9 3,21 4,10 4,18 5,15 5,20 6,9 6,16 7,8 7,14 8,14 8,19 9,15 10,18 10,21 11,19 12,13 12,16 12,17 13,14 13,19 16,17 18,20 20,21".split(" ").map(e=>e.split(",").map(Number));
 const G=graph(E),M=new Set(G.E.map((_,i)=>i).filter(i=>Math.floor(2190811748/2**i)%2)),P=matchings(G),good=P.filter(p=>odd(G,p)===0),C=factor(G,M),X=optimalCuts(C),hist={};verifyM(G,M);ck(P.length===26&&good.length===7&&X.length===36,"trap sizes");
 for(const x of X){ck(cost(G,M,x)===2,"optimal cut");const c=Math.min(...good.map(p=>cost(G,p,x)));hist[c]=(hist[c]??0)+1;}
 ck(hist[4]===23&&hist[6]===12&&hist[8]===1,"trap histogram");let parityChecks=0,parityYes=0;
 const oddC=C.filter(c=>c.e.length%2);
 for(const p of good){const f=G.E.map((_,i)=>i).filter(i=>!p.has(i)),B=[new Set()];for(let i=0;i<f.length;i++)for(let j=i+1;j<f.length;j++)B.push(new Set([f[i],f[j]]));for(const a of oddC[0].e)for(const b of oddC[1].e)for(const d of B){parityChecks++;if(parity(G,M,p,new Set([a,b]),d))parityYes++;}}ck(parityYes===0,"independent parity test");
 function supports(g,p){ck(p.length>0,"nonempty");return g.E.every((e,i)=>p.some(m=>m.has(i))&&p.some(m=>!m.has(i)));}
 ck(supports(G,P),"all matching statuses");
 // Explicit C03 adapter: a=F_M, shortest path of length two in cycle quotient.
 const own=new Map();C.forEach((c,i)=>c.v.forEach(v=>own.set(v,i)));const oc=C.map((c,i)=>c.v.length%2?i:-1).filter(i=>i>=0),h=C.map((_,i)=>i).find(i=>!oc.includes(i)),Z=new Set();
 for(const o of oc){const i=[...M].find(i=>{const [u,v]=G.E[i];return (own.get(u)===o&&own.get(v)===h)||(own.get(v)===o&&own.get(u)===h);});ck(i!==undefined,"quotient path");Z.add(i);}
 ck(![...M].some(i=>{const [u,v]=G.E[i];return oc.includes(own.get(u))&&oc.includes(own.get(v))&&own.get(u)!==own.get(v);}),"no shorter path");
 const a=G.E.map((_,i)=>i).filter(i=>!M.has(i)),b=new Set([...M].filter(i=>!Z.has(i)));
 for(const c of C){let prev=0;for(let j=0;j<c.v.length;j++){const u=c.v[j],i=G.A.get(u).find(([v,i])=>M.has(i))[1];prev^=+b.has(i);if(prev)b.add(c.e[j]);}ck(prev===0,"flow closure");}
 ck(G.V.every(v=>G.A.get(v).filter(([u,i])=>b.has(i)).length%2===0),"b flow");ck(G.E.every((_,i)=>a.includes(i)||b.has(i)||Z.has(i)),"zero set");
 // Local exact costs, 3-port and 2-port caps of K3,3. Each local test counts seam and internal defects.
 function localTest(k){const cap=k===3?[[0,3],[0,4],[0,5],[1,3],[1,4],[1,5],[2,3],[2,4],[2,5]]:[[0,3],[0,4],[0,5],[1,3],[1,4],[1,5],[2,3],[2,4],[2,5]];
   const g=graph(cap),mp=matchings(g);let count=0,lifts=0;const inside=k===3?[1,2,3,4,5]:[0,1,2,3,4,5],seams=k===3?[3,4,5]:[0,3],internal=g.E.filter(([u,v])=>k===3?u!==0:ek(u,v)!=="0,3");
   function selected(p,j){return p.has(g.idx.get(k===3?ek(0,seams[j]):"0,3"));}
   function reduced(x,j,p){if(k===2)return selected(p,0)?0:+(x[0]===x[1]);return selected(p,j)?0:+(x[j]===x[3]);}
   for(let word=0;word<2**(inside.length+k);word++){const y=Object.fromEntries(inside.map((u,j)=>[u,(word>>j)&1])),x=Array.from({length:k},(_,j)=>(word>>(inside.length+j))&1);
     const center=k===3?+(x.reduce((a,b)=>a+b,0)<2):null;const r=[...x,center];
     for(const p of mp){const l=internal.reduce((s,[u,v])=>s+(!p.has(g.idx.get(ek(u,v)))&&y[u]===y[v]?1:0),0)+seams.reduce((s,u,j)=>s+(!selected(p,j)&&y[u]===x[j]?1:0),0);
       const rr=k===3?seams.reduce((s,u,j)=>s+reduced(r,j,p),0):reduced(r,0,p);ck(rr<=l,"simultaneous projection");count++;
     }
   }
   for(let w=0;w<2**(k+(k===3?1:0));w++){const x=Array.from({length:k+(k===3?1:0)},(_,j)=>(w>>j)&1);
    const y=Object.fromEntries(inside.map(u=>[u,k===3?(u>=3?x[3]:1-x[3]):(u<3?1-x[0]:x[0])]));
    for(const p of mp){const l=internal.reduce((s,[u,v])=>s+(!p.has(g.idx.get(ek(u,v)))&&y[u]===y[v]?1:0),0)+seams.reduce((s,u,j)=>s+(!selected(p,j)&&y[u]===x[j]?1:0),0);const rr=k===3?seams.reduce((s,u,j)=>s+reduced(x,j,p),0):reduced(x,0,p);ck(rr===l,"exact lift");lifts++;}
   }return {ports:k,projectionChecks:count,liftChecks:lifts};}
 const local=[localTest(2),localTest(3)];
 function expand(g,ms,x){const id=new Map(g.V.map((v,j)=>[v,5*j])),ports=new Map(),E=[];for(const v of g.V){const t=id.get(v);g.A.get(v).forEach(([u,i],j)=>ports.set(`${v}:${i}`,t+j));for(let j=0;j<3;j++)for(let k=3;k<5;k++)E.push([t+j,t+k]);}
  g.E.forEach(([u,v],i)=>E.push([ports.get(`${u}:${i}`),ports.get(`${v}:${i}`)]));const H=graph(E);
  const nm=ms.map(m=>{const p=new Set();for(const i of m){const[u,v]=g.E[i];p.add(H.idx.get(ek(ports.get(`${u}:${i}`),ports.get(`${v}:${i}`))));}for(const v of g.V){const t=id.get(v),other=g.A.get(v).map(([u,i])=>i).filter(i=>!m.has(i)).map(i=>ports.get(`${v}:${i}`));ck(other.length===2,"two leaves");other.forEach((u,j)=>p.add(H.idx.get(ek(u,t+3+j))));}verifyM(H,p);return p;});
  const nx=new Set();for(const v of g.V){const t=id.get(v);for(let j=0;j<5;j++)if(x.has(v)===(j<3))nx.add(t+j);}
  ms.forEach((m,i)=>{ck(cost(g,m,x)===cost(H,nm[i],nx),"scaled cost");ck(odd(g,m)===odd(H,nm[i]),"scaled oddness");});
  return {H,nm,nx};
 }
 // Blind discovery of a batch of K2,3 shores by twin neighborhoods; decline overlaps or non-simple caps.
 function blind(g){const twins=new Map();for(const v of g.V){const key=g.A.get(v).map(([u,i])=>u).sort((a,b)=>a-b).join(",");if(!twins.has(key))twins.set(key,[]);twins.get(key).push(v);}
   const groups=[],used=new Set();for(const [key,hubs] of twins){if(hubs.length!==2)continue;const leaves=key.split(",").map(Number),S=new Set([...hubs,...leaves]);if(S.size!==5||[...S].some(v=>used.has(v)))continue;const ext=leaves.map(v=>g.A.get(v).filter(([u,i])=>!S.has(u)).map(([u,i])=>u));if(ext.some(z=>z.length!==1)||new Set(ext.flat()).size!==3)continue;groups.push([...S]);for(const v of S)used.add(v);}
   if(!groups.length)return null;const map=new Map(g.V.map(v=>[v,v]));for(const S of groups)for(const v of S)map.set(v,Math.min(...S));const E=g.E.map(([u,v])=>[map.get(u),map.get(v)]).filter(([u,v])=>u!==v);
   try{return {g:graph(E),groups:groups.length,map};}catch(e){return null;}
 }
 function gp(n,k){const E=[];for(let i=0;i<n;i++){E.push([i,(i+1)%n],[i+n,(i+k)%n+n],[i,i+n]);}return graph(E);}
 const baseCases=[["trap",G,M,good[0]],["prism",gp(5,1)],["Petersen",gp(5,2)]],scaled=[];
 for(const [name,g0,m0,p0] of baseCases){const ps=matchings(g0),m=m0??ps.find(p=>odd(g0,p)===2)??ps[0],p=p0??ps.find(p=>odd(g0,p)===0);let x=optimalCuts(factor(g0,m))[0],g=g0,ms=p?[m,p]:[m],rows=[];
  for(let k=0;k<=3;k++){const f=ms.map(m=>odd(g,m)),c=ms.map(m=>cost(g,m,x));if(p)evenColor(g,ms[1]);let z=g,counts=[];for(let j=0;j<k;j++){const d=blind(z);ck(d!==null,"blind motif");counts.push(d.groups);z=d.g;}ck(z.V.length===g0.V.length,"blind size");const re=matchings(z);ck(re.some(p=>odd(z,p)===0)===!!p,"blind decision");rows.push({n:g.V.length,oddness:f,cost:c,blindGroups:counts,basePM:re.length,verifiedColor:!!p});if(k<3){const t=expand(g,ms,x);g=t.H;ms=t.nm;x=t.nx;}}
  scaled.push({name,rows});
 }
 // C03 FP20 identical h=4,d=3 graph and pinned phase-zero b, one zero st.
 const h0=4,d0=3,n0=2*h0*d0,s=n0,t=n0+1,E0=[],a0=[],b0=[];for(let i=0;i<h0;i++)for(let j=0;j<2*d0;j++){const e=[i*2*d0+j,i*2*d0+(j+1)%(2*d0)];E0.push(e);a0.push(e);if(j%2===0)b0.push(e);}for(let i=0;i<h0;i++)for(let j=0;j<d0;j++){let u=i*2*d0+d0+j,v=((i+1)%h0)*2*d0+j;if(i===h0-1&&j<2){for(const z of [u,v]){let e=[z,z%2===0?s:t];E0.push(e);b0.push(e);}}else{E0.push([u,v]);b0.push([u,v]);}}E0.push([s,t]);const g0=graph(E0),B0=new Set(b0.map(e=>g0.idx.get(ek(...e)))),A0=new Set(a0.map(e=>g0.idx.get(ek(...e)))),m00=new Set(g0.E.map((_,i)=>i).filter(i=>!B0.has(i)));verifyM(g0,m00);evenColor(g0,m00);ck(g0.V.every(v=>[A0,B0].every(f=>g0.A.get(v).filter(([u,i])=>f.has(i)).length%2===0)),"peer conserved");ck(g0.E.filter((_,i)=>!A0.has(i)&&!B0.has(i)).length===1,"peer zero");
 return {trap:{edges:G.E,oldMatching:[...M].map(i=>G.E[i]),cycleLengths:C.map(c=>c.v.length),matchings:P.length,evenMatchings:good.map(p=>[...p].map(i=>G.E[i])),optimalCuts:X.length,histogram:hist,parityChecks,parityYes,allMatchingStatuses:true},adapter:{a:a.map(i=>G.E[i]),b:[...b].map(i=>G.E[i]),zeros:[...Z].map(i=>G.E[i]),minimum:2},local,scaled,peer:{source:"FP20 h=4,d=3 phase0",vertices:g0.V.length,edges:g0.E,oldMatching:[...m00].map(i=>g0.E[i]),a:[...A0].map(i=>g0.E[i]),b:[...B0].map(i=>g0.E[i]),oddness:odd(g0,m00),verifiedColor:true}};
}
console.log(JSON.stringify(audit(),null,2));
