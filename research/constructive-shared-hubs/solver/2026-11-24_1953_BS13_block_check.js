"use strict";
function supplementBS13(){
const stats={sccQueries:0,edgeVisits:0,referenceWords:0,wheelWords:0};
function sat(n,rs,pins={}){
 stats.sccQueries++;let g=Array.from({length:2*n},()=>[]),h=g.map(()=>[]);
 function edge(a,b){g[a].push(b);h[b].push(a)}
 function forbid(u,a,v,b){edge(2*u+a,2*v+(1-b));edge(2*v+b,2*u+(1-a))}
 for(let [u,v,m] of rs)for(let a=0;a<2;a++)for(let b=0;b<2;b++)if(!(m>>(2*a+b)&1))forbid(u,a,v,b);
 for(let k in pins)edge(2*(+k)+(1-pins[k]),2*(+k)+pins[k]);
 let seen=new Set(),order=[];function dfs(v){seen.add(v);for(let u of g[v]){stats.edgeVisits++;if(!seen.has(u))dfs(u)}order.push(v)}
 for(let i=0;i<2*n;i++)if(!seen.has(i))dfs(i);
 let comp=Array(2*n).fill(-1),c=0;function dfs2(v){comp[v]=c;for(let u of h[v]){stats.edgeVisits++;if(comp[u]<0)dfs2(u)}}
 for(let v of order.reverse())if(comp[v]<0){dfs2(v);c++}
 return Array.from({length:n},(_,i)=>i).every(i=>comp[2*i]!==comp[2*i+1])
}
function valid(rs,a){return rs.every(([u,v,m])=>!!(m>>(2*a[u]+a[v])&1))}
function support(n,rs,u,v){let mask=0;for(let a=0;a<2;a++)for(let b=0;b<2;b++)if(sat(n,rs,{[u]:a,[v]:b}))mask|=1<<(2*a+b);return mask}
function witness(n,rs,pins={}){if(!sat(n,rs,pins))return null;let p={...pins};for(let i=0;i<n;i++)if(!(i in p)){p[i]=0;if(!sat(n,rs,p))p[i]=1}return p}
let seed=123456789,rand=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
let cases={sat:0,unsat:0},scales=[];
for(let t=0;t<120;t++){let n=7,rs=[];for(let i=0;i<12;i++){let u=rand(n),v=(u+1+rand(n-1))%n;rs.push([u,v,1+rand(15)])}let exp=0;for(let i=0;i<1<<n;i++){stats.referenceWords++;let a=Array.from({length:n},(_,j)=>i>>j&1);if(valid(rs,a))exp|=1<<(2*a[0]+a[1])}
 let got=support(n,rs,0,1);if(got!==exp)throw Error("support mismatch");for(let k=0;k<4;k++)if(got>>k&1){let w=witness(n,rs,{0:k>>1,1:k&1});if(!w||!valid(rs,w))throw Error("witness mismatch")}cases[got?"sat":"unsat"]++}
for(let n of [8,32,64])for(let flip of [false,true]){let rs=[];for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)rs.push([u,v,flip&&u===0&&v===1?6:9]);let s=support(n,rs,0,n-1);if(s!==(flip?0:9))throw Error("dense support");let w=witness(n,rs);if(!!w===flip||w&&!valid(rs,w))throw Error("dense witness");scales.push({n,relations:rs.length,flip,support:s})}
for(let signs=0;signs<8;signs++)for(let a=0;a<4;a++)for(let b=0;b<4;b++)for(let c=0;c<4;c++){
 let sa=signs&1,sb=signs>>1&1,sc=signs>>2&1,al=(a&1)^sa,bl=(b&1)^sb,cl=(c&1)^sc;
 let ok=true;
 for(let eta=0;eta<2;eta++){let f=new Set([a^sa,a^sa^2,b^sb^1,c^sc^3^(2*eta)]);if(f.size===4)ok=false}
 if(ok===(al===bl&&bl===cl))throw Error("wheel double-star relation");stats.wheelWords++;
}
return {cases,scales,stats}
}
console.log(JSON.stringify(supplementBS13(),null,2));
