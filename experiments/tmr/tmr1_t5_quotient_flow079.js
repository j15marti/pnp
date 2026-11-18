'use strict';
// TMR-1/079: unannotated T5 forced-triad quotient -> exact integer dual-flow count.
// Standard Node.js, no dependency. All counts exact BigInt; deterministic finite tests.
const mod=x=>((x%5)+5)%5;
function parse(s){
 if(typeof s!=='string'||/[^01]/.test(s))throw Error('symbols');
 let i=0;while(s[i]==='1')i++;if(s[i++]!=='0')throw Error('n header');const n=i-1;
 let j=i;while(s[i]==='1')i++;if(s[i++]!=='0')throw Error('m header');const m=i-j-1;
 const w=Math.max(1,Math.ceil(Math.log2(Math.max(2,n))));
 if(s.length!==i+2*m*w)throw Error('length');
 const a=[];let last=[-1,-1];const get=()=>{let v=0;for(let k=0;k<w;k++)if(s[i++]==='1')v+=2**k;return v;};
 for(let t=0;t<m;t++){
   const u=get(),v=get();if(u>=n||v>=n||u<last[0]||(u===last[0]&&v<=last[1]))throw Error('order/range');
   a.push([u,v]);last=[u,v];
 }return {n,arcs:a};
}
function encode(n,arcs){const a=[...arcs].sort((a,b)=>a[0]-b[0]||a[1]-b[1]);const w=Math.max(1,Math.ceil(Math.log2(Math.max(2,n))));const bits=v=>Array.from({length:w},(_,i)=>(v>>i)&1).join('');return '1'.repeat(n)+'0'+'1'.repeat(a.length)+'0'+a.map(([u,v])=>bits(u)+bits(v)).join('');}
class UF{
 constructor(n){this.p=Array.from({length:n},(_,i)=>i);this.d=Array(n).fill(0);this.r=Array(n).fill(0);}
 find(x){if(this.p[x]===x)return [x,0];const [p,d]=this.find(this.p[x]);this.d[x]=mod(this.d[x]+d);this.p[x]=p;return [p,this.d[x]];}
 eq(u,v,k){const [a,da]=this.find(u),[b,db]=this.find(v),t=mod(k+da-db);if(a===b)return t===0;if(this.r[a]<this.r[b]){this.p[a]=b;this.d[a]=mod(-t);}else{this.p[b]=a;this.d[b]=t;if(this.r[a]===this.r[b])this.r[a]++;}return true;}
}
function quotient({n,arcs}){
 const set=new Set(arcs.map(e=>e.join(',')));
 if(arcs.some(([u,v])=>u===v||set.has(v+','+u)))return null;
 const uf=new UF(n),adj=Array.from({length:n},()=>Array(n).fill(false));
 for(const [u,v] of arcs)adj[u][v]=true;
 for(let u=0;u<n;u++)for(let v=0;v<n;v++)if(adj[u][v])for(let w=0;w<n;w++)if(adj[v][w]&&adj[u][w]){if(!uf.eq(u,v,3)||!uf.eq(u,w,1))return null;}
 const ids=[],off=[],map=new Map();for(let u=0;u<n;u++){const [r,p]=uf.find(u);if(!map.has(r))map.set(r,map.size);ids[u]=map.get(r);off[u]=p;}
 const masks=new Map();for(const [u,v] of arcs){let a=ids[u],b=ids[v],pu=off[u],pv=off[v];if(a===b){if(![1,3].includes(mod(pv-pu)))return null;continue;}
 const lo=Math.min(a,b),hi=Math.max(a,b),key=lo+','+hi;const d=[1,3].map(s=>a===lo?mod(s+pu-pv):mod(pv-pu-s));let mask=(masks.get(key)??31)&d.reduce((x,z)=>x|(1<<z),0);if(!mask)return null;masks.set(key,mask);}
 const edges=[...masks.entries()].map(([key,mask])=>{const [u,v]=key.split(',').map(Number);return {u,v,D:Array.from({length:5},(_,j)=>j).filter(j=>mask&(1<<j))};}).sort((a,b)=>a.u-b.u||a.v-b.v);
 return {n:map.size,edges};
}
function countFlow(n,edges){
 const m=edges.length,p=Array.from({length:n},(_,i)=>i),sz=Array(n).fill(1);const find=x=>{while(p[x]!==x){p[x]=p[p[x]];x=p[x];}return x;};
 const tree=[],chord=[];edges.forEach((e,i)=>{let a=find(e.u),b=find(e.v);if(a===b)chord.push(i);else{if(sz[a]<sz[b])[a,b]=[b,a];p[b]=a;sz[a]+=sz[b];tree.push(i);}});
 const adj=Array.from({length:n},()=>[]);for(const i of tree){const e=edges[i];adj[e.u].push([e.v,i]);adj[e.v].push([e.u,i]);}
 const parent=Array(n).fill(-1),pe=Array(n).fill(-1),seen=Array(n).fill(false),order=[];let c=0;
 for(let root=0;root<n;root++)if(!seen[root]){c++;seen[root]=true;const stack=[root];while(stack.length){const v=stack.pop();order.push(v);for(const [u,i] of adj[v])if(!seen[u]){seen[u]=true;parent[u]=v;pe[u]=i;stack.push(u);}}}
 const k=Array(m).fill(0),A=[0n,0n,0n,0n,0n],r=chord.length;
 function visit(j){if(j<r){for(let x=0;x<5;x++){k[chord[j]]=x;visit(j+1);}return;}
 const div=Array(n).fill(0);for(const i of chord){const e=edges[i];div[e.u]=mod(div[e.u]-k[i]);div[e.v]=mod(div[e.v]+k[i]);}
 for(let t=order.length-1;t>=0;t--){const v=order[t],u=parent[v];if(u<0){if(div[v])throw Error('divergence');continue;}const i=pe[v],e=edges[i],sign=e.v===v?1:-1;k[i]=mod(-sign*div[v]);div[u]=mod(div[u]+(e.v===u?k[i]:-k[i]));}
 let q=[1n,0n,0n,0n,0n];for(let i=0;i<m;i++){const z=[0n,0n,0n,0n,0n];for(let a=0;a<5;a++)for(const d of edges[i].D)z[mod(a-k[i]*d)]+=q[a];q=z;}for(let a=0;a<5;a++)A[a]+=q[a];
 }visit(0);
 if(!(A[1]===A[2]&&A[2]===A[3]&&A[3]===A[4]))throw Error('Galois invariance');let ans=A[0]-A[1];const exp=n-m;
 if(exp>=0)ans*=5n**BigInt(exp);else{const den=5n**BigInt(-exp);if(ans%den)throw Error('noninteger');ans/=den;}
 if(ans<0n)throw Error('negative');return {count:ans,rho:r,components:c};
}
function solve(word){const g=parse(word),q=quotient(g);return q===null?{count:0n,contradiction:true}:countFlow(q.n,q.edges);}
function brute(n,arcs,cyclic=false){let z=0n;for(let s=0;s<5**n;s++){const a=[];let k=s;for(let i=0;i<n;i++){a[i]=k%5;k=Math.floor(k/5);}if(arcs.every(([u,v])=>(cyclic?[1,4]:[1,3]).includes(mod(a[v]-a[u]))))z++;}return z;}
function gadget(n,edges){const out=[];edges.forEach(([u,v],i)=>{const z=n+2*i,w=z+1;out.push([u,z],[u,w],[w,z],[w,v]);});return [n+2*edges.length,out];}
function audit(){let tested=0,yes=0,no=0,comp=0;for(let n=0;n<=3;n++){const all=[];for(let i=0;i<n;i++)for(let j=0;j<n;j++)all.push([i,j]);for(let mask=0;mask<2**all.length;mask++){const a=all.filter((_,i)=>(mask>>i)&1),got=solve(encode(n,a)).count,exp=brute(n,a);if(got!==exp)throw Error('raw mismatch');tested++;yes+=exp>0n;no+=exp===0n;}}
 for(let n=1;n<=4;n++){const all=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)all.push([i,j]);for(let mask=0;mask<2**all.length;mask++){const e=all.filter((_,i)=>(mask>>i)&1);if(e.length>3)continue;const [N,a]=gadget(n,e);if(solve(encode(N,a)).count!==brute(n,e,true))throw Error('gadget mismatch');comp++;}}
 return {revision:'tmr1-t5-quotient-flow079-js-v1',raw_graph_cases:tested,raw_yes:yes,raw_no:no,composition_cases:comp,failures:0};}
if(require.main===module)console.log(JSON.stringify(audit(),null,2));
module.exports={parse,encode,quotient,countFlow,solve,brute,gadget,audit};
