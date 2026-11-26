// P3CC09 finite audit. Node.js; local exhaustive oracle used ONLY on bounded blocks.
function run(){
let checks=0;const ok=(b,m="")=>{checks++;if(!b)throw Error("check "+checks+" "+m)};
const base="000 012 010 110 111 221 333 332 002 100 103 223".split(" ").map(s=>[...s].map(Number));
const rows=(T,n)=>Array.from({length:3*n},(_,r)=>T.flatMap((t,e)=>t[Math.floor(r/n)]===r%n?[e]:[]));
const cover=(T,n,x,del=[])=>del.every(e=>x[e]===0)&&rows(T,n).every(r=>r.reduce((s,e)=>s+x[e],0)===1);
const br=rows(base,4),S=[];for(let m=0;m<4096;m++){const x=Array.from({length:12},(_,e)=>(m>>e)&1);if(cover(base,4,x))S.push(x);}ok(S.length===4);
const sig=base.map((_,e)=>S.map(x=>x[e]).join(""));const cls=new Map(),lit=sig.map(s=>{const c=s.replace(/[01]/g,b=>b==="0"?"1":"0"),k=s<c?s:c;if(!cls.has(k))cls.set(k,cls.size+1);return (s===k?1:-1)*cls.get(k);});ok(cls.size===5);
const value=(l,x)=>x.get(Math.abs(l))^Number(l<0);
function normalize(rs,pins){let rr=rs.map(r=>r.slice()),p=new Map(pins);while(true){let change=false,seen=new Set(),next=[];function pin(v,a){if(p.has(v))return p.get(v)===a;p.set(v,a);change=true;return true;}
for(const r of rr){let c=0,f=[];for(const l of r){if(p.has(Math.abs(l)))c+=value(l,p);else f.push(l);}if(c>1)return null;
if(c===1){for(const l of f)if(!pin(Math.abs(l),Number(l<0)))return null;continue;}
const cnt=new Map();for(const l of f)cnt.set(l,(cnt.get(l)||0)+1);
const both=[...cnt.keys()].filter(l=>l>0&&cnt.has(-l));if(both.length>1)return null;
if([...cnt.values()].some(c=>c>1)){for(const [l,c] of cnt)if(c>1&&!pin(Math.abs(l),Number(l<0)))return null;next.push(f);continue;}
if(both.length===1){for(const l of f)if(Math.abs(l)!==both[0]&&!pin(Math.abs(l),Number(l<0)))return null;continue;}
if(!f.length)return null;if(f.length===1){if(!pin(Math.abs(f[0]),Number(f[0]>0)))return null;continue;}
f.sort((a,b)=>a-b);const key=f.join(",");if(!seen.has(key)){seen.add(key);next.push(f);}}
rr=next;if(!change)return {rr,p};}}
// Tarjan edge blocks, then exact binary block-cut messages. Local brute is audit only.
function solve(rr){
const vs=[...new Set(rr.flat().map(Math.abs))],rN=rr.length,pos=new Map(vs.map((v,i)=>[v,rN+i])),n=rN+vs.length,E=[],G=Array.from({length:n},()=>[]);
rr.forEach((r,i)=>r.forEach(l=>{const j=pos.get(Math.abs(l)),e=E.length;E.push([i,j,l]);G[i].push([j,e]);G[j].push([i,e]);}));
const d=Array(n).fill(-1),low=[],stk=[],B=[];let time=0;
function dfs(v,pa){d[v]=low[v]=time++;for(const [u,e] of G[v])if(e!==pa){if(d[u]<0){stk.push(e);dfs(u,e);low[v]=Math.min(low[v],low[u]);if(low[u]>=d[v]){const b=[];let f;do{f=stk.pop();b.push(f);}while(f!==e);B.push(b);}}else if(d[u]<d[v]){stk.push(e);low[v]=Math.min(low[v],d[u]);}}}
for(let i=0;i<n;i++)if(d[i]<0)dfs(i,-1);
const M=Array.from({length:n},()=>[]),D=B.map((es,b)=>{const R=new Map(),V=new Map();for(const e of es){const [r,v,l]=E[e];if(!R.has(r))R.set(r,[]);R.get(r).push(l);V.set(v,(V.get(v)||0)+1);}for(const v of [...R.keys(),...V.keys()])M[v].push(b);return {R,V};});
let queries=0,maxVars=0;const seen=new Set();
function art(v,parent){const kids=M[v].filter(b=>b!==parent).map(b=>block(b,v)),out=new Map();for(const a of [0,1]){if(v>=rN){if(kids.every(t=>t.has(a)))out.set(a,kids.map(t=>t.get(a)));}else if(a===1){if(kids.every(t=>t.has(0)))out.set(a,kids.map(t=>t.get(0)));}else{const i=kids.findIndex((t,i)=>t.has(1)&&kids.every((u,j)=>j===i||u.has(0)));if(i>=0)out.set(a,kids.map((t,j)=>t.get(Number(j===i))));}}return out;}
function block(b,parent=-1){seen.add(b);const {R,V}=D[b],child=new Map();for(const v of [...R.keys(),...V.keys()])if(M[v].length>1&&v!==parent)child.set(v,art(v,b));const out=new Map(),vars=[...V.keys()];maxVars=Math.max(maxVars,vars.length);ok(vars.length<=12,"bounded audit block");
for(const a of parent<0?[0]:[0,1]){queries++;for(let mask=0;mask<2**vars.length;mask++){const x=new Map(vars.map((v,i)=>[vs[v-rN],(mask>>i)&1]));const val=v=>v>=rN?x.get(vs[v-rN]):R.get(v).reduce((s,l)=>s+value(l,x),0);
if(parent>=0&&val(parent)!==a)continue;if([...R.keys()].some(r=>M[r].length===1&&val(r)!==1))continue;if([...child].some(([v,t])=>!t.has(val(v))))continue;
out.set(a,{x,kids:[...child].flatMap(([v,t])=>t.get(val(v)))});break;}}return out;}
const x=new Map();function lift(w){for(const [v,a] of w.x){ok(!x.has(v)||x.get(v)===a);x.set(v,a);}for(const w2 of w.kids)lift(w2);}
let yes=true;for(let b=0;b<B.length;b++)if(!seen.has(b)){const s=block(b);if(!s.has(0)){yes=false;break;}lift(s.get(0));}
if(yes)ok(rr.every(r=>r.reduce((s,l)=>s+value(l,x),0)===1));
return {yes,x,globalHigh:vs.filter(v=>G[pos.get(v)].length>2).length,maxBlockHigh:Math.max(0,...D.map(d=>[...d.V.values()].filter(a=>a>2).length)),blocks:B.length,queries,maxVars};
}
function family(k,kind,del=[]){
const T=Array.from({length:k},(_,i)=>base.map(t=>t.map(v=>v+4*i))).flat(),swaps=[];
for(let i=0;i<k-1;i++){const c=kind==="chain"?1:2,a=12*i+(kind==="chain"?7:i%2?6:7),b=12*(i+1)+(kind==="chain"?0:i%2?6:7);[T[a][c],T[b][c]]=[T[b][c],T[a][c]];swaps.push([a,b,c]);}
ok(new Set(T.map(t=>t.join(","))).size===T.length);
const N=5*k,par=Array.from({length:N+1},(_,i)=>i),flip=Array(N+1).fill(0);
function find(v){if(par[v]===v)return [v,0];const [r,f]=find(par[v]);flip[v]^=f;par[v]=r;return [r,flip[v]];}
function raw(e){return Math.sign(lit[e%12])*(Math.abs(lit[e%12])+5*Math.floor(e/12));}
function join(a,b){const [r,f]=find(Math.abs(a)),[s,g]=find(Math.abs(b)),h=f^g^Number(a<0)^Number(b<0);if(r===s){ok(!h);return;}par[s]=r;flip[s]=h;}
for(let i=0;i<swaps.length;i++){const [a,b,c]=swaps[i],cross=T.flatMap((t,e)=>Number(e<12*(i+1))!==Number(t[c]<4*(i+1))?[e]:[]);ok(cross.length===2&&cross.includes(a)&&cross.includes(b));join(raw(a),raw(b));}
const map=T.map((_,e)=>{const a=raw(e),[r,f]=find(Math.abs(a));return (f^Number(a<0)?-1:1)*r;});
const p=new Map(),sr=rows(T,4*k);let contradiction=false,native=Array(T.length).fill(-1);
for(const e of del)native[e]=0;let change=true;while(change&&!contradiction){change=false;for(const r of sr){const one=r.filter(e=>native[e]===1),free=r.filter(e=>native[e]<0);if(one.length>1||!one.length&&!free.length){contradiction=true;break;}if(one.length){for(const e of free){native[e]=0;change=true;}}else if(free.length===1){native[free[0]]=1;change=true;}}}
const nativeNo=contradiction;
for(let e=0;e<native.length;e++)if(native[e]>=0){const l=map[e],v=Math.abs(l),a=native[e]^Number(l<0);if(p.has(v)&&p.get(v)!==a)contradiction=true;p.set(v,a);}
const rs=Array.from({length:k},(_,i)=>br.map(r=>r.map(e=>map[12*i+e]))).flat(),norm=contradiction?null:normalize(rs,p);
const s=norm?solve(norm.rr):{yes:false,globalHigh:0,maxBlockHigh:0,blocks:0,queries:0,maxVars:0};
let witness=null;if(s.yes){const val=new Map([...norm.p,...s.x]);const x=map.map(l=>(val.get(Math.abs(l))??0)^Number(l<0));ok(cover(T,4*k,x,del),"source lift");witness=x.flatMap((b,e)=>b?[e]:[]);}
const {x,...stats}=s;return {kind,k,triples:T.length-del.length,deleted:del,nativeNo,...stats,witness};
}
const families=[],neighbors=[];
for(const kind of ["chain","shared"]){for(const k of [1,2,4,8,16,32,64]){const s=family(k,kind);ok(s.yes,kind);families.push(s);if(k>=2){const plus=kind==="chain"?[1,2,8]:[6],minus=kind==="chain"?[...plus,12*(k-1)+11]:[...plus,12*(k-1)+7];const p=family(k,kind,plus),q=family(k,kind,minus);ok(p.yes&& !q.yes,kind+" neighbor");neighbors.push({p,q});}}}
// independent arbitrary signed quotient tests; finite seed, no unbounded random loops
let seed=261125;function rand(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n;}
for(let j=0;j<250;j++){const n=1+rand(7),m=1+rand(8),rs=Array.from({length:m},()=>{const l=[];for(let v=1;v<=n;v++)if(rand(3)===0)l.push(rand(2)?v:-v);if(!l.length)l.push(1+rand(n));return l;});let ref=false;for(let k=0;k<2**n;k++){let x=new Map(Array.from({length:n},(_,i)=>[i+1,(k>>i)&1]));if(rs.every(r=>r.reduce((s,l)=>s+value(l,x),0)===1)){ref=true;break;}}
const a=normalize(rs,new Map()),s=a?solve(a.rr):{yes:false};ok(s.yes===ref,"random");}

// Blind acquisition of balanced, oppositely directed, same-color 2-edge splices.
// Source row labels are preserved, no known target phase or block index used.
function blind(T,n,deleted=[]){
 const m=T.length,U=T.map(t=>t.map((a,c)=>a+c*n)),allR=Array.from({length:3*n},(_,r)=>r),seams=[],pieces=[];let attempts=0;
 function split(ids,rr){
 const R=new Set(rr),G=new Map([...ids.map(e=>[e+m,[]])]); // use disjoint keys: rows negative, triples positive
 const g=new Map();for(const r of rr)g.set(-r-1,[]);for(const e of ids)g.set(e,[]);
 const es=[];for(const e of ids)for(let c=0;c<3;c++){const r=U[e][c];ok(R.has(r));let i=es.length;es.push([e,r,c]);g.get(e).push([-r-1,i]);g.get(-r-1).push([e,i]);}
 function reach(start,i=-1,j=-1){const s=new Set([start]),q=[start];for(let h=0;h<q.length;h++)for(const [v,e] of g.get(q[h]))if(e!==i&&e!==j&&!s.has(v)){s.add(v);q.push(v);}return s;}
 const con=reach(ids[0]);if(con.size!==ids.length+rr.length){const a=ids.filter(e=>con.has(e)),b=rr.filter(r=>con.has(-r-1));split(a,b);split(ids.filter(e=>!con.has(e)),rr.filter(r=>!con.has(-r-1)));return;}
 for(let i=0;i<es.length;i++){const [e,r,c]=es[i];for(let j=i+1;j<es.length;j++){const [f,s,d]=es[j];if(c!==d||e===f||r===s)continue;attempts++;
 const A=reach(e,i,j);if(A.has(-r-1)||A.has(f)||!A.has(-s-1))continue;
 const a=ids.filter(v=>A.has(v)),b=rr.filter(v=>A.has(-v-1)),cnt=[0,0,0];b.forEach(r=>cnt[Math.floor(r/n)]++);
 if(cnt[0]!==cnt[1]||cnt[1]!==cnt[2])continue;
 // each side retains an original triple node and all its three rewired incidences.
 U[e][c]=s;U[f][c]=r;seams.push([e,f,c]);split(a,b);split(ids.filter(v=>!A.has(v)),rr.filter(v=>!A.has(-v-1)));return;
 }}
 pieces.push({ids,rr});
 }
 split(Array.from({length:m},(_,e)=>e),allR);
 // Every bounded atom is exactly inspected; larger atoms retain unmerged source IDs.
 const par=Array.from({length:m},(_,e)=>e),flip=Array(m).fill(0);
 function find(e){if(par[e]===e)return [e,0];const [r,f]=find(par[e]);flip[e]^=f;par[e]=r;return [r,flip[e]];}
 function join(e,f,d){const [a,b]=find(e),[c,h]=find(f);if(a===c)return (b^h)===d;par[c]=a;flip[c]=b^h^d;return true;}
 for(const [e,f] of seams)if(!join(e,f,0))return {yes:false,seams:seams.length,attempts};
 let impossible=false,forced=[];
 for(const {ids,rr} of pieces){if(ids.length>12)continue;const R=rr.map(r=>ids.filter(e=>U[e].includes(r))),S=[];
 for(let k=0;k<2**ids.length;k++){const b=ids.map((_,i)=>(k>>i)&1);if(R.every(r=>r.reduce((s,e)=>s+b[ids.indexOf(e)],0)===1))S.push(b);}
 if(!S.length){impossible=true;break;}const by=new Map();ids.forEach((e,i)=>{const s=S.map(b=>b[i]).join(""),c=s.replace(/[01]/g,b=>b==="0"?"1":"0");if(!s.includes("0")||!s.includes("1"))forced.push([e,Number(s[0])]);const k=s<c?s:c,d=Number(s!==k);if(by.has(k)){const [f,h]=by.get(k);if(!join(e,f,d^h))impossible=true;}else by.set(k,[e,d]);});}
 if(impossible)return {yes:false,seams:seams.length,attempts};
 const map=T.map((_,e)=>{const [r,f]=find(e);return (f?-1:1)*(r+1);}),p=new Map();
 // Original exact-one closure under source deletion guards.
 const x=Array(m).fill(-1);for(const e of deleted)x[e]=0;
 const sr=rows(T,n);let ch=true;while(ch&&!impossible){ch=false;for(const r of sr){const o=r.filter(e=>x[e]===1),f=r.filter(e=>x[e]<0);if(o.length>1||!o.length&&!f.length){impossible=true;break;}if(o.length){for(const e of f){x[e]=0;ch=true;}}else if(f.length===1){x[f[0]]=1;ch=true;}}}
 for(let e=0;e<m;e++)if(x[e]>=0)forced.push([e,x[e]]);
 for(const [e,a] of forced){const l=map[e],v=Math.abs(l),b=a^Number(l<0);if(p.has(v)&&p.get(v)!==b)impossible=true;p.set(v,b);}
 const R=Array.from({length:3*n},(_,r)=>T.flatMap((_,e)=>U[e].includes(r)?[map[e]]:[]));
 const norm=impossible?null:normalize(R,p),s=norm?solve(norm.rr):{yes:false,blocks:0,maxBlockHigh:0,globalHigh:0,queries:0,maxVars:0};let witness=null;
 if(s.yes){const a=new Map([...norm.p,...s.x]);const y=map.map(l=>(a.get(Math.abs(l))??0)^Number(l<0));ok(cover(T,n,y,deleted));witness=y.flatMap((b,e)=>b?[e]:[]);}
 const {x:unused,...stats}=s;return {...stats,seams:seams.length,attempts,pieceSizes:pieces.map(p=>p.ids.length),witness};
}
const blindTests=[];
for(const kind of ["chain","shared"])for(const k of [1,2,4,8,16]){
 const T=Array.from({length:k},(_,i)=>base.map(t=>t.map(v=>v+4*i))).flat();
 for(let i=0;i<k-1;i++){const c=kind==="chain"?1:2,a=12*i+(kind==="chain"?7:i%2?6:7),b=12*(i+1)+(kind==="chain"?0:i%2?6:7);[T[a][c],T[b][c]]=[T[b][c],T[a][c]];}
 // Deterministic reordering of original tuple IDs, with guard translation.
 const order=T.map((_,i)=>i).reverse(),R=order.map(i=>T[i]);const a=blind(R,4*k);ok(a.yes);
 let neg=null;if(k>=2){const del=kind==="chain"?[1,2,8,12*(k-1)+11]:[6,12*(k-1)+7];neg=blind(R,4*k,del.map(i=>order.indexOf(i)));ok(!neg.yes);}
 blindTests.push({kind,k,positive:a,negative:neg});
}

return {blindTests,checks,baseCovers:S.map(x=>x.flatMap((a,e)=>a?[e]:[])),signedLiterals:lit,randomTests:250,families,neighbors};}
console.log(JSON.stringify(run(),null,2));
