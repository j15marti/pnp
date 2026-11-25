function audit(){
 const stats={scans:0,forces:0,nodes:0,failed:0,stagnations:0,queries:0,verified:0,normalizations:0,exchanges:0};
 const perms=[[0,1,2],[0,2,1],[1,0,2],[1,2,0],[2,0,1],[2,1,0]];
 const assert=(b,m)=>{if(!b)throw Error(m)};
 function canon(a){let d=new Map();return a.map(x=>{if(!d.has(x))d.set(x,d.size);return d.get(x)}).join("")}
 function pole(n,E,P=[]){let edges=E.map(e=>e.slice());P.forEach((v,i)=>edges.push([v,n+i]));let inc=Array.from({length:n},()=>[]);edges.forEach((e,i)=>e.forEach(v=>{if(v<n)inc[v].push(i)}));assert(inc.every(a=>a.length===3),"cubic internal");return {n,E:E.map(e=>e.slice()),P:P.slice(),edges,inc}}
 function verify(g,w){assert(w.length===g.edges.length&&w.every(x=>[0,1,2].includes(x))&&g.inc.every(a=>new Set(a.map(i=>w[i])).size===3),"invalid witness");stats.verified++}
 function state(g,w){return canon(w.slice(g.E.length))}
 function solve(g,pins={},all=false){stats.queries++;let out=new Map(),first=null;
  function dfs(d){stats.nodes++;let changed=true;while(changed){changed=false;for(let a of g.inc){stats.scans++;let supp=[0,0,0];for(let p of perms)if(p.every((c,j)=>d[a[j]]&(1<<c)))p.forEach((c,j)=>supp[j]|=1<<c);for(let j=0;j<3;j++){let i=a[j],v=d[i]&supp[j];if(!v){stats.failed++;return false}if(v!==d[i]){d[i]=v;stats.forces++;changed=true}}}}
   let i=-1,best=4;for(let j=0;j<d.length;j++){let k=[1,2,4].filter(v=>d[j]&v).length;if(k>1&&k<best){i=j;best=k}}
   if(i<0){let w=d.map(x=>Math.log2(x));verify(g,w);if(!first)first=w;out.set(state(g,w),w);return !all}
   stats.stagnations++;for(let b of [1,2,4])if(d[i]&b){let q=d.slice();q[i]=b;if(dfs(q)&&!all)return true}return false
  }let d=Array(g.edges.length).fill(7);for(let [i,c] of Object.entries(pins))d[Number(i)]=1<<c;dfs(d);return {first,out}
 }
 function table(g){let p={};if(g.P.length)p[g.E.length]=0;return solve(g,p,true).out}
 function balanced(s){return [0,1,2].every(x=>[...s].filter(c=>+c===x).length===2)}
 function normal(g,w){w=w.slice();verify(g,w);let steps=0;
  for(;;){let bc=[0,0,0];w.slice(g.E.length).forEach(c=>bc[c]++);let a=bc.indexOf(Math.max(...bc)),b=bc.indexOf(Math.min(...bc));if(bc[a]-bc[b]<=2)break;
   let adj=Array.from({length:g.n+g.P.length},()=>[]);g.edges.forEach(([u,v],i)=>{if(w[i]===a||w[i]===b){adj[u].push([v,i]);adj[v].push([u,i])}});
   let found=false;for(let i=0;i<g.P.length&&!found;i++){let s=g.n+i;if(w[g.E.length+i]!==a)continue;let u=s,prev=-1,path=[];for(;;){let e=adj[u].find(x=>x[1]!==prev);if(!e)break;[u,prev]=e;path.push(prev)}assert(u>=g.n&&u!==s,"path ends");if(w[g.E.length+u-g.n]===a){for(let e of path)w[e]=w[e]===a?b:a;found=true;steps++;stats.exchanges++;verify(g,w)}}
   assert(found,"same-color path exists");assert(steps<=2,"two exchanges for six ports");
  }assert(balanced(state(g,w)),"normal form");stats.normalizations++;return w
 }
 function fromLeft(L,k){let E=L.flatMap((a,i)=>a.map(j=>[i,L.length+j]));return pole(L.length+k,E,Array.from({length:6},(_,i)=>L.length+i))}
 let cap=fromLeft([[4,5,2],[6,1,3],[4,6,0],[6,2,1],[5,3,0]],7);
 let near=fromLeft([[0,1,2],[0,3,4],[1,3,5],[2,4,5]],6);
 let C=table(cap),D=table(near);assert(C.size===15&&[...C.keys()].every(balanced),"cap saturation");assert(D.size===14&&[...D.keys()].every(balanced),"near cap");
 let missing=[...C.keys()].find(s=>!D.has(s));assert(missing==="012210","missing opposite pairing");
 function pairs(s){let out=[];for(let a of new Set(s)){let x=[...s].map((b,i)=>b===a?i:-1).filter(i=>i>=0);assert(x.length===2,"pair");out.push(x)}return out}
 function equalPole(s){let E=[],P=Array(6);pairs(s).forEach(([a,b],j)=>{let t=4*j;for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)if(u!==0||v!==1)E.push([t+u,t+v]);P[a]=t;P[b]=t+1});return pole(12,E,P)}
 function join(a,b){assert(a.P.length===b.P.length,"port count");let E=[...a.E,...b.E.map(e=>e.map(v=>v+a.n)),...a.P.map((v,i)=>[v,a.n+b.P[i]])];return pole(a.n+b.n,E)}
 function lift(a,b,wa,wb){let x=wa.slice(a.E.length),y=wb.slice(b.E.length),p={};y.forEach((v,i)=>{if(v in p)assert(p[v]===x[i],"compatible");p[v]=x[i]});let w=[...wa.slice(0,a.E.length),...wb.slice(0,b.E.length).map(c=>p[c]),...x];verify(join(a,b),w);return w}
 let Y=equalPole(missing),YT=table(Y),neg=solve(join(near,Y)).first,pos=solve(join(cap,Y)).first;assert(!neg&&pos,"14 fails 15 succeeds");
 let X1=equalPole("001122"),X2=equalPole("012201"); // P pairs 01,23,45; Q pairs 04? check union below
 let a=table(X1),b=table(X2);let common=[...a.keys()].filter(s=>b.has(s));assert(common.includes("000000")&&!common.some(balanced),"global balanced obstruction");
 let z=solve(join(X1,X2)).first;assert(z,"global obstruction SAT");
 function graph(n,E){return pole(n,E)}
 function prism(k){let E=[];for(let i=0;i<k;i++)E.push([i,(i+1)%k],[i+k,(i+1)%k+k],[i,i+k]);return graph(2*k,E)}
 let K4=graph(4,Array.from({length:4},(_,i)=>Array.from({length:4-i-1},(_,j)=>[i,i+j+1])).flat());
 let K33=graph(6,Array.from({length:3},(_,i)=>[3,4,5].map(j=>[i,j])).flat());
 let P=graph(10,Array.from({length:5},(_,i)=>[[i,(i+1)%5],[i+5,5+(i+2)%5],[i,i+5]]).flat());
 let flower=(()=>{let E=[];for(let i=0;i<5;i++){let a=4*i;E.push([a,a+1],[a,a+2],[a,a+3],[a+1,4*((i+1)%5)+1]);if(i<4)E.push([a+2,a+6],[a+3,a+7]);else E.push([a+2,3],[a+3,2])}return graph(20,E)})();
 let named=[["K4",K4,true],["K33",K33,true],["prism3",prism(3),true],["cube",prism(4),true],["prism5",prism(5),true],["Petersen",P,false],["flowerJ5",flower,false]];
 let controls=[],poles=0,lifts=0,joinChecks=0,empty=0,types=0, maxSteps=0;
 for(let [name,g,expected] of named){assert(Boolean(solve(g).first)===expected,"named "+name);let count=0;
  for(let i=0;i<g.E.length;i++)for(let j=i+1;j<g.E.length;j++)for(let k=j+1;k<g.E.length;k++){if(name==="flowerJ5")continue;let sel=[i,j,k];let pp=sel.flatMap(x=>g.E[x]);if(new Set(pp).size!==6)continue;
   let q=pole(g.n,g.E.filter((_,l)=>!sel.includes(l)),pp),T=table(q);poles++;count++;types+=T.size;if(!T.size)empty++;
   for(let [s,w] of T){let before=stats.exchanges,wb=normal(q,w),t=state(q,wb);maxSteps=Math.max(maxSteps,stats.exchanges-before);assert(T.has(t)&&C.has(t),"normal actual table");lift(cap,q,C.get(t),wb);lifts++}
   let c=solve(join(cap,q)).first;assert(Boolean(c)===Boolean(T.size),"cap join equivalence");joinChecks++;
  }controls.push({name,expected,deletedTriples:count})
 }
 // A non-colorable outside pole: take intact Petersen plus three equality pieces.
 let U=pole(P.n+Y.n,[...P.E,...Y.E.map(e=>e.map(v=>v+P.n))],Y.P.map(v=>v+P.n));assert(!solve(join(cap,U)).first,"unsat outside preserved");
 // Complete actual cap-witness table, all port state labels canonicalized.
 let capWords={};for(let [s,w] of C){let map={};w.slice(cap.E.length).forEach((c,i)=>map[c]=+s[i]);let v=w.map(c=>map[c]);verify(cap,v);capWords[s]=v}
 return {stats,controls,poles,empty,types,lifts,joinChecks,maxSteps,cap:{n:cap.n,E:cap.E,P:cap.P,words:capWords},near:{n:near.n,E:near.E,P:near.P,states:[...D.keys()].sort(),missing},obstruction:{Y:{E:Y.E,P:Y.P},negativeVertices:near.n+Y.n,positiveVertices:cap.n+Y.n,global:{P:X1.P,Q:X2.P,common,word:z}}}
}
console.log(JSON.stringify(audit(),null,2));
