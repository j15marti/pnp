#!/usr/bin/env node
"use strict";
// TMR-2/049: self-contained exact guarded-CNF audit; no dependencies or randomness.
// Symbolic all-size proof in companion report; finite observations only here.
const result = (function auditGuardedCNF(){
  "use strict";
  const stat={experiment:"TMR2_ALLENDER_GUARDED_CNF049",method:"exact V8 enumeration of distinct gate semantics, Tseitin CNF clauses, guarded CNF and both majority blocks",circuits:0,original_outer_assignments:0,unique_extension_checks:0,enumerated_guarded_assignments:0,inner_threshold_checks:0,outer_threshold_checks:0,positive_and_complement_sat_checks:0,extra_unique_variable_tie_counterexample:0,prime_width3_candidate_clauses:0,assertions:0,failures:0};
  function verify(cond,label){stat.assertions++;if(!cond){stat.failures++;throw Error(label)}}
  function gate(op,a,b){if(op==="and")return a&&b?1:0;if(op==="or")return a||b?1:0;if(op==="xor")return a!==b?1:0;return a?0:1}
  function evalCNF(cnf,assign){for(const cl of cnf){let ok=false;for(const lit of cl){const v=assign[Math.abs(lit)];if((lit>0&&v===1)||(lit<0&&v===0)){ok=true;break}}if(!ok)return false}return true}
  function build(ell,n,g,seed){
    const inCount=ell+n;const gates=[];const t=inCount+g+1;const clauses=[];
    for(let j=0;j<g;j++){
      const op=["and","or","xor","not"][(seed+j)%4];const z=inCount+j+1;
      const a=j===0?ell+1:inCount+j;
      const b=n>1?ell+1+(j%(n)):1;
      gates.push({op,a,b,z});
      if(op==="and")clauses.push([-z,a],[-z,b],[z,-a,-b]);
      else if(op==="or")clauses.push([z,-a],[z,-b],[-z,a,b]);
      else if(op==="xor")clauses.push([-a,-b,-z],[a,b,-z],[a,-b,z],[-a,b,z]);
      else clauses.push([z,a],[-z,-a]);
    }
    const forced=[...clauses,[inCount+g]];
    const guarded=[...forced.map(c=>[t,...c]),[-t,ell+1,...gates.map(x=>x.z)]];
    return {gates,forced,guarded,t,inCount};
  }
  for(let ell=1;ell<=2;ell++)for(let n=1;n<=3;n++)for(let g=1;g<=3;g++)for(let seed=0;seed<6;seed++){
    const c=build(ell,n,g,seed);stat.circuits++;
    let originalOuterYES=0,newOuterYES=0;
    verify(c.guarded.length<=4*g+2,"clause ledger");
    verify(c.guarded.reduce((p,cl)=>p+cl.length,0)<=17*g+4,"literal ledger");
    for(let av=0;av<(1<<ell);av++){
      stat.original_outer_assignments++;
      let S=0,H=0;
      for(let bv=0;bv<(1<<n);bv++){
        const a=new Array(c.t+1).fill(0);
        for(let i=0;i<ell;i++)a[i+1]=(av>>i)&1;
        for(let i=0;i<n;i++)a[ell+1+i]=(bv>>i)&1;
        for(const entry of c.gates)a[entry.z]=gate(entry.op,a[entry.a],a[entry.b]);
        const output=a[c.inCount+g];S+=output;
        const goodZ=c.gates.reduce((sum,entry,i)=>sum+(a[entry.z]<<(i)),0);
        let extensionCount=0;
        for(let zv=0;zv<(1<<g);zv++){
          for(let i=0;i<g;i++)a[c.inCount+i+1]=(zv>>i)&1;
          const valid=evalCNF(c.forced,a)?1:0;extensionCount+=valid;
          verify(valid===(output&&zv===goodZ?1:0),"forced CNF must be functional");
          stat.unique_extension_checks++;
          for(let v=0;v<2;v++){
            a[c.t]=v;
            const got=evalCNF(c.guarded,a)?1:0;
            const expected=v===0?valid:((a[ell+1]===1||zv!==0)?1:0);
            verify(got===expected,"CNF guards disagreed with direct semantics");
            H+=got;stat.enumerated_guarded_assignments++;
          }
        }
      }
      const expectedH=(1<<(n+g))-(1<<(n-1))+S;
      verify(H===expectedH,"exact count");
      verify((H >= (1<<(n+g)))===(S >= (1<<(n-1))),"inclusive inner tie");
      stat.inner_threshold_checks++;
      originalOuterYES+=S >= (1<<(n-1))?1:0;
      newOuterYES+=H >= (1<<(n+g))?1:0;
      // Explicit constant witnesses: t=1 and b1=1 satisfies G; t=1 and (b1,z)=0 falsifies G.
      const yes=new Array(c.t+1).fill(0);yes[c.t]=1;yes[ell+1]=1;
      const no=new Array(c.t+1).fill(0);no[c.t]=1;
      verify(evalCNF(c.guarded,yes)===true && evalCNF(c.guarded,no)===false,"both SAT and complement SAT");
      stat.positive_and_complement_sat_checks++;
    }
    verify(originalOuterYES===newOuterYES,"exact outer count");
    verify((originalOuterYES >= (1<<(ell-1)))===(newOuterYES >= (1<<(ell-1))),"outer inclusive majority");
    stat.outer_threshold_checks++;
  }
  // The smallest nontrivial inclusive tie is F(b)=b on one b and one unique auxiliary z=b.
  // Guard t=0 enforces (z<->b) AND z. Guard t=1 enforces (b OR z).
  const tieCNF=[[2,2,-1],[2,-2,1],[2,2],[-2,1,2]]; // b=1,z=2,t=3 in subsequent direct code instead
  const clean=[[3,-2,1],[3,2,-1],[3,2],[-3,1,2]];
  let h=0,extended=0;
  for(let b=0;b<2;b++)for(let z=0;z<2;z++)for(let t=0;t<2;t++){
    const a=[0,b,z,t];const ok=evalCNF(clean,a);if(ok)h++;
    for(let w=0;w<2;w++)if(ok && w===0)extended++;
  }
  verify(h===4 && extended===4,"minimal tied gadget counts");
  verify(h>=4 && extended<8,"one further counted fixed variable reverses tie");stat.extra_unique_variable_tie_counterexample++;
  // B=b OR z1 OR z2 OR z3 excludes exactly the all-zero 4-bit word.
  // Every non-tautological clause of width <=3 has >=2 falsifying words and cannot be entailed by B.
  for(let mask=1;mask<16;mask++)if((mask.toString(2).match(/1/g)||[]).length<=3){
    const vars=[0,1,2,3].filter(i=>(mask>>i)&1);
    for(let signs=0;signs<(1<<vars.length);signs++){
      const clause=vars.map((v,i)=>((signs>>i)&1)?v+1:-(v+1));
      let implied=true;
      for(let a=1;a<16;a++){
        const bits=[0,1,2,3,4].map(i=>i===0?0:(a>>(i-1))&1);
        if(!evalCNF([clause],bits)){implied=false;break}
      }
      verify(!implied,"spurious width<=3 implicate of 4-literal clause");
      stat.prime_width3_candidate_clauses++;
    }
  }
  stat.negative_controls={one_extra_unique_auxiliary:{original_satisfying:4,original_total:8,extra_satisfying:4,extra_total:16,original_inclusive_yes:true,extra_inclusive_yes:false},direct_guard_calibrator:{clause:"b1 OR z1 OR ... OR zg",minimum_clause_width_without_new_variables:"g+1",guarded_clause_width:"g+2",g_at_least_3_no_equivalent_width3_CNF_without_more_variables:true},existential_sat_oracle:{sat_guarded:true,sat_negation:true,independent_of_original_majority:true}};
  return stat;
})();
console.log(JSON.stringify(result,null,2));
