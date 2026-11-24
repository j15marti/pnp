'use strict';
function hullTest(){
let state=0x51f0640;const rnd=n=>{state^=state<<13;state^=state>>>17;state^=state<<5;return (state>>>0)%n};
const assert=(a,m)=>{if(!a)throw Error(m)};
function basis(){let a=new Map();return {add(v){while(v){let k=31-Math.clz32(v);if(a.has(k))v^=a.get(k);else{a.set(k,v);return true}}return false},has(v){while(v){let k=31-Math.clz32(v);if(!a.has(k))return false;v^=a.get(k)}return true},rank:()=>a.size}}
let out={seed:"0x51f0640",cases:0,sat:0,unsat:0,referenceAssignments:0,feasibleCountVectors:0,generatedActualWitnesses:0,hullComparisons:0};
for(let trial=0;trial<160;trial++){
let n=3+rnd(9),h=2+rnd(2),D=1+rnd(4),dict=Array.from({length:D},()=>({d:Array.from({length:h},()=>rnd(9)-4),e:rnd(4)}));
let rows=Array.from({length:n},()=>{let {d,e}=dict[rnd(D)],a=d.map(v=>Math.max(0,-v)+rnd(4)),g=rnd(4);return [{c:a,g},{c:a.map((v,j)=>v+d[j]),g:g^e}]});
let K=Array(h).fill(0),tag=0;for(const r of rows){let p=r[rnd(2)];K=K.map((v,j)=>v+p.c[j]);tag^=p.g}if(trial%2){K=K.map(v=>v-rnd(5));tag=rnd(4)}
function valid(x){let c=Array(h).fill(0),g=0;rows.forEach((rr,i)=>{let r=rr[(x>>>i)&1];g^=r.g;c=c.map((v,j)=>v+r.c[j])});return g===tag&&c.every((v,j)=>v<=K[j])}
let truth=[],ref=basis();for(let x=0;x<2**n;x++){if(valid(x)){if(truth.length)ref.add(x^truth[0]);truth.push(x)}out.referenceAssignments++}
let groups=new Map();rows.forEach(([a,b],i)=>{let key=b.c.map((v,j)=>v-a.c[j]).join(",")+"|"+(a.g^b.g);if(!groups.has(key))groups.set(key,[]);groups.get(key).push(i)});let G=[...groups.values()],ks=Array(G.length).fill(0),anchor=null,got=basis(),witnesses=[];
function add(x){assert(valid(x),"invalid generated witness");out.generatedActualWitnesses++;if(anchor===null){anchor=x;witnesses.push(x)}else if(got.add(x^anchor))witnesses.push(x)}
function rec(i,x){if(i===G.length){if(!valid(x))return;out.feasibleCountVectors++;add(x);for(let j=0;j<G.length;j++){let g=G[j],k=ks[j];if(k===0||k===g.length)continue;for(let a=0;a<k;a++)add(x^(1<<g[a])^(1<<g[k]));for(let b=k+1;b<g.length;b++)add(x^(1<<g[0])^(1<<g[b]))}return}let y=x;for(let k=0;k<=G[i].length;k++){ks[i]=k;rec(i+1,y);if(k<G[i].length)y|=1<<G[i][k]}}
rec(0,0);assert((anchor!==null)===(truth.length>0),"decision");if(truth.length){assert(got.rank()===ref.rank(),"rank");for(let x of truth)assert(got.has(x^anchor),"missed point");for(let x of witnesses)assert(ref.has(x^truth[0]),"bad basis");out.hullComparisons++}out.cases++;out[truth.length?"sat":"unsat"]++;
}
return out;
}
console.log(JSON.stringify(hullTest(),null,2));
