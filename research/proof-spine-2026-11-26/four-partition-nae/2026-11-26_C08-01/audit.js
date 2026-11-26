// Node.js: node audit.js
function audit(){
let checks=0,seed=20261126;function ok(x,msg){checks++;if(!x)throw Error(msg||"assertion "+checks)}function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
function basis(vs){let B=[];for(let v of vs){for(let b of B)if((v^b)<v)v^=b;if(v){B.push(v);B.sort((a,b)=>a>b?-1:a<b?1:0)}}return B}
function red(v,B){for(let b of B)if((v^b)<v)v^=b;return v}
function deficiency(U){let d=0;for(let s=1;s<2**U.length;s++){let a=U.filter((_,i)=>s>>i&1);d=Math.max(d,a.length-basis(a.flat()).length)}return d}
function contract(U,I,W){let B=basis(W);return U.filter((_,i)=>!I.includes(i)).map(L=>L.map(a=>red(a,B)))}
const AG=[[[0,1,2],[3,4,5],[6,7,8]],[[0,3,6],[1,4,7],[2,5,8]],[[0,4,8],[1,5,6],[2,3,7]],[[0,5,7],[1,3,8],[2,4,6]]];
const rows=c=>[(1n<<BigInt(c[0]))^(1n<<BigInt(c[1])),(1n<<BigInt(c[0]))^(1n<<BigInt(c[2]))];
let U=AG.flat().map(rows),D=deficiency(U);ok(D===4);let agChildren=[];for(let i=0;i<U.length;i++)for(let a of U[i]){let d=deficiency(contract(U,[i],[a]));ok(d>=D&&d<=D+1);agChildren.push(d)}
let random={cases:0,strictDrops:0,independent:0,rankLoss:0};for(let q=0;q<180;q++){let m=2+rnd(7),r=1+rnd(6),U=Array.from({length:m},()=>[BigInt(rnd(2**r)),BigInt(rnd(2**r))]);let D=deficiency(U),I=Array.from({length:m},(_,i)=>i).filter(()=>rnd(2)===0);let W=I.map(i=>U[i][rnd(2)]),rank=basis(W).length,d=deficiency(contract(U,I,W));ok(d>=D-(I.length-rank));ok(d<=D+rank);if(rank===I.length){ok(d>=D);random.independent++}if(d<D)random.strictDrops++;random.rankLoss+=I.length-rank;random.cases++}
function evalWord(c,x){return (x[c[0]]^x[c[1]])+2*(x[c[0]]^x[c[2]])}
function fit(F,x,s){return F.every((c,i)=>evalWord(c,x)!==s[i])}
const F=AG.flat();let models=Array.from({length:512},(_,w)=>Array.from({length:9},(_,i)=>w>>i&1)),sign=Array(12).fill(0);ok(!models.some(x=>fit(F,x,sign)));let oneBitNo=0;for(let i=0;i<12;i++)for(let b of [1,2]){let s=sign.slice();s[i]=b;ok(!models.some(x=>fit(F,x,s)));oneBitNo++}
let p=models.find(x=>F.filter(c=>evalWord(c,x)===0).length===2);ok(!!p);let t=F.map(c=>evalWord(c,p)===0?1:0);ok(t.filter(Boolean).length===2&&fit(F,p,t));
function build(k,yes){let P=[[],[],[],[]];for(let i=0;i<k;i++)for(let j=0;j<4;j++)for(let l=0;l<3;l++){let c=AG[j][l].map(v=>9*i+v);if(j===0&&(l===0||(yes&&l===1)))c[2]=9*((i+1)%k)+AG[j][l][2];P[j].push(c)}return P}
function auth(P,n){let pairs=new Set;for(let part of P){let cnt=Array(n).fill(0);for(let c of part){ok(new Set(c).size===3);for(let v of c){ok(v>=0&&v<n);cnt[v]++}for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let a=Math.min(c[i],c[j]),b=Math.max(c[i],c[j]),key=a*n+b;ok(!pairs.has(key));pairs.add(key)}}ok(cnt.every(a=>a===1))}
let a=Array.from({length:n},()=>[]);for(let c of P.flat())for(let v of c)for(let u of c)if(u!==v)a[v].push(u);let Q=[0],V=new Set(Q);for(let i=0;i<Q.length;i++)for(let u of a[Q[i]])if(!V.has(u)){V.add(u);Q.push(u)}ok(V.size===n)}
function sourceOnly(P,n){ // exact bounded component extraction and parity closure for admitted ring family
let a=Array.from({length:n},()=>[]);for(let c of P.slice(1).flat())for(let v of c)for(let u of c)if(u!==v)a[v].push(u);
let block=Array(n).fill(-1),B=[];for(let v=0;v<n;v++)if(block[v]<0){let Q=[v],i=B.length;block[v]=i;for(let j=0;j<Q.length;j++)for(let u of a[Q[j]])if(block[u]<0){block[u]=i;Q.push(u)}B.push(Q)}
let internal=B.map(()=>[]),external=[];for(let c of P.flat()){if(c.every(v=>block[v]===block[c[0]]))internal[block[c[0]]].push(c);else external.push(c)}
let phase=Array(n).fill(-1),offset=Array(n).fill(-1),locals=[];for(let i=0;i<B.length;i++){let V=B[i],id=new Map(V.map((v,j)=>[v,j])),C=internal[i].map(c=>c.map(v=>id.get(v)));ok(V.length===9);let T=models.filter(x=>C.every(c=>evalWord(c,x)!==0));if(!T.length)return{status:"UNSAT",reason:"local core"};let ports=V.filter(v=>external.some(c=>c.includes(v)));ok(ports.length===6);let root=id.get(ports[0]);for(let v of ports){let j=id.get(v),b=T[0][j]^T[0][root];ok(T.every(x=>(x[j]^x[root])===b));phase[v]=i;offset[v]=b}locals.push({V,T,root})}
let edges=B.map(()=>[]);for(let c of external){let t=c.map(v=>phase[v]);let i=t.findIndex((u,j)=>t.filter(w=>w===u).length===1);ok(i>=0);let p=c.filter((_,j)=>j!==i),v=c[i];ok(phase[p[0]]===phase[p[1]]&&offset[p[0]]===offset[p[1]]);let x=phase[p[0]],y=phase[v],b=1^offset[p[0]]^offset[v];edges[x].push([y,b]);edges[y].push([x,b])}
let z=Array(B.length).fill(-1);for(let v=0;v<B.length;v++)if(z[v]<0){z[v]=0;let Q=[v];for(let j=0;j<Q.length;j++)for(let [u,b] of edges[Q[j]]){let w=z[Q[j]]^b;if(z[u]<0){z[u]=w;Q.push(u)}else if(z[u]!==w)return{status:"UNSAT",reason:"parity contradiction"}}}
let x=Array(n);locals.forEach(({V,T,root},i)=>{let w=T.find(x=>x[root]===z[i]);ok(!!w);V.forEach((v,j)=>x[v]=w[j])});ok(fit(P.flat(),x,Array(4*n/3).fill(0)));return{status:"SAT",reason:"parity lift"}}
function shuffle(a){for(let i=a.length-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
let ring=[];for(let k of [2,4,8,16,32,64]){let n=9*k,P=build(k,false),Y=build(k,true);auth(P,n);auth(Y,n);let F=P.flat(),x=Array.from({length:n},(_,v)=>{let q=v%9,b=Math.floor(v/9)%2;return q<3?b:q<6?1^b:q===8?1:0});ok(fit(Y.flat(),x,Array(12*k).fill(0)));let s=F.map(c=>evalWord(c,x)===0?1:0);ok(s.filter(Boolean).length===k&&fit(F,x,s));for(let i=0;i<k;i++){let C=F.filter(c=>c.every(v=>Math.floor(v/9)===i)).map(c=>c.map(v=>v%9));ok(C.length===11);ok(!models.some(x=>fit(C,x,Array(11).fill(0))))}
let perm=shuffle(Array.from({length:n},(_,i)=>i));const re=P=>P.map(p=>shuffle(p.map(c=>shuffle(c.map(v=>perm[v])))));
let d0=sourceOnly(re(P),n),d1=sourceOnly(re(Y),n);ok(d0.status==="UNSAT"&&d1.status==="SAT");ring.push({k,n,m:12*k,deficiencyLower:3*k+1,nearestSatSignWeight:k,negative:d0,positive:d1})}
return{seed:20261126,checks,ag9:{D,agChildren,oneBitNo,satSigning:t},random,ring}
}
console.log(JSON.stringify(audit(),null,2));
