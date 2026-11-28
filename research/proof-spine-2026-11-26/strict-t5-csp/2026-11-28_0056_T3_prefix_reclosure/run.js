function run(s){
const C=Function(s.compiler.slice(s.compiler.indexOf("function compile("),s.compiler.indexOf("function auditLocal("))+";return compile")(),H=Function(s.hybrid.split('if(typeof require==="function"')[0]+";return {sha,norm,closure,affine,unique,solve}")(),B=JSON.parse(s.corpus),R=JSON.parse(s.registry),assert=(a,m)=>{if(!a)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b),enc=x=>JSON.stringify(x)+"\n",sha=x=>H.sha(typeof x==="string"?x:enc(x)),sorted=a=>[...new Set(a)].sort((a,b)=>a-b),variables=F=>sorted(F.flat().map(Math.abs)),toggle=(s,k)=>s.has(k)?s.delete(k):s.add(k);
assert(sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","sha");
const pc=Function("assert","toggle",s.runner.slice(s.runner.indexOf(" function pc("),s.runner.indexOf(" function grouped("))+";return pc")(assert,toggle);
const fast=Function("assert",s.indexed.slice(s.indexed.indexOf(" function fast("),s.indexed.indexOf(" function canon("))+";return fast")(assert);
const slow=Function("assert",s.indexed.slice(s.indexed.indexOf(" function fast("),s.indexed.indexOf(" function canon(")).replace("if(dict.has(key))","if(false&&dict.has(key))")+";return fast")(assert);
const helpers=Function("H","assert","eq","sorted","variables",s.prior.slice(s.prior.indexOf(" function replayProjection("),s.prior.indexOf(" function five("))+";return {replayProjection,toCNF,UP,restricted,anf,affineAndBinary,separator,rup,feedback}")(H,assert,eq,sorted,variables);
const {replayProjection,toCNF,UP,restricted,anf,affineAndBinary,separator,rup,feedback}=helpers;
let out=[],cert=null;
function poly(c){let p=new Set([""]);for(let l of c){let q=new Set();for(let t of p){let u=sorted((t?t.split(",").map(Number):[]).concat(Math.abs(l))).join(",");toggle(q,u);if(l>0)toggle(q,t)}p=q}return {terms:[...p].map(t=>t?t.split(",").map(Number):[])}}
function chkPC(F,V,rows,P){
 const M=[];for(let k=3;k>=0;k--){function gen(a,j,r){if(!r){M.push(a.join(","));return}for(let i=j;i<=V.length-r;i++)gen(a.concat(V[i]),i+1,r-1)}gen([],0,k)}
 let idx=new Map(M.map((m,i)=>[m,i])),decode=s=>{let a=BigInt("0x"+s),out=new Set();for(let i=0;a;i++,a>>=1n)if(a&1n)out.add(M[i]);return out},add=(p,q)=>{for(let k of q)toggle(p,k)},mul=(p,v)=>{let q=new Set();for(let t of p){let a=sorted((t?t.split(",").map(Number):[]).concat(v));assert(a.length<=3,"degree");toggle(q,a.join(","))}return q},low=p=>[...p].reduce((a,b)=>a===null||idx.get(b)<idx.get(a)?b:a,null);
 const A=assert;
 const verifier=Function("A","eq","sort","V","decode","add","mul","low","M",s.audit.slice(s.audit.indexOf(" function verify(pc,rows)"),s.audit.indexOf(" let check=verify("))+";return verify")(A,eq,sorted,V,decode,add,mul,low,M);
 return verifier(P,rows).summary
}
function replay(F,seq,skip=-1){
 let db=F.slice(),vis=0,admitted=[],failed=null;for(let i=0;i<seq.length;i++){if(i===skip)continue;let c=seq[i],u=UP(db,c.map(l=>-l));vis+=u.reads;if(!u.conflict){failed=i+1;break}db.push(c);admitted.push(c)}
 return {db,vis,admitted,failed}
}
for(const [key,id] of [["joint","JOINT-24"],["random","RANDOM-3CNF-40"]]){
 let t0=Date.now(),I=B.instances.find(x=>x.id===id),e=R.instances.find(x=>x.alias==="EB-"+id),G=C(I),raw=enc(G.network);
 assert(sha(raw)===e.sha256&&raw.length*8===e.N_bits&&sha(I.dimacs)===e.source_cnf.sha256&&I.dimacs.length*8===e.source_cnf.N_bits&&sha(G.source_map)===e.source_map_sha256,"auth");
 let S=H.norm(G.network),M={n:0,cap:2000000},pins=new Map(),local=H.closure(S.factors,pins,M),ge=H.affine(S);
 let P=fast(S.factors),U=slow(S.factors);assert(eq(P.trace,U.trace),"fresh grammar trace");let Q=replayProjection(S,P.trace);assert(eq(Q.fs.map(f=>[f.id,f.vs,f.ok]),P.fs.map(f=>[f.id,f.vs,f.ok])),"projection");
 let F=H.unique(toCNF(P.fs).F),u=UP(F),V=variables(F);assert(!u.conflict&&u.p.size===0,"root UP");
 let old=JSON.parse(s[key]);assert(old.instance_id===e.instance_id&&old.original_N_bits===e.N_bits&&old.map.gauge===S.gauge&&eq(old.map.projection,P.trace)&&eq(old.chart,F),"exact chart");
 let group=anf(F,true,true),groupChecks=0;for(let row of old.rows){for(let w=0;w<2**row.vs.length;w++){let b=v=>w>>row.vs.indexOf(v)&1;assert(row.terms.reduce((s,t)=>s^Number(t.every(b)),0)===Number(!row.ids.every(i=>F[i].some(l=>b(Math.abs(l))===Number(l>0)))),"ANF");groupChecks++}}assert(eq(old.rows,group.table),"group exact");
 let a=affineAndBinary(F),sep=separator(F),root=pc(group.table,V,3,150000),source=rup(F,150000),tree=H.solve(F,300000),treecheck=H.solve(F,300000,tree.tree);
 let co=I.dimacs.trim().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1)),cu=UP(co),ct=H.solve(co,300000);H.solve(co,300000,ct.tree);
 let sel=V.slice().sort((a,b)=>F.filter(c=>c.includes(b)||c.includes(-b)).length-F.filter(c=>c.includes(a)||c.includes(-a)).length||a-b).slice(0,4),guards=sel.map((v,i)=>sel.slice(0,i).concat(-v)).concat([sel]),covered=0;
 for(let m=1;m<32;m++){let p=new Map(),ok=true,k=0;for(let i=0;i<5;i++)if(m>>i&1){k++;for(let l of guards[i]){let v=Math.abs(l),b=Number(l>0);if(p.has(v)&&p.get(v)!==b)ok=false;p.set(v,b)}}if(ok)covered+=(k%2?1:-1)*2**(4-p.size)}assert(covered===16,"cover");
 let lanes=[];for(let g of guards){let u=UP(F,g);if(u.conflict){lanes.push({g,UP:"UNSAT",reads:u.reads});continue}let f=restricted(F,u.p),v=variables(f),h=anf(f,true,true);let pc1=pc(h.table,v,3,40000),r=rup(f,30000);lanes.push({g,UP:"UNKNOWN",reads:u.reads,variables:v.length,clauses:f.length,affine:affineAndBinary(f),separator:separator(f),pc:pc1.stats??pc1,rup:{status:r.status,reads:r.reads,learned:r.learned.length}})}
 let g=lanes.find(x=>x.UP==="UNKNOWN")?.g,fb=g?[2,4].map(w=>({width:w,arms:["baseline","table","residue"].map(mode=>({mode,...feedback(F,g,mode,100000,w)}))})):null;
 let o={id,sha:e.sha256,N:e.N_bits,guard:old.guard_id,residual:old.residual_id,certSha:sha(s[key]),native:{roots:S.roots,factors:S.factors.length,closure:local,pins:pins.size,localChecks:M.n,ge},grammar:{steps:P.trace.length,cached:P.counts.wordTests,uncached:U.counts.wordTests,replay:Q.words,entries:P.entries},chart:{n:V.length,m:F.length,up:u.reads,groupChecks},affine:a,separator:sep,rootPC:root.stats??root,blindRUP:{status:source.status,reads:source.reads,learned:source.learned.length},tree:{nodes:tree.nodes,reads:tree.scans,replay:treecheck.scans},companion:{N:e.source_cnf.N_bits,sha:e.source_cnf.sha256,pins:cu.p.size,reads:cu.reads,nodes:ct.nodes,treeReads:ct.scans},guards:lanes,cover:covered,feedback:fb};
 if(key==="random"){
  assert(sha(s.random)==="ed4d5336bf89902532fc422331a620007f6fb1f2bae2d89fb496d7c78dd36f2e","old cert sha");
  o.oldReplay=chkPC(F,V,old.rows,old.pc);assert(root.stats.status==="CLOSED_NO_ONE"&&root.stats.rank===old.pc.stats.rank,"fresh PC fixed point");
  let peer=JSON.parse(s.peer),peerSha=sha(s.peer);assert(peerSha==="6e51eff6a61d59e11420002279e5e3a89acff9178ff3c1f6680c557553bb23ad"&&peer.instance_id===e.instance_id&&peer.internal_guard===old.guard_id,"peer identity");
  let seq=peer.proof.slice(0,peer.prefixLength).map(c=>c.map(l=>Math.sign(l)*peer.dense_to_original_port_plus1[Math.abs(l)-1]));assert(seq.every(c=>c.length<=2&&c.every(l=>V.includes(Math.abs(l)))),"map");let rp=replay(F,seq);assert(rp.failed===null,"local RUP");let tested=[],witnesses=[];
  for(let k of [1,3,8,32,164]){let r=pc(group.table.concat(seq.slice(0,k).map(poly)),V,3,120000);tested.push({k,...r.stats});if(r.stats.status==="CLOSED_NO_ONE")tested[tested.length-1].independent=chkPC(F,V,group.table.concat(seq.slice(0,k).map(poly)),r);witnesses.push({k,pc:r})}
  let ablations=[];for(let i=0;i<3;i++){let r=replay(F,seq,i);ablations.push({skip:i+1,admitted:r.admitted.length,failed:r.failed,reads:r.vis})}
  // Fixed-chart graph: verify first contradictory binary prefix via independent reachability.
  let signed=V.flatMap(v=>[v,-v]),idx=new Map(signed.map((v,i)=>[v,i])),reach=signed.map((v,i)=>1n<<BigInt(i)),changes=0,ops=0,first=null;
  function arc(u,v){let i=idx.get(u),j=idx.get(v),a=1n<<BigInt(i),b=reach[j];for(let x=0;x<reach.length;x++){ops++;if(reach[x]&a){let d=b&~reach[x];while(d){changes++;d&=d-1n}reach[x]|=b}}}
  for(let [i,c] of seq.entries()){if(c.length===1)arc(-c[0],c[0]);else {arc(-c[0],c[1]);arc(-c[1],c[0])}let v=V.find(v=>(reach[idx.get(v)]&(1n<<BigInt(idx.get(-v))))&&(reach[idx.get(-v)]&(1n<<BigInt(idx.get(v)))));if(v!==undefined&&first===null)first={prefix:i+1,carrier:v}}
  assert(first!==null,"binary terminal");
  o.activation={peerSha,peerRows:seq.length,localReplayReads:rp.vis,prefixes:tested,ablations,graph:{first,changes,ops},producerDiscovery:peer.discovery};
  cert={schema:"T3-PC3-prefix-reclosure-v1",problem_id:old.problem_id,instance:old.instance,instance_id:old.instance_id,original_N_bits:old.original_N_bits,source_pin:old.source_pin,guard_id:old.guard_id,residual_id:old.residual_id,original_ids:old.original_ids,parents:["CERT-v1:sha256:"+sha(s.random),"CERT-v1:sha256:"+peerSha],claim:"exact old PC3 refusal replay and locally rederived binary prefix reclosure, scoped to this chart",peerDenseMap:peer.dense_to_original_port_plus1,seq,baseline:root,witnesses,graph:o.activation.graph,ablation:ablations};
 }
 o.ms=Date.now()-t0;out.push(o);
}
return {out,cert}
}
if(typeof require==='function'){let fs=require('fs'),keys=["compiler","corpus","registry","hybrid","runner","audit","joint","random","indexed","prior","peer"];let s=Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]));console.log(JSON.stringify(run(s),null,2));}
