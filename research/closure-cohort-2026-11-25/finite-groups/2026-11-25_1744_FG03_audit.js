'use strict';
function audit(){
  let checks=0,seed=20261125;
  const assert=(x,m="assertion")=>{checks++;if(!x)throw Error(m)};
  function rng(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
  const xor=a=>a.reduce((x,y)=>x^y,0n);
  function reduce(x,B){for(const [p,v] of B)if(x&p)x^=v;return x}
  function add(B,x){x=reduce(x,B);if(!x)return false;const p=1n<<BigInt(x.toString(2).length-1);B.push([p,x]);B.sort((a,b)=>a[0]>b[0]?-1:a[0]<b[0]?1:0);return true}
  function basis(A){let B=[];for(const x of A)add(B,x);return B}
  function uniq(A){return [...new Set(A)]}
  function solve(A,t,cap=4096){
    if(A.some(s=>!s.length))return {status:"NO",stages:0,maxStates:0};
    let H=[],log=[],changed=true;
    while(changed){changed=false;
      for(let i=0;i<A.length&&!changed;i++){
        const Q=uniq(A[i].map(x=>reduce(x,H))),set=new Set(Q),a=Q[0];
        for(const x of Q){const p=x^a;if(p&&Q.every(y=>set.has(y^p))){
          log.push({i,before:H.slice(),p});assert(add(H,p),"period independent");changed=true;break;
        }}
      }
    }
    const Q=A.map(s=>{const map=new Map();for(const x of s){const y=reduce(x,H);if(!map.has(y))map.set(y,x)}return [...map].map(([v,x])=>({v,x}))});
    const shift=xor(Q.map(q=>q[0].v)),target=reduce(t,H)^shift;
    const rows=Q.map(q=>q.map(({v,x})=>({v:v^q[0].v,x})));
    let suf=Array(A.length+1);suf[A.length]=[];
    for(let i=A.length-1;i>=0;i--){suf[i]=suf[i+1].slice();for(const x of rows[i])add(suf[i],x.v)}
    if(reduce(target,suf[0]))return {status:"NO",stages:log.length,rank:suf[0].length,maxStates:0};
    let dp=new Map([[0n,[]]]),maxStates=1;
    for(let i=0;i<A.length;i++){
      const nd=new Map();for(const [s,path] of dp)for(const {v,x} of rows[i]){
        const y=s^v;if(reduce(target^y,suf[i+1])||nd.has(y))continue;
        nd.set(y,[...path,x]);if(nd.size>cap)return {status:"UNKNOWN",stages:log.length,maxStates:nd.size};
      }
      dp=nd;maxStates=Math.max(maxStates,dp.size);
      if(!dp.size)return {status:"NO",stages:log.length,rank:suf[0].length,maxStates};
    }
    if(!dp.has(target))return {status:"NO",stages:log.length,rank:suf[0].length,maxStates};
    const w=dp.get(target).slice();let delta=t^xor(w);
    for(let j=log.length-1;j>=0;j--){
      const {i,before,p}=log[j],r=reduce(delta,before);
      assert(r===0n||r===p,"lift residual in next period");
      if(r){const wanted=reduce(w[i],before)^r;const v=A[i].find(x=>reduce(x,before)===wanted);
        assert(v!==undefined,"actual replacement");delta^=w[i]^v;w[i]=v}
    }
    assert(delta===0n&&xor(w)===t&&w.every((x,i)=>A[i].includes(x)),"lift actual");
    return {status:"YES",w,stages:log.length,rank:suf[0].length,maxStates};
  }
  function brute(A){let S=new Set([0n]);for(const a of A)S=new Set([...S].flatMap(x=>a.map(y=>x^y)));return S}
  function perfect(n,T,live,a,b,force=-1){
    const adj=Array.from({length:n},()=>[]);for(const e of live)adj[T[e][a]].push(e);
    const mx=Array(n).fill(-1),my=Array(n).fill(-1);if(force>=0){if(!live.has(force))return null;mx[T[force][a]]=force;my[T[force][b]]=force}
    function dfs(x,seen){for(const e of adj[x]){const y=T[e][b];if(seen.has(y))continue;seen.add(y);const f=my[y];if(f===force&&force>=0)continue;if(f<0||dfs(T[f][a],seen)){mx[x]=e;my[y]=e;return true}}return false}
    for(let x=0;x<n;x++)if(mx[x]<0&&!dfs(x,new Set()))return null;return mx;
  }
  function close(n,T,guards=[]){
    let live=new Set(T.map((_,i)=>i));for(const [e,v] of guards){if(!v){live.delete(e);continue}if(!live.has(e))return null;for(const f of [...live])if(f!==e&&T[f].some((x,k)=>x===T[e][k]))live.delete(f)}
    let changed=true;while(changed){changed=false;
      // One-at-a-time sound deletion, repeat unit/allowed matching closure.
      outer:for(let k=0;k<3;k++)for(let v=0;v<n;v++){
        const E=[...live].filter(e=>T[e][k]===v);if(!E.length)return null;
        if(E.length===1){const e=E[0];for(const f of live)if(f!==e&&T[f].some((x,j)=>x===T[e][j])){live.delete(f);changed=true;break outer}}
      }
      if(changed)continue;
      outer2:for(const [a,b] of [[0,1],[0,2],[1,2]]){if(!perfect(n,T,live,a,b))return null;for(const e of live)if(!perfect(n,T,live,a,b,e)){live.delete(e);changed=true;break outer2}}
    }return live;
  }
  function localTables(n,T,live){
    const adj=Array.from({length:2*n},()=>[]);for(const e of live){const [x,y]=T[e];adj[x].push([n+y,e]);adj[n+y].push([x,e])}
    let seen=new Set(),out=[],cycles=0;for(let x=0;x<n;x++)if(!seen.has(x)){
      const todo=[x],xs=[],edges=new Set();seen.add(x);
      while(todo.length){const v=todo.pop();if(v<n)xs.push(v);for(const [u,e] of adj[v]){edges.add(e);if(!seen.has(u)){seen.add(u);todo.push(u)}}}
      cycles+=edges.size-2*xs.length+1;
      let S=new Map();
      function rec(j,ys,word,s){if(j===xs.length){if(!S.has(s))S.set(s,word.slice());return}for(const [,e] of adj[xs[j]]){const y=T[e][1];if(ys.has(y))continue;ys.add(y);word.push(e);rec(j+1,ys,word,s^(1n<<BigInt(T[e][2])));word.pop();ys.delete(y)}}
      rec(0,new Set(),[],0n);out.push(S);
    }return {out,cycles};
  }
  function source(n,T,guards=[]){
    const live=close(n,T,guards);if(!live)return {status:"NO",stages:0,maxStates:0,closure:true};
    const {out,cycles}=localTables(n,T,live),A=out.map(x=>[...x.keys()]);const r=solve(A,(1n<<BigInt(n))-1n);
    if(r.status==="YES"){const word=r.w.flatMap((x,i)=>out[i].get(x));assert(word.length===n&&[0,1,2].every(k=>new Set(word.map(e=>T[e][k])).size===n),"source lift");assert(guards.every(([e,v])=>word.includes(e)===!!v),"guard");}
    return {...r,w:undefined,local:A.map(x=>x.length),cycles,live:live.size,rankBefore:basis(A.flatMap(a=>a.map(x=>x^a[0]))).length};
  }
  function sourceBrute(n,T,guards=[]){let found=false;function rec(x,Y,Z,W){if(x===n){if(guards.every(([e,v])=>W.includes(e)===!!v))found=true;return}for(let e=0;e<T.length;e++){const [a,b,c]=T[e];if(a!==x||Y.has(b)||Z.has(c))continue;Y.add(b);Z.add(c);W.push(e);rec(x+1,Y,Z,W);W.pop();Y.delete(b);Z.delete(c)}}rec(0,new Set(),new Set(),[]);return found}
  function plane(n,T,R){
    const v=3*n+T.length,A=Array.from({length:v},()=>new Set());for(let e=0;e<T.length;e++)for(let k=0;k<3;k++){const x=k*n+T[e][k],y=3*n+e;A[x].add(y);A[y].add(x)}
    assert(R.length===v&&R.every((r,i)=>r.length===A[i].size&&new Set(r).size===r.length&&r.every(j=>A[i].has(j))),"rotation incidence");
    let seen=new Set([0]),todo=[0];while(todo.length)for(const j of A[todo.pop()])if(!seen.has(j)){seen.add(j);todo.push(j)}assert(seen.size===v,"connected");
    const darts=new Set();let f=0;for(let i=0;i<v;i++)for(const j of R[i])if(!darts.has(i+","+j)){let x=i,y=j;f++;do{assert(!darts.has(x+","+y),"face cycle");darts.add(x+","+y);const r=R[y],z=r[(r.indexOf(x)+1)%r.length];x=y;y=z}while(x!==i||y!==j)}
    assert(v-3*T.length+f===2,"sphere Euler");return f;
  }
  const fixtures=[
    {name:"absorbing-SAT",T:[[0,1,0],[0,1,1],[0,2,2],[1,0,1],[1,0,2],[1,1,1],[2,1,0],[2,1,2],[2,2,0]],R:[[9,11,10],[12,13,14],[17,15,16],[13,12],[9,10,14,16,15],[11,17],[15,17,9],[10,12,14],[13,11,16],[0,4,6],[4,0,7],[8,0,5],[7,3,1],[1,3,8],[1,4,7],[2,6,4],[2,4,8],[5,6,2]]},
    {name:"hull-UNSAT",T:[[0,1,1],[0,2,2],[1,0,1],[1,2,0],[2,0,0],[2,1,2],[2,2,0],[2,2,2]],R:[[9,10],[11,12],[14,16,15,13],[13,11],[9,14],[12,15,16,10],[15,12,13],[11,9],[10,16,14],[0,4,7],[5,8,0],[3,1,7],[1,6,5],[2,6,3],[4,8,2],[5,6,2],[8,5,2]]},
    {name:"one-tuple-SAT-neighbor",T:[[0,1,1],[0,1,2],[1,0,1],[1,2,0],[2,0,0],[2,1,2],[2,2,0],[2,2,2]],R:[[9,10],[11,12],[14,16,15,13],[13,11],[9,10,14],[12,15,16],[15,12,13],[11,9],[10,16,14],[0,4,7],[4,0,8],[3,1,7],[1,6,5],[2,6,3],[8,2,4],[5,6,2],[5,2,8]]}
  ];
  const summary=[];let guarded=0,yes=0,no=0,randomTargets=0;
  for(const f of fixtures){const faces=plane(3,f.T,f.R),r=source(3,f.T);assert((r.status==="YES")===sourceBrute(3,f.T));summary.push({name:f.name,faces,...r});for(let e=0;e<f.T.length;e++)for(let v=0;v<2;v++){const g=[[e,v]],a=source(3,f.T,g),b=sourceBrute(3,f.T,g);assert(a.status!=="UNKNOWN"&&(a.status==="YES")===b,"guard comparison");guarded++;b?yes++:no++}}
  assert(summary[0].stages===2&&summary[0].rank===0,"absorption cascade in actual source");
  assert(summary[1].status==="NO"&&summary[2].status==="YES","source neighbors");
  for(let trial=0;trial<350;trial++){
    const d=1+rng(7),g=1+rng(6),A=Array.from({length:g},()=>uniq(Array.from({length:1+rng(7)},()=>BigInt(rng(1<<d))))),S=brute(A);
    for(let t=0;t<(1<<d);t++){const r=solve(A,BigInt(t));assert(r.status!=="UNKNOWN"&&(r.status==="YES")===S.has(BigInt(t)),"random support");randomTargets++}
  }
  // Adversarial family of exact finite support tables, not a claimed planar source compiler.
  const cascade=[];
  for(const n of [4,16,64,128]){
    const E=i=>1n<<BigInt(i),A=Array.from({length:n-1},(_,i)=>[0n,E(i),E(i)^E(i+1)]);A.push([0n,E(0)]);
    const r=solve(A,E(n-1));assert(r.status==="YES"&&r.stages===n&&r.rank===0);
    const B=A.slice();B[B.length-1]=[0n];const s=solve(B,E(n-1));assert(s.status==="NO","seed removed");
    cascade.push({n,rank:n,localRankSum:2*n-1,absorbed:r.stages,remaining:r.rank,seedRemoved:s.status,seedRemovedStates:s.maxStates})
  }
  // Disconnected actual planar source copies; use real local source tables, no invented high-width promise.
  const disjoint=[];
  for(const k of [1,4,16,32]){
    const T=[];for(let i=0;i<k;i++)for(const t of fixtures[0].T)T.push(t.map(x=>x+3*i));
    const r=source(3*k,T);assert(r.status==="YES"&&r.stages===2*k);disjoint.push({copies:k,tuples:T.length,groups:r.local.length,rankBefore:r.rankBefore,cycles:r.cycles,absorbed:r.stages,remaining:r.rank,maxStates:r.maxStates})
  }
  const pair=[[0n,1n,2n],[0n,1n,2n]];assert(solve(pair,3n).stages===0&&brute(pair).size===4,"local period saturation is not complete");
  return {seed:20261125,checks,randomTargets,guarded,guardedYES:yes,guardedNO:no,fixtures:summary,cascade,disjoint,pairObstruction:"two aperiodic 3-point sets have full 4-point sum",scope:"actual source local table enumeration only; no Fourier implementation; cascade tables abstract"};
}
console.log(JSON.stringify(audit(),null,2));
