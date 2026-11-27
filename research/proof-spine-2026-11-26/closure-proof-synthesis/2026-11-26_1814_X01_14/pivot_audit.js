function pivotAudit(){
let checks=0,systems=0,probes=0,seed=261126141;const ok=(b,m)=>{checks++;if(!b)throw Error(m||"check "+checks)};function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}function par(x){let b=0;while(x){x&=x-1;b^=1}return b}
function basis(A){let B=[];for(let a of A){for(let b of B)a=Math.min(a,a^b);if(a){B.push(a);B.sort((a,b)=>b-a)}}return B}
function span(A){let L=[0];for(let a of A)L=L.concat(L.map(x=>x^a));return L}
function solve(E,n){let B=Array(n).fill(null);for(let [a,b] of E){for(let j=n-1;j>=0;j--)if(a>>j&1){if(B[j]){a^=B[j][0];b^=B[j][1]}else{B[j]=[a,b];break}}if(a===0&&b)return null}let v=0;for(let j=0;j<n;j++)if(B[j]&&par(B[j][0]&v)!==B[j][1])v^=1<<j;return v}
function combinations(n,k,fn){let A=[];function rec(i){if(A.length===k){fn(A.slice());return}for(let j=i;j<=n-k+A.length;j++){A.push(j);rec(j+1);A.pop()}}rec(0)}
function make(n,m){return Array.from({length:m},()=>{let A=basis(Array.from({length:1+rnd(n)},()=>1+rnd((1<<n)-1))),a=rnd(1<<n);return{A,a}})}
function data(E){let P=[];for(let i=0;i<E.length;i++){P[i]=[];for(let j=i+1;j<E.length;j++){let a=E[i],b=E[j],S=new Set(span(b.A));P[i][j]={I:basis(span(a.A).filter(x=>S.has(x))),rank:basis([...a.A,...b.A]).length-1}}}return P}
function raw(E,P,v){let J=[];for(let i=0;i<E.length;i++)if(E[i].A.some(a=>par(a&v)))J.push(i);let cost=E.reduce((s,e,i)=>s+(J.includes(i)?0:e.A.length),0);for(let i of J)for(let j of J)if(i<j&&P[i][j].I.every(a=>par(a&(v^E[i].a^E[j].a))===0))cost+=P[i][j].rank;return {J,cost}}
function acquire(E,P,n,k){let best=null;for(let h=1;h<=Math.min(k,E.length);h++)combinations(E.length,h,J=>{let base=E.flatMap((e,i)=>J.includes(i)?[]:e.A.map(a=>[a,0])),pairs=[];for(let i of J)for(let j of J)if(i<j)pairs.push([i,j]);let R=base.length;
let choices=J.map(i=>E[i].A.map(a=>[[a,1]]));
function walkPairs(t,eqs,cost){if(best&&cost>=best.cost)return;if(t===pairs.length){probes++;let v=solve(eqs,n);if(v!==null){let z=raw(E,P,v);ok(z.J.length===h&&z.cost===cost);best={v,cost}}return}
let [i,j]=pairs[t],{I,rank}=P[i][j],a=E[i].a^E[j].a;
walkPairs(t+1,eqs.concat(I.map(w=>[w,par(w&a)])),cost+rank);
for(let w of I)walkPairs(t+1,eqs.concat([[w,par(w&a)^1]]),cost)
}
function touch(i,eqs){if(i===h){walkPairs(0,eqs,R);return}for(let a of choices[i])touch(i+1,eqs.concat(a))}
touch(0,base);
});return best}
function ev(e,x){return e.A.every(a=>par(a&(x^e.a))===0)}
let admitted=0,proj=0,maxRank=0;for(let t=0;t<180;t++){let n=2+rnd(5),m=2+rnd(5),E=make(n,m),P=data(E);maxRank=Math.max(maxRank,...E.map(e=>e.A.length));let best=null;for(let v=1;v<1<<n;v++){let z=raw(E,P,v);if(z.J.length&&z.J.length<=3&&(best===null||z.cost<best))best=z.cost}let q=acquire(E,P,n,3);ok((q?.cost??null)===best,"optimum");systems++;if(!q)continue;admitted++;let v=q.v,k=Math.floor(Math.log2(v&-v)),z=raw(E,P,v);
for(let y=0;y<1<<n;y++)if(!(y>>k&1)){let expected=[y,y^v].some(x=>E.every(e=>!ev(e,x)));let allowed=E.every((e,i)=>z.J.includes(i)||!ev(e,y));for(let i of z.J)for(let j of z.J)if(i<j&&((ev(E[i],y)&&ev(E[j],y^v))||(ev(E[i],y^v)&&ev(E[j],y))))allowed=false;ok(expected===allowed,"exact projection");proj++}
}
return{checks,systems,admitted,probes,projectionChecks:proj,maxRank,seed:261126141}
}
console.log(JSON.stringify(pivotAudit(),null,2));
