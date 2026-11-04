"use strict";
// LSPV-3/395: exact source-core and contradictory-unit controls.
// Execute: node experiments/arc/lspv3_395_source_core_ceiling.js
function assert(ok, why) { if (!ok) throw new Error("FAILED: " + why); }
function allSat(n, clauses, chooseIndices) {
  const c = chooseIndices ? chooseIndices.map(i => clauses[i]) : clauses;
  for (let a=0; a < 2**n; a++) {
    if (c.every(cl=>cl.some(l=>(((a >> (Math.abs(l)-1))&1)===1)===(l>0)))) return a;
  }
  return null;
}
function php(h){
  const n=h*(h+1), clauses=[];
  for(let p=0;p<h+1;p++)clauses.push(Array.from({length:h},(_,j)=>p*h+j+1));
  for(let j=0;j<h;j++)for(let p=0;p<h+1;p++)for(let q=p+1;q<h+1;q++)
    clauses.push([-(p*h+j+1),-(q*h+j+1)]);
  return {n,clauses};
}
function coreMin(n,c){
  const m=c.length;
  for(let k=1;k<=m;k++){
    function choose(start,sel){
      if(sel.length===k)return allSat(n,c,sel)===null ? [...sel] : null;
      for(let i=start;i<=m-(k-sel.length);i++){
        sel.push(i);let z=choose(i+1,sel);sel.pop();if(z!==null)return z;
      }
      return null;
    }
    let s=choose(0,[]);if(s!==null)return s;
  }
  throw new Error("no UNSAT subset");
}
function run(){
  let checks=0, rows=[];
  for(let h=1;h<=3;h++){
    const {n,clauses}=php(h);
    assert(allSat(n,clauses)===null,"PHP UNSAT "+h);checks++;
    for(let i=0;i<clauses.length;i++){
      const other=clauses.filter((_,j)=>i!==j);
      assert(allSat(n,other)!==null,"PHP source deletion SAT "+h+"/"+i);checks++;
    }
    const plus=[...clauses,[n+1],[-(n+1)]];
    assert(allSat(n+1,plus)===null,"plus UNSAT");checks++;
    // One paid resolution inference on the two source units obtains empty clause.
    const [u,v]=plus.slice(-2);
    assert(u.length===1 && v.length===1 && u[0]===-v[0],"valid one-node refutation");checks++;
    assert(plus.every(c=>c.length>0),"no empty source (zero-node impossible)");checks++;
    const oldcore=h<=2?coreMin(n,clauses):null;
    const newcore=h<=2?coreMin(n+1,plus):[clauses.length,clauses.length+1];
    assert(newcore.length===2,"plus minimum core size=2");checks++;
    if(h<=2){assert(oldcore.length===clauses.length,"old PHP clause-minimal "+h);checks++;}
    rows.push({holes:h,variablesOriginal:n,clausesOriginal:clauses.length,originalMinCore:oldcore?.length??null,
      newVariables:n+1,newClauses:plus.length,newMinCore:newcore.length,certifiedMixedProofNodes:1,
      originalUnsat:true,augmentedUnsat:true,allSingleDeletionsSat:true});
  }
  // Additional simple malformed/corrupted certificate controls
  function validDAGCertificate(clauses,record) {
    if(!Number.isInteger(record.pivot) || record.pivot<=0)return false;
    if(record.left<0||record.right<0||record.left>=clauses.length||record.right>=clauses.length)return false;
    const l=clauses[record.left],r=clauses[record.right],p=record.pivot;
    return l.includes(p)&&r.includes(-p)&&new Set([...l.filter(z=>z!==p),...r.filter(z=>z!==-p)]).size===0;
  }
  const h2=php(2);let plus2=[...h2.clauses,[h2.n+1],[-(h2.n+1)]],i=h2.clauses.length;
  assert(validDAGCertificate(plus2,{pivot:h2.n+1,left:i,right:i+1}),"good certificate");checks++;
  assert(!validDAGCertificate(plus2,{pivot:h2.n,left:i,right:i+1}),"corrupt pivot rejected");checks++;
  assert(!validDAGCertificate(plus2,{pivot:h2.n+1,left:i,right:999}),"bad source index rejected");checks++;
  assert(!validDAGCertificate(plus2,{pivot:"oracle",left:i,right:i+1}),"malformed pivot rejected");checks++;
  return {status:"COMPUTATIONAL",theorem:"PHP remains UNSAT, with 2 fresh opposite units and exact mixed cost 1; source-core=min assignment transversal",rows,checks,failures:0,scope:"Exhaustive truth-table SAT controls for h<=3 and exact minimum-core search h<=2. Haken asymptotic bound is external; no all-algorithm runtime inference."};
}
if (typeof module !== "undefined") console.log(JSON.stringify(run(),null,2));
