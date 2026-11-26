function flowAudit(){
 const A=(x,m)=>{if(!x)throw Error(m)}, R=n=>Array.from({length:n},(_,i)=>i), masks=n=>R(2**n), w=x=>x.toString(2).replace(/0/g,"").length, stats={cases:0,positive:0,negative:0,flows:0,augmentations:0,branches:0,closure:0,relaxations:0,affineRows:0,maxRank:0,dependentObservations:0,probes:0}, results=[];
 let seed=91042;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*n)};
 function edges(F){let E=new Map();F.forEach((v,j)=>v.e.forEach((e,i)=>{if(!E.has(e))E.set(e,[]);E.get(e).push([j,i])}));return E}
 function fits(v,t,p){return v.e.every((e,i)=>p[e]===undefined||p[e]===((t>>i&1)^v.s[i]))}
 function check(F,p){return F.every(v=>v.e.every(e=>p[e]===0||p[e]===1)&&v.T.some(t=>fits(v,t,p)))}
 function classes(T,d){let k=w(T[0]),active=R(d).filter(i=>T.some(x=>x>>i&1));if(!T.every(x=>w(x)===k))return null;if(k!==2||d<=3)return active.map(i=>[i]);
 let C=[];for(let i of active){let j=C.findIndex(c=>!T.includes((1<<i)|(1<<c[0])));if(j<0)C.push([i]);else C[j].push(i)}
 return active.every(i=>active.every(j=>i===j||(C.findIndex(c=>c.includes(i))!==C.findIndex(c=>c.includes(j)))===T.includes((1<<i)|(1<<j))))?C:null}
 function flow(n,arcs,s,t){stats.flows++;let adj=R(n).map(()=>[]),refs=[];for(let [u,v,c] of arcs){let a={v,c,rev:adj[v].length},b={v:u,c:0,rev:adj[u].length};adj[u].push(a);adj[v].push(b);refs.push(a)}
 let f=0;for(;;){let p=R(n).map(()=>null),Q=[s];p[s]=[-1,-1];for(let h=0;h<Q.length&&!p[t];h++)for(let j=0;j<adj[Q[h]].length;j++){let a=adj[Q[h]][j];if(a.c>0&&!p[a.v]){p[a.v]=[Q[h],j];Q.push(a.v)}}if(!p[t])break;let z=Infinity;for(let v=t;v!==s;){let [u,j]=p[v];z=Math.min(z,adj[u][j].c);v=u}for(let v=t;v!==s;){let [u,j]=p[v],a=adj[u][j];a.c-=z;adj[v][a.rev].c+=z;v=u}f+=z;stats.augmentations++}return{f,refs}}
 function allocation(F,p,relax=false){let U=[...edges(F)].filter(([e])=>p[e]===undefined), G=F.map(v=>{let free=R(v.e.length).filter(i=>p[v.e[i]]===undefined),T=[...new Set(v.T.map(t=>free.reduce((a,i,j)=>a|((t>>i&1)<<j),0)))];let k=relax?Math.max(...T.map(w)):w(T[0]),C=relax?R(free.length).map(i=>[i]):classes(T,free.length);return{free,k,C}});
 if(G.some(g=>!g.C))return undefined;if(!relax&&G.reduce((a,g)=>a+g.k,0)!==U.length)return null;
 let s=0,t=1,n=2,arcs=[],V=G.map(()=>n++),C=G.map(g=>g.C.map(()=>n++)),refs=[];
 G.forEach((g,j)=>{arcs.push([V[j],t,g.k]);g.C.forEach((c,i)=>arcs.push([C[j][i],V[j],1]))});
 for(let [e,occ] of U){A(occ.length===2,"free edge endpoints");let a=n++;arcs.push([s,a,1]);for(let [j,i] of occ){let h=G[j].C.findIndex(c=>c.includes(G[j].free.indexOf(i)));if(h>=0){refs.push([e,j,i,arcs.length]);arcs.push([a,C[j][h],1])}}}
 let z=flow(n,arcs,s,t);if(z.f!==U.length)return null;if(relax)return true;let q={...p};for(let [e,j,i,a] of refs)if(z.refs[a].c===0)q[e]=1^F[j].s[i];A(check(F,q),"flow lift");return q}
 function close(F,p,probe=false){p={...p};for(;;){stats.closure++;let G=F.map(v=>({...v,T:v.T.filter(t=>fits(v,t,p))}));if(G.some(v=>!v.T.length))return null;let change=false;for(let v of G)for(let i=0;i<v.e.length;i++)if(p[v.e[i]]===undefined&&v.T.every(t=>(t>>i&1)===(v.T[0]>>i&1))){p[v.e[i]]=(v.T[0]>>i&1)^v.s[i];change=true}if(change){F=G;continue}stats.relaxations++;if(!allocation(G,p,true))return null;
 if(probe){for(let [e] of edges(G))if(p[e]===undefined){stats.probes+=2;let a=close(G,{...p,[e]:0}),b=close(G,{...p,[e]:1});if(!a&&!b)return null;if(!a||!b){p=(a||b).p;F=G;change=true;break}}if(change)continue}return{F:G,p}}}
 function solve(F,p,cap=12,probe=false){let c=close(F,p,probe);if(!c)return null;F=c.F;p=c.p;let ids=[...edges(F).keys()],idx=new Map(ids.map((e,i)=>[e,i])),B=e=>1n<<BigInt(idx.get(e)),rows=new Map();
 function reduce(m,b,S){while(m){let i=m.toString(2).length-1;if(!S.has(i))break;let r=S.get(i);m^=r[0];b^=r[1]}return[m,b]}
 function add(m,b,S){[m,b]=reduce(m,b,S);if(!m)return b===0;S.set(m.toString(2).length-1,[m,b]);return true}
 for(let [e,x] of Object.entries(p))if(idx.has(+e)&&!add(B(+e),x,rows))return null;
 let obs=[];for(let j=0;j<F.length;j++){let v=F[j],d=v.e.length;
 for(let m=1;m<2**d;m++){let b=w(m&v.T[0])%2;if(v.T.every(t=>w(m&t)%2===b)){let g=0n;for(let i=0;i<d;i++)if(m>>i&1){g^=B(v.e[i]);b^=v.s[i]}stats.affineRows++;if(!add(g,b,rows))return null}}
 let weights=new Set(v.T.map(w));if(weights.size>1){obs.push({j,g:v.e.reduce((a,e)=>a^B(e),0n),flip:v.s.reduce((a,b)=>a^b,0),type:0})}
 else{let free=R(d).filter(i=>p[v.e[i]]===undefined),T=[...new Set(v.T.map(t=>free.reduce((a,i,j)=>a|((t>>i&1)<<j),0)))];if(!classes(T,free.length)){let i=free[0];obs.push({j,g:B(v.e[i]),flip:v.s[i],type:1,i})}}}
 let ext=new Map(rows),basis=[];for(let o of obs){if(reduce(o.g,0,ext)[0]){basis.push(o.g);add(o.g,0,ext)}}
 stats.maxRank=Math.max(stats.maxRank,basis.length);stats.dependentObservations+=obs.length-basis.length;if(basis.length>cap)return undefined;
 for(let m of masks(basis.length)){stats.branches++;let S=new Map(rows);basis.forEach((g,i)=>A(add(g,m>>i&1,S),"independent guard"));let G=F.map(v=>({...v,T:v.T.slice()}));for(let o of obs){let [g,b]=reduce(o.g,0,S);A(!g,"rank spans");let v=G[o.j];v.T=v.T.filter(t=>(o.type?(t>>o.i&1):w(t)%2)===(b^o.flip))}
 let q=close(G,p);if(!q)continue;let z=allocation(q.F,q.p);A(z!==undefined,"guarded matroid");if(z){A(check(F,z),"rank flow source lift");return z}}
 return null}
 function brute(F,p){let ids=[...edges(F).keys()].filter(e=>p[e]===undefined);for(let m of masks(ids.length)){let q={...p};ids.forEach((e,i)=>q[e]=m>>i&1);if(check(F,q))return q}return null}
 function compare(F,p,label,expected){let z=solve(F,p,12,true);A(z!==undefined&&!!z===expected,"decision "+label);if(z)A(check(F,z)&&Object.entries(p).every(([e,x])=>z[e]===x),"guard lift");stats.cases++;if(z)stats.positive++;else stats.negative++;return !!z}
 for(let t=0;t<200;t++){let F=R(5).map(()=>({e:[],s:[],T:[]})),id=0;for(let i=0;i<5;i++)for(let j=i+1;j<5;j++){F[i].e.push(id);F[i].s.push(0);F[j].e.push(id++);F[j].s.push(1)}
 let x=R(id).map(()=>rnd(2));for(let v of F){let a=v.e.reduce((m,e,i)=>m|((x[e]^v.s[i])<<i),0),q=t<100?w(a)%3:rnd(3);v.T=masks(4).filter(m=>w(m)%3===q&&(t<100&&m===a||rnd(3)!==0));if(!v.T.length)v.T=[masks(4).find(m=>w(m)%3===q)]}let p={};if(t%3===0)p[rnd(id)]=rnd(2);compare(F,p,"abstract",!!brute(F,p))}
 function native(rot,kind){let map=new Map(),id=0;for(let i=0;i<rot.length;i++)for(let j of rot[i])if(i<j)map.set(i+","+j,id++);return rot.map((a,i)=>({e:a.map(j=>map.get(Math.min(i,j)+","+Math.max(i,j))),s:a.map(()=>kind(i)),T:kind(i)?[3,5,6]:[0,7]}))}
 function prism(n){let rot=R(2*n).map(v=>{let l=Math.floor(v/n),i=v%n;return[l*n+(i+n-1)%n,l*n+(i+1)%n,(1-l)*n+i]});return native(rot,v=>(Math.floor(v/n)+v%n)%2)}
 for(let n of [6,12,18,36,72]){let F=prism(n),b=stats.branches,z=compare(F,{},"native prism",true);results.push({n,answer:z,branches:stats.branches-b})}
 let neg=[[22,19,18],[13,16,21],[14,13,21],[18,13,14],[19,22,17],[16,19,23],[12,17,20],[12,20,15],[15,23,12],[16,14,21],[17,22,20],[23,15,18],[6,7,8],[3,1,2],[9,3,2],[7,11,8],[1,5,9],[4,10,6],[11,0,3],[5,0,4],[10,7,6],[2,1,9],[10,4,0],[8,11,5]];
 let F=native(neg,v=>v<12?0:1);compare(F,{},"native negative",false);results.push({n:12,answer:false});
 return{stats,results,seed:91042}
}
console.log(JSON.stringify(flowAudit(),null,2));
