"use strict";
// LSPV-4 ARC-SOURCE-PROBE-TRANSCRIPT257 independent Node.js reproducer.
// No external dependencies. Original clauses, S/U local extremes and coherent globals.
function run(){
 const assert=(x,m)=>{if(!x)throw Error("check failed "+m)};
 const W="-1 3 -14;2 -8 9;10 -13 14;3 7 -13;-4 -9 -11;5 8 -14;4 -8 -11;1 7 13;1 -7 10;-5 -6 -15;-2 -6 12;-4 9 -10;-2 5 -12;-3 6 -15;6 -7 11;2 -9 11;4 8 -10;-3 12 15;-5 -12 15;-1 13 14";
 const W1=W.split(";").map(s=>s.split(" ").map(Number));
 const W2=W1.map(c=>c.slice());W2[7][0]=-1;W2[19][0]=1;
 const tl=(l,a)=>((a>>>(Math.abs(l)-1))&1)===(l>0?1:0);
 const nv=F=>Math.max(...F.flat().map(Math.abs));
 const vals=(F,a)=>F.map(c=>c.reduce((z,l)=>z+Number(tl(l,a)),0));
 const hist=v=>[0,1,2,3].map(k=>v.filter(x=>x===k).length);
 const mk=(pi,b)=>{
   let m=pi.length,F=pi.map(v=>[v,m+v,2*m+v]),a=3*m+1,c=3*m+3,w=3*m+4,d=3*m+2;
   if(b==="SAT"){
    for(let i of [1,-1])for(let j of [1,-1])F.push([w,i*a,j*d]);
    for(let i of [1,-1])for(let j of [1,-1])F.push([w,i*a,j*c]);
   }else for(let i of [1,-1])for(let j of [1,-1])for(let k of [1,-1])F.push([i*a,j*d,k*c]);
   F.push([-w,a,d]);return F;
 };
 const count=F=>{let total=0,wit=null;for(let a=0;a<(1<<nv(F));a++){if(F.every(c=>c.some(l=>tl(l,a)))){total++;if(wit===null)wit=a}}return{models:total,witness:wit,enumerated:(1<<nv(F))}};
 const extremes=F=>F.map((c,j)=>({source_clause:j,literals:c,
   S_all_literals_true:c.map(l=>[Math.abs(l),l>0?1:0]),
   U_all_literals_false:c.map(l=>[Math.abs(l),l>0?0:1]),
   indexed_occurrences:c.map(l=>({indexed:"x_"+Math.abs(l)+","+j,signed:l,S:l>0?1:0,
     inverted_S_U:l>0?0:1,U:l>0?0:1,inverted_U_S:l>0?1:0}))}));
 const matrix=F=>{
   let out=[];
   for(let j=0;j<F.length;j++)for(let k=j+1;k<F.length;k++){
     let A=new Map(F[j].map(l=>[Math.abs(l),Math.sign(l)])),B=new Map(F[k].map(l=>[Math.abs(l),Math.sign(l)]));
     let same=[],opposite=[];
     for(let [v,s] of A)if(B.has(v))(B.get(v)===s?same:opposite).push(v);
     let X={SS:opposite.length===0,SU:same.length===0,US:same.length===0,UU:opposite.length===0};
     let vv=[...new Set(F[j].concat(F[k]).map(Math.abs))],seen={SS:false,SU:false,US:false,UU:false};
     for(let mask=0;mask<(1<<vv.length);mask++){
       let b=Object.fromEntries(vv.map((v,h)=>[v,(mask>>h)&1]));
       const t=c=>c.reduce((z,l)=>z+Number(b[Math.abs(l)]===(l>0?1:0)),0);
       let t1=t(F[j]),t2=t(F[k]);
       if(t1===3&&t2===3)seen.SS=true;
       if(t1===3&&t2===0)seen.SU=true;
       if(t1===0&&t2===3)seen.US=true;
       if(t1===0&&t2===0)seen.UU=true;
     }
     for(let z of ["SS","SU","US","UU"])assert(X[z]===seen[z],j+","+k+","+z);
     out.push({j,k,same,opposite,...X});
   }return out;
 };
 const trail=F=>{
   let n=nv(F),all=(1<<n)-1,steps=[0,1,3,7,all].map(a=>{
     let v=vals(F,a);return{assignment_mask:a,truth_counts:v,N0_to_N3:hist(v),SAT:v.every(z=>z>0)};
   });
   for(let st of steps){let vv=vals(F,st.assignment_mask^all);assert(vv.every((z,j)=>z===3-st.truth_counts[j]))}
   for(let i=0;i<2;i++){
     let a=steps[i].assignment_mask,b=steps[i+1].assignment_mask,jump=a^b;
     assert((jump&(jump-1))===0);
     let v=F.map((c,j)=>steps[i].truth_counts[j]+c.filter(l=>Math.abs(l)===Math.log2(jump)+1).reduce((z,l)=>z+(tl(l,a)?-1:1),0));
     assert(v.every((z,j)=>z===steps[i+1].truth_counts[j]));
   }
   return steps;
 };
 const DPLL=F=>{
   let z={nodes:0,source_clause_reads:0,source_literal_tests:0,units:0,branches:0,
     contradictions:0,accepted_models:0,terminal_source_clause_reads:0,terminal_source_literal_tests:0,
     variable_selection_clause_reads:0,variable_selection_literal_scans:0,assignment_state_copies:0};
   function rec(A){
     z.nodes++;
     while(true){
       let again=false;
       for(let c of F){
         z.source_clause_reads++;let sat=false,un=[];
         for(let l of c){z.source_literal_tests++;let v=Math.abs(l);
           if(A[v]===undefined)un.push(l);
           else if(A[v]===(l>0?1:0)){sat=true;break}
         }
         if(sat)continue;
         if(!un.length){z.contradictions++;return false}
         if(un.length===1){let l=un[0];A[Math.abs(l)]=l>0?1:0;z.units++;again=true;break}
       }
       if(!again)break;
     }
     let all=true;
     for(let c of F){
       z.terminal_source_clause_reads++;let sat=false;
       for(let l of c){z.terminal_source_literal_tests++;
         if(A[Math.abs(l)]!==undefined&&A[Math.abs(l)]===(l>0?1:0)){sat=true;break}}
       if(!sat){all=false;break}
     }
     if(all){z.accepted_models++;return true}
     let cand=new Set();
     for(let c of F){z.variable_selection_clause_reads++;
       for(let l of c){z.variable_selection_literal_scans++;
         if(A[Math.abs(l)]===undefined)cand.add(Math.abs(l))}}
     if(!cand.size)return false;
     let v=Math.min(...cand);
     for(let b of [0,1]){z.branches++;z.assignment_state_copies+=Object.keys(A).length;
       let B={...A};B[v]=b;if(rec(B))return true}
     return false;
   }
   let sat=rec({}),work=Object.entries(z).filter(([k])=>!["nodes","accepted_models","contradictions"].includes(k))
      .reduce((u,[,v])=>u+v,0);
   return{SAT:sat,selected_work:work,...z};
 };
 const permCases=[[1,2,3,4],[4,3,2,1],[2,4,1,3]],cases=[];
 for(let pi of permCases)for(let label of ["SAT","UNSAT"]){
   let F=mk(pi,label),M=count(F),D=DPLL(F);
   assert((M.models>0)===(label==="SAT")&&D.SAT===(label==="SAT"));
   let reads=0,answers=[];
   for(let v=1;v<=pi.length;v++){let j=pi.indexOf(v)+1;answers.push(j);reads+=j}
   cases.push({id:"permutation_"+pi.join("")+"_"+label,clauses:F,
     ground_truth:M,local_extremes:extremes(F),SS_SU_US_UU_matrix:matrix(F),
     coherent_global_endpoints_and_flips:trail(F),baseline_DPLL:D,
     inverse_queries:{answers,source_word_reads_restarted:reads,index_prepass_reads:pi.length,
     index_storage_bits:pi.length*Math.ceil(Math.log2(pi.length+1))},
     augmented_scan_work:D.selected_work+reads,augmented_index_work:D.selected_work+2*pi.length,
     learned_forbidden_cube:{source_clause:F[0],source_proof:"All three literals of original clause false prohibit the partial cube."}});
 }
 for(let [name,F] of [["W1_UNSAT",W1],["W1_signed_swap_SAT",W2]]){
   let M=count(F),D=DPLL(F);assert((M.models===0)===(name==="W1_UNSAT")&&D.SAT===(name!=="W1_UNSAT"));
   cases.push({id:name,clauses:F,ground_truth:M,local_extremes:extremes(F),
     SS_SU_US_UU_matrix:matrix(F),coherent_global_endpoints_and_flips:trail(F),baseline_DPLL:D});
 }
 const targets=[1413,1766271,1389,1764896,1397,1765503,22451,3202];
 assert(cases.every((x,i)=>x.baseline_DPLL.selected_work===targets[i]));
 const controls=[];
 function facfall(m,t){let v=1;for(let i=0;i<t;i++)v*=m-i;return v}
 function perms(m){
    let counts=new Map(),tvals=[...new Set([1,2,m])];
    function walk(a,rest){
      if(!rest.length){
        for(let t of tvals){let s=Array.from({length:t},(_,i)=>a.indexOf(i+1)+1).join(",");
          if(!counts.has(t))counts.set(t,new Set());counts.get(t).add(s)}
        return;
      }
      for(let v of rest)walk(a.concat(v),rest.filter(x=>x!==v));
    }
    walk([],Array.from({length:m},(_,i)=>i+1));
    for(let [t,set] of counts)assert(set.size===facfall(m,t));
    return counts;
 }
 for(let m=3;m<=7;m++){let p=perms(m);
   for(let t of [...new Set([1,2,m])])for(let s of [0,Math.ceil(Math.log2(m)),2*Math.ceil(Math.log2(m))]){
     let Q=0;while(2**s*m**Q<facfall(m,t))Q++;
     controls.push({m,t,s,Q,number_of_exact_inverse_answer_tuples:p.get(t).size});
   }
 }
 const proof=[],known=new Set(),sig=a=>a.slice().sort((x,y)=>Math.abs(x)-Math.abs(y)||x-y).join(",");
 for(let a of [-1,1])for(let b of [-1,1])for(let c of [-1,1])known.add(sig([a,2*b,3*c]));
 function resolve(L,R,p){
   assert(known.has(sig(L))&&known.has(sig(R))&&L.includes(p)&&R.includes(-p));
   let C=[...new Set(L.filter(x=>x!==p).concat(R.filter(x=>x!==-p)))];
   assert(C.every(x=>!C.includes(-x)));known.add(sig(C));
   proof.push({parent_left:L,parent_right:R,pivot:p,resolvent:C});
 }
 for(let a of [1,-1])for(let b of [1,-1])resolve([a,2*b,3],[a,2*b,-3],3);
 for(let a of [1,-1])resolve([a,2],[a,-2],2);
 resolve([1],[-1],1);assert(proof.length===7&&known.has(""));
 function d2(p,q){const gcd=(a,b)=>b?gcd(b,a%b):a;
   let P=BigInt(p),Q=BigInt(q),a=2n*Q**3n+P*Q**2n-P**3n,b=2n*P**2n*Q,g=gcd(a,b);
   return (a/g)+"/"+(b/g);
 }
 assert(d2(6,5)==="23/45"&&d2(241,200)==="11642479/23232400");
 let nChecks=cases.reduce((s,x)=>s+x.ground_truth.enumerated,0);
 let pairChecks=cases.reduce((s,x)=>s+4*x.SS_SU_US_UU_matrix.length,0);
 assert(nChecks===458752&&pairChecks===3392);
 return {run_id:"LSPV4_ARC_SOURCE_PROBE_TRANSCRIPT257",status:"PASS restricted exact interface; computational hostile controls; arbitrary-A ARC and P versus NP OPEN",
   theorem:"2^s m^Q >= m!/(m-t)!",
   FLMV:{d_star_6_5:d2(6,5),d_star_241_200:d2(241,200),optimal_index:2,
     infinite_tail:"For c>=6/5, d1<=7/15, d3<=401/810, and k>=4 has d_k<= (5/6)^4 <1/2; d2 exceeds 1/2 at both selected c."},
   resolution_unsat_proof:proof,permutation_transcript_controls:controls,
   checks:{source_assignment_enumerations:nChecks,SS_SU_US_UU_pair_modes:pairChecks,
     resolution_steps:7,source_cases:cases.length},cases,
   limitations:"Indexed word logical operations not physical FLMV tape instructions. Inverse-interface restrictions do not imply general SAT hardness. No all-input power-short Phi."};
}
if(typeof process!=="undefined"&&process.stdout)process.stdout.write(JSON.stringify(run(),null,2)+"\n");
