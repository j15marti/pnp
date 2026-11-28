const fs=require('node:fs');
const pins={"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"],"batch":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_early_forced_probe/quadratic-batch-results.json","8569dbcce2128c84db7cbab9d5ed365e4d038aef"]};
const data=Object.fromEntries(Object.keys(pins).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
const run=function run(data){
 const compile=new Function("return function compile"+data.compiler.split("function compile")[1].split("function auditLocal")[0])();
 const {sha,norm,project,replay,key,canon,up,solve,check}=new Function(data.native+";return {sha,norm,project,replay,key,canon,up,solve,check};")();
 const A=(t,m)=>{if(!t)throw Error(m)},enc=o=>JSON.stringify(o)+"\n",V=C=>[...new Set(C.flat().map(Math.abs))].sort((a,b)=>a-b);
 let reg=JSON.parse(data.registry),corp=JSON.parse(data.corpus),out=[];
 const meter=()=>({scans:0,lits:0,cap:10000000});
 function simplify(C){let m=meter(),r=up(C,[],m);A(!r.conflict,"root");return {C:C.filter(c=>!c.some(l=>r.A.get(Math.abs(l))===+(l>0))).map(c=>c.filter(l=>!r.A.has(Math.abs(l)))),units:[...r.A],m}}
 function flips(C,extra,residue){
  const D=[...C,...extra],vs=V(D);let work=0,changed=0,steps=0,starts=[];
  function score(a){let bad=0,z=0;for(let c of D){let k=0,s=0;for(let l of c){work++;if(a.get(Math.abs(l))===+(l>0)){k++;s+=l>0?1:-1}}let km=k%3,sm=(s%3+3)%3;if(!k)bad++;else if(residue&&sm===0)z++;if(km!==k%3)throw Error("residue")}return [bad,z]}
  for(let init of [0,1]){let a=new Map(vs.map(v=>[v,init])),cur=score(a);for(;;){let best=null,plain=null;for(let v of vs){a.set(v,1-a.get(v));let q=score(a);a.set(v,1-a.get(v));if(q[0]>=cur[0])continue;if(!plain||q[0]<plain.q[0])plain={v,q};if(!best||q[0]<best.q[0]||(q[0]===best.q[0]&&residue&&q[1]<best.q[1]))best={v,q}}
   if(!best)break;if(best.v!==plain.v)changed++;a.set(best.v,1-a.get(best.v));cur=best.q;steps++}
   starts.push({remaining:cur[0],originalBad:C.filter(c=>!c.some(l=>a.get(Math.abs(l))===+(l>0))).length})}
  return {steps,changed,work,starts}
 }
 function fusion(C,mode,width=3){let rows=[],seen=new Set(C.map(c=>key(canon(c)))),pairs=0,tries=0;for(let i=0;i<C.length;i++)for(let j=i+1;j<C.length;j++){pairs++;let a=C[i],b=C[j],same=key(V([a]))===key(V([b]));if(mode==="same"?!same:same)continue;for(let p of a)if(b.includes(-p)){tries++;let c=canon([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);if(c.length>width||c.some(x=>c.includes(-x))||seen.has(key(c)))continue;seen.add(key(c));rows.push({i,j,p,c})}}
  for(let r of rows){let a=C[r.i],b=C[r.j];A(a.includes(r.p)&&b.includes(-r.p),"pivot");A(key(canon([...a.filter(x=>x!==r.p),...b.filter(x=>x!==-r.p)]))===key(r.c),"replay")}
  return {rows,pairs,tries}}
 function algebra(C,d,cap=2200000){
  let vs=V(C),idx=new Map(vs.map((v,i)=>[v,i])),bits=vs.map((_,i)=>1n<<BigInt(i)),rows=[],basis=new Map(),ops=0,attempts=0,rank=0,status="UNKNOWN",proof=null,peakTerms=0;
  const toggle=(s,v)=>s.has(v)?s.delete(v):s.add(v);
  function poly(c){let a=new Set([0n]);for(let l of c){let b=new Set(),x=bits[idx.get(Math.abs(l))];for(let t of a){toggle(b,t|x);if(l>0)toggle(b,t)}a=b}return a}
  const polys=C.map(poly),pc=x=>{let n=0;while(x){x&=x-1n;n++}return n};
  const top=s=>{let b=-1n;for(let x of s)if(x>b)b=x;return b};
  function insert(i,m){attempts++;let a=new Set();for(let t of polys[i])toggle(a,t|m);if(!a.size)return;let id=rows.length;rows.push({i,m:m.toString(16)});let cert=new Set([id]);
   while(a.size){let p=top(a);if(p===0n){status="UNSAT";proof=[...cert].map(j=>rows[j]);return}let b=basis.get(p);if(!b){basis.set(p,{a,cert});rank++;peakTerms+=a.size+cert.size;return}ops+=b.a.size+b.cert.size;if(ops>cap){status="UNKNOWN_CAP";return}for(let t of b.a)toggle(a,t);for(let j of b.cert)toggle(cert,j)}
  }
  // Degree of the actual square-free product is bounded by union of support and multiplier.
  for(let i=0;i<C.length&&status==="UNKNOWN";i++)if(V([C[i]]).length<=d)insert(i,0n);
  for(let k=1;k<=d&&status==="UNKNOWN";k++)for(let i=0;i<C.length&&status==="UNKNOWN";i++){let support=V([C[i]]),pool=bits.filter((_,j)=>!support.includes(vs[j]));if(support.length+k>d)continue;function gen(start,left,m){if(status!=="UNKNOWN")return;if(!left){insert(i,m);return}for(let j=start;j<=pool.length-left&&status==="UNKNOWN";j++)gen(j+1,left-1,m|pool[j])}gen(0,k,0n)}
  let verify=0;if(proof){let s=new Set();for(let r of proof){let m=BigInt("0x"+r.m);A(C[r.i]!==undefined&&pc(m)<=d,"index");for(let t of polys[r.i]){A(pc(t|m)<=d,"degree");toggle(s,t|m);verify++}}A(s.size===1&&s.has(0n),"identity")}
  return {d,status,rank,attempts,ops,peakTerms,proof,verify,variables:vs}
 }
 function test(C){
  let early=simplify(C),D=early.C,base=solve(D,500000),bc=base.status==="UNSAT"?check(D,base.tree):null;
  let same=fusion(D,"same"),cross=fusion(D,"cross"),joined=[...D,...cross.rows.map(r=>r.c)],hs=solve(joined,500000),hc=hs.status==="UNSAT"?check(joined,hs.tree):null;
  let a3=algebra(D,3),a4=a3.status==="UNSAT"?null:algebra(D,4),hy=algebra(joined,3);
  let feed=fusion(C,"cross",2),table=feed.rows.map(r=>r.c);return {early:{units:early.units,work:early.m,vars:V(D).length,clauses:D.length},same,cross,base,bc,hs,hc,a3,a4,hy,feedback:{width2:feed,baseline:flips(C,[],false),table:flips(C,table,false),residue:flips(C,table,true)}};
 }
 for(let old of JSON.parse(data.batch)){let s=corp.instances.find(x=>x.id===old.alias),R=reg.instances.find(x=>x.alias==="EB-"+old.alias),g=compile(s),raw=enc(g.network);
  A(sha(raw)===R.sha256&&raw.length*8===R.N_bits&&sha(s.dimacs)===R.source_cnf.sha256&&sha(enc(g.source_map))===R.source_map_sha256,"authentication");
  let b=norm(g.network),p=replay(b.C,old.chart.projection_trace);A(sha(enc(p.C))===old.chart.projected_sha,"chart");
  let cnf=s.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));
  out.push({alias:old.alias,registry:R,chart:old.chart,normalization:{components:b.components,vis:b.vis,rows:b.rows},projectionReplay:{pairs:p.pairs,scans:p.scans},native:test(p.C),cnf:test(cnf)});
 }
 return out
};
console.log(JSON.stringify(run(data),null,2));
