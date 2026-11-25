const fs=require('node:fs');
function run(raw){
function norm(c){let s=new Set(c);for(let l of s)if(s.has(-l))return null;let a=[...s].sort((a,b)=>Math.abs(a)-Math.abs(b));if(a[0]<0)a=a.map(x=>-x);return a}
function canonical(F){let m=new Map();for(let c of F){let a=norm(c);if(a!==null)m.set(a.join(","),a)}return [...m.values()]}
function lit(l,a){return a[Math.abs(l)-1]^(l<0?1:0)}
function ok(F,a){return F.every(c=>c.some(l=>lit(l,a)!==lit(c[0],a)))}
function solve(F,n,K,cap=4000){let source=F, C=canonical(F),log=[],stats={pairs:0,scans:0,binary:0,projected:0,maxOwners:C.length,maxBoundary:0,wide:0},alive=new Set(Array.from({length:n},(_,i)=>i+1)),status="OPEN";
while(true){stats.scans+=C.reduce((s,c)=>s+c.length,0);if(C.some(c=>c.length<2)){status="UNSAT";break}if(!C.length){status="SAT";break}
let b=C.find(c=>c.length===2);if(b){let v=Math.abs(b[0]),w=Math.abs(b[1]),delta=1^Number(b[0]<0)^Number(b[1]<0);log.push({v,w,delta});alive.delete(v);C=canonical(C.map(c=>c.map(l=>Math.abs(l)===v?((l<0)^delta?-w:w):l)));stats.binary++;continue}
let deg=new Map();for(let c of C)for(let l of c)deg.set(Math.abs(l),(deg.get(Math.abs(l))||0)+1);
let [v,d]=[...deg].sort((a,b)=>a[1]-b[1]||a[0]-b[0])[0];
if(d>K||C.length-d+d*(d-1)/2>cap){stats.stallDegree=d;break}
let bucket=C.filter(c=>c.some(l=>Math.abs(l)===v)).map(c=>{let p=c.includes(v);return c.filter(l=>Math.abs(l)!==v).map(l=>p?l:-l)});
let width=new Set(bucket.flat().map(Math.abs)).size;stats.maxBoundary=Math.max(stats.maxBoundary,width);if(width>10)stats.wide++;
let next=C.filter(c=>!c.some(l=>Math.abs(l)===v));for(let i=0;i<d;i++)for(let j=i+1;j<d;j++){stats.pairs++;next.push([...bucket[i],...bucket[j].map(l=>-l)])}
log.push({v,bucket});alive.delete(v);C=canonical(next);stats.projected++;stats.maxOwners=Math.max(stats.maxOwners,C.length);
}
let witness=null;if(status==="SAT"){let a=Array(n).fill(0);for(let e of [...log].reverse()){if(e.w){a[e.v-1]=a[e.w-1]^e.delta;continue}let required=new Set();for(let c of e.bucket){let z=c.map(l=>lit(l,a));if(z.every(t=>t===z[0]))required.add(1^z[0])}if(required.size>1)throw Error("lift conflict");a[e.v-1]=[...required][0]??0}if(!ok(source,a))throw Error("source lift");witness=a}
return {status,stats,witness,remaining:C.length,free:alive.size, residual:status==="OPEN"?{C,log}:undefined}}
function brute(F,n){for(let x=0;x<2**n;x++)if(ok(F,Array.from({length:n},(_,i)=>(x>>i)&1)))return true;return false}
function direct(F,n,cap=128){let nodes=0, scans=0;function go(a){if(++nodes>cap)return null;while(true){let changed=false;for(let c of F){scans++;let v=c.filter(l=>a[Math.abs(l)-1]!==-1).map(l=>lit(l,a));if(v.includes(0)&&v.includes(1))continue;let u=c.filter(l=>a[Math.abs(l)-1]===-1);if(!u.length)return false;if(u.length===1&&v.length){let l=u[0];a[Math.abs(l)-1]=1^v[0]^Number(l<0);changed=true}}if(!changed)break}
let v=a.indexOf(-1);if(v<0)return ok(F,a)?a:false;for(let b of [0,1]){let t=a.slice();t[v]=b;let z=go(t);if(z===null||z!==false)return z}return false}let z=go(Array(n).fill(-1));return {status:z===null?"OPEN":z===false?"UNSAT":"SAT",nodes,scans}}
let seed=10091;function rnd(n){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n}
let controls=[];let fano=[[1,2,3],[1,4,5],[1,6,7],[2,4,6],[2,5,7],[3,4,7],[3,5,6]];
controls.push({F:fano,n:7});for(let i=0;i<7;i++)for(let j=0;j<3;j++){let F=fano.map(c=>c.slice());F[i][j]*=-1;controls.push({F,n:7})}
for(let i=0;i<160;i++){let n=4+rnd(5),m=2+rnd(14),F=[];for(let j=0;j<m;j++){let a=new Set(),k=2+rnd(Math.min(n,5)-1);while(a.size<k)a.add(1+rnd(n));F.push([...a].map(v=>rnd(2)?v:-v))}controls.push({F,n})}
let sums={SAT:0,UNSAT:0,OPEN:0,pairs:0,binary:0,projected:0};for(let {F,n} of controls){let b=brute(F,n),z=solve(F,n,32);if(z.status!=="OPEN"&&(z.status==="SAT")!==b)throw Error("reference");sums[z.status]++;for(let k of ["pairs","binary","projected"])sums[k]+=z.stats[k]}
let F=raw.O.map(o=>o.t.map(v=>v+1));for(let w of [13310626,13308834])if(!ok(F,Array.from({length:raw.n},(_,i)=>(w>>i)&1)))throw Error("peer source word");
let common=[];for(let K of [0,3,4,6,8,12,16,32]){let z=solve(F,raw.n,K);common.push({K,...z})}
let rings=[];for(let n of [12,24,48,96]){let F=Array.from({length:n},(_,i)=>[i+1,(i+1)%n+1,(i+2)%n+1]);let z=solve(F,n,6);rings.push({n,...z,residual:undefined})}
return {controls:sums,common,direct:direct(F,raw.n),rings,fano:solve(fano,7,8),source:{n:raw.n,O:raw.O}};
}
const raw=JSON.parse(fs.readFileSync(process.argv[2],'utf8')); console.log(JSON.stringify(run(raw),null,2));
