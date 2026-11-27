function checkTree(F,pins,tree,cap=2500000){
 let visits=0,nodes=0;const universe=new Set(F.flatMap(f=>f.vs));
 function close(a){for(;;){let ch=false;for(let i=F.length-1;i>=0;i--){let f=F[i],ok=[];for(let w of f.ok){if(++visits>cap)throw Error("CHECK_CAP");let hit=true;for(let j=0;j<f.vs.length;j++)if(a.has(f.vs[j])&&a.get(f.vs[j])!==(w>>j&1)){hit=false;break}if(hit)ok.push(w)}if(!ok.length)return false;for(let j=0;j<f.vs.length;j++){let v=f.vs[j];if(a.has(v))continue;let have=0;for(let w of ok)have|=1<<(w>>j&1);if(have!==3){a.set(v,have===1?0:1);ch=true}}}if(!ch)return true}}
 function go(a,t){nodes++;if(!close(a))return true;if(t===0||!Array.isArray(t)||t.length!==3||!universe.has(t[0]))return false;let v=t[0];if(a.has(v))return go(a,t[a.get(v)+1]);let x=new Map(a),y=new Map(a);x.set(v,0);y.set(v,1);return go(x,t[1])&&go(y,t[2])}
 return{verified:go(new Map(pins),tree),visits,nodes}
}

function restrict(F,pins){let a=new Map(pins);return F.map((f,id)=>{let V=f.vs.filter(v=>!a.has(v)),ok=[...new Set(f.ok.filter(w=>f.vs.every((v,j)=>!a.has(v)||a.get(v)===(w>>j&1))).map(w=>V.reduce((s,v,j)=>s+((w>>f.vs.indexOf(v)&1)<<j),0)))].sort((a,b)=>a-b);return{id,vs:V,ok,ids:f.ids}}).filter(f=>f.ok.length!==2**f.vs.length).map((f,id)=>({...f,id}))}

function selectCover(candidates,n,k=5){let best=null,checks=0,subsets=0;function go(start,chosen,core){if(chosen.length){subsets++;let q=count(chosen.map(i=>candidates[i].guard),n);checks+=q.counts.length;if(q.covered===q.total){if(!best||core.size<best.B.length||core.size===best.B.length&&chosen.length<best.indices.length)best={indices:chosen.slice(),B:[...core].sort((a,b)=>a-b),coverage:q};return}}if(chosen.length===k)return;for(let i=start;i<candidates.length;i++){let C=new Set(core);for(let b of candidates[i].B)C.add(b);if(best&&C.size>best.B.length)continue;go(i+1,chosen.concat(i),C)}}function count(G,r){let counts=[],cov=0n;for(let s=1;s<2**G.length;s++){let a=new Map(),bad=false,k=0;for(let i=0;i<G.length;i++)if(s>>i&1){k++;for(let [v,b] of G[i]){if(a.has(v)&&a.get(v)!==b)bad=true;a.set(v,b)}}let c=bad?0n:1n<<BigInt(r-a.size);counts.push([s,c.toString()]);cov+=k%2?c:-c}return{counts,covered:cov.toString(),total:(1n<<BigInt(r)).toString()}}go(0,[],new Set());return{best,checks,subsets}}

function guardClause(guard,id){let vs=guard.map(p=>p[0]).sort((a,b)=>a-b),w=vs.reduce((s,v,i)=>s+(guard.find(x=>x[0]===v)[1]<<i),0);return{id,vs,ok:Array.from({length:2**vs.length},(_,i)=>i).filter(i=>i!==w)}}

function coreOverlaps(C){return C.map(x=>C.map(y=>x.B.filter(b=>y.B.includes(b)).length))}

function remainderAffine(guards,n){
 // each affine equation represented by [decimal mask, bit]; row reduction in GF(2)
 function normal(eq){let basis=new Map();for(let [mask,b] of eq){let x=BigInt(mask);while(x){let p=x&-x;if(!basis.has(p)){basis.set(p,[x,b]);break}let [y,c]=basis.get(p);x^=y;b^=c}if(!x&&b)return null}return [...basis.values()].map(([x,b])=>[x.toString(),b])}
 let cells=[[]],metrics={normalizations:0,candidates:0,peak:1};for(let G of guards){let next=[];for(let C of cells){let prefix=C;for(let [a,b] of G){metrics.candidates++;let P=normal(prefix.concat([[a,1-b]]));metrics.normalizations++;if(P)next.push(P);prefix=normal(prefix.concat([[a,b]]));metrics.normalizations++;if(!prefix)break}}cells=next;metrics.peak=Math.max(metrics.peak,cells.length)}return{cells,points:cells.reduce((s,C)=>s+(1n<<BigInt(n-C.length)),0n).toString(),metrics}
}

function testRemainder(){let seed=7313,rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return(seed>>>8)%n},n=7,check=0,peak=0,partial=0,full=0;const par=(x)=>{let b=0;while(x){x&=x-1;b^=1}return b};for(let t=0;t<120;t++){let guards=Array.from({length:rnd(6)},()=>Array.from({length:1+rnd(4)},()=>[String(1+rnd(127)),rnd(2)])),q=remainderAffine(guards,n),count=0;peak=Math.max(peak,q.cells.length);for(let w=0;w<128;w++){let accept=g=>g.every(([m,b])=>par(w&Number(m))===b),outside=!guards.some(accept),k=q.cells.filter(accept).length;if(k!==+outside)throw Error("bad affine cells");count+=k;check++}if(BigInt(q.points)!==BigInt(count))throw Error("bad count");if(count)partial++;else full++}return{trials:120,points:check,peak,partial,full}}
module.exports={checkTree,restrict,selectCover,guardClause,coreOverlaps,remainderAffine,testRemainder};
