/* Run node checker.js bw17.json ms27_support.json bs19_results.json. Exact reference only. */
const fs=require('fs');
const check=function check(data){
 let assertions=0,visits=0,scans=0,forced=0;const assert=(b)=>{assertions++;if(!b)throw Error("assertion "+assertions)};
 let seed=2601125;const rand=()=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296};
 const row=(x,t)=>t.reduce((a,v,i)=>a+(((x>>>v)&1)<<i),0);
 const accepts=(x,O)=>O.every(o=>!o.bad.includes(row(x,o.t)));
 function close(O,n){let p=Array(n).fill(-1),change=true;while(change){change=false;for(const o of O){scans++;const good=Array.from({length:8},(_,i)=>i).filter(i=>!o.bad.includes(i)&&o.t.every((v,j)=>p[v]<0||p[v]===((i>>j)&1)));if(!good.length)return false;for(let j=0;j<3;j++)if(p[o.t[j]]<0&&good.every(i=>((i>>j)&1)===((good[0]>>j)&1))){p[o.t[j]]=(good[0]>>j)&1;forced++;change=true;}}}return true}
 function models(O,n){assert(close(O,n));let a=[];for(let x=0;x<2**n;x++){visits++;if(accepts(x,O))a.push(x)}return a}
 const controls=[];for(const n of [9,12,15]){let O;let attempts=0;do{O=[];for(let p=0;p<8;p++){let v=Array.from({length:n},(_,i)=>i);for(let j=n-1;j>0;j--){let k=Math.floor(rand()*(j+1));[v[j],v[k]]=[v[k],v[j]]}for(let j=0;j<n;j+=3){const b=Math.floor(rand()*8);O.push({p,t:v.slice(j,j+3),bad:[b,b^7]})}}attempts++;if(attempts>100)throw Error("no root");}while(models(O,n).length);
 const initial=O.length;for(let i=O.length-1;i>=0;i--){const R=O.filter((_,j)=>i!==j);if(!models(R,n).length)O=R}
 assert(models(O,n).length===0);let neighbors=0;for(let i=0;i<O.length;i++){const R=O.filter((_,j)=>i!==j);const w=models(R,n)[0];assert(w!==undefined);for(let b=0;b<3;b++){const R=O.map((o,j)=>j===i?{...o,bad:o.bad.map(v=>v^(1<<b))}:o);assert(accepts(w,R));neighbors++}}
 const degree=Array(n).fill(0);O.forEach(o=>o.t.forEach(v=>degree[v]++));assert(Math.max(...degree)<=8);controls.push({n,attempts,initial,critical:O.length,maxDegree:Math.max(...degree),neighbors,registry:O});}
 // Replay exact BW17 fractional marginal support from independently supplied tangent.
 const O=data.bw.O,n=data.bw.n;assert(close(O,n));const key=(u,v)=>[u,v].sort((a,b)=>a-b).join(",");const edges=new Map(data.s.edgeOrder.map((e,i)=>[e,data.s.tangent[i]]));const owner=new Set(O.map(o=>o.t.slice().sort((a,b)=>a-b).join(",")));assert(O.every(o=>o.bad.includes(0)&&o.bad.includes(7)));for(const o of O){const [a,b,c]=o.t;assert(edges.has(key(a,b))&&edges.has(key(a,c))&&edges.has(key(b,c)));assert(edges.get(key(a,b))+edges.get(key(a,c))+edges.get(key(b,c))===0)}
 let zero=0,pos=0,min=Infinity;const pair=(a,b)=>edges.has(key(a,b))?200+edges.get(key(a,b)):150; // mismatch numerator /300
 // spin weight p=(1 + sum c*s*s)/8, c=(300-2d)/300; denominator 2400.
 for(let a=0;a<n;a++)for(let b=a+1;b<n;b++)for(let c=b+1;c<n;c++){
 let weights=[];for(let w=0;w<8;w++){let v=300;const s=i=>((w>>i)&1)?-1:1;v+=(300-2*pair(a,b))*s(0)*s(1)+(300-2*pair(a,c))*s(0)*s(2)+(300-2*pair(b,c))*s(1)*s(2);assert(v>=0);assert((v===0)===(owner.has([a,b,c].join(","))&&(w===0||w===7)));weights.push(v);if(v===0)zero++;else{pos++;min=Math.min(min,v)}}assert(weights.reduce((a,b)=>a+b,0)===2400);for(const [i,j,u,v] of [[0,1,a,b],[0,2,a,c],[1,2,b,c]])assert(weights.reduce((sum,z,w)=>sum+((((w>>i)^(w>>j))&1)?z:0),0)===8*pair(u,v));}
 // Actual existing source witness and residual reverse map: no new acquisition.
 const K=data.k.common.find(x=>x.K===16).residual;const original=12130883;assert(accepts(original,O));
 const lit=(x,l)=>((x>>>(Math.abs(l)-1))&1)^Number(l<0);
 const nae=(x,L)=>L.some(l=>lit(x,l)!==lit(x,L[0]));
 assert(K.C.every(L=>nae(original,L)));let x=original;for(const b of K.log)x&=~(1<<(b.v-1));for(const b of K.log.slice().reverse()){const z=x|(1<<(b.v-1));if(b.bucket.every(L=>nae(x,[b.v,...L]))){}else{assert(b.bucket.every(L=>nae(z,[b.v,...L])));x=z}}assert(accepts(x,O));
 return {assertions,visits,scans,forced,controls,bw:{zero,pos,minNumerator:min,denominator:2400,original,reverseLift:x,logs:K.log.length,wide:K.C.filter(L=>L.length>3).length}};
};
const [bw,s,k]=process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')));
console.log(JSON.stringify(check({bw,s,k}),null,2));
