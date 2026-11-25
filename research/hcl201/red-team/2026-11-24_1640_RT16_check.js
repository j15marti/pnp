function run(){
const out={basis_cases:0,projection_cases:0,projection_fibers:0,peer_core_subset_cases:0,neighbor_cases:0,root_cases:0,witnesses:0,unit_closure_rounds:0,assertions:0,scale:[]};
function ok(v){out.assertions++;if(!v)throw Error("assertion "+out.assertions)}
let seed=20261124;function rng(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
const bit=i=>1n<<BigInt(i);
function par(x){let p=0;while(x){p^=1;x&=x-1n}return p}
function rank(v){let b=[];for(let x of v){for(const y of b)if((x^y)<x)x^=y;if(x)b.push(x)}return b.length}
function span(v){let s=[0n];for(const x of v)if(!s.includes(x))s=s.concat(s.map(y=>y^x));return new Set(s)}
const plane=(a,b)=>[a,b,a^b].sort((x,y)=>x<y?-1:x>y?1:0);
const key=p=>p.join(",");
function planes(n){let m=new Map();for(let a=1;a<2**n;a++)for(let b=a+1;b<2**n;b++){let p=plane(BigInt(a),BigInt(b));m.set(key(p),p)}return [...m.values()]}
function recognize(P,W,n){let ps=[...new Map(P.map(p=>[key(p),p])).values()];let wr=rank(W),inside=x=>rank([...W,x])===wr;let forced=ps.map(p=>new Set(p.filter(x=>ps.filter(q=>q.includes(x)).length>1)));for(let i=0;i<ps.length;i++){let a=ps[i].filter(inside);if(a.length===1)forced[i].add(a[0]);if(forced[i].size>2)return null}
let picks=ps.map((p,i)=>{let a=[...forced[i]];for(const x of p)if(a.length<2&&!a.includes(x))a.push(x);return a});let u=[...new Set(picks.flat())],I=u.filter(inside),O=u.filter(x=>!inside(x));if(rank(I)!==I.length||rank([...W,...O])!==wr+O.length)return null;
let B=[...I];for(const x of W)if(rank([...B,x])>B.length)B.push(x);ok(B.length===wr);B.push(...O);for(let i=0;i<n;i++)if(rank([...B,bit(i)])>B.length)B.push(bit(i));ok(B.length===n&&rank(B)===n);return {B,wr,picks,ps}}
function bases(n){let b=[];function rec(v,start){if(v.length===n){b.push(v);return}for(let x=start;x<2**n;x++)if(rank([...v,BigInt(x)])>v.length)rec([...v,BigInt(x)],x+1)}rec([],1);return b}
function bruteBasis(P,W,bs){let r=rank(W);return bs.some(B=>B.filter(x=>rank([...W,x])===r).length===r&&P.every(p=>p.filter(x=>B.includes(x)).length===2))}
const p3=planes(3),b3=bases(3),b4=bases(4),p4=planes(4);let ws=[[],...Array.from({length:7},(_,i)=>[BigInt(i+1)]),...p3.map(p=>p.slice(0,2)),[1n,2n,4n]];
for(let mask=0;mask<128;mask++)for(const W of ws){let P=p3.filter((_,i)=>mask>>i&1);ok(Boolean(recognize(P,W,3))===bruteBasis(P,W,b3));out.basis_cases++}
for(let t=0;t<180;t++){let P=p4.filter(()=>rng(7)<2),W=b4[rng(b4.length)].slice(0,rng(5));ok(Boolean(recognize(P,W,4))===bruteBasis(P,W,b4));out.basis_cases++}
function clauses(E,R){let {B,ps,picks}=R;return E.map(([a,b,s,t])=>{let p=plane(a,b),q=picks[ps.findIndex(z=>key(z)===key(p))];function rhs(x){return x===a?s:x===b?t:s^t}return q.map(x=>2*B.indexOf(x)+(1^rhs(x)))})}
function evalC(C,x){return C.every(c=>c.some(l=>Number(x>>BigInt(l>>1)&1n)===(l&1)))}
function evalE(E,x){return E.every(([a,b,s,t])=>par(a&x)!==s||par(b&x)!==t)}
function closure(C,n){let pins=Array(n).fill(-1),changed=true;while(changed){out.unit_closure_rounds++;changed=false;for(const c of C){if(c.some(l=>pins[l>>1]===(l&1)))continue;let u=[...new Set(c.filter(l=>pins[l>>1]===-1))];if(!u.length)return null;if(u.length===1){let l=u[0];pins[l>>1]=l&1;changed=true}}}return pins}
function graph(C,n){let g=Array.from({length:2*n},()=>[]),r=g.map(()=>[]);for(let c of C){let a=c[0],b=c[1]??a;for(let [u,v] of [[a^1,b],[b^1,a]]){g[u].push(v);r[v].push(u)}}return {g,r}}
function solve(C,n){if(!closure(C,n))return null;let {g,r}=graph(C,n),seen=new Set(),order=[],co=Array(2*n).fill(-1);function dfs(u){if(seen.has(u))return;seen.add(u);for(let v of g[u])dfs(v);order.push(u)}for(let u=0;u<2*n;u++)dfs(u);function rev(u,k){if(co[u]>=0)return;co[u]=k;for(let v of r[u])rev(v,k)}let k=0;for(let u of order.reverse())if(co[u]<0)rev(u,k++);let x=0n;for(let i=0;i<n;i++){if(co[2*i]===co[2*i+1])return null;if(co[2*i+1]>co[2*i])x|=bit(i)}ok(evalC(C,x));return x}
function lift(B,y){let rows=[];for(let i=0;i<B.length;i++){let a=B[i],b=Number(y>>BigInt(i)&1n);for(let [u,v] of rows)if((a^u)<a){a^=u;b^=v}ok(a!==0n);rows.push([a,b])}rows.sort((p,q)=>p[0]<q[0]?-1:1);let x=0n;for(let [a,b] of rows){let i=BigInt(a.toString(2).length-1);if(par(a&x)!==b)x|=1n<<i}ok(B.every((a,i)=>par(a&x)===Number(y>>BigInt(i)&1n)));return x}
function projection(C,n,w){if(solve(C,n)===null)return [[]];let {g}=graph(C,n),P=[];for(let i=0;i<2*w;i++){let q=[i],seen=new Set(q);for(let j=0;j<q.length;j++)for(let v of g[q[j]])if(!seen.has(v)){seen.add(v);q.push(v)}for(let j=0;j<2*w;j++)if(seen.has(j))P.push([i^1,j])}return P}
function mixed(n){let B=Array.from({length:n},(_,i)=>bit(i));for(let t=0;t<8*n;t++){let i=rng(n),j=rng(n-1);if(j>=i)j++;B[i]^=B[j]}return B}
for(let t=0;t<100;t++){let n=5,B=mixed(n),w=rng(n+1),W=B.slice(0,w),E=[];for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)if(rng(4)<2)E.push([B[i],B[j],rng(2),rng(2)]);let R=recognize(E.map(([a,b])=>plane(a,b)),W,n);ok(R!==null);let C=clauses(E,R),P=projection(C,n,w),ys=new Set();for(let x=0n;x<bit(n);x++)if(evalE(E,x)){let y=0n;for(let i=0;i<w;i++)if(par(R.B[i]&x))y|=bit(i);ys.add(y)}for(let y=0n;y<bit(w);y++){ok(evalC(P,y)===ys.has(y));let units=Array.from({length:w},(_,i)=>[2*i+Number(y>>BigInt(i)&1n)]),z=solve([...C,...units],n);ok((z!==null)===ys.has(y));if(z!==null){let x=lift(R.B,z);ok(evalE(E,x));out.witnesses++}out.projection_fibers++}out.projection_cases++}
function family(k){let n=2*k+1,B=mixed(n),E=[];for(let s=0;s<2;s++){let path=[[0,s],...Array.from({length:k},(_,i)=>[1+s*k+i,1]),[0,1-s]];for(let i=0;i<path.length-1;i++){let [a,b]=path[i],[c,d]=path[i+1];E.push([B[a],B[c],b,1-d])}}return {n,E,B}}
for(let k of [2,3,4,5,8,16,32,64]){let {n,E,B}=family(k),R=recognize(E.map(([a,b])=>plane(a,b)),[],n);ok(R!==null);ok(solve(clauses(E,R),n)===null);out.root_cases++;let dis=[];for(let s=0;s<2;s++)for(let i=0;i+1<k;i+=2)dis.push(B[1+s*k+i],B[2+s*k+i]);ok(rank(dis)===dis.length);
if(k<=5){for(let mask=0;mask<2**E.length;mask++){let S=E.filter((_,i)=>mask>>i&1);let d=S.length-rank(S.flatMap(e=>e.slice(0,2)));ok(d===(S.length===E.length?1:Math.min(0,d)));out.peer_core_subset_cases++}}
let indices=k<=8?E.map((_,i)=>i):[0,k,k+1,E.length-1];for(let j of indices){let F=E.filter((_,i)=>i!==j),Q=recognize(F.map(([a,b])=>plane(a,b)),[],n);let z=solve(clauses(F,Q),n);ok(z!==null);ok(evalE(F,lift(Q.B,z)));out.witnesses++;out.neighbor_cases++}out.scale.push({k,n,m:E.length,intrinsic_lower:dis.length/2,neighbors:indices.length})}
return out
}
console.log(JSON.stringify(run(),null,2));
