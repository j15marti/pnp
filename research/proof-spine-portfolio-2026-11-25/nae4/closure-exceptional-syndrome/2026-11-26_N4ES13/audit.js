function audit(){
let checks=0;const assert=(x)=>{checks++;if(!x)throw Error("assertion "+checks)};
const eq=[0,15],nae=[1,2,3,4,5,6];
function source(k,yes){let C=[],X=[];for(let b=0;b<2*k;b++){let o=9*b;for(let i=0;i<9;i++)X.push((i<3?0:i<6?1:i===8?1:0)^(b%2));for(let c=0;c<4;c++)for(let a=0;a<3;a++){let t=[];for(let i=0;i<3;i++)t.push(o+(c===0?3*a+i:3*i+(a+(c-1)*i)%3));C.push({c,t,b})}}
const sw=(a,b)=>{let t=C[a].t;[t[0],C[b].t[0]]=[C[b].t[0],t[0]]};
for(let i=0;i<k;i++){sw(24*i,24*i+12);if(yes||i>0)sw(24*i+1,24*i+13)}
for(let i=0;i<k-1;i++)sw(24*i+15,24*(i+1)+16);
return {C,X,n:18*k};}
function authenticate(S){const seen=new Set(),freq=Array.from({length:S.n},()=>[0,0,0,0]);for(const {c,t} of S.C){assert(new Set(t).size===3);for(const x of t)freq[x][c]++;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){const key=[t[i],t[j]].sort((a,b)=>a-b).join();assert(!seen.has(key));seen.add(key)}}assert(freq.every(f=>f.every(x=>x===1)))}
function graph(S){const nodes=[],ports=Array.from({length:S.n},()=>[]);for(let i=0;i<S.C.length;i++)S.C[i].t.forEach((v,j)=>ports[v].push(3*i+j));for(let b=0;b<S.n/9;b++){for(let i=0;i<9;i++)nodes.push({p:ports[9*b+i],r:eq});for(let i=0;i<12;i++){let v=12*b+i;nodes.push({p:[3*v,3*v+1,3*v+2],r:nae})}}return nodes}
function tuple(p,w){return p.reduce((s,e,i)=>s+(w[e]<<i),0)}
function verify(g,w){return w!==null&&g.every(v=>v.r.includes(tuple(v.p,w)))}
function exact(g,stats){const es=[...new Set(g.flatMap(v=>v.p))];function rec(d){stats.dpll++;let change=true;while(change){change=false;for(const v of g){const rows=v.r.filter(r=>v.p.every((e,i)=>d[e]&(1<<((r>>i)&1))));if(!rows.length)return null;for(let i=0;i<v.p.length;i++){const e=v.p[i],mask=rows.reduce((a,r)=>a|1<<((r>>i)&1),0),z=d[e]&mask;if(!z)return null;if(z!==d[e]){d[e]=z;change=true}}}}let e=es.find(e=>d[e]===3);if(e===undefined)return Object.fromEntries(es.map(e=>[e,d[e]===1?0:1]));for(let b=0;b<2;b++){let a={...d,[e]:1<<b},w=rec(a);if(w)return w}return null}return rec(Object.fromEntries(es.map(e=>[e,3])))}
function edges(g){let h=new Map();g.forEach((v,i)=>v.p.forEach(e=>{if(!h.has(e))h.set(e,[]);h.get(e).push(i)}));assert([...h.values()].every(a=>a.length===2));return [...h].map(([e,[a,b]])=>({e,a,b}))}
function find(g,stats){let E=edges(g),n=g.length;const conn=(set)=>{let start=set.values().next().value,seen=new Set([start]),q=[start];for(let i=0;i<q.length;i++)for(const {a,b} of E){let j=a===q[i]?b:b===q[i]?a:-1;if(set.has(j)&&!seen.has(j)){seen.add(j);q.push(j)}}return seen.size===set.size};function check(A){if(A.size<2||n-A.size<2)return null;const cut=E.filter(({a,b})=>A.has(a)!==A.has(b)).map(x=>x.e);if(cut.length<1||cut.length>4)return null;let B=new Set(Array.from({length:n},(_,i)=>i).filter(i=>!A.has(i)));if(!conn(A)||!conn(B))return null;return {A,B,cut}}
for(let i=2;i<=n-2;i++){stats.probes++;let c=check(new Set(Array.from({length:i},(_,j)=>j)));if(c)return c}
return null; // prefix discovery only; exact DPLL fallback, not production exhaustive cut acquisition
}
function solve(g,stats){stats.calls++;let z=find(g,stats);if(!z)return exact(g,stats);let {A,B,cut}=z;if(A.size>B.size)[A,B]=[B,A];stats.cuts[cut.length]=(stats.cuts[cut.length]||0)+1;let a=g.filter((_,i)=>A.has(i)),b=g.filter((_,i)=>B.has(i)),M=(1<<cut.length)-1,models=new Map(),rows=[];for(let r=0;r<=M;r++){if(r>(r^M))continue;let w=solve([{p:cut,r:[r,r^M]},...a],stats);if(w){assert(verify(a,w));let t=tuple(cut,w);assert(t===r||t===(r^M));models.set(r,w);rows.push(r,r^M)}}if(!rows.length)return null;let w=solve([{p:cut,r:rows},...b],stats);if(!w)return null;let t=tuple(cut,w),r=Math.min(t,t^M),u=models.get(r);assert(!!u);let flip=tuple(cut,u)!==t;let merged={...w};for(let [e,v] of Object.entries(u)){let bit=v^Number(flip);if(e in merged)assert(merged[e]===bit);merged[e]=bit}assert(verify(g,merged));return merged}
const stats=()=>({calls:0,dpll:0,probes:0,cuts:{}});
let cases=[];
for(let k of [1,2,4,8,16])for(let yes of [true,false]){let S=source(k,yes);authenticate(S);let G=graph(S);if(yes)assert(S.C.every(({t})=>new Set(t.map(x=>S.X[x])).size===2));else{let C=S.C.filter(x=>x.b===0&&x.t.every(v=>v<9));assert(C.length===11);for(let x=0;x<512;x++)assert(!C.every(({t})=>new Set(t.map(i=>(x>>i)&1)).size===2))}
let st=stats(),w=solve(G,st);assert((w!==null)===yes);if(w)assert(verify(G,w));cases.push({k,yes,n:S.n,clauses:S.C.length,...st})}
let synthetic=[];for(let k of [3,4])for(let j=0;j<12;j++){let G=Array.from({length:2*k},()=>({p:[],r:[]})),e=0;for(let h=0;h<2;h++)for(let a=0;a<k;a++)for(let b=a+1;b<k;b++){G[h*k+a].p.push(e);G[h*k+b].p.push(e++)}for(let a=0;a<k;a++){G[a].p.push(e);G[k+a].p.push(e++)}for(let i=0;i<G.length;i++){let m=(1<<k)-1;for(let r=0;r<=m;r++)if(r<(r^m)&&((r*13+i*7+j*11)%17)<(j%3===0?4:12))G[i].r.push(r,r^m)}let st=stats(),w=solve(G,st),v=exact(G,stats());assert(!!w===!!v);if(w)assert(verify(G,w));synthetic.push({k,j,sat:!!w,...st})}
let recurrence=0;for(let a=2;a<=100;a++)for(let b=a;b<=100;b++){let u=BigInt(a-1),v=BigInt(b-1);assert(8n*u**4n+v**4n<=(u+v)**4n-1n);assert(16n*u**5n+v**5n<=(u+v)**5n-1n);recurrence+=2}
let cap=[];for(let k of [3,4]){let q=1<<(k-1),affine=0;for(let mask=0;mask<(1<<q);mask++){let S=Array.from({length:q},(_,i)=>i).filter(i=>(mask>>i)&1);let A=S.every(a=>S.every(b=>S.every(c=>S.includes(a^b^c))));if(A)affine++;}cap.push({arity:k,tables:1<<q,affine})}
return {checks,cases,synthetic,recurrence,cap,limits:"prefix cuts only, exact DPLL fallback; no general prime polynomial claim; synthetic comparisons use same exact leaf engine, not an independent solver"}}
console.log(JSON.stringify(audit(),null,2));
