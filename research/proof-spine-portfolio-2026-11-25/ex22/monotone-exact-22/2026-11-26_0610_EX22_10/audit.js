console.log(JSON.stringify((function audit(){
  const assert=(x,msg)=>{if(!x)throw Error(msg)};let checks=0;const ck=(x,m)=>{checks++;assert(x,m)};
  let seed=20261126;const rng=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
  const bits=(i,n)=>Array.from({length:n},(_,j)=>(i>>>j)&1);
  function fresh(E){return {E,p:[],edges:[],pins:{},add(p){this.p.push(p);return this.p.length-1},edge(u,v,z){ck(this.p[u]===0&&this.p[v]===1,"bipartition");this.edges.push([u,v,z])}}}
  function compile(n,clauses,mode){
    // E: original n bits, c0=n,c1=n+1, selector=n+2 (chain only)
    const g=fresh(n+(mode==="chain"?3:2));let c0=n,c1=n+1;g.extPins={[c0]:0,[c1]:1};
    function branch(a,b,z,value){let t=g.add(1);if(value===1){g.edge(a,t,z);g.edge(b,t,c0)}else{g.edge(a,t,c1);g.edge(b,t,z)}}
    if(mode==="chain"){let a=g.add(0);g.pins[a]=1;for(const C of [...clauses,[[n+2,1]]]){let b=g.add(0);for(const [z,v] of C)branch(a,b,z,v);a=b}g.pins[a]=0}
    else for(const C of clauses){let a=g.add(0);g.pins[a]=1;for(const [z,v] of C){let b=g.add(0);branch(a,b,z,1-v);a=b}g.pins[a]=0}
    return g;
  }
  function native(g){let rows=g.edges.map(([u,v,z],i)=>[g.E+u,g.E+v,z,g.E+g.p.length+i]);let n=g.E+g.p.length+rows.length;const pin={...g.extPins};for(const [u,b] of Object.entries(g.pins))pin[g.E+ +u]=b^g.p[u];return {rows,n,pin}}
  function reach(g,x){
    let adj=g.p.map(()=>[]);for(const [u,v,z] of g.edges){if(x[z])adj[u].push(v);else adj[v].push(u)}
    let y=g.p.map(()=>0),q=[];for(const [i,b] of Object.entries(g.pins))if(b){y[i]=1;q.push(+i)}
    for(let i=0;i<q.length;i++)for(const v of adj[q[i]])if(!y[v]){y[v]=1;q.push(v)}
    if(Object.entries(g.pins).some(([i,b])=>!b&&y[i]))return null;
    let X=[...x,...y.map((b,i)=>b^g.p[i])];for(const [u,v,z] of g.edges)X.push(2-X[g.E+u]-X[g.E+v]-X[z]);return X;
  }
  function verify(H,x){ck(x.length===H.n&&x.every(v=>v===0||v===1),"Boolean");ck(H.rows.every(C=>C.reduce((s,v)=>s+x[v],0)===2),"native witness");ck(Object.entries(H.pin).every(([i,b])=>x[i]===b),"pins")}
  function cnf(g){
    const adj=g.p.map(()=>[]);g.edges.forEach(([u,v,z])=>{adj[u].push([v,z,1]);adj[v].push([u,z,0])});
    // Forest check (parallel edges count as cycles).
    const seen=new Set();for(let s=0;s<adj.length;s++)if(!seen.has(s)){let q=[[s,-1]];seen.add(s);for(let i=0;i<q.length;i++){let [u,p]=q[i];let parents=0;for(let [v] of adj[u]){if(v===p){parents++;continue}ck(!seen.has(v),"not a forest");seen.add(v);q.push([v,u])}ck(parents<=1,"parallel")}}
    let caps=[];
    for(const [ss,b] of Object.entries(g.pins))if(b){let s=+ss;let parent=Array(adj.length).fill(null);parent[s]=[-1,-1,-1];let q=[s];for(let i=0;i<q.length;i++)for(let [v,z,k] of adj[q[i]])if(parent[v]===null){parent[v]=[q[i],z,k];q.push(v)}
      for(const [tt,b] of Object.entries(g.pins))if(!b&&parent[tt]!==null){let t=+tt,need=new Map(),bad=false;while(t!==s){let [v,z,k]=parent[t];if((z in g.extPins&&g.extPins[z]!==k)||(need.has(z)&&need.get(z)!==k)){bad=true;break}need.set(z,k);t=v}if(!bad)caps.push([...need].filter(([z])=>!(z in g.extPins)).map(([z,k])=>[z,1-k]))}
    }return caps;
  }
  const satC=(C,x)=>C.some(([z,k])=>x[z]===k);
  function exCNF(F){return F.flatMap(C=>C.flatMap((_,j)=>[C.filter((_,i)=>i!==j).map(z=>[z,1]),C.filter((_,i)=>i!==j).map(z=>[z,0])]))}
  function gac(H,extra={},probe=false){let d=Array(H.n).fill(3), scans=0;for(const [i,b] of Object.entries({...H.pin,...extra}))d[i]=1<<b;function prop(D){let ch=true;while(ch){ch=false;for(const C of H.rows){scans++;let lo=0,hi=0;for(const v of C){lo+=D[v]===2;hi+=D[v]!==1}if(lo>2||hi<2)return false;for(const v of C)if(D[v]===3&&(lo===2||hi===2)){D[v]=lo===2?1:2;ch=true}}}return true}let ok=prop(d),failed=0;if(ok&&probe){let changed=true;while(changed&&ok){changed=false;for(let i=0;i<d.length;i++)if(d[i]===3){for(let b=0;b<2;b++){let D=d.slice();D[i]=1<<b;if(!prop(D)){d[i]=1<<(1-b);failed++;changed=true;ok=prop(d);break}}if(!ok)break}}}return {ok,scans,failed,free:d.filter(v=>v===3).length}}
  function twoSat(n,C){
    let adj=Array.from({length:2*n},()=>[]),rev=adj.map(()=>[]);const add=(a,b)=>{adj[a].push(b);rev[b].push(a)};
    for(const c of C){if(!c.length)return false;ck(c.length<=2,"2cnf arity");let a=2*c[0][0]+c[0][1],b=2*c[c.length-1][0]+c[c.length-1][1];add(a^1,b);add(b^1,a)}
    let seen=new Set(),order=[];function dfs(u){if(seen.has(u))return;seen.add(u);adj[u].forEach(dfs);order.push(u)}for(let u=0;u<adj.length;u++)dfs(u);let comp=Array(adj.length).fill(-1),id=0;function dfs2(u){if(comp[u]>=0)return;comp[u]=id;rev[u].forEach(dfs2)}for(const u of order.reverse())if(comp[u]<0){dfs2(u);id++}return Array.from({length:n},(_,i)=>comp[2*i]!==comp[2*i+1]).every(Boolean)
  }
  let random={forests:0,boundaries:0,bruteInteriorWords:0,admitted2CNF:0,universal:0};
  for(let t=0;t<240;t++){let g=fresh(4);g.extPins={};let n=3+rng(5);g.add(0);for(let i=1;i<n;i++){let j=rng(i);g.add(1-g.p[j]);g.edge(...(g.p[j]===0?[j,i]:[i,j]),rng(4))}for(let i=0;i<n;i++)if(rng(3)===0)g.pins[i]=rng(2);let H=native(g),C=cnf(g);let any=false,all=true;for(let w=0;w<16;w++){let x=bits(w,4),Y=reach(g,x),ref=false;for(let v=0;v<(1<<n);v++){random.bruteInteriorWords++;let a=bits(v,n);if(Object.entries(g.pins).some(([i,b])=>(a[i]^g.p[i])!==b))continue;if(g.edges.every(([u,v,z])=>{let sum=a[u]+a[v]+x[z];return sum===1||sum===2})){ref=true;break}}ck(!!Y===ref&&C.every(c=>satC(c,x))===ref,"forest cap/ref");if(Y)verify(H,Y);any||=ref;all&&=ref;random.boundaries++}if(C.every(c=>c.length<=2)){ck(twoSat(4,C)===any,"SCC");random.admitted2CNF++}if(all){ck(C.length===0,"universal forest");random.universal++}random.forests++}
  let exhaustive=[];for(const F of [[[0,1,2,3]],Array.from({length:5},(_,i)=>[0,1,2,3,4].filter(j=>i!==j))]){let n=Math.max(...F.flat())+1,C=exCNF(F),a=compile(n,C,"chain"),b=compile(n,C,"forest"),Ha=native(a),Hb=native(b),D=cnf(b),models=0,blocked=0;for(let w=0;w<(1<<n);w++){let x=bits(w,n),ok=F.every(c=>c.reduce((s,i)=>s+x[i],0)===2);models+=ok;let xb=[...x,0,1],yb=reach(b,xb);ck(!!yb===ok&&D.every(c=>satC(c,xb))===ok,"forest compiler");if(yb)verify(Hb,yb);for(let s=0;s<2;s++){let xa=[...x,0,1,s],ya=reach(a,xa);ck(!!ya===!(s&&ok),"chain compiler");if(ya)verify(Ha,ya);else blocked++}}exhaustive.push({n,sourceClauses:F.length,models,blocked,chainRows:Ha.rows.length,forestRows:Hb.rows.length,forestCapClauses:D.length,chainClosure:gac(Ha,{},true),forestClosure:gac(Hb,{},true)})}
  // Native unguarded relative pin compiler: alternating six-module, using reference r.
  function pinLift(H,ext,model){let rows=H.rows.map(c=>c.slice()),n=H.n,r=n++,pins={...H.pin,...ext},Y=model?model.slice():null;if(Y)Y.push(0);for(const [i,b] of Object.entries(pins)){let a=Array(6);a[0]=r;a[b?1:2]=+i;for(let j=0;j<6;j++)if(a[j]===undefined){a[j]=n++;if(Y)Y.push(j%2)}for(let j=0;j<6;j++)rows.push(a.filter((_,l)=>l!==j&&l!==(j+1)%6));if(Y)ck(Y[+i]===b,"relative pin")}let out={rows,n,pin:{}};if(Y)verify(out,Y);return out}
  let scalable=[];for(const k of [1,2,4,8,16,32,64]){let F=Array.from({length:k},(_,i)=>[4*i,4*i+1,4*i+2,4*i+3]),n=4*k,C=exCNF(F),g=compile(n,C,"chain"),H=native(g),good=Array.from({length:n},(_,i)=>+(i%4>=2)),bad=good.slice();bad[0]=1;let x0=[...good,0,1,1],x1=[...bad,0,1,1],Y0=reach(g,x0),Y1=reach(g,x1);ck(!Y0&&!!Y1,"neighbors");verify(H,Y1);const ext=x=>Object.fromEntries(x.map((b,i)=>[i,b]));let no=pinLift(H,ext(x0),null),yes=pinLift(H,ext(x1),Y1);const valid=K=>K.rows.every(c=>c.length===4&&new Set(c).size===4);ck(valid(no)&&valid(yes),"proper neighbor");let gc0=gac(H,ext(x0)),gc1=gac(H,ext(x1));ck(!gc0.ok&&gc1.ok,"guarded closure");scalable.push({k,chainRows:H.rows.length,physicalVars:yes.n,physicalRows:yes.rows.length,guardedNOscans:gc0.scans,guardedYESscans:gc1.scans});}
  return {seed:20261126,random,exhaustive,scalable,checks};
})(), null, 2));
