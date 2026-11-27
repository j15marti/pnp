function run(){
 const assert=(b,m)=>{if(!b)throw Error(m)};
 const C=(a,b,c)=>new Set([a,b,c]).size===3&&[0,1,2,3,4].some(i=>[a,b,c].every(x=>[i,(i+1)%5,(i+2)%5].includes(x)));
 const R=(a,b,c)=>new Set([a,b,c]).size===3&&([1,3].includes((b-a+5)%5)!==[1,3].includes((c-a+5)%5));
 let relation=0,frames=0,domains=0,ors=0;
 for(let a=0;a<5;a++)for(let b=0;b<5;b++)for(let c=0;c<5;c++){assert(C(a,b,c)===(R(a,b,c)&&R(b,a,c)),"C R");relation++}
 for(let f=0;f<3125;f++){let v=Array.from({length:5},(_,i)=>Math.floor(f/5**i)%5);if(v.every((x,i)=>C(x,v[(i+1)%5],v[(i+2)%5]))) {assert(new Set(v).size===5,"frame");frames++}}
 for(let p=0;p<5;p++){let d=[2,3,4].every(j=>[0,1,2,3,4].some(u=>C(j,p,u)));assert(d===(p<2),"wire");domains++}
 for(let p=0;p<2;p++)for(let q=0;q<2;q++)for(let z=0;z<2;z++){let ok=false;for(let u=0;u<5;u++)for(let v=0;v<5;v++)if(C(1,2,u)&&C(0,1,v)&&C(4,p,u)&&C(3,q,v)&&C(z,u,v))ok=true;assert(ok===(z===(p|q)),"or");ors++}
 for(let p=0;p<2;p++)for(let z=0;z<2;z++)assert(C(2,p,z)===(z===1-p),"not");
 function graph(q,a,hostile=false){let L=2*a+3,d=2*a,k=L*q-d,t=q,A=[],P=[],M=[],U=Array(q).fill(L),V=Array(q).fill(0);
 function path(i,j,l,base=false){let vs=[i];for(let r=1;r<l;r++){vs.push(t++);U.push(l-r);V.push(-(l-r))}vs.push(j);let ids=[];for(let r=0;r<l;r++){ids.push(A.length);A.push([vs[r],vs[r+1]])}P.push({i,j,l,ids,vs,base});return P.length-1}
 let base=Array.from({length:q},(_,i)=>path(i,i,L,true));
 for(let i=1;i<q;i++){path(0,i,L-1);path(i,0,L-(i===1?a-1:a))}
 for(let i=1;i<q;i++)for(let j=1;j<q;j++)if(i!==j)path(i,j,2);
 if(hostile)path(2,2,L-a);
 M=Array.from({length:t},(_,i)=>i);for(let p of P.filter(p=>p.base))for(let id of p.ids){let [i,j]=A[id];M[i]=j}
 assert(new Set(M).size===t,"M");let inv=[];M.forEach((j,i)=>inv[j]=i);
 let edges=A.map(([i,j],id)=>({i,j,w:1,id})).concat(Array.from({length:t},(_,i)=>({i,j:i,w:0,id:A.length+i})));
 let tight=0,dual=U.reduce((x,y)=>x+y,0)+V.reduce((x,y)=>x+y,0);
 for(let e of edges){e.s=U[e.i]+V[e.j]-e.w;e.to=inv[e.j];assert(e.s>=0,"dual");if(M[e.i]===e.j){assert(!e.s,"tight");tight++}}
 assert(dual===q*L&&tight===t,"optimum");return{q,a,L,d,k,t,A,P,M,U,V,edges}
 }
 function topo(n,arcs,removed){let deg=Array(n).fill(0),adj=Array.from({length:n},()=>[]),cnt=0;for(let [i,j,w] of arcs)if(i!==removed&&j!==removed){adj[i].push([j,w]);deg[j]++}let Q=[];for(let i=0;i<n;i++)if(i!==removed&&!deg[i])Q.push(i);for(let p=0;p<Q.length;p++)for(let [j] of adj[Q[p]])if(--deg[j]===0)Q.push(j);return Q.length===n-(removed>=0?1:0)?{order:Q,adj}:null}
 function hybrid(F){let ar=F.edges.filter(e=>e.i!==e.to&&e.s<=F.d).map(e=>[e.i,e.to,e.s]);let z=topo(F.t,ar,0);if(!z)return {status:"UNKNOWN",retained:ar.length};let D=Array.from({length:F.t},()=>new Set()),checks=0;for(let [i,j,s] of ar)if(i===0)D[j].add(s);for(let i of z.order)for(let x of D[i])for(let [j,s] of z.adj[i]){checks++;if(x+s<=F.d)D[j].add(x+s)}let S=new Set([0]);for(let [i,j,s] of ar)if(j===0)for(let x of D[i]){checks++;if(x+s<=F.d)S.add(x+s)}return{status:S.has(F.d)?"YES":"NO",support:[...S].sort((x,y)=>x-y),checks,retained:ar.length,pruned:F.edges.length-F.t-ar.length}}
 function enumerate(F,cap){let out=Array.from({length:F.q},()=>[]);F.P.forEach((p,id)=>out[p.i].push(id));let visits=0,stop=false,S=new Set(),chosen=[],witness=null,used=new Set();function go(i,s){if(i===F.q){S.add(F.L*F.q-s);if(s===F.k)witness=chosen.slice();return}for(let id of [-1,...out[i]]){if(visits===cap){stop=true;return}visits++;let j=id===-1?i:F.P[id].j;if(used.has(j))continue;used.add(j);chosen.push(id);go(i+1,s+(id===-1?0:F.P[id].l));chosen.pop();used.delete(j);if(stop)return}}go(0,0);return{status:stop?"UNKNOWN":S.has(F.d)?"YES":"NO",visits,within:[...S].filter(x=>x<=F.d).sort((x,y)=>x-y),witness}}
 function raw(F){let h=F.t+F.k,E=[],O=Array.from({length:3*h},()=>[]),hash=2166136261;
 function add(x,y,z){let id=E.length;E.push([x,y,z]);for(let [a,v] of [[0,x],[1,y],[2,z]]){O[a*h+v].push(id);hash=Math.imul(hash^v,16777619)>>>0}}
 for(let i=0;i<F.t;i++){add(i,i,i);for(let a=0;a<F.k;a++)for(let b=0;b<F.k;b++)add(i,F.t+a,F.t+b)}
 for(let [i,j] of F.A)for(let c=0;c<F.k;c++)add(F.t+c,i,j);
 assert(O.every(r=>r.length>=2),"raw closure");return{h,E,O,hash:hash.toString(16)}}
 function proj(G,a,b){let adj=Array.from({length:G.h},()=>new Set());for(let e of G.E)adj[e[a]].add(e[b]);let H=Array(G.h).fill(-1),scans=0;function dfs(i,S){for(let j of adj[i]){scans++;if(S.has(j))continue;S.add(j);if(H[j]===-1||dfs(H[j],S)){H[j]=i;return true}}return false}for(let i=0;i<G.h;i++)if(!dfs(i,new Set()))return{ok:false,scans};return{ok:true,scans}}
 function lift(F,G,paths){let arcs=[];for(let p of paths)if(p>=0)arcs.push(...F.P[p].ids);let active=new Set(arcs.map(id=>F.A[id][0]));assert(active.size===F.k&&arcs.length===F.k,"pack");let inSet=new Set(arcs.map(id=>F.A[id][1]));assert(inSet.size===active.size&&[...active].every(i=>inSet.has(i)),"cycle");let M=new Map();G.E.forEach((e,id)=>M.set(e.join(","),id));let sol=[];let labels=[...active];for(let i=0;i<F.t;i++)if(!active.has(i))sol.push(M.get([i,i,i].join(",")));for(let [j,i] of labels.entries())sol.push(M.get([i,F.t+j,F.t+j].join(",")));for(let [j,id] of arcs.entries()){let [u,v]=F.A[id];sol.push(M.get([F.t+j,u,v].join(",")))}assert(sol.every(Number.isInteger),"IDs");let S=new Set(sol);assert(G.O.every(o=>o.filter(id=>S.has(id)).length===1),"cover");return sol.length}
 // Independent guard closure on raw exact-one source, after batch of certified deletions of any packing arc with cost >d or junction skip.
 function close(G,pins){let D=new Uint8Array(G.E.length).fill(3),Q=[],inq=new Uint8Array(G.O.length).fill(1),head=0,scans=0;for(let i=0;i<G.O.length;i++)Q.push(i);for(let id of pins)D[id]=1;while(head<Q.length){let i=Q[head++];inq[i]=0;let o=G.O[i],ones=0,can=0,last=-1;for(let j of o){scans++;if(D[j]===2)ones++;if(D[j]&2){can++;last=j}}if(!can||ones>1)return{no:true,scans};for(let j of o){let x=D[j];if(ones&&x===3)D[j]=1;else if(can===1&&j===last)D[j]=2;if(D[j]!==x)for(let a=0;a<3;a++){let r=a*G.h+G.E[j][a];if(!inq[r]){inq[r]=1;Q.push(r)}}}}return{no:false,scans,free:D.reduce((s,x)=>s+(x===3),0)}}
 let rows=[];
 for(let [q,a] of [[3,2],[4,3],[5,4],[6,5]]){let F=graph(q,a),G=raw(F),A=enumerate(F,65536),B=hybrid(F);assert(B.status==="NO"&&B.support.join(",")===[0,a,a+1].join(","),"hybrid");assert(A.status==="UNKNOWN"||A.status==="NO"&&A.within.join(",")===B.support.join(","),"reference");let Cc=close(G,[]);assert(!Cc.no&&Cc.free===G.E.length,"GAC");let heavy=new Set(F.P.filter(p=>F.L-p.l>F.d).flatMap(p=>p.ids)),pins=[];for(let id of heavy)for(let c=0;c<F.k;c++)pins.push(F.t*(1+F.k*F.k)+id*F.k+c);
 let re=close(G,pins);assert(!re.no,"pruned raw closure");
 let P=[[0,1],[0,2],[1,2]].map(([i,j])=>proj(G,i,j));assert(P.every(x=>x.ok),"projection");let E=G.E.length,O=G.O.length,n=64*E-20*O+5,m=78*E-24*O+5,N=n+1+2*Math.floor(Math.log2(m+1))+1+3*m*Math.ceil(Math.log2(n+1));
 // Separate algebraic lane: each admissible open cycle must use center; sums of two cheap cycles overlap. Verify path costs independently.
 let cheap=F.P.filter(p=>!p.base&&F.L-p.l<=F.d);assert(cheap.every(p=>p.i===0||p.j===0),"star");let costs=[];for(let i=1;i<q;i++){let x=cheap.find(p=>p.i===0&&p.j===i),y=cheap.find(p=>p.i===i&&p.j===0);assert(x&&y,"return");costs.push(2*F.L-x.l-y.l)}assert(costs[0]===a&&costs.slice(1).every(x=>x===a+1)&&2*a===F.d,"gap");
 rows.push({q,a,t:F.t,k:F.k,E,O,n,m,N,hash:G.hash,initial:Cc,imported:pins.length,reclosure:re,A:{status:A.status,visits:A.visits,within:A.within},B,algebra:{costs,naiveSumAttains:true},P})
 }
 let F=graph(3,2,true),G=raw(F),A=enumerate(F,65536),B=hybrid(F);assert(A.status==="YES"&&B.status==="UNKNOWN","hostile");let count=lift(F,G,A.witness);return{relation,frames,domains,ors,rows,hostile:{status:A.status,hybrid:B.status,witnessTriples:count}}
}
console.log(JSON.stringify(run(),null,2));
