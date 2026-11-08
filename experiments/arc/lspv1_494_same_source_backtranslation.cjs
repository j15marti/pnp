// LSPV-1/494. Independent strict-3CNF source controls; NOT historical native R_mix341 checker.
function run494(){
const ck=(v,msg)=>{if(!v)throw Error(msg||"invariant")};
const families={
K4:[4,Array.from({length:4},(_,a)=>Array.from({length:3-a},(_,k)=>[a,a+k+1])).flat()],
K33:[6,Array.from({length:3},(_,a)=>Array.from({length:3},(_,b)=>[a,b+3])).flat()],
cube:[8,Array.from({length:8},(_,a)=>[0,1,2].filter(k=>a<(a^(1<<k))).map(k=>[a,a^(1<<k)])).flat()],
Petersen:[10,[...Array.from({length:5},(_,i)=>[i,(i+1)%5]),...Array.from({length:5},(_,i)=>[i,i+5]),...Array.from({length:5},(_,i)=>[i+5,5+(i+2)%5])]]
};
const build=(h,edges,odd)=>{
  let inc=Array.from({length:h},()=>[]);
  for(let k=0;k<edges.length;k++)for(let v of edges[k])inc[v].push(k);
  ck(inc.every(row=>row.length===3));
  let clauses=[];
  for(let v=0;v<h;v++)for(let t=0;t<8;t++){
    let parity=((t&1)+((t>>1)&1)+((t>>2)&1))&1;
    if(parity===((odd&&v===0)?1:0))continue;
    clauses.push(inc[v].map((e,j)=>t&(1<<j)?-(e+1):e+1));
  }
  ck(clauses.length===4*h);
  return clauses;
};
const count=(cs,m)=>{let n=0;
  for(let a=0;a<(1<<m);a++)if(cs.every(c=>c.some(l=>(((a>>(Math.abs(l)-1))&1)===Number(l>0)))))n++;
  return n;
};
let results={},checks=0,negatives=0;
for(let [label,[h,edges]] of Object.entries(families)){
  let odd=build(h,edges,true),even=build(h,edges,false),m=edges.length;
  ck(count(odd,m)===0);checks++;
  ck(count(even,m)===(1<<(m-h+1)));checks++;
  for(let k=0;k<odd.length;k++){
    ck(count(odd.filter((_,j)=>j!==k),m)>0,"source deletion "+label+" "+k);checks++;
  }
  // Every local packet is exactly the four forbidden assignments of one parity equation.
  for(let v=0;v<h;v++){
    let p=odd.slice(4*v,4*v+4);
    ck(new Set(p.map(c=>c.join(","))).size===4);checks++;
    ck(p.every(c=>c.length===3 && new Set(c.map(l=>Math.abs(l))).size===3));checks++;
  }
  results[label]={h,edge_variables:m,strict3_clauses:4*h,odd_models:0,even_models:1<<(m-h+1),
    paid_semantic_nodes:4*h-1,unit_span:2+Math.ceil(Math.log2(h)),deletion_controls:4*h};
  if(count(odd.slice(1),m)===0)throw Error("hostile deletion unexpectedly UNSAT");
  negatives++;
}
return {scope:"finite strict-3CNF and declared-semantic arithmetic only",results,checks,hostile_controls:negatives,
caveat:"No historical R_mix341 accepted-byte replay; no Pang asymptotic lower-bound reproduction"};
}
if(typeof require!=="undefined"&&require.main===module)console.log(JSON.stringify(run494(),null,2));
