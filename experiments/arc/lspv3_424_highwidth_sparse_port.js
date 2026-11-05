#!/usr/bin/env node
'use strict';
// LSPV-3/424 self-contained original-source and high-width GF(2) port producer/checker.
// This implements the already fixed R_mix341 AND3/GF2 rules and a typed root view.
// Proposed CANON2R syntax is not the unique historical native grammar.
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const hash = x => crypto.createHash('sha256').update(x).digest('hex');
const canon = x => Array.isArray(x) ? '['+x.map(canon).join(',')+']' :
  x && typeof x==='object' ? '{'+Object.keys(x).sort().map(k=>JSON.stringify(k)+':'+canon(x[k])).join(',')+'}' :
  JSON.stringify(x);
let checks=0, badReject=0;
function eq(a,b,msg){assert.deepStrictEqual(a,b,msg);checks++}
function src(n){
  const clauses=[];for(let i=1;i<=n;i++)clauses.push([i],[i]);
  clauses.push([-1],[-1]);
  const raw=Buffer.from('p cnf '+n+' '+clauses.length+'\n'+clauses.map(c=>c[0]+' 0\n').join(''));
  return {raw,clauses};
}
function build(n){
  const {raw,clauses}=src(n);
  const nodes=[];
  function add(rule,more){let id=nodes.length;nodes.push({id,rule,...more});return {node:id,view:'affine'}}
  const arr=[];
  for(let i=1;i<=n;i++)arr.push(add('AND3',{left:{src:2*(i-1),view:'clause'},right:{src:2*(i-1)+1,view:'clause'},factor:{support:[i],truth:[0,1]},affine:{mask:[i],rhs:1}}));
  const neg=add('AND3',{left:{src:2*n,view:'clause'},right:{src:2*n+1,view:'clause'},factor:{support:[1],truth:[1,0]},affine:{mask:[1],rhs:0}});
  const xor=(a,b,mask,rhs)=>add('GF2',{left:a,right:b,affine:{mask,rhs}});
  let shared=arr[1];
  for(let i=3;i<=n;i++)shared=xor(shared,arr[i-1],Array.from({length:i-1},(_,j)=>j+2),(i-1)%2);
  const m=Array.from({length:n},(_,i)=>i+1);
  const positive=xor(shared,arr[0],m,n%2);
  const negative=xor(shared,neg,m,(n-1)%2);
  const final=xor(positive,negative,[],1);
  const source={nvars:n,clauses};
  const proof={format:'Rmix341-CANON2',source,source_sha256:hash(canon(source)),nodes,final};
  return {raw,certificate:{format:'Rmix341-CANON2R',source_raw_b64:raw.toString('base64'),source_raw_sha256:hash(raw),proof}};
}
function check(raw,w){
  eq(w.source_raw_b64,raw.toString('base64'),'exact original bytes');
  eq(w.source_raw_sha256,hash(raw),'raw SHA');
  const p=w.proof,n=p.source.nvars;
  eq(p.source_sha256,hash(canon(p.source)),'parsed source SHA');
  const views=new Map();
  for(let i=0;i<p.source.clauses.length;i++)views.set('s'+i,{kind:'clause',lits:p.source.clauses[i]});
  const ref=(r,k)=>{
    if('src' in r){eq(r.view,'clause','source type');return views.get('s'+r.src)}
    if(!(r.node>=0&&r.node<k))throw Error('bad index');
    return views.get('n'+r.node+':'+r.view);
  };
  const clause=(lits,e)=>+(lits.some(l=>e[Math.abs(l)]===+(l>0)));
  for(let i=0;i<p.nodes.length;i++){
    const r=p.nodes[i];eq(r.id,i,'node ordering');
    let a=ref(r.left,i),b=ref(r.right,i);if(!a||!b)throw Error('unauthenticated parent');
    if(r.rule==='AND3'){
      eq(a.kind,'clause','AND3 type');eq(b.kind,'clause','AND3 type');
      const s=[...new Set([...a.lits,...b.lits].map(Math.abs))].sort((x,y)=>x-y);
      if(s.length>3||s.some(x=>x>n))throw Error('AND3 support');
      eq(r.factor.support,s,'support');eq(r.factor.truth.length,2**s.length,'table length');
      for(let k=0;k<2**s.length;k++){
        const env=Object.fromEntries(s.map((v,j)=>[v,(k>>j)&1]));
        const want=clause(a.lits,env)&clause(b.lits,env);
        eq(r.factor.truth[k],want,'factor truth');
        eq(+(r.affine.mask.reduce((sum,v)=>sum^env[v],0)===r.affine.rhs),want,'annotation truth');
      }
      views.set('n'+i+':affine',{kind:'affine',row:r.affine});
    } else if(r.rule==='GF2'){
      eq(a.kind,'affine','GF2 type');eq(b.kind,'affine','GF2 type');
      const parity=new Map();
      for(const v of [...a.row.mask,...b.row.mask])parity.set(v,(parity.get(v)||0)^1);
      const m=[...parity].filter(x=>x[1]).map(x=>x[0]).sort((x,y)=>x-y);
      eq(r.affine,{mask:m,rhs:a.row.rhs^b.row.rhs},'authentic GF2');
      views.set('n'+i+':affine',{kind:'affine',row:r.affine});
    }else throw Error('not native AND3 or GF2');
  }
  eq(ref(p.final,p.nodes.length).row,{mask:[],rhs:1},'false terminal');
  eq(p.nodes.length,2*n+2,'paid node count');
  return {n,raw_source_bytes:raw.length,paid_nodes:p.nodes.length,wrapped_proof_bytes:Buffer.byteLength(canon(w)),dense_truth_bits:(1n<<BigInt(n)).toString()};
}
const summary=[];
for(const n of [2,3,4,5,8,12,16,32,64]){
  const {raw,certificate}=build(n);
  summary.push(check(raw,certificate));
  if(n===8){
    let w=structuredClone(certificate);w.proof.nodes.at(-1).affine.rhs^=1;
    try{check(raw,w);throw Error('forgery accepted')}catch(e){if(e.message==='forgery accepted')throw e;badReject++}
    w=structuredClone(certificate);w.source_raw_sha256='0'.repeat(64);
    try{check(raw,w);throw Error('wrong source accepted')}catch(e){if(e.message==='wrong source accepted')throw e;badReject++}
  }
}
for(const n of [4,5,8]){
  const target=n%2;
  for(let i=0;i<n;i++)for(let j=i+1;j<n;j++)for(let k=j+1;k<n;k++){
    let projection=new Set();
    for(let assignment=0;assignment<2**n;assignment++){
      let par=0;for(let v=0;v<n;v++)par^=(assignment>>v)&1;
      if(par===target)projection.add([i,j,k].map(v=>(assignment>>v)&1).join(''));
    }
    eq(projection.size,8,'every 3-projection is full');
  }
}
console.log(JSON.stringify({run:'LSPV3-424-GITHUB-COMPACT',checks,forged_rejections:badReject,summary,B3:'OPEN'},null,2));
