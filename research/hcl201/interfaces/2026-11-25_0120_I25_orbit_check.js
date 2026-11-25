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
function orbitReplay(inputs,files){
 const bit=i=>1n<<BigInt(i),assert=(a,m)=>{if(!a)throw Error(m||"assert")},comp=s=>s.replace(/[01]/g,x=>x==="0"?"1":"0");
 const out=[];
 for(let k=0;k<5;k++){const o=inputs[k],ms=inputs[5].jobs[k].combined,bh=inputs[6].jobs.find(x=>x.mode===true&&x.ref===files[k].ref);
  assert(JSON.stringify(o.guard)===JSON.stringify(ms.guard)&&JSON.stringify(o.guard)===JSON.stringify(bh.guard));
  const n=o.ownerIDs.length,R=o.rowMap.length,own=o.rowMap.map(x=>x[0]),g=Array.from({length:n},()=>[]),p=o.pairHex.map(x=>BigInt("0x"+x)),live=o.live.slice();own.forEach((x,i)=>g[x].push(i));
  let stat={ac:0,ternary:0,symmetry:0,addedImagePairBits:0,addedImageRows:0,addedImageTriples:0,anchorRemoved:0},ng=[],batch=[];
  function rel(a,b){return !!(p[a]&bit(b))}
  function closure(){let change=true;while(change){change=false;let ds=g.map(a=>a.filter(i=>live[i]));if(ds.some(a=>!a.length))return false;const masks=ds.map(a=>a.reduce((z,i)=>z|bit(i),0n));for(let a=0;a<R;a++)if(live[a])for(let j=0;j<n;j++)if(j!==own[a]){stat.ac++;if(!(p[a]&masks[j])){live[a]=false;change=true;break}}
    for(const t of ng){stat.ternary++;if(t.some(i=>!live[i]))continue;for(const a of t)if(t.every(b=>b===a||ds[own[b]].length===1&&ds[own[b]][0]===b)){live[a]=false;change=true;break}}
   }return g.every(a=>a.some(i=>live[i]))}
  assert(closure());const initial=live.filter(Boolean).length;let flip=Array(R).fill(-1),eligible=true;
  for(const a of g){const m=new Map(a.filter(i=>live[i]).map(i=>[o.rowMap[i][1],i]));for(const i of a)if(live[i]){const j=m.get(comp(o.rowMap[i][1]));if(j===undefined||j===i){eligible=false;break}flip[i]=j}}
  function invariant(){for(let a=0;a<R;a++)if(live[a]){if(flip[a]<0||!live[flip[a]])return false;for(let b=a+1;b<R;b++)if(live[b]&&own[a]!==own[b]){stat.symmetry++;if(rel(a,b)!==rel(b,a)||rel(a,b)!==rel(flip[a],flip[b]))return false}}return true}
  if(!eligible||!invariant()){out.push({ref:files[k].ref,id:o.id,guard:o.guard,initial,status:"DECLINE",stat});continue}
  for(const u of [ms,bh]){
   const direct=new Set(),image=new Set(),directRows=new Set((u.removedRows||[]).filter(i=>live[i]));
   for(const i of directRows){assert(flip[i]>=0);if(!directRows.has(flip[i]))stat.addedImageRows++;live[i]=live[flip[i]]=false}
   for(const [i,h] of u.delta||[]){if(!live[i])continue;let mask=BigInt("0x"+h);for(let j=0;j<R;j++)if(live[j]&&own[i]!==own[j]&&(mask&bit(j))){direct.add(i+":"+j);image.add(flip[i]+":"+flip[j])}}
   for(const x of image)if(!direct.has(x)){const [i,j]=x.split(":").map(Number);if(rel(i,j))stat.addedImagePairBits++}
   for(const x of new Set([...direct,...image])){const [i,j]=x.split(":").map(Number);p[i]&=~bit(j);p[j]&=~bit(i)}
   assert(closure());assert(invariant(),"symmetrized pair closure lost symmetry");batch.push(live.filter(Boolean).length)
  }
  const normalize=t=>t.slice().sort((a,b)=>a-b).join(",");
  const ds=new Set((bh.nogoods||[]).map(x=>x.rows).filter(t=>t.every(i=>live[i])).map(normalize));const both=new Set(ds);
  for(const s of ds){let t=s.split(",").map(Number);assert(new Set(t.map(i=>own[i])).size===3);let im=normalize(t.map(i=>flip[i]));if(!both.has(im)){stat.addedImageTriples++;both.add(im)}}
  ng=[...both].map(x=>x.split(",").map(Number));assert(closure());assert(invariant());assert(ng.every(t=>both.has(normalize(t.map(i=>flip[i])))));
  const pre=live.filter(Boolean).length,anchor=n-1,anchorRows=[];
  for(const i of g[anchor])if(live[i]&&o.rowMap[i][1]>o.rowMap[flip[i]][1]){live[i]=false;stat.anchorRemoved++;anchorRows.push(i)}
  let ok=closure(),final=live.filter(Boolean).length;
  const liveRows=live.map((v,i)=>v?i:-1).filter(i=>i>=0);
  out.push({ref:files[k].ref,id:o.id,guard:o.guard,initial,batch,pre,final,status:ok?"OPEN":"UNSAT",anchorOwner:o.ownerIDs[anchor],anchorRows,liveRows,stat,nogoods:ng.length})
 }
 return {files,tests:out};
}
const inputs=process.argv.slice(2).map(x=>JSON.parse(fs.readFileSync(x,'utf8')));if(inputs.length!==7)throw Error('seven inputs required');console.log(JSON.stringify(orbitReplay(inputs,files),null,2));
