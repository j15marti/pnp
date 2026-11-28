function interfaces(R,b){
 const out=[],cap=3000000;
 const ck=(p,m)=>{if(!p)throw Error(m||"check")},sort=a=>[...new Set(a)].sort((a,b)=>a-b);
 function study(C,V){
 let work={geometry:0,regions:0,verify:0,compress:0,occupancy:0,affine:0,dag:0,stochastic:0},cut=null;
 const sets=C.map(c=>sort(c.map(Math.abs))),adj=new Map(V.map(v=>[v,new Set()])),live=new Set(V),order=[];
 for(const S of sets)for(let v of S)for(let w of S)if(v!==w)adj.get(v).add(w);
 while(live.size){let best=null;for(let v of live){let q=[...adj.get(v)].filter(w=>live.has(w)),f=0;for(let i=0;i<q.length;i++)for(let j=i+1;j<q.length;j++){work.geometry++;if(!adj.get(q[i]).has(q[j]))f++}if(!best||f<best.f||f===best.f&&q.length<best.q.length)best={v,q,f}}for(let v of best.q)for(let w of best.q)if(v!==w)adj.get(v).add(w);order.push(best.v);live.delete(best.v)}
 const pos=new Map(order.map((v,i)=>[v,i]));
 for(const sign of [0,1]){let ix=C.map((_,i)=>i).sort((a,b)=>(sign?Math.max(...sets[a].map(v=>pos.get(v)))-Math.max(...sets[b].map(v=>pos.get(v))):Math.min(...sets[a].map(v=>pos.get(v)))-Math.min(...sets[b].map(v=>pos.get(v))))||a-b);
 for(let j=Math.ceil(C.length/3);j<=Math.floor(2*C.length/3);j++){let L=ix.slice(0,j),Q=ix.slice(j),lv=new Set(L.flatMap(i=>sets[i])),rv=new Set(Q.flatMap(i=>sets[i])),B=sort([...lv].filter(v=>rv.has(v)));work.geometry+=C.length;let li=lv.size-B.length,ri=rv.size-B.length;if(li<2||ri<2)continue;if(!cut||B.length<cut.B.length||B.length===cut.B.length&&Math.min(li,ri)>Math.min(cut.li,cut.ri))cut={L,Q,B,li,ri}}}
 if(!cut||cut.B.length>16)return{status:"UNKNOWN geometry cap or no balanced split",work,cut};
 let {B,L,Q}=cut, n=B.length,universe=2**n;
 function region(ids,reverse=false){let rows=ids.map(i=>C[i]),all=sort(rows.flat().map(Math.abs)),S=new Set(),nodes=0,peak=0,mode=reverse?"verify":"regions";
 function tick(k=1){work[mode]+=k;if(work.regions+work.verify>cap)throw Error("region cap")}
 function visit(p){nodes++;peak=Math.max(peak,p.size);let a=new Map(p);
 for(;;){let force=0,found=false;for(let j=0;j<rows.length;j++){let c=rows[reverse?rows.length-1-j:j];tick(c.length);if(c.some(l=>a.get(Math.abs(l))===(l>0)))continue;let u=c.filter(l=>!a.has(Math.abs(l)));if(!u.length)return;if(u.length===1){force=u[0];a.set(Math.abs(force),force>0);found=true;if(reverse)break}}if(!found)break}
 let unresolved=rows.filter(c=>{tick(c.length);return !c.some(l=>a.get(Math.abs(l))===(l>0))});
 if(!unresolved.length){let base=0,free=[];for(let i=0;i<n;i++){if(!a.has(B[i]))free.push(i);else if(a.get(B[i]))base|=1<<i}for(let t=0;t<2**free.length;t++){tick();let w=base;free.forEach((j,i)=>{if(t>>i&1)w|=1<<j});S.add(w)}return}
 let v=all.find(v=>!a.has(v)&&unresolved.some(c=>c.some(l=>Math.abs(l)===v)));ck(v!==undefined,"unresolved");for(let bit of reverse?[true,false]:[false,true]){let q=new Map(a);q.set(v,bit);visit(q)}}
 try{visit(new Map());return{status:"exact",support:sort([...S]),nodes,peak}}catch(e){if(e.message!=="region cap")throw e;return{status:"UNKNOWN cap",partial:S.size,nodes,peak}}}
 let A=region(L),D=region(Q);if(A.status!=="exact"||D.status!=="exact")return{status:"UNKNOWN regional acquisition",work,cut,A,D};
 let A2=region(L,true),D2=region(Q,true);if(A2.status!=="exact"||D2.status!=="exact")return{status:"UNKNOWN independent replay cap",work,cut,A,D,A2,D2};
 ck(A.support.join()===A2.support.join()&&D.support.join()===D2.support.join(),"response mismatch");
 let left=new Set(A.support),right=new Set(D.support),intersection=A.support.filter(w=>right.has(w));
 function rank(S){if(!S.length)return null;let basis=new Map();for(let w of S){let z=w^S[0];while(z){work.affine++;let j=31-Math.clz32(z);if(!basis.has(j)){basis.set(j,z);break}z^=basis.get(j)}}return basis.size}
 let affine=[rank(A.support),rank(D.support)];
 // Occupancy necessary conditions: exact achievable count on every original boundary scope, not independent joint feasibility.
 let scopes=[...new Map(sets.map(S=>S.filter(v=>B.includes(v))).filter(S=>S.length>=2).map(S=>[S.join(),S])).values()];
 function occupancy(S){return scopes.map(s=>{let idx=s.map(v=>B.indexOf(v)),values=new Set();for(let w of S){work.occupancy+=idx.length;values.add(idx.reduce((a,i)=>a+(w>>i&1),0))}return{scope:s,values:sort([...values])}})}
 let oa=occupancy(A.support),od=occupancy(D.support),occConflict=oa.some((s,i)=>!s.values.some(x=>od[i].values.includes(x)));
 function sketch(q){let size=2**q,ac=new Uint32Array(size),dc=new Uint32Array(size),key=w=>{let z=0;for(let j=0;j<n;j++)if(w>>j&1)z^=1<<(j%q);return z};if(q===0)key=w=>0;for(let w of A.support){ac[key(w)]++;work.compress++}for(let w of D.support){dc[key(w)]++;work.compress++}
 let defaults=Array.from(ac,(a,i)=>+(dc[i]>a)),correction=[],conflicts=0,both=0;
 for(let i=0;i<size;i++)if(ac[i]&&dc[i])both++;
 for(let w of A.support){work.compress++;if(defaults[key(w)]!==0)correction.push([w,0])}
 for(let w of D.support){work.compress++;if(defaults[key(w)]!==1)correction.push([w,1])}
 let dict=new Map(correction);if(!intersection.length){for(let w of A.support){work.compress++;ck((dict.has(w)?dict.get(w):defaults[key(w)])===0,"left decode")}for(let w of D.support){work.compress++;ck((dict.has(w)?dict.get(w):defaults[key(w)])===1,"right decode")}}
 let expected=Array.from(ac,(a,i)=>Math.min(a,dc[i])).reduce((a,b)=>a+b,0);ck(expected===correction.length);return{q,both,correctionCount:correction.length,estimatedBits:size+(n+1)*correction.length,defaults,correction,exactOnSupport:!intersection.length}}
 let sketches=[0,Math.min(4,n),Math.min(8,n),n].filter((x,i,a)=>a.indexOf(x)===i).map(sketch);
 // D lane: acquire all unary/binary exclusions of right region by exact support, then greedy cover left. Parent removal tests operate on exact LEFT support.
 let pool=[];for(let i=0;i<n;i++)for(let j=i;j<n;j++)for(let a=0;a<2;a++)for(let z=0;z<2;z++){if(i===j&&a!==z)continue;let match=w=>(w>>i&1)===a&&(w>>j&1)===z;let bad=false;for(let w of D.support){work.dag++;if(match(w)){bad=true;break}}if(!bad)pool.push({i,j,a,z})}
 let rem=A.support.slice(),selected=[];while(rem.length&&selected.length<32){let best=null;for(let p of pool){let hits=[];for(let w of rem){if(++work.dag>cap)break;if((w>>p.i&1)===p.a&&(w>>p.j&1)===p.z)hits.push(w)}if(work.dag>cap)break;if(!best||hits.length>best.hits.length)best={...p,hits}}if(work.dag>cap||!best||!best.hits.length)break;selected.push({i:best.i,j:best.j,a:best.a,z:best.z,hits:best.hits.length});let H=new Set(best.hits);rem=rem.filter(w=>!H.has(w))}
 let ablation=selected.map((p,i)=>A.support.filter(w=>!selected.some((g,j)=>i!==j&&(w>>g.i&1)===g.a&&(w>>g.j&1)===g.z)).length);
 // Stochastic control: sample exact acquired supports, compare direct key collisions, not uniform input solver advice.
 let seed=271127;for(let t=0;t<64;t++){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;if(A.support.length)work.stochastic+=1+Number(right.has(A.support[(seed>>>0)%A.support.length]))}
 return{status:intersection.length?"compatible support":"NO exact disjoint support",work,cut,A,D,affine,occupancy:{oa,od,occConflict},intersection,sketches,dag:{pool:pool.length,selected,uncovered:rem.length,ablation},verify:{A2:A2.nodes,D2:D2.nodes}};
 }
 for(let r of R.cases){let C=r.chart.F.flatMap(f=>Array.from({length:2**f.vs.length},(_,w)=>w).filter(w=>!f.ok.includes(w)).map(w=>f.vs.map((v,i)=>w>>i&1?-v:v)));let x=b.instances.find(z=>z.id===r.e.source_cnf.alias),D=x.dimacs.trimEnd().split("\n").slice(1).map(l=>l.trim().split(/\s+/).map(Number).slice(0,-1));out.push({entry:r.e,chartId:r.chartId,chart:r.chart,map:r.map,chartSha:r.chartSha,mapSha:r.mapSha,native:study(C,r.chart.V),companion:study(D,Array.from({length:x.nvars},(_,i)=>i+1))})}return out
}
const fs=require('node:fs');const [r,b]=process.argv.slice(2).map(x=>JSON.parse(fs.readFileSync(x,'utf8')));console.log(JSON.stringify(interfaces(r,b),null,2));
