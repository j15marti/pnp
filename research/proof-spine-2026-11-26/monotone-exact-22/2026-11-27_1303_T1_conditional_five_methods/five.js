// Node: node five.js compile.js benchmarks.json registry.json affine-closure.js
const fs=require("node:fs");
const pins={"compiler":"21b9d53fb8166c819b24e708656c742cd3c24f10","corpus":"e315349cd6c1fe3fa696504859f28312f6aab69a","registry":"0c14cdc57925788cf7a451dcd5aa171dce860f2c","projection":"d56c096ad434544c918f83cf551d24b930be7b92"};
const [compiler,corpus,registry,projection]=process.argv.slice(2).map(p=>fs.readFileSync(p,"utf8"));
function sha(s){
 const K=[],H=[];for(let p=2;K.length<64;p++){let prime=true;for(let d=2;d*d<=p;d++)if(p%d===0){prime=false;break}if(prime){if(H.length<8)H.push((Math.sqrt(p)%1*2**32)|0);K.push((Math.cbrt(p)%1*2**32)|0)}}
 const len=s.length,b=new Uint8Array(Math.ceil((len+9)/64)*64);for(let i=0;i<len;i++){if(s.charCodeAt(i)>127)throw Error("ASCII only");b[i]=s.charCodeAt(i)}b[len]=128;const dv=new DataView(b.buffer);dv.setUint32(b.length-8,Math.floor(len*8/2**32));dv.setUint32(b.length-4,(len*8)>>>0);const W=new Int32Array(64),rr=(x,n)=>(x>>>n)|(x<<(32-n));
 for(let o=0;o<b.length;o+=64){for(let j=0;j<16;j++)W[j]=dv.getInt32(o+4*j);for(let j=16;j<64;j++){let a=W[j-15],b=W[j-2];W[j]=(W[j-16]+(rr(a,7)^rr(a,18)^(a>>>3))+W[j-7]+(rr(b,17)^rr(b,19)^(b>>>10)))|0}let [a,b,c,d,e,f,g,h]=H;for(let j=0;j<64;j++){let t1=(h+(rr(e,6)^rr(e,11)^rr(e,25))+((e&f)^(~e&g))+K[j]+W[j])|0,t2=((rr(a,2)^rr(a,13)^rr(a,22))+((a&b)^(a&c)^(b&c)))|0;h=g;g=f;f=e;e=(d+t1)|0;d=c;c=b;b=a;a=(t1+t2)|0}for(let j=0;j<8;j++)H[j]=(H[j]+[a,b,c,d,e,f,g,h][j])|0}
 return H.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("");
}
function experiment(src,sha,pins){
 const compile=new Function(src.compiler.slice(src.compiler.indexOf("function compile("),src.compiler.indexOf("function auditLocal"))+"\nreturn compile")();
 const mod={exports:{}};new Function("module",src.projection)(mod);const {normalize,project,cnfFactors}=mod.exports;
 const corpus=JSON.parse(src.corpus),reg=JSON.parse(src.registry),json=x=>JSON.stringify(x)+"\n",uniq=a=>[...new Set(a)].sort((a,b)=>a-b),parity=x=>{let s=0;while(x){s^=1;x&=x-1}return s};
 if(sha("")!=="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"||sha("abc")!=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad")throw Error("sha vectors");
 const cap=300000;
 function lane(F,g,mode,limit=cap){
  let work=0;const tick=(n=1)=>{work+=n;if(work>limit)throw Error("cap")};const vars=uniq(F.flatMap(a=>a.v)),p=new Map(g),all=F.map((a,i)=>({...a,k:[i]}));
  const restrict=(a,p)=>{let v=a.v.filter(x=>!p.has(x)),ok=[];for(let w of a.ok){tick();if(a.v.every((x,i)=>!p.has(x)||p.get(x)===(w>>i&1)))ok.push(v.reduce((z,x,i)=>z|((w>>a.v.indexOf(x)&1)<<i),0))}return {v,ok:uniq(ok),k:a.k}};
  function gac(A,p){let used=new Set(),change=true,T;while(change){change=false;T=A.map(a=>restrict(a,p));for(let a of T){if(!a.ok.length)return {no:true,k:uniq([...used,...a.k])};for(let [j,x] of a.v.entries()){tick(a.ok.length);let b=a.ok[0]>>j&1;if(a.ok.every(w=>(w>>j&1)===b)){for(let k of a.k)used.add(k);if(p.has(x)&&p.get(x)!==b)return {no:true,k:uniq([...used,...a.k])};if(!p.has(x)){p.set(x,b);change=true}}}}}return {T,p,used:[...used]}}
  let tree=null;
  try {
   if(mode==="resolution"){
    const C=[];for(let [i,a] of F.entries())for(let w=0;w<2**a.v.length;w++){tick();if(!a.ok.includes(w))C.push({l:a.v.map((v,j)=>(w>>j&1)?-v:v),k:i})}
    let nodes=0;
    function search(g){if(++nodes>48)throw Error("node cap");const a=new Map(g),used=new Set();let ch=true;
     while(ch){ch=false;for(let c of C){let sat=false,U=[];for(let l of c.l){tick();let b=a.get(Math.abs(l));if(b===undefined)U.push(l);else if(b===+(l>0)){sat=true;break}}if(sat)continue;if(!U.length)return {t:0,k:uniq([...used,c.k])};if(U.length===1){a.set(Math.abs(U[0]),+(U[0]>0));used.add(c.k);ch=true}}}
     let scores=new Map();for(let c of C){tick(c.l.length);if(c.l.some(l=>a.get(Math.abs(l))===+(l>0)))continue;for(let l of c.l)if(!a.has(Math.abs(l)))scores.set(Math.abs(l),(scores.get(Math.abs(l))||0)+1)}
     if(!scores.size)return null;const v=[...scores].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];const l=search([...g,[v,0]]);if(!l)return null;const r=search([...g,[v,1]]);if(!r)return null;return {t:[v,l.t,r.t],k:uniq([...l.k,...r.k])}
    }
    const r=search(g);return {status:r?"CANDIDATE":"UNKNOWN",work,nodes,k:r?.k,tree:r?.t,mode};
   }
   const a=gac(all,p);if(a.no)return {status:"CANDIDATE",work,k:a.k,mode,reason:"shared cardinality closure"};
   const T=a.T,used=a.used;
   if(mode==="cardinality")return {status:"UNKNOWN",work,mode,pins:p.size};
   if(mode==="affine"){
    let index=new Map(vars.map((v,i)=>[v,BigInt(i+1)])),B=new Map();const bit=v=>1n<<index.get(v);
    function put(z,k){while(z>1n){tick();let h=z.toString(2).length;if(!B.has(h)){B.set(h,[z,k]);return null}let b=B.get(h);z^=b[0];k=uniq([...k,...b[1]])}return z===1n?k:null}
    for(let t of T)for(let m=1;m<2**t.v.length;m++){let b=parity(t.ok[0]&m);tick(t.ok.length);if(t.ok.every(w=>parity(w&m)===b)){let z=BigInt(b);t.v.forEach((v,j)=>{if(m>>j&1)z^=bit(v)});let k=put(z,t.k);if(k)return {status:"CANDIDATE",work,k:uniq([...used,...k]),mode,reason:"affine inconsistency"}}}
    return {status:"UNKNOWN",work,mode,rank:B.size};
   }
   if(mode==="hall"){
    // Positive literal resource relaxation. Pair exclusions are checked against an actual table.
    const pairs=new Map(),demands=[];for(let t of T){for(let j=0;j<t.v.length;j++)for(let k=j+1;k<t.v.length;k++){tick(t.ok.length);if(t.ok.every(w=>!(w>>j&1)||!(w>>k&1)))pairs.set([t.v[j],t.v[k]].join(","),t.k)}
     for(let m=1;m<2**t.v.length;m++){tick(t.ok.length);if(t.ok.every(w=>w&m))demands.push({v:t.v.filter((_,j)=>m>>j&1),k:t.k})}}
    const key=(a,b)=>[Math.min(a,b),Math.max(a,b)].join(","),groups=[],assigned=new Map(),s=new Set();
    for(let v of uniq(T.flatMap(t=>t.v))){let chosen=-1;for(let j=0;j<groups.length;j++){tick(groups[j].length);if(groups[j].every(u=>pairs.has(key(u,v)))){chosen=j;break}}if(chosen<0){chosen=groups.length;groups.push([])}groups[chosen].push(v);assigned.set(v,chosen)}
    const D=[];demands.sort((a,b)=>a.v.length-b.v.length||a.v[0]-b.v[0]);for(let d of demands){tick(d.v.length);if(d.v.every(v=>!s.has(v))){D.push(d);d.v.forEach(v=>s.add(v))}}
    let mate=new Map();function augment(i,seen){for(let j of uniq(D[i].v.map(v=>assigned.get(v)))){tick();if(seen.has(j))continue;seen.add(j);if(!mate.has(j)||augment(mate.get(j),seen)){mate.set(j,i);return true}}return false}
    for(let i=0;i<D.length;i++)if(!augment(i,new Set())){let k=[...used,...D.slice(0,i+1).flatMap(d=>d.k)];for(let G of groups)for(let a=0;a<G.length;a++)for(let b=a+1;b<G.length;b++)k.push(...pairs.get(key(G[a],G[b])));return {status:"CANDIDATE",work,k:uniq(k),mode,reason:"Hall deficiency"}}
    return {status:"UNKNOWN",work,mode,demands:D.length,resources:groups.length,matched:mate.size};
   }
   if(mode==="separator"){
    let live=T.slice(),pivots=0;for(;;){if(live.some(t=>!t.ok.length)){let k=live.find(t=>!t.ok.length).k;return {status:"CANDIDATE",work,k:uniq([...used,...k]),mode,pivots,reason:"exact bounded join"}}let occ=new Map();for(let t of live)for(let v of t.v){tick();if(!occ.has(v))occ.set(v,[]);occ.get(v).push(t)}
     let cs=[...occ].map(([v,L])=>({v,L,scope:uniq(L.flatMap(t=>t.v)).filter(x=>x!==v)})).filter(x=>x.scope.length<=6).sort((a,b)=>a.scope.length-b.scope.length||a.v-b.v);
     if(!cs.length)return {status:"UNKNOWN",work,mode,pivots};let {v,L,scope}=cs[0],u=[v,...scope],ok=[];
     for(let w=0;w<2**scope.length;w++){for(let b=0;b<2;b++){tick(L.length);if(L.every(t=>t.ok.includes(t.v.reduce((z,x,j)=>z|((((2*w+b)>>u.indexOf(x))&1)<<j),0)))){ok.push(w);break}}}
     live=live.filter(t=>!L.includes(t));live.push({v:scope,ok,k:uniq(L.flatMap(t=>t.k))});pivots++;
    }
   }throw Error("mode");
  }catch(e){if(!["cap","node cap"].includes(e.message))throw e;return {mode,status:"UNKNOWN",work,reason:e.message}}
 }
 // Independent proof discovery and verifier: table compatibility instead of CNF resolution, exact two-child coverage.
 function verifyCandidate(F,g,k,providedTree=null){
  let work=0,nodes=0;const A=k.map(i=>F[i]);const V=uniq(A.flatMap(t=>t.v));function tick(n=1){work+=n;if(work>1500000)throw Error("check cap")}
  function close(g){const d=new Map(g);let changed=true;while(changed){changed=false;for(let t of A){let R=[];for(let w of t.ok){tick();if(t.v.every((v,j)=>!d.has(v)||d.get(v)===(w>>j&1)))R.push(w)}if(!R.length)return null;for(let j=0;j<t.v.length;j++){tick(R.length);let b=R[0]>>j&1;if(R.every(w=>(w>>j&1)===b)){let v=t.v[j];if(d.has(v)&&d.get(v)!==b)return null;if(!d.has(v)){d.set(v,b);changed=true}}}}}return d}
  function build(g){if(++nodes>192)throw Error("check cap");const d=close(g);if(!d)return 0;const scores=new Map();for(let t of A)for(let v of t.v)if(!d.has(v)){tick();scores.set(v,(scores.get(v)||0)+1)}if(!scores.size)return null;const v=[...scores].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0],l=build([...g,[v,0]]);if(l===null)return null;const r=build([...g,[v,1]]);return r===null?null:[v,l,r]}
  function replay(t,g){nodes++;if(t===0)return close(g)===null;if(!Array.isArray(t)||t.length!==3||!V.includes(t[0])||g.some(([v])=>v===t[0]))return false;return replay(t[1],[...g,[t[0],0]])&&replay(t[2],[...g,[t[0],1]])}
  try{let tree=providedTree??build(g);if(tree===null)return {verified:false,work,nodes};let w=work,n=nodes,verified=replay(tree,g);return {verified,tree,buildWork:w,replayWork:work-w,work,nodes,buildNodes:n}}catch(e){if(e.message!=="check cap")throw e;return {verified:false,work,nodes,reason:e.message}}
 }
 function compare(F,meta,gauge=null){
  const modes=["cardinality","affine","hall","separator","resolution"], freq=new Map();for(let a of F)for(let v of a.v)freq.set(v,(freq.get(v)||0)+1);
  const [a,b,c]=[...freq].sort((x,y)=>y[1]-x[1]||x[0]-y[0]).slice(0,3).map(x=>x[0]);
  const guards=[[[a,0],[b,0]],[[a,0],[b,1]],[[a,1],[b,0]],[[a,1],[b,1],[c,0]],[[a,1],[b,1],[c,1]]].map(g=>g.sort((x,y)=>x[0]-y[0]));
  let rows=[],best=[],proofs=[];let vocab=uniq(F.flatMap(a=>a.v));let importFactors=[];
  const makeGuard=g=>{const gg=meta.problem_id==="STRICT-EB4-v1"?[[gauge-1,0],...g.map(([v,b])=>[v-1,b])].sort((a,b)=>a[0]-b[0]):g;const schema=meta.problem_id==="STRICT-EB4-v1"?"EB-PORT-PINS-v1":"CNF-VAR-PINS-v1";return {pins:gg,id:"GUARD-v1:sha256:"+sha(json(["PNP-GUARD-v1",meta.instance_id,schema,sha(json(gg))])),schema}};
  function acquire(g,stage,fs=F){
   let R=[];for(let mode of modes){let r=lane(fs,g,mode);let check=null;if(r.status==="CANDIDATE"){check=verifyCandidate(fs,g,r.k,r.tree??null);if(check.verified){let ids=uniq(r.k.flatMap(i=>fs[i].ids));let pr={stage,mode,guard:g,guard_artifact:makeGuard(g),k:r.k,original_B_or_clause_ids:ids,tree:check.tree,discovery:r.work,verification:check.work};let index=proofs.push(pr)-1;r.proofIndex=index;r.supportSize=ids.length}else r.status="UNKNOWN (unverified candidate)"}if(check)r.checkWork=check.work;delete r.tree;delete r.k;R.push(r)}return R
  }
  // All five methods on each common conditional context, before sharing any results.
  for(let [i,g] of guards.entries()){let R=acquire(g,"standalone");rows.push({guard:g,methods:R});let ids=R.filter(r=>r.proofIndex!==undefined).map(r=>r.proofIndex).sort((a,b)=>proofs[a].original_B_or_clause_ids.length-proofs[b].original_B_or_clause_ids.length);best.push(ids[0]??null)}
  // Independently checked negative guards become exact extra factors for the next epoch.
  function factor(i){let q=proofs[i],g=q.guard, v=g.map(x=>x[0]),forbid=g.reduce((z,x,j)=>z|(x[1]<<j),0);return {v,ok:Array.from({length:2**v.length},(_,w)=>w).filter(w=>w!==forbid),ids:q.original_B_or_clause_ids,parent:i}}
  importFactors=best.filter(i=>i!==null).map(factor);
  // Probabilistic discovery lane at stagnation: one fixed-seed sample of pair pins, no proof of probabilities.
  let random=[];if(best.some(i=>i===null)){let seed=20261127;function rng(){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return seed>>>0}
   for(let j=0;j<4;j++){let v=vocab[rng()%vocab.length],w=vocab[rng()%vocab.length];if(v===w)continue;let g=[[v,rng()&1],[w,rng()&1]].sort((a,b)=>a[0]-b[0]);let r=lane(F,g,"resolution",100000),q=null;if(r.status==="CANDIDATE"){q=verifyCandidate(F,g,r.k,r.tree??null);if(q.verified){let i=proofs.push({stage:"random",mode:"resolution",guard:g,guard_artifact:makeGuard(g),k:r.k,original_B_or_clause_ids:uniq(r.k.flatMap(i=>F[i].ids)),tree:q.tree,discovery:r.work,verification:q.work})-1;importFactors.push(factor(i));r.proofIndex=i}}delete r.tree;delete r.k;random.push({g,r,checkWork:q?.work??0})}
  }
  let hybrid=[],fs=[...F,...importFactors];
  for(let i=0;i<guards.length;i++)if(best[i]===null){let R=acquire(guards[i],"hybrid",fs);hybrid.push({i,methods:R});let ids=R.filter(r=>r.proofIndex!==undefined).map(r=>r.proofIndex).sort((a,b)=>proofs[a].original_B_or_clause_ids.length-proofs[b].original_B_or_clause_ids.length);if(ids.length)best[i]=ids[0]}
  // Exact coverage by inclusion-exclusion over the 5 coordinate subcubes of the common chart.
  let cover=0n;const good=best.map((x,i)=>x===null?null:guards[i]).filter(Boolean),D=vocab.length;
  for(let m=1;m<2**good.length;m++){let p=new Map(),ok=true,k=0;for(let j=0;j<good.length;j++)if(m>>j&1){k++;for(let [v,b] of good[j]){if(p.has(v)&&p.get(v)!==b)ok=false;p.set(v,b)}}if(ok)cover+=(k%2?1n:-1n)*(1n<<BigInt(D-p.size))}
  let overlaps=[];for(let [i,r] of rows.entries()){let q=r.methods.filter(m=>m.proofIndex!==undefined);for(let j=0;j<q.length;j++)for(let k=j+1;k<q.length;k++){let x=proofs[q[j].proofIndex].original_B_or_clause_ids,y=proofs[q[k].proofIndex].original_B_or_clause_ids,s=new Set(y);overlaps.push({guard:i,methods:[q[j].mode,q[k].mode],intersection:x.filter(v=>s.has(v)).length,union:new Set([...x,...y]).size})}}
  let cross=[];for(let i=0;i<best.length;i++)for(let j=i+1;j<best.length;j++)if(best[i]!==null&&best[j]!==null){let x=proofs[best[i]].original_B_or_clause_ids,y=proofs[best[j]].original_B_or_clause_ids,s=new Set(y);cross.push({guards:[i,j],intersection:x.filter(v=>s.has(v)).length,union:new Set([...x,...y]).size})}
  let support=uniq(best.filter(x=>x!==null).flatMap(i=>proofs[i].original_B_or_clause_ids));
  const sumwork=rows.concat(hybrid).flatMap(r=>r.methods).reduce((s,r)=>s+r.work+(r.checkWork??0),0)+random.reduce((s,r)=>s+r.r.work+r.checkWork,0);
  return {guards,rows,hybrid,random,proofs,best,imports:importFactors,overlaps,cross,carrierDimension:D,coverageNumerator:cover.toString(),coverageDenominator:(1n<<BigInt(D)).toString(),full:cover===(1n<<BigInt(D)),support,events:sumwork,execution:"deterministically interleaved five distinct lanes; no concurrent workers"};
 }
 const results=[];
 for(let alias of ["JOINT-24","RANDOM-3CNF-40"]){
  let ent=reg.instances.find(e=>e.alias==="EB-"+alias),x=corpus.instances.find(e=>e.id===alias),G=compile(x),bytes=json(G.network),map=json(G.source_map);
  if(sha(bytes)!==ent.sha256||8*bytes.length!==ent.N_bits||sha(map)!==ent.source_map_sha256||sha(x.dimacs)!==ent.source_cnf.sha256||8*x.dimacs.length!==ent.source_cnf.N_bits)throw Error("authentication mismatch "+alias);
  const n=normalize(G.network),p=project(n.F,1500000);if(p.status!=="COMPLETE")throw Error("projection cap "+alias);
  const meta={problem_id:"STRICT-EB4-v1",instance:ent.short_id,instance_id:ent.instance_id,original_N_bits:ent.N_bits,source_pin:pins,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{vertices:[0,G.network.types.length-1],ports:[0,4*G.network.types.length-1],edges:[0,G.network.edges.length-1]},parents:[]};
  const guardArtifact=[[p.gauge-1,0]],gId="GUARD-v1:sha256:"+sha(json(["PNP-GUARD-v1",ent.instance_id,"EB-PORT-PINS-v1",sha(json(guardArtifact))]));
  const mapArtifact={gauge:p.gauge,root:Array.from(n.root),par:Array.from(n.par),projection_steps:p.steps},residualHash=sha(json(p.final)),mapHash=sha(json(mapArtifact)),residual_id="RESIDUAL-v1:sha256:"+sha(json(["PNP-RESIDUAL-v1",ent.instance_id,gId,"EB-TABLE-ROOTPLUS1-v1",residualHash,mapHash]));
  let R=compare(p.final,meta,p.gauge),cnf=cnfFactors(x.dimacs);
  const cm={problem_id:"DIMACS-CNF-v1",instance:ent.source_cnf.short_id,instance_id:ent.source_cnf.instance_id,original_N_bits:ent.source_cnf.N_bits,source_pin:pins,guard_id:"EMPTY",residual_id:"ROOT",original_ids:{clauses:[1,cnf.length],variables:[1,x.nvars]},parents:[]};
  let C=compare(cnf,cm);
  results.push({alias,native:{...meta,claim:R.full?"root contradiction by checked guard cover and complement symmetry":"checked partial conditional exclusions only",proof:{chart:{gauge:p.gauge,guardArtifact,gId,residual_id,residualHash,mapHash,factorCount:p.final.length,projectionPivots:p.steps.length,normalization:n.counts,projection:p.counts},result:R}},cnf:{...cm,claim:C.full?"root contradiction by checked guard cover":"checked partial conditional exclusions only",proof:{result:C}},authenticated:{native:sha(bytes),map:sha(map),cnf:sha(x.dimacs)}});
 }
 return results;
}
console.log(JSON.stringify(experiment({compiler,corpus,registry,projection},sha,pins)));
