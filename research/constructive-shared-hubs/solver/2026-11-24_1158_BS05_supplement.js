const experiment = function experiment(){
const stats={closurePass:0,rowTests:0,deletions:0,graphEdges:0,cutNodes:0,pinAttempts:0,forestCalls:0,matchingCalls:0,matchingAttempts:0,affineCalls:0,dagCalls:0,dagEdges:0,dagDeclines:0,peakDAG:0,sourceChecks:0,bruteTuples:0}; const assert=(x,m)=>{if(!x)throw Error(m)};
const fresh=()=>({B:[],P:[],R:[]}); // row = {c:BigInt[],p:BigInt, id:number}
function input(B,P,R){return {B:B.map(BigInt),P:P.map(Number),R:R.map(rs=>rs.map((r,id)=>({c:r[0].map(BigInt),p:BigInt(r[1]),id})))}}
const bit=(x,j)=>Number((x>>BigInt(j))&1n);
function valid(F,rows){if(!rows||rows.length!==F.R.length)return false;let p=0n,c=F.B.map(()=>0n);for(let i=0;i<rows.length;i++){const r=rows[i];if(!F.R[i].includes(r))return false;p^=r.p;r.c.forEach((x,j)=>c[j]+=x)}return c.every((x,j)=>x<=F.B[j])&&F.P.every((x,j)=>bit(p,j)===x)}
function closure(F,R){R=R.map(a=>a.slice());for(;;){stats.closurePass++;if(R.some(a=>!a.length))return null;
let min=R.map(a=>F.B.map((_,j)=>a.reduce((x,r)=>r.c[j]<x?r.c[j]:x,a[0].c[j]))), sum=F.B.map((_,j)=>min.reduce((x,a)=>x+a[j],0n));
if(sum.some((x,j)=>x>F.B[j]))return null;
let base=R.map(a=>a[0].p), variable=R.map((a,i)=>a.reduce((x,r)=>x|(r.p^base[i]),0n)), total=base.reduce((x,y)=>x^y,0n), counts=F.P.map((_,j)=>variable.reduce((x,v)=>x+bit(v,j),0));
if(F.P.some((v,j)=>!counts[j]&&bit(total,j)!==v))return null;
let changed=false; outer:for(let i=0;i<R.length;i++)for(let k=0;k<R[i].length;k++){let r=R[i][k];stats.rowTests++;if(r.c.some((x,j)=>sum[j]-min[i][j]+x>F.B[j])||F.P.some((v,j)=>counts[j]===bit(variable[i],j)&&bit(total^base[i]^r.p,j)!==v)){R[i].splice(k,1);stats.deletions++;changed=true;break outer}}
if(!changed)return R}}
function graph(F,R){let E=[];for(let i=0;i<R.length;i++){for(let j=0;j<F.B.length+F.P.length;j++){const val=r=>j<F.B.length?r.c[j]:BigInt(bit(r.p,j-F.B.length));let D=[...new Set(R[i].map(val))];if(D.length>1)E.push({i,j,D})}}stats.graphEdges+=E.length;return E}
function cutset(F,R){let E=graph(F,R),n=R.length+F.B.length+F.P.length,p=Array.from({length:n},(_,i)=>i);function root(i){while(p[i]!==i)i=p[i];return i}let C=[];E.sort((a,b)=>b.D.length-a.D.length||a.i-b.i||a.j-b.j);for(let e of E){let x=root(e.i),y=root(R.length+e.j);if(x===y)C.push(e);else p[x]=y}return C}
function forest(F,R){stats.forestCalls++;for(let i=0;i<R.length;i++){if(R[i].length>1){let Q=R.slice();Q[i]=[R[i][0]];R=closure(F,Q);assert(R,"forest arbitrary row must extend")}}let w=R.map(a=>a[0]);assert(valid(F,w),"forest witness");return w}
const UNKNOWN=Symbol();
function matching(F,R){ // normalized rows choose one unit owner or zero; no varying parity
if(R.some(a=>a.some(r=>r.p!==a[0].p)))return UNKNOWN;
let mins=R.map(a=>F.B.map((_,j)=>a.reduce((x,r)=>r.c[j]<x?r.c[j]:x,a[0].c[j]))), cap=F.B.map((b,j)=>b-mins.reduce((s,a)=>s+a[j],0n));if(cap.some(c=>c<0n))return null;
let options=R.map((a,i)=>a.map(r=>{let d=r.c.map((v,j)=>v-mins[i][j]),nz=d.map((v,j)=>v?j:-1).filter(j=>j>=0);return nz.length===0?-1:nz.length===1&&d[nz[0]]===1n?nz[0]:-2}));if(options.some(a=>a.includes(-2)))return UNKNOWN;stats.matchingCalls++;
let slots=[],choice=Array(R.length).fill(-1);for(let j=0;j<cap.length;j++)for(let k=0;k<Number(cap[j]>BigInt(R.length)?BigInt(R.length):cap[j]);k++)slots.push(j);let occ=slots.map(()=>-1);
function aug(i,seen){for(let k=0;k<slots.length;k++){stats.matchingAttempts++;let a=options[i].indexOf(slots[k]);if(a<0||seen.has(k))continue;seen.add(k);if(occ[k]<0||aug(occ[k],seen)){occ[k]=i;choice[i]=a;return true}}return false}
for(let i=0;i<R.length;i++){let free=options[i].indexOf(-1);if(free>=0)choice[i]=free;else if(!aug(i,new Set()))return null}return R.map((a,i)=>a[choice[i]])}
function affine(F,R){if(F.B.some((b,j)=>R.reduce((s,a)=>s+a.reduce((v,r)=>r.c[j]>v?r.c[j]:v,0n),0n)>b))return UNKNOWN;
let base=new Map(), origins=[], anchor=0n, target=F.P.reduce((x,b,j)=>x|(BigInt(b)<<BigInt(j)),0n);
function add(M,v,k){while(v){let h=v.toString(2).length-1;if(!M.has(h)){M.set(h,[v,k]);return true}let a=M.get(h);v^=a[0];k^=a[1]}return false}
for(let i=0;i<R.length;i++){let a=R[i],z=a[0].p;anchor^=z;let M=new Map(),S=new Set(a.map(r=>r.p));for(let r of a){let d=r.p^z;if(add(M,d,0n)){let k=origins.length;origins.push([i,d]);add(base,d,1n<<BigInt(k))}}if(BigInt(S.size)!==(1n<<BigInt(M.size)))return UNKNOWN}
stats.affineCalls++;let v=target^anchor,k=0n;while(v){let a=base.get(v.toString(2).length-1);if(!a)return null;v^=a[0];k^=a[1]}let t=R.map(a=>a[0].p);origins.forEach(([i,d],j)=>{if((k>>BigInt(j))&1n)t[i]^=d});return R.map((a,i)=>a.find(r=>r.p===t[i]))}
function dag(F,R,limit=256){stats.dagCalls++;let M=new Map([["0|"+F.B.map(()=>0n).join(","),{p:0n,c:F.B.map(()=>0n),w:[]}]]);for(let a of R){let Q=new Map();for(let s of M.values())for(let r of a){stats.dagEdges++;let c=s.c.map((v,j)=>v+r.c[j]);if(c.some((v,j)=>v>F.B[j]))continue;let p=s.p^r.p,key=p+"|"+c.join(",");if(!Q.has(key))Q.set(key,{p,c,w:[...s.w,r]});stats.peakDAG=Math.max(stats.peakDAG,Q.size);if(Q.size>limit){stats.dagDeclines++;return UNKNOWN}}M=Q}let t=F.P.reduce((x,b,j)=>x|(BigInt(b)<<BigInt(j)),0n);for(let s of M.values())if(s.p===t)return s.w;return null}
function solve(F,opt={}){let root=closure(F,F.R);if(!root)return null;let C=cutset(F,root);
function go(R,k){stats.cutNodes++;R=closure(F,R);if(!R)return null;
if(!opt.cutOnly){for(let t of [matching,affine]){let w=t(F,R);if(w!==UNKNOWN)return w}if(!C.slice(k).length)return forest(F,R);let w=dag(F,R,opt.limit??256);if(w!==UNKNOWN)return w}
if(k===C.length)return forest(F,R);
let e=C[k],val=r=>e.j<F.B.length?r.c[e.j]:BigInt(bit(r.p,e.j-F.B.length));let D=[...new Set(R[e.i].map(val))];for(let d of D){stats.pinAttempts++;let Q=R.slice();Q[e.i]=Q[e.i].filter(r=>val(r)===d);let w=go(Q,k+1);if(w)return w}return null}
let w=go(root,0);if(w){stats.sourceChecks++;assert(valid(F,w),"solver witness")}return w}
function brute(F){let w=[];function rec(i){if(i===F.R.length){stats.bruteTuples++;return valid(F,w)}for(let r of F.R[i]){w.push(r);if(rec(i+1))return true;w.pop()}return false}return rec(0)}
let seed=208051;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
let counts={random:{sat:0,unsat:0},cube:{sat:0,unsat:0},fano:{sat:0,unsat:0},k5:{sat:0,unsat:0},scale:[],hostile:[]};
function check(F,expected,group,opt={}){let actual=!!solve(F,opt);assert(actual===expected,group+" mismatch");counts[group][actual?"sat":"unsat"]++}
for(let z=0;z<120;z++){let n=2+rnd(5),b=1+rnd(3),q=1+rnd(4);let F=input(Array.from({length:b},()=>rnd(9)),Array.from({length:q},()=>rnd(2)),Array.from({length:n},()=>Array.from({length:1+rnd(4)},()=>[Array.from({length:b},()=>rnd(4)),rnd(1<<q)])));let ex=brute(F);check(F,ex,"random");assert(!!solve(F,{cutOnly:true})===ex,"cut-only random")}
function cnf(n,cs){return input(cs.map(c=>c.length-1),[],Array.from({length:n},(_,i)=>[0,1].map(v=>[cs.map(c=>c.filter(l=>Math.abs(l)===i+1&&((l>0?1:0)!==v)).length),0])))}
let cube=Array.from({length:8},(_,x)=>[0,1,2].map(i=>((x>>i)&1)?-(i+1):i+1));for(let mask=1;mask<256;mask++){let F=cnf(3,cube.filter((_,j)=>(mask>>j)&1));check(F,mask!==255,"cube")}
let fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]].flatMap(a=>[a,a.map(v=>-v)]);for(let j=-1;j<14;j++){let F=cnf(7,fano.filter((_,k)=>j!==k));let e=brute(F);assert(e===(j>=0),"Fano reference");check(F,e,"fano")}
function rim(a,b,s){for(let z=0;z<64;z++){let x=[z&3,(z>>2)&3,(z>>4)&3];if(x.every((v,i)=>v!==x[(i+1)%3]&&v!==(a^(i===1?1:0))&&v!==(b^s^(i===1?0:1))))return x}return null}
for(let a=0;a<4;a++)for(let b=0;b<4;b++)for(let s=0;s<4;s++)assert(!!rim(a,b,s)===((a^b)!==s),"wheel projection")
function color(n,E){ // one row per vertex, one row per private projected wheel, parity occurrence synchronization
let q=4*E.length,vr=Array.from({length:n},()=>Array.from({length:4},()=>0n)),rr=[];E.forEach(([u,v,s],i)=>{for(let x=0;x<4;x++){vr[u][x]|=BigInt(x)<<BigInt(4*i);vr[v][x]|=BigInt(x)<<BigInt(4*i+2)}let a=[];for(let x=0;x<4;x++)for(let y=0;y<4;y++)if(rim(x,y,s))a.push([[],BigInt(x|(y<<2))<<BigInt(4*i)]);rr.push(a)});return input([],Array(q).fill(0),[...vr.map(a=>a.map(t=>[[],t])),...rr])}
let edges=[];for(let i=0;i<5;i++)for(let j=i+1;j<5;j++)edges.push([i,j,0]); // use equivalent direct edge clauses for K5 decisions, and actual wheel encoding on small triangle
for(let j=-1;j<10;j++){let E=edges.filter((_,i)=>i!==j),cs=[];for(let [u,v] of E)for(let a=0;a<4;a++)cs.push([2*u+1,2*u+2,2*v+1,2*v+2].map((x,k)=>((a>>(k%2))&1)?-x:x));let F=cnf(10,cs);check(F,j>=0,"k5")}
let tri=[[0,1,0],[1,2,0],[0,2,0]],W=color(3,[...tri,...tri]);let w=solve(W,{limit:32});assert(w,"duplicate wheels SAT");let x=w.slice(0,3).map(r=>r.id);for(let [u,v,s] of [...tri,...tri])assert(rim(x[u],x[v],s),"rim lift");
let U=color(2,[[0,1,0],[0,1,1],[0,1,2],[0,1,3]]);assert(!solve(U,{limit:32}),"all differences rejected");
for(let n of [8,32,128]){ // parity chain, budget leaves, all bits 1 or inconsistent last guard
let R=Array.from({length:n},(_,i)=>[0,1].map(v=>{let p=0n;if(i>0)p|=BigInt(v)<<BigInt(i-1);if(i<n-1)p|=BigInt(v)<<BigInt(i);return [Array.from({length:n},(_,j)=>i===j?(1n<<80n)+BigInt(v):0n),p]}));
let B=Array(n).fill((1n<<80n)+1n);B[0]=1n<<80n;B[n-1]=1n<<80n;
for(let h of [0,1]){let P=Array(n-1).fill(0);P[n-2]=h;let F=input(B,P,R);let c=closure(F,F.R),cuts=c?cutset(F,c).length:0;assert(!!solve(F,{cutOnly:true})===(h===0),"chain");counts.scale.push({n,q:n-1,sat:h===0,cuts,closureContradiction:!c})}
// unpinned connected mixed forest, all rows supported, 127 simultaneous parity bits
let F=input(Array(n).fill((1n<<80n)+1n),Array(n-1).fill(0),R);let c=closure(F,F.R);assert(c&&cutset(F,c).length===0&&solve(F,{cutOnly:true}),"forest scale");counts.scale.push({n,q:n-1,sat:true,cuts:0,unpinned:true,allRowsRetained:c.every(a=>a.length===2)})
}
// Two cyclic explicit factors, 2 budget owners; parity graph edge cut weight tests.
let part=input([5,5],[],[2,3,5].map(a=>[[[a,0],0],[[0,a],0]]));assert(solve(part,{cutOnly:true}),"partition sat");
let partU=input([4,4],[],[2,3,3].map(a=>[[[a,0],0],[[0,a],0]]));assert(!solve(partU,{cutOnly:true}),"partition unsat");
// unit matching cyclic eligibility, positive and negative
for(let k of [2,3]){let F=input([1,1],[],Array.from({length:k},()=>[[[1,0],0],[[0,1],0]]));assert(!!solve(F)===(k===2),"matching control")}
// count-like repeated signature DAG with varying parity and budgets, explicit cap
let D=input([2,2],[0],Array.from({length:4},()=>[[[1,0],0],[[0,1],1]]));assert(solve(D),"count profile");

let mixed=[];
for(let n of [8,32,128]){
 let R=[]; // nonaffine ternary local tags on parity chain, one coupled budget leaf per factor
 for(let i=0;i<n;i++){
  R.push([[0,0],[1,0],[0,1]].map(([l,r])=>{
   let p=0n;if(i>0)p|=BigInt(l)<<BigInt(i-1);if(i<n-1)p|=BigInt(r)<<BigInt(i);
   return [Array.from({length:n},(_,j)=>i===j?Number(l||r):0),p]
  }));
 }
 for(let i=0;i<n;i++)R.push([0,1].map(v=>[Array.from({length:n},(_,j)=>i===j?v:0),0]));
 let F=input(Array(n).fill(1),Array(n-1).fill(0),R);
 let Q=closure(F,F.R);assert(Q&&Q.every((a,i)=>a.length===F.R[i].length),"mixed closure retained all rows");
 assert(cutset(F,Q).length===0,"mixed forest");
 assert(affine(F,Q)===UNKNOWN,"active budgets exclude affine terminal");
 assert(matching(F,Q)===UNKNOWN,"parity excludes matching");
 assert(solve(F,{cutOnly:true}),"nonaffine mixed forest SAT");
 mixed.push({n,blocks:2*n,parityOwners:n-1,budgetOwners:n,cutVolume:1,allRowsRetained:true});
}
// Fixed graph weighted edge-cut optimum, independent exhaustive comparison.
// Graphs are abstract weighted incidence graphs; 6 vertices, up to 9 edges.
let weightedChecks=0;
for(let it=0;it<100;it++){
 let E=[];for(let i=0;i<3;i++)for(let j=3;j<6;j++)if(rnd(5)!==0)E.push([i,j,2+rnd(7)]);
 const product=(a)=>a.reduce((p,e)=>p*BigInt(e[2]),1n);
 const acyclic=a=>{let p=[0,1,2,3,4,5];let root=i=>{while(p[i]!==i)i=p[i];return i};for(let [u,v] of a){u=root(u);v=root(v);if(u===v)return false;p[u]=v}return true};
 let forest=[];for(let e of E.slice().sort((a,b)=>b[2]-a[2]))if(acyclic([...forest,e]))forest.push(e);
 let got=product(E.filter(e=>!forest.includes(e))),best=product(E);
 for(let m=0;m<(1<<E.length);m++){let a=E.filter((_,j)=>(m>>j)&1);if(acyclic(a)){let v=product(E.filter(e=>!a.includes(e)));if(v<best)best=v}}
 assert(got===best,"weighted cut optimum");weightedChecks++;
}
return {mixed,weightedChecks,stats,seed:208051,notes:"Full primary suite rerun before supplemental cases; abstract weighted graph optimum compared against every forest."}

};
console.log(JSON.stringify(experiment(),null,2));
