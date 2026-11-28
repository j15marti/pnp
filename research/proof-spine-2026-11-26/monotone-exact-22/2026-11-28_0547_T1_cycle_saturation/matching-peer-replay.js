// Recompute peer shell supports, blind pair ownership masks and tagged exact affine lift.
function replayPeer(raw,sha){
 const enc=x=>JSON.stringify(x)+"\n",v=x=>BigInt("0x"+x),hex=x=>x.toString(16),out=[];
 for(const p of raw){
  const c=p.cert,F=c.source;if("DELETION-SYNDROME-v1:sha256:"+sha(enc(F))!==c.instance_id||c.N!==8*enc(F).length||p.certificate_id!=="CERT-v1:sha256:"+sha(enc(c)))throw Error("authentication");
  const ct={clones:0,matching:0,ownership:0,pair:0,rank:0,replay:0};const n=F.labels.length,q=F.q,d=F.adj.length,target=v(F.target),options=[];
  function match(A,skip=-1){let own=Array(q).fill(-1);function aug(i,S){for(const j of A[i]){ct.matching++;if(j===skip||S.has(j))continue;S.add(j);if(own[j]<0||aug(own[j],S)){own[j]=i;return true}}return false}for(let i=0;i<A.length;i++)if(!aug(i,new Set()))return null;return own}
  for(let i=0;i<d;i++){ct.clones++;if(!match(F.adj.concat(Array.from({length:q-d},()=>F.adj[i]))))throw Error("Hall premise")}
  if(q-d!==1)throw Error("scope");for(let i=0;i<n;i++){let O=[];for(let j=0;j<q;j++){let w=match(F.adj,j);if(w)O.push({j,w,v:v(F.labels[i][j])})}if(O.length!==q)throw Error("Hall response");options.push(O)}
  let m=target.toString(2).length;for(const O of options)for(const a of O)m=Math.max(m,a.v.toString(2).length);
  const owners=Array.from({length:m},(_,b)=>options.map((O,i)=>{ct.ownership+=O.length;return O.some(a=>a.v&(1n<<BigInt(b)))?i:-1}).filter(i=>i>=0));
  let masks=new Map();for(let b=0;b<m;b++){const a=owners[b];if(a.length===2){let k=a.join(",");masks.set(k,(masks.get(k)||0n)|(1n<<BigInt(b)))}}
  let used=new Set(),pairs=[];for(const [k,mask] of masks){const [i,j]=k.split(",").map(Number);if(used.has(i)||used.has(j))continue;used.add(i);used.add(j);let O=[];for(const a of options[i])for(const b of options[j]){ct.pair++;if(((a.v^b.v^target)&mask)===0n)O.push([a.j,b.j,hex(a.v^b.v)])}pairs.push({i,j,mask:hex(mask),out:O})}
  if(used.size!==n)throw Error("pair cover");
  for(const a of c.pairs){ct.replay++;const b=pairs.find(z=>z.i===a.i&&z.j===a.j);const shifted=b?.out.map(([i,j,x])=>[i+1,j+1,x]);if(!b||b.mask!==a.mask||JSON.stringify(shifted)!==JSON.stringify(a.out))throw Error("peer pair mismatch "+c.instance_id+" "+JSON.stringify({a,b}))}
  function basis(){let B=new Map();return {B,insert(x,t=0n){while(x){let k=x.toString(2).length-1;if(!B.has(k)){B.set(k,[x,t]);return}let [y,u]=B.get(k);x^=y;t^=u;ct.rank++}},reduce(x){let t=0n;while(x){let k=x.toString(2).length-1;if(!B.has(k))break;let [y,u]=B.get(k);x^=y;t^=u;ct.rank++}return [x,t]}}}
  function affine(groups){let B=basis(),off=0n,gens=[];for(let i=0;i<groups.length;i++){const O=groups[i];if(!O.length)return {status:"NO_EMPTY"};const vals=[...new Set(O.map(x=>x[2]))].map(v),a=vals[0],C=basis();off^=a;for(const x of vals)C.insert(x^a);if(BigInt(vals.length)!==(1n<<BigInt(C.B.size)))return {status:"UNKNOWN_NONAFFINE"};for(const [y] of C.B.values()){B.insert(y,1n<<BigInt(gens.length));gens.push([i,y])}}
  const [r,t]=B.reduce(target^off);if(r)return {status:"NO_AFFINE",rank:B.B.size};const W=groups.map(O=>v(O[0][2]));gens.forEach(([i,y],k)=>{if(t&(1n<<BigInt(k)))W[i]^=y});const chosen=groups.map((O,i)=>O.find(x=>v(x[2])===W[i]));if(chosen.some(x=>!x))throw Error("joint lift");return {status:"YES",rank:B.B.size,chosen}}
  const all=affine(pairs.map(z=>z.out));if((c.decision==="YES")!==(all.status==="YES")||!["YES","NO_EMPTY","NO_AFFINE"].includes(all.status))throw Error("peer outcome");
  if(all.status==="YES"){let sum=0n,lift=[];for(let i=0;i<pairs.length;i++){let p=pairs[i],a=all.chosen[i];for(const [r,j] of [[p.i,a[0]],[p.j,a[1]]]){let O=options[r].find(z=>z.j===j);if(!O)throw Error("invalid");sum^=O.v;lift.push([r,j,O.w]);}}if(sum!==target)throw Error("syndrome");all.lift=lift;}
  let baseline=basis(),a=0n;for(const O of options){a^=O[0].v;for(const z of O)baseline.insert(z.v^O[0].v)}const rawAffine=baseline.reduce(target^a)[0]===0n;
  const record={instance_id:c.instance_id,original_N_bits:c.N,guard_id:"EMPTY",residual_id:"ROOT",original_ids:c.original_ids,parent:p.certificate_id,source:F,rawAffine,discoveredPairs:pairs,decision:all,ct,sourcePin:"b1bd8ec2b83f3b4f782ad7236da963d54a7b4e7e",indexing:"this output uses zero-based deleted bins, peer uses one-based"};out.push({certificate_id:"CERT-v1:sha256:"+sha(enc(record)),record})
 }
 return out;
}
const fs=require('node:fs'),crypto=require('node:crypto');console.log(JSON.stringify(replayPeer(JSON.parse(fs.readFileSync(process.argv[2],'utf8')),s=>crypto.createHash('sha256').update(s).digest('hex'))));
