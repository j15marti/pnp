function audit(){
  const C=(a,b)=>a.some((x,i)=>x===b[i]), key=t=>t.join(",");
  function groups(T,n){return Array.from({length:3*n},(_,i)=>T.map((t,j)=>t[Math.floor(i/n)]===i%n?j:-1).filter(j=>j>=0))}
  function project(T,n,c,d,yes=[],no=[]){
    const A=new Set(),B=new Set(),N=new Set(no);
    for(const i of yes){if(N.has(i)||A.has(T[i][c])||B.has(T[i][d]))return false;A.add(T[i][c]);B.add(T[i][d])}
    const adj=Array.from({length:n},()=>[]);
    T.forEach((t,i)=>{if(!N.has(i)&&!A.has(t[c])&&!B.has(t[d]))adj[t[c]].push(t[d])});
    const match=Array(n).fill(-1);
    function dfs(a,seen){for(const b of adj[a])if(!seen.has(b)){seen.add(b);if(match[b]<0||dfs(match[b],seen)){match[b]=a;return true}}return false}
    for(let a=0;a<n;a++)if(!A.has(a)&&!dfs(a,new Set()))return false;
    return true;
  }
  const pairs=[[0,1],[0,2],[1,2]], proj=(T,n,yes=[],no=[])=>pairs.every(([a,b])=>project(T,n,a,b,yes,no));
  function closure(T,n){
    T=T.slice();
    while(true){
      const G=groups(T,n);if(G.some(g=>!g.length)||!proj(T,n))return null;
      const forced=G.filter(g=>g.length===1).map(g=>g[0]);
      const dead=new Set();
      for(let i=0;i<T.length;i++){
        if(forced.some(j=>i!==j&&C(T[i],T[j]))||!proj(T,n,[i]))dead.add(i)
      }
      if(!dead.size)return T;
      T=T.filter((_,i)=>!dead.has(i));
    }
  }
  function sat2(m,F,units=[]){
    const E=Array.from({length:2*m},()=>[]), R=Array.from({length:2*m},()=>[]);
    const lit=x=>2*(Math.abs(x)-1)+(x<0?1:0);
    const add=(a,b)=>{E[a].push(b);R[b].push(a)};
    for(const [a,b] of F.concat(units.map(x=>[x,x]))){let x=lit(a),y=lit(b);add(x^1,y);add(y^1,x)}
    const vis=new Set(),ord=[];function dfs(v){vis.add(v);for(const u of E[v])if(!vis.has(u))dfs(u);ord.push(v)}
    for(let v=0;v<2*m;v++)if(!vis.has(v))dfs(v);
    const comp=Array(2*m).fill(-1);function dfs2(v,k){comp[v]=k;for(const u of R[v])if(comp[u]<0)dfs2(u,k)}
    let k=0;for(const v of ord.reverse())if(comp[v]<0)dfs2(v,k++);
    for(let i=0;i<m;i++)if(comp[2*i]===comp[2*i+1])return null;
    const model=Array.from({length:m},(_,i)=>comp[2*i]>comp[2*i+1]);
    if(!F.concat(units.map(x=>[x,x])).every(c=>c.some(x=>model[Math.abs(x)-1]===(x>0))))throw Error("bad 2sat witness");
    return model;
  }
  function formula(T,n,enhance=true){
    const F=[];for(const g of groups(T,n)){if(g.length<=2){if(!g.length)throw Error("empty group");F.push([g[0]+1,g[g.length-1]+1])}for(let i=0;i<g.length;i++)for(let j=i+1;j<g.length;j++)F.push([-g[i]-1,-g[j]-1])}
    if(enhance)for(let i=0;i<T.length;i++)for(let j=i+1;j<T.length;j++)for(const a of [false,true])for(const b of [false,true]){
      let yes=[],no=[];(a?yes:no).push(i);(b?yes:no).push(j);
      if(!proj(T,n,yes,no))F.push([a?-i-1:i+1,b?-j-1:j+1])
    }return F
  }
  function makeGraph(T,n,F,anchor){
    let G=groups(T,n),A=anchor.filter(a=>sat2(T.length,F,G[a].map(i=>-i-1))!==null);
    const V=T.map((_,i)=>i).filter(i=>A.some(a=>G[a].includes(i))&&sat2(T.length,F,[i+1])!==null);
    const w=V.map(i=>A.filter(a=>G[a].includes(i)).length),E=V.map(()=>new Set());
    for(let i=0;i<V.length;i++)for(let j=i+1;j<V.length;j++)if(sat2(T.length,F,[V[i]+1,V[j]+1])===null){E[i].add(j);E[j].add(i)}
    return {A,V,w,E}
  }
  function bruteIS(g){let best=-1,choice=[];function rec(i,S,W){if(i===g.V.length){if(W>best){best=W;choice=S.slice()}return}rec(i+1,S,W);if(S.every(j=>!g.E[i].has(j)))rec(i+1,S.concat(i),W+g.w[i])}rec(0,[],0);return {best,chosen:choice.map(j=>g.V[j])}}
  function exact(T,n){const sols=[];function rec(i,chosen,B,D){if(i===n){sols.push(chosen);return}for(let j=0;j<T.length;j++){let t=T[j];if(t[0]===i&&!B.has(t[1])&&!D.has(t[2]))rec(i+1,chosen.concat(j),new Set([...B,t[1]]),new Set([...D,t[2]]))}}rec(0,[],new Set(),new Set());return sols}
  function valid(T,n,ids){return ids.length===n&&[0,1,2].every(c=>new Set(ids.map(i=>T[i][c])).size===n)}
  function cube(){return Array.from({length:8},(_,i)=>[(i>>2)&1,(i>>1)&1,i&1])}
  function glue(T,f,k){let out=T.filter(t=>key(t)!==key(f));for(let b=1;b<8;b++)out.push(f.map((v,c)=>b&(1<<c)?k:v));return out.sort((a,b)=>key(a).localeCompare(key(b)))}
  const core=glue(cube(),[0,1,0],2);
  const W=[[[0,0,0],[1,1,1],[2,2,2]],[[0,0,1],[1,1,0],[2,2,2]],[[0,1,2],[1,0,1],[2,2,0]],[[0,2,0],[1,0,1],[2,1,2]]];
  let results={small:{instances:0,sat:0,unsat:0,closureNO:0,baseNO:0,graphCalls:0,zeroVertex:0,sourceVertices:0,compiledVertices:0,strictCompression:0},fixtures:[],scalable:[]};
  function test(T,n,label){
    let s=exact(T,n).length>0;let r=results.small;r.instances++;r[s?"sat":"unsat"]++;
    let L=closure(T,n);if(!L){if(s)throw Error("closure false no");r.closureNO++;return {label,source:s,closure:"NO"}}
    let F=formula(L,n);if(!sat2(L.length,F)){if(s)throw Error("2sat false no");r.baseNO++;return {label,source:s,base:"NO",live:L.length}}
    let sizes=[],targets=[],maxima=[];
    for(const a of [0,1,2,3]){
      const anchor=Array.from({length:a===3?3*n:n},(_,i)=>a===3?i:a*n+i),g=makeGraph(L,n,F,anchor),opt=bruteIS(g);
      const yes=opt.best===g.A.length;
      if(yes!==s)throw Error("graph equivalence");
      if(yes){const model=sat2(L.length,F,opt.chosen.map(i=>i+1));if(!model||!valid(L,n,model.map((v,i)=>v?i:-1).filter(i=>i>=0)))throw Error("bad source lift")}
      r.graphCalls++;r.zeroVertex+=g.V.length===0?1:0;r.sourceVertices+=L.length;r.compiledVertices+=g.V.length;r.strictCompression+=g.V.length<L.length?1:0;sizes.push(g.V.length);targets.push(g.A.length);maxima.push(opt.best)
    }return {label,source:s,live:L.length,sizes,targets,maxima}
  }
  for(let mask=0;mask<256;mask++)test(cube().filter((_,i)=>mask&(1<<i)),2,"cube-"+mask);
  let seed=0x13579bdf;function random(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed/4294967296}
  for(let i=0;i<120;i++)test(core.filter(()=>random()<0.72),3,"core-subset-"+i);
  const U=["000","002","010","011","021","022","100","101","111","201","202","221"].map(s=>s.split("").map(Number));
  results.fixtures.push(test(U,3,"AGE03 UNSAT"),test(U.concat([[1,1,0]]),3,"AGE03 SAT neighbor"),test(core,3,"claw core"));
  // For every old element, three distinct source-supported incident triples survive.
  // These prove that no sound 2-CNF can imply coverage of that element.
  let T=core,Ws=W.map(s=>s.slice());
  for(let n=3;n<=128;n++){
    if([3,4,8,16,32,64,128].includes(n)){
      const idx=new Map(T.map((t,i)=>[key(t),i]));
      for(const w of Ws){let ids=w.map(t=>idx.get(key(t)));if(ids.some(i=>i===undefined)||!valid(T,n,ids))throw Error("bad scalable witness")}
      let min=Infinity;for(let c=0;c<3;c++)for(let v=0;v<3;v++)min=Math.min(min,new Set(Ws.flat().filter(t=>t[c]===v).map(key)).size);
      if(min<3)throw Error("not 3 supported");
      let center=[0,1,2],leaves=[[0,0,0],[1,1,1],[2,2,2]];
      if(!leaves.every(t=>C(center,t))||leaves.some((a,i)=>leaves.some((b,j)=>i!==j&&C(a,b))))throw Error("bad claw");
      // Verify triangulation's local sphere certificates. Edges shared by 2 faces, Euler 2, each vertex link a connected cycle.
      const ed=new Map(),links=new Map();
      for(const t of T){let vs=t.map((v,c)=>c+":"+v);for(let c=0;c<3;c++){let u=vs[(c+1)%3],v=vs[(c+2)%3],e=[u,v].sort().join("|");ed.set(e,(ed.get(e)||0)+1);if(!links.has(vs[c]))links.set(vs[c],new Map());let L=links.get(vs[c]);if(!L.has(u))L.set(u,new Set());if(!L.has(v))L.set(v,new Set());L.get(u).add(v);L.get(v).add(u)}}
      if([...ed.values()].some(x=>x!==2)||links.size-ed.size+T.length!==2)throw Error("sphere Euler");
      for(const L of links.values()){if([...L.values()].some(s=>s.size!==2))throw Error("bad link");const seen=new Set(),todo=[[...L.keys()][0]];while(todo.length){let u=todo.pop();if(seen.has(u))continue;seen.add(u);todo.push(...L.get(u))}if(seen.size!==L.size)throw Error("disconnected link")}
      // Check all three projections retain every edge for selected sizes.
      let support=true;if(n<=32){support=T.every((_,i)=>proj(T,n,[i]));if(!support)throw Error("projection loss")}
      results.scalable.push({n,triples:T.length,minOldSupported:min,claw:[center,...leaves],sphere:true,projectionSupport:n<=32?support:"not executed"})
    }
    if(n===128)break;
    const used=new Set(Ws.flat().map(key));const f=T.find(t=>!used.has(key(t)));if(!f)throw Error("no unused face");T=glue(T,f,n);Ws=Ws.map(s=>s.concat([[n,n,n]]));
  }
  results.disconnectedModulatorLowerBound=[1,8,32,128].map(b=>({copies:b,triples:14*b,inducedDisjointClaws:b,minimumDeletionLowerBound:b}));
  return results
}
console.log(JSON.stringify(audit(),null,2));
