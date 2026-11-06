#!/usr/bin/env node
/* Independent verification of LSPV-4/437 finite Tseitin matching-split records.
   Reconstructs original signed 3-CNF and decides restricted parity by connected
   components, independently of producer's GF(2) elimination. Execute with
   node experiments/arc/lspv4_437_independent.mjs path/to/raw.json
   Full raw.json and Python producer are in the separately retained ZIP. */
import fs from 'node:fs';
import crypto from 'node:crypto';
const input=process.argv[2] || new URL('./raw.json',import.meta.url);
const raw=JSON.parse(fs.readFileSync(input,'utf8'));
let checks=0;
function ck(x,why){checks++;if(!x)throw Error(why);}
function source(h,edges,parity){
 const incidence=Array.from({length:h},()=>[]);
 edges.forEach(([u,v],i)=>{incidence[u].push(i+1);incidence[v].push(i+1)});
 const clauses=[],chi=Array(h).fill(0);chi[0]=parity;
 for(let v=0;v<h;v++){
  const [a,b,c]=[...incidence[v]].sort((x,y)=>x-y);
  for(let p=0;p<2;p++)for(let r=0;r<2;r++){
   const s=p^r^1^chi[v];clauses.push([p?-a:a,r?-b:b,s?-c:c]);
  }
 }
 const m=edges.length,w=Math.floor(Math.log2(m))+1;
 const bin=x=>x.toString(2).padStart(w,'0');
 const encoded='10100111'+'1'.repeat(h)+'0'+'1'.repeat(m)+'0'
  +chi.join('')+incidence.flatMap(x=>[...x].sort((a,b)=>a-b).map(bin)).join('')
  +clauses.flatMap(c=>c.map(x=>(x<0?'1':'0')+bin(Math.abs(x)))).join('');
 return {clauses,encoded};
}
function componentParitySAT(h,edges,parity,assigned){
 const nbr=Array.from({length:h},()=>[]),charges=Array(h).fill(0);
 charges[0]=parity;
 edges.forEach(([u,v],j)=>{
  if(assigned.has(j+1)){let x=Number(assigned.get(j+1));charges[u]^=x;charges[v]^=x;}
  else {nbr[u].push(v);nbr[v].push(u);}
 });
 const seen=new Set();
 for(let root=0;root<h;root++)if(!seen.has(root)){
  const stack=[root];seen.add(root);let bit=0;
  while(stack.length){let u=stack.pop();bit^=charges[u];
   for(let v of nbr[u])if(!seen.has(v)){seen.add(v);stack.push(v);}}
  if(bit)return false;
 }
 return true;
}
for(const rec of raw.results){
 const {h,edges,k,matching_edge_ids:ids,charge_parity:parity}=rec;
 const {clauses,encoded}=source(h,edges,parity);
 ck(encoded.length===rec.N,'length');
 ck(crypto.createHash('sha256').update(encoded).digest('hex')===rec.source_sha256,'source hash');
 ck(clauses.length===4*h,'original 3-CNF count');
 const endpoints=new Set(ids.flatMap(id=>edges[id-1]));
 ck(endpoints.size===2*k,'matching');
 ck(rec.branches.length===2**k,'all branches');
 for(const b of rec.branches){
  const a=new Map(ids.map((id,j)=>[id,b.bits[j]==='1']));
  const remain=[];
  for(const cl of clauses){
   if(cl.some(z=>a.has(Math.abs(z))&&a.get(Math.abs(z))===(z>0)))continue;
   remain.push(cl.filter(z=>!a.has(Math.abs(z))));
  }
  ck(remain.filter(z=>z.length===3).length===4*(h-2*k),'unaffected ternary clauses');
  ck(remain.filter(z=>z.length===2).length===4*k,'binary clauses');
  ck(remain.every(z=>z.length>=2),'no UP triggers');
  ck(componentParitySAT(h,edges,parity,a)===b.sat_GF2,'independent SAT labels');
 }
}
ck(raw.counts.branch_checks===raw.results.reduce((a,r)=>a+r.num_branches,0),'aggregate branches');
console.log(JSON.stringify({status:'PASS',checks,formulas:raw.results.length,branches:raw.counts.branch_checks,method:'component parity independent of Gaussian elimination'}));
