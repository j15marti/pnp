// Source inputs pinned to BS22 commit 0100a1421a264b657dc9b7f3a257dbd07dc06a44
const inputs = [{"n":7,"root":[{"t":[0,1,2],"bad":[0,7]},{"t":[0,3,4],"bad":[0,7]},{"t":[0,5,6],"bad":[0,7]},{"t":[1,3,5],"bad":[0,7]},{"t":[1,4,6],"bad":[0,7]},{"t":[2,3,6],"bad":[0,7]},{"t":[2,4,5],"bad":[0,7]}],"sat":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[0,7]},{"t":[0,5,6],"bad":[0,7]},{"t":[1,3,5],"bad":[0,7]},{"t":[1,4,6],"bad":[0,7]},{"t":[2,3,6],"bad":[0,7]},{"t":[2,4,5],"bad":[0,7]}],"guards":[]},{"n":15,"root":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[1,6]},{"t":[0,5,6],"bad":[3,4]},{"t":[0,7,8],"bad":[2,5]},{"t":[0,9,10],"bad":[3,4]},{"t":[0,11,12],"bad":[3,4]},{"t":[0,13,14],"bad":[1,6]},{"t":[1,3,5],"bad":[2,5]},{"t":[1,4,6],"bad":[3,4]},{"t":[1,7,9],"bad":[1,6]},{"t":[1,8,10],"bad":[3,4]},{"t":[1,11,13],"bad":[1,6]},{"t":[1,12,14],"bad":[2,5]},{"t":[2,3,6],"bad":[1,6]},{"t":[2,4,5],"bad":[2,5]},{"t":[2,7,10],"bad":[3,4]},{"t":[2,8,9],"bad":[2,5]},{"t":[2,11,14],"bad":[1,6]},{"t":[2,12,13],"bad":[1,6]},{"t":[3,7,11],"bad":[3,4]},{"t":[3,8,12],"bad":[3,4]},{"t":[3,9,13],"bad":[3,4]},{"t":[3,10,14],"bad":[3,4]},{"t":[4,7,12],"bad":[1,6]},{"t":[4,8,11],"bad":[2,5]},{"t":[4,9,14],"bad":[2,5]},{"t":[4,10,13],"bad":[1,6]},{"t":[5,7,13],"bad":[1,6]},{"t":[5,8,14],"bad":[3,4]},{"t":[5,9,11],"bad":[2,5]},{"t":[5,10,12],"bad":[2,5]},{"t":[6,7,14],"bad":[3,4]},{"t":[6,8,13],"bad":[2,5]},{"t":[6,9,12],"bad":[2,5]},{"t":[6,10,11],"bad":[0,7]}],"sat":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[1,6]},{"t":[0,5,6],"bad":[3,4]},{"t":[0,7,8],"bad":[2,5]},{"t":[0,9,10],"bad":[3,4]},{"t":[0,11,12],"bad":[3,4]},{"t":[0,13,14],"bad":[1,6]},{"t":[1,3,5],"bad":[2,5]},{"t":[1,4,6],"bad":[3,4]},{"t":[1,7,9],"bad":[1,6]},{"t":[1,8,10],"bad":[3,4]},{"t":[1,11,13],"bad":[1,6]},{"t":[1,12,14],"bad":[2,5]},{"t":[2,3,6],"bad":[1,6]},{"t":[2,4,5],"bad":[2,5]},{"t":[2,7,10],"bad":[3,4]},{"t":[2,8,9],"bad":[2,5]},{"t":[2,11,14],"bad":[1,6]},{"t":[2,12,13],"bad":[1,6]},{"t":[3,7,11],"bad":[3,4]},{"t":[3,8,12],"bad":[3,4]},{"t":[3,9,13],"bad":[3,4]},{"t":[3,10,14],"bad":[3,4]},{"t":[4,7,12],"bad":[1,6]},{"t":[4,8,11],"bad":[2,5]},{"t":[4,9,14],"bad":[2,5]},{"t":[4,10,13],"bad":[1,6]},{"t":[5,7,13],"bad":[1,6]},{"t":[5,8,14],"bad":[3,4]},{"t":[5,9,11],"bad":[2,5]},{"t":[5,10,12],"bad":[2,5]},{"t":[6,7,14],"bad":[3,4]},{"t":[6,8,13],"bad":[2,5]},{"t":[6,9,12],"bad":[2,5]},{"t":[6,10,11],"bad":[2,5]}],"guards":[[4,6,0],[6,8,0],[0,3,0],[1,2,0],[2,3,0],[3,5,1],[5,7,1]]}];
function run(inputs){
let checks=0,wordVisits=0,localScans=0,physicalLifts=0;const ck=b=>{checks++;if(!b)throw Error("assert "+checks)};
const bit=(x,i)=>(x>>i)&1;const relative=(a,b,c)=>(a^b)|((a^c)<<1);
const hole=o=>relative(bit(o.bad[0],0),bit(o.bad[0],1),bit(o.bad[0],2));
function build(n,O){
 const occ=Array.from({length:n},()=>[0,0,0]); for(const o of O)o.t.forEach((v,k)=>occ[v][k]++);
 let nv=0;const clouds=occ.map(a=>{let L=8*Math.max(1,...a),base=nv;nv+=3*L;return {L,base,used:[0,0,0]}});
 const V=(v,k,i)=>clouds[v].base+k*clouds[v].L+i;
 const edges=[];const owner=[];const col=[];for(let v=0;v<n;v++){let L=clouds[v].L;for(let k=0;k<3;k++)for(let i=0;i<L;i++){owner[V(v,k,i)]=v;col[V(v,k,i)]=k===0?1:0}for(let a=0;a<L;a++)for(let b=0;b<L;b++)edges.push({t:[V(v,0,a),V(v,1,b),V(v,2,(a+b)%L)],j:-1,h:0})}
 const internal=edges.length;
 O.forEach((o,j)=>{let starts=o.t.map((v,k)=>{let i=clouds[v].used[k];clouds[v].used[k]+=8;return i});for(let a=0;a<8;a++)edges.push({t:o.t.map((v,k)=>V(v,k,starts[k]+a)),j,h:hole(o)})});
 const pairs=new Set(),deg=Array(nv).fill(0),parent=Array.from({length:nv},(_,i)=>i),root=x=>{while(parent[x]!==x){parent[x]=parent[parent[x]];x=parent[x]}return x};
 for(const e of edges){let [a,b,c]=e.t;ck(new Set(e.t).size===3);ck(relative(col[a],col[b],col[c])!==0);for(let v of e.t)deg[v]++;for(let [i,j] of [[a,b],[a,c],[b,c]]){let k=Math.min(i,j)+","+Math.max(i,j);ck(!pairs.has(k));pairs.add(k);if(e.j<0)parent[root(i)]=root(j)}}
 const roots=new Set(parent.map((_,i)=>root(i)));ck(roots.size===n);for(let v=0;v<nv;v++)ck(root(v)===root(clouds[owner[v]].base));ck(edges.length-internal===8*O.length);
 // Check the analytic cloud cut certificate at every possible smaller-side size.
 for(let {L} of clouds)for(let s=1;s<=Math.floor(3*L/2);s++)ck(s*(2*L-s+1)>=2*L);
 return {edges,owner,nv,internal,maxDegree:Math.max(...deg),components:roots.size,clouds};
}
function close(n,O,G){let p=Array.from({length:n},(_,i)=>i),s=Array(n).fill(0);function find(x){if(p[x]===x)return [x,0];let [a,b]=find(p[x]);return [a,b^s[x]]}
 function add(a,b,c){let [u,x]=find(a),[v,y]=find(b);if(u===v)return (x^y)===c?0:-1;p[u]=v;s[u]=x^y^c;return 1}
 for(let [a,b,c] of G)if(add(a,b,c)<0)return "UNSAT";
 while(true){let changed=false;for(const o of O){localScans++;let map=o.t.map(find),R=[...new Set(map.map(a=>a[0]))],allowed=[];for(let w=0;w<2**R.length;w++){let z=map.map(([v,s])=>bit(w,R.indexOf(v))^s);if(relative(...z)!==hole(o))allowed.push(w)}if(!allowed.length)return "UNSAT";
 for(let i=0;i<R.length;i++)for(let j=i+1;j<R.length;j++){let q=bit(allowed[0],i)^bit(allowed[0],j);if(allowed.every(w=>(bit(w,i)^bit(w,j))===q)){let z=add(R[i],R[j],q);if(z<0)return "UNSAT";if(z>0)changed=true}}
 if(changed)break;}if(!changed)return "OPEN";}
}
let out=[];for(let z of inputs){for(let label of ["root","sat"]){let O=z[label],g=build(z.n,O);for(let G of [[],...(label==="root"&&z.guards.length?[z.guards.slice(0,1),z.guards]:[])]){let decision=close(z.n,O,G),count=0;for(let x=0;x<2**z.n;x++){wordVisits++;if(!G.every(([a,b,c])=>(bit(x,a)^bit(x,b))===c))continue;if(!O.every(o=>relative(...o.t.map(v=>bit(x,v)))!==hole(o)))continue;count++;for(let e of g.edges){let r=relative(...e.t.map(v=>bit(x,g.owner[v])));if(e.j<0)ck(r===0);else ck((r^e.h)!==0)}physicalLifts++}
 ck(decision!=="UNSAT"||count===0);out.push({n:z.n,label,guardSize:G.length,sourceModels:count,targetTuples:count/2,closure:decision,vertices:g.nv,owners:g.edges.length,group:g.edges.length-g.internal,components:g.components,maxDegree:g.maxDegree,zeroTarget:O.every(o=>hole(o)===0)})}}}
return {checks,wordVisits,localScans,physicalLifts,cases:out};
}
console.log(JSON.stringify(run(inputs),null,2));
