/* Reproducible LSPV-4 finite controls: deterministic, no external dependencies. */
function run(){
 const W1=[[-1,3,-14],[2,-8,9],[10,-13,14],[3,7,-13],[-4,-9,-11],[5,8,-14],[4,-8,-11],[1,7,13],[1,-7,10],[-5,-6,-15],[-2,-6,12],[-4,9,-10],[-2,5,-12],[-3,6,-15],[6,-7,11],[2,-9,11],[4,8,-10],[-3,12,15],[-5,-12,15],[-1,13,14]];
 const S15=[[-1,-3,14],[2,8,-9],[-10,13,14],[3,-7,-13],[-4,9,-11],[-5,-8,-14],[4,-8,11],[1,7,-13],[1,-7,10],[-5,-6,15],[-2,6,-12],[4,9,-10],[-2,5,-12],[3,6,-15],[-6,7,11],[2,-9,-11],[-4,8,10],[-3,12,15],[5,12,-15],[-1,13,-14]];
 const xorSat=[[-1,-2,3],[-1,2,-3],[1,-2,-3],[1,2,3]];
 const xorUnsat=[...xorSat,[-1,-2,-3],[-1,2,3],[1,-2,3],[1,2,-3]];
 const cases=[["W1_UNSAT",W1],["S15_SAT",S15],["XOR3_SAT",xorSat],["XOR3_UNSAT",xorUnsat],["HORN_SAT",[[1,2,3],[-1,2,3]]],["HORN_UNSAT",[[1,2,3],[-1,2,-3],[1,-2,-3],[-1,-2,3],[-1,2,3],[1,-2,3],[1,2,-3],[-1,-2,-3]]]];
 function maxvar(F){return Math.max(0,...F.flat().map(Math.abs))}
 function bitval(mask,v){return (mask>>(v-1))&1}
 function litval(l,mask){let b=bitval(mask,Math.abs(l));return l>0?b:1-b}
 function count(C,mask){return C.reduce((z,l)=>z+litval(l,mask),0)}
 function status(F,mask){return F.map(C=>count(C,mask))}
 function sat(F,mask){return status(F,mask).every(x=>x!==0)}
 function target(C,mode){return C.map(l=>({variable:Math.abs(l),literal:l,source_index:undefined,value:(l>0)===(mode==="S")?1:0}))}
 function pairModes(C,D){
    let out={};for(const a of ["S","U"])for(const b of ["S","U"]){let m=new Map(),ok=true;for(const [c,k] of [[C,a],[D,b]])for(const t of target(c,k)){if(m.has(t.variable)&&m.get(t.variable)!==t.value)ok=false;m.set(t.variable,t.value)}
       let vars=[...new Set([...C,...D].map(Math.abs))];let found=false;for(let x=0;x<(1<<vars.length);x++){let sub=0;for(let j=0;j<vars.length;j++)if((x>>j)&1)sub|=1<<(vars[j]-1);if((a==="S"?count(C,sub)===C.length:count(C,sub)===0)&&(b==="S"?count(D,sub)===D.length:count(D,sub)===0)){found=true;break}}
       if(found!==ok)throw Error("pair mismatch");
       out[a+b]=ok;
    }return out
 }
 function dpll(F,n){
    let nodes=0,literal_tests=0,clause_visits=0,forced=0,branches=0;
    function dfs(asg){
      nodes++;const a=asg.slice();
      while(true){let change=false,all=true;
       for(const C of F){clause_visits++;let yes=false,unknown=[];
         for(const l of C){literal_tests++;const v=a[Math.abs(l)];if(v===-1)unknown.push(l);else if((l>0&&v===1)||(l<0&&v===0)){yes=true;break}}
         if(yes)continue; all=false;if(unknown.length===0)return null;
         if(unknown.length===1){const l=unknown[0],i=Math.abs(l),val=l>0?1:0;if(a[i]!==-1&&a[i]!==val)return null;if(a[i]===-1){a[i]=val;forced++;change=true}}
       }
       if(!change){if(all)return a;break;}
      }
      let v=0;for(let i=1;i<=n;i++)if(a[i]===-1){v=i;break}if(!v)return a;
      branches++;for(const x of [0,1]){const b=a.slice();b[v]=x;let ret=dfs(b);if(ret)return ret}
      return null;
    }
    const witness=dfs(Array(n+1).fill(-1));
    if(Boolean(witness)!==Boolean(witness&&sat(F,witness.reduce((m,v,i)=>v===1?m|(1<<(i-1)):m,0))))throw Error("bad DPLL witness");
    return {sat:!!witness,nodes,branches,forced,clause_visits,literal_tests,work:clause_visits+literal_tests+branches+forced,witness:witness?witness.slice(1):null}
 }
 function firstResolution(F,n){for(let v=1;v<=n;v++){for(let i=0;i<F.length;i++)if(F[i].includes(v))for(let j=0;j<F.length;j++)if(F[j].includes(-v)){let R=[...new Set([...F[i].filter(x=>x!==v),...F[j].filter(x=>x!==-v)])];if(R.some(x=>R.includes(-x)))continue;for(let a=0;a<(1<<n);a++)if(sat(F,a)&&R.every(x=>litval(x,a)===0))throw Error("bad resolvent");return {pivot:v,clause_indices:[i+1,j+1],resolvent:R,forbidden_cube:R.map(x=>({variable:Math.abs(x),value:x>0?0:1})),proof_rule:"binary resolution on pivot"}}}return null}
 function gcd(a,b){a=a<0n?-a:a;b=b<0n?-b:b;while(b){let r=a%b;a=b;b=r;}return a}
 function Q(a,b=1n){a=BigInt(a);b=BigInt(b);if(b<0n){a=-a;b=-b;}let g=gcd(a,b);return [a/g,b/g]}
 function plus(x,y){return Q(x[0]*y[1]+y[0]*x[1],x[1]*y[1])}
 function neg(x){return [-x[0],x[1]]}
 function minus(x,y){return plus(x,neg(y))}
 function mul(x,y){return Q(x[0]*y[0],x[1]*y[1])}
 function div(x,y){return Q(x[0]*y[1],x[1]*y[0])}
 function lt(x,y){return x[0]*y[1]<y[0]*x[1]}
 function st(x){return String(x[0])+"/"+String(x[1])}
 function flmv(num,den){
    let c=Q(num,den),one=Q(1n),f=one,check=[],best=Q(-1n);
    for(let k=1;k<=200;k++){
       f=div(mul(c,f),plus(one,f));let xx=div(minus(div(one,f),c),Q(k));let yy=one;for(let j=0;j<k;j++)yy=div(yy,c);
       let d=lt(xx,yy)?xx:yy;check.push({k,d:st(d)});if(lt(best,d))best=d;
       let tail=div(yy,c);if(lt(tail,best)&&k>=3) return {c:st(c),max:st(best),max_k:check.find(x=>x.d===st(best)).k,checked:check,tail_bound:st(tail),strict:lt(tail,best)};
    }throw Error("uncertified tail")
 }
 function cm2(program,n){
    let pc=0,c=[0,0],steps=0;for(;steps<n;steps++){if(pc<0||pc>=program.length)return {halted:true,steps,registers:c};let ins=program[pc];if(ins[0]==="inc"){c[ins[1]]++;pc++;}else if(c[ins[1]]===0)pc++;else{c[ins[1]]--;pc=ins[2];}}
    return {halted:pc<0||pc>=program.length,steps,registers:c};
 }
 let finitePrograms=[
    ["HALT_4",Array.from({length:4},()=>["inc",0])],
    ["HALT_40",Array.from({length:40},()=>["inc",0])],
    ["LOOP",[["inc",0],["dec",0,0]]]
 ];
 let profiles=[];for(const [name,prog]of finitePrograms)for(const n of [2,4,8,16,32,64]){let r=cm2(prog,n);profiles.push({name,n,halted:r.halted,simulated_steps:r.steps,dummy_steps:r.halted?0:n**3,state_bits_upper:2*Math.ceil(Math.log2(n+1))+Math.ceil(Math.log2(prog.length+1))+10})}
 let out={run:"ARC-EXPONENT-SELECTOR263",time:"2026-10-30 21:36 America/Los_Angeles",status:"PROVED/EXACT conditional undecidability reduction; finite COMPUTATIONAL; ARC OPEN",flmv:[flmv(6n,5n),flmv(241n,200n)],profiles,formulae:[],finite_assertions:0};
 for(let [name,F] of cases){
   let n=maxvar(F),all=(1<<n)-1,models=0,counts=[0,0,0,0],comps=0;
   for(let a=0;a<(1<<n);a++){let t=status(F,a),u=status(F,all^a);for(let j=0;j<t.length;j++){if(t[j]+u[j]!==3)throw Error("complement");comps++;}if(t.every(v=>v>0))models++;}let d=dpll(F,n);if((models>0)!==d.sat)throw Error("DPLL ground truth");
   const pair=[];for(let i=0;i<F.length;i++)for(let j=i+1;j<F.length;j++){pair.push({clause_indices:[i+1,j+1],modes:pairModes(F[i],F[j])})}
   const targets=F.map((C,j)=>({clause_index:j+1,occurrences:C.map((l,h)=>({occurrence:[Math.abs(l),j+1,h+1],literal:l,S:l>0?1:0,invert_S:l>0?0:1,U:l>0?0:1,invert_U:l>0?1:0})),S:target(C,"S"),U:target(C,"U")}));
   let trail=[0,1,3,all^3,all].map(a=>({assignment:a,counts:status(F,a),satisfied:sat(F,a)}));
   const r=firstResolution(F,n);let pairchecks=pair.length*4;
   out.finite_assertions+=comps+pairchecks;
   out.formulae.push({name,n,m:F.length,clauses:F,models,baseline_dpll:d,endpoint_zero:status(F,0),endpoint_one:status(F,all),flip_trail:trail,targets,pair_compatibility:pair,proven_forbidden_cube:r,source_clause_probes_for_two_endpoints:6*F.length,pair_mode_comparisons:pairchecks,diagnostic_selected_work_estimate:d.work+6*F.length+9*pair.length,complement_checks:comps});
 }
 if(out.flmv[0].max!=="23/45"||out.flmv[1].max!=="11642479/23232400")throw Error("FLMV fraction mismatch");
 if(out.formulae[0].models!==0||out.formulae[1].models!==861)throw Error("W1/S15 mismatch");
 return out
}
console.log(JSON.stringify(run(),null,2));
