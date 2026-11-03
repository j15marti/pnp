'use strict';
// Offline finite exhaustive shortest-Resolution-DAG enumerator. NOT a P-time SAT solver.
function canonical(c) {
  if (!Array.isArray(c)) throw Error('clause not array');
  if (c.some(v => !Number.isInteger(v) || v === 0 || Math.abs(v)>30)) throw Error('bad literal');
  const a=[...new Set(c)].sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y);
  if (a.some(x=>a.includes(-x))) throw Error('tautological clause in compact restricted grammar');
  return a;
}
function key(c) {return c.join(',');}
function source(F) {
  if (!Array.isArray(F)) throw Error('source not array');
  return [...new Map(F.map(x=>{const y=canonical(x);return [key(y),y];})).values()];
}
function resolve(a,b,p) {
  if (!a.includes(p)||!b.includes(-p)) return null;
  const u=[...new Set([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)])];
  if(u.some(x=>u.includes(-x))) return null;
  return canonical(u);
}
function check(F,proof) {
  const lines=source(F).map(x=>[...x]);
  if (!Array.isArray(proof)) return false;
  if(lines.some(c=>c.length===0)) return proof.length===0;
  for(const d of proof) {
    if(!d||!Number.isInteger(d.i)||!Number.isInteger(d.j)||!Number.isInteger(d.p)||d.i>=lines.length||d.j>=lines.length||d.i<0||d.j<0||d.i===d.j) return false;
    const r=resolve(lines[d.i],lines[d.j],d.p);
    if(!r||!Array.isArray(d.out)||key(r)!==key(d.out)) return false;
    lines.push(r);
  }
  return proof.length>0&&lines[lines.length-1].length===0;
}
function exact(F,max=7) {
  const orig=source(F);if(orig.some(c=>!c.length))return {minimum:0,proof:[],states:1};
  if(orig.length===0)return {minimum:null,proof:null,states:1};
  const seen=new Set(), queue=[{extra:[],proof:[]}];let at=0;
  const qkey=arr=>arr.map(key).sort().join(';');seen.add(qkey(orig));
  while(at<queue.length) {
    const st=queue[at++],clauses=[...orig,...st.extra];
    if(st.extra.length===max)continue;
    for(let i=0;i<clauses.length;i++)for(let j=0;j<clauses.length;j++)if(i!==j) {
      for(const p of clauses[i])if(p>0 && clauses[j].includes(-p)) {
        const r=resolve(clauses[i],clauses[j],p);if(r===null)continue;
        if(clauses.some(c=>key(c)===key(r)))continue;
        const next={extra:st.extra.concat([r]),proof:st.proof.concat([{i,j,p,out:r}])};
        if(r.length===0)return {minimum:next.proof.length,proof:next.proof,states:at};
        const sig=qkey([...orig,...next.extra]);if(!seen.has(sig)){seen.add(sig);queue.push(next);}
      }
    }
  }
  return {minimum:null,proof:null,states:at,cutoff:max};
}
function models(F) {let orig=source(F),n=Math.max(0,...orig.flat().map(x=>Math.abs(x))),count=0;
  if(n>12)throw Error('model cap');
  for(let m=0;m<2**n;m++)if(orig.every(c=>c.some(x=>x>0?Boolean(m&(1<<(x-1))):!Boolean(m&(1<<(-x-1))))))count++;
  return count;
}
function run() {
  const fixtures=[
    ['unit_unsat',[[1],[-1]],1],
    ['chain_unsat',[[1],[-1,2],[-2]],2],
    ['complete_block_2',[[1,2],[1,-2],[-1,2],[-1,-2]],3],
    ['source_empty',[[]],0],
    ['sat_pair',[[1,2],[-1,2]],null],
    ['sat_unit',[[1]],null],
    ['empty_formula',[],null]
  ];
  const cases=[];let assertions=0;
  for(const [name,F,expected] of fixtures){let m=models(F),e=exact(F,4);
    if((m===0)!==(expected!==null))throw Error('model classification');assertions++;
    if(e.minimum!==expected)throw Error('minimum mismatch '+name+': '+e.minimum);assertions++;
    if(expected!==null&&!check(F,e.proof))throw Error('proof failed '+name);assertions++;
    cases.push({name,source:F,models:m,minimum:e.minimum,proof:e.proof,states:e.states});
  }
  const odd=[0,1,1,1],even=[0,0,0,0];
  function k4(charges){let edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
    const out=[];for(let v=0;v<4;v++){let e=edges.map((q,i)=>q.includes(v)?i+1:null).filter(Boolean);
      for(let bits=0;bits<8;bits++){let p=((bits&1)>0)+((bits&2)>0)+((bits&4)>0);
        if(p%2!==charges[v])out.push(e.map((x,j)=>bits&(1<<j)?-x:x));}}
    return out;
  }
  const parity={odd_models:models(k4(odd)),even_models:models(k4(even))};if(parity.odd_models!==0||parity.even_models!==8)throw Error('parity');assertions+=2;
  let malformed=0, corrupt=0;
  for(const bad of [null,{},[[0]],[[1.5]],'x']){try{source(bad);}catch(e){malformed++;}}
  for(const badProof of [[{i:0,j:1,p:2,out:[]}],[{i:9,j:1,p:1,out:[]}],[{i:0,j:1,p:1,out:[1]}]]){if(!check([[1],[-1]],badProof))corrupt++;}
  if(malformed!==5||corrupt!==3)throw Error('hostile controls');assertions+=malformed+corrupt;
  return {id:'LSPV1_364_BUDGETED_PROOF_SEARCH',scope:'finite ordinary Resolution, general theorem conditional on SAT in P and canonical Rmix341 proof evidence',cases,parity,malformed_rejected:malformed,corrupt_rejected:corrupt,assertions};
}
if(require.main===module)console.log(JSON.stringify(run(),null,2));
module.exports={canonical,source,resolve,check,models,exact,run};
