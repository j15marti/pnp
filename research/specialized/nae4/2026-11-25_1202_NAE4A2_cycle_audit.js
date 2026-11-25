function cycleAudit(){
let checks=0,seed=20261125,cases=0,cycles=0,restorations=0,unsafe=0;const rnd=()=>seed=(Math.imul(seed,1664525)+1013904223)>>>0,ck=(x)=>{checks++;if(!x)throw Error("cycle audit "+checks)};
const plane=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]],layered=Array.from({length:4},(_,p)=>Array.from({length:5},(_,i)=>[i,5+(i+p)%5,10+(i+2*p)%5]));
const rank=(rows,n)=>{let b=Array(n).fill(0);for(let w of rows){for(let i=n-1;i>=0;i--)if((w>>>i)&1){if(b[i])w^=b[i];else{b[i]=w;break}}}return b.filter(Boolean).length};
const good=(c,w)=>{let s=c.reduce((a,i)=>a+((w>>>i)&1),0);return s===1||s===2};
for(const P of [plane,layered]){let n=P[0].length*3,k=n/3,H=2*k,V=H+1;for(let a=0;a<4;a++)for(let b=a+1;b<4;b++){let C=P[a].concat(P[b]),all=Array.from({length:2**n},(_,w)=>w).filter(w=>C.every(c=>good(c,w)));let L=[],R=[];P[a].forEach((c,i)=>c.forEach(v=>L[v]=i));P[b].forEach((c,i)=>c.forEach(v=>R[v]=k+i));
for(let t=0;t<24;t++){let pins=Array(n).fill(null);if(t)for(let j=0;j<1+t%6;j++)pins[rnd()%n]=(rnd()>>>16)&1;
let F=all.filter(w=>pins.every((p,i)=>p===null||((w>>>i)&1)===p));if(!F.length)continue;let w=F[0],arcs=[],f=[];
for(let i=0;i<n;i++){arcs.push([L[i],R[i],pins[i]??0,pins[i]??1]);f.push((w>>>i)&1)}
for(let i=0;i<k;i++){arcs.push([H,i,1,2]);f.push(P[a][i].reduce((s,v)=>s+((w>>>v)&1),0))}
for(let i=0;i<k;i++){arcs.push([k+i,H,1,2]);f.push(P[b][i].reduce((s,v)=>s+((w>>>v)&1),0))}
let edges=[],adj=Array.from({length:V},()=>[]);for(let i=0;i<arcs.length;i++){let [u,v,l,h]=arcs[i];if(l===h)continue;let e=f[i]===l?{u,v,i,d:1}:{u:v,v:u,i,d:-1};edges.push(e);adj[e.u].push(e)}
function paths(root){let p=Array(V).fill(null);p[root]=[];let q=[root];for(let j=0;j<q.length;j++){let u=q[j];for(let e of adj[u])if(p[e.v]===null){p[e.v]=p[u].concat(e);q.push(e.v)}}return p}
let reach=Array.from({length:V},(_,v)=>paths(v)),seen=new Set(),words=[w];
function walk(W){let stack=[],vertices=[W[0].u];for(let e of W){ck(vertices[vertices.length-1]===e.u);let j=vertices.indexOf(e.v);stack.push(e);vertices.push(e.v);if(j>=0){let cyc=stack.slice(j),ff=f.slice(),z=w;for(let e of cyc){ff[e.i]+=e.d;if(e.i<n)z^=1<<e.i}ck(ff.every((x,i)=>x>=arcs[i][2]&&x<=arcs[i][3]));let bal=Array(V).fill(0);arcs.forEach(([u,v],i)=>{bal[u]-=ff[i];bal[v]+=ff[i]});ck(bal.every(x=>x===0));ck(F.includes(z));words.push(z);cycles++;stack=stack.slice(0,j);vertices=vertices.slice(0,j+1)}}ck(stack.length===0)}
for(let r=0;r<V;r++){if(seen.has(r))continue;let S=Array.from({length:V},(_,i)=>i).filter(i=>reach[r][i]!==null&&reach[i][r]!==null);S.forEach(v=>seen.add(v));for(let v of S)if(v!==r)walk(reach[r][v].concat(reach[v][r]));for(let e of edges)if(S.includes(e.u)&&S.includes(e.v))walk(reach[r][e.u].concat(e,reach[e.v][r]))}
ck(rank(words.map(z=>z^w),n)===rank(F.map(z=>z^w),n));cases++;
for(let p=0;p<4;p++)if(p!==a&&p!==b)for(let c of P[p]){ck(words.some(z=>good(c,z))===F.some(z=>good(c,z)));restorations++;if(t===0){for(let mask=0;mask<8;mask++){ck(F.some(z=>c.every((v,j)=>((z>>>v)&1)===((mask>>>j)&1))));unsafe++}}}
}}}
return {seed:20261125,checks,cases,cycles,restorations,matchingProjectionChecks:unsafe,scope:"Exhaustive side anchor/reference in this finite test only. Actual residual simple cycle witnesses reconstructed, checked and compared with exhaustive hull; no joint decision or DS17 expanded test."}}
console.log(JSON.stringify(cycleAudit(),null,2));
