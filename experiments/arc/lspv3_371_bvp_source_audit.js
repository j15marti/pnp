'use strict';
// LSPV-3 371: independent source/proof controls for established carry BVP.
const assert=require('node:assert/strict');
const fs=require('node:fs');
function canonical(a){let t=[...new Set(a)];t.sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);return t;}
function eq(a,b){return JSON.stringify(canonical(a))===JSON.stringify(canonical(b));}
function evalClause(c,bits){return c.some(l=>!!bits[Math.abs(l)]===(l>0));}
function build(n){
  const c=i=>n+i,x=i=>i,clauses=[[c(1)],[-c(n+1)]];
  for(let i=1;i<=n;i++)clauses.push([x(i),-c(i)],[-x(i),c(i)],[-c(i+1),x(i)],[-c(i+1),c(i)],[-x(i),-c(i),c(i+1)]);
  return clauses;
}
function resolve(a,b,p){
  if(a.includes(p)&&b.includes(-p))return canonical([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)]);
  if(a.includes(-p)&&b.includes(p))return canonical([...a.filter(x=>x!==-p),...b.filter(x=>x!==p)]);
  throw Error('invalid signed pivot');
}
function derive(n,clauses){
  let nodes=clauses.map((cl,i)=>({rule:'SOURCE',cl:canonical(cl),index:i})),unit=0;
  for(let i=1;i<=n;i++){
    const a=2+5*(i-1), k=a+4;
    let v=canonical([-(n+i),n+i+1]);
    assert(eq(v,resolve(nodes[a].cl,nodes[k].cl,i)));
    const first=nodes.length;nodes.push({rule:'RES',parents:[a,k],pivot:i,cl:v});
    const second=nodes.length;nodes.push({rule:'RES',parents:[unit,first],pivot:n+i,cl:[n+i+1]});
    unit=second;
  }
  nodes.push({rule:'RES',parents:[unit,1],pivot:2*n+1,cl:[]});
  return nodes;
}
function verifyProof(cs,nodes){
  for(let j=0;j<nodes.length;j++){
    const z=nodes[j];
    if(z.rule==='SOURCE'){if(z.index!==j||!eq(z.cl,cs[j]))throw Error('bad source');}
    else if(z.rule==='RES'){
      const [a,b]=z.parents;
      if(!Number.isInteger(a)||!Number.isInteger(b)||a>=j||b>=j||a<0||b<0||!eq(z.cl,resolve(nodes[a].cl,nodes[b].cl,z.pivot)))throw Error('bad inference');
    }else throw Error('unknown rule');
  }
  if(nodes.at(-1).cl.length!==0)throw Error('missing contradiction');
  return nodes.filter(z=>z.rule==='RES').length;
}
function assignment(n,index){let arr=[false];for(let i=1;i<=2*n+1;i++)arr[i]=!!(index&(1<<(i-1)));return arr;}
function modelCount(cs,n){let ans=0;for(let a=0;a<2**(2*n+1);a++)if(cs.every(c=>evalClause(c,assignment(n,a))))ans++;return ans;}
function deletionWitness(n,idx){
  const bits=Array(2*n+2).fill(false),c=i=>n+i;
  if(idx===0)return bits;
  if(idx===1){for(let i=1;i<=2*n+1;i++)bits[i]=true;return bits;}
  const stage=Math.floor((idx-2)/5)+1,kind=(idx-2)%5;
  if(kind!==0&&kind!==4)return null;
  for(let j=1;j<=n+1;j++)bits[c(j)]=j<=stage;
  for(let j=1;j<=n;j++)bits[j]=j<stage||(j===stage&&kind===4);
  return bits;
}
let assertions=0;
const results=[];
for(const n of [1,2,3,4,5,6,8,12,16,32,64]){
  const clauses=build(n),nodes=derive(n,clauses),q=verifyProof(clauses,nodes);
  assert(clauses.every(cl=>cl.filter(x=>x>0).length<=1));assertions++;
  assert(q===2*n+1);assert(clauses.length===5*n+2);assertions+=3;
  const dimacs='p cnf '+(2*n+1)+' '+clauses.length+'\n'+clauses.map(c=>c.join(' ')+' 0\n').join('');
  const input_bits=8*Buffer.byteLength(dimacs,'utf8'),proof_bits=8*Buffer.byteLength(JSON.stringify(nodes),'utf8');
  const essential=[0,1,...Array.from({length:n},(_,j)=>2+5*j),...Array.from({length:n},(_,j)=>6+5*j)];
  for(const idx of essential){const w=deletionWitness(n,idx);assert(!evalClause(clauses[idx],w));assert(clauses.every((cl,i)=>i===idx||evalClause(cl,w)));assertions+=2;}
  const invalid=structuredClone(nodes);invalid.at(-1).pivot=-1;assert.throws(()=>verifyProof(clauses,invalid));assertions++;
  const boundaryZero=clauses.map(x=>[...x]);boundaryZero[0]=[-(n+1)];
  const boundaryOne=clauses.map(x=>[...x]);boundaryOne[1]=[2*n+1];
  const zero=Array(2*n+2).fill(false),one=Array(2*n+2).fill(true);
  assert(boundaryZero.every(c=>evalClause(c,zero)));assert(boundaryOne.every(c=>evalClause(c,one)));assertions+=2;
  let truth=null;
  if(n<=6){truth={unsat_models:modelCount(clauses,n),zero_boundary_models:modelCount(boundaryZero,n),one_boundary_models:modelCount(boundaryOne,n)};
    assert.deepEqual(truth,{unsat_models:0,zero_boundary_models:1,one_boundary_models:1});assertions++;}
  results.push({n,variables:2*n+1,source_clauses:clauses.length,essential_sources:essential.length,charged_resolution_nodes:q,source_floor:essential.length-1,proof_nodes_with_sources:nodes.length,dimacs_input_bits:input_bits,json_proof_evidence_bits:proof_bits,verifier_node_visits:nodes.length,exhaustive_assignments_checked:n<=6?3*(2**(2*n+1)):0,truth});
}
const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
function paritySolutions(charge){let count=0;for(let mask=0;mask<(1<<edges.length);mask++){let ok=true;for(let v=0;v<4;v++){let bit=0;edges.forEach(([a,b],e)=>{if(a===v||b===v)bit^=(mask>>e)&1;});if(bit!==charge[v])ok=false;}if(ok)count++;}return count;}
const parity={even_k4_models:paritySolutions([0,0,0,0]),odd_k4_models:paritySolutions([1,0,0,0])};
assert.deepEqual(parity,{even_k4_models:8,odd_k4_models:0});assertions++;
const ledger={status:'COMPUTATIONAL; all-size source floor from prior BVP354',source:'LSPV3 BVP-BITBLAST-COLLAPSE354, blob aa462fbe0350d1b21be2942a2be243a620909b73',published_lower_bound:'Alekseev Theory of Computing 22(4) (2026) Theorem 3.5: any Ext-PC-sqrt over Q refutation of algebraic BVP_n requires Omega(2^n) bits',checks:{assertions,negative_pivot_tests:results.length,models_exhausted_up_to_n:6,parity_k4:parity},cases:results,bridge:'Polynomial-output-bit backtranslation from this O(n)-node B_n Resolution proof into original algebraic BVP_n is impossible; this is not B3.'};
if(process.argv[2])fs.writeFileSync(process.argv[2],JSON.stringify(ledger,null,2)+'\n');
console.log(JSON.stringify({assertions,cases:results.length,last:results.at(-1),status:'PASS'}));
