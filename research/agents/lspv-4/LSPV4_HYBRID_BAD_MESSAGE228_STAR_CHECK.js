/* LSPV-4 HYBRID-BAD-MESSAGE228: independently executable finite hostile controls.
 * Tested with JavaScript ECMAScript 2022. These tests do not prove the asymptotic theorem.
 * This compact GitHub reproducer supplements the full Python/JSON local bundle.
 */
function tuples(s) {
  const out=[];
  for(let mask=0;mask<(1<<s);mask++){
    const a=[];for(let j=0;j<s;j++)a.push((mask>>j)&1);
    out.push(a);
  }
  return out;
}
function has2CNF(s,rel) {
  const allowed=tuples(s);
  const clauses=[];
  for(let i=0;i<s;i++)for(let sign=0;sign<2;sign++)
    clauses.push([[i,sign]]);
  for(let i=0;i<s;i++)for(let j=i+1;j<s;j++)
    for(let a=0;a<2;a++)for(let b=0;b<2;b++)
      clauses.push([[i,a],[j,b]]);
  if(rel.length===0)return true; // empty clause
  const valid=clauses.filter(c=>rel.every(x=>c.some(([i,v])=>x[i]===v)));
  return allowed.every(x=>(valid.every(c=>c.some(([i,v])=>x[i]===v))) ===
    rel.some(y=>y.every((v,i)=>x[i]===v)));
}
function star(q,h,beta){
  const n=2*q+3*h;
  let witness=null, solutions=0, bruteChecks=0;
  for(let mask=0;mask<(1<<n);mask++){
    bruteChecks++;
    let ok=true,center=0;
    for(let i=0;i<q;i++){
      const x=(mask>>(2*i))&1,y=(mask>>(2*i+1))&1;
      if((x^y)!==0){ok=false;break;}
      center^=x^y;
    }
    if(!ok)continue;
    for(let j=0;j<h;j++){
      const t=2*q+3*j;
      const x=(mask>>t)&1,y=(mask>>(t+1))&1,z=(mask>>(t+2))&1;
      if((x^y^z)!==1){ok=false;break;}
      center^=x^y^z;
    }
    if(ok && center===beta) {
      solutions++;
      if(witness===null)witness=mask;
    }
  }
  const expected=beta===(h%2);
  if((witness!==null)!==expected)throw Error("star mismatch "+[q,h,beta]);
  return {q,h,beta,expected,bruteChecks,solutions,unionBits:3*h,fullInterface:2*q+3*h};
}
function audit(){
  let relCount=0,ternaryRecognized=0,binaryRecognized=0;
  for(let s=0;s<=3;s++){
    const rows=tuples(s);
    for(let mask=0;mask<(1<<rows.length);mask++){
      const rel=rows.filter((_,i)=>((mask>>i)&1)===1);
      const yes=has2CNF(s,rel);
      relCount++;
      if(s===2&&yes)binaryRecognized++;
      if(s===3&&yes)ternaryRecognized++;
    }
  }
  if(relCount!==278||binaryRecognized!==16||ternaryRecognized!==166)
    throw Error("2CNF recognition count mismatch");
  const stars=[];
  for(let q=1;q<=4;q++)for(let h=0;h<=2;h++)
    for(let beta=0;beta<=1;beta++)stars.push(star(q,h,beta));
  if(stars.length!==24)throw Error("star case count");
  // Two odd-parity leaves share the same 3 coordinates; the union is 3, not 6.
  // Centre pins all coordinates to zero, contradicting either parity leaf.
  let overlapSAT=false;
  for(let mask=0;mask<8;mask++){
    const x=mask&1,y=(mask>>1)&1,z=(mask>>2)&1;
    if((x^y^z)===1 && x===0&&y===0&&z===0)overlapSAT=true;
  }
  if(overlapSAT)throw Error("overlap UNSAT control failed");
  return {
    allAssertionsPassed:true,
    status:"COMPUTATIONAL finite controls only",
    relationTables:relCount,
    binaryRelations2CNF:binaryRecognized,
    ternaryRelations2CNF:ternaryRecognized,
    exhaustiveStarCases:stars.length,
    totalStarAssignmentsVisited:stars.reduce((a,x)=>a+x.bruteChecks,0),
    matchedStarSAT:stars.filter(x=>x.expected).length,
    matchedStarUNSAT:stars.filter(x=>!x.expected).length,
    largestFullInterface:Math.max(...stars.map(x=>x.fullInterface)),
    largestBadUnion:Math.max(...stars.map(x=>x.unionBits)),
    overlappingBadLeaves:{sumWidths:6,unionWidth:3,answer:"UNSAT"},
    stars
  };
}
if(typeof module!=="undefined" && module.exports)module.exports={audit};
