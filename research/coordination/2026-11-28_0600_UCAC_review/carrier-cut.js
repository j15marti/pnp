function carrierCuts(g){
 const cost={uf:0,pivots:0,xors:0,cuts:0};
 function uf(n){const p=Array.from({length:n},(_,i)=>i),sz=Array(n).fill(1);function root(i){while(i!==p[i]){i=p[i];cost.uf++}return i}function merge(i,j){i=root(i);j=root(j);if(i===j)return;if(sz[i]<sz[j])[i,j]=[j,i];p[j]=i;sz[i]+=sz[j]}return {root,merge}}
 const u=uf(4*g.types.length);for(const [a,b] of g.edges)u.merge(a,b);g.types.forEach((t,i)=>{if(t==="E")for(let j=1;j<4;j++)u.merge(4*i,4*i+j)});
 const ids=new Map(),owners=[],occ=[];g.types.forEach((t,i)=>{if(t==="B"){let a=[0,1,2,3].map(j=>{let v=u.root(4*i+j);if(!ids.has(v)){ids.set(v,ids.size);occ.push([])}return ids.get(v)});if(new Set(a).size!==4)throw Error("four distinct carrier promise");for(const v of a)occ[v].push(owners.length);owners.push(a)}});
 const m=owners.length,r=ids.size,idx=owners.map((_,i)=>i);
 function rank(rows){let B=new Map();for(let x of rows)while(x){let b=x&-x;cost.pivots++;if(!B.has(b)){B.set(b,x);break}x^=B.get(b);cost.xors++}return B.size}
 const A=owners.map(a=>a.reduce((s,i)=>s^(1n<<BigInt(i)),0n)),R=rank(A);
 function collapse(I){let v=uf(r);for(const i of I){let a=owners[i];for(let j=1;j<4;j++)v.merge(a[0],a[j])}let roots=Array.from({length:r},(_,i)=>v.root(i));let c=new Set(roots).size;let rows=owners.map(a=>a.reduce((s,i)=>s^(1n<<BigInt(roots[i])),0n));return {c,rank:rank(rows)}}
 const C=collapse(idx).c;
 function cut(P){cost.cuts++;let set=new Set(P),Q=idx.filter(i=>!set.has(i)),ip=0n,iq=0n,cross=0;occ.forEach((a,i)=>{if(a.every(j=>set.has(j)))ip|=1n<<BigInt(i);else if(a.every(j=>!set.has(j)))iq|=1n<<BigInt(i);else cross++});let raw=cross+rank(P.map(i=>A[i]&ip))+rank(Q.map(i=>A[i]&iq))-R;let p=collapse(P),q=collapse(Q),quot=r-p.c-q.c+p.rank+q.rank-R+C;return [raw,quot]}
 const adj=owners.map(()=>new Set());for(const a of occ){let u=a[0];for(const v of a)if(u!==v){adj[u].add(v);adj[v].add(u)}}let seen=new Set(),bfs=[];for(const i of idx)if(!seen.has(i)){let q=[i];seen.add(i);for(let j=0;j<q.length;j++){let u=q[j];bfs.push(u);for(const v of [...adj[u]].sort((a,b)=>a-b))if(!seen.has(v)){seen.add(v);q.push(v)}}}
 function tree(order){let raw=[],quot=[];function go(lo,hi){if(hi-lo<=1)return;let mid=(lo+hi)>>1;for(const [l,h] of [[lo,mid],[mid,hi]]){let [a,b]=cut(order.slice(l,h));raw.push(a);quot.push(b);if(h-l>1)go(l,h)}}go(0,order.length);const summary=a=>({max:Math.max(0,...a),sum:a.reduce((a,b)=>a+b,0)});return {raw:summary(raw),quot:summary(quot),cutLoss:raw.reduce((s,x,i)=>s+x-quot[i],0),decreased:raw.filter((x,i)=>x>quot[i]).length,increased:raw.filter((x,i)=>x<quot[i]).length}}
 return {owners:m,carriers:r,parityRank:R,components:C,rawRank:3*m-r+R,quotRank:2*m-r+R+C,source:tree(idx),incidence:tree(bfs),cost};
}
module.exports={carrierCuts};
