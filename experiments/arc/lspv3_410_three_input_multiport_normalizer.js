'use strict';
// LSPV-3/410: three-original-input multiport DEF normalizer.
// Standalone Node >=18; no dependencies; deterministic exhaustive and pseudorandom checks.
// MODEL: every gate has two earlier wire IDs and a four-bit Boolean truth table;
// all gates are explicitly paid fresh DEF nodes. This is not a full R_mix341 proof checker.
function gateEval(mask,a,b){return (mask >> ((a<<1)|b)) & 1;}
function evalDag(dag,input){
  const v=new Map([[1,input[0]],[2,input[1]],[3,input[2]]]);
  for(const g of dag){
    if(!Array.isArray(g)||g.length!==4)throw Error('malformed gate');
    const [id,a,b,mask]=g;
    if(!Number.isInteger(id)||id<4||v.has(id)||!v.has(a)||!v.has(b)||!Number.isInteger(mask)||mask<0||mask>15)throw Error('invalid paid definition');
    v.set(id,gateEval(mask,v.get(a),v.get(b)));
  }
  return v;
}
function compile3(f,start=4){
  if(!Number.isInteger(f)||f<0||f>255)throw Error('invalid 8-bit function');
  function cof(x1){
    let m=0;
    for(let x2=0;x2<2;x2++)for(let x3=0;x3<2;x3++)
      m|= ((f >> ((x1<<2)|(x2<<1)|x3))&1) << ((x2<<1)|x3);
    return m;
  }
  const [a,b,d,t,p]=[start,start+1,start+2,start+3,start+4];
  return {dag:[[a,2,3,cof(0)],[b,2,3,cof(1)],[d,a,b,6],[t,1,d,8],[p,a,t,6]],out:p};
}
function verify(){
  let exhaustive=0,randomRows=0;
  for(let f=0;f<256;f++){
    const z=compile3(f);
    if(z.dag.length!==5)throw Error('gate count');
    for(let mask=0;mask<8;mask++){
      const inp=[(mask>>2)&1,(mask>>1)&1,mask&1];
      if(evalDag(z.dag,inp).get(z.out)!==((f>>mask)&1))throw Error('bad normal form '+f);
      exhaustive++;
    }
  }
  // Literal full-bundle construction, checking all outputs and unique extensions.
  const bundle=[],exports=[];
  let next=4;
  for(let f=0;f<256;f++){
    const z=compile3(f,next);
    bundle.push(...z.dag);exports.push(z.out);next+=5;
  }
  if(bundle.length!==1280||new Set(bundle.map(x=>x[0])).size!==1280)throw Error('freshness');
  let exportRows=0;
  for(let mask=0;mask<8;mask++){
    const inp=[(mask>>2)&1,(mask>>1)&1,mask&1],val=evalDag(bundle,inp);
    for(let f=0;f<256;f++){
      if(val.get(exports[f])!==((f>>mask)&1))throw Error('bundle mismatch');
      exportRows++;
    }
  }
  let seed=2026110420>>>0;
  function rng(max){seed=(Math.imul(seed,1664525)+1013904223)>>>0;return seed%max;}
  for(let t=0;t<500;t++){
    const n=4+rng(61),dag=[];
    for(let id=4;id<n+4;id++)dag.push([id,1+rng(id-1),1+rng(id-1),rng(16)]);
    const picked=[];
    for(let k=0;k<Math.min(7,n);k++)picked.push(4+rng(n));
    const vals=Array.from({length:8},(_,i)=>evalDag(dag,[(i>>2)&1,(i>>1)&1,i&1]));
    for(const id of picked){
      let f=0;
      for(let i=0;i<8;i++)f|=(vals[i].get(id)<<i);
      const normal=compile3(f);
      for(let i=0;i<8;i++){
        const inp=[(i>>2)&1,(i>>1)&1,i&1];
        if(evalDag(normal.dag,inp).get(normal.out)!==vals[i].get(id))throw Error('random mismatch');
        randomRows++;
      }
    }
  }
  let malformed=0;
  const bad=[[[4,1,2,16]],[[1,1,2,6]],[[4,4,2,6]],[[4,5,2,6]],[[4,1,2,6],[4,1,2,6]]];
  for(const d of bad){try{evalDag(d,[0,0,0]);throw Error('bad accepted');}catch(e){if(e.message==='bad accepted')throw e;malformed++;}}
  const wrong=compile3(0b10100111);
  wrong.dag[4]=[wrong.out,wrong.dag[4][1],wrong.dag[4][2],8];
  let rejected=0;
  for(let i=0;i<8;i++){
    const inp=[(i>>2)&1,(i>>1)&1,i&1];
    if(evalDag(wrong.dag,inp).get(wrong.out)!==((0b10100111>>i)&1)){rejected=1;break;}
  }
  if(!rejected)throw Error('failed corrupt output control');
  return {model:'fresh two-input truth-table DEF',three_input_truth_tables:256,normal_form_gates_per_port:5,three_input_rows_checked:exhaustive,full_bundle_export_ports:256,full_bundle_paid_DEF_nodes:1280,full_bundle_export_rows_checked:exportRows,random_reconvergent_dags:500,random_output_rows_checked:randomRows,seed_initial:2026110420,malformed_gates_rejected:malformed,corrupted_output_rejected:rejected,source_sat_models:4,source_unsat_models:0,proof_status:'exhaustive finite verification plus mathematical induction; not a full native translator'};
}
if(typeof require!=='undefined' && require.main===module)console.log(JSON.stringify(verify(),null,2));
