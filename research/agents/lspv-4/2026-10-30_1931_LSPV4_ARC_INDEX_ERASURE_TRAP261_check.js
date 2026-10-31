// Independent checker for ARC-INDEX-ERASURE-TRAP261.
// Run from repository root with node [this-file].
function independentlyCheck(fixtures,raw){
 const check=(x,m)=>{if(!x)throw Error(m)};let assertions=0;
 for(const [name,F] of Object.entries(fixtures)){
   const R=raw.source_controls[name];let models=0;
   for(let a=0;a<32768;a++){
     let sat=F.every(C=>C.some(l=>(((a>>(Math.abs(l)-1))&1)===Number(l>0))));
     if(sat)models++;
   }
   check(models===R.models,'source model count '+name);assertions++;
   check((models>0)===R.dpll.sat,'DPLL label '+name);assertions++;
   for(let P of R.pair_modes){
     let [j,k]=P.source_clauses;const V=[...new Set([...F[j-1],...F[k-1]].map(Math.abs))];
     for(let s of ['S','U'])for(let u of ['S','U']){
       let exists=false;
       for(let a=0;a<(1<<V.length);a++){
         const assignment=new Map(V.map((v,i)=>[v,(a>>i)&1]));
         const both=[[F[j-1],s],[F[k-1],u]].every(([C,z])=>
           C.every(l=>assignment.get(Math.abs(l))===Number((l>0)===(z==='S'))));
         if(both){exists=true;break}
       }
       check(exists===P[s+u],'pair mode '+name);assertions++;
     }
   }
   for(let item of R.flip_trail){
     let t=F.map(C=>C.filter(l=>(((item.mask>>(Math.abs(l)-1))&1)===Number(l>0))).length);
     check(t.join(',')===item.t.join(','),'flip trail '+name);assertions++;
   }
   let resolution=R.resolution;
   for(let a=0;a<32768;a++){
     const inCube=Object.entries(resolution.prohibited_cube).every(([id,v])=>((a>>(Number(id)-1))&1)===v);
     if(inCube)check(!F.every(C=>C.some(l=>((a>>(Math.abs(l)-1))&1)===Number(l>0))),'resolvent cube unsound');
   }
   assertions++;
 }
 for(let t of raw.index_traces){
   let h=t.high_index_cell,q=t.repetitions;
   check(t.guest_actions===h+3*q,'guest operations');assertions++;
   check(t.rescan_actions===h+3*q+q*(h+1),'rescan operations');assertions++;
   check(t.cached_family_actions===h+4*q,'tagged family operations');assertions++;
 }
 return {passed:true,independent_assertions:assertions,models:Object.fromEntries(Object.entries(raw.source_controls).map(([name,C])=>[name,C.models]))};
}
if(typeof require==='function'&&require.main===module){
 const fs=require('fs');
 const F=JSON.parse(fs.readFileSync('research/agents/lspv-2/matched_cases260.json','utf8'));
 const R=JSON.parse(fs.readFileSync('results/raw/arc/2026-10-30_1931_LSPV4_ARC_INDEX_ERASURE_TRAP261_raw.json','utf8'));
 console.log(JSON.stringify(independentlyCheck(F,R),null,2));
}
