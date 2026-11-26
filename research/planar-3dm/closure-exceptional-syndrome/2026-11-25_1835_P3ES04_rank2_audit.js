function higherSeams(){
let seed=84371;const rnd=n=>((seed=(Math.imul(seed,1664525)+1013904223)>>>0)%n);let checks=0,usedMultiple=0,infeasible=0;const assert=x=>{if(!x)throw Error("rank-two seam mismatch");checks++};
function rank(A){let B={};for(let x of A){while(x){let k=31-Math.clz32(x);if(B[k])x^=B[k];else{B[k]=x;break}}}return Object.keys(B).length}
function min(A,b,w){let best=Infinity,ids=[];for(let mask=0;mask<2**A.length;mask++){let s=0,c=0,I=[];for(let j=0;j<A.length;j++)if(mask&(1<<j)){s^=A[j];c+=w[j];I.push(j)}if(s===b&&c<best){best=c;ids=I}}return {cost:best,ids}}
for(let k=0;k<400;k++){let L=[1,2,4,...Array.from({length:3},()=>1+rnd(7))],R=[1,2,8,...Array.from({length:3},()=>{let x=1+rnd(7);return (x&3)|((x&4)<<1)})],t=1+rnd(7);t=(t&3)|((t&4)<<1);let wL=L.map(()=>rnd(6)),wR=R.map(()=>rnd(6));assert(rank(L)+rank([...R,t])-rank([...L,...R,t])===2);let Q=[1,2,3],f=Q.map(q=>min(L,q,wL)),r=min([...R,...Q],t,[...wR,...f.map(x=>x.cost)]),z=min([...L,...R],t,[...wL,...wR]);assert(r.cost===z.cost);if(!Number.isFinite(r.cost)){infeasible++;continue}let mask=0,out=[];for(let i of r.ids){if(i<R.length)out.push(L.length+i);else for(let j of f[i-R.length].ids)mask^=1<<j}if(r.ids.filter(i=>i>=R.length).length>1)usedMultiple++;for(let i=0;i<L.length;i++)if(mask&(1<<i))out.push(i);let A=[...L,...R],w=[...wL,...wR];assert(out.reduce((s,i)=>s^A[i],0)===t);assert(out.reduce((s,i)=>s+w[i],0)===r.cost)}
return {seed:84371,rankTwoSeams:400,assertions:checks,multipleVirtualColumns:usedMultiple,infeasible}
}
console.log(JSON.stringify(higherSeams(),null,2));
