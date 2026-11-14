"use strict";
// TMR-4/017: independently executed V8 physical mock-machine controls.
function verify(ok,msg){if(!ok)throw Error(msg);}

function referenceLabel(bits){
  if(bits.length%3!==0)return "MALFORMED";
  let clauses=[];for(let i=0;i<bits.length;i+=3)clauses.push(parseInt(bits.slice(i,i+3),2));
  for(let a=0;a<8;a++)if(!clauses.includes(a))return "SAT";
  return "UNSAT";
}

function physicalTrace(bits,haltAt,erase){
  const L=bits.length,q=L+1;let p=0,time=0,parity=0,mask=0,part=0,mod=0,reads=0;
  while(p<q){
    if(p>=1&&p<=L){
      const bit=Number(bits[p-1]);verify(bit===0||bit===1,"not binary");
      reads++;parity^=bit;part=part*2+bit;mod++;
      if(mod===3){mask|=1<<part;part=0;mod=0;}
    }
    p++;time++;
  }
  verify(p===q&&reads===L,"outward sweep");
  const label=mod?"MALFORMED":mask===255?"UNSAT":"SAT";
  while(p>0){p--;time++;}
  verify(p===0,"first reset");
  let halted=haltAt===0,mSteps=0;
  p=1;time++;
  while(p<=L){
    if(!halted){mSteps++;if(haltAt!==null&&mSteps>=haltAt)halted=true;}
    p++;time++;
  }
  verify(p===q,"simulation sweep");
  while(p>0){p--;time++;}
  verify(p===0&&time===4*q,"pre-gate count");
  let detour=false;
  if(!erase&&halted&&parity===1){
    detour=true;while(p<q){p++;time++;}while(p>0){p--;time++;}
  }
  verify(p===0,"finish at source origin");
  time++;
  return {label,parity,halted,detour,reads,time,mSteps,peakWritableCells:0};
}

function experiment(){
  const limits=[null,0,1,3,7,11],per={},hist={SAT:0,UNSAT:0,MALFORMED:0};
  let tested=0,charged=0,detours=0,omitted=0;
  for(const haltAt of limits){
    const key=haltAt===null?"NEVER":"HALT_"+haltAt;
    const st={cases:0,detours:0,omitted:0,SAT:0,UNSAT:0,MALFORMED:0};
    for(let L=0;L<=11;L++){
      for(let z=0;z<2**L;z++){
        const bits=L===0?"":z.toString(2).padStart(L,"0");
        const real=physicalTrace(bits,haltAt,false),erased=physicalTrace(bits,haltAt,true);
        const expected=referenceLabel(bits),h=haltAt!==null&&haltAt<=L;
        const delta=2*(L+1)*Number(h&&real.parity===1);
        verify(real.label===expected&&erased.label===expected,"label");
        verify(real.halted===h&&erased.halted===h,"bounded simulation");
        verify(real.parity===(bits.split("1").length-1)%2,"parity");
        verify(real.reads===L&&erased.reads===L,"current-cell read count");
        verify(real.time-erased.time===delta&&erased.time===4*(L+1)+1,"exact time delta");
        verify(real.peakWritableCells===0,"finite mock M work space");
        st.cases++;st.detours+=Number(real.detour);st.omitted+=delta;st[expected]++;
        hist[expected]++;tested++;charged+=real.time+erased.time;detours+=Number(real.detour);omitted+=delta;
      }
    }
    per[key]=st;
  }
  const signed={
    unsat8:[0,1,2,3,4,5,6,7],unsat9Odd:[0,1,2,3,4,5,6,7,1],
    sat8:[0,1,2,3,4,5,6,6],sat9Even:[0,1,2,3,4,5,6,6,1]
  };
  const controls={};
  for(const [name,rows] of Object.entries(signed)){
    const bits=rows.map(x=>x.toString(2).padStart(3,"0")).join("");
    const a=physicalTrace(bits,7,false),b=physicalTrace(bits,7,true);
    verify(a.label===referenceLabel(bits)&&a.label!=="MALFORMED","valid CNF labels");
    verify(a.time-b.time===2*(bits.length+1)*a.parity,"valid CNF delta");
    controls[name]={L:bits.length,label:a.label,parity:a.parity,realSteps:a.time,erasedSteps:b.time};
  }
  return {experiment:"TMR4/017_uniform_gate_cost_exactness_undecidability_finite_controls",
    status:"COMPUTATIONAL",model:"one locally moving source head, fixed finite-state bounded-simulation mock M",
    exhaustive:{lengths:"0..11",fixtures:limits,sourceProgramPairs:tested,chargedStepsBoth:charged,realDetours:detours,omittedTransitions:omitted,labels:hist,perFixture:per},
    controls,seed:null,failedAssertions:0,
    limitation:"finite halt-after and never-halt fixtures are not a universal arbitrary-M compiler; undecidability follows separately by reduction from halting"};
}

if (typeof module !== "undefined" && require.main === module) console.log(JSON.stringify(experiment(),null,2));
