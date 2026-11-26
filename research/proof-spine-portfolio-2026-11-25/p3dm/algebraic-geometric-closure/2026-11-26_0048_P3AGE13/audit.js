console.log(JSON.stringify((function audit(){
const bit=i=>1n<<BigInt(i),has=(v,i)=>!!(v&bit(i)),range=n=>Array.from({length:n},(_,i)=>i),hi=v=>v.toString(2).length-1;
const ok=(x,m)=>{if(!x)throw Error(m)};
function bits(v){let a=[];while(v){let t=v&-v;a.push(hi(t));v^=t}return a}
function reduce(B,v,c=0n){while(v){let p=B.get(hi(v));if(!p)break;v^=p[0];c^=p[1]}return [v,c]}
function insert(B,v,c=0n){let [w,d]=reduce(B,v,c);if(!w)return false;B.set(hi(w),[w,d]);return true}
function basis(A,S){let B=new Map;for(let i of S)insert(B,A[i]);return B}
const rank=(A,S)=>basis(A,S).size;
function cut(A,S){let q=new Set(S);return rank(A,S)+rank(A,range(A.length).filter(i=>!q.has(i)))-rank(A,range(A.length))}
function mincut(A,P,Q,st){let E=range(A.length).filter(i=>!P.includes(i)&&!Q.includes(i)),I=new Set;
function oracle(F){let B=basis(A,F),D=new Map;for(let i of I)ok(insert(B,A[i],bit(i)),"independence");for(let i of E)if(!I.has(i)){let [w,c]=reduce(B,A[i]);D.set(i,[!!w,c])}return D}
for(;;){st.aug++;let D=oracle(P),F=oracle(Q),q=[],p=new Map;for(let [i,[f]] of D)if(f){q.push(i);p.set(i,-1)}
let sink=-1;for(let h=0;h<q.length;h++){let x=q[h];if(!I.has(x)&&F.get(x)[0]){sink=x;break}if(I.has(x)){for(let [y,[f,c]] of D)if((f||has(c,x))&&!p.has(y)){p.set(y,x);q.push(y)}}else{let [f,c]=F.get(x);for(let y of I)if((f||has(c,y))&&!p.has(y)){p.set(y,x);q.push(y)}}}
if(sink>=0){for(let x=sink;x!==-1;x=p.get(x))I.has(x)?I.delete(x):I.add(x);continue}
let Z=[...P,...E.filter(i=>!p.has(i))],v=cut(A,Z);ok(v===I.size+rank(A,P)+rank(A,Q)-rank(A,range(A.length)),"dual");return {Z,v}}
}
function acquire(A,k,st){let K=3*k+1,B=new Map,adj=A.map(()=>0n);
for(let i=0;i<A.length;i++){let [w,c]=reduce(B,A[i],bit(i));if(w)B.set(hi(w),[w,c]);else for(let j of bits(c^bit(i))){adj[i]|=bit(j);adj[j]|=bit(i)}}
function go(S){let f=cut(A,S);st.width=Math.max(st.width,f);ok(f<=K,"cut cap");if(S.length<=1)return {S};let L,H;if(f<K){L=[S[0]];H=S.slice(1)}else{let mask=S.reduce((p,i)=>p|bit(i),0n),b=new Map,X=[];
for(let i of range(A.length))if(!has(mask,i)&&insert(b,adj[i]&mask))X.push(i);ok(X.length===f,"fundamental cut");
if(X.length>16){st.refusal="test cap";return null}
let choices=range(2**(X.length-1)).filter(x=>x);choices.sort((a,b)=>Math.abs(2*bits(BigInt(a)).length-X.length)-Math.abs(2*bits(BigInt(b)).length-X.length));let hit=false;
for(let v of choices){let P=X.filter((_,i)=>(v>>i)&1),Q=X.filter((_,i)=>!((v>>i)&1));if(++st.cuts>5000){st.refusal="test cap";return null}let z=mincut(A,P,Q,st);if(z.v<Math.min(P.length,Q.length)){L=S.filter(i=>z.Z.includes(i));H=S.filter(i=>!z.Z.includes(i));ok(L.length&&H.length&&cut(A,L)<f&&cut(A,H)<f,"split lemma");hit=true;break}}
if(!hit){st.refusal="well-linked set";return null}}
let l=go(L);if(!l)return null;let h=go(H);if(!h)return null;return {S,l,h}}
return go(range(A.length))}
const incidence=(T,n)=>T.map(t=>t.reduce((p,x,c)=>p|bit(c*n+x),0n));
function close(A,T,n,target,G){let s=A.map(()=>-1),rounds=0;
for(let [i,v] of G){if(s[i]!==-1&&s[i]!==v)return null;s[i]=v}
for(;;){rounds++;let before=s.filter(x=>x!==-1).length;
for(let j of bits(target)){let R=range(A.length).filter(i=>has(A[i],j)),P=R.filter(i=>s[i]===1),L=R.filter(i=>s[i]===-1);if(P.length>1||(!P.length&&!L.length))return null;if(P.length)for(let i of L)s[i]=0;else if(L.length===1)s[L[0]]=1}
if(s.filter(x=>x!==-1).length!==before)continue;
let selected=range(A.length).filter(i=>s[i]===1),live=range(A.length).filter(i=>s[i]===-1),b=selected.reduce((p,i)=>p^A[i],target),B=new Map,free=0n;
for(let j=0;j<live.length;j++){let [w,c]=reduce(B,A[live[j]],bit(j));if(w)B.set(hi(w),[w,c]);else free|=c}
let [r,w]=reduce(B,b);if(r)return null;for(let j=0;j<live.length;j++)if(!has(free,j))s[live[j]]=has(w,j)?1:0;
if(s.filter(x=>x!==-1).length!==before)continue;
for(let [a,c] of [[0,1],[0,2],[1,2]]){let edges=new Map,match=new Map,U=bits(b).filter(i=>i>=a*n&&i<(a+1)*n).map(i=>i-a*n),V=bits(b).filter(i=>i>=c*n&&i<(c+1)*n).map(i=>i-c*n);if(U.length!==V.length)return null;
for(let i of live){let u=T[i][a],v=T[i][c];if(!edges.has(u))edges.set(u,[]);edges.get(u).push(v)}
function aug(u,S){for(let v of edges.get(u)||[]){if(S.has(v))continue;S.add(v);if(!match.has(v)||aug(match.get(v),S)){match.set(v,u);return true}}return false}
for(let u of U)if(!aug(u,new Set))return null;let adj=new Map(U.map(u=>[u,[]]));for(let i of live)adj.get(T[i][a]).push(match.get(T[i][c]));
let reach=new Map;for(let u of U){let q=[u],S=new Set(q);for(let h=0;h<q.length;h++)for(let v of adj.get(q[h]))if(!S.has(v)){S.add(v);q.push(v)}reach.set(u,S)}
for(let i of live)if(!reach.get(match.get(T[i][c])).has(T[i][a]))s[i]=0}
if(s.filter(x=>x!==-1).length===before)return {live,selected,b,rounds}
}}
function solve(T,n,k,G=[],raw=false){let A=incidence(T,n),target=(1n<<BigInt(3*n))-1n,C=raw?{live:range(A.length),selected:[],b:target,rounds:0}:close(A,T,n,target,G),st={width:0,cuts:0,aug:0,pairs:0,maxTable:0,rounds:C?.rounds||0};
if(!C)return {count:"0",st};let M=C.live.map(i=>A[i]),b=C.b;if(!M.length)return {count:b?"0":"1",st};
let tr=acquire(M,k,st);if(!tr)return {count:null,st};
function dp(t){let S=new Set(t.S),B=basis(M,range(M.length).filter(i=>!S.has(i))),out=new Map;function add(z,c,w){if(reduce(B,b^z)[0])return;let old=out.get(z);out.set(z,[c+(old?old[0]:0n),old?old[1]:w])}
if(!t.l){add(0n,1n,0n);add(M[t.S[0]],1n,bit(t.S[0]))}else{let L=dp(t.l),H=dp(t.h);for(let [z,[c,w]] of L)for(let [y,[d,v]] of H){st.pairs++;if(!(z&y))add(z|y,c*d,w|v)}}
ok(out.size<=2**cut(M,t.S),"rank table cap");st.maxTable=Math.max(st.maxTable,out.size);return out}
let ans=dp(tr).get(b);if(!ans)return {count:"0",st};let w=[...C.selected,...bits(ans[1]).map(i=>C.live[i])],z=0n;for(let i of w){ok(!(z&A[i]),"overlap");z|=A[i]}ok(z===target&&G.every(([i,v])=>w.includes(i)===!!v),"witness");return {count:String(ans[0]),st}}
function truth(T,n,G=[]){let A=incidence(T,n),b=(1n<<BigInt(3*n))-1n,c=0;function rec(j,z,W){if(j===n){if(z===b&&G.every(([i,v])=>W.includes(i)===!!v))c++;return}for(let i of range(T.length))if(T[i][0]===j&&!(z&A[i]))rec(j+1,z|A[i],[...W,i])}rec(0,0n,[]);return String(c)}
let seed=81377;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return (seed>>>8)%n}function shuffle(a){for(let i=a.length-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
const O=range(8).map(i=>[i>>2,(i>>1)&1,i&1]),U="000 002 010 011 021 022 100 101 111 201 202 221".split(" ").map(s=>Array.from(s,Number)),V=[...U,[1,1,0]];
let cuts=0,raw=0,closed=0,guarded=0,refusals=0;
for(let j=0;j<120;j++){let A=range(3+rnd(7)).map(()=>BigInt(rnd(64))),v=shuffle(range(A.length)),P=v.slice(0,1+rnd(2)),Q=v.slice(P.length,P.length+1),E=v.filter(i=>!P.includes(i)&&!Q.includes(i)),z=mincut(A,P,Q,{aug:0}),best=Infinity;for(let x=0;x<2**E.length;x++)best=Math.min(best,cut(A,[...P,...E.filter((_,i)=>(x>>i)&1)]));ok(z.v===best,"brute mincut");cuts++}
for(let s=0;s<256;s++){let T=O.filter((_,i)=>(s>>i)&1),ref=truth(T,2);for(let b of [false,true]){let r=solve(T,2,2,[],b);if(r.count===null){refusals++;continue}ok(r.count===ref,"small");b?raw++:closed++}if(T.length){let G=[[rnd(T.length),rnd(2)]],r=solve(T,2,2,G);if(r.count!==null){ok(r.count===truth(T,2,G),"guard");guarded++}else refusals++}}
for(let T of [U,V])for(let j=0;j<32;j++){let G=j?[[rnd(T.length),rnd(2)],[rnd(T.length),rnd(2)]]:[],r=solve(T,3,2,G);if(r.count!==null){ok(r.count===truth(T,3,G),"UV guard");guarded++}else refusals++}
function chain(k,B=null){let groups=[],n=0;for(let j=0;j<k;j++){let T=j===0&&B?B:O;groups.push(T.map(t=>t.map(x=>x+n)));n+=j===0&&B?3:2}for(let j=0;j+1<k;j++){let x=B?groups[j].length-1:1,y=B?0:2;[groups[j][x][1],groups[j+1][y][1]]=[groups[j+1][y][1],groups[j][x][1]]}return [groups,n]}
function transfer(groups){let owner=new Map;for(let j=0;j<groups.length;j++)for(let t of groups[j]){if(!owner.has(t[1]))owner.set(t[1],new Set);owner.get(t[1]).add(j)}let prev=new Map([["",1n]]);
for(let j=0;j<groups.length;j++){let L=[],R=[],P=[];for(let [v,S] of owner)if(S.has(j)){if(S.has(j-1))L.push(v);else if(S.has(j+1))R.push(v);else P.push(v)}L.sort((a,b)=>a-b);R.sort((a,b)=>a-b);let X=[...new Set(groups[j].map(t=>t[0]))],next=new Map;function rec(i,Y,Z){if(i===X.length){if(!P.every(v=>Y.has(v)))return;let a=L.filter(v=>!Y.has(v)).join(","),b=R.filter(v=>Y.has(v)).join(","),q=prev.get(a)||0n;if(q)next.set(b,(next.get(b)||0n)+q);return}for(let t of groups[j])if(t[0]===X[i]&&!Y.has(t[1])&&!Z.has(t[2]))rec(i+1,new Set([...Y,t[1]]),new Set([...Z,t[2]]))}rec(0,new Set,new Set);prev=next}return String(prev.get("")||0n)}
let scale=[],neighbors=[],stress=[];
for(let k of [1,2,4,8,16,32,64]){let [g,n]=chain(k),T=g.flat(),ref=transfer(g),r=solve(T,n,2);if(r.count!==null)ok(r.count===ref,"ordered chain");scale.push({k,m:T.length,count:r.count,reference:ref,...r.st});if(k<=8){let P=shuffle(T.slice()),q=solve(P,n,1);if(q.count!==null)ok(q.count===ref,"shuffled k1");let a=solve(P,n,2);if(a.count!==null)ok(a.count===ref,"shuffled k2");stress.push({k,m:T.length,reference:ref,k1:q,k2:a})}}
for(let k of [1,2,4,8])for(let [name,B] of [["U",U],["V",V]]){let [g,n]=chain(k,B),T=g.flat(),r=solve(T,n,2),ref=transfer(g);if(r.count!==null)ok(r.count===ref,"neighbor");neighbors.push({name,k,m:T.length,count:r.count,reference:ref,...r.st})}
return {seed:81377,bruteMincuts:cuts,smallRaw:raw,smallClosed:closed,guarded,refusals,scale,stress,neighbors}
})(),null,2));
