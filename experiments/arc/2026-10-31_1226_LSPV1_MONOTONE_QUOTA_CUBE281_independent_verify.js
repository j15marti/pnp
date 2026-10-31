'use strict';
// Independent original-source verifier: imports no producer code.

function check(condition,message){if(!condition)throw Error(message||'independent verification failure');}
function verify(F,R){
  const n=R.source_size.variables;
  check(Array.isArray(F)&&F.length===4*n/3,'m/n mismatch');
  const p=Array(n+1).fill(0),q=Array(n+1).fill(0),s=new Set();
  for(const C of F){
    check(C.length===3&&new Set(C.map(x=>Math.abs(x))).size===3,'improper clause');
    check(C.every(x=>x>0)||C.every(x=>x<0),'mixed polarity');
    const key=C.slice().sort((a,b)=>a-b).join(',');
    check(!s.has(key),'duplicate');s.add(key);
    for(const x of C){check(Math.abs(x)<=n&&Math.abs(x)>0,'bad variable');(x>0?p:q)[Math.abs(x)]++;}
  }
  check(p.slice(1).every(x=>x===2)&&q.slice(1).every(x=>x===2),'signed degree');
  check(R.original_clause_extreme_targets.length===F.length,'per-clause provenance missing');
  for(let j=0;j<F.length;j++){
    const a=R.original_clause_extreme_targets[j];
    check(a.source_clause_index===j,'source clause index wrong');
    for(let k=0;k<3;k++){
      const x=F[j][k],o=a.original_occurrences[k];
      check(o.literal===x&&o.variable===Math.abs(x),'literal provenance');
      check(o.S===Number(x>0)&&o.U===Number(x<0)&&o.invert_S===o.U&&o.invert_U===o.S,'local extrema or inverse');
    }
  }
  const matrix=R.clause_pair_extreme_compatibility.lexicographic_pairs_hex;
  check(matrix.length===F.length*(F.length-1)/2,'matrix pair count');
  let index=0;
  for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++){
    let mask=0;
    for(const mode of [['S','S',1],['S','U',2],['U','S',4],['U','U',8]]){
      let good=true,demands=new Map();
      for(const [C,kind] of [[F[i],mode[0]],[F[j],mode[1]]]){
        for(const lit of C){
          const v=Math.abs(lit),b=kind==='S'?Number(lit>0):Number(lit<0);
          if(demands.has(v)&&demands.get(v)!==b)good=false;
          demands.set(v,b);
        }
      }
      if(good)mask|=mode[2];
    }
    check(parseInt(matrix[index],16)===mask,'pair extreme mode mismatch j='+i+' k='+j);index++;
  }
  const hist=(a)=>{const h=[0,0,0,0];for(const c of F)h[c.filter(l=>a[Math.abs(l)]===Number(l>0)).length]++;return h;};
  const all0=Array(n+1).fill(0),all1=Array(n+1).fill(1);
  for(const [tag,a] of [['zero',all0],['one',all1]])check(hist(a).join()===R.endpoint_four_category_hist['all_'+tag].join(),'endpoint mismatch');
  let singles=0;
  for(let i=1;i<=n;i++)for(let b of [0,1]){const a=Array(n+1).fill(b);a[i]=1-b;check(hist(a).join()===R.each_single_variable_flip_hist.join(),'flip histogram');singles++;}
  check(singles===R.all_single_flip_checks,'flip record count');
  for(const row of R.sampled_coherent_partial_cubes){
    const a=Array(n+1).fill(-1);for(const [i,v] of row.assigned_literal_values){check(a[i]===-1||a[i]===v,'contradictory assigned cube');a[i]=v;}
    const t=a.slice(1).filter(v=>v===1).length,f=a.slice(1).filter(v=>v===0).length;
    check(row.fixed_true===t&&row.fixed_false===f,'cube assigned counts');
    for(const polarity of ['positive','negative']){
      const sign=polarity==='positive'?1:-1,bad=sign===1?0:1,checkHist=[0,0,0,0],fail=[];
      for(let j=0;j<F.length;j++){
        const c=F[j];if(Math.sign(c[0])!==sign)continue;
        let freeOrTrue=0;for(const l of c){if(a[Math.abs(l)]!==bad)freeOrTrue++;}
        checkHist[freeOrTrue]++;if(freeOrTrue===0)fail.push(j);
      }
      check(row.buckets[polarity].join()===checkHist.join(),'cube bucket mismatch');
      check(row.source_falsified_clause_indices[polarity].join()===fail.join(),'original falsified clause proofs wrong');
      const k=sign===1?f:t;
      check(checkHist[0]===2*(k-2*n/3)+checkHist[2]+2*checkHist[3],'conservation identity false');
    }
  }
  for(const parent of R.original_source_parent_resolution_forbidden_cubes){
    const [j,k]=parent.parents,pivot=parent.pivot,first=F[j],second=F[k];
    check(first.some(x=>Math.abs(x)===pivot)&&second.some(x=>Math.abs(x)===pivot),'parent pivot missing');
    check(first.some(x=>second.includes(-x)&&Math.abs(x)===pivot),'parent source signs');
    const out=first.filter(x=>Math.abs(x)!==pivot).concat(second.filter(x=>Math.abs(x)!==pivot));
    check(out.join()===parent.derived_clause.join(),'resolvent mismatch');
    check(!out.some(x=>out.includes(-x)),'tautological resolvent');
    for(const lit of out)check(parent.forbidden_partial_cube[Math.abs(lit)]===Number(lit<0),'incorrect forbidden cube');
  }
  if(R.SAT_witness){
    const a=[0,...R.SAT_witness.model_bits.split('').map(Number)];
    check(a.length===n+1,'witness length');
    check(F.every(C=>C.some(l=>a[Math.abs(l)]===Number(l>0))),'false SAT witness');
    check(hist(a).join()===R.SAT_witness.status_histogram.join(),'witness histogram');
  }
  if(n<=9){
    let models=0;for(let z=0;z<2**n;z++){
      const a=[0,...Array.from({length:n},(_,j)=>(z>>j)&1)];
      models+=Number(F.every(C=>C.some(l=>a[Math.abs(l)]===Number(l>0))));
    }
    check(R.exact_small_model_count===models,'finite model count mismatch');
  }
  return {name:R.name,n,m:F.length,checked_pair_modes:4*matrix.length,checked_partial_cubes:R.sampled_coherent_partial_cubes.length,checked_resolvents:R.original_source_parent_resolution_forbidden_cubes.length};
}


const fs=require('node:fs');
const sourcePath=process.argv[2]||'research/agents/lspv-2/2026-10-24_0011_DOECKER61_original_source.txt';
const prefix=process.argv[3]||'results/raw/arc/2026-10-31_1226_LSPV1_MONOTONE_QUOTA_CUBE281_';
const txt=fs.readFileSync(sourcePath,'utf8'),U=JSON.parse(txt.slice(txt.indexOf('[[')));
const V=U.map(c=>c.slice());[V[2][2],V[44][2]]=[V[44][2],V[2][2]];
const P6=[[1,2,3],[1,4,5],[2,4,6],[3,5,6]],Q6=[[1,2,4],[1,3,6],[2,3,5],[4,5,6]],P9=[[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9]],Q9=[[2,4,7],[1,6,9],[4,5,6],[3,7,8],[1,5,8],[2,3,9]];
function join(P,Q){return P.concat(Q.map(c=>c.map(x=>-x)));}
let total=0;for(const [name,F] of [['Y6',join(P6,Q6)],['Z9',join(P9,Q9)],['U198',U],['V198',V]]){
  const R=JSON.parse(fs.readFileSync(prefix+name+'.json','utf8'));
  const result=verify(F,R);total+=result.checked_pair_modes;
  console.log(JSON.stringify(result));
}
console.log('INDEPENDENT VERIFY281 PASS',total,'source-pair mode tests');
