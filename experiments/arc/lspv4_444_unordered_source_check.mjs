// LSPV-4/444 standalone restricted original-clause verifier.
// Usage: node experiments/arc/lspv4_444_unordered_source_check.mjs
// Fixed authenticated simple cubic K4 source. No full FLMV machine claim.
import assert from 'node:assert/strict';
let checks=0;
const check=(x)=>{assert(x);checks++};
const H=4, edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function source(chi){
 const adj=Array.from({length:H},()=>[]);
 edges.forEach(([u,v],i)=>{adj[u].push(i+1);adj[v].push(i+1)});
 return adj.flatMap((a,v)=>[0,1].flatMap(p=>[0,1].map(q=>
   a.map((e,i)=>[p,q,p^q^1^chi[v]][i]?-e:e))));
}
function idFor(c,chi){
 if(c.length!==3||c.some(x=>!Number.isInteger(x)||x===0))return -1;
 const s=[...c].sort((x,y)=>Math.abs(x)-Math.abs(y));
 const ids=s.map(Math.abs);
 if(new Set(ids).size!==3||ids[2]>edges.length)return -1;
 const e=ids.map(i=>edges[i-1]);
 const common=e[0].filter(v=>e[1].includes(v)&&e[2].includes(v));
 if(common.length!==1)return -1;
 const v=common[0];const adj=[];
 edges.forEach(([u,w],i)=>{if(u===v||w===v)adj.push(i+1)});
 adj.sort((a,b)=>a-b);
 if(adj.length!==3||adj.some((x,i)=>x!==ids[i]))return -1;
 const p=+(s[0]<0),q=+(s[1]<0),r=+(s[2]<0);
 return r===(p^q^1^chi[v])?4*v+2*p+q:-1;
}
function bucket(F,chi,b){
 const m=4*H;if(F.length!==m)return false;
 for(let start=0;start<m;start+=b){
  const count=new Uint8Array(Math.min(b,m-start));
  for(let c of F){
   const j=idFor(c,chi);
   if(j<0)return false;
   if(j>=start&&j<start+count.length)count[j-start]=Math.min(2,count[j-start]+1);
  }
  if(count.some(x=>x!==1))return false;
 }
 return true;
}
for(let parity of [0,1]){
 const chi=[parity,0,0,0],expected=source(chi);
 check(expected.length===16);
 for(let rotate=0;rotate<16;rotate++){
  const perm=expected.slice(rotate).concat(expected.slice(0,rotate));
  const reversed=perm.map(c=>[...c].reverse());
  const missingDuplicate=[...perm];missingDuplicate[0]=missingDuplicate[1];
  const foreign=[...perm];foreign[0]=[100,2,3];
  const wrongSign=[...perm];wrongSign[0]=[-wrongSign[0][0],...wrongSign[0].slice(1)];
  for(let b of [1,2,4,8,16]){
   check(bucket(perm,chi,b));
   check(bucket(reversed,chi,b));
   check(!bucket(missingDuplicate,chi,b));
   check(!bucket(foreign,chi,b));
   check(!bucket(wrongSign,chi,b));
   check(!bucket(perm.slice(1),chi,b));
   check(!bucket(perm.concat([perm[0]]),chi,b));
  }
 }
}
let subsets=0;
for(let mask=0;mask<(1<<16);mask++){
 let count=0;for(let i=0;i<16;i++)count+=(mask>>i)&1;
 if(count===8)subsets++;
}
check(subsets===12870);
console.log(JSON.stringify({status:'PASS',assertions:checks,half_prefix_subsets:subsets,scope:'K4 exact unordered-source checker; not native FLMV'},null,2));
