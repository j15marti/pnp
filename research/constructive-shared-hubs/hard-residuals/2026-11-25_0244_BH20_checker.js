// Node.js: node checker.js BW17.json BS19_results.json RT26_results.json
const fs=require('fs');
function run(bw,bs,rt){
 const stats={checks:0,referenceVisits:0,closureScans:0,forces:0,peelScans:0,peeled:0,lifts:0}; const assert=(x,msg)=>{stats.checks++;if(!x)throw Error(msg)};
 function word(o,a){return o.t.reduce((v,x,j)=>v+(a[x]<<j),0)}
 function legal(o,a){return !o.bad.includes(word(o,a))}
 function ok(O,a){return O.every(o=>legal(o,a))}
 function bits(w,n){return Array.from({length:n},(_,i)=>(w>>>i)&1)}
 function closure(O,a){let changed=true;while(changed){changed=false;for(const o of O){stats.closureScans++;for(const b of o.bad){let u=-1,nu=0,match=true;for(let j=0;j<o.t.length;j++){let x=o.t[j],v=a[x];if(v<0){u=j;nu++}else if(v!==((b>>>j)&1)){match=false;break}}if(!match)continue;if(!nu)return false;if(nu===1){a[o.t[u]]=1-((b>>>u)&1);stats.forces++;changed=true}}}}return true}
 function peel(O,a,protectedSet=new Set()){let rem=O.slice(),log=[];for(;;){let d=Array(a.length).fill(0);for(const o of rem)for(const x of o.t)d[x]++;let i=-1,x=-1;for(let j=0;j<rem.length&&i<0;j++){stats.peelScans++;const o=rem[j];if(o.t.length<2)continue;for(const v of o.t)if(a[v]<0&&!protectedSet.has(v)&&d[v]===1){ // Verify total one-coordinate projection analytically: no two bad rows differ only here.
 let p=o.t.indexOf(v);if(!o.bad.some(b=>o.bad.includes(b^(1<<p)))){i=j;x=v;break}}}
 if(i<0)break;log.push({o:rem[i],x});rem.splice(i,1);stats.peeled++}return {rem,log}}
 function lift(log,a){for(let i=log.length-1;i>=0;i--){let {o,x}=log[i];assert(a[x]<0||a[x]===0||a[x]===1,"bad lift");a[x]=0;if(!legal(o,a))a[x]=1;assert(legal(o,a),"lift failed");stats.lifts++}return a}
 function solve(O,n,guard,mode,cap=5000){let nodes=0,decline=false;function rec(R,a){if(nodes>=cap){decline=true;return null}nodes++;if(!closure(R,a))return null;let P=mode?peel(R,a):{rem:R,log:[]};let d=Array(n).fill(0);for(const o of P.rem)for(const x of o.t)if(a[x]<0)d[x]++;let x=-1;for(let i=0;i<n;i++)if(d[i]&& (x<0||d[i]>d[x]))x=i;
 if(x<0){let out=a.map(v=>v<0?0:v);return lift(P.log,out)}
 for(let b=0;b<2;b++){let c=a.slice();c[x]=b;let out=rec(P.rem,c);if(out)return lift(P.log,out);if(decline)return null}return null}
 let a=Array(n).fill(-1);for(const [x,b] of guard)a[x]=b;let w=rec(O,a);if(w){assert(ok(O,w),"source witness");assert(guard.every(([x,b])=>w[x]===b),"guard witness")}return {status:w?"SAT":decline?"DECLINE":"UNSAT",nodes,w:w?w.reduce((s,b,i)=>s+b*2**i,0):null}}
 function reference(O,n,g){let vars=[...new Set(O.flatMap(o=>o.t).concat(g.map(x=>x[0])))],pins=new Map(g),free=vars.filter(x=>!pins.has(x)),a=Array(n).fill(0);for(const [x,b] of g)a[x]=b;let count=0;for(let w=0;w<2**free.length;w++){stats.referenceVisits++;for(let j=0;j<free.length;j++)a[free[j]]=(w>>>j)&1;if(ok(O,a))count++}return count}
 function compare(O,n,g){let A=solve(O,n,g,false),B=solve(O,n,g,true),r=reference(O,n,g);assert(A.status===(r?"SAT":"UNSAT"),"direct");assert(B.status===A.status,"joint");return {A:A.nodes,B:B.nodes,r}}
 let fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]].map(t=>({t,bad:[0,7]}));
 let sets=[{name:"Fano",n:7,O:fano},...rt.controls.map(c=>({name:"RT26-"+c.n,n:c.n,O:c.registry}))],controls=[];
 for(const s of sets){let root=compare(s.O,s.n,[]);assert(root.r===0,"critical root");let neighbors=0,An=0,Bn=0;for(let i=0;i<s.O.length;i++)for(let j=0;j<3;j++){let Q=s.O.map((o,k)=>k===i?{...o,bad:o.bad.map(b=>b^(1<<j))}:o);let z=compare(Q,s.n,[]);assert(z.r>0,"neighbor");neighbors++;An+=z.A;Bn+=z.B}controls.push({name:s.name,root,neighbors,directNeighborNodes:An,jointNeighborNodes:Bn})}
 let budget=[];for(let i=0;i<fano.length;i++)for(let j=0;j<2;j++){let Q=fano.map((o,k)=>k===i?{...o,bad:[o.bad[j]]}:o),z=compare(Q,7,[]);assert(z.r===5,"budget neighbor");budget.push(z)}
 // Deterministic small random local regions: compare projection for every exterior word
 let seed=2601125;const rnd=n=>{seed=(Math.imul(1664525,seed)+1013904223)>>>0;return seed%n};
 let common=[],K=bs.common.find(x=>x.K===16),wide=K.residual.C.map(c=>({t:c.map(v=>Math.abs(v)-1),bad:[c.reduce((b,v,j)=>b+(v<0?2**j:0),0),c.reduce((b,v,j)=>b+(v>0?2**j:0),0)]}));
 for(const [name,O,n] of [["BW17",bw.O,bw.n],["K16",wide,bw.n]]){
 let a=Array(n).fill(-1),cc=closure(O,a),P=peel(O,a);let source=bits(12130883,n);assert(ok(bw.O,source),"BW17 supplied witness");assert(ok(O,source),"K16 supplied witness");
 // Replay existing reverse logs with deterministic valid values; authenticate the same word by each bucket.
 for(const L of K.residual.log){assert(L.bucket.every(c=>{let vals=[source[L.v-1],...c.map(v=>source[Math.abs(v)-1]^(v<0?1:0))];return vals.some(v=>v!==vals[0])}),"reverse bucket witness")}
 let direct=solve(O,n,[],false,2000),joint=solve(O,n,[],true,2000);assert(direct.status==="SAT"&&joint.status==="SAT","common solve");if(name==="K16"){for(const mode of [direct,joint]){let a=bits(mode.w,n);for(let i=K.residual.log.length-1;i>=0;i--){let {v,bucket}=K.residual.log[i];let valid=b=>bucket.every(c=>{let vs=[b,...c.map(x=>a[Math.abs(x)-1]^(x<0?1:0))];return vs.some(x=>x!==vs[0])});a[v-1]=valid(0)?0:1;assert(valid(a[v-1]),"reverse log");}assert(ok(bw.O,a),"K16 source lift");mode.source=a.reduce((s,b,i)=>s+b*2**i,0)}}
 common.push({name,closure:cc,forced:a.filter(v=>v>=0).length,rootPeeled:P.log.length,rootOwners:O.length,direct,joint})}
 let local={queries:0,regions:0,peeled:0,maxCore:0,forests:0,closureReject:0,exactReject:0};for(const s of [...sets,{name:"BW17",n:bw.n,O:bw.O}]){
 for(let trial=0;trial<80;trial++){let ids=new Set(),m=1+rnd(Math.min(4,s.O.length));while(ids.size<m)ids.add(rnd(s.O.length));let R=[...ids].map(i=>s.O[i]),vs=[...new Set(R.flatMap(o=>o.t))],k=rnd(Math.min(4,vs.length)+1),p=new Set();while(p.size<k)p.add(vs[rnd(vs.length)]);let pin=[...p],init=Array(s.n).fill(-1),P=peel(R,init,new Set(pin));local.regions++;local.peeled+=P.log.length;local.maxCore=Math.max(local.maxCore,P.rem.length);if(!P.rem.length)local.forests++;
 for(let w=0;w<2**k;w++){let g=pin.map((x,j)=>[x,(w>>>j)&1]),r=reference(R,s.n,g),q=reference(P.rem,s.n,g);assert(!!r===!!q,"projection decision");let out=solve(R,s.n,g,true);assert(out.status===(r?"SAT":"UNSAT"),"projection lift");let a=Array(s.n).fill(-1);for(let [x,b] of g)a[x]=b;if(!closure(R,a)){local.closureReject++;assert(!r,"closure false rejection")}if(!r)local.exactReject++;local.queries++}}}
 return {controls,budget,common,local,stats,seed:2601125};
}
console.log(JSON.stringify(run(...process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')))),null,2));
