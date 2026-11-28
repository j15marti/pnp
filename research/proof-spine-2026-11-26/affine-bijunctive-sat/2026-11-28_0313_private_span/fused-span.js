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

function experiment(corpus,registry){
 if(sha("")!=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"||sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("hash self test");
 let out=[];const cases=[...["JOINT-24","RANDOM-3CNF-40"].map(id=>corpus.instances.find(x=>x.id===id)),{id:"SAT-unit",nvars:1,dimacs:"p cnf 1 1\n1 0\n"},{id:"NO-unit",nvars:1,dimacs:"p cnf 1 2\n1 0\n-1 0\n"},{id:"SAT-overlap",nvars:3,dimacs:"p cnf 3 2\n1 2 3 0\n-1 2 -3 0\n"}];
 for(const c of cases){let {network,source_map}=compile(c),s=JSON.stringify(network)+"\n",d=sha(s),m=sha(JSON.stringify(source_map)+"\n"),cnf=sha(c.dimacs),N=s.length*8,R=registry.instances.find(x=>x.source_cnf.alias===c.id);if(R&&(d!==R.sha256||N!==R.N_bits||m!==R.source_map_sha256||cnf!==R.source_cnf.sha256||c.dimacs.length*8!==R.source_cnf.N_bits))throw Error("registry mismatch");
  let t=Date.now(),base=run(network,false),msBase=Date.now()-t;t=Date.now();let proj=run(network,2),msProj=Date.now()-t;
  if(base.decision!=="UNKNOWN"&&proj.decision!=="UNKNOWN"&&base.decision!==proj.decision)throw Error("decision mismatch");
  out.push({id:c.id,instance_id:"STRICT-EB4-v1:sha256:"+d,original_N_bits:N,source_cnf_sha256:cnf,source_map_sha256:m,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{vertices:[0,network.types.length-1],ports:[0,4*network.types.length-1],edges:[0,network.edges.length-1]},parents:[],base,proj,msBase,msProj,...(!R?{control:c}:{})});
 }
 return out;
}
const fs=require('node:fs'); console.log(JSON.stringify(experiment(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),JSON.parse(fs.readFileSync(process.argv[3],'utf8'))),null,2));
