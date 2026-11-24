'use strict';
function runS07(){
let seed=20261124;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
const S={seed:20261124,networks:0,decisions:0,sat:0,unsat:0,unknown:0,referenceTuples:0,closureDeletes:0,flowAugmentations:0,cycleWitnesses:0,rankChecks:0,verifiedLifts:0,scaling:[],hostile:[]};
const basis=()=>{const a=new Map();return {add(v){while(v){const i=31-Math.clz32(v);if(a.has(i))v^=a.get(i);else{a.set(i,v);return true}}return false},reduce(v){for(const i of [...a.keys()].sort((x,y)=>y-x))if((v>>>i)&1)v^=a.get(i);return v},rank(){return a.size}}};
const sum=(a,b)=>a.map((x,i)=>x+b[i]), row=(c,t)=>({c,t});
function brute(rows,K){let out=new Set();function rec(i,c,t){if(i===rows.length){S.referenceTuples++;if(c.every((x,j)=>x<=K[j]))out.add(t);return}for(const r of rows[i])rec(i+1,sum(c,r.c),t^r.t)}rec(0,K.map(()=>0),0);return out}
function solve(original,K,d,target){
const H=K.length,R=H,zero=()=>K.map(()=>0),rows=original.map(a=>a.map((r,id)=>({...r,id})));
while(true){
if(rows.some(a=>!a.length))return {kind:"UNSAT",why:"closure empty"};
const mins=rows.map(a=>K.map((_,i)=>Math.min(...a.map(r=>r.c[i])))),tot=mins.reduce(sum,zero());
if(tot.some((x,i)=>x>K[i]))return {kind:"UNSAT",why:"min budget"};
let changed=false;
outer:for(let b=0;b<rows.length;b++)for(let j=0;j<rows[b].length;j++){
const r=rows[b][j];let bad=r.c.some((x,i)=>x+tot[i]-mins[b][i]>K[i]);
if(!bad){const A=basis();let t=r.t;for(let z=0;z<rows.length;z++)if(z!==b){t^=rows[z][0].t;for(const a of rows[z])A.add(a.t^rows[z][0].t)}bad=A.reduce(t^target)!==0}
if(bad){rows[b].splice(j,1);S.closureDeletes++;changed=true;break outer}}
if(!changed)break;
}
let base=zero(),tag0=0,n=H+1,E=[],groups=new Map(),fixed=[],good=[];
function edge(u,v,cap,t,meta=null){E.push({u,v,cap,t,meta,f:0})}
for(let b=0;b<rows.length;b++){const a=rows[b];
if(a.length===1){base=sum(base,a[0].c);tag0^=a[0].t;fixed.push([b,a[0].id]);continue}
if(a.length===2){const D=a[1].c.map((x,i)=>(x-a[0].c[i])/d[i]),p=D.flatMap((x,i)=>x===1?[i]:[]),m=D.flatMap((x,i)=>x===-1?[i]:[]);
if(D.every(x=>x===0||x===1||x===-1)&&p.length<=1&&m.length<=1){base=sum(base,a[0].c);tag0^=a[0].t;const u=m[0]??R,v=p[0]??R,t=a[0].t^a[1].t,key=[u,v,t].join(",");if(!groups.has(key))groups.set(key,{u,v,t,items:[]});groups.get(key).items.push([b,a[0].id,a[1].id]);continue}}
const m=K.map((_,i)=>Math.min(...a.map(r=>r.c[i])));base=sum(base,m);
const cats=a.map(r=>{const D=r.c.map((x,i)=>(x-m[i])/d[i]),p=D.flatMap((x,i)=>x===1?[i]:[]);return D.every(x=>x===0||x===1)&&p.length<=1?(p[0]??R):-1});
if(cats.includes(-1))return {kind:"UNKNOWN",why:"recognition"};const node=n++;good.push(node);a.forEach((r,i)=>edge(node,cats[i],1,r.t,{row:[b,r.id]}));
}
for(const g of groups.values())edge(g.u,g.v,g.items.length,g.t,{items:g.items});
const U=K.map((x,i)=>Math.floor((x-base[i])/d[i])),b=Array(n).fill(0);
for(let i=0;i<H;i++){b[i]=U[i];edge(R,i,Math.max(0,U[i]+rows.length),0)}
for(const v of good)b[v]=-1;b[R]=good.length-U.reduce((x,y)=>x+y,0);
function residual(){const a=Array.from({length:n+2},()=>[]);E.forEach((e,i)=>{if(e.f<e.cap)a[e.u].push({u:e.u,v:e.v,i,s:1,t:e.t,cap:e.cap-e.f});if(e.f>0)a[e.v].push({u:e.v,v:e.u,i,s:-1,t:e.t,cap:e.f})});return a}
function path(a,s,t,allow=null){if(s===t)return [];const p=new Map([[s,null]]),Q=[s];for(let h=0;h<Q.length;h++)for(const e of a[Q[h]])if((!allow||allow.has(e.v))&&!p.has(e.v)){p.set(e.v,e);Q.push(e.v);if(e.v===t){let w=[],v=t;while(v!==s){const z=p.get(v);w.push(z);v=z.u}return w.reverse()}}return null}
const orig=E.length;let need=0;b.forEach((v,i)=>{if(v<0)edge(n,i,-v,0);if(v>0){edge(i,n+1,v,0);need+=v}});
let got=0;while(got<need){const p=path(residual(),n,n+1);if(!p)return {kind:"UNSAT",why:"flow cut"};const f=Math.min(...p.map(e=>e.cap));for(const e of p)E[e.i].f+=e.s*f;got+=f;S.flowAugmentations++}E=E.slice(0,orig);
const a=residual(),left=new Set(Array.from({length:n},(_,i)=>i)),comps=[];
while(left.size){const r=left.values().next().value,vs=new Set([...left].filter(v=>path(a,r,v)!==null&&path(a,v,r)!==null));for(const v of vs)left.delete(v);const C=[],A=basis();
function walk(w){if(!w.length)return;let V=[w[0].u],st=[];for(const e of w){const k=V.indexOf(e.v);if(k<0){st.push(e);V.push(e.v)}else{const c=[...st.slice(k),e],t=c.reduce((z,x)=>z^x.t,0);if(A.add(t)){C.push({c,t});S.cycleWitnesses++}st=st.slice(0,k);V=V.slice(0,k+1)}}if(st.length)throw Error("not closed")}
const from=new Map(),to=new Map();for(const v of vs){from.set(v,path(a,r,v,vs));to.set(v,path(a,v,r,vs));walk([...from.get(v),...to.get(v)])}for(const u of vs)for(const e of a[u])if(vs.has(e.v))walk([...from.get(u),e,...to.get(e.v)]);if(C.length)comps.push(C);
}
const delta=E.reduce((t,e)=>t^((e.f%2)?e.t:0),tag0)^target,all=basis();for(const C of comps)for(const c of C)all.add(c.t);
if(all.reduce(delta))return {kind:"UNSAT",why:"cycle hull",rank:all.rank()};
const W=basis(),todo=comps.slice(),chosen=[];let progress=true;
while(progress){progress=false;for(let i=0;i<todo.length;i++){const C=todo[i],A=basis();for(const c of C)A.add(W.reduce(c.t));S.rankChecks++;if(A.rank()<=1){const c=C.find(c=>W.reduce(c.t)!==0);if(c){W.add(c.t);chosen.push(c)}todo.splice(i,1);progress=true;break}}}
if(W.reduce(delta))return {kind:"UNKNOWN",why:"nonaffine SCC",rank:all.rank(),peeled:W.rank()};
const A=new Map();chosen.forEach((c,i)=>{let v=c.t,m=1n<<BigInt(i);while(v){const p=31-Math.clz32(v);if(A.has(p)){const a=A.get(p);v^=a.v;m^=a.m}else{A.set(p,{v,m});break}}});let v=delta,mask=0n;while(v){const p=31-Math.clz32(v),a=A.get(p);if(!a)throw Error("bad lift");v^=a.v;mask^=a.m}chosen.forEach((c,i)=>{if((mask>>BigInt(i))&1n)for(const e of c.c)E[e.i].f+=e.s});
const wit=Array(rows.length).fill(-1);for(const [b,id] of fixed)wit[b]=id;for(const e of E){if(e.f<0||e.f>e.cap)throw Error("capacity");if(e.meta?.row&&e.f){const [b,id]=e.meta.row;if(wit[b]!==-1)throw Error("duplicate");wit[b]=id}if(e.meta?.items)e.meta.items.forEach(([b,off,on],i)=>wit[b]=i<e.f?on:off)}if(wit.includes(-1))throw Error("missing");
let cost=zero(),t=0;wit.forEach((id,i)=>{const r=original[i][id];cost=sum(cost,r.c);t^=r.t});if(cost.some((x,i)=>x>K[i])||t!==target)throw Error("invalid lift");S.verifiedLifts++;return {kind:"SAT",rank:all.rank(),peeled:W.rank(),groups:groups.size,arcs:E.length};
}
for(let z=0;z<240;z++){const h=2+rnd(4),q=z%3===0?1:3,d=Array.from({length:h},()=>1+rnd(4)),rows=[],B=2+rnd(6);
for(let b=0;b<B;b++){const base=d.map(()=>rnd(3)),a=[];for(let i=0,L=rnd(2)?2:3+rnd(2);i<L;i++){const v=rnd(h+1),c=base.slice();if(v<h)c[v]+=d[v];a.push(row(c,rnd(1<<q)))}rows.push(a)}
const K=rows.reduce((s,a)=>sum(s,a[rnd(a.length)].c),d.map(()=>0)).map(x=>Math.max(0,x+rnd(5)-2)),ref=brute(rows,K);S.networks++;
for(let t=0;t<(1<<q);t++){const out=solve(rows,K,d,t);S.decisions++;if(ref.has(t))S.sat++;else S.unsat++;if(out.kind==="UNKNOWN"){S.unknown++;if(q===1)throw Error("one bit unknown")}else if((out.kind==="SAT")!==ref.has(t))throw Error("wrong decision "+JSON.stringify({rows,K,d,t,out}))}}
for(const k of [1,2,4,8,16,24]){const h=3*k,d=Array(h).fill(1),K=d.slice(),rows=[];for(let j=0;j<k;j++)for(let a=0;a<3;a++){const c=Array(h).fill(0),e=c.slice();c[3*j+a]=1;e[3*j+(a+1)%3]=1;rows.push([row(c,0),row(e,1<<j)])}
const yes=solve(rows,K,d,(1<<k)-1),no=solve(rows,K,d,1<<k);if(yes.kind!=="SAT"||yes.rank!==k||no.kind!=="UNSAT")throw Error("scaling "+JSON.stringify({k,yes,no}));S.scaling.push({k,blocks:rows.length,...yes,unsat:no.kind})}
const r=[[row([0,0,0],0),row([1,0,0],1),row([0,1,0],2)]];
// For this one-block control affine pinning alone rejects; use two independent 3-state tables with a shared owner capacity.
const hostile=solve(r,[1,1,1],[1,1,1],3);if(hostile.kind!=="UNSAT"||brute(r,[1,1,1]).has(3))throw Error("control");S.hostile.push({case:"single three-state mask",...hostile});
const r2=Array.from({length:9},()=>[row([1,0],0),row([0,1],1)]);for(let t=0;t<2;t++){const out=solve(r2,[4,5],[1,1],t);if(out.kind!==(t===1?"SAT":"UNSAT"))throw Error("count control");S.hostile.push({case:"nine identical transfers, exactly five on",target:t,...out})}
return S;
}
console.log(JSON.stringify(runS07(),null,2));
