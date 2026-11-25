const fs=require('fs');
const specs=[["85e959ac861572a2411b9858da0d58d7c72ac780","research/hcl201/red-team/2026-11-25_0240_RT26_results.json"],["6d9917749c8438435d889b31e5c81ed0fc410e9a","research/hcl208/algebra/2026-11-25_0305_DA21_closure_results.json"],["0e9605a8932c8e1b960bdc13d2d622e9e52d8a7b","research/hcl201/synthesis/2026-11-25_0349_S27_results.json"]];
function run(rt,da,s27){
 let seed=20261125,checks=0;const rng=k=>{seed=(Math.imul(seed,1664525)+1013904223)>>>0;return Math.floor(seed/4294967296*k)},ck=(v,msg)=>{if(!v)throw Error(msg);checks++};
 function val(reg,x){let c=0;for(const {t,bad} of reg){let w=t.reduce((a,i,j)=>a+(x[i]<<j),0);if(bad.includes(w))c+=4}return c}
 function solve(n,reg,cuts=[]){
  let p=Array.from({length:n},(_,i)=>i), b=Array(n).fill(0),scans=0,joins=0,tests=0,ops=0;
  const out=(status,method,extra={})=>({status,method,scans,joins,tests,ops,...extra});
  function join(i,j,v){let a=p[i],d=p[j],q=b[i]^b[j]^v;if(a===d)return q?-1:0;for(let k=0;k<n;k++)if(p[k]===d){p[k]=a;b[k]^=q}joins++;return 1}
  function close(){outer:while(true){for(const {t,bad} of reg){scans++;let good=[];for(let w=0;w<8;w++){if(bad.includes(w))continue;let ok=true;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++)if(p[t[i]]===p[t[j]]&&((w>>i^w>>j)&1)!==(b[t[i]]^b[t[j]]))ok=false;if(ok)good.push(w)}if(!good.length)return false;for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let v=(good[0]>>i^good[0]>>j)&1;if(good.every(w=>((w>>i^w>>j)&1)===v)){let z=join(t[i],t[j],v);if(z<0)return false;if(z>0)continue outer}}}return true}}
  if(!close())return out("UNSAT","closure");
  for(const [mask,v] of cuts){let a=[];for(let i=0;i<n;i++)if(parseInt(mask,16)>>i&1)a.push(i);ck(a.length===2,"pair cut");if(join(...a,v)<0||!close())return out("UNSAT","imported-cut closure")}
  let ids=[...new Set(p)],d=ids.length,idx=p.map(x=>ids.indexOf(x)),J=Array.from({length:d},()=>Array(d).fill(0)),C=reg.length;
  for(const {t,bad} of reg)for(let i=0;i<3;i++)for(let j=i+1;j<3;j++){let a=t[i],z=t[j],u=idx[a],v=idx[z],s=((bad[0]>>i^bad[0]>>j^b[a]^b[z])&1)?-1:1;if(u===v)C+=s;else{J[u][v]+=s;J[v][u]+=s}}
  function witness(s){tests++;let x=idx.map((j,i)=>(s[j]<0?1:0)^b[i]);return val(reg,x)===0?x.join(""):null}
  let w=witness(Array(d).fill(1));if(w!==null)return out("SAT","constant witness",{d,C,w});
  if(C<0)throw Error("nonnegative energy constant");
  let A=Array.from({length:d},()=>Array(d).fill(0));for(let i=0;i<d;i++)for(let j=i;j<d;j++){let s=0;for(let k=0;k<d;k++){s+=J[i][k]*J[k][j];ops++}A[i][j]=A[j][i]=s}
  const R=Math.max(...A.map(row=>row.reduce((s,x)=>s+Math.abs(x),0)));
  if(4n*BigInt(C)**2n>BigInt(d)**2n*BigInt(R))return out("UNSAT","square row bound",{d,C,R});
  // Exact positive definiteness via leading principal minors, Bareiss.
  if(d<=127){let M=J.map((row,i)=>row.map((x,j)=>BigInt(d*x+(i===j?2*C:0)))),prev=1n,pd=true;
   for(let k=0;k<d;k++){let v=M[k][k];if(v<=0n){pd=false;break}for(let i=k+1;i<d;i++)for(let j=k+1;j<d;j++){let u=v*M[i][j]-M[i][k]*M[k][j];ck(u%prev===0n,"Bareiss division");M[i][j]=u/prev;ops++}prev=v}
   if(pd)return out("UNSAT","exact positive definite",{d,C,R})}
  for(let i=0;i<d;i++){w=witness(A[i].map(x=>x<0?-1:1));if(w!==null)return out("SAT","square row witness",{d,C,R,w})}
  return out("OPEN","decline",{d,C,R})
 }
 function ref(n,reg,cuts=[]){let count=0,visits=0;for(let w=0;w<2**n;w++){let x=Array.from({length:n},(_,i)=>w>>i&1);visits++;if(!val(reg,x)){count++;for(let [m,b] of cuts){let z=0;for(let i=0;i<n;i++)if(parseInt(m,16)>>i&1)z^=x[i];ck(z===b,"imported necessary cut on model")}}}return {count,visits}}
 let peers=[];for(let c of rt.controls){let d=da.rt.find(x=>x.n===c.n);for(let neighbor of [false,true]){let reg=JSON.parse(JSON.stringify(c.registry));if(neighbor)reg[0].bad=reg[0].bad.map(x=>x^1);let cuts=(neighbor?d.neighborAlternating:d.alternating).accepted,reference=ref(c.n,reg,cuts),raw=solve(c.n,reg),combined=solve(c.n,reg,cuts);for(let a of [raw,combined])ck(a.status==="OPEN"||(a.status==="SAT")===(reference.count>0),"peer decision");peers.push({n:c.n,neighbor,reference,raw,combined})}}
 let adjacent=[];for(let c of s27.controls){if(!c.neighbor)continue;for(let [label,reg] of [["UNSAT",c.neighbor.root],["SAT",c.neighbor.satRegistry]]){let reference=ref(c.n,reg),a=solve(c.n,reg);ck((reference.count>0)===(label==="SAT"),"adjacent source");ck(a.status==="OPEN"||a.status===label,"adjacent decision");adjacent.push({n:c.n,label,reference,a})}}
 let random=[];for(let n of [7,15,31,63,127,255]){let T=[];for(let a=1;a<=n;a++)for(let b=a+1;b<=n;b++)if((a^b)>b)T.push([a-1,b-1,(a^b)-1]);for(let trial=0;trial<4;trial++){let hidden=Array.from({length:n},()=>rng(2));for(let planted of [false,true]){let reg=T.map(t=>{let v=planted?1+rng(3):rng(4);if(planted)v^=t.reduce((s,i,j)=>s+(hidden[i]<<j),0);return {t,bad:[v,v^7]}});if(planted)ck(val(reg,hidden)===0,"plant");let a=solve(n,reg);if(planted)ck(a.status!=="UNSAT","plant decision");let reference=n<=15?ref(n,reg):null;if(reference)ck(a.status==="OPEN"||(a.status==="SAT")===(reference.count>0),"random small decision");random.push({n,trial,planted,a,reference})}}}
 return {checks,peers,adjacent,random};
}
console.log(JSON.stringify(run(...specs.map(([,p])=>JSON.parse(fs.readFileSync(p,'utf8')))),null,2));
