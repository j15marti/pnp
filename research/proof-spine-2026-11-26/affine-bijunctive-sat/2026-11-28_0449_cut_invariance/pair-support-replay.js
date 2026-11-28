function sha(s){const p=[],h=[],k=[];for(let i=2;k.length<64;i++){if(p.some(q=>i%q===0))continue;p.push(i);if(h.length<8)h.push((Math.sqrt(i)%1*4294967296)|0);k.push((Math.cbrt(i)%1*4294967296)|0)}const a=Array.from(s,c=>c.charCodeAt(0));if(a.some(x=>x>127))throw Error("ASCII");const l=a.length*8;a.push(128);while(a.length%64!==56)a.push(0);for(let j=7;j>=0;j--)a.push(Math.floor(l/2**(8*j))%256);const R=(x,n)=>(x>>>n)|(x<<(32-n));for(let i=0;i<a.length;i+=64){let w=[];for(let j=0;j<16;j++)w.push((a[i+4*j]<<24)|(a[i+4*j+1]<<16)|(a[i+4*j+2]<<8)|a[i+4*j+3]);for(let j=16;j<64;j++){let x=w[j-15],y=w[j-2];w[j]=(w[j-16]+(R(x,7)^R(x,18)^(x>>>3))+w[j-7]+(R(y,17)^R(y,19)^(y>>>10)))|0}let [A,B,C,D,E,F,G,H]=h;for(let j=0;j<64;j++){let t=(H+(R(E,6)^R(E,11)^R(E,25))+((E&F)^(~E&G))+k[j]+w[j])|0,u=((R(A,2)^R(A,13)^R(A,22))+((A&B)^(A&C)^(B&C)))|0;[A,B,C,D,E,F,G,H]=[(t+u)|0,A,B,C,(D+t)|0,E,F,G]}[A,B,C,D,E,F,G,H].forEach((v,j)=>h[j]=(h[j]+v)|0)}return h.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("")}

function compile(instance){
 const lines=instance.dimacs.trimEnd().split("\n"),h=lines.shift().split(" ").map((s,i)=>i>=2?Number(s):s);
 if(h[0]!=="p"||h[1]!=="cnf"||h[2]!==instance.nvars||h[3]!==lines.length)throw Error("header");
 const n=instance.nvars,F=[],parents=[];let next=n;
 const add=(a,id)=>{F.push(a);parents.push(id)};
 lines.forEach((line,i)=>{const a=line.split(/\s+/).map(Number);if(a.pop()!==0||a.some(l=>!Number.isInteger(l)||!l||Math.abs(l)>n))throw Error("bad clause");const id=i+1;if(a.length===0){let v=++next;add([v,v,v],id);add([-v,-v,-v],id)}else if(a.length<=3){while(a.length<3)a.push(a[a.length-1]);add(a,id)}else{let prev=++next;add([a[0],a[1],prev],id);for(let j=2;j<a.length-2;j++){let t=++next;add([-prev,a[j],t],id);prev=t}add([-prev,a[a.length-2],a[a.length-1]],id)}});
 const types=[],used=[],edges=[],groups=new Map(),reps={},owners=[];
 const V=(t,owner)=>{types.push(t);used.push(0);owners.push(owner);return types.length-1};
 const P=v=>{if(used[v]>=4)throw Error("port overflow");return 4*v+used[v]++};
 const E=(a,b,s=0)=>edges.push([a,b,s]);
 const wire=(a,b,s)=>{const v=Array.from({length:5},()=>V("E",["wire",a,b]));for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(i!==0||j!==1)E(P(v[i]),P(v[j]));E(a,P(v[0]),s);E(b,P(v[1]),0)};
 const occ=(id,s,p)=>{if(!groups.has(id))groups.set(id,[]);groups.get(id).push([p,s])};
 F.forEach(([a,b,c],i)=>{const L=x=>["x"+Math.abs(x),Number(x<0)],z="z"+i,T=[[L(a),L(b),[z,0]],[[z,1],L(c),["f",0]]];for(let j=0;j<2;j++)for(let k=0;k<2;k++){let v=V("B",["clause",parents[i],i,j,k]);for(const [id,s] of T[j])occ(id,s,P(v));occ("w"+i+"_"+j,0,P(v))}});
 for(const [id,O] of groups){if(O.length%2||O.length<2)throw Error("occurrence parity");reps[id]=O[0];if(O.length===2){wire(O[0][0],O[1][0],O[0][1]^O[1][1]);continue}const a=Array.from({length:(O.length-2)/2},()=>V("E",["carrier",id]));for(let i=1;i<a.length;i++)wire(P(a[i-1]),P(a[i]),0);let k=0;for(const v of a)while(used[v]<4){const [p,s]=O[k++];wire(P(v),p,s)}if(k!==O.length)throw Error("fanout")}
 const seen=new Set(),ports=new Set();for(const [a,b,s] of edges){let u=Math.floor(a/4),v=Math.floor(b/4),key=Math.min(u,v)+":"+Math.max(u,v);if(u===v||seen.has(key)||ports.has(a)||ports.has(b)||![0,1].includes(s))throw Error("not simple signed 4-regular");seen.add(key);ports.add(a);ports.add(b)}
 if(used.some(x=>x!==4)||ports.size!==4*types.length)throw Error("degree");
 return {network:{format:"STRICT-EB4-v1",types,edges},source_map:{original_n:n,ternary_clauses:F,original_clause_ids:parents,representative_ports:reps,vertex_provenance:owners}};
}

function run(g,project){
 const counts={union:0,ge:0,words:0,clauseTests:0,reach:0,checks:0};const clock=()=>Object.values(counts).reduce((a,b)=>a+b,0),cap=30000000;
 const bit=i=>1n<<BigInt(i+1),low=x=>x&-x,par=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
 function reduce(B,x){let y=0n;while(x&~1n){counts.ge++;let p=low(x&~1n);if(B.has(p))x^=B.get(p);else{y^=p;x^=p}}return y^x}
 function ins(B,x){x=reduce(B,x);if(x===1n)return -1;if(!x)return 0;B.set(low(x&~1n),x);return 1}
 function solve(B){let x=0n;for(const [p,r] of [...B].sort((a,b)=>a[0]>b[0]?-1:1))if(par(r&x)^Number(r&1n))x|=p;return x}
 const evalf=(f,x)=>par(f&x)^Number(f&1n);
 let np=g.types.length*4,pa=Array.from({length:np},(_,i)=>i),sz=Array(np).fill(1),sg=Array(np).fill(0);
 function find(x){let s=0;while(pa[x]!==x){counts.union++;s^=sg[x];x=pa[x]}return [x,s]}
 function join(a,b,s){counts.union++;let [u,x]=find(a),[v,y]=find(b);if(u===v)return (x^y)===s;if(sz[u]<sz[v])[u,v]=[v,u];pa[v]=u;sg[v]=s^x^y;sz[u]+=sz[v];return true}
 const finish=(decision,reason,rest={})=>({decision,reason,counts,...rest});
 for(const [a,b,s] of g.edges)if(!join(a,b,s))return finish("NO","edge contradiction");
 for(let i=0;i<g.types.length;i++)if(g.types[i]==="E")for(let j=1;j<4;j++)if(!join(4*i,4*i+j,0))return finish("NO","E contradiction");
 const ids=new Map(),port=pa.map((_,i)=>{let [r,s]=find(i);if(!ids.has(r))ids.set(r,ids.size);return bit(ids.get(r))^BigInt(s)});
 const A=new Map(),B=[];for(let i=0;i<g.types.length;i++)if(g.types[i]==="B"){let [a,b,c,d]=port.slice(4*i,4*i+4);B.push([a^b,a^c]);if(ins(A,a^b^c^d)<0)return finish("NO","parity contradiction")}
 let parityRank=A.size,early=0,pairs;
 for(;;){pairs=[];let change=false;for(const [p0,q0] of B){let p=reduce(A,p0),q=reduce(A,q0);if(p===1n||q===1n||(p^q)===1n)continue;if(!p&&!q)return finish("NO","all equal",{parityRank,early});if(!p||!q||p===q){let z=ins(A,(p||q)^1n);if(z<0)return finish("NO","forced conflict");if(z){early++;change=true}}else pairs.push([p,q])}if(!change)break}
 spectralLog.push(spectral(g,port,A,reduce));
 const forms=[...new Set(pairs.flat())],idx=new Map(forms.map((f,i)=>[f,i])),adj=forms.map(()=>[]);for(const [a,b] of pairs){adj[idx.get(a)].push(idx.get(b));adj[idx.get(b)].push(idx.get(a))}
 const groups=[],seen=new Set();for(let i=0;i<forms.length;i++){if(seen.has(i))continue;let Q=[i];seen.add(i);for(const j of Q)for(const k of adj[j])if(!seen.has(k)){seen.add(k);Q.push(k)}groups.push(Q)}
 // Source-only bounded cross-block fusion using original affine coordinate support.
 const beforeGroups=groups.length, mergeLog=[];
 if(project===2){
  const of=new Map();groups.forEach((G,i)=>G.forEach(j=>of.set(j,i)));
  const supports=new Map();
  forms.forEach((f,i)=>{for(let v=f&~1n;v;v&=v-1n){counts.ge++;let p=low(v);if(!supports.has(p))supports.set(p,new Set());supports.get(p).add(of.get(i))}});
  const gp=groups.map((_,i)=>i),sz=groups.map(g=>g.length);function gr(i){while(gp[i]!==i)i=gp[i];return i}
  for(const [p,ss] of [...supports].sort((a,b)=>a[1].size-b[1].size||(a[0]<b[0]?-1:1))){
   if(ss.size<2||ss.size>3)continue;let a=[...new Set([...ss].map(gr))];if(a.length<2||a.reduce((s,i)=>s+sz[i],0)>8)continue;
   const j=a[0];for(const k of a.slice(1)){gp[k]=j;sz[j]+=sz[k]}mergeLog.push([p.toString(16),[...ss]]);
  }
  const gg=new Map();groups.forEach((G,i)=>{let j=gr(i);if(!gg.has(j))gg.set(j,[]);gg.get(j).push(...G)});groups.splice(0,groups.length,...gg.values());
 }
 const initialRank=A.size,allSpan=new Map();for(const f of forms)ins(allSpan,f&~1n);
 const fullRank=allSpan.size,regions=[],privateRows=[],hist={},projectedHist={};
 // Independent local consistency checker: build the actual global affine equations for each local word.
 function legal(F,w){const T=new Map();for(let i=0;i<F.length;i++)if(ins(T,F[i]^BigInt(w>>i&1))<0)return false;return true}
 function xorMask(F,mask){let f=0n;for(let i=0;i<F.length;i++)if(mask>>i&1)f^=F[i];return f}
 for(const G of groups){
  if(G.length>12||clock()>cap)return finish("UNKNOWN","block/cost cap",{early,parityRank});
  let F=G.map(i=>forms[i]),local=new Map(G.map((j,i)=>[j,i])),E=[];for(const j of G)for(const k of adj[j])if(j<k)E.push([local.get(j),local.get(k)]);
  let allowed=[];for(let w=0;w<2**F.length;w++){counts.words++;if(E.every(([i,j])=>(w>>i&1)||(w>>j&1))&&legal(F,w))allowed.push(w)}
  if(!allowed.length)return finish("NO","local empty",{early,parityRank});
  const L=new Map();for(const f of F)ins(L,f&~1n);
  let masks=[],S=[];
  if(project){
   const outside=new Map(),members=new Set(G);for(let i=0;i<forms.length;i++)if(!members.has(i))ins(outside,forms[i]&~1n);
   const Q=new Map(),shared=new Map();
   for(let i=0;i<F.length;i++){let r=reduce(outside,F[i]&~1n),c=1<<i;while(r){let p=low(r);counts.ge++;if(!Q.has(p)){Q.set(p,[r,c]);break}let [v,d]=Q.get(p);r^=v;c^=d}if(!r){let f=xorMask(F,c);if(ins(shared,f&~1n)>0){masks.push(c);S.push(f)}}}
   if(S.length!==L.size-Q.size)throw Error("intersection dimension");
   for(const s of S)if(reduce(outside,s&~1n))throw Error("intersection witness");
   // Check quotient complement and shared span against each block using separate rank calculation.
   let U=new Map(outside),increment=0;for(const f of F)if(ins(U,f&~1n)>0)increment++;
   if(increment!==L.size-S.length)throw Error("rank check");
   privateRows.push(increment);
  }else{masks=F.map((_,i)=>1<<i);S=F;privateRows.push(0)}
  const response=new Map();for(const w of allowed){let u=0;masks.forEach((m,i)=>{if(par(BigInt(w&m)))u|=1<<i});if(!response.has(u))response.set(u,w)}
  // Recompute exact projection image independently via scan of every possible output.
  for(let u=0;u<2**S.length;u++){counts.checks++;let ok=allowed.some(w=>masks.every((m,i)=>par(BigInt(w&m))===(u>>i&1)));if(ok!==response.has(u))throw Error("projection")}
  regions.push({F,S,masks,response,allowed});
  hist[F.length]=(hist[F.length]||0)+1;projectedHist[S.length]=(projectedHist[S.length]||0)+1;
 }
 const S=[...new Set(regions.flatMap(r=>r.S))], sid=new Map(S.map((f,i)=>[f,i])),SS=new Map();for(const f of S)ins(SS,f&~1n);
 const privateRank=privateRows.reduce((a,b)=>a+b,0);
 if(project&&privateRank+SS.size!==fullRank)throw Error("joint rank recomposition");
 const fixed=S.length,arcs=new Set(),proof=[],rounds=[];
 const addArc=(a,b)=>{let k=a*(2*fixed)+b;if(!arcs.has(k)){arcs.add(k);return 1}return 0};
 const addClause=(a,b)=>addArc(a^1,b)+addArc(b^1,a); // node 2i+v means form i = v.
 let stat={carriers:ids.size,balance:B.length,early,parityRank,forms:forms.length,fullRank,blocks:groups.length,beforeGroups,mergeCount:mergeLog.length,hist,projectedHist,sharedForms:fixed,sharedRank:SS.size,privateRank,rowsBefore:regions.reduce((a,r)=>a+r.allowed.length,0),rowsAfter:regions.reduce((a,r)=>a+r.response.size,0)};
 if(project===2) captures.push(audit(regions,forms,pairs,A,port,stat));
 for(let round=0;round<=ids.size+4*fixed*fixed+1;round++){
  if(clock()>cap)return finish("UNKNOWN","cost cap",{...stat,rounds});
  let oldRank=A.size,oldArcs=arcs.size,live=[];
  for(let bi=0;bi<regions.length;bi++){
   let r=regions[bi],F=r.S.map(f=>reduce(A,f)),W=[...r.response.keys()].filter(w=>{counts.words++;return legal(F,w)});live.push(W);
   if(!W.length)return finish("NO","empty filtered block",{...stat,rounds,proof});
   // Exhaustive affine equations in the bounded local scope.
   for(let m=1;m<2**F.length;m++){let v=par(BigInt(m&W[0]));counts.words++;if(W.every(w=>par(BigInt(w&m))===v)){let row=xorMask(r.S,m)^BigInt(v),z=ins(A,row);if(z<0)return finish("NO","affine conflict",{...stat,rounds,proof});if(z)proof.push(["block",bi,m,v]);}}
   for(let i=0;i<r.S.length;i++)for(let j=i;j<r.S.length;j++)for(let a=0;a<2;a++)for(let b=0;b<2;b++){counts.clauseTests++;if(!W.some(w=>(w>>i&1)===a&&(w>>j&1)===b))addClause(2*sid.get(r.S[i])+(1-a),2*sid.get(r.S[j])+(1-b))}
  }
  const canon=new Map();for(let i=0;i<fixed;i++){
   let f=reduce(A,S[i]);if(f===0n||f===1n){let a=2*i+Number(f);addClause(a,a)}
   else {let k=f&~1n;if(canon.has(k)){let [j,s]=canon.get(k),d=Number(f&1n)^s;for(let v=0;v<2;v++){addArc(2*i+v,2*j+(v^d));addArc(2*j+(v^d),2*i+v)}}else canon.set(k,[i,Number(f&1n)])}
  }
  const G=Array.from({length:2*fixed},()=>[]);for(const e of arcs)G[Math.floor(e/(2*fixed))].push(e%(2*fixed));
  const reach=[];for(let i=0;i<G.length;i++){let V=new Set([i]),Q=[i];for(const j of Q)for(const k of G[j]){counts.reach++;if(!V.has(k)){V.add(k);Q.push(k)}}reach.push(V)}
  for(let i=0;i<fixed;i++){
   const a=reach[2*i].has(2*i+1),b=reach[2*i+1].has(2*i);if(a&&b)return finish("NO","implication contradiction",{...stat,rounds,proof});
   if(a||b){let z=ins(A,S[i]^BigInt(a));if(z<0)return finish("NO","implication-affine contradiction",{...stat,rounds,proof});if(z)proof.push(["unit",i,Number(a)])}
   for(const j of reach[2*i])if(j>2*i+1&&reach[j].has(2*i)){let z=ins(A,S[i]^S[j>>1]^BigInt(j&1));if(z<0)return finish("NO","SCC-affine contradiction",{...stat,rounds,proof});if(z)proof.push(["SCC",i,j])}
  }
  rounds.push({rankGain:A.size-oldRank,arcGain:arcs.size-oldArcs,rank:A.size,arcs:arcs.size,liveRows:live.reduce((a,b)=>a+b.length,0)});
  if(A.size===oldRank&&arcs.size===oldArcs)break;
 }
 // A candidate is never a YES without full native witness. Lift through all local representatives.
 // Exact bounded shared-rank terminal, not a SAT oracle. Enumerate a basis of shared forms.
 let X=solve(A);const accepts=x=>regions.every(r=>r.response.has(r.S.reduce((w,f,j)=>w|(evalf(f,x)<<j),0)));
 if(!accepts(X)){
  const K=new Map(),chosen=[];
  for(const f of S){let u=reduce(A,f)&~1n;if(ins(K,u)>0)chosen.push(f)}
  if(chosen.length<=12){
   let found=false;for(let w=0;w<2**chosen.length;w++){counts.words++;const U=new Map(A);let ok=true;for(let j=0;j<chosen.length;j++)if(ins(U,chosen[j]^BigInt(w>>j&1))<0){ok=false;break}if(ok){let x=solve(U);if(accepts(x)){X=x;found=true;break}}}
   if(!found)return finish("NO","exhausted shared rank",{...stat,rounds,proof,terminalRank:chosen.length});
  }
 }
 const T=new Map(A);
 for(let i=0;i<regions.length;i++){let r=regions[i],u=r.S.reduce((w,f,j)=>w|(evalf(f,X)<<j),0);if(!r.response.has(u))return finish("UNKNOWN","fixed point: candidate fails projected relation",{...stat,rounds,proof,rankBudget:ids.size-initialRank,arcBudget:4*fixed*fixed});
  let w=r.response.get(u);for(let j=0;j<r.F.length;j++)if(ins(T,r.F[j]^BigInt(w>>j&1))<0)throw Error("joint lift failed")}
 let x=solve(T),vals=port.map(f=>evalf(f,x));let verified=g.edges.every(([a,b,s])=>(vals[a]^vals[b])===s)&&g.types.every((t,i)=>{let a=vals.slice(4*i,4*i+4);return t==="E"?a.every(v=>v===a[0]):a.reduce((s,v)=>s+v,0)===2});
 if(!verified)throw Error("native witness");
 return finish("YES","lifted checked witness",{...stat,rounds,proof,witness:vals.join("")});
}

function audit(regions,forms,pairs,A,port,stat){
 let ops=0,words=0;const high=x=>x.toString(2).length-1;
 function put(B,x,tag=0n){while(x&~1n){ops++;let p=high(x);if(B.has(p)){let [y,t]=B.get(p);x^=y;tag^=t}else{B.set(p,[x,tag]);return [1,tag]}}return [x===1n?-1:0,tag]}
 function rank(F){let B=new Map();for(const f of F)put(B,f&~1n);return B}
 const universe=rank(forms),shared=rank(regions.flatMap(r=>r.S)),owner=new Map();regions.forEach((r,i)=>r.F.forEach(f=>{if(owner.has(f))throw Error("duplicate form");owner.set(f,i)}));if(owner.size!==forms.length||pairs.some(([a,b])=>owner.get(a)!==owner.get(b)))throw Error("partition");
 let removed=0;
 for(let i=0;i<regions.length;i++){let r=regions[i],O=rank(regions.flatMap((q,j)=>i===j?[]:q.F)),outside=O.size,L=rank(r.F).size,inter=rank(r.S).size;
  if(inter!==r.S.length)throw Error("dependent shared basis");for(const f of r.S)if(put(O,f&~1n)[0])throw Error("outside containment");
  for(const f of r.F)put(O,f&~1n);if(L+outside-O.size!==inter)throw Error("wrong intersection rank");removed+=L-inter;
  const local=new Map(r.F.map((f,j)=>[f,j])),E=pairs.filter(([a])=>owner.get(a)===i).map(([a,b])=>[local.get(a),local.get(b)]),allowed=[],response=new Map();
  for(let w=0;w<2**r.F.length;w++){words++;if(E.some(([a,b])=>!(w>>a&1)&&!(w>>b&1)))continue;let B=new Map(),ok=true;for(let j=0;j<r.F.length;j++)if(put(B,r.F[j]^BigInt(w>>j&1))[0]<0){ok=false;break}if(!ok)continue;
   allowed.push(w);let u=0;for(let j=0;j<r.masks.length;j++){let x=w&r.masks[j],p=0;while(x){x&=x-1;p^=1}u|=p<<j}if(!response.has(u))response.set(u,w);
  }
  if(JSON.stringify(allowed)!==JSON.stringify(r.allowed)||JSON.stringify([...response])!==JSON.stringify([...r.response]))throw Error("independent support mismatch");
  for(let j=0;j<r.S.length;j++){let f=0n;for(let k=0;k<r.F.length;k++)if(r.masks[j]>>k&1)f^=r.F[k];if(f!==r.S[j])throw Error("map mismatch")}
 }
 if(removed!==stat.privateRank||universe.size!==shared.size+removed)throw Error("global rank mismatch");
 // Build an explicit independent shared coordinate basis and express all boundary forms in it.
 const Q=new Map(),chosen=[];for(const r of regions)for(const f of r.S){let [z]=put(Q,f&~1n,1n<<BigInt(chosen.length));if(z>0)chosen.push(f&~1n)}
 function express(f){let tag=0n,x=f&~1n;while(x){ops++;let p=high(x);if(!Q.has(p))throw Error("outside shared span");let [v,t]=Q.get(p);x^=v;tag^=t}return [tag.toString(16),Number(f&1n)]}
 const hex=x=>x.toString(16);
 const residual={schema:"PRIVATE-SPAN-RELATIONS-v1",sharedDimension:chosen.length,regions:regions.map(r=>({forms:r.S.map(express),allowed:[...r.response.keys()]}))};
 const map={schema:"PRIVATE-SPAN-LIFT-v1",carrierCount:stat.carriers,affineRows:[...A.values()].map(hex),sharedBasis:chosen.map(hex),ports:port.map(f=>[high(f&~1n)-1,Number(f&1n)]),regions:regions.map(r=>({localForms:r.F.map(hex),boundaryForms:r.S.map(hex),masks:r.masks,representatives:[...r.response]}))};
 return {residual,map,ops,words,removed,sharedRank:shared.size};
}
const captures=[];

function checked(corpus,registry){
 const out=[];
 for(const id of ["JOINT-24","RANDOM-3CNF-40"]){const c=corpus.instances.find(x=>x.id===id),R=registry.instances.find(x=>x.source_cnf.alias===id),{network,source_map}=compile(c),raw=JSON.stringify(network)+"\n";if(sha(raw)!==R.sha256||raw.length*8!==R.N_bits||sha(c.dimacs)!==R.source_cnf.sha256||sha(JSON.stringify(source_map)+"\n")!==R.source_map_sha256)throw Error("auth");
 const result=run(network,2),a=captures.pop(),residualBytes=JSON.stringify(a.residual)+"\n",mapBytes=JSON.stringify(a.map)+"\n",resSha=sha(residualBytes),mapSha=sha(mapBytes),resid="RESIDUAL-v1:sha256:"+sha(JSON.stringify(["PNP-RESIDUAL-v1",R.instance_id,"EMPTY",a.residual.schema,resSha,mapSha])+"\n");
 const cert={problem_id:"STRICT-EB4-v1",instance:R.short_id,instance_id:R.instance_id,original_N_bits:R.N_bits,source_pin:{registry:"0c14cdc57925788cf7a451dcd5aa171dce860f2c",corpus:"e315349cd6c1fe3fa696504859f28312f6aab69a",compiler:"21b9d53fb8166c819b24e708656c742cd3c24f10"},guard_id:"EMPTY",residual_id:"ROOT",original_ids:{vertices:[0,R.vertices-1],ports:[0,4*R.vertices-1],edges:[0,R.edges-1]},parents:[],claim:"Exact existential projection onto shared coordinate space with simultaneous lifting; removes private span dimensions, not a decision certificate.",output_residual_id:resid,residual_sha256:resSha,map_sha256:mapSha,residual_bytes:residualBytes.length,map_bytes:mapBytes.length,independent_high_pivot_audit:{pivot_events:a.ops,local_words:a.words,privateRank:a.removed,sharedRank:a.sharedRank},discovery_counts:result.counts,source_rank:result.fullRank,projected_rank:result.sharedRank,decision:result.decision,checker:"audit() in checked-fused-span.js; deterministic residual/map bytes produced by checked(); code replays source normalization, exhaustive region tables and independent high-pivot rank checks. No peer imported."};
 out.push({cert,residual:a.residual,map:a.map});
 }return out;
}

function spectral(g,port,A,reduce){
 const n=new Set(port.map(p=>p&~1n)).size,rows=[],seen=new Set(); 
 const cols=new Map();port.forEach(p=>{let k=p&~1n;if(!cols.has(k))cols.set(k,cols.size)});
 for(let i=0;i<g.types.length;i++)if(g.types[i]==="B"){let R=new Map();for(let j=0;j<4;j++){let f=port[4*i+j],v=cols.get(f&~1n);R.set(v,(R.get(v)||0)+(f&1n?-1:1))}
 let r=[...R].filter(([v,k])=>k).sort((a,b)=>a[0]-b[0]);if(!r.length)continue;if(r[0][1]<0)r=r.map(([v,k])=>[v,-k]);let key=JSON.stringify(r);if(!seen.has(key)){seen.add(key);rows.push(r)}}
 const dot=(a,b)=>{let z=0;for(let [i,v] of a)for(let [j,w] of b)if(i===j)z+=v*w;return z};
 let facts=new Map(),stats={n,distinctRows:rows.length,rowPairs:0,overlappingPairs:0,tests:0,diagonalTests:0,newGE:0,zeroDiag:0,scope:"exact projector upper bound from spans of one or two original signed real rows; no full projector"};
 const rev=[...cols.keys()];
 function pass(a,b){let aa=dot(a,a),bb=b?dot(b,b):1,ab=b?dot(a,b):0,D=aa*bb-ab*ab;if(D<=0)return;
 let S=[...new Set([...a,...(b||[])].map(z=>z[0]))],am=new Map(a),bm=new Map(b||[]);
 function residual(i,j,t){let u=(am.get(i)||0)+(j===null?0:t*(am.get(j)||0)),v=(bm.get(i)||0)+(j===null?0:t*(bm.get(j)||0));return (j===null?1:2)*D-(bb*u*u-2*ab*u*v+aa*v*v)}
 for(let i=0;i<S.length;i++){let p=S[i];stats.diagonalTests++;if(n*residual(p,null,0)<D)stats.zeroDiag++;
 for(let j=i+1;j<S.length;j++)for(let t of [-1,1]){let q=S[j];stats.tests++;if(n*residual(p,q,t)<4*D){let key=[Math.min(p,q),Math.max(p,q),t].join(",");if(!facts.has(key)){let z=rev[p]^rev[q]^BigInt(t===1);facts.set(key,{p,q,t,alreadyGE:reduce(A,z)===0n});}}}
 }}
 for(let i=0;i<rows.length;i++){pass(rows[i],null);for(let j=i+1;j<rows.length;j++){stats.rowPairs++;if(!rows[i].some(([v])=>rows[j].some(([w])=>v===w)))continue;stats.overlappingPairs++;pass(rows[i],rows[j])}}
 stats.facts=[...facts.values()];stats.newGE=stats.facts.filter(f=>!f.alreadyGE).length;return stats;
}
function compare(x){
 let ops=0;
 const low=v=>v&-v;
 function put(B,v,hi=false){while(v){ops++;let p=hi?1n<<BigInt(v.toString(2).length-1):low(v);if(B.has(p))v^=B.get(p);else{B.set(p,v);return 1}}return 0}
 const orig=x.map.regions.map(r=>r.localForms.map(s=>BigInt("0x"+s)&~1n)),shared=x.map.regions.map(r=>r.boundaryForms.map(s=>BigInt("0x"+s)&~1n));
 function profile(blocks,order,hi){let n=order.length,l=[],r=[],B=new Map(),C=new Map();for(let i=0;i<n;i++){for(const v of blocks[order[i]])put(B,v,hi);l.push(B.size);for(const v of blocks[order[n-1-i]])put(C,v,hi);r[n-1-i]=C.size}return l.slice(0,-1).map((v,i)=>v+r[i+1]-B.size)}
 const n=orig.length,order=Array.from({length:n},(_,i)=>i);
 let before=profile(orig,order,false),after=profile(shared,order,true);if(JSON.stringify(before)!==JSON.stringify(after))throw Error("invariance source");
 const key=i=>{let m=shared[i].reduce((z,v)=>z|v,0n);return low(m)},sorted=order.slice().sort((i,j)=>key(i)<key(j)?-1:key(i)>key(j)?1:i-j);
 let sorted0=profile(orig,sorted,true),sorted1=profile(shared,sorted,false);if(JSON.stringify(sorted0)!==JSON.stringify(sorted1))throw Error("invariance sorted");
 const rankOps=ops, R=x.residual.regions.map(r=>({F:r.forms.map(([s,c])=>(BigInt("0x"+s)<<1n)|BigInt(c)),W:r.allowed.slice()})),A=new Map();
 const masks=R.map(r=>r.F.reduce((z,f)=>z|(f&~1n),0n));
 let stats={pairs:0,overlap:0,nonzeroIntersection:0,wordTrials:0,maskTests:0,maskWordTests:0,affineGain:0,rowsExcluded:0,cap:2000000,capped:false,proofs:[]};
 const par=z=>{let p=0;while(z){z&=z-1n;p^=1}return p};
 function reduce(B,v){let z=0n;while(v&~1n){ops++;let p=low(v&~1n);if(B.has(p))v^=B.get(p);else{v^=p;z^=p}}return z^v}
 function admit(B,v){v=reduce(B,v);if(v===1n)return -1;if(!v)return 0;B.set(low(v&~1n),v);return 1}
 const bases=R.map(r=>{let B=new Map();for(let f of r.F)put(B,f&~1n);return B});
 let contradiction=null;
 outer:for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){
  stats.pairs++;if(!(masks[i]&masks[j]))continue;stats.overlap++;
  let T=new Map(bases[i]);for(let f of R[j].F)put(T,f&~1n);
  if(T.size===bases[i].size+bases[j].size)continue;stats.nonzeroIntersection++;
  let F=[...R[i].F,...R[j].F],W=[],shift=R[i].F.length;
  for(let a of R[i].W)for(let b of R[j].W){stats.wordTrials++;let w=a|(b<<shift),K=new Map(),ok=true;for(let k=0;k<F.length;k++)if(admit(K,F[k]^BigInt(w>>k&1))<0){ok=false;break}if(ok)W.push(w)}
  if(!W.length){contradiction={i,j};break outer}
  const wi=new Set(W.map(w=>w&((1<<shift)-1))),wj=new Set(W.map(w=>w>>shift));
  stats.rowsExcluded+=R[i].W.length-wi.size+R[j].W.length-wj.size;
  for(let m=1;m<2**F.length;m++){stats.maskTests++;let v=par(BigInt(m&W[0])),all=true;for(let w of W){stats.maskWordTests++;if(par(BigInt(m&w))!==v){all=false;break}}if(!all)continue;let row=BigInt(v);for(let k=0;k<F.length;k++)if(m>>k&1)row^=F[k];let r=admit(A,row);if(r){stats.proofs.push({i,j,m,v,row:row.toString(16),W});if(r<0){contradiction={i,j,m};break outer}stats.affineGain++}}
  if(ops-rankOps+stats.wordTrials+stats.maskWordTests>stats.cap){stats.capped=true;break outer}
 }
 const summarize=v=>({max:Math.max(0,...v),sum:v.reduce((a,b)=>a+b,0)});
 return {instance:x.cert.instance,instance_id:x.cert.instance_id,N:x.cert.original_N_bits,original_ids:x.cert.original_ids,guard_id:"EMPTY",residual_id:x.cert.output_residual_id,parent:"CERT-v1:sha256:"+sha(JSON.stringify(x.cert)+"\n"),source:summarize(before),projected:summarize(after),sorted:summarize(sorted1),cutChecks:2*before.length,rankOps,pairRankOps:ops-rankOps,pair:stats,contradiction,profiles:{before,after,sorted0,sorted1}};
}

const spectralLog=[];

function prune(x){
 const R=x.residual.regions.map(r=>({F:r.forms.map(([s,c])=>(BigInt("0x"+s)<<1n)|BigInt(c)),W:r.allowed.slice()}));
 const n=R.length, stats={rankEvents:0,pairs:0,wordTests:0,checkMasks:0,checkWords:0,checkParity:0,rounds:0,cap:3000000,capped:false},proof=[];
 const clock=()=>stats.rankEvents+stats.pairs+stats.wordTests+stats.checkMasks+stats.checkWords+stats.checkParity;
 const par=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
 const masks=R.map(r=>r.F.reduce((a,f)=>a|(f&~1n),0n));
 // Tagged GF2 elimination of coefficient rows gives every compatibility equation on joined words.
 function equations(F){const B=new Map(),E=[];for(let k=0;k<F.length;k++){let x=F[k],t=1<<k;while(x&~1n){stats.rankEvents++;let v=(x&~1n)&-(x&~1n);if(!B.has(v)){B.set(v,[x,t]);break}let [u,m]=B.get(v);x^=u;t^=m}if(!(x&~1n))E.push([t,Number(x&1n)])}return E}
 function test(E,w){stats.wordTests++;return E.every(([m,b])=>par(BigInt(m&w))===b)}
 // Independent replay: enumerate ALL zero-coefficient combinations, not tagged pivot equations.
 function verify(F,U,V,shift,side,removed){let E=[];for(let m=1;m<2**F.length;m++){stats.checkMasks++;let z=0n;for(let k=0;k<F.length;k++)if(m>>k&1)z^=F[k];if(!(z&~1n))E.push([m,Number(z&1n)])}
 for(let r of removed){for(let w of (side===0?V:U)){stats.checkWords++;let v=side===0?r|(w<<shift):w|(r<<shift);let ok=true;for(let [m,b] of E){stats.checkParity++;if(par(BigInt(m&v))!==b){ok=false;break}}if(ok)throw Error("invalid exclusion")}}
 return true}
 let empty=null;
 outer:for(let round=0;round<1+R.reduce((s,r)=>s+r.W.length,0);round++){let change=0;stats.rounds++;
 for(let i=0;i<n;i++)for(let j=i+1;j<n;j++){
  if(clock()>=stats.cap){stats.capped=true;break outer}stats.pairs++;
  if(!(masks[i]&masks[j]))continue;
  let F=[...R[i].F,...R[j].F],shift=R[i].F.length,E=equations(F),cross=E.some(([m])=>(m&((1<<shift)-1))&&(m>>shift));if(!cross)continue;
  let U=R[i].W,V=R[j].W,si=new Set(),sj=new Set();
  for(let a of U)for(let b of V)if(test(E,a|(b<<shift))){si.add(a);sj.add(b)}
  let di=U.filter(w=>!si.has(w)),dj=V.filter(w=>!sj.has(w));
  if(di.length||dj.length){verify(F,U,V,shift,0,di);verify(F,U,V,shift,1,dj);proof.push({i,j,beforeI:U,beforeJ:V,removedI:di,removedJ:dj});
   R[i].W=U.filter(w=>si.has(w));R[j].W=V.filter(w=>sj.has(w));change+=di.length+dj.length;
   if(!R[i].W.length||!R[j].W.length){empty={i,j};break outer}
  }
 }
 if(!change)break;
 }
 const residual={...x.residual,regions:x.residual.regions.map((r,i)=>({...r,allowed:R[i].W}))};
 const before=x.residual.regions.reduce((s,r)=>s+r.allowed.length,0),after=residual.regions.reduce((s,r)=>s+r.allowed.length,0);
 // Local affine-hull reclosure on the pruned exact tables (one scan; report independent gains only).
 const A=new Map(),affine=[];let rankOps=0;
 for(let i=0;i<R.length;i++){let {F,W}=R[i];if(!W.length)continue;for(let m=1;m<2**F.length;m++){let p=par(BigInt(m&W[0]));if(!W.every(w=>par(BigInt(m&w))===p))continue;let row=BigInt(p);for(let k=0;k<F.length;k++)if(m>>k&1)row^=F[k];let z=row;while(z&~1n){rankOps++;let b=(z&~1n)&-(z&~1n);if(A.has(b))z^=A.get(b);else{A.set(b,z);affine.push({i,m,p,row:row.toString(16)});break}}if(z===1n)affine.push({i,m,p,row:row.toString(16),contradiction:true})}}
 const raw=JSON.stringify(residual)+"\n",resSha=sha(raw),resID="RESIDUAL-v1:sha256:"+sha(JSON.stringify(["PNP-RESIDUAL-v1",x.cert.instance_id,"EMPTY",residual.schema,resSha,x.cert.map_sha256])+"\n");
 const cert={problem_id:"STRICT-EB4-v1",instance:x.cert.instance,instance_id:x.cert.instance_id,original_N_bits:x.cert.original_N_bits,source_pin:x.cert.source_pin,guard_id:"EMPTY",residual_id:x.cert.output_residual_id,original_ids:x.cert.original_ids,parents:["CERT-v1:sha256:"+sha(JSON.stringify(x.cert)+"\n")],claim:"Exact pair-support removal from authenticated projected tables; all removed words have no compatible partner even in current pair relaxation. Original feasibility and reconstruction preserved; no global decision inferred except empty table if any.",output_residual_id:resID,output_residual_sha256:resSha,map_sha256:x.cert.map_sha256,before,after,proof,stats,empty,affineReclosure:{rank:A.size,rankOps,affine},checker:"pair-support-replay.js prune(): tagged elimination discovery, independent full zero-coefficient mask enumeration for every deletion; exact before and after words; original map unchanged on remaining support."};
 return {cert,residual};
}

const fs=require("node:fs");const cases=checked(JSON.parse(fs.readFileSync(process.argv[2],"utf8")),JSON.parse(fs.readFileSync(process.argv[3],"utf8")));for(const x of cases){const y=prune(x);console.log(JSON.stringify(y));}
