"use strict";
const audit=function(){
const V=[[0,0,1],[0,1,1],[0,2,2],[1,0,1],[1,1,0],[2,0,2],[2,2,2],[2,3,3],[3,2,0],[3,3,3]];
const U=V.filter(t=>String(t)!=="2,2,2");
const rotations=[
[[12,14,13],[15,16],[19,18,17],[20,21],[12,15,17],[16,13],[14,18,20],[21,19],[16,20],[13,15,12],[17,18,14],[19,21],[0,9,4],[5,9,0],[10,6,0],[4,9,1],[1,5,8],[2,10,4],[6,10,2],[7,2,11],[8,6,3],[3,7,11]],
[[12,14,13],[15,16],[18,17],[19,20],[12,15,17],[16,13],[14,19],[20,18],[16,19],[13,15,12],[17,14],[18,20],[0,9,4],[5,9,0],[10,6,0],[4,9,1],[1,5,8],[2,10,4],[7,2,11],[8,6,3],[3,7,11]]
];
let checks=0;const ok=(b,m)=>{checks++;if(!b)throw Error(m)};
function plane(T,R){const E=Array.from({length:12+T.length},()=>[]);T.forEach((t,k)=>t.forEach((v,j)=>{E[4*j+v].push(12+k);E[12+k].push(4*j+v)}));for(let i=0;i<E.length;i++)ok(String(E[i].sort((a,b)=>a-b))===String([...R[i]].sort((a,b)=>a-b)),"rotation edges");const seen=new Set([0]),q=[0];for(const v of q)for(const w of R[v])if(!seen.has(w)){seen.add(w);q.push(w)}ok(q.length===R.length,"connected");const used=new Set();let faces=0;for(let i=0;i<R.length;i++)for(const j of R[i]){if(used.has(i+","+j))continue;let a=i,b=j;faces++;do{ok(!used.has(a+","+b),"face repeat");used.add(a+","+b);const k=R[b].indexOf(a);[a,b]=[b,R[b][(k+1)%R[b].length]]}while(a!==i||b!==j)}ok(R.length-3*T.length+faces===2,"Euler");return faces}
function matching(T,n){const out=[];function go(i,Y,M){if(i===n){out.push(M);return}T.forEach((t,j)=>{if(t[0]===i&&!Y.has(t[1]))go(i+1,new Set([...Y,t[1]]),[...M,j])})}go(0,new Set(),[]);return out}
function affine(T){let sol=[];for(let w=0;w<(1<<T.length);w++){let c=Array(12).fill(0);T.forEach((t,i)=>{if(w>>i&1)t.forEach((x,j)=>c[4*j+x]++)});if(c.every(x=>x%2===1))sol.push(w)}const pins=[];if(sol.length)for(let i=0;i<T.length;i++)if(sol.every(w=>((w^sol[0])>>i&1)===0))pins.push([T[i],sol[0]>>i&1]);return {paritySolutions:sol.length,pins}}
function constant(T,H){const ref=matching(T,4)[0],byX=[],byY=[];for(const i of ref){byX[T[i][0]]=i;byY[T[i][1]]=T[i][0]}function red(w){for(const p of H){const bit=1<<(31-Math.clz32(p));if(w&bit)w^=p}return w}
const A=T.map((t,i)=>[t[0],byY[t[1]],red((1<<t[2])^(1<<T[byX[t[0]]][2]))]);const reach=Array.from({length:4},(_,i)=>Array.from({length:4},(_,j)=>i===j));for(const [u,v] of A)reach[u][v]=true;for(let k=0;k<4;k++)for(let i=0;i<4;i++)for(let j=0;j<4;j++)reach[i][j] ||= reach[i][k]&&reach[k][j];const adj=Array.from({length:4},()=>[]);for(const [u,v,w] of A)if(reach[v][u]){adj[u].push([v,w]);adj[v].push([u,w])}const P=Array(4).fill(null);for(let i=0;i<4;i++)if(P[i]===null){P[i]=0;const q=[i];for(const u of q)for(const [v,w] of adj[u]){if(P[v]===null){P[v]=P[u]^w;q.push(v)}else if(P[v]!== (P[u]^w))return null}}
return red(ref.reduce((s,i)=>s^(1<<T[i][2]),0))}
let fixtures=[];for(const [i,T] of [V,U].entries()){const faces=plane(T,rotations[i]),counts={};for(const M of matching(T,4)){const s=M.reduce((w,j)=>w^(1<<T[j][2]),0);counts[s]=(counts[s]||0)+1}const H=i===0?[5,3]:[3],q=constant(T,H);ok(q!==null,"constant test");let target=15;for(const p of H)if(target&(1<<(31-Math.clz32(p))))target^=p;ok((q===target)===(i===0),"constant decision");fixtures.push({name:i===0?"V":"U",faces,counts,quotient:q,target,affine:affine(T)})}
return {checks,fixtures,scope:"Rotation certificates verified via connected orientable rotation and Euler characteristic. SCC potential test executed on two fixtures; reference matching acquired here by enumeration only on constant-size four-row controls. Affine pins independently checked by exhaustive reference; not a production Gaussian implementation."};
};
console.log(JSON.stringify(audit(),null,2));
