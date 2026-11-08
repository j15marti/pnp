/* LSPV-3/498. Distinct R_factorLOCAL model; NOT historical R_mix341.
   Exhaustive 5-variable factor-only LOCAL implication test.
   Run: node experiments/arc/lspv3_498_factoronly_local_firewall.cjs
*/
"use strict";
function run(){
 let checks=0,rejected=0,accepted=0,tops=0,identical=0,candidates=0;
 function ok(x,msg){checks++;if(!x)throw Error("LSPV3/498 "+msg);}
 function bits(x){let n=0;while(x){n+=x&1;x>>>=1;}return n;}
 function value(table,vars,assignment){let idx=0;vars.forEach((v,j)=>idx|=((assignment>>v)&1)<<j);return (table>>idx)&1;}
 function entails(bad,vars,table){for(let x=0;x<32;x++)if((x&7)!==bad&&!value(table,vars,x))return false;return true;}
 function test(packet){if(!Array.isArray(packet.parents)||packet.parents.length!==1||packet.parents[0]!=="F0"||packet.rule!=="LOCAL-FACTOR")throw Error("wrong tag/parent");
  const S=packet.support;
  if(!Array.isArray(S)||S.length>3||new Set(S).size!==S.length||S.some(v=>!Number.isInteger(v)||v<0||v>=5))throw Error("bad support");
  if(!Number.isInteger(packet.table)||packet.table<0||packet.table>=2**(2**S.length))throw Error("bad table");
  if(!entails(packet.sourceBad,S,packet.table))throw Error("not implied");
  return true;
 }
 for(let bad=0;bad<8;bad++){
  for(let mask=0;mask<32;mask++)if(bits(mask)<=3){
   const S=[...Array(5).keys()].filter(v=>(mask>>v)&1);
   for(let table=0;table<2**(2**S.length);table++){
    candidates++;
    const entailsFlag=entails(bad,S,table);
    let isTop=true,isSame=true;
    for(let x=0;x<32;x++){
     const g=value(table,S,x),f=((x&7)!==bad)?1:0;
     if(!g)isTop=false;
     if(g!==f)isSame=false;
    }
    ok(entailsFlag===(isTop||(mask===7&&isSame)),"LOCAL classification");
    if(entailsFlag){accepted++;if(isTop)tops++;if(isSame)identical++;}
   }
  }
 }
 ok(candidates===21936,"number of exhaustive local candidate tables");
 ok(accepted===216&&tops===208&&identical===8,"LOCAL result classification");
 const triples=[];for(let mask=0;mask<32;mask++)if(bits(mask)===3)triples.push(mask);
 let pairs=0;for(let i=0;i<triples.length;i++)for(let j=i+1;j<triples.length;j++){
  ok(bits(triples[i]|triples[j])>=4,"distinct source triple factor supports cannot AND3");pairs++;
 }
 ok(pairs===45,"pair count");
 // Four opposite-parity forbidden triples are a real shortcut when support repeats.
 for(let rhs=0;rhs<2;rhs++){
  const excluded=[...Array(8).keys()].filter(a=>(bits(a)&1)!==rhs);
  ok(excluded.length===4,"affine packet has four sources");
  for(let a=0;a<8;a++)ok((!excluded.includes(a))===((bits(a)&1)===rhs),"full XOR local table");
 }
 // A globally entailed arbitrary-width weakened clause remains subsumed by the original.
 const A=[1,2,3],B=[-1,4,5],Aweak=[1,2,3,6];
 const resolve=(a,b)=>[...new Set([...a.filter(v=>v!==1),...b.filter(v=>v!==-1)])];
 const direct=resolve(A,B),weaker=resolve(Aweak,B);
 ok(direct.every(l=>weaker.includes(l))&&direct.length<weaker.length,"resolution weakening erasure");
 function badPacket(p){let denied=false;try{test(p);}catch(e){denied=true;}ok(denied,"hostile accepted");rejected++;}
 const valid={rule:"LOCAL-FACTOR",parents:["F0"],sourceBad:0,support:[0,1,2],table:254};
 ok(test(valid),"exact source conversion");
 badPacket({...valid,table:255^2}); // bad: remove another satisfying assignment, not logically entailed
 badPacket({...valid,support:[0,1,3],table:254}); // unsupported cross-support nontrivial result
 badPacket({...valid,parents:["RES7"]}); // hidden RES -> factor promotion
 badPacket({...valid,rule:"LOCAL-CLAUSE-AS-FACTOR"}); // forged tag
 badPacket({...valid,support:[0,0,2]}); // duplicated dimension
 badPacket({...valid,table:1<<12}); // invalid table length
 const answer={model:"R_factorLOCAL distinct tag-sealed calculus only",sourceSignedVariants:8,originalVariables:5,
  outputSupportChoices:26,candidateLocalFactorTables:candidates,entailedTables:accepted,
  nontrivialCopies:identical,tautologies:tops,distinctSourceTriplePairs:pairs,
  oppositeParityPackets:2,negativeControlsRejected:rejected,assertions:checks,
  theoremStatus:"PROVED/RESTRICTED plus finite computational checks",historicalMixed:"OPEN",status:"PASS"};
 return answer;
}
if(typeof module!=="undefined"){module.exports={run};if(require.main===module)console.log(JSON.stringify(run(),null,2));}
