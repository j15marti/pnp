function audit(){
 const cap=65536; const out=[];
 const assert=(v,m)=>{if(!v)throw Error(m)};
 function perms(a){if(!a.length)return [[]];return a.flatMap((x,i)=>perms(a.filter((_,j)=>i!==j)).map(y=>[x,...y]));}
 function topo(adj,removed=[]){let n=adj.length, r=new Set(removed),deg=Array(n).fill(0);for(let u=0;u<n;u++)if(!r.has(u))for(let [v] of adj[u])if(!r.has(v))deg[v]++;let stack=[];for(let i=0;i<n;i++)if(!r.has(i)&&!deg[i])stack.push(i);let list=[];while(stack.length){let u=stack.pop();list.push(u);for(let [v] of adj[u])if(!r.has(v)&&!--deg[v])stack.push(v)}return list.length===n-r.size?list:null}
 function run(q,a,hostile=false){
 let L=2*a+3,d=2*a,k=L*q-d,t=q,paths=[],edges=[],base=[],U=Array(q).fill(L),V=Array(q).fill(0);
 let cheap=new Map();function pair(u,v,c){cheap.set(u*q+v,1);cheap.set(v*q+u,c-1)}
 pair(0,2,a);pair(1,2,a);pair(0,3,a+1);pair(1,4,hostile?a:a+1);for(let i=5;i<q;i++)pair(1,i,a+1);
 function path(u,v,l,local=false){let z=[u];for(let r=1;r<l;r++){z.push(t++);U.push(l-r);V.push(-(l-r));}z.push(v);paths.push({u,v,l,z,local});for(let i=0;i<l;i++){edges.push([z[i],z[i+1]]);if(local)base[z[i]]=z[i+1];}}
 for(let i=0;i<q;i++)path(i,i,L,true);
 for(let i=0;i<q;i++)for(let j=0;j<q;j++)if(i!==j)path(i,j,cheap.has(i*q+j)?L-cheap.get(i*q+j):2);
 for(let i=0;i<t;i++)if(base[i]===undefined)base[i]=i;
 assert(new Set(base).size===t,"base bijection");let inv=[];base.forEach((v,i)=>inv[v]=i);
 let W0=base.filter((v,i)=>v!==i).length;assert(W0===L*q&&U.reduce((x,y)=>x+y,0)+V.reduce((x,y)=>x+y,0)===W0,"dual");
 let adj=Array.from({length:t},()=>[]),pruned=0;for(let [u,v,w] of [...edges.map(([u,v])=>[u,v,1]),...Array.from({length:t},(_,i)=>[i,i,0])]){let s=U[u]+V[v]-w;assert(s>=0,"dual sign");if(base[u]===v){assert(s===0,"tight");continue}if(s<=d)adj[u].push([inv[v],s]);else pruned++}
 // A: independent reference at path level, after verified local reduction.
 let ref=new Set(),visits=0,limited=false;function rec(i,used,def){if(++visits>cap){limited=true;return}if(def>d)return;if(i===q){ref.add(def);return}for(let j=0;j<q;j++)if(!used.has(j)){let c=i===j?0:(cheap.has(i*q+j)?cheap.get(i*q+j):L-2);if(def+c<=d){used.add(j);rec(i+1,used,def+c);used.delete(j);if(limited)return}}}rec(0,new Set(),0);
 // B: independent enumeration of disjoint 2-cycles, since cheap undirected graph is a tree.
 let pairs=[];for(let i=0;i<q;i++)for(let j=i+1;j<q;j++)if(cheap.has(i*q+j))pairs.push([i,j,cheap.get(i*q+j)+cheap.get(j*q+i)]);
 let tree=new Set(),treeVisits=0;function tr(i,used,s){if(++treeVisits>cap)return;if(s>d)return;if(i===pairs.length){tree.add(s);return}tr(i+1,used,s);let [u,v,c]=pairs[i];if(!used.has(u)&&!used.has(v)){used.add(u);used.add(v);tr(i+1,used,s+c);used.delete(u);used.delete(v)}}tr(0,new Set(),0);
 // C: full contracted assignment, find <=2 FVS by independent recognition.
 let single=null,H=null,recognition=0;for(let i=0;i<t;i++){recognition++;if(topo(adj,[i])){single=i;break}}if(single!==null)H=[single];else outer:for(let i=0;i<t;i++)for(let j=i+1;j<t;j++){recognition++;if(topo(adj,[i,j])){H=[i,j];break outer}}
 assert(H&&H.length===2,"two hubs necessary");
 // Integrated: split active hubs into private sources/sinks; earliest token movement.
 let support=new Set([0]),states=0,trans=0,unknown=false;
 for(let mask=1;mask<1<<H.length;mask++){
 let S=H.filter((_,i)=>mask>>i&1),r=S.length, src=new Map(S.map((v,i)=>[v,t+i])),sink=new Map(S.map((v,i)=>[v,t+r+i])),hs=new Set(H);
 let g=Array.from({length:t+2*r},()=>[]);for(let u=0;u<t;u++)if(!hs.has(u)||src.has(u))for(let [v,c] of adj[u])if(!hs.has(v)||sink.has(v))g[src.get(u)??u].push([sink.get(v)??v,c]);
 let ord=topo(g);assert(ord,"split DAG"); // force all sources first and sinks last
 ord=[...S.map(v=>src.get(v)),...ord.filter(v=>v<t),...S.map(v=>sink.get(v))];let rank=[];ord.forEach((v,i)=>rank[v]=i);
 for(let perm of perms(S.map(v=>sink.get(v)))){
 let memo=new Set();function go(pos,c){if(unknown)return;let key=pos.join(",")+":"+c;if(memo.has(key))return;memo.add(key);if(++states>cap){unknown=true;return}let i=-1;for(let j=0;j<r;j++)if(pos[j]!==perm[j]&&(i===-1||rank[pos[j]]<rank[pos[i]]))i=j;if(i===-1){support.add(c);return}for(let [v,w] of g[pos[i]]){trans++;if(trans>cap){unknown=true;return}if(c+w>d||pos.includes(v)||(v>=t+r&&v!==perm[i]))continue;let p=pos.slice();p[i]=v;go(p,c+w)}}go(S.map(v=>src.get(v)),0);
 }}
 let sorted=s=>[...s].sort((x,y)=>x-y);assert(!limited&&!unknown&&treeVisits<=cap,"cap");assert(JSON.stringify(sorted(ref))===JSON.stringify(sorted(tree))&&JSON.stringify(sorted(ref))===JSON.stringify(sorted(support)),"support mismatch");
 assert(support.has(d)===hostile,"target");let E=t*(1+k*k)+k*edges.length,O=3*(t+k),n=64*E-20*O+5,m=78*E-24*O+5,N=n+2+2*Math.floor(Math.log2(m+1))+3*m*Math.ceil(Math.log2(n+1));
 // Raw GAC certificate: ordinary labels on heavy private paths are inactive, all other owners still have >=2 possibilities.
 let forced=paths.filter(p=>!p.local&&!cheap.has(p.u*q+p.v)).flatMap(p=>p.z.slice(1,-1));let removedArcs=paths.filter(p=>!p.local&&!cheap.has(p.u*q+p.v)).reduce((s,p)=>s+p.l,0);
 let remain=paths.filter(p=>p.local||cheap.has(p.u*q+p.v)),inD=Array(t).fill(0),outD=Array(t).fill(0);for(let p of remain)for(let i=0;i<p.l;i++){outD[p.z[i]]++;inD[p.z[i+1]]++}let F=new Set(forced);for(let i=0;i<t;i++)assert(F.has(i)?!inD[i]&&!outD[i]:inD[i]>0&&outD[i]>0,"closure degree");assert(t-forced.length>=k,"hub capacity");
 return {q,a,L,d,k,t,arcs:edges.length,E,O,n,m,N,hostile,pruned,forcedLoops:forced.length,removedRaw:forced.length*k*k+removedArcs*k,ref:sorted(ref),visits,treeVisits,H,recognition,states,trans};
 }
 for(let q=5;q<=8;q++)out.push(run(q,q-3));out.push(run(5,2,true));
 const C=(x,y,z)=>new Set([x,y,z]).size===3&&[0,1,2,3,4].some(i=>[i,(i+1)%5,(i+2)%5].every(j=>[x,y,z].includes(j)));
 const beat=(x,y)=>[1,3].includes((y-x+5)%5),R=(x,y,z)=>new Set([x,y,z]).size===3&&beat(x,y)!==beat(x,z);
 let rowsC=0,rowsR=0;for(let x=0;x<5;x++)for(let y=0;y<5;y++)for(let z=0;z<5;z++){rowsC+=+C(x,y,z);rowsR+=+R(x,y,z);assert(C(x,y,z)===(R(x,y,z)&&R(y,x,z)),"relations")}
 return {cap,rowsC,rowsR,cases:out};
}
console.log(JSON.stringify(audit(),null,2));
