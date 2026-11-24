'use strict';
function run(){
let seed=0x2010640;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
const assert=(v,m)=>{if(!v)throw Error(m)};
function valid(rows,K,t,x){let c=K.map(()=>0n),g=0;for(let i=0;i<rows.length;i++){const r=rows[i][x[i]];g^=r.g;for(let j=0;j<K.length;j++)c[j]+=r.c[j]}return g===t&&c.every((v,j)=>v<=K[j])}
function grouped(rows,K,t){let c=K.map(()=>0n),g=0,groups=new Map();for(let i=0;i<rows.length;i++){const [a,b]=rows[i];for(let j=0;j<K.length;j++)c[j]+=a.c[j];g^=a.g;const d=b.c.map((v,j)=>v-a.c[j]),e=a.g^b.g,key=d.join(",")+"|"+e;if(!groups.has(key))groups.set(key,{d,e,ids:[]});groups.get(key).ids.push(i)}
 const G=[...groups.values()],x=Array(rows.length).fill(0);let leaves=0;
 function dfs(i,c,g){if(i===G.length){leaves++;return g===t&&c.every((v,j)=>v<=K[j])}const {d,e,ids}=G[i];for(let k=0;k<=ids.length;k++){if(k)x[ids[k-1]]=1;if(dfs(i+1,c.map((v,j)=>v+BigInt(k)*d[j]),g^((k%2)*e)))return true}for(const j of ids)x[j]=0;return false}
 return {x:dfs(0,c,g)?x:null,leaves,types:G.length};
}
function brute(rows,K,t){let count=0,w=null;for(let m=0;m<2**rows.length;m++){const x=rows.map((_,i)=>(m>>i)&1);if(valid(rows,K,t,x)){count++;w=x}}return {count,w}}
let out={seed:"0x2010640",random:{cases:0,sat:0,unsat:0,assignments:0,countLeaves:0,tagged:0,largeBit:0},probe:{cases:0,failures:0},scaling:[],peer:{}};
for(let z=0;z<180;z++){let n=4+rnd(7),h=2+rnd(3),scale=z%9===0?2n**80n:1n;const dict=Array.from({length:1+rnd(3)},()=>({d:Array.from({length:h},()=>BigInt(rnd(9)-4)*scale),e:rnd(4)}));
const rows=Array.from({length:n},()=>{const {d,e}=dict[rnd(dict.length)],a=d.map(v=>(v<0n?-v:0n)+BigInt(rnd(5))*scale),g=rnd(4);return [{c:a,g},{c:a.map((v,j)=>v+d[j]),g:g^e}]});
let K=Array(h).fill(0n),t=0;for(const rr of rows){const r=rr[rnd(2)];K=K.map((v,j)=>v+r.c[j]);t^=r.g}if(z%2){K=K.map(v=>v-BigInt(rnd(6))*scale);t=rnd(4)}
const a=grouped(rows,K,t),b=brute(rows,K,t);assert(!!a.x===!!b.w,"random decision");if(a.x)assert(valid(rows,K,t,a.x),"witness");out.random.cases++;out.random[a.x?"sat":"unsat"]++;out.random.assignments+=2**n;out.random.countLeaves+=a.leaves;out.random.tagged++;if(scale>1n)out.random.largeBit++}
function family(h){let M=4*h+2,T=2*h*M+2*h+1,w=Array(2*h).fill(M).concat(Array(2*h).fill(M+1)),S=w.reduce((a,b)=>a+b,0);let rows=w.map(v=>[{c:[0n,BigInt(v)],g:0},{c:[BigInt(v),0n],g:0}]);return {M,T,w,S,rows}}
function gcd(a,b){while(b){[a,b]=[b,a%b]}return Math.abs(a)}
// LP exact feasibility (interval), and integer lattice membership after fixed rows.
// Rational witness is all free x_i = R/F. Integer witness uses -R at a free M and +R at a free M+1.
function probe(h,fix){const {M,T,w,S}=family(h);let A=0,B=0,F=0,g=0,hasM=false,hasNext=false;for(let i=0;i<w.length;i++){if(fix[i]===1)A+=w[i];else if(fix[i]===0)B+=w[i];else{F+=w[i];g=gcd(g,w[i]);hasM||=w[i]===M;hasNext||=w[i]===M+1}}let R=T-A;assert(R>=0&&R<=F&&S-T>=B,"LP");assert(g===1&&hasM&&hasNext,"lattice");assert((-R)*M+R*(M+1)===R,"integer witness");out.probe.cases++}
for(let h=1;h<=3;h++){let n=4*h,fix=Array(n).fill(-1);function rec(i,k){if(i===n){probe(h,fix);return}rec(i+1,k);if(k<2*h-1){fix[i]=0;rec(i+1,k+1);fix[i]=1;rec(i+1,k+1);fix[i]=-1}}rec(0,0)}
for(const h of [1,2,3,4,8,16,32,64,128]){let {M,T,w,S,rows}=family(h);let a=grouped(rows,[BigInt(T),BigInt(S-T)],0),b=grouped(rows,[BigInt(T),BigInt(S-T+1)],0);assert(!a.x&&b.x&&valid(rows,[BigInt(T),BigInt(S-T+1)],0,b.x),"family");assert(b.x.every((x,i)=>x===+(i>=2*h)),"unique neighbor form");let bruteCounts=null;if(h<=3){let x=brute(rows,[BigInt(T),BigInt(S-T)],0),y=brute(rows,[BigInt(T),BigInt(S-T+1)],0);assert(x.count===0&&y.count===1,"reference family");bruteCounts=[x.count,y.count]}out.scaling.push({h,blocks:w.length,M,T,unitEdges:2*S,pinDepth:2*h-1,log2Cut:4*h-1,unsatLeaves:a.leaves,satLeaves:b.leaves,bruteCounts})}
let w=[4,4,5,7],S=w.reduce((a,b)=>a+b,0),T=S/2,rows=w.map(v=>[{c:[0n,BigInt(v)],g:0},{c:[BigInt(v),0n],g:0}]);let b=brute(rows,[BigInt(T),BigInt(T)],0);assert(b.count===0,"peer");let pins=0;for(let i=0;i<w.length;i++)for(let bit=0;bit<2;bit++){let R=T-bit*w[i],u=w.filter((_,j)=>j!==i);assert(R>=0&&R<=u.reduce((a,b)=>a+b,0)&&R%u.reduce(gcd,0)===0,"peer pin");pins++}out.peer={MS06Partition:w,target:T,solutions:b.count,lpLatticeSurvivingPins:pins};
return out;
}
console.log(JSON.stringify(run(),null,2));
