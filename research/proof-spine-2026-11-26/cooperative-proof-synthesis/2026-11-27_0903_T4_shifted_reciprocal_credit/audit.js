const audit=function audit(){
 const pairs=[[15,32],[13,17],[14,36],[11,53],[10,39]];
 const swap=z=>((z&1)<<1)|(z>>1);
 const value=([u,v],z)=>((z&1)?u:0)^((z&2)?v:0);
 let actual=new Uint32Array(65536), predicted=new Uint32Array(65536), actualTrials=0;
 // Independent direct enumeration in original leaf coordinates; each group has two legal nonzero leaf choices.
 function direct(i,s,priv){
  if(i===5){actual[(priv<<6)|s]++;actualTrials++;return;}
  for(let x=1;x<4;x++)for(let y=1;y<4;y++){
    const a=(x&1)^(y>>1), b=(y&1)^(x>>1);
    const z=(x>>1)|((y>>1)<<1);
    direct(i+1,s^value(pairs[i],z),priv|((a|(b<<1))<<(2*i)));
  }
 }
 direct(0,0,0);
 let domainHistogram=[0,0,0,0,0], unsat=0, holeAtZero=0, target29Feasible=0, maxCount=0;
 for(let g=0;g<1024;g++){
  const dom=pairs.map((_,i)=>{const h=(g>>(2*i))&3;const d=[];for(let z=0;z<4;z++){if((swap(z)^(h&1))!==0 && (z^(h>>1))!==0)d.push(z)}return d});
  // right child coefficients (beta1+t_b,beta2), left (beta2+t_a,beta1).
  for(const d of dom)domainHistogram[d.length]++;
  let counts=new Uint32Array(64);counts[0]=1;
  for(let i=0;i<5;i++){let next=new Uint32Array(64);for(let s=0;s<64;s++)for(const z of dom[i])next[s^value(pairs[i],z)]+=counts[s];counts=next;}
  for(let s=0;s<64;s++){let k=(g<<6)|s;predicted[k]=counts[s];if(counts[s]!==actual[k])throw Error("mismatch "+k);if(!counts[s])unsat++;maxCount=Math.max(maxCount,counts[s]);}
  if(counts[29])target29Feasible++;
  if(g===0)holeAtZero=counts.reduce((a,b)=>a+!b,0);
 }
 // independently verify parent/child T2 collision claim
 let fiber=[];for(let x=0;x<1024;x++){let s=0,ok=true;for(let i=0;i<5;i++){let z=(x>>(2*i))&3;ok&&=z!==0;s^=value(pairs[i],z);}if(ok&&s===0)fiber.push(x);}
 let diffs=new Set();for(const x of fiber)for(const y of fiber)diffs.add(x^y);
 let kernel=[];for(let x=0;x<1024;x++){let s=0;for(let i=0;i<5;i++)s^=value(pairs[i],(x>>(2*i))&3);if(!s)kernel.push(x);}
 if(kernel.some(x=>!diffs.has(x))||kernel.length!==diffs.size)throw Error("T2 mismatch");
 // Forward recursion (affine map) vs independent bottom-up leaf-domain combination.
 let seed=20261127;function rand(){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed;}
 function tree(d){if(!d)return null;return {h:rand()>>>30,l:tree(d-1),r:tree(d-1)}}
 function forward(t,z){if(!t)return z!==0;return forward(t.l,swap(z)^(t.h&1))&&forward(t.r,z^(t.h>>1));}
 function bottom(t){if(!t)return [1,2,3];let out=new Set();for(let x of bottom(t.l))for(let y of bottom(t.r)){let h=((x&1)^(y>>1))|(((y&1)^(x>>1))<<1);if(h===t.h)out.add((x>>1)|((y>>1)<<1));}return [...out];}
 let treeChecks=0;for(let d=1;d<=7;d++)for(let j=0;j<100;j++){let t=tree(d);let b=bottom(t);for(let z=0;z<4;z++){if(forward(t,z)!==b.includes(z))throw Error("tree mismatch");treeChecks++;}}
 // Credit recurrence for worst-case full ternary branch; each node costs 4 finite track tickets.
 let bank=[];for(let k=0;k<=5;k++){let b=(3**(k+1)-1)/2;bank.push({k,nodes:b,tickets:4*b});if(k&&b!==1+3*bank[k-1].nodes)throw Error("credit");}
 return {actualTrials,comparisons:65536,unsat,domainHistogram,holeAtZero,target29Feasible,maxCount,fiber,differences:diffs.size,kernel:kernel.length,treeChecks,bank};
};
console.log(JSON.stringify(audit(),null,2));
