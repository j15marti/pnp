#!/usr/bin/env node
// LSPV-2/442: independent GF(2) and ORIGINAL signed-clause multiset verifier.
// Input: full raw442.json from the attached reproducibility archive.
// This host JS verifier is not a native FLMV or R_mix341 checker.
import fs from 'node:fs';
import crypto from 'node:crypto';
const dat=JSON.parse(fs.readFileSync(process.argv[2]||'./raw442.json','utf8'));
let assertions=0;
function assert(x,msg){assertions++;if(!x)throw Error('ASSERT '+msg)}
function parse(s){
 let lines=s.trim().split(/\r?\n/);let head=lines.shift().split(' ');
 if(head.length!==4||head[0]!=='p'||head[1]!=='cnf')return null;
 if(lines.length!==Number(head[3]))return null;
 const rows=[];
 for(let line of lines){let a=line.split(/\s+/);if(a.length!==4||a[3]!=='0')return null;rows.push(a.slice(0,3));}
 return rows;
}
function originalClauses(row){
 const {h,edges,charges,rename}=row;
 let adj=Array.from({length:h},()=>[]);
 for(let [a,b] of edges){adj[a].push(b);adj[b].push(a)}
 for(let x of adj)x.sort((a,b)=>a-b);
 let edgeId=(a,b)=>{const low=Math.min(a,b),high=Math.max(a,b);return 3*low+adj[low].indexOf(high)+1;};
 const ans=[];
 for(let v=0;v<h;v++){
   const vars=adj[v].map(u=>rename[String(edgeId(v,u))]);
   for(let mask=0;mask<8;mask++){
      const signs=[(mask>>2)&1,(mask>>1)&1,mask&1];
      if((signs[0]^signs[1]^signs[2])===charges[v])continue;
      ans.push(vars.map((x,j)=>(signs[j]?'-':'')+x));
   }
 }
 return ans;
}
function satGaussian(h,edges,chi){
 let basis=new Map();
 for(let v=0;v<h;v++){
  let lhs=0n,rhs=chi[v];
  edges.forEach(([a,b],j)=>{if(a===v||b===v)lhs|=1n<<BigInt(j)});
  while(lhs){const lead=lhs.toString(2).length-1;
    if(!basis.has(lead)){basis.set(lead,[lhs,rhs]);lhs=-1n;break}
    let [m,r]=basis.get(lead);lhs^=m;rhs^=r;
  }
  if(lhs===0n&&rhs)return false;
 }
 return true;
}
function key(cl){return cl.slice().sort((a,b)=>{
 const x=a.replace(/^-/,'');const y=b.replace(/^-/,'');
 if(x.length!==y.length)return x.length-y.length;
 return x.localeCompare(y);
 }).join(' ')}
for(let row of dat.cases){
 const hash=crypto.createHash('sha256').update(row.source).digest('hex');assert(hash===row.sha256,'hash');
 const got=parse(row.source);assert(got!==null,'parser');
 const expected=originalClauses({...row,h:row.charges.length});
 const a=got.map(key).sort(),b=expected.map(key).sort();assert(JSON.stringify(a)===JSON.stringify(b),'full signed clause multiset');
 const ans=satGaussian(row.charges.length,row.edges,row.charges);
 assert((row.expected==='SAT')===ans,'independent GF2 rank');
 assert(got.length===row.charges.length*4,'exact quartet count');
}
for(let bad of dat.mutations){
 const rows=parse(bad.source);
 if(bad.expected==='BAD_FORMAT')assert(rows===null,'bad header');
 else {
   assert(rows!==null,'well framed perturbation');
   let counts=new Map();for(let cl of rows)counts.set(key(cl),(counts.get(key(cl))||0)+1);
   assert([...counts.values()].some(n=>n>1),'duplicate introduced');
 }
}
const hostile=dat.cases.find(x=>x.graph==='two_K4'&&x.charge_case===2);
assert(!!hostile&&hostile.expected==='UNSAT','disconnected adversary');
assert(hostile.charges.reduce((a,b)=>a^b,0)===0,'global even but UNSAT');
console.log(JSON.stringify({cases:dat.cases.length,mutations:dat.mutations.length,assertions,global_even_disconnected_UNSAT:true}));
