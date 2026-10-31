'use strict';
// Independent, dependency-free Node.js raw producer, original source authentication by grammar and parent clauses.

function validate(F,n){
  if(!Number.isInteger(n)||n<3||n%3!==0||!Array.isArray(F)||F.length!==4*n/3)return false;
  const p=Array(n+1).fill(0),q=Array(n+1).fill(0),seen=new Set();
  for(const c of F){
    if(!Array.isArray(c)||c.length!==3||c.some(x=>!Number.isInteger(x)||x===0||Math.abs(x)>n)||new Set(c.map(Math.abs)).size!==3||!(c.every(x=>x>0)||c.every(x=>x<0)))return false;
    const key=c.slice().sort((a,b)=>a-b).join(',');
    if(seen.has(key))return false;seen.add(key);
    for(const x of c)(x>0?p:q)[Math.abs(x)]++;
  }
  return p.slice(1).every(x=>x===2)&&q.slice(1).every(x=>x===2);
}
function witness(F,a){return F.every(c=>c.some(x=>a[Math.abs(x)]===Number(x>0)));}
function hist(F,a){const h=[0,0,0,0];for(const c of F){let t=0;for(const x of c)t+=Number(a[Math.abs(x)]===Number(x>0));h[t]++;}return h;}
function cube(F,n,c){
  let t=0,f=0;for(let i=1;i<=n;i++){t+=Number(c[i]===1);f+=Number(c[i]===0);}
  const out={fixed_true:t,fixed_false:f,free:n-t-f,buckets:{positive:[0,0,0,0],negative:[0,0,0,0]},source_falsified_clause_indices:{positive:[],negative:[]},source_literal_tests:3*F.length};
  for(let j=0;j<F.length;j++){
    const plus=F[j][0]>0,sign=plus?'positive':'negative',bad=plus?0:1;
    let r=0;for(const x of F[j])if(c[Math.abs(x)]!==bad)r++;
    out.buckets[sign][r]++;if(r===0)out.source_falsified_clause_indices[sign].push(j);
  }
  for(const [sign,k] of [['positive',f],['negative',t]]){
    const q=out.buckets[sign],rhs=2*(k-2*n/3)+q[2]+2*q[3];
    if(q[0]!==rhs||q[0]!==out.source_falsified_clause_indices[sign].length||q[0]<Math.max(0,2*(k-2*n/3)))throw Error('exact signed quota/cube identity failed '+sign);
  }
  return out;
}
function dpll(F,n,limit){
  let nodes=0,lits=0,leaves=0;let found=null;
  function dfs(a){
    nodes++;if(nodes>limit)return null;
    while(true){
      let unit=0,done=true;
      for(const c of F){
        let yes=false,unknown=0,last=0;
        for(const l of c){
          lits++;const v=a[Math.abs(l)];
          if(v===-1){unknown++;last=l;}
          else if(v===Number(l>0)){yes=true;break;}
        }
        if(yes)continue;
        done=false;
        if(unknown===0){leaves++;return false;}
        if(unknown===1){unit=last;break;}
      }
      if(done){found=a.slice();return true;}
      if(!unit)break;
      const j=Math.abs(unit),v=Number(unit>0);
      if(a[j]>=0&&a[j]!==v){leaves++;return false;}
      a[j]=v;
    }
    let j=0;for(let x=1;x<=n;x++)if(a[x]===-1){j=x;break;}
    if(!j)return false;
    for(const val of [0,1]){const b=a.slice();b[j]=val;const r=dfs(b);if(r===null)return null;if(r)return true;}
    return false;
  }
  const result=dfs(Array(n+1).fill(-1));
  if(result===true&&!witness(F,found.map(x=>x<0?0:x)))throw Error('bad DPLL witness');
  return {status:result===null?'UNRESOLVED':result?'SAT':'UNSAT',nodes,source_literal_tests:lits,failed_leaves:leaves};
}
function audit(F,n,name,verifiedLabel,verifiedWitness){
  if(!validate(F,n))throw Error(name+' grammar failed');
  const z=Array(n+1).fill(0),o=Array(n+1).fill(1),e=[2*n/3,0,0,2*n/3],e1=[2*n/3-2,2,2,2*n/3-2];
  if(hist(F,z).join()!==e.join()||hist(F,o).join()!==e.join())throw Error('endpoint invariant failed');
  let flipChecks=0;for(let i=1;i<=n;i++)for(let base of [0,1]){const a=(base?o:z).slice();a[i]=1-base;if(hist(F,a).join()!==e1.join())throw Error('one-bit histogram invariant failed');flipChecks++;}
  let modelCount=null;
  if(n<=9){modelCount=0;for(let i=0;i<2**n;i++){const a=[0];for(let j=1;j<=n;j++)a.push((i>>(j-1))&1);modelCount+=Number(witness(F,a));}if((modelCount>0)!==(verifiedLabel==='SAT'))throw Error('small-model label mismatch');}
  let witnessRecord=null;if(verifiedWitness){const a=[0,...verifiedWitness.split('').map(Number)];if(a.length!==n+1||!witness(F,a))throw Error('supplied witness fails source');witnessRecord={verified:true,model_bits:verifiedWitness,status_histogram:hist(F,a)};}
  const occ=F.map((cl,j)=>({source_clause_index:j,original_occurrences:cl.map(l=>({variable:Math.abs(l),literal:l,S:Number(l>0),invert_S:Number(l<0),U:Number(l<0),invert_U:Number(l>0)}))}));
  let hex='',pairTests=0,sharedTests=0, modes={0:0,6:0,9:0,15:0,other:0},resolvents=[];
  for(let j=0;j<F.length;j++)for(let k=j+1;k<F.length;k++){
    const A=F[j],B=F[k],shareSame=[],shareOpp=[];
    for(const x of A)for(const y of B){sharedTests++;if(Math.abs(x)===Math.abs(y))(Math.sign(x)===Math.sign(y)?shareSame:shareOpp).push(x);}
    const same=shareSame.length>0,opposite=shareOpp.length>0;
    const mask=(opposite?0:9)|(same?0:6);hex+=mask.toString(16);
    if(modes[mask]===undefined)modes.other++;else modes[mask]++;pairTests++;
    if(shareOpp.length===1){
      const pivot=Math.abs(shareOpp[0]),r=A.filter(x=>Math.abs(x)!==pivot).concat(B.filter(x=>Math.abs(x)!==pivot));
      if(!r.some(x=>r.includes(-x))){
        const falsifying_cube={};for(const x of r)falsifying_cube[Math.abs(x)]=Number(x<0);
        resolvents.push({parents:[j,k],pivot,derived_clause:r,forbidden_partial_cube:falsifying_cube,proof:'one source-parent resolution step'});
      }
    }
  }
  const sample=[];
  function push(name,entries){const c=Array(n+1).fill(-1);for(const [j,v]of entries)c[j]=v;sample.push({label:name,assigned_literal_values:entries,...cube(F,n,c)});}
  push('empty_cube',[]);push('0_to_all',[...Array(n)].map((_,i)=>[i+1,0]));push('1_to_all',[...Array(n)].map((_,i)=>[i+1,1]));
  for(const s of [0,1])for(const k of [...new Set([1,2,3,Math.floor(2*n/3),Math.floor(2*n/3)+1,n])])push('prefix_'+s+'_'+k,[...Array(k)].map((_,i)=>[i+1,s]));
  const neg=F.find(c=>c[0]<0),pos=F.find(c=>c[0]>0);
  push('negative_original_clause_falsifying_cube',neg.map(x=>[Math.abs(x),1]));
  push('positive_original_clause_falsifying_cube',pos.map(x=>[Math.abs(x),0]));
  let exhaustive=0;if(n<=9){for(let code=0;code<3**n;code++){
    const a=Array(n+1).fill(-1);let v=code;for(let j=1;j<=n;j++){a[j]=v%3-1;v=Math.floor(v/3);}cube(F,n,a);exhaustive++;
  }}
  const corruption=[F.slice(1),F.concat([F[0]]),F.map((c,i)=>i===0?[c[0],c[0],c[2]]:c),F.map((c,i)=>i===0?[-c[0],c[1],c[2]]:c)];
  if(corruption.some(Q=>validate(Q,n)))throw Error('malformed input rejection failed');
  return {name,label:verifiedLabel,source_size:{variables:n,clauses:F.length,signed_occurrences:3*F.length},canonical_valid:true,
    exact_small_model_count:modelCount,SAT_witness:witnessRecord,
    UNSAT_certificate_dependency:verifiedLabel==='UNSAT'?'Original Döcker Appendix C 6-module complete 64-row refutation, independently verified in LSPV-5 TARGET_SCOPE247 and LSPV-1 PORT_CUT280':null,
    endpoint_four_category_hist:{all_zero:hist(F,z),all_one:hist(F,o)},
    each_single_variable_flip_hist:e1,all_single_flip_checks:flipChecks,
    original_clause_extreme_targets:occ,
    clause_pair_extreme_compatibility:{modes:['SS','SU','US','UU'],hex_bitmask_order:[1,2,4,8],lexicographic_pairs_hex:hex,mask_tally:modes,pairs:pairTests},
    original_source_parent_resolution_forbidden_cubes:resolvents,
    sampled_coherent_partial_cubes:sample,exhaustive_three_valued_partial_cubes:exhaustive,
    baseline_DPLL:dpll(F,n,n<=9?100000:1000),
    experimental_work_ledger:{source_grammar_occurrence_tests:3*F.length,source_flip_occurrence_tests:flipChecks*3*F.length,clause_pair_shared_literal_comparisons:sharedTests,source_parent_resolution_count:resolvents.length,source_partial_cube_literal_inspections:(sample.length+exhaustive)*3*F.length,actual_printed_raw_bytes:'available from resulting raw file',notes:'Host-language event ledger only; not native FLMV tape transitions, output storage retained and paid'},
    malformed_source_mutations_rejected:corruption.length
  };
}


const fs=require('node:fs');
const path=require('node:path');
const sourcePath=process.argv[2]||'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt';
const out=process.argv[3]||'results/raw/arc/2026-10-31_1226_LSPV1_MONOTONE_QUOTA_CUBE281_raw.json';
const s=fs.readFileSync(sourcePath,'utf8'),U=JSON.parse(s.slice(s.indexOf('[[')));
const V=U.map(c=>c.slice());[V[2][2],V[44][2]]=[V[44][2],V[2][2]];
const W='001110010011110001010001110100111110011011000101000101001010100001011010'+'101011000100000111001010110101001110001001101000110001100010100101101110'+'010101011001001100000110111001001101001101101001010101';
const P6=[[1,2,3],[1,4,5],[2,4,6],[3,5,6]],Q6=[[1,2,4],[1,3,6],[2,3,5],[4,5,6]];
const P9=[[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9]];
const Q9=[[2,4,7],[1,6,9],[4,5,6],[3,7,8],[1,5,8],[2,3,9]];
function join(P,Q){return P.concat(Q.map(c=>c.map(x=>-x)));}
const rows=[audit(join(P6,Q6),6,'Y6','SAT'),audit(join(P9,Q9),9,'Z9','SAT'),audit(U,198,'U198','UNSAT'),audit(V,198,'V198','SAT',W)];
const raw={run:'MONOTONE-QUOTA-CUBE281',date:'2026-10-31 12:26 America/Los_Angeles',
   status:'PROVED/EXACT restricted elementary identities, independent referee pending; COMPUTATIONAL finite checks; P vs NP OPEN',
   source_path:sourcePath,rows,
   theorem:'For each signed mode q0=2(k-2n/3)+q2+2q3, with k=fixed TRUE for negative and fixed FALSE for positive clauses.',
   caveat:'Quota reject never beats a fully checked original falsified-clause check. Prior 198-variable UNSAT certificate is imported, not reconstructed in this checker. No ARC child or FLMV bound is established.'};
fs.mkdirSync(path.dirname(out),{recursive:true});fs.writeFileSync(out,JSON.stringify(raw,null,2)+'\n');
console.log(JSON.stringify({rows:rows.map(r=>({name:r.name,label:r.label,small_model_count:r.exact_small_model_count,
  pairs:r.clause_pair_extreme_compatibility.pairs,resolvents:r.original_source_parent_resolution_forbidden_cubes.length,
  flips:r.all_single_flip_checks,partial_cubes:r.exhaustive_three_valued_partial_cubes,DPLL:r.baseline_DPLL})),outfile:out}));
