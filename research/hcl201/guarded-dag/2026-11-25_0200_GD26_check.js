// Node.js: node GD26_check.js /path/to/BS19_results.json
const fs=require('node:fs');
function check(data){
 const abs=Math.abs, val=(l,w)=>((w>>>(abs(l)-1))&1)^(l<0?1:0), nae=(L,w)=>L.some(l=>val(l,w)!==val(L[0],w)), flip=L=>L.map(l=>-l);
 let assertions=0;function ok(v){assertions++;if(!v)throw Error("assertion "+assertions)}
 function gate(B,w,stats){let flags=0;for(const L of B){let b=val(L[0],w),mono=true;for(const l of L){stats.lit++;if(val(l,w)!==b){mono=false;break}}if(mono)flags|=1<<b;if(flags===3)return false}return true}
 function pivot(C,v){return {B:C.filter(L=>L.some(l=>abs(l)===v)).map(L=>L.includes(v)?L.filter(l=>l!==v):flip(L.filter(l=>l!==-v))),rest:C.filter(L=>!L.some(l=>abs(l)===v))}}
 function scan(C){const vs=[...new Set(C.flat().map(abs))].sort((a,b)=>a-b);return {vs,v:vs.reduce((a,b)=>C.filter(L=>L.some(l=>abs(l)===a)).length<=C.filter(L=>L.some(l=>abs(l)===b)).length?a:b)}}
 function closure(C){let scans=0;for(const L of C){scans+=L.length;ok(new Set(L.map(abs)).size===L.length);ok(L.length>=3)}return scans}
 function run(C,n,source,log,name){
  const scans=closure(C), {vs,v}=scan(C), {B,rest}=pivot(C,v), other=vs.filter(x=>x!==v), pairs=[];
  for(let i=0;i<B.length;i++)for(let j=i+1;j<B.length;j++)pairs.push([...B[i],...flip(B[j])]);
  let explicitLit=0,gateStats={lit:0},modelCount=0,word=null,projectionWords=0;
  const all=2**other.length;
  for(let i=0;i<all;i++){
   let w=other.reduce((w,x,j)=>w|(((i>>>j)&1)<<(x-1)),0);
   const e=pairs.every(L=>{let first=val(L[0],w);for(let j=1;j<L.length;j++){explicitLit++;if(val(L[j],w)!==first)return true}return false});
   const g=gate(B,w,gateStats);const original=[w,w|(1<<(v-1))].some(z=>B.every(L=>nae([v,...L],z)));
   ok(e===g&&g===original);if(g)projectionWords++;
   if(g&&rest.every(L=>nae(L,w))){
    modelCount++;if(word===null){let z=[w,w|(1<<(v-1))].find(z=>B.every(L=>nae([v,...L],z)));ok(C.every(L=>nae(L,z)));for(const item of log.slice().reverse()){ok(item.bucket.every(L=>L.length>0));const candidates=[z&~(1<<(item.v-1)),z|(1<<(item.v-1))];z=candidates.find(q=>item.bucket.every(L=>nae([item.v,...L],q)));ok(z!==undefined)}if(source)ok(source.O.every(o=>!o.bad.includes(o.t.reduce((s,x,j)=>s|(((z>>>x)&1)<<j),0))));word=z}
   }
  }
  return {name,n,pivot:v,bucket:B.length,tailLiterals:B.reduce((s,L)=>s+L.length,0),pairOwners:pairs.length,pairLiterals:pairs.reduce((s,L)=>s+L.length,0),exteriorWords:all,projectionWords,modelCount,sourceWitness:word,explicitLit,gateLit:gateStats.lit,closureScans:scans}
 }
 // On raw 24 variables test only pivot's actual local boundary; K16 has 14 free vars so enumerate full projected registry.
 const K=data.common.find(x=>x.K===16).residual;const shared=run(K.C,24,data.source,K.log,"BW17 K16 residual");
 const raw=data.common.find(x=>x.K===0).residual.C;const {v}=scan(raw),rawB=pivot(raw,v).B;let rawStats={lit:0};let rawChecks=0;const bv=[...new Set(rawB.flat().map(abs))];for(let i=0;i<2**bv.length;i++){let w=bv.reduce((w,x,j)=>w|(((i>>>j)&1)<<(x-1)),0);ok(gate(rawB,w,rawStats)===[w,w|(1<<(v-1))].some(z=>rawB.every(L=>nae([v,...L],z))));rawChecks++}
 // cubic graph K4 and K3,3: parity group, split NAE4 into two NAE3 using distinct auxiliaries; verify every local assignment and lift global SAT neighbor.
 function graphControl(edges,nv,odd){const E=edges.length,r=E+1;let next=r+1,groups=[], charges=Array.from({length:nv},(_,i)=>odd&&i===0?1:0);for(let u=0;u<nv;u++){let ids=edges.map((e,j)=>e.includes(u)?j+1:0).filter(Boolean),cs=[];ok(ids.length===3);for(let w=0;w<8;w++){if(((w&1)^((w>>1)&1)^((w>>2)&1))===charges[u])continue;let L=ids.map((id,j)=>w&(1<<j)?-id:id);let t=next++;cs.push([r,L[0],t],[-t,L[1],L[2]]);for(let a=0;a<8;a++){let z=ids.reduce((s,id,j)=>s|(((a>>>j)&1)<<(id-1)),0);ok([z,z|(1<<(t-1))].some(q=>nae([r,L[0],t],q)&&nae([-t,L[1],L[2]],q))===L.some(l=>val(l,z)))}}groups.push({ids,cs})}
 let count=0;for(let w=0;w<2**E;w++){let feasible=true;for(let u=0;u<nv;u++){const {ids,cs}=groups[u];let local=true;for(let i=0;i<cs.length;i+=2){let t=cs[i][2];local&&=[w,w|(1<<(t-1))].some(z=>nae(cs[i],z)&&nae(cs[i+1],z))}ok(local===(ids.reduce((a,l)=>a^val(l,w),0)===charges[u]));feasible&&=local}if(feasible)count++}ok((count>0)===!odd);return {vertices:nv,edges:E,odd,sourceModels:count,owners:groups.reduce((s,g)=>s+g.cs.length,0),gaussian:"sum of all vertex equations yields 0="+Number(odd)}}
 // K3,3 uses 34 coordinates if all aux distinct; JS bit operations wrap for t>=33, but t is only local and edge/ref indices <=10; wrapped private positions can collide. Use K4 only and a second 3-regular multigraph-free K4 charge flip.
 let g=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
 const controls=[graphControl(g,4,true),graphControl(g,4,false)];
 return {shared,raw:{pivot:v,degree:rawB.length,boundary:bv.length,rawChecks,gateLit:rawStats.lit},controls,assertions};
}
console.log(JSON.stringify(check(JSON.parse(fs.readFileSync(process.argv[2],'utf8'))),null,2));
