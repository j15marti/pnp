function run(src){
 const C=Function(src.compiler.slice(src.compiler.indexOf("function compile("),src.compiler.indexOf("function auditLocal("))+";return compile")();
 const H=Function(src.hybrid.split('if(typeof require==="function"')[0]+";return {sha,norm,closure,affine,compact,reduce,canon,unique,lift,gadgetAudit}")();
 const make=Function(src.previous.slice(0,src.previous.indexOf("\n let results=[],certs=[];\n for(let id"))+";return {closure,restrict,ge,bij,separator,tree,verifyTree,guardPartition,cover,process};}return experiment")();
 const P=make(src),B=JSON.parse(src.corpus),R=JSON.parse(src.registry);
 const assert=(b,m)=>{if(!b)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),mod=(x,p)=>(x%p+p)%p;
 const vars=F=>[...new Set(F.flat().map(Math.abs))].sort((a,b)=>a-b);
 function extract(F,M){
  let db=new Map(F.map((c,i)=>[H.canon(c).join(","),i])),rows=[];
  for(let [i,c] of F.entries()){
   if(!c.length||c.length>8)continue;let proof=[i],ok=true;
   for(let a=0;a<c.length;a++)for(let b=a+1;b<c.length;b++){
    M.extract++;let j=db.get(H.canon([-c[a],-c[b]]).join(","));
    if(j===undefined)ok=false;else proof.push(j)
   }
   if(ok)rows.push({c,proof})
  }return rows
 }
 function field(F,p){
  let M={extract:0,field:0,check:0},V=vars(F),E=extract(F,M),n=V.length,m=E.length;
  let A=E.map((e,i)=>{let a=Array(n+1+m).fill(0),b=1;for(let l of e.c){a[V.indexOf(Math.abs(l))]=mod(l>0?1:-1,p);if(l<0)b--}a[n]=mod(b,p);a[n+1+i]=1;return a});
  let rank=0;
  for(let j=0;j<n&&rank<m;j++){
   let i=A.findIndex((r,i)=>i>=rank&&r[j]);M.field+=m;if(i<0)continue;
   [A[rank],A[i]]=[A[i],A[rank]];let r=A[rank],inv=p===3&&r[j]===2?2:1;
   for(let k=0;k<r.length;k++){r[k]=mod(r[k]*inv,p);M.field++}
   for(let a=0;a<m;a++)if(a!==rank&&A[a][j]){let b=A[a][j];for(let k=0;k<r.length;k++){A[a][k]=mod(A[a][k]-b*r[k],p);M.field++}}
   rank++;
  }
  let proofs=[];
  for(let a of A){
   let lhs=a.slice(0,n).map((u,i)=>[V[i],u]).filter(x=>x[1]),rhs=a[n],coeff=a.slice(n+1);
   if(!lhs.length&&rhs)proofs.push({type:"conflict",lhs,rhs,coeff});
   if(lhs.length===1){let [v,u]=lhs[0],b=mod(rhs*(p===3&&u===2?2:1),p);proofs.push({type:b===2?"conflict":"pin",lhs,rhs,coeff,v,b})}
  }
  // Independent combination replay: no reliance on the elimination transcript.
  for(let e of E){assert(eq(F[e.proof[0]],e.c),"row");let k=1;for(let i=0;i<e.c.length;i++)for(let j=i+1;j<e.c.length;j++){M.check++;assert(eq(H.canon(F[e.proof[k++]]),H.canon([-e.c[i],-e.c[j]])),"pair")}}
  for(let z of proofs){
   let a=new Map(),b=0;
   E.forEach((e,i)=>{let w=z.coeff[i],r=1;for(let l of e.c){M.check++;let v=Math.abs(l);a.set(v,mod((a.get(v)||0)+w*(l>0?1:-1),p));if(l<0)r--}b=mod(b+w*r,p)});
   let lhs=[...a].filter(x=>x[1]).sort((a,b)=>a[0]-b[0]);assert(eq(lhs,z.lhs)&&b===z.rhs,"combination");
   if(z.type==="conflict")assert(!lhs.length&&b||lhs.length===1&&p===3&&mod(b*(lhs[0][1]===2?2:1),3)===2,"conflict");
   else assert(lhs.length===1&&lhs[0][0]===z.v&&[0,1].includes(z.b)&&mod(lhs[0][1]*z.b,p)===b,"pin")
  }
  return {p,rows:E,rank,proofs,M}
 }
 function fusion(F,g){
  let meter={up:0},u=P.closure(F,g,meter),D=H.unique(P.restrict(F,u.p)),trace=[],pins=0;
  if(u.conflict)return {status:"UNSAT",via:"UP",trace,pins,meter,nodes:1,tree:0};
  for(let i=0;i<40;i++){
   let change=false;
   for(let p of [2,3]){
    let a=field(D,p),bad=a.proofs.find(x=>x.type==="conflict");
    if(bad){trace.push({D,a});return {status:"UNSAT",via:"GF"+p,trace,pins,meter,nodes:0}}
    let q=a.proofs.filter(x=>x.type==="pin");
    if(q.length){trace.push({D,a});let E=D.concat(q.map(x=>[x.b?x.v:-x.v]));let t=P.closure(E,[],meter);pins+=t.p.size;if(t.conflict)return {status:"UNSAT",via:"reclosure",trace,pins,meter,nodes:0};D=H.unique(P.restrict(E,t.p));change=true;break}
    trace.push({D,a})
   }
   if(!change)break
  }
  let t=P.tree(D,[],500000);if(t.status==="UNSAT")P.verifyTree(D,[],t.tree);
  return {status:t.status,via:"tree",trace,pins,meter,nodes:t.nodes,reads:t.reads,tree:t.tree,D}
 }
 function strip(a){return {status:a.status,via:a.via,pins:a.pins,nodes:a.nodes,reads:a.reads,up:a.meter.up,field:a.trace.reduce((s,t)=>s+t.a.M.field,0),extract:a.trace.reduce((s,t)=>s+t.a.M.extract,0),verify:a.trace.reduce((s,t)=>s+t.a.M.check,0),steps:a.trace.map(t=>({p:t.a.p,rows:t.a.rows.length,rank:t.a.rank,proofs:t.a.proofs.length}))}}
 let results=[],certs=[];
 for(let id of ["JOINT-24","RANDOM-3CNF-40"]){
  let x=B.instances.find(z=>z.id===id),e=R.instances.find(z=>z.alias==="EB-"+id),G=C(x),raw=JSON.stringify(G.network)+"\n";
  assert(H.sha(raw)===e.sha256&&raw.length*8===e.N_bits&&H.sha(x.dimacs)===e.source_cnf.sha256&&x.dimacs.length*8===e.source_cnf.N_bits,"identity");
  let S=H.norm(G.network),m={n:0,cap:2e6},p=new Map(),cl=H.closure(S.factors,p,m),ge=H.affine(S),K=H.compact(S,2e6),D=H.reduce(K.F,2e6);
  // Same native chart; all five separate methods and paired width 2/4 feedback from pinned runner.
  let F=D.F,base=P.process(F),fused=base.guards.guards.map(g=>fusion(F,g));
  let Q=x.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1)),pr=P.tree(Q,[],500000);if(pr.status==="UNSAT")P.verifyTree(Q,[],pr.tree);
  let chart=JSON.stringify({gauge:S.gauge,F})+"\n",map=JSON.stringify({gauge:S.gauge,privateTrace:K.trace,dpTrace:D.trace,normalizer:"hybrid.js@08f5d87b1534442cf0b8225761ba1a954a455e6c"})+"\n";
  let guardInfo=base.guards.guards.map(g=>{let schema="T3-relative-carrier-v1",bytes=JSON.stringify({gaugePort:S.gauge-1,relativePortBits:g.map(([v,b])=>[v-1,b]).sort((a,b)=>a[0]-b[0])})+"\n",id="GUARD-v1:sha256:"+H.sha(JSON.stringify(["PNP-GUARD-v1",e.instance_id,schema,H.sha(bytes)])+"\n");return {schema,bytes,id,residual_id:"RESIDUAL-v1:sha256:"+H.sha(JSON.stringify(["PNP-RESIDUAL-v1",e.instance_id,id,"T3-CNF-chart-v1",H.sha(chart),H.sha(map)])+"\n")}})
  let cert={problem_id:"STRICT-EB4-v1",instance:e.short_id,instance_id:e.instance_id,original_N_bits:e.N_bits,source_pin:"registry 0c14cdc57925788cf7a451dcd5aa171dce860f2c; compiler 21b9d53fb8166c819b24e708656c742cd3c24f10; corpus e315349cd6c1fe3fa696504859f28312f6aab69a",guard_id:"EMPTY",residual_id:"ROOT",original_ids:{vertices:[0,G.network.types.length-1],ports:[0,4*G.network.types.length-1],edges:[0,G.network.edges.length-1]},parents:[],chart,map,guardInfo,guards:base.guards,cover:base.cover,fused,pairedCertificates:base.certs};
  let s=JSON.stringify(cert)+"\n";certs.push({id,content:s,sha:H.sha(s)});
  let arms=base.results.map(a=>({name:a.name,ms:a.ms,rowsPeak:a.rowsPeak,litsPeak:a.litsPeak,proofReads:a.proofReads,status:a.guards.every(g=>g.status==="UNSAT")?"UNSAT":"UNKNOWN",nodes:a.guards.reduce((s,g)=>s+g.nodes,0),pins:a.guards.reduce((s,g)=>s+g.pins,0),learned:a.guards.reduce((s,g)=>s+(g.learned||0),0),flips:a.guards.reduce((s,g)=>s+(g.first?.flips||0)+(g.second?.flips||0),0),ties:a.guards.reduce((s,g)=>s+(g.first?.changedTies||0)+(g.second?.changedTies||0),0),metrics:a.guards.reduce((s,g)=>{for(let [k,v] of Object.entries(g.metrics))s[k]=(s[k]||0)+v;return s},{})}));
  results.push({id,instance:e.instance_id,N:e.N_bits,early:{roots:S.roots,factors:S.factors.length,pins:p.size,closure:cl,checks:m.n,ge,private:K.trace.length,dp:D.trace.length,chartRows:F.length,chartVars:vars(F).length,privateEvents:K.events,dpScans:D.scans,dpPairs:D.ops},lanes:base.lanes,arms,fused:fused.map(strip),cover:base.cover,companion:{status:pr.status,nodes:pr.nodes,reads:pr.reads},certificateSha:H.sha(s),bytes:s.length})
 }
 // Control: four signed exact-one rows on all triples of four variables. All pairwise binary exclusions included.
 const tetra=H.unique([1,2,3,4].flatMap(v=>{let c=[1,2,3,4].filter(w=>v!==w);return [c,...c.flatMap((a,i)=>c.slice(i+1).map(b=>[-a,-b]))]}));
 let fields=[field(tetra,2),field(tetra,3)],valid=0;
 for(let w=0;w<16;w++)if(tetra.every(c=>c.some(l=>(w>>(Math.abs(l)-1)&1)===+(l>0))))valid++;
 assert(valid===0&&fields[1].proofs.some(z=>z.type==="conflict")&&!fields[0].proofs.some(z=>z.type==="conflict"),"tetra");
 let td="p cnf 4 "+tetra.length+"\n"+tetra.map(c=>c.join(" ")+" 0\n").join(""),G=C({nvars:4,dimacs:td}),raw=JSON.stringify(G.network)+"\n",L=H.lift(tetra),bits="1".repeat(L.n)+"0",gamma=(L.m+1).toString(2);bits+="0".repeat(gamma.length-1)+gamma;let width=Math.ceil(Math.log2(L.n+1));for(let c of L.R)for(let v of c)bits+=v.toString(2).padStart(width,"0");assert(bits.length===L.N,"T5 size");
 const fano=H.unique([[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]].flatMap(c=>[c,c.map(x=>-x)])),fc=P.process(fano);
 return {results,certs,control:{tetra,dimacs:td,cnfSha:H.sha(td),cnfN:td.length*8,nativeSha:H.sha(raw),nativeN:raw.length*8,nativeVertices:G.network.types.length,nativeEdges:G.network.edges.length,orderedT5:{n:L.n,m:L.m,N:L.N,asciiBitSha:H.sha(bits),gadget:H.gadgetAudit()},fields,valid,fano:fc.results.map(a=>({name:a.name,nodes:a.guards.reduce((s,g)=>s+g.nodes,0),learned:a.guards.reduce((s,g)=>s+(g.learned||0),0)}))}}
}
if(typeof require==='function'){const fs=require('fs');const keys=['compiler','corpus','registry','hybrid','previous'];const src=Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]));console.log(JSON.stringify(run(src),null,2));}
