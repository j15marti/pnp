"use strict";
function audit(){
const E=[[[0,1],[2,3]],[[0,2],[1,4]],[[0,3],[2,4]],[[0,4],[1,3]],[[1,2],[3,4]]].flat();
let checks=0,fullSat=0,fullNo=0,oneOmittedFailures=0,force=0;const ok=(x)=>{checks++;if(!x)throw Error("disagreement")};
for(let sign=0;sign<1024;sign++){const masks=[],cutWords=[];for(let x=0;x<32;x++){let m=0,c=0;for(let i=0;i<10;i++){const [u,v]=E[i];const bit=((x>>u)^(x>>v))&1;c|=bit<<i;if(bit===((sign>>i)&1))m|=1<<(i>>1);}masks.push(m);cutWords.push(c);}
if(masks.includes(31))fullSat++;else fullNo++;
for(let i=0;i<10;i++)for(let s=0;s<2;s++){const can=new Uint8Array(32);for(let x=0;x<32;x++)if(((cutWords[x]>>i)&1)===s)can[masks[x]]=1;for(let j=0;j<5;j++)for(let T=0;T<32;T++)if(!(T&(1<<j)))can[T]|=can[T|(1<<j)];for(let T=0;T<32;T++)if(!(T&(1<<(i>>1)))){if(T===(31^(1<<(i>>1)))){if(!can[T])oneOmittedFailures++;}else{ok(can[T]);force++;}}}
}
const cross=[];for(const n of [5,9,33,129,513]){let edges=[];for(let i=0;i<n;i++)for(const d of [1,2])edges.push([i,(i+d)%n]);edges=edges.filter(([u,v])=>u!==0||v!==1);const G=edges.map(e=>[e,e.map(v=>v+n)]);G.push([[0,n],[1,n+1]]);const deg=Array(2*n).fill(0),seen=new Set();for(const a of G){ok(new Set(a.flat()).size===4);for(const [u,v] of a){const k=Math.min(u,v)+":"+Math.max(u,v);ok(!seen.has(k));seen.add(k);deg[u]++;deg[v]++;}}ok(deg.every(d=>d===4));const cut=G.flat().filter(([u,v])=>(u<n)!==(v<n)).length;const crossing=G.filter(a=>a.every(([u,v])=>(u<n)===(v<n))&&(a[0][0]<n)!==(a[1][0]<n)).length;ok(cut===2&&crossing===2*n-1);cross.push({n,physicalCut:cut,nonlocalGroups:crossing});}
return{allK5Signings:1024,fullSat,fullNo,force,oneOmittedFailures,checks,cross};
}
console.log(JSON.stringify(audit(),null,2));
