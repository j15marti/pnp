const fs=require('fs');
const specs=[
  [
    "1e765e0e95ae0a6eeea5a1b43a5c8c525f82e5fd",
    "research/constructive-shared-hubs/multisign-dag/2026-11-25_0021_BD18_pairs_1.json"
  ],
  [
    "ecbbf26c6a5d9b2b53f5942b1889131c3ebe1fce",
    "research/hcl201/multisign/2026-11-25_0028_MS24_results.json"
  ],
  [
    "ab85c853f3296c2423910ba3aee8b7db8189037c",
    "research/constructive-shared-hubs/hard-residuals/2026-11-25_0042_BH18_feedback_results.json"
  ],
  [
    "bdda062d50962d29343f7413764acfdf5edbc21b",
    "research/hcl201/interfaces/2026-11-25_0120_I25_orbit_results.json"
  ],
  [
    "ee97e4fb999b380ca981c892ce6913369b5e574a",
    "research/hcl201/multisign/2026-11-25_0136_MS26_results.json"
  ]
];
function run2(inputs){
const [o,ms,bh,ii,ms26]=inputs,bit=i=>1n<<BigInt(i),assert=(x,m)=>{if(!x)throw Error(m)},eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
let own=o.rowMap.map(x=>x[0]),groups=o.ownerIDs.map((_,i)=>own.flatMap((x,j)=>x===i?[j]:[])),R=own.length,f=own.map((i,a)=>groups[i].find(b=>o.rowMap[b][1]===o.rowMap[a][1].replace(/[01]/g,x=>x==="0"?"1":"0")));
let root={live:o.live.slice(),p:o.pairHex.map(x=>BigInt("0x"+x)),ng:[]};
const clone=s=>({live:s.live.slice(),p:s.p.slice(),ng:s.ng.slice()}),stat=()=>({ac:0,ng:0,probes:0}),cnt=s=>s.live.filter(Boolean).length;
function cut(s,a,b){let old=!!(s.p[a]&bit(b));s.p[a]&=~bit(b);s.p[b]&=~bit(a);return old}
function close(s,t){for(;;){let d=groups.map(g=>g.filter(a=>s.live[a]));if(d.some(g=>!g.length))return false;let masks=d.map(g=>g.reduce((z,a)=>z|bit(a),0n)),ch=false;for(let a=0;a<R;a++)if(s.live[a])for(let j=0;j<d.length;j++)if(j!==own[a]){t.ac++;if(!(s.p[a]&masks[j])){s.live[a]=false;ch=true;break}}if(ch)continue;for(let g of s.ng){t.ng++;if(g.some(a=>!s.live[a]))continue;let u=g.filter(a=>d[own[a]].length!==1);if(!u.length)return false;if(u.length===1){s.live[u[0]]=false;ch=true}if(u.length===2&&cut(s,...u))ch=true}if(!ch)return true}}
let t=stat();assert(close(root,t),"initial");
let imports=[ms.jobs[1].combined,bh.jobs.find(x=>x.mode===true&&x.ref.startsWith("1e765e0"))];
for(let u of imports){assert(eq(u.guard,o.guard),"guard");for(let a of u.removedRows||[]){root.live[a]=false;root.live[f[a]]=false}for(let [a,h]of u.delta||[])for(let b=0;b<R;b++)if(BigInt("0x"+h)&bit(b)){cut(root,a,b);cut(root,f[a],f[b])}for(let q of u.nogoods||[])root.ng.push(q.rows,q.rows.map(a=>f[a]));assert(close(root,t),"import")}
const or=ii.tests[1],aidx=o.ownerIDs.indexOf(or.anchorOwner),removed=new Set(or.anchorRows),S=groups[aidx].filter(a=>root.live[a]&&!removed.has(a)),C=groups[aidx].filter(a=>root.live[a]&&removed.has(a));assert(S.length===C.length&&S.every(a=>removed.has(f[a])),"phase partition");
let prior=[[6,229],[8,200],[8,229],[145,218],[145,249],[248,295],[248,308],[249,295],[250,312]],actual=ms26.results.shared.find(x=>x.name==="I25+MS25-anchor"&&!x.alg);assert(eq(actual.representativeAnchor,or.anchorRows),"anchor");
let aug=clone(root),unique=new Set(root.ng.map(g=>g.slice().sort((a,b)=>a-b).join(","))),added=[],pairAdded=[];
function insert(rows){let v=[...new Set(rows)].sort((a,b)=>a-b);if(new Set(v.map(a=>own[a])).size!==v.length)return;if(v.some(a=>!aug.live[a]))return;if(v.some((a,i)=>v.slice(i+1).some(b=>!(aug.p[a]&bit(b)))))return;let k=v.join(",");if(unique.has(k))return;unique.add(k);if(v.length===2){if(cut(aug,...v))pairAdded.push(v)}else if(v.length===3){aug.ng.push(v);added.push(v)}else throw Error("unexpected arity")}
for(let [a,b]of [...prior,...actual.deletedPairs]){for(let c of S)insert([a,b,c]);for(let c of C)insert([f[a],f[b],c])}
assert(close(aug,t),"aug closure");
let results=[];for(let [label,s]of [["baseline",root],["transported",aug]]){let st=clone(s),q=stat(),baseRows=cnt(st),cuts=[],del=[],order=[...new Set([...prior.flat(),...groups.slice().sort((a,b)=>a.length-b.length).flat()])];for(let a of order){if(q.probes>=64)break;if(!st.live[a])continue;let h=clone(st);for(let b of groups[own[a]])if(b!==a)h.live[b]=false;q.probes++;if(!close(h,q)){st.live[a]=false;del.push(a)}else for(let b=0;b<R;b++)if(st.live[b]&&own[a]!==own[b]&&(st.p[a]&bit(b))&&!h.live[b]){cut(st,a,b);cuts.push([a,b])}if(!close(st,q))break}results.push({label,baseRows,finalRows:cnt(st),cuts,del,stats:q})}
return {id:o.id,guard:o.guard,anchorOwner:or.anchorOwner,anchorRows:S,oppositeRows:C,originalNogoods:root.ng.length,guardedPairs:prior.length+actual.deletedPairs.length,addedTriples:added,addedPairs:pairAdded,importStats:t,results};
}
const inputs=process.argv.slice(2).map(p=>JSON.parse(fs.readFileSync(p,'utf8')));if(inputs.length!==specs.length)throw Error('five input JSON files in specs order');console.log(JSON.stringify(run2(inputs),null,2));
