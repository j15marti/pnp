function extract(F,k){let clauses=[],checks=0,seen=new Set();for(let i=0;i<F.length;i++){let f=F[i];function walk(start,sel){if(sel.length){for(let b=0;b<2**sel.length;b++){let c=sel.map((j,t)=>((b>>t)&1)?-f.vs[j]:f.vs[j]);let hit=false;for(let w of f.ok){checks++;if(sel.every((j,t)=>((w>>j)&1)===((b>>t)&1))){hit=true;break}}if(!hit&&!seen.has(c.join(","))){seen.add(c.join(","));clauses.push({c,f:i})}}}else if(!f.ok.length)clauses.push({c:[],f:i});if(sel.length<k)for(let j=start;j<f.vs.length;j++)walk(j+1,[...sel,j])}walk(0,[])}return {clauses,checks}}

function resolution(base,width,cap){
 let D=[],index=new Map(),keys=new Map(),pairs=0,subchecks=0,skipped=0,halt=false;
 const canon=c=>[...new Set(c)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b), key=c=>c.join(",");
 function insert(c,p){c=canon(c);if(c.some(l=>c.includes(-l))||c.length>width)return;let k=key(c);if(keys.has(k))return;for(let b=0;b<2**c.length-1;b++){subchecks++;if(keys.has(key(c.filter((_,j)=>b>>j&1))))return}let i=D.length;D.push({c,p});keys.set(k,i);for(let l of c){if(!index.has(l))index.set(l,[]);index.get(l).push(i)}if(!c.length)halt=true}
 base.forEach((x,i)=>insert(x.c,["base",i]));
 for(let i=0;i<D.length&&!halt&&pairs<cap;i++){for(let l of D[i].c){for(let j of (index.get(-l)||[])){if(j>=i)break;if(++pairs>cap)break;let r=canon([...D[i].c.filter(x=>x!==l),...D[j].c.filter(x=>x!==-l)]);if(r.length>width){skipped++;continue}insert(r,["res",i,j,l]);if(halt)break}if(halt||pairs>=cap)break}}
 return {status:halt?"UNSAT":pairs>=cap?"UNKNOWN_CAP":"UNKNOWN_SATURATED",D,pairs,subchecks,skipped}
}

function check(F,base,D,imports){let rows=0,steps=0;for(let {c,f} of base){if(f===-1){if(!imports.some(z=>JSON.stringify(z)===JSON.stringify(c)))throw Error("bad import");continue}let t=F[f];if(!c.every(l=>t.vs.includes(Math.abs(l))))throw Error("scope");for(let w of t.ok){rows++;if(!c.some(l=>((w>>t.vs.indexOf(Math.abs(l)))&1)===+(l>0)))throw Error("bad local clause")}}for(let i=0;i<D.length;i++){let {c,p}=D[i],e;if(p[0]==="base")e=base[p[1]].c;else{let [,a,b,l]=p;if(a>=i||b>=i||!D[a].c.includes(l)||!D[b].c.includes(-l))throw Error("bad pivot");e=[...D[a].c.filter(x=>x!==l),...D[b].c.filter(x=>x!==-l)]}e=[...new Set(e)].sort((a,b)=>Math.abs(a)-Math.abs(b)||a-b);if(JSON.stringify(e)!==JSON.stringify(c))throw Error("bad resolvent");steps++}return {rows,steps,empty:D.some(x=>!x.c.length)}}
module.exports={extract,resolution,check};
