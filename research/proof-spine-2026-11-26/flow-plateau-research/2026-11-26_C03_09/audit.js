const audit = function audit(){
const assert=(b)=>{if(!b)throw Error("assertion")};
const E=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)E.push([i,j]);
const bit=(a,b)=>1<<E.findIndex(([i,j])=>i===Math.min(a,b)&&j===Math.max(a,b));
const perm=(xs,k=xs.length)=>k===0?[[]]:xs.flatMap((x,i)=>perm(xs.filter((_,j)=>j!==i),k-1).map(y=>[x,...y]));
const P=perm([0,1,2,3,4]),C=[...new Set([3,4,5].flatMap(k=>perm([0,1,2,3,4],k).map(p=>p.reduce((m,x,i)=>m|bit(x,p[(i+1)%k]),0))))].sort((a,b)=>a-b);
const S=Array.from({length:1024},(_,i)=>i).filter(m=>[0,1,2,3,4].every(v=>E.filter(([a,b],i)=>(a===v||b===v)&&(m>>i&1)).length!==1));
const Q=m=>C.filter(c=>!(c&m)).reduce((a,b)=>a|b,0);
const base=[
[7,["12","10","41","63","50","54","60","32"],[2,4,3,6,5]],
[7,["06","14","43","24","21","53","63","50"],[5,0,6,2,1]],
[7,["06","03","25","31","21","26","45","34"],[5,0,4,6,1]],
[1,[],[-1,-1,0,0,0]],
[3,["01","12"],[1,0,2,2,0]],
[5,["01","12","23","34","40"],[3,2,4,1,0]],
[9,["01","05","12","16","27","35","36","46","47","57","48"],[2,3,0,8,8]]];
let nodes=0;
function cost(cap,w){
 let [n,es,ps]=cap,inc=Array.from({length:n},()=>[]),d=Array(n).fill(0),free=ps.map((v,i)=>v===-1?i:-1).filter(x=>x>=0);
 if(free.length&&w[free[0]]!==w[free[1]])return 99;
 es.forEach((e,i)=>{for(let v of e)inc[+v].push(i)});ps.forEach((v,i)=>{if(v>=0)d[v]^=w[i]});
 assert(inc.every((x,v)=>x.length+ps.filter(y=>y===v).length===3));
 let best=99;
 function rec(f){
  nodes++;
  for(;;){let changed=false;for(let v=0;v<n;v++){let unknown=inc[v].filter(i=>f[i]===-1),r=inc[v].reduce((a,i)=>f[i]<0?a:a^f[i],d[v]);if(!unknown.length&&r)return;if(unknown.length===1){f[unknown[0]]=r;changed=true;}}if(!changed)break;}
  let z=f.filter(x=>x===0).length;if(z>=best)return;let j=f.indexOf(-1);if(j<0){best=z;return}for(let c=0;c<4;c++){let g=f.slice();g[j]=c;rec(g);}
 }rec(es.map(()=>-1));return best;
}
const W=E.map(([a,b])=>[0,1,2,3,4].map(i=>i===a?2:i===b?3:1));
const table=base.map(b=>W.map(w=>cost(b,w)));
const V=base.flatMap((b,j)=>P.map(p=>{const v=E.map(([a,b])=>table[j][E.findIndex(([x,y])=>x===Math.min(p[a],p[b])&&y===Math.max(p[a],p[b]))]);return {m:v.reduce((m,z,i)=>m|(z===0?1<<i:0),0),v,j,p};}));
const R=[...new Set(V.filter(v=>v.j<6).map(v=>v.m))].sort((a,b)=>a-b),T=S.filter(t=>t&1),F=R.filter(c=>c&1);
const rel=(a,ts)=>ts.map(t=>+(!!(a&t))).join("");
let groups=new Map(),cycleGroups=new Map(),max=0;
for(let a of S){let k=rel(a,F),r=rel(a,T);assert(!groups.has(k)||groups.get(k)===r);groups.set(k,r);let ck=rel(a,C.filter(c=>c&1));if(!cycleGroups.has(ck))cycleGroups.set(ck,new Set());cycleGroups.get(ck).add(r);if(a){const x=V.filter(v=>v.v[0]<=1&&rel(v.m,T)===r);assert(x.length);max=Math.max(max,Math.min(...x.map(v=>base[v.j][0])));}if(a&1)assert(V.some(v=>v.v[0]===0&&Q(v.m)===Q(a)));}
for(let t of T)assert(F.filter(c=>(c&t)===c).reduce((a,b)=>a|b,0)===t);
for(let c of C)assert(V.some(v=>v.m===c&&v.v[0]<=1));
assert(C.length===37&&S.length===314&&R.length===142&&F.length===75&&groups.size===33&&max===9);
assert(750n*10n**79n<11n**79n);
let dirty=[];for(let k=0;k<1024;k++){let w=Array.from({length:5},(_,i)=>k>>2*i&3);if(w.filter(x=>x===0).length===1&&w.reduce((a,b)=>a^b,0)===0)dirty.push(w)}
const dirtyCosts=base.map(b=>dirty.map(w=>cost(b,w)));
return {table,base,admissible:S.length,cycles:C.length,catalog:R.length,probes:F.length,groups:groups.size,cycleOnlyAmbiguous:[...cycleGroups.values()].filter(s=>s.size>1).length,maximumCap:max,dirtyWords:dirty.length,dirtyZeroFree:dirtyCosts.map(x=>x.filter(z=>z===0).length),nodes};
};
console.log(JSON.stringify(audit(),null,2));
