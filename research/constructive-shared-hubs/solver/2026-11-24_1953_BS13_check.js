"use strict";
function runBS13(){
const stats={closureScans:0,pins:0,matchingCalls:0,matchingVertices:0,matchingEdges:0,blossoms:0,regionalQueries:0,blockTransitions:0,blocks:0,cycleBlocks:0,branches:0,countWords:0,declines:0};
const chk=(x,m)=>{if(!x)throw Error(m)};
const row=(v,l,u,s=v.map(()=>0))=>({v,l,u,s});
const valid=(F,a)=>F.every(r=>{let k=r.v.reduce((z,v,i)=>z+(a[v]^r.s[i]),0);return k>=r.l&&k<=r.u});
function merge(a,b){let c={...a};for(let k in b){if(k in c&&c[k]!==b[k])return null;c[k]=b[k]}return c}
function close(F,p={}){
 let a={...p};
 for(;;){stats.closureScans++;let G=[],pin=null;
 for(let r of F){let v=[],s=[],l=r.l,u=r.u;
 for(let i=0;i<r.v.length;i++){let x=r.v[i];if(x in a){let z=a[x]^r.s[i];l-=z;u-=z}else{v.push(x);s.push(r.s[i])}}
 l=Math.max(0,l);u=Math.min(v.length,u);if(l>u)return null;
 if(l===0&&u===v.length)continue;
 if(u===0||l===v.length){pin=[v[0],s[0]^(u===0?0:1)];break}
 G.push(row(v,l,u,s))}
 if(!pin){let basis=new Map();
 for(let r of G)if(r.l===r.u){let m=0n,b=r.l&1;for(let i=0;i<r.v.length;i++){m^=1n<<BigInt(r.v[i]);b^=r.s[i]}
 while(m){let k=m.toString(2).length-1;if(!basis.has(k)){basis.set(k,[m,b]);break}let q=basis.get(k);m^=q[0];b^=q[1]}
 if(!m&&b)return null}
 let ks=[...basis.keys()].sort((x,y)=>x-y);
 for(let k of ks){let [m,b]=basis.get(k);for(let j of ks){if(j>=k)break;if((m>>BigInt(j))&1n){let q=basis.get(j);m^=q[0];b^=q[1]}}basis.set(k,[m,b]);if((m&(m-1n))===0n){pin=[k,b];break}}
 }
 if(!pin)return {G,a};a[pin[0]]=pin[1];stats.pins++;
 }
}
function blossom(g){
 let n=g.length,mt=Array(n).fill(-1),p,base,used,bl;
 function lca(a,b){let seen=Array(n).fill(false);for(;;){a=base[a];seen[a]=true;if(mt[a]<0)break;a=p[mt[a]]}for(;;){b=base[b];if(seen[b])return b;b=p[mt[b]]}}
 function mark(v,b,ch){while(base[v]!==b){bl[base[v]]=bl[base[mt[v]]]=true;p[v]=ch;ch=mt[v];v=p[mt[v]]}}
 function find(root){p=Array(n).fill(-1);base=Array.from({length:n},(_,i)=>i);used=Array(n).fill(false);used[root]=true;let q=[root];
 for(let h=0;h<q.length;h++){let v=q[h];for(let u of g[v]){if(base[v]===base[u]||mt[v]===u)continue;
 if(u===root||(mt[u]>=0&&p[mt[u]]>=0)){stats.blossoms++;let b=lca(v,u);bl=Array(n).fill(false);mark(v,b,u);mark(u,b,v);for(let i=0;i<n;i++)if(bl[base[i]]){base[i]=b;if(!used[i]){used[i]=true;q.push(i)}}}
 else if(p[u]<0){p[u]=v;if(mt[u]<0)return u;u=mt[u];used[u]=true;q.push(u)}}}return -1}
 for(let i=0;i<n;i++)if(mt[i]<0){let v=find(i);while(v>=0){let pv=p[v],pp=pv<0?-1:mt[pv];mt[v]=pv;if(pv>=0)mt[pv]=v;v=pp}}
 return mt
}
function factor(F,fixed={},extra=[]){
 stats.regionalQueries++;let c=close(F,fixed);if(!c)return null;let {G,a}=c,occ=new Map(),bounds=G.map(r=>[r.l,r.u]),edges=[],decode=[];
 for(let i=0;i<G.length;i++)for(let j=0;j<G[i].v.length;j++){let x=G[i].v[j];if(!occ.has(x))occ.set(x,[]);occ.get(x).push([i,G[i].s[j]])}
 function edge(u,v){edges.push([u,v]);return edges.length-1}
 for(let [x,o] of occ){if(o.length>2)throw Error("invalid occurrence after certification");
 let [u,s]=o[0],e;
 if(o.length===1){let v=bounds.length;bounds.push([0,1]);e=edge(u,v)}
 else if(s===o[1][1])e=edge(u,o[1][0]);
 else{let v=bounds.length;bounds.push([1,1]);e=edge(u,v);edge(v,o[1][0])}
 decode.push([x,s,e])}
 let g=[],opts=[],slots=[];let node=()=>{g.push([]);return g.length-1};let add=(u,v)=>{g[u].push(v);g[v].push(u)};
 for(let [l,u] of bounds){let z=[];for(let j=0;j<u;j++){let t=node();z.push(t);if(j>=l)opts.push(t)}slots.push(z)}
 if(g.length%2)opts.push(node());
 for(let i=0;i<opts.length;i++)for(let j=0;j<i;j++)add(opts[i],opts[j]);
 let eNodes=[];for(let [u,v] of edges){let x=node(),y=node();eNodes.push([x,y]);add(x,y);for(let t of slots[u])add(x,t);for(let t of slots[v])add(y,t)}
 stats.matchingCalls++;stats.matchingVertices+=g.length;stats.matchingEdges+=g.reduce((z,x)=>z+x.length,0)/2;
 let mt=blossom(g);if(mt.some(x=>x<0))return null;
 for(let [x,s,e] of decode){let [u,v]=eNodes[e];a[x]=s^(mt[u]===v?0:1)}
 for(let x of [...extra,...F.flatMap(r=>r.v)])if(!(x in a))a[x]=0;
 chk(valid(F,a),"factor witness");return a
}
function encode(scope,table){
 let keys=[...table.keys()].sort();
 if(!keys.length)return [row([],1,0)];
 if(keys.length===2**scope.length)return [];
 if(scope.length===1||keys.length===1)return scope.map((v,i)=>row([v],+keys[0][i],+keys[0][i]));
 let [x,y]=scope;
 if(keys.length===2){if(keys[0][0]===keys[1][0])return [row([x],+keys[0][0],+keys[0][0])];if(keys[0][1]===keys[1][1])return [row([y],+keys[0][1],+keys[0][1])];return [row(scope,1,1,[0,keys[0][0]===keys[0][1]?1:0])]}
 let bad=["00","01","10","11"].find(k=>!table.has(k));return [row(scope,1,2,[+bad[0],+bad[1]])]
}
function cactus(F){
 let occ=new Map();F.forEach((r,i)=>r.v.forEach(x=>{if(!occ.has(x))occ.set(x,[]);occ.get(x).push(i)}));
 let hubs=[...occ].filter(([x,o])=>o.length>2).map(([x])=>x),H=new Set(hubs),pa=F.map((_,i)=>i);
 function root(i){while(pa[i]!==i){pa[i]=pa[pa[i]];i=pa[i]}return i}
 for(let [x,o] of occ)if(!H.has(x))for(let j=1;j<o.length;j++)pa[root(o[j])]=root(o[0]);
 let parts=new Map();F.forEach((r,i)=>{let k=root(i);if(!parts.has(k))parts.set(k,[]);parts.get(k).push(r)});
 let R=[...parts.values()],n=R.length+hubs.length,g=Array.from({length:n},()=>[]),ed=[],meta=R.map(rows=>({rows,attachments:[]}));
 for(let x of hubs)meta.push({hub:x,attachments:[]});
 for(let i=0;i<R.length;i++){let o=new Map();for(let r of R[i])for(let x of r.v)o.set(x,(o.get(x)||0)+1);
 if([...o.values()].some(k=>k>2)){stats.declines++;return undefined}
 for(let x of hubs)if(o.has(x)){let j=R.length+hubs.indexOf(x);let e=ed.length;ed.push([i,j]);g[i].push([j,e]);g[j].push([i,e])}
 meta[i].occ=o}
 let blocks=[],stack=[],tin=Array(n).fill(-1),low=[],clk=0;
 function dfs(v,pe){tin[v]=low[v]=clk++;for(let [u,e] of g[v]){if(e===pe)continue;if(tin[u]<0){stack.push(e);dfs(u,e);low[v]=Math.min(low[v],low[u]);if(low[u]>=tin[v]){let b=[],z;do{z=stack.pop();b.push(z)}while(z!==e);blocks.push(b)}}else if(tin[u]<tin[v]){stack.push(e);low[v]=Math.min(low[v],tin[u])}}}
 for(let i=0;i<n;i++)if(tin[i]<0)dfs(i,-1);
 let B=blocks.map(es=>{let adj=new Map();for(let e of es){let [v,u]=ed[e];if(!adj.has(v))adj.set(v,[]);if(!adj.has(u))adj.set(u,[]);adj.get(v).push(u);adj.get(u).push(v)}return adj});
 let inc=Array.from({length:n},()=>[]);
 for(let b=0;b<B.length;b++){let A=B[b];if(blocks[b].length>1){if([...A.values()].some(z=>z.length!==2)){stats.declines++;return undefined}
 for(let [v,us] of A)if(v<R.length&&us.some(u=>meta[v].occ.get(meta[u].hub)!==1)){stats.declines++;return undefined}}
 for(let v of A.keys())inc[v].push(b)}
 let visited=new Set();
 function ports(v,neighbors){return v>=R.length?[meta[v].hub]:neighbors.map(u=>meta[u].hub)}
 function key(scope,a){return scope.map(x=>a[x]).join("")}
 function attach(v,msg){let m=meta[v];m.attachments.push(msg);if(v<R.length){m.rows=m.rows.concat(encode(msg.scope,msg.table));if(!close(m.rows))return false}else if(![0,1].some(x=>m.attachments.every(t=>t.table.has(String(x)))))return false;return true}
 function query(v,fixed){let m=meta[v],a;
 if(v<R.length){a=factor(m.rows,fixed,m.attachments.flatMap(t=>t.scope));if(!a)return null}
 else {let x=m.hub;let val=(x in fixed)?fixed[x]:[0,1].find(y=>m.attachments.every(t=>t.table.has(String(y))));if(val===undefined)return null;a={[x]:val}}
 for(let t of m.attachments){let b=t.table.get(key(t.scope,a));if(!b)return null;a=merge(a,b);chk(a,"child witness conflict")}return a}
 function prep(v,parent){visited.add(v);for(let b of inc[v])if(b!==parent){let t=block(b,v);if(!attach(v,t))return false}return true}
 function block(b,p){stats.blocks++;let A=B[b],scope=ports(p,A.get(p)),table=new Map();
 let good=true;for(let v of A.keys())if(v!==p&&!prep(v,b))good=false;
 if(!good)return {scope,table};
 if(blocks[b].length===1){let v=A.get(p)[0];for(let x=0;x<2;x++){let a=query(v,{[scope[0]]:x});if(a)table.set(String(x),a)}return {scope,table}}
 stats.cycleBlocks++;let order=[],last=p,v=A.get(p)[0];while(v!==p){order.push(v);let u=A.get(v).find(x=>x!==last);last=v;v=u}
 let local=order.map((v,i)=>{let left=i?order[i-1]:p,right=i+1<order.length?order[i+1]:p;let S=ports(v,[left,right]),tab=new Map();
 for(let x=0;x<2;x++)for(let y=0;y<2;y++){if(S.length===1&&x!==y)continue;let fixed={[S[0]]:x};if(S.length===2)fixed[S[1]]=y;let a=query(v,fixed);if(a)tab.set(""+x+y,a)}return tab});
 for(let x=0;x<2;x++)for(let y=0;y<2;y++){if(scope.length===1&&x!==y)continue;let dp=new Map([[x,{}]]);
 for(let tab of local){let next=new Map();for(let [a,w] of dp)for(let z=0;z<2;z++){stats.blockTransitions++;let q=tab.get(""+a+z);if(q){let m=merge(w,q);chk(m,"cycle witness conflict");if(!next.has(z))next.set(z,m)}}dp=next}
 if(dp.has(y))table.set(scope.length===1?String(x):""+x+y,dp.get(y))}
 return {scope,table}}
 let ans={};for(let v=0;v<n;v++)if(!visited.has(v)){if(!prep(v,-1))return null;let a=query(v,{});if(!a)return null;ans=merge(ans,a);chk(ans,"component conflict")}return ans
}
function brute(F,vs,base={}){for(let i=0;i<2**vs.length;i++){let a={...base};vs.forEach((v,j)=>a[v]=(i>>j)&1);stats.countWords++;if(valid(F,a))return a}return null}
function solve(F,n,p={}){
 let c=close(F,p);if(!c)return null;let {G,a}=c;
 if(!G.length){for(let i=0;i<n;i++)if(!(i in a))a[i]=0;return a}
 let w=cactus(G);if(w!==undefined){if(!w)return null;let z=merge(a,w);chk(z,"root pin conflict");for(let i=0;i<n;i++)if(!(i in z))z[i]=0;chk(valid(F,z),"root witness");return z}
 let vs=[...new Set(G.flatMap(r=>r.v))];
 if(vs.length<=4){w=brute(G,vs,a);if(w)for(let i=0;i<n;i++)if(!(i in w))w[i]=0;return w}
 stats.branches++;let cnt=x=>G.reduce((z,r)=>z+Number(r.v.includes(x)),0);vs.sort((x,y)=>cnt(y)-cnt(x));let x=vs[0];
 for(let b of [0,1]){w=solve(F,n,{...a,[x]:b});if(w)return w}return null
}
function family(k,cap){let F=[row(Array.from({length:2*k},(_,i)=>i),0,cap)];
 for(let i=0;i<k;i++)F.push(row([2*i,2*i+1],1,2));
 for(let i=0;i<2*k;i++)F.push(row([i,2*k+i],0,1));return {F,n:4*k}}
function reference(F,n){let count=0;for(let i=0;i<2**n;i++){let a=Array.from({length:n},(_,j)=>(i>>j)&1);if(valid(F,a))count++}return count}
let results={binaryRelations:0,small:[],scaling:[],fano:[],random:{sat:0,unsat:0},hostile:[],stats};
for(let mask=0;mask<16;mask++){let t=new Map();for(let i=0;i<4;i++)if(mask>>i&1)t.set(i.toString(2).padStart(2,"0"),{});let F=encode([0,1],t);for(let i=0;i<4;i++){let s=i.toString(2).padStart(2,"0");chk(valid(F,[+s[0],+s[1]])===t.has(s),"binary table")}results.binaryRelations++}
for(let k=1;k<=4;k++)for(let cap of [Math.max(0,k-1),k]){let {F,n}=family(k,cap),z=solve(F,n),ref=reference(F,n);chk(Boolean(z)===Boolean(ref),"small");if(z)chk(valid(F,z),"small lift");results.small.push({k,cap,models:ref,sat:!!z})}
for(let k of [8,32,64])for(let cap of [k-1,k]){let {F,n}=family(k,cap),before={...stats},z=solve(F,n);chk(Boolean(z)===(cap===k),"scaling");if(z)chk(valid(F,z),"scale lift");results.scaling.push({k,cap,sat:!!z,matchingCalls:stats.matchingCalls-before.matchingCalls,branches:stats.branches-before.branches,cycleBlocks:stats.cycleBlocks-before.cycleBlocks})}
let fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(v=>row(v,1,2));
for(let i=-1;i<35;i++){let F=fano.map(r=>({...r,s:r.s.slice()}));if(i>=0&&i<14){let j=Math.floor(i/2);F[j]=row(F[j].v,i%2?1:0,i%2?3:2)}else if(i>=14){let j=Math.floor((i-14)/3);F[j].s[(i-14)%3]=1}let z=solve(F,7),ref=reference(F,7);chk(!!z===!!ref,"Fano");if(z)chk(valid(F,z),"Fano lift");results.fano.push({i,models:ref,sat:!!z})}
let seed=246813579;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
for(let t=0;t<100;t++){let n=6,F=[];for(let j=0;j<8;j++){let a=rnd(n),b=(a+1+rnd(n-1))%n,c=(b+1)%n;while(c===a||c===b)c=(c+1)%n;let lo=rnd(3),hi=lo+rnd(4-lo);F.push(row([a,b,c],lo,hi,[rnd(2),rnd(2),rnd(2)]))}let z=solve(F,n),ref=reference(F,n);chk(!!z===!!ref,"random");if(z)chk(valid(F,z),"random lift");results.random[z?"sat":"unsat"]++}
return results
}
console.log(JSON.stringify(runBS13(),null,2));
