// Node.js: supply seven JSON files in exact order in results.files.
const fs=require('fs');
const files=[
  {
    "ref": "1fc8b6c7157cb8db0a0a9f26dee59ba74195aa9a",
    "path": "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_0.json"
  },
  {
    "ref": "1e765e0e95ae0a6eeea5a1b43a5c8c525f82e5fd",
    "path": "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_1.json"
  },
  {
    "ref": "80b472196e2bd606c45cd95bf2190618748d5606",
    "path": "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_2.json"
  },
  {
    "ref": "37578c1135e1bade2d1c6847235cd61500092c58",
    "path": "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_3.json"
  },
  {
    "ref": "33f9839bb80d205ad94af013b6141aeb119f8e87",
    "path": "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_4.json"
  },
  {
    "ref": "ecbbf26c6a5d9b2b53f5942b1889131c3ebe1fce",
    "path": "research/hcl201/multisign/2026-11-25_0028_MS24_results.json"
  },
  {
    "ref": "ab85c853f3296c2423910ba3aee8b7db8189037c",
    "path": "research/constructive-shared-hubs/hard-residuals/2026-11-25_0042_BH18_feedback_results.json"
  }
];
function run(inputs,files){
 const assert=(a,m)=>{if(!a)throw Error(m||"assert")};
 function solve(o,updates=[]){
  const n=o.ownerIDs.length,R=o.rowMap.length,owner=o.rowMap.map(x=>x[0]),bit=Array.from({length:R},(_,i)=>1n<<BigInt(i)),p=o.pairHex.map(x=>BigInt("0x"+x)),live=o.live.slice(),masks=Array(n).fill(0n),groups=Array.from({length:n},()=>[]);
  for(let i=0;i<R;i++){groups[owner[i]].push(i);if(live[i])masks[owner[i]]|=bit[i]}
  let stats={acScans:0,partitions:0,cliqueChecks:0,matchingCalls:0,augmentScans:0,deleted:0,upstreamDeleted:0},certs=[];
  function del(i){if(live[i]){live[i]=false;masks[owner[i]]&=~bit[i];return true}return false}
  function ac(){let change=true;while(change){change=false;if(masks.some(x=>!x))return false;for(let i=0;i<R;i++)if(live[i])for(let j=0;j<n;j++)if(j!==owner[i]){stats.acScans++;if(!(p[i]&masks[j])){del(i);change=true;break}}}return !masks.some(x=>!x)}
  function check(){for(let i=0;i<R;i++)if(live[i])for(let j=i+1;j<R;j++)if(live[j]&&owner[i]!==owner[j])assert(Boolean(p[i]&bit[j])===Boolean(p[j]&bit[i]),"asymmetric")}
  check();if(!ac())return {id:o.id,guard:o.guard,status:"UNSAT",stats,certs};
  for(const u of updates){for(const i of u.removedRows||[])del(i);for(const [i,h] of u.delta||[]){let b=BigInt("0x"+h);p[i]&=~b;}check();if(!ac())return {id:o.id,guard:o.guard,status:"UNSAT",stats,certs}}
  const initial=live.filter(Boolean).length;
  function partition(reverse){
   stats.partitions++;let order=Array.from({length:R},(_,i)=>i).filter(i=>live[i]);if(reverse)order.reverse();
   let unused=order.reduce((a,i)=>a|bit[i],0n),buckets=[],which=Array(R).fill(-1);
   for(const i of order){if(!(unused&bit[i]))continue;let b=[i],used=new Set([owner[i]]);unused&=~bit[i];let eligible=unused&~p[i]; // within-owner entries may be marked compatible; handle explicitly
    eligible=unused&(~p[i]|masks[owner[i]]);
    for(let pass=0;pass<2;pass++)for(const j of order){if(!(eligible&bit[j])||!(unused&bit[j])||(pass===0&&used.has(owner[j])))continue;b.push(j);used.add(owner[j]);unused&=~bit[j];eligible&=(~p[j]|masks[owner[j]])&unused;}
    for(const a of b){which[a]=buckets.length;for(const c of b)if(a<c){stats.cliqueChecks++;assert(owner[a]===owner[c]||!(p[a]&bit[c]),"clique")}}
    buckets.push(b)
   }
   return {buckets,which};
  }
  function test(P,fixOwner=-1,fixBucket=-1){
   stats.matchingCalls++;const adj=groups.map(g=>[...new Set(g.filter(i=>live[i]).map(i=>P.which[i]))]);let match=Array(P.buckets.length).fill(-1);
   if(fixOwner>=0){assert(adj[fixOwner].includes(fixBucket));adj[fixOwner]=[fixBucket];}
   for(let a=0;a<n;a++){let seen=new Set(),owners=new Set();function aug(i){owners.add(i);for(const b of adj[i]){stats.augmentScans++;if(seen.has(b))continue;seen.add(b);if(match[b]<0||aug(match[b])){match[b]=i;return true}}return false}
    if(!aug(a)){let O=[...owners],B=[...seen];assert(B.length<O.length);assert(O.every(i=>adj[i].every(b=>seen.has(b))));return {ok:false,O,B}}
   }return {ok:true}
  }
  let changed=true;
  while(changed){changed=false;for(let rev of [false,true]){
   let P=partition(rev),root=test(P);if(!root.ok){certs.push({type:"root",buckets:P.buckets,...root});return {id:o.id,guard:o.guard,status:"UNSAT",initial,stats,certs}}
   let groupsByEdge=new Map();for(let i=0;i<R;i++)if(live[i]){let key=owner[i]+":"+P.which[i];if(!groupsByEdge.has(key))groupsByEdge.set(key,[]);groupsByEdge.get(key).push(i)}
   let doomed=[];for(const rows of groupsByEdge.values()){let i=rows[0],z=test(P,owner[i],P.which[i]);if(!z.ok){doomed.push(...rows);certs.push({type:"pin",rows,fix:[owner[i],P.which[i]],O:z.O,B:z.B,buckets:P.buckets})}}
   if(doomed.length){for(const i of doomed)if(del(i))stats.deleted++;changed=true;if(!ac())return {id:o.id,guard:o.guard,status:"UNSAT",initial,stats,certs}}
  }}
  const final=live.filter(Boolean).length;
  let witness=null;if(masks.every(x=>x&&(x&(x-1n))===0n)){witness=groups.map(g=>g.find(i=>live[i]));assert(witness.every(i=>witness.every(j=>owner[i]===owner[j]||Boolean(p[i]&bit[j]))));}
  return {id:o.id,guard:o.guard,status:witness?"SAT":"OPEN",initial,final,stats,certs,witness};
 }
 function chart(id,domains,compat){let rowMap=domains.flatMap((d,i)=>d.map(x=>[i,x]));return {id,guard:[],ownerIDs:domains.map((_,i)=>i),rowMap,live:rowMap.map(()=>true),pairHex:rowMap.map(([i,a])=>rowMap.reduce((z,[j,b],k)=>i!==j&&compat(i,a,j,b)?z|(1n<<BigInt(k)):z,0n).toString(16))}}
 function exhaustive(o){let ds=o.ownerIDs.map((_,i)=>o.rowMap.map((x,j)=>x[0]===i?j:-1).filter(x=>x>=0)),p=o.pairHex.map(x=>BigInt("0x"+x)),count=0,support=new Set();function f(a){if(a.length===ds.length){count++;a.forEach(x=>support.add(x));return}for(let i of ds[a.length])if(a.every(j=>p[i]&(1n<<BigInt(j))))f([...a,i])}f([]);return {count,support}}
 let controls=[];for(const [n,q,missing] of [[4,3,false],[3,3,false],[4,3,true],[5,4,false],[4,4,false]]){
 let o=chart(`K${n}-${q}-${missing}`,Array.from({length:n},()=>Array.from({length:q},(_,i)=>i)),(i,a,j,b)=>missing&&Math.min(i,j)===0&&Math.max(i,j)===1||a!==b),r=solve(o),e=exhaustive(o);assert(r.status!=="UNSAT"||!e.count);for(let c of r.certs)if(c.type==="pin")assert(c.rows.every(i=>!e.support.has(i)));controls.push({count:e.count,...r})
 }
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 for(let signed of [false,true]){let o=chart("Fano"+signed,fano.map((_,i)=>Array.from({length:8},(_,x)=>x).filter(x=>{let y=x^(signed&&i===0?1:0);return y!==0&&y!==7})),(i,a,j,b)=>fano[i].every((v,k)=>!fano[j].includes(v)||((a>>k)&1)===((b>>fano[j].indexOf(v))&1))),r=solve(o),e=exhaustive(o);assert(r.status!=="UNSAT"||!e.count);for(let c of r.certs)if(c.type==="pin")assert(c.rows.every(i=>!e.support.has(i)));controls.push({count:e.count,...r})}
 const jobs=inputs.slice(0,5).map((o,i)=>{let ms=inputs[5].jobs[i].combined,bh=inputs[6].jobs.find(x=>x.mode===true&&x.ref===files[i].ref);assert(JSON.stringify(ms.guard)===JSON.stringify(o.guard)&&JSON.stringify(bh.guard)===JSON.stringify(o.guard));return {ref:files[i].ref,baseline:solve(o),combined:solve(o,[ms,bh])}});
 return {files,controls,jobs};
}
const inputs=process.argv.slice(2).map(x=>JSON.parse(fs.readFileSync(x,'utf8')));if(inputs.length!==7)throw Error('seven files required');console.log(JSON.stringify(run(inputs,files),null,2));
