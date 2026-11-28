function experiment(src){
 const start=Date.now(),C=Function(src.compiler.slice(src.compiler.indexOf("function compile("),src.compiler.indexOf("function auditLocal("))+";return compile")(),H=Function(src.hybrid.split('if(typeof require==="function"')[0]+";return {sha,norm,closure,affine,unique,solve,lift,gadgetAudit}")(),B=JSON.parse(src.corpus),R=JSON.parse(src.registry);
 const assert=(b,m)=>{if(!b)throw Error(m)},enc=x=>JSON.stringify(x)+"\n",sha=x=>H.sha(typeof x==="string"?x:enc(x)),sorted=a=>[...new Set(a)].sort((a,b)=>a-b),variables=F=>sorted(F.flat().map(Math.abs)),parse=s=>s.trim().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1)),eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 assert(sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","SHA");
 const p=src.prior.slice(src.prior.indexOf(" function replayProjection("),src.prior.indexOf(" function five("));
 const helpers=Function("H","assert","eq","sorted","variables",p+";return {replayProjection,toCNF,UP,restricted,anf,affineAndBinary,separator,rup,feedback}")(H,assert,eq,sorted,variables);
 const {replayProjection,toCNF,UP,restricted,anf,affineAndBinary,separator,rup,feedback}=helpers;
 const g=src.indexed.slice(src.indexed.indexOf(" function fast("),src.indexed.indexOf(" function canon("));
 const fast=Function("assert",g+";return fast")(assert),slow=Function("assert",g.replace("if(dict.has(key))","if(false&&dict.has(key))")+";return fast")(assert);
 const toggle=(s,x)=>s.has(x)?s.delete(x):s.add(x);
 // Exact full closure of square-free Boolean calculus at degree d, not static monomial multiples.
 // Maintain a row basis. For each variable calculate kernel of degree d+1 coefficient map on current W.
 // Snapshot at each variable; iterate until no rank changes. All multiplications admitted after Boolean reduction.
 function pc(rows,V,d,cap=160000){
  let t0=Date.now(),ops=0,counts={xor:0,products:0,terms:0,projections:0,epochs:0,initial:0,admissions:0},basis=new Map(),M=[],index=new Map(),bits=[],bitIndex=new Map(),high=Array(V.length).fill(0n),mul=Array.from({length:V.length},()=>[]),constId=-1,terminal=false,peak=0;
  const tick=(k,n=1)=>{counts[k]+=n;ops+=n;if(ops>cap)throw Error("cap")};
  let n=V.length, vpos=new Map(V.map((v,i)=>[v,i])),degree=m=>{let k=0;for(let x=m;x;x&=x-1n)k++;return k};
  for(let k=d;k>=0;k--){function gen(a,j,r){if(!r){let i=M.length,b=1n<<BigInt(i);M.push(a);index.set(a,i);bits.push(b);bitIndex.set(b,i);if(!a)constId=i;return}for(let i=j;i<=n-r;i++)gen(a|(1n<<BigInt(i)),i+1,r-1)}gen(0n,0,k)}
  for(let i=0;i<n;i++)for(let j=0;j<M.length;j++){let u=M[j]|(1n<<BigInt(i)),k=index.get(u);mul[i][j]=k===undefined?null:bits[k];if(k===undefined)high[i]|=bits[j]}
  let proof=[],ids=new Map(); // stored row DAG on every pivot addition: axiom, sum, multiply
  const lb=a=>a&-a;
  function add(a,reason){let parents=[];while(a){let b=lb(a),q=basis.get(b);if(!q){let id=proof.length;proof.push({reason,parents,row:a.toString(16)});basis.set(b,{a,id});peak=Math.max(peak,basis.size);if(a===bits[constId])terminal=true;return true}tick("xor");a^=q.a;parents.push(q.id)}return false}
  function encode(terms){let a=0n;for(let t of terms){let m=0n;for(let v of t){assert(vpos.has(v),"monomial source");m|=1n<<BigInt(vpos.get(v))}let i=index.get(m);if(i===undefined)return null;a^=bits[i]}return a}
  function multiply(a,i){let b=0n;while(a){tick("terms");let k=lb(a),u=mul[i][bitIndex.get(k)];assert(u!==null,"admission degree");b^=u;a^=k}return b}
  let initialRows=rows.map(r=>encode(r.terms));if(initialRows.some(a=>a===null))return {status:"INADMISSIBLE",d,n,reason:"initial degree exceeds bound",dimension:M.length,ops:0};
  let status="UNKNOWN_CAP",lastRank=0;
  try{
   for(let i=0;i<initialRows.length;i++){tick("initial");add(initialRows[i],{axiom:i});if(terminal)break}
   if(!terminal)for(;;){counts.epochs++;let before=basis.size;for(let i=0;i<n&&!terminal;i++){
    // Each high-pivot row keeps the actual W-combination (represented by basis row IDs).
    let P=new Map(),snapshot=[...basis.values()];
    for(let row of snapshot){tick("projections");let a=row.a,b=a&high[i],parents=new Set([row.id]);
     while(b){let k=lb(b),q=P.get(k);if(!q){P.set(k,{a,b,parents});break}tick("xor");a^=q.a;b^=q.b;for(let j of q.parents){tick("terms");toggle(parents,j)}}
     if(!b){tick("products");let z=multiply(a,i);if(add(z,{mul:V[i],parents:[...parents]}))counts.admissions++;if(terminal)break}
    }
   }if(terminal)break;if(basis.size===before){status="CLOSED_NO_ONE";break}lastRank=before}
   if(terminal)status="UNSAT";
  }catch(e){if(String(e)!=="Error: cap")throw e}
  // Independent checker of all retained derivations. Reconstruct axiom source, sum/multiply and reductions.
  let checked=[],verifyTerms=0,verifyXors=0;for(let q of proof){let a=0n;if(q.reason.axiom!==undefined)a=initialRows[q.reason.axiom];else{for(let j of q.reason.parents){assert(j<checked.length,"future parent");a^=checked[j];verifyXors++}let b=0n,v=vpos.get(q.reason.mul);while(a){let k=lb(a),m=M[bitIndex.get(k)]|(1n<<BigInt(v)),idx=index.get(m);assert(idx!==undefined,"checker degree");b^=bits[idx];a^=k;verifyTerms++}a=b}for(let j of q.parents){assert(j<checked.length,"future xor");a^=checked[j];verifyXors++}assert(a===BigInt("0x"+q.row),"proof replay");checked.push(a)}
  // Dual certificate lambda evaluated on monomial basis. Solve for pivot values in reverse order.
  let dual=null,dualChecks=0,dualSupport=0;if(!terminal){let l=bits[constId],ordered=[...basis.entries()].sort((a,b)=>a[0]<b[0]?1:-1);function parity(a){let r=0;while(a){a&=a-1n;r^=1;dualChecks++}return r}for(let [b,row] of ordered){if(parity(row.a&l))l^=b}assert((l&bits[constId])!==0n,"lambda1");for(let row of basis.values())assert(!parity(row.a&l),"dual");dual=l.toString(16);let z=l;while(z){dualSupport++;z&=z-1n}}
  // Independently certify a reported fixed point with full kernel replay (same exact kernel principle, separate implementation).
  let closedCheck=null;if(status==="CLOSED_NO_ONE"){let checks=0;for(let i=0;i<n;i++){let P=new Map();for(let row of checked){let a=row,b=a&high[i];while(b){let k=lb(b);if(!P.has(k)){P.set(k,a);break}a^=P.get(k);b=a&high[i];checks++}if(!b){let z=0n;while(a){let k=lb(a);let m=M[bitIndex.get(k)]|(1n<<BigInt(i));z^=bits[index.get(m)];a^=k;checks++}while(z){let q=basis.get(lb(z));assert(q,"closure refusal kernel");z^=q.a;checks++}}}}closedCheck=checks}
  const stats={status,d,n,dimension:M.length,rank:basis.size,dualDimension:terminal?null:M.length-basis.size-1,dualSupport,dualChecks,ops,counts,peakBasisBits:peak*M.length,proofRows:proof.length,verifyTerms,verifyXors,closedCheck,ms:Date.now()-t0};
  return {stats,proof,dual};
 }
 function grouped(F){return anf(F,true,true)}
 function summaryPC(p){return p.stats??p}
 // Same gauge-free exact polynomial grouping: combine complementary guarded clauses with same scope; grouped OR equals p(x+a).
 function gaugeRows(F,a){let Y=variables(F),terms=grouped(F).table,rows=[];for(let p of terms){let out=new Set();for(let t of p.terms){toggle(out,t.join(","));if(t.length){let k=t.length;for(let m=0;m<2**k-1;m++)toggle(out,[a,...t.filter((v,i)=>m>>i&1)].sort((x,y)=>x-y).join(","))}}let T=[...out].map(k=>k?k.split(",").map(Number):[]);assert(T.every(t=>t.length<=Math.max(...p.terms.map(t=>t.length))),"gauge degree");let V=sorted([a,...p.vs]);for(let w=0;w<2**V.length;w++){let b=v=>w>>V.indexOf(v)&1, val=T.reduce((s,t)=>s^Number(t.every(v=>b(v))),0),orig=p.terms.reduce((s,t)=>s^Number(t.every(v=>b(v)^b(a))),0);assert(val===orig,"gauge identity")}rows.push({vs:V,terms:T,ids:p.ids})}return rows}
 let results=[],certs=[];
 function caseRun(I,e,controls){
  let rawcnf=I.dimacs,cnfsha=sha(rawcnf),cnfN=rawcnf.length*8,comp=C(I),G=comp.network,raw=enc(G),nativeSha=sha(raw),N=raw.length*8;assert(nativeSha===e.sha256&&N===e.N_bits&&cnfsha===e.source_cnf.sha256&&cnfN===e.source_cnf.N_bits,"auth");let S=H.norm(G),meter={n:0,cap:2000000},pins=new Map(),cl=H.closure(S.factors,pins,meter),ge=H.affine(S),P=fast(S.factors),U=slow(S.factors);assert(eq(P.trace,U.trace),"grammar trace");let replay=replayProjection(S,P.trace);assert(eq(replay.fs.map(f=>[f.id,f.vs,f.ok]),P.fs.map(f=>[f.id,f.vs,f.ok])),"projection replay");let Q=toCNF(P.fs),F=H.unique(Q.F),up=UP(F),A=restricted(F,up.p),V=variables(A),b=affineAndBinary(A),sep=separator(A),group=grouped(A),ind=anf(A,false,false);
  let c0=parse(rawcnf),cUP=UP(c0),cR=grouped(restricted(c0,cUP.p));
  let root=pc(group.table,V,3),root2=pc(group.table,V,2),gauge=pc(gaugeRows(F,S.gauge),variables(F).concat(S.gauge).sort((a,b)=>a-b),3),r=rup(A,100000),tree;
  try{let t=H.solve(A,400000);let t2=H.solve(A,400000,t.tree);tree={status:"UNSAT",nodes:t.nodes,reads:t.scans,replay:t2.scans,tree:t.tree}}catch(err){tree={status:"UNKNOWN",error:String(err)}}
  let cnt=new Map();for(let c of F)for(let l of c)cnt.set(Math.abs(l),(cnt.get(Math.abs(l))??0)+1);let sel=V.slice().sort((a,b)=>cnt.get(b)-cnt.get(a)||a-b).slice(0,4),guards=sel.map((v,i)=>sel.slice(0,i).concat(-v)).concat([sel]),cover=0;
  for(let m=1;m<32;m++){let s=new Map(),ok=true,par=0;for(let i=0;i<5;i++)if(m>>i&1){par^=1;for(let l of guards[i]){let v=Math.abs(l),a=Number(l>0);if(s.has(v)&&s.get(v)!==a)ok=false;s.set(v,a)}}if(ok)cover+=(par?1:-1)*2**(4-s.size)}assert(cover===16,"guard coverage");
  let gr=[],first=null;for(let g of guards){let u=UP(F,g);if(u.conflict){gr.push({g,UP:"UNSAT",reads:u.reads,pins:u.p.size});continue}let A=restricted(F,u.p),W=variables(A),a=affineAndBinary(A),s=separator(A),z=grouped(A),p=pc(z.table,W,3,100000),r=rup(A,60000);let o={g,UP:"UNKNOWN",reads:u.reads,pins:u.p.size,variables:W.length,clauses:A.length,affine:a,separator:s,pc:summaryPC(p),rup:{status:r.status,reads:r.reads,learned:r.learned.length}};if(!first)first={g,A};gr.push(o)}
  let fb=first?[2,4].map(w=>({width:w,arms:["baseline","table","residue"].map(mode=>({mode,...feedback(F,first.g,mode,150000,w)}))})):null;
  const map={gauge:S.gauge,projection:P.trace,rootPins:[...up.p]},guardArtifact=[[S.gauge-1,0]],gid="GUARD-v1:sha256:"+sha(["PNP-GUARD-v1",e.instance_id,"EB-PORT-PINS-v1",sha(guardArtifact)]),rid="RESIDUAL-v1:sha256:"+sha(["PNP-RESIDUAL-v1",e.instance_id,gid,"T3-GRAMMAR-CNF-v1",sha(A),sha(map)]);
  let cert={schema:"T3-PC-CLOSURE-v1",problem_id:"STRICT-EB4-v1",instance:e.short_id,instance_id:e.instance_id,original_N_bits:N,source_pin:"registry 0c14cdc57925788cf7a451dcd5aa171dce860f2c; compiler 21b9d53fb8166c819b24e708656c742cd3c24f10; corpus e315349cd6c1fe3fa696504859f28312f6aab69a",guard_id:gid,residual_id:rid,original_ids:{vertices:[0,G.types.length-1],ports:[0,4*G.types.length-1],edges:[0,G.edges.length-1]},parents:[],guardArtifact,map,chart:A,rows:group.table,degree:3,pc:root,rootTree:tree,claim:"bounded PC derivations and dual fixed span at named cap; closure refusal only if CLOSED_NO_ONE, no unrestricted hardness"};
  let s=enc(cert);certs.push({id:I.id,content:s,sha:sha(s)});
  results.push({id:I.id,N,nativeSha,cnfN,cnfsha,gid,rid,sourceMapHash:sha(comp.source_map),initial:{roots:S.roots,factors:S.factors.length,local:cl?"UNKNOWN":"UNSAT",pins:pins.size,checks:meter.n,affine:ge},grammar:{steps:P.trace.length,cache:P.counts.wordTests,uncached:U.counts.wordTests,replayWords:replay.words,entries:P.entries,counts:P.counts},post:{n:V.length,clauses:A.length,pins:up.p.size,UP:up.reads,groupRows:group.rows,groupDegree:group.counts.degree,individualDegree:ind.counts.degree,individualRank:ind.rank,groupRank:group.rank,affineBinary:b,separator:safe(sep)},rootPC2:summaryPC(root2),rootPC3:summaryPC(root),gaugePC3:summaryPC(gauge),rup:{status:r.status,reads:r.reads,learned:r.learned.length},tree:{status:tree.status,nodes:tree.nodes,reads:tree.reads,replay:tree.replay},guardCoverage:cover,guards:gr,feedback:fb,companion:{earlyPins:cUP.p.size,reads:cUP.reads,groupStatus:cR.status,degree:cR.counts?.degree},certificateSha:sha(s)})
 }
 function safe(x){return x}
 for(let id of ["JOINT-24","RANDOM-3CNF-40"]){caseRun(B.instances.find(x=>x.id===id),R.instances.find(x=>x.alias==="EB-"+id),true)}
 // Non-affine, triple-packing NAE4 controls. One randomized deterministic shuffle per n/seed; exact label via exhaustive check.
 function packing(n,seed){
  let a=[];for(let i=1;i<=n;i++)for(let j=i+1;j<=n;j++)for(let k=j+1;k<=n;k++)for(let l=k+1;l<=n;l++)a.push([i,j,k,l]);
  let rng=seed>>>0;for(let i=a.length-1;i>0;i--){rng=(Math.imul(rng,1664525)+1013904223)>>>0;let j=rng%(i+1);[a[i],a[j]]=[a[j],a[i]]}
  let seen=new Set(),E=[];for(let t of a){let q=t.map((_,i)=>t.filter((_,j)=>i!==j).join(","));if(q.some(k=>seen.has(k)))continue;q.forEach(k=>seen.add(k));E.push(t)}
  let masks=E.map(t=>t.reduce((s,v)=>s|(1<<(v-1)),0)),sat=0,first=null,checks=0;
  for(let x=0;x<2**n;x++){let good=true;for(let m of masks){checks++;let y=m&x;if(y===0||y===m){good=false;break}}if(good){sat++;if(first===null)first=x}}
  let F=E.flatMap(t=>[t,t.map(v=>-v)]),dimacs=`p cnf ${n} ${F.length}\n`+F.map(c=>c.join(" ")+" 0\n").join(""),G=grouped(F),P=pc(G.table,variables(F),3,300000);
  // direct analytic full-PC refusal: each cubic appears in precisely one row and each row has cubic avoiding each multiplier.
  let cubics=new Map();for(let [i,r] of G.table.entries())for(let t of r.terms.filter(t=>t.length===3)){let k=t.join(",");assert(!cubics.has(k),"triple uniqueness");cubics.set(k,i)}
  let uniqueChecks=0;for(let r of G.table)for(let v=1;v<=n;v++){assert(r.terms.some(t=>t.length===3&&!t.includes(v)),"private leading cubic");uniqueChecks++}
  assert(G.rank===E.length&&!G.proof,"span");let dual=new Set([""]);for(let r of G.table){let t=r.terms.find(t=>t.length===3);dual.add(t.join(","))}for(let r of G.table)assert(r.terms.reduce((s,t)=>s^Number(dual.has(t.join(","))),0)===0,"explicit dual");
  return {n,seed,E,F,dimacs,cnfSha:sha(dimacs),cnfN:dimacs.length*8,sat,first,checks,uniqueChecks,rank:G.rank,pc:summaryPC(P),explicitDual:[...dual],groupedRows:G.table}
 }
 let cases=[];for(let [n,seed] of [[16,20261127],[18,20261128]]){let x=packing(n,seed);cases.push(x)}
 // Native grammar transfer of both controls: source-only projection; compare source signed carrier map afterward.
 let native=[];
 for(let x of cases){let I={id:`PACK-${x.n}-${x.seed}`,nvars:x.n,dimacs:x.dimacs},comp=C(I),G=comp.network,raw=enc(G),S=H.norm(G),M={n:0,cap:2000000},pins=new Map(),local=H.closure(S.factors,pins,M),ge=H.affine(S),P=fast(S.factors),rep=replayProjection(S,P.trace),Q=toCNF(P.fs),F=H.unique(Q.F),grp=grouped(F),V=variables(F),p=pc(grp.table,V,3,160000);assert(eq(rep.fs.map(f=>[f.id,f.vs,f.ok]),P.fs.map(f=>[f.id,f.vs,f.ok])),"native packing replay");
  let signed=new Map();for(let i=1;i<=x.n;i++){let [port,s]=comp.source_map.representative_ports["x"+i],v=S.r[port]+1,bit=s^S.p[port];signed.set(i,bit?-v:v)}let translated=H.unique(x.F.map(c=>c.map(l=>Math.sign(l)*signed.get(Math.abs(l))))),key=f=>f.map(c=>c.join(",")).sort();let exact=eq(key(translated),key(F));
  // If native compiler image has extra auxiliaries, no claim of direct equality, no automatic proof transfer.
  let L=H.lift(x.F),bits="1".repeat(L.n)+"0",gamma=(L.m+1).toString(2);bits+="0".repeat(gamma.length-1)+gamma;let w=Math.ceil(Math.log2(L.n+1));for(let c of L.R)for(let v of c)bits+=v.toString(2).padStart(w,"0");assert(bits.length===L.N,"T5 size");let bytes="";for(let i=0;i<bits.length;i+=8)bytes+=String.fromCharCode(parseInt(bits.slice(i,i+8).padEnd(8,"0"),2));
  let m={id:I.id,cnfSha:x.cnfSha,cnfN:x.cnfN,nativeSha:sha(raw),nativeN:raw.length*8,sourceMapSha:sha(comp.source_map),vertices:G.types.length,edges:G.edges.length,gauge:S.gauge,roots:S.roots,initial:{local:local?"UNKNOWN":"UNSAT",pins:pins.size,checks:M.n,ge},grammar:{steps:P.trace.length,cached:P.counts.wordTests,replayWords:rep.words,entries:P.entries},residual:{variables:V.length,clauses:F.length,groupedDegree:grp.counts.degree,groupedRows:grp.rows,exactSignedMapMatch:exact},pc:summaryPC(p),t5:{n:L.n,m:L.m,logicalN:L.N,packedN:bytes.length*8,sha:sha(bytes),gadget:H.gadgetAudit()},sourceSat:x.sat,sourceWitness:x.first,guard:"EMPTY",residualId:"ROOT"};
  native.push(m)
 }
 return {results,certs,cases,native,elapsed:Date.now()-start}
}
if(typeof require==='function'){let fs=require('fs'),keys=['compiler','corpus','registry','hybrid','indexed','prior'];let src=Object.fromEntries(keys.map((k,i)=>[k,fs.readFileSync(process.argv[i+2],'utf8')]));console.log(JSON.stringify(experiment(src),null,2));}
