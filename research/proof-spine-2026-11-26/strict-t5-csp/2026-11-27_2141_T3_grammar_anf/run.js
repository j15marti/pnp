function run(d){
 const compile=Function(d.compiler.slice(d.compiler.indexOf("function compile("),d.compiler.indexOf("function auditLocal("))+";return compile")();
 const H=Function(d.hybrid.split('if(typeof require==="function"')[0]+";return {sha,norm,closure,affine,unique,solve,reduce,lift,gadgetAudit}")();
 const code=d.indexed.slice(d.indexed.indexOf(" function fast("),d.indexed.indexOf(" function canon("));
 const assert=(b,m)=>{if(!b)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),enc=x=>JSON.stringify(x)+"\n",sha=H.sha;
 const fast=Function("assert",code+";return fast")(assert);
 const slow=Function("assert",code.replace("if(dict.has(key))","if(false&&dict.has(key))")+";return fast")(assert);
 const sorted=a=>[...new Set(a)].sort((a,b)=>a-b),variables=F=>sorted(F.flat().map(Math.abs)),parse=s=>s.trim().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));
 const B=JSON.parse(d.corpus),R=JSON.parse(d.registry),mm=JSON.parse(d.mm),manyM=JSON.parse(d.manyM),nativeMany=JSON.parse(d.nativeMany);
 const getInput=(key,id)=>{let a=JSON.parse(d[key]).find(x=>x.cert.alias===id).cert;return {id,dimacs:a.dimacs,nvars:Number(a.dimacs.split(" ")[2])}};
 let results=[],certs=[],lifts=[];
 function replayProjection(S,T){
  let map=new Map(S.factors.map(f=>[f.id,f])),inc=new Map(),words=0,scopeReads=0;
  function add(f){map.set(f.id,f);for(let v of f.vs){if(!inc.has(v))inc.set(v,new Set());inc.get(v).add(f.id)}}
  function rm(f){map.delete(f.id);for(let v of f.vs)inc.get(v).delete(f.id)}
  for(let f of S.factors)add(f);
  for(let t of T){let ids=[...inc.get(t.pivot)??[]],b=ids.map(i=>map.get(i)),U=sorted(b.flatMap(f=>f.vs)),V=U.filter(v=>v!==t.pivot);scopeReads+=ids.length;assert(eq(ids,t.in)&&eq(V,t.vs)&&!map.has(t.out)&&U.length<=7,"replay scope");let good=new Set();
   for(let w=0;w<2**U.length;w++){words++;if(b.every(f=>f.ok.includes(f.vs.reduce((a,v,j)=>a+((w>>U.indexOf(v)&1)<<j),0))))good.add(V.reduce((a,v,j)=>a+((w>>U.indexOf(v)&1)<<j),0))}
   assert(eq([...good].sort((a,b)=>a-b),t.ok),"replay words");for(let f of b)rm(f);if(t.ok.length!==2**V.length)add({id:t.out,vs:V,ok:t.ok})
  }return {fs:[...map.values()],words,scopeReads}
 }
 function toCNF(fs){let F=[],owners=[],words=0;for(let f of fs){let n=f.vs.length,bad=Array.from({length:2**n},(_,w)=>w).filter(w=>!f.ok.includes(w));if(!bad.length)continue;let fixed=f.vs.map((v,i)=>[v,i,bad[0]>>i&1]).filter(([v,i,b])=>bad.every(w=>(w>>i&1)===b));let Q=bad.length===2**(n-fixed.length)?[fixed.map(([v,i,b])=>b?-v:v)]:bad.map(w=>f.vs.map((v,i)=>w>>i&1?-v:v));for(let w=0;w<2**n;w++){words++;assert(Q.every(c=>c.some(l=>(w>>f.vs.indexOf(Math.abs(l))&1)===Number(l>0)))===f.ok.includes(w),"cnf")};for(let c of Q){F.push(c);owners.push(f.id)}}return {F,owners,words}}
 const UP=(F,guard=[],cap=500000)=>{let p=new Map(),reads=0;for(let l of guard){if(p.has(Math.abs(l))&&p.get(Math.abs(l))!==Number(l>0))return {conflict:true,p,reads};p.set(Math.abs(l),Number(l>0))}for(;;){let changed=false;for(let c of F){let un=[],hit=false;for(let l of c){if(++reads>cap)return {unknown:true,p,reads};let v=Math.abs(l);if(!p.has(v))un.push(l);else if(p.get(v)===Number(l>0)){hit=true;break}}if(hit)continue;if(!un.length)return {conflict:true,p,reads};if(un.length===1){p.set(Math.abs(un[0]),Number(un[0]>0));changed=true}}if(!changed)return {conflict:false,p,reads}}};
 function restricted(F,p){return F.flatMap(c=>c.some(l=>p.get(Math.abs(l))===Number(l>0))?[]:[c.filter(l=>!p.has(Math.abs(l)))])}
 function tables(F,group=true){let map=new Map();F.forEach((c,i)=>{let vs=sorted(c.map(Math.abs)),key=group?vs.join(","):"i"+i;if(!map.has(key))map.set(key,{vs,ids:[]});map.get(key).ids.push(i)});return [...map.values()]}
 function anf(F,group=true,cache=true){
  let G=tables(F,group),dict=new Map(),rows=[],counts={words:0,xors:0,hits:0,keyChars:0,rankToggles:0,parentToggles:0,verifyWords:0,degree:0};
  for(let g of G){let {vs,ids}=g,n=vs.length;if(n>7)return {status:"UNKNOWN",reason:"width",counts};let masks=ids.map(i=>F[i].map(l=>(vs.indexOf(Math.abs(l))+1)*Math.sign(l)).sort((a,b)=>a-b)).sort((a,b)=>a.join(",").localeCompare(b.join(","))),key=JSON.stringify([n,masks]);counts.keyChars+=key.length;let terms;
   if(cache&&dict.has(key)){terms=dict.get(key);counts.hits++}else{let a=Array.from({length:2**n},(_,w)=>{counts.words++;return Number(!masks.every(c=>c.some(l=>(w>>(Math.abs(l)-1)&1)===Number(l>0))))});for(let j=0;j<n;j++)for(let w=0;w<a.length;w++)if(w>>j&1){a[w]^=a[w^(1<<j)];counts.xors++};terms=a.flatMap((v,w)=>v?[w]:[]);dict.set(key,terms)}
   let actual=terms.map(w=>vs.filter((v,j)=>w>>j&1));for(let t of actual)counts.degree=Math.max(counts.degree,t.length);rows.push({vs,ids,terms:actual})
  }
  const toggle=(s,x)=>s.has(x)?s.delete(x):s.add(x);
  let basis=new Map(),dependencies=[],proof=null;
  for(let i=0;i<rows.length;i++){let a=new Set(rows[i].terms.map(t=>t.join(","))),p=new Set([i]);while(a.size){let k=[...a].sort((u,v)=>u===""?1:v===""?-1:u.localeCompare(v))[0];if(!basis.has(k)){basis.set(k,{a,p});break}let q=basis.get(k);for(let x of q.a){toggle(a,x);counts.rankToggles++}for(let x of q.p){toggle(p,x);counts.parentToggles++}}if(!a.size)dependencies.push([...p].sort((a,b)=>a-b))}
  // Constant monomial is last pivot, so this row, if present, is exactly {1}.
  if(basis.has("")){let q=basis.get("");assert(q.a.size===1,"constant pivot");proof=sorted([...q.p])}
  let flexible=new Set(dependencies.flat()),necessary=proof?proof.filter(i=>!flexible.has(i)):[],optional=proof?proof.filter(i=>flexible.has(i)):[];
  // Independently evaluate original rows and reconstruct the kernel/support claims.
  for(let r of rows){let {vs,ids,terms}=r;for(let w=0;w<2**vs.length;w++){counts.verifyWords++;let val=terms.reduce((s,t)=>s^Number(t.every(v=>w>>vs.indexOf(v)&1)),0),expect=Number(!ids.every(i=>F[i].some(l=>(w>>vs.indexOf(Math.abs(l))&1)===Number(l>0))));assert(val===expect,"ANF replay")}}
  function xor(ids){let a=new Set();for(let i of ids)for(let t of rows[i].terms)toggle(a,t.join(","));return [...a].sort()}
  for(let v of dependencies)assert(xor(v).length===0,"kernel vector");
  if(proof)assert(eq(xor(proof),[""]),"proof constant");
  return {status:proof?"UNSAT":"UNKNOWN",rows:rows.length,rank:basis.size,nullity:dependencies.length,necessary:necessary.length,optional:optional.length,proof,dependencies,table:rows,entries:dict.size,counts}
 }
 function affineAndBinary(F){let rows=tables(F),V=variables(F),pos=new Map(V.map((v,i)=>[v,i])),basis=new Map(),binary=[],words=0,ops=0,contradiction=false;
  for(let {vs,ids} of rows){if(vs.length>7)continue;let ok=[];for(let w=0;w<2**vs.length;w++){words++;if(ids.every(i=>F[i].some(l=>(w>>vs.indexOf(Math.abs(l))&1)===Number(l>0))))ok.push(w)}if(!ok.length){contradiction=true;break}
   for(let mask=1;mask<2**vs.length;mask++){let parity=w=>{let t=w&mask,b=0;while(t){t&=t-1;b^=1}return b};let b=parity(ok[0]);if(!ok.every(w=>parity(w)===b))continue;let a=vs.reduce((z,v,j)=>z^((mask>>j&1)?1n<<BigInt(pos.get(v)):0n),0n);while(a){ops++;let k=a&-a;if(!basis.has(k)){basis.set(k,[a,b]);break}let q=basis.get(k);a^=q[0];b^=q[1]}if(!a&&b)contradiction=true}
   for(let i=0;i<vs.length;i++)for(let j=i+1;j<vs.length;j++)for(let x=0;x<4;x++)if(!ok.some(w=>(w>>i&1)===(x&1)&&(w>>j&1)===(x>>1))){binary.push([(x&1)?-vs[i]:vs[i],(x>>1)?-vs[j]:vs[j]])}
  }
  let adj=new Map();function edge(a,b){if(!adj.has(a))adj.set(a,[]);adj.get(a).push(b)}
  for(let [a,b] of binary){edge(-a,b);edge(-b,a)}
  let visits=0,bc=false;function reach(a,b){let q=[a],s=new Set(q);for(let j=0;j<q.length;j++){if(q[j]===b)return true;for(let t of adj.get(q[j])??[]){visits++;if(!s.has(t)){s.add(t);q.push(t)}}}return false}for(let v of V){if(reach(v,-v)&&reach(-v,v)){bc=true;break}}
  return {affine:contradiction?"UNSAT":"UNKNOWN",rank:basis.size,wordTests:words,rowOps:ops,binary:bc?"UNSAT":"UNKNOWN",binaryClauses:binary.length,graphVisits:visits}
 }
 function separator(F){let V=variables(F),adj=new Map(V.map(v=>[v,new Set()]));for(let c of F)for(let a of c)for(let b of c)if(Math.abs(a)!==Math.abs(b))adj.get(Math.abs(a)).add(Math.abs(b));let work=0,maxWidth=0;while(adj.size){let [v,S]=[...adj].sort((a,b)=>a[1].size-b[1].size||a[0]-b[0])[0];maxWidth=Math.max(maxWidth,S.size);if(S.size>6)return {status:"UNKNOWN",reason:"width cap",maxWidth,work};for(let a of S){adj.get(a).delete(v);for(let b of S)if(a!==b){adj.get(a).add(b);work++}}adj.delete(v)}return {status:"ADMITTED_NOT_EXECUTED",maxWidth,work}}
 function rup(F,cap=300000){let G=H.unique(F),V=variables(G),known=new Set(G.map(c=>c.join(","))),learned=[],reads=0,probes=0,rounds=0;
  let candidates=[];for(let v of V)for(let a of [v,-v])candidates.push([a]);for(let i=0;i<V.length;i++)for(let j=i+1;j<V.length;j++)for(let a of [V[i],-V[i]])for(let b of [V[j],-V[j]])candidates.push([a,b].sort((x,y)=>x-y));
  for(;;){rounds++;let changed=false;for(let c of candidates){let k=c.join(",");if(known.has(k))continue;let u=UP(G,c.map(l=>-l),cap-reads);reads+=u.reads;probes++;if(u.unknown||reads>=cap)return {status:"UNKNOWN",reads,probes,rounds,learned};if(u.conflict){G.push(c);known.add(k);learned.push(c);changed=true;let t=UP(G,[],cap-reads);reads+=t.reads;if(t.conflict){let replay=0,db=H.unique(F);for(let C of learned){let r=UP(db,C.map(x=>-x),1000000);assert(r.conflict,"RUP replay");replay+=r.reads;db.push(C)}let e=UP(db);assert(e.conflict,"RUP terminal");return {status:"UNSAT",reads,probes,rounds,learned,replay:replay+e.reads}}if(t.unknown)return {status:"UNKNOWN",reads,probes,rounds,learned}}}if(!changed)return {status:"UNKNOWN",reads,probes,rounds,learned}}
 }
 function feedback(F,guard,mode,cap=300000,width=4){
  let t0=Date.now(),G=H.unique(F),V=variables(G),p=new Map(V.map(v=>[v,0])),locked=new Set(guard.map(Math.abs)),reads=0,flips=0,ties=0,learned=[],peak=G.reduce((s,c)=>s+c.length,0),stat="UNKNOWN";
  for(let l of guard)p.set(Math.abs(l),Number(l>0));
  function score(flip){let bad=0,z=0;for(let c of G){let k=0,t=0;for(let l of c){if(++reads>cap)throw Error("cap");let b=p.get(Math.abs(l))??0;if(Math.abs(l)===flip)b^=1;if(b===Number(l>0)){k++;t+=Math.sign(l)}}let kmod=k%3,smod=(t%3+3)%3;if(k===0)bad++;else if(smod===0)z++;assert(kmod===k%3,"count residue")}return [bad,z]}
  try{if(mode!=="baseline"){for(let i=0;i<=G.length;i++){let base=score(0),best=null,plain=null;for(let v of V){if(locked.has(v))continue;let q=score(v);if(q[0]>=base[0])continue;if(!plain||q[0]<plain[1][0])plain=[v,q];if(!best||q[0]<best[1][0]||q[0]===best[1][0]&&mode==="residue"&&q[1]<best[1][1])best=[v,q]}if(!best)break;if(best[0]!==plain[0])ties++;p.set(best[0],1-p.get(best[0]));flips++}}
   // Frozen candidates independent of feedback, so no unjustified proof selection advantage.
   let cand=[];for(let i=0;i<G.length&&cand.length<48;i++)for(let j=i+1;j<G.length&&cand.length<48;j++)for(let l of G[i]){if(++reads>cap)throw Error("cap");if(!G[j].includes(-l))continue;let c=H.unique([[...G[i].filter(x=>x!==l),...G[j].filter(x=>x!==-l)]])[0];if(c&&c.length<=width&&!G.some(a=>eq(a,c))&&!cand.some(a=>eq(a.c,c)))cand.push({i,j,l,c})}
   if(mode!=="baseline")for(let a of cand){let c=H.unique([[...G[a.i].filter(l=>l!==a.l),...G[a.j].filter(l=>l!==-a.l)]])[0];assert(eq(c,a.c),"resolution");G.push(c);learned.push(a);peak+=c.length;if(mode==="table"||mode==="residue")score(0)}
   let all=G.concat(guard.map(l=>[l]));let s=H.solve(all,Math.max(1,cap-reads));reads+=s.scans;let check=H.solve(all,cap,s.tree);assert(check.nodes===s.nodes,"tree replay");stat="UNSAT";return {stat,reads,flips,ties,learned:learned.length,nodes:s.nodes,replayReads:check.scans,peakLiterals:peak,ms:Date.now()-t0}
  }catch(e){return {stat,reads,flips,ties,learned:learned.length,peakLiterals:peak,ms:Date.now()-t0,error:String(e)}}
 }
 function five(F){let root=UP(F),V=variables(F),cnt=new Map();for(let c of F)for(let l of c)cnt.set(Math.abs(l),(cnt.get(Math.abs(l))??0)+1);let sel=V.filter(v=>!root.p.has(v)).sort((a,b)=>cnt.get(b)-cnt.get(a)||a-b).slice(0,4),guards=[];for(let i=0;i<sel.length;i++)guards.push(sel.slice(0,i).concat(-sel[i]));guards.push(sel);let out=[],trees=[],cover=0;for(let g of guards)cover+=2**(sel.length-g.length);assert(cover===2**sel.length,"guard partition");
  for(let g of guards){let u=UP(F,g),o={guard:g,early:{reads:u.reads,pins:u.p.size,conflict:!!u.conflict}};
   if(u.conflict){o.statuses=["UNSAT","UNSAT","UNSAT","UNSAT","UNSAT"];trees.push({guard:g,tree:0});out.push(o);continue}
   let Q=restricted(F,u.p),a=affineAndBinary(Q),s=separator(Q),p=anf(Q,true,true),r=rup(Q,150000);o.residual={variables:variables(Q).length,clauses:Q.length};o.statuses=["UNKNOWN",a.affine,a.binary,s.status,p.status];o.affine=a;o.separator=s;o.rup={status:r.status,reads:r.reads,probes:r.probes,learned:r.learned.length};o.anf={status:p.status,rank:p.rank,counts:p.counts};
   try{let A=F.concat(g.map(l=>[l])),t=H.solve(A,250000),v=H.solve(A,250000,t.tree);o.tree={nodes:t.nodes,reads:t.scans,replay:v.scans};trees.push({guard:g,tree:t.tree})}catch(e){o.tree={status:"UNKNOWN",error:String(e)}}out.push(o)
  }return {root:{pins:root.p.size,reads:root.reads,conflict:!!root.conflict},guards:out,trees,coverage:{selectors:sel,covered:cover,total:2**sel.length}}
 }
 function mini(a){let {table,proof,dependencies,...x}=a;return x}
 function sourceCase(I,e,doNative=true,controls=false){
  let id=I.id,cnf=I.dimacs,cnfSha=sha(cnf),n=I.nvars,F0=parse(cnf);let cnfExpected=e.source_cnf??{sha256:(e.cnf_id??e.instance_id??"").split(":").pop(),N_bits:e.cnf_N??e.N_bits};assert(cnfSha===cnfExpected.sha256&&cnf.length*8===cnfExpected.N_bits,"cnf auth "+id);
  let cUP=UP(F0),cnfR=anf(restricted(F0,cUP.p)),out={id,cnf:{sha:cnfSha,N:cnf.length*8,variables:n,clauses:F0.length,early:{pins:cUP.p.size,conflict:!!cUP.conflict,reads:cUP.reads},grouped:mini(cnfR)}};
  if(!doNative){results.push(out);return}
  let G=compile(I),raw=enc(G.network),nativeSha=sha(raw),N=raw.length*8,mapHash=sha(enc(G.source_map)),exp=e.native??e;assert(nativeSha===(exp.sha256??exp.instance?.split(":").pop()??exp.instance_id?.split(":").pop())&&N===(exp.N_bits??exp.N),"native auth "+id);if(exp.source_map_sha256||exp.mapHash||exp.map_sha256)assert(mapHash===(exp.source_map_sha256??exp.mapHash??exp.map_sha256),"map");
  let S=H.norm(G.network),M={n:0,cap:2000000},pins=new Map(),early=H.closure(S.factors,pins,M),ge=H.affine(S);
  let t=Date.now(),P=fast(S.factors),ms=Date.now()-t,t1=Date.now(),U=slow(S.factors),uncachedMs=Date.now()-t1;assert(eq(P.trace,U.trace),"grammar baseline");let replay=replayProjection(S,P.trace);assert(eq(replay.fs.map(f=>[f.id,f.vs,f.ok]),P.fs.map(f=>[f.id,f.vs,f.ok])),"grammar replay");
  let Q=toCNF(P.fs),F=H.unique(Q.F),post=UP(F),A=restricted(F,post.p),plain=anf(A,false,false),group=anf(A,true,false),cached=anf(A,true,true);assert(eq(group.table,cached.table)&&eq(group.proof,cached.proof)&&eq(group.dependencies,cached.dependencies),"grammar ANF");
  let b=affineAndBinary(A),sep=separator(A),r=rup(A,300000);
  out.native={sha:nativeSha,N,mapHash,vertices:G.network.types.length,edges:G.network.edges.length,gauge:S.gauge,roots:S.roots,factors:S.factors.length,initial:{closure:early?"UNKNOWN":"UNSAT",pins:pins.size,reads:M.n,affine:ge},grammar:{steps:P.trace.length,entries:P.entries,...P.counts,ms,uncachedWords:U.counts.wordTests,uncachedMs,replayWords:replay.words,replayScopeReads:replay.scopeReads,remainingFactors:P.fs.length,remainingVariables:variables(F).length,clauses:F.length,cnfReplayWords:Q.words},postUP:{reads:post.reads,pins:post.p.size,conflict:!!post.conflict},individualANF:mini(plain),groupedANF:mini(group),cachedANF:mini(cached),affineBinary:b,separator:sep,width2RUP:{status:r.status,reads:r.reads,probes:r.probes,learned:r.learned.length}};
  let body={schema:"T3-GRAMMAR-ANF-v1",problem_id:"STRICT-EB4-v1",instance_id:"STRICT-EB4-v1:sha256:"+nativeSha,original_N_bits:N,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{vertices:[0,G.network.types.length-1],ports:[0,G.network.types.length*4-1],edges:[0,G.network.edges.length-1]},parents:[],gauge:S.gauge,source_pins:{compiler:"21b9d53fb8166c819b24e708656c742cd3c24f10",input:id},projection:P.trace,rootPins:[...post.p],groupedRows:cached.table,proof:cached.proof,kernelBasis:cached.dependencies};
  if(controls){let C=five(F);out.native.five={root:C.root,guards:C.guards,coverage:C.coverage};body.guardedTrees=C.trees;let g=C.guards.find(x=>!x.early.conflict)?.guard;if(g){out.native.feedback={guard:g,arms:[2,4].map(width=>({width,results:["baseline","table","residue"].map(mode=>({mode,...feedback(F,g,mode,300000,width)}))}))}}}
  if(cached.proof||body.guardedTrees?.length===5){let content=enc(body),digest=sha(content);certs.push({id,content,digest});out.native.certSha=digest}
  // Exact ordered T5 lift from authenticated original CNF, no free inverse discovery. Avoid costly lift on large native image: original input path is paid provenance-assisted.
  if(id.startsWith("MIXED")&&id.endsWith("NO")&&F0.length<=500){let L=H.lift(F0),bits="1".repeat(L.n)+"0",gamma=(L.m+1).toString(2);bits+="0".repeat(gamma.length-1)+gamma;let w=Math.ceil(Math.log2(L.n+1));for(let c of L.R)for(let v of c)bits+=v.toString(2).padStart(w,"0");assert(bits.length===L.N,"lift size");let bytes="";for(let i=0;i<bits.length;i+=8)bytes+=String.fromCharCode(parseInt(bits.slice(i,i+8).padEnd(8,"0"),2));out.lift={n:L.n,m:L.m,N:L.N,packedBytes:bytes.length,packedSha:sha(bytes),gadget:H.gadgetAudit(),status:"decision equivalent transfer; not separate T5 solve"}}
  results.push(out)
 }
 for(let id of ["JOINT-24","RANDOM-3CNF-40"]){let I=B.instances.find(x=>x.id===id),e=R.instances.find(x=>x.alias==="EB-"+id);sourceCase(I,e,true,true)}
 for(let id of ["MIXED-3-NO","MIXED-3-YES"]){let I=getInput("mixed",id),e=mm.instances.find(x=>x.alias===id);sourceCase(I,e,true,false)}
 // Large family native case after primary regressions; all other sizes use exact companion only.
 for(let id of ["MIXED-MANY-3-NO","MIXED-MANY-4-NO","MIXED-MANY-5-NO","MIXED-MANY-8-NO"]){let I=getInput("many",id),e=manyM.instances.find(x=>x.alias===id);if(id==="MIXED-MANY-3-NO"){let n=nativeMany.instances.find(x=>x.short_id.startsWith("EB-"+id+"@"));sourceCase(I,n,true,false)}else sourceCase(I,e,false,false)}
 return {results,certs}
}
if(typeof require==='function'){let fs=require('fs'),keys=["compiler","corpus","registry","hybrid","indexed","mixed","mm","many","manyM","nativeMany"];let d=Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]));console.log(JSON.stringify(run(d),null,2));}
