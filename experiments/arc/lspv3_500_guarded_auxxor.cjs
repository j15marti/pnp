'use strict';
/* LSPV-3/500 declared GF(2)-row macro into source-only Resolution.
 * Historical R_mix341 accepted-byte conversion remains OPEN.
 * Node: node lspv3_500_guarded_auxxor.js
 */
(function(root){
  const fail=s=>{throw Error(s)}, ok=(b,s)=>{if(!b)fail(s)};
  const S=[1,2,3], all=Array.from({length:8},(_,i)=>S.map((_,k)=>(i>>k)&1));
  const bit=(a,v)=>a[v-1], clause=(a,V)=>V.map(i=>bit(a,i)?-i:i);
  const key=c=>c.slice().sort((a,b)=>a-b).join(',');
  const eq=(a,b)=>JSON.stringify(a)===JSON.stringify(b);
  const sat=(c,a)=>c.some(i=>bit(a,Math.abs(i))===(i>0?1:0));
  const P=a=>((bit(a,1)&bit(a,2))^bit(a,3))===0;
  const Q=a=>(bit(a,2)^bit(a,3))===0;
  const C=a=>((bit(a,1)&bit(a,2))^bit(a,2))===0;
  function canonical(V,f){let m=new Map();for(const a of all)if(!f(a)){let c=clause(a,V);m.set(key(c),c)}return [...m.values()]}
  const p=canonical([1,2,3],P),q=canonical([2,3],Q),c=canonical([1,2],C);
  const original=[...p,...q,[-1],[2]];
  ok(p.length===4&&q.length===2&&eq(c,[[1,-2]]),'canonical clause counts');
  function dimacs(src){return 'p cnf 3 '+src.length+'\n'+src.map(c=>c.join(' ')+' 0').join('\n')+'\n'}
  function parse(s){
    ok(typeof s==='string','source text');let a=s.trim().split(/\s+/);
    ok(a[0]==='p'&&a[1]==='cnf'&&/^[0-9]+$/.test(a[2])&&/^[0-9]+$/.test(a[3]),'header');
    let n=Number(a[2]),m=Number(a[3]);ok(Number.isSafeInteger(n)&&Number.isSafeInteger(m)&&n===3,'bounds');
    let src=[],current=[];for(let t of a.slice(4)){
      ok(t==='0'||/^-?[1-9][0-9]*$/.test(t),'bad signed token');
      if(t==='0'){src.push(current);current=[]}else{let x=Number(t);ok(Number.isSafeInteger(x)&&Math.abs(x)<=n,'literal');current.push(x)}
    }
    ok(!current.length&&src.length===m,'termination/count');return src;
  }
  function signedBind(src,declared){ok(eq(src,declared),'source binding mismatch');return true}
  const steps=[],by=new Map();original.forEach((v,i)=>by.set('s'+i,v));
  function emit(rule,parents,out,pivot){let id='d'+(steps.length+1);steps.push({id,rule,parents,out,pivot:pivot??null});by.set(id,out);return id}
  function weak(parent,out){ok(by.get(parent).every(x=>out.includes(x)),'weak premise');return emit('WEAKEN',[parent],out)}
  function res(a,b,piv){let x=by.get(a),y=by.get(b);ok(x.includes(piv)&&y.includes(-piv),'pivot');
    let out=[...new Set([...x.filter(z=>z!==piv),...y.filter(z=>z!==-piv)])].sort((i,j)=>Math.abs(i)-Math.abs(j));
    ok(!out.some(z=>out.includes(-z)),'tautological result');return emit('RES',[a,b],out,piv);
  }
  const branches=[];
  for(let a of all.filter(v=>!C(v))){
    let useP=!P(a),useQ=!Q(a);ok(useP||useQ,'XOR soundness');
    let local=clause(a,useP?[1,2,3]:[2,3]);
    let i=original.findIndex(v=>key(v)===key(local));ok(i>=0,'source clause missing');
    let out=clause(a,S),id='s'+i;
    if(!eq(local,out))id=weak(id,out);
    branches.push({a:a.join(''),chosen:useP?'P':'Q',id,out});
  }
  ok(branches.length===2,'AND obligations');let l=branches.find(z=>z.a==='010'),r=branches.find(z=>z.a==='011');
  ok(l&&r&&l.chosen==='Q'&&r.chosen==='P','two cases / t');
  let concl=res(l.id,r.id,3);ok(eq(by.get(concl),c[0]),'wrong projected conclusion');
  let minusY=res(concl,'s6',1);ok(eq(by.get(minusY),[-2]),'wrong unit');
  let end=res('s7',minusY,2);ok(eq(by.get(end),[]),'no contradiction');
  function verify(source,proof,declared=original){
    signedBind(source,declared);
    let index=new Map();source.forEach((cl,i)=>{ok(Array.isArray(cl)&&cl.every(x=>Number.isSafeInteger(x)&&x!==0&&Math.abs(x)<=3),'bad literal');index.set('s'+i,cl)});
    for(const z of proof){
      ok(!index.has(z.id),'duplicate');let pp=z.parents.map(id=>index.get(id));ok(pp.every(Boolean),'forward/unbound premise');
      let expected;
      if(z.rule==='WEAKEN'){ok(pp.length===1,'weak arity');ok(pp[0].every(x=>z.out.includes(x)),'illegal weakening');expected=z.out}
      else if(z.rule==='RES'){
        ok(pp.length===2,'res arity');ok(pp[0].includes(z.pivot)&&pp[1].includes(-z.pivot),'wrong orientation');
        expected=[...new Set([...pp[0].filter(x=>x!==z.pivot),...pp[1].filter(x=>x!==-z.pivot)])].sort((i,j)=>Math.abs(i)-Math.abs(j));
      } else fail('unknown rule');
      ok(!expected.some(x=>expected.includes(-x)),'tautological');ok(eq(z.out,expected),'bad resolvent');index.set(z.id,z.out);
    }
    ok(proof.length&&eq(proof.at(-1).out,[]),'not refutation');return true;
  }
  ok(verify(parse(dimacs(original)),steps),'source-authenticated original');
  let satBase=all.filter(a=>[...p,...q].every(z=>sat(z,a))).map(z=>z.join(''));
  let satFull=all.filter(a=>original.every(z=>sat(z,a)));
  ok(eq(satBase,['000','100','111'])&&satFull.length===0,'both-label controls');
  for(const t of [0,1]){const a=[0,1,t];ok(!C(a),'conclusion false');
    ok(t===0?(!Q(a)&&P(a)):(!P(a)&&Q(a)),'one-parent-only error');
  }
  const negatives=[];function bad(name,fn){let s=JSON.parse(JSON.stringify(original)),r=JSON.parse(JSON.stringify(steps));
    fn(s,r);let rejected=false;try{verify(s,r)}catch(e){rejected=true}ok(rejected,'false accept '+name);negatives.push(name)}
  bad('wrong-pivot',(s,r)=>{r.find(z=>z.rule==='RES').pivot=1});
  bad('changed-resolvent',(s,r)=>{r.at(-1).out=[1]});
  bad('missing-parent',(s,r)=>{r[0].parents=['unknown']});
  bad('forward-parent',(s,r)=>{r[0].parents=['d99']});
  bad('invalid-weakening',(s,r)=>{r.find(z=>z.rule==='WEAKEN').out=[2,3]});
  bad('altered-original-source-sign',(s,r)=>{s[0][0]=-s[0][0]});
  bad('omitted-required-t-case',(s,r)=>{r.splice(r.findIndex(z=>z.id===l.id),1)});
  const malformed=['p cnf 3 1\n1 -0','p cnf 3 1\n1 0 0','p cnf 3 1\n4 0','p cnf -3 1\n1 0','p cnf 3 1\n1'];
  for(const x of malformed){let rejected=false;try{parse(x)}catch(e){rejected=true}ok(rejected,'malformed pass');}
  const summary={status:'PASS',system:'distinct declared R_canon500; NOT historical R_mix341',
    sourceCount:original.length,source:original,sourceText:dimacs(original),numVariables:3,
    Pclauses:p.length,Qclauses:q.length,Cclauses:c.length,conclusion:c[0],
    branchWitnesses:branches,paidProof:steps,paidNodes:steps.length,paidWeakenings:steps.filter(x=>x.rule==='WEAKEN').length,
    paidResolutions:steps.filter(x=>x.rule==='RES').length,baseModels:satBase,fullModels:satFull.length,
    corruptedRejected:negatives,malformedRejected:malformed.length,distinctAncestorCone:3,
    falseConclusionModelsWithPOnly:['010'],falseConclusionModelsWithQOnly:['011']};
  root.lspv3_500_summary=summary;if(typeof module!=='undefined')module.exports={run:()=>summary};
  if(typeof console!=='undefined'&&typeof process!=='undefined'&&process.argv?.[1]?.includes('lspv3_500_guarded_auxxor'))console.log(JSON.stringify(summary,null,2));
})(globalThis);