function run(){
let seed=1242026;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
const C={cases:0,sat:0,unsat:0,sourceTuples:0,parityStates:0,matchingNodes:0,matchingWitnesses:0,closureScans:0,deletedRows:0,identityInsertions:0,hullChecks:0,badGroupChecks:0,badGroupTuples:0,parallelGadgetChecks:0};
const chk=(v,msg)=>{if(!v)throw Error(msg)};
const insert=(B,v)=>{while(v){const i=31-Math.clz32(v);if(B[i])v^=B[i];else{B[i]=v;return}}};
const inSpan=(B,v)=>{while(v){const i=31-Math.clz32(v);if(!B[i])return false;v^=B[i]}return true};
const basis=xs=>{const B=[];for(const v of xs)insert(B,v);return B};
const dot=(x,y)=>{let v=x&y,r=0;while(v){v&=v-1;r^=1}return r};
const hull=xs=>xs.length?{a:xs[0],B:basis(xs.map(x=>x^xs[0]))}:null;
const same=(a,b)=>a===null||b===null?a===b:inSpan(a.B,a.a^b.a)&&a.B.every(v=>inSpan(b.B,v))&&b.B.every(v=>inSpan(a.B,v));
function one(rows,caps,h,b,z){
const nr=rows.flat().length, n=rows.length, g=[...new Set(h)], cls=h.map(t=>g.indexOf(t));let id=0;
rows=rows.map((rs,i)=>rs.map(o=>({o,mask:1<<id++,tag:b[i]^h[o]})));
const ref=[];function rec(i,occ,tag,x){if(i===n){C.sourceTuples++;if(tag===z)ref.push(x);return}for(const r of rows[i])if(occ[r.o]<caps[r.o]){occ[r.o]++;rec(i+1,occ,tag^r.tag,x^r.mask);occ[r.o]--}}rec(0,caps.map(()=>0),0,0);
let active=rows.map(rs=>rs.slice()), eq=[];
function closure(){while(true){C.closureScans++;if(active.some(rs=>!rs.length))return false;let changed=false;outer:for(let i=0;i<n;i++)for(const r of active[i]){
 let ok=caps[r.o]>0;let req=z;let base=0;const B=[];const val=t=>{let a=t.tag;for(let j=0;j<eq.length;j++)a|=dot(t.mask,eq[j][0])<<(2+j);return a};
 for(let j=0;j<eq.length;j++)req|=eq[j][1]<<(2+j);
 for(let k=0;k<n;k++){const rs=k===i?[r]:active[k];const v=val(rs[0]);base^=v;for(const s of rs)insert(B,val(s)^v)}
 if(!inSpan(B,req^base))ok=false;
 let mandatory=1;for(let k=0;k<n;k++)if(k!==i&&active[k].every(s=>s.o===r.o))mandatory++;
 if(mandatory>caps[r.o])ok=false;
 if(!ok){active[i]=active[i].filter(s=>s!==r);C.deletedRows++;changed=true;break outer}
 }if(!changed)return true}}
 const pre=closure(), graphHulls=[];let all=[];
 if(pre)for(let p=0;p<(1<<g.length);p++){let t=b.reduce((a,x)=>a^x,0),pcount=0;for(let j=0;j<g.length;j++)if(p>>j&1){t^=g[j];pcount^=1}if(t!==z||pcount!==(n&1))continue;C.parityStates++;
 let adj=Array.from({length:n},()=>[]), slots=[];function v(){adj.push([]);return adj.length-1}function edge(a,b,mask=0){adj[a].push([b,mask]);adj[b].push([a,mask])}
 for(let o=0;o<caps.length;o++)for(let k=0;k<Math.min(n,caps[o]);k++)slots.push({o,v:v()});
 for(let i=0;i<n;i++)for(const r of active[i])for(const s of slots)if(s.o===r.o)edge(i,s.v,r.mask);
 for(let j=0;j<g.length;j++){const vs=slots.filter(s=>cls[s.o]===j).map(s=>s.v);if((vs.length&1)!==(p>>j&1))vs.push(v());for(let a=0;a<vs.length;a++)for(let d=a+1;d<vs.length;d++)edge(vs[a],vs[d])}
 const a=v(),d=v();edge(a,d); // marker coordinate is implicit constant 1
 const words=[];function dfs(left,x){C.matchingNodes++;if(!left){C.matchingWitnesses++;words.push(x);return}const bit=left&-left,i=31-Math.clz32(bit);for(const [j,m] of adj[i])if(left&(1<<j))dfs(left^bit^(1<<j),x^m)}
 chk(adj.length<31,"test graph too large");dfs((1<<adj.length)-1,0);
 // Experimental substitute: enumerate all perfect matchings; use only a basis of homogeneous projected words.
 const L=basis(words.map(x=>x|(1<<nr)));const marker=1<<nr;
 if(words.length){const anchor=L.find(x=>x&marker);chk(anchor!==undefined,"anchor");const B=basis(L.filter(Boolean).map(x=>(x^(x&marker?anchor:0))& (marker-1)));graphHulls.push({a:anchor&(marker-1),B});all.push(...words)}
 }
 const combined=graphHulls.length?{a:graphHulls[0].a,B:basis(graphHulls.flatMap(H=>[H.a^graphHulls[0].a,...H.B.filter(Boolean)]))}:null;
 chk(same(combined,hull(ref)),"hull differs");chk(new Set(all).size===new Set(ref).size&&all.every(x=>ref.includes(x)),"support differs");
 if(combined){ // select a basis of all forced linear identities and reclose after each insertion
 const dual=[];for(let u=1;u<(1<<nr);u++)if(combined.B.every(v=>!dot(u,v))&&!inSpan(dual,u)){insert(dual,u);eq.push([u,dot(u,combined.a)]);C.identityInsertions++;chk(closure(),"identity rejected");for(const x of ref)chk(dot(x,u)===dot(combined.a,u),"false identity")}
 for(let u=0;u<(1<<nr);u++){const vals=new Set(ref.map(x=>dot(x,u)));const fixed=combined.B.every(v=>!dot(v,u));chk(fixed===(vals.size===1),"probe mismatch");C.hullChecks++}
 }
 C.cases++;C[ref.length?"sat":"unsat"]++;
}
for(let it=0;it<100;it++){const n=2+rnd(2),o=2+rnd(2),h=Array.from({length:o},()=>rnd(4)),b=Array.from({length:n},()=>rnd(4)),caps=Array.from({length:o},()=>rnd(3));const rows=Array.from({length:n},()=>Array.from({length:o},(_,j)=>j).filter(()=>rnd(4)!==0));one(rows,caps,h,b,rnd(4))}
one([[0,1,2,3],[0,1,2,3]],[1,1,1,1],[0,1,2,3],[0,0],0);
for(let z=1;z<4;z++)one([[0,1,2,3],[0,1,2,3]],[1,1,1,1],[0,1,2,3],[0,0],z);
for(let n=1;n<=7;n++)for(let k=0;k<=n;k++){const xs=[];for(let x=0;x<1<<n;x++){let c=0;for(let i=0;i<n;i++)c+=x>>i&1;if(c===k)xs.push(x);C.badGroupTuples++}
const a=(1<<k)-1;const B=[];if(k>0&&k<n)for(let i=0;i<k;i++)for(let j=k;j<n;j++)insert(B,(1<<i)^(1<<j));chk(same({a,B},hull(xs)),"bad hull");C.badGroupChecks++}
return {seed:1242026,...C,discrepancies:0,backend:"exhaustive small perfect matching enumeration and GF(2) basis, not Lovasz polynomial algorithm"};
}
console.log(JSON.stringify(run(),null,2));
