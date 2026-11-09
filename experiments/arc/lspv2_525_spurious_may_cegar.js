// LSPV-2/525: independently replayable spurious MAY transition and RUP CEGAR repair.
// Native source clauses (a|b|c),(a|~b|c),(a|b|~c),(a|~b|~c).
'use strict';
const F = [[1,2,3],[1,-2,3],[1,2,-3],[1,-2,-3]];
function check(x,m){if(!x)throw Error(m)}
function resolvent(a,b,p){
  check(a.includes(p)&&b.includes(-p),'bad pivot');
  const out=[...new Set([...a.filter(x=>x!==p),...b.filter(x=>x!==-p)])];
  check(out.every(x=>!out.includes(-x)),'tautological inference');return out;
}
function rup(clauses,clause){
 const asgn=new Map();
 for(const lit of clause){let x=-lit;if(asgn.has(Math.abs(x))&&asgn.get(Math.abs(x))!==(x>0))return true;asgn.set(Math.abs(x),x>0)}
 while(true){let changed=false;
 for(const c of clauses){let sat=false,unit=[];
   for(const lit of c){const val=asgn.get(Math.abs(lit));if(val===undefined)unit.push(lit);else if(val===(lit>0)){sat=true;break}}
   if(sat)continue;if(unit.length===0)return true;
   if(unit.length===1){asgn.set(Math.abs(unit[0]),unit[0]>0);changed=true;break}
 }
 if(!changed)return false;
 }
}
const r1=resolvent(F[0],F[1],2);
const r2=resolvent(F[2],F[3],2);
const r3=resolvent(r1,r2,3);
check(JSON.stringify(r1)==='[1,3]'&&JSON.stringify(r2)==='[1,-3]'&&JSON.stringify(r3)==='[1]','valid three-node abstract Resolution block');
check(!rup(F,[1]),'abstract cost-one a must fail concrete RUP replay');
check(!rup(F,[]),'SAT source must reject false refutation');
check(rup([[1],[-1]],[]),'genuine RUP empty must be retained');
let satAssignments=0;
for(let mask=0;mask<8;mask++){
 const valid=F.every(c=>c.some(l=>(((mask>>(Math.abs(l)-1))&1)===1)===(l>0)));
 if(valid)satAssignments++;
}
check(satAssignments===4,'source exactly forces a=1');
console.log(JSON.stringify({status:'COMPUTATIONAL',originalClauses:4,variables:3,resolutionNodes:3,abstractCost:1,abstractExport:r3,sourceModels:satAssignments,rupExport:false,rupEmpty:false,genuineRupEmpty:true,refinement:'require an authenticated UP/RUP trail before accepting an abstract learned-clause transition'},null,2));
