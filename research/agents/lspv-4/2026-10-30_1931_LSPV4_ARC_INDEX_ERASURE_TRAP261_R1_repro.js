// LSPV-4 ARC-INDEX-ERASURE-TRAP261_R1: run at repo root with node [this-file] > raw.json
// Selected-event instrumentation, not a native FLMV benchmark.
function audit(cases) {
  const must=(b,m)=>{if(!b)throw Error(m)};
  const tar=(l,s)=>s==='S'?Number(l>0):Number(l<0);
  const clauseStats=(F,a)=>{let t=F.map(C=>C.reduce((z,l)=>z+Number(((a>>(Math.abs(l)-1))&1)===Number(l>0)),0));
    let bins=[0,0,0,0];t.forEach(z=>bins[z]++);return {t,bins,sat:bins[0]===0}};
  function solver(F,n) {
    let m={nodes:0,branches:0,units:0,conflicts:0,probes:0};
    function dfs(A) {
      m.nodes++;
      for(;;) {
        let change=false,done=true;
        for(let C of F){
          let ok=false,free=0,last=0;
          for(let l of C){m.probes++;let v=A[Math.abs(l)-1];if(v===-1){free++;last=l}
            else if(v===Number(l>0)){ok=true;break}}
          if(ok)continue;done=false;
          if(free===0){m.conflicts++;return null}
          if(free===1){A[Math.abs(last)-1]=Number(last>0);m.units++;change=true;break}
        }
        if(done)return A.map(v=>v===-1?0:v);
        if(!change)break;
      }
      let id=A.indexOf(-1);must(id>=0,'bad recursion');m.branches++;
      for(let v of [0,1]){let B=A.slice();B[id]=v;let w=dfs(B);if(w)return w}
      return null;
    }
    let witness=dfs(Array(n).fill(-1));
    if(witness)must(F.every(C=>C.some(l=>witness[Math.abs(l)-1]===Number(l>0))),'bad witness');
    return {...m,sat:!!witness,witness,selected_work:F.length*3+m.nodes+m.branches+m.units+m.probes};
  }
  let controls={};
  for(let [name,F] of Object.entries(cases)){
    let n=Math.max(...F.flat().map(Math.abs)),m=F.length;
    let occurrence_targets=F.map((C,j)=>({source_clause:j+1,literals:C,occurrences:C.map(l=>({
      indexed_occurrence:'x_'+Math.abs(l)+','+(j+1),literal:l,
      local_all_SAT:tar(l,'S'),inverted_local_UNSAT:1-tar(l,'S'),
      local_all_UNSAT:tar(l,'U'),inverted_local_SAT:1-tar(l,'U')}))}));
    let pair_modes=[];
    for(let j=0;j<m;j++)for(let k=j+1;k<m;k++){
      let s=[],o=[],M={};
      for(let l of F[j])for(let p of F[k])if(Math.abs(l)===Math.abs(p))(l*p>0?s:o).push(Math.abs(l));
      for(let x of ['S','U'])for(let y of ['S','U']){
        let d=new Map(),yes=true;
        for(let [C,t] of [[F[j],x],[F[k],y]])for(let l of C){
          let id=Math.abs(l),v=tar(l,t);if(d.has(id)&&d.get(id)!==v)yes=false;d.set(id,v)}
        must(yes===(x===y?o.length===0:s.length===0),'pair conflict formula');
        let ids=[...new Set([...F[j],...F[k]].map(Math.abs))],exists=false;
        for(let b=0;b<(1<<ids.length);b++){
          let A=new Map(ids.map((id,p)=>[id,(b>>p)&1]));
          if([[F[j],x],[F[k],y]].every(([C,t])=>C.every(l=>A.get(Math.abs(l))===tar(l,t)))){exists=true;break}
        }
        must(exists===yes,'pair exhaustive test');M[x+y]=yes;
      }
      pair_modes.push({source_clauses:[j+1,k+1],same_sign:s,opposite_sign:o,
        SS:M.SS,SU:M.SU,US:M.US,UU:M.UU,universal_middle:s.length>0&&o.length>0});
    }
    let models=0;
    for(let a=0;a<(1<<n);a++){
      let r=clauseStats(F,a),q=clauseStats(F,a^((1<<n)-1));
      must(r.t.every((v,j)=>v+q.t[j]===3),'per-clause complement');
      must(r.bins.every((v,j)=>v===q.bins[3-j]),'histogram complement');
      if(r.sat)models++;
    }
    let resolution=null;
    outer:for(let j=0;j<m;j++)for(let k=j+1;k<m;k++)
      for(let p of F[j])if(F[k].includes(-p)){
        let D=[...new Set([...F[j].filter(l=>l!==p),...F[k].filter(l=>l!==-p)])];
        if(D.some(l=>D.includes(-l)))continue;
        let cube=Object.fromEntries(D.map(l=>[Math.abs(l),Number(l<0)]));
        for(let a=0;a<(1<<n);a++)if(Object.entries(cube).every(([id,v])=>((a>>(Number(id)-1))&1)===v))
          must(!clauseStats(F,a).sat,'resolution cube');
        resolution={source_parents:[j+1,k+1],pivot:Math.abs(p),resolvent:D,
          prohibited_cube:cube};break outer;
      }
    must(resolution!==null,'missing resolvent');
    let dpll=solver(F,n);must(dpll.sat===(models>0),'bad solver label');
    controls[name]={n,m,models,occurrence_targets,pair_modes,
      coherent_zero:clauseStats(F,0),coherent_one:clauseStats(F,(1<<n)-1),
      flip_trail:[0,1,3,7,15,(1<<n)-1].map((a,i)=>({step:i,mask:a,...clauseStats(F,a)})),
      resolution,exhaustive_complement_assignments:1<<n,dpll};
  }
  let index_traces=[];
  for(let h of [16,32,128])for(let q of [4,64,512])index_traces.push({
    high_index_cell:h,repetitions:q,read_only_input_address:'2^'+h,
    guest_actions:2*h+3*q+1,rescan_actions:2*h+3*q+1+q*(h+1),
    cached_family_actions:2*h+4*q+1,counted_index_cells:h+1});
  let paired=Object.entries(controls).map(([name,c])=>({
    source:name,sat:c.dpll.sat,models:c.models,dpll_nodes:c.dpll.nodes,
    baseline_selected_work:c.dpll.selected_work,
    wrapper_no_rescan:c.dpll.selected_work+833,
    wrapper_with_rescan:c.dpll.selected_work+9281}));
  return {id:'ARC-INDEX-ERASURE-TRAP261_R1',status:'restricted wrapper falsification; universal ARC OPEN',
    fixture:'research/agents/lspv-2/matched_cases260.json',
    index_traces,paired,source_controls:controls};
}
if (typeof require==='function' && require.main===module){
  const fs=require('fs');
  const cases=JSON.parse(fs.readFileSync('research/agents/lspv-2/matched_cases260.json','utf8'));
  console.log(JSON.stringify(audit(cases),null,2));
}
