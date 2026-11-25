const inputs = [{"n":7,"root":[{"t":[0,1,2],"bad":[0,7]},{"t":[0,3,4],"bad":[0,7]},{"t":[0,5,6],"bad":[0,7]},{"t":[1,3,5],"bad":[0,7]},{"t":[1,4,6],"bad":[0,7]},{"t":[2,3,6],"bad":[0,7]},{"t":[2,4,5],"bad":[0,7]}],"sat":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[0,7]},{"t":[0,5,6],"bad":[0,7]},{"t":[1,3,5],"bad":[0,7]},{"t":[1,4,6],"bad":[0,7]},{"t":[2,3,6],"bad":[0,7]},{"t":[2,4,5],"bad":[0,7]}],"guards":[]},{"n":15,"root":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[1,6]},{"t":[0,5,6],"bad":[3,4]},{"t":[0,7,8],"bad":[2,5]},{"t":[0,9,10],"bad":[3,4]},{"t":[0,11,12],"bad":[3,4]},{"t":[0,13,14],"bad":[1,6]},{"t":[1,3,5],"bad":[2,5]},{"t":[1,4,6],"bad":[3,4]},{"t":[1,7,9],"bad":[1,6]},{"t":[1,8,10],"bad":[3,4]},{"t":[1,11,13],"bad":[1,6]},{"t":[1,12,14],"bad":[2,5]},{"t":[2,3,6],"bad":[1,6]},{"t":[2,4,5],"bad":[2,5]},{"t":[2,7,10],"bad":[3,4]},{"t":[2,8,9],"bad":[2,5]},{"t":[2,11,14],"bad":[1,6]},{"t":[2,12,13],"bad":[1,6]},{"t":[3,7,11],"bad":[3,4]},{"t":[3,8,12],"bad":[3,4]},{"t":[3,9,13],"bad":[3,4]},{"t":[3,10,14],"bad":[3,4]},{"t":[4,7,12],"bad":[1,6]},{"t":[4,8,11],"bad":[2,5]},{"t":[4,9,14],"bad":[2,5]},{"t":[4,10,13],"bad":[1,6]},{"t":[5,7,13],"bad":[1,6]},{"t":[5,8,14],"bad":[3,4]},{"t":[5,9,11],"bad":[2,5]},{"t":[5,10,12],"bad":[2,5]},{"t":[6,7,14],"bad":[3,4]},{"t":[6,8,13],"bad":[2,5]},{"t":[6,9,12],"bad":[2,5]},{"t":[6,10,11],"bad":[0,7]}],"sat":[{"t":[0,1,2],"bad":[2,5]},{"t":[0,3,4],"bad":[1,6]},{"t":[0,5,6],"bad":[3,4]},{"t":[0,7,8],"bad":[2,5]},{"t":[0,9,10],"bad":[3,4]},{"t":[0,11,12],"bad":[3,4]},{"t":[0,13,14],"bad":[1,6]},{"t":[1,3,5],"bad":[2,5]},{"t":[1,4,6],"bad":[3,4]},{"t":[1,7,9],"bad":[1,6]},{"t":[1,8,10],"bad":[3,4]},{"t":[1,11,13],"bad":[1,6]},{"t":[1,12,14],"bad":[2,5]},{"t":[2,3,6],"bad":[1,6]},{"t":[2,4,5],"bad":[2,5]},{"t":[2,7,10],"bad":[3,4]},{"t":[2,8,9],"bad":[2,5]},{"t":[2,11,14],"bad":[1,6]},{"t":[2,12,13],"bad":[1,6]},{"t":[3,7,11],"bad":[3,4]},{"t":[3,8,12],"bad":[3,4]},{"t":[3,9,13],"bad":[3,4]},{"t":[3,10,14],"bad":[3,4]},{"t":[4,7,12],"bad":[1,6]},{"t":[4,8,11],"bad":[2,5]},{"t":[4,9,14],"bad":[2,5]},{"t":[4,10,13],"bad":[1,6]},{"t":[5,7,13],"bad":[1,6]},{"t":[5,8,14],"bad":[3,4]},{"t":[5,9,11],"bad":[2,5]},{"t":[5,10,12],"bad":[2,5]},{"t":[6,7,14],"bad":[3,4]},{"t":[6,8,13],"bad":[2,5]},{"t":[6,9,12],"bad":[2,5]},{"t":[6,10,11],"bad":[2,5]}],"guards":[[4,6,0],[6,8,0],[0,3,0],[1,2,0],[2,3,0],[3,5,1],[5,7,1]]}];
const run = function run(inputs) {
  const stats={assertions:0, balanceTests:0,flowCalls:0,augmentations:0, boundaryTrials:0, projections:0,closureScans:0,forcedMerges:0,sourceClosureScans:0,referenceWords:0};
  const check=(v,m)=>{stats.assertions++;if(!v)throw Error("Assertion "+stats.assertions+": "+m)};
  const b=(x,i)=>(x>>>i)&1;
  const energy=(E,x)=>E.reduce((s,[u,v,p,w])=>s+w*Number((x[u]^x[v])!==p),0);
  function normalize(V,E,K=0) {
    let M=new Map();
    for(let [u,v,p,w] of E){if(!w)continue;if(u===v){K+=p*w;continue}
      if(u>v)[u,v]=[v,u];let id=u+","+v,a=M.get(id)||[u,v,0,0];a[2+p]+=w;M.set(id,a)}
    let out=[];for(let [u,v,a,c] of M.values()){K+=Math.min(a,c);if(a!==c)out.push([u,v,Number(c>a),Math.abs(a-c)])}
    return {V,E:out,K};
  }
  function balance(V,E,del=new Set()) {
    stats.balanceTests++;let A=new Map(V.filter(v=>!del.has(v)).map(v=>[v,[]]));
    for(let [u,v,p,w] of E)if(A.has(u)&&A.has(v)&&w){A.get(u).push([v,p]);A.get(v).push([u,p])}
    let g={};for(let v of A.keys())if(g[v]===undefined){g[v]=0;let q=[v];for(let i=0;i<q.length;i++)for(let [w,p] of A.get(q[i])){let z=g[q[i]]^p;if(g[w]===undefined){g[w]=z;q.push(w)}else if(g[w]!==z)return null}}
    return g;
  }
  function* combos(V,k,start=0,prev=[]){if(!k){yield prev;return}for(let i=start;i<=V.length-k;i++)yield*combos(V,k-1,i+1,[...prev,V[i]])}
  function findMod(V,E,k){
    for(let j=0;j<=Math.min(k,V.length);j++)for(let X of combos(V,j)){let g=balance(V,E,new Set(X));if(g)return {X,g}}
    return null;
  }
  function maxflow(cap,s,t){
    stats.flowCalls++;let n=cap.length,R=cap.map(a=>a.slice()),f=0;
    for(;;){let p=Array(n).fill(-1),q=[s];p[s]=s;
      for(let i=0;i<q.length&&p[t]<0;i++)for(let j=0;j<n;j++)if(p[j]<0&&R[q[i]][j]>0){p[j]=q[i];q.push(j)}
      if(p[t]<0)return {f,reach:new Set(q)};
      let d=Infinity;for(let v=t;v!==s;v=p[v])d=Math.min(d,R[p[v]][v]);
      for(let v=t;v!==s;v=p[v]){R[p[v]][v]-=d;R[v][p[v]]+=d}f+=d;stats.augmentations++;
    }
  }
  function localOpt(C,E,B,pin,mod){
    let {X,g}=mod,U=C.filter(v=>!X.includes(v)),I=new Map(U.map((v,i)=>[v,i])),s=U.length,t=s+1,best=null;
    for(let a=0;a<2**X.length;a++){
      let x={...pin};X.forEach((v,i)=>x[v]=b(a,i));let cap=Array.from({length:t+1},()=>Array(t+1).fill(0)),K=0;
      for(let [u,v,p,w] of E){
        let uu=I.has(u),vv=I.has(v);
        if(uu&&vv){check((g[u]^g[v])===p,"gauge");cap[I.get(u)][I.get(v)]+=w;cap[I.get(v)][I.get(u)]+=w}
        else if(!uu&&!vv)K+=w*Number((x[u]^x[v])!==p);
        else {if(!uu)[u,v]=[v,u];let want=g[u]^x[v]^p;if(want===0)cap[s][I.get(u)]+=w;else cap[I.get(u)][t]+=w;}
      }
      let z=maxflow(cap,s,t);for(let u of U)x[u]=g[u]^Number(!z.reach.has(I.get(u)));
      check(energy(E,x)===K+z.f,"mincut witness");let cost=K+z.f;if(!best||cost<best.cost)best={cost,x};
    }
    return best;
  }
  function connected(V,E,B){
    let D=new Set(B),A=new Map(V.filter(v=>!D.has(v)).map(v=>[v,[]]));
    for(let [u,v] of E)if(A.has(u)&&A.has(v)){A.get(u).push(v);A.get(v).push(u)}
    let seen=new Set(),out=[];for(let v of A.keys())if(!seen.has(v)){let q=[v];seen.add(v);for(let i=0;i<q.length;i++)for(let w of A.get(q[i]))if(!seen.has(w)){q.push(w);seen.add(w)}out.push(q)}
    return out;
  }
  function project(C,B,E,mod) {
    let T=[],F=[],base;
    for(let a=0;a<2**B.length;a++){let pin={};B.forEach((v,i)=>pin[v]=b(a,i));let z=localOpt(C,E,B,pin,mod);T.push(z);F.push(z.cost)}
    for(let a=0;a<F.length;a++)check(F[a]===F[F.length-1-a],"complement symmetry");
    // Fourier coefficient of pair in the projected energy; mismatch with p=0 has coefficient -w/2.
    let K=F.reduce((s,v)=>s+v,0)/F.length;
    let P=[];
    for(let i=0;i<B.length;i++)for(let j=i+1;j<B.length;j++){
      let c=F.reduce((s,v,a)=>s+v*((b(a,i)^b(a,j))?-1:1),0)/F.length;
      if(c){let w=2*Math.abs(c);P.push([B[i],B[j],Number(c>0),w]);K-=w/2}
    }
    for(let a=0;a<F.length;a++){let pin={};B.forEach((v,i)=>pin[v]=b(a,i));check(K+energy(P,pin)===F[a],"projection table")}
    stats.projections++;return {P,K,T};
  }
  function close(G,history){
    for(;;){stats.closureScans++;let zero=Object.fromEntries(G.V.map(v=>[v,0])),ub=energy(G.E,zero),e=G.E.find(e=>e[3]>ub);
      if(!e)return G;let [u,v,p]=e;history.push({kind:"merge",u,v,p});stats.forcedMerges++;
      G=normalize(G.V.filter(w=>w!==v),G.E.map(([a,b,q,w])=>[a===v?u:a,b===v?u:b,q^((a===v)?p:0)^((b===v)?p:0),w]),G.K)
    }
  }
  function solve(G,k,combined){
    let original=G,history=[],stages=0;G=close(G,history);
    while(true){let mod=findMod(G.V,G.E,k);
      if(mod){let z=localOpt(G.V,G.E,[],{},mod),x=z.x,cost=z.cost+G.K;
        for(let r of history.reverse())if(r.kind==="merge")x[r.v]=x[r.u]^r.p;else {let a=r.B.reduce((s,v,i)=>s+2**i*x[v],0);Object.assign(x,r.T[a].x)}
        check(energy(original.E,x)+original.K===cost,"global lift");return {cost,x,stages}}
      if(!combined)return {open:true,stages};let found=false;
      for(let j=1;j<=Math.min(3,G.V.length-1)&&!found;j++)for(let S of combos(G.V,j)){
        stats.boundaryTrials++;for(let C of connected(G.V,G.E,S)){
          let cs=new Set(C),LE=G.E.filter(([u,v])=>cs.has(u)||cs.has(v)),B=[...new Set(LE.flatMap(([u,v])=>[u,v]).filter(v=>!cs.has(v)))].sort((a,b)=>a-b);
          let lm=findMod(C,LE,k);if(!lm)continue;
          let z=project(C,B,LE,lm);history.push({kind:"project",B,T:z.T});stages++;
          G=normalize(G.V.filter(v=>!cs.has(v)),[...G.E.filter(([u,v])=>!cs.has(u)&&!cs.has(v)),...z.P],G.K+z.K);
          G=close(G,history);found=true;break;
        }
        if(found)break;
      }
      if(!found){G=close(G,history);return {open:true,stages}}
    }
  }
  function reference(V,E,K=0,pin={}){
    let U=V.filter(v=>pin[v]===undefined),best=Infinity;
    for(let a=0;a<2**U.length;a++){stats.referenceWords++;let x={...pin};U.forEach((v,i)=>x[v]=b(a,i));best=Math.min(best,K+energy(E,x))}
    return best;
  }
  // Actual guard-relative certified NAE closure. Each parity equation is x_u XOR x_v=p.
  function source(n,O,guards){
    let par=Array.from({length:n},(_,i)=>i),rel=Array(n).fill(0);
    function f(i){if(par[i]===i)return [i,0];let [r,p]=f(par[i]);rel[i]^=p;par[i]=r;return [r,rel[i]]}
    function add(u,v,p){let [a,x]=f(u),[d,y]=f(v);if(a===d)return (x^y)===p?0:-1;par[d]=a;rel[d]=p^x^y;return 1}
    for(let [u,v,p] of guards)if(add(u,v,p)<0)return null;
    for(;;){stats.sourceClosureScans++;let changed=false;
      for(let {t,bad} of O){let q=t.map((v,i)=>{let [r,p]=f(v);return [r,p^b(bad[0],i)]});
        let distinct=[...new Set(q.map(z=>z[0]))],done=false;
        for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(q[i][0]===q[j][0]&&q[i][1]!==q[j][1])done=true;
        if(done)continue;
        if(distinct.length===1)return null;
        if(distinct.length===2){let k=q.findIndex((z,i)=>q.filter(w=>w[0]===z[0]).length===1),a=q[(k+1)%3],d=q[k],z=add(a[0],d[0],1^a[1]^d[1]);if(z<0)return null;if(z>0){changed=true;break}}
      }
      if(!changed)break;
    }
    let L=Array.from({length:n},(_,i)=>f(i)),E=[];
    for(let {t,bad} of O)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let [u,p]=L[t[i]],[v,q]=L[t[j]];E.push([u,v,1^p^q^b(bad[0],i)^b(bad[0],j),1])}
    return {G:normalize([...new Set(L.map(z=>z[0]))].sort((a,b)=>a-b),E),L};
  }
  function verifySource(n,O,guards,z,L){
    let x=L.map(([v,p])=>z.x[v]^p);
    check(guards.every(([u,v,p])=>(x[u]^x[v])===p),"source guard");
    let violated=O.filter(({t,bad})=>bad.includes(t.reduce((a,v,i)=>a+2**i*x[v],0))).length;
    check(z.cost===O.length+2*violated,"source energy identity");return {violated,word:x.join("")}
  }
  let actual=[];
  for(let o of inputs)for(let [label,O,guards] of [["root",o.root,[]],["sat",o.sat,[]],...(o.guards.length?[["first",o.root,o.guards.slice(0,1)],["all",o.root,o.guards]]:[])]){
    let n=o.n,min=Infinity,models=0;
    for(let a=0;a<2**n;a++){stats.referenceWords++;if(!guards.every(([u,v,p])=>(b(a,u)^b(a,v))===p))continue;let q=O.filter(({t,bad})=>bad.includes(t.reduce((s,v,i)=>s+2**i*b(a,v),0))).length;min=Math.min(min,O.length+2*q);if(q===0)models++}
    let S=source(n,O,guards);if(!S){check(!models,"source closure");actual.push({n,label,models,min,baseline:"UNSAT by closure",combined:"UNSAT by closure"});continue}
    let a=solve(S.G,2,false),c=solve(S.G,2,true);for(let z of [a,c])if(!z.open){check(z.cost===min,"source optimum");z.lift=verifySource(n,O,guards,z,S.L)}
    actual.push({n,label,models,min,baseline:a.open?"OPEN":a.cost,combined:c.open?"OPEN":c.cost,stages:c.stages,lift:c.lift||null})
  }
  let seed=0x5d235023;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
  let localTests=0;
  for(let it=0;it<120;it++){let h=2+rand(6),q=rand(4),C=Array.from({length:h},(_,i)=>i),B=Array.from({length:q},(_,i)=>i+h),V=[...C,...B],E=[],g=C.map(()=>rand(2));
    for(let i=0;i<h;i++)for(let j=i+1;j<h;j++)if(rand(3))E.push([i,j,i<2?rand(2):g[i]^g[j],1+rand(7)]);
    for(let i of C)for(let j of B)if(rand(3))E.push([i,j,rand(2),1+rand(7)]);
    let mod=findMod(C,E,2);check(!!mod,"planted modulator");let z=project(C,B,E,mod);
    for(let a=0;a<2**q;a++){let p={};B.forEach((v,i)=>p[v]=b(a,i));check(z.T[a].cost===reference(V,E,0,p),"local independent optimum");localTests++}
  }
  const synthetic=[];
  for(let h of [2,4,8]){let V=Array.from({length:5*h+1},(_,i)=>i),E=[];
    for(let i=0;i<=h;i++)for(let j=i+1;j<=h;j++)E.push([i,j,0,2]);
    for(let i=0;i<h;i++){let C=Array.from({length:4},(_,j)=>h+1+4*i+j);for(let a=0;a<4;a++){for(let b=a+1;b<4;b++)E.push([C[a],C[b],1,1]);for(let v of [i,i+1])E.push([C[a],v,0,1]);}}
    let G=normalize(V,E),a=solve(G,2,false),c=solve(G,2,true);check(c.cost===5*h,"module expected optimum");check(a.open,"global cap fails");synthetic.push({modules:h,n:V.length,edges:E.length,baseline:"OPEN",combined:c.cost,stages:c.stages,thresholdSAT:5*h,thresholdUNSAT:5*h-1})
  }
  let f=Array.from({length:16},(_,a)=>{let k=[0,1,2,3].reduce((s,i)=>s+b(a,i),0);return Math.min(k,4-k)}),quartic=f.reduce((s,v,a)=>s+v*(([0,1,2,3].reduce((p,i)=>p^b(a,i),0))?-1:1),0)/16;check(quartic!==0,"four-port obstruction");
  return {pin:"0100a1421a264b657dc9b7f3a257dbd07dc06a44",actual,localTests,synthetic,quartic,stats};
};
console.log(JSON.stringify(run(inputs),null,2));
