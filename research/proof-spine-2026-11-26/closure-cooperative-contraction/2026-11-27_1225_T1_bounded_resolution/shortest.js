function shortest(base,width,cap){
 let D=[],active=[],index=new Map(),keys=new Map(),Q=Array.from({length:width+1},()=>[]),head=new Array(width+1).fill(0),pairs=0,subset=0,superchecks=0,retired=0,skipped=0,halt=false,stale=0,peak=0,live=0;
 const canon=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);
 function put(c,p){c=canon(c);if(c.length>width||c.some(l=>c.includes(-l)))return;let k=c.join(",");if(keys.has(k))return;
 for(let b=0;b<2**c.length-1;b++){subset++;if(keys.has(c.filter((_,j)=>b>>j&1).join(",")))return}
 if(c.length){let min=c.reduce((a,b)=>(index.get(a)?.size||0)<=(index.get(b)?.size||0)?a:b);for(let i of index.get(min)||[]){superchecks++;if(c.every(l=>D[i].c.includes(l))){active[i]=false;retired++;live--;for(let l of D[i].c)index.get(l).delete(i)}}}
 let i=D.length;D.push({c,p});active.push(true);keys.set(k,i);Q[c.length].push(i);live++;peak=Math.max(peak,live);for(let l of c){if(!index.has(l))index.set(l,new Set());index.get(l).add(i)}if(!c.length)halt=true;
 }
 for(let i=0;i<base.length&&!halt;i++)put(base[i].c,["base",i]);
 while(!halt&&pairs<cap){let i=-1;for(let w=0;w<=width&&i<0;w++)while(head[w]<Q[w].length){let z=Q[w][head[w]++];if(active[z]){i=z;break}stale++}if(i<0)break;
 for(let l of D[i].c){if(!active[i])break;let js=[...(index.get(-l)||[])];for(let j of js){if(!active[i]||halt||pairs>=cap)break;if(!active[j]){stale++;continue}pairs++;let r=canon([...D[i].c.filter(x=>x!==l),...D[j].c.filter(x=>x!==-l)]);if(r.length>width){skipped++;continue}put(r,["res",i,j,l])}if(halt||pairs>=cap)break}
 }
 return {status:halt?"UNSAT":pairs>=cap?"UNKNOWN_CAP":"UNKNOWN_EXHAUSTED",D,pairs,subset,superchecks,retired,stale,skipped,peak,live}
}
module.exports={shortest};
