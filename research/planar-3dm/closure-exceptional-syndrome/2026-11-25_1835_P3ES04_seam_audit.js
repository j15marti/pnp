function seamAudit(){
let seed=73951,checks=0,used=0,notUsed=0,zero=0,infeasible=0;const rnd=n=>((seed=(Math.imul(seed,1664525)+1013904223)>>>0)%n);const assert=(x)=>{if(!x)throw Error("seam mismatch");checks++};
function rank(A){let B={};for(let x of A){while(x){let k=31-Math.clz32(x);if(B[k])x^=B[k];else{B[k]=x;break}}}return Object.keys(B).length}
function min(A,b,w){let best=Infinity,ids=[];for(let mask=0;mask<2**A.length;mask++){let s=0,c=0,I=[];for(let j=0;j<A.length;j++)if(mask&(1<<j)){s^=A[j];c+=w[j];I.push(j)}if(s===b&&c<best){best=c;ids=I}}return {cost:best,ids}}
for(let k=0;k<500;k++){let L=[2,3,...Array.from({length:4},()=>1+rnd(7))],R=[8,9,...Array.from({length:4},()=>{let x=1+rnd(7);return (x&1)|((x&6)<<2)})],q=1;let t=(1+rnd(7));t=(t&1)|((t&6)<<2);let wL=L.map(()=>rnd(6)),wR=R.map(()=>rnd(6));let root=R.concat(t);assert(rank(L)+rank(root)-rank(L.concat(root))===1);let l=min(L,q,wL);let r=min([...R,q],t,[...wR,l.cost]);let z=min(L.concat(R),t,wL.concat(wR));assert(r.cost===z.cost);if(!Number.isFinite(r.cost)){infeasible++;continue}if(r.cost===0)zero++;if(r.ids.includes(R.length))used++;else notUsed++;let ids=[...r.ids.filter(i=>i<R.length).map(i=>L.length+i),...(r.ids.includes(R.length)?l.ids:[])],A=L.concat(R),w=wL.concat(wR);assert(ids.reduce((s,i)=>s^A[i],0)===t);assert(ids.reduce((s,i)=>s+w[i],0)===z.cost)}
const L=[1,2,3],w=[2,2,1];const table=[0,1,2,3].map(t=>min(L,t,w).cost);assert(table[3]!==table[1]+table[2]);
return {seed:73951,randomRankOneSeams:500,assertions:checks,usedVirtualColumn:used,omittedVirtualColumn:notUsed,infeasible,zeroOptimum:zero,rankTwoJointCostTable:table}
}
console.log(JSON.stringify(seamAudit(),null,2));
