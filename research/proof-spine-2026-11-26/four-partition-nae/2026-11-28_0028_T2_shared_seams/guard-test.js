// Guarded phase support check. Uses already source-audited manifest maps.
function run(manifest,sha){
 const enc=x=>JSON.stringify(x)+"\n",out=[];
 for(const t of manifest.instances.filter(x=>x.n===12)){
  const B=t.certificate.map.B,E=t.certificate.map.E,n=t.n,m=B.length,cnt=new Map();
  for(const b of B)for(const l of b)cnt.set(Math.abs(l),(cnt.get(Math.abs(l))||0)+1);
  const words=[];
  for(let w=0;w<2**n;w++){
   let mask=0;for(let i=0;i<m;i++)if(B[i].every(l=>((w>>(Math.abs(l)-1))&1)===+(l>0)))mask|=1<<i;
   words.push({w,mask});
  }
  let guards=[],seed=271128;function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed}
  for(let k=0;k<=6;k++)for(let q=0;q<12;q++){
   let pins=new Map();
   for(let i=0;i<k;i++)pins.set(Math.abs(B[i].find(l=>cnt.get(Math.abs(l))===1)),q===0?1:rand()>>>31);
   if(q%3===1)pins.set(7,rand()>>>31);
   if(q%3===2){pins.set(8,rand()>>>31);pins.set(9,rand()>>>31)}
   guards.push([...pins].sort((a,b)=>a[0]-b[0]));
  }
  let unique=[...new Map(guards.map(g=>[enc(g),g])).values()];
  let supportChecks=0,branchTests=0,originalWordsScanned=0,maxExceptions=0,maxBranchUpper=0,caseRows=[];
  for(let g of unique){
   let pins=new Map(g),exact=new Set();
   for(let {w,mask} of words){originalWordsScanned++;if(g.every(([v,b])=>((w>>(v-1))&1)===b))exact.add(mask)}
   let simp=B.map(b=>({disabled:b.some(l=>pins.has(Math.abs(l))&&pins.get(Math.abs(l))!==+(l>0)),free:b.filter(l=>!pins.has(Math.abs(l)))}));
   let ex=simp.map((z,i)=>!z.disabled&&!z.free.some(l=>cnt.get(Math.abs(l))===1)?i:-1).filter(i=>i>=0);
   let upper=ex.reduce((a,i)=>a*(1+simp[i].free.length),1);
   maxExceptions=Math.max(maxExceptions,ex.length);maxBranchUpper=Math.max(maxBranchUpper,upper);
   function admit(mask){
    let a=new Map(pins);
    for(let i=0;i<m;i++)if(mask>>i&1){
     if(simp[i].disabled)return false;
     for(let l of simp[i].free){let v=Math.abs(l),b=+(l>0);if(a.has(v)&&a.get(v)!==b)return false;a.set(v,b)}
    }
    let need=ex.filter(i=>!(mask>>i&1));
    function rec(k,p){branchTests++;if(k===need.length)return true;let i=need[k];for(let l of simp[i].free){let v=Math.abs(l),x=+(l<0);if(p.has(v)&&p.get(v)!==x)continue;let b=new Map(p);b.set(v,x);if(rec(k+1,b))return true}return false}
    return rec(0,a);
   }
   let predicted=0,sat=0;
   for(let mask=0;mask<2**m;mask++){let ok=admit(mask);if(ok!==exact.has(mask))throw Error("support mismatch");supportChecks++;if(ok){predicted++;if(E.every(([i,j])=>((mask>>i)&1)!==((mask>>j)&1)))sat++}}
   let gid=g.length?"GUARD-v1:sha256:"+sha(enc(["PNP-GUARD-v1",t.instance_id,"CNF-VAR-PINS-v1",sha(enc(g))])):"EMPTY";
   caseRows.push({guard:g,guard_id:gid,exceptions:ex,branchUpper:upper,predictedSupport:predicted,phaseModels:sat});
  }
  out.push({instance:t.instance,instance_id:t.instance_id,original_N_bits:t.N,guardCount:unique.length,supportChecks,branchTests,originalWordsScanned,maxExceptions,maxBranchUpper,caseRows});
 }
 return out;
}
if(typeof require!=="undefined"&&require.main===module){const fs=require("node:fs"),sha=s=>require("node:crypto").createHash("sha256").update(s,"utf8").digest("hex");console.log(JSON.stringify(run(JSON.parse(fs.readFileSync(process.argv[2],"utf8")),sha)));}
