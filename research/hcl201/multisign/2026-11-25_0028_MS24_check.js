function run(job, prior=null, cap=128) {
  const tables=job.finalTables, n=job.witness?.length||Math.max(...tables.flatMap(t=>t.v),...job.guard.map(g=>g[0]))+1;
  const owners=tables.map(t=>t.v), map=prior?prior.rowMap:tables.flatMap((t,i)=>t.a.map(s=>[i,s]));
  const R=map.length,m=owners.length, bit=Array.from({length:R},(_,i)=>1n<<BigInt(i)), vb=Array.from({length:n},(_,i)=>1n<<BigInt(i)), C=1n<<BigInt(n), mask=C-1n;
  const rowInt=map.map(([i,s])=>[...s].reduce((a,b,j)=>a+(Number(b)<<j),0));
  const all=owners.map(()=>0n), ix=owners.map(()=>[]);
  for(let i=0;i<R;i++){const a=map[i][0];if(!tables[a].a.includes(map[i][1]))throw Error("row provenance");all[a]|=bit[i];ix[a].push(i);}
  if(prior&&(JSON.stringify(prior.guard)!==JSON.stringify(job.guard)||prior.id!==job.id||JSON.stringify(prior.ownerIDs)!==JSON.stringify(tables.map(t=>t.id))))throw Error("guard/owner mismatch");
  const cnt={pivots:0,closurePasses:0,rowScans:0,pairScans:0,gaussXor:0,localHullRows:0,conditionalContradictions:0,deletedRows:0,deletedPairs:0,acceptedBatches:0};
  let live=0n;for(let i=0;i<R;i++)if((!prior||prior.live[i])&&job.guard.every(([v,b])=>{let k=owners[map[i][0]].indexOf(v);return k<0||Number(map[i][1][k])===b}))live|=bit[i];
  const adj=Array(R).fill(0n);
  function agree(i,j){const a=map[i][0],b=map[j][0];if(a===b)return false;for(let k=0;k<owners[a].length;k++){let l=owners[b].indexOf(owners[a][k]);if(l>=0&&map[i][1][k]!==map[j][1][l])return false;}return true;}
  for(let i=0;i<R;i++)if(prior)adj[i]=BigInt("0x"+(prior.pairHex[i]||"0"));else for(let j=0;j<R;j++)if(agree(i,j))adj[i]|=bit[j];
  const startAdj=adj.slice(),startLive=live;
  function parity(x){let p=0;while(x){p^=1;x&=x-1;}return p;}
  function hull(a,domain){
    let anchor=-1;const k=owners[a].length,B=Array(k).fill(0);if(k>24)throw Error("local arity cap");
    for(let i of ix[a]){cnt.localHullRows++;if(!(domain&bit[i]))continue;let w=rowInt[i];if(anchor<0){anchor=w;continue;}w^=anchor;for(let p=k-1;p>=0&&w;p--)if(w&(1<<p)){if(B[p]){w^=B[p];cnt.gaussXor++;}else{B[p]=w;break;}}}
    if(anchor<0)return null;
    const eq=[];for(let f=0;f<k;f++)if(!B[f]){let q=1<<f;for(let p=0;p<k;p++)if(B[p]&&parity(B[p]&q))q|=1<<p;let x=parity(q&anchor)?C:0n;for(let j=0;j<k;j++)if(q&(1<<j))x|=vb[owners[a][j]];eq.push(x);}
    return eq;
  }
  function make(domains){const B=Array(n).fill(0n);
    function add(w){for(let p=n-1;p>=0;p--)if(w&vb[p]){if(B[p]){w^=B[p];cnt.gaussXor++;}else{B[p]=w;return true;}}return w===0n;}
    for(const [v,b] of job.guard)if(!add(vb[v]|(b?C:0n)))return null;
    for(let a=0;a<m;a++){const h=hull(a,domains[a]);if(h===null)return null;for(const w of h)if(!add(w))return null;}return B;
  }
  function localProjection(B,a){const Q=Array(n).fill(null), eq=[];const scope=owners[a];
    for(let j=0;j<scope.length;j++){let w=vb[scope[j]],q=1<<j;for(let p=n-1;p>=0;p--)if((w&vb[p])&&B[p]){w^=B[p];cnt.gaussXor++;}
      for(let p=n-1;p>=0;p--)if(w&vb[p]){if(Q[p]){w^=Q[p][0];q^=Q[p][1];cnt.gaussXor++;}else{Q[p]=[w,q];break;}}
      if(!(w&mask))eq.push([q,w&C?1:0]);}
    return eq;
  }
  function bad(i,E){return E.some(([q,b])=>parity(q&rowInt[i])!==b);}
  function removeRow(i){if(live&bit[i]){live^=bit[i];cnt.deletedRows++;}}
  function removePair(i,j){if(adj[i]&bit[j]){adj[i]^=bit[j];adj[j]&=~bit[i];cnt.deletedPairs++;}}
  function close(){while(true){cnt.closurePasses++;let changed=false;for(let a=0;a<m;a++)if(!(live&all[a]))return false;
    for(let i=0;i<R;i++)if(live&bit[i]){cnt.rowScans++;for(let a=0;a<m;a++)if(a!==map[i][0]&&!(adj[i]&live&all[a])){removeRow(i);changed=true;break;}}
    const B=make(all.map(x=>x&live));if(!B)return false;
    for(let a=0;a<m;a++){const E=localProjection(B,a);for(let i of ix[a])if(live&bit[i]){cnt.rowScans++;if(bad(i,E)){removeRow(i);changed=true;}}}
    if(!changed)return true;
  }}
  const startRows=()=>ix.reduce((s,ids)=>s+ids.filter(i=>!!(live&bit[i])).length,0);
  let ok=close(), complete=false, baselineRows=cnt.deletedRows;
  // A bounded deterministic pass; reclose after every accepted conditional batch.
  if(ok){let dirty=true;while(dirty&&cnt.pivots<cap&&ok){dirty=false;let exhausted=true;for(let i=0;i<R;i++)if(live&bit[i]){
    if(cnt.pivots>=cap){exhausted=false;break;}cnt.pivots++;const a=map[i][0], D=all.map((x,j)=>j===a?bit[i]:x&live&adj[i]), B=make(D);
    if(!B){cnt.conditionalContradictions++;removeRow(i);dirty=true;cnt.acceptedBatches++;ok=close();if(!ok)break;continue;}
    let changes=0;for(let b=0;b<m;b++)if(b!==a){const E=localProjection(B,b);if(E.length)for(let j of ix[b])if(D[b]&bit[j]){cnt.pairScans++;if(bad(j,E)){removePair(i,j);changes++;}}}
    if(changes){dirty=true;cnt.acceptedBatches++;ok=close();if(!ok)break;}
  } if(exhausted&&!dirty&&ok){complete=true;break;}}}
  let witnessOK=null;if(job.witness){const ids=owners.map((v,a)=>{const s=v.map(k=>job.witness[k]).join("");return ix[a].find(i=>map[i][1]===s);});witnessOK=ok&&ids.every(i=>i!==undefined&&(live&bit[i]))&&ids.every(i=>ids.every(j=>i===j||!!(adj[i]&bit[j])))&&job.guard.every(([v,b])=>job.witness[v]===b);if(!witnessOK)throw Error("known model lost "+job.id);}
  const removedRows=map.map((_,i)=>i).filter(i=>(startLive&bit[i])&&!(live&bit[i]));
  const delta=adj.map((x,i)=>[i,(x^startAdj[i]).toString(16)]).filter(([i,s])=>s!=="0");
  return {id:job.id,guard:job.guard,prior:!!prior,initial:R,final:startRows(),ok,complete,baselineRows,witnessOK,cnt,removedRows,delta};
}
function controls(){
 const triples=[[0,1,2],[0,3,4],[1,3,5],[2,4,5]];
 function gated(label,both,neighbor){const T=[];for(let side=0;side<(both?2:1);side++)for(let i=0;i<4;i++){const v=[6,...triples[i]],a=[];for(let w=0;w<16;w++){const s=Array.from({length:4},(_,j)=>w>>j&1);if(s[0]!==side||(s[1]^s[2]^s[3])===(i===3&&!neighbor?1:0))a.push(s.join(""));}T.push({id:T.length,v,a});}
 const j={id:label,guard:[],finalTables:T};let models=[];for(let w=0;w<128;w++){let x=Array.from({length:7},(_,i)=>w>>i&1);if(T.every(t=>t.a.includes(t.v.map(v=>x[v]).join(""))))models.push(x);}if(models.length)j.witness=models[0];return {j,models:models.length};}
 const fano=[[0,1,2],[0,3,4],[0,5,6],[1,3,5],[1,4,6],[2,3,6],[2,4,5]];
 function nae(neighbor){const T=(neighbor?fano.slice(0,-1):fano).map((v,id)=>({id,v,a:["001","010","011","100","101","110"]}));const j={id:"Fano"+(neighbor?"-deletion":""),guard:[],finalTables:T};let models=[];for(let w=0;w<128;w++){let x=Array.from({length:7},(_,i)=>w>>i&1);if(T.every(t=>t.a.includes(t.v.map(v=>x[v]).join(""))))models.push(x);}if(models.length)j.witness=models[0];return {j,models:models.length};}
 return [gated("gate-forced",false,false),gated("gate-UNSAT",true,false),gated("gate-SAT",true,true),nae(false),nae(true)];
}
const fs=require('fs');const jobs=JSON.parse(fs.readFileSync(process.argv[2],'utf8')).results.filter(j=>j.mode==='pair'&&j.cap===0);const pairs=process.argv.slice(3).map(p=>JSON.parse(fs.readFileSync(p,'utf8')));const result={refs:["1fc8b6c7157cb8db0a0a9f26dee59ba74195aa9a","1e765e0e95ae0a6eeea5a1b43a5c8c525f82e5fd","80b472196e2bd606c45cd95bf2190618748d5606","37578c1135e1bade2d1c6847235cd61500092c58","33f9839bb80d205ad94af013b6141aeb119f8e87"],drRef:"9ac7e9d745b7220f0634990bd08d919313471f82",cap:128,controls:controls().map(({j,models})=>({models,result:run(j,null,10000)})),jobs:jobs.map((j,i)=>({standalone:run(j,null,128),combined:run(j,pairs[i],128)}))};console.log(JSON.stringify(result));
