function run(){
const par=x=>{let p=0;while(x){x&=x-1n;p^=1}return p};
const key=x=>x.map(([a,b])=>a.toString(16)+":"+b).join(",");
let calls=0, checks=0;
function canon(rows,n){calls++;let t=rows.map(([a,b])=>[a,b]),j=0;for(let i=n-1;i>=0;i--){let z=t.findIndex(([a],k)=>k>=j&&((a>>BigInt(i))&1n));if(z<0)continue;[t[j],t[z]]=[t[z],t[j]];for(let k=0;k<t.length;k++)if(k!==j&&((t[k][0]>>BigInt(i))&1n)){t[k][0]^=t[j][0];t[k][1]^=t[j][1]}j++}return t.slice(j).some(([a,b])=>b)?null:t.slice(0,j)}
const space=(u,n)=>canon(u.map(a=>[a,0]),n).map(x=>x[0]);
function evalrow(a,P){let b=0;for(const [v,w] of P)if(a!==0n&&((a>>BigInt(v.toString(2).length-1))&1n)){a^=v;b^=w}return a===0n?b:null}
function intersect(A,B,n){const all=[...A,...B],base=new Map(),out=[];for(let i=0;i<all.length;i++){let a=all[i],tag=1n<<BigInt(i);while(a){let p=a.toString(2).length-1;if(!base.has(p)){base.set(p,[a,tag]);break}const [b,c]=base.get(p);a^=b;tag^=c}if(!a){let v=0n;for(let j=0;j<A.length;j++)if((tag>>BigInt(j))&1n)v^=A[j];if(v)out.push(v)}}return space(out,n)}
function solve(G,n){if(G===null)return null;let x=0n;for(const [a,b] of [...G].reverse()){let p=1n<<BigInt(a.toString(2).length-1);if(par(a&x)!==b)x^=p}return x}
function holds(P,x){return P.every(([a,b])=>par(a&x)===b)}
function closure(P,G,n){G=canon(G,n);if(!G)return {unsat:true};let change=true,scans=0;while(change){change=false;for(const p of P){scans++;let r=canon([...G,...p],n);if(!r)continue;if(r.length===G.length)return {unsat:true,scans};if(r.length===G.length+1){let q=p.find(([a])=>evalrow(a,G)===null);G=canon([...G,[q[0],q[1]^1]],n);change=true;break}}}return {G,scans}}
function discover(P,n){
let M=P.length,U=P.map(p=>p.map(x=>x[0])),uniq=new Map();
for(let i=0;i<M;i++)for(let j=0;j<i;j++){let I=intersect(U[i],U[j],n);if(I.length)uniq.set(I.map(x=>x.toString(16)).join(","),I)}
let L=[...uniq.values()].sort((a,b)=>a.length-b.length),atoms=[];
for(const a of L)if(!atoms.some(b=>b.every(x=>evalrow(x,a.map(y=>[y,0]))!==null)))atoms.push(a);
if(atoms.length<2)return {reason:"no atoms",atoms:atoms.length};
let contains=U.map(u=>atoms.map(a=>a.every(v=>evalrow(v,u.map(x=>[x,0]))!==null)));
let co=atoms.map((_,i)=>atoms.map((_,j)=>i===j||contains.some(x=>x[i]&&x[j])));
let left=new Set(atoms.map((_,i)=>i)),groups=[];
while(left.size){let i=left.values().next().value,g=[i];left.delete(i);for(let k=0;k<g.length;k++)for(const j of [...left])if(!co[g[k]][j]){left.delete(j);g.push(j)}groups.push(g)}
if(groups.length<2||groups.some(g=>g.length<2||g.some(i=>g.some(j=>i!==j&&co[i][j]))))return {reason:"not multipartite",atoms:atoms.length};
let S=groups.map(g=>space(g.flatMap(i=>atoms[i]),n));
if(space(S.flat(),n).length!==S.reduce((a,x)=>a+x.length,0))return {reason:"not direct sum",atoms:atoms.length};
let lists=groups.map(()=>new Map()),tupleSet=new Set();
for(let i=0;i<M;i++){let tuple=[],rebuild=[];for(let j=0;j<groups.length;j++){let a=groups[j].filter(k=>contains[i][k]);if(a.length!==1)return {reason:"not single atom per block",atoms:atoms.length};let p=atoms[a[0]].map(v=>[v,evalrow(v,P[i])]);p=canon(p,n);let k=key(p);lists[j].set(k,p);tuple.push(k);rebuild.push(...p)}
if(key(canon(rebuild,n))!==key(P[i]))return {reason:"packet mismatch",atoms:atoms.length};tupleSet.add(JSON.stringify(tuple))}
if(lists.reduce((a,b)=>a*BigInt(b.size),1n)!==BigInt(tupleSet.size))return {reason:"not full product",atoms:atoms.length};
return {atoms:atoms.length,lists:lists.map(m=>[...m.values()]),S,groups:groups.map(g=>g.length)}
}
function projectedGuard(G,S,n){let I=intersect(G.map(x=>x[0]),S,n);return canon(I.map(a=>[a,evalrow(a,G)]),n)}
function transform(P,n,seed){let state=seed>>>0;let rand=()=>{state=(Math.imul(state,1664525)+1013904223)>>>0;return state};let ops=[];for(let i=0;i<8*n;i++){let a=rand()%n,b=(rand()>>>8)%n;if(a!==b)ops.push([a,b])}return P.map(p=>canon(p.map(([v,b])=>{for(let [i,j] of ops)if((v>>BigInt(i))&1n)v^=1n<<BigInt(j);return [v,b]}),n))}
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
function src(shift,flip=false){return fano.map(([a,b,c],i)=>[[ (1n<<BigInt(a+shift))^(1n<<BigInt(b+shift)),flip&&i===0?1:0],[(1n<<BigInt(a+shift))^(1n<<BigInt(c+shift)),0]])}
function product(lists,n){let z=[[]];for(let L of lists)z=z.flatMap(a=>L.map(b=>[...a,...b]));return z.map(p=>canon(p,n))}
let result=[];
for(let flip of [false,true])for(let seed of [23,45,89]){
let n=14,P=transform(product([src(0,flip),src(7,flip)],n),n,seed),D=discover(P,n);if(!D.lists)throw Error(JSON.stringify(D));let raw=0,valid=0;let gcase=[];
for(let g of [[],[[3n,0]],[[0x221n,1],[0x184n,0]],[[1n,0],[1n,1]]]){
let G=canon(g,n),C=closure(P,g,n),direct=0,found=false,lift=null;
if(G)for(let x=0n;x<(1n<<BigInt(n));x++){if(holds(G,x)&&P.every(p=>!holds(p,x)))direct++}
if(!C.unsat){for(let j=0;j<D.lists.length;j++){let pg=projectedGuard(C.G,D.S[j],n),cc=closure(D.lists[j],pg,n);if(cc.unsat)continue;for(let mask=0;mask<2**D.S[j].length;mask++){let e=D.S[j].map((a,i)=>[a,(mask>>i)&1]);let z=solve(canon([...C.G,...e],n),n);checks++;if(z!==null&&D.lists[j].every(p=>!holds(p,z))){if(!holds(G,z)||!P.every(p=>!holds(p,z)))throw Error("bad lift");found=true;lift=z.toString(16);break}}if(found)break}}
if(found!==!!direct)throw Error("decision mismatch");gcase.push({guard:g.map(([a,b])=>[a.toString(16),b]),models:direct,found,lift,closureScans:C.scans||0})}
let hole=discover(P.slice(1),n);result.push({flip,seed,atoms:D.atoms,groups:D.groups,childRanks:D.S.map(x=>x.length),parentMass:P.reduce((s,p)=>s+p.length,0),childCredit:D.lists.reduce((s,L)=>s+1+L.reduce((t,p)=>t+p.length,0),0),cases:gcase,holeDecline:!hole.lists,holeReason:hole.reason})
}
return {result,gaussianCalls:calls,guardLiftTrials:checks}
}
console.log(JSON.stringify(run(),null,2));
