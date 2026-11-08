'use strict';
function truthLit(lit,bits){const b=(bits>>>(Math.abs(lit)-1))&1;return lit>0?b===1:b===0;}
function allSat(clauses,bits){return clauses.every(cl=>cl.some(lit=>truthLit(lit,bits)));}
const clauses=[];for(let k=0;k<8;k++)clauses.push([1,2,3].map((id,j)=>(k&(1<<j))?-id:id));
const res={formulas:0,original_assignments:0,projected_branches:0,auxiliary_trials:0,sat:0,unsat:0,guard_clause_count:0,flipped_signed_clause_rejections:0};
for(let mask=0;mask<256;mask++){
 const F=clauses.filter((_,k)=>(mask>>>k)&1),m=F.length,z=4+m,G=[];
 F.forEach((cl,i)=>{const a=4+i;G.push([cl[0],cl[1],a],[-a,cl[2],z]);});
 if(!G.every(cl=>new Set(cl.map(Math.abs)).size===3))throw Error('nonproper');
 res.guard_clause_count+=G.length;let fsat=false;
 for(let x=0;x<8;x++){const fval=allSat(F,x);fsat=fsat||fval;res.original_assignments++;
   for(let zb=0;zb<2;zb++){let seen=false;
      for(let ab=0;ab<(1<<m);ab++){const word=x|(ab<<3)|(zb<<(z-1));res.auxiliary_trials++;if(allSat(G,word))seen=true;}
      if(seen!==(Boolean(zb)||fval))throw Error('bad projection '+mask+' '+x+' '+zb);
      res.projected_branches++;
   }
 }
 if(fsat!==(mask!==255))throw Error('wrong SAT '+mask);
 res[fsat?'sat':'unsat']++;res.formulas++;
}
const F=[[1,2,3]],broken=[[1,2,4],[-4,3,-5]];let bad=false;
for(let x=0;x<8;x++)for(let z=0;z<=1;z++){let exists=false;for(let a=0;a<=1;a++)exists ||=allSat(broken,x|(a<<3)|(z<<4));if(exists!==(Boolean(z)||allSat(F,x)))bad=true;}
if(!bad)throw Error('mutation not detected');res.flipped_signed_clause_rejections++;
res.status='PASS';res.native_FLMV_simulated=false;
console.log(JSON.stringify(res,null,2));
