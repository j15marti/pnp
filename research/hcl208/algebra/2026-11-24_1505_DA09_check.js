"use strict";
function run(){
 const C={assertions:0,closureSweeps:0,arcTests:0,blocks:0,reduceScans:0,doubleSteps:0,dropSteps:0,degreeCalls:0,blockTuples:0,referenceNodes:0,lifts:0};
 const counts={random:{sat:0,unsat:0},fano:{sat:0,unsat:0},chain:{sat:0,unsat:0},closed:{sat:0,unsat:0},k4:{sat:0,unsat:0}};
 const A=(v,msg)=>{C.assertions++;if(!v)throw Error(msg)};
 const pop=m=>((m&1)+((m>>1)&1)+((m>>2)&1)+((m>>3)&1)), colors=m=>[0,1,2,3].filter(x=>m&(1<<x));
 const key=(u,v)=>u<v?u+","+v:v+","+u;
 const canon=E=>{const M=new Map();for(const [u,v,m] of E){if(u===v)throw Error("loop");if(m)M.set(key(u,v),(M.get(key(u,v))||0)|m)}return [...M].map(([k,m])=>[...k.split(",").map(Number),m])};
 const ok=(E,x)=>E.every(([u,v,m])=>x.has(u)&&x.has(v)&&!(m&(1<<(x.get(u)^x.get(v)))));
 const adj=(V,E)=>{let a=new Map(V.map(v=>[v,[]]));for(const [u,v,m] of E){a.get(u).push([v,m]);a.get(v).push([u,m])}return a};
 const components=(V,E)=>{let a=adj(V,E),seen=new Set(),out=[];for(const v of V)if(!seen.has(v)){let q=[v];seen.add(v);for(let i=0;i<q.length;i++)for(const [w] of a.get(q[i]))if(!seen.has(w)){seen.add(w);q.push(w)}out.push(q)}return out};
 function blockList(V,E){
  const a=adj(V,E),disc=new Map(),low=new Map(),stack=[],out=[];let time=0;
  function dfs(u,p){disc.set(u,++time);low.set(u,time);for(const [v,m] of a.get(u)){if(v===p)continue;if(!disc.has(v)){stack.push([u,v,m]);dfs(v,u);low.set(u,Math.min(low.get(u),low.get(v)));if(low.get(v)>=disc.get(u)){let b=[],e;do{e=stack.pop();b.push(e)}while(e[0]!==u||e[1]!==v);out.push(b)}}else if(disc.get(v)<disc.get(u)){stack.push([u,v,m]);low.set(u,Math.min(low.get(u),disc.get(v)))}}}
  for(const v of V)if(!disc.has(v))dfs(v,-1); C.blocks+=out.length;
  return out.map(e=>{const v=[...new Set(e.flatMap(([u,v])=>[u,v]))],a=adj(v,e);const clique=e.length===v.length*(v.length-1)/2,cycle=v.length>=3&&v.every(u=>a.get(u).length===2);return {e,v,a,clique,cycle,gdp:(clique||cycle)&&e.every(x=>pop(x[2])===pop(e[0][2]))}})
 }
 function closure(V,E,pins=new Map()){
  const D=new Map(V.map(v=>[v,pins.has(v)?1<<pins.get(v):15]));let changed=true;
  while(changed){C.closureSweeps++;changed=false;for(const [u,v,m] of E)for(const [a,b] of [[u,v],[v,u]]){let keep=0;for(const x of colors(D.get(a)))for(const y of colors(D.get(b))){C.arcTests++;if(!(m&(1<<(x^y)))){keep|=1<<x;break}}if(keep!==D.get(a)){D.set(a,keep);changed=true;if(!keep)return false}}}return true
 }
 function canDegree(V,E,D){
  C.degreeCalls++;if(V.some(v=>!D.get(v)))return false;
  const aa=adj(V,E);
  for(const v of V)A(pop(D.get(v))>=aa.get(v).reduce((s,e)=>s+pop(e[1]),0),"degree invariant");
  for(const vv of components(V,E)){
   const S=new Set(vv),ee=E.filter(([u,v])=>S.has(u)&&S.has(v));
   if(vv.some(v=>pop(D.get(v))>aa.get(v).reduce((s,e)=>s+pop(e[1]),0)))continue;
   const B=blockList(vv,ee);if(B.some(b=>!b.gdp))continue;
   const at=new Map(vv.map(v=>[v,[]]));B.forEach((b,i)=>b.v.forEach(v=>at.get(v).push(i)));
   function vm(v,prev){let m=D.get(v);for(const i of at.get(v))if(i!==prev)m&=bm(i,v);return m}
   function bm(i,root){
    const b=B[i],rest=b.v.filter(v=>v!==root),L=new Map(rest.map(v=>[v,vm(v,i)]));let out=0;
    if(b.clique){
     const z=new Map();function rec(j){if(j===rest.length)return true;const v=rest[j];for(const x of colors(L.get(v))){C.blockTuples++;if(b.a.get(v).every(([w,m])=>!z.has(w)||!(m&(1<<(x^z.get(w)))))){z.set(v,x);if(rec(j+1))return true;z.delete(v)}}return false}
     for(let c=0;c<4;c++){z.clear();z.set(root,c);if(rec(0))out|=1<<c}
    }else{
     const order=[root];let prev=-1,v=root;while(true){const w=b.a.get(v).find(([u])=>u!==prev)[0];if(w===root)break;order.push(w);prev=v;v=w}
     A(order.length===b.v.length,"cycle ordering");
     for(let c=0;c<4;c++){let m=1<<c;for(let j=1;j<order.length;j++){let next=0,edge=b.a.get(order[j]).find(([u])=>u===order[j-1])[1];for(const x of colors(L.get(order[j])))for(const y of colors(m)){C.blockTuples++;if(!(edge&(1<<(x^y))))next|=1<<x}m=next}let edge=b.a.get(order[order.length-1]).find(([u])=>u===root)[1];if(colors(m).some(x=>!(edge&(1<<(x^c)))))out|=1<<c}
    }return out
   }
   if(!vm(vv[0],-1))return false
  }return true
 }
 function solveFixed(V,E,pins){
  if(!closure(V,E,pins))return null;
  let D=new Map(V.filter(v=>!pins.has(v)).map(v=>[v,15]));let x=new Map(pins);
  for(const [u,v,m] of E){if(pins.has(u)&&pins.has(v)){if(m&(1<<(pins.get(u)^pins.get(v))))return null}else if(pins.has(u)||pins.has(v)){let a=pins.has(u)?u:v,b=a===u?v:u;for(const d of colors(m))D.set(b,D.get(b)&~(1<<(pins.get(a)^d)))}}
  let W=[...D.keys()],F=E.filter(([u,v])=>D.has(u)&&D.has(v));
  if(!canDegree(W,F,D))return null;
  while(W.length){let v=W[0],chosen=false;for(const c of colors(D.get(v))){let DD=new Map(D);DD.delete(v);for(const [a,b,m] of F)if(a===v||b===v){let w=a===v?b:a;for(const d of colors(m))DD.set(w,DD.get(w)&~(1<<(c^d)))}let WW=W.slice(1),FF=F.filter(([a,b])=>a!==v&&b!==v);if(canDegree(WW,FF,DD)){x.set(v,c);W=WW;F=FF;D=DD;chosen=true;break}}A(chosen,"self reduction")}
  A(ok(E,x),"fixed source lift");return x
 }
 function reduce(V,E,Q){
  V=V.slice();E=canon(E);const keep=new Set(Q),records=[];let bad=false;
  while(true){
   C.reduceScans++;if(!closure(V,E)||E.some(e=>e[2]===15)){bad=true;break}
   const a=adj(V,E),P=V.filter(v=>!keep.has(v)),setP=new Set(P),IE=E.filter(([u,v])=>setP.has(u)&&setP.has(v));let moved=false;
   for(const v of P){const t=a.get(v);A(t.reduce((s,e)=>s+pop(e[1]),0)<=4,"private degree");if(t.length===2&&t.every(e=>pop(e[1])===2)){
    const [[u,p],[w,q]]=t;let allowed=0;for(const i of colors(15^p))for(const j of colors(15^q))allowed|=1<<(i^j);
    A(allowed===15||pop(allowed)===2,"line sumset");records.push({v,u,w,p,q});V=V.filter(x=>x!==v);E=canon(E.filter(([a,b])=>a!==v&&b!==v).concat([[u,w,15^allowed]]));C.doubleSteps++;moved=true;break
   }}if(moved)continue;
   for(const vv of components(P,IE)){const S=new Set(vv),ee=IE.filter(([u,v])=>S.has(u)&&S.has(v)),all=E.filter(([u,v])=>S.has(u)||S.has(v));const b=all.reduce((s,[u,v,m])=>s+(S.has(u)!==S.has(v)?pop(m):0),0);
    const slack=vv.some(v=>a.get(v).reduce((s,e)=>s+pop(e[1]),0)<4),triple=ee.some(e=>pop(e[2])===3),nonGDP=blockList(vv,ee).some(b=>!b.gdp);
    if(!b||slack||triple||nonGDP){
     if(!b&&!solveFixed(vv,ee,new Map())){bad=true;break}
     records.push({vv,all});V=V.filter(v=>!S.has(v));E=E.filter(([u,v])=>!S.has(u)&&!S.has(v));C.dropSteps++;moved=true;break
    }
    A(vv.length<=2*b-4,"boundary kernel inequality");
   }if(bad||!moved)break;
  }
  return {V,E,records,bad}
 }
 function lift(R,x,original){for(const rec of R.records.slice().reverse()){if("v" in rec){const {v,u,w,p,q}=rec;const c=[0,1,2,3].find(c=>!(p&(1<<(c^x.get(u))))&&!(q&(1<<(c^x.get(w)))));A(c!==undefined,"double reverse");x.set(v,c)}else{let s=new Set(rec.vv),outside=[...new Set(rec.all.flatMap(([a,b])=>[a,b]).filter(v=>!s.has(v)))];const pins=new Map(outside.map(v=>[v,x.get(v)]));A(outside.every(v=>x.has(v)),"reverse boundary");const y=solveFixed(rec.vv.concat(outside),rec.all,pins);A(y!==null,"drop reverse");for(const v of rec.vv)x.set(v,y.get(v))}}A(ok(original,x),"original lift");C.lifts++;return x}
 function brute(V,E,pins){let x=new Map(pins),W=V.filter(v=>!x.has(v)),a=adj(V,E);if(E.some(([u,v,m])=>x.has(u)&&x.has(v)&&(m&(1<<(x.get(u)^x.get(v))))))return false;
  function r(i){C.referenceNodes++;if(i===W.length)return true;let v=W[i];for(let c=0;c<4;c++)if(a.get(v).every(([w,m])=>!x.has(w)||!(m&(1<<(x.get(w)^c))))){x.set(v,c);if(r(i+1))return true;x.delete(v)}return false}return r(0)}
 function trial(V,E,Q,R,pins,expected,kind){let x=R.bad?null:solveFixed(R.V,R.E,pins);A(!!x===expected,"label "+kind);counts[kind][x?"sat":"unsat"]++;if(x)lift(R,x,E)}
 let seed=0xDA0905;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
 const seq=n=>Array.from({length:n},(_,i)=>i),scale=[];
 for(let j=0;j<100;j++){let n=3+rnd(5),V=seq(n),Q=V.slice(0,rnd(Math.min(n,3)+1)),E=[],deg=V.map(()=>0);for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(rnd(3)===0){let t=Math.min(1+rnd(3),4-deg[u],4-deg[v]);if(t>0){let m=0;while(pop(m)<t)m|=1<<rnd(4);E.push([u,v,m]);deg[u]+=t;deg[v]+=t}}let R=reduce(V,E,Q);for(let w=0;w<4**Q.length;w++){let p=new Map(Q.map((v,i)=>[v,(w>>(2*i))&3]));trial(V,E,Q,R,p,brute(V,E,p),"random")}}
 // Fano and all one-owner relaxations: DA07 affine star chart.
 const triples=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],owners=triples.flatMap(t=>[...([0,1].map(s=>({t,s})))]);
 let fanoModels=[];
 for(let omit=-1;omit<14;omit++){let os=owners.filter((_,i)=>i!==omit),V=seq(os.length*5),Q=[],E=[];os.forEach((o,i)=>{for(let j=1;j<=4;j++){Q.push(5*i+j);E.push([5*i,5*i+j,1])}});let R=reduce(V,E,Q),num=0;for(let z=0;z<128;z++){let pins=new Map();let good=true;os.forEach(({t,s},i)=>{pins.set(5*i+1,0);let any=false;t.forEach((v,j)=>{let lit=((z>>v)&1)^s;any||=!!lit;pins.set(5*i+2+j,(j+1)*(1-lit))});good&&=any});trial(V,E,Q,R,pins,good,"fano");if(good)num++}A(num===(omit<0?0:5),"Fano count");fanoModels.push(num)}
 // Double-bundle chains: same affine direction survives, differing direction dissolves.
 for(const n of [8,32,128,512])for(const mixed of [false,true]){let V=seq(n+2),Q=[0,n+1],E=seq(n+1).map(i=>[i,i+1,mixed&&i===n?5:3]);let R=reduce(V,E,Q);A(R.V.length===2,"chain size");let expectedMask=mixed?15:((n+1)%2?12:3);A((R.E.length?15^R.E[0][2]:15)===expectedMask,"chain relation");for(let x=0;x<4;x++)for(let y=0;y<4;y++)trial(V,E,Q,R,new Map([[0,x],[n+1,y]]),!!(expectedMask&(1<<(x^y))),"chain");scale.push({family:"double-chain",private:n,mixed,remaining:R.V.length-2,allowed:pop(expectedMask)})}
 // Sharp simple K4-chain boundary: b=2k+2, n=4k.
 for(const k of [1,2,4,8,16]){let E=[],Q=[],n=4*k;for(let i=0;i<k;i++)for(let u=0;u<4;u++)for(let v=u+1;v<4;v++)E.push([4*i+u,4*i+v,1]);for(let i=0;i<k-1;i++)E.push([4*i+3,4*(i+1),1]);let deg=seq(n).map(v=>E.filter(e=>e[0]===v||e[1]===v).length);for(let v=0;v<n;v++)if(deg[v]===3){let q=n+Q.length;Q.push(q);E.push([v,q,1])}let V=seq(n+Q.length),R=reduce(V,E,Q);A(R.V.length-Q.length===n&&Q.length===2*k+2,"sharp K4 kernel");let p=new Map(Q.map(v=>[v,rnd(4)]));let expected=n<=8?brute(V,E,p):!!solveFixed(V,E,p);trial(V,E,Q,R,p,expected,"k4");scale.push({family:"K4-chain",private:n,b:Q.length,remaining:n})}
 // Closed K5, one-edge deletion, four distinct parallel exclusions and triple root.
 for(const variant of ["K5","K5-minus","four","triple"]){let n=variant.startsWith("K5")?5:2,V=seq(n),E=[];if(n===5){for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if(variant!=="K5-minus"||u!==0||v!==1)E.push([u,v,1])}else E=[[0,1,variant==="four"?15:7]];let R=reduce(V,E,[]);trial(V,E,[],R,new Map(),brute(V,E,new Map()),"closed")}
 return {seed:"0xDA0905",counts,ledger:C,fanoModels,scale}
}
console.log(JSON.stringify(run(),null,2));
