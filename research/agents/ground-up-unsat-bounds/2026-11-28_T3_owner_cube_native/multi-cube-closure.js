const fs=require('node:fs');
const pins={"runner":["research/agents/ground-up-unsat-bounds/2026-11-28_T3_owner_cube_native/run.js","7fb35af63bcc0f88a5045a073ff7d06cfd5b19a5"],"results":["research/agents/ground-up-unsat-bounds/2026-11-28_T3_owner_cube_native/results.json","d9beb1519cd8f6b924da0af0fa4171e890243788"],"registry":["research/coordination/shared-eb-2026-11-27/instance-registry-v1.json","0c14cdc57925788cf7a451dcd5aa171dce860f2c"],"compiler":["research/coordination/shared-eb-2026-11-27/compile.js","21b9d53fb8166c819b24e708656c742cd3c24f10"],"corpus":["research/coordination/shared-unsat-2026-11-27/benchmarks.json","e315349cd6c1fe3fa696504859f28312f6aab69a"],"native":["research/agents/ground-up-unsat-bounds/2026-11-27_T3_native_transport_replay/native.js","303d735ba73855b69b47df734d4d3686f760b215"]};
const data=Object.fromEntries(Object.keys(pins).map(k=>[k,fs.readFileSync(process.argv[2]+'/'+k,'utf8')]));
const run=function run(data,pins){
 const {sha,norm}=new Function(data.native+";return {sha,norm};")(),compile=new Function(data.compiler.slice(data.compiler.indexOf("function compile("),data.compiler.indexOf("function auditLocal"))+";return compile;")();
 const expr=data.runner.slice(data.runner.indexOf("const run=")+10,data.runner.lastIndexOf(";\nconsole.log(")).replace("let roots=[];","return {makeNative,chart};let roots=[];");
 const {makeNative,chart}=new Function("return ("+expr+")")()(data,pins);
 const A=(b,s)=>{if(!b)throw Error(s)},enc=x=>JSON.stringify(x)+"\n",hx=x=>x.toString(16);
 function closure(D,target,cap=10000000){
 let count={rank:0,xor:0,options:0,dependencies:0,checks:0,joins:0},B=new Map(),tags=[],select=[];
 function tick(k){count[k]++;if(Object.values(count).reduce((a,b)=>a+b,0)>cap)throw Error("cap")}
 function add(B,x,t=0n){while(x){tick("rank");let k=x&-x;if(!B.has(k)){B.set(k,[x,t]);return true}let [a,b]=B.get(k);x^=a;t^=b;tick("xor")}return false}
 function reduce(B,x){let t=0n;while(x){tick("rank");let k=x&-x;if(!B.has(k))return {x,t};let [a,b]=B.get(k);x^=a;t^=b;tick("xor")}return {x,t}}
 // Greedy selection of exact local cubes of dimension at most two; full span required, not presumed.
 try{
 for(let i=0;i<D.length;i++){let S=D[i],best={a:S[0],d:[],gain:0};
 function offer(a,d){tick("options");let T=new Map(B);for(let x of d)add(T,x);let gain=T.size-B.size;if(gain>best.gain)best={a,d,gain}}
 for(let a of S){for(let x of S){let u=x^a;if(!u)continue;offer(a,[u]);for(let y of S){let v=y^a;if(v&&u<v&&S.includes(a^u^v))offer(a,[u,v])}}}
 select.push(best);for(let d of best.d){let j=tags.length;tags.push({i,d});add(B,d,1n<<BigInt(j))}
 }
 let dep=D.map(()=>new Set()),bad=new Set();
 for(let i=0;i<D.length;i++)for(let x of D[i]){let r=reduce(B,x^select[i].a);if(r.x){bad.add(i);continue}let t=r.t;while(t){tick("dependencies");let k=t&-t;t^=k;dep[i].add(tags[k.toString(2).length-1].i)}}
 let change=true;while(change){change=false;for(let i=0;i<D.length;i++)if(!bad.has(i))for(let j of dep[i]){tick("dependencies");if(bad.has(j)){bad.add(i);change=true;break}}}
 let good=D.map((_,i)=>i).filter(i=>!bad.has(i)),goodSet=new Set(good),Q=new Map(),offset=0n;
 for(let i of good){offset^=select[i].a;for(let j=0;j<tags.length;j++)if(tags[j].i===i)add(Q,tags[j].d,1n<<BigInt(j))}
 // Independent high-pivot containment verification, and each cube member is original.
 let H=new Map();function high(x){while(x){tick("checks");let k=x.toString(2).length-1;if(!H.has(k)){H.set(k,x);return}x^=H.get(k)}}
 for(let i of good)for(let d of select[i].d)high(d);
 A(H.size===Q.size,"rank check");for(let i of good){let s=select[i];for(let w=0;w<2**s.d.length;w++){let x=s.d.reduce((a,d,j)=>a^((w>>j&1)?d:0n),s.a);tick("checks");A(D[i].includes(x),"cube")}
 for(let v of D[i]){let x=v^s.a;while(x){tick("checks");let k=x.toString(2).length-1;A(H.has(k),"closure");x^=H.get(k)}}}
 // canonical linear quotient must reduce ALL pivot columns, not stop on a missing low pivot.
 let ks=[...Q.keys()].sort((a,b)=>a<b?-1:1);
 function project(x){let t=0n;for(let k of ks){tick("rank");if(x&k){let [v,z]=Q.get(k);x^=v;t^=z;tick("xor")}}return {x,t}}
 let other=D.map((_,i)=>i).filter(i=>!goodSet.has(i)),R=new Map([[0n,[]]]),peak=1,b=project(target^offset).x;
 let status="UNKNOWN",witness=null;
 for(let i of other){let T=new Map();for(let [x,w] of R)for(let j=0;j<D[i].length;j++){tick("joins");let y=x^project(D[i][j]).x;if(!T.has(y))T.set(y,[...w,[i,j]]);if(T.size>512)return {status,good:good.length,remaining:other.length,rank:Q.size,selectedRank:B.size,peak:T.size,count,goodOwners:good,selected:good.map(i=>({i,a:hx(select[i].a),d:select[i].d.map(hx)}))}}R=T;peak=Math.max(peak,R.size)}
 if(!R.has(b))status="NO";else{let picked=R.get(b),correction=target^offset^picked.reduce((a,[i,j])=>a^D[i][j],0n),r=project(correction);A(!r.x,"quotient correction");let w=D.map((_,i)=>select[i].a);for(let [i,j] of picked)w[i]=D[i][j];for(let j=0;j<tags.length;j++)if(r.t>>BigInt(j)&1n){A(goodSet.has(tags[j].i),"owner");w[tags[j].i]^=tags[j].d}A(w.every((x,i)=>D[i].includes(x))&&w.reduce((a,b)=>a^b,0n)===target,"lift");status="YES";witness=w.map(hx)}
 return {status,good:good.length,remaining:other.length,rank:Q.size,selectedRank:B.size,peak,count,goodOwners:good,selected:good.map(i=>({i,a:hx(select[i].a),d:select[i].d.map(hx)})),witness,offset:hx(offset),target:hx(target),quotientTarget:hx(b)};
 }catch(e){if(e.message!=="cap")throw e;return {status:"UNKNOWN",reason:"event cap",count}}
 }
 let prior=JSON.parse(data.results),roots=[],controls=[];
 for(let r of prior.roots){let s=JSON.parse(data.corpus).instances.find(x=>x.id===r.alias),g=compile(s);A(sha(enc(g.network))===r.entry.sha256&&enc(g.network).length*8===r.entry.N_bits&&sha(enc(g.source_map))===r.entry.source_map_sha256&&sha(s.dimacs)===r.entry.source_cnf.sha256&&s.dimacs.length*8===r.entry.source_cnf.N_bits,"auth");let b=norm(g.network),t=chart(g.network,b);roots.push({entry:r.entry,owner:closure(t.blocks.map(o=>o.S),0n)})}
 for(let r of prior.controls){let g=makeNative(r.k,r.no);A(sha(enc(g))===r.entry.sha256&&enc(g).length*8===r.entry.N_bits,"native auth");let b=norm(g),t=chart(g,b),x=closure(t.blocks.map(o=>o.S),0n);A(x.status===r.cert.status,"closure result");if(x.status==="YES"){let a=new Map([[b.gauge,0]]);for(let i=0;i<t.blocks.length;i++){let o=t.blocks[i],j=o.S.indexOf(BigInt("0x"+x.witness[i])),w=o.rows[j];for(let j0=0;j0<o.vs.length;j0++){let v=o.vs[j0],z=w>>j0&1;A(!a.has(v)||a.get(v)===z,"lift");a.set(v,z)}}let v=b.root.map((r,i)=>(a.get(r)||0)^b.sign[i]);A(g.edges.every(([a,b,s])=>(v[a]^v[b])===s)&&g.types.every((t,i)=>{let a=v.slice(4*i,4*i+4);return t==="E"?a.every(x=>x===a[0]):a.reduce((s,x)=>s+x,0)===2}),"native lift");x.nativeWitnessSha=sha(enc(v))}
 controls.push({entry:r.entry,k:r.k,no:r.no,owner:x})}
 let explicit=[];for(let k of [4,16,64])for(let no of [false,true]){let d=4*k+2,vec=Array.from({length:d},(_,i)=>(1n<<BigInt(i))^(i+1<d?(1n<<BigInt(i+1)):0n));let X=[],Y=[];for(let i=0;i<k;i++){let [a,b,c,e]=vec.slice(4*i,4*i+4);X.push([0n,a,b,a^b,c]);Y.push([0n,c,e,c^e,a])}let a=vec[d-2],b=vec[d-1],D=[...X,...Y,[0n,a,b]],target=vec.slice(0,d-2).reduce((a,b)=>a^b,0n)^a^(no?b:0n),x=closure(D,target);A(x.status===(no?"NO":"YES")&&x.rank===4*k,"explicit saturation");
 // independently check each 2-owner support spans full 4D group; defect target in span but absent.
 let checks=[];for(let i=0;i<k;i++){let z=new Set();for(let a of X[i])for(let b of Y[i])z.add(a^b);A(z.size===16,"full pair");checks.push(z.size)}
 const source={format:"EXPLICIT-XOR-SUMSET-v1",d,blocks:D.map(S=>S.map(hx)),target:hx(target)},raw=enc(source),id=sha(raw),entry={alias:"CUBE2-MIXED-"+k+"-"+(no?"NO":"YES"),problem_id:source.format,sha256:id,N_bits:raw.length*8};entry.short_id=entry.alias+"@"+id.slice(0,12);entry.instance_id=source.format+":sha256:"+id;let certificate={entry,source,guard_id:"EMPTY",residual_id:"ROOT",parents:[],original_ids:{blocks:[0,D.length-1],coordinates:[0,d-1]},result:x,independentPairCounts:checks};explicit.push({entry,k,no,certificate,certHash:sha(enc(certificate))});
 }
 return {roots,controls,explicit};
};
console.log(JSON.stringify(run(data,pins),null,2));
