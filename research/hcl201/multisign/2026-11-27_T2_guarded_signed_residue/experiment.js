const fs=require('node:fs');
const specs=[
  [
    "21b9d53fb8166c819b24e708656c742cd3c24f10",
    "research/coordination/shared-eb-2026-11-27/compile.js"
  ],
  [
    "e315349cd6c1fe3fa696504859f28312f6aab69a",
    "research/coordination/shared-unsat-2026-11-27/benchmarks.json"
  ],
  [
    "0c14cdc57925788cf7a451dcd5aa171dce860f2c",
    "research/coordination/shared-eb-2026-11-27/instance-registry-v1.json"
  ],
  [
    "a830475f2d7b927fe3897079af04ebb99c82106b",
    "research/hcl201/matching/2026-11-27_T1_hall_clause_feedback/experiment.js"
  ],
  [
    "d7cb4c38ee4dc1df3378177b716cd0d238d0e4db",
    "research/hcl201/interfaces/2026-11-27_T2_quadratic_response/experiment.js"
  ],
  [
    "18cef3300d462b73dd537b399929bae5bce8c261",
    "research/hcl201/matching/2026-11-27_T1_five_guard_cover_rank/EB-JOINT-24-certificate.json"
  ],
  [
    "a1915fee03fc538094509ceb07d49246fe32be52",
    "research/hcl201/matching/2026-11-27_T1_five_guard_cover_rank/EB-RANDOM-3CNF-40-certificate.json"
  ]
];
function run(inputs){
 const [co,corpus,reg,base,quadcode,...peers]=inputs, A=(b,m)=>{if(!b)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
 const compile=Function(co.slice(co.indexOf("function compile("),co.indexOf("function auditLocal"))+";return compile")(), {sha,normalize,independentNormalize,eliminate,verifyTrace,gauge}=Function(base.slice(0,base.indexOf("function runCase"))+";return {sha,normalize,independentNormalize,eliminate,verifyTrace,gauge}")();
 const quad=Function(quadcode.slice(quadcode.indexOf(" function lane("),quadcode.indexOf(" let shared=[]"))+";return lane")();
 A(sha("")==="e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"&&sha("abc")==="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad","sha vectors");
 const bytes=x=>JSON.stringify(x)+"\n", bit=i=>1n<<BigInt(i), hi=x=>x.toString(2).length-1;
 function basis(){let B=new Map(),xor=0;return {B,add(x){while(x){let h=hi(x);if(!B.has(h)){B.set(h,x);return true}x^=B.get(h);xor++}return false},get xor(){return xor}}}
 function restrict(F,guard){let a=new Map(guard.map(l=>[Math.abs(l),+(l>0)]));return F.map(f=>{let vs=f.vs.filter(v=>!a.has(v));return {...f,vs,ok:[...new Set(f.ok.filter(w=>f.vs.every((v,i)=>!a.has(v)||a.get(v)===(w>>i&1))).map(w=>vs.reduce((z,v,i)=>z|((w>>f.vs.indexOf(v)&1)<<i),0)))].sort((a,b)=>a-b)}})}
 function gac(F,a=new Map(),s={reads:0}){for(;;){let ch=false,R=[];for(let f of F){let ok=f.ok.filter(w=>{s.reads++;return f.vs.every((v,i)=>!a.has(v)||a.get(v)===(w>>i&1))});if(!ok.length)return null;R.push({...f,ok});for(let i=0;i<f.vs.length;i++)if(!a.has(f.vs[i])&&ok.every(w=>(w>>i&1)===(ok[0]>>i&1))){a.set(f.vs[i],ok[0]>>i&1);ch=true}}if(!ch)return R}}
 function cnf(F){let C=[];for(let f of F)for(let w=0;w<2**f.vs.length;w++)if(!f.ok.includes(w))C.push({c:f.vs.map((v,i)=>(w>>i&1)?-v:v),support:f.support||f.ids||[]});return C}
 function dag(F,cap=120000){let C=cnf(F),s={reads:0,nodes:0},support=new Set();function visit(a){s.nodes++;for(;;){let ch=false;for(let {c,support:ids} of C){if(++s.reads>cap)throw Error("cap");if(c.some(l=>a.get(Math.abs(l))===+(l>0)))continue;let u=c.filter(l=>!a.has(Math.abs(l)));if(!u.length){for(let i of ids)support.add(i);return null}if(u.length===1){a.set(Math.abs(u[0]),+(u[0]>0));for(let i of ids)support.add(i);ch=true}}if(!ch)break}
 let M=new Map();for(let {c}of C)if(!c.some(l=>a.get(Math.abs(l))===+(l>0)))for(let l of c)if(!a.has(Math.abs(l)))M.set(Math.abs(l),(M.get(Math.abs(l))||0)+1);if(!M.size)throw Error("SAT-or-empty");let v=[...M].sort((a,b)=>b[1]-a[1]||a[0]-b[0])[0][0];let b=new Map(a);b.set(v,0);let left=visit(b);b=new Map(a);b.set(v,1);return [v,left,visit(b)]}
 try{let tree=visit(new Map());return {status:"UNSAT",tree,support:[...support].sort((a,b)=>a-b),...s}}catch(e){if(String(e).includes("cap")||String(e).includes("SAT-or-empty"))return {status:"UNKNOWN",reason:String(e),...s};throw e}}
 function check(F,tree){let C=cnf(F),reads=0;function visit(a,t){while(true){let changed=false;for(let {c}of C){reads++;let hit=false,un=[];for(let l of c){if(!a.has(Math.abs(l)))un.push(l);else if(a.get(Math.abs(l))===+(l>0)){hit=true;break}}if(hit)continue;if(!un.length)return true;if(un.length===1){a.set(Math.abs(un[0]),+(un[0]>0));changed=true;break}}if(!changed)break}if(!Array.isArray(t)||a.has(t[0]))return false;let x=new Map(a),y=new Map(a);x.set(t[0],0);y.set(t[0],1);return visit(x,t[1])&&visit(y,t[2])}return {valid:visit(new Map(),tree),reads}}
 function bij(F){let s={reads:0},a=new Map(),R=gac(F,a,s);if(!R)return {status:"UNSAT",...s};let adj=new Map(),edges=0;function add(u,v){if(!adj.has(u))adj.set(u,new Set());adj.get(u).add(v);edges++}function clause(u,v){add(-u,v);add(-v,u)}
 for(let [v,b]of a)clause(b?v:-v,b?v:-v);for(let f of R)for(let i=0;i<f.vs.length;i++)for(let j=i+1;j<f.vs.length;j++)for(let w=0;w<4;w++){s.reads+=f.ok.length;if(!f.ok.some(z=>((z>>i&1)+2*(z>>j&1))===w))clause((w&1)?-f.vs[i]:f.vs[i],(w&2)?-f.vs[j]:f.vs[j])}
 function reach(u,v){let q=[u],S=new Set(q);for(let x of q){if(x===v)return true;for(let y of adj.get(x)||[]){s.reads++;if(!S.has(y)){q.push(y);S.add(y)}}}return false}
 for(let v of new Set(F.flatMap(f=>f.vs)))if(reach(v,-v)&&reach(-v,v))return {status:"UNSAT",edges,...s};return {status:"UNKNOWN",edges,...s}}
 function join(F){let s={reads:0,joins:0,declines:0},a=new Map(),P=gac(F,a,s);if(!P)return {status:"UNSAT",...s};P=restrict(P,[...a].map(([v,b])=>b?v:-v));while(P.length){if(P.some(f=>!f.ok.length))return {status:"UNSAT",...s};let m=new Map();for(let f of P)for(let v of f.vs){if(!m.has(v))m.set(v,[]);m.get(v).push(f)}if(!m.size)return {status:"UNKNOWN",...s};let L=[...m].map(([v,fs])=>({v,fs,U:[...new Set(fs.flatMap(f=>f.vs))].sort((a,b)=>a-b)})).sort((a,b)=>a.U.length-b.U.length||a.v-b.v);let {v,fs,U}=L[0];if(U.length>7||s.reads>90000)return {status:"UNKNOWN",width:U.length,...s};let V=U.filter(x=>x!==v),ok=new Set();for(let w=0;w<2**U.length;w++){let good=true;for(let f of fs){s.reads++;let q=f.vs.reduce((z,x,i)=>z|((w>>U.indexOf(x)&1)<<i),0);if(!f.ok.includes(q)){good=false;break}}if(good)ok.add(V.reduce((z,x,i)=>z|((w>>U.indexOf(x)&1)<<i),0))}P=P.filter(f=>!fs.includes(f));P.push({vs:V,ok:[...ok]});s.joins++}return {status:"UNKNOWN",...s}}
 function lanes(F,g){let R=restrict(F,g),s={reads:0},occ=gac(R,new Map(),s);let q=quad(R,true,0,false),b=bij(R),j=join(R),d=dag(R);return {guard:g,occupancy:{status:occ?"UNKNOWN":"UNSAT",...s},quadratic:{status:q.status,stats:q.stats,initial:q.initial},bijunctive:b,separator:j,dag:d}}
 // Complement of k pin guards: union of flats, one contradicted pin per guard. 
 function response(V,guards){let n=V.length,idx=new Map(V.map((v,i)=>[v,i])),D=1+n+n*(n-1)/2,B=basis(),L=basis(),flats=new Map(),points=0;
 function rec(i,a){if(i===guards.length){let key=[...a].sort((a,b)=>a[0]-b[0]).map(x=>x.join(":")).join(",");flats.set(key,new Map(a));return}for(let l of guards[i]){let v=idx.get(Math.abs(l)),b=+(l<0);if(v===undefined)throw Error("guard carrier");if(a.has(v)&&a.get(v)!==b)continue;let z=new Map(a);z.set(v,b);rec(i+1,z)}}rec(0,new Map());
 function ev(w){let z=1n;for(let i=0;i<n;i++)if(w&bit(i))z|=bit(i+1);L.add(z);let k=n+1;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++,k++)if((w&bit(i))&&(w&bit(j)))z|=bit(k);B.add(z);points++}
 for(let a of flats.values()){let w=0n,free=[];for(let i=0;i<n;i++){if(a.has(i)){if(a.get(i))w|=bit(i)}else free.push(i)}ev(w);for(let i of free)ev(w^bit(i));for(let i=0;i<free.length;i++)for(let j=i+1;j<free.length;j++)ev(w^bit(free[i])^bit(free[j]))}
 let counts=[],cover=0n;for(let mask=1;mask<2**guards.length;mask++){let a=new Map(),ok=true,k=0;for(let i=0;i<guards.length;i++)if(mask>>i&1){k++;for(let l of guards[i]){let v=Math.abs(l),b=+(l>0);if(a.has(v)&&a.get(v)!==b)ok=false;a.set(v,b)}}let c=ok?bit(n-a.size):0n;cover+=k%2?c:-c;counts.push([mask,c.toString()])}
 return {n,D,flats:flats.size,points,rank:B.B.size,affineRank:L.B.size,quadraticNullity:D-B.B.size,affineNullity:n+1-L.B.size,xors:B.xor+L.xor,covered:cover.toString(),total:bit(n).toString(),counts}
 }
 function policy(F){let V=[...new Set(F.flatMap(f=>f.vs))],m=new Map(V.map(v=>[v,F.filter(f=>f.vs.includes(v)).length])),[u,v,w]=V.sort((a,b)=>m.get(b)-m.get(a)||a-b);return [[-u,-v],[-u,v],[u,-v],[u,v,-w],[u,v,w]]}
 function supports(F,trace){let M=new Map(F.map(f=>[f.id,f.ids||[]]));for(let t of trace)M.set(t.out,[...new Set(t.in.flatMap(i=>M.get(i)||[]))]);return M}
function feedback(F,g,mode,width,cap=10000){
 const start=Date.now(),R=restrict(F,g), pins=new Map(),s={reads:0};if(!gac(R,pins,s))return {mode,width,stage:"early contradiction",status:"UNSAT",early:s.reads,ms:Date.now()-start};
 let orig=cnf(R).map(x=>x.c.slice().sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b)),C=orig.slice(),V=[...new Set(R.flatMap(f=>f.vs))].filter(v=>!pins.has(v)).sort((a,b)=>a-b),learn=[],pairs=0,verify=0,flips=[],evals=0,changed=0,peakRows=C.length,peakLiterals=C.flat().length;
 const key=c=>c.join(","),seen=new Set(C.map(key));
 function score(a){let bad=0,zero=0,collisions=0,fields=[];for(let c of C){let k=0,sum=0;for(let l of c){evals++;if(a.get(Math.abs(l))===+(l>0)){k++;sum+=l>0?1:-1}}let r=k%3,z=(sum%3+3)%3;fields.push([k,r,z]);if(k===0)bad++;if(k>0&&z===0)zero++;if(k===3)collisions++}return {bad,zero,collisions,fields}}
 function greedy(init,phase){let a=new Map(V.map(v=>[v,init]));for(let [v,b]of pins)a.set(v,b);let first=score(a),cur=first,steps=[];for(let t=0;t<V.length;t++){let cand=[];for(let v of V){a.set(v,1-a.get(v));let q=score(a);a.set(v,1-a.get(v));if(q.bad<cur.bad)cand.push({v,bad:q.bad,zero:q.zero})}if(!cand.length)break;cand.sort((a,b)=>a.bad-b.bad||a.v-b.v);let plain=cand[0];if(mode==="residue")cand.sort((a,b)=>a.bad-b.bad||a.zero-b.zero||a.v-b.v);let q=cand[0];if(q.v!==plain.v)changed++;a.set(q.v,1-a.get(q.v));let next=score(a);if(!(next.bad<cur.bad))throw Error("nonimprovement");steps.push([q.v,cur.bad,next.bad,plain.v]);cur=next;}flips.push({init,phase,start:first.bad,end:cur.bad,steps,initialFields:first.fields,finalFields:cur.fields});}
 if(["flips","table","residue"].includes(mode)){greedy(0,"before");greedy(1,"before")}
 if(["deductions","table","residue"].includes(mode)){
  outer:for(let i=0;i<C.length;i++)for(let j=0;j<i;j++){if(pairs>=cap||learn.length>=64)break outer;pairs++;for(let p of C[i])if(C[j].includes(-p)){let d=[...new Set([...C[i].filter(x=>x!==p),...C[j].filter(x=>x!==-p)])].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);if(d.length>width||d.some(l=>d.includes(-l))||seen.has(key(d)))continue;
   // Independent resolution check: every falsifying assignment to the resolvent falsifies one parent for either pivot value.
   for(let b=0;b<2;b++){let a=new Map(d.map(l=>[Math.abs(l),+(l<0)]));a.set(Math.abs(p),b);verify++;if([C[i],C[j]].every(c=>c.some(l=>a.get(Math.abs(l))===+(l>0))))throw Error("resolution replay")}
   learn.push({i,j,p,d});C.push(d);seen.add(key(d));if(learn.length>=64)break outer;
  }}
  peakRows=Math.max(peakRows,C.length);peakLiterals=Math.max(peakLiterals,C.flat().length);
  if(mode!=="deductions"){greedy(0,"after");greedy(1,"after")}
 }
 let extra=learn.map(({d},i)=>({id:-1000-i,vs:d.map(Math.abs),ok:Array.from({length:2**d.length},(_,w)=>w).filter(w=>d.some((l,j)=>(w>>j&1)===+(l>0))),support:[]}));
 let D=dag([...R,...extra],120000),replay=D.status==="UNSAT"?check([...R,...extra],D.tree):null;if(replay&&!replay.valid)throw Error("tree replay");
 return {mode,width,stage:"guarded",status:D.status,early:s.reads,pins:[...pins],rows:orig.length,free:V.length,learn,pairs,verify,flips,evals,changed,peakRows,peakLiterals,dag:D,replay,ms:Date.now()-start};
}
 const shared=[];for(let k=0;k<2;k++){
 let id=["JOINT-24","RANDOM-3CNF-40"][k],x=JSON.parse(corpus).instances.find(z=>z.id===id),e=JSON.parse(reg).instances.find(z=>z.alias==="EB-"+id),g=compile(x),native=bytes(g.network),map=bytes(g.source_map);
 A(sha(native)===e.sha256&&native.length*8===e.N_bits&&sha(x.dimacs)===e.source_cnf.sha256&&x.dimacs.length*8===e.source_cnf.N_bits&&sha(map)===e.source_map_sha256,"identity mismatch");
 let N=normalize(g.network),I=independentNormalize(g.network);A(eq(N.fs,I.fs),"source normalization");let a=gauge(N.fs);A(N.fs.every(f=>f.ok.every(w=>f.ok.includes(w^(2**f.vs.length-1)))),"gauge symmetry");let G=restrict(N.fs,[-a]),E=eliminate(G,false),Z=verifyTrace(restrict(I.fs,[-a]),E.trace);A(eq(E.fs,Z.fs),"trace");
 let M=supports(N.fs,E.trace),F=Z.fs.map(f=>({...f,support:M.get(f.id)})),V=[...new Set(F.flatMap(f=>f.vs))].sort((a,b)=>a-b),guards=policy(F),results=[],verified=[],checks=0;
 for(let guard of guards){let q=lanes(F,guard);results.push(q);if(q.dag.status==="UNSAT"){let r=check(restrict(F,guard),q.dag.tree);A(r.valid,"own tree check");checks+=r.reads;verified.push(guard)}}
 let first=results.filter(q=>q.occupancy.status==="UNSAT"||q.quadratic.status==="UNSAT"||q.bijunctive.status==="UNSAT"||q.separator.status==="UNSAT").filter(q=>q.dag.status==="UNSAT").map(q=>q.guard);
 let feedbackRuns=guards.map(h=>({guard:h,runs:[["baseline",2],["flips",2],["deductions",2],["table",2],["residue",2],["deductions",4],["table",4],["residue",4]].map(([m,w])=>feedback(F,h,m,w))}));let initial=response(V,first),full=response(V,verified),coreOverlaps=[];for(let i=0;i<results.length;i++)for(let j=i+1;j<results.length;j++){let s=results[i].dag.support,t=results[j].dag.support;if(s&&t)coreOverlaps.push({i,j,intersection:s.filter(v=>t.includes(v)).length,symmetricDifference:s.filter(v=>!t.includes(v)).length+t.filter(v=>!s.includes(v)).length})}
 // Independently reprove a peer guard with own native chart. Only import on proof, no reference label.
 let p=JSON.parse(peers[k]),digest=sha(peers[k]),expected=["6352fbcdb311ce5c648aee862cae7b9a0119722f4c780457431baa7cbd82c9fd","a1018e717fd8e1f22602664519ba88cbfb0cc63b44208b8ae2b3e8bb1dc6a63e"][k];A(digest===expected&&p.instance_id===e.instance_id,"peer identity");let art=p.guardArtifacts[0].art,pg=art.pins.map(([v,b])=>b?v+1:-(v+1)),peer={digest,bytes:peers[k].length,guard:pg,anchor:art.anchor,status:"UNKNOWN adapter"};
 if(art.anchor===a-1&&pg.every(l=>V.includes(Math.abs(l)))){let d=dag(restrict(F,pg),200000);peer={...peer,...d};if(d.status==="UNSAT"){let r=check(restrict(F,pg),d.tree);A(r.valid,"peer replay");peer.check=r;let vs=pg.map(Math.abs),bad=pg.reduce((z,l,i)=>z|((+(l>0))<<i),0),extra={id:-1,vs,ok:Array.from({length:2**vs.length},(_,i)=>i).filter(i=>i!==bad),support:d.support};let hybrid=quad([...F,extra],true,16,true);peer.hybrid={status:hybrid.status,stats:hybrid.stats,rootPins:hybrid.rootPins,ded:hybrid.ded};let b=quad(F,true,16,true);peer.standalone={status:b.status,stats:b.stats,rootPins:b.rootPins,ded:b.ded};}}
 // Original CNF independent attempt: use exact clauses, no peer inputs.
 let C=x.dimacs.trimEnd().split("\n").slice(1).map((line,i)=>{let c=line.split(/\s+/).map(Number).slice(0,-1),vs=[...new Set(c.map(Math.abs))];A(vs.length<=10,"CNF local cap");return {id:i+1,vs,ok:Array.from({length:2**vs.length},(_,w)=>w).filter(w=>c.some(l=>(w>>vs.indexOf(Math.abs(l))&1)===+(l>0))),support:[i+1]}});
 let cq=quad(C,true,16,true),cd=dag(C,200000);if(cd.status==="UNSAT"){cd.check=check(C,cd.tree);A(cd.check.valid,"CNF tree")}
 let seed=271828+k,random=[];if(full.covered!==full.total){for(let t=0;t<4;t++){let h=[];for(let j=0;j<2;j++){seed=(Math.imul(seed,1664525)+1013904223)>>>0;let v=V[seed%V.length];if(!h.some(l=>Math.abs(l)===v))h.push(seed&256?v:-v)}let q=dag(restrict(F,h),20000);if(q.status==="UNSAT"){q.check=check(restrict(F,h),q.tree);A(q.check.valid,"random check")}random.push({guard:h,...q})}}
 let mapArtifact={schema:"MINPORT-PLUS1-GAUGE-BUCKET-v1",gauge:a,trace:E.trace,source:sha(native),normalizer:"pinned T1 BFS and independent parity DSU"},mh=sha(bytes(mapArtifact)),rh=sha(bytes(F));let residual="RESIDUAL-v1:sha256:"+sha(bytes(["PNP-RESIDUAL-v1",e.instance_id,"EMPTY","RELATIVE-MINPORT-TABLES-v1",rh,mh]));
 let guardArtifacts=guards.map(h=>{let art={schema:"EB-RELATIVE-PORT-PINS-v1",anchor:a-1,pins:h.map(l=>[Math.abs(l)-1,+(l>0)]).sort((a,b)=>a[0]-b[0])},hsh=sha(bytes(art));let gid="GUARD-v1:sha256:"+sha(bytes(["PNP-GUARD-v1",e.instance_id,art.schema,hsh])),rr=sha(bytes(restrict(F,h)));return {art,sha:hsh,guard_id:gid,residual_id:"RESIDUAL-v1:sha256:"+sha(bytes(["PNP-RESIDUAL-v1",e.instance_id,gid,"RELATIVE-MINPORT-TABLES-v1",rr,mh]))}});
 shared.push({entry:e,auth:{native:sha(native),map:sha(map),cnf:sha(x.dimacs)},root:{gauge:a,normalization:{arcs:N.arcs,local:N.local,independent:I.counts},projection:{checks:E.checks,scans:E.scans,words:E.words,verifyTests:Z.tests,verifyScans:Z.scans,steps:E.trace.length},residual,mh,rh,mapArtifact,guardArtifacts,V},results,feedbackRuns,checks,coreOverlaps,first,initial,full,peer,cnf:{quad:cq,dag:cd},random})
 }
 let controls=[];for(let n=1;n<=5;n++){let V=Array.from({length:n},(_,i)=>i+1),guards=[[-1],...(n>=2?[[1,-2]]:[])],r=response(V,guards),Q=basis(),L=basis();for(let w=0;w<2**n;w++){if(guards.some(g=>g.every(l=>+(l>0)===(w>>(Math.abs(l)-1)&1))))continue;let z=1n;for(let i=0;i<n;i++)if(w>>i&1)z|=bit(i+1);L.add(z);let t=n+1;for(let i=0;i<n;i++)for(let j=i+1;j<n;j++,t++)if((w>>i&1)&&(w>>j&1))z|=bit(t);Q.add(z)}A(r.rank===Q.B.size&&r.affineRank===L.B.size,"response control");controls.push({n,r})}
 // Exclude just 00: remaining 01,10,11 has full affine hull, nonzero quadratic vanishing identity.
 let control=response([1,2],[[-1,-2]]);A(control.affineNullity===0&&control.quadraticNullity===1,"nonlinear control");return {shared,controls,control};
}
const inputs=process.argv.slice(2).map(p=>fs.readFileSync(p,'utf8'));console.log(JSON.stringify(run(inputs),null,2));
