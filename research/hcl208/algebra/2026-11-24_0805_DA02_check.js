console.log(JSON.stringify((function run(){
const assert=(x,m)=>{if(!x)throw Error(m)};
let seed=2080205;const rnd=n=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%n};
const lit=(v,s=0)=>2*v+s, vid=l=>Math.floor(l/2);
const ok=(row,x)=>{let a=x[vid(row[0])]^(row[0]&1);return row.some(l=>(x[vid(l)]^(l&1))!==a)};
const verify=(rows,x)=>rows.every(r=>ok(r,x));
function graph(rows){let adj=new Map(),inc=new Map();for(let j=0;j<rows.length;j++){let V=[...new Set(rows[j].map(vid))];for(let u of V){if(!adj.has(u)){adj.set(u,new Set());inc.set(u,[])}inc.get(u).push(j);for(let v of V)if(v!==u)adj.get(u).add(v)}}return {adj,inc}}
function discover(adj,k,stats,visit){
 const seen=new Set();let stop=false;
 function walk(C,B){stats.nodes++;if(stop)return;let z=Infinity;
 for(let u of C)for(let v of adj.get(u)) {stats.neighborVisits++;if(!C.has(v)&&!B.has(v)&&v<z)z=v}
 if(z===Infinity){let cs=[...C].sort((a,b)=>a-b),key=cs.join(",");if(seen.has(key))return;seen.add(key);stats.regions++;stop=visit(cs,[...B].sort((a,b)=>a-b))===true;return}
 if(C.size<k){let c=new Set(C);c.add(z);walk(c,B)}
 if(!stop&&B.size<2){let b=new Set(B);b.add(z);walk(C,b)}
 }
 for(let s of adj.keys()){walk(new Set([s]),new Set());if(stop)break}
}
function solve(n,input,k){
 let rows=input.map(r=>r.slice()),records=[],stats={nodes:0,neighborVisits:0,regions:0,tableTrials:0,literalVisits:0,sweeps:0,closureScans:0,unions:0,projections:0,projectedVars:0,forcedRegions:0,emptyRegions:0};
 const out=(status,x=null)=>({status,x,stats});
 for(;;){
 // Exact binary and repeated-literal closure. Every substitution is recorded.
 for(;;){let changed=false,next=[];for(let r of rows){stats.closureScans++;let a=[...new Set(r)];if(a.some(l=>a.includes(l^1)))continue;if(a.length<=1)return out("UNSAT");next.push(a)}rows=next;
 let q=rows.find(r=>r.length===2);if(!q)break;let u=vid(q[0]),v=vid(q[1]),b=1^(q[0]&1)^(q[1]&1);if(u>v)[u,v]=[v,u];records.push({type:"union",u,v,b});stats.unions++;rows=rows.map(r=>r.map(l=>vid(l)===v?lit(u,(l&1)^b):l));
 }
 if(!rows.length){let x=Array(n).fill(0);for(let r of records.slice().reverse()){if(r.type==="union")x[r.v]=x[r.u]^r.b;else {let mask=r.B.reduce((s,v,i)=>s|(x[v]<<i),0),w=r.table[mask];assert(w!==null,"lift absent");r.C.forEach((v,i)=>x[v]=(w>>i)&1)}}assert(verify(input,x),"lift invalid");return out("SAT",x)}
 stats.sweeps++;const {adj,inc}=graph(rows),eq=new Map(),chosen=[],usedI=new Set(),usedB=new Set();let empty=false;
 discover(adj,k,stats,(C,B)=>{
 const js=[...new Set(C.flatMap(v=>inc.get(v)))],V=[...C,...B],idx=new Map(V.map((v,i)=>[v,i]));
 const local=js.map(j=>rows[j].map(l=>2*idx.get(vid(l))+(l&1)));
 let table=Array(1<<B.length).fill(null);
 for(let p=0;p<table.length;p++){for(let a=0;a<(1<<C.length);a++){stats.tableTrials++;let mask=a|(p<<C.length),pass=true;for(let r of local){let f=((mask>>vid(r[0]))&1)^(r[0]&1),different=false;for(let l of r){stats.literalVisits++;if((((mask>>vid(l))&1)^(l&1))!==f){different=true;break}}if(!different){pass=false;break}}if(pass){table[p]=a;break}}}
 let support=table.map(x=>x!==null);
 if(!support.some(Boolean)){stats.emptyRegions++;empty=true;return true}
 if(B.length===2){assert(support[0]===support[3]&&support[1]===support[2],"complement");if(support[0]!==support[1]){let b=support[0]?0:1;eq.set(B.join(",")+":"+b,[lit(B[0]),lit(B[1],1^b)]);stats.forcedRegions++;return false}}
 assert(support.every(Boolean),"not full");
 if(C.every(v=>!usedI.has(v)&&!usedB.has(v))&&B.every(v=>!usedI.has(v))){C.forEach(v=>usedI.add(v));B.forEach(v=>usedB.add(v));chosen.push({type:"proj",C,B,table,js})}
 return false
 });
 if(empty)return out("UNSAT");
 if(eq.size){rows.push(...eq.values());continue}
 if(!chosen.length)return out("UNKNOWN");
 let removed=new Set();for(let a of chosen){a.js.forEach(j=>removed.add(j));records.push(a);stats.projections++;stats.projectedVars+=a.C.length}rows=rows.filter((r,j)=>!removed.has(j));
 }
}
const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
function gadget(a,b,alloc,rows){let p=alloc(),u=alloc(),v=alloc(),w=alloc(),z=alloc();for(let r of [[a,u,v],[a,w,z],[b,u,w],[b,v,z],[p,u,z],[p,v,w]])rows.push(r.map(x=>lit(x)))}
function base(){let n=1,rows=[],alloc=()=>n++;let ends=[];for(let j=0;j<2;j++){let a=0;for(let i=0;i<4;i++){let b=alloc();gadget(a,b,alloc,rows);a=b}ends.push(a)}rows.push([0,...ends].map(x=>lit(x)));return {n,rows}}
function stretch(F){let n=F.n,rows=[],alloc=()=>n++;for(let r of F.rows){let z=[];for(let l of r){let b=alloc();gadget(vid(l),b,alloc,rows);z.push(lit(b,l&1))}rows.push(z)}return {n,rows}}
function brute(n,rows){let count=0;for(let a=0;a<(1<<n);a++){let x=Array.from({length:n},(_,i)=>(a>>i)&1);if(verify(rows,x))count++}return count}
const result={seed:2080205,discovery:{graphs:0,sets:0,referenceSubsets:0},random:{SAT:0,UNSAT:0,UNKNOWN:0,referenceSAT:0,referenceUNSAT:0,referenceAssignments:0},controls:[],neighbors:{baseDeletion:0,baseOwner:0,stretchDeletion:0,stretchOwner:0},totals:{nodes:0,neighborVisits:0,regions:0,tableTrials:0,literalVisits:0,sweeps:0,closureScans:0,unions:0,projections:0,projectedVars:0,forcedRegions:0,emptyRegions:0}};
function add(r){for(let k in result.totals)result.totals[k]+=r.stats[k]}
for(let t=0;t<80;t++){let n=3+rnd(7),adj=new Map(Array.from({length:n},(_,i)=>[i,new Set()]));for(let u=0;u<n;u++)for(let v=u+1;v<n;v++)if((rnd(17))<6){adj.get(u).add(v);adj.get(v).add(u)}let k=1+rnd(Math.min(n,5)),seen=new Set(),s={nodes:0,neighborVisits:0,regions:0};discover(adj,k,s,(C,B)=>{seen.add(C.join(","));return false});let ref=new Set();for(let a=1;a<(1<<n);a++){result.discovery.referenceSubsets++;let C=Array.from({length:n},(_,i)=>i).filter(i=>(a>>i)&1);if(C.length>k)continue;let B=new Set(C.flatMap(v=>[...adj.get(v)].filter(w=>!((a>>w)&1))));if(B.size>2)continue;let reached=new Set([C[0]]),q=[C[0]];for(let u of q)for(let v of adj.get(u))if(((a>>v)&1)&&!reached.has(v)){reached.add(v);q.push(v)}if(reached.size===C.length)ref.add(C.join(","))}assert(seen.size===ref.size&&[...seen].every(x=>ref.has(x)),"discovery mismatch");result.discovery.graphs++;result.discovery.sets+=seen.size}
for(let t=0;t<120;t++){let n=3+rnd(7),m=1+rnd(20),rows=[];for(let i=0;i<m;i++){let vs=new Set();while(vs.size<3)vs.add(rnd(n));rows.push([...vs].map(v=>lit(v,rnd(19)%2)))}if(t%3===0)rows.push([lit(0),lit(1,rnd(17)%2)]);let c=brute(n,rows),r=solve(n,rows,3);result.random.referenceAssignments+=1<<n;result.random[c?"referenceSAT":"referenceUNSAT"]++;result.random[r.status]++;assert(r.status==="UNKNOWN"||(r.status==="SAT")===(c>0),"random decision");add(r)}
let f={n:7,rows:fano.map(r=>r.map(v=>lit(v)))},b=base(),s=stretch(b);
for(let [name,F,k] of [["Fano",f,5],["DO02-base",b,5],["DO02-stretch",s,5]]){let r=solve(F.n,F.rows,k);assert(r.status==="UNSAT",name+" root");result.controls.push({name,n:F.n,m:F.rows.length,k,status:r.status,stats:r.stats});add(r)}
for(let [name,F,inds] of [["base",b,Array.from({length:b.rows.length},(_,i)=>i)],["stretch",s,[0,Math.floor(s.rows.length/2),s.rows.length-1]]]){
 for(let i of inds){let r=solve(F.n,F.rows.filter((_,j)=>i!==j),5);assert(r.status==="SAT",name+" deletion "+i+" "+r.status);add(r);result.neighbors[name+"Deletion"]++;let x=r.x,edge=F.rows[i];assert(!ok(edge,x),"criticality witness");for(let want=0;want<2;want++){let y=x[vid(edge[0])]===want?x:x.map(v=>v^1);assert(verify(F.rows.filter((_,j)=>i!==j),y)&&edge.every(l=>y[vid(l)]===want),"owner witness");result.neighbors[name+"Owner"]++}}
}
return result
})(),null,2));
