// node redteam.js
function redteam(){
let seed=91783,checks=0,queries=0,augmentations=0,exchangeArcs=0,nonGreedy=0,subsets=0;
function ok(v){checks++;if(!v)throw Error("check "+checks)}
function rnd(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)%n}
function shuffle(a){for(let i=a.length-1;i>0;i--){let j=rnd(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
function parity(v){let p=0;while(v){v&=v-1;p^=1}return p}
function make(){let p=Array(9).fill(0),b=Array(9).fill(0),r=0;function reduce(v,z=0){for(let i=8;i>=0;i--)if(((v>>i)&1)&&p[i]){v^=p[i];z^=b[i]}return[v,z]}return{reduce,add(v,z=0){[v,z]=reduce(v,z);if(!v)return z?-1:0;let i=31-Math.clz32(v);p[i]=v;b[i]=z;r++;return 1},get rank(){return r}}}
const C=[[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[1,5,6],[2,3,7],[0,5,7],[1,3,8],[2,4,6]];
function independent(E,ids){let b=make();return ids.every(i=>b.add(E[i].v)===1)}
function mi(E){queries++;let I=[];
for(;;){let s=new Set(I),outside=E.map((_,i)=>i).filter(i=>!s.has(i)),own=new Map(I.map(i=>[E[i].o,i])),prev=new Map(),queue=[];
for(let i of outside)if(independent(E,I.concat(i))){queue.push(i);prev.set(i,-1)}
let end=-1;for(let k=0;k<queue.length&&end<0;k++){let i=queue[k];if(!s.has(i)){let j=own.get(E[i].o);if(j===undefined){end=i;break}if(!prev.has(j)){queue.push(j);prev.set(j,i);exchangeArcs++}}else{let J=I.filter(j=>j!==i);for(let j of outside)if(!prev.has(j)&&independent(E,J.concat(j))){prev.set(j,i);queue.push(j);exchangeArcs++}}}
if(end<0)return I.length;let len=0;while(end>=0){if(s.has(end))s.delete(end);else s.add(end);end=prev.get(end);len++}if(len>1)nonGreedy++;ok(s.size===I.length+1);I=[...s];ok(independent(E,I)&&new Set(I.map(i=>E[i].o)).size===I.length);augmentations++}}
let results=[];
for(let t=0;t<96;t++){let H=make(),w=rnd(512),q=rnd(9);while(H.rank<q){let a=2*rnd(256);if(parity(a))a^=1;H.add(a,parity(a&w))}
let ownerRows=[],f=0;
for(let c of C){let V=[[0,1],[0,2],[1,2]].map(([i,j])=>H.reduce((1<<c[i])^(1<<c[j])));if(V.some(([v,b])=>!v&&b===1)){f++;continue}ownerRows.push(V.filter(([v])=>v).map(([v])=>v))}
let E=shuffle(ownerRows.flatMap((a,o)=>a.map(v=>({o,v})))),r=mi(E),min=ownerRows.length;
for(let s=0;s<2**ownerRows.length;s++){let B=make(),z=0;for(let i=0;i<ownerRows.length;i++)if((s>>i)&1){z++;ownerRows[i].forEach(v=>B.add(v))}min=Math.min(min,ownerRows.length-z+B.rank);subsets++}
ok(r===min);ok(7*f<=16*q);results.push({q,f,r})}
return{seed:91783,checks,queries,augmentations,exchangeArcs,nonGreedy,subsets,results}
}
console.log(JSON.stringify(redteam(),null,2));
