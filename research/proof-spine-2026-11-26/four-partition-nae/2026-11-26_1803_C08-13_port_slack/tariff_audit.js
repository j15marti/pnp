// node tariff_audit.js
function tariffAudit(){
let seed=20261127,checks=0;function ok(t,msg){checks++;if(!t)throw Error(msg||"check "+checks)}
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
function shuffle(a){for(let i=a.length-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
const bit=(w,v)=>(w>>>v)&1, truth=(p,w)=>bit(w,p[0])^p[1], nae=(c,w)=>c.some(p=>truth(p,w)!==truth(c[0],w)), valid=(C,w)=>C.every(c=>nae(c,w));
function match(C,n,I){let adj=C.map(c=>[...new Set(c.map(p=>p[0]))]),mv=Array(n).fill(-1),mc=Array(C.length).fill(-1),allowed=new Set(I);
function aug(c,seen){for(let v of adj[c])if(allowed.has(v)&&!seen.has(v)){seen.add(v);if(mv[v]<0||aug(mv[v],seen)){mv[v]=c;mc[c]=v;return true}}return false}
let rI=0;for(let c=0;c<C.length;c++)if(aug(c,new Set))rI++;allowed=new Set(Array.from({length:n},(_,i)=>i));let r=rI;for(let c=0;c<C.length;c++)if(mc[c]<0&&aug(c,new Set))r++;ok(mv.filter((c,v)=>c>=0&&I.includes(v)).length===rI);return{mc,mv,r,rI}}
function deficiency(C,P){let m=C.length,d=0,S=new Set(P);for(let mask=0;mask<2**m;mask++){let V=new Set(),t=0;for(let i=0;i<m;i++)if(bit(mask,i)){t++;for(let [v] of C[i])if(!S.has(v))V.add(v)}d=Math.max(d,t-V.size)}return d}
function proj(P,w){return P.reduce((a,v,i)=>a+bit(w,v)*2**i,0)}
let random={cases:0,deficient:0,charts:0,strictBound:0,maxShattered:0,equalityCases:0};
for(let j=0;j<720;j++){
let n=4+rnd(7),m=2+rnd(10),w=rnd(2**n),C=[];for(let i=0;i<m;i++){let s=rnd(3)===0?2:3;let c=shuffle(Array.from({length:n},(_,i)=>i)).slice(0,s).map(v=>[v,rnd(2)]);if(!nae(c,w))c[0][1]^=1;ok(nae(c,w));C.push(c)}
let P=shuffle(Array.from({length:n},(_,i)=>i)).slice(0,2+rnd(n-1)),I=Array.from({length:n},(_,i)=>i).filter(v=>!P.includes(v)),M=match(C,n,I),d=m-M.rI,e=m-M.r;
ok(deficiency(C,P)===d&&deficiency(C,[])===e);
let eq=[];for(let i=0;i<m;i++){let c=C[i],a=M.mc[i]>=0?c.find(p=>p[0]===M.mc[i]):c[0],b=c.find(p=>truth(p,w)!==truth(a,w));ok(b!==undefined);eq.push([a[0],b[0],1^a[1]^b[1]])}
let portWords=new Set(),allWords=new Set(),count=0;
for(let u=0;u<2**n;u++){if(valid(C,u))allWords.add(proj(P,u));if(!eq.every(([a,b,t])=>(bit(u,a)^bit(u,b))===t))continue;ok(valid(C,u));portWords.add(proj(P,u));count++}
ok(portWords.has(proj(P,w)));let dimension=Math.log2(portWords.size);ok(Number.isInteger(dimension)&&dimension>=Math.max(0,P.length-d));let free=0;
for(let mask=0;mask<2**P.length;mask++){let s=mask.toString(2).split("1").length-1;let S=new Set([...portWords].map(v=>v&mask));if(S.size===2**s)free=Math.max(free,s)}ok(free===dimension);
let deg=Array(n).fill(0);for(let c of C)for(let [v] of c)deg[v]++;let positions=P.reduce((a,v)=>a+deg[v],0),excess=I.reduce((a,v)=>a+Math.max(0,deg[v]-3),0),short=C.filter(c=>c.length===2).length;
ok(3*d<=positions+excess+short);
if(allWords.size===2&&allWords.has(0)&&allWords.has(2**P.length-1)){ok(short+excess>=3*(P.length-1)-positions);random.equalityCases++}
random.cases++;random.deficient+=e>0;random.charts+=count;random.strictBound+=dimension>Math.max(0,P.length-d);random.maxShattered=Math.max(random.maxShattered,free)
}
const FANO=[[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
let patterns=[];for(let w=0;w<128;w++)if(valid(FANO.map(c=>c.map(v=>[v,0])),w)){ok((w&7)===0||(w&7)===7);patterns.push(w)}ok(patterns.length===10);
let chain=[];for(let k of [3,4,5,8,16,32,64,128]){let r=k-2,n=7*r,C=[],P=[];for(let i=0;i<r;i++){for(let c of FANO)C.push(c.map(v=>[7*i+v,0]));if(i<r-1)C.push([[7*i+2,0],[7*(i+1)+1,1]]);for(let j=0;j<3;j++)if(!(j===1&&i>0)&&!(j===2&&i<r-1))P.push(7*i+j)}
ok(P.length===k&&C.filter(c=>c.length===2).length===k-3);let d=Array(n).fill(0);for(let c of C)for(let [v] of c)d[v]++;ok(d.every((a,v)=>a===(P.includes(v)?2:3)));let M=match(C,n,Array.from({length:n},(_,i)=>i).filter(v=>!P.includes(v)));ok(C.length-M.rI===k-1);
for(let b of [0,1]){let w=patterns.find(w=>(w&7)===(b?7:0)),x=Array.from({length:n},(_,i)=>bit(w,i%7));ok(C.every(c=>c.some(([v,s])=>(x[v]^s)!==(x[c[0][0]]^c[0][1]))));ok(P.every(v=>x[v]===b))}
chain.push({ports:k,vars:n,short:k-3,privateDeficiency:C.length-M.rI,matchingDeficit:C.length-M.r})}
return{seed:20261127,checks,random,chain}}
console.log(JSON.stringify(tariffAudit(),null,2));
