// Node.js, deterministic C08-04 audit
function audit(){
let checks=0,seed=261126;function ok(x,msg){checks++;if(!x)throw Error(msg||"assertion "+checks)}
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
function shuffle(a){for(let i=a.length-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
function cyclic(p){return Array.from({length:4},(_,s)=>Array.from({length:p},(_,i)=>[i,p+(i+s)%p,2*p+(i+2*s)%p]))}
const AG=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]];
function auth(F,n){let seen=new Set;ok(F.length===4);for(let P of F){let counts=Array(n).fill(0);for(let c of P){ok(c.length===3&&new Set(c).size===3);for(let v of c){ok(v>=0&&v<n);counts[v]++}for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let k=Math.min(c[i],c[j])*n+Math.max(c[i],c[j]);ok(!seen.has(k));seen.add(k)}}ok(counts.every(x=>x===1))}}
function components(C,n){let a=Array.from({length:n},(_,i)=>i);function f(x){while(a[x]!==x){a[x]=a[a[x]];x=a[x]}return x}for(let c of C)for(let v of c)a[f(v)]=f(c[0]);return new Set(a.map((_,i)=>f(i))).size}
function rank2(rows){let b=new Map;for(let v of rows){while(v){let k=v.toString(2).length-1;if(!b.has(k)){b.set(k,v);break}v^=b.get(k)}}return b.size}
const M=cyclic(5).map(P=>P.map(c=>c.reduce((a,v)=>a|(1<<v),0))),all=M.flat(),w=239;
const V=(x,C=all)=>C.reduce((a,c)=>a+((x&c)===0||(x&c)===c),0);
function chart(P,drop=-1){let X=[0];for(let [i,m] of P.entries()){let a=i===drop?[...Array(15).keys()].filter(v=>m&(1<<v)).map(v=>1<<v):[m];for(let d of a)X=X.concat(X.map(x=>x^d))}return X}
const X=M.map(P=>chart(P)),moves=[...new Set(X.flat())];ok(V(w)===1);
const one=X.map(A=>A.filter(d=>V(w^d)===0).length);ok(one.every(x=>x===0));
let seen=new Set([w]),queue=[w];for(let i=0;i<queue.length;i++)for(let d of moves){let t=queue[i]^d;if(!seen.has(t)&&V(t)<=1){seen.add(t);queue.push(t)}}ok(queue.length===20&&queue.every(x=>V(x)===1));for(let x of queue)for(let d of moves)ok(V(x^d)>1||seen.has(x^d));
const path=[239,1767,997];ok(V(path[0])===1&&V(path[1])===2&&V(path[2])===0);for(let i=1;i<path.length;i++)ok(moves.includes(path[i]^path[i-1]));
ok(V(255)===0&&((255^w)===16));ok(chart(M[0],4).includes(255^w));
let core=all.filter((_,i)=>i!==2);let robust=M.map((P,s)=>chart(P,s===0?2:-1).filter(d=>V(w^d,core)===0).length);ok(robust.every(x=>x===0));
function bits(w,n){return Array.from({length:n},(_,i)=>(w>>>i)&1)}
function viol(F,x){return F.flat().filter(c=>c.every(v=>x[v]===x[c[0]])).length}
function splice(F,G,n,i=2,j=0){let H=F.map((P,s)=>P.map(c=>c.slice()).concat(G[s].map(c=>c.map(v=>v+n))));let k=F[0].length+j;[H[0][i][0],H[0][k][0]]=[H[0][k][0],H[0][i][0]];return H}
function relabel(F,n){let p=shuffle(Array.from({length:n},(_,i)=>i));return{F:F.map(P=>shuffle(P.map(c=>shuffle(c.map(v=>p[v]))))),p}}
function gf3(F,n){let a=F.flat().map(c=>{let x=new Uint8Array(n);for(let v of c)x[v]=1;return x}),rank=0,piv=[];for(let j=0;j<n;j++){let i=rank;while(i<a.length&&!a[i][j])i++;if(i===a.length)continue;[a[rank],a[i]]=[a[i],a[rank]];if(a[rank][j]===2)for(let k=j;k<n;k++)a[rank][k]=2*a[rank][k]%3;for(let i=0;i<a.length;i++)if(i!==rank&&a[i][j]){let q=a[i][j];for(let k=j;k<n;k++)a[i][k]=(a[i][k]+6-q*a[rank][k])%3}piv.push(j);rank++}let P=new Set(piv),free=Array.from({length:n},(_,i)=>i).filter(i=>!P.has(i)),b=free.map(j=>{let x=Array(n).fill(0);x[j]=1;for(let i=0;i<rank;i++)x[piv[i]]=(3-a[i][j])%3;return x});if(b.length>8)return{nullity:b.length,witness:null};for(let w=0;w<3**b.length;w++){let t=w,x=Array(n).fill(0);for(let i=0;i<b.length;i++){let d=t%3;t=Math.floor(t/3);for(let j=0;j<n;j++)x[j]=(x[j]+d*b[i][j])%3}if(F.flat().every(c=>new Set(c.map(v=>x[v])).size===3))return{nullity:b.length,witness:x.map(v=>v===0?0:1)}}return{nullity:b.length,witness:null}}
let cover=[],joined=[];
for(let p of [5,7,13,31,127,1021]){let F=cyclic(p),n=3*p;auth(F,n);for(let i=0;i<4;i++)for(let j=i+1;j<4;j++)ok(components(F[i].concat(F[j]),n)===1);let r=n<=381?rank2(F.flat().map(c=>c.reduce((a,v)=>a|(1n<<BigInt(v)),0n))):null;if(r!==null)ok(r===n-2);let x=Array.from({length:n},(_,v)=>v<p?1:v<2*p?0:1);ok(viol(F,x)===0);cover.push({p,n,rank:r,log2MinimumExplicitChartCover:p});
let G=splice(cyclic(5),F,15),N=n+15;auth(G,N);ok(components(G.flat(),N)===1);let w0=bits(w,15).concat(x),sat=Array.from({length:15},(_,v)=>v<5?1:v<10?0:1).concat(x);ok(viol(G,w0)===1);ok(viol(G,sat)===0);let {F:H,p:perm}=relabel(G,N);auth(H,N);let y=Array(N);sat.forEach((a,i)=>y[perm[i]]=a);ok(viol(H,y)===0);let g=N<=396?gf3(H,N):null;if(g){ok(g.nullity===3&&g.witness&&viol(H,g.witness)===0)}let repair=w0.slice();repair[4]^=1;ok(viol(G,repair)===0);joined.push({n:N,violations:1,allFourFullChartsImpossibleByFixedCore: true,sourceOnlyGF3Nullity:g?.nullity??null,sourceOnlyWitness:!!g?.witness})}
function ring(no){let F=[[],[],[],[]];for(let t=0;t<2;t++)for(let s=0;s<4;s++)for(let i=0;i<3;i++){let c=AG[s][i].map(v=>v+9*t);if(s===0&&(i===0||(!no&&i===1)))c[2]=9*(1-t)+AG[s][i][2];F[s].push(c)}return F}
let controls=[];for(let p of [5,31,127,1021]){let F=cyclic(p),x=Array.from({length:3*p},(_,v)=>v<p?0:v<2*p?0:1);for(let no of [false,true]){let R=ring(no),G=splice(R,F,18,2,0),N=18+3*p;auth(G,N);ok(components(G.flat(),N)===1);if(no){let C=G.flat().filter(c=>c.every(v=>v>=9&&v<18));ok(C.length===11);for(let w=0;w<512;w++)ok(C.some(c=>c.every(v=>((w>>(v-9))&1)===((w>>(c[0]-9))&1))))}else{let u=[0,0,0,1,1,1,0,0,1,1,1,1,0,0,0,0,0,1];ok(viol(G,u.concat(x))===0)}controls.push({n:N,status:no?"UNSAT":"SAT",method:no?"11-line core exhaustive certificate":"explicit source witness"})}}
return{checks,seed:261126,core:{word:w,violated:all.map((c,i)=>V(w,[c])?i:-1).filter(i=>i>=0),fullChartCounts:one,relaxedSpliceChartCounts:robust,plateau:queue.sort((a,b)=>a-b),moves:moves.length,path},cover,joined,controls};
}
console.log(JSON.stringify(audit(),null,2));
