#!/usr/bin/env node
// TMR-1/022, deterministic independent V8 implementation; Node.js compatible.
function audit(){
 const assert=(x,m)=>{if(!x)throw Error(m||"assertion failed")};
 const M={cases:0,c0_minimality_controls:0,c1_near_sat_controls:0,c1_record_critical_controls:0,r1_short_c1_witnesses:0,sensitive_disjoint_blocks:0,exhaustive_hamming_strings:0,independent_full_sat_checks:0,fastpath:0,fallback:0,matching_checks:0,failed:0};
 const samples=[];const kbits=(x,j)=>(x>>j)&1;
 const U=(k,r)=>Array.from({length:1<<k},(_,s)=>Array(r).fill(s)).flat();
 const unsat=(w,k)=>new Set(w).size===(1<<k);
 const V=(k,r,s,j)=>U(k,r).map(x=>x===s?x^(1<<j):x);
 const compatible=(sig,i,obs,k)=>{for(let j=0;j<k;j++){const key=i*k+j;if(obs.has(key)&&kbits(sig,j)!==obs.get(key))return false}return true};
 const canCover=(k,m,obs)=>{
  const match=new Array(m).fill(-1);
  const dfs=(s,seen)=>{
   for(let i=0;i<m;i++){if(seen[i]||!compatible(s,i,obs,k))continue;seen[i]=true;
    if(match[i]<0||dfs(match[i],seen)){match[i]=s;return true}
   }return false
  };
  for(let s=0;s<(1<<k);s++)if(!dfs(s,new Array(m).fill(false)))return false;
  return true;
 };
 for(let k=2;k<=4;k++)for(let r=1;r<=4;r++){
  const u=U(k,r),m=u.length,ell=k*m;assert(unsat(u,k));M.cases++;
  const c0=new Map();for(let s=0;s<(1<<k);s++)for(let j=0;j<k;j++)c0.set((s*r)*k+j,kbits(s,j));
  assert(canCover(k,m,c0));assert(c0.size===k*(1<<k));
  for(let [key] of c0){let part=new Map(c0);part.delete(key);let s=Math.floor(key/(r*k));
   // No clause is now forced to have signature s. All can avoid s.
   for(let i=0;i<m;i++)assert(Array.from({length:1<<k},(_,a)=>a).some(a=>a!==s&&compatible(a,i,part,k)));
   M.c0_minimality_controls++;
  }
  let blocks=[];for(let s=0;s<(1<<k);s++)for(let j=0;j<k;j++){
   let B=new Set();let mut=u.slice();for(let a=0;a<r;a++){B.add((s*r+a)*k+j);mut[s*r+a]^=1<<j}
   for(let prev of blocks)for(let p of B)assert(!prev.has(p));
   blocks.push(B);assert(!unsat(mut,k));M.sensitive_disjoint_blocks++;
   const v=V(k,r,s,j);
   assert(!unsat(v,k));assert(!new Set(v).has(s));assert(new Set(v).size===(1<<k)-1);
   let c1=new Map();
   for(let i=0;i<m;i++){let l=Array.from({length:k},(_,j)=>j).find(j=>kbits(v[i],j)!==kbits(s,j));assert(l!==undefined);c1.set(i*k+l,kbits(v[i],l))}
   assert(!canCover(k,m,c1));M.c1_near_sat_controls++;M.matching_checks++;
   if(r>=2){
    for(let [key] of c1){let i=Math.floor(key/k),z=v.slice();z[i]=s;assert(unsat(z,k));let partial=new Map(c1);partial.delete(key);
     for(let [key2,b]of partial)assert(kbits(z[Math.floor(key2/k)],key2%k)===b);
     if(r===2&&s===0&&j===0)assert(canCover(k,m,partial)),M.matching_checks++;
     M.c1_record_critical_controls++;
    }
   }else{
    const dup=s^(1<<j),hits=v.map((a,i)=>a===dup?i:-1).filter(i=>i>=0);
    assert(hits.length===2);
    const short=new Map();for(let i of hits)for(let l=0;l<k;l++)short.set(i*k+l,kbits(dup,l));
    assert(!canCover(k,m,short));assert(short.size===2*k);M.r1_short_c1_witnesses++;M.matching_checks++;
   }
  }
  assert(blocks.length===k*(1<<k));
  if(k===3)samples.push({k,r,sign_bits:ell,clauses:m,c0:k*(1<<k),c1_nearest_sat:r>=2?m:"at most 6",distance:r,bs:k*(1<<k),nearest_sat:(1<<k)*Math.pow(k,r)});
 }
 const layers=[[2,1],[2,2],[2,3],[3,1],[3,2],[3,3]];
 for(let [k,r]of layers){
  const u=U(k,r),ell=k*u.length,expected=(1<<k)*Math.pow(k,r);
  for(let d=0;d<=r;d++){
   let satcount=0;
   const rec=(start,used,arr)=>{
    if(used===d){let w=u.slice();for(let p of arr)w[Math.floor(p/k)]^=1<<(p%k);if(!unsat(w,k))satcount++;M.exhaustive_hamming_strings++;return}
    for(let p=start;p<=ell-(d-used);p++){arr.push(p);rec(p+1,used+1,arr);arr.pop()}
   };rec(0,0,[]);
   assert(satcount===(d===r?expected:0),`Hamming ${k},${r},${d}: ${satcount}`);
  }
  samples.push({exhaustive_k:k,exhaustive_r:r,count:expected});
 }
 // Independent clause truth-table checking with deterministic pseudo-random controls
 let seed=221114|0;
 const rnd=()=>{seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return(seed>>>0)};
 const truesat=(n,clauses)=>{for(let x=0;x<(1<<n);x++)if(clauses.every(c=>c.v.some((v,j)=>((x>>v)&1)!==c.s[j])))return true;return false};
 const solver=(n,clauses)=>{if(n===3&&clauses.every(c=>c.v.length===3&&c.v.slice().sort((a,b)=>a-b).join(",")==="0,1,2")){
  let mask=0;for(let c of clauses){let sig=0;for(let j=0;j<3;j++)sig|=c.s[j]<<c.v[j];mask|=1<<sig}
  M.fastpath++;return mask!==255;
 }M.fallback++;return truesat(n,clauses)};
 for(let q=0;q<1100;q++){
  let n=3+rnd()%4,m=rnd()%20,clauses=[];
  for(let i=0;i<m;i++){
    let all=Array.from({length:n},(_,j)=>j);
    for(let h=n-1;h>0;h--){let j=rnd()%(h+1);[all[h],all[j]]=[all[j],all[h]]}
    clauses.push({v:all.slice(0,3),s:[rnd()%2,rnd()%2,rnd()%2]});
  }
  assert(solver(n,clauses)===truesat(n,clauses));M.independent_full_sat_checks++;
 }
 for(let r=1;r<=5;r++)for(let sat=0;sat<=1;sat++){
  let w=sat?V(3,r,0,0):U(3,r);
  let clauses=w.map(s=>({v:[0,1,2],s:[kbits(s,0),kbits(s,1),kbits(s,2)]}));
  assert(solver(3,clauses)===!!sat);assert(truesat(3,clauses)===!!sat);M.independent_full_sat_checks++;
 }
 return {claim:"TMR1/022 fixed-k full-signature CNF cube exact certificate and safe-dispatch barrier",
 model:"k sign bits per ordered clause over fixed k variables, k=2,3,4 tests; no unrestricted TM cost inference",
 status:"COMPUTATIONAL, symbolic proof in role report",counts:M,samples,success:true};
}
console.log(JSON.stringify(audit(),null,2));
