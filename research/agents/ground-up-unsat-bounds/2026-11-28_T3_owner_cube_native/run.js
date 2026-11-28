const fs=require('node:fs');
const pins={"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"],"peer":["research/proof-spine-2026-11-26/closure-exceptional-syndrome/2026-11-28_0452_T3_seed_rank_replay/joint-rank-certificate.json","97297a0e530965297aaae1b6f7197887448a5939"]};
const data=Object.fromEntries(Object.keys(pins).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
const run=function run(data,pins){
const {sha,norm,project,replay,up,solve,check,canon}=new Function(data.native+";return {sha,norm,project,replay,up,solve,check,canon};")();
const compile=new Function(data.compiler.slice(data.compiler.indexOf("function compile("),data.compiler.indexOf("function auditLocal"))+";return compile;")();
const enc=x=>JSON.stringify(x)+"\n", A=(b,s)=>{if(!b)throw Error(s)}, hx=x=>x.toString(16), pop=x=>{let n=0;while(x){n++;x&=x-1n}return n}, m=()=>({scans:0,lits:0,cap:10000000,nodes:0});
const reg=JSON.parse(data.registry),cor=JSON.parse(data.corpus);
function basis(V,c){let B=new Map();for(let x of V){while(x){c.rank++;let k=x&-x;if(!B.has(k)){B.set(k,x);break}x^=B.get(k);c.xor++}}return B}
function member(B,x,c){while(x){c.rank++;let k=x&-x;if(!B.has(k))return false;x^=B.get(k);c.xor++}return true}
function independentRank(V){let B=new Map();for(let x of V)while(x){let k=x.toString(2).length-1;if(!B.has(k)){B.set(k,x);break}x^=B.get(k)}return B}
function verifyNative(g,v){A(v.length===4*g.types.length,"length");A(g.edges.every(([a,b,s])=>(v[a]^v[b])===s),"edges");A(g.types.every((t,i)=>t==="E"?v.slice(4*i,4*i+4).every(x=>x===v[4*i]):v.slice(4*i,4*i+4).reduce((a,b)=>a+b,0)===2),"owners");return true}
function makeNative(k,no){
 const types=[],edges=[],used=[],occ=new Map();function V(t){types.push(t);used.push(0);return types.length-1}function P(v){A(used[v]<4,"port");return 4*v+used[v]++}function E(a,b,s=0){edges.push([a,b,s])}
 function wire(a,b,s){let v=Array.from({length:5},()=>V("E"));for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)if(i!==0||j!==1)E(P(v[i]),P(v[j]));E(a,P(v[0]),s);E(b,P(v[1]),0)}
 // Shared carrier f connects all groups in the actual native graph. Opposite labels differ only in one owner's signs.
 let rows=[];for(let i=0;i<k;i++)rows.push([i,0]);for(let i=0;i<k;i++)rows.push([i,0]);rows.push([k-1,3],[k-1,no?5:3]); // defect has 4 owners: change second base owner below
 rows[k+k-1][1]=6;
 // masks on the three private variables: 0, 6, 3, 5 are all even parity and exclude the four possible even/odd words when anchor zero.
 for(let [i,mask] of rows){let v=V("B");for(let j=0;j<4;j++){let id=j===0?0:3*i+j,s=j===0?0:(mask>>(j-1))&1;if(!occ.has(id))occ.set(id,[]);occ.get(id).push([P(v),s])}}
 for(let O of occ.values()){if(O.length===2){wire(O[0][0],O[1][0],O[0][1]^O[1][1]);continue}let a=Array.from({length:(O.length-2)/2},()=>V("E"));for(let i=1;i<a.length;i++)wire(P(a[i-1]),P(a[i]),0);let t=0;for(let v of a)while(used[v]<4){let [p,s]=O[t++];wire(P(v),p,s)}A(t===O.length,"fanout")}
 A(used.every(x=>x===4),"degree");return {format:"STRICT-EB4-v1",types,edges};
}
function chart(g,b){
 let blocks=[],inc=new Map(),localTests=0;
 for(let i=0;i<g.types.length;i++)if(g.types[i]==="B"){let ports=Array.from({length:4},(_,j)=>4*i+j),vs=[...new Set(ports.map(p=>b.root[p]).filter(v=>v!==b.gauge))].sort((a,b)=>a-b),rows=[];
 for(let w=0;w<2**vs.length;w++){localTests++;let sum=ports.reduce((s,p)=>s+((b.root[p]===b.gauge?0:(w>>vs.indexOf(b.root[p])&1))^b.sign[p]),0);if(sum===2)rows.push(w)}
 if(!rows.length)return {empty:i,localTests};
 let id=blocks.length;blocks.push({id,owner:i,vs,rows,S:[]});for(let v of vs){if(!inc.has(v))inc.set(v,[]);inc.get(v).push(id)}}
 let col=0,by=blocks.map(()=>new Map());for(let [v,ids] of inc){for(let j=1;j<ids.length;j++){let bit=1n<<BigInt(col++);by[ids[0]].set(v,(by[ids[0]].get(v)||0n)^bit);by[ids[j]].set(v,(by[ids[j]].get(v)||0n)^bit)}}
 for(let o of blocks){o.S=o.rows.map(w=>o.vs.reduce((s,v,j)=>s^((w>>j&1)?by[o.id].get(v)||0n:0n),0n));}
 return {blocks,inc,col,localTests};
}
function evaluate(g,b,T,cap=10000000){
 if(T.empty!==undefined)return {status:"NO-local",owner:T.empty};const B=T.blocks,c={rank:0,xor:0,pairs:0,cube:0,checks:0,spectral:0,joins:0,peak:0,cap};
 const budget=()=>{if(c.rank+c.xor+c.pairs+c.cube+c.checks+c.spectral+c.joins>cap)throw Error("cap")};
 const basisLocal=B.map(o=>basis(o.S.map(x=>x^o.S[0]),c));let target=B.reduce((s,o)=>s^o.S[0],0n),all=basis(B.flatMap(o=>o.S.map(x=>x^o.S[0])),c),rank=all.size;
 let order=B.map(o=>o.id),cut=Math.floor(order.length/2),U=basis(order.slice(0,cut).flatMap(i=>[...basisLocal[i].values()]),c),V=basis(order.slice(cut).flatMap(i=>[...basisLocal[i].values()]),c),mid=U.size+V.size-rank;
 // Fixed-point graph diffusion only proposes ordering. Exact scope incidence.
 let adj=B.map(()=>new Map());for(let ids of T.inc.values())for(let i of ids)for(let j of ids)if(i!==j){adj[i].set(j,(adj[i].get(j)||0)+1);c.spectral++}let deg=adj.map(x=>[...x.values()].reduce((s,v)=>s+v,0)),md=Math.max(1,...deg),z=order.map(i=>Math.round(1000000*(2*i-order.length+1)/Math.max(1,order.length-1)));
 for(let t=0;t<8;t++)z=z.map((x,i)=>{let y=(2*md-deg[i])*x;for(let [j,w] of adj[i]){c.spectral++;y+=w*z[j]}A(Number.isSafeInteger(y),"precision");return Math.trunc(y/(2*md))});
 let spec=order.slice().sort((i,j)=>z[i]-z[j]||i-j),SM=basis(spec.slice(0,cut).flatMap(i=>[...basisLocal[i].values()]),c),SN=basis(spec.slice(cut).flatMap(i=>[...basisLocal[i].values()]),c),specMid=SM.size+SN.size-rank;
 // Exact scope-based direct sum: disjoint coordinates, without using generated owner grouping.
 let par=order.slice();function root(i){while(par[i]!==i)i=par[i];return i}for(let ids of T.inc.values())for(let j=1;j<ids.length;j++)par[root(ids[j])]=root(ids[0]);
 let groups=new Map();for(let i of order){let r=root(i);if(!groups.has(r))groups.set(r,[]);groups.get(r).push(i)}
 // Separate bounded prefix table baseline, retains actual backpointers, no semantic shortcut.
 function dp(ids,limit){let D=new Map([[0n,[]]]),peak=1,trans=0;for(let i of ids){let R=new Map();for(let [x,p] of D)for(let j=0;j<B[i].S.length;j++){c.joins++;trans++;let y=x^B[i].S[j];if(!R.has(y))R.set(y,[...p,[i,j]]);if(R.size>limit)return {status:"UNKNOWN",peak:R.size,trans};budget()}D=R;peak=Math.max(peak,D.size)}return {status:D.has(0n)?"YES":"NO",peak,trans,witness:D.get(0n)}}
 let baseline=dp(order,512),spectral=dp(spec,512);
 // Cube acquisition: exact test of all 1- and 2-dimensional cubes in an owner's table, no assumed period.
 function cubes(o){let out=[];for(let i=0;i<o.S.length;i++){let a=o.S[i];out.push({anchor:a,ds:[]});for(let j=0;j<o.S.length;j++)if(o.S[j]!==a){let x=a^o.S[j];out.push({anchor:a,ds:[x]});for(let l=j+1;l<o.S.length;l++){c.cube++;let y=a^o.S[l];if(y&&x!==y&&o.S.includes(a^x^y))out.push({anchor:a,ds:[x,y]})}}}return out}
 let certificates=[],choice=[],status="YES",peak=0,exactPairs=0;
 for(let ids of groups.values()){
  // For large components, cap before expensive group rank/cube search. Direct sum acquisition is exact, not full branchwidth optimizer.
  if(ids.length>32){status="UNKNOWN";certificates.push({ids,kind:"unadmitted-large-component"});continue}
  let full=basis(ids.flatMap(i=>B[i].S.map(x=>x^B[i].S[0])),c),selected=[],ds=[];
  for(let i of ids){let best=null;for(let C of cubes(B[i])){let k=basis([...ds,...C.ds],c).size;c.checks++;if(!best||k>best.k)best={...C,k};budget()}selected.push({i,anchor:best.anchor,ds:best.ds});ds.push(...best.ds)}
  let span=basis(ds,c),offset=selected.reduce((a,x)=>a^x.anchor,0n),fullSat=span.size===full.size;
  // Independent high-pivot rank + local cube validation, exact anchor correction.
  let independent=independentRank(ds),independentFull=independentRank(ids.flatMap(i=>B[i].S.map(x=>x^B[i].S[0])));A(independent.size===span.size&&independentFull.size===full.size,"rank audit");
  for(let x of selected)for(let w=0;w<2**x.ds.length;w++){c.checks++;A(B[x.i].S.includes(x.ds.reduce((v,d,j)=>v^((w>>j&1)?d:0n),x.anchor)),"cube check")}
  if(fullSat){A(ds.every(x=>member(full,x,c)),"contained");let o=offset,tagged=new Map(),flat=selected.flatMap(x=>x.ds.map(d=>({i:x.i,d})));
   for(let j=0;j<flat.length;j++){let x=flat[j].d,t=1n<<BigInt(j);while(x){c.rank++;let h=x&-x;if(!tagged.has(h)){tagged.set(h,[x,t]);break}let [v,u]=tagged.get(h);x^=v;t^=u;c.xor++}}
   let mask=0n;while(o){c.rank++;let h=o&-o;if(!tagged.has(h))break;let [v,t]=tagged.get(h);o^=v;mask^=t;c.xor++}
   let w=selected.map(x=>x.anchor);if(o){status="NO";certificates.push({ids,kind:"cube-affine-NO",rank:full.size,offset:hx(offset),selected:selected.map(x=>({i:x.i,anchor:hx(x.anchor),ds:x.ds.map(hx)}))});break}
   for(let j=0;j<flat.length;j++)if(mask>>BigInt(j)&1n)w[ids.indexOf(flat[j].i)]^=flat[j].d;
   let picked=w.map((x,j)=>[ids[j],B[ids[j]].S.indexOf(x)]);A(picked.every(x=>x[1]>=0)&&w.reduce((a,b)=>a^b,0n)===0n,"cube lift");choice.push(...picked);
   certificates.push({ids,kind:"cube-affine-YES",rank:full.size,selected:selected.map(x=>({i:x.i,anchor:hx(x.anchor),ds:x.ds.map(hx)})),picked});
  }else{let r=dp(ids,512);peak=Math.max(peak,r.peak);exactPairs+=r.trans;certificates.push({ids,kind:"bounded-exact-"+r.status,rank:full.size,selectedRank:span.size,peak:r.peak,trans:r.trans,picked:r.witness});if(r.status==="NO"){status="NO";break}if(r.status==="UNKNOWN")status="UNKNOWN";else choice.push(...r.witness)}
 }
 let witness=null;if(status==="YES"){let a=new Map([[b.gauge,0]]);for(let [i,j] of choice){let o=B[i],w=o.rows[j];for(let t=0;t<o.vs.length;t++){let v=o.vs[t],x=w>>t&1;A(!a.has(v)||a.get(v)===x,"shared lift");a.set(v,x)}}witness=b.root.map((v,i)=>(a.get(v)||0)^b.sign[i]);verifyNative(g,witness)}
 // Independent NO checker enumerates only a bounded component's underlying carrier assignments.
 let noAudit=null;if(status==="NO"){let q=certificates.at(-1),ids=q.ids,vs=[...new Set(ids.flatMap(i=>B[i].vs))];if(vs.length<=16){let tests=0,sat=0;for(let w=0;w<2**vs.length;w++){let ok=true;for(let i of ids){tests++;let o=B[i],v=o.vs.reduce((a,x,j)=>a+((w>>vs.indexOf(x)&1)<<j),0);if(!o.rows.includes(v)){ok=false;break}}if(ok)sat++}A(!sat,"NO audit");noAudit={vars:vs.length,tests,sat}}}
 return {status,rank,mid,specMid,groupSizes:[...groups.values()].map(x=>x.length),baseline,spectral,certificates,choice,witness,noAudit,c,peak,exactPairs,chart:{coordinates:T.col,owners:B.map(o=>({owner:o.owner,vs:o.vs,rows:o.rows,S:o.S.map(hx)})),gauge:b.gauge},spectralOrder:spec};
}
let roots=[];
for(let alias of ["JOINT-24","RANDOM-3CNF-40"]){let s=cor.instances.find(x=>x.id===alias),r=reg.instances.find(x=>x.alias==="EB-"+alias),g=compile(s);A(sha(enc(g.network))===r.sha256&&enc(g.network).length*8===r.N_bits&&sha(enc(g.source_map))===r.source_map_sha256&&sha(s.dimacs)===r.source_cnf.sha256&&s.dimacs.length*8===r.source_cnf.N_bits,"authentication");
 let b=norm(g.network),early=m(),u=up(b.C,[],early);A(!u.conflict,"root UP");let p=project(b.C,128),q=replay(b.C,p.trace);A(enc(p.C)===enc(q.C),"projection");
 let ref=solve(p.C,500000),ver=ref.status==="UNSAT"?check(q.C,ref.tree):null;
 let cnf=s.dimacs.trim().split("\n").slice(1).map(l=>canon(l.trim().split(/\s+/).map(Number).slice(0,-1))),cs=solve(cnf,500000),cv=cs.status==="UNSAT"?check(cnf,cs.tree):null;
 // exact rank/spectral pass at the source-normalized gauge chart before new owner search. Large component remains UNKNOWN.
 let t=chart(g.network,b),a=evaluate(g.network,b,t);
 roots.push({alias,entry:r,early,units:[...u.A],projection:{trace:p.trace,scans:p.scans,pairs:p.pairs,replayScans:q.scans,replayPairs:q.pairs},residualSha:sha(enc(p.C)),ref,ver,cnf:cs,cnfCheck:cv,owner:{status:a.status,rank:a.rank,mid:a.mid,specMid:a.specMid,groupSizes:a.groupSizes,baseline:a.baseline,spectral:a.spectral,c:a.c,chartSha:sha(enc(a.chart)),localTests:t.localTests},gauge:b.gauge,normalization:{vis:b.vis,rows:b.rows,components:b.components}});
}
let controls=[];
for(let k of [4,8,16,32,64])for(let no of [false,true]){
 let g=makeNative(k,no),raw=enc(g),b=norm(g),t=chart(g,b),a=evaluate(g,b,t);
 A(a.status===(no?"NO":"YES"),"control label "+k+" "+no);A(no?!!a.noAudit:!!a.witness,"independent control check");
 let entry={problem_id:"STRICT-EB4-v1",alias:"EB-OWNER-CUBE-"+k+"-"+(no?"NO":"YES"),sha256:sha(raw),N_bits:raw.length*8,vertices:g.types.length,edges:g.edges.length};
 entry.short_id=entry.alias+"@"+entry.sha256.slice(0,12);entry.instance_id="STRICT-EB4-v1:sha256:"+entry.sha256;
 let cert={entry,guard_id:"EMPTY",residual_id:"ROOT",parents:[],original_ids:{vertices:[0,g.types.length-1],ports:[0,4*g.types.length-1],edges:[0,g.edges.length-1]},gauge:b.gauge,rootMapSha:sha(enc([b.root,b.sign])),chartSha:sha(enc(a.chart)),status:a.status,certificates:a.certificates,choice:a.choice,witness:a.witness,noAudit:a.noAudit};
 controls.push({entry,k,no,cert,certHash:sha(enc(cert)),rank:a.rank,mid:a.mid,specMid:a.specMid,groupSizes:a.groupSizes,baseline:a.baseline,spectral:a.spectral,c:a.c,peak:a.peak,exactPairs:a.exactPairs,localTests:t.localTests,normalization:{vis:b.vis,rows:b.rows,components:b.components}});
}
return {roots,controls};
};
console.log(JSON.stringify(run(data,pins),null,2));
