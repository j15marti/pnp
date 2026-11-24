const run=()=>{
let seed=70421;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
const pop=x=>{let k=0;while(x){x&=x-1;k++}return k}; // masks only for <= 8 owners in tests
const masks=x=>{let a=[];for(let i=0;i<30;i++)if(x&(1<<i))a.push(i);return a};
const recognize=rows=>{if(!rows.length)return false;let r=pop(rows[0]),S=new Set(rows);if(rows.some(x=>pop(x)!==r))return false;for(let a of rows)for(let b of rows)for(let e of masks(a&~b)){if(!masks(b&~a).some(f=>S.has(a^(1<<e)^(1<<f))))return false}return true};
let stats={cases:0,sat:0,unsat:0,pins:0,referenceTuples:0,augmentations:0,certificates:0,recognitionRejects:0,closureDeletes:0};
function prep(rows,K){rows=rows.map(a=>[...new Set(a)]);for(;;){if(rows.some(a=>!a.length))return null;let minima=rows.map(a=>a.reduce((x,y)=>x&y));let base=K.map((_,i)=>minima.reduce((s,a)=>s+((a>>i)&1),0));if(base.some((v,i)=>v>K[i]))return null;let changed=false;for(let b=0;b<rows.length;b++){let bad=rows[b].findIndex(a=>masks(a&~minima[b]).some(i=>base[i]>=K[i]));if(bad>=0){rows[b].splice(bad,1);stats.closureDeletes++;changed=true;break}}if(!changed)return rows}}
function solve(raw,K){let rows=prep(raw,K);if(!rows)return {ok:false};if(rows.some(a=>!recognize(a)))return {unknown:true};const E=[];rows.forEach((a,b)=>masks(a.reduce((x,y)=>x|y,0)).forEach(i=>E.push([b,i])));const n=E.length,R=rows.reduce((s,a)=>s+pop(a[0]),0);let I=new Set();
function ind(S,which){if(which===1){let v=rows.map(()=>0);for(const e of S){let[b,i]=E[e];v[b]|=1<<i}return rows.every((a,b)=>a.some(x=>(x&v[b])===v[b]))}let v=K.map(()=>0);for(const e of S)if(++v[E[e][1]]>K[E[e][1]])return false;return true}
function mod(e,f){let a=new Set(I);if(f!==undefined)a.delete(f);a.add(e);return a}
while(I.size<R){let outside=E.map((_,e)=>e).filter(e=>!I.has(e)),inside=[...I];let prev=new Map(),queue=[];for(let e of outside)if(ind(mod(e),1)){prev.set(e,-1);queue.push(e)}let end=-1;for(let q=0;q<queue.length;q++){let e=queue[q];if(!I.has(e)&&ind(mod(e),2)){end=e;break}
let next=I.has(e)?outside.filter(f=>ind(mod(f,e),1)):inside.filter(f=>ind(mod(e,f),2));for(let f of next)if(!prev.has(f)){prev.set(f,e);queue.push(f)}}
if(end<0){let U=K.map((k,i)=>queue.filter(e=>E[e][1]===i).length>=k);let cap=K.reduce((s,k,i)=>s+(U[i]?k:0),0);
let demand=rows.reduce((s,a)=>s+Math.min(...a.map(x=>masks(x).filter(i=>U[i]).length)),0);if(!(demand>cap))throw Error("Hall certificate failed");stats.certificates++;return {ok:false,cap,demand}}
for(let e=end;e>=0;e=prev.get(e)){if(I.has(e))I.delete(e);else I.add(e)}if(!ind(I,1)||!ind(I,2))throw Error("bad augment");stats.augmentations++}
let v=rows.map(()=>0);for(let e of I){let[b,i]=E[e];v[b]|=1<<i}if(!raw.every((a,b)=>a.includes(v[b])))throw Error("bad lift");return {ok:true,v}}
function ref(rows,K){let v=K.map(()=>0);function go(b){if(b===rows.length){stats.referenceTuples++;return true}let ok=false;for(let a of rows[b]){let is=masks(a);for(let i of is)v[i]++;if(v.every((x,i)=>x<=K[i]))ok=go(b+1)||ok;for(let i of is)v[i]--}return ok}return go(0)}
function check(rows,K,pin=false){let z=solve(rows,K),r=ref(rows,K);if(z.unknown||z.ok!==r)throw Error("reference discrepancy");if(pin)stats.pins++;else{stats.cases++;stats[r?"sat":"unsat"]++}}
for(let t=0;t<180;t++){let h=3+rnd(4),B=2+rnd(4),rows=[];for(let b=0;b<B;b++){let vec=Array.from({length:h},()=>rnd(8));let a=[]; // binary rank-two vector matroid: distinct nonzero GF2^2 columns
vec=vec.map(x=>x%4);for(let i=0;i<h;i++)for(let j=i+1;j<h;j++)if(vec[i]&&vec[j]&&vec[i]!==vec[j])a.push((1<<i)|(1<<j));if(!a.length)a=[1<<rnd(h)];rows.push(a)}let K=Array.from({length:h},()=>rnd(B+1));check(rows,K);for(let b=0;b<rows.length;b++)for(let a of rows[b]){let p=rows.slice();p[b]=[a];check(p,K,true)}}
let hostile=[3,12];if(recognize(hostile))throw Error("false exchange recognition");stats.recognitionRejects++;
// arbitrary many blocks on six owners, rank 2 choices of four owners, plus spare owners not reachable.
// full solution with capacities 2B/4 each; lower one creates Hall deficit despite spare capacity.
let scaling=[];for(let B of [8,16,32,64]){let rows=Array.from({length:B},()=>[3,5,9,6,10,12]);let K=[B/2,B/2,B/2,B/2,B,B];let a=solve(rows,K);K[0]--;let b=solve(rows,K);if(!a.ok||b.ok||b.unknown)throw Error("scaling");scaling.push({blocks:B,localRows:6,totalTupleSpace:"6^"+B,sat:a.ok,unsat:!b.ok,hallDemand:b.demand,hallCapacity:b.cap})}
return {seed:70421,...stats,scaling};
};
console.log(JSON.stringify(run(),null,2));
