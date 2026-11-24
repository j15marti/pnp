"use strict";
const main=function(){
"use strict";
let seed=20261124;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
const assert=(b,m)=>{if(!b)throw Error(m)},edge=(a,b)=>a<b?`${a},${b}`:`${b},${a}`,idx=(v,x)=>v.slice(1).reduce((s,b,i)=>s+((x[v[0]]^x[b])<<i),0),cost=(fs,x)=>fs.reduce((s,f)=>s+f.t[idx(f.v,x)],0);
const metrics={local_checks:0,table_entries:0,dual_calls:0,max_defects:0,pairing_states:0,cache_hits:0,expanded_keys:0,tree_edges:0,source_checks:0,brute_assignments:0,guard_checks:0,closure_deletions:0,closure_relations:0};
function compile(p,fs){
 let D=new Map(),EF=new Map(),c=0;p.faces.forEach((f,i)=>f.forEach((u,j)=>{let k=edge(u,f[(j+1)%f.length]);if(!EF.has(k))EF.set(k,[]);EF.get(k).push(i);D.set(k,0)}));for(const [k,f] of EF)assert(f.length===2,"face incidence "+k);
 const add=(a,b,d)=>{let k=edge(a,b);assert(D.has(k),"missing fill "+k);D.set(k,D.get(k)+d)};
 for(const f of fs){let v=f.v,t=f.t;assert(v.length<=3&&t.length===2**Math.max(0,v.length-1),"arity");c+=2*t[0];if(v.length===2)add(v[0],v[1],2*(t[1]-t[0]));if(v.length===3){let [a,b,d,e]=t;add(v[0],v[1],b+e-a-d);add(v[0],v[2],d+e-a-b);add(v[1],v[2],b+d-a-e)}}
 return {D,EF,c}
}
function dual(p,compiled,bits){
 let D=new Map(compiled.D),c=compiled.c,M=1+[...D.values()].reduce((s,d)=>s+Math.abs(d),0);
 for(let i=1;i<p.B.length;i++){let k=edge(p.B[0],p.B[i]),b=(bits>>(i-1))&1;assert(D.has(k),"boundary clique");D.set(k,D.get(k)+(b?-M:M));if(b)c+=M}
 let E=[...D.keys()].sort(),adj=Array.from({length:p.faces.length},()=>[]),defects=Array(p.faces.length).fill(0),pref=[],w=[];
 E.forEach((k,i)=>{let d=D.get(k),[a,b]=compiled.EF.get(k);pref[i]=+(d<0);w[i]=Math.abs(d);c+=Math.min(0,d);defects[a]^=pref[i];defects[b]^=pref[i];if(a!==b){adj[a].push([b,w[i],i]);adj[b].push([a,w[i],i])}});
 let T=defects.flatMap((b,i)=>b?[i]:[]);assert(T.length%2===0&&T.length<=22,"test pairing cap");metrics.dual_calls++;metrics.max_defects=Math.max(metrics.max_defects,T.length);
 const paths=T.map(s=>{let dist=Array(adj.length).fill(Infinity),prev=Array(adj.length).fill(null),done=new Set();dist[s]=0;for(let q=0;q<adj.length;q++){let u=-1;for(let i=0;i<adj.length;i++)if(!done.has(i)&&(u<0||dist[i]<dist[u]))u=i;if(u<0||!Number.isFinite(dist[u]))break;done.add(u);for(const [v,d,e] of adj[u])if(!done.has(v)&&dist[v]>dist[u]+d){dist[v]=dist[u]+d;prev[v]=[u,e]}}return {dist,prev}});
 let memo=new Map([[0,[0,-1,-1]]]);function match(mask){if(memo.has(mask))return memo.get(mask)[0];let i=0;while(!(mask&(1<<i)))i++;let val=Infinity,best=-1;for(let j=i+1;j<T.length;j++)if(mask&(1<<j)){let v=paths[i].dist[T[j]]+match(mask^(1<<i)^(1<<j));if(v<val){val=v;best=j}}memo.set(mask,[val,i,best]);return val}
 let mask=(1<<T.length)-1,mw=match(mask),sel=Array(E.length).fill(0);while(mask){let [,i,j]=memo.get(mask);assert(j>=0,"pairing");let v=T[j];while(v!==T[i]){let [u,e]=paths[i].prev[v];sel[e]^=1;v=u}mask^=(1<<i)^(1<<j)}metrics.pairing_states+=memo.size;
 let pa=new Map(p.V.map(v=>[v,[]]));E.forEach((k,i)=>{let [a,b]=k.split(",").map(Number),z=pref[i]^sel[i];pa.get(a).push([b,z]);pa.get(b).push([a,z])});let x={};for(const s of p.V)if(x[s]===undefined){x[s]=0;let q=[s];for(let i=0;i<q.length;i++)for(const [v,z] of pa.get(q[i])){let val=x[q[i]]^z;if(x[v]===undefined){x[v]=val;q.push(v)}else assert(x[v]===val,"cycle integration")}}
 assert(idx(p.B,x)===bits,"hard boundary");let actual=E.reduce((s,k,i)=>s+w[i]*sel[i],0);assert(actual===mw,"T join equality");return {x,value:(c+actual)/2}
}
function allFactors(p){return p.fs.concat(p.ch.flatMap(allFactors))}
function allVertices(p){return [...new Set(p.V.concat(p.ch.flatMap(allVertices)))].sort((a,b)=>a-b)}
function brute(fs,V,B=[],bits=0){let best=Infinity,xbest=null;for(let k=0;k<2**V.length;k++){let x={};V.forEach((v,i)=>x[v]=(k>>i)&1);if(idx(B,x)!==bits)continue;metrics.brute_assignments++;let c=cost(fs,x);if(c<best){best=c;xbest=x}}return {value:best,x:xbest}}
function close(fs,V){
 let rows=fs.map(f=>f.t.flatMap((c,i)=>c===0?[i]:[])),eq=new Map();
 function feasible(v,b){let a=new Map(V.map(x=>[x,[]]));for(const [k,z] of eq){let [i,j]=k.split(",").map(Number);a.get(i).push([j,z]);a.get(j).push([i,z])}for(let i=1;i<v.length;i++){let z=(b>>(i-1))&1;a.get(v[0]).push([v[i],z]);a.get(v[i]).push([v[0],z])}let x={};for(let s of V)if(x[s]===undefined){x[s]=0;let q=[s];for(let i=0;i<q.length;i++)for(let [u,z] of a.get(q[i])){let y=x[q[i]]^z;if(x[u]===undefined){x[u]=y;q.push(u)}else if(x[u]!==y)return false}}return true}
 let changed=true;while(changed){changed=false;for(let j=0;j<fs.length;j++){let v=fs[j].v,old=rows[j];rows[j]=old.filter(b=>feasible(v,b));if(rows[j].length<old.length){changed=true;metrics.closure_deletions+=old.length-rows[j].length}if(!rows[j].length)return false;
 for(let a=0;a<v.length;a++)for(let b=a+1;b<v.length;b++){let bit=(r,k)=>k===0?0:(r>>(k-1))&1,z=bit(rows[j][0],a)^bit(rows[j][0],b);if(rows[j].every(r=>(bit(r,a)^bit(r,b))===z)){let k=edge(v[a],v[b]);if(eq.has(k)){if(eq.get(k)!==z)return false}else{eq.set(k,z);changed=true;metrics.closure_relations++}}}}if(!feasible([],0))return false}return true
}
function solve(p,cache,checkLocal=false){
 const kids=p.ch.map(c=>solve(c,cache,checkLocal));metrics.tree_edges+=kids.length;const fs=p.fs.concat(kids.map((r,i)=>({v:p.ch[i].B,t:r.tab.map(e=>e.value)}))),compiled=compile(p,fs);
 const key=JSON.stringify([p.V,p.faces,p.B,compiled.c,[...compiled.D].sort()]);let tab=cache.get(key);
 if(tab)metrics.cache_hits++;else{metrics.expanded_keys++;tab=[];for(let b=0;b<2**Math.max(0,p.B.length-1);b++){let r=dual(p,compiled,b);assert(Number.isInteger(r.value)&&r.value===cost(fs,r.x),"table cost");if(checkLocal){let ref=brute(fs,p.V,p.B,b);assert(ref.value===r.value,"local min");metrics.local_checks++}tab.push(r);metrics.table_entries++}cache.set(key,tab)}
 return {tab,kids,p}
}
function lift(r,i=0,flip=0,x={}){let a=r.tab[i].x;for(let v of r.p.V){let z=a[v]^flip;if(x[v]!==undefined)assert(x[v]===z,"guard correlation");x[v]=z}r.kids.forEach(k=>{let B=k.p.B,b=idx(B,x),y=k.tab[b].x;lift(k,b,B.length?x[B[0]]^y[B[0]]:0,x)});return x}
function wheel(B,priv,L,fs=[],ch=[]){let V=[...B,...priv];assert(V.length===L+1,"wheel size");let h=V[0],r=V.slice(1),faces=r.map((v,i)=>[h,v,r[(i+1)%L]]);faces.push(r.slice().reverse());return {V,faces,B:B.slice(),fs,ch}}
function tri(B,fs=[],ch=[]){return {V:B.slice(),faces:[B.slice(),B.slice().reverse()],B:[],fs,ch}}
const nae=(v,sign=0)=>({v,t:Array.from({length:4},(_,k)=>{let x=[0,k&1,(k>>1)&1].map((a,i)=>a^((sign>>i)&1));return +(x[0]===x[1]&&x[1]===x[2])})});
function factor(v,mode){return {v,t:Array.from({length:2**Math.max(0,v.length-1)},()=>rnd(mode?5:2))}}
let random={cases:0,sat:0,unsat:0};
for(let it=0;it<160;it++){
 let root=tri([0,1,2],[factor([0,1,2],it%2)]),cur=root,next=3,depth=1+rnd(3);
 for(let j=0;j<depth;j++){let B=j===0?[0,1,2]:cur.faces[1].slice(),L=3+rnd(3),priv=Array.from({length:L-2},()=>next++),p=wheel(B,priv,L);p.fs=p.faces.slice(0,L).map(v=>it%3===0?nae(v,rnd(8)):factor(v,it%2));p.fs.push(factor(p.faces[0].slice(0,2),it%2));cur.ch.push(p);cur=p}
 let fs=allFactors(root),V=allVertices(root),cl=close(fs,V),cache=new Map(),res=solve(root,cache,true),x=lift(res),ref=brute(fs,V);assert(ref.value===res.tab[0].value&&cost(fs,x)===ref.value,"global min");assert(cl||ref.value>0,"closure");random.cases++;random[ref.value===0?"sat":"unsat"]++;metrics.source_checks++;
 let p=cur,v=p.faces[0].slice(0,2),old=p.fs.slice();for(let b=0;b<2;b++){p.fs=old.concat({v,t:b?[1,0]:[0,1]});let f=allFactors(root),cl2=close(f,V),r=solve(root,cache),xx=lift(r),rr=brute(f,V);assert(r.tab[0].value===rr.value&&cost(f,xx)===rr.value&&(cl2||rr.value>0),"guard");metrics.guard_checks++}p.fs=old
}
let tableControls=0;for(let mask=0;mask<16;mask++){let p=wheel([0,1,2],[3],3,[{v:[0,1,2],t:Array.from({length:4},(_,j)=>(mask>>j)&1)}]),r=solve(p,new Map(),true);assert(r.tab.every((a,i)=>a.value===((mask>>i)&1)),"relation");tableControls++}
let scaling=[];for(const t of [4,16,64,256,1024]){
 let root=tri([0,1,2]);for(let j=0;j<t;j++){let p=wheel([0,1,2],[3+j],3);p.fs=[nae([0,1,3+j]),nae([1,2,3+j]),nae([2,0,3+j])];root.ch.push(p)}
 root.fs=[{v:[0,1,2],t:[0,1,1,1]}];let cache=new Map(),before=metrics.dual_calls,ex0=metrics.expanded_keys,fs=allFactors(root),V=allVertices(root);assert(close(fs,V),"scale closure");let r=solve(root,cache),x=lift(r);assert(r.tab[0].value===0&&cost(fs,x)===0,"scale sat");let calls=metrics.dual_calls-before,keys=metrics.expanded_keys-ex0;
 root.fs.push({v:[0,1],t:[1,0]});let fs2=allFactors(root);assert(!close(fs2,V),"scale closure contradiction");before=metrics.dual_calls;let rr=solve(root,cache),xx=lift(rr);assert(rr.tab[0].value>0&&cost(fs2,xx)===rr.tab[0].value,"scale unsat");scaling.push({leaves:t,vertices:t+3,first_dual_calls:calls,first_keys:keys,changed_root_dual_calls:metrics.dual_calls-before,unsat_cost:rr.tab[0].value})
}
let F=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]],fano={base_models:0,neighbor_models:[],primal_edges:new Set(F.flatMap(v=>[edge(v[0],v[1]),edge(v[0],v[2]),edge(v[1],v[2])])).size};
for(let a=0;a<128;a++){let x=Object.fromEntries(Array.from({length:7},(_,i)=>[i,(a>>i)&1]));if(F.every(v=>cost([nae(v)],x)===0))fano.base_models++}
for(let i=0;i<7;i++)for(let b=0;b<2;b++){let n=0;for(let a=0;a<128;a++){let x=Object.fromEntries(Array.from({length:7},(_,j)=>[j,(a>>j)&1]));if(F.every((v,j)=>j===i?!v.every(u=>x[u]===b):cost([nae(v)],x)===0))n++}assert(n===5,"Fano neighbor");fano.neighbor_models.push(n)}assert(fano.base_models===0&&fano.primal_edges===21,"Fano");
let nonlocal=[];for(const t of [1,4,16,64,256]){
 let root=tri([0,1,2]);for(let j=0;j<t;j++){let z=3+j,p=wheel([0,1,2],[z],3);p.fs=[nae([0,1,z]),nae([1,2,z]),nae([2,0,z])];root.ch.push(p)}
 let p=root.ch[0];p.fs=[nae([0,1,2],0),nae([0,1,3],2),nae([0,2,3],6),nae([1,2,3],2)];let fs=allFactors(root),V=allVertices(root),cache=new Map();assert(close(fs,V),"nonlocal closure should stall");let before=metrics.dual_calls,r=solve(root,cache),x=lift(r);assert(r.tab[0].value===1&&cost(fs,x)===1,"nonlocal unsat");let calls=metrics.dual_calls-before;p.fs.shift();fs=allFactors(root);assert(close(fs,V),"neighbor closure");before=metrics.dual_calls;r=solve(root,cache);x=lift(r);assert(r.tab[0].value===0&&cost(fs,x)===0,"neighbor sat");nonlocal.push({leaves:t,vertices:t+3,closure_stalls:true,unsat_cost:1,unsat_dual_calls:calls,neighbor_dual_calls:metrics.dual_calls-before})
}
return {seed:20261124,random,tableControls,scaling,nonlocal,fano,metrics,discrepancies:0,backend:"supplied wheel embeddings; exact shortest paths + exponential small-terminal pairing DP; polynomial blossom backend not executed"}
};
console.log(JSON.stringify(main(),null,2));
