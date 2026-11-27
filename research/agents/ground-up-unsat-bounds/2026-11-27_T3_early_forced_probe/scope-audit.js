const fs=require('node:fs');
const pins={"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"],"results":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_early_forced_probe/results.json","1d0dc7becd25027a2e6b2f2d28ce93ffb63ff047"],"runner":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_early_forced_probe/replay.js","ed9e19f1ad8d485c028765111ba4250d812892b4"],"jointPeer":["research/proof-spine-2026-11-26/four-partition-nae/2026-11-27_T2_orientation_guard_cover/JOINT-24-direct-conservation.json","a6e8108a11830101e72ecbaac87bcf677f29ad41"],"randomPeer":["research/proof-spine-2026-11-26/closure-cooperative-contraction/2026-11-27_1404_T1_symmetry_degree/RANDOM-3CNF-40-symmetry-cert.json","769730551779e03f55319cf6b085649e9a421244"]};
const data=Object.fromEntries(Object.keys(pins).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
const audit=function audit(data,pins){
 const compile=new Function("return function compile"+data.compiler.split("function compile")[1].split("function auditLocal")[0])();
 const {sha,norm,project,replay,canon,key}=new Function(data.native+";return {sha,norm,project,replay,canon,key};")();
 const A=(t,m)=>{if(!t)throw Error(m)},enc=o=>JSON.stringify(o)+"\n";
 const old=JSON.parse(data.results),reg=JSON.parse(data.registry),corp=JSON.parse(data.corpus);
 const expr=data.runner.slice(data.runner.indexOf("const experiment=")+17,data.runner.lastIndexOf(";\nconsole.log(")).replace("let results=[];","return {learn,verify,stats,up,reduce}; let results=[];");
 const {learn,stats,up,reduce}=new Function("return ("+expr+")")()(data,pins);
 const vars=C=>[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b);
 function altUP(C,assumptions){
  let active=C.map(c=>c.slice()),queue=assumptions.slice(),p=new Map(),scans=0,lits=0;
  for(;;){if(active.some(c=>c.length===0))return {conflict:true,scans,lits,p};
   for(let c of active){scans++;if(c.length===1)queue.push(c[0])}
   if(!queue.length)return {conflict:false,scans,lits,p};
   let l=queue.shift(),v=Math.abs(l);if(p.has(v)){if(p.get(v)!==l)return {conflict:true,scans,lits,p};continue}
   p.set(v,l);let next=[];for(let c of active){scans++;lits+=c.length;if(c.includes(l))continue;next.push(c.filter(x=>x!==-l))}active=next}
 }
 function altVerify(C,tr){let m={clauses:0,scans:0,lits:0};let D=C.slice();for(let c of tr){let u=altUP(D,c.map(l=>-l));A(u.conflict,"independent RUP fail");m.clauses++;m.scans+=u.scans;m.lits+=u.lits;D.push(c)}return m}
 function carrierAudit(g,b){
  let n=4*g.types.length,P=Array.from({length:n},(_,i)=>i),S=new Uint8Array(n),work=0;
  function find(i){let s=0,j=i;while(P[j]!==j){work++;s^=S[j];j=P[j]}return [j,s]}
  function join(i,j,s){let [a,u]=find(i),[b,v]=find(j);if(a===b){A((u^v)===s,"DSU conflict");return}if(a>b)[a,b]=[b,a];P[b]=a;S[b]=u^v^s}
  for(let [i,j,s] of g.edges)join(i,j,s);
  for(let v=0;v<g.types.length;v++)if(g.types[v]==="E")for(let k=1;k<4;k++)join(4*v,4*v+k,0);
  for(let p=0;p<n;p++){let [r,s]=find(p);A(r+1===b.root[p]&&s===b.sign[p],"carrier map")}
  return work;
 }
 function localTables(g,b,owners){
  return owners.map(v=>{A(g.types[v]==="B","B owner");let p=Array.from({length:4},(_,i)=>4*v+i),V=canon(p.map(i=>b.root[i])),W=[];
   for(let w=0;w<2**V.length;w++){let sum=p.reduce((s,i)=>s+(((w>>V.indexOf(b.root[i]))&1)^b.sign[i]),0);if(sum===2)W.push(w)}
   return {V,W,v};
  })
 }
 function gac(T,assumptions){
  let p=new Map(),work=0,passes=0,trace=[];
  for(let l of assumptions){let v=Math.abs(l),z=+(l>0);if(p.has(v)&&p.get(v)!==z)return {conflict:true,work,passes,trace};p.set(v,z)}
  for(;;){passes++;let change=false;
   for(let {V,W,v} of T){let F=[];for(let w of W){work++;if(V.every((x,i)=>!p.has(x)||p.get(x)===(w>>i&1)))F.push(w)}
    if(!F.length)return {conflict:true,work,passes,trace,conflictOwner:v};
    for(let i=0;i<V.length;i++)if(!p.has(V[i])){let z=F[0]>>i&1;work+=F.length;if(F.every(w=>(w>>i&1)===z)){p.set(V[i],z);trace.push([V[i],z,v]);change=true}}
   }if(!change)return {conflict:false,work,passes,trace};
  }
 }
 function guardLits(b,pins){return pins.map(([p,v])=>((v^b.sign[p])?1:-1)*b.root[p])}
 function peerAudit(alias,g,b){
  let raw=alias==="JOINT-24"?data.jointPeer:data.randomPeer,peer=JSON.parse(raw),id=alias==="JOINT-24"?"e1f3c884142546ba67b979cc00003f7e7ff3c595377f79e58301eba3dc55b7e0":"69c62f8bcf0da083649520a0ff8f3f643f66b4e4867a7ccc261f5b73e7c9ff9a";
  A(sha(raw)===id,"peer hash");let row=alias==="JOINT-24"?{guard:peer.excluded_guard.guard,B_vertices:peer.original_ids.B_vertices}:peer.children[0];
  let guard=row.guard, owners=row.B_vertices,l=guardLits(b,guard),c=canon(l.map(x=>-x)),d=canon(l);
  let T=localTables(g,b,owners),r=gac(T,l),s=gac(T,l.map(x=>-x)),conservation=null;
  if(alias==="JOINT-24"){
   let fixed=new Map(l.map(x=>[Math.abs(x),+(x>0)])),cnt=new Map();
   for(let v of owners)for(let j=0;j<4;j++){let p=4*v+j,k=b.root[p];if(!cnt.has(k))cnt.set(k,[0,0]);cnt.get(k)[b.sign[p]]++}
   let max=0,min=0;for(let [k,[pos,neg]] of cnt){if(fixed.has(k)){let z=fixed.get(k)?pos:neg;min+=z;max+=z}else{min+=Math.min(pos,neg);max+=Math.max(pos,neg)}}
   A(max<2*owners.length,"conservation");conservation={max,min,required:2*owners.length,terms:[...cnt]};
  }
  const verified=alias==="JOINT-24"?Boolean(conservation):r.conflict&&s.conflict;
  return {parent:"CERT-v1:sha256:"+id,guard,owners,clauses:verified?[c,d]:[],conservation,gac:{guard:r,complement:s},verified,bytes:raw.length};
 }
 function lin(C,mode,unionCap=5){
  const vs=vars(C),idx=new Map(vs.map((v,i)=>[v,i])),n=vs.length,one=1n<<BigInt(n),X=one-1n;
  let bit=v=>1n<<BigInt(idx.get(v)),B=new Map(),cert=[],work={scopeTests:0,wordTests:0,clauseTests:0,eqTests:0,xors:0},contr=false;
  function insert(row,reason){let a=row;while(a&X){let p=(a&X).toString(2).length-1;if(!B.has(p)){B.set(p,a);cert.push({row:row.toString(16),reason});return}a^=B.get(p);work.xors++}if(a&one){contr=true;cert.push({row:row.toString(16),reason})}}
  let scopeMap=new Map();for(let c of C){let z=vars([c]);if(z.length<=unionCap)scopeMap.set(key(z),z)}
  let scopes=[...scopeMap.values()];
  if(mode==="pairs"){let orig=scopes.slice();for(let i=0;i<orig.length;i++)for(let j=i+1;j<orig.length;j++)if(orig[i].some(x=>orig[j].includes(x))){let z=canon([...orig[i],...orig[j]]);if(z.length<=unionCap)scopeMap.set(key(z),z)}scopes=[...scopeMap.values()]}
  const parity=a=>{let p=0;while(a){a&=a-1;p^=1}return p};
  for(let scope of scopes){if(contr)break;let local=[];
   for(let i=0;i<C.length;i++){work.scopeTests++;if(C[i].every(l=>scope.includes(Math.abs(l)))&&(mode!=="same"||vars([C[i]]).length===scope.length))local.push(i)}
   let rows=[];for(let w=0;w<2**scope.length;w++){work.wordTests++;let good=true;for(let i of local){work.clauseTests++;if(!C[i].some(l=>+(l>0)===(w>>scope.indexOf(Math.abs(l))&1))){good=false;break}}if(good)rows.push(w)}
   if(!rows.length){insert(one,{scope,local,empty:true});break}
   for(let mask=1;mask<2**scope.length;mask++){let b=parity(mask&rows[0]);work.eqTests+=rows.length;if(!rows.every(w=>parity(mask&w)===b))continue;let row=b?one:0n;scope.forEach((v,i)=>{if(mask>>i&1)row|=bit(v)});insert(row,{scope,local,mask,b})}
  }
  let reduced=new Map(B),piv=[...B.keys()].sort((a,b)=>a-b);
  for(let p of piv)for(let q of piv)if(q>p&&((reduced.get(q)>>BigInt(p))&1n)){reduced.set(q,reduced.get(q)^reduced.get(p));work.xors++}
  let forced=[],eq=[];for(let [p,a] of reduced){let inds=vs.filter((v,i)=>(a>>BigInt(i))&1n);if(inds.length===1)forced.push([inds[0],+(Boolean(a&one))]);if(inds.length===2)eq.push([inds,+(Boolean(a&one))])}
  let free=vs.map((v,i)=>i).filter(i=>!B.has(i)),trials=0,count=null,model=null,enumChecks=0;
  if(!contr&&free.length<=15){count=0;
   for(let w=0;w<2**free.length;w++){trials++;let x=0n;free.forEach((p,i)=>{if(w>>i&1)x|=1n<<BigInt(p)});for(let [p,row] of reduced){let a=row&X&x,b=Boolean(row&one),t=0;while(a){a&=a-1n;t^=1}if(Boolean(t)!==b)x|=1n<<BigInt(p)}
    let ok=true;for(let c of C){enumChecks++;if(!c.some(l=>Boolean(x&bit(Math.abs(l)))===(l>0))){ok=false;break}}if(ok){count++;model=x.toString(16)}
   }
  }
  // Exact quadratic identity from binary-clause failure polynomials after affine substitution.
  let qstatus="NOT_RUN",qrank=0,qcert=[],qfeatures=0,quadraticOps=0;
  if(!contr&&free.length<=25){
   let k=free.length,fi=new Map(free.map((i,j)=>[i,j])),features=[0n];for(let j=0;j<k;j++)features.push(1n<<BigInt(j));for(let i=0;i<k;i++)for(let j=i+1;j<k;j++)features.push((1n<<BigInt(i))|(1n<<BigInt(j)));qfeatures=features.length;
   let ix=new Map(features.map((f,i)=>[f.toString(),i])),QB=new Map();
   function affineVar(v){let i=idx.get(v);if(fi.has(i))return [1n<<BigInt(fi.get(i))];let row=reduced.get(i),terms=[];if(row&one)terms.push(0n);for(let j of free)if(row>>BigInt(j)&1n)terms.push(1n<<BigInt(fi.get(j)));return terms}
   function failure(l){let a=affineVar(Math.abs(l));if(l>0){if(a.includes(0n))a=a.filter(x=>x!==0n);else a.push(0n)}return a}
   function mul(a,b){let S=new Set();for(let i of a)for(let j of b){quadraticOps++;let z=(i|j).toString();if(S.has(z))S.delete(z);else S.add(z)}return [...S].map(BigInt)}
   qstatus="UNKNOWN";
   for(let ci=0;ci<C.length;ci++){let c=C[ci];if(c.length>2)continue;let p=[0n];for(let l of c)p=mul(p,failure(l));let row=0n;for(let t of p){let i=ix.get(t.toString());A(i!==undefined,"feature");row^=1n<<BigInt(i)}
    let a=row,combo=1n<<BigInt(ci);while(a>1n){let j=a.toString(2).length-1;if(!QB.has(j)){QB.set(j,[a,combo]);qrank++;break}let [b,z]=QB.get(j);a^=b;combo^=z;quadraticOps++}
    if(a===1n){qstatus="UNSAT";qcert=C.map((_,i)=>i).filter(i=>combo>>BigInt(i)&1n);break}
   }
  }
  return {status:contr||count===0||qstatus==="UNSAT"?"UNSAT":count>0?"SAT":"UNKNOWN",rank:B.size,n,free:free.length,forced,eq,scopes:scopes.length,work,certificate:cert,enumeration:{trials,count,checks:enumChecks,model},quadratic:{status:qstatus,rank:qrank,features:qfeatures,ops:quadraticOps,clauseIndices:qcert},basis:[...reduced].map(([p,a])=>[p,a.toString(16)]),variables:vs};
 }
 let results=[];
 for(let r of old.results){
  const src=corp.instances.find(x=>x.id===r.alias),rr=reg.instances.find(x=>x.alias==="EB-"+r.alias),g0=compile({nvars:src.nvars,dimacs:src.dimacs}),g=g0.network;
  A(sha(enc(g))===rr.sha256&&enc(g).length*8===rr.N_bits&&sha(src.dimacs)===rr.source_cnf.sha256&&sha(enc(g0.source_map))===rr.source_map_sha256,"source fingerprint");
  const b=norm(g),dsu=carrierAudit(g,b),p=replay(b.C,r.proof.projection_trace);
  A(sha(enc(p.C))===r.proof.projected_sha,"projection hash");
  let C=src.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));
  let independent={native:altVerify(p.C,r.proof.rup_trace),cnf:altVerify(C,r.cproof.rup_trace)};
  let natRoot=up(p.C,[],stats()),D=reduce(p.C,natRoot.P);
  let local={native:lin(D,"complete"),cnf:lin(C,"complete")},pair={native:lin(D,"pairs"),cnf:lin(C,"pairs")};
  let peer=peerAudit(r.alias,g,b),survive=new Set(vars(p.C)),filtered=peer.clauses.filter(c=>c.every(l=>survive.has(Math.abs(l)))),H,recompute=null;
  if(filtered.length===peer.clauses.length){H=[...p.C,...filtered.filter(c=>!p.C.some(a=>key(a)===key(c)))]}
  else{let extra=peer.clauses.filter(c=>!b.C.some(a=>key(a)===key(c)));let f=project([...b.C,...extra],128);H=f.C;recompute={scans:f.scans,pairs:f.pairs,steps:f.trace.length}}
  let h=learn(H,"pair"),ha=altVerify(H,h.tr),hg=up(H,[],stats());
  let rnd=123456789,random=()=>{rnd=(Math.imul(1664525,rnd)+1013904223)>>>0;return rnd};let m=stats(),rv=vars(p.C).filter(v=>!natRoot.P.has(v)),seen=new Set(),hits=[],checkScans=0;
  for(let i=0;i<64;i++){let x=rv[random()%rv.length],y=rv[random()%rv.length];if(x===y)continue;let a=random()>>>30&1?x:-x,b=random()>>>30&1?y:-y,k=key(canon([a,b]));if(seen.has(k))continue;seen.add(k);if(up(p.C,[a,b],m).conflict){let c=canon([-a,-b]),chk=altUP(p.C,[a,b]);A(chk.conflict,"random replay");checkScans+=chk.scans;hits.push(c)}}
  results.push({alias:r.alias,instance_id:rr.instance_id,original_N_bits:rr.N_bits,source_pin:pins,dsu,replay:{pairs:p.pairs,scans:p.scans},independent,local,pair,peer,hybrid:{before:p.C.length,after:H.length,imported:filtered,recompute,rootFixed:hg.P.size,status:h.status,m:h.m,tr:h.tr,checker:ha},random:{seed:123456789,draws:64,distinct:seen.size,verified:hits.length,work:m,checkScans,hits}});
 }
 return {results};
};
console.log(JSON.stringify(audit(data,pins),null,2));
