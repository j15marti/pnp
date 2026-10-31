"use strict";
/* Independently replays the source truth tables, all indexed S/U pair
 * constraints, exact cofactor correspondence, witness and charged accounting.
 * Usage: node arc_quiescent_dfs266_check.js raw266.json */
function audit(R){
  let asserts=0;function ok(b,msg){asserts++;if(!b)throw Error("assert #"+asserts+": "+msg);}
  function sat(clause,mask){return clause.some(l=>((mask>>(Math.abs(l)-1))&1)===(l>0?1:0));}
  function full(F,mask){return F.every(c=>sat(c,mask));}
  function countTrue(cl,mask){return cl.filter(l=>((mask>>(Math.abs(l)-1))&1)===(l>0?1:0)).length;}
  function split(F,x,v){let ans=[];for(let cl of F){if(cl.some(l=>Math.abs(l)===x&&(l>0?1:0)===v))continue;ans.push(cl.filter(l=>Math.abs(l)!==x));}return ans;}
  function format(C,n){let s="p cnf "+n+" "+C.length+"\n";for(let cl of C)s+=cl.join(" ")+" 0\n";return s;}
  for(let rec of R.cases){
    let F=rec.original_clauses,n=rec.n,lim=1<<n,models=0,byPin=[0,0],found=null;
    for(let a=0;a<lim;a++)if(full(F,a)){models++;byPin[a&1]++;if(found===null)found=a;}
    ok(models===rec.models,rec.name+" source model count");
    ok((models>0)===rec.original_sat,rec.name+" label");
    if(found!==null){ok(rec.source_full_witness!==null,rec.name+" witness exists");ok(full(F,rec.source_full_witness),rec.name+" original witness valid");}
    else ok(rec.source_full_witness===null,rec.name+" no SAT witness");
    for(let v=0;v<=1;v++){
      let C=split(F,1,v),ind=rec.cofactor_counts.find(p=>p.v===v),nc=0;
      for(let a=0;a<lim;a++)if(full(C,a))nc++;
      ok(nc===ind.count,rec.name+" child brute count");
      ok(nc===2*byPin[v],rec.name+" exact pinned-source cofactor correspondence");
    }
    let seen=rec.serial.child_log;
    ok(seen.length===rec.serial.child_calls,rec.name+" call count");
    for(let i=0;i<seen.length;i++){
      let cl=split(F,1,seen[i].pin_x1),bytes=format(cl,n).length;
      ok(JSON.stringify(cl)===JSON.stringify(seen[i].child_clauses),rec.name+" exact serialized clauses");
      ok(bytes===seen[i].physical_child_bytes,rec.name+" physical bytes");
      ok(seen[i].sat===(byPin[seen[i].pin_x1]>0),rec.name+" same-source child label");
      if(i<seen.length-1)ok(!seen[i].sat,rec.name+" only continue after NO");
    }
    ok(rec.serial.sat===rec.original_sat,rec.name+" serial both-label");
    ok(rec.serial.peak_live_child_buffer_bytes===Math.max(...seen.map(x=>x.physical_child_bytes)),rec.name+" peak one-buffer");
    ok(rec.batch.peak_live_child_buffer_bytes===[0,1].reduce((s,v)=>s+format(split(F,1,v),n).length,0),rec.name+" eager buffers");
    ok(rec.batch.peak_live_child_buffer_bytes>=rec.serial.peak_live_child_buffer_bytes,rec.name+" peak gap");
    let origRead=F.reduce((s,c)=>s+c.length,0);
    ok(rec.serial.source_literal_reads===seen.length*origRead,rec.name+" source scans charged");
    ok(rec.serial.child_bytes_written===seen.reduce((s,x)=>s+x.physical_child_bytes,0),rec.name+" output writes charged");
    ok(rec.serial.selected_work===rec.serial.source_literal_reads+rec.serial.child_bytes_written+rec.serial.guest_literal_tests+rec.serial.reset_upper_proxy_cells,rec.name+" full selected ledger");
    if(F.every(c=>c.length===3)){
      ok(rec.indexed_local_extremes.length===F.length,rec.name+" indexed source clauses");
      for(let j=0;j<F.length;j++){
        let occ=rec.indexed_local_extremes[j].occurrences;ok(occ.length===3,rec.name+" proper");
        for(let o=0;o<3;o++){let lit=F[j][o];ok(occ[o].signed_occurrence===lit,rec.name+" occurrence sign");
          ok(occ[o].local_S===(lit>0?1:0),rec.name+" local S");
          ok(occ[o].local_U===(lit>0?0:1),rec.name+" local U");
          ok(occ[o].invert_S_U===occ[o].local_U && occ[o].invert_U_S===occ[o].local_S,rec.name+" inverse");
        }
      }
      for(let row of rec.pair_compatibility){
        let [i,j]=row.source_clauses,A=F[i-1],B=F[j-1],vars=[...new Set([...A,...B].map(x=>Math.abs(x)))];
        ok(i<j,rec.name+" indexed pair order");
        for(let mode of ["SS","SU","US","UU"]){let exists=false;
          for(let mask=0;mask<(1<<vars.length);mask++){let a=0;for(let k=0;k<vars.length;k++)a|=((mask>>k)&1)<<(vars[k]-1);
            if(countTrue(A,a)===(mode[0]==="S"?3:0)&&countTrue(B,a)===(mode[1]==="S"?3:0)){exists=true;break;}
          }
          ok(exists===row[mode],rec.name+" pair "+i+"-"+j+" "+mode);
        }
      }
      for(let stat of rec.endpoints_and_flip_trail){
        let counts=F.map(c=>countTrue(c,stat.assignment)),hist=[0,0,0,0];for(let x of counts)hist[x]++;
        ok(JSON.stringify(counts)===JSON.stringify(stat.counts),rec.name+" flip full counts");
        ok(JSON.stringify(hist)===JSON.stringify(stat.histogram),rec.name+" flip histogram");
        ok(stat.formula_sat===(hist[0]===0),rec.name+" flip SAT");
      }
      for(let p of rec.resolvent_forbidden_cubes.examples){
        let [i,j]=p.parents,A=F[i-1],B=F[j-1],x=p.pivot;
        let pa=A.find(l=>Math.abs(l)===x),pb=B.find(l=>Math.abs(l)===x);
        ok(pa===-pb,rec.name+" genuine opposite pivot");
        let resolvent=[...new Set([...A.filter(l=>Math.abs(l)!==x),...B.filter(l=>Math.abs(l)!==x)])];
        ok(JSON.stringify(resolvent)===JSON.stringify(p.resolvent),rec.name+" correct resolvent");
        for(let a=0;a<lim;a++)if(full(F,a)){ok(sat(resolvent,a),rec.name+" original-source resolvent sound");}
      }
    }
  }
  let wanted=[["6/5","23/45",2],["241/200","11642479/23232400",2],["7/5","949/5145",3],["3/2","49/648",4],["8/5","2145161/335544320",8]];
  for(let [i,e] of wanted.entries()){let f=R.flmv[i];ok(f.c===e[0]&&f.max===e[1]&&f.max_k===e[2],"exact FLMV match");ok(f.tail_excluded_from>=f.max_k+1,"FLMV tail sorted");}
  return {pass:true,assertions:asserts,cases:R.cases.map(c=>({name:c.name,models:c.models,serial_calls:c.serial.child_calls,serial_peak_bytes:c.serial.peak_live_child_buffer_bytes,eager_peak_bytes:c.batch.peak_live_child_buffer_bytes})),status:"independent finite truth-table check, not a native indexed-TM benchmark"};
}
if(typeof require!=="undefined" && require.main===module){
  const fs=require("fs");if(!process.argv[2])throw Error("usage: node arc_quiescent_dfs266_check.js results.json");
  console.log(JSON.stringify(audit(JSON.parse(fs.readFileSync(process.argv[2],"utf8"))),null,2));
}
