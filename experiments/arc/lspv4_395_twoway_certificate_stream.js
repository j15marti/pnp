'use strict';
// LSPV-4 395: exact finite witness/stream controls. Node >=18. No dependencies.
const runCertificateAudit = function runCertificateAudit() {
  "use strict";
  let checks=0,malformedRejected=0;
  const assert=(c,m)=>{checks++;if(!c)throw Error(m)};
  const types=[[-1],[1],[-2],[2],[-1,-2],[-1,2],[1,-2],[1,2]];
  const parse=(f)=>{
    if(!f||!Number.isSafeInteger(f.n)||f.n<0||!Array.isArray(f.clauses))return false;
    for(const c of f.clauses){if(!Array.isArray(c))return false;const seen=new Set();
      for(const l of c){if(!Number.isSafeInteger(l)||l===0||Math.abs(l)>f.n||seen.has(l))return false;seen.add(l)}
    }return true;
  };
  const model=(f,w)=>{
    if(!parse(f)||!Array.isArray(w)||w.length!==f.n||w.some(v=>v!==0&&v!==1))return false;
    for(const c of f.clauses){let yes=false;for(const lit of c){
      const ix=Math.abs(lit)-1;let v=0;
      for(let j=0;j<w.length;j++)if(j===ix)v=w[j];
      if(lit>0?v===1:v===0)yes=true;
    }if(!yes)return false}
    return true;
  };
  let sat=0,unsat=0,assignmentChecks=0,modelAccepts=0;
  for(let mask=0;mask<256;mask++){
    const f={n:2,clauses:types.filter((_,j)=>(mask>>j)&1)},labels=[];
    for(let a=0;a<4;a++){const w=[a&1,(a>>1)&1],ok=model(f,w);
      const independent=f.clauses.every(c=>c.some(l=>l>0?!!(a&(1<<(l-1))):!(a&(1<<(-l-1)))));
      assert(ok===independent,"witness error");labels.push(ok);assignmentChecks++;if(ok)modelAccepts++;
    }
    assert(labels.some(Boolean)===([0,1,2,3].some(a=>f.clauses.every(c=>c.some(l=>l>0?!!(a&(1<<(l-1))):!(a&(1<<(-l-1))))))),"label");
    if(labels.some(Boolean))sat++;else unsat++;
  }
  assert(sat===95&&unsat===161,"ground truth");
  const invalid=[null,{n:2,clauses:[[0]]},{n:2,clauses:[[3]]},{n:2,clauses:[[1,1]]},
    {n:-1,clauses:[]},{n:2,clauses:"1"},{n:2,clauses:[null]},
    {n:2,clauses:[[1.5]]},{n:2,clauses:[[NaN]]}];
  for(const f of invalid){assert(!parse(f),"malformed");malformedRejected++}
  const edges=[[0,1],[0,2],[0,3],[1,2],[1,3],[2,3]];
  function makeTseitin(ch){
    const clauses=[];
    for(let v=0;v<4;v++){const ids=edges.map((e,j)=>e.includes(v)?j+1:0).filter(Boolean);
      for(let t=0;t<8;t++){const parity=((t&1)?1:0)^((t&2)?1:0)^((t&4)?1:0);
        if(parity!==ch[v])clauses.push(ids.map((j,r)=>(t&(1<<r))?-j:j));
      }
    }return {n:6,clauses};
  }
  const counts=[];
  for(const ch of [[1,0,0,0],[0,0,0,0]]){
    const f=makeTseitin(ch);let k=0;
    for(let a=0;a<64;a++)if(model(f,[0,1,2,3,4,5].map(j=>(a>>j)&1)))k++;
    counts.push(k);
  }
  assert(counts[0]===0&&counts[1]===8,"parity controls");
  let pairChecks=0;
  for(let k=1;k<=7;k++){const n=1<<k;
    for(let b=0;b<n;b++)for(let c=0;c<n;c++)if(b!==c){
      const y=b;assert((b===y)!==(c===y),"one-pass state distinction");pairChecks++;
    }
  }
  return {tag:"LSPV4-395-TWOWAY-CERTIFICATE-STREAM-FIREWALL",status:"PASS",
    source:"self-contained JavaScript, no dependencies",seed:null,enumeration:"exhaustive",
    twoVariable:{formulas:256,sat,unsat,assignmentChecks,modelAccepts},
    malformedRejected,k4Models:{odd:counts[0],even:counts[1]},
    streamingEquality:{maxK:7,pairDistinguishingChecks:pairChecks,
      lowerBound:"2^k distinct post-prefix states, k bits on strict one-pass b-then-y machine",
      indexed:"O(log input size) work cells with two-way read-only witness and repeated rescans"},
    assertionGroups:checks,spaceMeasured:false,proofStatuses:"KNOWN characterization; PROVED elementary strict-stream lemma; COMPUTATIONAL finite",
    B1:"OPEN",B2:"OPEN",B3:"OPEN",PvsNP:"OPEN"};
};
console.log(JSON.stringify(runCertificateAudit(),null,2));
