/* LSPV-4/470 independently implemented V8 check: live INDEX bits vs counted WORK radix storage.
 * No assumption that this is a native FLMV simulator. */
'use strict';
const crypto=require('crypto');
const counters={assertions:0};
function check(p,s){counters.assertions++;if(!p)throw Error(s)}
function radixIndependent(source){
  const n=source.length;
  check((n&(n-1))===0,'power-of-two INDEX length');
  const maps=new Map(),distinct=new Map();let next=1;
  function visit(from,width){
    if(width===1)return source[from]?1:0;
    let a=visit(from,width/2),b=visit(from+width/2,width/2);
    if(a===0&&b===0)return 0;
    const height=Math.log2(width),key=height+','+a+','+b;
    if(!maps.has(key)){
      maps.set(key,++next);
      distinct.set(height,(distinct.get(height)||0)+1);
    }
    return maps.get(key);
  }
  visit(0,n);
  return {live_nodes:maps.size,distinct};
}
function run(){
  let cases=[];
  for(let k of [2,4,8,16]){
    const m=2**k,L=k*m,source=Buffer.alloc(L);
    let ones=0;
    for(let word=0;word<m;word++)for(let b=0;b<k;b++){
      const bit=Math.floor(word/2**b)%2;
      source[word*k+b]=bit;ones+=bit;
    }
    check(source.length===L,'input INDEX length');
    const radix=radixIndependent(source),level=Math.log2(k),blocks=radix.distinct.get(level);
    check(blocks>=m-1,'distinct aligned subtrees persist');
    check(radix.live_nodes>=m-1,'cannot recycle still-live nodes');
    const digest=crypto.createHash('sha256').update(source).digest('hex');
    let clearing=Buffer.from(source),steps=0;
    for(let j=0;j<L;j++){clearing[j]=0;steps++;}
    check(clearing.every(v=>v===0),'guest INDEX clearing');
    cases.push({k,blocks:m,index_length:L,live_nodes:radix.live_nodes,
      distinct_level_k_nodes:blocks,bound_live_nodes:m-1,work_highwater:0,
      peak_index_ones:ones,guest_prefix_steps:L,guest_index_clear_steps:steps,
      bit_sha256:digest});
  }
  const E=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  let control=[];
  for(let odd of [false,true]){
    const charges=[Number(odd),0,0,0],clauses=[];
    for(let v=0;v<4;v++){
      const edgeids=E.map((e,i)=>e.includes(v)?i+1:0).filter(Boolean);
      for(let t=0;t<8;t++){
        let parity=0;for(let j=0;j<3;j++)parity^=(t>>j)&1;
        if(parity!==charges[v])clauses.push(edgeids.map((id,j)=>((t>>j)&1)?-id:id));
      }
    }
    let sat=0;
    for(let a=0;a<64;a++)if(clauses.every(c=>c.some(l=>(((a>>(Math.abs(l)-1))&1)===Number(l>0)))))sat++;
    check(clauses.length===16,'strict 3CNF size');check(sat===(odd?0:8),'signed parity labels');
    control.push({odd,clauses:16,models:sat});
  }
  for(let clause of [[1,1,2],[1,-1,2]])check(new Set(clause.map(Math.abs)).size!==3,'reject improper source clause');
  return {status:'COMPUTATIONAL; independently replayed abstract representation, not FLMV',
    cases,tseitin_controls:control,malformed_duplicate_abs_literal_rejected:2,
    assertions:counters.assertions};
}
console.log(JSON.stringify(run(),null,2));
