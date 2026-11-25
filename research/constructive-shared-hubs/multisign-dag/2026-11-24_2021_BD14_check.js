const run = function run(){
const stats={checks:0,gram:0,linear:0,joins:0,rejects:0,insertions:0,probes:0,closureScans:0,localRows:0,globalRows:0,referenceWords:0,maxTable:0,maxWidth:0,queries:0};
const check=x=>{stats.checks++;if(!x)throw Error("assertion "+stats.checks)};
const bits=m=>{const a=[];while(m){const b=m&-m;a.push(b);m^=b;}return a};
const par=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
const pop=x=>bits(x).length;
const abs=x=>x<0n?-x:x;
function gcd(a,b){a=abs(a);b=abs(b);while(b){[a,b]=[b,a%b]}return a}
function reduce(rows){stats.linear++;const B=new Map();for(let [a,b] of rows){while(a){const p=a&-a;if(!B.has(p)){B.set(p,[a,b]);break}let [c,d]=B.get(p);a^=c;b^=d}if(!a&&b)return null}return B}
function addVec(B,v){let w=v.slice();for(const [p,b] of B){if(w[p]){const a=w[p],c=b[p];w=w.map((x,i)=>c*x-a*b[i]);const g=w.reduce((s,x)=>gcd(s,x),0n);if(g>1n)w=w.map(x=>x/g)}}let p=w.findIndex(x=>x!==0n);if(p<0)return false;const g=w.reduce((s,x)=>gcd(s,x),0n);if(g>1n)w=w.map(x=>x/g);B.push([p,w]);return true}
function affCount(scope,rows){const B=reduce(rows);return B===null?0n:1n<<BigInt(pop(scope)-B.size)}
function words(scope){const a=[0n];for(const b of bits(scope)){const n=a.length;for(let i=0;i<n;i++)a.push(a[i]|b)}return a}
const pin=(scope,x)=>bits(scope).map(b=>[b,Number(!!(b&x))]);
const term=(c,...eq)=>[BigInt(c),eq];
const evalLeaf=(L,x)=>L.terms.map(ts=>ts.reduce((s,[c,r])=>s+(r.every(([a,b])=>par(a&x)===b)?c:0n),0n));
function leafBasis(L,key,twist,paired){const D=L.terms.length;let ts=L.terms;if(paired)ts=ts.concat(ts.map(t=>t.flatMap(([c,r])=>[[c,r],[-2n*c,r.concat([[twist,1]])]])));
 const out=[],B=[];const scope=L.scope, base=pin(L.w,key);
 function outside(rows){stats.gram++;const Q=ts.map(t=>ts.map(u=>{let z=0n;for(const [c,r] of t)for(const [d,s] of u)z+=c*d*affCount(scope,rows.concat(r,s));return z}));let A=B.slice();return Q.some(v=>addVec(A,v))}
 while(outside(base)){let r=base.slice(),x=key;for(const b of bits(scope&~L.w)){stats.probes++;if(outside(r.concat([[b,0]])))r.push([b,0]);else {r.push([b,1]);x|=b}}let v=evalLeaf(L,x);if(paired)v=v.concat(v.map(z=>par(twist&x)?-z:z));check(addVec(B,v));out.push({v,x});stats.insertions++}
 return out}
function makeTree(leaves,op){let a=leaves.map((l,i)=>({...l,id:i}));while(a.length>1){let b=[];for(let i=0;i<a.length;i+=2){if(i+1===a.length)b.push(a[i]);else b.push({a:a[i],b:a[i+1],scope:a[i].scope|a[i+1].scope,op})}a=b}const root=a[0];function prep(v,out){v.w=v.scope&out;stats.maxWidth=Math.max(stats.maxWidth,pop(v.w));if(v.a){prep(v.a,out|v.b.scope);prep(v.b,out|v.a.scope)}}prep(root,0n);return root}
const mul=(a,b)=>a.map((x,i)=>x*b[i]);
function solve(root,read,a=null,rhs=0){stats.queries++;const paired=a!==null;let rem=a||0n;const split=new Map();function assign(v){if(v.a){assign(v.a);assign(v.b)}else{split.set(v.id,rem&v.scope);rem&=~v.scope}}assign(root);check(rem===0n);
 function go(v){const table=new Map();if(!v.a){for(const k of words(v.w)){const z=leafBasis(v,k,split.get(v.id),paired);if(z.length)table.set(k,z)}}else{const A=go(v.a),C=go(v.b),over=v.a.scope&v.b.scope, bmap=new Map();for(const aa of A.values())for(const bb of C.values())for(const x of aa)for(const y of bb){stats.joins++;if((x.x^y.x)&over){stats.rejects++;continue}const w=x.x|y.x,k=w&v.w;let z;if(paired){const h=x.v.length/2,j=y.v.length/2;z=v.op(x.v.slice(0,h),y.v.slice(0,j)).concat(v.op(x.v.slice(h),y.v.slice(j)))}else z=v.op(x.v,y.v);if(!bmap.has(k))bmap.set(k,[]);if(addVec(bmap.get(k),z)){if(!table.has(k))table.set(k,[]);table.get(k).push({v:z,x:w});stats.insertions++}}}
 stats.maxTable=Math.max(stats.maxTable,[...table.values()].reduce((a,b)=>a+b.length,0));return table}
 const dot=(v,r)=>r.reduce((s,x,i)=>s+x*v[i],0n);
 const tab=go(root).get(0n)||[];let q=read;if(paired)q=read.concat(read.map(x=>rhs? -x:x));return tab.find(z=>dot(z.v,q)!==0n)?.x??null}
function evalTree(t,x){return t.a?t.op(evalTree(t.a,x),evalTree(t.b,x)):evalLeaf(t,x)}
function closeLocal(owners,E){while(true){stats.closureScans++;let changed=false;for(const o of owners){const ok=words(o.scope).filter(x=>o.accept(x)&&reduce(E.concat(pin(o.scope,x)))!==null);if(!ok.length)return false;for(const a of words(o.scope).slice(1)){let b=par(a&ok[0]);if(ok.every(x=>par(a&x)===b)&&reduce(E.concat([[a,1-b]]))!==null){E.push([a,b]);stats.localRows++;changed=true;break}}if(changed)break}if(!changed)return true}}
function nullBasis(rows,scope){const B=reduce(rows.map(a=>[a,0]));const piv=[...B.keys()];return bits(scope).filter(b=>!B.has(b)).map(b=>{let x=b;for(const p of piv.slice().sort((a,b)=>a>b?-1:a<b?1:0)){const [r]=B.get(p);if(par(r&x))x|=p}return x})}
function hull(root,read,owners=[]){const E=[];if(!closeLocal(owners,E))return {sat:false};const anchor=solve(root,read);if(anchor===null)return {sat:false};const value=x=>read.reduce((s,c,i)=>s+c*evalTree(root,x)[i],0n);check(value(anchor)!==0n);const D=[];let q=0;while(D.length+E.length<pop(root.scope)){let a=null;for(const z of nullBasis(D,root.scope)){if(reduce(E.concat([[z,1-par(z&anchor)]]))!==null){a=z;break}}check(a!==null);q++;let rhs=1-par(a&anchor),x=solve(root,read,a,rhs);if(x===null){E.push([a,1-rhs]);stats.globalRows++;check(closeLocal(owners,E));}else{check(par(a&x)===rhs&&value(x)!==0n);check(E.every(([r,b])=>par(r&x)===b));D.push(x^anchor)}}
check(q<=pop(root.scope));return {sat:true,anchor,D,E,probes:q}}
const clause=(vars,signs)=>{let scope=vars.reduce((a,b)=>a|b,0n);let eq=vars.map((b,i)=>[b,signs[i]]);return {scope,terms:[[term(1),term(-1,...eq)]],accept:x=>!eq.every(([a,b])=>par(a&x)===b)}};
function nae(v,s){return [clause(v,s),clause(v,s.map(b=>1-b))]}
function cnf(owners,n){const all=(1n<<BigInt(n))-1n;let scope=owners.reduce((s,o)=>s|o.scope,0n);return makeTree(owners.concat(bits(all&~scope).map(b=>({scope:b,terms:[[term(1)]]}))),mul)}
const cases=[];function test(name,root,read,owners=[],expected=null,rank=null,exhaust=true){let H=hull(root,read,owners);let modelCount=null;if(exhaust){const S=words(root.scope).filter(x=>{stats.referenceWords++;return read.reduce((s,c,i)=>s+c*evalTree(root,x)[i],0n)!==0n});modelCount=S.length;check(H.sat===!!S.length);if(H.sat){check(S.every(x=>H.E.every(([r,b])=>par(r&x)===b)));const R=reduce(S.map(x=>[x^H.anchor,0]));check(R.size===H.D.length);check(H.D.length+H.E.length===pop(root.scope));}}if(expected!==null)check(H.sat===expected);if(rank!==null)check(H.D.length===rank);cases.push({name,n:pop(root.scope),sat:H.sat,rank:H.D?.length??null,forced:H.E?.length??null,probes:H.probes??null,models:modelCount})}
let v=Array.from({length:7},(_,i)=>1n<<BigInt(i)), edges=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];function fano(f=-1,j=-1){return edges.flatMap((e,i)=>nae(e.map(z=>v[z]),e.map((_,k)=>i===f&&k===j?1:0)))}
let f=fano();test("Fano",cnf(f,7),[1n],f,false);for(let i=0;i<14;i++){let o=f.filter((_,j)=>j!==i);test("budget-"+i,cnf(o,7),[1n],o,true)}for(let i=0;i<7;i++)for(let j=0;j<3;j++){let o=fano(i,j);test("sign-"+i+"-"+j,cnf(o,7),[1n],o,true)}
let seed=83021;const rng=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};for(let t=0;t<12;t++){let o=[];for(let j=0;j<8;j++){let u=[];while(u.length<3){let b=1n<<BigInt(rng(7));if(!u.includes(b))u.push(b)}o.push(clause(u,u.map(()=>rng(2))))}test("random-"+t,cnf(o,7),[1n],o)}
// Dense forced parity at width zero. Each leaf represents [1, (-1)^x_i].
function charTree(n,cancel=false){let b=bits((1n<<BigInt(n))-1n);return makeTree(b.map(x=>({scope:x,terms:[[term(1)],cancel?[term(1)]:[term(1),term(-2,[x,1])]]})),mul)}
test("signed-parity-8",charTree(8),[1n,-1n],[],true,7);test("signed-zero-8",charTree(8,true),[1n,-1n],[],false);
test("signed-parity-32",charTree(32),[1n,-1n],[],true,31,false);
const big=(1n<<24n)-1n;
test("rank24-leaf",makeTree([{scope:big,terms:[[term(1),term(-1,[big,1])]]}],mul),[1n],[],true,23,false);
for(let n of [8,32]){let b=bits((1n<<BigInt(n))-1n),o=[];for(let i=0;i<n;i+=2)o.push(clause([b[i],b[i+1]],[0,0]));test("interleaved-OR-"+n,cnf(o,n),[1n],o,true,n,n===8)}
return {seed:83021,stats,cases,sat:cases.filter(x=>x.sat).length,unsat:cases.filter(x=>!x.sat).length,limitations:"Coordinate-scope specialization of character lift and Gram contraction; general linear observation spaces symbolic only. No physical compiler, full portfolio or memory instrumentation."}
};
console.log(JSON.stringify(run(),null,2));
