function check(){
let seed=20261124,M={assertions:0,reduce:0,closureScans:0,closureDeductions:0,localProbes:0,searchNodes:0,guardNodes:0,witnesses:0,referenceWords:0,ms15Cuts:0,qc01Activations:0},random=[],family=[],scale=[];
const assert=(b,msg)=>{M.assertions++;if(!b)throw Error(msg)};
const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n};
const bit=i=>1n<<BigInt(i),parity=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
function red(B,x,c=0){M.reduce++;for(const [p,r,s] of B)if(x&p){x^=r;c^=s}return [x,c]}
function add(B,x,c=0){[x,c]=red(B,x,c);if(!x)return c?-1:0;let p=x&-x;B.push([p,x,c]);B.sort((a,b)=>a[0]<b[0]?-1:1);return 1}
const clone=B=>B.map(r=>r.slice());
function basis(rows){let B=[];for(const x of rows)add(B,x);return B}
const rank=rows=>basis(rows).length,has=(B,x)=>red(B,x)[0]===0n,hits=(B,[u,v])=>has(B,u)||has(B,v)||has(B,u^v);
function exact(P){for(let h=0;;h++){function visit(B,k){M.searchNodes++;let p=P.find(p=>!hits(B,p));if(!p)return B;if(!k)return null;for(const x of [p[0],p[1],p[0]^p[1]]){let C=clone(B);add(C,x);let z=visit(C,k-1);if(z)return z}return null}let z=visit([],h);if(z)return z}}
function greedy(P,raw=false){let B=[];for(const p of P)if(raw?(!has(B,p[0])&&!has(B,p[1])):!hits(B,p)){add(B,p[0]);add(B,p[1])}return B}
function bruteSubspace(P,d){let seen=new Map([["0",[0n]]]);for(let h=0;h<=d;h++){for(const S of seen.values())if(P.every(([u,v])=>S.includes(u)||S.includes(v)||S.includes(u^v)))return h;let next=new Map;for(const S of seen.values())for(let i=1;i<2**d;i++){let x=BigInt(i);if(S.includes(x))continue;let T=[...S,...S.map(y=>y^x)].sort((a,b)=>a<b?-1:a>b?1:0);next.set(T.join(","),T)}seen=next}throw Error("no subspace")}
const val=(r,x)=>parity(r&x);
function closure(B,G){outer:while(true){for(const [u,v,w,s] of G){M.closureScans++;let support=[];for(let a=0;a<8;a++){let C=clone(B),b=[a&1,(a>>1)&1,(a>>2)&1];M.localProbes++;if((b[0]*b[1]^b[2])!==s)continue;if([u,v,w].every((f,j)=>add(C,f,b[j])>=0))support.push(a)}if(!support.length)return false;for(let m=1;m<8;m++){let p=parity(BigInt(m&support[0]));if(support.every(a=>parity(BigInt(m&a))===p)){let r=(m&1?u:0n)^(m&2?v:0n)^(m&4?w:0n);let z=add(B,r,p);if(z<0)return false;if(z>0){M.closureDeductions++;continue outer}}}}return true}}
function witness(B){let x=0n;for(let j=B.length-1;j>=0;j--){let [p,r,c]=B[j];if(val(r,x)!==c)x^=p}return x}
function solve(d,L,G){let B=[];for(const [r,c] of L)if(add(B,r,c)<0)return {count:0n,h:0,raw:0,root:0};let before=B.length;if(!closure(B,G))return {count:0n,h:0,raw:0,root:B.length-before};let root=B.length-before;let P=G.map(([u,v])=>[red(B,u)[0],red(B,v)[0]]).filter(([u,v])=>u&&v&&u!==v);let K=exact(P),raw=greedy(P,true).length,h=K.length,count=0n;
function dfs(C,j){M.guardNodes++;if(!closure(C,G))return;while(j<K.length&&has(C,K[j][1]))j++;if(j<K.length){for(let c=0;c<2;c++){let D=clone(C);if(add(D,K[j][1],c)>=0)dfs(D,j+1)}return}
for(const [u,v,w,s] of G){let [a,ca]=red(C,u),[b,cb]=red(C,v);assert(!a||!b||a===b,"nonlinear terminal");let row=w;if(!a){if(ca)row^=v}else if(!b){if(cb)row^=u}else if(!(ca^cb))row^=u;let z=add(C,row,s);if(z<0)return;if(z>0){M.closureDeductions++;if(!closure(C,G))return}}
let x=witness(C);assert(L.every(([r,c])=>val(r,x)===c)&&G.every(([u,v,w,s])=>(val(u,x)*val(v,x)^val(w,x))===s),"lift");M.witnesses++;count+=1n<<BigInt(d-C.length)
}dfs(B,0);return {count,h,raw,root}}
function brute(d,L,G){let c=0n;for(let i=0;i<2**d;i++){M.referenceWords++;let x=BigInt(i);if(L.every(([r,c])=>val(r,x)===c)&&G.every(([u,v,w,s])=>(val(u,x)*val(v,x)^val(w,x))===s))c++}return c}
for(let j=0;j<80;j++){let d=3+rnd(3),G=Array.from({length:1+rnd(8)},()=>[BigInt(rnd(2**d)),BigInt(rnd(2**d)),BigInt(rnd(2**d)),rnd(2)]),L=Array.from({length:rnd(3)},()=>[BigInt(rnd(2**d)),rnd(2)]);let s=solve(d,L,G),b=brute(d,L,G);assert(s.count===b,"random count");let P=G.map(([u,v])=>[u,v]).filter(([u,v])=>u&&v&&u!==v),h=exact(P).length;assert(h===bruteSubspace(P,d),"exact optimal");assert(greedy(P).length<=2*h,"greedy bound");random.push({d,G:G.map(g=>g.map(String)),L:L.map(g=>g.map(String)),count:String(b),h,greedy:greedy(P).length})}
function fam(n,s,flip=-1){let X=Array.from({length:n},(_,i)=>bit(i+1)),Z=Array.from({length:n},(_,i)=>bit(n+i+1));let L=[[X.reduce((a,b)=>a^b,0n),0],[Z.reduce((a,b)=>a^b,0n),s]],G=X.map((x,i)=>[x,x^1n,Z[i],i===flip?1:0]);return {d:2*n+1,L,G}}
for(let n=2;n<=6;n++)for(let f=-1;f<n;f++){let {d,L,G}=fam(n,1,f),s=solve(d,L,G),b=brute(d,L,G);assert(s.count===b&&b===(f<0?0n:1n<<BigInt(n)),"family count");assert(s.h===1&&s.root===0,"family closure/rank");family.push({n,flip:f,count:String(b),h:s.h,rawGreedy:s.raw,rootDeductions:s.root})}
for(const n of [8,16,32,64])for(const f of [-1,0]){let {d,L,G}=fam(n,1,f),s=solve(d,L,G);assert(s.count===(f<0?0n:1n<<BigInt(n))&&s.h===1&&s.root===0,"scale");scale.push({n,flip:f,count:String(s.count),h:s.h,rawOptimal:n-1,rawGreedy:s.raw})}
function inter(A,B){return rank(A)+rank(B)-rank([...A,...B])}
for(let j=0;j<100;j++){let d=5,L=Array.from({length:3},()=>BigInt(rnd(2**d))),R=Array.from({length:3},()=>BigInt(rnd(2**d))),V=[...L,...R],B=basis(V).map(r=>r[1]);let safe=B.filter(b=>has(basis(L),b)||has(basis(R),b)),U=B.filter(()=>rnd(2)),p=[BigInt(rnd(2**d))],w=inter(L,R),q=rank([...L,...U,...p])+rank([...R,...U,...p])-rank([...V,...U,...p])-rank([...U,...p]);assert(q<=w+rank(V)-safe.length+1,"MS15 width");M.ms15Cuts++}
for(let k=1;k<=6;k++)for(let a=0;a<2**(2*k);a++){let conn=false;for(let i=0;i<k;i++)if(((a>>(2*i))&3)===3)conn=true;let dual=true;for(let g=0;g<2**k;g++){let yes=false;for(let i=0;i<k;i++)if(a&(1<<(2*i+((g>>i)&1))))yes=true;if(!yes)dual=false}assert(conn===dual,"QC01 cut");M.qc01Activations++}
return {seed:20261124,metrics:M,random,family,scale}
}
console.log(JSON.stringify(check(), null, 2));
