"use strict";
function protectedCheck(){
 let seed=246813579;function rng(n){seed^=seed<<13;seed^=seed>>>17;seed^=seed<<5;return (seed>>>0)%n}
 const cols=[1,2,4,3,5,7],H=63,dir=cols.map((c,i)=>i<3?c:c<<3), xor=a=>a.reduce((x,y)=>x^y,0);
 const C={systems:0,keys:0,referenceTransitions:0,targets:0,sat:0,unsat:0,lifts:0,protectedPairChecks:0,closureChecks:0};
 function span(a){let S=new Set([0]);for(let v of a)for(let w of [...S])S.add(w^v);return S}
 if(span(dir).size!==64)throw Error("rank");
 for(let s=0;s<16;s++){
  const R=cols.map((c,i)=>Array.from({length:2},(_,k)=>{
   let vals=[0,c,c<<3,c^(c<<3)],miss=rng(4);let rows=vals.filter((_,j)=>j!==miss).map(v=>v^(rng(1)<<6)); // all private tags in H
   let pair=rows.flatMap(x=>rows.includes(x^dir[i])?[[x,x^dir[i]]]:[])[0];
   if(!pair||!rows.includes(pair[0])||!rows.includes(pair[1]))throw Error("pair");
   C.protectedPairChecks++;return {rows,pair,tag:rng(4),cost:[k,rng(3)]};
  }));
  const external=[{v:0,tag:0,cost:[0,1]},{v:rng(64),tag:1,cost:[1,0]},{v:rng(64),tag:3,cost:[0,2]}];
  let budget=[1+rng(6),2+rng(10)],ref=new Map(),projected=new Map();
  // Exact necessary local affordability closure, restarting after every deletion.
  let active=R.map(a=>[...a]);let changed=true;
  while(changed){changed=false;outer:for(let i=0;i<active.length;i++)for(let j=0;j<active[i].length;j++){C.closureChecks++;let row=active[i][j];if(row.cost.some((v,k)=>v+active.reduce((t,a,l)=>t+(l===i?0:Math.min(...a.map(b=>b.cost[k]))),0)+Math.min(...external.map(b=>b.cost[k]))>budget[k])){active[i].splice(j,1);changed=true;break outer}}if(active.some(a=>!a.length))break}
  // Every retained key has an authenticated pair. Compare projected vs full exact supports.
  for(let mask=0;mask<64;mask++){let keys=R.map((a,i)=>a[(mask>>i)&1]);C.keys++;
   let vals=new Set([0]);for(let a of keys){let next=new Set();for(let x of vals)for(let y of a.rows){C.referenceTransitions++;next.add(x^y)}vals=next}
   for(let e of external){let c=[0,1].map(k=>keys.reduce((a,b)=>a+b.cost[k],e.cost[k]));if(c.some((v,k)=>v>budget[k]))continue;
    let tag=xor(keys.map(a=>a.tag))^e.tag;
    for(let v of vals)ref.set((tag<<6)|(v^e.v),true);
    if(keys.every((a,i)=>active[i].includes(a))&&!projected.has(tag))projected.set(tag,{keys,e});
   }
  }
  let masks=new Map();for(let mask=0;mask<64;mask++)masks.set(xor(dir.filter((_,i)=>(mask>>i)&1)),mask);
  for(let t=0;t<256;t++){C.targets++;let w=projected.get(t>>6),sat=!!w;if(sat!==ref.has(t))throw Error("protected mismatch");C[sat?"sat":"unsat"]++;
   if(w){let {keys,e}=w,base=xor(keys.map(a=>a.pair[0]))^e.v,mask=masks.get((t&H)^base);
    let rows=keys.map((a,i)=>a.pair[(mask>>i)&1]);if(rows.some((v,i)=>!keys[i].rows.includes(v))||(xor(rows)^e.v)!==(t&H)||((xor(keys.map(a=>a.tag))^e.tag)!==(t>>6))||[0,1].some(k=>keys.reduce((a,b)=>a+b.cost[k],e.cost[k])>budget[k]))throw Error("lift");C.lifts++;
   }
  }
  C.systems++;
 }
 // Mask sensitivity: original A+B all four, pin A=0 removes target 3.
 let A=[0,1,2],B=[0,1,2],before=new Set(A.flatMap(a=>B.map(b=>a^b))),after=new Set(B);
 if(!before.has(3)||after.has(3))throw Error("pin control");
 return {seed:246813579,counters:C,pinControl:{target:3,beforeSAT:true,afterSAT:false},discrepancies:0}
}
console.log(JSON.stringify(protectedCheck(),null,2));
