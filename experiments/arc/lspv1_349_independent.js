'use strict';
// Independent enumerator, DAG pruning and model checks. No Python imports.
const fs=require('fs'); const raw=JSON.parse(fs.readFileSync(process.argv[2]||'source_excess_349.json'));
function parents(n){let all=[[]];for(let x=0;x<n;x++)all.push([x]);for(let x=0;x<n;x++)for(let y=x+1;y<n;y++)all.push([x,y]);return all}
function run(m,q){let total=0,freq=new Map(),sel=[];
 function recurse(i){if(i===q){
   let seen=new Set(),stack=[m+q-1];while(stack.length){let u=stack.pop();if(seen.has(u))continue;seen.add(u);if(u>=m)stack.push(...sel[u-m]);}
   if(seen.size!==m+q)return;total++;
   let E=sel.reduce((a,row)=>a+row.length,0),d=2*q-E,b=E-(m+q-1);
   if(d<0||b<0||d+b!==q-m+1)throw Error('Euler identity');
   let k=d+':'+b;freq.set(k,(freq.get(k)||0)+1);return;
 }
 for(let p of parents(m+i)){sel[i]=p;recurse(i+1)}
 }recurse(0);
 return {m,q,pruned_ancestry_dags:total,slack_classes:[...freq].map(([key,count])=>{let [delta,beta]=key.split(':').map(Number);return {delta,beta,count}}).sort((x,y)=>x.delta-y.delta||x.beta-y.beta)};
}
let assertions=0;
for(let x of raw.cases){let a=run(x.m,x.q);if(a.pruned_ancestry_dags!==x.pruned_ancestry_dags)throw Error('count mismatch '+x.m+','+x.q);assertions++;
 if(JSON.stringify(a.slack_classes.map(z=>[z.delta,z.beta,z.count]))!==JSON.stringify([...x.slack_classes].sort((y,z)=>y.delta-z.delta||y.beta-z.beta).map(z=>[z.delta,z.beta,z.count])))throw Error('class mismatch');assertions++;
}
function verifyWeighted(ex){let r=ex.source_ancestors,q=ex.parents.length,E=0,seen=new Set(),stack=[r+q-1];
 if(q!==ex.node_weights.length||r<ex.min_unsat_core_size)throw Error('bad dimensions');
 for(let i=0;i<q;i++){let a=ex.parents[i];if(new Set(a).size!==a.length)throw Error('duplicate dependency');
  for(let p of a){if(p<0||p>=r+i)throw Error('wrong parent');E++}}
 while(stack.length){let x=stack.pop();if(seen.has(x))continue;seen.add(x);if(x>=r)stack.push(...ex.parents[x-r])}
 if(seen.size!==r+q)throw Error('unpruned weighted DAG');
 let beta=E-(r+q-1),charged=ex.node_weights.reduce((a,b)=>a+b,0),surplus=ex.node_weights.reduce((a,w,i)=>a+w-ex.parents[i].length+1,0),
 mu=ex.min_unsat_core_size,excess=charged-(mu-1);
 if(beta<0||beta!==ex.cyclomatic_excess||surplus!==ex.rule_charge_surplus||excess!==ex.proof_excess||excess!==r-mu+beta+surplus)throw Error('weighted Euler identity');
 return true;
}
for(let ex of raw.weighted_examples){verifyWeighted(ex);assertions++}
let corrupt=[];
{let c=structuredClone(raw.weighted_examples[1]);c.parents[0]=[999];corrupt.push(c)}
{let c=structuredClone(raw.weighted_examples[2]);c.cyclomatic_excess+=1;corrupt.push(c)}
{let c=structuredClone(raw.weighted_examples[2]);c.node_weights[0]+=1;corrupt.push(c)}
{let c=structuredClone(raw.weighted_examples[1]);c.parents[1]=[0,1];corrupt.push(c)}
for(let c of corrupt){try{verifyWeighted(c);throw Error('corrupt admitted')}catch(e){if(e.message==='corrupt admitted')throw e;assertions++}}
function sat(cnf,n){let matches=[];for(let z=0;z<2**n;z++)if(cnf.every(C=>C.some(l=>Boolean((z>>(Math.abs(l)-1))&1)===(l>0))))matches.push(z);return matches}
let G=[[-3,1,4],[-1,2],[1,3],[-4,-3],[-2,-1,3],[-2,4]];
if(sat(G,4).length!==0)throw Error('G unsat');assertions++;
for(let i=0;i<6;i++){let old=G.filter((_,j)=>i!==j);if(sat(old,4).length===0)throw Error('deletion');assertions++;}
for(let i=0;i<6;i++)for(let j=0;j<G[i].length;j++){let F=G.map(x=>x.slice());F[i][j]*=-1;if(sat(F,4).length===0)throw Error('flip');assertions++;}
function valid(s){let rows=s.trim().split(/\n/),hdr=rows.shift()?.split(/\s+/);if(!hdr||hdr.length!==4||hdr[0]!=='p'||hdr[1]!=='cnf')return false;
let n=+hdr[2],m=+hdr[3];if(!Number.isInteger(n)||n<1||!Number.isInteger(m)||m<0||rows.length!==m)return false;
return rows.every(r=>{let parts=r.trim().split(/\s+/).map(Number);if(parts.at(-1)!==0||parts.some(x=>!Number.isInteger(x))||parts.slice(0,-1).some(x=>!x||Math.abs(x)>n))return false;let c=parts.slice(0,-1);return new Set(c).size===c.length&&!c.some(x=>c.includes(-x))&&!c.includes(0)});
}
if(!valid('p cnf 1 2\n1 0\n-1 0'))throw Error('valid input rejected');assertions++;
for(let x of ['p cnf 1 2\n1 0\n','p cnf 1 2\n1 0\n-2 0','p cnf 1 2\n1 0\n-1','p cnf 1 2\n1 0\n-1 0\nextra']){if(valid(x))throw Error('malformed accepted');assertions++}
if(sat([[1],[1]],1).length!==1)throw Error('SAT control');assertions++;
console.log(JSON.stringify({verified:true,assertions,dag_cases:raw.cases.length,model_deletion:6,model_signflips:14,malformed_rejections:4,corrupted_graph_rejections:corrupt.length},null,2));
