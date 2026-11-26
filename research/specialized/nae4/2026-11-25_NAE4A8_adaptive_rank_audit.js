// NAE4A8 audit: node-compatible; deterministic seed.
let seed=20261125,checks=0;
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
function ok(x){checks++;if(!x)throw Error("check "+checks)}
function basis(xs){let b=new Map;for(let x of xs){while(x){let j=x.toString(2).length-1;if(b.has(j))x^=b.get(j);else{b.set(j,x);break}}}return [...b.entries()].sort((a,b)=>b[0]-a[0]).map(x=>x[1])}
const rk=x=>basis(x).length;
function meetdim(a,b){return rk(a)+rk(b)-rk([...a,...b])}
function q(x,W){for(let a of W){let j=1n<<BigInt(a.toString(2).length-1);if(x&j)x^=a}return x}
function meet(a,b){let r=[];for(let i=0;i<(1<<a.length);i++){let x=0n;for(let j=0;j<a.length;j++)if(i>>j&1)x^=a[j];if(rk([...b,x])===b.length)r.push(x)}return basis(r)}
function par(x){let r=0;while(x){r^=1;x&=x-1n}return r}
function pair(a,b){return (1n<<BigInt(a))^(1n<<BigInt(b))}
function obs(c){return [pair(c[0],c[1]),pair(c[0],c[2])]}
function sat(c,x){return obs(c).some(a=>par(a&x))}
function all(n,cs){let x=[];for(let i=0;i<2**n;i++)if(cs.every(c=>sat(c,BigInt(i))))x.push(BigInt(i));return x}
let jobs=0,inc=0,dec=0,exact=0;
for(let n=2;n<=8;n++)for(let j=0;j<200;j++){
 let sp=()=>basis(Array.from({length:rnd(n+1)},()=>BigInt(rnd(1<<n))));let A=sp(),B=sp(),W=sp(),k=W.length,w=meetdim(A,B),v=meetdim(A.map(a=>q(a,W)),B.map(b=>q(b,W)));
 ok(v===w+meetdim(W,[...A,...B])-meetdim(W,A)-meetdim(W,B));ok(v>=w-k&&v<=w+k);
 let I=meet(A,B);ok(I.length===w);ok(meetdim(A.map(a=>q(a,I)),B.map(b=>q(b,I)))===0);
 jobs++;if(v>w)inc++;if(v<w)dec++;if(v===w)exact++;
}
function plane(){let r=[];for(let j=0;j<3;j++)r.push([j,3+j,6+j]);for(let i=0;i<3;i++)r.push([3*i,3*i+1,3*i+2]);for(let j=0;j<3;j++){r.push([j,3+(j+1)%3,6+(j+2)%3]);r.push([j,3+(j+2)%3,6+(j+1)%3])}return r}
function key(x,I){return I.reduce((a,b,i)=>a|(par(x&b)<<i),0)}
// Local affine forced-information closure audit: finite owner truth tables on its
// 2 observation rows plus guard. Oracle guards enumerated only for tiny controls.
function close(n,cs,guard){let G=guard.slice(),changes=0;for(;;){let feasible=[];for(let i=0;i<(1<<n);i++){let x=BigInt(i);if(G.every(([a,b])=>par(a&x)===b))feasible.push(x)}if(!feasible.length)return {bad:true,changes};
 let added=false;for(let c of cs){let [a,b]=obs(c),loc=feasible.filter(x=>sat(c,x));if(!loc.length)return {bad:true,changes};
 for(let f of [a,b,a^b]){let p=par(loc[0]&f);if(loc.every(x=>par(x&f)===p)&&feasible.some(x=>par(x&f)!==p)){G.push([f,p]);changes++;added=true;break}}if(added)break}
 if(!added)return {bad:false,changes};}}
let controls=[],closureCalls=0;
for(let [name,n,cs] of [["plane",9,plane()],["plane_minus1",9,plane().slice(1)],["plane_minus2",9,plane().slice(2)],["triple",3,[[0,1,2]]]]){let solutions=all(n,cs),root=close(n,cs,[]);closureCalls++;ok(!root.bad||solutions.length===0);let splits=0,successful=0;for(let t=0;t<Math.min(20,2**cs.length);t++){let A=[],B=[];for(let c of cs)(rnd(2)?A:B).push(c);let U=basis(A.flatMap(obs)),V=basis(B.flatMap(obs)),I=meet(U,V);let L=new Map,R=new Map;for(let x of all(n,A))L.set(key(x,I),x);for(let x of all(n,B))R.set(key(x,I),x);let K=[...L.keys()].filter(k=>R.has(k));ok((K.length>0)===(solutions.length>0));for(let k of K){let x=L.get(k),y=R.get(k),glued=null;for(let i=0;i<2**n;i++){let z=BigInt(i);if(U.every(a=>par(a&z)===par(a&x))&&V.every(a=>par(a&z)===par(a&y))){glued=z;break}}ok(glued!==null&&cs.every(c=>sat(c,glued)));}for(let k=0;k<2**I.length;k++){let C=close(n,cs,I.map((a,i)=>[a,(k>>i)&1]));closureCalls++;ok(!C.bad||!K.includes(k))}splits++;successful+=K.length>0}controls.push({name,solutions:solutions.length,splits,successful,initialClosure:root})}
function torus(L){let p=L*L,idx=(x,y)=>((x+L)%L)*L+(y+L)%L;let s=[[0,0],[1,0],[0,1],[1,1]],cs=[];for(let [a,b] of s)for(let x=0;x<L;x++)for(let y=0;y<L;y++)cs.push([idx(x,y),p+idx(x+a,y+b),2*p+idx(x+2*a,y+2*b)]);return cs}
function verify(cs,n){let pairs=new Set;for(let j=0;j<4;j++){let a=cs.slice(j*n/3,(j+1)*n/3).flat();ok(a.length===n&&new Set(a).size===n)}for(let c of cs)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let s=[c[i],c[j]].sort((a,b)=>a-b).join(",");ok(!pairs.has(s));pairs.add(s)}return pairs}
function width(cs,n){let m=cs.length;function cc(indices){let p=Array.from({length:n},(_,i)=>i),count=n;function f(i){while(p[i]!==i){p[i]=p[p[i]];i=p[i]}return i}for(let i of indices){let [a,b,c]=cs[i];for(let v of [b,c]){let x=f(a),y=f(v);if(x!==y){p[x]=y;count--}}}return count}let all=Array.from({length:m},(_,i)=>i),C=cc(all),w=0,Q=all.map(i=>[i]);while(Q.length>1){for(let s of Q){let S=new Set(s);w=Math.max(w,n-cc(s)-cc(all.filter(i=>!S.has(i)))+C)}let P=[];for(let i=0;i<Q.length;i+=2)P.push(Q[i+1]?[...Q[i],...Q[i+1]]:Q[i]);Q=P}return w}
let grid=[];
for(let L of [5,7,11,17]){let p=L*L,n=3*p,cs=torus(L),pairs=verify(cs,n);let witness=((1n<<BigInt(p))-1n)<<BigInt(p);ok(cs.every(c=>sat(c,witness)));
 for(let x=0;x<L;x++)for(let y=0;y<L;y++){let i=x*L+y;ok(pairs.has(i+","+(p+i)));if(x+1<L)ok(pairs.has(i+","+(p+(x+1)*L+y)));if(y+1<L)ok(pairs.has(i+","+(p+x*L+y+1)))}
 // add plane with one swapped owner in partition 0, preserve unsat 11-owner core.
 let pl=plane(); // plane partitions in order vertical, horizontal, two slopes interleaved
 pl=[...pl.slice(0,6),pl[6],pl[8],pl[10],pl[7],pl[9],pl[11]];
 let mixed=[];for(let j=0;j<4;j++)mixed.push(...cs.slice(j*p,(j+1)*p).map(c=>c.slice()),...pl.slice(j*3,j*3+3).map(c=>c.map(x=>x+n)));[mixed[0][0],mixed[p][0]]=[mixed[p][0],mixed[0][0]];let mp=verify(mixed,n+9);ok(all(9,pl.slice(1)).length===0);
 for(let x=1;x<L;x++)for(let y=1;y<L;y++){let i=x*L+y;ok(mp.has(i+","+(p+i)));if(x+1<L)ok(mp.has(i+","+(p+(x+1)*L+y)));if(y+1<L)ok(mp.has(i+","+(p+x*L+y+1)))}
 grid.push({L,n,clauseOrderWidth:width(cs,n),SAT_witness:true,mixedN:n+9,mixedWidth:width(mixed,n+9),UNSAT_core:true,gridMinorSize:L,mixedGridMinorSize:L-1});
}
console.log(JSON.stringify({seed:20261125,checks,jobs,inc,dec,exact,closureCalls,controls,grid}));